#!/usr/bin/env python3
"""Apply the 2026 header and footer (docs/chrome_v4.py) to every page. Idempotent."""
import glob, sys
sys.path.insert(0, "docs")
from chrome_v4 import apply
n = 0
for p in glob.glob("**/index.html", recursive=True):
    if p.startswith(("mockups/", "dist/")): continue
    h = open(p, encoding="utf-8").read(); o = apply(h)
    if o != h: open(p, "w", encoding="utf-8").write(o); n += 1
print("pages updated:", n)
