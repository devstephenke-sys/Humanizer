from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

ToolName = Literal[
    "humanize",
    "rewrite",
    "paraphrase",
    "essay",
    "article",
    "sentence",
    "paragraph",
    "improve",
    "grammar",
]
ProfileName = Literal["swift", "studio", "careful", "plain"]
DetectMode = Literal["quick", "deep"]


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=1, max_length=80)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserPublic(BaseModel):
    id: str
    email: EmailStr
    display_name: str


class AuthResponse(BaseModel):
    token: str
    user: UserPublic


class RewriteRequest(BaseModel):
    text: str = Field(min_length=1)
    tool: ToolName = "humanize"
    intensity: int = Field(default=5, ge=1, le=10)
    profile: ProfileName = "studio"
    language: str = "auto"
    preserve_citations: bool = True

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Enter some text.")
        return value


class RewriteResponse(BaseModel):
    tool: ToolName
    text: str
    intensity: int
    profile: ProfileName
    word_count: int
    character_count: int
    warnings: list[str]
    provider: str
    disclaimer: str


class AlternativesRequest(BaseModel):
    sentence: str = Field(min_length=1)
    context: str = ""
    tool: ToolName = "humanize"
    intensity: int = Field(default=5, ge=1, le=10)
    language: str = "auto"

    @field_validator("sentence")
    @classmethod
    def sentence_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Enter a sentence.")
        return value.strip()


class AlternativesResponse(BaseModel):
    alternatives: list[str]
    disclaimer: str


class DetectRequest(BaseModel):
    text: str = Field(min_length=1)
    mode: DetectMode = "deep"

    @field_validator("text")
    @classmethod
    def text_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Enter some text.")
        return value


class SentenceSignal(BaseModel):
    text: str
    ai_likelihood: int
    label: Literal["lower", "mixed", "higher"]
    note: str


class DetectResponse(BaseModel):
    mode: DetectMode
    word_count: int
    character_count: int
    ai_likelihood: int
    human_like: int
    label: str
    summary: str
    reading_ease: float | None
    short_text_warning: str | None
    signals: list[str]
    sentences: list[SentenceSignal]
    disclaimer: str


class DocumentCreate(BaseModel):
    title: str = Field(default="", max_length=180)
    tool: ToolName
    input_text: str = Field(min_length=1)
    output_text: str = ""
    settings_json: str = "{}"


class DocumentUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=180)
    output_text: str | None = None
    input_text: str | None = None
    settings_json: str | None = None


class DocumentPublic(BaseModel):
    id: str
    title: str
    tool: ToolName
    input_text: str
    output_text: str
    settings_json: str
    created_at: datetime
    updated_at: datetime


class ExportRequest(BaseModel):
    title: str = "Draftwell"
    text: str = Field(min_length=1)


class HealthResponse(BaseModel):
    status: str
    provider: str
    provider_configured: bool
    payments_enabled: bool = False
