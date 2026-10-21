
import os
import sys

from dotenv import load_dotenv
from groq import Groq

from src.exception import CustomException
from src.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class Generator:

    def __init__(self, config: dict):
        self.config = config["generation"]

        api_key = os.environ.get("GROQ_API_KEY")

        if not api_key:
            logger.warning(
                "GROQ_API_KEY is not set. "
                "Generation will fail if requested."
            )

        self.client = Groq(api_key=api_key) if api_key else None

    def generate(self, query: str, retrieved_chunks: list):
        try:
            query = query.strip()

            if not query:
                return "Please enter a question."

            if self.client is None:
                raise RuntimeError(
                    "GROQ_API_KEY is not configured."
                )

            # Handle missing retrieval results
            if not retrieved_chunks:
                return (
                    "I couldn't find relevant information in the "
                    "clinic knowledge base. Please consult your "
                    "doctor or clinic reception for guidance."
                )

            # Build context from retrieved document chunks
            context_blocks = "\n\n".join(
                (
                    f"[Source: {chunk.get('source', 'Unknown')}]\n"
                    f"{chunk.get('text', '')}"
                )
                for chunk in retrieved_chunks
                if isinstance(chunk, dict) and chunk.get("text")
            )

            if not context_blocks.strip():
                return (
                    "I couldn't find usable information in the "
                    "clinic knowledge base. Please consult your "
                    "doctor or clinic reception."
                )

            # IMPORTANT: Include BOTH the context and actual question
            user_message = f"""
Clinic knowledge base context:

{context_blocks}

Patient's question:
{query}

Instructions:
- Answer the patient's question directly.
- Understand the question even if it is written in Hinglish.
- Respond in the language used by the patient when practical.
- Use only relevant information from the supplied context.
- If the context does not answer the question, clearly say so.
- Do not invent medical facts or recommendations.
- Do not prescribe medicines or dosages.
- Mention the relevant source or topic when possible.
- Keep the answer concise, around 3-5 sentences.
- Explain that the response is general information, not a diagnosis.
"""

            response = self.client.chat.completions.create(
                model=self.config["model"],
                max_tokens=self.config["max_tokens"],
                messages=[
                    {
                        "role": "system",
                        "content": self.config["system_prompt"]
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )

            answer = response.choices[0].message.content

            if not answer or not answer.strip():
                raise RuntimeError(
                    "Groq returned an empty response."
                )

            answer = answer.strip()

            logger.info(
                f"Generated answer for '{query}': "
                f"{answer[:100]}..."
            )

            return answer

        except Exception as e:
            logger.exception("Answer generation failed")
            raise CustomException(e, sys) from e
