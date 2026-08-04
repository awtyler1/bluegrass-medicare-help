"""Generate 4 design concepts for the /schedule/ booking landing page.
Mockups only (noindex). The calendar area is a placeholder that matches the real
GoHighLevel widget's footprint so the layouts read honestly at screenshot time."""
import os

NAV = """<div class="ustrip"><div class="wrap">
<span>📍 <strong>Lexington, Kentucky</strong> &nbsp;·&nbsp; Serving Fayette &amp; surrounding counties</span>
<span class="rate"><span class="stars">★★★★★</span> 5.0 on Google</span>
</div></div>
<nav class="nav"><div class="wrap">
<a class="brand" href="/"><img class="brand-logo" src="/assets/logo.png" alt="Bluegrass Medicare Help" height="46"></a>
<div class="navlinks">
<a href="/turning-65/">Turning 65?</a>
<a href="/articles/">Learning Center</a>
<a href="/kentucky/">Kentucky</a>
<a href="/reviews/">Reviews</a>
<a href="/schedule/" class="active">Schedule</a>
<a href="/about/">About</a>
</div>
<a class="navcta" href="tel:18596186443">Call</a>
</div></nav>"""

FOOT = """<footer class="foot"><div class="wrap">
<div class="fnm">Tyler Insurance Group</div>
1029 Monarch Street, Suite 110, Lexington, KY 40513<br>
<a href="tel:8596186443">(859) 618-6443</a>
<div class="disc">We respect your privacy. This is a solicitation for insurance. Tyler Insurance Group is not connected with or endorsed by the United States government or the federal Medicare program. We do not offer every plan available in your area. Currently we represent 6 organizations which offer 158 products in your area. Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance Program (SHIP) to get information on all of your options.</div>
</div></footer>"""

# Calendar placeholder that mimics the real widget footprint
def cal(h=560):
    return f"""<div class="calbox" style="min-height:{h}px">
  <div class="calhead"><b>Pick a time that works for you</b><span>Free · 20 minutes · phone or video</span></div>
  <div class="calgrid">
    <div class="calmonth">August 2026 <span>&lsaquo; &rsaquo;</span></div>
    <div class="caldays"><i>S</i><i>M</i><i>T</i><i>W</i><i>T</i><i>F</i><i>S</i></div>
    <div class="calnums">{''.join(f'<i class="{"on" if d in (5,6,7,12,13,14,19,20,21) else ""}{" sel" if d==13 else ""}">{d}</i>' for d in range(1,29))}</div>
    <div class="calslots"><b>Thursday, August 13</b>
      <span>9:00 AM</span><span>10:30 AM</span><span>1:00 PM</span><span>2:30 PM</span><span>4:00 PM</span>
    </div>
  </div>
  <p class="calnote">Booking widget loads here</p>
</div>"""

BASE_CSS = """
:root{--cream:#f4efe7;--cream2:#faf6ef;--warm:#efe6d6;--ink:#2a2620;--dark:#1f1d1a;--coral:#d05528;--coral-d:#b3431d;--mute:#5f594f;--faint:#6f6a60;--line:#e2d9c8;--white:#fff;--green:#3a7d52;--serif:'Fraunces',Georgia,serif;--sans:'Source Sans 3',-apple-system,sans-serif;}
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:var(--sans);color:var(--ink);background:var(--cream);line-height:1.6;}
img{max-width:100%;display:block;} a{color:var(--coral-d);text-decoration:none;}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px;}
/* calendar placeholder */
.calbox{background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px;box-shadow:0 18px 40px rgba(80,60,30,.10);}
.calhead{border-bottom:1px solid var(--line);padding-bottom:14px;margin-bottom:16px;}
.calhead b{display:block;font-family:var(--serif);font-size:21px;}
.calhead span{font-size:14.5px;color:var(--mute);}
.calmonth{font-weight:700;font-size:16px;margin-bottom:10px;display:flex;justify-content:space-between;}
.calmonth span{color:var(--faint);letter-spacing:6px;}
.caldays{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-bottom:6px;}
.caldays i{font-style:normal;text-align:center;font-size:12px;color:var(--faint);font-weight:700;}
.calnums{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-bottom:18px;}
.calnums i{font-style:normal;text-align:center;font-size:14px;padding:8px 0;border-radius:8px;color:#b9b1a4;}
.calnums i.on{color:var(--ink);background:var(--cream2);border:1px solid var(--line);font-weight:600;}
.calnums i.sel{background:var(--coral);color:#fff;border-color:var(--coral);}
.calslots b{display:block;font-size:14.5px;margin-bottom:8px;}
.calslots span{display:inline-block;border:1.5px solid var(--coral);color:var(--coral-d);font-weight:700;font-size:14.5px;padding:9px 14px;border-radius:9px;margin:0 6px 6px 0;}
.calnote{margin-top:14px;font-size:12px;color:#c2b9ab;text-align:center;font-style:italic;}
/* chrome */
.ustrip{background:var(--dark);color:#cfc7bb;font-size:13px;padding:7px 0;}
.ustrip .wrap{display:flex;justify-content:space-between;}
.ustrip .stars{color:#e9b949;}
.nav{background:#fff;border-bottom:1px solid var(--line);position:sticky;top:0;z-index:30;}
.nav .wrap{display:flex;align-items:center;gap:26px;padding-top:12px;padding-bottom:12px;}
.brand-logo{height:42px;width:auto;}
.navlinks{display:flex;gap:22px;margin-left:auto;}
.navlinks a{color:var(--ink);font-weight:600;font-size:15px;}
.navlinks a.active{color:var(--coral-d);}
.navcta{background:var(--green);color:#fff;font-weight:700;padding:10px 18px;border-radius:10px;font-size:14.5px;}
.foot{background:var(--dark);color:#9a948c;padding:28px 0 34px;font-size:13px;margin-top:56px;}
.foot .fnm{color:var(--cream);font-weight:600;font-size:15px;font-family:var(--serif);}
.foot a{color:#bdb6ac;}
.foot .disc{margin-top:12px;padding-top:12px;border-top:1px solid #333;color:#918b80;font-size:11.5px;}
.mocklabel{position:fixed;left:0;top:0;background:var(--coral);color:#fff;font-weight:700;font-size:12px;padding:6px 14px;z-index:99;letter-spacing:.5px;}
"""

def page(name, label, css, body):
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{label} | Schedule page concept</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,500&family=Source+Sans+3:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{BASE_CSS}{css}</style></head><body>
<div class="mocklabel">{label}</div>
{NAV}
{body}
{FOOT}
</body></html>"""

BULLETS = [
 ("A plan built around your doctors","We check that the doctors and hospital you already use are in-network before you enroll, not after."),
 ("Your prescriptions priced, drug by drug","We run your exact medication list through each plan so the cheapest premium doesn't hide the biggest drug bill."),
 ("Every option on the table","Advantage, Supplement, and drug plans compared side by side, in plain English, with the trade-offs said out loud."),
 ("One person to call, all year","Not a call center. A local agent in Lexington who answers the phone in March when a claim goes sideways."),
]

# ---------------------------------------------------------------- A: Split Card
A_CSS = """
.hero{padding:56px 0 20px;}
.hgrid{display:grid;grid-template-columns:1.05fr .95fr;gap:52px;align-items:start;}
.kicker{display:inline-block;font-size:12px;font-weight:800;letter-spacing:1.4px;text-transform:uppercase;color:var(--coral-d);background:rgba(208,85,40,.1);padding:6px 12px;border-radius:20px;margin-bottom:18px;}
h1{font-family:var(--serif);font-weight:500;font-size:47px;line-height:1.08;letter-spacing:-1px;margin-bottom:16px;}
.sub{font-size:19.5px;color:var(--mute);margin-bottom:28px;max-width:520px;}
.who{display:flex;gap:16px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin-bottom:26px;}
.who img{width:76px;height:76px;border-radius:50%;object-fit:cover;object-position:center top;border:3px solid var(--coral);}
.who b{font-family:var(--serif);font-size:19px;display:block;}
.who span{font-size:14.5px;color:var(--mute);}
.vlist{list-style:none;}
.vlist li{position:relative;padding-left:38px;margin-bottom:20px;}
.vlist li::before{content:"✓";position:absolute;left:0;top:2px;width:26px;height:26px;border-radius:50%;background:var(--green);color:#fff;font-size:14px;font-weight:800;display:flex;align-items:center;justify-content:center;}
.vlist b{display:block;font-family:var(--serif);font-size:18.5px;margin-bottom:2px;}
.vlist span{font-size:16px;color:var(--mute);}
.callalt{margin-top:26px;background:var(--warm);border-left:4px solid var(--coral);border-radius:10px;padding:16px 18px;font-size:16.5px;}
.callalt b{font-family:var(--serif);}
.strip{background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-top:44px;padding:34px 0;}
.strip .wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;}
.strip h3{font-family:var(--serif);font-size:19px;margin-bottom:6px;}
.strip p{font-size:15.5px;color:var(--mute);}
.strip .n{width:30px;height:30px;border-radius:50%;background:var(--coral);color:#fff;font-weight:700;display:flex;align-items:center;justify-content:center;margin-bottom:10px;font-size:15px;}
@media(max-width:900px){.hgrid{grid-template-columns:1fr;gap:34px;}h1{font-size:34px;}.strip .wrap{grid-template-columns:1fr;}}
"""
A_BODY = f"""<section class="hero"><div class="wrap"><div class="hgrid">
<div>
<span class="kicker">No cost · No pressure · No obligation</span>
<h1>Talk to a local Medicare agent, at a time you pick.</h1>
<p class="sub">Twenty minutes on the phone with someone who lives here, knows the Lexington hospital networks, and will tell you honestly if the plan you have is already the right one.</p>
<div class="who"><img src="/assets/austin-tyler.jpg" alt="Austin Tyler">
<div><b>Austin Tyler</b><span>Licensed Kentucky Medicare agent · Tyler Insurance Group · Lexington</span></div></div>
<ul class="vlist">{''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t,d in BULLETS)}</ul>
<div class="callalt"><b>Rather just call?</b> Dial <a href="tel:18596186443">(859) 618-6443</a> and you will get a real person, usually me.</div>
</div>
<div>{cal()}</div>
</div></div></section>
<section class="strip"><div class="wrap">
<div><div class="n">1</div><h3>You pick a time</h3><p>Choose any open slot. You will get a confirmation email and a reminder before we talk.</p></div>
<div><div class="n">2</div><h3>We talk for 20 minutes</h3><p>Your doctors, your prescriptions, your budget. Bring questions; there are no dumb ones.</p></div>
<div><div class="n">3</div><h3>You decide, or you don't</h3><p>If what you have already fits, I will say so and you will hear from me again next fall.</p></div>
</div></section>"""

# ---------------------------------------------------------------- B: Trust Wall
B_CSS = """
.hero{padding:44px 0 18px;}
.hgrid{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:start;}
h1{font-family:var(--serif);font-weight:500;font-size:42px;line-height:1.1;letter-spacing:-.8px;margin-bottom:14px;}
.sub{font-size:18.5px;color:var(--mute);margin-bottom:26px;}
.proofcard{background:#fff;border:1px solid var(--line);border-radius:16px;padding:24px;margin-bottom:22px;box-shadow:0 10px 26px rgba(80,60,30,.06);}
.pchead{display:flex;gap:16px;align-items:center;padding-bottom:18px;border-bottom:1px solid var(--line);margin-bottom:18px;}
.pchead img{width:88px;height:88px;border-radius:14px;object-fit:cover;object-position:center top;}
.pchead b{font-family:var(--serif);font-size:21px;display:block;}
.pchead .cred{font-size:14.5px;color:var(--mute);display:block;margin-top:2px;}
.pchead .stars{color:#e9b949;font-size:15px;letter-spacing:2px;margin-top:6px;display:block;}
.pchead .stars small{color:var(--mute);letter-spacing:0;font-size:13.5px;}
.quote{border-left:3px solid var(--warm);padding-left:16px;margin-bottom:16px;}
.quote p{font-size:16px;font-style:italic;color:#4a443b;margin-bottom:5px;}
.quote span{font-size:13.5px;color:var(--faint);font-weight:600;}
.badges{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px;}
.badges i{font-style:normal;font-size:13px;font-weight:700;background:var(--cream2);border:1px solid var(--line);border-radius:20px;padding:6px 12px;color:var(--mute);}
.vlist{list-style:none;background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px 24px;}
.vlist>b{font-family:var(--serif);font-size:18px;display:block;margin-bottom:14px;}
.vlist li{position:relative;padding-left:30px;margin-bottom:13px;font-size:16.5px;}
.vlist li::before{content:"✓";position:absolute;left:0;color:var(--green);font-weight:800;}
.stickycal{position:sticky;top:88px;}
@media(max-width:900px){.hgrid{grid-template-columns:1fr;gap:30px;}h1{font-size:32px;}.stickycal{position:static;}}
"""
B_BODY = f"""<section class="hero"><div class="wrap"><div class="hgrid">
<div>
<h1>Book 20 minutes with the agent your neighbors already trust.</h1>
<p class="sub">Free, no pressure, and no obligation to change a thing.</p>
<div class="proofcard">
<div class="pchead"><img src="/assets/austin-tyler.jpg" alt="Austin Tyler">
<div><b>Austin Tyler</b><span class="cred">Licensed Kentucky Medicare agent · Lexington</span>
<span class="stars">★★★★★ <small>5.0 on Google</small></span></div></div>
<div class="quote"><p>&ldquo;Austin was extremely knowledgeable and explained everything in great detail so I could easily understand. I know that my insurance needs are in good hands!&rdquo;</p><span>Doug S. · Google review</span></div>
<div class="quote"><p>&ldquo;Austin is such a pleasant man to talk to. He cares about his clients and finds ways to get what we need.&rdquo;</p><span>Robert E. · Google review</span></div>
<div class="badges"><i>Independent, not captive</i><i>6 carriers represented</i><i>Lexington based</i><i>No fee to you, ever</i></div>
</div>
<ul class="vlist"><b>What you get out of the call</b>
{''.join(f'<li>{t}</li>' for t,_ in BULLETS)}
<li>An honest answer, even when it is "keep what you have"</li>
</ul>
</div>
<div class="stickycal">{cal()}</div>
</div></div></section>"""

# ---------------------------------------------------------------- C: Editorial Dark Band
C_CSS = """
.band{background:var(--dark);color:#f0e9dd;padding:60px 0 150px;}
.band h1{font-family:var(--serif);font-weight:500;font-size:52px;line-height:1.05;letter-spacing:-1.2px;margin-bottom:18px;max-width:640px;}
.band h1 em{font-style:italic;color:#e9b949;}
.band .sub{font-size:20px;color:#bdb4a6;max-width:560px;margin-bottom:30px;}
.bandrow{display:flex;gap:20px;align-items:center;}
.bandrow img{width:82px;height:82px;border-radius:50%;object-fit:cover;object-position:center top;border:3px solid #e9b949;}
.bandrow b{font-family:var(--serif);font-size:20px;color:#fff;display:block;}
.bandrow span{font-size:15px;color:#a49b8d;}
.lift{margin-top:-120px;padding-bottom:20px;}
.lgrid{display:grid;grid-template-columns:1fr 1.02fr;gap:40px;align-items:start;}
.valcard{background:#fff;border:1px solid var(--line);border-radius:18px;padding:30px;box-shadow:0 18px 40px rgba(80,60,30,.10);}
.valcard h2{font-family:var(--serif);font-size:24px;margin-bottom:20px;}
.valcard li{list-style:none;position:relative;padding-left:36px;margin-bottom:20px;}
.valcard li::before{content:"";position:absolute;left:0;top:5px;width:22px;height:22px;border-radius:6px;background:var(--warm);border:1.5px solid var(--coral);}
.valcard li::after{content:"✓";position:absolute;left:5px;top:5px;color:var(--coral-d);font-weight:800;font-size:13px;}
.valcard b{display:block;font-size:17.5px;font-family:var(--serif);}
.valcard span{font-size:15.5px;color:var(--mute);}
.mini{margin-top:24px;padding-top:20px;border-top:1px solid var(--line);font-size:16px;color:var(--mute);}
.mini a{font-weight:700;}
@media(max-width:900px){.band h1{font-size:34px;}.lgrid{grid-template-columns:1fr;gap:26px;}.lift{margin-top:-110px;}}
"""
C_BODY = f"""<section class="band"><div class="wrap">
<h1>The Medicare decision is <em>yours</em>. The homework is mine.</h1>
<p class="sub">Pick a time below. Twenty minutes, no cost, no pressure, and no obligation to change anything.</p>
<div class="bandrow"><img src="/assets/austin-tyler.jpg" alt="Austin Tyler">
<div><b>Austin Tyler</b><span>Licensed Kentucky Medicare agent · Tyler Insurance Group · Lexington</span></div></div>
</div></section>
<section class="lift"><div class="wrap"><div class="lgrid">
<div class="valcard"><h2>What the 20 minutes buys you</h2><ul>
{''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t,d in BULLETS)}
</ul>
<p class="mini">Prefer the phone? Call <a href="tel:18596186443">(859) 618-6443</a>. You will get a real person, usually me, not a menu.</p>
</div>
<div>{cal()}</div>
</div></div></section>"""

# ---------------------------------------------------------------- D: Kitchen Table Letter
D_CSS = """
.hero{padding:50px 0 24px;}
.hgrid{display:grid;grid-template-columns:1fr .95fr;gap:50px;align-items:start;}
h1{font-family:var(--serif);font-weight:500;font-size:44px;line-height:1.08;letter-spacing:-.9px;margin-bottom:22px;}
.letter{background:var(--cream2);border:1px solid var(--line);border-left:5px solid var(--coral);border-radius:14px;padding:26px 28px;margin-bottom:26px;}
.letter p{font-size:17.5px;color:#413b32;margin-bottom:14px;}
.letter p:last-of-type{margin-bottom:18px;}
.sig{display:flex;gap:14px;align-items:center;padding-top:16px;border-top:1px solid var(--line);}
.sig img{width:64px;height:64px;border-radius:50%;object-fit:cover;object-position:center top;border:2px solid var(--coral);}
.sig b{font-family:var(--serif);font-size:20px;font-style:italic;display:block;}
.sig span{font-size:14px;color:var(--mute);}
.steps{list-style:none;counter-reset:s;}
.steps li{counter-increment:s;position:relative;padding-left:52px;margin-bottom:22px;}
.steps li::before{content:counter(s);position:absolute;left:0;top:-2px;width:36px;height:36px;border-radius:50%;background:#fff;border:2px solid var(--coral);color:var(--coral-d);font-family:var(--serif);font-weight:700;font-size:18px;display:flex;align-items:center;justify-content:center;}
.steps b{display:block;font-family:var(--serif);font-size:18.5px;margin-bottom:3px;}
.steps span{font-size:16px;color:var(--mute);}
.stitle{font-family:var(--serif);font-size:23px;margin-bottom:20px;}
.reassure{margin-top:26px;display:flex;flex-wrap:wrap;gap:10px;}
.reassure i{font-style:normal;font-size:14px;font-weight:700;color:var(--green);background:rgba(58,125,82,.09);border-radius:20px;padding:8px 14px;}
@media(max-width:900px){.hgrid{grid-template-columns:1fr;gap:32px;}h1{font-size:33px;}}
"""
D_BODY = f"""<section class="hero"><div class="wrap"><div class="hgrid">
<div>
<h1>Let's sit down and sort your Medicare out.</h1>
<div class="letter">
<p>Medicare is not complicated because you are missing something. It is complicated because it was built that way, and because most of the people explaining it are paid to steer you.</p>
<p>Here is my offer: give me twenty minutes. I will look at your doctors, your prescriptions, and what you actually pay, and I will tell you straight whether you are in the right plan. If you are, I will say so, and you will not hear a pitch.</p>
<p>That is the whole thing. Pick a time on the calendar and I will call you.</p>
<div class="sig"><img src="/assets/austin-tyler.jpg" alt="Austin Tyler">
<div><b>Austin Tyler</b><span>Licensed Kentucky Medicare agent · Lexington</span></div></div>
</div>
<h2 class="stitle">What happens on the call</h2>
<ul class="steps">
<li><b>You tell me who you see</b><span>Your doctors and your hospital. I check them against every plan available in your county.</span></li>
<li><b>We price your prescriptions</b><span>Drug by drug, plan by plan, so the cheap premium doesn't hide an expensive year.</span></li>
<li><b>I lay out the options</b><span>Advantage, Supplement, drug plans, side by side in plain English, trade-offs included.</span></li>
<li><b>You decide, on your time</b><span>No same-day pressure. Sleep on it, talk to your spouse, call me back whenever.</span></li>
</ul>
<div class="reassure"><i>✓ Free, always</i><i>✓ No obligation</i><i>✓ Independent agent</i><i>✓ Local, not a call center</i></div>
</div>
<div>{cal()}</div>
</div></div></section>"""

here=os.path.dirname(os.path.abspath(__file__))
for fn,label,css,body in [
 ("concept-a-split-card.html","CONCEPT A · Split Card",A_CSS,A_BODY),
 ("concept-b-trust-wall.html","CONCEPT B · Trust Wall",B_CSS,B_BODY),
 ("concept-c-editorial.html","CONCEPT C · Editorial Band",C_CSS,C_BODY),
 ("concept-d-letter.html","CONCEPT D · Kitchen Table Letter",D_CSS,D_BODY),
]:
    open(os.path.join(here,fn),"w",encoding="utf-8").write(page(fn,label,css,body))
    print("wrote",fn)
