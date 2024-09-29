# Langchain dependencies
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.schema import Document 
from dotenv import load_dotenv 
import os 
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from app.settings import IndexConfig, embedding
from loguru import logger

class DocumentSearch:
    def __init__(self, embedding=embedding):
        self.embedding = embedding
        self.CHROMA_PATH = IndexConfig.CHROMA_PATH
        self.db = Chroma(embedding_function=self.embedding, persist_directory=self.CHROMA_PATH)
    
    def retrivial(self, query_text: str, topk: int = 3, score: float =0.6):
        results = self.db.similarity_search_with_relevance_scores(query_text, k=topk)
        if len(results) == 0 or results[0][1] < score:
            logger.info("Unable to find matching results.")
        return [doc.page_content for doc, _score in results]