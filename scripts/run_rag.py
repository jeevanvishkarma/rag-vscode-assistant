import sys
import os
import time

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# =====================================================
# RETRIEVAL
# =====================================================

from retrieval.retriever import retrieve as dense_retrieve

from retrieval.bm25_retriever import bm25_rerank

# =====================================================
# RERANK + GENERATION
# =====================================================

from retrieval.reranker import rerank

from generation.generate_answer import generate_answer


# =====================================================
# HYBRID RAG PIPELINE
# =====================================================

def run_rag(query, history=None):

    timings = {}

    # =================================================
    # STEP 1: DENSE RETRIEVAL
    # =================================================
    t0 = time.perf_counter()

    # retrieve broader semantic candidates
    dense_docs = dense_retrieve(
        query,
        k=100,
        history=history
    )

    timings["dense_retrieval"] = round(
        time.perf_counter() - t0,
        3
    )

    print(
        f"\n✅ Dense retrieved: "
        f"{len(dense_docs)}"
    )

    # =================================================
    # STEP 2: BM25 RERANK OVER DENSE CANDIDATES
    # =================================================
    t0 = time.perf_counter()

    # lexical refinement
    bm25_docs = bm25_rerank(
        query,
        dense_docs,
        top_k=20
    )

    timings["bm25"] = round(
        time.perf_counter() - t0,
        3
    )

    print(
        f"✅ BM25 reranked: "
        f"{len(bm25_docs)}"
    )

    # =================================================
    # STEP 3: CROSS-ENCODER RERANK
    # =================================================
    t0 = time.perf_counter()

    # NOW reranker only sees 20 docs
    docs = rerank(
        query,
        bm25_docs,
        top_k=5
    )

    timings["rerank"] = round(
        time.perf_counter() - t0,
        3
    )

    print(
        f"✅ Final reranked docs: "
        f"{len(docs)}"
    )

    # =================================================
    # STEP 4: GENERATION
    # =================================================
    t0 = time.perf_counter()

    answer = generate_answer(
        query,
        docs,
        history=history
    )

    timings["generation"] = round(
        time.perf_counter() - t0,
        3
    )

    # =================================================
    # TOTAL LATENCY
    # =================================================
    timings["total"] = round(
        sum(timings.values()),
        3
    )

    # =================================================
    # LOGGING
    # =================================================
    print(
        f"\n🔹 Dense Retrieval: "
        f"{timings['dense_retrieval']} sec"
    )

    print(
        f"🔹 BM25 Rerank: "
        f"{timings['bm25']} sec"
    )

    print(
        f"🔹 Cross-Encoder Rerank: "
        f"{timings['rerank']} sec"
    )

    print(
        f"🔹 Generation: "
        f"{timings['generation']} sec"
    )

    print(
        f"\n🚀 Total Latency: "
        f"{timings['total']} sec"
    )

    return answer, docs, timings


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    query = "What are the new features in Python 3.12?"

    answer, docs, timings = run_rag(query)

    print("\n============================")
    print("FINAL ANSWER")
    print("============================\n")

    print(answer)