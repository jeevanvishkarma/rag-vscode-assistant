import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ==============================
# PATH SETUP (ROBUST)
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INDEX_PATH = os.path.join(BASE_DIR, "..", "faiss_index", "faiss.index")
META_PATH = os.path.join(BASE_DIR, "..", "faiss_index", "metadata.jsonl")

print("Index path:", INDEX_PATH)
print("Exists:", os.path.exists(INDEX_PATH))

# ==============================
# LOAD MODEL
# ==============================
print("\n🔹 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ==============================
# LOAD FAISS INDEX
# ==============================
print("🔹 Loading FAISS index...")
index = faiss.read_index(INDEX_PATH)

# ==============================
# LOAD METADATA
# ==============================
print("🔹 Loading metadata...")

metadata = []
with open(META_PATH, "r", encoding="utf-8") as f:
    for line in f:
        metadata.append(json.loads(line))

print(f"✅ Metadata loaded: {len(metadata)} records")

# ==============================
# RETRIEVE FUNCTION
# ==============================
def retrieve(query, k=10,history=None):
    # encode query
    query_vector = model.encode([query]).astype("float32")

    # normalize (IMPORTANT for cosine similarity)
    faiss.normalize_L2(query_vector)

    # search
    D, I = index.search(query_vector, k)

    results = []
    for idx in I[0]:
        if idx < len(metadata):
            results.append(metadata[idx])

    return results


# ==============================
# TEST
# ==============================
if __name__ == "__main__":
    query = "VS Code explorer not showing files"

    results = retrieve(query, k=5)

    print("\n🔹 Results:\n")
    for i, r in enumerate(results):
        print(f"{i+1}.", r)