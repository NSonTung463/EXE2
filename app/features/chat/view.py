from pydantic.v1 import BaseModel as BaseModel_v1

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.features.search.service import DocumentSearch
from .model import ExampleSearchMetadata
from .service import Chat

chat = Chat()
document_search = DocumentSearch()
router = APIRouter()

@router.post("/chitchat")
def chitchat(request: Request, input: ExampleSearchMetadata):

    question = input.question
    top_k = input.top_k
    score = input.score

    retrivial_search = document_search.retrivial(query_text=question, topk=top_k, score=score)
    context_text = "\n\n".join(retrivial_search)
    results = chat.chat_with_doc(query_text=question, context_text=context_text)

    return JSONResponse(
        content={
            "data": results,
            "message": "Data retrieved successfully",
        },
        status_code=status.HTTP_200_OK,
    )

