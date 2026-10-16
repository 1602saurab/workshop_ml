import os 
import sys 
from groq import Groq 
from src.exception import CustomException 
from src.logger import get_logger 
logger = get_logger(__name__) 

class Generator:
    def __init__(self, config:dict):
        self.config = config['generation'] 
        api_key = os.environ.get("GROQ_API_KEY") 
        if not api_key:
            logger.info("GROQ API KEY is not set- Geenrator will raise a clear error only when genrrate() is actually called..") 
        self.client = Groq(api_key=api_key) if api_key else None 

    def generate(self, query:str , retrieved_chunks:list):
        try:
            if not retrieved_chunks:
                return(
                    "I don't know the answer of this question.So please ocntact the doctor or clinic reception"
                )
            if self.client is None:
                raise RuntimeError(
                    "GROQ_API_KEY is not set"
                )
            context_blocks = "\n\n".join(
                f"[Source: {c['source']}]\n {c['text']}" for c in retrieved_chunks 
            )
            user_message = (
                f"Context experts from clinic knowledge base:\n\n{context_blocks}\n\n"
            )
            response = self.client.chat.completions.create(
                model=self.config['model'],
                max_tokens=self.config['max_tokens'],
                messages = [
                    {"role":"system", "content": self.config['system_prompt']},
                    {"role":"user", "content":user_message} 
                ]
            )
            answer = response.choices[0].message.content 
            logger.info(f"Generated answer for '{query}' : {answer[:100]}....") 
            return answer 
        
        except Exception as e :
            raise CustomException(e,sys) 