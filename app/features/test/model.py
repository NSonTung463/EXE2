from enum import Enum, unique
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.v1 import BaseModel as BaseModel_v1

class ExampleSearchMetadata(BaseModel):
    question: str
    top_k: int = 3
    score: float = 0.5