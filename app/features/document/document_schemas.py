from typing import AnyStr, Dict
from pydantic import BaseModel, Field
from app.utils.utils import get_current_time

class DocModel(BaseModel):
    id: str = Field(..., description="Document ID")
    name: str = Field(..., description="Document Name")
    path: str = Field(..., description="Document Path")
    content: str = Field(..., description="Document Content")
    upload_at: str = Field(..., description="Document Uploaded At")

class DocSchema:
    '''
    Schema and Validation for Document
    '''
    def __init__(
        self,
        doc_id: AnyStr = None,
        name: AnyStr = "",
        path: AnyStr = "",
        content: AnyStr = "",
        upload_at: AnyStr = get_current_time()
    ):
        self.id = doc_id
        self.name = name
        self.path = path
        self.content = content
        self.upload_at = upload_at

    def to_dict(self, include_id = True):
        data_dict = {
            "name": self.name,
            "path": self.path,
            "content": self.content,
            "upload_at": self.upload_at
        }
        if include_id:
            data_dict["id"] = self.id
        return data_dict

    @staticmethod
    def from_dict(data: Dict):
        return DocSchema(
            doc_id=data.get("id"),
            name=data.get("name"),
            path=data.get("path"),
            content=data.get("content"),
            upload_at=data.get("upload_at")
        )
