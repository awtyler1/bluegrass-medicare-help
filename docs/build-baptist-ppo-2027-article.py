#!/usr/bin/env python3
"""Build /articles/baptist-health-out-of-network-medicare-advantage-ppo-2027/ from the current article chrome.
Facts and sources: docs/dossiers/baptist-health-out-of-network-ppo-2027.md."""
import json, re, os, html as H

SRC = "articles/90-dollar-medicare-payment-kentucky/index.html"
OLD_URL = "https://www.bluegrassmedicarehelp.com/articles/90-dollar-medicare-payment-kentucky/"
SLUG = "baptist-health-out-of-network-medicare-advantage-ppo-2027"
URL = f"https://www.bluegrassmedicarehelp.com/articles/{SLUG}/"
TITLE = "Baptist Health Letter: Out-of-Network Medicare Advantage PPOs in 2027"
H1 = "Got the Baptist Health Letter? What It Means for Medicare Advantage PPO Members in 2027"
DESC = ("Baptist Health will not schedule appointments in 2027 for patients in out-of-network Medicare Advantage plans, "
        "including PPOs. Which plans are affected, what still works, and your options before December 7.")
CRUMB_LABEL = "Baptist Health and PPO Plans, 2027"
DATE, DATE_LONG = "2026-11-17", "November 17, 2026"
OG = f"https://www.bluegrassmedicarehelp.com/assets/og/{SLUG}.png"
OG_ALT = ("Baptist Health and Medicare Advantage PPO plans in 2027: no appointments for out-of-network plans starting "
          "January 1, 2027. Switch by December 7 or know your options.")

src = open(SRC, encoding="utf-8").read()
out = src
old_title = re.search(r"<title>(.*?)</title>", out).group(1)
old_desc = re.search(r'<meta name="description" content="([^"]*)"', out).group(1)
out = out.replace(old_title, TITLE).replace(old_desc, DESC).replace(OLD_URL, URL)
out = re.sub(r'https://www\.bluegrassmedicarehelp\.com/assets/(?:og-image\.png|og/[a-z0-9-]+\.png)', OG, out)
out = re.sub(r'\n<meta property="og:image:alt"[^>]*>|\n<meta name="twitter:image:alt"[^>]*>', '', out)
out = out.replace('<meta property="og:image:height" content="630">',
                  f'<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="{OG_ALT}">', 1)
out = out.replace(f'<meta name="twitter:image" content="{OG}">',
                  f'<meta name="twitter:image" content="{OG}">\n<meta name="twitter:image:alt" content="{OG_ALT}">', 1)
out = out.replace("</style>", """
.letter{background:#fff;border:1px solid var(--line);border-left:5px solid var(--ink);border-radius:12px;padding:20px 22px;margin:6px 0 10px;font-size:18px;line-height:1.55;color:var(--ink);}
.letter p{margin:0 0 10px;} .letter p:last-child{margin-bottom:0;}
.nettbl td small{display:block;font-weight:500;color:var(--mute);font-size:14.5px;white-space:normal;margin-top:2px;}
.letter .src{font-size:14.5px;color:var(--mute);}
</style>""", 1)

BODY = r"""
    <p class="updated">Updated __DATE_LONG__. Based on Baptist Health's October 2026 letter to patients and its published Medicare Advantage network list. Baptist's list can change before January 1, so confirm your exact plan at BaptistHealth.com/MedicareAdvantage before you decide. <strong>The Annual Enrollment Period ends December 7.</strong></p>
    <p>If you are on a Medicare Advantage PPO and have been seen at Baptist Health in the past year, you may have received a letter this fall titled <em>Important Information About Your Access to Medical Care from Baptist Health</em>. It is short, and it is easy to set aside. Please don't. It means that starting January 1, 2027, the Baptist doctors and hospitals you may have used for years will stop scheduling you, unless you change plans or qualify for an exception.</p>

    <div class="ans">
      <p><strong>The short version:</strong></p>
      <ul>
        <li><strong>What changed:</strong> Baptist Health will not schedule appointments on or after <strong>January 1, 2027</strong> for patients in Medicare Advantage plans that are out of its network, and the letter says that explicitly includes <strong>PPO plans</strong>.</li>
        <li><strong>Why it hits PPO members:</strong> a PPO pays for out-of-network care, so many people kept using Baptist and paid a little more. That only worked because Baptist agreed to see them. It is no longer agreeing.</li>
        <li><strong>Which plans:</strong> at the company level, Baptist lists <strong>UnitedHealthcare, Wellcare, Essence and Devoted</strong> Medicare Advantage as out of network, and <strong>Humana, Aetna and Anthem</strong> as in network. If you got the letter, Baptist's records show your plan is out.</li>
        <li><strong>What still works:</strong> emergencies are always treated and covered. Patients in active treatment for a serious or complex condition can ask for an exception.</li>
        <li><strong>Your best window is now:</strong> switch to a plan that includes Baptist by <strong>December 7</strong>, or decide to keep your plan and use other hospitals. The January to March window is a backup.</li>
      </ul>
    </div>

    <h2>What the letter actually says</h2>
    <p>Here is the key paragraph, word for word:</p>
    <div class="letter">
      <p>"Baptist Health is not scheduling appointments for dates of service beginning Jan. 1, 2027, for patients who are enrolled in out-of-network Medicare Advantage plans, which include out-of-network Medicare Advantage PPO plans. Exceptions will be made for patients who are undergoing an active course of treatment for a serious or complex medical condition."</p>
      <p class="src">Baptist Health patient letter, October 2026</p>
    </div>
    <p>The letter applies to Baptist Health hospitals, physicians, advanced practice providers, specialists and outpatient facilities. Baptist's stated reason is that out-of-network plans "impose coverage determinations, prior authorization requirements, out-of-network restrictions and benefit limitations" that delay care and make it hard to get services approved. That is Baptist's side of a long-running dispute; the insurers have disputed similar claims in the past. For you, the practical effect is the same either way.</p>

    <h2>What changes for PPO members</h2>
    <p>The difference between an HMO and a PPO is that a PPO will pay something toward care from providers outside its network. That is why many people in the Lexington area chose PPOs: they could keep seeing Baptist doctors even when their plan did not have a contract with Baptist, at a higher copay or coinsurance.</p>
    <p>But that arrangement always had a catch, and Medicare spells it out plainly: in a PPO, <strong>"out-of-network doctors, hospitals, and other providers may decide not to treat you, even if you've used them before."</strong> Your plan can be willing to pay; it cannot make a provider without a contract agree to see you. Baptist's letter is Baptist making that choice for 2027.</p>
    <div class="twocol">
      <div class="yes"><b>Through December 31, 2026</b>
        <ul>
          <li>Out-of-network PPO members could usually still book with Baptist</li>
          <li>The plan paid its out-of-network share; you paid more than in-network</li>
          <li>Emergencies covered</li>
        </ul>
      </div>
      <div class="no"><b>Starting January 1, 2027</b>
        <ul>
          <li>Baptist will not schedule appointments for out-of-network plans, PPOs included</li>
          <li>Exception: active treatment for a serious or complex condition</li>
          <li>Emergencies still treated and covered</li>
        </ul>
      </div>
    </div>
    <p><strong>Emergencies are not affected.</strong> Hospitals must treat a medical emergency, and every Medicare Advantage plan must cover emergency and urgently needed care, in network or not, at in-network cost sharing. If you are having a heart attack or a stroke, go to the nearest emergency room, Baptist included.</p>

    <h2>Which plans are in and out at Baptist</h2>
    <p>Baptist Health publishes its Medicare Advantage network status by insurance company. This is the picture for 2027 as of mid-November:</p>
    <div class="tblwrap">
    <table class="nettbl">
      <tr><th>Medicare Advantage company</th><th>At Baptist Health</th></tr>
      <tr><td>Humana</td><td class="in">In network<small>Restored April 2024</small></td></tr>
      <tr><td>Aetna</td><td class="in">In network<small>Listed for 2026</small></td></tr>
      <tr><td>Anthem</td><td class="in">In network<small>Listed for 2026</small></td></tr>
      <tr><td>UnitedHealthcare</td><td class="out">Out of network<small>Since January 2024</small></td></tr>
      <tr><td>Wellcare</td><td class="out">Out of network<small>Since January 2024</small></td></tr>
      <tr><td>Essence Healthcare</td><td class="out">Out of network<small>Since January 2026</small></td></tr>
      <tr><td>Devoted Health</td><td class="out">Out of network<small>Listed in Baptist's October 2026 update</small></td></tr>
      <tr><td>Passport by Molina</td><td class="ask">Some locations<small>In network at Baptist Hardin, Louisville and La Grange only</small></td></tr>
      <tr><td>Original Medicare, with or without a Medigap plan</td><td class="in">Accepted<small>No network applies</small></td></tr>
    </table>
    </div>
    <p class="vstamp">Sources: Baptist Health's published Medicare Advantage network status, as checked by us in July 2026 and in Baptist's October 5, 2026 update as reported by a regional advisory firm. Baptist cautions that carrier-level status does not guarantee every individual plan. Check your exact plan name.</p>
    <p>Two things to read carefully in that table. First, being with an in-network company is not a guarantee that <em>your plan</em> is in network; carriers sell several plans, and networks can differ between them. Second, if you received this letter, Baptist's own records say your current plan does not participate, whatever company it is with. Believe the letter, then verify.</p>

    <h2>Are you an exception?</h2>
    <p>The letter says Baptist will make exceptions for patients "undergoing an active course of treatment for a serious or complex medical condition." It does not define those words, so do not assume. If you are in the middle of cancer treatment, recovering from surgery, in a cardiac program or seeing a Baptist specialist for something ongoing:</p>
    <div class="stage"><span class="num">1</span><span class="st"><b>Call your Baptist doctor's office now.</b>Ask whether you qualify for the exception, for how long, and whether it covers your hospital and outpatient visits as well as the doctor.</span></div>
    <div class="stage"><span class="num">2</span><span class="st"><b>Call your plan.</b>Ask how it will pay for continuing care at Baptist in 2027, what your out-of-network cost will be, and whether it offers any transition-of-care help for people mid-treatment.</span></div>
    <div class="stage"><span class="num">3</span><span class="st"><b>Get it in writing</b>, from Baptist and from the plan, before December 7, so you still have time to switch plans if the answer is no.</span></div>

    <h2>Your options before January 1</h2>
    <div class="stage"><span class="num">1</span><span class="st"><b>Switch to a plan that includes Baptist, by December 7.</b>During the Annual Enrollment Period you can move to any Medicare Advantage plan in your county. Look at plans from companies Baptist lists as in network, then confirm Baptist is in network for that exact plan in 2027, and check that your other doctors and your prescriptions work too. A new plan takes effect January 1, so there is no gap.</span></div>
    <div class="stage"><span class="num">2</span><span class="st"><b>Move to Original Medicare with a supplement and a drug plan.</b>Baptist, like nearly every doctor and hospital, accepts Original Medicare, with no network to worry about again. The catch in Kentucky: leaving Medicare Advantage for a Medigap plan usually means answering health questions, and you can be charged more or turned down. Kentucky's birthday rule does not help you here. There is one exception: if you joined Medicare Advantage for the first time within the last 12 months (when you first became eligible, or after dropping a supplement), a federal trial right lets you get a supplement without health questions. Read <a href="/articles/switching-medicare-advantage-to-medigap/">switching from Medicare Advantage to Medigap</a> before you drop anything.</span></div>
    <div class="stage"><span class="num">3</span><span class="st"><b>Keep your plan and use a different hospital system.</b>If your doctors are elsewhere or you are willing to move, your plan may already work well. In Lexington, UnitedHealthcare and Wellcare were in network at UK HealthCare and accepted at CHI Saint Joseph in 2026; confirm their 2027 status by name. Our <a href="/articles/does-baptist-health-take-medicare-advantage/">Lexington hospital network guide</a> has the details and phone numbers.</span></div>
    <div class="stage"><span class="num">4</span><span class="st"><b>Missed December 7? There is a backup.</b>From January 1 to March 31, anyone already in a Medicare Advantage plan gets one switch, to another Advantage plan or to Original Medicare. The change starts the first of the following month, so January appointments could still fall in the gap. A hospital leaving at the start of a plan year does not usually create a special enrollment period, so do not count on one.</span></div>

    <h2>Before you switch, check these five things</h2>
    <ul>
      <li><strong>Baptist by name.</strong> Use the plan's 2027 provider directory, then call Baptist to confirm. Ask about the specific hospital and doctor you use.</li>
      <li><strong>Your other doctors.</strong> A plan that adds Baptist can drop someone else you see.</li>
      <li><strong>Your prescriptions.</strong> Enter every drug in Medicare's Plan Finder; the formulary and drug costs change with the plan.</li>
      <li><strong>HMO or PPO.</strong> An HMO usually covers nothing out of network except emergencies and urgent care, and may need referrals. Know which you are choosing.</li>
      <li><strong>The out-of-pocket limit.</strong> It is in the plan's documents and is the most you would pay in a bad year. See our guide to <a href="/articles/medicare-advantage-premium-deductible-copay-coinsurance-explained/">the five cost terms</a>.</li>
    </ul>

    <div class="note">
      <div class="who">
        <span class="duo"><img src="/assets/austin-tyler.jpg" alt="Austin Tyler" width="600" height="750"><img src="/assets/andrew-horn.jpg" alt="Andrew Horn" width="600" height="750"></span>
        <div><b>A note from our advisors</b><span>Tyler Insurance Group, Lexington</span></div>
      </div>
      <p>A lot of folks in Central Kentucky picked a PPO precisely so they could keep Baptist even when the plan and the hospital were not on speaking terms. That workaround ends on January 1. If Baptist is where your doctors are, this is the year to make sure your plan includes it, and the deadline is close.</p>
      <p>Bring the letter, your plan card and your medication list. We will check which 2027 plans in your county include Baptist and your other doctors, compare the costs, and tell you plainly whether to switch, at no charge.</p>
    </div>

    <h2 id="faq">Common questions</h2>
    <div class="faq">
      <h3>Why did I get a letter from Baptist Health about my Medicare Advantage plan?</h3>
      <p>Baptist Health sent the letter in October 2026 to patients it treated in the past year whose records show a Medicare Advantage PPO plan that does not participate in Baptist's network. It explains that Baptist will not schedule appointments for dates of service beginning January 1, 2027, for patients in out-of-network Medicare Advantage plans, including PPOs.</p>
      <h3>Which Medicare Advantage plans does Baptist Health accept for 2027?</h3>
      <p>At the company level, Baptist Health lists Humana, Aetna and Anthem Medicare Advantage as in network, and UnitedHealthcare, Wellcare, Essence Healthcare and Devoted Health as out of network. Passport by Molina is in network only at Baptist Hardin, Louisville and La Grange. Individual plans can differ, so confirm your exact plan at BaptistHealth.com/MedicareAdvantage or with the plan.</p>
      <h3>Can I still use Baptist Health with my PPO if I pay the out-of-network cost?</h3>
      <p>Not for scheduled care starting January 1, 2027, unless you qualify for Baptist's exception for active treatment of a serious or complex condition. A PPO pays toward out-of-network care, but out-of-network providers can decide not to treat you, and Baptist has said it will not schedule out-of-network Medicare Advantage patients, PPOs included.</p>
      <h3>Will Baptist Health still treat me in an emergency?</h3>
      <p>Yes. Hospitals must treat medical emergencies, and Medicare Advantage plans must cover emergency and urgently needed care in or out of network at in-network cost sharing. The scheduling change affects appointments, not emergencies.</p>
      <h3>What should I do if I want to keep seeing Baptist Health doctors?</h3>
      <p>Before December 7, 2026, switch to a 2027 Medicare Advantage plan that includes Baptist Health, after confirming Baptist, your other doctors and your prescriptions for that exact plan. Or move to Original Medicare with a Medigap plan and a drug plan, which Baptist accepts, keeping in mind that Medigap insurers in Kentucky can usually ask health questions when you leave Medicare Advantage.</p>
      <h3>What if I miss the December 7 deadline?</h3>
      <p>From January 1 to March 31, 2027, people in a Medicare Advantage plan can make one switch, to another Medicare Advantage plan or to Original Medicare. The change takes effect the first of the following month, so appointments in the meantime may not be scheduled at Baptist.</p>
    </div>

    <div class="endcta">
      <h3>Want us to check your options?</h3>
      <p>Bring the letter, your plan card and your prescriptions. We will find the 2027 plans in your county that include Baptist and your other doctors, and compare them with what you have, at no charge.</p>
      <div class="row">
        <a class="btn" href="/schedule/">Book a free review &rarr;</a>
        <p class="callline">Or call us directly: <a href="tel:18597858289">(859) 785-8289</a></p>
      </div>
    </div>

    <section class="recap">
      <h2>Quick recap</h2>
      <div class="recap-item">Baptist Health will not schedule appointments from January 1, 2027, for patients in out-of-network Medicare Advantage plans, and that includes PPOs.</div>
      <div class="recap-item">A PPO can pay for out-of-network care, but an out-of-network provider does not have to see you. Baptist has decided not to.</div>
      <div class="recap-item">Baptist lists Humana, Aetna and Anthem as in network; UnitedHealthcare, Wellcare, Essence and Devoted as out. Confirm your exact plan.</div>
      <div class="recap-item">Emergencies are always treated and covered. Patients in active treatment for a serious or complex condition can ask for an exception.</div>
      <div class="recap-item">Options: switch to a plan with Baptist by December 7, move to Original Medicare with a supplement (health questions usually apply), or keep your plan and use another system.</div>
      <div class="recap-item">Backup: one switch between January 1 and March 31, effective the next month.</div>
    </section>

    <section class="kcheck">
      <h2>Test what you learned</h2>
      <p class="kc-sub">Five quick questions. Pick an answer to see if you're right, and why.</p>
      <div id="kcheck"></div>
    </section>
    <script>window.KCHECK = __KCHECK__;</script>

    <div class="sources">
      <b>Sources</b>
      Baptist Health, "Important Information About Your Access to Medical Care from Baptist Health," patient letter, October 2026 &middot;
      Baptist Health Medicare Advantage network status, BaptistHealth.com/MedicareAdvantage, checked July 2026, and Baptist's October 5, 2026 update as reported by Bedrock Financial Group &middot;
      Kentucky Lantern, WDRB and Healthcare Dive, January 2024 (UnitedHealthcare and Wellcare); Kentucky Lantern, March 2024 (Humana restored) &middot;
      Medicare.gov, "Preferred Provider Organizations (PPOs)," "Understanding Medicare Advantage Plans," and enrollment period guidance &middot;
      KFF, emergency services and cost sharing in Medicare Advantage &middot;
      Medicare Rights Center, special enrollment periods for Medicare Advantage &middot;
      Kentucky Revised Statutes 304.14-525 (Medigap birthday rule) &middot;
      UK HealthCare and CHI Saint Joseph Health published Medicare Advantage lists, July and August 2026.
      Checked November 17, 2026.
    </div>

    <p class="stamp"><b>Written and reviewed by Austin Tyler, MBA</b>, Licensed Medicare Advisor, NPN 20234188, Kentucky DOI license #1187780. Network statuses change; we re-check this page before December 7.</p>

    <p class="disclaim">This article is general information, not advice for your specific situation. Network status is as published by Baptist Health on the dates noted and can change; confirm your exact plan with the plan and with Baptist Health. Tyler Insurance Group is not affiliated with Baptist Health. No specific plan is recommended. Tyler Insurance Group is not connected with or endorsed by the United States government or the federal Medicare program. We do not offer every plan available in your area. Currently we represent 6 organizations which offer 158 products in your area. Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance Program (SHIP) to get information on all of your options.</p>
"""
BODY = BODY.replace("__DATE_LONG__", DATE_LONG)

KCHECK = [
 {"q": "Starting January 1, 2027, what will Baptist Health do for patients in out-of-network Medicare Advantage PPO plans?",
  "options": ["See them at a higher copay, as before", "Not schedule appointments, except for certain patients in active treatment", "Refuse emergency care", "Bill them the full price"], "answer": 1,
  "why": "The letter says Baptist is not scheduling appointments from January 1, 2027, for out-of-network Medicare Advantage plans, PPOs included, with exceptions for active treatment of a serious or complex condition."},
 {"q": "Your PPO pays for out-of-network care. Why can Baptist still decline to schedule you?",
  "options": ["PPOs never cover out-of-network care", "Out-of-network providers may decide not to treat PPO members", "Medicare bans PPOs at hospitals", "It can't; this letter is a scam"], "answer": 1,
  "why": "Medicare.gov says out-of-network doctors and hospitals may decide not to treat you, even if you've used them before. The plan can pay; it cannot make a provider agree to see you."},
 {"q": "You have chest pain on February 3 and the closest ER is a Baptist hospital. What happens?",
  "options": ["You will be turned away", "You are treated, and your plan must cover the emergency", "Only if you pay cash", "Only Humana members are treated"], "answer": 1,
  "why": "Hospitals must treat emergencies, and every Medicare Advantage plan covers emergency care in or out of network at in-network cost sharing."},
 {"q": "What is the last day to switch to a 2027 plan that starts January 1?",
  "options": ["November 30", "December 7", "December 31", "March 31"], "answer": 1,
  "why": "The Annual Enrollment Period runs October 15 to December 7. January 1 to March 31 allows one more switch, but it takes effect the following month."},
 {"q": "You have been on Medicare Advantage for six years and want to move to a Medigap plan in Kentucky. What usually applies?",
  "options": ["Guaranteed acceptance through the birthday rule", "Health questions, and the insurer can charge more or decline", "No premium for the first year", "Automatic enrollment"], "answer": 1,
  "why": "Kentucky's birthday rule only helps people already on Medigap. Leaving Medicare Advantage usually means underwriting, unless you are within 12 months of first joining (federal trial right)."},
]
body_html = BODY.replace("__KCHECK__", json.dumps(KCHECK, ensure_ascii=False))
assert not re.findall(r"__[A-Z_]+__", body_html)

out = re.sub(r'(<nav class="crumb" aria-label="Breadcrumb">).*?(</nav>)',
             r'\1<a href="/">Home</a> &rsaquo; <a href="/articles/">Learning Center</a> &rsaquo; <a href="/articles/on-medicare/">Already on Medicare</a> &rsaquo; '
             + CRUMB_LABEL + r'\2', out, count=1, flags=re.S)
out = re.sub(r'<span class="tag">.*?</span>', '<span class="tag">Already on Medicare · Local Kentucky</span>', out, count=1, flags=re.S)
out = re.sub(r'<h1>.*?</h1>', f'<h1>{H1}</h1>', out, count=1, flags=re.S)
out = re.sub(r'(Licensed Medicare Advisor, Tyler Insurance Group · )[^<]*(</div>)', r'\g<1>' + DATE_LONG + r' · 8 min read\2', out, count=1)
m = re.search(r'(<div class="body">\n)(.*?)(\n  </div>\n</article>)', out, re.S); assert m
out = out[:m.start(2)] + body_html.strip("\n") + out[m.end(2):]

mm = re.search(r'<script type="application/ld\+json">(.*?)</script>', out, re.S)
d = json.loads(mm.group(1))
faq_html = re.search(r'<div class="faq">(.*?)</div>', out, re.S).group(1)
clean = lambda s: H.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip())
pairs = [(clean(q), clean(a)) for q, a in re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", faq_html, re.S)]
for node in d["@graph"]:
    t = node.get("@type")
    if t == "BlogPosting":
        node.update({"headline": H1, "description": DESC, "datePublished": DATE, "dateModified": DATE, "image": [OG],
                     "articleSection": "Already on Medicare", "mainEntityOfPage": {"@type": "WebPage", "@id": URL}, "@id": URL + "#article"})
    elif t == "BreadcrumbList":
        node["itemListElement"] = [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.bluegrassmedicarehelp.com/"},
            {"@type": "ListItem", "position": 2, "name": "Learning Center", "item": "https://www.bluegrassmedicarehelp.com/articles/"},
            {"@type": "ListItem", "position": 3, "name": "Already on Medicare", "item": "https://www.bluegrassmedicarehelp.com/articles/on-medicare/"},
            {"@type": "ListItem", "position": 4, "name": CRUMB_LABEL, "item": URL}]
    elif t == "FAQPage":
        node["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]
out = out[:mm.start(1)] + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + out[mm.end(1):]
head = out.split('<div class="body">')[0]
assert "$90" not in re.sub(r"<script.*?</script>", "", head, flags=re.S), "template text left in head"

os.makedirs(f"articles/{SLUG}", exist_ok=True)
open(f"articles/{SLUG}/index.html", "w", encoding="utf-8").write(out)
print(f"wrote articles/{SLUG}/index.html ({len(pairs)} FAQ, {len(KCHECK)} kcheck)")
