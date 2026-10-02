#!/usr/bin/env python3
"""Build /articles/chronic-condition-medicare-advantage-plans-kentucky/ by cloning chrome from an
existing article and swapping in new head, schema, body and knowledge check."""
import json, re, os

SRC = "articles/does-baptist-health-take-medicare-advantage/index.html"
DST_DIR = "articles/chronic-condition-medicare-advantage-plans-kentucky"
URL = "https://www.bluegrassmedicarehelp.com/articles/chronic-condition-medicare-advantage-plans-kentucky/"
TITLE = "Medicare Chronic Condition Plans in Kentucky: Who Qualifies"
H1 = "You Might Qualify for a Chronic Condition Medicare Plan and Not Know It: A Central Kentucky Guide"
DESC = ("Diabetes, a heart condition, or heart failure can qualify you for a Chronic Condition Special "
        "Needs Plan. Two new ones arrive in Central Kentucky for 2027. What counts, what does not, and how to check.")
CRUMB_LABEL = "Chronic Condition Plans"

src = open(SRC, encoding="utf-8").read()
out = src
for a, b in [
 ("<title>Does Baptist Health Take Medicare Advantage? (2026)</title>", f"<title>{TITLE}</title>"),
 ('<meta property="og:title" content="Does Baptist Health Take Medicare Advantage? (2026)">', f'<meta property="og:title" content="{TITLE}">'),
 ('<meta name="twitter:title" content="Does Baptist Health Take Medicare Advantage? (2026)">', f'<meta name="twitter:title" content="{TITLE}">'),
]:
    assert out.count(a) == 1, a[:60]; out = out.replace(a, b)
OLD_DESC = ("Which Medicare Advantage plans are in-network at Baptist Health, UK HealthCare and CHI "
            "Saint Joseph in Lexington, carrier by carrier, verified 2026.")
assert out.count(OLD_DESC) == 3; out = out.replace(OLD_DESC, DESC)
OLD_CANON = "https://www.bluegrassmedicarehelp.com/articles/does-baptist-health-take-medicare-advantage/"
out = out.replace(f'<link rel="canonical" href="{OLD_CANON}">', f'<link rel="canonical" href="{URL}">')
out = out.replace(f'<meta property="og:url" content="{OLD_CANON}">', f'<meta property="og:url" content="{URL}">')

NEWCSS = """
.note{background:var(--cream2);border:1px solid var(--line);border-radius:14px;padding:24px 24px 20px;margin:30px 0 26px;}
.note .who{display:flex;align-items:center;gap:14px;margin-bottom:14px;}
.note .who img{width:56px;height:56px;border-radius:50%;object-fit:cover;object-position:center top;border:2px solid var(--coral);}
.note .who b{display:block;font-size:16.5px;color:var(--ink);}
.note .who span{font-size:14.5px;color:var(--faint);}
.note p{font-size:17.5px;color:#3b352c;margin-bottom:14px;}
.note p:last-child{margin-bottom:0;}
.ans{background:var(--warm);border-left:4px solid var(--coral);border-radius:0 12px 12px 0;padding:20px 22px;margin:0 0 26px;}
.ans p{margin:0 0 12px;font-size:18.5px;} .ans p:last-child{margin-bottom:0;}
.chk{list-style:none;padding:0;margin:0 0 22px;}
.chk li{position:relative;padding:12px 14px 12px 48px;margin-bottom:8px;background:#fff;border:1px solid var(--line);border-radius:12px;font-size:17px;}
.chk li::before{content:"";position:absolute;left:14px;top:14px;width:22px;height:22px;border-radius:6px;border:2px solid var(--green);background:rgba(58,125,82,.10);}
.chk li.no::before{border-color:#b3431d;background:rgba(179,67,29,.08);}
.chk li b{color:var(--ink);}
.stamp{font-size:14.5px;color:var(--faint);margin:26px 0 0;}
.stamp b{color:var(--mute);font-weight:600;}
"""
out = out.replace("</style>", NEWCSS + "</style>")

BODY = r"""
    <p>When I say the words "chronic condition plan" across a kitchen table, people picture an oxygen tank. Then I ask whether they take metformin, or whether a cardiologist put a stent in a few years back, and the answer is often yes. <strong>Those are the people these plans were built for, and almost none of them know it.</strong></p>
    <p>This is a guide to a kind of Medicare Advantage plan called a Chronic Condition Special Needs Plan, or C-SNP, written for Central Kentucky, where the conditions that qualify are not rare. They are the norm after 65.</p>

    <div class="ans">
      <p><strong>A C-SNP is a Medicare Advantage plan built around a specific diagnosis.</strong> You qualify by having the condition, not by being very sick. Diabetes, a heart condition such as coronary artery disease or AFib, or heart failure are the three that matter here.</p>
      <p><strong>For 2027, two more carriers are offering diabetes-and-heart C-SNPs in Fayette, Clark, Jessamine, Scott and Madison counties</strong>, on top of the ones already sold here. About <strong>one in four Kentuckians over 65 has diagnosed diabetes</strong>. You can join a C-SNP at any time of year, and your doctor confirms the diagnosis within 60 days.</p>
    </div>

    <h2>The word "chronic" is doing a lot of damage</h2>
    <p>In plain English, chronic means ongoing. It does not mean severe, and it does not mean disabled. Medicare uses it the same way. A condition you manage with a daily pill and a yearly checkup is a chronic condition. The person who hears the phrase and thinks "that's not me" is, more often than not, exactly who it describes.</p>
    <p>Medicare recognizes fifteen categories of condition that a C-SNP can be built around. The two new Central Kentucky plans, and most of the ones already here, focus on three of them. Here is what each one actually means, in the words your doctor would use.</p>

    <h3>Does this describe you?</h3>
    <ul class="chk">
      <li><b>Diabetes.</b> Type 1 or Type 2, whether you manage it with insulin, pills, or diet alone. If a doctor has diagnosed it, it counts.</li>
      <li><b>Coronary artery disease.</b> A past heart attack, a stent, bypass surgery, or a diagnosis of angina or blocked arteries.</li>
      <li><b>A heart rhythm problem.</b> Atrial fibrillation (AFib) is the common one. Any diagnosed cardiac arrhythmia is in this group.</li>
      <li><b>Peripheral vascular disease.</b> Poor circulation in the legs from narrowed arteries, sometimes called PAD.</li>
      <li><b>A chronic blood clot disorder.</b> Ongoing treatment for venous clots, such as recurring DVT.</li>
      <li><b>Chronic heart failure.</b> Sometimes described to patients as a weak heart, a low ejection fraction, or fluid around the heart or lungs.</li>
    </ul>
    <p>If you checked one, you may qualify for every diabetes-and-heart C-SNP sold in your county. Now the ones people assume count and do not:</p>
    <ul class="chk">
      <li class="no"><b>High blood pressure by itself.</b> Hypertension is not in the cardiovascular group Medicare uses. It qualifies only if it has led to one of the conditions above.</li>
      <li class="no"><b>High cholesterol by itself.</b> Same answer.</li>
      <li class="no"><b>Prediabetes.</b> Not a diabetes diagnosis.</li>
      <li class="no"><b>COPD or emphysema.</b> This is its own Medicare category, chronic lung disorders, and it is a real one. But <strong>no lung-disorder C-SNP is sold in our counties</strong> as of the 2026 plan file, and neither of the two new 2027 plans covers it. That matters in Kentucky, where roughly one in five people over 65 has COPD, and I would rather tell you plainly than let you assume.</li>
    </ul>

    <h2>Why this matters more here than almost anywhere</h2>
    <p>Kentucky ranked <strong>46th of 50 states</strong> in the 2025 America's Health Rankings Senior Report, and 49th on health outcomes. Underneath that number is a set of figures that, read next to the eligibility list above, explain why I am writing this.</p>
    <div class="tblwrap">
    <table class="nettbl">
      <tr><th>Kentucky adults 65 and older</th><th>Share with the condition</th><th>Qualifies for the 2027 plans?</th></tr>
      <tr><td>Diagnosed diabetes</td><td><strong>about 25 to 27 percent</strong></td><td class="in">Yes</td></tr>
      <tr><td>Coronary heart disease</td><td><strong>about 13 to 15 percent</strong></td><td class="in">Yes</td></tr>
      <tr><td>COPD</td><td><strong>about 19 to 20 percent</strong></td><td class="out">No (different category)</td></tr>
    </table>
    </div>
    <p class="vstamp">Sources: Kentucky Department for Public Health 2025 Diabetes Report (25.0% in 2023) and Kentucky BRFSS reports (27.2% and 27.6% in other recent years); Kentucky DPH COPD prevalence 2024 (19.2%) and BRFSS 2018 and 2019 (20.2%, 19.4%); Kentucky BRFSS coronary heart disease, 65 and older, 13.0% to 15.5% across recent survey years. Checked October 2026. These are statewide survey estimates, not county counts.</p>
    <p>Nationally, about <strong>68 percent of people on Medicare have two or more chronic conditions</strong>, per CMS. Put the Kentucky figures against that and the picture is simple: in a county like Fayette, with <strong>56,114 people eligible for Medicare and 30,598 of them already on a Medicare Advantage plan</strong>, a meaningful share of the people reading this already qualify for a plan they have never been offered.</p>
    <p>I am not going to turn those percentages into a headcount for your county, because that would be my arithmetic dressed up as a statistic. The honest version is that if the statewide rate holds, it is thousands of people in Fayette County alone.</p>

    <h2>What is new for 2027 in Central Kentucky</h2>
    <p>Two carriers are adding diabetes-and-heart C-SNPs for the 2027 plan year, which you can enroll in starting October 15, 2026, for coverage on January 1:</p>
    <div class="tblwrap">
    <table class="nettbl">
      <tr><th>Plan (2027)</th><th>Conditions it is built for</th><th>Our counties in its service area</th></tr>
      <tr><td><strong>Aetna Medicare Chronic Care (HMO C-SNP)</strong>, H0628-044</td><td>Diabetes, chronic heart failure, cardiovascular disorders</td><td>Fayette, Clark, Jessamine, Scott, Madison, Woodford, Franklin, Montgomery, Garrard, plus 9 other Kentucky counties</td></tr>
      <tr><td><strong>Anthem Chronic Care Advantage (HMO C-SNP)</strong>, H9525-022</td><td>Diabetes, cardiovascular disorders, chronic heart failure</td><td>Statewide service area, including all of the above</td></tr>
    </table>
    </div>
    <p class="vstamp">Source: each plan's 2027 Summary of Benefits, plan year January 1 to December 31, 2027. Both plans include Part D drug coverage and both are HMOs. Service areas confirmed from the carrier documents in October 2026; CMS publishes the official county list in its 2027 plan landscape file.</p>
    <p>They join C-SNPs that were already here in 2026: a UnitedHealthcare diabetes-and-heart plan, two Devoted Health diabetes-and-heart plans (those are PPOs), and a Humana and an Anthem plan each built for chronic kidney disease. So a Central Kentuckian with diabetes or a heart condition may have four or more of these plans to compare for 2027, which was not true a few years ago.</p>
    <div class="callout"><b>Why I am not listing copays here.</b>Plan benefits change every January, and a comparison between these plans and the one you have now depends entirely on your doctors, your pharmacy and your prescriptions. Printing a copay table would be out of date by spring and misleading today. The plan documents are public, and I will walk through them with you line by line, at no cost.</div>

    <h2>How a C-SNP differs from the Advantage plan you have now</h2>
    <p>It is still Medicare Advantage. The same federal rules apply: you keep Part A and Part B, you use the plan's network, your care is coordinated through a primary doctor, and there is a yearly out-of-pocket maximum. Three things are different, and they are the reason the plan exists:</p>
    <ul>
      <li><strong>It is built around your diagnosis.</strong> Medicare requires every C-SNP to run a formal Model of Care for the condition it serves, which in practice means a care manager, a health risk assessment when you join, and a plan of care that is reviewed. Benefits are designed around what people with that condition actually use.</li>
      <li><strong>You have to have the condition, and keep having it.</strong> That is the trade. A C-SNP can only enroll people with the qualifying diagnosis, so your doctor has to confirm it.</li>
      <li><strong>You can get in outside the fall window.</strong> See the next section, because this is the part almost everyone gets wrong.</li>
    </ul>

    <h2>You do not have to wait for October</h2>
    <p>Most people believe they can only change Medicare plans between October 15 and December 7. For a C-SNP, that is not true. <strong>Having a qualifying chronic condition gives you a Special Enrollment Period to join a C-SNP at any time of year.</strong> If you are reading this in February after a January diagnosis, you do not sit on it for nine months.</p>
    <p>The Annual Enrollment Period still works too, and this fall it runs October 15 to December 7 for a January 1 start. If you are on an Advantage plan now, you also have the January 1 to March 31 open enrollment window to make one change.</p>
    <div class="callout warn" style="background:#fdecea;border-left-color:#b3431d;"><b>The 60-day rule, which is where people get tripped up.</b>A C-SNP can enroll you based on your own answers, but it must then verify the diagnosis with your treating doctor. If that confirmation is not in hand within 60 days of your start date, the plan has to disenroll you at the end of your second month. You would get a two-month window to pick another plan, but you would have spent two months on a plan you then lose. The fix is simple: before you enroll, call your doctor's office and tell them a verification form is coming.</div>

    <h2>Four things to check before you switch</h2>
    <div class="stage"><span class="num">1</span><span class="st"><b>Your hospital and your specialists</b>Both new plans are HMOs, which means a network. For most people here that comes down to UK HealthCare, Baptist Health Lexington and CHI Saint Joseph, and the cardiologist or endocrinologist you already see. Our <a href="/articles/does-baptist-health-take-medicare-advantage/">Lexington hospital network table</a> is the place to start, and the plan's own directory is the place to finish.</span></div>
    <div class="stage"><span class="num">2</span><span class="st"><b>Every prescription, by name, on the 2027 formulary</b>Diabetes and heart drugs are exactly the kind that sit on different tiers in different plans. Insulin is capped at $35 a month on every Part D plan, but everything else varies. Look up each one.</span></div>
    <div class="stage"><span class="num">3</span><span class="st"><b>Whether your doctor will confirm the diagnosis</b>Not whether you have it, whether the office will send the form within 60 days. Ask before you enroll.</span></div>
    <div class="stage"><span class="num">4</span><span class="st"><b>What you would be giving up</b>If your current plan has something you lean on, make sure the C-SNP's version of it is at least as good for you. A plan built for your condition is usually a strong fit, but usually is not always, and the comparison is the point.</span></div>

    <div class="note">
      <div class="who">
        <img src="/assets/austin-tyler.jpg" alt="Austin Tyler" width="600" height="750">
        <div><b>A note from Austin</b><span>Licensed Kentucky Medicare agent, Lexington</span></div>
      </div>
      <p>The people who qualify for these plans are almost never the people who think they do. The ones who come in asking about a chronic condition plan usually have something that does not count, like blood pressure. The ones who qualify came in to ask about something else entirely, and the metformin or the stent only comes up because I ask.</p>
      <p>So I will say the quiet part. If you are on a Medicare Advantage plan in Central Kentucky and you have diabetes or a heart diagnosis, there are now plans in your county that were built for you, and the only reason you have not heard about them is that nobody was required to tell you. That is what the free review is for.</p>
    </div>

    <h2>Who this is not for</h2>
    <ul>
      <li><strong>No qualifying diagnosis.</strong> Blood pressure, cholesterol or prediabetes alone will not get you in, and a plan cannot keep you if the doctor will not confirm a listed condition.</li>
      <li><strong>COPD only.</strong> You have a real chronic condition under Medicare's definition, but no plan in our counties is built for it yet. If one arrives, this page will say so.</li>
      <li><strong>Medicare plus Medicaid.</strong> You likely qualify for a Dual Eligible Special Needs Plan instead, which is a different conversation and often a better one.</li>
      <li><strong>Happy on a Medicare Supplement.</strong> A C-SNP is a Medicare Advantage plan. If you chose Original Medicare with a Supplement for the freedom of no network, this is not a reason to give that up.</li>
    </ul>
    <p>If none of those are you, and one of the boxes in the first checklist is, the next step is a comparison, not a decision. Kentucky SHIP offers free, non-sales counseling statewide, and I do the same comparison at no cost with every plan in your county on the table. For a county-by-county look at what is sold where, see our <a href="/articles/medicare-advantage-central-kentucky-counties/">Central Kentucky Medicare Advantage guide</a>.</p>

    <h2 id="faq">Common questions from Central Kentucky</h2>
    <div class="faq">
      <h3>What is a Chronic Condition Special Needs Plan?</h3>
      <p>A C-SNP is a Medicare Advantage plan that only enrolls people with a specific diagnosis and is required by Medicare to run a formal care model for that condition. It includes Part D drug coverage and uses a network like other Advantage plans. The plans sold in Central Kentucky are built for diabetes, cardiovascular disorders and chronic heart failure, and two for chronic kidney disease. You qualify by having the diagnosis, confirmed by your doctor, not by being seriously ill.</p>
      <h3>Does high blood pressure qualify me for a chronic condition plan?</h3>
      <p>Not on its own. The cardiovascular group Medicare uses for C-SNPs is limited to cardiac arrhythmias such as atrial fibrillation, coronary artery disease, peripheral vascular disease and chronic venous thromboembolic disorder. High blood pressure or high cholesterol alone are not on that list. If blood pressure has led to one of those diagnoses, or to heart failure, that diagnosis is what qualifies you.</p>
      <h3>I have COPD. Can I join one of the new Kentucky C-SNPs?</h3>
      <p>Not the two new 2027 plans, which are built for diabetes, cardiovascular disorders and heart failure. COPD falls under a separate Medicare category, chronic lung disorders, and as of the 2026 plan file no lung-disorder C-SNP is sold in Fayette, Clark, Jessamine, Scott or Madison counties. If you also have diabetes or a qualifying heart diagnosis, that second condition can qualify you.</p>
      <h3>Can I switch to a C-SNP in the middle of the year?</h3>
      <p>Yes. A qualifying chronic condition gives you a Special Enrollment Period to join a C-SNP at any time of year, not only during the October 15 to December 7 Annual Enrollment Period. The 2027 plans can be joined starting October 15, 2026, for a January 1 start, or later in 2027 under that Special Enrollment Period.</p>
      <h3>What happens if my doctor does not send the verification?</h3>
      <p>The plan must confirm your diagnosis with your treating physician within 60 days of your start date. If it cannot, you are disenrolled at the end of your second month and returned to Original Medicare, with a two-month Special Enrollment Period to choose another plan. Calling your doctor's office before you enroll, so they expect the form, prevents nearly all of these cases.</p>
      <h3>Are the new 2027 plans HMOs?</h3>
      <p>Yes, both the Aetna and the Anthem 2027 C-SNPs in Central Kentucky are HMOs, so you use the plan's network and a primary care doctor coordinates referrals. Check that your hospital system and your specialists are in the plan's 2027 directory before you enroll. Two of the Devoted Health C-SNPs already sold here are PPOs, which work differently.</p>
    </div>

    <div class="endcta">
      <h3>Think one of those boxes is you?</h3>
      <p>I will pull every chronic condition plan sold in your county for 2027, check your doctors, your hospital and your prescriptions against each one, and tell you plainly whether any of them beats what you have. No cost, and if the answer is "keep your plan," that is what you will hear.</p>
      <div class="row">
        <a class="btn" href="/review/">Get a free plan comparison &rarr;</a>
        <p class="callline">Or call me directly: <a href="tel:18596186443">(859) 618-6443</a></p>
      </div>
    </div>

    <section class="recap">
      <h2>Quick recap</h2>
      <div class="recap-item">A C-SNP is a Medicare Advantage plan built around a diagnosis. You qualify by having diabetes, a cardiovascular disorder such as coronary artery disease or AFib, or chronic heart failure, confirmed by your doctor.</div>
      <div class="recap-item">"Chronic" means ongoing, not severe. A condition managed with a daily pill counts. High blood pressure, high cholesterol and prediabetes alone do not.</div>
      <div class="recap-item">About one in four Kentuckians over 65 has diagnosed diabetes, and Kentucky ranks 46th in the 2025 Senior Report. The people who qualify are common, not rare.</div>
      <div class="recap-item">For 2027, Aetna and Anthem each add a diabetes-and-heart HMO C-SNP covering Fayette, Clark, Jessamine, Scott and Madison, joining the UnitedHealthcare, Devoted and kidney-disease plans already here.</div>
      <div class="recap-item">No COPD plan is sold in our counties yet, and this page says so rather than letting you assume.</div>
      <div class="recap-item">You can join a C-SNP any time of year, but your doctor must confirm the diagnosis within 60 days or you are disenrolled. Call the office first.</div>
      <div class="recap-item">Both new plans are HMOs. Check your hospital, your specialists and every prescription against the 2027 directory and formulary before you switch.</div>
    </section>

    <section class="kcheck">
      <h2>Test what you learned</h2>
      <p class="kc-sub">Five quick questions. Pick an answer to see if you're right, and why.</p>
      <div id="kcheck"></div>
    </section>
    <script>window.KCHECK = __KCHECK__;</script>

    <div class="sources">
      <b>Sources</b>
      Aetna Medicare Chronic Care (HMO C-SNP) H0628-044 and Anthem Chronic Care Advantage (HMO C-SNP) H9525-022, 2027 Summaries of Benefits &middot;
      CMS CY2026 Medicare Advantage Landscape file, Kentucky extract (existing C-SNPs by county) &middot;
      CMS Special Needs Plans FAQ and Medicare Managed Care Manual, chapter 16-B (qualifying condition categories; cardiovascular disorders definition) &middot;
      CMS contract year 2025 final rule and Medicare Interactive (physician verification within 60 days; Special Enrollment Period) &middot;
      Kentucky Department for Public Health, 2025 Diabetes Report and COPD Prevalence 2024; Kentucky Behavioral Risk Factor Survey annual reports &middot;
      America's Health Rankings, 2025 Senior Report &middot;
      CMS Chronic Conditions among Medicare Beneficiaries chartbook.
      Checked October 2026.
    </div>

    <p class="stamp"><b>Written and reviewed by Austin Tyler</b>, licensed Kentucky agent, NPN 20234188, Kentucky DOI license #1187780. Plan details taken from the carriers' 2027 Summaries of Benefits and the CMS plan file; health figures from Kentucky DPH and BRFSS reports, October 2026.</p>

    <p class="disclaim">This article is general information, not advice for your specific situation. Plans are named for factual eligibility information only; this is not an endorsement, a comparison of benefits, or a statement about plan quality, and benefits, premiums, networks and service areas can change each year. Eligibility for a Chronic Condition Special Needs Plan requires a qualifying diagnosis verified by your physician. Tyler Insurance Group is not connected with or endorsed by the United States government or the federal Medicare program. We do not offer every plan available in your area. Currently we represent 6 organizations which offer 158 products in your area. Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance Program (SHIP) to get information on all of your options.</p>
"""

KCHECK = [
 {"q": "Which of these qualifies someone for the diabetes-and-heart C-SNPs sold in Central Kentucky?",
  "options": ["High blood pressure controlled with one pill", "Type 2 diabetes managed with diet alone", "High cholesterol", "Prediabetes"],
  "answer": 1,
  "why": "Any diagnosed diabetes counts, however it is managed. Blood pressure, cholesterol and prediabetes alone are not on Medicare's qualifying list."},
 {"q": "A friend has COPD and nothing else. Can she join one of the two new 2027 plans?",
  "options": ["Yes, COPD is a chronic condition", "Only during October", "No, those plans are built for diabetes and heart conditions, and no lung plan is sold here yet", "Yes, if her doctor signs a form"],
  "answer": 2,
  "why": "COPD is its own Medicare category, chronic lung disorders. The 2027 Aetna and Anthem plans cover diabetes, cardiovascular disorders and heart failure, and no lung-disorder C-SNP appears in the Kentucky plan file for our counties."},
 {"q": "When can a person with a qualifying condition join a C-SNP?",
  "options": ["Only October 15 to December 7", "Only in January", "At any time of year, through a Special Enrollment Period", "Only when turning 65"],
  "answer": 2,
  "why": "A qualifying chronic condition gives you a Special Enrollment Period to join a C-SNP year-round. The fall window and the January-to-March window work too."},
 {"q": "What happens if the plan cannot confirm your diagnosis with your doctor within 60 days?",
  "options": ["Nothing, you stay enrolled", "You are disenrolled at the end of your second month", "Your premium goes up", "You lose Part B"],
  "answer": 1,
  "why": "Medicare requires physician verification within 60 days. Without it the plan must disenroll you, with a two-month window to choose another plan. Calling your doctor's office before enrolling prevents this."},
 {"q": "Roughly what share of Kentuckians over 65 have diagnosed diabetes?",
  "options": ["About 1 in 20", "About 1 in 10", "About 1 in 4", "About half"],
  "answer": 2,
  "why": "Kentucky Department for Public Health and BRFSS reports put it at 25 to 27 percent in recent years, which is why these plans fit far more people than the word chronic suggests."},
]
body_html = BODY.replace("__KCHECK__", json.dumps(KCHECK, ensure_ascii=False))

out = re.sub(r'(<nav class="crumb" aria-label="Breadcrumb">).*?(</nav>)',
             r'\1<a href="/">Home</a> &rsaquo; <a href="/articles/">Learning Center</a> &rsaquo; <a href="/articles/coverage/">Coverage Choices</a> &rsaquo; '
             + CRUMB_LABEL + r'\2', out, count=1, flags=re.S)
out = re.sub(r'<span class="tag">.*?</span>', '<span class="tag">Coverage Choices · Local Kentucky</span>', out, count=1, flags=re.S)
out = re.sub(r'<h1>.*?</h1>', f'<h1>{H1}</h1>', out, count=1, flags=re.S)
out = re.sub(r'(Local Kentucky Medicare agent · )[^<]*(</div>)', r'\1October 2, 2026 · 12 min read\2', out, count=1)
m = re.search(r'(<div class="body">\n)(.*?)(\n  </div>\n</article>)', out, re.S); assert m
out = out[:m.start(2)] + body_html.strip("\n") + out[m.end(2):]

mm = re.search(r'<script type="application/ld\+json">(.*?)</script>', out, re.S)
d = json.loads(mm.group(1))
faq_html = re.search(r'<div class="faq">(.*?)</div>', out, re.S).group(1)
clean = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()
pairs = [(clean(q), clean(a)) for q, a in re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", faq_html, re.S)]
for node in d["@graph"]:
    t = node.get("@type")
    if t == "BlogPosting":
        node.update({"headline": H1, "description": DESC, "datePublished": "2026-10-02", "dateModified": "2026-10-02",
                     "articleSection": "Coverage Choices", "mainEntityOfPage": {"@type": "WebPage", "@id": URL}, "@id": URL + "#article"})
    elif t == "BreadcrumbList":
        node["itemListElement"] = [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.bluegrassmedicarehelp.com/"},
            {"@type": "ListItem", "position": 2, "name": "Learning Center", "item": "https://www.bluegrassmedicarehelp.com/articles/"},
            {"@type": "ListItem", "position": 3, "name": "Coverage Choices", "item": "https://www.bluegrassmedicarehelp.com/articles/coverage/"},
            {"@type": "ListItem", "position": 4, "name": CRUMB_LABEL, "item": URL}]
    elif t == "FAQPage":
        node["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]
out = out[:mm.start(1)] + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + out[mm.end(1):]

os.makedirs(DST_DIR, exist_ok=True)
open(f"{DST_DIR}/index.html", "w", encoding="utf-8").write(out)
print(f"wrote {DST_DIR}/index.html ({len(pairs)} FAQ, {len(KCHECK)} kcheck)")
