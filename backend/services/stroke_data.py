"""
Lesson Registry & Stroke Trajectory Definitions for Tamil, Telugu, and Hindi.
Provides dynamic character/word lessons, transliterations, meanings, and SVG stroke paths for "Show Me How" step-by-step animations.
"""

from typing import List, Dict, Any, Optional

TAMIL_LESSONS = [
    # Vowels (உயிரெழுத்துகள்)
    {
        "char": "அ",
        "transliteration": "a",
        "category": "vowel",
        "example_word": "அம்மா (Amma)",
        "meaning": "Mother",
        "stroke_count": 3,
        "difficulty": 1,
        "svg_guide": "M 35,30 C 55,20 65,45 45,55 C 30,62 25,40 45,35 L 70,35 C 75,35 80,45 80,75",
        "starting_point": {"x": 35, "y": 30},
        "directional_arrows": [{"x": 50, "y": 25, "angle": 0}, {"x": 45, "y": 45, "angle": 180}],
        "strokes": [
            "M 35,30 C 55,20 65,45 45,55",
            "M 45,55 C 30,62 25,40 45,35 L 70,35",
            "M 70,35 C 75,35 80,45 80,75"
        ]
    },
    {
        "char": "ஆ",
        "transliteration": "aa",
        "category": "vowel",
        "example_word": "ஆடு (Aadu)",
        "meaning": "Goat",
        "stroke_count": 4,
        "difficulty": 1,
        "svg_guide": "M 35,30 C 55,20 65,45 45,55 C 30,62 25,40 45,35 L 70,35 C 75,35 80,45 80,70 C 80,78 70,82 65,75",
        "starting_point": {"x": 35, "y": 30},
        "directional_arrows": [{"x": 50, "y": 25, "angle": 0}],
        "strokes": [
            "M 35,30 C 55,20 65,45 45,55",
            "M 45,55 C 30,62 25,40 45,35 L 70,35",
            "M 70,35 C 75,35 80,45 80,70",
            "M 80,70 C 80,78 70,82 65,75"
        ]
    },
    {
        "char": "இ",
        "transliteration": "i",
        "category": "vowel",
        "example_word": "இலை (Ilai)",
        "meaning": "Leaf",
        "stroke_count": 3,
        "difficulty": 2,
        "svg_guide": "M 30,35 C 50,25 60,45 40,55 C 25,62 30,80 55,75 C 75,70 80,40 60,35",
        "starting_point": {"x": 30, "y": 35},
        "directional_arrows": [{"x": 45, "y": 30, "angle": 0}],
        "strokes": [
            "M 30,35 C 50,25 60,45 40,55",
            "M 40,55 C 25,62 30,80 55,75",
            "M 55,75 C 75,70 80,40 60,35"
        ]
    },
    {
        "char": "ஈ",
        "transliteration": "ii",
        "category": "vowel",
        "example_word": "ஈட்டி (Eeti)",
        "meaning": "Spear",
        "stroke_count": 4,
        "difficulty": 2,
        "svg_guide": "M 25,25 L 25,75 M 25,25 L 75,25 M 75,25 L 75,75 M 40,50 A 3,3 0 1,1 40,49 M 60,50 A 3,3 0 1,1 60,49",
        "starting_point": {"x": 25, "y": 25},
        "directional_arrows": [{"x": 25, "y": 50, "angle": 90}],
        "strokes": [
            "M 25,25 L 25,75",
            "M 25,25 L 75,25",
            "M 75,25 L 75,75",
            "M 40,50 A 3,3 0 1,1 40,49 M 60,50 A 3,3 0 1,1 60,49"
        ]
    },
    {
        "char": "உ",
        "transliteration": "u",
        "category": "vowel",
        "example_word": "உரல் (Ural)",
        "meaning": "Mortar",
        "stroke_count": 2,
        "difficulty": 1,
        "svg_guide": "M 35,35 C 55,25 65,45 45,55 L 75,55 L 75,75",
        "starting_point": {"x": 35, "y": 35},
        "directional_arrows": [{"x": 50, "y": 30, "angle": 0}],
        "strokes": [
            "M 35,35 C 55,25 65,45 45,55",
            "M 45,55 L 75,55 L 75,75"
        ]
    },
    # Consonants & Special Letters (மெய்யெழுத்துகள் / சிறப்பு)
    {
        "char": "க",
        "transliteration": "ka",
        "category": "consonant",
        "example_word": "கண் (Kan)",
        "meaning": "Eye",
        "stroke_count": 3,
        "difficulty": 2,
        "svg_guide": "M 25,30 L 75,30 M 50,30 L 50,75 M 50,50 C 70,50 75,65 75,75",
        "starting_point": {"x": 25, "y": 30},
        "directional_arrows": [{"x": 50, "y": 30, "angle": 0}],
        "strokes": [
            "M 25,30 L 75,30",
            "M 50,30 L 50,75",
            "M 50,50 C 70,50 75,65 75,75"
        ]
    },
    {
        "char": "ம",
        "transliteration": "ma",
        "category": "consonant",
        "example_word": "மரம் (Maram)",
        "meaning": "Tree",
        "stroke_count": 2,
        "difficulty": 1,
        "svg_guide": "M 30,25 L 30,75 L 75,75 M 75,40 L 75,75",
        "starting_point": {"x": 30, "y": 25},
        "directional_arrows": [{"x": 30, "y": 50, "angle": 90}],
        "strokes": [
            "M 30,25 L 30,75 L 75,75",
            "M 75,40 L 75,75"
        ]
    },
    {
        "char": "ழ",
        "transliteration": "zha",
        "category": "special",
        "example_word": "தமிழ் (Tamil)",
        "meaning": "Tamil Language",
        "stroke_count": 4,
        "difficulty": 3,
        "svg_guide": "M 30,30 L 70,30 M 50,30 L 50,60 C 50,75 35,75 35,60 C 35,45 65,45 75,75",
        "starting_point": {"x": 30, "y": 30},
        "directional_arrows": [{"x": 50, "y": 30, "angle": 0}],
        "strokes": [
            "M 30,30 L 70,30",
            "M 50,30 L 50,60",
            "M 50,60 C 50,75 35,75 35,60",
            "M 35,60 C 35,45 65,45 75,75"
        ]
    },
    # Tamil Words (சொற்கள்)
    {
        "char": "அம்மா",
        "transliteration": "Amma",
        "category": "word",
        "example_word": "அன்பான அம்மா",
        "meaning": "Loving Mother",
        "stroke_count": 8,
        "difficulty": 2,
        "svg_guide": "M 20,30 C 35,20 40,40 30,45 L 45,45 L 45,70 M 55,25 L 55,70 L 75,70 M 75,45 L 75,70",
        "starting_point": {"x": 20, "y": 30},
        "directional_arrows": [{"x": 30, "y": 25, "angle": 0}],
        "strokes": [
            "M 20,30 C 35,20 40,40 30,45 L 45,45 L 45,70",
            "M 55,25 L 55,70 L 75,70",
            "M 75,45 L 75,70"
        ]
    },
    {
        "char": "மரம்",
        "transliteration": "Maram",
        "category": "word",
        "example_word": "பச்சை மரம்",
        "meaning": "Green Tree",
        "stroke_count": 6,
        "difficulty": 2,
        "svg_guide": "M 20,25 L 20,70 L 45,70 M 45,40 L 45,70 M 55,30 L 75,30 M 65,30 L 65,70 L 80,70",
        "starting_point": {"x": 20, "y": 25},
        "directional_arrows": [{"x": 20, "y": 45, "angle": 90}],
        "strokes": [
            "M 20,25 L 20,70 L 45,70",
            "M 45,40 L 45,70",
            "M 55,30 L 75,30 M 65,30 L 65,70 L 80,70"
        ]
    }
]

TELUGU_LESSONS = [
    {
        "char": "అ",
        "transliteration": "a",
        "category": "vowel",
        "example_word": "అమ్మ (Amma)",
        "meaning": "Mother",
        "stroke_count": 2,
        "difficulty": 1,
        "svg_guide": "M 35,40 C 35,20 65,20 65,40 C 65,65 35,65 35,40 M 65,40 L 75,75",
        "starting_point": {"x": 35, "y": 40},
        "directional_arrows": [{"x": 50, "y": 25, "angle": 0}],
        "strokes": [
            "M 35,40 C 35,20 65,20 65,40 C 65,65 35,65 35,40",
            "M 65,40 L 75,75"
        ]
    },
    {
        "char": "ఆ",
        "transliteration": "aa",
        "category": "vowel",
        "example_word": "ఆవు (Aavu)",
        "meaning": "Cow",
        "stroke_count": 3,
        "difficulty": 1,
        "svg_guide": "M 35,40 C 35,20 65,20 65,40 C 65,65 35,65 35,40 M 65,40 L 75,75 M 75,75 C 80,80 85,70 80,65",
        "starting_point": {"x": 35, "y": 40},
        "directional_arrows": [{"x": 50, "y": 25, "angle": 0}],
        "strokes": [
            "M 35,40 C 35,20 65,20 65,40 C 65,65 35,65 35,40",
            "M 65,40 L 75,75",
            "M 75,75 C 80,80 85,70 80,65"
        ]
    },
    {
        "char": "క",
        "transliteration": "ka",
        "category": "consonant",
        "example_word": "కలము (Kalamu)",
        "meaning": "Pen",
        "stroke_count": 3,
        "difficulty": 2,
        "svg_guide": "M 30,50 C 30,30 50,30 50,50 C 50,70 70,70 70,50 M 45,25 L 55,20",
        "starting_point": {"x": 30, "y": 50},
        "directional_arrows": [{"x": 40, "y": 35, "angle": 0}],
        "strokes": [
            "M 30,50 C 30,30 50,30 50,50",
            "M 50,50 C 50,70 70,70 70,50",
            "M 45,25 L 55,20"
        ]
    },
    {
        "char": "అమ్మ",
        "transliteration": "Amma",
        "category": "word",
        "example_word": "ప్రియమైన అమ్మ",
        "meaning": "Dear Mother",
        "stroke_count": 5,
        "difficulty": 2,
        "svg_guide": "M 25,40 C 25,20 50,20 50,40 M 50,40 L 60,75 M 65,45 C 65,30 85,30 85,50 L 85,75",
        "starting_point": {"x": 25, "y": 40},
        "directional_arrows": [{"x": 35, "y": 25, "angle": 0}],
        "strokes": [
            "M 25,40 C 25,20 50,20 50,40",
            "M 50,40 L 60,75",
            "M 65,45 C 65,30 85,30 85,50 L 85,75"
        ]
    }
]

HINDI_LESSONS = [
    {
        "char": "अ",
        "transliteration": "a",
        "category": "vowel",
        "example_word": "अनार (Anaar)",
        "meaning": "Pomegranate",
        "stroke_count": 4,
        "difficulty": 1,
        "svg_guide": "M 30,30 C 50,25 55,40 40,45 C 55,50 55,70 30,65 M 40,45 L 70,45 M 60,25 L 60,70 M 20,20 L 75,20",
        "starting_point": {"x": 30, "y": 30},
        "directional_arrows": [{"x": 40, "y": 25, "angle": 0}],
        "strokes": [
            "M 30,30 C 50,25 55,40 40,45 C 55,50 55,70 30,65",
            "M 40,45 L 70,45",
            "M 60,25 L 60,70",
            "M 20,20 L 75,20"
        ]
    },
    {
        "char": "आ",
        "transliteration": "aa",
        "category": "vowel",
        "example_word": "आम (Aam)",
        "meaning": "Mango",
        "stroke_count": 5,
        "difficulty": 1,
        "svg_guide": "M 30,30 C 50,25 55,40 40,45 C 55,50 55,70 30,65 M 40,45 L 70,45 M 55,25 L 55,70 M 70,25 L 70,70 M 20,20 L 80,20",
        "starting_point": {"x": 30, "y": 30},
        "directional_arrows": [{"x": 40, "y": 25, "angle": 0}],
        "strokes": [
            "M 30,30 C 50,25 55,40 40,45 C 55,50 55,70 30,65",
            "M 40,45 L 70,45",
            "M 55,25 L 55,70",
            "M 70,25 L 70,70",
            "M 20,20 L 80,20"
        ]
    },
    {
        "char": "क",
        "transliteration": "ka",
        "category": "consonant",
        "example_word": "कमल (Kamal)",
        "meaning": "Lotus",
        "stroke_count": 4,
        "difficulty": 2,
        "svg_guide": "M 50,25 L 50,75 M 50,45 C 30,45 30,65 50,65 M 50,45 C 70,45 75,60 70,70 M 20,20 L 80,20",
        "starting_point": {"x": 50, "y": 25},
        "directional_arrows": [{"x": 50, "y": 45, "angle": 90}],
        "strokes": [
            "M 50,25 L 50,75",
            "M 50,45 C 30,45 30,65 50,65",
            "M 50,45 C 70,45 75,60 70,70",
            "M 20,20 L 80,20"
        ]
    },
    {
        "char": "माँ",
        "transliteration": "Maa",
        "category": "word",
        "example_word": "प्यारी माँ",
        "meaning": "Beloved Mother",
        "stroke_count": 6,
        "difficulty": 2,
        "svg_guide": "M 25,30 L 25,70 M 25,30 L 45,50 L 65,30 L 65,70 M 75,30 L 75,70 M 15,20 L 85,20 M 60,12 C 65,8 75,8 80,12 M 70,6 A 2,2 0 1,1 70,5",
        "starting_point": {"x": 25, "y": 30},
        "directional_arrows": [{"x": 25, "y": 50, "angle": 90}],
        "strokes": [
            "M 25,30 L 25,70 M 25,30 L 45,50 L 65,30 L 65,70",
            "M 75,30 L 75,70",
            "M 15,20 L 85,20",
            "M 60,12 C 65,8 75,8 80,12 M 70,6 A 2,2 0 1,1 70,5"
        ]
    }
]

def get_lessons_by_language(language: str = "Tamil") -> List[Dict[str, Any]]:
    lang_lower = (language or "Tamil").lower()
    if lang_lower == "telugu":
        return TELUGU_LESSONS
    elif lang_lower == "hindi":
        return HINDI_LESSONS
    return TAMIL_LESSONS

def get_lesson_by_char(char: str, language: str = "Tamil") -> Optional[Dict[str, Any]]:
    lessons = get_lessons_by_language(language)
    for l in lessons:
        if l["char"] == char:
            return l
    # Generic fallback definition for unlisted characters
    return {
        "char": char,
        "transliteration": char,
        "category": "custom",
        "example_word": char,
        "meaning": f"Character {char}",
        "stroke_count": 3,
        "difficulty": 1,
        "svg_guide": "M 30,30 L 70,30 M 50,30 L 50,70",
        "starting_point": {"x": 30, "y": 30},
        "directional_arrows": [{"x": 50, "y": 30, "angle": 0}],
        "strokes": ["M 30,30 L 70,30", "M 50,30 L 50,70"]
    }
