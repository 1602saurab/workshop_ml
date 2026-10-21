
import sys
import faiss
import numpy as np

from src.exception import CustomException
from src.logger import get_logger
from rag.vector_store import VectorStore

logger = get_logger(__name__)


class Retriever:

    def __init__(self, config: dict):
        self.config = config["retrieval"]

        self.vector_store = VectorStore(config)

        self.vectorizer, self.index, self.chunks = (
            self.vector_store.load()
        )

        logger.info(
            f"Retriever ready with {len(self.chunks)} indexed chunks"
        )

    def retrieve(self, query: str):
        try:
            query = query.strip()

            if not query:
                logger.warning("Empty query received by retriever")
                return []

            top_k = self.config["top_k"]
            min_similarity = self.config["min_similarity"]

            # Convert query into a TF-IDF vector
            query_vec = (
                self.vectorizer
                .transform([query])
                .toarray()
                .astype("float32")
            )

            # Normalize query vector for cosine similarity
            faiss.normalize_L2(query_vec)

            # Search the FAISS index
            scores, indices = self.index.search(
                query_vec,
                top_k
            )

            results = []

            # Collect ALL chunks above the threshold
            for score, idx in zip(scores[0], indices[0]):

                # Ignore invalid indices
                if idx == -1:
                    continue

                # Ignore chunks below the similarity threshold
                if score < min_similarity:
                    continue

                chunk = self.chunks[idx]

                results.append({
                    "text": chunk["text"],
                    "source": chunk["source"],
                    "chunk_id": chunk["chunk_id"],
                    "score": round(float(score), 4)
                })

            # Log after processing every result
            logger.info(
                f"Retrieved {len(results)} chunks for query: '{query}'"
            )

            # IMPORTANT: Return outside the loop
            return results

        except Exception as e:
            logger.exception("Document retrieval failed")
            raise CustomException(e, sys) from e
