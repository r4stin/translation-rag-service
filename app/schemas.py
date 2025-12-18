from pydantic import BaseModel


class TranslationPair(BaseModel):
    source_language: str
    target_language: str
    sentence: str
    translation: str


class PromptResponse(BaseModel):
    prompt: str


class StammeringResponse(BaseModel):
    has_stammer: bool
