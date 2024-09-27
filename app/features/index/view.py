import os

from fastapi import APIRouter, Request, UploadFile, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from loguru import logger
from pathlib import Path
import shutil

from .service import Indexer
from .model import ListFileName

UPLOAD_DIRECTORY = "uploaded_files" 
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

indexer = Indexer()
router = APIRouter()

@router.post("/index")
def index(request: Request, file: UploadFile):
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    indexer.index(file_location)
    return JSONResponse(
        content={
            "status": status.HTTP_200_OK,
            "message": "Hoàn thành lập chỉ mục",
            "data": "",
        }
    )
@router.post("/delete")
def delete(
    request: Request,
    list_file_name: ListFileName,
):
    pass