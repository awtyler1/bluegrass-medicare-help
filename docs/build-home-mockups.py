#!/usr/bin/env python3
"""Build three homepage mockups. Emits a repo copy (full document, root-relative assets, noindex)
to mockups/home-v3/<key>/index.html and an artifact copy (no skeleton, relative assets) to the
scratchpad. Usage: build-home-mockups.py <artifact_out_dir>"""
import os, sys

ART = sys.argv[1] if len(sys.argv) > 1 else "/tmp/home-mockups"
os.makedirs(ART, exist_ok=True)
PHONE_TXT = "(859) 785-8289"; TEL = "tel:18597858289"

BASE_CSS = """
:root{--cream:#f4efe7;--cream2:#faf6ef;--warm:#efe6d6;--ink:#2a2620;--dark:#1f1d1a;--coral:#d05528;--coral-d:#b3431d;--mute:#5f594f;--faint:#938c80;--line:#e2d9c8;--green:#3a7d52;--green-d:#2f6844;--white:#fff;--serif:'Fraunces',Georgia,serif;--sans:'Source Sans 3',-apple-system,'Segoe UI',sans-serif;}
*{box-sizing:border-box;margin:0;padding:0;}
html{-webkit-text-size-adjust:100%;color-scheme:light;}
body{font-family:var(--sans);font-size:19px;line-height:1.55;color:var(--ink);background:var(--cream);-webkit-font-smoothing:antialiased;}
img{max-width:100%;display:block;}
a{color:var(--coral-d);text-decoration:none;}
a:focus-visible,button:focus-visible{outline:3px solid var(--green);outline-offset:3px;}
.wrap{max-width:1100px;margin:0 auto;padding-left:max(18px,env(safe-area-inset-left,0px));padding-right:max(18px,env(safe-area-inset-right,0px));}
h1,h2,h3{font-family:var(--serif);font-weight:500;line-height:1.12;letter-spacing:-.3px;text-wrap:balance;}
h2{font-size:32px;margin-bottom:8px;}
.lead{color:var(--mute);font-size:19px;max-width:620px;margin-bottom:26px;}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:58px;padding:0 30px;border-radius:14px;background:var(--coral);color:#fff;font-weight:700;font-size:20px;border:0;cursor:pointer;-webkit-tap-highlight-color:transparent;}
.btn:hover{background:var(--coral-d);}
.btn.ghost{background:transparent;color:var(--ink);border:2px solid var(--ink);}
.btn.ghost:hover{background:var(--warm);}
.btn svg{width:22px;height:22px;flex-shrink:0;}
.sec{padding-block:56px;}
.sec.alt{background:var(--cream2);border-top:1px solid var(--line);border-bottom:1px solid var(--line);}
/* nav */
.nav{background:var(--white);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20;}
.nav .wrap{display:flex;align-items:center;gap:18px;min-height:72px;}
.brand{display:flex;align-items:center;gap:10px;color:var(--ink);font-family:var(--serif);font-size:21px;}
.brand img{height:44px;width:auto;}
.navlinks{display:none;gap:26px;margin-left:auto;font-weight:600;font-size:17px;}
.navlinks a{color:var(--ink);padding:10px 2px;}
.navlinks a:hover{color:var(--coral-d);}
.navcall{margin-left:auto;display:inline-flex;align-items:center;gap:8px;min-height:48px;padding:0 18px;border-radius:12px;background:var(--green);color:#fff;font-weight:700;font-size:17px;white-space:nowrap;}
.navcall svg{width:18px;height:18px;}
.navtog{width:48px;height:48px;border:1px solid var(--line);border-radius:12px;background:var(--white);display:inline-flex;align-items:center;justify-content:center;color:var(--ink);}
@media(min-width:900px){.navlinks{display:flex;} .navcall{margin-left:0;} .navtog{display:none;} .navcall .full{display:inline;}}
.navcall .full{display:none;}
/* trust row */
.trust{display:flex;flex-wrap:wrap;gap:10px 26px;color:var(--mute);font-size:16.5px;font-weight:600;}
.trust span{display:inline-flex;align-items:center;gap:8px;}
.trust .star{color:#e8a13a;letter-spacing:1px;}
/* cards */
.grid{display:grid;gap:18px;grid-template-columns:1fr;}
@media(min-width:640px){.grid.c2{grid-template-columns:1fr 1fr;} .grid.c3{grid-template-columns:repeat(3,1fr);} .grid.c4{grid-template-columns:1fr 1fr;}}
@media(min-width:960px){.grid.c4{grid-template-columns:repeat(4,1fr);}}
.card{display:block;background:var(--white);border:1px solid var(--line);border-radius:16px;padding:24px 24px 22px;color:var(--ink);min-height:0;}
.card:hover{border-color:var(--coral);}
.card h3{font-size:22px;margin:12px 0 8px;}
.card p{color:var(--mute);font-size:17px;line-height:1.5;}
.card .go{display:inline-block;margin-top:14px;font-weight:700;color:var(--coral-d);font-size:17px;}
.glyph{width:52px;height:52px;border-radius:14px;background:var(--warm);display:flex;align-items:center;justify-content:center;color:var(--green-d);}
.glyph svg{width:28px;height:28px;}
/* reviews */
.rev{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:24px;}
.rev .star{color:#e8a13a;font-size:18px;letter-spacing:2px;}
.rev p{font-size:18px;margin:10px 0 14px;line-height:1.5;}
.rev b{font-size:16px;color:var(--mute);font-weight:600;}
/* counties */
.chips{display:flex;flex-wrap:wrap;gap:10px;}
.chip{display:inline-flex;align-items:center;min-height:50px;padding:0 20px;border-radius:999px;border:1.5px solid var(--line);background:var(--white);color:var(--ink);font-weight:600;font-size:17px;}
.chip:hover{border-color:var(--green);color:var(--green-d);}
.chip.more{background:var(--green);color:#fff;border-color:var(--green);}
/* note from Austin */
.note{display:grid;gap:20px;grid-template-columns:1fr;background:var(--white);border:1px solid var(--line);border-radius:18px;padding:26px;}
@media(min-width:760px){.note{grid-template-columns:200px 1fr;align-items:start;}}
.note img{width:160px;height:160px;border-radius:50%;object-fit:cover;object-position:center top;}
.note h2{font-size:26px;}
.note p{color:#3b352c;margin-top:12px;font-size:18px;}
.note small{display:block;color:var(--faint);font-size:15px;margin-top:12px;}
/* final CTA */
.final{background:var(--dark);color:#fff;padding-block:56px;text-align:center;}
.final h2{color:#fff;font-size:34px;}
.final p{color:#d9d2c5;font-size:19px;margin:10px auto 26px;max-width:560px;}
.final .num{font-family:var(--serif);font-size:40px;color:#fff;display:block;margin-top:14px;letter-spacing:-.5px;}
.final .btn{background:var(--coral);}
/* footer */
.foot{background:var(--dark);color:#bdb5a6;font-size:15px;padding-block:28px 100px;border-top:1px solid #3a3530;}
.foot .links{display:flex;flex-wrap:wrap;gap:8px 22px;margin-bottom:18px;}
.foot .links a{color:#e9e2d5;font-weight:600;padding:8px 0;}
.foot .disc{max-width:900px;line-height:1.5;color:#a39b8c;}
.foot b{color:#e9e2d5;}
/* sticky call bar (phones) */
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:30;padding:10px max(14px,env(safe-area-inset-left,0px)) calc(10px + env(safe-area-inset-bottom,0px)) max(14px,env(safe-area-inset-right,0px));background:rgba(250,246,239,.96);border-top:1px solid var(--line);backdrop-filter:blur(6px);}
.sticky a{display:flex;align-items:center;justify-content:center;gap:10px;min-height:58px;border-radius:14px;background:var(--coral);color:#fff;font-weight:700;font-size:20px;}
.sticky svg{width:20px;height:20px;}
@media(min-width:900px){.sticky{display:none;} .foot{padding-bottom:36px;}}
.mock{position:fixed;top:0;left:0;z-index:40;background:#1f1d1a;color:#fff;font-size:12px;padding:4px 10px;border-bottom-right-radius:8px;letter-spacing:1px;text-transform:uppercase;font-weight:700;}
@media(prefers-reduced-motion:reduce){*{transition:none!important;}}
"""

PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
G = {
 "cake": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 21h16M5 21v-7a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v7M8 12V9M12 12V9M16 12V9M8 6v1M12 5v2M16 6v1"/><path d="M5 17c1.5 1 3 1 4.5 0s3-1 4.5 0 3 1 4.5 0"/></svg>',
 "card": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 10h18M7 15h4"/></svg>',
 "family": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="7" r="3"/><circle cx="17" cy="9" r="2.3"/><path d="M3 20v-2a5 5 0 0 1 5-5h2a5 5 0 0 1 5 5v2M15 20v-1.5a3.5 3.5 0 0 1 3.5-3.5H19a3 3 0 0 1 3 3V20"/></svg>',
 "dollar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M16.5 6.5A3.5 3.5 0 0 0 13 4h-2a3.5 3.5 0 0 0 0 7h2a3.5 3.5 0 0 1 0 7h-2a3.5 3.5 0 0 1-3.5-3.5"/></svg>',
 "fork": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22V12M12 12L6 6M12 12l6-6M4 6h4V2M20 6h-4V2"/></svg>',
 "calendar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4M8 14h3v3H8z"/></svg>',
 "map": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-7-5.2-7-11a7 7 0 0 1 14 0c0 5.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h6a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4zM20 4h-6a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h7z"/></svg>',
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l8 3v7c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V5z"/><path d="M9 12l2 2 4-4"/></svg>',
 "pill": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="8" width="18" height="8" rx="4" transform="rotate(-45 12 12)"/><path d="M8.5 15.5l7-7"/></svg>',
 "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 5h16v11H9l-5 4z"/></svg>',
 "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>',
}
def glyph(k): return f'<span class="glyph">{G[k]}</span>'

def nav(a, label):
    return f"""<span class="mock">Mockup {label}</span>
<nav class="nav"><div class="wrap">
  <a class="brand" href="#"><img src="{a}logo.png" alt="Bluegrass Medicare Help"></a>
  <div class="navlinks"><a href="#">Start here</a><a href="#">Learning Center</a><a href="#">Your county</a><a href="#">About Austin</a></div>
  <a class="navcall" href="{TEL}">{PHONE_SVG}<span class="full">Call&nbsp;</span>{PHONE_TXT}</a>
  <button class="navtog" aria-label="Open menu"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
</div></nav>"""

REVIEWS = [("Austin was extremely knowledgeable and explained everything in great detail so I could easily understand. I know that my insurance needs are in good hands!", "Doug S., Google review"),
           ("He responds promptly and keeps us updated as to the status of our insurance. Thank you Austin!", "Denise L., Google review"),
           ("Best agent I have ever worked with. Organized, customer service oriented, follows up in a timely manner.", "Stephen C., Google review")]
def reviews(h="What Kentuckians say"):
    cards = "".join(f'<div class="rev"><div class="star">★★★★★</div><p>“{t}”</p><b>{w}</b></div>' for t, w in REVIEWS)
    return f"""<section class="sec"><div class="wrap">
  <h2>{h}</h2><p class="lead">5.0 on Google from more than 1,000 Kentuckians helped since 2019. <a href="#">Read all reviews &rarr;</a></p>
  <div class="grid c3">{cards}</div></div></section>"""

COUNTIES = ["Fayette (Lexington)", "Madison (Richmond)", "Jessamine (Nicholasville)", "Scott (Georgetown)", "Clark (Winchester)", "Woodford", "Franklin", "Boyle", "Mercer", "Bourbon"]
def counties(h="Medicare help in your county", lead="Plan counts, hospital networks and $0-premium options change from county to county. Pick yours."):
    chips = "".join(f'<a class="chip" href="#">{c}</a>' for c in COUNTIES) + '<a class="chip more" href="#">All 120 Kentucky counties &rarr;</a>'
    return f"""<section class="sec alt"><div class="wrap"><h2>{h}</h2><p class="lead">{lead}</p><div class="chips">{chips}</div></div></section>"""

def note(a):
    return f"""<section class="sec"><div class="wrap"><div class="note">
  <img src="{a}austin-tyler.jpg" alt="Austin Tyler, licensed Kentucky Medicare agent">
  <div><h2>A note from Austin</h2>
  <p>I'm Austin Tyler, a licensed Kentucky agent based in Lexington. I built this site so Kentuckians could get straight answers about Medicare without a sales pitch. Reading is free. So is calling: the carriers pay licensed agents, so you never pay me, and I represent several companies rather than one.</p>
  <p>If you'd rather sit across a table, the office is at 1029 Monarch Street, Suite 110, Lexington, right off Beaumont Circle.</p>
  <small>Kentucky DOI license #1187780 · NPN 20234188 · Tyler Insurance Group</small></div>
</div></div></section>"""

def final(h="Ready to talk it through?", p="One call, no forms, no pressure. If your current plan is right, you'll hear that too."):
    return f"""<section class="final"><div class="wrap"><h2>{h}</h2><p>{p}</p>
  <a class="btn" href="{TEL}">{PHONE_SVG}Call Austin</a><span class="num">{PHONE_TXT}</span>
  <p style="margin-top:18px;font-size:17px;">Prefer a time that suits you? <a href="#" style="color:#fff;text-decoration:underline;">Schedule a call</a></p></div></section>"""

FOOT = f"""<footer class="foot"><div class="wrap">
  <div class="links"><a href="#">Learning Center</a><a href="#">Turning 65</a><a href="#">Already on Medicare</a><a href="#">Your county</a><a href="#">Videos</a><a href="#">Glossary</a><a href="#">Quizzes</a><a href="#">Reviews</a><a href="#">About</a><a href="#">Schedule</a></div>
  <div class="disc"><b>Tyler Insurance Group</b> dba Bluegrass Medicare Help · 1029 Monarch Street, Suite 110, Lexington, KY 40513 · {PHONE_TXT}<br><br>
  We respect your privacy. This is a solicitation for insurance. Tyler Insurance Group is not connected with or endorsed by the United States government or the federal Medicare program. We do not offer every plan available in your area. Currently we represent 6 organizations which offer 158 products in your area. Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance Program (SHIP) to get information on all of your options.</div>
</div></footer>
<div class="sticky"><a href="{TEL}">{PHONE_SVG}Call Austin {PHONE_TXT}</a></div>"""

TRUST = '<div class="trust"><span><span class="star">★★★★★</span>5.0 on Google</span><span>1,000+ Kentuckians helped</span><span>KY licensed agent #1187780</span></div>'

# ---------------------------------------------------------------- A: The Front Desk
CSS_A = BASE_CSS + """
.hero{background:var(--white);padding-block:40px 48px;}
.hero .wrap{display:grid;gap:30px;grid-template-columns:1fr;align-items:center;}
@media(min-width:900px){.hero .wrap{grid-template-columns:1.1fr .9fr;gap:56px;} .hero{padding-block:64px 72px;}}
.eyebrow{display:inline-block;color:var(--green-d);font-weight:700;font-size:15px;letter-spacing:1.6px;text-transform:uppercase;margin-bottom:14px;}
.hero h1{font-size:40px;}
@media(min-width:900px){.hero h1{font-size:52px;}}
.hero .sub{font-size:20px;color:var(--mute);margin:16px 0 26px;max-width:540px;}
.ctarow{display:flex;flex-wrap:wrap;gap:12px 18px;align-items:center;margin-bottom:22px;}
.ctarow .or{color:var(--mute);font-size:17px;}
.ctarow .or a{font-weight:700;text-decoration:underline;}
.photo{position:relative;}
.photo img{width:100%;max-width:440px;aspect-ratio:4/5;object-fit:cover;object-position:center top;border-radius:20px;margin:0 auto;}
.photo .cap{position:absolute;left:50%;bottom:-18px;transform:translateX(-50%);background:var(--white);border:1px solid var(--line);border-radius:12px;padding:10px 18px;font-size:16px;white-space:nowrap;box-shadow:0 8px 24px rgba(42,38,32,.10);}
.photo .cap b{display:block;font-family:var(--serif);font-size:19px;}
.door{display:flex;align-items:center;gap:18px;padding:22px 24px;}
.door h3{margin:0 0 4px;}
.door .arrow{margin-left:auto;color:var(--coral-d);font-size:26px;}
"""
BODY_A = lambda a: f"""{nav(a,'A')}
<header class="hero"><div class="wrap">
  <div>
    <span class="eyebrow">Free Medicare help across Kentucky</span>
    <h1>Medicare, explained in plain English by a real person in Kentucky.</h1>
    <p class="sub">Guides for every Medicare question, and a licensed local agent who picks up the phone. No cost, no pressure, no call center.</p>
    <div class="ctarow"><a class="btn" href="{TEL}">{PHONE_SVG}Call {PHONE_TXT}</a><span class="or">or <a href="#">schedule a time</a></span></div>
    {TRUST}
  </div>
  <div class="photo"><img src="{a}austin-tyler.jpg" alt="Austin Tyler"><div class="cap"><b>Austin Tyler</b>Licensed agent · Lexington, KY</div></div>
</div></header>

<section class="sec"><div class="wrap">
  <h2>Where are you right now?</h2><p class="lead">Pick the one that fits and we'll start you in the right place.</p>
  <div class="grid c3">
    <a class="card door" href="#">{glyph('cake')}<div><h3>I'm turning 65</h3><p>Your dates, your choices, your first-year checklist.</p></div><span class="arrow">&rarr;</span></a>
    <a class="card door" href="#">{glyph('card')}<div><h3>I already have Medicare</h3><p>Check your plan for 2027 before December 7.</p></div><span class="arrow">&rarr;</span></a>
    <a class="card door" href="#">{glyph('family')}<div><h3>I'm helping a parent or spouse</h3><p>What to gather, what to ask, how to help well.</p></div><span class="arrow">&rarr;</span></a>
  </div>
</div></section>

<section class="sec alt"><div class="wrap">
  <h2>The guides people need most this month</h2><p class="lead">Written for Kentucky, checked against CMS and Social Security, dated. <a href="#">Browse all 45 guides &rarr;</a></p>
  <div class="grid c4">
    <a class="card" href="#">{glyph('dollar')}<h3>What Medicare costs in 2027</h3><p>Part B premium, deductibles, the $2,400 drug cap.</p><span class="go">Read &rarr;</span></a>
    <a class="card" href="#">{glyph('fork')}<h3>Advantage or Medigap?</h3><p>Two different roads, compared without a thumb on the scale.</p><span class="go">Read &rarr;</span></a>
    <a class="card" href="#">{glyph('calendar')}<h3>Find your enrollment dates</h3><p>Enter your birthday, get your 7-month window.</p><span class="go">Use the calculator &rarr;</span></a>
    <a class="card" href="#">{glyph('shield')}<h3>Stop Medicare sales calls</h3><p>The Kentucky steps that actually work.</p><span class="go">Read &rarr;</span></a>
  </div>
</div></section>

{counties()}
{reviews("Why people call Austin")}
{note(a)}
{final()}
{FOOT}"""

# ---------------------------------------------------------------- B: The Library
CSS_B = BASE_CSS + """
.hero{background:var(--white);padding-block:44px 40px;text-align:center;}
.hero h1{font-size:40px;max-width:760px;margin:0 auto;}
@media(min-width:900px){.hero h1{font-size:50px;} .hero{padding-block:60px 48px;}}
.hero .sub{font-size:20px;color:var(--mute);margin:14px auto 28px;max-width:600px;}
.ask{display:flex;max-width:680px;margin:0 auto 14px;background:var(--cream2);border:2px solid var(--ink);border-radius:16px;overflow:hidden;}
.ask input{flex:1;min-width:0;border:0;background:transparent;font:inherit;font-size:19px;padding:0 20px;min-height:60px;color:var(--ink);}
.ask button{border:0;background:var(--ink);color:#fff;font:inherit;font-weight:700;font-size:18px;padding:0 22px;display:inline-flex;align-items:center;gap:8px;cursor:pointer;}
.ask button svg{width:20px;height:20px;}
.hint{color:var(--faint);font-size:16px;}
.hint a{color:var(--mute);text-decoration:underline;}
.topics{padding-block:36px 30px;}
.topic{display:flex;align-items:flex-start;gap:16px;padding:22px 22px 20px;}
.topic h3{margin:0 0 2px;font-size:23px;}
.topic .glyph{flex-shrink:0;}
.topic small{color:var(--faint);font-size:15px;font-weight:600;}
.person{display:flex;flex-wrap:wrap;align-items:center;gap:16px 22px;background:var(--white);border:1px solid var(--line);border-radius:18px;padding:18px 22px;margin-top:26px;}
.person img{width:72px;height:72px;border-radius:50%;object-fit:cover;object-position:center top;}
.person .t{flex:1;min-width:220px;}
.person .t b{display:block;font-family:var(--serif);font-size:22px;font-weight:500;}
.person .t span{color:var(--mute);font-size:16.5px;}
.timely .card{border-left:5px solid var(--coral);}
.timely small{display:block;color:var(--coral-d);font-weight:700;font-size:14px;letter-spacing:1px;text-transform:uppercase;}
.tools{display:grid;gap:18px;grid-template-columns:1fr;}
@media(min-width:760px){.tools{grid-template-columns:1fr 1fr;}}
.tool{display:flex;gap:18px;align-items:flex-start;padding:24px;}
.tool h3{margin:0 0 6px;}
"""
BODY_B = lambda a: f"""{nav(a,'B')}
<header class="hero"><div class="wrap">
  <h1>Kentucky's plain-English Medicare guide.</h1>
  <p class="sub">Free, dated, checked against the official sources. Written by a licensed Kentucky agent you can actually call.</p>
  <form class="ask" onsubmit="return false"><input id="q" type="search" placeholder="What's your Medicare question?" aria-label="Search the guides"><button type="submit">{G['search']}Search</button></form>
  <p class="hint">Or pick a topic below. Not a reader? <a href="{TEL}">Call Austin at {PHONE_TXT}</a>.</p>
</div></header>

<section class="topics"><div class="wrap">
  <div class="grid c3">
    <a class="card topic" href="#">{glyph('book')}<div><h3>Medicare basics</h3><small>16 guides</small><p>Parts A, B, C and D, and the five cost words, explained once and clearly.</p></div></a>
    <a class="card topic" href="#">{glyph('cake')}<div><h3>Turning 65</h3><small>5 guides + calculator</small><p>Your enrollment window, your first decisions, the penalties to avoid.</p></div></a>
    <a class="card topic" href="#">{glyph('fork')}<div><h3>Choosing coverage</h3><small>14 guides</small><p>Advantage, Medigap, Part D, chronic-condition plans, dental fine print.</p></div></a>
    <a class="card topic" href="#">{glyph('dollar')}<div><h3>Costs and savings</h3><small>12 guides</small><p>2027 premiums, IRMAA, Extra Help, and what a $0 plan really costs.</p></div></a>
    <a class="card topic" href="#">{glyph('card')}<div><h3>Already on Medicare</h3><small>7 guides</small><p>Your Annual Notice of Change, switching, and this year's changes.</p></div></a>
    <a class="card topic" href="#">{glyph('map')}<div><h3>Your Kentucky county</h3><small>18 local pages</small><p>Plan counts, hospital networks and $0 options where you live.</p></div></a>
  </div>
  <div class="person">
    <img src="{a}austin-tyler.jpg" alt="Austin Tyler">
    <div class="t"><b>Have a question the guides don't answer? Ask Austin.</b><span>Licensed Kentucky agent #1187780 · Lexington · free, no pressure</span></div>
    <a class="btn" href="{TEL}">{PHONE_SVG}{PHONE_TXT}</a>
  </div>
</div></section>

<section class="sec alt timely"><div class="wrap">
  <h2>This month in Medicare</h2><p class="lead">What changed, what is due, and what to ignore.</p>
  <div class="grid c3">
    <a class="card" href="#"><small>Due December 7</small><h3>Annual Enrollment ends in 38 days</h3><p>How to read your Annual Notice of Change and decide whether to stay.</p><span class="go">Read &rarr;</span></a>
    <a class="card" href="#"><small>Updated October 8</small><h3>The $90 Medicare payment</h3><p>Who got it, why Advantage members didn't, and the scam calls to expect.</p><span class="go">Read &rarr;</span></a>
    <a class="card" href="#"><small>Plan year 2027</small><h3>What changes in Kentucky for 2027</h3><p>Part B premium, the $700 drug deductible, the $2,400 cap, plans leaving.</p><span class="go">Read &rarr;</span></a>
  </div>
</div></section>

<section class="sec"><div class="wrap">
  <h2>Tools</h2><p class="lead">Two things that take a minute and save a lot of guessing.</p>
  <div class="tools">
    <a class="card tool" href="#">{glyph('calendar')}<div><h3>Enrollment date calculator</h3><p>Type your birthday. Get your 7-month window, your coverage start date and a reminder you can add to your calendar. Nothing is saved.</p><span class="go">Find my dates &rarr;</span></div></a>
    <a class="card tool" href="#">{glyph('chat')}<div><h3>Five-question knowledge checks</h3><p>Every guide ends with one. Try the Medicare basics check and see where you stand.</p><span class="go">Take the quiz &rarr;</span></div></a>
  </div>
</div></section>

{counties()}
{note(a)}
{reviews()}
{final("Still have a question?", "Call and you get Austin, not a queue. If reading is all you need today, that's fine too.")}
{FOOT}"""

# ---------------------------------------------------------------- C: The Kitchen Table
CSS_C = BASE_CSS + """
.hero{background:var(--white);padding-block:36px 44px;}
.who{display:flex;align-items:center;gap:14px;margin-bottom:22px;}
.who img{width:56px;height:56px;border-radius:50%;object-fit:cover;object-position:center top;}
.who b{display:block;font-size:17px;} .who span{color:var(--mute);font-size:15.5px;}
.hero h1{font-size:40px;max-width:700px;}
@media(min-width:900px){.hero h1{font-size:50px;} .hero{padding-block:56px 60px;}}
.hero .q{font-size:22px;color:var(--mute);margin:16px 0 22px;}
.big{display:grid;gap:14px;grid-template-columns:1fr;max-width:720px;}
.big a{display:flex;align-items:center;gap:18px;min-height:88px;padding:18px 22px;border-radius:18px;background:var(--cream2);border:2px solid var(--line);color:var(--ink);font-size:22px;font-weight:700;}
.big a:hover{border-color:var(--coral);background:var(--white);}
.big a small{display:block;font-weight:500;color:var(--mute);font-size:16.5px;margin-top:2px;}
.big a .arrow{margin-left:auto;color:var(--coral-d);font-size:28px;}
.callrow{display:flex;flex-wrap:wrap;align-items:center;gap:12px 18px;margin-top:26px;max-width:720px;}
.callrow .btn{background:var(--green);} .callrow .btn:hover{background:var(--green-d);}
.callrow span{color:var(--mute);font-size:17px;}
.steps{display:grid;gap:16px;grid-template-columns:1fr;}
@media(min-width:760px){.steps{grid-template-columns:repeat(3,1fr);}}
.step{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:24px;}
.step .n{width:44px;height:44px;border-radius:50%;background:var(--green);color:#fff;display:flex;align-items:center;justify-content:center;font-family:var(--serif);font-size:22px;margin-bottom:12px;}
.step h3{font-size:22px;margin-bottom:6px;}
.step p{color:var(--mute);font-size:17.5px;}
.list{background:var(--white);border:1px solid var(--line);border-radius:16px;overflow:hidden;}
.list a{display:flex;align-items:center;gap:16px;min-height:70px;padding:14px 22px;border-top:1px solid var(--line);color:var(--ink);font-size:19px;font-weight:600;}
.list a:first-child{border-top:0;}
.list a:hover{background:var(--cream2);}
.list a .arrow{margin-left:auto;color:var(--coral-d);font-size:24px;}
.hero .wrap{max-width:820px;}
.list a small{display:block;color:var(--faint);font-weight:500;font-size:15px;}
"""
BODY_C = lambda a: f"""{nav(a,'C')}
<header class="hero"><div class="wrap">
  <div class="who"><img src="{a}austin-tyler.jpg" alt="Austin Tyler"><div><b>Austin Tyler, licensed Kentucky Medicare agent</b><span>Lexington · helping all 120 counties · free</span></div></div>
  <h1>Let's figure out Medicare together.</h1>
  <p class="q">Which one sounds like you?</p>
  <div class="big">
    <a href="#">{glyph('cake')}<div>I'm turning 65 soon<small>Find your dates and your first decisions</small></div><span class="arrow">&rarr;</span></a>
    <a href="#">{glyph('card')}<div>I already have Medicare<small>Check your plan for 2027 before December 7</small></div><span class="arrow">&rarr;</span></a>
    <a href="#">{glyph('family')}<div>I'm helping a parent or spouse<small>What to gather and what to ask</small></div><span class="arrow">&rarr;</span></a>
  </div>
  <div class="callrow"><a class="btn" href="{TEL}">{PHONE_SVG}Not sure? Call {PHONE_TXT}</a><span>Most people start here. That's fine.</span></div>
</div></header>

<section class="sec"><div class="wrap">
  <h2>What happens when you call</h2><p class="lead">Three short steps. No forms, no homework, nothing to sign on the call.</p>
  <div class="steps">
    <div class="step"><div class="n">1</div><h3>We talk for ten minutes</h3><p>Your doctors, your prescriptions, your budget. You don't need to know anything about Medicare first.</p></div>
    <div class="step"><div class="n">2</div><h3>Austin does the comparing</h3><p>Every plan available in your county, side by side, in plain English. You never read a brochure.</p></div>
    <div class="step"><div class="n">3</div><h3>You decide</h3><p>Pick one, keep what you have, or think about it. The carriers pay the agent, so the help is free either way.</p></div>
  </div>
</div></section>

{reviews("What clients say")}

<section class="sec alt"><div class="wrap">
  <h2>Learn at your own pace</h2><p class="lead">Plain-English guides for Kentucky, each with a recap and a five-question check. <a href="#">See all 45 &rarr;</a></p>
  <div class="list">
    <a href="#">{glyph('dollar')}<div>What Medicare costs in 2027<small>Part B premium, deductibles, the $2,400 drug cap</small></div><span class="arrow">&rarr;</span></a>
    <a href="#">{glyph('fork')}<div>Medicare Advantage or Medigap?<small>The honest comparison, including the underwriting trap</small></div><span class="arrow">&rarr;</span></a>
    <a href="#">{glyph('book')}<div>Premium, deductible, copay, coinsurance, max out-of-pocket<small>The five words that run your plan</small></div><span class="arrow">&rarr;</span></a>
    <a href="#">{glyph('shield')}<div>How to stop Medicare sales calls in Kentucky<small>The steps that work, with the Attorney General's line</small></div><span class="arrow">&rarr;</span></a>
    <a href="#">{glyph('calendar')}<div>Find your enrollment dates<small>A one-minute calculator, nothing saved</small></div><span class="arrow">&rarr;</span></a>
  </div>
</div></section>

{counties("We serve all of Kentucky", "The office is in Lexington. The phone works everywhere. Local pages for the counties we know best:")}
{final()}
{FOOT}"""

# ---------------------------------------------------------------- B v2: The Library, Devoted-style refinements + palette switcher
# Layout: colour-blocked full-width bands (no borders between sections), white cards floating on soft tints,
# pill buttons, one signature colour used for every action. Palettes swap through data-palette on <html>.
CSS_B2 = """
:root{
  --bg:#ffffff;--surf:#ffffff;--tint1:#eaf3fb;--tint2:#fdf3e1;--tint3:#eaf6ef;--ink:#14212e;--mute:#45525f;--line:#d9e3ec;
  --cta:#1f62a8;--cta-d:#174f8a;--link:#1a5a9c;--accent:#c9382d;--glyph:#1f62a8;--glyphbg:#eaf3fb;--foot:#14212e;--star:#e09a1a;
  --serif:'Fraunces',Georgia,serif;--sans:'Source Sans 3',-apple-system,'Segoe UI',sans-serif;--rounded:'Figtree','Source Sans 3',-apple-system,sans-serif;
  --head:var(--serif);--headw:500;
  color-scheme:light;
}
html[data-palette="meadow"]{--tint1:#e9f6ee;--tint2:#fff4d6;--tint3:#e8f2fb;--ink:#17261d;--mute:#46544b;--line:#d8e6dc;--cta:#1c7a4b;--cta-d:#145f3a;--link:#17683f;--accent:#8a5a00;--glyph:#1c7a4b;--glyphbg:#e9f6ee;--foot:#17261d;}
html[data-palette="coral"]{--tint1:#fff0e8;--tint2:#e9f3fb;--tint3:#fff7df;--ink:#1b2836;--mute:#4a5563;--line:#eadfd6;--cta:#d2481f;--cta-d:#b23c17;--link:#b23c17;--accent:#1b6f8f;--glyph:#d2481f;--glyphbg:#fff0e8;--foot:#1b2836;}
html[data-palette="current"]{--bg:#f4efe7;--tint1:#faf6ef;--tint2:#efe6d6;--tint3:#faf6ef;--ink:#2a2620;--mute:#5f594f;--line:#e2d9c8;--cta:#d05528;--cta-d:#b3431d;--link:#b3431d;--accent:#b3431d;--glyph:#2f6844;--glyphbg:#efe6d6;--foot:#1f1d1a;}
html[data-head="sans"]{--head:var(--rounded);--headw:700;}
*{box-sizing:border-box;margin:0;padding:0;}
html{-webkit-text-size-adjust:100%;}
body{font-family:var(--sans);font-size:19px;line-height:1.55;color:var(--ink);background:var(--bg);-webkit-font-smoothing:antialiased;}
img{max-width:100%;display:block;}
a{color:var(--link);text-decoration:none;}
a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--accent);outline-offset:3px;}
.wrap{max-width:1100px;margin:0 auto;padding-left:max(18px,env(safe-area-inset-left,0px));padding-right:max(18px,env(safe-area-inset-right,0px));}
h1,h2,h3{font-family:var(--head);font-weight:var(--headw);line-height:1.12;letter-spacing:-.4px;text-wrap:balance;color:var(--ink);}
h2{font-size:32px;margin-bottom:8px;}
.lead{color:var(--mute);font-size:19px;max-width:620px;margin-bottom:28px;}
.band{padding-block:60px;} .t1{background:var(--tint1);} .t2{background:var(--tint2);} .t3{background:var(--tint3);} .plain{background:var(--bg);}
.pill{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:56px;padding:0 28px;border-radius:999px;background:var(--cta);color:#fff;font-weight:700;font-size:19px;border:0;cursor:pointer;white-space:nowrap;-webkit-tap-highlight-color:transparent;}
.pill:hover{background:var(--cta-d);}
.pill svg{width:21px;height:21px;flex-shrink:0;}
.eyebrow{display:inline-block;color:var(--accent);font-weight:700;font-size:15px;letter-spacing:1.6px;text-transform:uppercase;margin-bottom:14px;}
/* review switcher (mockup only) */
.switch{background:#111;color:#eee;font-size:14px;padding-block:8px;}
.switch .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;}
.switch b{font-weight:700;letter-spacing:.5px;text-transform:uppercase;font-size:12px;color:#aaa;margin-right:2px;}
.switch button{font:inherit;font-size:14px;font-weight:600;border:1px solid #555;background:#222;color:#eee;border-radius:999px;padding:6px 12px;min-height:34px;cursor:pointer;}
.switch button[aria-pressed="true"]{background:#fff;color:#111;border-color:#fff;}
.switch .sep{width:1px;height:20px;background:#444;margin:0 4px;}
/* header */
.nav{background:var(--surf);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20;}
.nav .wrap{display:flex;align-items:center;gap:18px;min-height:76px;}
.brand img{height:46px;width:auto;}
.navlinks{display:none;gap:28px;margin-left:auto;font-weight:600;font-size:17px;}
.navlinks a{color:var(--ink);padding:10px 2px;}
.navlinks a:hover{color:var(--link);}
.navcall{margin-left:auto;display:inline-flex;flex-direction:column;align-items:flex-end;line-height:1.15;color:var(--ink);}
.navcall small{font-size:13px;color:var(--mute);font-weight:600;}
.navcall span{display:inline-flex;align-items:center;gap:7px;font-weight:700;font-size:18px;color:var(--cta);}
.navcall svg{width:17px;height:17px;}
.navtog{width:48px;height:48px;border:1px solid var(--line);border-radius:999px;background:var(--surf);display:inline-flex;align-items:center;justify-content:center;color:var(--ink);}
@media(min-width:900px){.navlinks{display:flex;} .navcall{margin-left:12px;} .navtog{display:none;}}
@media(max-width:420px){.navcall small{display:none;} .navcall span{font-size:16.5px;}}
/* hero */
.hero{background:var(--bg);padding-block:52px 56px;text-align:center;}
@media(min-width:900px){.hero{padding-block:76px 72px;}}
.hero h1{font-size:42px;max-width:780px;margin:0 auto;}
@media(min-width:900px){.hero h1{font-size:58px;}}
.hero .sub{font-size:20.5px;color:var(--mute);margin:16px auto 30px;max-width:600px;}
.ask{display:flex;align-items:center;max-width:660px;margin:0 auto;background:var(--surf);border:2px solid var(--line);border-radius:999px;padding:6px;box-shadow:0 10px 30px rgba(20,33,46,.08);}
.ask:focus-within{border-color:var(--cta);}
.ask input{flex:1;min-width:0;border:0;background:transparent;font:inherit;font-size:19px;padding:0 18px;min-height:52px;color:var(--ink);}
.ask input:focus{outline:none;}
.ask button{flex-shrink:0;}
.ask button svg{width:19px;height:19px;}
@media(max-width:480px){.ask .lbl{display:none;} .ask button{padding:0 18px;}}
.human{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:12px 14px;margin-top:22px;color:var(--mute);font-size:17.5px;}
.human img{width:44px;height:44px;border-radius:50%;object-fit:cover;object-position:center top;}
.human a{font-weight:700;color:var(--link);white-space:nowrap;}
.trust{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 26px;margin-top:22px;color:var(--mute);font-size:16px;font-weight:600;}
.trust .star{color:var(--star);letter-spacing:1px;margin-right:6px;}
/* cards */
.grid{display:grid;gap:18px;grid-template-columns:1fr;}
@media(min-width:640px){.grid.c2{grid-template-columns:1fr 1fr;} .grid.c3{grid-template-columns:1fr 1fr;}}
@media(min-width:960px){.grid.c3{grid-template-columns:repeat(3,1fr);}}
.card{display:flex;gap:16px;align-items:flex-start;background:var(--surf);border-radius:20px;padding:24px;color:var(--ink);box-shadow:0 1px 2px rgba(20,33,46,.06),0 8px 24px rgba(20,33,46,.06);transition:transform .15s,box-shadow .15s;min-width:0;}
.card:hover{transform:translateY(-2px);box-shadow:0 2px 4px rgba(20,33,46,.08),0 14px 32px rgba(20,33,46,.10);}
.card > div{min-width:0;}
.card h3{font-size:23px;margin-bottom:4px;}
.card p{color:var(--mute);font-size:17px;line-height:1.5;}
.card small{display:block;color:var(--mute);font-size:15px;font-weight:600;margin-bottom:4px;}
.card .go{display:inline-block;margin-top:12px;font-weight:700;color:var(--link);font-size:17px;}
.glyph{flex-shrink:0;width:54px;height:54px;border-radius:50%;background:var(--glyphbg);display:flex;align-items:center;justify-content:center;color:var(--glyph);}
.t1 .glyph{background:var(--tint1);}
.glyph svg{width:27px;height:27px;}
.chipdate{display:inline-block;background:var(--tint2);color:var(--ink);font-size:14px;font-weight:700;border-radius:999px;padding:4px 12px;margin-bottom:10px;}
.stack{flex-direction:column;gap:6px;}
/* ask austin band */
.askband{display:flex;flex-wrap:wrap;align-items:center;gap:20px 26px;}
.askband img{width:96px;height:96px;border-radius:50%;object-fit:cover;object-position:center top;border:4px solid var(--surf);}
.askband .t{flex:1;min-width:240px;}
.askband h2{font-size:28px;margin-bottom:4px;}
.askband p{color:var(--mute);font-size:17.5px;}
/* counties */
.chips{display:flex;flex-wrap:wrap;gap:10px;}
.chip{display:inline-flex;align-items:center;min-height:50px;padding:0 20px;border-radius:999px;background:var(--surf);color:var(--ink);font-weight:600;font-size:17px;box-shadow:0 1px 2px rgba(20,33,46,.08);}
.chip:hover{color:var(--link);}
.chip.more{background:var(--cta);color:#fff;}
/* reviews */
.rev{background:var(--surf);border-radius:20px;padding:24px;box-shadow:0 1px 2px rgba(20,33,46,.06),0 8px 24px rgba(20,33,46,.06);}
.rev .star{color:var(--star);font-size:18px;letter-spacing:2px;}
.rev p{font-size:18px;margin:10px 0 14px;line-height:1.5;}
.rev b{font-size:16px;color:var(--mute);font-weight:600;}
/* note */
.note{display:grid;gap:22px;grid-template-columns:1fr;align-items:start;}
@media(min-width:760px){.note{grid-template-columns:220px 1fr;}}
.note img{width:180px;height:180px;border-radius:50%;object-fit:cover;object-position:center top;}
.note h2{font-size:30px;}
.note p{margin-top:12px;font-size:18.5px;max-width:640px;}
.note small{display:block;color:var(--mute);font-size:15px;margin-top:14px;}
/* final */
.final{background:var(--cta);color:#fff;padding-block:60px;text-align:center;}
.final h2{color:#fff;font-size:36px;}
.final p{color:rgba(255,255,255,.92);font-size:19.5px;margin:10px auto 26px;max-width:560px;}
.final .pill{background:#fff;color:var(--cta);}
.final .pill:hover{background:rgba(255,255,255,.9);}
.final .num{display:block;margin-top:16px;font-size:30px;font-weight:700;letter-spacing:.3px;}
.final a.u{color:#fff;text-decoration:underline;}
/* footer */
.foot{background:var(--foot);color:rgba(255,255,255,.72);font-size:15px;padding-block:30px 104px;}
.foot .links{display:flex;flex-wrap:wrap;gap:6px 22px;margin-bottom:18px;}
.foot .links a{color:#fff;font-weight:600;padding:8px 0;}
.foot .disc{max-width:900px;line-height:1.55;}
.foot b{color:#fff;}
@media(min-width:900px){.foot{padding-bottom:36px;}}
/* sticky call (phones) */
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:30;padding:10px max(14px,env(safe-area-inset-left,0px)) calc(10px + env(safe-area-inset-bottom,0px)) max(14px,env(safe-area-inset-right,0px));background:var(--surf);box-shadow:0 -6px 20px rgba(20,33,46,.10);}
.sticky a{display:flex;align-items:center;justify-content:center;gap:10px;min-height:56px;border-radius:999px;background:var(--cta);color:#fff;font-weight:700;font-size:19.5px;}
.sticky svg{width:20px;height:20px;}
@media(min-width:900px){.sticky{display:none;}}
@media(prefers-reduced-motion:reduce){*{transition:none!important;}}
"""

SWITCH = """<div class="switch" role="region" aria-label="Mockup review controls"><div class="wrap">
  <b>Mockup B</b><b>Colors</b>
  <button type="button" data-p="blue" aria-pressed="true">Logo blue</button>
  <button type="button" data-p="meadow" aria-pressed="false">Meadow green</button>
  <button type="button" data-p="coral" aria-pressed="false">Bright coral</button>
  <button type="button" data-p="current" aria-pressed="false">Current</button>
  <span class="sep"></span><b>Headings</b>
  <button type="button" data-h="serif" aria-pressed="true">Serif</button>
  <button type="button" data-h="sans" aria-pressed="false">Rounded sans</button>
</div></div>"""
SWITCH_JS = """<script>
(function(){
  var root=document.documentElement;
  function setP(p){ if(p==='blue'){root.removeAttribute('data-palette');}else{root.setAttribute('data-palette',p);}
    document.querySelectorAll('[data-p]').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-p')===p?'true':'false');});
    try{localStorage.setItem('bmh-pal',p);}catch(e){} }
  function setH(h){ if(h==='serif'){root.removeAttribute('data-head');}else{root.setAttribute('data-head',h);}
    document.querySelectorAll('[data-h]').forEach(function(b){b.setAttribute('aria-pressed',b.getAttribute('data-h')===h?'true':'false');});
    try{localStorage.setItem('bmh-head',h);}catch(e){} }
  document.querySelectorAll('[data-p]').forEach(function(b){b.addEventListener('click',function(){setP(b.getAttribute('data-p'));});});
  document.querySelectorAll('[data-h]').forEach(function(b){b.addEventListener('click',function(){setH(b.getAttribute('data-h'));});});
  try{var p=localStorage.getItem('bmh-pal'); if(p) setP(p); var h=localStorage.getItem('bmh-head'); if(h) setH(h);}catch(e){}
  var f=document.querySelector('.ask'); if(f) f.addEventListener('submit',function(e){e.preventDefault();});
})();
</script>"""

def card(g, h, small, p, go=None):
    return (f'<a class="card" href="#">{glyph(g)}<div><h3>{h}</h3>' + (f'<small>{small}</small>' if small else '') +
            f'<p>{p}</p>' + (f'<span class="go">{go} &rarr;</span>' if go else '') + '</div></a>')

BODY_B2 = lambda a: f"""{SWITCH}
<nav class="nav"><div class="wrap">
  <a class="brand" href="#"><img src="{a}logo.png" alt="Bluegrass Medicare Help"></a>
  <div class="navlinks"><a href="#">Start here</a><a href="#">Learning Center</a><a href="#">Your county</a><a href="#">About Austin</a></div>
  <a class="navcall" href="{TEL}"><small>Talk to Austin, free</small><span>{PHONE_SVG}{PHONE_TXT}</span></a>
  <button class="navtog" aria-label="Open menu"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
</div></nav>

<header class="hero"><div class="wrap">
  <span class="eyebrow">Free Medicare help for all of Kentucky</span>
  <h1>Kentucky's plain-English Medicare guide.</h1>
  <p class="sub">Every Medicare question answered in plain English, checked against official sources. Written by a licensed Kentucky agent you can actually call.</p>
  <form class="ask" role="search"><input id="q" type="search" placeholder="Type your Medicare question" aria-label="Search the guides"><button class="pill" type="submit">{G['search']}<span class="lbl">Search</span></button></form>
  <div class="human"><img src="{a}austin-tyler.jpg" alt=""><span>Rather talk it through? Austin picks up.</span><a href="{TEL}">{PHONE_TXT}</a></div>
  <div class="trust"><span><span class="star">★★★★★</span>5.0 on Google</span><span>1,000+ Kentuckians helped</span><span>KY licensed agent #1187780</span></div>
</div></header>

<section class="band t1"><div class="wrap">
  <h2>Start with a topic</h2><p class="lead">Forty-five guides, each with a short recap and a five-question check.</p>
  <div class="grid c3">
    {card('book','Medicare basics','16 guides','Parts A, B, C and D, and the five cost words, explained once and clearly.')}
    {card('cake','Turning 65','5 guides + calculator','Your enrollment window, your first decisions, the penalties to avoid.')}
    {card('fork','Choosing coverage','14 guides','Advantage, Medigap, Part D, chronic-condition plans, dental fine print.')}
    {card('dollar','Costs and savings','12 guides','2027 premiums, IRMAA, Extra Help, and what a $0 plan really costs.')}
    {card('card','Already on Medicare','7 guides','Your Annual Notice of Change, switching, and this year’s changes.')}
    {card('map','Your Kentucky county','18 local pages','Plan counts, hospital networks and $0 options where you live.')}
  </div>
</div></section>

<section class="band t2"><div class="wrap askband">
  <img src="{a}austin-tyler.jpg" alt="Austin Tyler">
  <div class="t"><h2>Have a question the guides don't answer?</h2><p>Ask Austin. Licensed Kentucky agent, Lexington office, no cost and no pressure.</p></div>
  <a class="pill" href="{TEL}">{PHONE_SVG}Call {PHONE_TXT}</a>
</div></section>

<section class="band plain"><div class="wrap">
  <h2>This month in Medicare</h2><p class="lead">What changed, what is due, and what you can ignore.</p>
  <div class="grid c3">
    <a class="card stack" href="#"><span class="chipdate">Due December 7</span><h3>Annual Enrollment ends in 38 days</h3><p>How to read your Annual Notice of Change and decide whether to stay.</p><span class="go">Read &rarr;</span></a>
    <a class="card stack" href="#"><span class="chipdate">Updated October 8</span><h3>The $90 Medicare payment</h3><p>Who got it, why Advantage members didn't, and the scam calls to expect.</p><span class="go">Read &rarr;</span></a>
    <a class="card stack" href="#"><span class="chipdate">Plan year 2027</span><h3>What changes in Kentucky for 2027</h3><p>Part B premium, the $700 drug deductible, the $2,400 cap, plans leaving.</p><span class="go">Read &rarr;</span></a>
  </div>
</div></section>

<section class="band t3"><div class="wrap">
  <h2>Two free tools</h2><p class="lead">Each takes about a minute.</p>
  <div class="grid c2">
    {card('calendar','Enrollment date calculator','','Type your birthday. Get your 7-month window, your coverage start date and a calendar reminder. Nothing is saved.','Find my dates')}
    {card('chat','Five-question knowledge checks','','Every guide ends with one. Try the Medicare basics check and see where you stand.','Take the quiz')}
  </div>
</div></section>

<section class="band plain"><div class="wrap">
  <h2>Medicare help in your county</h2><p class="lead">Plan counts, hospital networks and $0-premium options change from county to county. Pick yours.</p>
  <div class="chips">{''.join(f'<a class="chip" href="#">{c}</a>' for c in COUNTIES)}<a class="chip more" href="#">All 120 Kentucky counties &rarr;</a></div>
</div></section>

<section class="band t1"><div class="wrap">
  <h2>What Kentuckians say</h2><p class="lead">5.0 on Google from more than 1,000 Kentuckians helped since 2019. <a href="#">Read all reviews &rarr;</a></p>
  <div class="grid c3">{''.join(f'<div class="rev"><div class="star">★★★★★</div><p>“{t}”</p><b>{w}</b></div>' for t, w in REVIEWS)}</div>
</div></section>

<section class="band plain"><div class="wrap note">
  <img src="{a}austin-tyler.jpg" alt="Austin Tyler, licensed Kentucky Medicare agent">
  <div><h2>A note from Austin</h2>
  <p>I'm Austin Tyler, a licensed Kentucky agent based in Lexington. I built this site so Kentuckians could get straight answers about Medicare without a sales pitch. Reading is free. So is calling: the carriers pay licensed agents, so you never pay me, and I represent several companies rather than one.</p>
  <p>If you'd rather sit across a table, the office is at 1029 Monarch Street, Suite 110, Lexington, right off Beaumont Circle.</p>
  <small>Kentucky DOI license #1187780 · NPN 20234188 · Tyler Insurance Group</small></div>
</div></section>

<section class="final"><div class="wrap"><h2>Still have a question?</h2><p>Call and you get Austin, not a queue. If reading is all you need today, that's fine too.</p>
  <a class="pill" href="{TEL}">{PHONE_SVG}Call Austin</a><span class="num">{PHONE_TXT}</span>
  <p style="margin-top:16px;font-size:17px;">Prefer a set time? <a class="u" href="#">Schedule a call</a></p></div></section>
{FOOT}
{SWITCH_JS}"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Figtree:wght@600;700;800&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Source+Sans+3:wght@400;500;600;700&display=swap" rel="stylesheet">'
DESIGNS = {"a": ("The Front Desk", CSS_A, BODY_A), "b": ("The Library", CSS_B2, BODY_B2), "c": ("The Kitchen Table", CSS_C, BODY_C)}
for key, (name, css, body) in DESIGNS.items():
    title = f"Homepage mockup {key.upper()}: {name}"
    repo = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex,nofollow"><title>{title}</title>{FONTS}
<style>{css}</style></head><body>
{body('/assets/')}
</body></html>"""
    d = f"mockups/home-v3/{key}"; os.makedirs(d, exist_ok=True); open(f"{d}/index.html", "w", encoding="utf-8").write(repo)
    art = f"""<title>{name}</title>
<meta name="claude:viewport-fit-sides" content="cover">
{FONTS}
<style>{css}</style>
{body('')}"""
    open(f"{ART}/{key}.html", "w", encoding="utf-8").write(art)
    print("built", key, name, len(repo))
