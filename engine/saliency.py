"""
ClickBait Shield AI — Mathematical Token Saliency & Attribution Engine
Computes token-level attribution directly from trained Machine Learning model weights.
"""
import re
from typing import List, Dict, Any, Optional
from engine.types_data import TokenSaliency
from engine.tokenizer import clean_word


def compute_token_saliency(raw_text: str, vocab: Dict[str, int], coefs: Any) -> List[TokenSaliency]:
    """
    Computes per-token saliency attribution scores between -1.0 (factual anchor)
    and +1.0 (clickbait trigger) using learned model coefficients.
    """
    words = raw_text.strip().split() if raw_text.strip() else []
    if not words:
        return []

    tokens_saliency: List[TokenSaliency] = []
    
    # Calculate baseline max coefficient magnitude for normalization
    max_weight_observed = 8.0

    for i, word in enumerate(words):
        clean = clean_word(word)
        weight = 0.0

        # Check unigram coefficient
        if clean in vocab:
            weight = float(coefs[vocab[clean]])

        # Check bigram with next word if unigram is neutral
        if i < len(words) - 1:
            next_clean = clean_word(words[i + 1])
            bigram = f"{clean} {next_clean}"
            if bigram in vocab:
                bi_weight = float(coefs[vocab[bigram]])
                if abs(bi_weight) > abs(weight):
                    weight = bi_weight

        # Boost score slightly for uppercase shouting or exclamation
        if re.match(r'^[A-Z]{3,}$', word):
            if weight > 0:
                weight += 1.5
        if re.search(r'[!?]', word):
            if weight > 0:
                weight += 1.0

        # Normalize score to [-1.0, 1.0]
        norm_score = max(-1.0, min(1.0, weight / max_weight_observed))

        # Categorization
        if norm_score >= 0.40:
            category = "high_clickbait"
            explanation = f"Strong clickbait signal in trained model (learned weight: {weight:+.2f})"
        elif norm_score >= 0.15:
            category = "moderate_clickbait"
            explanation = f"Moderate sensational indicator (learned weight: {weight:+.2f})"
        elif norm_score <= -0.15:
            category = "factual"
            explanation = f"Objective journalistic anchor term (learned weight: {weight:+.2f})"
        else:
            category = "neutral"
            explanation = "Neutral structural token"

        attribution_percent = int(min(100, abs(norm_score) * 100))

        tokens_saliency.append(TokenSaliency(
            token=word,
            clean_token=clean,
            score=round(norm_score, 2),
            category=category,
            attribution_percent=attribution_percent,
            matched_trigger=word if category != "neutral" else None,
            explanation=explanation
        ))

    return tokens_saliency
