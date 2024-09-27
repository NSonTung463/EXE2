from pydantic import BaseModel
from enum import Enum

class ChatMessage(BaseModel):
    question: str

class ModelName(Enum):
    LLAMA = "llama"
    GEMINI = "gemini"
    GROQ = "groq"
    OPENAI = "openai"
    AZURE_OPENAI = "azure_openai"
    ANTHROPIC2 = "anthropic2"
    ANTHROPIC3 = "anthropic3"

from enum import Enum, unique
from typing import Optional

from pydantic import BaseModel, Field
from pydantic.v1 import BaseModel as BaseModel_v1

class ExampleSearchMetadata(BaseModel):
    question: str
    top_k: int = 3
    score: float = 0.5