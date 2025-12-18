"""
Pydantic models defining request and response schemas.

These models provide validation, serialization, and documentation
for the FastAPI endpoints.
"""

from pydantic import BaseModel


class TranslationPair(BaseModel):
    """
    Represents a translation example stored in the system.
    """
    source_language: str
    target_language: str
    sentence: str
    translation: str


class PromptResponse(BaseModel):
    """
    Response model for the /prompt endpoint.
    """
    prompt: str


class StammeringResponse(BaseModel):
    """
    Response model for the /stammering endpoint.
    """
    has_stammer: bool
