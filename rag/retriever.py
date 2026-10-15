import sys 
import faiss 
import numpy as np 
from src.exception import CustomException 
from src.logger import get_logger 
from rag.vector_store import VectorStore 
logger = get_logger(__name__) 

class Retriever:
    def __init__(self, config:dict):
        self.config = config['retrieval'] 
        self.vector_store = VectorStore(config) 
        self.vectorizer , self.index, self.chunks = self.vector_store.load() 
        logger.info(f"Retriever ready with {len(self.chunks)} indexed chunks") 

    def retrieve(self, query:str):
        try:
            top_k = self.config['top_k'] 
            min_similarity = self.config['min_similarity'] 
            query_vec = self.vectorizer.transform([query]).toarray().astype('float32') 
            faiss.normalize_L2(query_vec) 
            scores, indices = self.index.search(query_vec, top_k) 
            results = [] 
            for score, idx in zip(scores[0], indices[0]):
                if idx == -1 or score< min_similarity:
                    continue 
                chunk = self.chunks[idx] 
                results.append({
                    "text": chunk['text'],
                    "source": chunk['source'],
                    "chunk_id": chunk['chunk_id'],
                    "score": round(float(score),4) 
                })
                logger.info(f"Retrieved {len(results)} chunks for query: '{query}' ")
                return results 
        except Exception as e:
            raise CustomException(e,sys) 