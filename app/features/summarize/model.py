from enum import Enum, unique
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.v1 import BaseModel as BaseModel_v1

class ExampleSearchMetadata(BaseModel):
    question: str
    top_k: int = 3
    score: float = 0.5
    
@unique
class FeatureType(Enum):
    SUMMARIZE = "Summarize"

SUMARIZE_QUESTION =  {
    "list_retrivial_questions": [
        {
            "question": "Mark the letter A, B, C, or D on your answer sheet to indicate the",
        },
        {
            "question": "Read the following passage and mark the letter A, B, C, or D on your answer sheet to indicate",
        },
    ]
}