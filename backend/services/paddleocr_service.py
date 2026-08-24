import cv2
import numpy as np
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger("ammachi.paddleocr")

_ocr_instances: Dict[str, Any] = {}


def get_ocr_engine(lang: str = "ta"):
    """
    Create and cache a Tamil/Telugu PaddleOCR engine.

    PaddleOCR PP-OCRv5 provides dedicated Tamil and Telugu
    recognition models.
    """

    if lang in _ocr_instances:
        return _ocr_instances[lang]

    try:
        from paddleocr import PaddleOCR

        if lang == "ta":
            language = "ta"
        elif lang == "te":
            language = "te"
        else:
            language = "ta"

        logger.info("Initializing PaddleOCR language=%s", language)

        ocr = PaddleOCR(
            lang=language,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            engine="paddle"
        )

        _ocr_instances[lang] = ocr

        return ocr

    except Exception as e:
        logger.exception("Failed to initialize PaddleOCR: %s", e)
        return None


def preprocess_image_for_ocr(image_path: str) -> Optional[np.ndarray]:
    """
    Prepare notebook image for OCR.
    """

    try:
        img = cv2.imread(image_path)

        if img is None:
            return None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        h, w = gray.shape[:2]

        # Upscale small images
        if max(h, w) < 1200:
            scale = 1200 / max(h, w)

            gray = cv2.resize(
                gray,
                None,
                fx=scale,
                fy=scale,
                interpolation=cv2.INTER_CUBIC
            )

        # Reduce camera noise
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        # Improve contrast
        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        enhanced = clahe.apply(gray)

        # Convert back to 3-channel image
        processed = cv2.cvtColor(
            enhanced,
            cv2.COLOR_GRAY2BGR
        )

        return processed

    except Exception as e:
        logger.exception("Image preprocessing failed: %s", e)
        return None


def extract_text_from_image(
    image_path: str,
    language: str = "Tamil"
) -> Dict[str, Any]:

    language_map = {
        "tamil": "ta",
        "telugu": "te"
    }

    lang_code = language_map.get(
        language.lower(),
        "ta"
    )

    ocr = get_ocr_engine(lang_code)

    if ocr is None:
        return {
            "success": False,
            "text": "",
            "confidence": 0.0,
            "engine": "none"
        }

    try:

        processed = preprocess_image_for_ocr(image_path)

        image = (
            processed
            if processed is not None
            else image_path
        )

        results = ocr.predict(image)

        texts = []
        confidences = []

        for result in results:

            # PaddleOCR 3.x result object
            data = result.json

            if callable(data):
                data = data()

            if isinstance(data, str):
                import json
                data = json.loads(data)

            res = data.get("res", data)

            rec_texts = res.get("rec_texts", [])
            rec_scores = res.get("rec_scores", [])

            for text, score in zip(
                rec_texts,
                rec_scores
            ):

                text = str(text).strip()

                if not text:
                    continue

                texts.append(text)
                confidences.append(float(score))

        if not texts:

            return {
                "success": False,
                "text": "",
                "confidence": 0.0,
                "engine": "PaddleOCR-PP-OCRv5"
            }

        full_text = "".join(texts)

        confidence = float(
            np.mean(confidences)
        )

        logger.info(
            "PaddleOCR result='%s' confidence=%.3f",
            full_text,
            confidence
        )

        return {
            "success": True,
            "text": full_text,
            "confidence": confidence,
            "engine": "PaddleOCR-PP-OCRv5"
        }

    except Exception as e:

        logger.exception(
            "PaddleOCR inference failed: %s",
            e
        )

        return {
            "success": False,
            "text": "",
            "confidence": 0.0,
            "engine": "PaddleOCR-error"
        }