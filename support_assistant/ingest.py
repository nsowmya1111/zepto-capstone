from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


PROJECT_DIR = Path(__file__).parent
DOCUMENT_FOLDER = PROJECT_DIR / "docs"
VECTOR_STORE = PROJECT_DIR / "chroma_db"


def read_policy_files():
    texts = []
    file_ids = []

    for document in sorted(DOCUMENT_FOLDER.glob("doc_*.txt")):
        content = document.read_text(encoding="utf-8").strip()

        if content:
            file_ids.append(document.stem)
            texts.append(content)

    return file_ids, texts


def build_vector_store(file_ids, texts):
    encoder = SentenceTransformer("all-MiniLM-L6-v2")

    vectors = encoder.encode(
        texts,
        convert_to_numpy=True
    ).tolist()

    db = chromadb.PersistentClient(path=str(VECTOR_STORE))

    policies = db.get_or_create_collection(
        name="zepto_policies",
        metadata={"hnsw:space": "cosine"}
    )

    policies.upsert(
        ids=file_ids,
        documents=texts,
        embeddings=vectors
    )

    return policies


def main():
    ids, texts = read_policy_files()

    print("Documents found:", len(texts))

    collection = build_vector_store(ids, texts)

    print("Collection:", collection.name)
    print("Documents stored:", collection.count())
    print("Embedding process completed.")


if __name__ == "__main__":
    main()