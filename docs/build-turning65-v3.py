#!/usr/bin/env python3
"""Build /turning-65/ as a Devoted-style audience page: one job (get a turning-65 reader ready),
one primary action (book a free review), four steps in the order they come up, the right tools and
guides, common questions, and a final call band. Replaces the old quote-form page and the
/articles/turning-65/ topic page. The guide list between the T65-GUIDES markers is filled by
docs/build-hubs.py from the Learning Center. Idempotent."""
import json, re

SITE = "https://www.bluegrassmedicarehelp.com"
URL = SITE + "/turning-65/"
TITLE = "Turning 65 in Kentucky: Your Medicare Plan, Step by Step"
DESC = ("Turning 65 in Kentucky? Your enrollment window, whether to sign up or wait, Advantage or a "
        "Supplement, and drug coverage, in order. Free help from licensed Lexington advisors.")
TEL = "tel:18597858289"; PN = "(859) 785-8289"

home = open("index.html", encoding="utf-8").read()
cur = open("turning-65/index.html", encoding="utf-8").read()
head_top = cur[:cur.index("<title>")]                       # tracking snippet, unchanged
fonts_css = home[home.index('<link rel="preconnect"'):home.index("<style>")]
home_css = home[home.index("<style>") + 7:home.index("</style>")]
chrome_top = home[home.index('<a class="skip-link"'):home.index('<main id="main">')]
chrome_bottom = home[home.index('<div class="sticky">'):home.index("</footer>") + len("</footer>")]
NAV_JS = ("<script>(function(){var tog=document.getElementById('navtog'),links=document.getElementById('navlinks');"
          "if(!tog||!links)return;tog.addEventListener('click',function(){var o=links.classList.toggle('open');"
          "tog.setAttribute('aria-expanded',o?'true':'false');});links.addEventListener('click',function(e){"
          "if(e.target.tagName==='A'){links.classList.remove('open');tog.setAttribute('aria-expanded','false');}});})();</script>")
keep_guides = re.search(r"<!--T65-GUIDES-->.*?<!--/T65-GUIDES-->", cur, re.S)
GUIDES = keep_guides.group(0) if keep_guides else "<!--T65-GUIDES--><!--/T65-GUIDES-->"

FAQ = [
 ("When should I start planning?", "About six months before your 65th birthday. Your sign-up window opens three months before your birthday month, and the decisions about Advantage, a Supplement and drug coverage are easier with a few weeks to compare."),
 ("What does your help cost?", "Nothing, now or ever. Licensed agents are paid by the insurance carriers, and on Medicare Advantage and drug plans that amount is set by Medicare and is the same across carriers, so it never comes out of your pocket and never steers the advice."),
 ("Are you part of Medicare or the government?", "No. Tyler Insurance Group is a private, licensed, independent insurance agency in Lexington. We are not connected with the federal government or the Medicare program."),
 ("What if I am not ready to decide?", "Then you do not decide. A review has no obligation. You leave with your dates, your options in plain English, and time to think it over."),
]

CSS = home_css + """
/* turning 65 page */
.hero{text-align:left;}
.hero .wrap{max-width:860px;}
.hero h1{margin:0;max-width:760px;}
.hero .sub{margin:16px 0 26px;max-width:640px;}
.heroact{display:flex;flex-wrap:wrap;align-items:center;gap:14px 20px;}
.heroact .or{color:var(--mute);font-size:18px;}
.heroact .or a{font-weight:700;white-space:nowrap;}
.human{justify-content:flex-start;}
.steps{display:grid;gap:18px;grid-template-columns:1fr;counter-reset:s;}
@media(min-width:760px){.steps{grid-template-columns:1fr 1fr;}}
.step{background:var(--surf);border-radius:20px;padding:24px;box-shadow:0 1px 2px rgba(27,40,54,.06),0 8px 24px rgba(27,40,54,.06);}
.step .n{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:var(--cta);color:#fff;font-weight:800;font-family:var(--head);font-size:19px;margin-bottom:12px;}
.step h3{font-family:var(--head);font-size:22px;line-height:1.2;margin-bottom:8px;}
.step p{color:var(--mute);font-size:17px;line-height:1.55;}
.step a{display:inline-block;margin-top:10px;font-weight:700;}
.glist{background:var(--surf);border-radius:20px;overflow:hidden;box-shadow:0 1px 2px rgba(27,40,54,.06),0 8px 24px rgba(27,40,54,.06);}
.glist a{display:flex;align-items:center;gap:16px;min-height:72px;padding:16px 22px;border-top:1px solid var(--line);color:var(--ink);}
.glist a:first-child{border-top:0;}
.glist a:hover{background:var(--tint1);}
.glist b{display:block;font-size:18.5px;line-height:1.3;}
.glist small{display:block;color:var(--mute);font-size:15.5px;line-height:1.45;margin-top:3px;}
.glist .arrow{margin-left:auto;color:var(--cta-d);font-size:24px;flex-shrink:0;}
.acc details{background:var(--surf);border-radius:16px;margin-bottom:12px;box-shadow:0 1px 2px rgba(27,40,54,.06);}
.acc summary{cursor:pointer;list-style:none;padding:20px 22px;font-weight:700;font-size:19px;display:flex;justify-content:space-between;gap:14px;min-height:56px;}
.acc summary::-webkit-details-marker{display:none;}
.acc summary::after{content:"+";color:var(--cta-d);font-size:24px;line-height:1;}
.acc details[open] summary::after{content:"\\2212";}
.acc .a{padding:0 22px 20px;color:var(--mute);font-size:17.5px;line-height:1.6;}
.team{display:grid;gap:18px;grid-template-columns:1fr;}
@media(min-width:760px){.team{grid-template-columns:1fr 1fr;}}
"""

steps = [
 ("Find your seven-month window", "Your Initial Enrollment Period is the three months before your birthday month, that month, and the three months after. Sign up in the three months before, and coverage starts the month you turn 65.", "/medicare-enrollment-calculator/", "Find my dates"),
 ("Sign up now, or safely wait", "Still working at an employer with 20 or more employees? You may be able to delay Part B without a penalty. COBRA and retiree coverage do not count, so check before you wait.", "/articles/working-past-65-medicare/", "Working past 65"),
 ("Choose your path", "Original Medicare with a Supplement and a drug plan, or a Medicare Advantage plan. Your first six months on Part B is your window to buy a Supplement without health questions.", "/articles/medicare-advantage-vs-medigap/", "Advantage or a Supplement"),
 ("Do not skip drug coverage", "Going without creditable drug coverage adds a Part D penalty for as long as you have Medicare, even if you take nothing today.", "/articles/medicare-late-enrollment-penalties/", "How the penalties work"),
]
STEPS = "".join(f'<div class="step"><span class="n">{i+1}</span><h3>{h}</h3><p>{p}</p><a href="{u}">{l} &rarr;</a></div>' for i, (h, p, u, l) in enumerate(steps))
ACC = "".join(f"<details><summary>{q}</summary><div class=\"a\">{a}</div></details>" for q, a in FAQ)

BODY = f"""{chrome_top}<main id="main">
<header class="hero"><div class="wrap">
  <span class="eyebrow">Turning 65 in Kentucky</span>
  <h1>Turning 65? Here is your Medicare plan, in order.</h1>
  <p class="sub">Four steps, in the order they come up. Read them here, or book a free review and a licensed advisor will walk through all four with you.</p>
  <div class="heroact"><a class="pill" href="/schedule/">Book a free review</a><span class="or">or call <a href="{TEL}">{PN}</a></span></div>
  <div class="human"><span class="duo"><img src="/assets/austin-tyler.jpg" alt="" width="48" height="48"><img src="/assets/andrew-horn.jpg" alt="" width="48" height="48"></span><span>Free, about 30 minutes, with no obligation.</span></div>
</div></header>

<section class="band t1" aria-labelledby="steps-h"><div class="wrap">
  <h2 id="steps-h">Your first year with Medicare, in four steps</h2><p class="lead">Each step links to the full guide when you want more.</p>
  <div class="steps">{STEPS}</div>
</div></section>

<section class="band" aria-labelledby="tools-h"><div class="wrap">
  <h2 id="tools-h">Two free tools</h2><p class="lead">Each takes about a minute.</p>
  <div class="grid c2">
    <a class="card" href="/medicare-enrollment-calculator/"><span class="glyph"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4M8 14h3v3H8z"/></svg></span><span class="cb"><span class="ch">Enrollment date calculator</span><span class="cp">Type your birthday. See your seven-month window and the day coverage starts.</span><span class="go">Find my dates &rarr;</span></span></a>
    <a class="card" href="/quiz-65/"><span class="glyph"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/></svg></span><span class="cb"><span class="ch">Am I ready for Medicare?</span><span class="cp">Ten true-or-false questions on the mistakes that cost people money at 65.</span><span class="go">Take the quiz &rarr;</span></span></a>
  </div>
</div></section>

<section class="band t2" aria-labelledby="guides-h"><div class="wrap">
  <h2 id="guides-h">Guides for turning 65 and retirement</h2><p class="lead">Plain English, checked against official sources.</p>
  {GUIDES}
</div></section>

<section class="band" aria-labelledby="team-h"><div class="wrap">
  <h2 id="team-h">Your advisors</h2>
  <p class="lead">Independent, licensed in Kentucky, with an office in Lexington. The carriers pay us, never you, and we work with several companies rather than one.</p>
  <div class="team">
    <a class="adv" href="/about/"><img src="/assets/austin-tyler.jpg" alt="Austin Tyler" width="104" height="104"><div><b>Austin Tyler</b><span>Founder and Partner</span><small>Licensed Medicare agent &middot; KY DOI #1187780 &middot; NPN 20234188</small></div></a>
    <a class="adv" href="/about/"><img src="/assets/andrew-horn.jpg" alt="Andrew Horn" width="104" height="104"><div><b>Andrew Horn</b><span>Partner</span><small>Tyler Insurance Group &middot; Lexington, Kentucky</small></div></a>
  </div>
</div></section>

<section class="band t1" aria-labelledby="faq-h"><div class="wrap">
  <h2 id="faq-h">Common questions</h2>
  <div class="acc">{ACC}</div>
</div></section>

<section class="final" aria-labelledby="final-h"><div class="wrap"><h2 id="final-h">Ready when you are.</h2><p>One conversation covers your dates, your doctors, your prescriptions and every plan you qualify for.</p>
  <a class="pill" href="/schedule/">Book a free review</a><span class="num">{PN}</span></div></section>
</main>

{chrome_bottom}
{NAV_JS}
"""

ld = {"@context": "https://schema.org", "@graph": [
  {"@type": "WebPage", "@id": URL, "url": URL, "name": TITLE, "description": DESC, "inLanguage": "en-US",
   "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": SITE + "/#business"}},
  {"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
    {"@type": "ListItem", "position": 2, "name": "Turning 65", "item": URL}]},
  {"@type": "FAQPage", "@id": URL + "#faq", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]}
OG = (f'<link rel="canonical" href="{URL}">\n<meta name="robots" content="index, follow, max-image-preview:large">\n'
      f'<meta property="og:type" content="website">\n<meta property="og:site_name" content="Bluegrass Medicare Help">\n'
      f'<meta property="og:title" content="{TITLE}">\n<meta property="og:description" content="{DESC}">\n'
      f'<meta property="og:url" content="{URL}">\n<meta property="og:image" content="{SITE}/assets/og-image.png">\n'
      f'<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="{TITLE}">\n'
      f'<meta name="twitter:description" content="{DESC}">\n<meta name="twitter:image" content="{SITE}/assets/og-image.png">\n'
      '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(",", ":")) + "</script>\n")
page = (head_top + f"<title>{TITLE}</title>\n<meta name=\"description\" content=\"{DESC}\">\n" + fonts_css +
        "<style>" + CSS + "</style>\n" + OG + "</head>\n<body>\n" + BODY + "</body>\n</html>\n")
page = page.replace('href="/turning-65/">Turning 65</a>', 'href="/turning-65/" aria-current="page">Turning 65</a>', 1)
open("turning-65/index.html", "w", encoding="utf-8").write(page)
print("wrote turning-65/index.html", len(page))
