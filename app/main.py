"""
Main application entry point.

This module defines the FastAPI application and exposes the REST endpoints
for managing translation pairs, generating RAG-based translation prompts,
and detecting stammering in translated sentences.
"""

import os
from fastapi import FastAPI, Query

from app.schemas import TranslationPair, PromptResponse, StammeringResponse
from app.storage import TranslationStore
from app.similarity import build_prompt
from app.stammering import detect_stammering

# Ensure persistent data directory exists
os.makedirs("data", exist_ok=True)

# Initialize FastAPI application
app = FastAPI(title="RAG Translation Backend")

# Initialize persistent storage
store = TranslationStore()


@app.post("/pairs")
def add_translation_pair(pair: TranslationPair):
    """
    Store a new translation pair.

    The operation is idempotent: duplicate pairs are ignored at the
    database level via a UNIQUE constraint.

    Args:
        pair (TranslationPair): Source/target languages and translation data.

    Returns:
        dict: Status message.
    """
    store.add(pair)
    return {"status": "ok"}


@app.get("/prompt", response_model=PromptResponse)
def get_prompt(
    source_language: str = Query(...),
    target_language: str = Query(...),
    query_sentence: str = Query(...)
):
    """
    Generate a translation prompt using Retrieval-Augmented Generation (RAG).

    The system retrieves the most relevant translation examples for the
    specified language pair and builds a prompt suitable for LLM-based
    translation.

    Args:
        source_language (str): Source language code.
        target_language (str): Target language code.
        query_sentence (str): Sentence to be translated.

    Returns:
        PromptResponse: Generated prompt string.
    """
    pairs = store.get_by_language(source_language, target_language)
    prompt = build_prompt(
        query_sentence,
        source_language,
        target_language,
        pairs
    )
    return {"prompt": prompt}


@app.get("/stammering", response_model=StammeringResponse)
def stammering(
    source_sentence: str = Query(...),
    translated_sentence: str = Query(...)
):
    """
    Detect stammering artifacts introduced during translation.

    Stammering is identified via deterministic heuristics such as
    repetition amplification, character flooding, and phrase repetition.

    Args:
        source_sentence (str): Original input sentence.
        translated_sentence (str): Generated translation.

    Returns:
        StammeringResponse: Boolean indicating presence of stammering.
    """
    has_stammer = detect_stammering(
        source_sentence,
        translated_sentence
    )
    return {"has_stammer": has_stammer}
