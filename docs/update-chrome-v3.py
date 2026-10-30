#!/usr/bin/env python3
"""Sitewide header update for the 2026 redesign (idempotent).
- Nav links: Turning 65 | Learning Center | Your County | About (Videos moves to the footer only).
- Call button shows the number on wide screens.
- Top strip: statewide framing instead of 'Serving Fayette & surrounding counties'."""
import glob, re

NAVLINKS = ('<div class="navlinks" id="navlinks">\n      <a href="/turning-65/">Turning 65</a>\n      <a href="/articles/">Learning Center</a>\n'
            '      <a href="/kentucky/">Your County</a>\n      <a href="/about/">About</a>\n    </div>')
STRIP_RE = re.compile(r'<span>(?:📍|&#128205;|\\U0001F4CD) <strong>Lexington, Kentucky</strong> (?:&nbsp;)?(?:·|&middot;)(?:&nbsp;)? Serving Fayette &amp; surrounding counties</span>')
STRIP = '<span><strong>Free Medicare help for all of Kentucky</strong> &nbsp;&middot;&nbsp; Office in Lexington</span>'
CALL_RE = re.compile(r'(<a class="navcta" href="tel:18597858289">\s*<svg.*?</svg>)\s*Call\s*</a>', re.S)
changed = 0
for p in glob.glob("**/index.html", recursive=True):
    if p.startswith("mockups/") or p == "index.html":
        continue
    h = open(p, encoding="utf-8").read(); o = h
    m = re.search(r'<div class="navlinks" id="navlinks">(.*?)</div>', h, re.S)
    if m:
        cur = re.search(r'href="([^"]+)"[^>]*(?:aria-current="page"|class="active")', m.group(1))
        new = NAVLINKS
        if cur:
            new = new.replace(f'<a href="{cur.group(1)}">', f'<a href="{cur.group(1)}" aria-current="page">', 1)
        h = h[:m.start()] + new + h[m.end():]
    h = STRIP_RE.sub(STRIP, h)
    h = CALL_RE.sub(r'\1Call<span class="nc-num">&nbsp;(859) 785-8289</span></a>', h)
    if h != o:
        open(p, "w", encoding="utf-8").write(h); changed += 1
print("pages updated:", changed)
