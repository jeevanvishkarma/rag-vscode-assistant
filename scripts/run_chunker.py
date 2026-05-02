import os
import jsonlines
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==============================
# PATHS
# ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

INPUT_FILE = os.path.join(DATA_DIR, "vscode_issues_all.jsonl")
OUTPUT_FILE = os.path.join(DATA_DIR, "all_chunks.jsonl")

# ==============================
# CONFIG
# ==============================
CHUNK_SIZE = 400
CHUNK_OVERLAP = 80
COMMENTS_LIMIT = 3

# ==============================
# CHUNKER
# ==============================
splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

def build_document(issue):
    comments = "\n".join(issue.get("comments", [])[:COMMENTS_LIMIT])

    return f"""
Title: {issue['title']}

Description:
{issue['description']}

Comments:
{comments}
""".strip()

# ==============================
# MAIN
# ==============================
def main():
    count = 0

    with jsonlines.open(INPUT_FILE) as reader, \
         jsonlines.open(OUTPUT_FILE, "w") as writer:

        for issue in reader:
            if not issue.get("description") or len(issue["description"]) < 50:
                continue

            text = build_document(issue)
            chunks = splitter.split_text(text)

            for chunk in chunks:
                writer.write({
                    "text": chunk,
                    "ticket_id": issue["ticket_id"],
                    "timestamp": issue["timestamp"]
                })
                count += 1

            if count % 10000 == 0:
                print(f"Chunks written: {count}")

    print(f"✅ Done. Total chunks: {count}")


if __name__ == "__main__":
    main()