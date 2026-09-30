"""
ClickBait Shield AI — Lexical and Syntactic Tokenizer
Extracts clean words and quantitative syntactic metrics from headlines.
"""
import re
from engine.types_data import LexicalMetrics

def clean_word(word: str) -> str:
    """Strip leading/trailing punctuation and convert to lowercase."""
    return re.sub(r'^[^\w]+|[^\w]+$', '', word).lower()

def extract_lexical_metrics(text: str) -> LexicalMetrics:
    """Extract structural and syntactic indicators from a headline."""
    trimmed = text.strip()
    words = trimmed.split() if trimmed else []
    chars = len(trimmed)

    # Exclamation and Question marks
    exclamation_count = len(re.findall(r'!', text))
    question_count = len(re.findall(r'\?', text))

    # Letter capitalization ratio
    letters = re.findall(r'[a-zA-Z]', text)
    upper_letters = re.findall(r'[A-Z]', text)
    uppercase_ratio = round((len(upper_letters) / len(letters)) * 100, 1) if letters else 0.0

    # Digits
    digits = re.findall(r'\d', text)
    digit_count = len(digits)

    # Number listicle hook detection (e.g., "15 Shocking...", "10 Things...")
    has_number_list_bait = bool(re.search(
        r'^(#?\d+|top\s+\d+|[0-9]+\s+(simple|ways|things|reasons|facts|secrets|tricks|photos|celebs))',
        trimmed,
        re.IGNORECASE
    ))

    # Curiosity gap phrasing
    has_curiosity_gap = bool(re.search(
        r'(you won\'?t believe|this is why|here\'?s why|what happens? next|see why|find out why|what he discovered|what she looked like)',
        trimmed,
        re.IGNORECASE
    ))

    # Demonstrative forward-referencing pronouns ("this one trick", "these reasons")
    has_demonstrative_pronouns = bool(
        re.search(r'\b(this|these|here)\b', trimmed, re.IGNORECASE) and
        re.search(r'\b(will|can|is|are|happened|looks|broke)\b', trimmed, re.IGNORECASE)
    )

    return LexicalMetrics(
        word_count=len(words),
        char_count=chars,
        exclamation_count=exclamation_count,
        question_count=question_count,
        uppercase_ratio=uppercase_ratio,
        digit_count=digit_count,
        emotional_valence=0.0,
        has_number_list_bait=has_number_list_bait,
        has_curiosity_gap=has_curiosity_gap,
        has_demonstrative_pronouns=has_demonstrative_pronouns
    )
