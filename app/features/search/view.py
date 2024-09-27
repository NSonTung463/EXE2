from pydantic.v1 import BaseModel as BaseModel_v1

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from .model import ExampleSearchMetadata
from .service import DocumentSearch

document_search = DocumentSearch()
router = APIRouter()

@router.post("/retrieve")
def retrieve_data(request: Request, input: ExampleSearchMetadata):

    question = input.question
    top_k = input.top_k
    score = input.score

    results = document_search.retrivial(question, top_k, score)

    return JSONResponse(
        content={
            "data": results,
            "message": "Data retrieved successfully",
        },
        status_code=status.HTTP_200_OK,
    )

