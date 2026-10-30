#!/usr/bin/env python3
"""Rebuild each Learning Center topic page's article list and ItemList schema from /articles/index.html.
Run after adding, merging or retiring an article, so topic pages never drift from the Learning Center."""
import json, re, html as H
from datetime import date

SITE = "https://www.bluegrassmedicarehelp.com"
HUBS = {"basics": ("basics", "Medicare Basics"), "coverage": ("coverage", "Coverage Choices"),
        "costs": ("costs", "Costs &amp; Savings"), "on-medicare": ("onmedicare", "Already on Medicare"),
        "turning-65": ("turning65", "Turning 65")}
lc = open("articles/index.html", encoding="utf-8").read()
rows = re.findall(r'<a class="lcrow" data-cat="([^"]+)" data-date="([^"]+)" href="([^"]+)">.*?<h2 class="lcrow-title">(.*?)</h2>\s*<p class="lcrow-dek">(.*?)</p>', lc, re.S)
plain = lambda s: re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", s))).strip()

for slug, (cat, tag) in HUBS.items():
    p = f"articles/{slug}/index.html"; h = open(p, encoding="utf-8").read()
    mine = sorted([r for r in rows if cat in r[0].split()], key=lambda r: r[1], reverse=True)
    out = []
    for cats, d, url, title, dek in mine:
        t = tag if cat != "turning65" or "ss" not in cats.split() else "Social Security"
        nice = date.fromisoformat(d).strftime("%b %-d, %Y")
        out.append(f'    <a class="hubrow" href="{url}">\n      <div class="hubrow-main">\n'
                   f'        <div class="hubrow-meta"><span class="hubtag">{t}</span><span class="hubdate">{nice}</span></div>\n'
                   f'        <h2 class="hubrow-title">{title.strip()}</h2>\n        <p class="hubrow-dek">{dek.strip()}</p>\n'
                   f'      </div>\n      <span class="hubrow-go">Read &rarr;</span>\n    </a>')
    s = h.index('<div class="hublist">'); last = h.rfind('class="hubrow"')
    e = h.index("</div>", h.index("</a>", last)) + len("</div>") if last > s else h.index("</div>", s) + len("</div>")
    h = h[:s] + '<div class="hublist">\n' + "\n".join(out) + "\n  </div>" + h[e:]
    def fix(m):
        d = json.loads(m.group(1)); nodes = d.get("@graph", [d])
        for n in nodes:
            for holder in (n, n.get("mainEntity") if isinstance(n.get("mainEntity"), dict) else None):
                if isinstance(holder, dict) and holder.get("@type") == "ItemList":
                    holder["itemListElement"] = [{"@type": "ListItem", "position": i + 1, "url": SITE + r[2], "name": plain(r[3])} for i, r in enumerate(mine)]
                    if "numberOfItems" in holder: holder["numberOfItems"] = len(mine)
        return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>"
    h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, h, flags=re.S)
    open(p, "w", encoding="utf-8").write(h)
    print(f"{slug:12s} {len(mine)} guides")
