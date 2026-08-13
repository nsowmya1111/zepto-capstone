# Zepto Support Assistant

## Module 3 — Support Assistant

A small RAG-based GenAI service for answering questions about Zepto policies.

## Features

- 8 Zepto policy documents
- Local embeddings using `all-MiniLM-L6-v2`
- ChromaDB vector database
- LangGraph StateGraph with intent routing
- Pydantic structured output
- FastAPI `/ask` endpoint
- Deterministic offline `MOCK_LLM` mode
- Docker support

## Architecture

The RAG pipeline follows these stages:

### 1. Ingestion

The eight Zepto policy documents are stored in the `docs/` directory:

- `doc_01.txt` — Delivery Policy
- `doc_02.txt` — Returns & Refunds
- `doc_03.txt` — Membership Tiers
- `doc_04.txt` — Order Tracking
- `doc_05.txt` — Order Cancellation Policy
- `doc_06.txt` — Damaged or Missing Items
- `doc_07.txt` — Gift Cards
- `doc_08.txt` — Customer Support Hours

The ingestion code in `ingest.py` loads the documents and prepares them for vector storage.

### 2. Embedding

Each document chunk is embedded locally using the
`all-MiniLM-L6-v2` model from `sentence-transformers`.

No external LLM API is required for embeddings.

### 3. Retrieval

The embeddings are stored in ChromaDB in the local `chroma_db/`
directory.

For policy questions, the `retrieve_and_answer` LangGraph node embeds
the incoming query and retrieves the top-3 most similar chunks using
cosine similarity.

### 4. Generation

The LangGraph workflow contains three main nodes:

```text
User Query
    |
    v
classify_intent
    |
    +---- policy_question ----> retrieve_and_answer
    |                              |
    |                              v
    |                         ChromaDB Retrieval
    |                              |
    |                              v
    |                         Grounded Answer
    |
    +---- general_question ----> direct_answer
                                   |
                                   v
                              Direct Response