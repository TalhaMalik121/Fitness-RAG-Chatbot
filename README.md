# 🏋️ Next Rep — Full Stack AI Fitness Assistant

Welcome to the production-ready version of **Next Rep**, a full-stack Retrieval-Augmented Generation (RAG) platform. This project has been migrated from Streamlit to a modern **React + FastAPI** architecture for better performance, scalability, and UI control.

---

## 🏗️ Architecture

### **Frontend (React + Tailwind CSS)**
- **Modern UI**: A ChatGPT-inspired dark interface with a premium teal/cyan aesthetic.
- **Vite**: Powered by Vite for lightning-fast development and optimized builds.
- **Lucide Icons**: Clean, professional iconography.
- **Responsive**: Designed to work seamlessly across different screen sizes.

### **Backend (FastAPI + RAG)**
- **FastAPI**: High-performance asynchronous API framework.
- **RAG Pipeline**: 
    - **Tier 1 (PDF)**: Retrieval from your custom PDF knowledge base via FAISS.
    - **Tier 2 (General AI)**: General fitness expertise for topics not in the PDF.
    - **Tier 3 (Guardrails)**: Automatic filtering of off-topic questions.
- **Groq API**: Powered by Llama 3.3 for near-instant responses.

---

## 📁 Project Structure

```text
Fitness-Chatbot/
├── backend/                  # FastAPI RAG Backend
│   ├── KnowledgeBase/        # PDF Knowledge Source + Indices
│   ├── app.py                # FastAPI Server
│   ├── rag_pipeline.py       # Core RAG & Logic Engine
│   ├── requirements.txt      # Backend dependencies
│   └── .env                  # API Keys (Groq, etc.)
│
├── frontend/                 # React + Tailwind Frontend
│   ├── src/
│   │   ├── components/       # UI Components (ChatBox, etc.)
│   │   ├── api/              # API Client (Axios)
│   │   └── App.jsx           # Main App Layout
│   ├── tailwind.config.js    # UI Theme Configuration
│   └── package.json          # Frontend dependencies
│
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites
- **Node.js** (v18+)
- **Python** (v3.10+)
- **Conda** (Recommended)

### 2. Backend Setup
```bash
cd backend
conda create -n fitness-backend python=3.10 -y
conda activate fitness-backend
pip install -r requirements.txt
```
*Create a `.env` file in the `backend/` folder and add your `GROQ_API_KEY`.*

### 3. Frontend Setup
```bash
cd frontend
npm install
```

---

## 🏃 Running the Application

You will need two terminal windows open:

**Terminal 1: Start Backend**
```bash
cd backend
python app.py
```
*API will run on `http://localhost:8000`*

**Terminal 2: Start Frontend**
```bash
cd frontend
npm run dev
```
*App will run on `http://localhost:5173`*

---

## 🌟 Key Features
- **Instant Responses**: Powered by Groq for high-speed inference.
- **Topic Guarding**: Ensures the AI stays focused on fitness, training, and health.
- **Premium Design**: Custom dark theme with teal accents and smooth animations.
- **PDF Grounding**: Answers are cross-referenced with your specific knowledge base.

**Happy Training! 🏋️‍♂️**
