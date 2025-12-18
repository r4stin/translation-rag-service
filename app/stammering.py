import re
from itertools import groupby
from collections import Counter


def normalize(text: str):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.split()


def max_consecutive_repetition(words):
    return max((len(list(group)) for _, group in groupby(words)), default=0)


def detect_stammering(source_sentence: str, translated_sentence: str) -> bool:
    src_words = normalize(source_sentence)
    tgt_words = normalize(translated_sentence)

    if not tgt_words:
        return False

    if re.search(r"(.)\1{5,}", translated_sentence.lower()):
        return True

    src_rep = max_consecutive_repetition(src_words)
    tgt_rep = max_consecutive_repetition(tgt_words)

    if tgt_rep >= 4 and tgt_rep > src_rep:
        return True

    trigrams = list(zip(tgt_words, tgt_words[1:], tgt_words[2:]))
    tri_counts = Counter(trigrams)

    if any(count >= 3 and len(set(tri)) > 1 for tri, count in tri_counts.items()):
        return True

    unique_ratio = len(set(tgt_words)) / len(tgt_words)
    if len(tgt_words) >= 8 and unique_ratio < 0.4:
        return True

    return False
