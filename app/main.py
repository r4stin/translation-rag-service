import os
from fastapi import FastAPI, Query
from app.schemas import TranslationPair, PromptResponse, StammeringResponse
from app.storage import TranslationStore
from app.similarity import build_prompt
from app.stammering import detect_stammering

os.makedirs("data", exist_ok=True)

app = FastAPI(title="RAG Translation Backend")
store = TranslationStore()



@app.post("/pairs")
def add_translation_pair(pair: TranslationPair):
    store.add(pair)
    return {"status": "ok"}


@app.get("/prompt", response_model=PromptResponse)
def get_prompt(
    source_language: str = Query(...),
    target_language: str = Query(...),
    query_sentence: str = Query(...)
):
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
    has_stammer = detect_stammering(
        source_sentence,
        translated_sentence
    )
    return {"has_stammer": has_stammer}

