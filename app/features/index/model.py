from pydantic import BaseModel, validator
from typing import Optional

class ListFileName(BaseModel):
    list_file_name: list[str] = []

class SearchData(BaseModel):
    question: str
    top_k: int
    file_name: Optional[str]