#!/usr/bin/env python3
"""Build /articles/medicare-advantage-dental-coinsurance-kentucky/ by cloning chrome from an
existing article and swapping in new head, schema, body, visuals and knowledge check."""
import json, re, os

SRC = "articles/does-baptist-health-take-medicare-advantage/index.html"
DST_DIR = "articles/medicare-advantage-dental-coinsurance-kentucky"
URL = "https://www.bluegrassmedicarehelp.com/articles/medicare-advantage-dental-coinsurance-kentucky/"
TITLE = "Medicare Advantage Dental Coinsurance Explained (Kentucky)"
H1 = "Your Medicare Advantage Dental Allowance Has Fine Print Now: Coinsurance, Explained With One Crown"
DESC = ("Many Medicare Advantage dental benefits quietly added coinsurance. What a $1,000 allowance with 25% "
        "coinsurance really pays on a $500 crown, why plans are doing it, and how to check yours.")
CRUMB_LABEL = "Dental Coinsurance"

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
.viz{margin:10px 0 8px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px;}
.viz svg{width:100%;height:auto;display:block;}
.vizcap{font-size:14.5px;color:var(--faint);margin:6px 0 26px;line-height:1.5;}
.stamp{font-size:14.5px;color:var(--faint);margin:26px 0 0;}
.stamp b{color:var(--mute);font-weight:600;}
"""
out = out.replace("</style>", NEWCSS + "</style>")

F = 'font-family="Source Sans 3, Arial, sans-serif"'
# ---- Visual 1: two receipts for the same $500 crown
VIZ1 = f"""<figure class="viz" role="img" aria-label="Two receipts for the same $500 crown. Left, no coinsurance: you pay $0, the plan pays $500, $500 of the $1,000 allowance is left. Right, 25 percent coinsurance: you pay $125, the plan pays $375, $625 of the allowance is left.">
<svg viewBox="0 0 860 440" xmlns="http://www.w3.org/2000/svg">
<g {F}>
<text x="430" y="30" text-anchor="middle" font-size="19" font-weight="700" fill="#2a2620">The same $500 crown, two plan designs, same $1,000 allowance</text>
<!-- left receipt -->
<rect x="30" y="56" width="380" height="360" rx="14" fill="#faf6ef" stroke="#e2d9c8" stroke-width="2"/>
<rect x="30" y="56" width="380" height="54" rx="14" fill="#3a7d52"/>
<rect x="30" y="92" width="380" height="18" fill="#3a7d52"/>
<text x="220" y="90" text-anchor="middle" font-size="18" font-weight="700" fill="#fff">Plan A: no coinsurance</text>
<text x="56" y="150" font-size="16" fill="#5f594f">Crown, in network</text><text x="384" y="150" text-anchor="end" font-size="16" fill="#2a2620">$500</text>
<text x="56" y="186" font-size="16" fill="#5f594f">Your coinsurance</text><text x="384" y="186" text-anchor="end" font-size="16" fill="#2a2620">0%</text>
<line x1="56" y1="206" x2="384" y2="206" stroke="#e2d9c8" stroke-width="2"/>
<text x="56" y="244" font-size="18" font-weight="700" fill="#2a2620">You pay today</text><text x="384" y="244" text-anchor="end" font-size="26" font-weight="700" fill="#2f6844">$0</text>
<text x="56" y="282" font-size="16" fill="#5f594f">Plan pays</text><text x="384" y="282" text-anchor="end" font-size="16" fill="#2a2620">$500</text>
<text x="56" y="330" font-size="15" fill="#5f594f">Allowance used</text>
<rect x="56" y="342" width="328" height="20" rx="10" fill="#efe6d6"/>
<rect x="56" y="342" width="164" height="20" rx="10" fill="#3a7d52"/>
<text x="56" y="392" font-size="16" font-weight="700" fill="#2a2620">$500 of $1,000 left for the year</text>
<!-- right receipt -->
<rect x="450" y="56" width="380" height="360" rx="14" fill="#faf6ef" stroke="#e2d9c8" stroke-width="2"/>
<rect x="450" y="56" width="380" height="54" rx="14" fill="#b3431d"/>
<rect x="450" y="92" width="380" height="18" fill="#b3431d"/>
<text x="640" y="90" text-anchor="middle" font-size="18" font-weight="700" fill="#fff">Plan B: 25% coinsurance</text>
<text x="476" y="150" font-size="16" fill="#5f594f">Crown, in network</text><text x="804" y="150" text-anchor="end" font-size="16" fill="#2a2620">$500</text>
<text x="476" y="186" font-size="16" fill="#5f594f">Your coinsurance</text><text x="804" y="186" text-anchor="end" font-size="16" fill="#2a2620">25%</text>
<line x1="476" y1="206" x2="804" y2="206" stroke="#e2d9c8" stroke-width="2"/>
<text x="476" y="244" font-size="18" font-weight="700" fill="#2a2620">You pay today</text><text x="804" y="244" text-anchor="end" font-size="26" font-weight="700" fill="#b3431d">$125</text>
<text x="476" y="282" font-size="16" fill="#5f594f">Plan pays</text><text x="804" y="282" text-anchor="end" font-size="16" fill="#2a2620">$375</text>
<text x="476" y="330" font-size="15" fill="#5f594f">Allowance used</text>
<rect x="476" y="342" width="328" height="20" rx="10" fill="#efe6d6"/>
<rect x="476" y="342" width="123" height="20" rx="10" fill="#b3431d"/>
<text x="476" y="392" font-size="16" font-weight="700" fill="#2a2620">$625 of $1,000 left for the year</text>
</g></svg></figure>
<p class="vizcap">Figure 1. Same crown, same allowance. Coinsurance moves $125 onto you today and leaves more of the allowance unspent. Assumes the plan's share counts against the maximum, which is the usual design.</p>"""

# ---- Visual 2: three crowns in a year, stacked
VIZ2 = f"""<figure class="viz" role="img" aria-label="Bar chart of what you pay across one, two and three $500 crowns in a year. No coinsurance: $0, $0, then $500 once the allowance runs out, total $500. 25 percent coinsurance: $125, $250, $500 in total after three crowns.">
<svg viewBox="0 0 860 400" xmlns="http://www.w3.org/2000/svg">
<g {F}>
<text x="430" y="30" text-anchor="middle" font-size="19" font-weight="700" fill="#2a2620">What you have paid in total, as the year goes on</text>
<line x1="90" y1="330" x2="830" y2="330" stroke="#5f594f" stroke-width="2"/>
<!-- groups: 1 crown, 2 crowns, 3 crowns; scale $500 = 240px -->
<g>
<text x="215" y="362" text-anchor="middle" font-size="16" fill="#5f594f">After 1 crown</text>
<rect x="150" y="329" width="56" height="1" fill="#3a7d52"/><text x="178" y="316" text-anchor="middle" font-size="16" font-weight="700" fill="#2f6844">$0</text>
<rect x="224" y="270" width="56" height="60" rx="6" fill="#b3431d"/><text x="252" y="258" text-anchor="middle" font-size="16" font-weight="700" fill="#b3431d">$125</text>
</g>
<g>
<text x="460" y="362" text-anchor="middle" font-size="16" fill="#5f594f">After 2 crowns</text>
<rect x="395" y="329" width="56" height="1" fill="#3a7d52"/><text x="423" y="316" text-anchor="middle" font-size="16" font-weight="700" fill="#2f6844">$0</text>
<rect x="469" y="210" width="56" height="120" rx="6" fill="#b3431d"/><text x="497" y="198" text-anchor="middle" font-size="16" font-weight="700" fill="#b3431d">$250</text>
</g>
<g>
<text x="705" y="362" text-anchor="middle" font-size="16" fill="#5f594f">After 3 crowns</text>
<rect x="640" y="90" width="56" height="240" rx="6" fill="#3a7d52"/><text x="668" y="78" text-anchor="middle" font-size="16" font-weight="700" fill="#2f6844">$500</text>
<rect x="714" y="90" width="56" height="240" rx="6" fill="#b3431d"/><text x="742" y="78" text-anchor="middle" font-size="16" font-weight="700" fill="#b3431d">$500</text>
</g>
<rect x="90" y="382" width="16" height="16" rx="4" fill="#3a7d52"/><text x="114" y="395" font-size="15" fill="#2a2620">Plan A, no coinsurance</text>
<rect x="330" y="382" width="16" height="16" rx="4" fill="#b3431d"/><text x="354" y="395" font-size="15" fill="#2a2620">Plan B, 25% coinsurance</text>
<text x="830" y="395" text-anchor="end" font-size="14" fill="#6f6a60">$1,000 allowance, $500 crowns, in network</text>
</g></svg></figure>
<p class="vizcap">Figure 2. Plan A costs you nothing until the allowance is gone, then the whole third crown is yours. Plan B costs you something every time but stretches the allowance across all three. After three crowns both have cost you $500; the difference is when you paid it and how much the plan contributed in between.</p>"""

# ---- Visual 3: where it hides in the Summary of Benefits
VIZ3 = f"""<figure class="viz" role="img" aria-label="A mock Summary of Benefits dental row. Preventive dental shows $0 copay. Comprehensive dental shows 50 percent coinsurance, $1,000 annual maximum, highlighted. The word coinsurance is what to look for.">
<svg viewBox="0 0 860 250" xmlns="http://www.w3.org/2000/svg">
<g {F}>
<rect x="30" y="20" width="800" height="210" rx="12" fill="#fff" stroke="#e2d9c8" stroke-width="2"/>
<text x="56" y="56" font-size="15" font-weight="700" fill="#6f6a60" letter-spacing="1">SUMMARY OF BENEFITS, DENTAL (EXAMPLE LAYOUT)</text>
<line x1="56" y1="70" x2="804" y2="70" stroke="#e2d9c8" stroke-width="2"/>
<text x="56" y="106" font-size="17" fill="#2a2620">Preventive dental (exams, cleanings, x-rays)</text>
<text x="804" y="106" text-anchor="end" font-size="17" fill="#2f6844" font-weight="700">$0 copay</text>
<rect x="44" y="130" width="772" height="74" rx="10" fill="rgba(179,67,29,.08)" stroke="#b3431d" stroke-width="2.5"/>
<text x="56" y="162" font-size="17" fill="#2a2620">Comprehensive dental (fillings, crowns, dentures)</text>
<text x="804" y="162" text-anchor="end" font-size="17" fill="#b3431d" font-weight="700">50% coinsurance</text>
<text x="56" y="190" font-size="15" fill="#5f594f">In network. $1,000 combined annual maximum. Frequency limits apply.</text>
<text x="440" y="226" text-anchor="middle" font-size="15" font-weight="700" fill="#b3431d">This word is what you are looking for</text>
</g></svg></figure>
<p class="vizcap">Figure 3. An example of how the row usually reads. Preventive at $0 is nearly universal; the comprehensive row is where coinsurance shows up, and it is a percentage, not a dollar copay.</p>"""

BODY = r"""
    <p>A client called me in the spring after a crown. Same plan she had the year before, same dentist, same tooth that had been bothering her since Christmas. The bill was $250. The year before, the same work had cost her nothing.</p>
    <p>Nothing had gone wrong with her claim. Her plan's dental benefit had changed shape on January 1, in a line of the Annual Notice of Change she had not read, and the change has a name most people have never had explained to them: <strong>coinsurance</strong>.</p>

    <div class="ans">
      <p><strong>Many Medicare Advantage plans have moved their dental benefit from "the plan pays, up to an allowance" to "you pay a percentage of every procedure, and the plan pays the rest up to a maximum."</strong> The headline dollar figure often looks the same or bigger. What you pay at the dentist's chair does not.</p>
      <p>Below: the same $500 crown under both designs, why carriers are making this change, and the three documents where you can check your own plan in about ten minutes. The short version of that last part: <strong>look at the comprehensive dental row and find out whether it says a dollar amount or a percentage.</strong></p>
    </div>

    <h2>Two words that sound alike and are not</h2>
    <p><strong>An allowance</strong> (also called an annual maximum or benefit maximum) is the most the plan will pay toward dental work in a year. Spend past it and the rest is yours.</p>
    <p><strong>Coinsurance</strong> is your share of each procedure, as a percentage. With 25 percent coinsurance on a $500 crown, you pay $125 at the counter and the plan pays $375. With 50 percent, you pay $250.</p>
    <p>A plan can have an allowance with no coinsurance, an allowance with coinsurance, or in a few cases coinsurance with no allowance at all. The first design is the one most people picture when they hear "dental allowance." The second is the one more and more of them actually have.</p>

    <h2>The same crown, two ways</h2>
    <p>Here is the example that makes it click. Two people, two plans, both with a <strong>$1,000 annual dental allowance</strong>, both needing one <strong>$500 crown</strong>, both at an in-network dentist with nothing else used that year.</p>
    __VIZ1__
    <p>On Plan A you walk out owing nothing and have $500 left for the rest of the year. On Plan B you walk out owing $125 and have $625 left. Notice that Plan B's allowance lasts longer. That is not an accident, and it is how a plan with coinsurance can advertise a bigger maximum while costing you more at the chair.</p>

    <h3>Where it goes from there</h3>
    <p>One crown rarely stays one crown. Watch what happens across a year:</p>
    __VIZ2__
    <div class="tblwrap">
    <table class="nettbl">
      <tr><th>$500 crown, $1,000 allowance</th><th>No coinsurance</th><th>25% coinsurance</th><th>50% coinsurance</th></tr>
      <tr><td>You pay at the chair</td><td class="in">$0</td><td>$125</td><td class="out">$250</td></tr>
      <tr><td>Plan pays</td><td>$500</td><td>$375</td><td>$250</td></tr>
      <tr><td>Allowance left after one crown</td><td>$500</td><td>$625</td><td>$750</td></tr>
      <tr><td>Second crown: you pay</td><td class="in">$0</td><td>$125</td><td class="out">$250</td></tr>
      <tr><td>Third crown: you pay</td><td class="out">$500 (allowance gone)</td><td>$250</td><td>$250</td></tr>
      <tr><td><strong>Three crowns, your total</strong></td><td><strong>$500</strong></td><td><strong>$500</strong></td><td><strong>$750</strong></td></tr>
    </table>
    </div>
    <p class="vstamp">Arithmetic, not a quote from any plan. Assumes the plan's paid share counts against the annual maximum, which is the common design. Some plans apply the maximum differently; your Evidence of Coverage says which.</p>
    <p>Two things this table teaches. First, <strong>if you need one or two things done in a year, coinsurance costs you money that the no-coinsurance plan would have covered entirely.</strong> Second, if you need a lot done, the difference narrows or disappears, because the no-coinsurance allowance runs out sooner. Which design is better for you depends on how much dental work you actually expect, which is why "the plan with the bigger allowance" is the wrong question.</p>

    <h2>Why plans are doing this</h2>
    <p>This is a national shift, not something that happened only to you. Milliman's analysis of 2026 Medicare Advantage plans found that the value of supplemental benefits the plans added on top of Medicare fell by about <strong>$7 per member per month</strong> from 2025 to 2026, that <strong>standalone comprehensive dental limits declined about 8 percent</strong>, and that plans restructured so preventive dental is fully covered while <strong>major work carries significant cost sharing</strong>. KFF, which tracks the market each year, notes that 98 percent of plans offer dental and that plans routinely change the annual maximum and the cost sharing from one year to the next. Over-the-counter allowances fell about 13 percent in the same period and fewer plans offer transportation.</p>
    <p>The reasons the carriers give are the ones you would expect: medical costs rose faster than Medicare's payments to the plans in the 2025 and 2026 rate years, and carriers say they are concentrating benefits where members use them. There is a second, quieter reason that the receipts above make obvious. <strong>Coinsurance shares the cost of every procedure with you, and it makes the advertised maximum stretch further.</strong> A plan can keep a $1,500 dental figure on the brochure, add 50 percent coinsurance underneath it, and pay out less than it did on a $1,000 allowance with no coinsurance. Neither of those motives is sinister. Both are reasons to read the row rather than the headline.</p>

    <h2>Why this matters more in Kentucky</h2>
    <p>Dental benefits are a nice-to-have in some states. Here they are decision-relevant. <strong>24.8 percent of Kentuckians 65 and older have lost all of their natural teeth, the fifth highest rate in the country</strong>, against a national figure of about 14 percent. Just over half of Kentuckians over 65 have had six or more teeth extracted, compared with about 40 percent nationally. Fewer than six in ten Kentucky adults saw a dentist last year.</p>
    <p>In practical terms, the people reading this page in Lexington, Winchester, Nicholasville, Georgetown and Richmond are more likely than almost anyone in the country to need crowns, extractions, partials and dentures, which is exactly the "comprehensive" category where coinsurance now lives. For a Kentuckian, the dental row is not fine print. It can be the largest out-of-pocket line on the plan.</p>
    <p class="vstamp">Sources: Kentucky Department for Public Health oral health data (BRFSS), CDC National Center for Health Statistics data brief on tooth loss among older adults, America's Health Rankings 2024 dental visit measure. Checked October 2026.</p>

    <h2>How to check whether your plan has coinsurance</h2>
    <p>Three documents, one phone call, ten minutes. Do this before you need the work, not in the dentist's chair.</p>
    <div class="stage"><span class="num">1</span><span class="st"><b>The Summary of Benefits, dental section</b>Find the row for comprehensive dental (sometimes "restorative" or listed by service: fillings, crowns, dentures). If it reads as a dollar amount or "$0 copay," there is no coinsurance on that service. If it reads as a percentage, that is your share of every procedure. Here is how the row usually looks:</span></div>
    __VIZ3__
    <div class="stage"><span class="num">2</span><span class="st"><b>The Evidence of Coverage, benefits chart</b>This is the long document, and the dental section answers the questions the summary skips: the annual maximum and whether preventive counts against it, whether the maximum is per year or combined with vision and hearing, frequency limits (a crown on the same tooth once every five years is typical), any waiting period, and whether out-of-network dentists are covered at all. It is on the plan's website and they will mail it on request.</span></div>
    <div class="stage"><span class="num">3</span><span class="st"><b>The Annual Notice of Change, every September</b>The table titled something like "Changes to benefits and costs for next year" will show the dental row with this year's design in one column and next year's in the other. This is the single page that would have saved my client $250. Read that row every fall before you decide whether to stay.</span></div>
    <div class="stage"><span class="num">4</span><span class="st"><b>One call to the plan, three questions</b>Is there coinsurance on crowns, root canals, extractions and dentures, and what percentage? Does the amount the plan pays count against my annual maximum, or the total charge? Is my dentist in the plan's <em>dental</em> network? That last one matters because many plans run dental through a separate administrator, and a dentist who takes your medical plan may not be in the dental network at all.</span></div>
    <div class="stage"><span class="num">5</span><span class="st"><b>Before any major work, ask the dentist for a pre-treatment estimate</b>Dental offices do this routinely: they send the proposed treatment to the plan and get back, in writing, what the plan will pay and what you will owe. It costs nothing and it is the only way to know your number before the drill starts.</span></div>

    <div class="callout"><b>Last year's answer is not this year's answer.</b>A plan can carry the same name, the same premium and the same card and change its dental design on January 1. KFF documents plans adjusting dental maximums and cost sharing year to year, and the Annual Notice of Change exists because of it. The row you checked in 2025 tells you nothing about 2027. Check it every fall.</div>

    <div class="note">
      <div class="who">
        <img src="/assets/austin-tyler.jpg" alt="Austin Tyler" width="600" height="750">
        <div><b>A note from Austin</b><span>Licensed Kentucky Medicare agent, Lexington</span></div>
      </div>
      <p>In the Annual Notices of Change my clients have brought me for this coming year, the pattern is the same one Milliman found nationally: plan after plan that paid dental up to an allowance last year now has a percentage sitting under the same dollar figure. The number on the brochure did not move. What moves is the bill.</p>
      <p>I do not think most people would have chosen their plan differently if they had known. I do think they would have budgeted differently, and some would have had the crown done in December instead of January. That is what a ten-minute check buys you.</p>
    </div>

    <h2>A few traps around the edges</h2>
    <ul>
      <li><strong>A "flex card" is not a dental allowance.</strong> Some plans load a prepaid card with a combined amount for dental, vision, hearing and sometimes groceries. It spends differently and it can carry its own rules. Our guide to <a href="/articles/medicare-flex-card-truth/">what the Medicare flex card really is</a> covers that.</li>
      <li><strong>Implants are often excluded or capped separately</strong>, even on plans that cover crowns and dentures well. Check the exclusions list, not just the maximum.</li>
      <li><strong>Out-of-network can mean zero.</strong> On many HMO dental networks there is no out-of-network benefit at all. On others you pay a higher percentage. Confirm your dentist by name in the plan's dental directory.</li>
      <li><strong>The allowance does not roll over.</strong> Unused dental benefit disappears on December 31, which is why the timing of major work matters.</li>
    </ul>
    <p>If you are weighing whether an Advantage plan's extras are worth the network trade-off in the first place, our honest look at <a href="/articles/is-medicare-advantage-worth-it/">whether Medicare Advantage is worth it</a> is the place to start, and the <a href="/articles/does-medicare-cover-dental-vision-hearing/">dental, vision and hearing guide</a> covers what Original Medicare does and does not pay.</p>

    <h2 id="faq">Common questions from Kentucky</h2>
    <div class="faq">
      <h3>What is dental coinsurance on a Medicare Advantage plan?</h3>
      <p>Coinsurance is the percentage of each dental procedure you pay yourself, with the plan paying the rest up to its annual maximum. With 25 percent coinsurance, a $500 crown costs you $125; with 50 percent, $250. It applies to comprehensive services such as fillings, crowns, root canals, extractions and dentures. Preventive care such as exams and cleanings is usually covered at $0 regardless.</p>
      <h3>What is the difference between a dental allowance and coinsurance?</h3>
      <p>An allowance, also called an annual or benefit maximum, is the most the plan will pay toward dental care in a year. Coinsurance is your share of each procedure. A plan can have an allowance with no coinsurance, in which case the plan pays procedures in full until the allowance is used, or an allowance with coinsurance, in which case you pay a percentage of each procedure and the plan's share counts against the maximum. The headline allowance can be identical on both designs while what you pay at the dentist is very different.</p>
      <h3>How do I know if my Medicare Advantage dental benefit has coinsurance?</h3>
      <p>Look at the comprehensive dental row in your plan's Summary of Benefits. A dollar amount or "$0 copay" means no coinsurance on that service; a percentage means coinsurance. The Evidence of Coverage benefits chart gives the annual maximum, frequency limits, waiting periods and network rules. Each September the Annual Notice of Change shows the dental row for this year and next side by side. Confirm by calling the plan and asking the percentage on crowns, root canals, extractions and dentures.</p>
      <h3>Why did my plan add dental coinsurance this year?</h3>
      <p>It is part of a national shift. Milliman's analysis of 2026 plans found supplemental benefit value fell about $7 per member per month from 2025, standalone comprehensive dental limits fell about 8 percent, and plans restructured so preventive dental is fully covered while major work carries significant cost sharing. Carriers cite medical costs rising faster than Medicare payments. Coinsurance also shares each procedure's cost with the member and makes the advertised maximum last longer.</p>
      <h3>Can my dental benefit change next year even if I keep the same plan?</h3>
      <p>Yes. Medicare Advantage plans can change the dental annual maximum, add or raise coinsurance, change frequency limits and change the dental network each January while keeping the same plan name. The Annual Notice of Change you receive by September 30 lists these changes in its benefits table. Read the dental row every fall before deciding whether to stay.</p>
      <h3>Is a $1,500 allowance with 50 percent coinsurance better than $1,000 with none?</h3>
      <p>Not automatically. On a single $500 crown, the $1,000 no-coinsurance plan costs you $0 and the $1,500 plan with 50 percent coinsurance costs you $250. The larger plan only pulls ahead if you need enough work to exhaust the smaller allowance, roughly $1,000 or more of dental in a year. The right comparison is how much dental work you realistically expect, not which number is bigger on the brochure.</p>
    </div>

    <div class="endcta">
      <h3>Not sure what your dental row says?</h3>
      <p>Bring me your Annual Notice of Change, or the name of your plan, and I will read the dental row with you and tell you what a crown would actually cost on it next year. No charge. If your plan is still the right one, you will hear that too.</p>
      <div class="row">
        <a class="btn" href="/review/">Get a free plan review &rarr;</a>
        <p class="callline">Or call me directly: <a href="tel:18596186443">(859) 618-6443</a></p>
      </div>
    </div>

    <section class="recap">
      <h2>Quick recap</h2>
      <div class="recap-item">An allowance is the most the plan pays in a year. Coinsurance is your percentage of each procedure. A plan can have the same allowance with or without coinsurance, and the bill at the chair is very different.</div>
      <div class="recap-item">$1,000 allowance, $500 crown: no coinsurance costs you $0; 25 percent costs you $125; 50 percent costs you $250. Coinsurance also makes the allowance last longer, which is how a bigger advertised maximum can pay out less.</div>
      <div class="recap-item">Nationally, supplemental benefit value fell about $7 a month per member from 2025 to 2026 and standalone comprehensive dental limits fell about 8 percent, with major work shifting to significant cost sharing (Milliman).</div>
      <div class="recap-item">Kentucky ranks fifth in the nation for complete tooth loss over 65 (24.8 percent), so the comprehensive dental row is where Kentuckians' money actually goes.</div>
      <div class="recap-item">Check the comprehensive dental row in the Summary of Benefits: a dollar amount means no coinsurance, a percentage means coinsurance. Confirm maximums, frequency limits and the dental network in the Evidence of Coverage.</div>
      <div class="recap-item">Read the dental row in your Annual Notice of Change every September. Last year's design does not carry over.</div>
      <div class="recap-item">Before any major work, ask the dentist for a pre-treatment estimate so you know your number before the drill starts.</div>
    </section>

    <section class="kcheck">
      <h2>Test what you learned</h2>
      <p class="kc-sub">Five quick questions. Pick an answer to see if you're right, and why.</p>
      <div id="kcheck"></div>
    </section>
    <script>window.KCHECK = __KCHECK__;</script>

    <div class="sources">
      <b>Sources</b>
      KFF, Medicare Advantage 2026 Spotlight and "Medicare and Dental Coverage: A Closer Look" (98 percent of plans offer dental; parameters change year to year; major work often carries coinsurance) &middot;
      Milliman, State of the 2026 Medicare Advantage Industry and Trends in Medicare Advantage Benefits 2023 to 2026 (supplemental value down about $7 PMPM; standalone comprehensive dental limits down about 8 percent; preventive covered, major work with significant cost sharing) &middot;
      ATI Advisory, CY2026 Medicare Advantage Trends in Supplemental Benefits &middot;
      Kentucky Department for Public Health oral health data (BRFSS); CDC NCHS Data Brief 368, tooth loss among older adults; America's Health Rankings, dental visit, Kentucky.
      Checked October 2026. The crown examples are arithmetic, not quotes from any plan.
    </div>

    <p class="stamp"><b>Written and reviewed by Austin Tyler</b>, licensed Kentucky agent, NPN 20234188, Kentucky DOI license #1187780. National benefit-design figures from KFF and Milliman; Kentucky oral health figures from Kentucky DPH and CDC, October 2026.</p>

    <p class="disclaim">This article is general information, not advice for your specific situation. The dollar examples are illustrations of how allowances and coinsurance work and are not quotes from any plan; your plan's actual maximums, coinsurance, frequency limits, networks and exclusions are in its Evidence of Coverage and can change each year. No specific plan is named or recommended. Tyler Insurance Group is not connected with or endorsed by the United States government or the federal Medicare program. We do not offer every plan available in your area. Currently we represent 6 organizations which offer 158 products in your area. Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance Program (SHIP) to get information on all of your options.</p>
"""
BODY = BODY.replace("__VIZ1__", VIZ1).replace("__VIZ2__", VIZ2).replace("__VIZ3__", VIZ3)

KCHECK = [
 {"q": "Your plan has a $1,000 dental allowance with 25% coinsurance. A crown costs $500. What do you pay at the dentist?",
  "options": ["$0", "$125", "$250", "$500"], "answer": 1,
  "why": "25 percent of $500 is $125. The plan pays the other $375, which counts against your $1,000 maximum, leaving $625."},
 {"q": "Same crown, same $1,000 allowance, but no coinsurance. What do you pay?",
  "options": ["$0", "$125", "$250", "$500"], "answer": 0,
  "why": "With no coinsurance the plan pays procedures in full until the allowance is used. You pay nothing and have $500 left for the year."},
 {"q": "Where in your plan documents does dental coinsurance usually show up?",
  "options": ["The preventive dental row", "The comprehensive dental row, as a percentage", "The premium line", "It is never written down"], "answer": 1,
  "why": "Preventive is nearly always $0. Coinsurance appears on comprehensive services such as crowns and dentures, written as a percentage rather than a dollar copay."},
 {"q": "Your dental benefit had no coinsurance in 2026. What does that tell you about 2027?",
  "options": ["It will be the same", "Nothing, until you read the Annual Notice of Change", "It can only improve", "Coinsurance cannot be added mid-contract"], "answer": 1,
  "why": "Plans can change dental maximums and cost sharing every January under the same plan name. The Annual Notice of Change each September is where the change appears."},
 {"q": "What is the one thing to do before major dental work on an Advantage plan?",
  "options": ["Pay cash and file later", "Ask the dentist for a pre-treatment estimate from the plan", "Switch plans first", "Nothing, the allowance covers it"], "answer": 1,
  "why": "A pre-treatment estimate tells you in writing what the plan will pay and what you will owe before the work is done. Dental offices do this routinely and it costs nothing."},
]
body_html = BODY.replace("__KCHECK__", json.dumps(KCHECK, ensure_ascii=False))

out = re.sub(r'(<nav class="crumb" aria-label="Breadcrumb">).*?(</nav>)',
             r'\1<a href="/">Home</a> &rsaquo; <a href="/articles/">Learning Center</a> &rsaquo; <a href="/articles/coverage/">Coverage Choices</a> &rsaquo; '
             + CRUMB_LABEL + r'\2', out, count=1, flags=re.S)
out = re.sub(r'<span class="tag">.*?</span>', '<span class="tag">Coverage Choices · Costs &amp; Savings</span>', out, count=1, flags=re.S)
out = re.sub(r'<h1>.*?</h1>', f'<h1>{H1}</h1>', out, count=1, flags=re.S)
out = re.sub(r'(Local Kentucky Medicare agent · )[^<]*(</div>)', r'\1October 2, 2026 · 11 min read\2', out, count=1)
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
