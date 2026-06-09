"""
Document Ingestion & Chunking Pipeline
=======================================
Loads all .txt files, cleans them, and chunks them using
LangChain's RecursiveCharacterTextSplitter.

Chunk size : 300 words  (≈ 1 800 chars at ~6 chars/word)
Overlap    : 30  words  (≈  180 chars)
"""

import os
import re
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ── Configuration ─────────────────────────────────────────────────────────────

DOCS_DIR    = "./documents"          # folder that holds your .txt files
print(os.listdir(DOCS_DIR))

CHUNK_SIZE  = 300               # target chunk size in characters
CHUNK_OVERLAP = 30              # overlap in characters

# Source metadata — keyed by filename (without extension).
# Add / edit entries to match your actual filenames.
SOURCE_METADATA = {
    "broward-reopening":     {"source": "The Alligator",             "doc_id": 4},
    "conference-guide":      {"source": "Conference Guide",          "doc_id": 6},
    "florida-fresh-dining":  {"source": "UF Florida Fresh Dining",   "doc_id": 2},
    "neurology":             {"source": "UF Dept of Neurology",      "doc_id": 9},
    "off-campus-alligator":  {"source": "The Alligator",             "doc_id": 5},
    "prked":                 {"source": "Prked",                     "doc_id": 7},
    "reddit":                {"source": "Reddit Thread",             "doc_id": 1},
    "spoon-university":      {"source": "Spoon University",          "doc_id": 8},
    "student-meal-plans":    {"source": "The Alligator",             "doc_id": 10},
    "swamprentals":          {"source": "SwampRentals",              "doc_id": 3},
}



# ── Cleaning ──────────────────────────────────────────────────────────────────

def clean_text(text: str) -> str:
    """
    Normalise raw scraped / copy-pasted text:
      1. Collapse runs of whitespace / blank lines
      2. Strip leading/trailing whitespace per line
      3. Remove non-printable / control characters
      4. Normalise unicode dashes and quotes to ASCII equivalents
    """
   # Remove "Source: ..." and "URL: ..." header lines
    text = re.sub(r"^(Source|URL):.*$", "", text, flags=re.MULTILINE)

    # Remove non-printable control characters (keep newlines/tabs)
    text = re.sub(r"[^\x09\x0A\x0D\x20-\x7E\u00A0-\uFFFF]", " ", text)

    # Strip leading punctuation/whitespace from chunk boundaries
    text = re.sub(r"^[\s.,;:]+", "", text)

    # Normalise unicode punctuation
    text = (
        text.replace("\u2018", "'").replace("\u2019", "'")   # curly single quotes
            .replace("\u201C", '"').replace("\u201D", '"')   # curly double quotes
            .replace("\u2013", "-").replace("\u2014", "-")   # en/em dashes
            .replace("\u00A0", " ")                          # non-breaking space
    )

    # Strip trailing whitespace on each line
    lines = [line.rstrip() for line in text.splitlines()]

    # Collapse 3+ consecutive blank lines down to 2
    cleaned_lines: list[str] = []
    blank_count = 0
    for line in lines:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= 2:
                cleaned_lines.append("")
        else:
            blank_count = 0
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


# ── Loading ───────────────────────────────────────────────────────────────────

def load_txt_files(directory: str) -> list[dict]:
    """
    Walk *directory* and load every .txt file with open() / .read().
    Returns a list of dicts: {filename, stem, raw_text, metadata}.
    """
    docs_path = Path(directory)
    if not docs_path.exists():
        raise FileNotFoundError(f"Directory not found: {docs_path.resolve()}")

    documents = []
    txt_files = sorted(docs_path.glob("*.txt"))

    if not txt_files:
        print(f"[WARNING] No .txt files found in '{docs_path.resolve()}'")
        return documents

    for filepath in txt_files:
        stem = filepath.stem                        # filename without extension
        with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
            raw_text = fh.read()

        meta = SOURCE_METADATA.get(stem, {"source": stem, "doc_id": None})
        meta["filename"] = filepath.name

        documents.append({
            "filename":  filepath.name,
            "stem":      stem,
            "raw_text":  raw_text,
            "metadata":  meta,
        })
        print(f"  Loaded  : {filepath.name}  ({len(raw_text):,} chars)")

    return documents


# ── Chunking ──────────────────────────────────────────────────────────────────

def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Clean each document then split with RecursiveCharacterTextSplitter.
    Returns a flat list of chunk dicts ready for embedding.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        # Prefer natural break points: paragraph > sentence > word
        separators=["\n\n", "\n", ". ", "! ", "? ", ", ", " ", ""],
        length_function=len,
        is_separator_regex=False,
    )

    all_chunks: list[dict] = []

    for doc in documents:
        cleaned = clean_text(doc["raw_text"])
        splits  = splitter.split_text(cleaned)

        splits = [s for s in splits if len(s.strip()) > 50]

        for idx, chunk_text in enumerate(splits):
            all_chunks.append({
                "chunk_id":   f"{doc['stem']}_chunk_{idx:04d}",
                "text":       chunk_text,
                "metadata": {
                    **doc["metadata"],
                    "chunk_index":  idx,
                    "total_chunks": len(splits),
                },
            })

        print(f"  Chunked : {doc['filename']}  →  {len(splits)} chunks")

    return all_chunks


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*55}")
    print("  Document Ingestion & Chunking Pipeline")
    print(f"{'='*55}")
    print(f"  Docs dir     : {DOCS_DIR}")
    print(f"  Chunk size   : {CHUNK_SIZE} chars")
    print(f"  Chunk overlap: {CHUNK_OVERLAP} chars")
    print(f"{'='*55}\n")

    # 1. Load
    print("[1/3] Loading .txt files …")
    documents = load_txt_files(DOCS_DIR)
    print(f"      → {len(documents)} file(s) loaded\n")

    # 2. Chunk
    print("[2/3] Cleaning & chunking …")
    chunks = chunk_documents(documents)
    print(f"      → {len(chunks)} total chunks produced\n")

    # 3. Summary
    print("[3/3] Summary")
    print(f"{'─'*55}")
    print(f"  {'File':<35} {'Chunks':>6}")
    print(f"{'─'*55}")

    from collections import defaultdict
    counts: dict[str, int] = defaultdict(int)
    for c in chunks:
        counts[c["metadata"]["filename"]] += 1
    for fname, n in counts.items():
        print(f"  {fname:<35} {n:>6}")

    print(f"{'─'*55}")
    print(f"  {'TOTAL':<35} {len(chunks):>6}")
    print(f"{'─'*55}\n")

    # Return chunks for the next pipeline stage (embedding)
    return chunks


if __name__ == "__main__":
    chunks = main()

    # ── Quick sanity-check: print the first chunk ──────────────────────────
    if chunks:
        first = chunks[0]
        print("── First chunk preview ──────────────────────────────────")
        print(f"  ID       : {first['chunk_id']}")
        print(f"  Source   : {first['metadata']['source']}")
        print(f"  Doc ID   : {first['metadata']['doc_id']}")
        print(f"  Chars    : {len(first['text'])}")
        print(f"  Text     :\n\n{first['text']}\n")

# Print 5 random chunks from different sources
    import random
    seen_sources = set()
    sample_chunks = []

    shuffled = random.sample(chunks, len(chunks))
    for chunk in shuffled:
        source = chunk['metadata']['source']
        if source not in seen_sources:
            seen_sources.add(source)
            sample_chunks.append(chunk)
        if len(sample_chunks) == 5:
            break

    print("\n── 5 Random Chunks from Different Sources ──────────────")
    for i, chunk in enumerate(sample_chunks, 1):
        print(f"\n[{i}] ID      : {chunk['chunk_id']}")
        print(f"    Source  : {chunk['metadata']['source']}")
        print(f"    Doc ID  : {chunk['metadata']['doc_id']}")
        print(f"    Chars   : {len(chunk['text'])}")
        print(f"    Text    : {chunk['text'][:200]}...")
        print(f"{'─'*55}")