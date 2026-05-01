import json
import re
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# --------- Load JSON / JSONL ----------
def load_data(path):
    data = []
    
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith(".jsonl"):
            for line in f:
                if line.strip():  # avoid empty lines
                    data.append(json.loads(line))
        else:
            data = json.load(f)
    
    return data

# --------- Clean Text ----------
def clean(text):
    text = str(text).lower()  # safety: convert None → string
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

# --------- Preprocess ----------
def preprocess(data):
    texts = []
    
    for item in data:
        q = clean(item.get("question", ""))
        a = clean(item.get("answer", ""))
        
        if q and a:
            texts.append(f"{q} {a}")
    
    return texts

# --------- Create Embeddings ----------
def embed_texts(texts):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, convert_to_numpy=True,show_progress_bar=True)
    faiss.normalize_L2(embeddings)
    embeddings = embeddings.astype("float32")
    return embeddings, model

# --------- Build FAISS Index ----------
def build_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index

# --------- Save ----------
def save(index, texts):
    faiss.write_index(index, "fitness.index")
    
    with open("texts.json", "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)

# --------- Run ----------
if __name__ == "__main__":
    data = load_data("Fitness Q & A Dataset/fitness.jsonl")
    
    texts = preprocess(data)
    print("Samples:", len(texts))
    
    embeddings, _ = embed_texts(texts)
    
    index = build_index(embeddings)
    
    save(index, texts)
    
    print("✅ Done: embeddings + FAISS index created")