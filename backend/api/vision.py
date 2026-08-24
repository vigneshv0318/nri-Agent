import json
from typing import Optional, List, Dict, Any

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends,
)

from database.connection import get_db
from database import crud
from api.auth import get_current_user

from schemas.vision import (
    VisionAnalyzeResponse,
    LetterItem,
    WritingEvaluateResponse,
    HandwritingStatsResponse
)

from services.paddleocr_service import (
    extract_text_from_image
)

from services.gemini_service import (
    evaluate_handwriting_with_gemini
)

from writing_curriculum.curriculum_manager import (
    get_complete_curriculum,
    get_curriculum_item
)

from services.stroke_engine import (
    get_stroke_data
)

from services.handwriting_evaluator import (
    preprocess_handwriting_image,
    calculate_comprehensive_evaluation,
    normalize_indic_text
)

router = APIRouter()


# ============================================================
# TAMIL LETTERS
# ============================================================

TAMIL_LETTERS = [
    LetterItem(
        char="அ",
        transliteration="a",
        example_word="அம்மா (Amma)",
        meaning="Mother"
    ),
    LetterItem(
        char="ஆ",
        transliteration="aa",
        example_word="ஆடு (Aadu)",
        meaning="Goat"
    ),
    LetterItem(
        char="இ",
        transliteration="i",
        example_word="இலை (Ilai)",
        meaning="Leaf"
    ),
    LetterItem(
        char="ஈ",
        transliteration="ii",
        example_word="ஈட்டி (Eeti)",
        meaning="Spear"
    ),
    LetterItem(
        char="உ",
        transliteration="u",
        example_word="உரல் (Ural)",
        meaning="Mortar"
    ),
    LetterItem(
        char="ஊ",
        transliteration="uu",
        example_word="ஊஞ்சல் (Oonjal)",
        meaning="Swing"
    ),
    LetterItem(
        char="எ",
        transliteration="e",
        example_word="எலி (Eli)",
        meaning="Mouse"
    ),
    LetterItem(
        char="ஏ",
        transliteration="ee",
        example_word="ஏணி (Eani)",
        meaning="Ladder"
    ),
    LetterItem(
        char="ஐ",
        transliteration="ai",
        example_word="ஐந்து (Ainthu)",
        meaning="Five"
    ),
    LetterItem(
        char="ஒ",
        transliteration="o",
        example_word="ஒட்டகம் (Ottagam)",
        meaning="Camel"
    ),
    LetterItem(
        char="ஓ",
        transliteration="oo",
        example_word="ஓடம் (Odam)",
        meaning="Boat"
    ),
    LetterItem(
        char="ஔ",
        transliteration="au",
        example_word="ஔவையார் (Avvaiyar)",
        meaning="Poet"
    ),
    LetterItem(
        char="ஃ",
        transliteration="akku",
        example_word="எஃகு (Ehgu)",
        meaning="Steel"
    ),
    LetterItem(
        char="க",
        transliteration="ka",
        example_word="கண் (Kan)",
        meaning="Eye"
    ),
    LetterItem(
        char="ச",
        transliteration="sa",
        example_word="சக்கரம் (Sakkaram)",
        meaning="Wheel"
    ),
    LetterItem(
        char="த",
        transliteration="tha",
        example_word="தாமரை (Thamarai)",
        meaning="Lotus"
    ),
    LetterItem(
        char="ப",
        transliteration="pa",
        example_word="பட்டம் (Pattam)",
        meaning="Kite"
    ),
    LetterItem(
        char="ம",
        transliteration="ma",
        example_word="மரம் (Maram)",
        meaning="Tree"
    ),
    LetterItem(
        char="வ",
        transliteration="va",
        example_word="வண்டு (Vandu)",
        meaning="Beetle"
    ),
]


# ============================================================
# TELUGU LETTERS
# ============================================================

TELUGU_LETTERS = [
    LetterItem(
        char="అ",
        transliteration="a",
        example_word="అమ్మ (Amma)",
        meaning="Mother"
    ),
    LetterItem(
        char="ఆ",
        transliteration="aa",
        example_word="ఆవు (Aavu)",
        meaning="Cow"
    ),
    LetterItem(
        char="ఇ",
        transliteration="i",
        example_word="ఇల్లు (Illu)",
        meaning="House"
    ),
    LetterItem(
        char="ఈ",
        transliteration="ii",
        example_word="ఈగ (Eega)",
        meaning="Housefly"
    ),
    LetterItem(
        char="ఉ",
        transliteration="u",
        example_word="ఉడుత (Udutha)",
        meaning="Squirrel"
    ),
    LetterItem(
        char="ఊ",
        transliteration="uu",
        example_word="ఊయల (Ooyala)",
        meaning="Cradle"
    ),
    LetterItem(
        char="ఎ",
        transliteration="e",
        example_word="ఎలుక (Eluka)",
        meaning="Rat"
    ),
    LetterItem(
        char="ఏ",
        transliteration="ee",
        example_word="ఏనుగు (Eenugu)",
        meaning="Elephant"
    ),
    LetterItem(
        char="క",
        transliteration="ka",
        example_word="కలము (Kalamu)",
        meaning="Pen"
    ),
    LetterItem(
        char="గ",
        transliteration="ga",
        example_word="గడప (Gadap)",
        meaning="Threshold"
    ),
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize Unicode text for reliable Tamil/Telugu comparison.

    Removes:
    - leading/trailing spaces
    - internal whitespace
    - Unicode representation differences
    """

    if not text:
        return ""

    text = unicodedata.normalize("NFC", str(text))

    # Remove whitespace
    text = "".join(text.split())

    return text.strip()


def contains_indic_script(text: str) -> bool:
    """
    Check whether text contains Tamil or Telugu characters.
    """

    for char in text:

        code = ord(char)

        # Tamil
        if 0x0B80 <= code <= 0x0BFF:
            return True

        # Telugu
        if 0x0C00 <= code <= 0x0C7F:
            return True

    return False


def is_ascii_text(text: str) -> bool:
    """
    Check whether OCR returned ASCII characters.

    Example:
        'a'
        'A'
        'b'
    """

    if not text:
        return False

    return all(ord(char) < 128 for char in text)


def determine_recognition_status(
    target: str,
    detected: str,
    confidence: float
) -> str:
    """
    Decide whether the handwriting is:

    CORRECT
    INCORRECT
    UNCERTAIN

    IMPORTANT:
    Gemini is NOT used for this decision.
    """

    target = normalize_text(target)
    detected = normalize_text(detected)

    # No target -> cannot reliably evaluate
    if not target:
        return "UNCERTAIN"

    # No OCR result
    if not detected:
        return "UNCERTAIN"

    # Low OCR confidence
    if confidence < 0.65:
        return "UNCERTAIN"

    # Exact match
    if detected == target:
        return "CORRECT"

    # --------------------------------------------------------
    # IMPORTANT:
    # If PaddleOCR turns Tamil/Telugu into English ASCII,
    # don't immediately tell the child they wrote English.
    #
    # This is most likely an OCR recognition uncertainty.
    # --------------------------------------------------------

    if is_ascii_text(detected) and not is_ascii_text(target):
        return "UNCERTAIN"

    # Another Indian-script character was confidently detected
    if contains_indic_script(detected):
        return "INCORRECT"

    # Anything else is uncertain
    return "UNCERTAIN"


def get_score_for_status(status: str) -> int:

    if status == "CORRECT":
        return 92

    if status == "INCORRECT":
        return 30

    return 0


def get_points_for_status(status: str) -> int:

    if status == "CORRECT":
        return 15

    if status == "INCORRECT":
        return 5

    # No points for uncertain recognition
    return 0


# ============================================================
# GET LETTERS
# ============================================================

@router.get(
    "/letters",
    response_model=List[LetterItem]
)
def get_letters(language: str = "Tamil"):
    items = get_complete_curriculum(language)
    res = []
    for item in items:
        s_data = get_stroke_data(item["char"], language)
        res.append(LetterItem(**{**item, **s_data}))
    return res


@router.get(
    "/lessons",
    response_model=List[LetterItem]
)
def get_writing_lessons(language: str = "Tamil", category: Optional[str] = None, level: Optional[int] = None):
    items = get_complete_curriculum(language, category=category, level=level)
    res = []
    for item in items:
        s_data = get_stroke_data(item["char"], language)
        res.append(LetterItem(**{**item, **s_data}))
    return res


@router.get(
    "/curriculum"
)
def get_writing_curriculum(language: str = "Tamil", category: Optional[str] = None, level: Optional[int] = None):
    items = get_complete_curriculum(language, category=category, level=level)
    res = []
    for item in items:
        s_data = get_stroke_data(item["char"], language)
        res.append({**item, **s_data})
    return res


@router.get(
    "/stats",
    response_model=HandwritingStatsResponse
)
def get_writing_stats(
    current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    stats = crud.get_user_handwriting_stats(db, current_user.id)
    return HandwritingStatsResponse(**stats)


@router.post(
    "/evaluate",
    response_model=WritingEvaluateResponse
)
def evaluate_handwriting_canvas(
    file: UploadFile = File(...),
    target_text: str = Form("அ"),
    practice_mode: str = Form("trace"),
    language: str = Form("Tamil"),
    attempt_number: int = Form(1),
    strokes_json: Optional[str] = Form(None),
    current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    import tempfile, os
    input_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(file.file.read())
            input_path = tmp.name

        canvas_strokes = None
        if strokes_json:
            try:
                canvas_strokes = json.loads(strokes_json)
            except Exception:
                pass

        image_metrics = preprocess_handwriting_image(input_path)

        ocr_text = ""
        ocr_confidence = 0.0
        # Fast path: If stroke vector data is present, evaluate stroke geometry directly for sub-50ms latency.
        # Only invoke heavy CPU PaddleOCR inference for notebook photo uploads without stroke vectors.
        if (not canvas_strokes or len(canvas_strokes) == 0) and image_metrics.get("has_ink", False):
            try:
                ocr_res = extract_text_from_image(input_path, language=language)
                ocr_text = ocr_res.get("text", "")
                ocr_confidence = float(ocr_res.get("confidence", 0.0))
            except Exception as e:
                print(f"[EVALUATE] OCR fallback note: {e}")

        eval_res = calculate_comprehensive_evaluation(
            target_char=target_text,
            ocr_text=ocr_text,
            ocr_confidence=ocr_confidence,
            practice_mode=practice_mode,
            image_metrics=image_metrics,
            canvas_strokes=canvas_strokes,
            language=language
        )

        points_to_award = 0
        if eval_res["is_correct"]:
            points_to_award = 20 if attempt_number == 1 else 15
        elif eval_res["overall_score"] >= 60:
            points_to_award = 10
        else:
            points_to_award = 5

        updated = crud.update_user_points_and_stamp(
            db=db,
            username=current_user.username,
            points_to_add=points_to_award
        )

        activity_title = f"Handwriting: {target_text}"
        crud.log_learning_progress(
            db=db,
            user_id=current_user.id,
            module="writing",
            activity=activity_title,
            score=eval_res["overall_score"],
            language=language
        )

        session_meta = {
            "target": target_text,
            "language": language,
            "mode": practice_mode,
            "attempt": attempt_number,
            "overall_score": eval_res["overall_score"],
            "recognition_confidence": ocr_confidence,
            "shape_score": eval_res["shape_score"],
            "stroke_score": eval_res["stroke_score"],
            "alignment_score": eval_res["alignment_score"],
            "feedback_type": eval_res["feedback_type"]
        }
        crud.log_learning_session(
            db=db,
            user_id=current_user.id,
            module="writing",
            score=eval_res["overall_score"],
            session_metadata=session_meta
        )

        return WritingEvaluateResponse(
            target=target_text,
            detected=eval_res["detected"],
            is_correct=eval_res["is_correct"],
            overall_score=eval_res["overall_score"],
            character_score=eval_res["character_score"],
            shape_score=eval_res["shape_score"],
            stroke_score=eval_res["stroke_score"],
            alignment_score=eval_res["alignment_score"],
            recognition_status=eval_res["recognition_status"],
            feedback_type=eval_res["feedback_type"],
            specific_feedback=eval_res["specific_feedback"],
            mistake_explanation=eval_res["mistake_explanation"],
            encouragement=eval_res["encouragement"],
            stroke_animation=eval_res["stroke_animation"],
            attempt_number=attempt_number,
            mastered=(eval_res["overall_score"] >= 85),
            points_awarded=points_to_award,
            total_points=updated["points"]
        )
    finally:
        if input_path and os.path.exists(input_path):
            try:
                os.remove(input_path)
            except Exception:
                pass


# ============================================================
# ANALYZE HANDWRITING
# ============================================================

@router.post(
    "/analyze",
    response_model=VisionAnalyzeResponse
)
def analyze_handwriting(

    file: UploadFile = File(...),

    target_char: Optional[str] = Form(None),

    mode: str = Form("general"),

    language: str = Form("Tamil"),

    current_user=Depends(get_current_user),

    db=Depends(get_db)
):

    """
    Analyze child handwriting.

    Pipeline:

        Image
          ↓
        PaddleOCR
          ↓
        OCR text + confidence
          ↓
        Target-aware recognition
          ↓
        CORRECT / INCORRECT / UNCERTAIN
          ↓
        Gemini feedback generation
          ↓
        PostgreSQL progress update
    """

    is_video = (
        file.content_type
        and file.content_type.startswith("video")
    )

    suffix = ".mp4" if is_video else ".png"

    input_path = None
    frame_path = None

    try:

        # ====================================================
        # SAVE UPLOADED FILE
        # ====================================================

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as tmp:

            tmp.write(file.file.read())

            input_path = tmp.name

        frame_path = input_path

        # ====================================================
        # VIDEO → FRAME
        # ====================================================

        if is_video:

            cap = cv2.VideoCapture(input_path)

            total_frames = int(
                cap.get(cv2.CAP_PROP_FRAME_COUNT)
            )

            middle_frame = max(
                0,
                total_frames // 2
            )

            cap.set(
                cv2.CAP_PROP_POS_FRAMES,
                middle_frame
            )

            ret, frame = cap.read()

            cap.release()

            if not ret:

                raise ValueError(
                    "Could not extract a frame from the video."
                )

            frame_path = (
                input_path + "_frame.png"
            )

            cv2.imwrite(
                frame_path,
                frame
            )

        # ====================================================
        # 1. PADDLEOCR
        # ====================================================

        ocr_result = extract_text_from_image(
            frame_path,
            language=language
        )

        ocr_text = normalize_text(
            ocr_result.get("text", "")
        )

        ocr_confidence = float(
            ocr_result.get("confidence", 0.0)
        )

        ocr_engine = ocr_result.get(
            "engine",
            "unknown"
        )

        print(
            f"[VISION] OCR engine: {ocr_engine}"
        )

        print(
            f"[VISION] OCR text: '{ocr_text}'"
        )

        print(
            f"[VISION] OCR confidence: "
            f"{ocr_confidence:.3f}"
        )

        # ====================================================
        # 2. TARGET-AWARE DECISION
        # ====================================================

        target = normalize_text(
            target_char or ""
        )

        recognition_status = (
            determine_recognition_status(
                target=target,
                detected=ocr_text,
                confidence=ocr_confidence
            )
        )

        print(
            f"[VISION] Target: '{target}'"
        )

        print(
            f"[VISION] Recognition status: "
            f"{recognition_status}"
        )

        # ====================================================
        # 3. SCORE IS DECIDED BY BACKEND
        # ====================================================

        score = get_score_for_status(
            recognition_status
        )

        points_to_award = get_points_for_status(
            recognition_status
        )

        is_correct = (
            recognition_status == "CORRECT"
        )

        # ====================================================
        # 4. GEMINI GENERATES FEEDBACK ONLY
        # ====================================================

        gemini_result = (
            evaluate_handwriting_with_gemini(
                image_path=frame_path,
                target_text=target_char,
                ocr_hint=ocr_text,
                ocr_confidence=ocr_confidence,
                recognition_status=recognition_status,
                language=language,
                mode=mode
            )
        )

        # ====================================================
        # 5. DETECTED TEXT
        # ====================================================

        if ocr_text:

            detected_text = ocr_text

        elif recognition_status == "UNCERTAIN":

            detected_text = "Unclear Writing"

        else:

            detected_text = (
                target_char or "Letter"
            )

        # ====================================================
        # 6. FEEDBACK
        # ====================================================

        feedback = gemini_result.get(
            "feedback"
        )

        if not feedback:

            if recognition_status == "CORRECT":

                feedback = (
                    f"Sabash Kanna! "
                    f"You wrote '{target_char}' "
                    f"beautifully!"
                )

            elif recognition_status == "INCORRECT":

                feedback = (
                    f"Good try, Kanna! "
                    f"Let's practice '{target_char}' "
                    f"once more."
                )

            else:

                feedback = (
                    f"Kanna, I couldn't clearly "
                    f"recognize the writing. "
                    f"Please take a clearer photo "
                    f"and try again."
                )

        # ====================================================
        # 7. MISTAKE EXPLANATION
        # ====================================================

        mistake = gemini_result.get(
            "mistake_explanation",
            ""
        )

        if recognition_status == "UNCERTAIN":

            mistake = (
                "The handwriting could not be "
                "recognized confidently. "
                "Please try again with a clearer "
                "image and better lighting."
            )

        # ====================================================
        # 8. DATABASE
        # ====================================================

        activity_title = (
            f"Handwriting: {target_char}"
            if target_char
            else f"Handwriting ({mode})"
        )

        crud.log_learning_progress(
            db=db,
            user_id=current_user.id,
            module="writing",
            activity=activity_title,
            score=score,
            language=language
        )

        # Only update points when there is a real result
        updated = crud.update_user_points_and_stamp(
    db=db,
    username=current_user.username,
    points_to_add=points_to_award
)


        # ====================================================
        # 9. RESPONSE
        # ====================================================

        return VisionAnalyzeResponse(

            detected_text=detected_text,

            feedback=feedback,

            is_correct=is_correct,

            score=score,

            recognition_status=recognition_status,

            expected_text=target_char,

            mistake_explanation=mistake,

            points_awarded=points_to_award,

            total_points=updated["points"]
        )

    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        import traceback

        traceback.print_exc()

        return VisionAnalyzeResponse(

            detected_text="Unclear Writing",

            feedback=(
                "Aiyayo Kanna! "
                "I couldn't analyze the image properly. "
                "Please make sure the notebook is clearly "
                "visible and try again."
            ),

            is_correct=False,

            score=0,

            recognition_status="UNCERTAIN",

            expected_text=target_char,

            mistake_explanation=(
                "Image processing failed. "
                "Please try again with good lighting."
            ),

            points_awarded=0,

            total_points=current_user.points or 0
        )

    # ========================================================
    # CLEANUP
    # ========================================================

    finally:

        paths_to_remove = []

        if input_path:
            paths_to_remove.append(input_path)

        if frame_path and frame_path != input_path:
            paths_to_remove.append(frame_path)

        for path in paths_to_remove:

            if os.path.exists(path):

                try:
                    os.remove(path)

                except Exception:
                    pass