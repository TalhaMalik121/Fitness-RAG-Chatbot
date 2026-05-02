# import streamlit as st
# import json
# import faiss
# import numpy as np
# import os
# import re
# from dotenv import load_dotenv
# from sentence_transformers import SentenceTransformer
# from groq import Groq

# load_dotenv()

# # ─────────────────────────────────────────────
# # PAGE CONFIG
# # ─────────────────────────────────────────────
# st.set_page_config(
#     page_title="Next Rep — AI Fitness Assistant",
#     page_icon="💪",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ─────────────────────────────────────────────
# # STYLING
# # ─────────────────────────────────────────────
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Barlow:wght@400;600;700&family=Barlow+Condensed:wght@700;800&display=swap');

#     html, body, [class*="css"] {
#         font-family: 'Barlow', sans-serif;
#     }

#     /* ── background ── */
#     .stApp {
#         background: #080b10;
#     }
#     .main .block-container {
#         padding-top: 1.5rem;
#         padding-bottom: 6rem;
#         max-width: 860px;
#     }

#     /* ── sidebar ── */
#     section[data-testid="stSidebar"] {
#         background: #0d1117;
#         border-right: 1px solid #1f2937;
#     }
#     section[data-testid="stSidebar"] h1 {
#         font-family: 'Barlow Condensed', sans-serif;
#         font-size: 1.6rem;
#         letter-spacing: 0.08em;
#         color: #f97316;
#     }

#     /* ── chat messages ── */
#     [data-testid="stChatMessage"] {
#         background: transparent !important;
#         border: none !important;
#     }

#     /* ── user bubble ── */
#     [data-testid="stChatMessage"][data-role="user"] .stMarkdown p {
#         background: #1a2233;
#         border: 1px solid #1f2d45;
#         border-radius: 18px 18px 4px 18px;
#         padding: 12px 18px;
#         display: inline-block;
#         max-width: 82%;
#         float: right;
#         color: #e2e8f0;
#     }

#     /* ── assistant bubble ── */
#     [data-testid="stChatMessage"][data-role="assistant"] .stMarkdown p {
#         color: #cbd5e1;
#         line-height: 1.7;
#     }

#     /* ── chat input ── */
#     [data-testid="stChatInput"] > div {
#         background: #111827 !important;
#         border: 1px solid #1f2937 !important;
#         border-radius: 14px !important;
#     }
#     [data-testid="stChatInput"] textarea {
#         color: #e2e8f0 !important;
#     }

#     /* ── confidence badge ── */
#     .badge {
#         display: inline-flex;
#         align-items: center;
#         gap: 5px;
#         padding: 3px 10px;
#         border-radius: 20px;
#         font-size: 0.72rem;
#         font-weight: 600;
#         margin-top: 6px;
#         letter-spacing: 0.04em;
#     }
#     .badge-high {
#         background: rgba(34,197,94,.12);
#         color: #22c55e;
#         border: 1px solid rgba(34,197,94,.25);
#     }
#     .badge-low {
#         background: rgba(239,68,68,.12);
#         color: #ef4444;
#         border: 1px solid rgba(239,68,68,.25);
#     }

#     /* ── suggestion pills ── */
#     div[data-testid="stButton"] > button {
#         background: #111827;
#         border: 1px solid #1f2937;
#         color: #94a3b8;
#         border-radius: 999px;
#         padding: 8px 18px;
#         font-size: 0.85rem;
#         transition: all 0.18s ease;
#     }
#     div[data-testid="stButton"] > button:hover {
#         border-color: #f97316;
#         color: #f97316;
#         background: rgba(249,115,22,.07);
#     }

#     /* ── new chat button ── */
#     div[data-testid="stButton"]:first-child > button {
#         background: #f97316;
#         border-color: #f97316;
#         color: #000;
#         font-weight: 700;
#         letter-spacing: 0.05em;
#         border-radius: 8px;
#     }
#     div[data-testid="stButton"]:first-child > button:hover {
#         background: #ea6c0a;
#     }

#     /* ── debug panel ── */
#     .debug-box {
#         background: #0d1117;
#         border: 1px solid #1f2937;
#         border-radius: 8px;
#         padding: 10px 14px;
#         font-size: 0.75rem;
#         color: #64748b;
#         margin-top: 6px;
#         font-family: monospace;
#     }

#     /* ── footer ── */
#     .footer {
#         position: fixed;
#         bottom: 0; left: 0; right: 0;
#         text-align: center;
#         padding: 8px;
#         font-size: 0.68rem;
#         color: #374151;
#         pointer-events: none;
#     }

#     /* ── scrollbar ── */
#     ::-webkit-scrollbar { width: 6px; }
#     ::-webkit-scrollbar-track { background: #080b10; }
#     ::-webkit-scrollbar-thumb { background: #1f2937; border-radius: 4px; }
# </style>
# """, unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # TEXT CLEANING  ← must match embed.py exactly
# # ─────────────────────────────────────────────
# def clean(text: str) -> str:
#     """Lowercase, collapse whitespace, strip punctuation."""
#     text = str(text).lower()
#     text = re.sub(r"\s+", " ", text)
#     text = re.sub(r"[^\w\s]", "", text)
#     return text.strip()


# # ─────────────────────────────────────────────
# # LOAD RESOURCES (cached)
# # ─────────────────────────────────────────────
# @st.cache_resource
# def load_resources():
#     try:
#         index  = faiss.read_index("fitness.index")
#         with open("texts.json", "r", encoding="utf-8") as f:
#             texts = json.load(f)
#         model  = SentenceTransformer("all-MiniLM-L6-v2")
#         client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#         return index, texts, model, client
#     except Exception as e:
#         st.error(f"❌ Failed to load resources: {e}")
#         return None, None, None, None

# index, texts, model, client = load_resources()


# # ─────────────────────────────────────────────
# # CONSTANTS
# # ─────────────────────────────────────────────
# # FIX: lowered from 0.60 → 0.35
# # Cosine similarity for sentence-transformers rarely exceeds 0.75
# # for paraphrases; 0.35 captures genuine semantic matches well.
# SIMILARITY_THRESHOLD = 0.35
# TOP_K                = 4    # retrieve more candidates before filtering


# # ─────────────────────────────────────────────
# # SEARCH  ← FIX: clean the query before encoding
# # ─────────────────────────────────────────────
# def search(query: str, k: int = TOP_K) -> list[dict]:
#     """
#     Clean the query the same way the index texts were cleaned,
#     then perform cosine-similarity search.
#     """
#     cleaned = clean(query)           # ← THE CRITICAL FIX

#     query_vec = model.encode(
#         [cleaned],
#         convert_to_numpy=True,
#     ).astype("float32")
#     faiss.normalize_L2(query_vec)

#     scores, indices = index.search(query_vec, k)

#     results = []
#     for score, idx in zip(scores[0], indices[0]):
#         if idx == -1:
#             continue
#         results.append({
#             "text":  texts[idx],
#             "score": float(score),
#         })
#     return results


# # ─────────────────────────────────────────────
# # PROMPT BUILDER
# # ─────────────────────────────────────────────
# def build_prompt(query: str, chunks: list[dict]) -> str:
#     context_block = "\n\n".join(
#         f"[Context {i+1}] (relevance: {c['score']:.2f})\n{c['text']}"
#         for i, c in enumerate(chunks)
#     )
#     return f"""You are Next Rep, a knowledgeable and friendly AI fitness coach.
# Answer the user's question using ONLY the context provided below.
# - Be clear, practical, and encouraging.
# - Use bullet points or short paragraphs where helpful.
# - If the context does not contain enough information, respond with:
#   "I don't have reliable information on that topic right now."

# --- CONTEXT START ---
# {context_block}
# --- CONTEXT END ---

# User question: {query}

# Answer:"""


# # ─────────────────────────────────────────────
# # STREAMING RESPONSE
# # ─────────────────────────────────────────────
# def stream_response(query: str, chunks: list[dict]):
#     prompt = build_prompt(query, chunks)
#     stream = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.35,
#         max_tokens=600,
#         stream=True,
#     )
#     for chunk in stream:
#         delta = chunk.choices[0].delta.content
#         if delta:
#             yield delta


# # ─────────────────────────────────────────────
# # SESSION STATE
# # ─────────────────────────────────────────────
# if "messages"       not in st.session_state:
#     st.session_state.messages       = []
# if "past_questions" not in st.session_state:
#     st.session_state.past_questions = []
# if "debug_mode"     not in st.session_state:
#     st.session_state.debug_mode     = False


# # ─────────────────────────────────────────────
# # SIDEBAR
# # ─────────────────────────────────────────────
# with st.sidebar:
#     st.markdown("<h1 style='text-align:center; margin-bottom:0;'>NEXT REP 💪</h1>", unsafe_allow_html=True)
#     st.markdown("<p style='text-align:center; color:#4b5563; font-size:0.8rem; margin-top:4px;'>AI Fitness Coach</p>", unsafe_allow_html=True)
#     st.markdown("---")

#     if st.button("＋  New Chat", use_container_width=True):
#         st.session_state.messages       = []
#         st.session_state.past_questions = []
#         st.rerun()

#     st.markdown("---")

#     # Debug toggle — useful during development
#     st.session_state.debug_mode = st.toggle(
#         "🔍 Debug mode",
#         value=st.session_state.debug_mode,
#         help="Shows raw retrieval scores for each response",
#     )

#     st.markdown("---")
#     st.markdown("### Recent Questions")
#     if st.session_state.past_questions:
#         for q in reversed(st.session_state.past_questions[-10:]):
#             st.markdown(f"<small style='color:#4b5563;'>› {q[:30]}…</small>", unsafe_allow_html=True)
#     else:
#         st.markdown("<small style='color:#374151;'>No history yet.</small>", unsafe_allow_html=True)


# # ─────────────────────────────────────────────
# # MAIN AREA
# # ─────────────────────────────────────────────
# st.markdown(
#     "<h2 style='font-family:\"Barlow Condensed\",sans-serif; font-size:2rem;"
#     " letter-spacing:0.06em; color:#f97316; margin-bottom:0;'>NEXT REP</h2>"
#     "<p style='color:#4b5563; margin-top:0;'>Your AI-powered fitness coach — ask anything about training, nutrition & recovery.</p>",
#     unsafe_allow_html=True,
# )

# # ── Render chat history ──────────────────────
# for msg in st.session_state.messages:
#     with st.chat_message(msg["role"], avatar="💪" if msg["role"] == "assistant" else "🧑"):
#         st.markdown(msg["content"])

#         # badge
#         if "score" in msg:
#             high = msg["score"] >= SIMILARITY_THRESHOLD
#             cls  = "badge-high" if high else "badge-low"
#             icon = "●" if high else "⚠"
#             st.markdown(
#                 f'<div class="badge {cls}">{icon} Relevance {msg["score"]:.2f}</div>',
#                 unsafe_allow_html=True,
#             )

#         # debug panel (history)
#         if st.session_state.debug_mode and "debug" in msg:
#             st.markdown(
#                 "<div class='debug-box'>" + msg["debug"] + "</div>",
#                 unsafe_allow_html=True,
#             )

# # ── Welcome screen (first visit) ────────────
# if not st.session_state.messages:
#     with st.chat_message("assistant", avatar="💪"):
#         st.markdown(
#             "Hey! I'm **Next Rep**, your AI fitness coach. "
#             "Ask me anything about workouts, nutrition, or recovery 💪"
#         )

#     st.markdown("#### Quick questions:")
#     suggestions = [
#         "How do I build muscle?",
#         "Best foods for fat loss",
#         "How many rest days do I need?",
#         "What is progressive overload?",
#         "How much protein should I eat?",
#     ]
#     cols = st.columns(len(suggestions))
#     for i, s in enumerate(suggestions):
#         if cols[i].button(s, key=f"sug_{i}"):
#             st.session_state.messages.append({"role": "user", "content": s})
#             st.session_state.past_questions.append(s)
#             st.rerun()

# # ── Chat input ───────────────────────────────
# if prompt := st.chat_input("Ask Next Rep anything…"):

#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.session_state.past_questions.append(prompt)

#     with st.chat_message("user", avatar="🧑"):
#         st.markdown(prompt)

#     with st.chat_message("assistant", avatar="💪"):

#         # Step 1: Retrieve
#         with st.status("Searching fitness knowledge base…", expanded=False) as status:
#             chunks   = search(prompt)
#             reliable = [c for c in chunks if c["score"] >= SIMILARITY_THRESHOLD]
#             status.update(label="Done!", state="complete")

#         # Build debug string
#         debug_lines = [f"Query (cleaned): <b>{clean(prompt)}</b><br>"]
#         for i, c in enumerate(chunks):
#             flag = "✓" if c["score"] >= SIMILARITY_THRESHOLD else "✗"
#             preview = c["text"][:90].replace("\n", " ")
#             debug_lines.append(f"{flag} [{c['score']:.3f}] {preview}…")
#         debug_html = "<br>".join(debug_lines)

#         # Step 2: Respond
#         if not reliable:
#             best   = chunks[0]["score"] if chunks else 0.0
#             reply  = "I don't have reliable information on that topic right now."
#             st.markdown(reply)
#             st.markdown(
#                 f'<div class="badge badge-low">⚠ Relevance {best:.2f} — below threshold {SIMILARITY_THRESHOLD}</div>',
#                 unsafe_allow_html=True,
#             )
#             if st.session_state.debug_mode:
#                 st.markdown(f'<div class="debug-box">{debug_html}</div>', unsafe_allow_html=True)

#             st.session_state.messages.append({
#                 "role":    "assistant",
#                 "content": reply,
#                 "score":   best,
#                 "debug":   debug_html,
#             })

#         else:
#             full_response = st.write_stream(stream_response(prompt, reliable))
#             best = reliable[0]["score"]
#             st.markdown(
#                 f'<div class="badge badge-high">● Relevance {best:.2f}</div>',
#                 unsafe_allow_html=True,
#             )
#             if st.session_state.debug_mode:
#                 st.markdown(f'<div class="debug-box">{debug_html}</div>', unsafe_allow_html=True)

#             st.session_state.messages.append({
#                 "role":    "assistant",
#                 "content": full_response,
#                 "score":   best,
#                 "debug":   debug_html,
#             })

# # ── Footer ───────────────────────────────────
# st.markdown(
#     '<div class="footer">Next Rep AI · RAG + Groq · FYP Project</div>',
#     unsafe_allow_html=True,
# )
"""
app.py — Next Rep Fitness AI Chatbot
======================================
3-tier answering logic:
  TIER 1 — High-confidence match in the PDF knowledge base  → RAG answer
  TIER 2 — Low/no match BUT question is fitness-related      → LLM general answer
  TIER 3 — Not fitness-related                               → polite refusal

Run:
    streamlit run app.py
"""

import streamlit as st
import json
import faiss
import numpy as np
import os
import re
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

# ─────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Next Rep — AI Fitness Coach",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
# STYLING
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,400;0,600;0,700;1,400&family=Barlow+Condensed:wght@700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Barlow', sans-serif; }

/* ── app background ── */
.stApp { background: #07090f; }
.main .block-container {
    padding-top: 1.4rem;
    padding-bottom: 7rem;
    max-width: 880px;
}

/* ── sidebar ── */
section[data-testid="stSidebar"] {
    background: #0c0f18;
    border-right: 1px solid #1c2333;
}

/* ── chat messages ── */
[data-testid="stChatMessage"] { background: transparent !important; border: none !important; }

/* user bubble */
[data-testid="stChatMessage"][data-role="user"] .stMarkdown p {
    background: #131c2e;
    border: 1px solid #1e2d47;
    border-radius: 18px 18px 4px 18px;
    padding: 11px 17px;
    display: inline-block;
    max-width: 84%;
    float: right;
    color: #dde5f0;
}

/* assistant text */
[data-testid="stChatMessage"][data-role="assistant"] .stMarkdown p,
[data-testid="stChatMessage"][data-role="assistant"] .stMarkdown li {
    color: #c8d4e3;
    line-height: 1.75;
}

/* ── chat input ── */
[data-testid="stChatInput"] > div {
    background: #101520 !important;
    border: 1px solid #1c2333 !important;
    border-radius: 14px !important;
}
[data-testid="stChatInput"] textarea { color: #dde5f0 !important; }

/* ── tier / confidence badge ── */
.badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 11px; border-radius: 20px;
    font-size: 0.71rem; font-weight: 700;
    margin-top: 7px; letter-spacing: 0.05em;
}
.badge-rag    { background:rgba(34,197,94,.12);  color:#22c55e; border:1px solid rgba(34,197,94,.3); }
.badge-llm    { background:rgba(250,204,21,.12); color:#facc15; border:1px solid rgba(250,204,21,.3); }
.badge-off    { background:rgba(239,68,68,.12);  color:#ef4444; border:1px solid rgba(239,68,68,.3); }

/* ── suggestion buttons ── */
div[data-testid="stButton"] > button {
    background: #101520; border: 1px solid #1c2333;
    color: #8899bb; border-radius: 999px;
    padding: 8px 18px; font-size: 0.84rem;
    transition: all 0.18s;
}
div[data-testid="stButton"] > button:hover {
    border-color: #f97316; color: #f97316;
    background: rgba(249,115,22,.07);
}

/* new-chat button */
div[data-testid="stButton"]:first-child > button {
    background: #f97316; border-color: #f97316;
    color: #000; font-weight: 700; letter-spacing: 0.05em;
    border-radius: 8px;
}
div[data-testid="stButton"]:first-child > button:hover { background: #e56b10; }

/* ── debug panel ── */
.debug-box {
    background: #0c0f18; border: 1px solid #1c2333;
    border-radius: 8px; padding: 10px 14px;
    font-size: 0.73rem; color: #4b5e80;
    margin-top: 6px; font-family: monospace;
    line-height: 1.6;
}

/* ── footer ── */
.footer {
    position: fixed; bottom: 0; left: 0; right: 0;
    text-align: center; padding: 8px;
    font-size: 0.67rem; color: #2d3a50;
    pointer-events: none;
}

/* ── scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #07090f; }
::-webkit-scrollbar-thumb { background: #1c2333; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────
RAG_THRESHOLD     = 0.35   # cosine score → use PDF context
TOP_K             = 5      # candidates retrieved from FAISS

# Keywords used by the fitness-topic classifier (Tier 2 guard)
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


# ─────────────────────────────────────────────────────────
# TEXT CLEANING — must be IDENTICAL to embed.py
# ─────────────────────────────────────────────────────────
def clean_for_embedding(text: str) -> str:
    """Lowercase + strip punctuation. Applied to query before FAISS search."""
    text = str(text).lower()
    text = re.sub(r"\s+",     " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


# ─────────────────────────────────────────────────────────
# FITNESS TOPIC CLASSIFIER
# ─────────────────────────────────────────────────────────
def is_fitness_related(query: str) -> bool:
    """
    Lightweight keyword check.
    Returns True if the question is plausibly about fitness/health/nutrition.
    """
    lower = query.lower()
    return any(kw in lower for kw in FITNESS_KEYWORDS)


# ─────────────────────────────────────────────────────────
# LOAD RESOURCES (cached across reruns)
# ─────────────────────────────────────────────────────────
@st.cache_resource
def load_resources():
    try:
        index  = faiss.read_index("fitness.index")
        with open("texts.json", "r", encoding="utf-8") as f:
            texts = json.load(f)
        model  = SentenceTransformer("all-MiniLM-L6-v2")
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        return index, texts, model, client
    except Exception as e:
        st.error(f"Failed to load resources: {e}")
        return None, None, None, None

index, texts, model, client = load_resources()


# ─────────────────────────────────────────────────────────
# SEARCH — returns ranked chunks with cosine scores
# ─────────────────────────────────────────────────────────
def search(query: str, k: int = TOP_K) -> list[dict]:
    cleaned   = clean_for_embedding(query)          # ← same cleaning as embed.py
    query_vec = model.encode([cleaned], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(query_vec)

    scores, indices = index.search(query_vec, k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        results.append({"text": texts[idx], "score": float(score)})
    return results


# ─────────────────────────────────────────────────────────
# PROMPT BUILDERS
# ─────────────────────────────────────────────────────────
def prompt_rag(query: str, chunks: list[dict]) -> str:
    """Tier 1 — answer grounded in PDF context."""
    ctx = "\n\n".join(
        f"[Source {i+1} | relevance {c['score']:.2f}]\n{c['text']}"
        for i, c in enumerate(chunks)
    )
    return f"""You are Next Rep, an expert AI fitness coach for the Next Rep Fitness app.

Answer the user's question using ONLY the context provided below.
Rules:
- Be clear, practical, and encouraging.
- Use bullet points or short paragraphs where helpful.
- If the context partially answers the question, use what is available and say so.
- Do NOT make up information not present in the context.

--- KNOWLEDGE BASE CONTEXT ---
{ctx}
--- END CONTEXT ---

User question: {query}

Answer:"""


def prompt_general_fitness(query: str) -> str:
    """Tier 2 — answer from LLM general fitness knowledge (no PDF context)."""
    return f"""You are Next Rep, an expert AI fitness coach.

The user asked a fitness question that isn't covered in the app's knowledge base.
Answer using your general fitness expertise.
Rules:
- Be clear, practical, and encouraging.
- Mention at the start that this is general guidance, not from the app's specific knowledge base.
- Use bullet points or short paragraphs.
- Keep it concise and actionable.
- Do NOT give medical diagnoses. Always recommend consulting a professional for medical concerns.

User question: {query}

Answer:"""


OFF_TOPIC_REPLY = (
    "I'm **Next Rep**, your AI fitness coach — I can only help with topics related to "
    "fitness, training, nutrition, recovery, and health. "
    "Your question seems to be outside that scope. "
    "Feel free to ask me anything about workouts, diet, or exercise! 💪"
)


# ─────────────────────────────────────────────────────────
# STREAMING LLM CALL
# ─────────────────────────────────────────────────────────
def stream_llm(prompt: str):
    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.35,
        max_tokens=700,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


# ─────────────────────────────────────────────────────────
# 3-TIER ANSWER LOGIC
# ─────────────────────────────────────────────────────────
def determine_tier(chunks: list[dict], query: str) -> str:
    """
    TIER 1 — at least one chunk above RAG_THRESHOLD  → use PDF context
    TIER 2 — no good chunk, but question is fitness   → LLM general answer
    TIER 3 — not fitness-related                      → polite refusal
    """
    reliable = [c for c in chunks if c["score"] >= RAG_THRESHOLD]
    if reliable:
        return "rag"
    if is_fitness_related(query):
        return "llm"
    return "off"


# ─────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────
for key, default in [
    ("messages",       []),
    ("past_questions", []),
    ("debug_mode",     False),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ─────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<h1 style='text-align:center;font-family:\"Barlow Condensed\",sans-serif;"
        "letter-spacing:.1em;color:#f97316;margin-bottom:0'>NEXT REP</h1>"
        "<p style='text-align:center;color:#2d3a50;font-size:.78rem;margin-top:2px'>AI Fitness Coach</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    if st.button("＋  New Chat", use_container_width=True):
        st.session_state.messages       = []
        st.session_state.past_questions = []
        st.rerun()

    st.markdown("---")
    st.session_state.debug_mode = st.toggle(
        "🔍 Debug mode",
        value=st.session_state.debug_mode,
        help="Shows retrieval scores and answer tier for each response",
    )

    st.markdown("---")
    st.markdown(
        "<p style='color:#2d3a50;font-size:.8rem;font-weight:700;margin-bottom:6px'>ANSWER TIERS</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<small>"
        "<span style='color:#22c55e'>●</span> <b>PDF Knowledge Base</b> — from your app docs<br>"
        "<span style='color:#facc15'>●</span> <b>AI Fitness Expert</b> — general fitness knowledge<br>"
        "<span style='color:#ef4444'>●</span> <b>Out of Scope</b> — non-fitness question"
        "</small>",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("<p style='color:#2d3a50;font-size:.8rem;font-weight:700;margin-bottom:6px'>RECENT</p>", unsafe_allow_html=True)
    if st.session_state.past_questions:
        for q in reversed(st.session_state.past_questions[-8:]):
            st.markdown(f"<small style='color:#2d3a50'>› {q[:32]}…</small>", unsafe_allow_html=True)
    else:
        st.markdown("<small style='color:#1c2333'>No history yet.</small>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# MAIN CHAT AREA
# ─────────────────────────────────────────────────────────
st.markdown(
    "<h2 style='font-family:\"Barlow Condensed\",sans-serif;font-size:2.1rem;"
    "letter-spacing:.07em;color:#f97316;margin-bottom:0'>NEXT REP</h2>"
    "<p style='color:#2d3a50;margin-top:0'>AI Fitness Coach — ask anything about training, nutrition & recovery.</p>",
    unsafe_allow_html=True,
)

# ── Render history ───────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="💪" if msg["role"] == "assistant" else "🧑"):
        st.markdown(msg["content"])

        if "tier" in msg:
            tier_map = {
                "rag": ("badge-rag", "● PDF Knowledge Base",  f"relevance {msg.get('score', 0):.2f}"),
                "llm": ("badge-llm", "● AI Fitness Expert",   "general knowledge"),
                "off": ("badge-off", "● Out of Scope",        "non-fitness query"),
            }
            cls, label, detail = tier_map[msg["tier"]]
            st.markdown(
                f'<div class="badge {cls}">{label} &nbsp;·&nbsp; {detail}</div>',
                unsafe_allow_html=True,
            )

        if st.session_state.debug_mode and "debug" in msg:
            st.markdown(
                f'<div class="debug-box">{msg["debug"]}</div>',
                unsafe_allow_html=True,
            )

# ── Welcome screen ───────────────────────────────────────
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="💪"):
        st.markdown(
            "Hey! I'm **Next Rep**, your AI fitness coach.\n\n"
            "I'll first check our **knowledge base** for answers. If the topic isn't "
            "there but it's fitness-related, I'll answer from my general expertise. "
            "Ask me anything about workouts, nutrition, or recovery! 💪"
        )

    st.markdown("#### Quick questions:")
    suggestions = [
        "How do I build muscle?",
        "What is progressive overload?",
        "How much protein do I need?",
        "Best foods for fat loss",
        "How many rest days per week?",
        "What is TDEE?",
    ]
    cols = st.columns(3)
    for i, s in enumerate(suggestions):
        if cols[i % 3].button(s, key=f"sug_{i}"):
            st.session_state.messages.append({"role": "user", "content": s})
            st.session_state.past_questions.append(s)
            st.rerun()

# ── Chat input ───────────────────────────────────────────
if prompt := st.chat_input("Ask Next Rep anything about fitness…"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.past_questions.append(prompt)

    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="💪"):

        # Step 1: Retrieve from FAISS
        with st.status("Searching knowledge base…", expanded=False) as status:
            chunks  = search(prompt)
            tier    = determine_tier(chunks, prompt)
            status.update(label="Done!", state="complete")

        # Build debug HTML
        reliable = [c for c in chunks if c["score"] >= RAG_THRESHOLD]
        debug_lines = [
            f"Query (cleaned): <b>{clean_for_embedding(prompt)}</b>",
            f"Tier: <b>{tier.upper()}</b> | Threshold: {RAG_THRESHOLD} | "
            f"Reliable chunks: {len(reliable)}/{len(chunks)}",
            "",
        ]
        for i, c in enumerate(chunks):
            flag    = "✓" if c["score"] >= RAG_THRESHOLD else "✗"
            preview = c["text"][:100].replace("\n", " ")
            debug_lines.append(f"{flag} [{c['score']:.3f}] {preview}…")
        debug_html = "<br>".join(debug_lines)

        # ── TIER 1: PDF answer ──────────────────────────
        if tier == "rag":
            full_response = st.write_stream(stream_llm(prompt_rag(prompt, reliable)))
            best_score    = reliable[0]["score"]
            st.markdown(
                f'<div class="badge badge-rag">● PDF Knowledge Base &nbsp;·&nbsp; relevance {best_score:.2f}</div>',
                unsafe_allow_html=True,
            )
            if st.session_state.debug_mode:
                st.markdown(f'<div class="debug-box">{debug_html}</div>', unsafe_allow_html=True)

            st.session_state.messages.append({
                "role":    "assistant",
                "content": full_response,
                "tier":    "rag",
                "score":   best_score,
                "debug":   debug_html,
            })

        # ── TIER 2: General fitness LLM answer ──────────
        elif tier == "llm":
            full_response = st.write_stream(stream_llm(prompt_general_fitness(prompt)))
            st.markdown(
                '<div class="badge badge-llm">● AI Fitness Expert &nbsp;·&nbsp; general knowledge</div>',
                unsafe_allow_html=True,
            )
            if st.session_state.debug_mode:
                st.markdown(f'<div class="debug-box">{debug_html}</div>', unsafe_allow_html=True)

            st.session_state.messages.append({
                "role":    "assistant",
                "content": full_response,
                "tier":    "llm",
                "debug":   debug_html,
            })

        # ── TIER 3: Off-topic refusal ────────────────────
        else:
            st.markdown(OFF_TOPIC_REPLY)
            st.markdown(
                '<div class="badge badge-off">● Out of Scope &nbsp;·&nbsp; non-fitness query</div>',
                unsafe_allow_html=True,
            )
            if st.session_state.debug_mode:
                st.markdown(f'<div class="debug-box">{debug_html}</div>', unsafe_allow_html=True)

            st.session_state.messages.append({
                "role":    "assistant",
                "content": OFF_TOPIC_REPLY,
                "tier":    "off",
                "debug":   debug_html,
            })

# ── Footer ───────────────────────────────────────────────
st.markdown(
    '<div class="footer">Next Rep AI · PDF RAG + Groq · FYP Project</div>',
    unsafe_allow_html=True,
)