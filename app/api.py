from fastapi import APIRouter, Depends

from app.features.chat.view import router as chat_router
from app.features.index.view import router as indexing_router
from app.features.search.view import router as search_router

api_router = APIRouter(prefix="/api/v1")
authenticated_api_router = APIRouter()

api_router.include_router(
    search_router,
    prefix="/search",
    tags=["search"],
)


api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["chat"],
)

api_router.include_router(
    indexing_router,
    prefix="/index",
    tags=["index"],
)
