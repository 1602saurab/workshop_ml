import os
import sys
import traceback

import faiss

from rag.vector_store import VectorStore
from src.utils import load_object


def main():
    print("\n========== VECTOR STORE SAVE TEST ==========\n")

    # Update these paths if your project config uses different paths.
    config = {
        "vector_store": {
            "faiss_index_path": os.path.join("artifacts", "faiss.index"),
            "vectorizer_path": os.path.join("artifacts", "vectorizer.pkl"),
            "chunks_metadata_path": os.path.join("artifacts", "chunks.pkl"),
        }
    }

    # Small sample data; this test does not need your document loader.
    chunks = [
        {"text": "Python is a programming language used for data science."},
        {"text": "FAISS supports efficient similarity search over vectors."},
        {"text": "Retrieval augmented generation uses retrieved context."},
        {"text": "TF-IDF represents text using term importance."},
    ]

    try:
        store = VectorStore(config)
        print("[1/4] Calling VectorStore.build()...")
        store.build(chunks)

        print("\n[2/4] Checking whether artifact files exist...")
        paths = {
            "FAISS index": config["vector_store"]["faiss_index_path"],
            "TF-IDF vectorizer": config["vector_store"]["vectorizer_path"],
            "Chunk metadata": config["vector_store"]["chunks_metadata_path"],
        }

        all_exist = True
        for label, path in paths.items():
            exists = os.path.isfile(path)
            size = os.path.getsize(path) if exists else 0
            print(f"{'PASS' if exists and size > 0 else 'FAIL'}: {label}: {path}"
                  + (f" ({size} bytes)" if exists else " (missing or empty)"))
            if not exists or size == 0:
                all_exist = False

        print("\n[3/4] Loading saved artifacts...")
        index = faiss.read_index(paths["FAISS index"])
        vectorizer = load_object(paths["TF-IDF vectorizer"])
        saved_chunks = load_object(paths["Chunk metadata"])

        print(f"PASS: FAISS index loaded; vectors={index.ntotal}, dimension={index.d}")
        print(f"PASS: Vectorizer loaded; vocabulary size={len(vectorizer.vocabulary_)}")
        print(f"PASS: Chunk metadata loaded; chunks={len(saved_chunks)}")

        print("\n[4/4] Validating artifact contents...")
        checks_pass = (
            index.ntotal == len(chunks)
            and len(vectorizer.vocabulary_) > 0
            and len(saved_chunks) == len(chunks)
        )
        print(f"{'PASS' if checks_pass else 'FAIL'}: Saved artifacts contain expected data")

        if all_exist and checks_pass:
            print("\nSUCCESS: Vector store artifacts were saved and loaded correctly.")
        else:
            print("\nFAILURE: One or more artifact checks failed.")
            sys.exit(1)

    except Exception as exc:
        print("\nTEST FAILED: An exception occurred.")
        print(f"{type(exc).__name__}: {exc}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()