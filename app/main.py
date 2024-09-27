# Import necessary libraries and modules
import asyncio
import ssl

import uvicorn
from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette.requests import Request
from starlette.responses import Response

from app.api import api_router
from app.config.logging_config import setup_logging

load_dotenv()
# Create a FastAPI instance


ssl._create_default_https_context = ssl._create_unverified_context

app = FastAPI(
    title="EXE2 App",
    description="Welcome to app chatbot",
)
setup_logging()

logger.info("Starting app")


# Dictionary to keep track of connected clients
clients = {}


router = APIRouter()
router.include_router(api_router)

app.include_router(router)


@app.get("/healthcheck")
def healthcheck():
    return {"status": "OK", "object": "health"}


@app.get("/")
def root():
    return {"message": "Welcome to Symphony project"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
