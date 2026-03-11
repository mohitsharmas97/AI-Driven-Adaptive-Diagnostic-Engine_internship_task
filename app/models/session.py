from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class Response(BaseModel):
    question_id: str
    selected_answer: str
    correct_answer: str
    is_correct: bool
    difficulty: float
    topic: str
    ability_before: float
    ability_after: float


class UserSession(BaseModel):
    id: Optional[str] = None
    student_id: str
    ability_score: float = 0.5          # starts at 0.5 (IRT θ)
    responses: List[Response] = []
    answered_ids: List[str] = []
    status: Literal["active", "completed"] = "active"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    total_questions: int = 10           # session ends after this many questions
    study_plan: Optional[dict] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
