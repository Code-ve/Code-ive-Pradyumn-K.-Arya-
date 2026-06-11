import requests
import re
from collections import defaultdict
from datetime import datetime

HANDLE = "pradyumn_k.arya"

# Get user info
user = requests.get(
    f"https://codeforces.com/api/user.info?handles={HANDLE}"
).json()["result"][0]

rating = user.get("rating", "Unrated")
max_rating = user.get("maxRating", "Unrated")

# Get submissions
subs = requests.get(
    f"https://codeforces.com/api/user.status?handle={HANDLE}"
).json()["result"]

solved = {}

for sub in subs:
    if sub.get("verdict") != "OK":
        continue

    problem = sub["problem"]

    key = (
        problem.get("contestId"),
        problem.get("index")
    )

    solved[key] = problem

distribution = defaultdict(int)

for problem in solved.values():
    r = problem.get("rating")

    if r is None:
        continue

    bucket = (r // 100) * 100
    distribution[bucket] += 1

total = len(solved)

stats = f"""
Current Rating: {rating}
Max Rating: {max_rating}

Problems Solved: {total}

Rating Distribution
"""

for bucket in sorted(distribution):
    stats += f"\n{bucket:<4} → {distribution[bucket]}"

stats += f"\n\nLast Updated: {datetime.utcnow().strftime('%Y-%m-%d')}"

with open("README.md", "r", encoding="utf8") as f:
    readme = f.read()

pattern = r'<!-- CF_STATS_START -->(.*?)<!-- CF_STATS_END -->'

replacement = (
    "<!-- CF_STATS_START -->\n"
    + stats +
    "\n<!-- CF_STATS_END -->"
)

readme = re.sub(
    pattern,
    replacement,
    readme,
    flags=re.S
)

with open("README.md", "w", encoding="utf8") as f:
    f.write(readme)
