from langchain_text_splitters import RecursiveCharacterTextSplitter

import jsonlines

# =========================================================
# CONFIG
# =========================================================

# INPUT JSONL FILE
INPUT_FILE = r"/Users/jeevanvishkarma/Desktop/LLM Projects/rag-vscode-assistant/data/vscode_issues_all.jsonl"

# OUTPUT CHUNKS JSONL
OUTPUT_FILE = r"/Users/jeevanvishkarma/Desktop/LLM Projects/rag-vscode-assistant/data/chunks_all.jsonl"


# CHUNK SETTINGS
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 150

# =========================================================
# SEMANTIC SPLITTER
# =========================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,

    # IMPORTANT:
    # preserve semantic structure first
    separators=[
        "\n# ",
        "\n\n",
        "\n",
        ". ",
        " ",
        ""
    ]
)

# =========================================================
# BUILD SEMANTIC ISSUE DOCUMENT
# =========================================================

def build_document(issue):

    # -----------------------------------
    # LABELS
    # -----------------------------------
    labels = ", ".join(
        issue.get("labels", [])
    )

    # -----------------------------------
    # COMMENTS
    # -----------------------------------
    comments = issue.get("comments", [])

    comments_text = "\n\n".join(
        comments[:3]   # limit comments
    )

    # -----------------------------------
    # FINAL SEMANTIC DOCUMENT
    # -----------------------------------
    text = f"""
# TITLE
{issue.get('title', '')}

# LABELS
{labels}

# DESCRIPTION
{issue.get('description', '')}

# COMMENTS
{comments_text}
"""

    return text.strip()

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    total_issues = 0
    total_chunks = 0

    # =====================================================
    # STREAM INPUT JSONL
    # =====================================================
    with jsonlines.open(INPUT_FILE) as reader:

        # =================================================
        # WRITE OUTPUT JSONL
        # =================================================
        with jsonlines.open(
            OUTPUT_FILE,
            mode="w"
        ) as writer:

            for issue in reader:

                total_issues += 1

                # =========================================
                # BUILD FULL ISSUE DOCUMENT
                # =========================================
                full_text = build_document(issue)

                # =========================================
                # SMALL ISSUES
                # KEEP WHOLE
                # =========================================
                if len(full_text) <= CHUNK_SIZE:

                    writer.write({
                        "text": full_text,
                        "ticket_id": issue.get("ticket_id"),
                        "title": issue.get("title"),
                        "timestamp": issue.get("timestamp"),
                        "labels": issue.get("labels", []),
                        "chunk_index": 0
                    })

                    total_chunks += 1

                # =========================================
                # LARGE ISSUES
                # SPLIT SEMANTICALLY
                # =========================================
                else:

                    chunks = text_splitter.split_text(
                        full_text
                    )

                    for idx, chunk in enumerate(chunks):

                        writer.write({
                            "text": chunk,
                            "ticket_id": issue.get("ticket_id"),
                            "title": issue.get("title"),
                            "timestamp": issue.get("timestamp"),
                            "labels": issue.get("labels", []),
                            "chunk_index": idx
                        })

                        total_chunks += 1

                # =========================================
                # LOGGING
                # =========================================
                if total_issues % 5000 == 0:

                    print(
                        f"✅ Issues processed: {total_issues} | "
                        f"Chunks created: {total_chunks}"
                    )

    # =====================================================
    # DONE
    # =====================================================
    print("\n🚀 DONE")
    print(f"✅ Total issues processed: {total_issues}")
    print(f"✅ Total chunks created: {total_chunks}")
    print(f"✅ Output saved to: {OUTPUT_FILE}")