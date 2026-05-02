import os
import json
import re
import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

# CONFIG
RAG_THRESHOLD = 0.35
TOP_K = 5

FITNESS_KEYWORDS = [
    "workout", "exercise", "fitness", "muscle", "weight", "fat", "protein",
    "calorie", "diet", "nutrition", "cardio", "gym", "training", "strength",
    "endurance", "recovery", "sleep", "supplement", "creatine", "whey",
    "squat", "deadlift", "bench", "rep", "set", "bmi", "bmr", "tdee",
    "bulk", "cut", "deficit", "surplus", "macro", "carb", "hypertrophy",
    "hiit", "stretch", "mobility", "injury", "pain", "posture", "core",
    "body", "lean", "mass", "overload", "split", "ppl", "push", "pull",
    "leg", "chest", "back", "shoulder", "bicep", "tricep", "glute",
    "hamstring", "quad", "abs", "run", "jog", "walk", "swim", "sport",
    "health", "lose", "gain", "build", "tone", "shred", "deload", "rir",
    "rpe", "form", "technique", "warm", "cool", "rest", "day", "week",
    "meal", "food", "eat", "hunger", "fast", "intermittent", "plateau",
]

def clean_for_embedding(text: str) -> str:
    text = str(text).lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

def is_fitness_related(query: str) -> bool:
    lower = query.lower()
    return any(kw in lower for kw in FITNESS_KEYWORDS)

class RAGPipeline:
    def __init__(self):
        # Use absolute paths relative to this file
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(BASE_DIR, "KnowledgeBase", "fitness.index")
        texts_path = os.path.join(BASE_DIR, "KnowledgeBase", "texts.json")
        
        if not os.path.exists(index_path) or not os.path.exists(texts_path):
            print(f"CRITICAL ERROR: Knowledge base files not found at {index_path} or {texts_path}")
            # Try fallback to project root if needed
            index_path = os.path.join("backend", "KnowledgeBase", "fitness.index")
            texts_path = os.path.join("backend", "KnowledgeBase", "texts.json")

        self.index = faiss.read_index(index_path)
        with open(texts_path, "r", encoding="utf-8") as f:
            self.texts = json.load(f)
            
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("ERROR: GROQ_API_KEY is missing from environment variables!")
        self.client = Groq(api_key=api_key)

    def search(self, query: str, k: int = TOP_K):
        cleaned = clean_for_embedding(query)
        query_vec = self.model.encode([cleaned], convert_to_numpy=True).astype("float32")
        faiss.normalize_L2(query_vec)
        scores, indices = self.index.search(query_vec, k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1: continue
            results.append({"text": self.texts[idx], "score": float(score)})
        return results

    def determine_tier(self, chunks: list[dict], query: str):
        reliable = [c for c in chunks if c["score"] >= RAG_THRESHOLD]
        if reliable:
            return "rag", reliable
        if is_fitness_related(query):
            return "llm", []
        return "off", []

    def get_response(self, query: str):
        chunks = self.search(query)
        tier, reliable = self.determine_tier(chunks, query)
        
        if tier == "rag":
            prompt = self.prompt_rag(query, reliable)
        elif tier == "llm":
            prompt = self.prompt_general_fitness(query)
        else:
            return "Sorry, I can only answer fitness-related questions about training, nutrition, and recovery. 💪"

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.35,
            max_tokens=800,
        )
        return response.choices[0].message.content

    def prompt_rag(self, query: str, chunks: list[dict]):
        ctx = "\n\n".join([f"[Source {i+1}]\n{c['text']}" for i, c in enumerate(chunks)])
        return f"""You are Fitness Coach, an expert AI fitness coach.
Answer the user using ONLY the context provided.
Rules:
- Be clear, practical, and encouraging.
- Use bullet points where helpful.
- If the context doesn't fully answer, say so.

--- CONTEXT ---
{ctx}
--- END ---

User: {query}
Answer:"""

    def prompt_general_fitness(self, query: str):
        return f"""You are Fitness Coach, an expert AI fitness coach.
The knowledge base doesn't cover this specifically, so use your general expertise.
Rules:
- Be practical and encouraging.
- Do NOT give medical diagnoses.
- Keep it concise.

User: {query}
Answer:"""
