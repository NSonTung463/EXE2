from fastapi import APIRouter, Request, UploadFile, status
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil

from .config import db
from .service import FirebaseProvider, extract_text_from_pdf
from app.utils.utils import get_current_time
from app.features.index.service import Indexer
from app.features.vectorstore.service import VectorStore
UPLOAD_DIRECTORY = "uploaded_files"
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

firebase_provider = FirebaseProvider()
router = APIRouter()
index = Indexer()
vectorstore = VectorStore()

@router.post("/upload")
def upload_document(request: Request, file: UploadFile):
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    file_content = extract_text_from_pdf(file_location)
    # print(file_content)
    
    index.index(file_location)
    # documents = index.load_documents(file_location)
    # chunks = index.split_text(documents)
    # vectorstore.upload_documents(chunks)

    data = {
        "filename": file.filename,
        "content": file_content,
        "uploaded_at": get_current_time()
    }
    
    result = firebase_provider.upload_doc(data)
    return JSONResponse(
        content={
            "status": status.HTTP_200_OK if "successfully" in result else status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": result,
            "data": "",
        }
    )

@router.get("/document/{document_id}")
def get_document(document_id: str):
    result = firebase_provider.get_doc(document_id)
    if result:
        return JSONResponse(
            content={
                "status": status.HTTP_200_OK,
                "message": "Document retrieved successfully",
                "data": result,
            }
        )
    else:
        return JSONResponse(
            content={
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Document not found",
                "data": "",
            }
        )

@router.delete("/document/{document_id}")
def delete_document(document_id: str):
    result = firebase_provider.delete_doc(document_id)
    return JSONResponse(
        content={
            "status": status.HTTP_200_OK if "successfully" in result else status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": result,
            "data": "",
        }
    )

@router.put("/document/{document_id}")
def update_document(document_id: str, data: dict):
    result = firebase_provider.update_doc(document_id, data)
    return JSONResponse(
        content={
            "status": status.HTTP_200_OK if "successfully" in result else status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": result,
            "data": "",
        }
    )