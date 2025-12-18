"""
Stammering detection heuristics.

This module detects repetition artifacts introduced during translation,
focusing on explainable and deterministic rules.
"""

import re
from itertools import groupby
from collections import Counter


def normalize(text: str):
    """Lowercase, remove punctuation, and tokenize."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()


def max_consecutive_repetition(words):
    """Return the maximum number of consecutive repeated tokens."""
    return max((len(list(group)) for _, group in groupby(words)), default=0)


def detect_stammering(source_sentence: str, translated_sentence: str) -> bool:
    """
    Detect stammering artifacts in a translated sentence.

    The detection is based on multiple heuristics:
    - Character flooding (e.g. 'sooooo')
    - Repetition amplification relative to the source
    - Phrase-level repetition via n-grams
    - Low lexical diversity in long outputs

    Args:
        source_sentence (str): Original input sentence.
        translated_sentence (str): Translated output.

    Returns:
        bool: True if stammering is detected, False otherwise.
    """
    src_words = normalize(source_sentence)
    tgt_words = normalize(translated_sentence)

    if not tgt_words:
        return False

    # Character flooding
    if re.search(r"(.)\1{5,}", translated_sentence.lower()):
        return True

    src_rep = max_consecutive_repetition(src_words)
    tgt_rep = max_consecutive_repetition(tgt_words)

    # Repetition amplification
    if tgt_rep >= 4 and tgt_rep > src_rep:
        return True

    # Phrase repetition (trigrams)
    trigrams = list(zip(tgt_words, tgt_words[1:], tgt_words[2:]))
    tri_counts = Counter(trigrams)

    if any(count >= 3 and len(set(tri)) > 1 for tri, count in tri_counts.items()):
        return True

    # Low lexical diversity in long outputs
    unique_ratio = len(set(tgt_words)) / len(tgt_words)
    if len(tgt_words) >= 8 and unique_ratio < 0.4:
        return True

    return False
