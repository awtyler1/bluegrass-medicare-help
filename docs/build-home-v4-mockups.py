#!/usr/bin/env python3
"""Three advisor-first homepage variations (November 2026), built from the live homepage's own CSS,
chrome and sections so they look finished. Output: /mockups/home-v4/{a,b,c}/ plus an index. Not indexed.
Brief: the main action on the homepage is talking to a local advisor; resources stay, lower down;
no search box in the hero (most visitors do not know what to search, and most land on articles from Google)."""
import os, re

SRC = open("index.html", encoding="utf-8").read()
TEL, PN = "tel:18597858289", "(859) 785-8289"
CAL = ('<svg class="cta-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
       'stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/>'
       '<line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>')
PHONE = ('<svg class="cta-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 '
         '19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6'
         'l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>')

def section(name):
    m = re.search(rf'<section class="[^"]*" aria-labelledby="{name}-h">.*?</section>', SRC, re.S)
    assert m, name
    return m.group(0)
TOPICS, SEASON, TOOLS, COUNTY, REVIEWS, TEAM, FINAL = (section(n) for n in ("topics", "month", "tools", "county", "rev", "note", "final"))
NGUIDES = re.search(r"(\d+) plain-English guides", SRC).group(1)

def retitle(sec, old_h, new_h, old_lead=None, new_lead=None):
    assert old_h in sec, old_h
    sec = sec.replace(old_h, new_h)
    if old_lead:
        sec = re.sub(r'<p class="lead">.*?</p>', f'<p class="lead">{new_lead}</p>', sec, count=1, flags=re.S)
    return sec

FINAL_BOOK = ('<section class="final" aria-labelledby="final-h"><div class="wrap"><h2 id="final-h">Talk it through with a local advisor</h2>'
              '<p>Free, licensed, and based in Lexington. Phone, video or in person, at a time that suits you.</p>'
              f'<a class="pill" href="/schedule/">{CAL}Book a free review</a><span class="num">or call {PN}</span></div></section>')
TRUST = ('<div class="trust"><span><span class="star">★★★★★</span>5.0 on Google</span><span>Over 1,000 Kentuckians helped</span>'
         '<span>Independent Lexington firm</span></div>')
STEPS = f"""<section class="band t2" aria-labelledby="how-h"><div class="wrap">
  <h2 id="how-h">How a free review works</h2><p class="lead">About 30 minutes, by phone, video or at our Lexington office. You never pay us; the insurance companies pay licensed agents.</p>
  <ol class="steps">
    <li><b>Pick a time</b><span>Book online in a minute, or call and we will set it up with you.</span></li>
    <li><b>We do the comparing</b><span>We check your doctors, hospital and exact prescriptions against the plans in your county.</span></li>
    <li><b>You decide</b><span>We explain the options in plain English. No pressure to switch, and we will say so if your current plan is the right one.</span></li>
  </ol>
  <p class="stepcta"><a class="pill" href="/schedule/">{CAL}Book a free review</a></p>
</div></section>"""
SITUATIONS = [("I'm turning 65", "Your sign-up window and first choices", "/turning-65/"),
              ("I'm reviewing my plan for 2027", "What to check before December 7", "/articles/medicare-annual-enrollment-period/"),
              ("My plan is ending", "What a non-renewal letter means and your options", "/articles/medicare-advantage-plan-ending-kentucky/"),
              ("I'm still working at 65", "When you can wait on Part B, and when you can't", "/articles/working-past-65-medicare/"),
              ("Advantage or a Supplement?", "The real differences, side by side", "/articles/medicare-advantage-vs-medigap/"),
              ("I need help paying", "Programs that lower premiums and drug costs", "/articles/help-paying-for-medicare/")]
SIT_GRID = "".join(f'<a class="sit" href="{u}"><b>{t}</b><span>{d}</span><i aria-hidden="true">&rarr;</i></a>' for t, d, u in SITUATIONS)

EXTRA_CSS = """
.steps{list-style:none;counter-reset:s;display:grid;gap:16px;grid-template-columns:1fr;margin:6px 0 0;}
@media(min-width:800px){.steps{grid-template-columns:repeat(3,1fr);}}
.steps li{counter-increment:s;background:var(--surf);border-radius:20px;padding:24px 24px 22px;box-shadow:0 1px 2px rgba(27,40,54,.06),0 8px 24px rgba(27,40,54,.06);}
.steps li::before{content:counter(s);display:flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:var(--cta);color:#fff;font-family:var(--head);font-weight:800;font-size:19px;margin-bottom:12px;}
.steps b{display:block;font-family:var(--head);font-size:22px;margin-bottom:4px;} .steps span{color:var(--mute);font-size:17px;}
.stepcta{margin-top:26px;}
.callline{display:inline-flex;align-items:center;min-height:56px;font-weight:700;font-size:19px;color:var(--link);}
.ticks{list-style:none;display:flex;flex-wrap:wrap;gap:8px 20px;margin:20px 0 0;color:var(--ink);font-weight:600;font-size:17px;}
.ticks li::before{content:"";display:inline-block;width:9px;height:15px;border:solid #2f6844;border-width:0 3px 3px 0;transform:rotate(45deg);margin:0 10px 0 4px;position:relative;top:-2px;}
.sit{position:relative;display:block;background:var(--surf);border-radius:18px;padding:20px 52px 20px 22px;color:var(--ink);box-shadow:0 1px 2px rgba(27,40,54,.06),0 8px 24px rgba(27,40,54,.06);}
.sit b{display:block;font-family:var(--head);font-size:21px;line-height:1.2;} .sit span{display:block;color:var(--mute);font-size:16.5px;margin-top:4px;}
.sit i{position:absolute;right:20px;top:50%;transform:translateY(-50%);font-style:normal;font-weight:700;font-size:22px;color:var(--link);}
.sit:hover{box-shadow:0 2px 4px rgba(27,40,54,.08),0 14px 32px rgba(27,40,54,.10);}
.sits{display:grid;gap:14px;grid-template-columns:1fr;} @media(min-width:700px){.sits{grid-template-columns:1fr 1fr;}} @media(min-width:1000px){.sits{grid-template-columns:repeat(3,1fr);}}
.readlink{margin-top:22px;font-size:18px;} .readlink a{font-weight:700;}
/* A: advisor-first split hero */
.hva{display:grid;gap:30px;align-items:center;padding-block:44px 52px;}
@media(min-width:900px){.hva{grid-template-columns:1.1fr .9fr;gap:48px;padding-block:64px 70px;}}
.hva h1{font-size:40px;font-weight:800;} @media(min-width:900px){.hva h1{font-size:54px;}}
.hva .sub{font-size:20.5px;color:var(--mute);margin:16px 0 26px;max-width:560px;}
.hva .row{display:flex;flex-wrap:wrap;align-items:center;gap:6px 20px;}
.hva .trust{justify-content:flex-start;}
.duocard{background:var(--tint1);border-radius:26px;padding:22px;}
.duocard .ph{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.duocard figure{margin:0;} .duocard img{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;object-position:center 20%;border-radius:18px;}
.duocard figcaption{margin-top:10px;font-size:15.5px;color:var(--mute);line-height:1.35;} .duocard figcaption b{display:block;font-family:var(--head);font-size:19px;color:var(--ink);}
.duocard .office{margin-top:16px;padding-top:14px;border-top:1px solid var(--line);font-size:16px;color:var(--ink);}
/* B: local-first */
.hvb{text-align:center;padding-block:48px 56px;} @media(min-width:900px){.hvb{padding-block:70px 72px;}}
.hvb h1{font-size:40px;font-weight:800;max-width:820px;margin:0 auto;} @media(min-width:900px){.hvb h1{font-size:56px;}}
.hvb .sub{font-size:20.5px;color:var(--mute);margin:16px auto 28px;max-width:620px;}
.zipcard{max-width:560px;margin:0 auto;background:var(--surf);border:2px solid var(--line);border-radius:26px;padding:22px;box-shadow:0 14px 34px rgba(27,40,54,.08);text-align:left;}
.zipcard label{display:block;font-family:var(--head);font-weight:700;font-size:21px;margin-bottom:12px;}
.zipcard .zrow{display:flex;gap:10px;} .zipcard input{flex:1;min-width:0;font:inherit;font-size:22px;letter-spacing:2px;min-height:58px;border:2px solid var(--line);border-radius:14px;padding:0 16px;}
.zipcard input:focus{outline:none;border-color:var(--cta);}
.zipans{margin-top:16px;} .zipans p{font-size:18px;margin-bottom:14px;} .zipans .acts{display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center;}
.zipskip{margin-top:14px;font-size:16.5px;color:var(--mute);text-align:center;} .zipskip a{font-weight:700;}
.hvb .human{margin-top:22px;}
/* C: situation-first */
.hvc{padding-block:46px 30px;text-align:center;} @media(min-width:900px){.hvc{padding-block:66px 40px;}}
.hvc h1{font-size:40px;font-weight:800;max-width:820px;margin:0 auto;} @media(min-width:900px){.hvc h1{font-size:56px;}}
.hvc .sub{font-size:20.5px;color:var(--mute);margin:16px auto 26px;max-width:600px;}
.hvc .row{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:6px 20px;}
.hvc .human{margin-top:18px;}
.ways{display:grid;gap:12px;grid-template-columns:1fr;max-width:860px;margin:26px auto 0;text-align:left;}
@media(min-width:640px){.ways{grid-template-columns:1fr 1fr;max-width:640px;}}
.orway{margin:22px 0 0;color:var(--mute);font-size:16.5px;font-weight:600;}
.ways{margin-top:10px !important;}
.way{display:flex;gap:12px;align-items:center;background:var(--surf);border:2px solid var(--line);border-radius:16px;padding:14px 16px;color:var(--ink);font-weight:600;font-size:17px;}
.way b{display:block;font-family:var(--head);font-size:18.5px;} .way small{display:block;color:var(--mute);font-weight:500;font-size:15px;}
.way .glyph{width:44px;height:44px;} .way .glyph svg{width:22px;height:22px;}
"""

def page(title, hero, sections, sticky_book=False):
    out = SRC
    out = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex,nofollow">', out, count=1)
    out = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', out, count=1)
    out = re.sub(r'<link rel="canonical"[^>]*>\n?', '', out, count=1)
    out = out.replace("</style>", EXTRA_CSS + "</style>", 1)
    m = re.search(r'<main id="main">.*?</main>', out, re.S)
    out = out[:m.start()] + '<main id="main">\n' + hero + "\n\n" + "\n\n".join(sections) + "\n</main>" + out[m.end():]
    if sticky_book:
        out = re.sub(r'<div class="sticky"><a href="tel:18597858289">.*?</a></div>',
                     f'<div class="sticky"><a href="/schedule/">{CAL}Book a free review</a></div>', out, count=1, flags=re.S)
    return out

# ---------- A. Advisor-first
HERO_A = f"""<header class="hero-a"><div class="wrap hva">
  <div>
    <span class="eyebrow">Free Medicare help for all of Kentucky</span>
    <h1>Talk to a local Medicare advisor before you choose.</h1>
    <p class="sub">A free review with a licensed advisor from our Lexington office. We check your doctors and prescriptions against the plans in your county and explain your options in plain English.</p>
    <div class="row"><a class="pill" href="/schedule/">{CAL}Book a free review</a><a class="callline" href="{TEL}">or call {PN}</a></div>
    <ul class="ticks"><li>Always free</li><li>Phone, video or in person</li><li>No pressure to switch</li></ul>
    {TRUST.replace('class="trust"', 'class="trust" style="justify-content:flex-start"')}
  </div>
  <div class="duocard">
    <div class="ph">
      <figure><img src="/assets/austin-tyler.jpg" alt="Austin Tyler" width="600" height="750"><figcaption><b>Austin Tyler, MBA</b>Licensed Medicare Advisor</figcaption></figure>
      <figure><img src="/assets/andrew-horn.jpg" alt="Andrew Horn" width="768" height="960"><figcaption><b>Andrew Horn, MHA</b>Licensed Medicare Advisor</figcaption></figure>
    </div>
    <p class="office">Your call is answered by one of us, not a call center. Office: 1029 Monarch Street, Lexington.</p>
  </div>
</div></header>"""
TOPICS_A = retitle(TOPICS, '>Start with a topic<', '>Prefer to read first?<', True,
                   'Free plain-English guides, written by our advisors and checked against official sources. <a href="/articles/">See all guides &rarr;</a>')
A = page("Homepage mockup A: Advisor first", HERO_A, [STEPS, REVIEWS, TOPICS_A, COUNTY, FINAL_BOOK], sticky_book=True)

# ---------- B. Local-first (ZIP check, then book)
HERO_B = f"""<header class="hero-b"><div class="wrap hvb">
  <span class="eyebrow">Licensed Medicare advisors in Kentucky</span>
  <h1>Medicare help from advisors who live here.</h1>
  <p class="sub">Free reviews by phone, video or at our Lexington office, for anyone in Kentucky.</p>
  <form class="zipcard" id="zipform" novalidate>
    <label for="zip">Is help available where you live?</label>
    <div class="zrow"><input id="zip" name="zip" inputmode="numeric" autocomplete="postal-code" maxlength="5" placeholder="Your ZIP code" aria-describedby="zipans"><button class="pill" type="submit">Check</button></div>
    <div class="zipans" id="zipans" aria-live="polite" hidden></div>
  </form>
  <p class="zipskip">Already know you want to talk? <a href="/schedule/">Book a free review</a> or call <a href="{TEL}">{PN}</a></p>
  {TRUST}
</div></header>
<script>
(function(){{
  var f=document.getElementById('zipform'), z=document.getElementById('zip'), a=document.getElementById('zipans');
  f.addEventListener('submit',function(e){{
    e.preventDefault(); var v=(z.value||'').replace(/\\D/g,'');
    if(v.length!==5){{ a.hidden=false; a.innerHTML='<p>Please enter a 5-digit ZIP code.</p>'; z.focus(); return; }}
    var p=parseInt(v.slice(0,3),10);
    if(p>=400&&p<=427){{
      a.innerHTML='<p><b>Yes, we help people in your area.</b> Your review can be by phone or video from home, or at our Lexington office.</p>'
        +'<div class="acts"><a class="pill" href="/schedule/">{CAL}Book a free review</a><a class="callline" href="{TEL}">or call {PN}</a></div>';
    }} else {{
      a.innerHTML='<p>That ZIP is outside Kentucky, where we are licensed. For free help in your state, call 1-800-MEDICARE (1-800-633-4227) or your State Health Insurance Assistance Program (SHIP).</p>';
    }}
    a.hidden=false;
  }});
}})();
</script>"""
SIT_B = f"""<section class="band t1" aria-labelledby="sit-h"><div class="wrap">
  <h2 id="sit-h">Not sure what to ask? Start with your situation.</h2><p class="lead">Short guides written by our advisors. Each one ends with a quick way to talk to us.</p>
  <div class="sits">{SIT_GRID}</div>
  <p class="readlink">Or browse <a href="/articles/">all {NGUIDES} guides in the Learning Center &rarr;</a></p>
</div></section>"""
COUNTY_B = retitle(COUNTY, '>Medicare help in your county<', '>What is different in your county<')
B = page("Homepage mockup B: Local first", HERO_B, [SIT_B, STEPS, COUNTY_B, REVIEWS, TEAM, FINAL_BOOK], sticky_book=True)

# ---------- C. Situation-first
def way(glyph, title, small, href):
    return f'<a class="way" href="{href}"><span class="glyph">{glyph}</span><span><b>{title}</b><small>{small}</small></span></a>'
GLY_CAL = CAL.replace('class="cta-ico" ', '')
GLY_PH = PHONE.replace('class="cta-ico" ', '')
GLY_BACK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>')
HERO_C = f"""<header class="hero-c"><div class="wrap hvc">
  <span class="eyebrow">Free Medicare help for all of Kentucky</span>
  <h1>Talk to a licensed Medicare advisor. It's free.</h1>
  <p class="sub">Independent advisors from Lexington. We compare plans from several insurers for your doctors and prescriptions, and you decide.</p>
  <div class="row"><a class="pill" href="/schedule/">{CAL}Book a free review</a></div>
  <p class="orway">Or reach us another way:</p>
  <div class="ways">
    {way(GLY_PH, 'Call now', PN + ', a licensed advisor answers', TEL)}
    {way(GLY_BACK, 'Have us call you', 'Leave your number', '/schedule/#cback')}
  </div>
  <div class="human"><span class="duo"><img src="/assets/austin-tyler.jpg" alt="" width="48" height="48"><img src="/assets/andrew-horn.jpg" alt="" width="48" height="48"></span><span>You talk to Austin or Andrew, not a call center.</span></div>
  {TRUST}
</div></header>"""
SIT_C = f"""<section class="band t1" aria-labelledby="sit-h"><div class="wrap">
  <h2 id="sit-h">What brings you here?</h2><p class="lead">Pick the one that fits. Each guide is short, and you can talk to us at any point.</p>
  <div class="sits">{SIT_GRID}</div>
</div></section>"""
TOPICS_C = retitle(TOPICS, '>Start with a topic<', '>Or browse by topic<')
C = page("Homepage mockup C: Situation first", HERO_C, [SIT_C, REVIEWS, TEAM, TOPICS_C, SEASON, FINAL_BOOK])

for slug, html in (("a", A), ("b", B), ("c", C)):
    os.makedirs(f"mockups/home-v4/{slug}", exist_ok=True)
    open(f"mockups/home-v4/{slug}/index.html", "w", encoding="utf-8").write(html)

INDEX = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>Homepage mockups, November 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@700;800&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>body{font-family:'Source Sans 3',-apple-system,sans-serif;background:#f5f8fb;color:#1b2836;margin:0;padding:40px 18px;font-size:18px;line-height:1.5}
.w{max-width:760px;margin:0 auto}h1{font-family:Figtree,sans-serif;font-weight:800;font-size:34px;line-height:1.15}
a.c{display:block;background:#fff;border:1px solid #e3e8ee;border-radius:18px;padding:20px 22px;margin:14px 0;color:#1b2836;text-decoration:none}
a.c b{display:block;font-size:22px;font-family:Figtree,sans-serif}a.c span{color:#4a5563}</style></head><body><div class="w">
<h1>Homepage mockups: advisor first</h1>
<p>Three ways to make "talk to a local advisor" the main action on the homepage, with the guides still close at hand. Built from the live homepage's styles. Not indexed.</p>
<a class="c" href="/mockups/home-v4/a/"><b>A. Advisor first</b><span>Split hero with Austin and Andrew, one "Book a free review" button, how a review works in three steps, reviews, then "Prefer to read first?"</span></a>
<a class="c" href="/mockups/home-v4/b/"><b>B. Local first</b><span>"Is help available where you live?" ZIP check that answers yes for Kentucky and leads to booking, then "Not sure what to ask?" situations, steps, county, advisors.</span></a>
<a class="c" href="/mockups/home-v4/c/"><b>C. Situation first</b><span>One booking button plus two other ways to reach us (call now, or have us call you), then "What brings you here?" situation tiles for people who do not know what to search.</span></a>
</div></body></html>
"""
open("mockups/home-v4/index.html", "w", encoding="utf-8").write(INDEX)
print("wrote mockups/home-v4/ a, b, c and index")
