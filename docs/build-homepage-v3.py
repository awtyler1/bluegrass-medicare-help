#!/usr/bin/env python3
"""Build the homepage (bright coral + rounded sans; advisor-first since November 2026) into index.html.

Idempotent: keeps the tracking snippet (everything before <title>) and the SEO tail
(<link rel="canonical"> through </head>) from the existing index.html, and regenerates the rest.
Topic counts and the search index are read from /articles/index.html so they never drift."""
import json, os, re, html as H

SRC = "index.html"
cur = open(SRC, encoding="utf-8").read()
head_top = cur[:cur.index("<title>")]
tail = cur[cur.index('<link rel="canonical"'):cur.index("</head>")]

TITLE = "Free Medicare Help from Licensed Kentucky Advisors | Bluegrass Medicare Help"
DESC = ("Talk to a licensed Medicare advisor from our Lexington office, free. We compare plans for your doctors and "
        "prescriptions. Plus plain-English Medicare guides for every Kentucky county.")
def _team(m):
    """Firm schema: both partners on the business node, Andrew as his own Person."""
    d = json.loads(m.group(1)); g = d.get("@graph", [])
    if not any(n.get("@id", "").endswith("#andrew-horn") for n in g):
        g.append({"@type": "Person", "@id": "https://www.bluegrassmedicarehelp.com/#andrew-horn", "name": "Andrew Horn",
                  "jobTitle": "Licensed Medicare Advisor", "image": "https://www.bluegrassmedicarehelp.com/assets/andrew-horn.jpg",
                  "url": "https://www.bluegrassmedicarehelp.com/about/", "worksFor": {"@id": "https://www.bluegrassmedicarehelp.com/#business"}})
    for n in g:
        if n.get("@id", "").endswith("#business"):
            n["employee"] = [{"@id": "https://www.bluegrassmedicarehelp.com/#austin-tyler"}, {"@id": "https://www.bluegrassmedicarehelp.com/#andrew-horn"}]
            n["description"] = ("Independent Medicare advisory firm in Lexington, Kentucky. Free help for Kentuckians "
                                "turning 65 or already on Medicare. No call center, no pressure.")
        if n.get("@id", "").endswith(("#austin-tyler", "#andrew-horn")):
            n["jobTitle"] = "Licensed Medicare Advisor"
            n["honorificSuffix"] = "MBA" if n["@id"].endswith("#austin-tyler") else "MHA"
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "</script>"
tail = re.sub(r'<script type="application/ld\+json">(.*?)</script>', _team, tail, flags=re.S)
tail = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + TITLE, tail)
tail = re.sub(r'(<meta name="twitter:title" content=")[^"]*', r'\g<1>' + TITLE, tail)
tail = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>' + DESC, tail)
tail = re.sub(r'(<meta name="twitter:description" content=")[^"]*', r'\g<1>' + DESC, tail)

# ---- data from the Learning Center
lc = open("articles/index.html", encoding="utf-8").read()
count = {m.group(1): int(m.group(2)) for m in re.finditer(r'data-filter="([a-z0-9]+)".*?<span class="m2n">(\d+) guides?</span>', lc, re.S)}
rows = re.findall(r'<a class="lcrow" data-cat="[^"]+" data-date="([^"]+)" href="([^"]+)">.*?<h2 class="lcrow-title">(.*?)</h2>\s*<p class="lcrow-dek">(.*?)</p>', lc, re.S)
strip = lambda s: re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", s))).strip()
INDEX = [{"t": strip(t), "d": strip(d), "u": u} for _, u, t, d in rows]
INDEX += [
  {"t": "Medicare enrollment date calculator", "d": "Enter your birthday to see your 7-month Initial Enrollment Period and when coverage starts.", "u": "/medicare-enrollment-calculator/"},
  {"t": "Medicare glossary", "d": "Deductible, coinsurance, formulary, prior authorization and more, in plain English.", "u": "/glossary/"},
  {"t": "Medicare quizzes", "d": "Are you ready for 65? Does Advantage or a Supplement fit you better?", "u": "/quizzes/"},
  {"t": "Kentucky Medicare county by county", "d": "Plan counts, hospitals and $0-premium options in your county.", "u": "/kentucky/"},
  {"t": "Medicare in Lexington and Fayette County", "d": "Plans, hospitals and local help in Lexington.", "u": "/medicare-lexington-ky/"},
  {"t": "Medicare in Richmond and Madison County", "d": "Plans, hospitals and local help in Richmond.", "u": "/medicare-richmond-ky/"},
  {"t": "Medicare in Nicholasville and Jessamine County", "d": "Plans, hospitals and local help in Nicholasville.", "u": "/medicare-nicholasville-ky/"},
  {"t": "Medicare in Georgetown and Scott County", "d": "Plans, hospitals and local help in Georgetown.", "u": "/medicare-georgetown-ky/"},
  {"t": "Medicare in Winchester and Clark County", "d": "Plans, hospitals and local help in Winchester.", "u": "/medicare-winchester-ky/"},
  {"t": "Book a free review", "d": "Pick a time to talk with a licensed advisor, or have us call you. Free, no pressure.", "u": "/schedule/"},
  {"t": "Turning 65 in Kentucky", "d": "Your enrollment window, your first decisions and the guides to read, in order.", "u": "/turning-65/"},
]
NGUIDES = len(rows)

PH = '<svg class="cta-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
SW = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
G = {
 "book": f'<svg {SW}><path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4zM20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/></svg>',
 "cake": f'<svg {SW}><path d="M4 21h16M5 21v-7a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v7M8 12V9M12 12V9M16 12V9M8 6v1M12 5v2M16 6v1"/><path d="M5 17c1.5 1 3 1 4.5 0s3-1 4.5 0 3 1 4.5 0"/></svg>',
 "fork": f'<svg {SW}><path d="M12 22V12M12 12L6 6M12 12l6-6M4 6h4V2M20 6h-4V2"/></svg>',
 "dollar": f'<svg {SW}><path d="M12 2v20M16.5 6.5A3.5 3.5 0 0 0 13 4h-2a3.5 3.5 0 0 0 0 7h2a3.5 3.5 0 0 1 0 7h-2a3.5 3.5 0 0 1-3.5-3.5"/></svg>',
 "card": f'<svg {SW}><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M7 15h4"/></svg>',
 "map": f'<svg {SW}><path d="M12 21s-7-5.2-7-11a7 7 0 0 1 14 0c0 5.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 "calendar": f'<svg {SW}><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4M8 14h3v3H8z"/></svg>',
 "abc": f'<svg {SW}><path d="M4 19l4-12 4 12M5.5 15h5M15 7h3a2.5 2.5 0 0 1 0 5h-3zM15 12h3.5a3.5 3.5 0 0 1 0 7H15z"/></svg>',
 "check": f'<svg {SW}><circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/></svg>',
 "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
}
def gl(k): return f'<span class="glyph">{G[k]}</span>'
def tcard(g, h, small, p, href):
    return f'<a class="card" href="{href}">{gl(g)}<span class="cb"><span class="ch">{h}</span><span class="cs">{small}</span><span class="cp">{p}</span></span></a>'
def n(k, word="guides"): return f'{count.get(k, 0)} {word}'

REVIEWS = [
 ("Austin was extremely knowledgeable and explained everything in great detail so I could easily understand. I know that my insurance needs are in good hands!", "Doug S."),
 ("Austin is very professional and knowledgeable about what is available to us and the best way to go about it. He responds promptly and keeps us updated as to the status of our insurance. Thank you Austin!", "Denise L."),
 ("Tyler is great to work with. He’s organized and customer service oriented. He follows up in a timely manner. Best agent I have ever worked with.", "Stephen C."),
]
COUNTIES = [("Fayette County (Lexington)", "/medicare-lexington-ky/"), ("Madison County (Richmond)", "/medicare-richmond-ky/"),
            ("Jessamine County (Nicholasville)", "/medicare-nicholasville-ky/"), ("Scott County (Georgetown)", "/medicare-georgetown-ky/"),
            ("Clark County (Winchester)", "/medicare-winchester-ky/")]

CSS = """
/* Layout: full-width colour bands (no rules between sections); white cards float on soft tints; one coral action colour; pill buttons. */
:root{
  --bg:#ffffff;--surf:#ffffff;--tint1:#fff0e8;--tint2:#e9f3fb;--tint3:#fff7df;
  --ink:#1b2836;--mute:#4a5563;--line:#eadfd6;--cta:#cf461e;--cta-d:#b23c17;--link:#b23c17;--accent:#1b6f8f;
  --glyph:#cf461e;--glyphbg:#fff0e8;--foot:#1b2836;--star:#e09a1a;
  --head:'Figtree','Source Sans 3',-apple-system,'Segoe UI',sans-serif;--sans:'Source Sans 3',-apple-system,'Segoe UI',sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0;}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;}
body{font-family:var(--sans);font-size:19px;line-height:1.55;color:var(--ink);background:var(--bg);-webkit-font-smoothing:antialiased;}
img{max-width:100%;display:block;}
a{color:var(--link);text-decoration:none;}
.wrap{max-width:1100px;margin:0 auto;padding-left:max(20px,env(safe-area-inset-left,0px));padding-right:max(20px,env(safe-area-inset-right,0px));}
h1,h2,.ch{font-family:var(--head);font-weight:700;line-height:1.12;letter-spacing:-.4px;text-wrap:balance;color:var(--ink);}
h2{font-size:31px;margin-bottom:8px;}
@media(min-width:900px){h2{font-size:36px;}}
.lead{color:var(--mute);font-size:19px;max-width:640px;margin-bottom:28px;}
.lead a{font-weight:700;}
.band{padding-block:60px;} .t1{background:var(--tint1);} .t2{background:var(--tint2);} .t3{background:var(--tint3);}
.pill{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:56px;padding:0 28px;border-radius:999px;background:var(--cta);color:#fff;font-weight:700;font-size:19px;border:0;cursor:pointer;white-space:nowrap;font-family:var(--sans);transition:background .15s;}
.pill:hover{background:var(--cta-d);}
.pill .cta-ico,.pill svg{width:21px;height:21px;}
.eyebrow{display:inline-block;color:var(--accent);font-weight:700;font-size:15px;letter-spacing:1.6px;text-transform:uppercase;margin-bottom:14px;}
/* hero */
.hero{padding-block:52px 56px;text-align:center;}
@media(min-width:900px){.hero{padding-block:76px 72px;}}
.hero h1{font-size:42px;font-weight:800;max-width:800px;margin:0 auto;}
@media(min-width:900px){.hero h1{font-size:60px;}}
.hero .sub{font-size:20.5px;color:var(--mute);margin:16px auto 30px;max-width:620px;}
.find{position:relative;max-width:680px;margin:0 auto;text-align:left;}
.ask{display:flex;align-items:center;background:var(--surf);border:2px solid var(--line);border-radius:999px;padding:6px;box-shadow:0 10px 30px rgba(27,40,54,.08);}
.ask:focus-within{border-color:var(--cta);}
.ask label{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);}
.ask input{flex:1;min-width:0;border:0;background:transparent;font:inherit;font-size:19px;padding:0 18px;min-height:52px;color:var(--ink);}
.ask input:focus{outline:none;}
.ask input::-webkit-search-cancel-button{display:none;}
@media(max-width:480px){.ask .lbl{display:none;} .ask .pill{padding:0 18px;}}
.results{margin-top:12px;background:var(--surf);border:1px solid var(--line);border-radius:22px;overflow:hidden;box-shadow:0 14px 34px rgba(27,40,54,.10);}
.results a{display:block;padding:14px 22px;border-top:1px solid var(--line);color:var(--ink);}
.results a:first-child{border-top:0;}
.results a:hover,.results a:focus-visible{background:var(--tint1);}
.results b{display:block;font-size:18px;line-height:1.3;}
.results span{display:block;color:var(--mute);font-size:15.5px;line-height:1.4;margin-top:2px;}
.results .none{padding:18px 22px;color:var(--mute);font-size:17px;}
.results .all{font-weight:700;color:var(--link);}
.human{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:10px 14px;margin-top:24px;color:var(--mute);font-size:18px;}
.human .duo{display:inline-flex;}
.human .duo img,.askband .duo img{border-radius:50%;object-fit:cover;object-position:center 20%;border:3px solid var(--surf);}
.human .duo img{width:48px;height:48px;}
.human .duo img+img,.askband .duo img+img{margin-left:-14px;}
.human a{font-weight:700;white-space:nowrap;}
.trust{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 26px;margin-top:20px;color:var(--mute);font-size:16px;font-weight:600;}
.trust .star{color:var(--star);letter-spacing:1px;margin-right:6px;}
/* advisor-first hero (mockup A) */
.hva{display:grid;gap:30px;align-items:center;padding-block:44px 52px;}
@media(min-width:900px){.hva{grid-template-columns:1.1fr .9fr;gap:48px;padding-block:64px 70px;}}
.hva h1{font-size:40px;font-weight:800;} @media(min-width:900px){.hva h1{font-size:54px;}}
.hva .sub{font-size:20.5px;color:var(--mute);margin:16px 0 26px;max-width:560px;}
.hva .row{display:flex;flex-wrap:wrap;align-items:center;gap:6px 20px;}
.hva .trust{justify-content:flex-start;}
.callline{display:inline-flex;align-items:center;min-height:56px;font-weight:700;font-size:19px;color:var(--link);}
.ticks{list-style:none;display:flex;flex-wrap:wrap;gap:8px 20px;margin:20px 0 0;color:var(--ink);font-weight:600;font-size:17px;}
.ticks li::before{content:"";display:inline-block;width:9px;height:15px;border:solid #2f6844;border-width:0 3px 3px 0;transform:rotate(45deg);margin:0 10px 0 4px;position:relative;top:-2px;}
.duocard{background:var(--tint1);border-radius:26px;padding:22px;}
.duocard .ph{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.duocard figure{margin:0;} .duocard img{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;object-position:center 20%;border-radius:18px;}
.duocard figcaption{margin-top:10px;font-size:15.5px;color:var(--mute);line-height:1.35;} .duocard figcaption b{display:block;font-family:var(--head);font-size:19px;color:var(--ink);}
.duocard .office{margin-top:16px;padding-top:14px;border-top:1px solid var(--line);font-size:16px;color:var(--ink);}
/* situations (mockup C) */
.sits{display:grid;gap:14px;grid-template-columns:1fr;} @media(min-width:700px){.sits{grid-template-columns:1fr 1fr;}} @media(min-width:1000px){.sits{grid-template-columns:repeat(3,1fr);}}
.sit{position:relative;display:block;background:var(--surf);border-radius:18px;padding:20px 52px 20px 22px;color:var(--ink);box-shadow:0 1px 2px rgba(27,40,54,.06),0 8px 24px rgba(27,40,54,.06);transition:box-shadow .15s;}
.sit b{display:block;font-family:var(--head);font-size:21px;line-height:1.2;} .sit span{display:block;color:var(--mute);font-size:16.5px;margin-top:4px;}
.sit i{position:absolute;right:20px;top:50%;transform:translateY(-50%);font-style:normal;font-weight:700;font-size:22px;color:var(--link);}
.sit:hover{box-shadow:0 2px 4px rgba(27,40,54,.08),0 14px 32px rgba(27,40,54,.10);}
/* how a review works */
.steps{list-style:none;counter-reset:s;display:grid;gap:16px;grid-template-columns:1fr;margin:6px 0 0;}
@media(min-width:800px){.steps{grid-template-columns:repeat(3,1fr);}}
.steps li{counter-increment:s;background:var(--surf);border-radius:20px;padding:24px 24px 22px;box-shadow:0 1px 2px rgba(27,40,54,.06),0 8px 24px rgba(27,40,54,.06);}
.steps li::before{content:counter(s);display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:var(--cta);color:#fff;font-family:var(--head);font-weight:800;font-size:19px;margin-bottom:12px;}
.steps b{display:block;font-family:var(--head);font-size:22px;margin-bottom:4px;} .steps span{color:var(--mute);font-size:17px;}
.stepcta{margin-top:26px;}
.topicsearch{max-width:680px;margin:0 0 28px;}
/* cards */
.grid{display:grid;gap:18px;grid-template-columns:1fr;}
@media(min-width:640px){.grid.c2,.grid.c3{grid-template-columns:1fr 1fr;}}
@media(min-width:960px){.grid.c3{grid-template-columns:repeat(3,1fr);}}
.card{display:flex;gap:16px;align-items:flex-start;background:var(--surf);border-radius:20px;padding:24px;color:var(--ink);box-shadow:0 1px 2px rgba(27,40,54,.06),0 8px 24px rgba(27,40,54,.06);transition:transform .15s,box-shadow .15s;min-width:0;}
.card:hover{transform:translateY(-2px);box-shadow:0 2px 4px rgba(27,40,54,.08),0 14px 32px rgba(27,40,54,.10);}
.cb{display:block;min-width:0;}
.ch{display:block;font-size:23px;margin-bottom:4px;}
.cs{display:block;color:var(--mute);font-size:15px;font-weight:600;margin-bottom:4px;}
.cp{display:block;color:var(--mute);font-size:17px;line-height:1.5;}
.go{display:inline-block;margin-top:12px;font-weight:700;color:var(--link);font-size:17px;}
.glyph{flex-shrink:0;width:54px;height:54px;border-radius:50%;background:var(--glyphbg);display:flex;align-items:center;justify-content:center;color:var(--glyph);}
.glyph svg{width:27px;height:27px;}
.stack{flex-direction:column;gap:6px;}
.chipdate{display:inline-block;background:var(--tint2);color:var(--ink);font-size:14px;font-weight:700;border-radius:999px;padding:4px 12px;margin-bottom:10px;}
/* ask austin */
.askband{display:flex;flex-wrap:wrap;align-items:center;gap:20px 26px;}
.askband .duo{display:inline-flex;flex-shrink:0;}
.askband .duo img{width:92px;height:92px;border-width:4px;}
.askband .t{flex:1;min-width:240px;}
.askband h2{font-size:28px;margin-bottom:4px;}
.askband p{color:var(--mute);font-size:17.5px;}
/* counties */
.chips{display:flex;flex-wrap:wrap;gap:10px;}
.chip{display:inline-flex;align-items:center;min-height:52px;padding:0 22px;border-radius:999px;background:var(--surf);color:var(--ink);font-weight:600;font-size:17px;box-shadow:0 1px 2px rgba(27,40,54,.08),0 4px 12px rgba(27,40,54,.05);}
.chip:hover{color:var(--link);}
.chip.more{background:var(--cta);color:#fff;}
/* reviews */
.rev{background:var(--surf);border-radius:20px;padding:24px;box-shadow:0 1px 2px rgba(27,40,54,.06),0 8px 24px rgba(27,40,54,.06);}
.rev .star{color:var(--star);font-size:18px;letter-spacing:2px;}
.rev p{font-size:18px;margin:10px 0 14px;line-height:1.5;}
.rev b{font-size:16px;color:var(--mute);font-weight:600;}
/* advisors */
.team{display:grid;gap:18px;grid-template-columns:1fr;margin-top:6px;}
@media(min-width:760px){.team{grid-template-columns:1fr 1fr;}}
.adv{display:flex;gap:18px;align-items:center;background:var(--surf);border-radius:20px;padding:20px;color:var(--ink);box-shadow:0 1px 2px rgba(27,40,54,.06),0 8px 24px rgba(27,40,54,.06);}
.adv img{width:104px;height:104px;border-radius:50%;object-fit:cover;object-position:center 20%;flex-shrink:0;}
.adv b{display:block;font-family:var(--head);font-size:22px;}
.adv span{display:block;color:var(--cta-d);font-weight:700;font-size:15px;margin:2px 0 6px;}
.adv small{display:block;color:var(--mute);font-size:15px;line-height:1.45;}
.firmnote{margin-top:22px;font-size:18px;color:var(--ink);max-width:760px;}
.firmnote a{font-weight:700;}
/* final */
.final{background:var(--cta);color:#fff;padding-block:60px;text-align:center;}
.final h2{color:#fff;}
.final p{color:#fff;font-size:19.5px;margin:10px auto 26px;max-width:560px;}
.final .pill{background:#fff;color:var(--cta-d);}
.final .pill:hover{background:#fff4ee;}
.final .num{display:block;margin-top:16px;font-size:30px;font-weight:700;letter-spacing:.3px;}
.final a.u{color:#fff;text-decoration:underline;font-weight:700;}
/* legal footer */
.foot{background:var(--foot);color:rgba(255,255,255,.78);font-size:15px;line-height:1.6;padding-block:30px 110px;}
.foot .fnm{color:#fff;font-weight:700;font-size:16px;margin-bottom:4px;}
.foot a{color:#fff;}
.foot .disc{margin-top:16px;max-width:920px;}
@media(min-width:900px){.foot{padding-bottom:36px;}}
/* sticky call bar (phones) */
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:50;padding:10px max(14px,env(safe-area-inset-left,0px)) calc(10px + env(safe-area-inset-bottom,0px)) max(14px,env(safe-area-inset-right,0px));background:var(--surf);box-shadow:0 -6px 20px rgba(27,40,54,.10);}
.sticky a{display:flex;align-items:center;justify-content:center;gap:10px;min-height:56px;border-radius:999px;background:var(--cta);color:#fff;font-weight:700;font-size:19.5px;}
.sticky .cta-ico{width:20px;height:20px;}
@media(min-width:900px){.sticky{display:none;}}
"""

TEL = "tel:18597858289"; PN = "(859) 785-8289"
def ustrip():
    return ('<div class="ustrip">\n  <div class="wrap">\n    <span><strong>Free Medicare help for all of Kentucky</strong> &nbsp;&middot;&nbsp; Office in Lexington</span>\n'
            '    <span class="rate"><span class="stars">★★★★★</span> 5.0 on Google</span>\n  </div>\n</div>')
NAV = ('<nav class="nav">\n  <div class="wrap">\n'
 '    <a class="brand" href="/" aria-label="Bluegrass Medicare Help home">\n'
 '      <img class="brand-logo" src="/assets/logo.png" alt="Bluegrass Medicare Help" width="169" height="46"\n'
 '           onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'flex\';">\n'
 '      <span class="brand-fallback"><span class="mark">B</span><span class="wm">Bluegrass<small>Medicare Help</small></span></span>\n'
 '    </a>\n'
 '    <div class="navlinks" id="navlinks">\n      <a href="/turning-65/">Turning 65</a>\n      <a href="/articles/">Learning Center</a>\n      <a href="/kentucky/">Your County</a>\n      <a href="/about/">About</a>\n    </div>\n'
 '    <a class="navbook" href="/schedule/"><svg class="cta-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg><span class="nb-full">Schedule</span><span class="nb-short">Book</span></a>\n'
 f'    <a class="navcta" href="{TEL}">{PH}Call<span class="nc-num">&nbsp;{PN}</span></a>\n'
 '    <button class="navtog" id="navtog" aria-label="Open menu" aria-expanded="false" aria-controls="navlinks">\n'
 '      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>\n'
 '    </button>\n  </div>\n</nav>')

t65 = "/turning-65/"
CAL = '<svg class="cta-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
SITUATIONS = [("I'm turning 65", "Your sign-up window and first choices", "/turning-65/"),
              ("I'm reviewing my plan for next year", "What to check before December 7", "/articles/medicare-annual-enrollment-period/"),
              ("My plan is ending", "What a non-renewal letter means and your options", "/articles/medicare-advantage-plan-ending-kentucky/"),
              ("I'm still working at 65", "When you can wait on Part B, and when you can't", "/articles/working-past-65-medicare/"),
              ("Advantage or a Supplement?", "The real differences, side by side", "/articles/medicare-advantage-vs-medigap/"),
              ("I need help paying", "Programs that lower premiums and drug costs", "/articles/help-paying-for-medicare/")]
SIT_GRID = "".join(f'<a class="sit" href="{u}"><b>{t}</b><span>{d}</span><i aria-hidden="true">&rarr;</i></a>' for t, d, u in SITUATIONS)
BODY = f"""<a class="skip-link" href="#main">Skip to content</a>
{ustrip()}

{NAV}

<main id="main">
<header class="hero-a"><div class="wrap hva">
  <div>
    <span class="eyebrow">Free Medicare help for all of Kentucky</span>
    <h1>Talk to a local Medicare advisor before you choose.</h1>
    <p class="sub">A free review with a licensed advisor from our Lexington office. We check your doctors and prescriptions against the plans in your county and explain your options in plain English.</p>
    <div class="row"><a class="pill" href="/schedule/">{CAL}Book a free review</a><a class="callline" href="{TEL}">or call {PN}</a></div>
    <ul class="ticks"><li>Always free</li><li>Phone, video or in person</li><li>No pressure to switch</li></ul>
    <div class="trust"><span><span class="star">★★★★★</span>5.0 on Google</span><span>Over 1,000 Kentuckians helped</span><span>Independent Lexington firm</span></div>
  </div>
  <div class="duocard">
    <div class="ph">
      <figure><img src="/assets/austin-tyler.jpg" alt="Austin Tyler" width="600" height="750"><figcaption><b>Austin Tyler, MBA</b>Licensed Medicare Advisor</figcaption></figure>
      <figure><img src="/assets/andrew-horn.jpg" alt="Andrew Horn" width="768" height="960"><figcaption><b>Andrew Horn, MHA</b>Licensed Medicare Advisor</figcaption></figure>
    </div>
    <p class="office">Your call is answered by one of us, not a call center. Office: 1029 Monarch Street, Lexington.</p>
  </div>
</div></header>

<section class="band t1" aria-labelledby="sit-h"><div class="wrap">
  <h2 id="sit-h">What brings you here?</h2><p class="lead">Pick the one that fits. Each guide is short, and you can talk to us at any point.</p>
  <div class="sits">{SIT_GRID}</div>
</div></section>

<section class="band t2" aria-labelledby="how-h"><div class="wrap">
  <h2 id="how-h">How a free review works</h2><p class="lead">About 30 minutes, by phone, video or at our Lexington office. You never pay us; the insurance companies pay licensed agents, and we work with several of them rather than one.</p>
  <ol class="steps">
    <li><b>Pick a time</b><span>Book online in a minute, or call and we will set it up with you.</span></li>
    <li><b>We do the comparing</b><span>We check your doctors, hospital and exact prescriptions against the plans in your county.</span></li>
    <li><b>You decide</b><span>We explain the options in plain English. No pressure to switch, and we will say so if your current plan is the right one.</span></li>
  </ol>
  <p class="stepcta"><a class="pill" href="/schedule/">{CAL}Book a free review</a></p>
</div></section>

<section class="band t1" aria-labelledby="rev-h"><div class="wrap">
  <h2 id="rev-h">What Kentuckians say</h2><p class="lead">5.0 on Google. <a href="/reviews/">Read all reviews &rarr;</a></p>
  <div class="grid c3">{''.join(f'<div class="rev"><div class="star" aria-label="5 out of 5 stars">★★★★★</div><p>“{t}”</p><b>{w}, Google review</b></div>' for t, w in REVIEWS)}</div>
</div></section>

<section class="band" aria-labelledby="topics-h"><div class="wrap">
  <h2 id="topics-h">Prefer to read first?</h2><p class="lead">{NGUIDES} free plain-English guides, written by our advisors and checked against official sources. <a href="/articles/">See them all &rarr;</a></p>
  <div class="find topicsearch">
    <form class="ask" role="search" id="askform" action="/articles/">
      <label for="q">Search the Medicare guides</label>
      <input id="q" name="q" type="search" placeholder="Search the guides" autocomplete="off" aria-controls="results">
      <button class="pill" type="submit">{G['search']}<span class="lbl">Search</span></button>
    </form>
    <div class="results" id="results" role="region" aria-live="polite" aria-label="Matching guides" hidden></div>
  </div>
  <div class="grid c3">
    {tcard('book','Medicare basics',n('basics'),'Parts A, B, C and D, and the cost words every plan uses, explained once and clearly.','/articles/basics/')}
    {tcard('cake','Turning 65',n('turning65') + ' + a date calculator','Your enrollment window, your first decisions, and the penalties to avoid.',t65)}
    {tcard('fork','Choosing coverage',n('coverage'),'Advantage, Medigap, Part D, chronic-condition plans, and the dental fine print.','/articles/coverage/')}
    {tcard('dollar','Costs and savings',n('costs'),'Premiums, IRMAA, Extra Help, and what a $0 plan really costs.','/articles/costs/')}
    {tcard('card','Already on Medicare',n('onmedicare'),'Your Annual Notice of Change, switching plans, and this year’s changes.','/articles/on-medicare/')}
    {tcard('map','Your Kentucky county','County pages + ' + n('local','local guides'),'Plan counts, hospital networks and $0-premium options where you live.','/kentucky/')}
  </div>
</div></section>



<section class="band t2" aria-labelledby="month-h"><div class="wrap">
  <h2 id="month-h">This season in Medicare</h2><p class="lead">What changed, what is due, and what you can ignore.</p>
  <div class="grid c3">
    <a class="card stack" href="/articles/medicare-annual-enrollment-period/"><span class="chipdate" id="aepchip">Ends December 7</span><span class="ch">Annual Enrollment: October 15 to December 7</span><span class="cp">How to read your Annual Notice of Change and decide whether to keep your plan.</span><span class="go">Read &rarr;</span></a>
    <a class="card stack" href="/articles/90-dollar-medicare-payment-kentucky/"><span class="chipdate">Updated October 8</span><span class="ch">The $90 Medicare payment</span><span class="cp">Who got it, why Advantage members didn't, and the scam calls to expect.</span><span class="go">Read &rarr;</span></a>
    <a class="card stack" href="/articles/medicare-changes-2027-kentucky/"><span class="chipdate">Plan year 2027</span><span class="ch">What changes in Kentucky for 2027</span><span class="cp">Part B premium, the $700 drug deductible, the $2,400 cap, and plans leaving.</span><span class="go">Read &rarr;</span></a>
  </div>
</div></section>

<section class="band t3" aria-labelledby="tools-h"><div class="wrap">
  <h2 id="tools-h">Free tools</h2><p class="lead">Each takes about a minute.</p>
  <div class="grid c3">
    <a class="card" href="/medicare-enrollment-calculator/">{gl('calendar')}<span class="cb"><span class="ch">Enrollment date calculator</span><span class="cp">Type your birthday. See your 7-month window and the day coverage starts. Nothing you type is saved.</span><span class="go">Find my dates &rarr;</span></span></a>
    <a class="card" href="/quizzes/">{gl('check')}<span class="cb"><span class="ch">Medicare quizzes</span><span class="cp">Are you ready for 65? Does Advantage or a Supplement fit you better? A few questions each.</span><span class="go">Take a quiz &rarr;</span></span></a>
    <a class="card" href="/glossary/">{gl('abc')}<span class="cb"><span class="ch">Medicare glossary</span><span class="cp">Deductible, coinsurance, formulary, prior authorization: every word, in plain English.</span><span class="go">Look up a word &rarr;</span></span></a>
  </div>
</div></section>

<section class="band" aria-labelledby="county-h"><div class="wrap">
  <h2 id="county-h">Medicare help in your county</h2><p class="lead">Plan counts, hospital networks and $0-premium options change from county to county.</p>
  <div class="chips">{''.join(f'<a class="chip" href="{u}">{c}</a>' for c, u in COUNTIES)}<a class="chip more" href="/kentucky/">Find your county &rarr;</a></div>
</div></section>



<section class="final" aria-labelledby="final-h"><div class="wrap"><h2 id="final-h">Talk it through with a local advisor</h2><p>Free, licensed, and based in Lexington. Phone, video or in person, at a time that suits you.</p>
  <a class="pill" href="/schedule/">{CAL}Book a free review</a><span class="num">or call {PN}</span></div></section>
</main>

<div class="sticky"><a href="/schedule/">{CAL}Book a free review</a></div>
<nav class="fnav" aria-label="Footer">
  <div class="wrap">
    <a href="/" class="fnav-logo" aria-label="Bluegrass Medicare Help home"><img src="/assets/logo.png" alt="Bluegrass Medicare Help" width="806" height="220" onerror="this.closest('.fnav-logo').style.display='none'"></a>
    <div class="fnav-links"><a href="/">Home</a><a href="/turning-65/">Turning 65?</a><a href="/articles/">Learning Center</a><a href="/glossary/">Glossary</a><a href="/kentucky/">Your County</a><a href="/reviews/">Reviews</a><a href="/schedule/">Schedule</a><a href="/quizzes/">Quizzes</a><a href="/guide/">Free Guide</a><a href="/review/">Free Review</a><a href="/about/">About</a></div>
    <a class="fcall" href="{TEL}">{PH}Call {PN}</a>
  </div>
</nav>

<footer class="foot">
  <div class="wrap">
    <div class="fnm">Tyler Insurance Group</div>
    1029 Monarch Street, Suite 110, Lexington, KY 40513<br>
    <a href="{TEL}">{PN}</a> &middot; <a href="https://www.tylerinsurancegroup.com">tylerinsurancegroup.com</a>
    <div class="disc">
      We respect your privacy. This is a solicitation for insurance. Tyler Insurance Group is not connected with or endorsed by the United States government or the federal Medicare program. We do not offer every plan available in your area. Currently we represent 6 organizations which offer 158 products in your area. Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance Program (SHIP) to get information on all of your options.</div>
  </div>
</footer>

<script>
(function(){{
  var tog=document.getElementById('navtog'), links=document.getElementById('navlinks');
  if(tog&&links){{
    tog.addEventListener('click',function(){{ var open=links.classList.toggle('open'); tog.setAttribute('aria-expanded', open?'true':'false'); }});
    links.addEventListener('click',function(e){{ if(e.target.tagName==='A'){{ links.classList.remove('open'); tog.setAttribute('aria-expanded','false'); }} }});
  }}
  // days left in the Annual Enrollment Period (Oct 15 to Dec 7)
  var chip=document.getElementById('aepchip');
  if(chip){{
    var now=new Date(), y=now.getFullYear(), start=new Date(y,9,15), end=new Date(y,11,7,23,59);
    var day=86400000;
    if(now>=start && now<=end){{ var d=Math.ceil((end-now)/day); chip.textContent = d<=1 ? 'Ends today' : d+' days left'; }}
    else if(now<start){{ chip.textContent='Opens October 15'; }}
    else {{ chip.textContent='Next window: October 15'; }}
  }}
  // guide search
  var IDX={json.dumps(INDEX, ensure_ascii=False)};
  var STOP={{'a':1,'an':1,'the':1,'and':1,'or':1,'of':1,'to':1,'in':1,'on':1,'for':1,'is':1,'it':1,'my':1,'i':1,'do':1,'does':1,'what':1,'how':1,'can':1,'if':1,'when':1,'me':1,'with':1,'are':1,'be':1,'about':1,'medicare':1}};
  var q=document.getElementById('q'), out=document.getElementById('results'), form=document.getElementById('askform');
  function esc(s){{ return s.replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}}); }}
  function search(text){{
    var terms=text.toLowerCase().replace(/[^a-z0-9$ ]/g,' ').split(/\\s+/).filter(function(t){{return t && !STOP[t];}});
    if(!terms.length) return [];
    return IDX.map(function(it){{
      var t=it.t.toLowerCase(), d=it.d.toLowerCase(), s=0;
      terms.forEach(function(w){{ var stem=w.length>4?w.slice(0,w.length-1):w; if(t.indexOf(stem)>-1) s+=3; else if(d.indexOf(stem)>-1) s+=1; }});
      return {{it:it,s:s}};
    }}).filter(function(r){{return r.s>0;}}).sort(function(a,b){{return b.s-a.s;}}).slice(0,6).map(function(r){{return r.it;}});
  }}
  function render(){{
    var text=q.value.trim();
    if(text.length<2){{ out.hidden=true; out.innerHTML=''; return; }}
    var hits=search(text);
    if(!hits.length){{
      out.innerHTML='<div class="none">No guide matches that yet. <a href="{TEL}" class="all">Call us at {PN}</a> or <a href="/articles/" class="all">browse every guide</a>.</div>';
    }} else {{
      out.innerHTML=hits.map(function(h){{return '<a href="'+h.u+'"><b>'+esc(h.t)+'</b><span>'+esc(h.d)+'</span></a>';}}).join('')+'<a href="/articles/" class="all">Browse all guides &rarr;</a>';
    }}
    out.hidden=false;
  }}
  if(q&&out&&form){{
    var timer; q.addEventListener('input',function(){{ clearTimeout(timer); timer=setTimeout(render,120); }});
    form.addEventListener('submit',function(e){{ e.preventDefault(); render(); var first=out.querySelector('a'); if(first && search(q.value.trim()).length) first.focus(); }});
  }}
}})();
</script>
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@600;700;800&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">')
page = (head_top + f"<title>{TITLE}</title>\n<meta name=\"description\" content=\"{DESC}\">\n{FONTS}\n"
        '<link rel="stylesheet" href="/assets/site.css">\n<style>' + CSS + "</style>\n" + tail + "</head>\n<body>\n" + BODY + "</body>\n</html>\n")
page = page.replace('<meta name="theme-color" content="#1f1d1a">', '<meta name="theme-color" content="#cf461e">')
import sys as _s; _s.path.insert(0, "docs")
from chrome_v4 import apply as _chrome
page = _chrome(page)
open(SRC, "w", encoding="utf-8").write(page)
print("wrote index.html", len(page), "bytes;", NGUIDES, "guides;", len(INDEX), "search entries; counts", count)
