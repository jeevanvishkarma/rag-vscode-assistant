import json

# Load the vscode issues
with open("vscode_issues.json", "r", encoding="utf-8") as f:
    all_data = json.load(f)
print(all_data)

# Create evaluation data
evaluation_data = [
    {
        "query": "explorer not showing files",
        "expected_ticket_id": [311208]
    },
    {
        "query": "copilot rate limit error",
        "expected_ticket_id": [311205, 311197]
    },
    {
        "query": "disable copilot",
        "expected_ticket_id": [311210]
    },
    {
        "query": "copilot summarization",
        "expected_ticket_id": [311196]
    },
    {
        "query": "chat conversation missing",
        "expected_ticket_id": [311168]
    },
    {
        "query": "sign in credentials",
        "expected_ticket_id": [311162]
    },
    {
        "query": "quota limit reached",
        "expected_ticket_id": [311147, 311146]
    },
    {
        "query": "terminal editor dragging",
        "expected_ticket_id": [311164]
    },
    {
        "query": "extension restart badge",
        "expected_ticket_id": [311167]
    },
    {
        "query": "search next match vertical center",
        "expected_ticket_id": [311180]
    }
]

# Save evaluation data
with open("evaluation_data.json", "w", encoding="utf-8") as f:
    json.dump(evaluation_data, f, indent=2)

print("Evaluation data created with", len(evaluation_data), "test cases")
print("Saved to evaluation_data.json")