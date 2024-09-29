from pydantic.v1 import BaseModel as BaseModel_v1

from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.features.test.service import CreateExam

create_exam = CreateExam()
router = APIRouter()

@router.post("/creat_exam")
def creat_exam(request: Request):
    res = create_exam.run()
    return JSONResponse(
        content={
            "data": res,
            "message": "Success Summarize",
        },  
        status_code=status.HTTP_200_OK,
    )