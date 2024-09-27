import sys
from typing import Dict
from urllib.parse import parse_qs

from fastapi import APIRouter, Body, Request
from fastapi.encoders import jsonable_encoder
from loguru import logger



def setup_logging():
    logger.remove()
    logger.add(
        "logs/app.log",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} | {message}",
        rotation="5 MB",
        retention=10,
    )
    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    logger.add(
        sys.stdout,
        level="DEBUG",
        colorize=True,
        format=logger_format,
        # format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{line} | {message}",
    )
