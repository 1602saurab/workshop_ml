import sys 
from src.exception import CustomException 
from src.logger import get_logger 
from rag.generator import Generator 
from rag.retriever import Retriever 
from rag.rag_config_loader import load_rag_config 
logger = get_logger(__name__) 

class RAGPipeline:
    def __init__(self):
        self.config = load_rag_config() 
        self.retriever = Retriever(self.config)
        self.generator = Generator(self.config) 

    def answer(self, query:str):
        try:
            logger.info(f"RAG query received: '{query}' ") 
            retrieved_chunks = self.retriever.retrieve(query) 
            answer_text = self.generator.generate(query, retrieved_chunks) 

            sources = sorted({c['source'] for c in retrieved_chunks}) 
            response = {
                "answer": answer_text,
                "sources": sources,
                "retrieved_chunks": retrieved_chunks
            }
            logger.info(f"RAG answer generated. Source used: {sources}") 
            return response 
        except Exception as e:
            raise CustomException(e,sys)  
