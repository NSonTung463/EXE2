import os
from dataclasses import dataclass
from typing import Union
from langchain_community.embeddings import HuggingFaceEmbeddings

from dotenv import dotenv_values, load_dotenv

# Load variables from .env file into a dictionary
load_dotenv()
config = dotenv_values(".env")

@dataclass
class AzureOpenAIGPT35:
    azure_endpoint: str = config.get("AZURE-OPENAI-GPT35-ENDPOINT")
    api_key: str = config.get("AZURE-OPENAI-GPT35-API-KEY")
    api_version: str = config.get("AZURE-OPENAI-GPT35-API-VERSION")
    azure_deployment: str = config.get("AZURE-OPENAI-GPT35-DEPLOYMENT")

@dataclass
class AzureOpenAIGPT4:
    azure_endpoint: str = config.get("AZURE-OPENAI-GPT4-ENDPOINT")
    api_key: str = config.get("AZURE-OPENAI-GPT4-API-KEY")
    api_version: str = config.get("AZURE-OPENAI-GPT4-API-VERSION")
    azure_deployment: str = config.get("AZURE-OPENAI-GPT4-DEPLOYMENT")
    model_name: str = config.get("AZURE-OPENAI-GPT4-MODEL-NAME")

@dataclass
class IndexConfig:
    SENTENCE_TRANSFORMERS_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    CHUNK_SIZE: int = 600
    CHUNK_OVERLAP: int = 128
    CHROMA_PATH: str = "my_vectordb"

embedding = HuggingFaceEmbeddings(
            model_name=IndexConfig.SENTENCE_TRANSFORMERS_MODEL_NAME,
            model_kwargs={"device": "cpu"}
        )