import pickle
import jsonlines
from rank_bm25 import BM25Okapi

# =====================================================
# PATHS
# =====================================================

META_FILE = r"faiss_index/metadata.jsonl"

OUTPUT_FILE = r"data/bm25.pkl"

# =====================================================
# LOAD METADATA
# =====================================================

docs = []

with jsonlines.open(META_FILE) as reader:

    for obj in reader:
        docs.append(obj)

print(f"✅ Loaded docs: {len(docs)}")

# =====================================================
# TOKENIZE
# =====================================================

tokenized_corpus = [
    doc["text"].lower().split()
    for doc in docs
]

print("✅ Tokenization complete")

# =====================================================
# BUILD BM25
# =====================================================

bm25 = BM25Okapi(tokenized_corpus)

print("✅ BM25 index created")

# =====================================================
# SAVE PICKLE
# =====================================================

with open(OUTPUT_FILE, "wb") as f:

    pickle.dump({
        "bm25": bm25,
        "docs": docs
    }, f)

print(f"✅ BM25 saved to: {OUTPUT_FILE}")