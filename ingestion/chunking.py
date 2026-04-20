from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import json,os

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

def create_documents(all_data):
    documents = []

    for issue in all_data:
        text = build_document(issue)

        doc = Document(
            page_content=text,
            metadata={
                "ticket_id": issue["ticket_id"],
                "timestamp": issue["timestamp"]
            }
        )

        documents.append(doc)

    return documents

def chunk_document(document, chunk_size=500, overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = text_splitter.split_documents(document)
    return chunks
VECTORSTORE_PATH = r'C:\Users\jeeva\OneDrive\Desktop\Rag_Chatbot\vs_code_issues_rag\faiss_index'
def create_or_update_embeddings(chunks, persist_directory=VECTORSTORE_PATH):
    """Create new or update existing vectorstore"""
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # If vectorstore exists, load and add new chunks
    if os.path.exists(persist_directory):
        print("Adding to existing vectorstore...")
        vectorstore = FAISS.load_local(persist_directory, embeddings,allow_dangerous_deserialization= True)
        vectorstore.add_documents(chunks)
    else:
        print("Creating new vectorstore...")
        vectorstore = FAISS.from_documents(chunks, embeddings)
    
    vectorstore.save_local(persist_directory)
    return vectorstore

if __name__ == "__main__":
    with open("vscode_issues.json", "r", encoding="utf-8") as f:
        all_data = json.load(f)
    documents = create_documents(all_data)
    chunks = chunk_document(documents)
    create_or_update_embeddings(chunks)