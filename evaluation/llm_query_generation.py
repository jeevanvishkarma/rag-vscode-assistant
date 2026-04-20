import json,random
import ast
import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import generation.call_llm as call_llm
issues_data = json.load(open("data\\vscode_issues.json", "r", encoding="utf-8"))
random_issue = random.sample(issues_data, 25)
real_issue_title =[issue['title'] for issue in random_issue]
short_issues = [ issue["title"] + " " + issue["description"][:150]
        for issue in random_issue
    ]

prompt = f"""
You are simulating real users typing search queries into Google or StackOverflow.

For each issue below, generate EXACTLY 2 queries.

Rules:
- Each query must be <= 10 words
- Use natural, casual language (like real users)
- Avoid repeating the same structure
- Do NOT copy the issue text directly
- Make queries slightly varied (one short, one descriptive)
- No punctuation at the end
- No explanations

Output format:
Return ONLY a valid Python list of strings.
Total queries = 2 × number of issues
Do NOT include any text other than the list.
Do NOT add python or ``` or list in output.

Example:
["vscode explorer not showing files", "why are files missing in vscode folder"]

Issues:
{short_issues}"""

response = call_llm.call_llm(prompt, max_tokens=800)
print("Generated Queries:", response)
generated_queries = ast.literal_eval(response)
all_queries = real_issue_title + generated_queries
with open("data\\llm_generated_queries.json", "w", encoding="utf-8") as f:
    json.dump(all_queries, f, indent=2)
