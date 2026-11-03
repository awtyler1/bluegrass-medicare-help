#!/usr/bin/env python3
"""Build /articles/medicare-advantage-by-the-numbers/ from the current article chrome.
Facts, sources and the lifetime-cost assumptions: docs/dossiers/medicare-advantage-by-the-numbers.md.
Structure follows data-journalism practice: answer first, chart titles state the finding, natural
frequencies (per 1,000) instead of stacked percentages, ranges and a break-even instead of one
point estimate, published data kept separate from our own estimates, and a methods box."""
import json, re, os, html as H

SRC = "articles/2027-social-security-raise-medicare-costs/index.html"
OLD_URL = "https://www.bluegrassmedicarehelp.com/articles/2027-social-security-raise-medicare-costs/"
SLUG = "medicare-advantage-by-the-numbers"
URL = f"https://www.bluegrassmedicarehelp.com/articles/{SLUG}/"
TITLE = "Medicare Advantage by the Numbers: Denials, Costs and Facts"
H1 = "Medicare Advantage, by the Numbers"
DEK = ("More than half of Medicare now runs through private plans, and few topics draw stronger opinions. "
       "We set the opinions aside and went through the public data on denials, costs and the alternatives.")
DESC = ("How many people are on Medicare Advantage, how often plans deny care, why the program draws so much criticism, "
        "and what a Medicare Supplement, Original Medicare alone and an Advantage plan cost over 20 years, from public data.")
CRUMB_LABEL = "Medicare Advantage by the Numbers"
DATE, DATE_LONG = "2026-11-03", "November 3, 2026"

# ---- the 20-year model (every input is printed in the methods box)
YEARS, PLAN_G, PDP, PARTB_DED, MA_AVG, MA_MAX = 20, 160, 35, 283, 5421, 9250
def path_year(r, k): return PLAN_G * 12 * (1 + r) ** k + PDP * 12 * 1.05 ** k + PARTB_DED * 1.05 ** k
def cumulative(yearly):
    c, out = 0, []
    for k in range(YEARS):
        c += yearly(k); out.append(c)
    return out
SUP = {r: cumulative(lambda k, r=r: path_year(r, k)) for r in (.05, .08, .10)}
MA_AVG_CUM = cumulative(lambda k: MA_AVG * 1.05 ** k)
MA_MAX_TOT = cumulative(lambda k: MA_MAX * 1.05 ** k)[-1]
k_ = lambda x: f"${round(x / 1000):,}k"
LOW, MID, HIGH = SUP[.05][-1], SUP[.08][-1], SUP[.10][-1]
BE = {r: (round(SUP[r][-1] / MA_AVG_CUM[-1] * YEARS), round(SUP[r][-1] / MA_MAX_TOT * YEARS)) for r in SUP}
BAD_YEAR = 283 + 0.2 * (100000 - 283)
assert round(BAD_YEAR) == 20226 and BE[.05] == (10, 6) and BE[.10] == (15, 9)

src = open(SRC, encoding="utf-8").read()
out = src
old_title = re.search(r"<title>(.*?)</title>", out).group(1)
old_desc = re.search(r'<meta name="description" content="([^"]*)"', out).group(1)
out = out.replace(old_title, TITLE).replace(old_desc, DESC).replace(OLD_URL, URL)
out = out.replace("</style>", """
.dek{font-size:20px;line-height:1.5;color:var(--mute);margin:10px 0 0;max-width:680px;}
.findings{border-top:3px solid var(--ink);border-bottom:1px solid var(--line);padding:18px 0 6px;margin:0 0 30px;}
.findings h2{font-size:15px;letter-spacing:.08em;text-transform:uppercase;margin:0 0 12px;color:var(--ink);}
.findings ol{margin:0;padding-left:22px;} .findings li{font-size:17.5px;line-height:1.55;margin:0 0 12px;}
.viz .vt{font-family:var(--serif);font-weight:700;font-size:19px;line-height:1.3;color:var(--ink);margin:2px 4px 2px;}
.viz .vs{font-size:14.5px;color:var(--mute);margin:0 4px 6px;}
.disclose{font-size:15px;color:var(--mute);border-left:3px solid var(--line);padding:4px 0 4px 14px;margin:0 0 26px;}
.methods{background:var(--cream2);border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin:32px 0 10px;}
.methods h2{font-size:20px;margin:0 0 10px;} .methods p,.methods li{font-size:15.5px;line-height:1.55;color:var(--ink);}
.methods ul{padding-left:20px;margin:0 0 10px;}
</style>""", 1)

F = 'font-family="Source Sans 3, Arial, sans-serif"'
INK, MUTE, LINE, GREEN_D, CORAL_D, GRAY, NAVY_L = "#1b2836", "#4a5563", "#e3e8ee", "#2f6844", "#b23c17", "#8a94a0", "#5b6b80"
def viz(title, sub, label, w, h, inner, cap):
    """A chart whose title states the finding; subtitle says what is measured; caption gives the source."""
    return (f'<figure class="viz" role="img" aria-label="{label}"><p class="vt">{title}</p><p class="vs">{sub}</p>\n'
            f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><g {F}>\n{inner}\n</g></svg></figure>\n<p class="vizcap">{cap}</p>')
def hbar(y, label, value_txt, width, color, inside=True):
    t = (f'<text x="20" y="{y}" font-size="16.5" fill="{MUTE}">{label}</text>'
         f'<rect x="20" y="{y+9}" width="{max(width, 4):.0f}" height="32" rx="6" fill="{color}"/>')
    if inside:
        return t + f'<text x="{20+width-12:.0f}" y="{y+31}" text-anchor="end" font-size="17" font-weight="700" fill="#fff">{value_txt}</text>'
    return t + f'<text x="{20+max(width, 4)+10:.0f}" y="{y+31}" font-size="17" font-weight="700" fill="{color}">{value_txt}</text>'

# Figure 1: share of eligible beneficiaries in Medicare Advantage
def share(y, yr, pct):
    w = 380 * pct / 100
    return (f'<text x="20" y="{y}" font-size="16.5" font-weight="700" fill="{INK}">{yr}</text>'
            f'<rect x="20" y="{y+9}" width="380" height="34" rx="6" fill="{LINE}"/>'
            f'<rect x="20" y="{y+9}" width="{w:.0f}" height="34" rx="6" fill="{INK}"/>'
            f'<text x="{20+w-10:.0f}" y="{y+32}" text-anchor="end" font-size="17" font-weight="700" fill="#fff">{pct}%</text>'
            f'<text x="390" y="{y+32}" text-anchor="end" font-size="15" fill="{MUTE}">{100-pct}%</text>')
VIZ_SHARE = viz("Medicare Advantage went from 1 in 5 to more than half", "Share of eligible beneficiaries (Part A and B) in Medicare Advantage; the rest are in traditional Medicare",
    "Bars show 19 percent of eligible Medicare beneficiaries in Medicare Advantage in 2007 and 55 percent in 2026.", 420, 150,
    share(24, "2007", 19) + share(92, "2026", 55),
    "Figure 1. Source: KFF, Medicare Advantage in 2026: Enrollment Update and Key Trends. Enrollment passed 35 million in February 2026.")

# Figure 2: prior authorization per 1,000 requests
VIZ_PA = viz("Most requests are approved, and most denials are never appealed", "Medicare Advantage prior authorization requests, all plans, 2024, per 1,000 requests",
    "Out of every 1,000 prior authorization requests in 2024, 923 were approved and 77 denied. About 9 of the 77 denials were appealed, and about 7 of those appeals succeeded. About 68 denials were never appealed.", 420, 290,
    hbar(24, "Approved", "923", 380, GREEN_D)
    + hbar(90, "Denied", "77", 32, CORAL_D, False)
    + hbar(156, "Denials that were appealed", "about 9", 4, CORAL_D, False)
    + hbar(222, "Appeals that succeeded", "about 7", 4, GREEN_D, False),
    "Figure 2. 52.8 million requests: 7.7% denied in full or part, 11.5% of denials appealed, 80.7% of appeals overturned in full or part. Source: KFF analysis of CMS data. Per-1,000 counts are our arithmetic.")

# Figure 3: yearly premiums by path
WP = 380 / 5183
VIZ_PREM = viz("A supplement path costs about $2,750 a year more in premiums", "Average yearly premiums in 2026, including the Part B premium paid on every path",
    "Yearly premiums in 2026: Original Medicare with an average Plan G and drug plan, $5,183; a $0-premium Medicare Advantage plan with drug coverage, $2,435; Original Medicare alone, $2,435.", 420, 230,
    hbar(24, "Original Medicare + Plan G + drug plan", "$5,183", 5183 * WP, CORAL_D)
    + hbar(90, "$0-premium Advantage plan with drugs", "$2,435", 2435 * WP, INK)
    + hbar(156, "Original Medicare alone (no drug plan)", "$2,435", 2435 * WP, GRAY),
    "Figure 3. Part B $202.90 a month (CMS); Plan G $194, the average among current policyholders (KFF analysis of NAIC data); stand-alone drug plan about $35 (CMS). About 3 in 4 Advantage drug-plan members pay no premium beyond Part B (KFF). Copays are not included.")

# Figure 4: Medigap average premium over time
def col(x, yr, v, top=260, base=200):
    hgt = (v / top) * base
    return (f'<rect x="{x}" y="{230-hgt:.0f}" width="80" height="{hgt:.0f}" rx="6" fill="{CORAL_D}"/>'
            f'<text x="{x+40}" y="{222-hgt:.0f}" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}">${v}</text>'
            f'<text x="{x+40}" y="252" text-anchor="middle" font-size="16" fill="{MUTE}">{yr}</text>')
VIZ_MG = viz("The average supplement premium rose 20% in five years", "Average monthly Medigap premium among current policyholders",
    "Columns show the average monthly Medigap premium: $203 in 2020, $217 in 2023 and $244 in 2025.", 420, 262,
    f'<line x1="20" y1="230" x2="400" y2="230" stroke="{LINE}" stroke-width="2"/>' + col(50, "2020", 203) + col(170, "2023", 217) + col(290, "2025", 244),
    "Figure 4. Source: KFF analysis of NAIC data via Mark Farrah Associates. Up 7% from 2024 to 2025. Industry analysis of 2026 filings found Plan G increases of roughly 12% to 26% at several large insurers.")

# Figure 5: cumulative 20-year cost (line chart)
X0, X1, Y0, Y1, YMAX = 56, 330, 270, 30, 180000
xp = lambda i: X0 + (X1 - X0) * (i + 1) / YEARS
yp = lambda v: Y0 - (Y0 - Y1) * v / YMAX
pts = lambda arr: " ".join(f"{xp(i):.1f},{yp(v):.1f}" for i, v in enumerate(arr))
band = pts(SUP[.10]) + " " + " ".join(f"{xp(i):.1f},{yp(v):.1f}" for i, v in reversed(list(enumerate(SUP[.05]))))
grid = "".join(f'<line x1="{X0}" y1="{yp(v):.1f}" x2="{X1}" y2="{yp(v):.1f}" stroke="{LINE}" stroke-width="1"/>'
               f'<text x="{X0-6}" y="{yp(v)+5:.1f}" text-anchor="end" font-size="13" fill="{MUTE}">${v//1000}k</text>' for v in (0, 50000, 100000, 150000))
xlab = "".join(f'<text x="{X0 + (X1-X0)*a/20:.1f}" y="{Y0+20}" text-anchor="middle" font-size="13" fill="{MUTE}">{65+a}</text>' for a in (0, 5, 10, 15, 20))
VIZ_CUM = viz("A supplement's cost is predictable; an Advantage plan's depends on your health",
    "Running total of out-of-pocket costs beyond the Part B premium, age 65 to 85",
    f"Line chart of running totals from 65 to 85. The supplement path, Plan G plus a drug plan plus the Part B deductible, reaches about {k_(LOW)} if premiums rise 5 percent a year and {k_(HIGH)} at 10 percent, shown as a shaded range. A $0-premium Advantage plan where the member reaches the average out-of-pocket limit every single year reaches about {k_(MA_AVG_CUM[-1])}. In a year with no care, the Advantage plan costs nothing beyond Part B.", 420, 330,
    grid + xlab
    + f'<polygon points="{band}" fill="{CORAL_D}" fill-opacity=".18"/>'
    + f'<polyline points="{pts(SUP[.10])}" fill="none" stroke="{CORAL_D}" stroke-width="2.5" stroke-dasharray="6 4"/>'
    + f'<polyline points="{pts(SUP[.05])}" fill="none" stroke="{CORAL_D}" stroke-width="3"/>'
    + f'<polyline points="{pts(MA_AVG_CUM)}" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="2 5" stroke-linecap="round"/>'
    + f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{INK}" stroke-width="2"/>'
    + f'<text x="{X1+8}" y="{yp(MA_AVG_CUM[-1])+5:.1f}" font-size="14.5" font-weight="700" fill="{INK}">{k_(MA_AVG_CUM[-1])}</text>'
    + f'<text x="{X1+8}" y="{yp(HIGH)+5:.1f}" font-size="14.5" font-weight="700" fill="{CORAL_D}">{k_(HIGH)}</text>'
    + f'<text x="{X1+8}" y="{yp(LOW)+5:.1f}" font-size="14.5" font-weight="700" fill="{CORAL_D}">{k_(LOW)}</text>'
    + f'<text x="{X1+8}" y="{Y0+5}" font-size="14.5" font-weight="700" fill="{INK}">$0</text>'
    + f'<line x1="22" y1="302" x2="44" y2="302" stroke="{CORAL_D}" stroke-width="3"/><text x="50" y="307" font-size="13.5" fill="{MUTE}">Supplement path, premiums +5% to +10% a year</text>'
    + f'<line x1="22" y1="322" x2="44" y2="322" stroke="{INK}" stroke-width="3" stroke-dasharray="2 5" stroke-linecap="round"/><text x="50" y="327" font-size="13.5" fill="{MUTE}">Advantage plan, average limit reached every year</text>',
    "Figure 5. Our estimate, inputs in the methods box below. The dotted line is a worst case for the Advantage plan; most members do not reach their limit every year. The bottom line, $0, is an Advantage year with no care.")

# Figure 6: one expensive year
WB = 380 / BAD_YEAR
VIZ_BAD = viz("In one expensive year, the order flips", "What you would owe for $100,000 of Medicare-approved outpatient care in 2026",
    "For one year with $100,000 of Medicare-approved outpatient care: Original Medicare alone $20,226; an Advantage plan at the legal maximum limit $9,250; at the average limit $5,421; Plan G $283.", 420, 290,
    hbar(24, "Original Medicare alone (no yearly cap)", "$20,226", BAD_YEAR * WB, CORAL_D)
    + hbar(90, "Advantage plan at the legal maximum", "$9,250", MA_MAX * WB, INK)
    + hbar(156, "Advantage plan at the average limit", "$5,421", MA_AVG * WB, NAVY_L)
    + hbar(222, "Plan G supplement", "$283", 283 * WB, GREEN_D, False),
    "Figure 6. Part B services, in-network for the Advantage plan. Original Medicare: $283 deductible plus 20% of the rest. Advantage limits for 2026 from KFF. Premiums are separate.")

BODY = r"""
    <p class="disclose"><b>Disclosure:</b> Tyler Insurance Group is an independent agency licensed to sell both Medicare Supplement and Medicare Advantage plans, and insurers pay us commissions on both. Every figure here comes from a public source listed at the end; where we calculate something ourselves, we say so.</p>

    <p>Medicare Advantage now covers more than half of the people who are eligible for it, and it is the part of Medicare people argue about most. Supporters point to low premiums and a yearly spending cap. Critics point to denied care, narrow networks and aggressive sales. Both sides have evidence. The question is what the evidence says when you put it in one place.</p>
    <p>The short answer: Advantage plans approve the large majority of requests, but their denials are real, uneven and rarely challenged. Supplements offer the strongest protection in an expensive year, but their premiums are rising faster than most retirees' incomes and, in most states, are not guaranteed to be available later. Which costs less over a lifetime depends mostly on how many expensive years you have, and the break-even point is further out than many people assume.</p>

    <section class="findings">
      <h2>What we found</h2>
      <ol>
        <li><strong>55% of eligible beneficiaries</strong> are in Medicare Advantage in 2026, up from 19% in 2007.</li>
        <li><strong>Of every 1,000 prior authorization requests</strong> in 2024, plans denied 77. About 9 of those denials were appealed, and about 7 of the appeals succeeded.</li>
        <li><strong>The average supplement premium rose 20%</strong> from 2020 to 2025, to $244 a month, and most states let insurers reject applicants for health reasons after the first six months on Part B.</li>
        <li><strong>Over 20 years</strong>, a Plan G supplement with a drug plan costs an estimated __LOW__ to __HIGH__ beyond the Part B premium. A $0-premium Advantage plan costs more only if the member reaches the average out-of-pocket limit in roughly __BE_LOW__ to __BE_HIGH__ of those 20 years.</li>
        <li><strong>In a single expensive year</strong>, a supplement costs least, an Advantage plan stops at its cap, and Original Medicare alone has no ceiling at all.</li>
      </ol>
    </section>

    <h2>More than half of Medicare is now private</h2>
    __VIZ_SHARE__
    <p>The growth has slowed, to about 3% in 2026, and most of it is in Special Needs Plans for people who also have Medicaid or chronic conditions; those plans now hold 8.2 million people, nearly a quarter of members. The market is concentrated: UnitedHealth Group and Humana together cover 46% of Advantage members. Whatever one thinks of the program, the typical member is not a rare exception. A majority of people who can choose are choosing it.</p>

    <h2>How often plans say no</h2>
    <p>Almost every Advantage plan requires prior authorization for some services, meaning the plan must approve them in advance. CMS now collects the counts, and KFF has analyzed them.</p>
    __VIZ_PA__
    <p>Three things about these numbers matter. First, the denial rate counts requests, not people, and includes partial denials. Second, the low appeal rate is the striking figure: when people appeal, they usually win, which suggests many denials that stand are never tested. Third, the rate is rising by a newer measure. Insurers' own published figures for 2025, covering 14 large companies, show 12% of standard requests denied, or about 120 of every 1,000. That data set is built differently, so it is not a clean year-over-year comparison.</p>
    <p>Two federal reviews explain much of the distrust. The HHS Inspector General examined a sample of 2019 denials from 15 large plans and found that 13% of the denied prior authorization requests met Medicare's coverage rules and likely would have been approved under traditional Medicare. And a 2024 U.S. Senate subcommittee report found that UnitedHealthcare's denial rate for post-acute care, such as skilled nursing and rehabilitation, rose from 8.7% of requests in 2019 to 22.7% in 2022, and that post-acute denials at UnitedHealthcare and CVS ran about three times their overall rates. UnitedHealthcare said the report mischaracterized its clinical practices; CVS said it does not use artificial intelligence to deny claims; the industry group AHIP said the report relied on cherry-picked anecdotes.</p>
    <p>Traditional Medicare uses prior authorization far less, about 2 requests per 100 people in 2024, but denied about 23% of the requests it did review. Since January 2026, a federal pilot called WISeR has required prior authorization for selected services in traditional Medicare in Arizona, New Jersey, Ohio, Oklahoma, Texas and Washington.</p>

    <h2>Why the program draws so much criticism</h2>
    <p>Beyond denials, four documented issues drive most of the criticism:</p>
    <ul>
      <li><strong>Networks change.</strong> Becker's Hospital Review counted about 40 health systems dropping some or all Advantage contracts in 2025 and at least 25 in 2026, often citing prior authorization and slow payment.</li>
      <li><strong>The marketing.</strong> A 2022 Senate Finance Committee staff report found that beneficiary complaints to CMS about Advantage marketing more than doubled from 2020 to 2021.</li>
      <li><strong>The cost to the program.</strong> MedPAC, Congress's Medicare advisory commission, estimates Advantage plans will be paid about 14% more in 2026 than traditional Medicare would have spent on the same people, about $76 billion, adding an estimated $11 billion to total Part B premiums. The Better Medicare Alliance, an industry-backed group, called the estimate "one data point among many."</li>
      <li><strong>The door back can close.</strong> Outside a one-time six-month window after enrolling in Part B at 65, and certain events such as losing retiree coverage, insurers in most states can turn down supplement applicants for health reasons. Only Connecticut, Massachusetts, Maine and New York guarantee access every year for people 65 and older. A federal trial right allows a return within 12 months of first joining an Advantage plan.</li>
    </ul>
    <p>The research on outcomes is more muted than the debate. A KFF review of 62 studies found few large differences between Advantage and traditional Medicare across a wide range of measures, and in one analysis of federal survey data, 94% of people in each program said they were satisfied with the quality of their care.</p>

    <h2>The budget most retirees are working with</h2>
    <p>Coverage decisions are budget decisions, so the household numbers come first. The figures below are medians, the midpoint, where available, because averages are pulled up by the wealthiest retirees.</p>
    <ul>
      <li><strong>Income and savings:</strong> half of all people on Medicare live on less than $43,200 a year per person and have less than $110,100 in savings. A quarter have income below $24,600 and savings below $18,950.</li>
      <li><strong>Social Security:</strong> the average retired worker receives about $2,071 a month in 2026, or about $24,900 a year, rising about 3.6% in January 2027. For 12% of men and 15% of women 65 and older on Social Security, it is at least 90% of their income.</li>
      <li><strong>Retirement accounts:</strong> about half of households aged 65 to 74 have one. Among those that do, the median balance is about $200,000.</li>
      <li><strong>Health costs:</strong> people on Medicare spent an average of $6,459 out of pocket on health care in 2023, including premiums, which KFF calculates as 36% of average Social Security income per beneficiary.</li>
    </ul>
    __VIZ_PREM__
    <p>Advantage members are more likely than people in traditional Medicare to have incomes below $20,000 a year. For households at that level, a premium gap of roughly $2,750 a year is a large share of the budget, which helps explain where the enrollment growth has come from.</p>

    <h2>Supplements: strong coverage, rising price</h2>
    <p>A Medicare Supplement such as Plan G pays nearly everything traditional Medicare leaves behind, at any doctor in the country who accepts Medicare. The trade-off is the premium, and its direction.</p>
    __VIZ_MG__
    <p>Plan G averaged $194 a month in 2025, from $164 in New Mexico to $257 in New York, and its average rose about 13% in that one year. Most states allow insurers to price policies by attained age, so the premium also climbs as the policyholder gets older, on top of the yearly rate increases. KFF notes these policies tend to be the cheapest at first and the most expensive over time. Combined with medical underwriting after the first six months, that is why "just buy a supplement" is not a real option for many people who did not buy one at 65.</p>

    <h2>Twenty years, three ways</h2>
    <p>To compare lifetime costs we modeled 20 years, from 65 to 85, using national averages. The Part B premium is left out because every path pays it. Because future premium increases are uncertain, the supplement path is shown as a range, and the Advantage plan is tested against a deliberately harsh assumption.</p>
    __VIZ_CUM__
    <p>The chart brackets what an Advantage plan can cost. In a year with no care, it costs nothing beyond Part B, the bottom line. If a member reached the plan's average out-of-pocket limit, $5,421, every single year for 20 years, which almost no one does, costs would follow the dotted line. The supplement path lands between the two, and it is predictable: you pay it whether or not you use care. So the useful question is how many expensive years it takes for the Advantage plan to cost more.</p>
    <div class="tblwrap">
    <table class="nettbl">
      <tr><th>If supplement premiums rise</th><th>20-year supplement path</th><th>The Advantage plan costs more if you reach</th></tr>
      <tr><td>5% a year</td><td>__LOW__</td><td>the average limit in __BE5A__ of 20 years, or the maximum in __BE5M__</td></tr>
      <tr><td>8% a year</td><td>__MID__</td><td>the average limit in __BE8A__ of 20 years, or the maximum in __BE8M__</td></tr>
      <tr><td>10% a year</td><td>__HIGH__</td><td>the average limit in __BE10A__ of 20 years, or the maximum in __BE10M__</td></tr>
    </table>
    </div>
    <p class="vstamp">Our estimate. Assumes no copays in the years the limit is not reached, which flatters the break-even slightly; real copays in other years would lower it. Public data do not show how many members reach their limit in a given year.</p>
    <p>A single bad year looks different, and this is where supplements earn their price:</p>
    __VIZ_BAD__
    <p>Traditional Medicare on its own, with no supplement, matches a $0 Advantage plan on premiums but has no ceiling on the 20% coinsurance. About 3.5 million people, 13% of those in traditional Medicare, have no supplemental coverage. In KFF's analysis of federal survey data, they were the group most likely to report problems paying for care, at 30% in 2018, while people with supplements were the least likely and Advantage members fell in between.</p>

    <h2>What the numbers say about who comes out ahead</h2>
    <p>Put together, the data point to fairly clear patterns:</p>
    <ul>
      <li><strong>An Advantage plan with drug coverage</strong> costs the least in most years, caps the bad ones, and includes extras that traditional Medicare does not cover: more than 99% of members have some vision coverage, 98% dental and 95% hearing. The trade-offs are networks, prior authorization, and a harder path back to a supplement.</li>
      <li><strong>A supplement with a drug plan</strong> costs the most in a typical year and the least in a bad one, with the freedom to see any doctor who takes Medicare. Its risk is the premium trend, which compounds over decades.</li>
      <li><strong>Traditional Medicare alone</strong> carries the most risk: the same premium as a $0 Advantage plan, with no cap. It works mainly for people with other coverage, such as retiree benefits, Medicaid or VA care.</li>
    </ul>
    <div class="tblwrap">
    <table class="nettbl">
      <tr><th>Path</th><th>Tends to fit people who</th></tr>
      <tr><td><b>Supplement + drug plan</b></td><td>can comfortably carry rising premiums for decades, want any doctor nationwide, travel or split time between states, or expect heavy care, and are buying in their guaranteed window</td></tr>
      <tr><td><b>Advantage with drug coverage</b></td><td>are on a fixed income, want a yearly cap with little or no premium, have their doctors and hospital in network, and value dental, vision and hearing benefits</td></tr>
      <tr><td><b>Traditional Medicare alone</b></td><td>have other coverage that fills the gaps</td></tr>
    </table>
    </div>

    <div class="methods">
      <h2>How we did this</h2>
      <p><b>Data.</b> Enrollment, prior authorization, premiums, out-of-pocket limits and supplemental benefits come from KFF research using CMS and NAIC data; payment estimates from MedPAC; denial reviews from the HHS Inspector General and the Senate Permanent Subcommittee on Investigations; income and savings from KFF and the Urban Institute; Social Security figures from the Social Security Administration. Each figure was confirmed in at least two sources or taken from the primary government source.</p>
      <p><b>The 20-year model.</b> Our own estimate, with these inputs:</p>
      <ul>
        <li>Plan G at $160 a month at 65, the typical national quote for a new enrollee in 2025, rising 5%, 8% or 10% a year to reflect both age and rate increases (the 2025 average increase was 7%; 2026 filings at large insurers ran about 12% to 26%).</li>
        <li>A stand-alone drug plan at $35 a month (the CMS 2026 average) and the $283 Part B deductible, each rising 5% a year.</li>
        <li>Advantage out-of-pocket limits of $5,421 (2026 average) and $9,250 (2026 legal maximum), each rising 5% a year, with a $0 premium beyond Part B, as for about 3 in 4 Advantage drug-plan members.</li>
        <li>Drug costs under the Part D cap are treated as the same on both paths. Dollar amounts are not adjusted for inflation.</li>
      </ul>
      <p><b>What the data cannot tell us.</b> How many Advantage members reach their out-of-pocket limit in a typical year; how care quality differs for a specific condition or plan; and what any one person will pay, which varies widely by state, insurer, age and health.</p>
    </div>

    <div class="note">
      <div class="who">
        <span class="duo"><img src="/assets/austin-tyler.jpg" alt="Austin Tyler" width="600" height="750"><img src="/assets/andrew-horn.jpg" alt="Andrew Horn" width="600" height="750"></span>
        <div><b>A note from our advisors</b><span>Tyler Insurance Group</span></div>
      </div>
      <p>We wrote this because the conversation about Medicare Advantage is usually louder than the data behind it. Both paths can be the right one. The deciding facts are personal: your budget, your doctors, your health and your state's rules on supplements.</p>
      <p>If you want those facts laid out for your own situation, we will do it with you, the same way we did here.</p>
    </div>

    <h2 id="faq">Common questions</h2>
    <div class="faq">
      <h3>How many people are on Medicare Advantage?</h3>
      <p>In 2026, 55% of eligible Medicare beneficiaries, more than 35 million people, are enrolled in Medicare Advantage, according to KFF. The share was 19% in 2007. About 8.2 million are in Special Needs Plans.</p>
      <h3>How often do Medicare Advantage plans deny prior authorization?</h3>
      <p>In 2024, plans denied 77 of every 1,000 prior authorization requests (7.7% of 52.8 million), fully or partly, according to KFF's analysis of CMS data. About 9 of those 77 denials were appealed, and about 7 of the appeals succeeded. Insurer-published data for 2025 show about 120 of every 1,000 standard requests denied.</p>
      <h3>Why do so many people dislike Medicare Advantage?</h3>
      <p>The main documented reasons are prior authorization denials, including Inspector General and Senate findings on care that should likely have been approved and on post-acute care; health systems leaving plan networks; aggressive marketing; MedPAC's estimate that plans are paid about 14% more than traditional Medicare would cost; and the difficulty of returning to a supplement later in most states.</p>
      <h3>How much does a Medicare Supplement cost over a lifetime?</h3>
      <p>The average Medigap premium was $244 a month in 2025, and Plan G averaged $194. In our 20-year estimate, Plan G starting at $160 a month at age 65 and rising 5% to 10% a year, plus a drug plan and the Part B deductible, costs about __LOW__ to __HIGH__ beyond the Part B premium. Actual costs depend on state, insurer, age and rate increases.</p>
      <h3>Is Original Medicare alone cheaper than Medicare Advantage?</h3>
      <p>On premiums they can be the same, since both may cost only the Part B premium. The difference is risk: Original Medicare alone has no yearly limit on the 20% coinsurance, so a year with $100,000 of outpatient care would cost about $20,226, while a Medicare Advantage plan caps in-network costs at its limit, $5,421 on average in 2026.</p>
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
      <div class="recap-item">55% of eligible beneficiaries, more than 35 million people, are in Medicare Advantage in 2026, up from 19% in 2007.</div>
      <div class="recap-item">Of every 1,000 prior authorization requests in 2024, 77 were denied; about 9 denials were appealed and about 7 appeals succeeded.</div>
      <div class="recap-item">Federal reviews found some denials that should likely have been approved, and sharply higher denial rates for post-acute care at large insurers; the insurers dispute the findings.</div>
      <div class="recap-item">The average Medigap premium rose 20% from 2020 to 2025, to $244 a month, and most states allow medical underwriting after the first six months.</div>
      <div class="recap-item">Over 20 years, the supplement path costs an estimated __LOW__ to __HIGH__; a $0 Advantage plan costs more only if the average limit is reached in roughly __BE_LOW__ to __BE_HIGH__ of those years.</div>
      <div class="recap-item">In one expensive year, Plan G costs about $283, an Advantage plan up to its cap, and Original Medicare alone has no ceiling.</div>
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
      U.S. Senate Permanent Subcommittee on Investigations, "Refusal of Recovery" (October 2024), and company responses, as reported by Healthcare Dive, McKnight's and the Center for Medicare Advocacy &middot;
      U.S. Senate Finance Committee, "Deceptive Marketing Practices Flourish in Medicare Advantage" (November 2022) &middot;
      MedPAC, March 2026 Report to the Congress, chapter 12, and Better Medicare Alliance response &middot;
      Becker's Hospital Review, health systems dropping Medicare Advantage contracts, 2025 and 2026 &middot;
      CMS WISeR model, as summarized by the Congressional Research Service and Kiplinger &middot;
      KFF, "Key Facts About Medigap Enrollment and Premiums" (NAIC data) and "Medigap Guaranteed Issue Requirements" &middot;
      KFF, "A Review of 62 Studies", "Cost-Related Problems Are Less Common Among Beneficiaries in Traditional Medicare Than in Medicare Advantage, Mainly Due to Supplemental Coverage", "A Snapshot of Sources of Coverage Among Medicare Beneficiaries", and "Key Facts About Health Care Affordability for People With Medicare"; Commonwealth Fund (satisfaction) &middot;
      KFF and Urban Institute DYNASIM, income and assets of Medicare beneficiaries, 2024 &middot;
      Federal Reserve Survey of Consumer Finances 2022, as reported by Yahoo Finance and The Motley Fool &middot;
      Social Security Administration, 2026 and 2027 COLA fact sheets and Social Security basic facts &middot;
      CMS, 2026 Medicare Parts A and B premiums and deductibles &middot;
      Industry analysis of 2026 Medigap rate filings (Telos Actuarial, as reported by MedicareFAQ and others); new-enrollee Plan G quotes from ValuePenguin and MedicareSupplement.com.
      Checked November 3, 2026. Per-1,000 counts and the 20-year model are our own calculations and are labeled as such.
    </div>

    <p class="stamp"><b>Written and reviewed by Austin Tyler</b>, Licensed Medicare Advisor, NPN 20234188, Kentucky DOI license #1187780.</p>

    <p class="disclaim">This article is general information, not advice for your specific situation. National averages hide wide differences by state, insurer, age and health; your own costs will differ. The 20-year figures are illustrations built on stated assumptions, not predictions. No specific plan is named or recommended. Tyler Insurance Group is not connected with or endorsed by the United States government or the federal Medicare program. We do not offer every plan available in your area. Currently we represent 6 organizations which offer 158 products in your area. Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance Program (SHIP) to get information on all of your options.</p>
"""
for key, val in [("__VIZ_SHARE__", VIZ_SHARE), ("__VIZ_PA__", VIZ_PA), ("__VIZ_PREM__", VIZ_PREM), ("__VIZ_MG__", VIZ_MG),
                 ("__VIZ_CUM__", VIZ_CUM), ("__VIZ_BAD__", VIZ_BAD)]:
    assert BODY.count(key) == 1, key; BODY = BODY.replace(key, val)
for key, val in [("__LOW__", k_(LOW)), ("__MID__", k_(MID)), ("__HIGH__", k_(HIGH)),
                 ("__BE_LOW__", str(BE[.05][0])), ("__BE_HIGH__", str(BE[.10][0])),
                 ("__BE5A__", str(BE[.05][0])), ("__BE5M__", str(BE[.05][1])), ("__BE8A__", str(BE[.08][0])),
                 ("__BE8M__", str(BE[.08][1])), ("__BE10A__", str(BE[.10][0])), ("__BE10M__", str(BE[.10][1]))]:
    BODY = BODY.replace(key, val)

KCHECK = [
 {"q": "Roughly what share of eligible Medicare beneficiaries are in Medicare Advantage in 2026?",
  "options": ["About 1 in 5", "About a third", "More than half (55%)", "Nearly 90%"], "answer": 2,
  "why": "KFF reports 55% of eligible beneficiaries, more than 35 million people, in 2026, up from 19% in 2007."},
 {"q": "Of every 1,000 Medicare Advantage prior authorization requests in 2024, about how many denials were appealed?",
  "options": ["About 9 of the 77 denials", "About half of them", "All of them", "None; appeals are not allowed"], "answer": 0,
  "why": "Plans denied 77 of every 1,000 requests. Only about 9 of those were appealed, and about 7 of the appeals succeeded, so most denials are never tested."},
 {"q": "You have been on an Advantage plan for five years and want a Plan G supplement. In most states, what can happen?",
  "options": ["You must be accepted at standard rates", "The insurer can ask health questions and decline or charge more", "Medicare assigns you a plan", "You must wait until 70"], "answer": 1,
  "why": "Outside your first six months on Part B and certain federal events, most states allow medical underwriting. Only CT, MA, ME and NY guarantee issue every year for people 65 and older."},
 {"q": "With Original Medicare alone and no supplement, about how much would you owe for $100,000 of Medicare-approved outpatient care in one year (2026)?",
  "options": ["$283", "$5,421", "About $20,226", "Nothing"], "answer": 2,
  "why": "You pay the $283 Part B deductible and 20% of the rest, with no yearly cap. An Advantage plan would stop at its limit; Plan G would leave only the $283."},
 {"q": "Using 2026 averages, how much more a year does the supplement path (Plan G plus a drug plan) cost in premiums than a $0-premium Advantage plan?",
  "options": ["About $250", "About $2,750", "About $10,000", "Nothing; they cost the same"], "answer": 1,
  "why": "An average Plan G ($194) and drug plan ($35) add about $229 a month, about $2,750 a year, on top of the Part B premium that both paths pay."},
]
body_html = BODY.replace("__KCHECK__", json.dumps(KCHECK, ensure_ascii=False))
assert not re.findall(r"__[A-Z0-9_]+__", body_html), re.findall(r"__[A-Z0-9_]+__", body_html)

out = re.sub(r'(<nav class="crumb" aria-label="Breadcrumb">).*?(</nav>)',
             r'\1<a href="/">Home</a> &rsaquo; <a href="/articles/">Learning Center</a> &rsaquo; <a href="/articles/coverage/">Coverage Choices</a> &rsaquo; '
             + CRUMB_LABEL + r'\2', out, count=1, flags=re.S)
out = re.sub(r'<span class="tag">.*?</span>', '<span class="tag">Coverage Choices · Costs &amp; Savings · Data</span>', out, count=1, flags=re.S)
out = re.sub(r'<h1>.*?</h1>', f'<h1>{H1}</h1>\n    <p class="dek">{DEK}</p>', out, count=1, flags=re.S)
out = re.sub(r'(Licensed Medicare Advisor, Tyler Insurance Group · )[^<]*(</div>)', r'\g<1>' + DATE_LONG + r' · 13 min read\2', out, count=1)
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
        node.update({"headline": "Medicare Advantage by the Numbers: Enrollment, Denials and Lifetime Costs", "description": DESC,
                     "datePublished": DATE, "dateModified": DATE, "articleSection": "Coverage Choices",
                     "mainEntityOfPage": {"@type": "WebPage", "@id": URL}, "@id": URL + "#article"})
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
print(f"wrote articles/{SLUG}/index.html ({len(pairs)} FAQ, {len(KCHECK)} kcheck); 20-yr {k_(LOW)}/{k_(MID)}/{k_(HIGH)}; break-even {BE}")
