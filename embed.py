"""
Embedding + Vector Store + Retrieval
=====================================
Embeds all chunks from document-ingestion.py using all-MiniLM-L6-v2
and stores them in ChromaDB with source metadata.

Architecture:
  document-ingestion.py  →  embed_and_retrieve.py  →  (Generation / Claude API)
"""

import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# ── Import chunks from your ingestion pipeline ────────────────────────────────
from document_ingestion import main as get_chunks   # reuses your existing pipeline

# ── Configuration ─────────────────────────────────────────────────────────────

EMBEDDING_MODEL  = "all-MiniLM-L6-v2"
CHROMA_DB_PATH   = "./chroma_db"        # folder where ChromaDB persists data
COLLECTION_NAME  = "uf_dining_guide"
TOP_K            = 5


# ── Setup ─────────────────────────────────────────────────────────────────────

print(f"\n{'='*55}")
print("  Embedding + Vector Store Setup")
print(f"{'='*55}")

# Load the embedding model
print(f"\n[1/3] Loading embedding model: {EMBEDDING_MODEL} ...")
model = SentenceTransformer(EMBEDDING_MODEL)
print("      → Model loaded")

# Set up ChromaDB persistent client
print(f"\n[2/3] Setting up ChromaDB at '{CHROMA_DB_PATH}' ...")
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Delete existing collection if it exists (clean re-index on each run)
existing = [c.name for c in client.list_collections()]
if COLLECTION_NAME in existing:
    client.delete_collection(COLLECTION_NAME)
    print(f"      → Deleted existing collection '{COLLECTION_NAME}'")

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},   # cosine similarity for sentence embeddings
)
print(f"      → Collection '{COLLECTION_NAME}' ready")


# ── Embed + Store ─────────────────────────────────────────────────────────────

print(f"\n[3/3] Running document ingestion pipeline ...")
chunks = get_chunks()   # returns list of chunk dicts from document-ingestion.py

print(f"\n      Embedding {len(chunks)} chunks ...")

# Batch embed all chunk texts at once (faster than one-by-one)
texts     = [c["text"]       for c in chunks]
ids       = [c["chunk_id"]   for c in chunks]
metadatas = [
    {
        "source":       str(c["metadata"].get("source",       "")),
        "doc_id":       str(c["metadata"].get("doc_id",       "")),
        "filename":     str(c["metadata"].get("filename",     "")),
        "chunk_index":  str(c["metadata"].get("chunk_index",  "")),
        "total_chunks": str(c["metadata"].get("total_chunks", "")),
    }
    for c in chunks
]

embeddings = model.encode(texts, show_progress_bar=True).tolist()

# Store in ChromaDB
collection.add(
    ids        = ids,
    documents  = texts,
    embeddings = embeddings,
    metadatas  = metadatas,
)

print(f"\n      → {collection.count()} chunks stored in ChromaDB")
print(f"\n{'='*55}")
print("  Embedding complete. Vector store ready.")
print(f"{'='*55}\n")


# ── Retrieve ──────────────────────────────────────────────────────────────────

def retrieve(query: str, top_k: int = TOP_K) -> list[dict]:
    """
    Embed a query string and return the top-k most relevant chunks.

    Args:
        query:  The user's question or search string.
        top_k:  Number of results to return (default 5).

    Returns:
        List of dicts with keys: chunk_id, text, source, doc_id, distance
    """
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings = query_embedding,
        n_results        = top_k,
        include          = ["documents", "metadatas", "distances"],
    )

    retrieved = []
    for i in range(len(results["ids"][0])):
        retrieved.append({
            "chunk_id": results["ids"][0][i],
            "text":     results["documents"][0][i],
            "source":   results["metadatas"][0][i].get("source",   ""),
            "doc_id":   results["metadatas"][0][i].get("doc_id",   ""),
            "filename": results["metadatas"][0][i].get("filename", ""),
            "distance": round(results["distances"][0][i], 4),
        })

    return retrieved


# ── Test Retrieval ─────────────────────────────────────────────────────────────

def print_results(query: str):
    """Helper to pretty-print retrieval results for a query."""
    print(f"\n{'─'*55}")
    print(f"  Query : \"{query}\"")
    print(f"{'─'*55}")
    results = retrieve(query)
    for i, r in enumerate(results, 1):
        print(f"\n  [{i}] {r['chunk_id']}")
        print(f"      Source   : {r['source']} (doc {r['doc_id']})")
        print(f"      Distance : {r['distance']}  (lower = more similar)")
        print(f"      Text     : {r['text'][:200]}...")
    print()


if __name__ == "__main__":
    # ── Run test queries to verify retrieval is working ───────────────────────
    test_queries = [
        "What meal plans are available for freshmen at UF?",
        "What are the best vegan restaurants near UF campus?",
        "How much does it cost to eat at Broward dining hall?",
        "What off-campus restaurants are near the University of Florida?",
        "What is the Bite Club meal plan?",
    ]

    print("\n" + "="*55)
    print("  Retrieval Test")
    print("="*55)

    for query in test_queries:
        print_results(query)