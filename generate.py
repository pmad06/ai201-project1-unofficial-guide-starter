"""
Generation
==========
Takes a query string + top-5 retrieved chunks from ChromaDB
and generates an answer using Groq's llama-3.3-70b-versatile.

Source attribution is guaranteed programmatically — not left to the LLM.
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

# ── Groq client ───────────────────────────────────────────────────────────────

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL    = "llama-3.3-70b-versatile"
MAX_TOKENS = 1024

# ── System prompt ─────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a helpful dining and meal plan guide for students at the University of Florida (UF).

You will be given a question and a set of context passages retrieved from UF dining and restaurant documents.

Rules you must follow:
1. Answer ONLY using the information found in the provided context passages.
2. Do NOT use any outside knowledge or make assumptions beyond what is in the context.
3. If the context does not contain enough information to answer the question, respond with exactly: "I don't have enough information on that."
4. Be concise and helpful. Write in a friendly tone suited for a college student.
5. Do not mention the context passages or that you are reading from documents — just answer naturally.
"""

# ── Generate ──────────────────────────────────────────────────────────────────

def generate(query: str, chunks: list[dict]) -> dict:
    """
    Generate an answer from retrieved chunks using Groq.

    Args:
        query:  The user's question.
        chunks: List of chunk dicts from retrieve(), each with 'text' and 'source'.

    Returns:
        Dict with:
            'answer'  — the LLM's response string
            'sources' — deduplicated list of source document names (guaranteed)
    """

    # ── 1. Extract sources programmatically before calling the LLM ────────────
    sources = []
    seen    = set()
    for chunk in chunks:
        source = chunk.get("source", "Unknown Source")
        if source not in seen:
            seen.add(source)
            sources.append(source)

    # ── 2. Build the context block from retrieved chunks ──────────────────────
    context_block = ""
    for i, chunk in enumerate(chunks, 1):
        context_block += f"[Passage {i}]\n{chunk['text'].strip()}\n\n"

    # ── 3. Build the user message ─────────────────────────────────────────────
    user_message = f"""Context:
{context_block.strip()}

Question: {query}"""

    # ── 4. Call Groq API ──────────────────────────────────────────────────────
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
    )

    answer = response.choices[0].message.content.strip()

    return {
        "answer":  answer,
        "sources": sources,
    }


# ── Quick test ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Import retrieve from embed.py to run a quick end-to-end test
    from embed import retrieve

    test_queries = [
        "What meal plans are available for freshmen at UF?",
        "What are the best vegan restaurants near UF campus?",
        "How much does it cost to eat at Broward dining hall?",
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"  Q: {query}")
        print(f"{'='*60}")

        chunks = retrieve(query)
        result = generate(query, chunks)

        print(f"\n  Answer:\n  {result['answer']}")
        print(f"\n  Sources: {', '.join(result['sources'])}")