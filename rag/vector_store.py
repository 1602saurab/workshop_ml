import os 
import sys 
import faiss 
import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer 

from src.exception import CustomException 
from src.logger import get_logger 
from src.utils import load_object, save_object 
logger = get_logger(__name__) 

class VectorStore:
    def __init__(self, config:dict):
        self.config = config['vector_store'] 

    def build(self, chunks:list):
        logger.info("RAG STAGE: VECTOR STORE BUILD STARTED....") 
        try:
            texts = [c['text'] for c in chunks] 
            vectorizer = TfidfVectorizer(max_features=1000, stop_words='english') 
            tfidf_matrix = vectorizer.fit_transform(texts).toarray().astype('float32') 
            faiss.normalize_L2(tfidf_matrix) 
            dimension = tfidf_matrix.shape[1] 
            index = faiss.IndexFlatIP(dimension) 
            index.add(tfidf_matrix) 

            os.makedirs(os.path.dirname(self.config['faiss_index_path']), exist_ok=True) 
            faiss.write_index(index, self.config['faiss_index_path']) 
            save_object(self.config['vectorizer_path'], vectorizer) 
            save_object(self.config['chunks_metadata_path'], chunks) 
            logger.info(
                f"Vector store built: {len(chunks)} chunks, {dimension}--dim TF-IDF vectors",
                f"FAISS IndexFlatIP saved at {self.config['faiss_index_path']}"
            )
            logger.info(f"-----------RAG STAGE: VECTOR STORE BUILD COMPLETED----------") 

        except Exception as e:
            raise CustomException(e,sys) 

    def load(self):
        try:
            vectorizer = load_object(self.config['vectorizer_path']) 
            index = faiss.read_index(self.config['faiss_index_path']) 
            chunks = load_object(self.config['chunks_metadata_path']) 
            return vectorizer, index, chunks 
        except  Exception as e:
            raise CustomException(e,sys) 