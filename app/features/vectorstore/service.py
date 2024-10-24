from ...utils.constant import INDEX_NAME
from ..vectorstore.config import pc
from langchain_pinecone import PineconeVectorStore # type: ignore
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.settings import IndexConfig

class VectorStore:
    def __init__(self) :
        self.embedding = HuggingFaceEmbeddings(
            model_name=IndexConfig.SENTENCE_TRANSFORMERS_MODEL_NAME,
            model_kwargs={"device": "cpu"}
        )
        self.index_name = INDEX_NAME
        self.pc = pc

    def upload_documents(self, document):
        print(f"Going to add {len(documents)} to Pinecone")
        vector_store = PineconeVectorStore(index=self.pc, embedding=self.embedding)
        vector_store.add_documents(documents=documents)
        print("****Loading to vectorstore done ***")
       