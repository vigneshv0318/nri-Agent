from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class VisionAnalyzeResponse(BaseModel):
    detected_text: str
    feedback: str
    is_correct: bool
    score: int
    recognition_status: str = "UNCERTAIN"
    expected_text: Optional[str] = None
    mistake_explanation: Optional[str] = None
    audio_base64: Optional[str] = None
    points_awarded: int = 0
    total_points: int = 0

class LetterItem(BaseModel):
    char: str
    transliteration: str
    example_word: Optional[str] = None
    meaning: Optional[str] = None
    audio_hint: Optional[str] = None
    category: Optional[str] = "vowel"
    difficulty: Optional[int] = 1
    svg_guide: Optional[str] = None
    starting_point: Optional[Dict[str, float]] = None
    directional_arrows: Optional[List[Dict[str, Any]]] = None
    strokes: Optional[List[str]] = None

class WritingEvaluateResponse(BaseModel):
    target: str
    detected: str
    is_correct: bool
    overall_score: int
    character_score: int
    shape_score: int
    stroke_score: int
    alignment_score: int
    recognition_status: str
    feedback_type: str
    specific_feedback: str
    mistake_explanation: str
    encouragement: str
    stroke_animation: Optional[List[str]] = []
    attempt_number: int = 1
    mastered: bool = False
    points_awarded: int = 0
    total_points: int = 0

class HandwritingStatsResponse(BaseModel):
    total_attempts: int
    practiced_count: int
    mastered_count: int
    avg_score: int
    best_score: int
    best_character: str
    best_character_score: int
    mastered_characters: List[Dict[str, Any]]
    weak_characters: List[Dict[str, Any]]
    improvement_pct: int
    recent_attempts: List[Dict[str, Any]]