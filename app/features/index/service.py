# Langchain dependencies
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.schema import Document 
from dotenv import load_dotenv 
import os 
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from app.settings import IndexConfig
from loguru import logger
import uuid

    
class Indexer:
    def __init__(self):
        self.embedding = HuggingFaceEmbeddings(
            model_name=IndexConfig.SENTENCE_TRANSFORMERS_MODEL_NAME,
            model_kwargs={"device": "cpu"}
        )
        self.text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=int(IndexConfig.CHUNK_SIZE),
            chunk_overlap=int(IndexConfig.CHUNK_OVERLAP),
            length_function=len
        )
        self.CHROMA_PATH = IndexConfig.CHROMA_PATH
        self.db = Chroma(embedding_function=self.embedding, persist_directory=self.CHROMA_PATH)
        
    def load_documents(self, data_path):
        if data_path.endswith(".pdf"):
            logger.info("Loading PDF document.")
            document_loader = PyPDFLoader(data_path)
        elif data_path.endswith(".docx") or data_path.endswith(".doc"):
            logger.info("Loading DOCX/DOC document.")
            document_loader = Docx2txtLoader(data_path)
        elif data_path.endswith(".txt"):
            logger.info("Loading TXT document.")
            document_loader = TextLoader(data_path)
        return document_loader.load() 

    def split_text(self, documents: list[Document]):
        text_chunks = self.text_splitter.split_documents(documents)
        for i, chunk in enumerate(text_chunks):
            chunk.id = f'id_{i}'
        return text_chunks 

    def save_to_chroma(self, chunks: list[Document]):
        db = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding,
            persist_directory=self.CHROMA_PATH,
        )
        db.persist()
        logger.info(f"Saved {len(chunks)} chunks to {self.CHROMA_PATH}.")
        
    def add_documents(self, chunks: list[Document]):
        self.db.add_documents(chunks)
        logger.info(f"Add {len(chunks)} chunks to {self.CHROMA_PATH}.")

    def index(self, data_path):
        logger.info(f"Indexing documents from {data_path}")
        documents = self.load_documents(data_path)
        chunks = self.split_text(documents)
        self.add_documents(chunks)
        logger.info("Indexing completed.")
