🤖 VS Code Issues RAG Assistant

Semantic + Hybrid Retrieval over GitHub VS Code Issues using FAISS, BM25, Cross-Encoder Reranking, and GPT-4o-mini.

⸻

🚀 Demo

Add your demo GIF / screenshots here

/demo/demo.gif

⸻

📌 Overview

This project is a production-style Retrieval-Augmented Generation (RAG) system built on top of GitHub VS Code Issues.

The assistant can:

* Perform semantic search over GitHub issues
* Retrieve relevant issues using FAISS vector search
* Improve exact keyword matching using BM25
* Rerank results using a Cross-Encoder reranker
* Generate contextual answers using GPT-4o-mini
* Support conversational history-aware retrieval
* Display retrieval latency and retrieved context

The project focuses heavily on:

* Retrieval quality
* Low latency
* Hybrid search architecture
* Real-world scalability
* Semantic chunking

⸻

🧠 Architecture

User Query
    ↓
Dense Retrieval (FAISS IVF)
    ↓
Top 100 Semantic Candidates
    ↓
BM25 Lexical Reranking
    ↓
Top 20 Candidates
    ↓
Cross-Encoder Reranking
    ↓
Top 5 Final Context Chunks
    ↓
GPT-4o-mini
    ↓
Generated Answer

⸻

✨ Features

🔎 Hybrid Retrieval

Combines:

* Dense semantic retrieval using Sentence Transformers + FAISS
* Lexical retrieval refinement using BM25

This improves:

* Exact technical term matching
* Version-specific retrieval
* Error/log retrieval
* Semantic understanding

⸻

⚡ Fast Retrieval

Uses:

* FAISS IVF Index
* Approximate Nearest Neighbor Search
* Cross-Encoder reranking only on narrowed candidates

Optimized for:

* Large-scale datasets
* Low latency retrieval
* GPU-efficient embeddings

⸻

🧩 Semantic Chunking

Custom semantic chunking pipeline:

* Preserves issue structure
* Maintains title + description context
* Stores metadata separately
* Optimized for retrieval quality

⸻

🧠 Conversational Retrieval

Supports:

* Multi-turn chat history
* Query rewriting
* Context-aware retrieval

⸻

📊 Latency Tracking

The UI displays:

* Dense retrieval latency
* BM25 latency
* Cross-encoder reranking latency
* Generation latency
* Total pipeline latency

⸻

🛠️ Tech Stack

Component	Technology
Embeddings	Sentence Transformers
Vector DB	FAISS IVF
Lexical Search	BM25
Reranker	Cross-Encoder
LLM	GPT-4o-mini
UI	Streamlit
Backend	Python
Dataset	GitHub VS Code Issues

⸻

📂 Project Structure

project/
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
├── scripts/
│   └── run_rag.py
│
├── ingestion/
│   ├── create_chunks.py
│   ├── create_embeddings.py
│   └── build_bm25.py
│
├── files/
│   └── index_folder/
│       ├── faiss.index
│       └── metadata.jsonl
│
├── data/
│   └── bm25.pkl
│
├── demo/
│   └── demo.gif
│
├── requirements.txt
│
└── README.md

⸻

📦 Dataset

The system is built on top of GitHub VS Code Issues.

Dataset characteristics:

* ~250K GitHub issues
* ~800K semantic chunks
* Includes:
    * Titles
    * Descriptions
    * Comments
    * Metadata

⸻

🧪 Retrieval Pipeline

1️⃣ Dense Retrieval

Uses:

* SentenceTransformer embeddings
* FAISS IVF index

Purpose:

* Broad semantic recall
* Fast approximate nearest-neighbor retrieval

Retrieves:

Top 100 semantic candidates

⸻

2️⃣ BM25 Lexical Reranking

Purpose:

* Improve exact keyword matching
* Better handling of:
    * Version numbers
    * Error messages
    * Package names
    * APIs
    * Stack traces

BM25 reranks only the FAISS candidates.

This avoids expensive full-corpus lexical search.

Produces:

Top 20 lexical candidates

⸻

3️⃣ Cross-Encoder Reranking

Uses a transformer reranker to:

* Improve precision
* Remove semantic noise
* Rank final candidates more accurately

Produces:

Top 5 final chunks

⸻

4️⃣ Answer Generation

The final chunks are passed to GPT-4o-mini for answer generation.

⸻

📈 Retrieval Metrics

Example evaluation metrics:

{
  "precision_at_k": 0.679,
  "recall_at_k": 0.962,
  "mrr": 0.94
}

⸻

⚙️ Installation

1️⃣ Clone Repository

git clone <your_repo_url>
cd <repo_name>

⸻

2️⃣ Create Virtual Environment

python -m venv venv

Activate:

Windows

venv\Scripts\activate

macOS/Linux

source venv/bin/activate

⸻

3️⃣ Install Requirements

pip install -r requirements.txt

⸻

🔑 Environment Variables

Create:

.env

Add:

OPENAI_API_KEY=your_api_key_here

⸻

🚀 Running the App

streamlit run app.py

⸻

🧱 Building the Pipeline

1️⃣ Create Semantic Chunks

python ingestion/create_chunks.py

⸻

2️⃣ Create FAISS Embeddings

python ingestion/create_embeddings.py

⸻

3️⃣ Build BM25 Index

python ingestion/build_bm25.py

⸻

💻 Example Queries

VS Code Python interpreter not detected after update
Explorer not showing files after opening workspace
Copilot is really slow in VS Code
VS Code crashes on macOS when opening terminal
Python environment keeps changing

⸻

🔮 Future Improvements

Potential future enhancements:

* Neighbor chunk expansion
* Parent-child retrieval
* Multi-query retrieval
* Elasticsearch/OpenSearch integration
* Streaming responses
* Agentic workflows
* Citation support
* Better query rewriting
* Feedback loops for retrieval improvement

⸻

📸 UI Preview

Add screenshots here

⸻

🙌 Acknowledgements

Built using:

* FAISS
* Sentence Transformers
* Streamlit
* OpenAI APIs
* BM25
* LangChain

