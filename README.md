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
├── app.py                         # Streamlit application
├── requirements.txt
├── README.md
│
├── retrieval/
│   ├── retriever.py              # FAISS semantic retrieval
│   ├── bm25_retriever.py         # BM25 lexical reranking
│   ├── reranker.py               # Cross-encoder reranker
│   └── query_rewriter.py         # History-aware query rewriting
│
├── generation/
│   └── generate_answer.py        # GPT answer generation
│
├── scripts/
│   └── run_rag.py                # Main RAG orchestration pipeline
│
├── ingestion/
│   ├── create_chunks_all.py      # Semantic chunk creation
│   ├── create_embeddings.py      # FAISS embedding generation
│   └── build_bm25.py             # BM25 index creation
│
├── files/
│   └── index_folder/
│       ├── faiss.index           # FAISS vector index
│       └── metadata.jsonl        # Chunk metadata
│
├── data/
│   └── bm25.pkl                  # Serialized BM25 index
│
└── evaluation/
    ├── retrieval_eval.py
    └── generation_eval.py
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

## 🚀 Running the Project

### 1️⃣ Clone Repository

```bash
git clone https://github.com/jeevanvishkarma/rag-vscode-assistant.git
cd rag-vscode-assistant
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Add Environment Variables

Create:

```text
.env
```

Add:

```env
OPENAI_API_KEY=your_api_key_here
```

---

### 4️⃣ Run Streamlit App

```bash
streamlit run app.py
```

---

## 💡 Example Queries

```text
VS Code Python interpreter not detected after update
```

```text
Copilot is really slow in VS Code
```

```text
VS Code crashes on macOS when opening terminal
```

```text
Python environment keeps changing
```

---

## 🔮 Future Improvements

- Neighbor chunk expansion
- Elasticsearch/OpenSearch integration
- Streaming responses
- Multi-query retrieval
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