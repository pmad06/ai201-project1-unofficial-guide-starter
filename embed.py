"""
Embedding + Vector Store + Retrieval
=====================================
Embeds all chunks from document_ingestion.py using all-MiniLM-L6-v2
and stores them in ChromaDB with source metadata.

Run directly to build/rebuild the vector store:
    python embed.py

Import retrieve() in other scripts without triggering re-embedding:
    from embed import retrieve
"""

from sentence_transformers import SentenceTransformer
import chromadb

# ── Configuration ─────────────────────────────────────────────────────────────

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_DB_PATH  = "./chroma_db"
COLLECTION_NAME = "uf_dining_guide"
TOP_K           = 5

# ── These always run on import (fast — just loads model + connects to DB) ──────

model  = SentenceTransformer(EMBEDDING_MODEL)
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"},
)


# ── Retrieve (always available on import) ─────────────────────────────────────

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
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
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


# ── Everything below only runs when calling `python embed.py` directly ─────────

if __name__ == "__main__":
    from document_ingestion import main as get_chunks

    print(f"\n{'='*55}")
    print("  Embedding + Vector Store Setup")
    print(f"{'='*55}")

    # Rebuild collection from scratch
    print(f"\n[1/3] Loading embedding model: {EMBEDDING_MODEL} ...")
    print("      → Model loaded")

    print(f"\n[2/3] Setting up ChromaDB at '{CHROMA_DB_PATH}' ...")
    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)
        print(f"      → Deleted existing collection '{COLLECTION_NAME}'")

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    print(f"      → Collection '{COLLECTION_NAME}' ready")

    print(f"\n[3/3] Running document ingestion pipeline ...")
    chunks = get_chunks()

    print(f"\n      Embedding {len(chunks)} chunks ...")

    texts     = [c["text"]     for c in chunks]
    ids       = [c["chunk_id"] for c in chunks]
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

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"\n      → {collection.count()} chunks stored in ChromaDB")
    print(f"\n{'='*55}")
    print("  Embedding complete. Vector store ready.")
    print(f"{'='*55}\n")

    # ── Test retrieval ─────────────────────────────────────────────────────────
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
        print(f"\n{'─'*55}")
        print(f"  Query : \"{query}\"")
        print(f"{'─'*55}")
        for i, r in enumerate(retrieve(query), 1):
            print(f"\n  [{i}] {r['chunk_id']}")
            print(f"      Source   : {r['source']} (doc {r['doc_id']})")
            print(f"      Distance : {r['distance']}  (lower = more similar)")
            print(f"      Text     : {r['text'][:200]}...")
        print()