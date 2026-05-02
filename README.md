# 🏋️ Next Rep — AI Fitness Assistant (RAG)

Welcome to **Next Rep**, your high-performance AI fitness coach. This project is a Retrieval-Augmented Generation (RAG) chatbot designed to provide accurate, science-based answers to your fitness, nutrition, and recovery questions.

---

## 🎓 Teacher's Corner: How it Works?

Hello, student! Let's understand how this "brain" works. Imagine you have a massive library of fitness books (your data), but you don't want to read them all every time someone asks a question.

### 🔄 The RAG Pipeline (Step-by-Step)

1.  **Preparation (The Library Index):**
    *   We take a dataset of fitness questions and answers (`fitness.jsonl`).
    *   We turn every question into a list of numbers called an **Embedding** (using a `SentenceTransformer` model).
    *   We store these numbers in a specialized database called a **FAISS Index**. This is like a very fast "search engine" for meanings.

2.  **The User Asks (The Query):**
    *   When you type *"How much protein do I need?"*, the chatbot turns your question into the same kind of "number list" (embedding).

3.  **The Search (Retrieval):**
    *   It looks into the **FAISS Index** to find the most similar numbers. It says, *"Hey, I found 4 books that talk about protein!"*

4.  **The Answer (Generation):**
    *   The chatbot takes those 4 matching snippets and hands them to a very smart AI (Llama 3 via Groq).
    *   It tells the AI: *"Using ONLY these snippets, answer the user's question."*
    *   The AI writes a friendly, helpful response based **only** on the facts it was just given.

**Why is this better?** Because the AI doesn't "hallucinate" (make things up). If it's not in the library, it says *"I don't know,"* keeping you safe and informed!

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

Once everything is set up, starting the coach is easy:

```bash
streamlit run app.py
```
This will open a beautiful dark-themed dashboard in your browser where you can start chatting!

---

## 📁 Project Structure

Here is what each file does:

*   📂 **`app.py`**: The heart of the project. It handles the **Streamlit UI**, the chat logic, and communicates with Groq.
*   📂 **`embeddings.py`**: The "librarian" script. Use this if you want to update the knowledge base or re-index your data.
*   📂 **`fitness.index`**: The "Search Engine" file. It contains the mathematical representations (vectors) of all fitness data.
*   📂 **`texts.json`**: The "Bookshelf". This holds the actual text of the questions and answers that the AI reads.
*   📂 **`requirements.txt`**: The list of all Python libraries needed (Streamlit, Faiss, Sentence-Transformers, etc.).
*   📂 **`.env`**: Your secret vault for API keys (never share this!).
*   📂 **`.gitignore`**: Tells Git which files to ignore (like your private `.env`).

---

## 🌟 Key Features
- **Dark Mode UI**: Sleek, premium fitness aesthetic.
- **Relevance Scores**: See how confident the AI is about its source material.
- **Debug Mode**: Toggle the sidebar to see exactly what snippets the AI is looking at.
- **History Tracking**: Keeps a list of your recent questions in the sidebar.

**Happy Training! 🏋️‍♂️**
