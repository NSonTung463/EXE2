from pydantic.v1 import BaseModel as BaseModel_v1

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.features.summarize.service import Sumarizer
from app.llm.llm_selector import LLMSelector
selector = LLMSelector()
llm = selector.get_llm("gemini")
sumary  = Sumarizer(llm)
router = APIRouter()

@router.post("/summarize")
def summarize(request: Request):
    exam_information = sumary.retrivial_data()
    summary_content = sumary.run(exam_information)
    return JSONResponse(
        content={
            "data": summary_content,
            "message": "Success Summarize",
        },  
        status_code=status.HTTP_200_OK,
    )