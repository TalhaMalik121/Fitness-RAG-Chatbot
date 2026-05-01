import json
import faiss
import numpy as np
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

# -------- Load resources --------
print("Loading index...")
index = faiss.read_index("fitness.index")

with open("texts.json", "r", encoding="utf-8") as f:
    texts = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print(f"Ready. {index.ntotal} vectors loaded.\n")

SIMILARITY_THRESHOLD = 0.60

# -------- Search (with normalization) --------
def search(query: str, k: int = 3) -> list[dict]:
    # Encode and normalize — must match how index was built
    query_vec = model.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(query_vec)  # same normalization used in indexing

    scores, indices = index.search(query_vec, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        results.append({
            "text": texts[idx],
            "score": float(score),
        })
    return results


# -------- Build prompt --------
def build_prompt(query: str, chunks: list[dict]) -> str:
    context_block = "\n\n".join(
        f"[Context {i+1}] (relevance: {c['score']:.2f})\n{c['text']}"
        for i, c in enumerate(chunks)
    )

    return f"""You are Next Rep, an expert AI fitness assistant.
Answer the user's question using ONLY the context below.
If the context does not contain enough information, say: "I don't have reliable information on that."
Keep your answer clear, concise, and practical.

--- CONTEXT START ---
{context_block}
--- CONTEXT END ---

User question: {query}"""


# -------- Ask LLM --------
def ask_llm(query: str, chunks: list[dict]) -> str:
    prompt = build_prompt(query, chunks)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",      # free, fast Groq model
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,              # low = more factual, less creative
        max_tokens=512,
    )

    return response.choices[0].message.content.strip()


# -------- Main pipeline --------
def answer(query: str) -> str:
    chunks = search(query)

    # Filter low-confidence chunks before sending to LLM
    reliable = [c for c in chunks if c["score"] >= SIMILARITY_THRESHOLD]

    if not reliable:
        return (
            f"⚠ No reliable context found (best score: {chunks[0]['score']:.2f}). "
            "Try rephrasing your question."
        )

    return ask_llm(query, reliable)


# -------- REPL --------
if __name__ == "__main__":
    print("Next Rep Fitness Chatbot  |  type 'quit' to exit")
    print("=" * 50)

    while True:
        try:
            query = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not query:
            continue
        if query.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        print("\nBot: ", end="", flush=True)
        response = answer(query)
        print(response)