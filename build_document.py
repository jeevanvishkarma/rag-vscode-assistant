import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS

def build_document(issue):
    comments_text = "\n".join(issue["comments"][:3])  # limit comments

    text = f"""
Title: {issue['title']}

Description:
{issue['description']}

Comments:
{comments_text}
"""
    return text.strip()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

def create_chunks(all_data):
    docs = []

    for issue in all_data:
        text = build_document(issue)
        chunks = splitter.split_text(text)

        for chunk in chunks:
            docs.append({
                "text": chunk,
                "metadata": {
                    "ticket_id": issue["ticket_id"],
                    "timestamp": issue["timestamp"]
                }
            })
    return docs



if __name__ == "__main__":
    with open("vscode_issues.json", "r", encoding="utf-8") as f:
        all_data = json.load(f)
    all_data = all_data[:10]
    chunks_docs =create_chunks(all_data)
    import json

    with open("chunks.json", "w") as f:
        json.dump(chunks_docs, f)
    # print("chunks_docs",chunks_docs)
    # Create embeddings and vectorstore
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode([d["text"] for d in chunks_docs])
    import faiss
    import numpy as np

    vectors = np.array(embeddings).astype("float32")
    print(vectors.shape)
    print("chunks_docs",len(chunks_docs))
    # print(vectors[:2])
    index = faiss.IndexFlatL2(vectors.shape[1])
    print("Index created",index)
    index.add(vectors)
    faiss.write_index(index, "faiss.index")
    query = "VS Code explorer not showing files"
    query_vector = model.encode([query]).astype("float32")

    faiss.normalize_L2(query_vector)
    D, I = index.search(query_vector, k=3)
    print("Distances:", D)
    print("Indices:", I)
    print(chunks_docs[50])


    
