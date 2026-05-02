# import json
# import re
# import numpy as np
# import faiss
# from sentence_transformers import SentenceTransformer


# # ─────────────────────────────────────────────
# # 1. LOAD
# # ─────────────────────────────────────────────
# def load_data(path: str) -> list[dict]:
#     data = []
#     with open(path, "r", encoding="utf-8") as f:
#         if path.endswith(".jsonl"):
#             for line in f:
#                 line = line.strip()
#                 if line:
#                     data.append(json.loads(line))
#         else:
#             data = json.load(f)
#     return data


# # ─────────────────────────────────────────────
# # 2. CLEAN  (must match app.py exactly)
# # ─────────────────────────────────────────────
# def clean(text: str) -> str:
#     text = str(text).lower()
#     text = re.sub(r"\s+", " ", text)
#     text = re.sub(r"[^\w\s]", "", text)   # removes punctuation
#     return text.strip()


# # ─────────────────────────────────────────────
# # 3. PREPROCESS
# #    FIX: index the QUESTION only as the search vector,
# #         but store the full "Q + A" string for the LLM context.
# #    This gives much cleaner semantic matching because a user's
# #    query is structurally a question, not a question+answer blob.
# # ─────────────────────────────────────────────
# def preprocess(data: list[dict]) -> tuple[list[str], list[str]]:
#     """
#     Returns
#     -------
#     index_texts   : cleaned question strings  → used to build FAISS vectors
#     display_texts : full Q+A strings          → stored in texts.json for the LLM
#     """
#     index_texts   = []
#     display_texts = []

#     skipped = 0
#     for item in data:
#         q = clean(item.get("question", ""))
#         a = clean(item.get("answer",   ""))

#         if not q or not a:
#             skipped += 1
#             continue

#         index_texts.append(q)                         # embed question only
#         display_texts.append(f"Q: {q}\nA: {a}")       # full pair for context

#     print(f"✅ Loaded {len(index_texts)} pairs  |  ⚠️  Skipped {skipped} empty rows")
#     return index_texts, display_texts


# # ─────────────────────────────────────────────
# # 4. EMBED
# # ─────────────────────────────────────────────
# def embed_texts(texts: list[str], model_name: str = "all-MiniLM-L6-v2"):
#     model = SentenceTransformer(model_name)
#     print(f"Encoding {len(texts)} texts with '{model_name}' …")
#     embeddings = model.encode(
#         texts,
#         convert_to_numpy=True,
#         show_progress_bar=True,
#         batch_size=64,
#     )
#     faiss.normalize_L2(embeddings)          # cosine similarity via inner product
#     return embeddings.astype("float32"), model


# # ─────────────────────────────────────────────
# # 5. BUILD FAISS INDEX
# # ─────────────────────────────────────────────
# def build_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
#     dim   = embeddings.shape[1]
#     index = faiss.IndexFlatIP(dim)          # inner product = cosine after L2-norm
#     index.add(embeddings)
#     print(f"FAISS index built  |  {index.ntotal} vectors  |  dim={dim}")
#     return index


# # ─────────────────────────────────────────────
# # 6. SAVE
# # ─────────────────────────────────────────────
# def save(index: faiss.IndexFlatIP, display_texts: list[str]) -> None:
#     faiss.write_index(index, "fitness.index")
#     with open("texts.json", "w", encoding="utf-8") as f:
#         json.dump(display_texts, f, ensure_ascii=False, indent=2)
#     print("💾  Saved  →  fitness.index  +  texts.json")


# # ─────────────────────────────────────────────
# # 7. MAIN
# # ─────────────────────────────────────────────
# if __name__ == "__main__":
#     DATASET_PATH = "Fitness Q & A Dataset/fitness.jsonl"

#     data = load_data(DATASET_PATH)
#     print(f"Raw rows loaded: {len(data)}")

#     index_texts, display_texts = preprocess(data)

#     embeddings, _ = embed_texts(index_texts)

#     index = build_index(embeddings)

#     save(index, display_texts)

#     print("\n✅  All done — re-run app.py to test the chatbot.")

"""
embed.py — Next Rep Fitness RAG
================================
Reads the knowledge-base PDF, splits it into clean overlapping
chunks (section-aware), embeds with sentence-transformers, and saves:

  • fitness.index   — FAISS inner-product index (cosine after L2-norm)
  • texts.json      — list of readable display chunks passed to the LLM

Run once (or whenever the PDF changes):
    python embed.py
"""

import json
import re
import os
import pdfplumber
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


# ─────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────
PDF_PATH     = os.path.join("KnowledgeBase", "Fitness_RAG_Knowledge_Base.pdf")
INDEX_OUT    = os.path.join("KnowledgeBase", "fitness.index")
TEXTS_OUT    = os.path.join("KnowledgeBase", "texts.json")
MODEL_NAME   = "all-MiniLM-L6-v2"

CHUNK_WORDS  = 400   # target words per chunk
OVERLAP_WORDS= 60    # word overlap between consecutive chunks
MIN_WORDS    = 12    # discard micro-fragments shorter than this


# ─────────────────────────────────────────────────────────
# 1. EXTRACT TEXT FROM PDF
# ─────────────────────────────────────────────────────────
def extract_pdf(path: str) -> str:
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t and t.strip():
                pages.append(t.strip())
    full = "\n\n".join(pages)
    print(f"Extracted {len(pages)} pages | {len(full):,} chars")
    return full


# ─────────────────────────────────────────────────────────
# 2. LIGHT CLEAN (keeps readable sentence structure)
# ─────────────────────────────────────────────────────────
def light_clean(text: str) -> str:
    # Remove repetitive page headers/footers
    text = re.sub(r"NEXT REP FITNESS \|.*?\n", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Confidential.*?\n",         "", text, flags=re.IGNORECASE)
    text = re.sub(r"Page \d+\s*\n",             "", text, flags=re.IGNORECASE)
    # Collapse 3+ blank lines → 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Collapse multiple spaces within a line
    lines = [re.sub(r" {2,}", " ", ln) for ln in text.splitlines()]
    return "\n".join(lines).strip()


# ─────────────────────────────────────────────────────────
# 3. SECTION-AWARE SPLITTING
# ─────────────────────────────────────────────────────────
def split_sections(text: str) -> list[dict]:
    """
    Detect section headings like "SECTION 12: FITNESS BASICS — Q&A"
    and pair each with its body text.
    Returns list of {"section": str, "body": str}
    """
    pattern = re.compile(r"(SECTION\s+\d+\s*[:\-—]\s*.+)", re.IGNORECASE)
    parts   = pattern.split(text)
    # parts = [pre_text, heading1, body1, heading2, body2, ...]

    sections = []

    if parts[0].strip():
        sections.append({"section": "Introduction / Overview", "body": parts[0].strip()})

    i = 1
    while i < len(parts) - 1:
        heading = parts[i].strip()
        body    = parts[i + 1].strip() if (i + 1) < len(parts) else ""
        if body:
            sections.append({"section": heading, "body": body})
        i += 2

    print(f"Split into {len(sections)} sections")
    return sections


# ─────────────────────────────────────────────────────────
# 4. WORD-WINDOW CHUNKING WITH OVERLAP
# ─────────────────────────────────────────────────────────
def chunk_body(section_label: str, body: str) -> list[dict]:
    ws     = body.split()
    chunks = []
    start  = 0
    while start < len(ws):
        end  = min(start + CHUNK_WORDS, len(ws))
        blob = " ".join(ws[start:end])
        chunks.append({"section": section_label, "text": blob})
        if end == len(ws):
            break
        start += CHUNK_WORDS - OVERLAP_WORDS
    return chunks


def build_all_chunks(sections: list[dict]) -> list[dict]:
    all_chunks = []
    for sec in sections:
        all_chunks.extend(chunk_body(sec["section"], sec["body"]))
    print(f"Total chunks: {len(all_chunks)}")
    return all_chunks


# ─────────────────────────────────────────────────────────
# 5. PREPARE INDEX vs DISPLAY TEXTS
#    • display_text  → stored in texts.json, sent to LLM as-is (readable)
#    • index_text    → aggressively cleaned, ONLY used for the embedding
#
#    KEY LESSON from v1: the same cleaning must be applied to BOTH
#    the stored vectors AND the query at search-time. This is done
#    in app.py via the identical clean_for_embedding() function.
# ─────────────────────────────────────────────────────────
def clean_for_embedding(text: str) -> str:
    """Lowercase + strip punctuation. Used for VECTORS only, not display."""
    text = str(text).lower()
    text = re.sub(r"\s+",      " ", text)
    text = re.sub(r"[^\w\s]",  "", text)
    return text.strip()


def prepare_texts(chunks: list[dict]) -> tuple[list[str], list[str]]:
    index_texts   = []   # what gets embedded into FAISS
    display_texts = []   # what gets stored in texts.json for the LLM

    for c in chunks:
        display = f"[{c['section']}]\n{c['text']}"
        index   = clean_for_embedding(c["section"] + " " + c["text"])

        if len(index.split()) < MIN_WORDS:
            continue

        index_texts.append(index)
        display_texts.append(display)

    print(f"Kept {len(index_texts)} chunks after filtering")
    return index_texts, display_texts


# ─────────────────────────────────────────────────────────
# 6. EMBED
# ─────────────────────────────────────────────────────────
def embed(texts: list[str]) -> np.ndarray:
    model = SentenceTransformer(MODEL_NAME)
    print(f"Encoding {len(texts)} chunks with '{MODEL_NAME}' ...")
    vecs = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True,
        batch_size=64,
    )
    faiss.normalize_L2(vecs)          # enables cosine via inner product
    return vecs.astype("float32")


# ─────────────────────────────────────────────────────────
# 7. BUILD FAISS INDEX
# ─────────────────────────────────────────────────────────
def build_index(vecs: np.ndarray) -> faiss.IndexFlatIP:
    dim   = vecs.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vecs)
    print(f"FAISS index: {index.ntotal} vectors | dim={dim}")
    return index


# ─────────────────────────────────────────────────────────
# 8. SAVE
# ─────────────────────────────────────────────────────────
def save(index: faiss.IndexFlatIP, display_texts: list[str]) -> None:
    faiss.write_index(index, INDEX_OUT)
    with open(TEXTS_OUT, "w", encoding="utf-8") as f:
        json.dump(display_texts, f, ensure_ascii=False, indent=2)
    print(f"Saved: {INDEX_OUT}  +  {TEXTS_OUT}")


# ─────────────────────────────────────────────────────────
# 9. MAIN
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  Next Rep — PDF Embedding Pipeline")
    print("=" * 50)

    raw      = extract_pdf(PDF_PATH)
    cleaned  = light_clean(raw)
    sections = split_sections(cleaned)
    chunks   = build_all_chunks(sections)

    index_texts, display_texts = prepare_texts(chunks)

    vecs  = embed(index_texts)
    index = build_index(vecs)
    save(index, display_texts)

    print("\nDone — run:  streamlit run app.py")