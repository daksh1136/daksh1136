import json
from pathlib import Path
import datetime as dt

DATA = Path("data/contributions.json")
OUT = Path("contrib-heatmap.svg")
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def esc(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def main():
    obj = json.loads(DATA.read_text(encoding="utf-8"))
    days = obj["days"]
    stats = obj["stats"]
    if not days:
        raise RuntimeError("No contribution data found. Run fetch_contributions.py first.")

    start = dt.date.fromisoformat(days[0]["date"])
    pad = (start.weekday() + 1) % 7
    cells = [{"date": "", "count": 0, "level": 0}] * pad + days
    weeks = [cells[i:i + 7] for i in range(0, len(cells), 7)]
    while len(weeks[-1]) < 7:
        weeks[-1].append({"date": "", "count": 0, "level": 0})

    cell, gap, left, top = 13, 3, 48, 45
    step = cell + gap
    width, height = max(860, left + len(weeks) * step + 25), 175

    svg = [f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" rx="10" fill="#0d1117" stroke="#30363d"/>
<style>
.h {{ font-family:"Cascadia Mono","Consolas",monospace; fill:#c9d1d9; font-size:13px; font-weight:bold; }}
.t {{ font-family:"Cascadia Mono","Consolas",monospace; fill:#8b949e; font-size:11px; }}
.c {{ opacity:0; animation:pop .42s ease-out forwards; }}
@keyframes pop {{
from {{ opacity:0; transform:translateY(-7px); }}
to {{ opacity:1; transform:translateY(0); }}
}}
</style>
<text class="h" x="18" y="23">daksh@github ~ $ ./contributions.sh</text>
<text class="t" x="15" y="63">Sun</text><text class="t" x="15" y="79">Mon</text>
<text class="t" x="15" y="95">Tue</text><text class="t" x="15" y="111">Wed</text>
<text class="t" x="15" y="127">Thu</text><text class="t" x="15" y="143">Fri</text>
<text class="t" x="15" y="159">Sat</text>
"""]

    delay = 0.0
    for wi, week in enumerate(weeks):
        for di, day in enumerate(week):
            x, y = left + wi * step, top + di * step
            level = max(0, min(5, int(day.get("level", 0))))
            title = f'{day.get("date", "")}: {day.get("count", 0)} contributions'
            svg.append(
                f'<rect class="c" style="animation-delay:{delay:.3f}s" '
                f'x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" '
                f'fill="{PALETTE[level]}"><title>{esc(title)}</title></rect>'
            )
            delay += 0.008

    footer_y = height - 11
    best = stats.get("best_day", {})
    svg.append(
        f'<text class="t" x="{left}" y="{footer_y}">'
        f'{stats.get("total", 0):,} contributions • current streak '
        f'{stats.get("current_streak", 0)} • longest '
        f'{stats.get("longest_streak", 0)} • best day '
        f'{best.get("count", 0):,}</text>'
    )
    legend_x = width - 126
    svg.append(f'<text class="t" x="{legend_x - 5}" y="{footer_y}">Less</text>')
    for i, color in enumerate(PALETTE):
        svg.append(f'<rect x="{legend_x + 28 + i * 14}" y="{footer_y - 10}" width="11" height="11" rx="2" fill="{color}"/>')
    svg.append(f'<text class="t" x="{width - 12}" y="{footer_y}" text-anchor="end">More</text>')
    svg.append("</svg>")

    OUT.write_text("\\n".join(svg), encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
