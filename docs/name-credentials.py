#!/usr/bin/env python3
"""Show the partners' degrees after their names (November 2026; idempotent): Austin Tyler, MBA and
Andrew Horn, MHA. Applies to visible name labels (bylines, advisor cards, figure captions, the
"Written and reviewed by" line) in public pages and the page builders, and adds honorificSuffix to
their Person nodes in JSON-LD. Alt text, review quotes and running prose are left alone."""
import glob, json, re

CRED = {"Austin Tyler": "MBA", "Andrew Horn": "MHA"}
LABELS = [
    # <b>Name</b>, <h3>Name</h3>, "Written and reviewed by Name</b>"
    (re.compile(r'(<b>|<h3>)(Austin Tyler|Andrew Horn)(</b>|</h3>)'), lambda m: f"{m.group(1)}{m.group(2)}, {CRED[m.group(2)]}{m.group(3)}"),
    (re.compile(r'(Written and reviewed by )(Austin Tyler)(?!, MBA)'), lambda m: f"{m.group(1)}{m.group(2)}, MBA"),
    # both partners in one label
    (re.compile(r'<b>Austin Tyler (&amp;|and) Andrew Horn</b>'), lambda m: f"<b>Austin Tyler, MBA {m.group(1)} Andrew Horn, MHA</b>"),
]

def schema(m):
    raw = m.group(1)
    try:
        d = json.loads(raw)
    except ValueError:
        return m.group(0)
    hit = False
    def walk(n):
        nonlocal hit
        if isinstance(n, dict):
            if n.get("@type") == "Person" and n.get("name") in CRED and n.get("honorificSuffix") != CRED[n["name"]]:
                n["honorificSuffix"] = CRED[n["name"]]; hit = True
            for v in n.values(): walk(v)
        elif isinstance(n, list):
            for v in n: walk(v)
    walk(d)
    if not hit:
        return m.group(0)
    compact = '":"' in raw[:300]
    out = json.dumps(d, ensure_ascii=False, separators=(",", ":")) if compact else json.dumps(d, ensure_ascii=False)
    return '<script type="application/ld+json">' + out + "</script>"

def apply(h, is_html=True):
    for rx, fn in LABELS:
        h = rx.sub(fn, h)
    if is_html:
        h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', schema, h, flags=re.S)
    return h

if __name__ == "__main__":
    changed = []
    files = [p for p in glob.glob("**/index.html", recursive=True) + ["404.html"] if not p.startswith(("mockups/", "dist/"))]
    files += [p for p in glob.glob("docs/build-*.py") if "tig" not in p]   # the Tyler Insurance Group site keeps its own byline spec
    for p in sorted(set(files)):
        h = open(p, encoding="utf-8").read()
        new = apply(h, p.endswith(".html"))
        if new != h:
            open(p, "w", encoding="utf-8").write(new); changed.append(p)
    print("files updated:", len(changed))
