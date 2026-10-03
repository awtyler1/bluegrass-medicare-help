#!/usr/bin/env python3
"""Validate one article before commit. Usage: python3 docs/validate-article.py <slug> [sibling-slug ...]
Checks: tag balance, inline SVG well-formedness, JSON-LD parse + FAQ schema equals visible FAQ,
KCHECK answer ranges, em dashes, British spellings, internal link existence, chrome + tracking IDs,
TPMO disclaimer, sibling similarity under 40 percent, Learning Center card counts, sitemap XML."""
import re, json, os, sys, difflib
from collections import Counter
from html.parser import HTMLParser
import xml.dom.minidom

slug = sys.argv[1]; sibs = sys.argv[2:]
V = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class B(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.st=[]; s.e=[]
    def handle_starttag(s,t,a):
        if t not in V: s.st.append(t)
    def handle_endtag(s,t):
        if t in V: return
        if s.st and s.st[-1]==t: s.st.pop()
        else: s.e.append((t,s.getpos()))
class T(HTMLParser):
    def __init__(s): super().__init__(convert_charrefs=True); s.o=[]; s.k=0
    def handle_starttag(s,t,a):
        if t in("script","style","svg","noscript","head"): s.k+=1
    def handle_endtag(s,t):
        if t in("script","style","svg","noscript","head") and s.k: s.k-=1
    def handle_data(s,d):
        if not s.k: s.o.append(d)
def words(f):
    t=T(); t.feed(open(f,encoding="utf-8").read()); return re.sub(r'\s+',' '," ".join(t.o))

F=f"articles/{slug}/index.html"; h=open(F,encoding="utf-8").read(); ok=True
b=B(); b.feed(h); b.close(); print("tags:","balanced" if not b.e and not b.st else f"ERR {b.e[:3]} {b.st[:4]}"); ok&=not(b.e or b.st)
for m in re.finditer(r'<svg.*?</svg>',h,re.S): xml.dom.minidom.parseString(m.group(0))
print("inline SVGs well-formed:",len(re.findall(r'<svg',h)))
d=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',h,re.S).group(1))
faq=[n for n in d["@graph"] if n["@type"]=="FAQPage"][0]
clean=lambda s: re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',s)).strip()
pairs=[(clean(q),clean(a)) for q,a in re.findall(r'<h3>(.*?)</h3>\s*<p>(.*?)</p>',re.search(r'<div class="faq">(.*?)</div>',h,re.S).group(1),re.S)]
same=[(q["name"],q["acceptedAnswer"]["text"]) for q in faq["mainEntity"]]==pairs
print("FAQ schema:",len(faq["mainEntity"]),"matches page:",same); ok&=same
k=json.loads(re.search(r'window\.KCHECK\s*=\s*(\[.*?\]);',h,re.S).group(1)); assert all(0<=x["answer"]<len(x["options"]) for x in k); print("KCHECK:",len(k))
body=words(F); dashes=body.count("—")+h.count("&mdash;")+h.count("—"); print("words:",len(body.split()),"| em dashes:",dashes); ok&=dashes==0
brit=re.findall(r'\b(?:licence|enrolment|enrol|specialise\w*|organisation\w*|neighbour\w*|programme|counselling|labelled|analyse\w*|centre|recognises?)\b',h,re.I); print("British:",brit or "none"); ok&=not brit
miss=[x for x in set(re.findall(r'href="(/[^"#?]*)"',h)) if not any(os.path.exists(c) for c in [x.lstrip("/"),x.lstrip("/")+"index.html",x.lstrip("/").rstrip("/")+"/index.html"])]; print("broken links:",miss or "none"); ok&=not miss
chrome=all(x in h for x in ['class="ustrip"','class="fnav"','27176602235306137','G-NF57CZ802N','/assets/site.js','/assets/site.css']); print("chrome+tracking:",chrome,"| TPMO:",h.count("Currently we represent 6 organizations")); ok&=chrome and h.count("Currently we represent 6 organizations")>=1
me=body.split()
for o in sibs:
    r=difflib.SequenceMatcher(None,me,words(f"articles/{o}/index.html").split()).ratio()*100; print(f"  similarity {r:5.1f}%  {o}"); ok&=r<40
hi=open("articles/index.html",encoding="utf-8").read(); c=Counter()
for r in re.findall(r'<a class="lcrow" data-cat="([^"]+)"',hi):
    for cat in r.split(): c[cat]+=1
for m in re.finditer(r'data-filter="([a-z0-9]+)".*?<b>([^<]+)</b><span class="m2n">(\d+) guides?</span>',hi,re.S):
    if c[m.group(1)]!=int(m.group(3)): ok=False; print("CARD MISMATCH",m.group(2),m.group(3),c[m.group(1)])
print("in Learning Center:",f'/articles/{slug}/' in hi,"| in sitemap:",f'/articles/{slug}/' in open("sitemap.xml",encoding="utf-8").read()); xml.dom.minidom.parse("sitemap.xml")
print("ALL OK" if ok else "PROBLEMS"); sys.exit(0 if ok else 1)
