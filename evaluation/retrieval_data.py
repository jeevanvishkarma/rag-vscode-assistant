import json,os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
import json


# same embedding model (IMPORTANT!)
embeddings = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# load vectorstore
vectorstore = FAISS.load_local(
    r"faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# create retriever
# retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

def retrieve(query):
    retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 3, "lambda_mult": 0.7}
        )
    docs = retriever.invoke(query)
    return docs

if __name__ == "__main__":
    query_data = json.load(open("data\\llm_generated_queries.json", "r", encoding="utf-8"))

    retrieval_output = []
    for query in query_data:
        print(f"\n🔍 Query: {query}")
        query_result = {"query": query, "results": []}
        docs = retrieve(query)
        for i, doc in enumerate(docs):
            print(f"\nResult {i+1}")
            query_result["results"].append(doc.page_content)
            # print(doc.page_content[:300])
        retrieval_output.append(query_result)

    with open("data\\retrieval_results.json", "w", encoding="utf-8") as f:
        json.dump(retrieval_output, f, indent=4)