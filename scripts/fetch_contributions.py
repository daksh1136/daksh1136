import json, re
from datetime import datetime, timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup

USERNAME = "daksh1136"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path("data/contributions.json")

r = requests.get(URL, timeout=30, headers={"User-Agent": "daksh1136-profile-art"})
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")

days = []
for cell in soup.select("td.ContributionCalendar-day"):
    date = cell.get("data-date")
    level = cell.get("data-level")
    if not date or level is None:
        continue
    tooltip = cell.get("data-tooltip") or ""
    m = re.search(r"([\d,]+)\s+contribution", tooltip)
    count = int(m.group(1).replace(",", "")) if m else 0
    days.append({"date": date, "count": count, "level": int(level)})

if not days:
    raise RuntimeError("No contribution cells found; GitHub may have changed its HTML.")

days.sort(key=lambda x: x["date"])
run = longest = 0
for d in days:
    if d["count"] > 0:
        run += 1
        longest = max(longest, run)
    else:
        run = 0

current = 0
for d in reversed(days):
    if d["count"] > 0:
        current += 1
    else:
        break

best = max(days, key=lambda x: x["count"])
monthly = {}
for d in days:
    monthly[d["date"][:7]] = monthly.get(d["date"][:7], 0) + d["count"]

payload = {
    "username": USERNAME,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "days": days,
    "stats": {
        "total": sum(d["count"] for d in days),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best,
        "monthly_totals": monthly
    }
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(f"Wrote {OUT} with {len(days)} days.")
