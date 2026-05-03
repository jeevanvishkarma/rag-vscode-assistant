# 🤖 VS Code Issues RAG Assistant

A production-style Retrieval-Augmented Generation (RAG) system built to analyze and answer queries based on **VS Code GitHub issues and Copilot-related discussions**.

---

## 🚀 Live Demo

👉 [VS Code Issues RAG Assistant](https://jeevanvishkarma-rag-vscode-assistant-app-coee99.streamlit.app/)

---

## 🧠 Overview

This system enables users to:

- Ask natural language questions about VS Code issues
- Get context-aware, grounded answers
- Handle follow-up queries using conversation memory
- Retrieve both semantic and exact keyword matches using hybrid retrieval

---

## ⚙️ Architecture

```text
User Query
    ↓
Query Rewriting (history-aware)
    ↓
Dense Retrieval (FAISS + MiniLM)
    ↓
Top 100 Semantic Candidates
    ↓
BM25 Lexical Reranking
    ↓
Top 20 Candidates
    ↓
Cross-Encoder Reranking
    ↓
Top 5 Final Chunks
    ↓
LLM Generation (GPT-4o-mini)
    ↓
Answer
```

---

## 📊 Evaluation

### 🔍 Retrieval Performance

| Metric | Score |
|---|---:|
| Recall@K | 0.96 |
| Precision@K | 0.68 |
| MRR | 0.94 |
| Avg Relevant Docs | 2.01 |

---

### 🧠 Generation Quality (LLM-as-Judge)

| Metric | Score |
|---|---:|
| Relevance | 0.98 |
| Faithfulness | 0.98 |
| Completeness | 0.94 |

---

## ✨ Features

- ✅ Hybrid Retrieval (FAISS + BM25)
- ✅ Semantic search over VS Code GitHub issues
- ✅ Query rewriting using LLM (history-aware)
- ✅ FAISS IVF vector database with SentenceTransformers
- ✅ BM25 lexical reranking for exact keyword matching
- ✅ Cross-Encoder reranking for improved precision
- ✅ Grounded answer generation (low hallucination)
- ✅ Multi-turn conversational memory
- ✅ Context viewer for transparency
- ✅ Latency tracking for each pipeline stage
- ✅ Full evaluation pipeline (retrieval + generation)

---

## ⚡ Latency

| Stage | Avg Latency |
|---|---:|
| Dense Retrieval | ~0.4 sec |
| BM25 Reranking | ~0.03 sec |
| Cross-Encoder Reranking | ~0.8 sec |
| Generation | ~1.4 sec |
| Total | ~2.7 sec |

---

## 🖥️ Demo UI

- Chat-based interface (Streamlit)
- Hybrid retrieval visualization
- Expandable retrieved context viewer
- Retrieval latency metrics
- Conversation memory support

---

## 📂 Project Structure

```text
rag-vscode-assistant/
│
├── app.py
│
├── retrieval/
│   ├── retriever.py
│   ├── bm25_retriever.py
│   ├── reranker.py
│   └── query_rewriter.py
│
├── generation/
│   └── generate_answer.py
│
├── ingestion/
│   ├── create_chunks.py
│   ├── create_embeddings.py
│   └── build_bm25.py
│
├── scripts/
│   └── run_rag.py
│
├── files/
│   └── index_folder/
│       ├── faiss.index
│       └── metadata.jsonl
│
├── data/
│   └── bm25.pkl
│
├── requirements.txt
│
└── README.md
```

---

## 🧩 Dataset

- ~250K GitHub VS Code Issues
- ~800K Semantic Chunks

Includes:
- Issue titles
- Descriptions
- Comments
- Metadata

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Embeddings | SentenceTransformers |
| Vector Search | FAISS IVF |
| Lexical Search | BM25 |
| Reranking | Cross-Encoder |
| LLM | GPT-4o-mini |
| UI | Streamlit |
| Backend | Python |

---

## 🔮 Future Improvements

- Neighbor chunk expansion
- Elasticsearch/OpenSearch integration
- Multi-query retrieval
- Streaming responses
- Citation support
- Agentic retrieval workflows

---

## 🙌 Acknowledgements

Built using:
- FAISS
- SentenceTransformers
- Streamlit
- OpenAI APIs
- BM25
- LangChain