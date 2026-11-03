#!/usr/bin/env python3
"""Build /articles/medicare-advantage-by-the-numbers/ from the current article chrome.
Facts, sources and the lifetime-cost assumptions: docs/dossiers/medicare-advantage-by-the-numbers.md."""
import json, re, os, html as H

SRC = "articles/2027-social-security-raise-medicare-costs/index.html"
OLD_URL = "https://www.bluegrassmedicarehelp.com/articles/2027-social-security-raise-medicare-costs/"
SLUG = "medicare-advantage-by-the-numbers"
URL = f"https://www.bluegrassmedicarehelp.com/articles/{SLUG}/"
TITLE = "Medicare Advantage by the Numbers: Denials, Costs and Facts"
H1 = "Medicare Advantage by the Numbers: Enrollment, Denials, Lifetime Costs, and the Facts Behind the Debate"
DESC = ("How many people are on Medicare Advantage, how often plans deny care, why the program draws so much anger, "
        "and what a Medicare Supplement, Original Medicare alone and an Advantage plan cost over 20 years, using public data.")
CRUMB_LABEL = "Medicare Advantage by the Numbers"
DATE, DATE_LONG = "2026-11-03", "November 3, 2026"

# ---- the lifetime model (assumptions are printed on the page)
YEARS = 20
def total(start, r, n=YEARS): return sum(start * (1 + r) ** k for k in range(n))
PLAN_G, PDP, PARTB_DED = 160, 35, 283
PATHS = {r: total(PLAN_G * 12, r) + total(PDP * 12, .05) + total(PARTB_DED, .05) for r in (.05, .08, .10)}
k = lambda x: f"${round(x / 1000):,}k"
usd = lambda x: f"${x:,.0f}"
LOW, MID, HIGH = PATHS[.05], PATHS[.08], PATHS[.10]
PERYR_LOW, PERYR_HIGH = round(LOW / YEARS, -2), round(HIGH / YEARS, -2)
BAD_YEAR = 283 + 0.2 * (100000 - 283)
assert round(BAD_YEAR) == 20226

src = open(SRC, encoding="utf-8").read()
out = src
old_title = re.search(r"<title>(.*?)</title>", out).group(1)
old_desc = re.search(r'<meta name="description" content="([^"]*)"', out).group(1)
out = out.replace(old_title, TITLE).replace(old_desc, DESC).replace(OLD_URL, URL)

F = 'font-family="Source Sans 3, Arial, sans-serif"'
INK, MUTE, LINE, WARM, GREEN_D, CORAL_D, GRAY = "#1b2836", "#4a5563", "#e3e8ee", "#fff0e8", "#2f6844", "#b23c17", "#8a94a0"
def viz(label, w, h, inner, cap):
    return (f'<figure class="viz" role="img" aria-label="{label}">\n<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><g {F}>\n{inner}\n</g></svg></figure>\n<p class="vizcap">{cap}</p>')
def hbar(y, label, value_txt, width, color, txt_inside=True):
    t = (f'<text x="20" y="{y}" font-size="16.5" fill="{MUTE}">{label}</text>'
         f'<rect x="20" y="{y+9}" width="{width:.0f}" height="34" rx="7" fill="{color}"/>')
    if txt_inside:
        t += f'<text x="{20+width-12:.0f}" y="{y+32}" text-anchor="end" font-size="17" font-weight="700" fill="#fff">{value_txt}</text>'
    else:
        t += f'<text x="{20+width+10:.0f}" y="{y+32}" font-size="17" font-weight="700" fill="{color}">{value_txt}</text>'
    return t

# Figure 1: prior authorization per 1,000 requests
VIZ_PA = viz("Out of every 1,000 prior authorization requests in Medicare Advantage in 2024, 923 were approved and 77 were denied. Of the 77 denials, about 9 were appealed and about 7 of those were overturned. About 68 denials were never appealed.", 420, 330,
    f'<text x="210" y="30" text-anchor="middle" font-size="19" font-weight="700" fill="{INK}">Every 1,000 requests, 2024</text>'
    + hbar(62, "Approved", "923", 380, GREEN_D)
    + hbar(130, "Denied", "77", 32, CORAL_D, False)
    + hbar(198, "Denials that were appealed", "about 9", 6, CORAL_D, False)
    + hbar(266, "Appeals that won", "about 7", 5, GREEN_D, False),
    "Figure 1. Medicare Advantage prior authorization, all plans, 2024: 52.8 million requests, 7.7% denied, 11.5% of denials appealed, 80.7% of appeals overturned. Source: KFF analysis of CMS data. Per-1,000 figures are our arithmetic.")

# Figure 2: what premiums take from the average check
VIZ_CHECK = viz("On the average retired worker's Social Security check of $2,071 a month, Original Medicare with an average Plan G and an average drug plan takes $431.90 in premiums, about 21 percent. A $0-premium Medicare Advantage plan with drug coverage takes only the Part B premium, $202.90, about 10 percent.", 420, 250,
    f'<text x="210" y="30" text-anchor="middle" font-size="19" font-weight="700" fill="{INK}">Premiums from a $2,071 check</text>'
    f'<text x="20" y="66" font-size="16.5" fill="{MUTE}">Original Medicare + Plan G + drug plan</text>'
    f'<rect x="20" y="76" width="380" height="36" rx="7" fill="{LINE}"/>'
    f'<rect x="20" y="76" width="{380*202.90/2071:.0f}" height="36" rx="7" fill="{INK}"/>'
    f'<rect x="{20+380*202.90/2071:.0f}" y="76" width="{380*229/2071:.0f}" height="36" fill="{CORAL_D}"/>'
    f'<text x="{20+380*431.9/2071+10:.0f}" y="100" font-size="17" font-weight="700" fill="{CORAL_D}">$432 (21%)</text>'
    f'<text x="20" y="148" font-size="16.5" fill="{MUTE}">$0-premium Advantage plan with drugs</text>'
    f'<rect x="20" y="158" width="380" height="36" rx="7" fill="{LINE}"/>'
    f'<rect x="20" y="158" width="{380*202.90/2071:.0f}" height="36" rx="7" fill="{INK}"/>'
    f'<text x="{20+380*202.90/2071+10:.0f}" y="182" font-size="17" font-weight="700" fill="{INK}">$203 (10%)</text>'
    f'<rect x="20" y="214" width="14" height="14" fill="{INK}"/><text x="40" y="226" font-size="14.5" fill="{MUTE}">Part B</text>'
    f'<rect x="100" y="214" width="14" height="14" fill="{CORAL_D}"/><text x="120" y="226" font-size="14.5" fill="{MUTE}">Plan G $194 + drug plan $35</text>',
    "Figure 2. 2026 figures: average retired-worker benefit $2,071 (SSA), Part B $202.90 (CMS), average Plan G premium $194 among current policyholders (KFF analysis of NAIC data), average stand-alone drug plan premium about $35 (CMS). Copays and other costs are not included.")

# Figure 3: 20 years of supplement premiums against median savings
W = 380 / max(HIGH, 110100)
VIZ_LIFE = viz(f"Twenty years of Plan G, a drug plan and the Part B deductible cost about {k(LOW)} if premiums rise 5 percent a year, {k(MID)} at 8 percent, and {k(HIGH)} at 10 percent. Half of people on Medicare have savings below $110,100.", 420, 330,
    f'<text x="210" y="30" text-anchor="middle" font-size="19" font-weight="700" fill="{INK}">20 years of a supplement, age 65 to 85</text>'
    + hbar(62, "Premiums rise 5% a year", k(LOW), LOW * W, CORAL_D)
    + hbar(130, "Premiums rise 8% a year", k(MID), MID * W, CORAL_D)
    + hbar(198, "Premiums rise 10% a year", k(HIGH), HIGH * W, CORAL_D)
    + hbar(266, "Median savings of a person on Medicare", "$110k", 110100 * W, GRAY),
    f"Figure 3. Plan G at $160 a month at 65, a $35 drug plan and the $283 Part B deductible, the last two rising 5% a year; the Part B premium is left out because every path pays it. Median savings from KFF and the Urban Institute (2024). Our arithmetic; assumptions in the table above.")

# Figure 4: one bad year
WB = 380 / BAD_YEAR
VIZ_BAD = viz("For one year with $100,000 of Medicare-approved outpatient care, Original Medicare alone leaves you $20,226. A Medicare Advantage plan stops at its limit: $9,250 at most, $5,421 on average. Plan G leaves only the $283 Part B deductible.", 420, 330,
    f'<text x="210" y="30" text-anchor="middle" font-size="19" font-weight="700" fill="{INK}">One $100,000 year: what you owe</text>'
    + hbar(62, "Original Medicare alone (no cap)", "$20,226", BAD_YEAR * WB, CORAL_D)
    + hbar(130, "Advantage plan at the legal maximum", "$9,250", 9250 * WB, INK)
    + hbar(198, "Advantage plan, average limit", "$5,421", 5421 * WB, INK)
    + hbar(266, "Plan G supplement", "$283", 283 * WB, GREEN_D, False),
    "Figure 4. 2026 rules, Part B services, in-network for the Advantage plan. Original Medicare: $283 deductible plus 20% of the rest, with no yearly cap. Advantage limits from KFF. Premiums are separate: Plan G's are what buy that $283.")

BODY = r"""
    <p class="updated">Updated __DATE_LONG__. Every figure on this page comes from a public source (KFF, CMS, MedPAC, the HHS Inspector General, the Social Security Administration, the U.S. Senate) and is listed at the bottom. Where we do our own arithmetic, we say so and show the assumptions.</p>
    <p>Few topics in Medicare start arguments faster than Medicare Advantage. Some people call it the best deal in retirement; others say they would never touch it. Much of what gets said in both directions is a story, a TV ad or a bad experience someone heard about. This page sets the stories aside and lays out the numbers: how many people use these plans, how often they deny care, why so many people distrust them, and what each way of getting Medicare actually costs over a lifetime. We are not here to pick a side. We are here so you can decide with facts.</p>

    <div class="ans">
      <p><strong>The short version:</strong></p>
      <ul>
        <li><strong>More than half of Medicare is now Advantage:</strong> 55% of eligible people, more than 1 in 2, over 35 million, in 2026.</li>
        <li><strong>Most prior authorization requests are approved.</strong> In 2024, plans denied 7.7%, about 1 in 13 requests. Only about 1 in 9 denials was appealed, and about 4 in 5 appeals won.</li>
        <li><strong>The distrust has real causes:</strong> documented denial problems in nursing-home and rehab care, hospitals leaving networks, aggressive marketing, and federal estimates that plans are paid more than Original Medicare would cost.</li>
        <li><strong>Supplements are getting harder to afford.</strong> The average Medigap premium rose 20% from 2020 to 2025, from $203 to $244 a month, about $490 more a year. Outside your first six months on Part B, most states let insurers turn you down for health reasons.</li>
        <li><strong>Over 20 years</strong>, a Plan G supplement plus a drug plan costs roughly __LOW__ to __HIGH__ in premiums and deductibles, against median savings of $110,100 among people on Medicare. A $0-premium Advantage plan costs more only if your copays average more than about __PERYR_LOW__ to __PERYR_HIGH__ a year, every year.</li>
      </ul>
    </div>

    <h2>The percentages in everyday terms</h2>
    <p>Percentages are easy to misread, so here is what the main ones on this page mean in people, requests and dollars. Conversions marked "our arithmetic" are calculated from the published figures.</p>
    <div class="tblwrap">
    <table class="nettbl">
      <tr><th>The figure</th><th>What it means</th></tr>
      <tr><td>55% of eligible people are on Advantage</td><td>More than 1 in 2 people, about 35 million</td></tr>
      <tr><td>46% are with UnitedHealth or Humana</td><td>Nearly half of members, about 16 million people</td></tr>
      <tr><td>7.7% of prior authorization requests denied (2024)</td><td>About 1 in 13 requests; 12 of every 13 are approved</td></tr>
      <tr><td>11.5% of denials appealed</td><td>About 1 in 9 denials; the other 8 are never challenged</td></tr>
      <tr><td>80.7% of appeals overturned</td><td>About 4 in 5 people who appeal win, fully or partly</td></tr>
      <tr><td>12% of standard requests denied (2025 insurer data)</td><td>About 1 in 8 requests</td></tr>
      <tr><td>13% of sampled denials met Medicare rules (Inspector General)</td><td>About 1 in 8 denials in the sample should likely have been approved</td></tr>
      <tr><td>UnitedHealthcare post-acute denials, 8.7% to 22.7%</td><td>From about 1 in 11 requests in 2019 to nearly 1 in 4 in 2022</td></tr>
      <tr><td>About 23% of Original Medicare prior authorization requests denied</td><td>Nearly 1 in 4, but only about 2 requests are made per 100 people a year</td></tr>
      <tr><td>Advantage paid about 14% more ($76 billion, MedPAC)</td><td>Roughly $2,200 per Advantage member per year, and Part B premiums roughly $15 a month higher for everyone (our arithmetic)</td></tr>
      <tr><td>12% of men and 15% of women rely on Social Security for 90%+ of income</td><td>About 1 in 8 men and 1 in 7 women 65 and older on Social Security</td></tr>
      <tr><td>Health costs equal 36% of Social Security income</td><td>About $1 of every $3, or more than four months of benefits a year</td></tr>
      <tr><td>Medigap premiums up 7% in 2025</td><td>About $16 more a month on the average $244 premium, about $190 a year</td></tr>
      <tr><td>Plan G filings up 12% to 26% in 2026</td><td>On a $194 premium, about $23 to $50 more a month, $280 to $605 a year</td></tr>
      <tr><td>13% of people in Original Medicare have no supplement</td><td>About 1 in 8, 3.5 million people</td></tr>
      <tr><td>30% of them had trouble paying for care</td><td>About 3 in 10</td></tr>
      <tr><td>You pay 20% on Original Medicare alone</td><td>$20 of every $100 bill, and $20,000 of every $100,000, with no ceiling</td></tr>
      <tr><td>9% of Advantage members are in plans at the legal maximum limit</td><td>About 1 in 11 members, 1.8 million people</td></tr>
      <tr><td>94% satisfied with the quality of their care</td><td>More than 9 in 10, in both programs</td></tr>
    </table>
    </div>
    <p>And the dollar figures, measured against the average retired worker's Social Security check of $2,071 a month:</p>
    <div class="tblwrap">
    <table class="nettbl">
      <tr><th>Cost</th><th>Equals about</th></tr>
      <tr><td>Premiums on Original Medicare + Plan G + drug plan: $432 a month (21% of the check)</td><td>$5,183 a year, about $2,750 a year more than Part B alone</td></tr>
      <tr><td>Premium on a $0 Advantage plan: Part B only, $203 a month (10%)</td><td>$2,435 a year</td></tr>
      <tr><td>Plan G in a bad year: $283</td><td>About four days of Social Security</td></tr>
      <tr><td>Average Advantage out-of-pocket limit: $5,421</td><td>About 2.6 months of Social Security</td></tr>
      <tr><td>Legal maximum Advantage limit: $9,250</td><td>About 4.5 months</td></tr>
      <tr><td>One $100,000 year on Original Medicare alone: $20,226</td><td>Nearly 10 months</td></tr>
      <tr><td>20 years of a supplement, drug plan and deductible: __LOW__ to __HIGH__</td><td>3.5 to 5.4 years of Social Security checks</td></tr>
    </table>
    </div>
    <p class="vstamp">Months and years are our arithmetic: the cost divided by $2,071 a month or $24,852 a year.</p>

    <h2>How many people are on Medicare Advantage?</h2>
    <p>In 2026, <strong>55% of eligible Medicare beneficiaries</strong> are enrolled in a Medicare Advantage plan, according to KFF. Enrollment passed 35 million people in February. In 2007 the share was 19%. Growth has slowed to about 3% a year, and most of the recent growth is in Special Needs Plans for people with Medicaid or chronic conditions, which now hold 8.2 million people, nearly 1 in 4 enrollees. Two companies, UnitedHealth Group and Humana, cover 46% of all Advantage members.</p>
    <p>So the first fact is simple: a majority of people who can choose are choosing it. That does not make it right for everyone, but it does mean the typical Advantage member is not a rare or confused exception.</p>

    <h2>Denials: what the data actually shows</h2>
    <p>Most Advantage plans require <strong>prior authorization</strong> for some services, meaning the plan must approve them before you get them. This is the heart of most complaints, so here is the full picture from KFF's analysis of CMS data.</p>
    __VIZ_PA__
    <ul>
      <li><strong>Volume:</strong> 52.8 million prior authorization requests in 2024.</li>
      <li><strong>Denials:</strong> 4.1 million fully or partly denied, <strong>7.7%</strong>, about 1 in 13.</li>
      <li><strong>Appeals:</strong> only <strong>11.5%</strong> of denials were appealed (about 1 in 9), and <strong>80.7%</strong> of those appeals reversed the denial in full or in part (about 4 in 5).</li>
      <li><strong>Newer data:</strong> insurers' own published figures for 2025, covering 14 large companies, show 12% of standard requests denied in Advantage and 67% of appealed denials overturned. The method differs from the CMS data, so the two years are not directly comparable.</li>
    </ul>
    <p>Two harder facts belong next to those. In 2022 the HHS Inspector General reviewed a sample of 2019 denials from 15 large plans and found that <strong>13% of denied prior authorization requests met Medicare's own coverage rules</strong>, about 1 in 8, meaning Original Medicare likely would have paid. And in 2024 a U.S. Senate investigation found UnitedHealthcare's denial rate for post-acute care (skilled nursing, rehab) rose from <strong>8.7% in 2019 to 22.7% in 2022</strong>, from about 1 in 11 requests to nearly 1 in 4, with post-acute denials at UnitedHealthcare and CVS running about three times their overall rates. The insurers dispute the report's conclusions.</p>
    <p>Original Medicare is not denial-free either. It requires prior authorization for far fewer services, about 2 requests per 100 people in 2024, but it denied about 23% of those, nearly 1 in 4. Since January 2026, a federal pilot called WISeR has added prior authorization to traditional Medicare for selected services in six states (Arizona, New Jersey, Ohio, Oklahoma, Texas and Washington).</p>
    <p><strong>What the denial numbers mean for you:</strong> the large majority of requests are approved, but if you are denied, appeal. Most people do not, and most people who do, win.</p>

    <h2>Why so many people dislike Medicare Advantage</h2>
    <p>The anger is not just emotion. Each of the common complaints has a documented basis, and it is worth knowing which is which.</p>
    <div class="stage"><span class="num">1</span><span class="st"><b>Denials, especially for rehab and nursing care.</b>The Inspector General and Senate findings above are the source of many stories people repeat, and the post-acute numbers are the strongest evidence behind them.</span></div>
    <div class="stage"><span class="num">2</span><span class="st"><b>Networks that change.</b>Becker's Hospital Review tracked about 40 health systems dropping some or all Advantage contracts in 2025, and at least 25 more in 2026, often citing prior authorization and slow payment. If your hospital leaves your plan's network, your plan may no longer cover care there except in emergencies.</span></div>
    <div class="stage"><span class="num">3</span><span class="st"><b>The marketing.</b>A 2022 Senate Finance Committee report found complaints to CMS about Advantage marketing more than doubled from 2020 to 2021. Many people's first impression of these plans is a late-night ad or a cold call, and that sticks.</span></div>
    <div class="stage"><span class="num">4</span><span class="st"><b>The cost to taxpayers.</b>Medicare's own advisory commission, MedPAC, estimates that Advantage plans will be paid about 14% more in 2026 than Original Medicare would have spent on the same people, about $76 billion, roughly $2,200 per Advantage member a year. MedPAC also estimates it makes Part B premiums $11 billion higher in total, roughly $15 a month for each person on Part B (our arithmetic). The industry disputes the method. This is a real policy debate about the program's cost, separate from what your own plan charges you.</span></div>
    <div class="stage"><span class="num">5</span><span class="st"><b>It can be hard to go back.</b>If you leave a supplement for an Advantage plan and later want the supplement again, insurers in most states can ask health questions and turn you down. Only Connecticut, Massachusetts, Maine and New York guarantee that right every year for people 65 and older. A federal trial right lets you return within 12 months of first joining an Advantage plan, but after that, the door may not open.</span></div>
    <p>Now the other side of the ledger, also from the research. KFF's review of 62 studies comparing the two programs found <strong>few big differences</strong> across a wide range of measures. Satisfaction is similar: in one analysis of federal survey data, 94% of people in each program said they were satisfied with the quality of their care. And Advantage members are more likely than people in Original Medicare to have incomes below $20,000, which matters for the next section.</p>

    <h2>What seniors actually live on</h2>
    <p>Any honest comparison has to start with the budget, because for most people the budget decides.</p>
    <ul>
      <li><strong>The average retired worker's Social Security check</strong> is about $2,071 a month in 2026, rising to about $2,170 in January 2027. For 12% of men and 15% of women 65 and older on Social Security, about 1 in 8 men and 1 in 7 women, it is 90% or more of their income.</li>
      <li><strong>Half of all people on Medicare</strong> live on less than $43,200 a year per person and have less than <strong>$110,100</strong> in savings. One in four has income below $24,600 and savings below $18,950.</li>
      <li><strong>Retirement accounts:</strong> only about half of households aged 65 to 74 have one at all. For those that do, the median balance is about $200,000.</li>
      <li><strong>Spending:</strong> households headed by someone 65 or older spent an average of $61,432 in 2024 on everything, according to the Bureau of Labor Statistics. That is a household figure; the average retired worker's check is about $24,900 a year.</li>
      <li><strong>Health costs already take a big bite:</strong> in 2023 people on Medicare spent an average of $6,459 out of pocket on health care, including premiums. That equals 36% of the average Social Security income per beneficiary: about $1 of every $3, or more than four months of benefits.</li>
    </ul>
    __VIZ_CHECK__
    <p>That is the first fact that drives many people toward Advantage: before any copay, Original Medicare with an average supplement and drug plan takes about one dollar in five from the average check in premiums. A $0-premium Advantage plan takes about one in ten.</p>

    <h2>Supplement premiums: how much, and how fast they rise</h2>
    <p>Medicare Supplement (Medigap) plans are excellent coverage: Plan G pays nearly everything Original Medicare leaves behind, at any doctor in the country who takes Medicare. The issue is price, and price over time.</p>
    <ul>
      <li>The <strong>average Medigap premium was $244 a month</strong> ($2,926 a year) among current policyholders in 2025, according to KFF's analysis of insurer data. Plan G averaged $194, ranging from $164 in New Mexico to $257 in New York.</li>
      <li>Premiums rose <strong>7% from 2024 to 2025</strong> (about $16 a month) <strong>and 20% from 2020 to 2025</strong> ($203 to $244 a month) on average; Plan G's average rose about 13% in 2025 alone, about $22 a month.</li>
      <li>Industry analysis of 2026 rate filings found Plan G increases of roughly 12% to 26% at several of the largest insurers. On a $194 premium, that is about $23 to $50 more a month.</li>
      <li>In most states, insurers price by <strong>attained age</strong>, so your premium also rises as you get older, on top of those yearly increases. KFF notes these policies are the cheapest at first and can be the most expensive over time.</li>
    </ul>
    <p>And the timing problem: the only point at which every insurer must sell you a supplement at its standard rate, regardless of health, is your <strong>six-month Medigap open enrollment period</strong>, which starts when you are 65 and enrolled in Part B. Certain events, such as losing retiree coverage, also create a guaranteed right. Miss those windows, or leave later, and in most states a heart condition, diabetes or a cancer history can mean higher rates or a denial. For many people, "just get a supplement" is not an option they actually have.</p>

    <h2>What a supplement costs over a lifetime</h2>
    <p>Here is the arithmetic for 20 years, age 65 to 85, using national figures. We leave out the Part B premium, because you pay it on every path.</p>
    <div class="tblwrap">
    <table class="nettbl">
      <tr><th>Assumption</th><th>Value</th><th>Basis</th></tr>
      <tr><td>Plan G premium at 65</td><td>$160 a month</td><td>national quotes for a new 65-year-old, about $155 to $160 (2025)</td></tr>
      <tr><td>Yearly increase, age and price together</td><td>5%, 8% or 10%</td><td>7% average in 2025; 12% to 26% filings in 2026</td></tr>
      <tr><td>Stand-alone drug plan</td><td>$35 a month, +5% a year</td><td>CMS 2026 average $35.09</td></tr>
      <tr><td>Part B deductible (Plan G does not pay it)</td><td>$283, +5% a year</td><td>CMS 2026; it was $166 in 2016</td></tr>
    </table>
    </div>
    __VIZ_LIFE__
    <p>So 20 years of a supplement, drug plan and deductible runs roughly <strong>__LOW__ to __HIGH__</strong>. For the median person on Medicare, that is somewhere between most of and more than their entire savings. For the one in four with under $18,950 saved, it is less than ten years of Plan G premiums alone at today's price.</p>
    <p>None of that makes a supplement a bad buy. It buys near-total protection and freedom to see any doctor, and for someone who can comfortably afford it, that can be worth every dollar. It does explain why so many people on fixed incomes look elsewhere.</p>

    <h2>Original Medicare alone vs. a Medicare Advantage plan</h2>
    <p>Some people skip a supplement and stay on Original Medicare by itself: about 3.5 million people, 13% of everyone in traditional Medicare, have no supplemental coverage at all. On premiums, this looks identical to a $0 Advantage plan: you pay Part B and nothing else. The difference is what happens in a bad year.</p>
    <ul>
      <li><strong>Original Medicare alone:</strong> after the $283 Part B deductible you pay 20% of every outpatient bill ($20 of every $100), plus $1,736 for each hospital stay's benefit period, with <strong>no yearly limit</strong>.</li>
      <li><strong>Medicare Advantage:</strong> every plan must cap your in-network Part A and B costs. The 2026 average limit is <strong>$5,421</strong>; the legal maximum is $9,250 (rising to $9,850 in 2027).</li>
    </ul>
    __VIZ_BAD__
    <p>It shows in people's lives. In KFF's analysis of federal survey data, people in Original Medicare with no supplement were the most likely of any group to report problems paying for care: 30%, about 3 in 10 (2018 data). People with a supplement were the least likely. Advantage members fell in between.</p>

    <h2>The case for a Medicare Advantage plan, in facts</h2>
    <p>Put the pieces together and the factual case for an Advantage plan with drug coverage (often called an MAPD) looks like this:</p>
    <ul>
      <li><strong>Low or no premium:</strong> about 3 in 4 people in these plans pay nothing beyond Part B. The average is $15 a month.</li>
      <li><strong>A hard yearly cap:</strong> unlike Original Medicare alone, your in-network costs stop at the plan's limit, $5,421 on average.</li>
      <li><strong>Drug coverage included</strong>, with the same $2,100 yearly drug cap (2026) as any Part D plan.</li>
      <li><strong>Benefits Original Medicare does not cover:</strong> more than 99% of members have some vision coverage, 98% dental and 95% hearing. How generous those benefits are varies widely by plan.</li>
      <li><strong>The break-even math:</strong> for a $0-premium plan to cost more than the supplement path over 20 years, your copays and coinsurance would have to average more than about <strong>__PERYR_LOW__ to __PERYR_HIGH__ a year, every year</strong>, which is roughly the average plan's entire out-of-pocket limit. Public data do not show how many members reach their limit, but by definition, the years you do not reach it cost less.</li>
    </ul>

    <h2>What a Medicare Advantage plan does not do</h2>
    <p>Facts cut both ways, and you should weigh these before choosing:</p>
    <ul>
      <li><strong>Networks.</strong> Most plans work best, or only, with in-network doctors and hospitals, and networks can change each year.</li>
      <li><strong>Prior authorization.</strong> Some care needs approval first, and denials, while a minority, do happen.</li>
      <li><strong>A bad year costs more than a supplement.</strong> In a year you hit the cap, you pay up to the cap; with Plan G you would pay about $283.</li>
      <li><strong>Travel and second homes.</strong> Coverage away from home is usually limited to emergencies, unless the plan is a PPO or has a travel benefit.</li>
      <li><strong>The way back may close.</strong> Returning to a supplement later can depend on your health.</li>
    </ul>

    <h2>Who each path tends to fit</h2>
    <div class="tblwrap">
    <table class="nettbl">
      <tr><th>Path</th><th>Tends to fit people who</th></tr>
      <tr><td><b>Original Medicare + supplement + drug plan</b></td><td>can comfortably afford rising premiums for decades, want any doctor in the country, travel or split time between states, or expect heavy care, and are buying during their open enrollment window</td></tr>
      <tr><td><b>Medicare Advantage with drug coverage</b></td><td>are on a fixed income, want a yearly cap with little or no premium, have their doctors and hospital in the plan's network, and value dental, vision and hearing benefits</td></tr>
      <tr><td><b>Original Medicare alone</b></td><td>rarely fits on its own; it works mainly for people with other coverage that fills the gaps, such as retiree coverage, Medicaid, or VA care</td></tr>
    </table>
    </div>

    <div class="note">
      <div class="who">
        <span class="duo"><img src="/assets/austin-tyler.jpg" alt="Austin Tyler" width="600" height="750"><img src="/assets/andrew-horn.jpg" alt="Andrew Horn" width="600" height="750"></span>
        <div><b>A note from our advisors</b><span>Tyler Insurance Group</span></div>
      </div>
      <p>We sell both supplements and Advantage plans, and we hear strong feelings about both every week. The numbers on this page are why we do not start with feelings. A $0-premium plan with a cap is a real financial safety net for someone living on a $2,000 check, and a supplement is real peace of mind for someone who can carry the premium for twenty years.</p>
      <p>The right answer depends on your budget, your doctors, your health and where you live. Bring those four things and we will lay the numbers side by side for you, the same way we did here.</p>
    </div>

    <h2 id="faq">Common questions</h2>
    <div class="faq">
      <h3>How many people are on Medicare Advantage?</h3>
      <p>In 2026, 55% of eligible Medicare beneficiaries, more than 35 million people, are enrolled in Medicare Advantage, according to KFF. The share was 19% in 2007. About 8.2 million are in Special Needs Plans.</p>
      <h3>How often do Medicare Advantage plans deny prior authorization?</h3>
      <p>In 2024, Medicare Advantage plans fully or partly denied 7.7% of 52.8 million prior authorization requests, according to KFF's analysis of CMS data. Only 11.5% of denials were appealed, and 80.7% of appeals overturned the denial in full or in part. Insurer-published data for 2025 show 12% of standard requests denied.</p>
      <h3>Why do so many people dislike Medicare Advantage?</h3>
      <p>The main documented reasons are prior authorization denials (including findings by the HHS Inspector General and a 2024 Senate investigation into post-acute care), health systems leaving plan networks, aggressive marketing, federal estimates that plans are paid about 14% more than Original Medicare would cost, and the difficulty of returning to a Medigap supplement later because most states allow medical underwriting.</p>
      <h3>How much does a Medicare Supplement cost over a lifetime?</h3>
      <p>The average Medigap premium was $244 a month in 2025, and Plan G averaged $194. Using $160 a month at age 65 with yearly increases of 5% to 10%, plus a drug plan and the Part B deductible, 20 years costs roughly __LOW__ to __HIGH__, excluding the Part B premium. Actual costs depend on your state, insurer, age and rate increases.</p>
      <h3>Is Original Medicare alone cheaper than Medicare Advantage?</h3>
      <p>On premiums they can be the same, since both may cost only the Part B premium. The difference is risk: Original Medicare alone has no yearly limit on the 20% you pay, so a year with $100,000 of outpatient care would cost about $20,226, while a Medicare Advantage plan caps in-network costs at its limit, $5,421 on average in 2026.</p>
      <h3>Can I switch from Medicare Advantage back to a Medigap plan?</h3>
      <p>You can apply at any time, but outside your six-month Medigap open enrollment period and certain federal guaranteed-issue events, insurers in most states can ask health questions and deny you or charge more. Connecticut, Massachusetts, Maine and New York guarantee issue every year for people 65 and older. If you joined Medicare Advantage when first eligible, a federal trial right lets you switch back within 12 months.</p>
    </div>

    <div class="endcta">
      <h3>Want your own numbers side by side?</h3>
      <p>Bring your budget, your doctors and your prescriptions. We will compare a supplement, an Advantage plan and your current coverage for your situation, at no charge.</p>
      <div class="row">
        <a class="btn" href="/schedule/">Book a free review &rarr;</a>
        <p class="callline">Or call us directly: <a href="tel:18597858289">(859) 785-8289</a></p>
      </div>
    </div>

    <section class="recap">
      <h2>Quick recap</h2>
      <div class="recap-item">55% of eligible people, over 35 million, are on Medicare Advantage in 2026.</div>
      <div class="recap-item">2024 prior authorization: 7.7% denied, 11.5% of denials appealed, 80.7% of appeals won. The Inspector General found 13% of sampled denials met Medicare rules.</div>
      <div class="recap-item">The distrust has documented causes: post-acute denials, networks, marketing, payment levels, and the hard road back to a supplement.</div>
      <div class="recap-item">Half of people on Medicare have savings under $110,100; the average retired worker's check is about $2,071.</div>
      <div class="recap-item">Medigap averaged $244 a month in 2025, up 20% in five years. Twenty years of Plan G plus a drug plan: roughly __LOW__ to __HIGH__.</div>
      <div class="recap-item">Original Medicare alone has no cap: one $100,000 year can cost about $20,226. Advantage plans cap in-network costs, $5,421 on average.</div>
      <div class="recap-item">A supplement buys freedom and near-total protection; an Advantage plan buys a cap and extras for little or no premium. Budget, doctors and health decide.</div>
    </section>

    <section class="kcheck">
      <h2>Test what you learned</h2>
      <p class="kc-sub">Five quick questions. Pick an answer to see if you're right, and why.</p>
      <div id="kcheck"></div>
    </section>
    <script>window.KCHECK = __KCHECK__;</script>

    <div class="sources">
      <b>Sources</b>
      KFF, "Medicare Advantage in 2026: Enrollment Update and Key Trends" and "Medicare Advantage in 2026: Premiums, Out-of-Pocket Limits, Supplemental Benefits, and Prior Authorization" &middot;
      KFF, "Medicare Advantage Insurers Made Nearly 53 Million Prior Authorization Determinations in 2024" and "Prior Authorization Metrics Provide New Insights into Insurer Practices, but Gaps Remain" (2026), with Fierce Healthcare and MedCity News &middot;
      HHS Office of Inspector General, OEI-09-18-00260 (April 2022) &middot;
      U.S. Senate Permanent Subcommittee on Investigations, "Refusal of Recovery" (October 2024), as reported by Healthcare Dive, McKnight's and the Center for Medicare Advocacy &middot;
      U.S. Senate Finance Committee, "Deceptive Marketing Practices Flourish in Medicare Advantage" (November 2022) &middot;
      MedPAC, March 2026 Report to the Congress, chapter 12 &middot;
      Becker's Hospital Review, health systems dropping Medicare Advantage contracts, 2025 and 2026 &middot;
      CMS WISeR model, as summarized by the Congressional Research Service and Kiplinger &middot;
      KFF, "Key Facts About Medigap Enrollment and Premiums" (NAIC data, 2025) and "Medigap Guaranteed Issue Requirements" &middot;
      KFF, "A Review of 62 Studies", "Cost-Related Problems Are Less Common Among Beneficiaries in Traditional Medicare Than in Medicare Advantage, Mainly Due to Supplemental Coverage", "A Snapshot of Sources of Coverage Among Medicare Beneficiaries", and "Key Facts About Health Care Affordability for People With Medicare"; Commonwealth Fund (satisfaction) &middot;
      KFF and Urban Institute DYNASIM, income and assets of Medicare beneficiaries, 2024 &middot;
      Federal Reserve Survey of Consumer Finances 2022, as reported by Yahoo Finance and The Motley Fool &middot; Bureau of Labor Statistics Consumer Expenditure Survey 2024, age 65 and older (FRED series CXUTOTALEXPLB0407M) &middot;
      Social Security Administration, 2026 and 2027 COLA fact sheets and Social Security basic facts &middot;
      CMS, 2026 Medicare Parts A and B premiums and deductibles &middot;
      Industry analysis of 2026 Medigap rate filings (Telos Actuarial, as reported by MedicareFAQ and others); new-enrollee Plan G quotes from ValuePenguin and MedicareSupplement.com.
      Checked November 3, 2026. Lifetime and per-1,000 figures are our arithmetic and are labeled as such.
    </div>

    <p class="stamp"><b>Written and reviewed by Austin Tyler</b>, Licensed Medicare Advisor, NPN 20234188, Kentucky DOI license #1187780. Every figure was confirmed against at least two sources or a primary government source.</p>

    <p class="disclaim">This article is general information, not advice for your specific situation. National averages hide wide differences by state, insurer, age and health; your own costs will differ. Lifetime figures are illustrations built on stated assumptions, not predictions. No specific plan is named or recommended. Tyler Insurance Group is not connected with or endorsed by the United States government or the federal Medicare program. We do not offer every plan available in your area. Currently we represent 6 organizations which offer 158 products in your area. Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance Program (SHIP) to get information on all of your options.</p>
"""
for key, val in [("__VIZ_PA__", VIZ_PA), ("__VIZ_CHECK__", VIZ_CHECK), ("__VIZ_LIFE__", VIZ_LIFE), ("__VIZ_BAD__", VIZ_BAD),
                 ("__DATE_LONG__", DATE_LONG)]:
    assert BODY.count(key) == 1, key; BODY = BODY.replace(key, val)
BODY = (BODY.replace("__LOW__", k(LOW)).replace("__HIGH__", k(HIGH))
            .replace("__PERYR_LOW__", usd(PERYR_LOW)).replace("__PERYR_HIGH__", usd(PERYR_HIGH)))

KCHECK = [
 {"q": "Roughly what share of eligible Medicare beneficiaries are on Medicare Advantage in 2026?",
  "options": ["About 1 in 5", "About a third", "55%", "Nearly 90%"], "answer": 2,
  "why": "KFF reports 55% of eligible beneficiaries, more than 35 million people, in 2026, up from 19% in 2007."},
 {"q": "In 2024, what happened to most Medicare Advantage prior authorization denials that were appealed?",
  "options": ["Almost all were upheld", "About 4 in 5 were overturned in full or in part", "Appeals are not allowed", "They went to court"], "answer": 1,
  "why": "80.7% of appeals reversed the denial in full or in part. The catch: only 11.5% of denials were appealed at all."},
 {"q": "You have been on an Advantage plan for five years and want a Plan G supplement. In most states, what can happen?",
  "options": ["You must be accepted at standard rates", "The insurer can ask health questions and decline or charge more", "Medicare assigns you a plan", "You must wait until 70"], "answer": 1,
  "why": "Outside your first six months on Part B and certain federal events, most states allow medical underwriting. Only CT, MA, ME and NY guarantee issue every year for people 65 and older."},
 {"q": "With Original Medicare alone and no supplement, about how much would you owe for $100,000 of Medicare-approved outpatient care in one year (2026)?",
  "options": ["$283", "$5,421", "About $20,226", "Nothing"], "answer": 2,
  "why": "You pay the $283 Part B deductible and 20% of the rest, with no yearly cap. An Advantage plan would stop at its limit; Plan G would leave only the $283."},
 {"q": "On the average $2,071 Social Security check, about how much do Part B, an average Plan G and an average drug plan take in premiums?",
  "options": ["About 5%", "About 10%", "About 21%", "About 50%"], "answer": 2,
  "why": "$202.90 + $194 + $35 is about $432, roughly 21% of $2,071. A $0-premium Advantage plan with drug coverage leaves just the Part B premium, about 10%."},
]
body_html = BODY.replace("__KCHECK__", json.dumps(KCHECK, ensure_ascii=False))
assert "__" not in re.sub(r"window\.KCHECK", "", body_html.split("<script>window.KCHECK")[0])

out = re.sub(r'(<nav class="crumb" aria-label="Breadcrumb">).*?(</nav>)',
             r'\1<a href="/">Home</a> &rsaquo; <a href="/articles/">Learning Center</a> &rsaquo; <a href="/articles/coverage/">Coverage Choices</a> &rsaquo; '
             + CRUMB_LABEL + r'\2', out, count=1, flags=re.S)
out = re.sub(r'<span class="tag">.*?</span>', '<span class="tag">Coverage Choices · Costs &amp; Savings</span>', out, count=1, flags=re.S)
out = re.sub(r'<h1>.*?</h1>', f'<h1>{H1}</h1>', out, count=1, flags=re.S)
out = re.sub(r'(Licensed Medicare Advisor, Tyler Insurance Group · )[^<]*(</div>)', r'\g<1>' + DATE_LONG + r' · 14 min read\2', out, count=1)
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
        node.update({"headline": H1, "description": DESC, "datePublished": DATE, "dateModified": DATE,
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
head = out.split('<div class="body">')[0]
assert "3.6%" not in head and "2027 Social Security" not in head, "template text left in head"

os.makedirs(f"articles/{SLUG}", exist_ok=True)
open(f"articles/{SLUG}/index.html", "w", encoding="utf-8").write(out)
print(f"wrote articles/{SLUG}/index.html ({len(pairs)} FAQ, {len(KCHECK)} kcheck); 20-yr {k(LOW)} / {k(MID)} / {k(HIGH)}; per-yr {usd(PERYR_LOW)}-{usd(PERYR_HIGH)}")
