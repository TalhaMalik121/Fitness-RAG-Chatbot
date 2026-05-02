import json
import re
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


# ─────────────────────────────────────────────
# 1. LOAD
# ─────────────────────────────────────────────
def load_data(path: str) -> list[dict]:
    data = []
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith(".jsonl"):
            for line in f:
                line = line.strip()
                if line:
                    data.append(json.loads(line))
        else:
            data = json.load(f)
    return data


# ─────────────────────────────────────────────
# 2. CLEAN  (must match app.py exactly)
# ─────────────────────────────────────────────
def clean(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)   # removes punctuation
    return text.strip()


# ─────────────────────────────────────────────
# 3. PREPROCESS
#    FIX: index the QUESTION only as the search vector,
#         but store the full "Q + A" string for the LLM context.
#    This gives much cleaner semantic matching because a user's
#    query is structurally a question, not a question+answer blob.
# ─────────────────────────────────────────────
def preprocess(data: list[dict]) -> tuple[list[str], list[str]]:
    """
    Returns
    -------
    index_texts   : cleaned question strings  → used to build FAISS vectors
    display_texts : full Q+A strings          → stored in texts.json for the LLM
    """
    index_texts   = []
    display_texts = []

    skipped = 0
    for item in data:
        q = clean(item.get("question", ""))
        a = clean(item.get("answer",   ""))

        if not q or not a:
            skipped += 1
            continue

        index_texts.append(q)                         # embed question only
        display_texts.append(f"Q: {q}\nA: {a}")       # full pair for context

    print(f"✅ Loaded {len(index_texts)} pairs  |  ⚠️  Skipped {skipped} empty rows")
    return index_texts, display_texts


# ─────────────────────────────────────────────
# 4. EMBED
# ─────────────────────────────────────────────
def embed_texts(texts: list[str], model_name: str = "all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    print(f"Encoding {len(texts)} texts with '{model_name}' …")
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True,
        batch_size=64,
    )
    faiss.normalize_L2(embeddings)          # cosine similarity via inner product
    return embeddings.astype("float32"), model


# ─────────────────────────────────────────────
# 5. BUILD FAISS INDEX
# ─────────────────────────────────────────────
def build_index(embeddings: np.ndarray) -> faiss.IndexFlatIP:
    dim   = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)          # inner product = cosine after L2-norm
    index.add(embeddings)
    print(f"FAISS index built  |  {index.ntotal} vectors  |  dim={dim}")
    return index


# ─────────────────────────────────────────────
# 6. SAVE
# ─────────────────────────────────────────────
def save(index: faiss.IndexFlatIP, display_texts: list[str]) -> None:
    faiss.write_index(index, "fitness.index")
    with open("texts.json", "w", encoding="utf-8") as f:
        json.dump(display_texts, f, ensure_ascii=False, indent=2)
    print("💾  Saved  →  fitness.index  +  texts.json")


# ─────────────────────────────────────────────
# 7. MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    DATASET_PATH = "Fitness Q & A Dataset/fitness.jsonl"

    data = load_data(DATASET_PATH)
    print(f"Raw rows loaded: {len(data)}")

    index_texts, display_texts = preprocess(data)

    embeddings, _ = embed_texts(index_texts)

    index = build_index(embeddings)

    save(index, display_texts)

    print("\n✅  All done — re-run app.py to test the chatbot.")