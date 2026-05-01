import json
import faiss
import numpy as np
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# -------- Load data --------
index = faiss.read_index("fitness.index")

with open("texts.json", "r", encoding="utf-8") as f:
    texts = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

# -------- Search function --------
def search(query, k=3):
    query_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, k)

    results = []
    for i, idx in enumerate(indices[0]):
        results.append({
            "text": texts[idx],
            "score": float(distances[0][i])
        })
    return results


# -------- Test loop --------
if __name__ == "__main__":
    while True:
        q = input("\nAsk: ")
        results = search(q)

        print("\nTop Matches:\n" + "-"*40)
        for r in results:
            print(f"Score: {r['score']}")
            print(f"Text: {r['text']}\n")