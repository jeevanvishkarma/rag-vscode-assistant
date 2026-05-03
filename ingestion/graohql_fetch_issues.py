import requests
import json
import time
import os

# ==============================
# CONFIG (EDIT ONLY THIS)
# ==============================git 
GITHUB_TOKEN = os.getenv("git_token")

import requests
import json
import time
import os
from dotenv import load_dotenv

# ==============================
# LOAD ENV (FIX PATH IF NEEDED)
# ==============================

# ==============================
# CONFIG (EDIT ONLY THIS)
# ==============================
# GITHUB_TOKEN = os.getenv("git_token")

OWNER = "microsoft"
REPO = "vscode"

MAX_ISSUES = None        # 👉 None = ALL
COMMENTS_LIMIT = 5
MIN_BODY_LENGTH = 50

SAVE_MODE = "jsonl"     # "jsonl" OR "json"
OUTPUT_FILE = "vscode_issues_all"

# ==============================

URL = "https://api.github.com/graphql"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

QUERY = """
query($cursor: String, $comments_limit: Int!) {
  repository(owner: "%s", name: "%s") {
    issues(first: 100, after: $cursor, states: [OPEN, CLOSED]) {
      pageInfo {
        hasNextPage
        endCursor
      }
      nodes {
        number
        title
        body
        createdAt
        labels(first: 5) {
          nodes {
            name
          }
        }
        comments(first: $comments_limit) {
          nodes {
            body
          }
        }
      }
    }
  }
}
""" % (OWNER, REPO)


def run_query(cursor=None):
    variables = {
        "cursor": cursor,
        "comments_limit": COMMENTS_LIMIT
    }

    response = requests.post(
        URL,
        json={"query": QUERY, "variables": variables},
        headers=HEADERS
    )

    if response.status_code != 200:
        print("Error:", response.text)
        return None

    return response.json()


def main():
    cursor = None
    total_count = 0

    all_data = []

    if SAVE_MODE == "jsonl":
        file = open(f"{OUTPUT_FILE}.jsonl", "w", encoding="utf-8")

    while True:
        result = run_query(cursor)

        if result is None:
            break

        issues = result["data"]["repository"]["issues"]["nodes"]
        page_info = result["data"]["repository"]["issues"]["pageInfo"]

        for issue in issues:

            if not issue["body"] or len(issue["body"]) < MIN_BODY_LENGTH:
                continue

            comments = [
                c["body"] for c in issue["comments"]["nodes"]
                if c.get("body")
            ]

            labels = [
                l["name"] for l in issue["labels"]["nodes"]
                if l.get("name")
            ]

            issue_data = {
                "ticket_id": issue["number"],
                "title": issue["title"],
                "description": issue["body"],
                "labels": labels,
                "timestamp": issue["createdAt"],
                "comments": comments
            }

            # SAVE
            if SAVE_MODE == "jsonl":
                file.write(json.dumps(issue_data) + "\n")
            else:
                all_data.append(issue_data)

            total_count += 1

            if MAX_ISSUES and total_count >= MAX_ISSUES:
                print(f"\nDone. Collected {total_count} issues.")
                break

        print(f"Collected so far: {total_count}")

        if MAX_ISSUES and total_count >= MAX_ISSUES:
            break

        if not page_info["hasNextPage"]:
            break

        cursor = page_info["endCursor"]

        time.sleep(1)

    if SAVE_MODE == "jsonl":
        file.close()

    if SAVE_MODE == "json":
        with open(f"{OUTPUT_FILE}.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=2)

    print(f"\nFinished. Total collected: {total_count}")


if __name__ == "__main__":
    main()