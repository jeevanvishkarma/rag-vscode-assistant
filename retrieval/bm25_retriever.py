# retrieval/bm25_retriever.py

from rank_bm25 import BM25Okapi
import numpy as np


# =====================================================
# BM25 OVER CANDIDATES ONLY
# =====================================================

def bm25_rerank(query, candidate_docs, top_k=20):

    # ---------------------------------------------
    # TOKENIZE CANDIDATES
    # ---------------------------------------------
    tokenized_corpus = [

        doc["text"].lower().split()

        for doc in candidate_docs
    ]

    # ---------------------------------------------
    # BUILD TEMP BM25
    # ---------------------------------------------
    bm25 = BM25Okapi(tokenized_corpus)

    # ---------------------------------------------
    # QUERY
    # ---------------------------------------------
    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = [
        candidate_docs[i]
        for i in top_indices
    ]

    return results