#!/usr/bin/env python3
"""Build /articles/2027-social-security-raise-medicare-costs/ from the current article chrome.
Facts and sources: docs/dossiers/2027-social-security-medicare-numbers.md. When CMS announces the
2027 Part B premium, update PARTB below and the projected wording, then rebuild."""
import json, re, os, html as H

SRC = "articles/90-dollar-medicare-payment-kentucky/index.html"
OLD_URL = "https://www.bluegrassmedicarehelp.com/articles/90-dollar-medicare-payment-kentucky/"
SLUG = "2027-social-security-raise-medicare-costs"
URL = f"https://www.bluegrassmedicarehelp.com/articles/{SLUG}/"
TITLE = "2027 Social Security Raise and Medicare Costs: The Numbers"
H1 = "The 2027 Social Security Raise and Medicare Costs: What's Official, What's Coming, and What It Means for Your Check"
DESC = ("Social Security rises 3.6% in January 2027. Here is what that means after the Part B premium, plus the official "
        "2027 drug plan, Medicare Advantage and Medigap numbers, and what Kentuckians should do before December 7.")
CRUMB_LABEL = "2027 Raise and Medicare Costs"
DATE, DATE_LONG = "2026-11-02", "November 2, 2026"

src = open(SRC, encoding="utf-8").read()
out = src
out = out.replace("</style>", """
.nettbl .proj{display:block;font-size:12.5px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--coral-d);margin-top:2px;}
@media(max-width:520px){.nettbl{font-size:15px;} .nettbl th,.nettbl td{padding:10px 9px;}}
.tlfig{margin:18px 0 6px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px 20px 4px;}
.tlfig figcaption{font-family:var(--serif);font-weight:700;font-size:19px;color:var(--ink);margin:0 0 16px;}
.tl{list-style:none;margin:0;padding:0;}
.tl li{position:relative;padding:0 0 18px 40px;}
.tl li::before{content:"";position:absolute;left:0;top:1px;width:24px;height:24px;border-radius:50%;background:var(--ink);box-sizing:border-box;
  color:#fff;font-size:15px;font-weight:700;line-height:24px;text-align:center;}
.tl li::after{content:"";position:absolute;left:11px;top:27px;bottom:2px;width:3px;background:var(--line);}
.tl li:last-child::after{display:none;}
.tl li.done::before{content:"\\2713";background:#2f6844;}
.tl li.next::before{background:#fff;border:3px solid var(--coral-d);}
.tl b{display:block;font-size:17px;color:var(--ink);line-height:1.3;}
.tl li.next b{color:var(--coral-d);}
.tl span{display:block;font-size:16px;color:var(--mute);line-height:1.45;margin-top:2px;}
</style>""", 1)
old_title = re.search(r"<title>(.*?)</title>", out).group(1)
old_desc = re.search(r'<meta name="description" content="([^"]*)"', out).group(1)
out = out.replace(old_title, TITLE).replace(old_desc, DESC).replace(OLD_URL, URL)

# chart palette: the 2026 tokens
F = 'font-family="Source Sans 3, Arial, sans-serif"'
INK, MUTE, LINE, WARM, GREEN_D, CORAL_D = "#1b2836", "#4a5563", "#e3e8ee", "#fff0e8", "#2f6844", "#b23c17"
def viz(label, w, h, inner, cap):
    return (f'<figure class="viz" role="img" aria-label="{label}">\n<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><g {F}>\n{inner}\n</g></svg></figure>\n<p class="vizcap">{cap}</p>')

# Figure 1: the raise against the projected premium change (600 wide so the text stays readable on a phone)
VIZ_NET = viz("Three bars for the average retired worker. The Social Security raise adds about $75 a month. The projected Part B premium increase takes back about $6.60. What is left is about $68 more a month.", 420, 286,
    f'<text x="210" y="30" text-anchor="middle" font-size="20" font-weight="700" fill="{INK}">The average retiree, January 2027</text>'
    f'<text x="20" y="70" font-size="17" fill="{MUTE}">3.6% Social Security raise</text>'
    f'<rect x="20" y="80" width="380" height="38" rx="8" fill="{GREEN_D}"/>'
    f'<text x="386" y="106" text-anchor="end" font-size="19" font-weight="700" fill="#fff">+$75</text>'
    f'<text x="20" y="148" font-size="17" fill="{MUTE}">Projected Part B increase</text>'
    f'<rect x="20" y="158" width="34" height="38" rx="8" fill="{CORAL_D}"/>'
    f'<text x="66" y="184" font-size="19" font-weight="700" fill="{CORAL_D}">&#8722;$6.60</text>'
    f'<rect x="20" y="214" width="380" height="56" rx="12" fill="{WARM}" stroke="{CORAL_D}" stroke-width="2"/>'
    f'<text x="210" y="250" text-anchor="middle" font-size="21" font-weight="700" fill="{INK}">About $68 more a month</text>',
    "Figure 1. The raise is about eleven times the projected premium increase. Raise from the SSA 2027 fact sheet (average retired-worker benefit about $2,095 to $2,170); premium from the 2026 Medicare Trustees Report projection ($202.90 to $209.50). The real 2027 premium comes from CMS in November.")

# Figure 2: what is out and what is still coming (HTML, so it stays readable on a phone)
STEPS = [("done", "April", "Drug plan deductible $700 and cap $2,400; Advantage out-of-pocket ceilings"),
         ("done", "July 28", "Drug plan base premium $41.33; the extra drug-plan premium subsidy ends"),
         ("done", "October 14", "Social Security raise: 3.6%"),
         ("done", "October", "Medigap Plan K, Plan L and high-deductible Plan G limits"),
         ("next", "Mid-November (still to come)", "Part B premium and deductible, Part A, IRMAA income brackets"),
         ("", "December 7", "Last day to change your plan for 2027"),
         ("", "January 1, 2027", "Everything above takes effect")]
VIZ_TIME = ('<figure class="tlfig"><figcaption>2027 numbers: what is out, what is coming</figcaption><ol class="tl">'
            + "".join(f'<li class="{c}"><b>{w}</b><span>{t}</span></li>' for c, w, t in STEPS)
            + '</ol></figure>\n<p class="vizcap">Figure 2. Green checks are final. The open circle is the one big number still to come, which CMS usually announces in November.</p>')

BODY = r"""
    <p class="updated">Updated __DATE_LONG__. Social Security's 2027 numbers are final. Medicare's 2027 Part B premium has <strong>not</strong> been announced yet; CMS usually releases it in mid-November, and we will update this page when it does. Until then, the Part B figures below are the official projection and are labeled that way.</p>
    <p>Two envelopes decide most of your 2027 budget: Social Security's cost-of-living notice and Medicare's premium announcement. The first one is out, and it is good news. The second one is a few weeks away. Here is everything that is official for 2027, what is still a projection, what it means for the check that lands in January, and the one decision you need to make before December 7.</p>

    <div class="ans">
      <p><strong>The short version:</strong></p>
      <ul>
        <li><strong>Social Security goes up 3.6% in January 2027.</strong> For the average retired worker that is about $75 a month, from about $2,095 to about $2,170. It is the biggest raise in several years.</li>
        <li><strong>The 2027 Part B premium is not out yet.</strong> The official projection is about <strong>$209.50</strong> a month, up $6.60 from $202.90. If that holds, the average retiree keeps about $68 of the $75 raise.</li>
        <li><strong>Drug plans are where 2027 can surprise you.</strong> The deductible rises to $700 and the yearly cap to $2,400, and the extra federal help that held stand-alone drug plan premiums down has ended. There will be no $0-premium stand-alone drug plans for people without Extra Help.</li>
        <li><strong>Medicare Advantage premiums are projected to fall</strong>, but the highest out-of-pocket limit a plan can set rises to $9,850 in-network.</li>
        <li><strong>What to do now:</strong> compare your drug coverage for 2027 before the Annual Enrollment Period ends on <strong>December 7</strong>. That is the decision with real dollars in it.</li>
      </ul>
    </div>

    <h2>The 2027 numbers at a glance</h2>
    <div class="tblwrap">
    <table class="nettbl">
      <tr><th>What</th><th>2026</th><th>2027</th></tr>
      <tr><td>Social Security cost-of-living raise</td><td>2.8%</td><td><b>3.6%</b></td></tr>
      <tr><td>Average retired-worker benefit</td><td>about $2,095</td><td>about $2,170</td></tr>
      <tr><td>Part B standard premium</td><td>$202.90</td><td>about $209.50 <span class="proj">Projected</span></td></tr>
      <tr><td>Part B deductible</td><td>$283</td><td>about $292 <span class="proj">Projected</span></td></tr>
      <tr><td>IRMAA income brackets</td><td>start at $109,000 single, $218,000 joint</td><td>with the premium <span class="proj">Not yet</span></td></tr>
      <tr><td>Part D drug deductible (maximum)</td><td>$615</td><td>$700</td></tr>
      <tr><td>Part D out-of-pocket cap</td><td>$2,100</td><td>$2,400</td></tr>
      <tr><td>Advantage out-of-pocket ceiling, in-network</td><td>$9,250</td><td>$9,850</td></tr>
      <tr><td>Advantage PPO ceiling, in and out of network</td><td>$13,900</td><td>$14,800</td></tr>
      <tr><td>Medigap Plan K / Plan L out-of-pocket limit</td><td>$8,000 / $4,000</td><td>$8,360 / $4,180</td></tr>
      <tr><td>High-deductible Plan G deductible</td><td>$2,950</td><td>$3,050</td></tr>
      <tr><td>Earnings limit if you claim before full retirement age</td><td>$24,480</td><td>$25,560</td></tr>
      <tr><td>Earnings subject to Social Security tax</td><td>$184,500</td><td>$192,300</td></tr>
      <tr><td>SSI federal payment, individual / couple</td><td>$994 / $1,491</td><td>$1,029 / $1,544</td></tr>
    </table>
    </div>
    <p class="vstamp">Every 2027 figure is official unless marked. Projections are from the 2026 Medicare Trustees Report. Official figures were published by the Social Security Administration or CMS between April and October 2026.</p>
    __VIZ_TIME__

    <h2>Your Social Security raise</h2>
    <p>The Social Security Administration announced on October 14 that benefits rise <strong>3.6% for 2027</strong>, up from 2.8% this year. The raise is set by a federal formula that compares consumer prices over the summer to the year before, so it is automatic: there is nothing to apply for.</p>
    <p>For the average retired worker, the monthly benefit goes from about $2,095 to about $2,170. Someone receiving $1,500 a month gets about $54 more; someone receiving $2,500 gets about $90 more. The higher amount starts with your January 2027 payment, paid on your usual January date. People on SSI see their increase a little sooner, in the payment dated December 31, 2026.</p>
    <p>Your own figure will be on your COLA notice. Social Security mails those in December. If you use my Social Security, the agency's online account, and have chosen online notices, you can see yours there earlier. That notice is worth keeping: it also shows the Medicare premium that will come out of your check.</p>

    <h2>The Part B premium: what we know, and when the real number comes</h2>
    <p>If you are on Social Security and Medicare, your Part B premium comes out of your check before it reaches you. That is why the two announcements belong together, and why the second one matters to the first.</p>
    <p>CMS has not announced the 2027 premium yet. It usually does in November, often in the middle of the month. The best number we have is the projection in this year's Medicare Trustees Report: <strong>about $209.50 a month, up $6.60</strong> from $202.90, with the Part B deductible going from $283 to about $292. That would be a far smaller increase than this year's $17.90 jump. Projections can move, and some private forecasters expect a higher figure, so treat $209.50 as a planning number, not a promise.</p>
    __VIZ_NET__
    <p>Even if the premium comes in higher than projected, the math is lopsided: the average raise is about $75, so the premium would have to rise by more than that before the typical check went down. For most people, January's deposit will be noticeably larger.</p>
    <p><strong>If you pay IRMAA</strong>, the income-based surcharge for higher earners, your 2027 amount will be based on your 2025 tax return, and the new brackets come out with the premium. If your income has dropped since 2025 because you retired, stopped working or lost a spouse, you can ask Social Security to use a more recent year on form SSA-44. Our guide to <a href="/articles/medicare-irmaa-high-income-surcharge/">the IRMAA surcharge</a> walks through it.</p>
    <p>Received the one-time $90 Part B payment in October? It does not change the 2027 premium; see <a href="/articles/90-dollar-medicare-payment-kentucky/">who got the $90 and why</a>.</p>

    <h2>Drug coverage: the change most worth checking</h2>
    <p>The protection is still strong: once your covered drug costs reach <strong>$2,400</strong> for the year, you pay nothing more for covered drugs, and insulin stays at $35 a month. But three things moved underneath it for 2027.</p>
    <ul>
      <li><strong>The deductible rises to $700</strong>, from $615. Many plans charge less, but in a plan that uses the full amount, January and February prescriptions cost more before coverage kicks in.</li>
      <li><strong>The extra federal subsidy ended.</strong> For 2025 and 2026, Medicare paid stand-alone drug plans extra to keep premiums down. CMS ended that program after 2026. CMS expects the average stand-alone premium to rise less than a dollar, to about $36. KFF's analysis is less reassuring: if nobody switched, the average premium would rise about 50%, and some plans rise far more.</li>
      <li><strong>No $0-premium stand-alone plans.</strong> KFF found that in 2027 there are no stand-alone drug plans with a $0 premium for people who do not get Extra Help. About 4 million people were in one this year nationwide. If you are one of them, staying put means paying a premium in January.</li>
    </ul>
    <p>The average person also has fewer stand-alone plans to choose from, nine instead of eleven. The good news on the other side: Medicare's second round of negotiated drug prices, which includes Ozempic, Wegovy and Rybelsus, takes effect January 1. Our <a href="/articles/medicare-changes-2027-kentucky/">2027 Medicare changes guide</a> covers that list.</p>
    <p>The practical point: if you have a Medigap policy and a stand-alone drug plan, <strong>this is the year to compare your drug plan</strong> rather than let it renew. Your Annual Notice of Change shows what your current plan will charge; a side-by-side check of your exact prescriptions shows whether another plan charges less.</p>

    <h2>Medicare Advantage: lower premiums, higher ceilings</h2>
    <p>CMS projects the average Medicare Advantage premium will fall from $14.37 to about $12 a month in 2027, and most people can keep their current plan at the same or a lower premium. That matters in Kentucky, where 562,671 of the state's 1,012,834 Medicare beneficiaries, about 56%, are on an Advantage plan.</p>
    <p>The ceiling went the other way. The most a plan can make you pay out of pocket for in-network care in a year rises to <strong>$9,850</strong>, from $9,250, and the combined in- and out-of-network ceiling for PPOs rises to $14,800. Those are maximums; many plans set their own limit lower, and that plan-specific number is the one to find in your Annual Notice of Change. If the terms are a blur, our guide to <a href="/articles/medicare-advantage-premium-deductible-copay-coinsurance-explained/">premium, deductible, copay and coinsurance</a> explains which number to look at. The average person also has fewer Advantage drug plans to pick from, 28 instead of 32, so if your plan is leaving, start comparing now.</p>

    <h2>Medigap: three numbers that moved</h2>
    <p>If you have a Medicare Supplement, the standard plans do not change, but three limits rise with inflation. <strong>Plan K's</strong> yearly out-of-pocket limit goes to $8,360 and <strong>Plan L's</strong> to $4,180. The <strong>high-deductible Plan G</strong> deductible rises to $3,050. Plan G and Plan N holders should still expect their own premium notices from their insurance company, which follow each company's schedule rather than January.</p>

    <h2>Still working, or helping someone on SSI?</h2>
    <p>If you claim Social Security before full retirement age and keep working, Social Security holds back $1 for every $2 you earn above <strong>$25,560</strong> in 2027. In the year you reach full retirement age, the limit is $67,920 and the hold-back is $1 for every $3, counting only earnings before the month you reach it. After that, there is no limit. Wages up to $192,300 are subject to the Social Security payroll tax. For how this fits with Medicare, see <a href="/articles/working-past-65-medicare/">working past 65</a>.</p>
    <p>SSI's federal payment rises to $1,029 a month for an individual and $1,544 for a couple. People with SSI usually qualify for Medicaid in Kentucky, which can also pay Medicare premiums; our guide to <a href="/articles/help-paying-for-medicare/">help paying for Medicare</a> covers the programs.</p>

    <h2>One more: telehealth stays through 2027</h2>
    <p>Congress extended Medicare's telehealth rules through December 31, 2027, so you can keep seeing your doctor by video, or by phone in some cases, from home. Telehealth for mental health from home is permanent.</p>

    <h2>Your to-do list before January</h2>
    <div class="stage"><span class="num">1</span><span class="st"><b>Compare your drug coverage by December 7.</b>Especially if you are in a stand-alone drug plan with a $0 premium this year. Use your exact prescription list, not the plan's star rating.</span></div>
    <div class="stage"><span class="num">2</span><span class="st"><b>Find your plan's own out-of-pocket limit.</b>It is in your Annual Notice of Change. The $9,850 figure is a ceiling, not your number.</span></div>
    <div class="stage"><span class="num">3</span><span class="st"><b>Budget with $209.50 for Part B until CMS announces.</b>We will update this page with the real premium, deductible and IRMAA brackets.</span></div>
    <div class="stage"><span class="num">4</span><span class="st"><b>Watch for your COLA notice.</b>It arrives in December (sooner online) and shows both your new benefit and the premium being deducted.</span></div>
    <div class="stage"><span class="num">5</span><span class="st"><b>If your income dropped since 2025 and you pay IRMAA</b>, file form SSA-44 with Social Security so your 2027 surcharge reflects your current income.</span></div>

    <div class="note">
      <div class="who">
        <span class="duo"><img src="/assets/austin-tyler.jpg" alt="Austin Tyler" width="600" height="750"><img src="/assets/andrew-horn.jpg" alt="Andrew Horn" width="600" height="750"></span>
        <div><b>A note from our advisors</b><span>Tyler Insurance Group, Lexington</span></div>
      </div>
      <p>Every November we get the same call: "My raise is supposed to be bigger than this." Usually the answer is the Part B premium coming out first, or a drug plan premium that went up in January. This year the raise is healthy and the projected Part B increase is small, so the risk sits mostly in drug plans.</p>
      <p>If you are on a stand-alone drug plan that cost nothing this year, please look at your Annual Notice of Change before December 7. That one letter is the difference between keeping most of your raise and handing part of it to a plan that no longer fits.</p>
    </div>

    <h2 id="faq">Common questions</h2>
    <div class="faq">
      <h3>How much is the Social Security raise for 2027?</h3>
      <p>Benefits rise 3.6% starting with the January 2027 payment, announced by the Social Security Administration on October 14, 2026. For the average retired worker that is about $75 a month, from about $2,095 to about $2,170. SSI payments rise 3.6% beginning with the payment dated December 31, 2026.</p>
      <h3>What is the Medicare Part B premium for 2027?</h3>
      <p>CMS had not announced it as of November 2, 2026; it usually does in November. The 2026 Medicare Trustees Report projects about $209.50 a month, up $6.60 from $202.90, with the Part B deductible rising from $283 to about $292. We will update this page when the official figures are released.</p>
      <h3>Will the Part B premium eat my 2027 Social Security raise?</h3>
      <p>Not for most people. If the premium rises to the projected $209.50, it goes up $6.60 a month, while the average raise is about $75, so the average retiree keeps about $68. People who pay the IRMAA surcharge or whose drug plan premium rises sharply could keep less.</p>
      <h3>What are the 2027 Medicare Part D deductible and out-of-pocket cap?</h3>
      <p>The maximum Part D deductible is $700 in 2027, up from $615, and the out-of-pocket cap on covered drugs is $2,400, up from $2,100. Insulin stays capped at $35 a month. KFF reports there are no $0-premium stand-alone drug plans for people without Extra Help in 2027.</p>
      <h3>What is the Medicare Advantage out-of-pocket maximum for 2027?</h3>
      <p>The highest in-network out-of-pocket limit a Medicare Advantage plan can set in 2027 is $9,850, up from $9,250. For PPOs, the combined in- and out-of-network ceiling is $14,800, up from $13,900. Many plans set lower limits; check your plan's Annual Notice of Change for its own figure.</p>
      <h3>What is the Social Security earnings limit for 2027?</h3>
      <p>If you are under full retirement age all year, Social Security withholds $1 for every $2 you earn above $25,560. In the year you reach full retirement age, it withholds $1 for every $3 above $67,920, counting only earnings before that month. There is no limit once you reach full retirement age.</p>
    </div>

    <div class="endcta">
      <h3>Want your 2027 numbers checked?</h3>
      <p>Bring your Annual Notice of Change and your prescription list. We will price your drugs against the 2027 plans in your county and tell you plainly whether to stay or switch, at no charge.</p>
      <div class="row">
        <a class="btn" href="/schedule/">Book a free review &rarr;</a>
        <p class="callline">Or call us directly: <a href="tel:18597858289">(859) 785-8289</a></p>
      </div>
    </div>

    <section class="recap">
      <h2>Quick recap</h2>
      <div class="recap-item">Social Security rises 3.6% in January 2027, about $75 a month for the average retired worker (about $2,095 to $2,170). SSI rises with the December 31 payment.</div>
      <div class="recap-item">The 2027 Part B premium is not announced yet. The official projection is about $209.50, up $6.60, with the deductible at about $292. CMS usually announces in November.</div>
      <div class="recap-item">If the projection holds, the average retiree keeps about $68 of the raise.</div>
      <div class="recap-item">Part D: $700 deductible, $2,400 cap, the extra premium subsidy has ended, and there are no $0-premium stand-alone plans without Extra Help.</div>
      <div class="recap-item">Medicare Advantage: average premium projected to fall to about $12, but the in-network out-of-pocket ceiling rises to $9,850.</div>
      <div class="recap-item">Medigap: Plan K limit $8,360, Plan L $4,180, high-deductible G deductible $3,050.</div>
      <div class="recap-item">Compare your drug coverage before December 7. Telehealth from home continues through 2027.</div>
    </section>

    <section class="kcheck">
      <h2>Test what you learned</h2>
      <p class="kc-sub">Five quick questions. Pick an answer to see if you're right, and why.</p>
      <div id="kcheck"></div>
    </section>
    <script>window.KCHECK = __KCHECK__;</script>

    <div class="sources">
      <b>Sources</b>
      Social Security Administration, 2027 Cost-of-Living Adjustment Fact Sheet, COLA announcement and advocates notice of October 14, 2026, and "SSI Federal Payment Amounts for 2027" (COLA, average benefit, taxable maximum, earnings test, SSI), with CNBC, Kiplinger and The Motley Fool, October 2026 &middot;
      2026 Medicare Trustees Report, as reported by AARP, Kiplinger and NCOA (2027 Part B premium and deductible projections) &middot;
      CMS, CY 2027 Medicare Advantage and Part D Rate Announcement, April 2026 (Part D deductible and cap), and Part D national average bid release of July 28, 2026 (base beneficiary premium, end of the premium stabilization demonstration) &middot;
      CMS press release, "Medicare Advantage and Medicare Prescription Drug Programs Expected to Remain Stable in 2027" (average premiums) &middot;
      KFF, "Medicare Part D Premiums and Cost Sharing in 2027", "The Average Monthly Premium for Medicare Part D Stand-Alone Plans Is Projected to Increase by 50%", and "Medicare Advantage Plan Availability Varies Widely by County for 2027" &middot;
      NCOA and CMS CY 2027 Part C bid materials as reported by MedicareGuide (Advantage out-of-pocket ceilings) &middot;
      CMS, CY 2027 Medigap Plans K and L out-of-pocket limits and high-deductible F, G and J announcements, October 2026 &middot;
      HHS telehealth.hhs.gov policy updates and American Bar Association Health Law Section (telehealth through 2027) &middot;
      CMS Medicare Advantage penetration file, August 2026, Kentucky extract.
      Checked November 2, 2026. Projections are labeled as projections.
    </div>

    <p class="stamp"><b>Written and reviewed by Austin Tyler</b>, Licensed Medicare Advisor, NPN 20234188, Kentucky DOI license #1187780. Every figure was confirmed against at least two sources; Social Security and CMS documents are the primary references.</p>

    <p class="disclaim">This article is general information, not advice for your specific situation. Figures are as published by the Social Security Administration and CMS on the dates noted; projections may differ from the final amounts. No specific plan is named or recommended. Tyler Insurance Group is not connected with or endorsed by the United States government or the federal Medicare program. We do not offer every plan available in your area. Currently we represent 6 organizations which offer 158 products in your area. Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance Program (SHIP) to get information on all of your options.</p>
"""
for k, v in [("__VIZ_NET__", VIZ_NET), ("__VIZ_TIME__", VIZ_TIME), ("__DATE_LONG__", DATE_LONG)]:
    assert BODY.count(k) == 1, k; BODY = BODY.replace(k, v)

KCHECK = [
 {"q": "How much do Social Security benefits rise in January 2027?",
  "options": ["2.8%", "3.6%", "5.9%", "They stay the same"], "answer": 1,
  "why": "The Social Security Administration announced a 3.6% cost-of-living raise on October 14, 2026, up from 2.8% for 2026. For the average retired worker that is about $75 a month."},
 {"q": "As of early November 2026, what is the official 2027 Part B premium?",
  "options": ["$202.90", "$209.50, final", "Not announced yet; about $209.50 is the projection", "$185.00"], "answer": 2,
  "why": "CMS usually announces the premium in November. The 2026 Medicare Trustees Report projects about $209.50, but that is a projection until CMS publishes the final figure."},
 {"q": "Your stand-alone drug plan had a $0 premium in 2026 and you do not get Extra Help. What should you expect for 2027?",
  "options": ["It stays $0 automatically", "A premium, because no $0 stand-alone plans exist for 2027 without Extra Help", "Medicare will move you to a new plan", "Your deductible goes away"], "answer": 1,
  "why": "KFF found no $0-premium stand-alone drug plans for people without Extra Help in 2027, after CMS ended the extra premium subsidy. Compare plans before December 7."},
 {"q": "Your Advantage plan's notice lists an out-of-pocket maximum of $6,700. The 2027 federal ceiling is $9,850. Which number is your limit?",
  "options": ["$9,850, the federal ceiling", "$6,700, your plan's own limit", "Whichever is higher", "Neither; Advantage plans have no limit"], "answer": 1,
  "why": "$9,850 is the most any plan may set for in-network care. Your plan's own limit, shown in its Annual Notice of Change, is the one that applies to you."},
 {"q": "You are 63, already claiming Social Security, and earning $35,560 in 2027. How much will Social Security hold back?",
  "options": ["Nothing", "$5,000", "$10,000", "All of it"], "answer": 1,
  "why": "Under full retirement age, Social Security holds back $1 for every $2 above $25,560. $35,560 is $10,000 over, so $5,000 is withheld. It is credited back once you reach full retirement age."},
]
body_html = BODY.replace("__KCHECK__", json.dumps(KCHECK, ensure_ascii=False))

out = re.sub(r'(<nav class="crumb" aria-label="Breadcrumb">).*?(</nav>)',
             r'\1<a href="/">Home</a> &rsaquo; <a href="/articles/">Learning Center</a> &rsaquo; <a href="/articles/costs/">Costs &amp; Savings</a> &rsaquo; '
             + CRUMB_LABEL + r'\2', out, count=1, flags=re.S)
out = re.sub(r'<span class="tag">.*?</span>', '<span class="tag">Costs &amp; Savings · Already on Medicare · Social Security</span>', out, count=1, flags=re.S)
out = re.sub(r'<h1>.*?</h1>', f'<h1>{H1}</h1>', out, count=1, flags=re.S)
out = re.sub(r'(Licensed Medicare Advisor, Tyler Insurance Group · )[^<]*(</div>)', r'\g<1>' + DATE_LONG + r' · 9 min read\2', out, count=1)
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
                     "articleSection": "Costs & Savings", "mainEntityOfPage": {"@type": "WebPage", "@id": URL}, "@id": URL + "#article"})
    elif t == "BreadcrumbList":
        node["itemListElement"] = [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.bluegrassmedicarehelp.com/"},
            {"@type": "ListItem", "position": 2, "name": "Learning Center", "item": "https://www.bluegrassmedicarehelp.com/articles/"},
            {"@type": "ListItem", "position": 3, "name": "Costs & Savings", "item": "https://www.bluegrassmedicarehelp.com/articles/costs/"},
            {"@type": "ListItem", "position": 4, "name": CRUMB_LABEL, "item": URL}]
    elif t == "FAQPage":
        node["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]
out = out[:mm.start(1)] + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + out[mm.end(1):]
assert "$90" not in re.sub(r'<a href="/articles/90-dollar[^>]*>.*?</a>|one-time \$90', "", out.split('<div class="body">')[0]), "template text left in head"

os.makedirs(f"articles/{SLUG}", exist_ok=True)
open(f"articles/{SLUG}/index.html", "w", encoding="utf-8").write(out)
print(f"wrote articles/{SLUG}/index.html ({len(pairs)} FAQ, {len(KCHECK)} kcheck)")
