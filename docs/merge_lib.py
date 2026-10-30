"""Helpers for folding one page into another (October 2026 consolidation)."""
import json, re

def read(p): return open(p, encoding="utf-8").read()
def write(p, s): open(p, "w", encoding="utf-8").write(s)
def strip(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

STOPS = ['<h2', '<section class="recap"', '<div class="endcta"', '<section class="kcheck"', '<div class="sources"', '<p class="disclaim"']

def section(h, title_startswith):
    """Return the HTML of an <h2> section whose text starts with title_startswith, up to the next stop."""
    for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', h, re.S):
        if strip(m.group(1)).startswith(title_startswith):
            ends = [h.find(s, m.end()) for s in STOPS]
            end = min(e for e in ends if e != -1)
            return h[m.start():end].rstrip() + "\n"
    raise KeyError(title_startswith)

def faq_pairs(h):
    m = re.search(r'<div class="faq">(.*?)</div>', h, re.S)
    return re.findall(r'(<h3>(.*?)</h3>\s*<p>(.*?)</p>)', m.group(1), re.S) if m else []

def pick_faq(h, *starts):
    out = []
    for blk, q, a in faq_pairs(h):
        if any(strip(q).startswith(s) for s in starts): out.append(blk)
    assert len(out) == len(starts), (starts, [strip(q) for _, q, _ in faq_pairs(h)])
    return out

def add_faq(h, blocks):
    m = re.search(r'(<div class="faq">)(.*?)(</div>)', h, re.S)
    return h[:m.end(2)] + "".join("\n      " + b for b in blocks) + "\n    " + h[m.end(2):]

def sync_faq_schema(h):
    m = re.search(r'<div class="faq">(.*?)</div>', h, re.S)
    pairs = [(strip(q), strip(a)) for q, a in re.findall(r'<h3>(.*?)</h3>\s*<p>(.*?)</p>', m.group(1), re.S)]
    def fix(js):
        d = json.loads(js.group(1))
        nodes = d["@graph"] if "@graph" in d else [d]
        for n in nodes:
            if n.get("@type") == "FAQPage":
                n["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]
            if n.get("@type") in ("BlogPosting", "Article", "WebPage") and "dateModified" in n:
                n["dateModified"] = "2026-10-30"
        return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "</script>"
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, h, flags=re.S), len(pairs)

def carry_css(src, dst, snippet):
    """Copy top-level CSS rules for classes used in snippet that dst does not define."""
    classes = set(c for cl in re.findall(r'class="([^"]+)"', snippet) for c in cl.split())
    sst = "".join(re.findall(r'<style>(.*?)</style>', src, re.S))
    dst_st = "".join(re.findall(r'<style>(.*?)</style>', dst, re.S))
    add = []
    flat = re.sub(r'@media[^{]*\{(?:[^{}]*\{[^}]*\})*[^}]*\}', '', sst)
    for c in sorted(classes):
        if re.search(rf'\.{re.escape(c)}\b', dst_st): continue
        add += [r for r in re.findall(r'[^{}]+\{[^}]*\}', flat) if re.search(rf'\.{re.escape(c)}\b', r.split("{")[0])]
    if add:
        dst = dst.replace("</style>", "\n/* carried over in the October 2026 merge */\n" + "\n".join(a.strip() for a in add) + "\n</style>", 1)
    return dst, len(add)

def insert_before(h, anchor, html):
    i = h.find(anchor); assert i != -1, anchor
    return h[:i] + html + h[i:]

def unlink_self(h, url):
    return re.sub(rf'<a href="{re.escape(url)}">(.*?)</a>', r'\1', h)
