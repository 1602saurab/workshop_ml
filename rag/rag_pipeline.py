# import sys 
# from src.exception import CustomException 
# from src.logger import get_logger 
# from rag.generator import Generator 
# from rag.retriever import Retriever 
# from rag.rag_config_loader import load_rag_config 
# logger = get_logger(__name__) 

# class RAGPipeline:
#     def __init__(self):
#         self.config = load_rag_config() 
#         self.retriever = Retriever(self.config)
#         self.generator = Generator(self.config) 

#     def answer(self, query:str):
#         try:
#             logger.info(f"RAG query received: '{query}' ") 
#             retrieved_chunks = self.retriever.retrieve(query) 
#             answer_text = self.generator.generate(query, retrieved_chunks) 

#             sources = sorted({c['source'] for c in retrieved_chunks}) 
#             response = {
#                 "answer": answer_text,
#                 "sources": sources,
#                 "retrieved_chunks": retrieved_chunks
#             }
#             logger.info(f"RAG answer generated. Source used: {sources}") 
#             return response 
#         except Exception as e:
#             raise CustomException(e,sys)  



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

    def answer(self, query: str):
        try:
            query = query.strip()

            if not query:
                return {
                    "answer": "Please enter a question.",
                    "sources": [],
                    "retrieved_chunks": []
                }

            logger.info(f"RAG query received: '{query}'")

            # Step 1: Retrieve relevant document chunks
            retrieved_chunks = self.retriever.retrieve(query)

            # Step 2: Handle None or empty retrieval results
            if retrieved_chunks is None:
                logger.warning(
                    "Retriever returned None. Using empty context."
                )
                retrieved_chunks = []

            # Ensure the retriever returns a list
            if not isinstance(retrieved_chunks, list):
                raise TypeError(
                    "Retriever must return a list of chunks, "
                    f"but received {type(retrieved_chunks).__name__}."
                )

            # Step 3: Generate the answer
            answer_text = self.generator.generate(
                query,
                retrieved_chunks
            )

            # Step 4: Collect source names safely
            sources = sorted({
                chunk["source"]
                for chunk in retrieved_chunks
                if isinstance(chunk, dict)
                and chunk.get("source")
            })

            # Step 5: Build the response
            response = {
                "answer": answer_text,
                "sources": sources,
                "retrieved_chunks": retrieved_chunks
            }

            logger.info(
                f"RAG answer generated. Sources: {sources}"
            )

            return response

        except Exception as e:
            logger.exception("RAG pipeline failed")
            raise CustomException(e, sys) from e
