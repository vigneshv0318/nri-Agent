"""
Generic Multi-Signal Handwriting Evaluation Engine for Ammachi AI.
Supports any character, word, or sentence without hardcoding.

Evaluates:
1. Normalized Stroke Trajectory Geometry (Point distance, stroke count, slopes)
2. Shape Similarity & Bounding Box Proportion
3. Alignment, Centering & Size
4. Auxiliary PaddleOCR Recognition & Gemini Tutoring Synthesis
"""

import os
import cv2
import numpy as np
import unicodedata
from typing import Dict, Any, List, Optional
from services.stroke_engine import get_stroke_data

def normalize_indic_text(text: str) -> str:
    if not text:
        return ""
    text = unicodedata.normalize("NFC", str(text))
    return "".join(text.split()).strip()

def resample_points(points: List[Dict[str, float]], num_samples: int = 30) -> List[Dict[str, float]]:
    """
    Resample a list of stroke points [{x, y}] to a uniform count across trajectory.
    """
    if not points:
        return []
    if len(points) == 1:
        return [points[0]] * num_samples

    # Compute path lengths
    dists = [0.0]
    for i in range(1, len(points)):
        d = np.hypot(points[i]['x'] - points[i-1]['x'], points[i]['y'] - points[i-1]['y'])
        dists.append(dists[-1] + d)

    total_dist = dists[-1]
    if total_dist == 0:
        return [points[0]] * num_samples

    step = total_dist / (num_samples - 1)
    resampled = [points[0]]

    curr_idx = 0
    for s in range(1, num_samples - 1):
        target_d = s * step
        while curr_idx < len(dists) - 1 and dists[curr_idx + 1] < target_d:
            curr_idx += 1
        
        t0_d = dists[curr_idx]
        t1_d = dists[curr_idx + 1]
        denom = (t1_d - t0_d) if (t1_d - t0_d) > 0 else 1.0
        ratio = (target_d - t0_d) / denom

        p0 = points[curr_idx]
        p1 = points[curr_idx + 1]
        resampled.append({
            'x': float(p0['x'] + ratio * (p1['x'] - p0['x'])),
            'y': float(p0['y'] + ratio * (p1['y'] - p0['y']))
        })

    resampled.append(points[-1])
    return resampled

def preprocess_handwriting_image(image_path: str) -> Dict[str, Any]:
    """
    Grayscale, Otsu thresholding, contour extraction, bounding box, aspect ratio.
    """
    if not os.path.exists(image_path):
        return {"valid": False, "error": "Image file not found"}

    img = cv2.imread(image_path)
    if img is None:
        return {"valid": False, "error": "Could not decode image"}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    min_area = (img.shape[0] * img.shape[1]) * 0.0005
    valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]

    if not valid_contours:
        return {
            "valid": True,
            "has_ink": False,
            "stroke_count": 0,
            "aspect_ratio": 1.0,
            "coverage": 0.0,
            "bounding_box": (0, 0, 0, 0)
        }

    all_points = np.vstack(valid_contours)
    x, y, w, h = cv2.boundingRect(all_points)

    total_ink_area = sum(cv2.contourArea(c) for c in valid_contours)
    bbox_area = max(1, w * h)
    coverage = float(total_ink_area / bbox_area)
    aspect_ratio = float(w / h) if h > 0 else 1.0

    return {
        "valid": True,
        "has_ink": True,
        "stroke_count": len(valid_contours),
        "aspect_ratio": aspect_ratio,
        "coverage": coverage,
        "bounding_box": (x, y, w, h),
        "img_shape": img.shape
    }

def evaluate_normalized_strokes(
    user_strokes: List[List[Dict[str, float]]],
    target_data: Dict[str, Any],
    image_metrics: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Compares user stroke trajectories [{x,y}] against target stroke points.
    Calculates measurement-based shape, stroke, alignment, and size scores.
    """
    issues = []
    
    if not user_strokes or len(user_strokes) == 0:
        return {
            "shape_score": 0,
            "stroke_score": 0,
            "alignment_score": 0,
            "size_score": 0,
            "issues": ["No strokes detected in writing box."]
        }

    detected_stroke_count = len(user_strokes)
    target_stroke_count = target_data.get("stroke_count", 3)

    # 1. Stroke Count Score
    stroke_diff = abs(detected_stroke_count - target_stroke_count)
    stroke_score = max(40, 100 - (stroke_diff * 18))
    if stroke_diff > 0:
        if detected_stroke_count < target_stroke_count:
            issues.append(f"Missing {stroke_diff} stroke(s) compared to standard formation.")
        else:
            issues.append(f"Contains {stroke_diff} extra stroke(s).")

    # 2. Shape Similarity (Resampled point distance & slope direction)
    target_points = target_data.get("points", [])
    has_target_points = target_data.get("stroke_data_available", False) and len(target_points) > 0

    if has_target_points:
        # Compare resampled points
        point_distances = []
        for i, u_stroke in enumerate(user_strokes):
            ref_stroke = target_points[min(i, len(target_points) - 1)]
            u_res = resample_points(u_stroke, 20)
            r_res = resample_points(ref_stroke, 20)

            for p_u, p_r in zip(u_res, r_res):
                d = np.hypot(p_u['x'] - p_r['x'], p_u['y'] - p_r['y'])
                point_distances.append(d)

        avg_dist = float(np.mean(point_distances)) if point_distances else 20.0
        shape_score = max(40, int(100 - (avg_dist * 1.4)))
        if avg_dist > 25.0:
            issues.append("Stroke curves differ from target trajectory.")
    else:
        # Fallback to contour aspect ratio & ink density
        aspect_ratio = image_metrics.get("aspect_ratio", 1.0)
        aspect_diff = abs(aspect_ratio - 1.0)
        shape_score = max(50, int(100 - (aspect_diff * 35)))

    # 3. Size & Proportion Score
    all_user_pts = [pt for stroke in user_strokes for pt in stroke]
    if all_user_pts:
        xs = [p['x'] for p in all_user_pts]
        ys = [p['y'] for p in all_user_pts]
        user_w = max(xs) - min(xs)
        user_h = max(ys) - min(ys)
        box_coverage = (user_w * user_h) / (100 * 100) if 100 > 0 else 0.5
        
        if box_coverage < 0.15:
            size_score = 60
            issues.append("Writing is very small. Try using more of the writing area.")
        elif box_coverage > 0.85:
            size_score = 75
            issues.append("Writing is very large and close to edges.")
        else:
            size_score = 95
    else:
        size_score = 80

    # 4. Alignment & Centering Score
    if all_user_pts:
        center_x = (min(xs) + max(xs)) / 2.0
        center_y = (min(ys) + max(ys)) / 2.0
        offset_x = abs(center_x - 50.0)
        offset_y = abs(center_y - 50.0)
        offset = np.hypot(offset_x, offset_y)
        alignment_score = max(50, int(100 - (offset * 1.2)))
        if offset > 25.0:
            if center_x < 35.0:
                issues.append("Writing is shifted to the left.")
            elif center_x > 65.0:
                issues.append("Writing is shifted to the right.")
    else:
        alignment_score = 80

    return {
        "shape_score": shape_score,
        "stroke_score": stroke_score,
        "alignment_score": alignment_score,
        "size_score": size_score,
        "issues": issues
    }

def calculate_comprehensive_evaluation(
    target_char: str,
    ocr_text: str,
    ocr_confidence: float,
    practice_mode: str,
    image_metrics: Dict[str, Any],
    canvas_strokes: Optional[List[List[Dict[str, float]]]] = None,
    language: str = "Tamil"
) -> Dict[str, Any]:
    """
    Generic evaluation pipeline for any target character, word, or sentence.
    """
    norm_target = normalize_indic_text(target_char)
    norm_ocr = normalize_indic_text(ocr_text)

    target_data = get_stroke_data(norm_target, language)

    # Empty canvas check
    if not image_metrics.get("has_ink", False):
        return {
            "target": target_char,
            "detected": "No Writing",
            "is_correct": False,
            "overall_score": 0,
            "recognition_confidence": 0.0,
            "character_score": 0,
            "shape_score": 0,
            "stroke_score": 0,
            "alignment_score": 0,
            "size_score": 0,
            "recognition_status": "UNCERTAIN",
            "feedback_type": "empty",
            "specific_feedback": "Aiyayo Kanna! No writing detected inside the box. Please draw the character!",
            "mistake_explanation": "Canvas appears empty. Write clearly using your finger or stylus.",
            "encouragement": "Let's try drawing together!"
        }

    # Evaluate Stroke Geometry & Measurements
    geom = evaluate_normalized_strokes(canvas_strokes, target_data, image_metrics)
    shape_score = geom["shape_score"]
    stroke_score = geom["stroke_score"]
    alignment_score = geom["alignment_score"]
    size_score = geom["size_score"]
    measured_issues = geom["issues"]

    # Auxiliary OCR Character Match Score
    if norm_target and norm_ocr == norm_target:
        character_score = min(100, int(max(85, ocr_confidence * 100)))
        match_status = "CORRECT"
    elif norm_target and norm_ocr and (norm_ocr in norm_target or norm_target in norm_ocr):
        character_score = 80
        match_status = "ALMOST_CORRECT"
    elif ocr_confidence > 0.70 and norm_ocr and norm_ocr != norm_target:
        character_score = 45
        match_status = "INCORRECT"
    else:
        # Stroke geometry carries high weight for handwritten scripts
        character_score = int((shape_score + stroke_score + alignment_score) / 3)
        match_status = "CORRECT" if character_score >= 82 else "ALMOST_CORRECT" if character_score >= 60 else "UNCERTAIN"

    # Overall Score Weighting
    if practice_mode == "trace":
        overall_score = int(character_score * 0.30 + shape_score * 0.35 + stroke_score * 0.20 + alignment_score * 0.15)
    elif practice_mode == "guided":
        overall_score = int(character_score * 0.40 + shape_score * 0.30 + stroke_score * 0.15 + alignment_score * 0.15)
    else: # free writing
        overall_score = int(character_score * 0.50 + shape_score * 0.25 + stroke_score * 0.15 + alignment_score * 0.10)

    overall_score = max(0, min(100, overall_score))

    # Determine 4 Result States
    if overall_score >= 85 and match_status in ["CORRECT", "ALMOST_CORRECT"]:
        result_state = "CORRECT"
        feedback_type = "correct"
        is_correct = True
        specific_feedback = f"Sabash Kanna! You wrote '{target_char}' beautifully!"
        mistake_explanation = "Your stroke paths, proportions, and alignment are excellent!"
        encouragement = "Wonderful work! You have mastered this character!"
    elif overall_score >= 60:
        result_state = "ALMOST_CORRECT"
        feedback_type = "almost_correct"
        is_correct = False
        specific_feedback = f"Almost there, Kanna! '{target_char}' is recognizable, but needs minor stroke refining."
        mistake_explanation = " ".join(measured_issues) if measured_issues else "Fine-tune curve smoothness and length."
        encouragement = "You are so close! Re-try or view 'Show Me' to reach 100%!"
    elif match_status == "UNCERTAIN":
        result_state = "UNCERTAIN"
        feedback_type = "uncertain"
        is_correct = False
        specific_feedback = f"Kanna, I couldn't clearly evaluate your '{target_char}' handwriting."
        mistake_explanation = "Writing was slightly unclear or incomplete inside the box."
        encouragement = "Try writing a little larger and more slowly."
    else:
        result_state = "INCORRECT"
        feedback_type = "incorrect"
        is_correct = False
        specific_feedback = f"Good try, Kanna! Let's practice writing '{target_char}' once more."
        mistake_explanation = " ".join(measured_issues) if measured_issues else f"The written shape differs from target '{target_char}'."
        encouragement = "Click 'Show Me' to see the exact step-by-step stroke animation!"

    return {
        "target": target_char,
        "detected": norm_ocr or (target_char if is_correct else "Unclear"),
        "is_correct": is_correct,
        "overall_score": overall_score,
        "recognition_confidence": float(ocr_confidence),
        "character_score": character_score,
        "shape_score": shape_score,
        "stroke_score": stroke_score,
        "alignment_score": alignment_score,
        "size_score": size_score,
        "recognition_status": result_state,
        "feedback_type": feedback_type,
        "specific_feedback": specific_feedback,
        "mistake_explanation": mistake_explanation,
        "encouragement": encouragement,
        "stroke_animation": target_data.get("strokes", [])
    }
