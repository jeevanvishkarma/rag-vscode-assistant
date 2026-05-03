from sentence_transformers import CrossEncoder

# load once
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query, docs, top_k=3):
    pairs = [(query, doc['text']) for doc in docs]

    scores = reranker.predict(pairs)

    # combine docs + scores
    scored_docs = list(zip(docs, scores))

    # sort by score descending
    ranked = sorted(scored_docs, key=lambda x: x[1], reverse=True)

    # return top_k docs
    return [doc for doc, score in ranked[:top_k]]