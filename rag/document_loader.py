import os 
import sys 
from src.exception import CustomException 
from src.logger import get_logger 
logger = get_logger(__name__)  

def load_documents(source_dir: str):
    try:
        documents = [] 
        for filename in sorted(os.listdir(source_dir)):
            if filename.endswith(".md"):
                filepath = os.path.join(source_dir, filename) 
                with open(filepath, 'r', encoding='utf-8')as f:
                    text = f.read() 
                documents.append({"source": filename, "text": text}) 
        logger.info(f"Laded {len(documents)} documents from {source_dir}")
        return documents 
    except Exception as e:
        raise CustomException(e,sys) 

def chunk_text(text:str, chunk_size: int , chunk_overlap:int):
    paragraphs = [p.strip() for p in text.split("\n\n")if p.strip()] 
    chunks = [] 
    current_chunk = "" 
    for para in paragraphs:
        if len(current_chunk) + len(para) <= chunk_size:
            current_chunk += ('\n\n' if current_chunk else "") + para 
        else:
            if current_chunk:
                chunks.append(current_chunk) 
            overlap_text = current_chunk[-chunk_overlap:] if current_chunk else "" 
            current_chunk = (overlap_text + "\n\n" + para).strip() 

    if current_chunk:
        chunks.append(current_chunk) 
    return chunks 


def build_chunks(source_dir: str , chunk_size: int , chunk_overlap:int):
    try:
        documents = load_documents(source_dir) 
        all_chunks = [] 
        for doc in documents:
            doc_chunks = chunk_text(doc['text'], chunk_size, chunk_overlap) 
            for i, chunk in enumerate(doc_chunks):
                all_chunks.append({
                    "source": doc['source'],
                    "chunk_id": i,
                    "text": chunk
                }) 

        logger.info(f"Built {len(all_chunks)} chunks from {len(documents)} documents.")
        return all_chunks 

    except Exception as e:
        raise CustomException(e,sys) 


