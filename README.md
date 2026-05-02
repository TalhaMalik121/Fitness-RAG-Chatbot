# 🏋️ Next Rep — AI Fitness Assistant (PDF RAG)

Welcome to **Next Rep**, your high-performance AI fitness coach. This project is a **Retrieval-Augmented Generation (RAG)** chatbot designed to provide accurate, science-based answers to your fitness, nutrition, and recovery questions by reading directly from your custom PDF knowledge base.

---

## 🎓 Teacher's Corner: How it Works?

Hello, student! Let's understand how this "brain" works. Imagine you have a massive library of fitness books (your PDF), but you don't want to read them all every time someone asks a question.

### 🔄 The RAG Pipeline (Step-by-Step)

1.  **Preparation (The Library Index):**
    *   We take your fitness knowledge PDF (`Fitness_RAG_Knowledge_Base.pdf`).
    *   We split the PDF into small, readable "chunks" (paragraphs).
    *   We turn every chunk into a list of numbers called an **Embedding** (using a `SentenceTransformer` model).
    *   We store these numbers in a specialized database called a **FAISS Index** inside the `KnowledgeBase` folder. This is like a very fast "search engine" for meanings.

2.  **The User Asks (The Query):**
    *   When you type *"How much protein do I need?"*, the chatbot turns your question into the same kind of "number list" (embedding).

3.  **The Search (Retrieval):**
    *   It looks into the **FAISS Index** to find the most similar chunks. It says, *"Hey, I found 5 sections in the PDF that talk about protein!"*

4.  **The Answer (Generation):**
    *   The chatbot takes those matching snippets and hands them to a very smart AI (Llama 3 via Groq).
    *   It tells the AI: *"Using ONLY these snippets from the PDF, answer the user's question."*
    *   The AI writes a friendly, helpful response based **only** on the facts it was just given.

**Why is this better?** Because the AI doesn't "hallucinate" (make things up). If it's not in the PDF, it can still use its general expertise if the question is fitness-related, or politely refuse if it's off-topic!

---

## 🛠️ Installation & Setup

Follow these steps to get your coach up and running.

### 1. Create a Virtual Environment (Conda)
It is best to keep your project in its own little "bubble" so it doesn't mess with other projects.

```bash
# Create the environment (we use Python 3.10)
conda create -n fitness-bot python=3.10 -y

# Activate the environment
conda activate fitness-bot
```

### 2. Install Requirements
Now, let's install the "tools" the chatbot needs.

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
You need an API key from **Groq** (it's fast and free to start!).

1.  Go to [Groq Cloud](https://console.groq.com/) and create an API key.
2.  In the project folder, create a file named `.env`.
3.  Add your key to it like this:
    ```env
    GROQ_API_KEY=your_actual_key_here
    ```

---

## 🚀 How to Run

### Step 1: Process the Knowledge Base
If you have updated your PDF or are running for the first time, you need to "index" the data:
```bash
python embeddings.py
```
This will create the files inside the `KnowledgeBase` folder.

### Step 2: Start the Chatbot
Once indexed, start the dashboard:
```bash
streamlit run app.py
```
This will open a beautiful dark-themed dashboard in your browser with a premium teal/cyan aesthetic.

---

## 📁 Project Structure

```text
Fitness-Chatbot/
├── KnowledgeBase/
│   ├── Fitness_RAG_Knowledge_Base.pdf  # 📚 Raw Knowledge Source
│   ├── fitness.index                   # 🧠 FAISS Vector Index (Search Engine)
│   └── texts.json                      # 📄 Processed text chunks for AI context
├── app.py                              # 🚀 Main Streamlit Application (Frontend + Logic)
├── embeddings.py                       # 🛠️ Data Processing & Indexing Script
├── requirements.txt                    # 📦 Python Dependencies
├── .env                                # 🔑 Private API Keys (Groq)
└── .gitignore                          # 🙈 Files to exclude from Git
```

### File Details:
*   📂 **`app.py`**: The heart of the coach. It manages the **Streamlit UI**, user session state, RAG retrieval logic, and streams responses from Llama 3.3.
*   📂 **`embeddings.py`**: The "Ingestion" engine. It extracts text from the PDF, cleans it, splits it into overlapping chunks, and generates the FAISS index.
*   📂 **`KnowledgeBase/`**: This folder houses the brain of the bot. If you update the PDF, you must re-run `embeddings.py` to refresh the index.
*   📂 **`requirements.txt`**: Contains all necessary libraries including `pdfplumber` for PDF parsing and `faiss-cpu` for vector search.
*   📂 **`.env`**: Contains your `GROQ_API_KEY`. **Keep this file private!**


---

## 🌟 Key Features
- **Premium Teal Theme**: Sleek, high-performance aesthetic matching modern fitness apps.
- **3-Tier Answer Logic**:
    1.  **PDF Grounded**: Answers directly from your PDF documents.
    2.  **General Expertise**: Answers from AI knowledge if PDF doesn't have it (fitness only).
    3.  **Topic Guard**: Refuses off-topic questions (e.g., about movies or politics).
- **Relevance Scores**: See how closely the AI's source material matches your question.
- **Debug Mode**: Toggle the sidebar to see exactly which PDF snippets the AI is using.

**Happy Training! 🏋️‍♂️**
