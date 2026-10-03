#!/usr/bin/env python3
"""Build /articles/medicare-advantage-premium-deductible-copay-coinsurance-explained/ by cloning
chrome from an existing article and swapping in head, schema, body, visuals and knowledge check."""
import json, re, os

SRC = "articles/does-baptist-health-take-medicare-advantage/index.html"
SLUG = "medicare-advantage-premium-deductible-copay-coinsurance-explained"
DST_DIR = f"articles/{SLUG}"
URL = f"https://www.bluegrassmedicarehelp.com/articles/{SLUG}/"
TITLE = "Medicare Advantage Costs: 5 Terms Explained Simply"
H1 = "Premium, Deductible, Copay, Coinsurance, Max Out-of-Pocket: The Five Words That Run Your Medicare Advantage Plan"
DESC = ("Plain-English explanations of the five cost words on every Medicare Advantage plan, one picture each, "
        "a full year walked through, and why the deductible and the out-of-pocket maximum are not the same number.")
CRUMB_LABEL = "Five Cost Terms"

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
.ans ol{margin:0;padding-left:22px;} .ans li{font-size:18px;margin:0 0 8px;line-height:1.5;} .ans li:last-child{margin-bottom:0;}
.viz{margin:10px 0 8px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px;}
.viz svg{width:100%;height:auto;display:block;}
.vizcap{font-size:14.5px;color:var(--faint);margin:6px 0 26px;line-height:1.5;}
.term{border:1px solid var(--line);border-radius:16px;padding:22px 22px 6px;margin:0 0 26px;background:var(--cream2);}
.term h2{margin-top:0;} .term .def{font-size:19px;color:var(--ink);margin:0 0 14px;}
.term .def b{color:var(--coral-d);}
.term .viz{background:#fff;}
.term .anoc{font-size:16.5px;color:var(--mute);background:#fff;border-left:4px solid var(--green);padding:12px 16px;border-radius:0 10px 10px 0;margin:4px 0 18px;}
.term .anoc b{color:var(--ink);}
.stamp{font-size:14.5px;color:var(--faint);margin:26px 0 0;}
.stamp b{color:var(--mute);font-weight:600;}
.plan{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 20px;margin:0 0 26px;}
.plan b{display:block;font-family:var(--serif);font-size:19px;margin-bottom:8px;}
.plan ul{margin:0;padding-left:20px;columns:2;column-gap:28px;} .plan li{font-size:16.5px;margin:0 0 6px;break-inside:avoid;}
@media(max-width:600px){.plan ul{columns:1;}}
"""
out = out.replace("</style>", NEWCSS + "</style>")

F = 'font-family="Source Sans 3, Arial, sans-serif"'
INK, MUTE, FAINT, LINE, WARM, GREEN, GREEN_D, CORAL, CORAL_D = "#2a2620", "#5f594f", "#938c80", "#e2d9c8", "#efe6d6", "#3a7d52", "#2f6844", "#d05528", "#b3431d"

def viz(label, w, h, inner, cap):
    return (f'<figure class="viz" role="img" aria-label="{label}">\n<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><g {F}>\n{inner}\n</g></svg></figure>\n<p class="vizcap">{cap}</p>')

# 1 Premium: 12 month tiles
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
tiles = ""
for i, m in enumerate(months):
    x = 30 + i * 66
    tiles += (f'<rect x="{x}" y="60" width="58" height="72" rx="10" fill="{WARM}" stroke="{LINE}" stroke-width="1.5"/>'
              f'<text x="{x+29}" y="84" text-anchor="middle" font-size="14" fill="{MUTE}">{m}</text>'
              f'<text x="{x+29}" y="116" text-anchor="middle" font-size="20" font-weight="700" fill="{GREEN_D}">$0</text>')
VIZ_PREM = viz("Twelve month tiles, January to December, each showing a $0 plan premium, with a note that the Part B premium of $202.90 a month is still paid to Medicare separately.", 860, 230,
    f'<text x="430" y="34" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}">The plan premium: the bill that comes whether you see a doctor or not</text>'
    + tiles +
    f'<rect x="30" y="156" width="800" height="52" rx="10" fill="#fff" stroke="{CORAL_D}" stroke-width="2"/>'
    f'<text x="52" y="178" font-size="15" fill="{INK}">Still paid to Medicare every month, separately, on every plan:</text>'
    f'<text x="52" y="199" font-size="15" fill="{MUTE}">Part B premium, $202.90 in 2026 (usually taken out of your Social Security check)</text>'
    f'<text x="808" y="190" text-anchor="end" font-size="22" font-weight="700" fill="{CORAL_D}">$202.90</text>',
    "Figure 1. A $0 plan premium means the plan itself charges nothing each month. It does not erase the Part B premium, which every Medicare Advantage member keeps paying.")

# 2 Deductible: a meter with first $250
VIZ_DED = viz("A $250 deductible shown as a meter. The first $250 of covered bills in the year is paid by you; after the meter is full, copays and coinsurance take over.", 860, 250,
    f'<text x="430" y="34" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}">The deductible: the first dollars of the year are yours</text>'
    f'<rect x="60" y="70" width="740" height="44" rx="22" fill="{WARM}" stroke="{LINE}" stroke-width="1.5"/>'
    f'<rect x="60" y="70" width="185" height="44" rx="22" fill="{CORAL_D}"/>'
    f'<text x="152" y="99" text-anchor="middle" font-size="17" font-weight="700" fill="#fff">You pay the first $250</text>'
    f'<text x="520" y="99" text-anchor="middle" font-size="17" fill="{MUTE}">Then the plan starts sharing: copays and coinsurance apply</text>'
    f'<line x1="245" y1="60" x2="245" y2="124" stroke="{CORAL_D}" stroke-width="2" stroke-dasharray="4 4"/>'
    f'<text x="245" y="146" text-anchor="middle" font-size="14" fill="{CORAL_D}" font-weight="700">deductible met</text>'
    f'<text x="60" y="186" font-size="15" fill="{MUTE}">Many Medicare Advantage plans set the medical deductible at $0.</text>'
    f'<text x="60" y="208" font-size="15" fill="{MUTE}">The drug deductible is separate and can be up to $700 in 2027.</text>'
    f'<text x="60" y="230" font-size="15" fill="{MUTE}">A deductible usually applies only to some services (an MRI, a hospital stay), not to a $0 primary care visit.</text>',
    "Figure 2. A deductible is a starting hurdle, not a yearly cap. Once it is met, you are still paying copays and coinsurance until you reach the out-of-pocket maximum.")

# 3 Copay: price tags
def tag(x, label, amt, col):
    return (f'<path d="M{x} 80 h170 l22 22 l-22 22 h-170 z" fill="#fff" stroke="{LINE}" stroke-width="2"/>'
            f'<circle cx="{x+16}" cy="102" r="5" fill="{LINE}"/>'
            f'<text x="{x+34}" y="97" font-size="14" fill="{MUTE}">{label}</text>'
            f'<text x="{x+34}" y="117" font-size="19" font-weight="700" fill="{col}">{amt}</text>')
VIZ_COPAY = viz("Four price tags: primary care $0, specialist $45, emergency room $125, hospital $350 a day for days one to five. A copay is a flat dollar amount per visit, known before you go.", 860, 200,
    f'<text x="430" y="34" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}">The copay: a flat price tag you know before you walk in</text>'
    + tag(30, "Primary care visit", "$0", GREEN_D) + tag(232, "Specialist visit", "$45", INK) + tag(434, "Emergency room", "$125", INK) + tag(636, "Hospital, per day", "$350", CORAL_D)
    + f'<text x="430" y="172" text-anchor="middle" font-size="15" fill="{MUTE}">Same price whether the bill behind it was $90 or $9,000. Hospital copay applies days 1 to 5. Sample plan, not a quote.</text>',
    "Figure 3. Copays are the easiest term because they are fixed. The catch is that they add up: a hospital copay is per day, and a specialist copay is per visit.")

# 4 Coinsurance: a bill split
VIZ_COINS = viz("A $1,500 MRI bill drawn as a bar split 20 percent and 80 percent. Your 20 percent coinsurance is $300; the plan pays $1,200. Below it a $8,000 infusion bill at the same 20 percent: you pay $1,600.", 860, 250,
    f'<text x="430" y="34" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}">Coinsurance: a slice of the bill, so a bigger bill means a bigger slice</text>'
    f'<text x="60" y="76" font-size="15" fill="{MUTE}">MRI, $1,500 bill, 20% coinsurance</text>'
    f'<rect x="60" y="86" width="740" height="36" rx="8" fill="{WARM}"/>'
    f'<rect x="60" y="86" width="148" height="36" rx="8" fill="{CORAL_D}"/>'
    f'<text x="134" y="110" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">You $300</text>'
    f'<text x="504" y="110" text-anchor="middle" font-size="15" fill="{INK}">Plan pays $1,200</text>'
    f'<text x="60" y="160" font-size="15" fill="{MUTE}">Infusion treatment, $8,000 bill, same 20% coinsurance</text>'
    f'<rect x="60" y="170" width="740" height="36" rx="8" fill="{WARM}"/>'
    f'<rect x="60" y="170" width="148" height="36" rx="8" fill="{CORAL_D}"/>'
    f'<text x="134" y="194" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">You $1,600</text>'
    f'<text x="504" y="194" text-anchor="middle" font-size="15" fill="{INK}">Plan pays $6,400</text>'
    f'<text x="430" y="236" text-anchor="middle" font-size="14" fill="{FAINT}">The percentage never changes. The dollars do, because the bill does.</text>',
    "Figure 4. Coinsurance is a copay that scales with the bill. You cannot know the dollar amount until you know the price of the service, which is why it is the term people like least.")

# 5 MOOP: the ceiling
VIZ_MOOP = viz("A stack of your payments through the year rising toward a ceiling line labeled out-of-pocket maximum $5,000. Above the line everything covered is $0. Premiums and drug costs are shown outside the stack because they do not count.", 860, 300,
    f'<text x="430" y="34" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}">The max out-of-pocket: the ceiling on your medical bills for the year</text>'
    f'<line x1="60" y1="80" x2="560" y2="80" stroke="{CORAL_D}" stroke-width="3"/>'
    f'<text x="60" y="70" font-size="16" font-weight="700" fill="{CORAL_D}">Out-of-pocket maximum: $5,000 (sample plan)</text>'
    f'<rect x="110" y="200" width="90" height="60" rx="6" fill="{GREEN}"/><text x="155" y="236" text-anchor="middle" font-size="14" fill="#fff">copays</text>'
    f'<rect x="110" y="140" width="90" height="56" rx="6" fill="{GREEN_D}"/><text x="155" y="173" text-anchor="middle" font-size="14" fill="#fff">coinsurance</text>'
    f'<rect x="110" y="110" width="90" height="26" rx="6" fill="#4f9468"/><text x="155" y="128" text-anchor="middle" font-size="13" fill="#fff">deductible</text>'
    f'<line x1="60" y1="262" x2="560" y2="262" stroke="{MUTE}" stroke-width="2"/>'
    f'<text x="250" y="130" font-size="15" fill="{INK}">All three count toward the ceiling.</text>'
    f'<text x="250" y="152" font-size="15" fill="{INK}">When the stack touches the line, covered</text>'
    f'<text x="250" y="172" font-size="15" fill="{INK}">medical care is $0 until January 1.</text>'
    f'<text x="250" y="206" font-size="14" fill="{MUTE}">Highest a plan may set it, in network:</text>'
    f'<text x="250" y="226" font-size="14" fill="{MUTE}">$9,250 (2026), $9,850 (2027).</text>'
    f'<text x="250" y="246" font-size="14" fill="{MUTE}">Most plans set theirs lower.</text>'
    f'<rect x="600" y="60" width="230" height="200" rx="12" fill="{WARM}" stroke="{LINE}" stroke-width="1.5"/>'
    f'<text x="715" y="88" text-anchor="middle" font-size="15" font-weight="700" fill="{INK}">Does NOT count</text>'
    f'<text x="620" y="118" font-size="14.5" fill="{MUTE}">&#10005; Plan premium</text>'
    f'<text x="620" y="142" font-size="14.5" fill="{MUTE}">&#10005; Part B premium</text>'
    f'<text x="620" y="166" font-size="14.5" fill="{MUTE}">&#10005; Prescription drugs (own cap)</text>'
    f'<text x="620" y="190" font-size="14.5" fill="{MUTE}">&#10005; Dental, vision, hearing extras</text>'
    f'<text x="620" y="214" font-size="14.5" fill="{MUTE}">&#10005; Care the plan does not cover</text>'
    f'<text x="620" y="238" font-size="14.5" fill="{MUTE}">&#10005; Out of network on an HMO</text>',
    "Figure 5. The maximum is the one number that tells you your worst case. Add twelve months of premiums to it and you have the most a bad year can cost you for covered medical care.")

# 6 Floor vs ceiling
VIZ_MIX = viz("A tall vertical bar for one year of medical bills. A thin band at the bottom is labeled deductible, the first dollars, often $0 on Medicare Advantage. A line at the top is labeled out-of-pocket maximum, the last dollar, typically $4,000 to $6,000. The space between is copays and coinsurance.", 860, 360,
    f'<text x="430" y="34" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}">The floor and the ceiling are not the same number</text>'
    f'<rect x="330" y="70" width="200" height="250" rx="10" fill="{WARM}" stroke="{LINE}" stroke-width="1.5"/>'
    f'<rect x="330" y="296" width="200" height="24" rx="0" fill="{CORAL_D}"/>'
    f'<path d="M330 320 h200 v-24 h-200 z" fill="{CORAL_D}"/>'
    f'<rect x="330" y="70" width="200" height="6" fill="{GREEN_D}"/>'
    f'<text x="430" y="200" text-anchor="middle" font-size="15" fill="{MUTE}">copays and coinsurance</text>'
    f'<text x="430" y="222" text-anchor="middle" font-size="15" fill="{MUTE}">as you use care</text>'
    f'<text x="300" y="312" text-anchor="end" font-size="16" font-weight="700" fill="{CORAL_D}">DEDUCTIBLE</text>'
    f'<text x="300" y="332" text-anchor="end" font-size="14" fill="{MUTE}">the first dollars</text>'
    f'<text x="300" y="350" text-anchor="end" font-size="14" fill="{MUTE}">often $0 on Advantage plans</text>'
    f'<text x="560" y="78" font-size="16" font-weight="700" fill="{GREEN_D}">OUT-OF-POCKET MAXIMUM</text>'
    f'<text x="560" y="98" font-size="14" fill="{MUTE}">the last dollar you can pay</text>'
    f'<text x="560" y="116" font-size="14" fill="{MUTE}">typically $4,000 to $6,000, up to $9,850 in 2027</text>'
    f'<text x="560" y="150" font-size="14" fill="{INK}">Seeing a $5,900 maximum and thinking</text>'
    f'<text x="560" y="168" font-size="14" fill="{INK}">"I owe $5,900 before the plan pays" is the</text>'
    f'<text x="560" y="186" font-size="14" fill="{INK}">mistake. The ceiling is the most you can be</text>'
    f'<text x="560" y="204" font-size="14" fill="{INK}">asked for, and most years you never reach it.</text>',
    "Figure 6. Same bar, two ends. The deductible sits at the bottom and is usually small or zero. The maximum sits at the top and is the largest number on the page. People read the big number as a hurdle. It is a lid.")

# 7 Ruth's year, cumulative bars with ceiling
cum = [0,45,45,45,345,1745,2545,3720,5000,5000,5000,5000]
paid = [0,45,0,0,300,1400,800,1175,1280,0,0,0]
bars = ""
base_y, scale = 300, 220/5000
for i, (m, c, p) in enumerate(zip(months, cum, paid)):
    x = 80 + i * 62; h = round(c*scale)
    bars += f'<rect x="{x}" y="{base_y-h}" width="44" height="{h}" rx="4" fill="{GREEN}"/>'
    bars += f'<text x="{x+22}" y="324" text-anchor="middle" font-size="13" fill="{MUTE}">{m}</text>'
    if p: bars += f'<text x="{x+22}" y="{base_y-h-8}" text-anchor="middle" font-size="12" fill="{INK}">+${p:,}</text>'
    elif c >= 5000: bars += f'<text x="{x+22}" y="{base_y-h-8}" text-anchor="middle" font-size="12" fill="{GREEN_D}">$0</text>'
VIZ_YEAR = viz("Bar chart of Ruth's cumulative out-of-pocket medical spending by month on the sample plan. It rises from $0 in January through $45, $345, $1,745, $2,545, $3,720 and reaches the $5,000 out-of-pocket maximum in September, then stays flat at $5,000 with $0 added in October, November and December.", 860, 350,
    f'<text x="430" y="30" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}">Ruth&#8217;s year: what she has paid so far, month by month</text>'
    f'<line x1="70" y1="{base_y-220}" x2="830" y2="{base_y-220}" stroke="{CORAL_D}" stroke-width="2.5" stroke-dasharray="7 5"/>'
    f'<text x="80" y="{base_y-230}" font-size="14" font-weight="700" fill="{CORAL_D}">Out-of-pocket maximum $5,000</text>'
    f'<line x1="70" y1="{base_y}" x2="830" y2="{base_y}" stroke="{MUTE}" stroke-width="2"/>'
    + bars +
    f'<text x="80" y="346" font-size="13" fill="{FAINT}">Bars are the running total. Labels are what each month added. Sample plan; premiums and drug costs not included.</text>',
    "Figure 7. Six months of ordinary care cost her under $400. One knee and its complications took her to the ceiling by September. From there, every covered medical bill was $0 until January.")

# 8 ANOC mock
rows = [("Monthly plan premium","$0","$0",False),("Medical deductible","$0","$0",False),("Maximum out-of-pocket (in network)","$5,000","$5,900",True),
        ("Primary care visit","$0","$0",False),("Specialist visit","$45","$50",True),("Inpatient hospital, per day (days 1 to 5)","$350","$395",True),
        ("Outpatient surgery, MRI, infusions","20%","20%",False)]
rr = ""
for i, (lab, a, b, chg) in enumerate(rows):
    y = 118 + i * 34
    if chg: rr += f'<rect x="44" y="{y-22}" width="772" height="32" rx="6" fill="rgba(179,67,29,.08)"/>'
    rr += f'<text x="56" y="{y}" font-size="15.5" fill="{INK}">{lab}</text><text x="600" y="{y}" text-anchor="middle" font-size="15.5" fill="{MUTE}">{a}</text>'
    rr += f'<text x="760" y="{y}" text-anchor="middle" font-size="15.5" font-weight="{"700" if chg else "400"}" fill="{CORAL_D if chg else INK}">{b}</text>'
VIZ_ANOC = viz("A mock Annual Notice of Change table with columns for 2026 and 2027. Premium stays $0, deductible stays $0, maximum out-of-pocket rises from $5,000 to $5,900, specialist copay rises from $45 to $50, hospital per-day copay rises from $350 to $395, coinsurance stays 20 percent. Changed rows are highlighted.", 860, 380,
    f'<rect x="30" y="20" width="800" height="340" rx="12" fill="#fff" stroke="{LINE}" stroke-width="2"/>'
    f'<text x="56" y="52" font-size="14" font-weight="700" fill="{FAINT}" letter-spacing="1">ANNUAL NOTICE OF CHANGE: CHANGES TO BENEFITS AND COSTS (EXAMPLE LAYOUT)</text>'
    f'<line x1="56" y1="64" x2="804" y2="64" stroke="{LINE}" stroke-width="2"/>'
    f'<text x="600" y="88" text-anchor="middle" font-size="14" font-weight="700" fill="{MUTE}">2026 (this year)</text>'
    f'<text x="760" y="88" text-anchor="middle" font-size="14" font-weight="700" fill="{CORAL_D}">2027 (next year)</text>'
    + rr +
    f'<text x="430" y="348" text-anchor="middle" font-size="14" fill="{FAINT}">Highlighted rows changed. Read those with Ruth&#8217;s year in mind: her worst case just went up $900.</text>',
    "Figure 8. The notice puts this year and next year side by side. You now know what every row means, so you can ask the only question that matters: on the care I actually use, what does next year cost me?")

BODY = r"""
    <p>Every September a thick envelope shows up from your Medicare Advantage plan. Inside is a table with two columns, this year and next year, and a dozen rows of numbers. Most people look at it the way you would look at a utility bill in a language you half speak. You recognize the dollar signs. You are not quite sure which ones are going to hurt.</p>
    <p>There are only five words in that table that matter. If you know what each one means, you can read the whole thing in ten minutes and decide, with real confidence, whether to keep your plan. This page explains the five, one picture each, and then walks one person through a whole year so you can see them working together.</p>

    <div class="ans">
      <p><strong>The five, in one sentence each:</strong></p>
      <ol>
        <li><strong>Premium</strong> is the monthly bill you pay whether or not you use the plan.</li>
        <li><strong>Deductible</strong> is the first dollars of the year you pay yourself before the plan starts sharing.</li>
        <li><strong>Copay</strong> is a flat price per visit or per day, fixed in advance.</li>
        <li><strong>Coinsurance</strong> is a percentage of the bill, so it grows with the bill.</li>
        <li><strong>Max out-of-pocket</strong> is the ceiling: the most you can pay in a year for covered medical care, after which the plan pays everything.</li>
      </ol>
      <p>The one people get backwards: <strong>the deductible is the floor and the maximum is the ceiling.</strong> They are not the same number, and on most Advantage plans the floor is $0.</p>
    </div>

    <h2>The sample plan we will use</h2>
    <p>Every number below comes from one made-up plan. It is in the range of real Central Kentucky HMO plans, but it is not any carrier's plan and nothing here is a quote. Your own numbers are in your Summary of Benefits.</p>
    <div class="plan">
      <b>Sample plan, 2026</b>
      <ul>
        <li>Monthly premium: <strong>$0</strong></li>
        <li>Medical deductible: <strong>$0</strong></li>
        <li>Primary care visit: <strong>$0</strong></li>
        <li>Specialist visit: <strong>$45</strong></li>
        <li>Emergency room: <strong>$125</strong></li>
        <li>Hospital stay: <strong>$350 a day</strong>, days 1 to 5, then $0</li>
        <li>Outpatient surgery, MRI, infusions: <strong>20% coinsurance</strong></li>
        <li>Physical therapy: <strong>$40 a visit</strong></li>
        <li>Max out-of-pocket, in network: <strong>$5,000</strong></li>
      </ul>
    </div>

    <section class="term" id="premium">
      <h2>1. Premium</h2>
      <p class="def"><b>What you pay every month to have the plan</b>, whether you see a doctor that month or not. Think of it as the subscription.</p>
      __VIZ_PREM__
      <p>About <strong>59 percent of Medicare Advantage plans offered for 2026 carry a $0 premium</strong>, and in Fayette County it is 21 of the 40 plans on offer. A $0 premium does not mean free. Every Advantage member keeps paying the Part B premium to Medicare, $202.90 a month in 2026, and the plan's copays and coinsurance still apply when you use care. The premium is simply the one cost that does not depend on how sick you get.</p>
      <p class="anoc"><b>On the Annual Notice of Change:</b> the first row, usually. A premium that goes from $0 to $25 is $300 a year, every year, before you have used anything. A premium that stays at $0 tells you nothing about the rest of the table.</p>
    </section>

    <section class="term" id="deductible">
      <h2>2. Deductible</h2>
      <p class="def"><b>The amount you pay yourself at the start of the year</b>, for the services it applies to, before the plan starts sharing the cost. The sample plan's medical deductible is $0, so here is what a $250 one would look like:</p>
      __VIZ_DED__
      <p>Three things about deductibles on Advantage plans that surprise people. First, <strong>many plans set the medical deductible at $0</strong>, so you go straight to copays. Second, when a plan does have one, it usually applies only to some services, such as a hospital stay or outpatient surgery, and not to a $0 primary care visit. Third, <strong>the prescription drug deductible is a separate thing</strong>, up to $615 in 2026 and $700 in 2027, and it sits inside the drug benefit, not the medical one.</p>
      <p>What a deductible is not: it is not the most you can pay. Meeting it does not switch the plan to free. It is the entry fee, and copays and coinsurance begin once it is paid.</p>
      <p class="anoc"><b>On the Annual Notice of Change:</b> a medical deductible appearing where there was none (say, $0 to $300) means the first $300 of hospital or surgery bills next year is yours before the copays even start. Check which services it applies to; the Evidence of Coverage lists them.</p>
    </section>

    <section class="term" id="copay">
      <h2>3. Copay</h2>
      <p class="def"><b>A flat dollar amount for a visit or a service</b>, printed in advance. $45 to see a specialist is $45 whether the specialist bills $150 or $600.</p>
      __VIZ_COPAY__
      <p>Copays are the most predictable of the five and the easiest to budget. The two places they bite are <strong>frequency</strong> (a $45 specialist copay is $540 a year if you go monthly) and <strong>the per-day hospital copay</strong>, which most people have never had to think about. $350 a day for days 1 to 5 means a four-day stay is $1,400 and a six-day stay is $1,750. That single row often moves more money than every other copay combined.</p>
      <p class="anoc"><b>On the Annual Notice of Change:</b> copays change in small-looking steps, $45 to $50, $350 to $395. Multiply each change by how often you actually use that service. Five dollars times your twelve cardiology visits is $60; forty-five dollars times a four-day hospital stay is $180.</p>
    </section>

    <section class="term" id="coinsurance">
      <h2>4. Coinsurance</h2>
      <p class="def"><b>Your share of the bill as a percentage.</b> At 20 percent coinsurance, a $1,500 MRI costs you $300. An $8,000 infusion at the same 20 percent costs you $1,600.</p>
      __VIZ_COINS__
      <p>Coinsurance is where the unpredictability lives, because you cannot know your cost until you know the price, and prices for the same scan vary between hospitals. On Advantage plans it most often shows up on <strong>outpatient surgery, imaging, chemotherapy and infusions, durable medical equipment, and increasingly on dental</strong>. Our guide to <a href="/articles/medicare-advantage-dental-coinsurance-kentucky/">dental coinsurance on Advantage plans</a> walks through a crown under both designs.</p>
      <p>The protection against coinsurance is the next term. Coinsurance can produce a scary number on one bill, but it cannot take you past the maximum.</p>
      <p class="anoc"><b>On the Annual Notice of Change:</b> watch for a service moving from a copay to a percentage (an MRI going from "$250" to "20%"), and for the percentage itself rising. A change from 20 to 30 percent is a 50 percent increase in what you pay on every one of those bills.</p>
    </section>

    <section class="term" id="moop">
      <h2>5. Max out-of-pocket</h2>
      <p class="def"><b>The most you can pay in a calendar year</b> for covered medical care in the plan's network. Once your deductible, copays and coinsurance add up to this number, the plan pays 100 percent of covered care until January 1.</p>
      __VIZ_MOOP__
      <p>This is the number that makes a Medicare Advantage plan safe to carry, and it is the one Original Medicare by itself does not have. Federal rules cap what a plan may set it at: <strong>$9,250 in network for 2026 and $9,850 for 2027</strong>, with a higher combined limit on PPO plans that includes out-of-network care ($13,900 in 2026, $14,800 in 2027). Most plans set theirs well below the ceiling; the typical in-network limit on 2026 plans is in the <strong>$5,000 to $6,000</strong> range, lower on HMOs and higher on PPOs.</p>
      <p>Three things do <strong>not</strong> count toward it, and these are the ones that catch people: your premiums (plan and Part B), your prescription drug costs (those have their own cap, $2,100 in 2026 and $2,400 in 2027), and extras like dental, vision and hearing. So your true worst case for a year is <em>the maximum, plus twelve months of premiums, plus the drug cap</em>. For the sample plan that is $5,000 plus $2,434.80 in Part B premiums, about $7,435, before drugs.</p>
      <p class="anoc"><b>On the Annual Notice of Change:</b> this is the row to read first. A maximum going from $5,000 to $5,900 raises your worst-case year by $900 even if nothing else on the page moves. It is also the fairest single number for comparing two plans: a plan with slightly higher copays and a much lower maximum can be the safer choice.</p>
    </section>

    <h2>The mix-up: deductible versus maximum</h2>
    <p>Here is the mistake I see more than any other, and it runs in both directions.</p>
    <p>Someone opens the notice, sees "Maximum out-of-pocket: $5,900," and reads it as a deductible: <em>I have to pay $5,900 before this plan covers anything.</em> They are frightened by a number that is actually their protection. Or they see "Deductible: $0" and read it as a maximum: <em>I have no costs on this plan.</em> Then the first hospital stay arrives at $350 a day.</p>
    __VIZ_MIX__
    <p>The confusion is not a Medicare problem; it is a vocabulary problem that most of the country shares. In a national Policygenius survey, <strong>only 4 percent of insured adults could correctly define all four of deductible, copay, coinsurance and out-of-pocket maximum</strong>. Only 42 percent defined out-of-pocket maximum correctly, even though 67 percent said they understood it. A 2013 study in the Journal of Health Economics found 14 percent could answer all four concept questions. These were general-population surveys, not Medicare-specific, but nothing about turning 65 makes the words clearer.</p>
    <p>The fix is a single sentence to keep: <strong>the deductible is what you pay first; the maximum is the most you can pay, ever, in a year.</strong> One is a floor you step over on the way in. The other is a ceiling that most people never touch.</p>

    <h2>One whole year, all five at once</h2>
    <p>Meet Ruth, 71, in Nicholasville, on the sample plan. She is reasonably healthy until a knee gives out in June.</p>
    __VIZ_YEAR__
    <div class="tblwrap">
    <table class="nettbl">
      <tr><th>Month</th><th>What happened</th><th>Which term</th><th>She paid</th><th>Running total</th></tr>
      <tr><td>Jan</td><td>Primary care checkup</td><td>Copay</td><td class="in">$0</td><td>$0</td></tr>
      <tr><td>Feb</td><td>Orthopedic specialist</td><td>Copay</td><td>$45</td><td>$45</td></tr>
      <tr><td>May</td><td>MRI, $1,500 bill</td><td>Coinsurance, 20%</td><td>$300</td><td>$345</td></tr>
      <tr><td>Jun</td><td>Knee replacement, 4 hospital days</td><td>Copay, $350 a day</td><td>$1,400</td><td>$1,745</td></tr>
      <tr><td>Jul</td><td>Physical therapy, 20 visits</td><td>Copay, $40 a visit</td><td>$800</td><td>$2,545</td></tr>
      <tr><td>Aug</td><td>ER visit, then 3-day readmission</td><td>Copays</td><td>$1,175</td><td>$3,720</td></tr>
      <tr><td>Sep</td><td>Infusions, $8,000 bill (20% would be $1,600)</td><td>Coinsurance, capped</td><td class="out">$1,280</td><td><strong>$5,000</strong></td></tr>
      <tr><td>Oct to Dec</td><td>Follow-ups, more therapy, a scan</td><td>Maximum reached</td><td class="in">$0</td><td>$5,000</td></tr>
    </table>
    </div>
    <p class="vstamp">Sample plan arithmetic, not a quote. Deductible $0. Premiums and prescription drugs are separate and not shown.</p>
    <p>Notice what the year teaches. Through May, the plan cost Ruth $345: the copays and one coinsurance bill. The knee turned a cheap year into an expensive one in about ten weeks, and the per-day hospital copay was the biggest single line. In September the maximum did its job: the plan owed her 20 percent of $8,000, but she only had $1,280 of room left under the ceiling, so that is all she paid. For the rest of the year, every covered bill was $0.</p>
    <p>Her total for the year: <strong>$5,000 in cost sharing, plus $2,434.80 in Part B premiums, plus whatever her prescriptions cost under the separate drug cap.</strong> That is her worst case, and she knew it on January 1, because the maximum told her.</p>

    <h2>Now read your Annual Notice of Change</h2>
    <p>Your plan must get this notice to you by September 30 each year. It shows this year and next year side by side. With the five words in hand, it reads like this:</p>
    __VIZ_ANOC__
    <p>Here is how to use it, in order:</p>
    <div class="stage"><span class="num">1</span><span class="st"><b>Find the maximum out-of-pocket row first.</b>That is your worst case. If it went up, your worst case went up by that amount, full stop.</span></div>
    <div class="stage"><span class="num">2</span><span class="st"><b>Find the two or three rows you actually use.</b>Your specialists, your scans, your therapy, a hospital stay if one is likely. Multiply each change by how often you use it. Ignore rows for care you do not get.</span></div>
    <div class="stage"><span class="num">3</span><span class="st"><b>Check whether any copay became a percentage.</b>A dollar amount turning into "20%" is the change most likely to surprise you mid-year.</span></div>
    <div class="stage"><span class="num">4</span><span class="st"><b>Then look past the five words.</b>Your doctors and hospital still in network? Your drugs still on the list, same tier? Those two sections of the notice can matter more than any copay. Our <a href="/articles/annual-medicare-review-aep/">yearly plan review guide</a> covers them.</span></div>
    <div class="stage"><span class="num">5</span><span class="st"><b>Decide by December 7.</b>The Annual Enrollment Period runs October 15 to December 7. If next year's numbers no longer fit your year, that is the window to change. If they do, keeping the plan is a confident decision, not a default.</span></div>

    <div class="callout"><b>Why this is worth ten minutes a year.</b>A plan is not good or bad in the abstract. It is good or bad for the care you get. Once you can read these five rows, you are no longer trusting a brochure, a TV ad or a phone call; you are reading the contract and doing the arithmetic yourself. That is the whole point of understanding your coverage: fewer surprises, and the ability to say "I checked, and this is still right for me."</div>

    <div class="note">
      <div class="who">
        <img src="/assets/austin-tyler.jpg" alt="Austin Tyler" width="600" height="750">
        <div><b>A note from Austin</b><span>Licensed Kentucky Medicare agent, Lexington</span></div>
      </div>
      <p>When I sit down with someone's Annual Notice of Change, the first thing I do is put my finger on the maximum out-of-pocket row and ask, "Do you know what this number is?" More often than not the answer is a version of "that's what I have to pay before it kicks in." It is not. It is the opposite. And the relief on people's faces when they understand that is the reason I wanted this page to exist.</p>
      <p>The second thing I do is ask what care they actually had this year. That turns the table from twelve abstract rows into two or three that matter. Anyone can do that at their own kitchen table once they know the words.</p>
    </div>

    <h2 id="faq">Common questions from Kentucky</h2>
    <div class="faq">
      <h3>What is the difference between a deductible and an out-of-pocket maximum on Medicare Advantage?</h3>
      <p>The deductible is the amount you pay first, at the start of the year, before the plan shares costs on the services it applies to. Many Medicare Advantage plans set the medical deductible at $0. The out-of-pocket maximum is the most you can pay in a calendar year for covered in-network medical care, counting deductible, copays and coinsurance together. Once you reach it, the plan pays 100 percent of covered care until January 1. The deductible is the floor; the maximum is the ceiling.</p>
      <h3>Does a $0 premium Medicare Advantage plan mean I pay nothing?</h3>
      <p>No. A $0 premium means the plan charges no monthly fee of its own. You still pay the Part B premium to Medicare, $202.90 a month in 2026, and you still pay the plan's copays and coinsurance when you use care, up to its out-of-pocket maximum. About 59 percent of 2026 plan offerings have a $0 premium.</p>
      <h3>What is the maximum out-of-pocket limit for Medicare Advantage in 2027?</h3>
      <p>For 2027, a Medicare Advantage plan may set its in-network out-of-pocket maximum no higher than $9,850, up from $9,250 in 2026. PPO plans have a higher combined limit that includes out-of-network care: $14,800 in 2027, up from $13,900. Most plans set their limits lower; the typical in-network maximum on 2026 plans is roughly $5,000 to $6,000. Prescription drugs have a separate cap of $2,400 in 2027.</p>
      <h3>What counts toward the out-of-pocket maximum?</h3>
      <p>Your deductible, copays and coinsurance for covered Part A and Part B medical services in the plan's network. Premiums do not count, prescription drug costs do not count (they have their own cap), and extra benefits such as dental, vision and hearing do not count. On an HMO, out-of-network care generally does not count because it is generally not covered.</p>
      <h3>What is the difference between a copay and coinsurance?</h3>
      <p>A copay is a flat dollar amount, such as $45 for a specialist visit, fixed no matter what the visit cost. Coinsurance is a percentage of the bill, such as 20 percent of a $1,500 MRI, which is $300. Copays are predictable; coinsurance grows with the price of the service. Both count toward your out-of-pocket maximum.</p>
      <h3>When do I get the Annual Notice of Change and what should I check?</h3>
      <p>Your plan must deliver the Annual Notice of Change by September 30. Check the out-of-pocket maximum row first, then the copay and coinsurance rows for the care you actually use, then whether any copay became a percentage. After the cost rows, confirm your doctors and hospital are still in network and your drugs are still covered on the same tier. The Annual Enrollment Period to change plans runs October 15 to December 7.</p>
    </div>

    <div class="endcta">
      <h3>Want someone to read your notice with you?</h3>
      <p>Bring your Annual Notice of Change and a list of the care you had this year. I will go row by row, tell you what next year costs on the care you actually use, and say plainly whether the plan still fits. If it does, you will hear that. No charge.</p>
      <div class="row">
        <a class="btn" href="/review/">Get a free plan review &rarr;</a>
        <p class="callline">Or call me directly: <a href="tel:18596186443">(859) 618-6443</a></p>
      </div>
    </div>

    <section class="recap">
      <h2>Quick recap</h2>
      <div class="recap-item">Premium: the monthly bill regardless of use. A $0 plan premium still leaves the Part B premium ($202.90 in 2026) and all cost sharing.</div>
      <div class="recap-item">Deductible: the first dollars of the year you pay before the plan shares, on the services it applies to. Often $0 for medical on Advantage plans; the drug deductible is separate (up to $700 in 2027).</div>
      <div class="recap-item">Copay: a flat price per visit or per hospital day. Predictable, but multiply by frequency.</div>
      <div class="recap-item">Coinsurance: a percentage of the bill. Grows with the bill; common on surgery, imaging, infusions and now dental.</div>
      <div class="recap-item">Max out-of-pocket: the ceiling on covered in-network medical costs for the year. Plans may set it up to $9,250 in 2026 and $9,850 in 2027; most are $5,000 to $6,000. Premiums, drugs and extras do not count.</div>
      <div class="recap-item">The deductible is the floor, the maximum is the ceiling. Reading the maximum as "what I owe before coverage starts" is the most common mistake, and it runs the wrong way.</div>
      <div class="recap-item">On the Annual Notice of Change (by September 30), read the maximum first, then the rows for care you use, then network and drug list. Decide by December 7.</div>
    </section>

    <section class="kcheck">
      <h2>Test what you learned</h2>
      <p class="kc-sub">Five quick questions. Pick an answer to see if you're right, and why.</p>
      <div id="kcheck"></div>
    </section>
    <script>window.KCHECK = __KCHECK__;</script>

    <div class="sources">
      <b>Sources</b>
      CMS, CY2027 Medicare Advantage rate announcement and final rule (in-network out-of-pocket ceiling $9,850, combined $14,800; 2026 ceilings $9,250 and $13,900), as reported by BenefitsUSA, SmartMatch and the Nebraska Department of Insurance Medicare Advantage fact sheet &middot;
      KFF and RISE Health, Medicare Advantage 2026 plan landscape (59 percent of offerings at $0 premium; median plan maximum $5,900; average in-network maximum about $5,400) &middot;
      CMS, 2026 Part B premium $202.90 and deductible $283; Part D deductible $615 (2026) and $700 (2027); Part D cap $2,100 (2026) and $2,400 (2027) &middot;
      Fayette County plan count and $0-premium count from the CMS CY2026 landscape file, our extract &middot;
      Policygenius, national health insurance literacy survey (4 percent define all four terms; 42 percent define out-of-pocket maximum); Loewenstein et al., "Consumers' misunderstanding of health insurance," Journal of Health Economics, 2013 &middot;
      NCOA and Medicare.gov on the Annual Notice of Change (delivered by September 30) and the Annual Enrollment Period (October 15 to December 7).
      Checked October 2026. The sample plan and Ruth's year are illustrations, not quotes from any plan.
    </div>

    <p class="stamp"><b>Written and reviewed by Austin Tyler</b>, licensed Kentucky agent, NPN 20234188, Kentucky DOI license #1187780. Federal limits from the CMS CY2027 rate announcement; plan-landscape figures from KFF; Kentucky plan counts from the CMS landscape file, October 2026.</p>

    <p class="disclaim">This article is general information, not advice for your specific situation. The sample plan and the year walk-through are illustrations of how premiums, deductibles, copays, coinsurance and out-of-pocket maximums work and are not quotes from any plan; your plan's actual costs are in its Summary of Benefits and Evidence of Coverage and can change each year. No specific plan is named or recommended. Tyler Insurance Group is not connected with or endorsed by the United States government or the federal Medicare program. We do not offer every plan available in your area. Currently we represent 6 organizations which offer 158 products in your area. Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance Program (SHIP) to get information on all of your options.</p>
"""
for k, v in [("__VIZ_PREM__", VIZ_PREM), ("__VIZ_DED__", VIZ_DED), ("__VIZ_COPAY__", VIZ_COPAY), ("__VIZ_COINS__", VIZ_COINS),
             ("__VIZ_MOOP__", VIZ_MOOP), ("__VIZ_MIX__", VIZ_MIX), ("__VIZ_YEAR__", VIZ_YEAR), ("__VIZ_ANOC__", VIZ_ANOC)]:
    assert BODY.count(k) == 1, k; BODY = BODY.replace(k, v)

KCHECK = [
 {"q": "Your Annual Notice of Change says \"Maximum out-of-pocket: $5,900.\" What does that mean?",
  "options": ["You must pay $5,900 before the plan covers anything", "The most you can pay for covered in-network medical care in the year", "Your monthly premium times twelve", "The deductible for hospital stays"], "answer": 1,
  "why": "The maximum is the ceiling, not a hurdle. Once your deductible, copays and coinsurance add up to it, covered care is $0 for the rest of the year. Most people never reach it."},
 {"q": "A plan has a $0 premium and a $0 medical deductible. What will you pay when you use care?",
  "options": ["Nothing, the plan is free", "Copays and coinsurance, up to the out-of-pocket maximum, plus the Part B premium", "Only the Part B premium", "20 percent of everything"], "answer": 1,
  "why": "A $0 premium and $0 deductible mean no monthly plan fee and no entry hurdle. Copays and coinsurance still apply to each service, up to the maximum, and the Part B premium is still paid to Medicare."},
 {"q": "Your plan has 20 percent coinsurance on outpatient imaging. An MRI is billed at $1,500. What do you pay?",
  "options": ["$20", "$150", "$300", "$1,500"], "answer": 2,
  "why": "Coinsurance is a percentage of the bill: 20 percent of $1,500 is $300. The plan pays the other $1,200, and your $300 counts toward the out-of-pocket maximum."},
 {"q": "Which of these does NOT count toward your Medicare Advantage out-of-pocket maximum?",
  "options": ["A $45 specialist copay", "20 percent coinsurance on surgery", "Your Part B premium", "A $350-a-day hospital copay"], "answer": 2,
  "why": "Premiums never count toward the maximum, and neither do prescription drug costs or dental, vision and hearing extras. Copays and coinsurance for covered in-network medical care do."},
 {"q": "Ruth reaches her plan's $5,000 maximum in September. What does she pay for a covered follow-up scan in November?",
  "options": ["20 percent of the bill", "The usual copay", "$0", "The full bill, since the allowance is used up"], "answer": 2,
  "why": "Once the maximum is reached, the plan pays 100 percent of covered in-network medical care until the year resets on January 1."},
]
body_html = BODY.replace("__KCHECK__", json.dumps(KCHECK, ensure_ascii=False))

out = re.sub(r'(<nav class="crumb" aria-label="Breadcrumb">).*?(</nav>)',
             r'\1<a href="/">Home</a> &rsaquo; <a href="/articles/">Learning Center</a> &rsaquo; <a href="/articles/basics/">Medicare Basics</a> &rsaquo; '
             + CRUMB_LABEL + r'\2', out, count=1, flags=re.S)
out = re.sub(r'<span class="tag">.*?</span>', '<span class="tag">Medicare Basics · Costs &amp; Savings</span>', out, count=1, flags=re.S)
out = re.sub(r'<h1>.*?</h1>', f'<h1>{H1}</h1>', out, count=1, flags=re.S)
out = re.sub(r'(Local Kentucky Medicare agent · )[^<]*(</div>)', r'\1October 3, 2026 · 12 min read\2', out, count=1)
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
        node.update({"headline": H1, "description": DESC, "datePublished": "2026-10-03", "dateModified": "2026-10-03",
                     "articleSection": "Medicare Basics", "mainEntityOfPage": {"@type": "WebPage", "@id": URL}, "@id": URL + "#article"})
    elif t == "BreadcrumbList":
        node["itemListElement"] = [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.bluegrassmedicarehelp.com/"},
            {"@type": "ListItem", "position": 2, "name": "Learning Center", "item": "https://www.bluegrassmedicarehelp.com/articles/"},
            {"@type": "ListItem", "position": 3, "name": "Medicare Basics", "item": "https://www.bluegrassmedicarehelp.com/articles/basics/"},
            {"@type": "ListItem", "position": 4, "name": CRUMB_LABEL, "item": URL}]
    elif t == "FAQPage":
        node["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]
out = out[:mm.start(1)] + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + out[mm.end(1):]

os.makedirs(DST_DIR, exist_ok=True)
open(f"{DST_DIR}/index.html", "w", encoding="utf-8").write(out)
print(f"wrote {DST_DIR}/index.html ({len(pairs)} FAQ, {len(KCHECK)} kcheck)")
