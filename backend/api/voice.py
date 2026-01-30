from fastapi import APIRouter, UploadFile, File, Form
from models import VoiceResponse
import os
import tempfile
from langchain_groq import ChatGroq

router = APIRouter()

@router.post("/analyze", response_model=VoiceResponse)
def analyze_voice(file: UploadFile = File(...)):
    print(f"Received audio upload: {file.filename}")
    
    # 1. Save Audio Temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(file.file.read()) # No await in def
        audio_path = tmp.name
        
    try:
        from groq import Groq
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        # 2. Transcribe with Groq Whisper (Literal Transcription)
        print("Transcribing with Whisper...")
        with open(audio_path, "rb") as f:
            transcription = client.audio.transcriptions.create(
                file=(audio_path, f.read()),
                model="whisper-large-v3",
                response_format="text",
                language="ta" # Tamil audio expected? Or mixed. Let's try auto or set to 'ta' if we know it's Tamil context. 
                # User said "Native Language Tutor", safe to assume Tamil primarily but children migh speak Tanglish.
                # "whisper-large-v3" is good at auto-detect. Let's not force 'ta' to allow Tanglish.
            )
        raw_text = str(transcription).strip()
        print(f"Raw Transcription: {raw_text}")

        # 3. Patience Agent (Denoise Stutters)
        # Using a fast model for text processing
        chat = ChatGroq(model_name="llama-3.3-70b-versatile", api_key=os.environ.get("GROQ_API_KEY"))
        
        patience_prompt = f"""You are an expert Speech-to-Text polisher for children. 
Task: Clean the text to find the child's intended meaning.
Input: "{raw_text}"

Rules:
- Remove repeated words (stutters) like "A... A... Amma".
- Remove filler words (um, uh).
- Fix minor phonetic misinterpretations if obvious in context of a child speaking Tamil/English.
- OUTPUT ONLY THE CLEANED TEXT. No explanation."""

        msg = chat.invoke(patience_prompt)
        cleaned_text = msg.content.strip()
        print(f"Cleaned Text: {cleaned_text}")

        # 4. Ammachi's Conversational Reply
        conversation_prompt = f"""You are Ammachi, a warm and loving Tamil grandmother. 
The child said to you: "{cleaned_text}"
(Raw recording had: "{raw_text}")

Your Goal: Have a frindly enthusiastic conversation with the child and guide them to learn Tamil. 
- **Reply relevantly** to what they said in a mix of Tamil and English (Tanglish).
- **Subtle Correction**: If they made a grammar mistake, repeat their sentence back to them CORRECTLY as part of your reply (recasting).
- **Encourage**: Use terms like "Kanna", "Chellam", "Sabash".
- **Keep it short**: One or two sentences max.
- **CRITICAL**: DO NOT use any jourgons and difficult words and special characters like asterisks (**), dashes, or extra colon marks. Use only simple Tamil and English words with basic punctuation (full stops and commas).
- **Do NOT** specifically say "Your pronunciation was good". Just talk to them!
"""
        feedback_msg = chat.invoke(conversation_prompt)

        return VoiceResponse(
            transcription=cleaned_text,
            feedback=feedback_msg.content  # The 'feedback' field now acts as the conversational reply
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return VoiceResponse(
            transcription="Error processing audio",
            feedback=f"Aiyayo! My ears are not working properly. (Error: {str(e)})"
        )
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

def clean_text_for_speech(text: str) -> str:
    """
    Removes markdown symbols and other characters that TTS engines shouldn't speak literally.
    """
    import re
    # Remove markdown bold/italic
    text = re.sub(r'[\*_]{1,3}', '', text)
    # Remove extra colons if they appear as part of a list or header (like "Correction: ...")
    # But keep them if they are part of a sentence? Actually TTS shouldn't say "colon".
    # ElevenLabs usually handles them, but let's be safe.
    text = text.replace(':', '.') 
    # Remove other common symbols
    text = text.replace('#', '')
    text = text.replace('-', ' ')
    # Ensure commas are just commas (TTS should pause, not say "comma")
    # If the user says it says "coma", it might be some weird unicode comma?
    
    return text.strip()

@router.post("/speak")
def text_to_speech(text: str = Form(...)):
    """
    Generates audio for the given text.
    Prioritizes gTTS for Tamil text (better native support), Eleven Labs for English/Tanglish.
    """
    try:
        from fastapi.responses import StreamingResponse
        import io
        
        # Clean the text before sending to any TTS
        text = clean_text_for_speech(text)
        print(f"Cleaned Text for TTS: {text}")

        # Check if text contains Tamil characters
        def is_tamil(t):
            return any('\u0B80' <= c <= '\u0BFF' for c in t)

        if is_tamil(text):
            print(f"Tamil detected. Switching to gTTS.")
            from gtts import gTTS
            
            # Generate gTTS audio in memory
            tts = gTTS(text=text, lang='ta', slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            return StreamingResponse(fp, media_type="audio/mpeg")

        # Else try Eleven Labs for Tanglish/English
        try:
            from elevenlabs.client import ElevenLabs
            
            api_key = os.environ.get("ELEVEN_LABS_API") or os.environ.get("ELEVENLABS_API_KEY")
            if not api_key:
                 raise ValueError("ELEVEN_LABS_API key missing.")
            
            client = ElevenLabs(api_key=api_key)
            # Default to "Dorothy" (ThT5KcBeYPX3keUQqHPh) - deeply older Indian female, serves as good "Grandma" fallback
            voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "ThT5KcBeYPX3keUQqHPh") 
            
            print(f"Generating Eleven Labs TTS for: {text[:50]}...")
            audio_stream = client.generate(
                text=text,
                voice=voice_id,
                model="eleven_multilingual_v2"
            )
            
            def iterfile():
                for chunk in audio_stream:
                    yield chunk
                    
            return StreamingResponse(iterfile(), media_type="audio/mpeg")

        except Exception as e_eleven:
            print(f"Eleven Labs Failed: {e_eleven}. Falling back to gTTS (English/Auto).")
            # Fallback to gTTS if Eleven Labs fails
            from gtts import gTTS
            tts = gTTS(text=text, lang='en', slow=False) # Default to En for fallback
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return StreamingResponse(fp, media_type="audio/mpeg")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"TTS Critical Error: {e}")
        return {"error": str(e)}