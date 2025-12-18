from typing import List
from app.schemas import TranslationPair
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_prompt(
    query_sentence: str,
    src_lang: str,
    tgt_lang: str,
    pairs: List[TranslationPair],
    k: int = 4
) -> str:


    if not pairs:
        return "\n".join([
            f"Translate the following sentence from {src_lang} to {tgt_lang}:",
            f"{src_lang}: {query_sentence}"
        ])

    corpus = [p.sentence for p in pairs] + [query_sentence]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(corpus)

    similarities = cosine_similarity(
        vectors[-1],
        vectors[:-1]
    )[0]

    ranked = sorted(
        zip(similarities, pairs),
        key=lambda x: x[0],
        reverse=True
    )

    top_pairs = [p for score, p in ranked if score > 0][:k]


    if not top_pairs:
        return "\n".join([
            f"Translate the following sentence from {src_lang} to {tgt_lang}:",
            f"{src_lang}: {query_sentence}"
        ])

    prompt = [
        f"Translate the following sentence from {src_lang} to {tgt_lang}.",
        "",
        "Examples:"
    ]

    for p in top_pairs:
        prompt.append(f"{src_lang}: {p.sentence}")
        prompt.append(f"{tgt_lang}: {p.translation}")
        prompt.append("")

    prompt.append("Sentence to translate:")
    prompt.append(f"{src_lang}: {query_sentence}")

    return "\n".join(prompt)
