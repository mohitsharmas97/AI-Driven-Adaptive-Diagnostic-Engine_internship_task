from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from bson import ObjectId


class Question(BaseModel):
    id: Optional[str] = None
    text: str
    options: Dict[str, str]          # {"A": "...", "B": "...", "C": "...", "D": "..."}
    correct_answer: str              # "A" | "B" | "C" | "D"
    difficulty: float                # 0.0 – 1.0 (IRT b-parameter)
    topic: str
    tags: List[str] = []

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
