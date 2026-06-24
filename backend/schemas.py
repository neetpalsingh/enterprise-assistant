from pydantic import BaseModel, Field, field_validator
from typing import Optional

BLOCKED_PATTERNS = [
    "ignore previous instructions",
    "ignore all instructions",
    "show system prompt",
    "reveal prompt",
    "reveal system prompt",
    "disregard previous",
    "forget previous instructions",
    "bypass security",
    "override instructions",
    "admin mode",
    "developer mode",
    "god mode"
]

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="User question")
    thread_id: Optional[str] = Field(default="default")

    @field_validator('question')
    @classmethod
    def validate_question(cls, v: str) -> str:
        stripped = v.strip()

        if not stripped:
            raise ValueError("Question cannot be empty")

        if len(stripped) < 3:
            raise ValueError("Question must be at least 3 characters long")

        question_lower = stripped.lower()

        for pattern in BLOCKED_PATTERNS:
            if pattern in question_lower:
                raise ValueError("Request violates system safety policies")

        return stripped

class AskResponse(BaseModel):
    answer: str
    thread_id: str
    success: bool = True

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    success: bool = False

class HealthResponse(BaseModel):
    status: str
    llm_provider: str
    available_providers: dict
