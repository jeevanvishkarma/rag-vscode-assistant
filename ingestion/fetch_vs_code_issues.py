import requests, time,json,os
import dotenv
dotenv.load_dotenv()
import streamlit as st

def get_secret(key):
    value = os.getenv(key)
    if not value:
        st.error(f"Error: {key} not found in environment variables.")
        st.stop()
    return value



TOKEN = get_secret("git_token")


OWNER = "microsoft"
REPO = "vscode"

url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}"
}

all_data = []
def safe_request(url, headers):
    for _ in range(3):  # retry 3 times
        try:
            response = requests.get(url, headers=headers, timeout=10)
            return response
        except requests.exceptions.RequestException as e:
            print("Retrying due to error:", e)
            time.sleep(2)
    return None

for page in range(1, 21):   # 20 pages × 100 = 2000 issues
    params = {
        "state": "all",
        "per_page": 100,
        "page": page
    }

    response = requests.get(url, headers=headers, params=params)
    issues = response.json()

    if not issues:
        break

    for issue in issues:
        if "pull_request" in issue:
            continue

        if not issue.get("body"):
            continue

        # fetch comments
        import requests

        # comments_resp = requests.get(issue["comments_url"], headers=headers)
        comments_resp =safe_request(issue["comments_url"], headers)
        # comments = comments_resp.json()
        # comments_resp = None
        if comments_resp is not None:
            comments = comments_resp.json()

            comments_list = [c["body"] for c in comments if c.get("body")]

            if len(comments_list) == 0:
                continue

            issue_data = {
                "ticket_id": issue["number"],
                "title": issue["title"],
                "description": issue["body"],
                "labels": [l["name"] for l in issue["labels"]],
                "timestamp": issue["created_at"],
                "comments": comments_list
            }

            all_data.append(issue_data)

    print(f"Page {page} done → Total: {len(all_data)}")

    time.sleep(1)  # avoid rate limit
# print(all_data)
with open("vscode_issues.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)
print(f"\nFinal dataset size: {len(all_data)}")
