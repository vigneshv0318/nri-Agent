from fastapi import APIRouter, UploadFile, File, Form
from models import VisionResponse
import cv2
import numpy as np
import mediapipe as mp
from PIL import Image
import tempfile
import os
import base64
import pytesseract

from langchain_groq import ChatGroq
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()

# Configure Tesseract path if provided in .env (common for Windows)
tesseract_cmd = os.getenv("TESSERACT_PATH")
if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

# -------------------- MediaPipe Hands --------------------
mp_hands = None
hands = None
try:
    import mediapipe.python.solutions.hands as mp_hands_module
    mp_hands = mp_hands_module
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5
    )
    print("MediaPipe Hands loaded.")
except Exception as e:
    print(f"MediaPipe disabled: {e}")
    hands = None


# -------------------- Stroke Extraction --------------------
def extract_stroke_path(video_path):
    if hands is None:
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        cap.release()
        if ret:
            return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return Image.new("RGB", (640, 480), "black")

    cap = cv2.VideoCapture(video_path)
    points = []

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            lm = results.multi_hand_landmarks[0].landmark[8]
            cx, cy = int(lm.x * width), int(lm.y * height)
            points.append((cx, cy))

    cap.release()

    if len(points) > 1:
        for i in range(1, len(points)):
            cv2.line(canvas, points[i-1], points[i], (255, 255, 255), 2)

    return Image.fromarray(canvas)


# -------------------- OCR Preprocessing --------------------
def preprocess_for_ocr(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None: return None
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.adaptiveThreshold(
        img, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 2
    )
    return img


def run_tesseract(image_path):
    try:
        img = preprocess_for_ocr(image_path)
        if img is None: return "Error: Could not read image."
        text = pytesseract.image_to_string(
            img,
            lang="tam+eng",
            config="--psm 6"
        )
        return text.strip()
    except Exception as e:
        return f"Tesseract error: {str(e)}"


# -------------------- API --------------------
@router.post("/analyze", response_model=VisionResponse)
def analyze_video(
    file: UploadFile = File(...),
    target_char: str = Form(None),
    mode: str = Form("trace")
):
    print(f"Received upload: {file.filename}, Mode: {mode}")
    
    is_video = file.content_type.startswith("video")
    suffix = ".mp4" if is_video else ".png"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file.file.read())
        file_path = tmp.name

    try:
        image_path = file_path

        # -------- TRACE MODE --------
        if mode == "trace":
            if is_video:
                stroke_img = extract_stroke_path(file_path)
                image_path = file_path + "_stroke.png"
                stroke_img.save(image_path)

            system_prompt = f"Analyze this stroke path image of the Tamil letter '{target_char}'. Give warm Ammachi-style guidance if the stroke start or direction is wrong."

        # -------- GENERAL MODE --------
        else:
            if is_video:
                cap = cv2.VideoCapture(file_path)
                total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                cap.set(cv2.CAP_PROP_POS_FRAMES, total // 2)
                ret, frame = cap.read()
                cap.release()

                if ret:
                    image_path = file_path + "_frame.png"
                    cv2.imwrite(image_path, frame)

            # --- Tesseract Hybrid Flow ---
            ocr_text = run_tesseract(image_path)
            print(f"Tesseract OCR: {ocr_text}")

            system_prompt = f"""You are Ammachi, a warm Tamil grandmother teacher. 
A local OCR tool (Tesseract) extracted this text: "{ocr_text}".

Based on the image provided and this OCR hint:
1. Transcribe the Tamil text correctly.
2. Correct any spelling or grammar mistakes.
3. Provide warm, encouraging feedback in a mix of Tamil and English.
Keep your response short and motherly."""

        # -------- LLM ANALYSIS --------
        with open(image_path, "rb") as f:
            img_str = base64.b64encode(f.read()).decode()

        chat = ChatGroq(
            model_name="meta-llama/llama-4-scout-17b-16e-instruct",
            api_key=os.environ.get("GROQ_API_KEY")
        )

        msg = chat.invoke([
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": system_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}}
                ]
            }
        ])

        return VisionResponse(
            detected_text=f"Handwriting analysis ({mode})",
            feedback=msg.content,
            is_correct=True
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return VisionResponse(
            detected_text="Error",
            feedback=f"Aiyayo! My eyes are a bit blurry: {str(e)}",
            is_correct=False
        )

    finally:
        for p in [file_path, file_path + "_stroke.png", file_path + "_frame.png"]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except:
                    pass
