from uuid import UUID

from pydantic import BaseModel


class SessionCreateResponse(BaseModel):
    session_token: UUID
    status: str

class AnswerCreate(BaseModel):
    session_token: UUID
    question_code: str
    value: dict
    weighted_score: int