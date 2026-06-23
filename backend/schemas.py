from pydantic import BaseModel, Field, field_validator
from typing import Optional

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    thread_id: Optional[str] = Field(default="default")
    
    @field_validator('question')
    @classmethod
    def validate_question(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Question cannot be empty")
        return v.strip()

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
