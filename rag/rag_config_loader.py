import sys
import yaml

from src.exception import CustomException
from src.logger import get_logger

logger = get_logger(__name__)

RAG_CONFIG_PATH = "rag/config/rag_config.yaml"
_rag_config_cache = None


def load_rag_config(config_path: str = RAG_CONFIG_PATH) -> dict:
    global _rag_config_cache
    try:
        if _rag_config_cache is not None:
            return _rag_config_cache

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        logger.info(f"RAG config loaded from: {config_path}")
        _rag_config_cache = config
        return config

    except Exception as e:
        raise CustomException(e, sys)