"""
Writing Curriculum Manager for Ammachi AI.
Provides complete, structured language datasets for Tamil, Telugu, and Hindi.
Supports Vowels, Aytham, Consonants, Grantha, Uyirmei, Words, and Sentences.
"""

from typing import List, Dict, Any, Optional

# ============================================================
# TAMIL CURRICULUM DATASET
# ============================================================

TAMIL_VOWELS = [
    {"char": "அ", "transliteration": "a", "category": "vowel", "level": 1, "example_word": "அம்மா", "meaning": "Mother"},
    {"char": "ஆ", "transliteration": "aa", "category": "vowel", "level": 1, "example_word": "ஆடு", "meaning": "Goat"},
    {"char": "இ", "transliteration": "i", "category": "vowel", "level": 1, "example_word": "இலை", "meaning": "Leaf"},
    {"char": "ஈ", "transliteration": "ii", "category": "vowel", "level": 1, "example_word": "ஈட்டி", "meaning": "Spear"},
    {"char": "உ", "transliteration": "u", "category": "vowel", "level": 1, "example_word": "உரல்", "meaning": "Mortar"},
    {"char": "ஊ", "transliteration": "uu", "category": "vowel", "level": 1, "example_word": "ஊஞ்சல்", "meaning": "Swing"},
    {"char": "எ", "transliteration": "e", "category": "vowel", "level": 1, "example_word": "எலி", "meaning": "Mouse"},
    {"char": "ஏ", "transliteration": "ee", "category": "vowel", "level": 1, "example_word": "ஏணி", "meaning": "Ladder"},
    {"char": "ஐ", "transliteration": "ai", "category": "vowel", "level": 1, "example_word": "ஐந்து", "meaning": "Five"},
    {"char": "ஒ", "transliteration": "o", "category": "vowel", "level": 1, "example_word": "ஒட்டகம்", "meaning": "Camel"},
    {"char": "ஓ", "transliteration": "oo", "category": "vowel", "level": 1, "example_word": "ஓடம்", "meaning": "Boat"},
    {"char": "ஔ", "transliteration": "au", "category": "vowel", "level": 1, "example_word": "ஔவையார்", "meaning": "Poetess"}
]

TAMIL_AYTHAM = [
    {"char": "ஃ", "transliteration": "akku", "category": "aytham", "level": 1, "example_word": "எஃகு", "meaning": "Steel"}
]

TAMIL_CONSONANTS = [
    {"char": "க", "transliteration": "ka", "category": "consonant", "level": 2, "example_word": "கண்", "meaning": "Eye"},
    {"char": "ங", "transliteration": "nga", "category": "consonant", "level": 2, "example_word": "சிங்கம்", "meaning": "Lion"},
    {"char": "ச", "transliteration": "sa", "category": "consonant", "level": 2, "example_word": "சக்கரம்", "meaning": "Wheel"},
    {"char": "ஞ", "transliteration": "nya", "category": "consonant", "level": 2, "example_word": "ஞாயிறு", "meaning": "Sun"},
    {"char": "ட", "transliteration": "ta", "category": "consonant", "level": 2, "example_word": "பட்டம்", "meaning": "Kite"},
    {"char": "ண", "transliteration": "na", "category": "consonant", "level": 2, "example_word": "பணம்", "meaning": "Money"},
    {"char": "த", "transliteration": "tha", "category": "consonant", "level": 2, "example_word": "தாமரை", "meaning": "Lotus"},
    {"char": "ந", "transliteration": "na", "category": "consonant", "level": 2, "example_word": "நரி", "meaning": "Fox"},
    {"char": "ப", "transliteration": "pa", "category": "consonant", "level": 2, "example_word": "பந்து", "meaning": "Ball"},
    {"char": "ம", "transliteration": "ma", "category": "consonant", "level": 2, "example_word": "மரம்", "meaning": "Tree"},
    {"char": "ய", "transliteration": "ya", "category": "consonant", "level": 2, "example_word": "யானை", "meaning": "Elephant"},
    {"char": "ர", "transliteration": "ra", "category": "consonant", "level": 2, "example_word": "ரயில்", "meaning": "Train"},
    {"char": "ல", "transliteration": "la", "category": "consonant", "level": 2, "example_word": "லட்டு", "meaning": "Laddu Sweet"},
    {"char": "வ", "transliteration": "va", "category": "consonant", "level": 2, "example_word": "வண்டு", "meaning": "Beetle"},
    {"char": "ழ", "transliteration": "zha", "category": "consonant", "level": 2, "example_word": "தமிழ்", "meaning": "Tamil Language"},
    {"char": "ள", "transliteration": "la", "category": "consonant", "level": 2, "example_word": "கிளி", "meaning": "Parrot"},
    {"char": "ற", "transliteration": "ra", "category": "consonant", "level": 2, "example_word": "பறவை", "meaning": "Bird"},
    {"char": "ன", "transliteration": "na", "category": "consonant", "level": 2, "example_word": "மீன்", "meaning": "Fish"}
]

TAMIL_GRANTHA = [
    {"char": "ஜ", "transliteration": "ja", "category": "grantha", "level": 2, "example_word": "ஜன்னல்", "meaning": "Window"},
    {"char": "ஷ", "transliteration": "sha", "category": "grantha", "level": 2, "example_word": "புஷ்பம்", "meaning": "Flower"},
    {"char": "ஸ", "transliteration": "sa", "category": "grantha", "level": 2, "example_word": "ஸர்ப்பம்", "meaning": "Snake"},
    {"char": "ஹ", "transliteration": "ha", "category": "grantha", "level": 2, "example_word": "ஹரி", "meaning": "Hari"},
    {"char": "க்ஷ", "transliteration": "ksha", "category": "grantha", "level": 2, "example_word": "லக்ஷ்மி", "meaning": "Lakshmi"},
    {"char": "ஸ்ரீ", "transliteration": "shree", "category": "grantha", "level": 2, "example_word": "ஸ்ரீராம்", "meaning": "Shree Ram"}
]

TAMIL_UYIRMEI_SAMPLES = [
    {"char": "கா", "transliteration": "kaa", "category": "uyirmei", "level": 3, "example_word": "காடு", "meaning": "Forest"},
    {"char": "கி", "transliteration": "ki", "category": "uyirmei", "level": 3, "example_word": "கிளி", "meaning": "Parrot"},
    {"char": "கீ", "transliteration": "kii", "category": "uyirmei", "level": 3, "example_word": "கீரை", "meaning": "Spinach"},
    {"char": "கு", "transliteration": "ku", "category": "uyirmei", "level": 3, "example_word": "குடை", "meaning": "Umbrella"},
    {"char": "கூ", "transliteration": "kuu", "category": "uyirmei", "level": 3, "example_word": "கூடு", "meaning": "Nest"},
    {"char": "கெ", "transliteration": "ke", "category": "uyirmei", "level": 3, "example_word": "கெண்டை", "meaning": "Carp Fish"},
    {"char": "கே", "transliteration": "kee", "category": "uyirmei", "level": 3, "example_word": "கேள்வி", "meaning": "Question"},
    {"char": "கை", "transliteration": "kai", "category": "uyirmei", "level": 3, "example_word": "கை", "meaning": "Hand"},
    {"char": "கொ", "transliteration": "ko", "category": "uyirmei", "level": 3, "example_word": "கொடி", "meaning": "Flag"},
    {"char": "கோ", "transliteration": "koo", "category": "uyirmei", "level": 3, "example_word": "கோயில்", "meaning": "Temple"},
    {"char": "கௌ", "transliteration": "kau", "category": "uyirmei", "level": 3, "example_word": "கௌதாரி", "meaning": "Partridge"}
]

TAMIL_WORDS = [
    {"char": "அம்மா", "transliteration": "Amma", "category": "word", "level": 4, "example_word": "அன்பான அம்மா", "meaning": "Mother"},
    {"char": "அப்பா", "transliteration": "Appa", "category": "word", "level": 4, "example_word": "பாசமுள்ள அப்பா", "meaning": "Father"},
    {"char": "மரம்", "transliteration": "Maram", "category": "word", "level": 4, "example_word": "பச்சை மரம்", "meaning": "Tree"},
    {"char": "நாய்", "transliteration": "Naai", "category": "word", "level": 4, "example_word": "நல்ல நாய்", "meaning": "Dog"},
    {"char": "வீடு", "transliteration": "Veedu", "category": "word", "level": 4, "example_word": "அழகான வீடு", "meaning": "House"},
    {"char": "பூ", "transliteration": "Poo", "category": "word", "level": 4, "example_word": "மணமுள்ள பூ", "meaning": "Flower"},
    {"char": "நீர்", "transliteration": "Neer", "category": "word", "level": 4, "example_word": "குளிர்ந்த நீர்", "meaning": "Water"},
    {"char": "தமிழ்", "transliteration": "Tamil", "category": "word", "level": 4, "example_word": "இனிய தமிழ்", "meaning": "Tamil Language"},
    {"char": "நிலா", "transliteration": "Nilaa", "category": "word", "level": 4, "example_word": "வெள்ளை நிலா", "meaning": "Moon"},
    {"char": "மலர்", "transliteration": "Malar", "category": "word", "level": 4, "example_word": "அழகிய மலர்", "meaning": "Blossom"}
]

TAMIL_SENTENCES = [
    {"char": "தமிழ் எங்கள் தாய்மொழி", "transliteration": "Tamil engal thaaimozhi", "category": "sentence", "level": 5, "example_word": "வாழ்க தமிழ்", "meaning": "Tamil is our mother tongue"},
    {"char": "அம்மா அன்பானவர்", "transliteration": "Amma anbaanavar", "category": "sentence", "level": 5, "example_word": "அன்பே சிவம்", "meaning": "Mother is loving"},
    {"char": "மரம் பச்சையாக உள்ளது", "transliteration": "Maram pachaiyaaga ullathu", "category": "sentence", "level": 5, "example_word": "இயற்கை அழகு", "meaning": "The tree is green"}
]

# ============================================================
# TELUGU CURRICULUM DATASET
# ============================================================

TELUGU_VOWELS = [
    {"char": "అ", "transliteration": "a", "category": "vowel", "level": 1, "example_word": "అమ్మ", "meaning": "Mother"},
    {"char": "ఆ", "transliteration": "aa", "category": "vowel", "level": 1, "example_word": "ఆవు", "meaning": "Cow"},
    {"char": "ఇ", "transliteration": "i", "category": "vowel", "level": 1, "example_word": "ఇల్లు", "meaning": "House"},
    {"char": "ఈ", "transliteration": "ii", "category": "vowel", "level": 1, "example_word": "ఈగ", "meaning": "Housefly"},
    {"char": "ఉ", "transliteration": "u", "category": "vowel", "level": 1, "example_word": "ఉడుత", "meaning": "Squirrel"},
    {"char": "ఊ", "transliteration": "uu", "category": "vowel", "level": 1, "example_word": "ఊయల", "meaning": "Cradle"},
    {"char": "ఋ", "transliteration": "ru", "category": "vowel", "level": 1, "example_word": "ఋషి", "meaning": "Sage"},
    {"char": "ఎ", "transliteration": "e", "category": "vowel", "level": 1, "example_word": "ఎలుక", "meaning": "Rat"},
    {"char": "ఏ", "transliteration": "ee", "category": "vowel", "level": 1, "example_word": "ఏనుగు", "meaning": "Elephant"},
    {"char": "ఐ", "transliteration": "ai", "category": "vowel", "level": 1, "example_word": "ఐదు", "meaning": "Five"},
    {"char": "ఒ", "transliteration": "o", "category": "vowel", "level": 1, "example_word": "ఒంటె", "meaning": "Camel"},
    {"char": "ఓ", "transliteration": "oo", "category": "vowel", "level": 1, "example_word": "ఓడ", "meaning": "Ship"},
    {"char": "ఔ", "transliteration": "au", "category": "vowel", "level": 1, "example_word": "ఔషధము", "meaning": "Medicine"}
]

TELUGU_CONSONANTS = [
    {"char": "క", "transliteration": "ka", "category": "consonant", "level": 2, "example_word": "కలము", "meaning": "Pen"},
    {"char": "ఖ", "transliteration": "kha", "category": "consonant", "level": 2, "example_word": "ఖడ్గము", "meaning": "Sword"},
    {"char": "గ", "transliteration": "ga", "category": "consonant", "level": 2, "example_word": "గడప", "meaning": "Threshold"},
    {"char": "ఘ", "transliteration": "gha", "category": "consonant", "level": 2, "example_word": "ఘటము", "meaning": "Pot"},
    {"char": "చ", "transliteration": "cha", "category": "consonant", "level": 2, "example_word": "చందమామ", "meaning": "Moon"},
    {"char": "జ", "transliteration": "ja", "category": "consonant", "level": 2, "example_word": "జలము", "meaning": "Water"},
    {"char": "ట", "transliteration": "ta", "category": "consonant", "level": 2, "example_word": "టపాకాయ", "meaning": "Firecracker"},
    {"char": "డ", "transliteration": "da", "category": "consonant", "level": 2, "example_word": "డబ్బాలు", "meaning": "Boxes"},
    {"char": "త", "transliteration": "tha", "category": "consonant", "level": 2, "example_word": "తబులా", "meaning": "Tablas"},
    {"char": "ద", "transliteration": "da", "category": "consonant", "level": 2, "example_word": "దయ", "meaning": "Kindness"},
    {"char": "న", "transliteration": "na", "category": "consonant", "level": 2, "example_word": "నమస్కారము", "meaning": "Greetings"},
    {"char": "ప", "transliteration": "pa", "category": "consonant", "level": 2, "example_word": "పలక", "meaning": "Slate"},
    {"char": "బ", "transliteration": "ba", "category": "consonant", "level": 2, "example_word": "బంతి", "meaning": "Ball"},
    {"char": "మ", "transliteration": "ma", "category": "consonant", "level": 2, "example_word": "మలయము", "meaning": "Sandalwood"}
]

TELUGU_WORDS = [
    {"char": "అమ్మ", "transliteration": "Amma", "category": "word", "level": 4, "example_word": "మంచి అమ్మ", "meaning": "Mother"},
    {"char": "నాన్న", "transliteration": "Naanna", "category": "word", "level": 4, "example_word": "ప్రియమైన నాన్న", "meaning": "Father"},
    {"char": "చెట్టు", "transliteration": "Chettu", "category": "word", "level": 4, "example_word": "పచ్చని చెట్టు", "meaning": "Tree"},
    {"char": "పువ్వు", "transliteration": "Puvvu", "category": "word", "level": 4, "example_word": "అందమైన పువ్వు", "meaning": "Flower"}
]

TELUGU_SENTENCES = [
    {"char": "తెలుగు మా మాతృభాష", "transliteration": "Telugu maa maathrubhaasha", "category": "sentence", "level": 5, "example_word": "తెలుగు వెలుగు", "meaning": "Telugu is our mother tongue"}
]

# ============================================================
# HINDI CURRICULUM DATASET
# ============================================================

HINDI_VOWELS = [
    {"char": "अ", "transliteration": "a", "category": "vowel", "level": 1, "example_word": "अनार", "meaning": "Pomegranate"},
    {"char": "आ", "transliteration": "aa", "category": "vowel", "level": 1, "example_word": "आम", "meaning": "Mango"},
    {"char": "इ", "transliteration": "i", "category": "vowel", "level": 1, "example_word": "इमली", "meaning": "Tamarind"},
    {"char": "ई", "transliteration": "ii", "category": "vowel", "level": 1, "example_word": "ईख", "meaning": "Sugarcane"},
    {"char": "उ", "transliteration": "u", "category": "vowel", "level": 1, "example_word": "उल्लू", "meaning": "Owl"},
    {"char": "ऊ", "transliteration": "uu", "category": "vowel", "level": 1, "example_word": "ऊन", "meaning": "Wool"},
    {"char": "ऋ", "transliteration": "ru", "category": "vowel", "level": 1, "example_word": "ऋषि", "meaning": "Sage"},
    {"char": "ए", "transliteration": "e", "category": "vowel", "level": 1, "example_word": "एक", "meaning": "One"},
    {"char": "ऐ", "transliteration": "ai", "category": "vowel", "level": 1, "example_word": "ऐनक", "meaning": "Spectacles"},
    {"char": "ओ", "transliteration": "o", "category": "vowel", "level": 1, "example_word": "ओखली", "meaning": "Mortar"},
    {"char": "औ", "transliteration": "au", "category": "vowel", "level": 1, "example_word": "औरत", "meaning": "Woman"},
    {"char": "अं", "transliteration": "am", "category": "vowel", "level": 1, "example_word": "अंगूर", "meaning": "Grapes"}
]

HINDI_CONSONANTS = [
    {"char": "क", "transliteration": "ka", "category": "consonant", "level": 2, "example_word": "कमल", "meaning": "Lotus"},
    {"char": "ख", "transliteration": "kha", "category": "consonant", "level": 2, "example_word": "खरगोश", "meaning": "Rabbit"},
    {"char": "ग", "transliteration": "ga", "category": "consonant", "level": 2, "example_word": "गमला", "meaning": "Flowerpot"},
    {"char": "घ", "transliteration": "gha", "category": "consonant", "level": 2, "example_word": "घड़ी", "meaning": "Clock"},
    {"char": "च", "transliteration": "cha", "category": "consonant", "level": 2, "example_word": "चम्मच", "meaning": "Spoon"},
    {"char": "छ", "transliteration": "chha", "category": "consonant", "level": 2, "example_word": "छतरी", "meaning": "Umbrella"},
    {"char": "ज", "transliteration": "ja", "category": "consonant", "level": 2, "example_word": "जग", "meaning": "Jug"},
    {"char": "झ", "transliteration": "jha", "category": "consonant", "level": 2, "example_word": "झंडा", "meaning": "Flag"},
    {"char": "ट", "transliteration": "ta", "category": "consonant", "level": 2, "example_word": "टमाटर", "meaning": "Tomato"},
    {"char": "ठ", "transliteration": "tha", "category": "consonant", "level": 2, "example_word": "ठठेरा", "meaning": "Tinker"},
    {"char": "ड", "transliteration": "da", "category": "consonant", "level": 2, "example_word": "डमरू", "meaning": "Small Drum"},
    {"char": "ढ", "transliteration": "dha", "category": "consonant", "level": 2, "example_word": "ढक्कन", "meaning": "Lid"},
    {"char": "त", "transliteration": "tha", "category": "consonant", "level": 2, "example_word": "तरबूज", "meaning": "Watermelon"},
    {"char": "थ", "transliteration": "thaa", "category": "consonant", "level": 2, "example_word": "थर्मस", "meaning": "Flask"},
    {"char": "द", "transliteration": "da", "category": "consonant", "level": 2, "example_word": "दवात", "meaning": "Inkpot"},
    {"char": "ध", "transliteration": "dha", "category": "consonant", "level": 2, "example_word": "धनुष", "meaning": "Bow"},
    {"char": "न", "transliteration": "na", "category": "consonant", "level": 2, "example_word": "नल", "meaning": "Tap"},
    {"char": "प", "transliteration": "pa", "category": "consonant", "level": 2, "example_word": "पतंग", "meaning": "Kite"},
    {"char": "फ", "transliteration": "pha", "category": "consonant", "level": 2, "example_word": "फल", "meaning": "Fruit"},
    {"char": "ब", "transliteration": "ba", "category": "consonant", "level": 2, "example_word": "बस", "meaning": "Bus"},
    {"char": "भ", "transliteration": "bha", "category": "consonant", "level": 2, "example_word": "भालू", "meaning": "Bear"},
    {"char": "म", "transliteration": "ma", "category": "consonant", "level": 2, "example_word": "मछली", "meaning": "Fish"}
]

HINDI_WORDS = [
    {"char": "माँ", "transliteration": "Maa", "category": "word", "level": 4, "example_word": "प्यारी माँ", "meaning": "Mother"},
    {"char": "पिता", "transliteration": "Pita", "category": "word", "level": 4, "example_word": "आदरणीय पिता", "meaning": "Father"},
    {"char": "पेड़", "transliteration": "Ped", "category": "word", "level": 4, "example_word": "हरा पेड़", "meaning": "Tree"},
    {"char": "फूल", "transliteration": "Phool", "category": "word", "level": 4, "example_word": "सुंदर फूल", "meaning": "Flower"}
]

HINDI_SENTENCES = [
    {"char": "हिंदी हमारी राष्ट्रभाषा है", "transliteration": "Hindi hamari rashtrabhasha hai", "category": "sentence", "level": 5, "example_word": "जय हिंद", "meaning": "Hindi is our national language"}
]


def get_complete_curriculum(language: str = "Tamil", category: Optional[str] = None, level: Optional[int] = None) -> List[Dict[str, Any]]:
    lang_lower = (language or "Tamil").lower()
    
    if lang_lower == "telugu":
        all_items = TELUGU_VOWELS + TELUGU_CONSONANTS + TELUGU_WORDS + TELUGU_SENTENCES
    elif lang_lower == "hindi":
        all_items = HINDI_VOWELS + HINDI_CONSONANTS + HINDI_WORDS + HINDI_SENTENCES
    else:
        all_items = (
            TAMIL_VOWELS + TAMIL_AYTHAM + TAMIL_CONSONANTS + 
            TAMIL_GRANTHA + TAMIL_UYIRMEI_SAMPLES + TAMIL_WORDS + TAMIL_SENTENCES
        )

    if category and category != "all":
        all_items = [i for i in all_items if i.get("category") == category]
        
    if level and level > 0:
        all_items = [i for i in all_items if i.get("level") == level]

    return all_items


def get_curriculum_item(char: str, language: str = "Tamil") -> Dict[str, Any]:
    items = get_complete_curriculum(language)
    for i in items:
        if i["char"] == char:
            return i
    # Dynamic fallback item for unlisted characters or custom words
    return {
        "char": char,
        "transliteration": char,
        "category": "word" if len(char) > 1 else "consonant",
        "level": 4 if len(char) > 1 else 2,
        "example_word": char,
        "meaning": f"Character {char}"
    }
