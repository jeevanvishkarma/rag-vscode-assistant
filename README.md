# 🤖 VS Code Issues RAG Assistant

A production-style Retrieval-Augmented Generation (RAG) system built to analyze and answer queries based on **VS Code GitHub issues and Copilot-related discussions**.

---

## 🚀 Live Demo
👉 https://your-app.streamlit.app

---

## 🧠 Overview

This system enables users to:

- Ask natural language questions about VS Code issues
- Get context-aware, grounded answers
- Handle follow-up queries using conversation memory

---

## ⚙️ Architecture
User Query
↓
Query Rewriting (history-aware)
↓
Vector Search (FAISS + MiniLM)
↓
MMR Retrieval (Top 10)
↓
Reranking (Top 3)
↓
LLM Generation (grounded) (GPT-4o-mini)
↓
Answer

---


---

## 📊 Evaluation

### 🔍 Retrieval Performance

| Metric        | Score |
|--------------|------|
| Recall@3     | 0.98 |
| Precision@3  | 0.67 |
| MRR          | 0.95 |
| Avg Relevant Docs | 1.90 |

---

### 🧠 Generation Quality (LLM-as-Judge)

| Metric         | Score |
|---------------|------|
| Relevance     | 0.98 |
| Faithfulness  | 0.98 |
| Completeness  | 0.94 |

---

## ✨ Features

- ✅ Semantic search over VS Code issue data  
- ✅ Query rewriting using LLM (history-aware)  
- ✅ FAISS vector database with SentenceTransformers  
- ✅ MMR retrieval for diversity  
- ✅ Reranking for improved precision  
- ✅ Grounded answer generation (low hallucination)  
- ✅ Multi-turn chat support  
- ✅ Context viewer for transparency  
- ✅ Full evaluation pipeline (retrieval + generation)

---

## 🖥️ Demo UI

- Chat-based interface (Streamlit)
- Conversation memory support
- Expandable context viewer

---

## 📂 Project Structure
rag-project/
│
├── app/ # Streamlit UI
├── retrieval/ # Retrieval + query rewriting
├── generation/ # Answer generation
├── evaluation/ # Metrics + LLM judge
├── prompts/ # Prompt templates
├── scripts/ # Pipeline runners
├── data/ # Dataset + outputs
├── prompts/ # Prompts
├── requirements.txt
└── README.md

