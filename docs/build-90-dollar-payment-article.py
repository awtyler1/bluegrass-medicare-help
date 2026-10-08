#!/usr/bin/env python3
"""Build /articles/90-dollar-medicare-payment-kentucky/ from the shared article chrome."""
import json, re, os

SRC = "articles/does-baptist-health-take-medicare-advantage/index.html"
SLUG = "90-dollar-medicare-payment-kentucky"
DST_DIR = f"articles/{SLUG}"
URL = f"https://www.bluegrassmedicarehelp.com/articles/{SLUG}/"
TITLE = "The $90 Medicare Payment: Who Gets It in Kentucky"
H1 = "The $90 Medicare Payment: Who Gets It, Who Doesn't, and What It Means for Kentuckians"
DESC = ("A one-time $90 Part B rebate started landing October 8. Who qualifies, why Medicare Advantage members are left out, "
        "where the money comes from, how many Kentuckians get it, and the scams to expect.")
CRUMB_LABEL = "The $90 Payment"

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
.ans ul{margin:0;padding-left:22px;} .ans li{font-size:18px;margin:0 0 8px;line-height:1.5;} .ans li:last-child{margin-bottom:0;}
.viz{margin:10px 0 8px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px;}
.viz svg{width:100%;height:auto;display:block;}
.vizcap{font-size:14.5px;color:var(--faint);margin:6px 0 26px;line-height:1.5;}
.stamp{font-size:14.5px;color:var(--faint);margin:26px 0 0;}
.stamp b{color:var(--mute);font-weight:600;}
.twocol{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:0 0 26px;}
.twocol>div{border-radius:14px;padding:18px 20px;border:1px solid var(--line);}
.twocol .yes{background:#eef5f0;border-color:#b9d4c2;} .twocol .no{background:#fbeee8;border-color:#e8c4b4;}
.twocol b{display:block;font-family:var(--serif);font-size:19px;margin-bottom:10px;}
.twocol ul{margin:0;padding-left:20px;} .twocol li{font-size:16.5px;margin:0 0 7px;line-height:1.5;}
@media(max-width:640px){.twocol{grid-template-columns:1fr;}}
.updated{font-size:15px;color:var(--mute);background:var(--cream2);border:1px solid var(--line);border-radius:10px;padding:10px 14px;margin:0 0 22px;}
"""
out = out.replace("</style>", NEWCSS + "</style>")

F = 'font-family="Source Sans 3, Arial, sans-serif"'
INK, MUTE, FAINT, LINE, WARM, GREEN, GREEN_D, CORAL_D = "#2a2620", "#5f594f", "#938c80", "#e2d9c8", "#efe6d6", "#3a7d52", "#2f6844", "#b3431d"
def viz(label, w, h, inner, cap):
    return (f'<figure class="viz" role="img" aria-label="{label}">\n<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg"><g {F}>\n{inner}\n</g></svg></figure>\n<p class="vizcap">{cap}</p>')

# Visual 1: four-question eligibility path
def q(y, text, no_text):
    return (f'<rect x="60" y="{y}" width="430" height="58" rx="12" fill="{WARM}" stroke="{LINE}" stroke-width="1.5"/>'
            f'<text x="275" y="{y+35}" text-anchor="middle" font-size="16.5" font-weight="700" fill="{INK}">{text}</text>'
            f'<line x1="490" y1="{y+29}" x2="560" y2="{y+29}" stroke="{CORAL_D}" stroke-width="2"/>'
            f'<rect x="560" y="{y+6}" width="250" height="46" rx="10" fill="#fbeee8" stroke="#e8c4b4" stroke-width="1.5"/>'
            f'<text x="685" y="{y+28}" text-anchor="middle" font-size="13.5" fill="{CORAL_D}" font-weight="700">No $90</text>'
            f'<text x="685" y="{y+45}" text-anchor="middle" font-size="12.5" fill="{MUTE}">{no_text}</text>'
            f'<line x1="275" y1="{y+58}" x2="275" y2="{y+86}" stroke="{GREEN_D}" stroke-width="2.5"/>'
            f'<text x="290" y="{y+78}" font-size="13" fill="{GREEN_D}" font-weight="700">yes</text>')
VIZ_ELIG = viz("Four yes-or-no questions. Are you in Original Medicare, not a Medicare Advantage plan? Does Medicaid or a Medicare Savings Program pay your Part B premium? Do you pay an income-related surcharge, IRMAA? Do you live in the United States? Answering yes, no, no, yes leads to a $90 payment; any other answer means no payment.", 860, 470,
    f'<text x="430" y="30" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}">Do I get the $90? Four questions</text>'
    + q(52, "Are you in Original Medicare (not an Advantage plan)?", "Advantage members are excluded")
    .replace('fill="#fbeee8"','fill="#fbeee8"')
    + q(138, "Do you pay your own Part B premium (not Medicaid)?", "Medicaid or MSP pays it: excluded")
    + q(224, "Is your premium the standard amount (no IRMAA)?", "Higher-income surcharge: excluded")
    + q(310, "Do you live in the United States?", "Living abroad: excluded")
    + f'<rect x="60" y="396" width="430" height="58" rx="12" fill="{GREEN_D}"/>'
    f'<text x="275" y="432" text-anchor="middle" font-size="18" font-weight="700" fill="#fff">$90, automatically. Nothing to apply for.</text>'
    f'<text x="560" y="420" font-size="13" fill="{MUTE}">Medigap or a standalone drug plan</text>'
    f'<text x="560" y="438" font-size="13" fill="{MUTE}">does not change the answer.</text>',
    "Figure 1. Four yes-or-no questions settle it. The first one is the big one in Kentucky: more than half of the state's Medicare members are on an Advantage plan, and none of them qualify.")

# Visual 2: Kentucky by the numbers
VIZ_KY = viz("Horizontal bars for Kentucky. All Medicare: 1,012,834. Enrolled in Medicare Advantage, excluded: 562,671. Original Medicare: 450,163. Our estimate of Kentuckians who receive the $90: roughly 320,000.", 860, 300,
    f'<text x="430" y="30" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}">Kentucky: who is in the pool</text>'
    f'<text x="60" y="76" font-size="15" fill="{MUTE}">Everyone on Medicare in Kentucky</text>'
    f'<rect x="60" y="84" width="740" height="30" rx="6" fill="{LINE}"/>'
    f'<text x="792" y="105" text-anchor="end" font-size="15" font-weight="700" fill="{INK}">1,012,834</text>'
    f'<text x="60" y="140" font-size="15" fill="{MUTE}">On a Medicare Advantage plan (not eligible)</text>'
    f'<rect x="60" y="148" width="411" height="30" rx="6" fill="{CORAL_D}"/>'
    f'<text x="463" y="169" text-anchor="end" font-size="15" font-weight="700" fill="#fff">562,671</text>'
    f'<text x="60" y="204" font-size="15" fill="{MUTE}">On Original Medicare (the pool the $90 draws from)</text>'
    f'<rect x="60" y="212" width="329" height="30" rx="6" fill="{GREEN}"/>'
    f'<text x="381" y="233" text-anchor="end" font-size="15" font-weight="700" fill="#fff">450,163</text>'
    f'<text x="60" y="268" font-size="15" fill="{MUTE}">Likely to receive it, after Medicaid and IRMAA exclusions (our estimate)</text>'
    f'<rect x="60" y="276" width="234" height="16" rx="5" fill="{GREEN_D}"/>'
    f'<text x="304" y="289" font-size="15" font-weight="700" fill="{GREEN_D}">about 320,000</text>',
    "Figure 2. Counts from the CMS Medicare Advantage penetration file, August 2026. The last bar is our estimate, applying the national ratio (about 72 percent of Original Medicare enrollees qualify) to Kentucky; CMS had not published a state count as of October 8.")

# Visual 3: $90 against the premium
VIZ_PREM = viz("A bar for one month of Part B premium, $202.90, with a $90 slice marked, 44 percent of the month. Below it a bar for a year, $2,434.80, with the $90 slice at 3.7 percent. A note shows the projected 2027 increase of about $6.60 a month, about $79 a year.", 860, 290,
    f'<text x="430" y="30" text-anchor="middle" font-size="18" font-weight="700" fill="{INK}">How far $90 goes against the Part B premium</text>'
    f'<text x="60" y="72" font-size="15" fill="{MUTE}">One month of Part B, 2026: $202.90</text>'
    f'<rect x="60" y="80" width="740" height="34" rx="7" fill="{WARM}"/>'
    f'<rect x="60" y="80" width="328" height="34" rx="7" fill="{GREEN_D}"/>'
    f'<text x="224" y="103" text-anchor="middle" font-size="15" font-weight="700" fill="#fff">$90 = 44% of one month</text>'
    f'<text x="60" y="156" font-size="15" fill="{MUTE}">One year of Part B, 2026: $2,434.80</text>'
    f'<rect x="60" y="164" width="740" height="34" rx="7" fill="{WARM}"/>'
    f'<rect x="60" y="164" width="27" height="34" rx="7" fill="{GREEN_D}"/>'
    f'<text x="98" y="187" font-size="15" font-weight="700" fill="{GREEN_D}">$90 = 3.7% of the year</text>'
    f'<rect x="60" y="222" width="740" height="46" rx="10" fill="#fff" stroke="{CORAL_D}" stroke-width="2"/>'
    f'<text x="80" y="242" font-size="14.5" fill="{INK}">Projected 2027 premium: $209.50 (Trustees), up about $6.60 a month, about $79 a year.</text>'
    f'<text x="80" y="260" font-size="14.5" fill="{MUTE}">At that rate the increase alone uses up the $90 in about 14 months. Private forecasts run higher.</text>',
    "Figure 3. Real money, and a small share of the bill. The projection is from the 2026 Medicare Trustees report; CMS announces the actual 2027 premium in November.")

BODY = r"""
    <p class="updated">Updated October 8, 2026, the day direct deposits began. Figures come from the CMS rebate FAQ and the White House fact sheet as reported by the Associated Press, KFF, CNBC, CBS and Kiplinger, and from our own extract of the CMS Kentucky enrollment file. We will update this page when the 2027 Part B premium is announced in November.</p>
    <p>If you checked your bank account this morning and found an extra $90 from Social Security, that is the Medicare Part B rebate the White House announced on Friday, October 2. If you checked and found nothing, you are in the majority in Kentucky, and there is probably nothing wrong with your account. This page explains who gets the payment, why the rules fall where they do, where the money comes from, what it does and does not change, and the phone calls you should expect to receive about it.</p>

    <div class="ans">
      <p><strong>The short version:</strong></p>
      <ul>
        <li><strong>It is a one-time $90 payment</strong>, not a monthly change to your premium, sent to about 20.8 million people nationally.</li>
        <li><strong>You get it only if you are on Original Medicare</strong>, pay the standard Part B premium yourself, and live in the U.S. Medicare Advantage members, people whose Part B is paid by Medicaid, and higher-income people paying the IRMAA surcharge do not get it.</li>
        <li><strong>There is nothing to apply for</strong>. It arrives by direct deposit (most people, around October 8) or by a Treasury check later in October. Anyone who calls, texts or emails asking you to "claim" it is a scammer.</li>
        <li><strong>In Kentucky, roughly one person in three on Medicare receives it</strong>, by our estimate: about 320,000 of just over a million.</li>
        <li><strong>It does not change what plan is right for you</strong>, and the Annual Enrollment Period that opens October 15 should be decided on next year's costs, not on this payment.</li>
      </ul>
    </div>

    <h2>Who gets the $90</h2>
    <p>The Centers for Medicare &amp; Medicaid Services set four conditions. You must be enrolled in Part B. You must be in Original Medicare, meaning Medicare itself pays your claims, rather than in a Medicare Advantage plan. You must pay your own Part B premium, so Medicaid or a Medicare Savings Program cannot be paying it for you. And you must pay the standard premium, $202.90 a month in 2026, rather than a higher income-related amount. You also have to live in the United States.</p>
    __VIZ_ELIG__
    <p>Two things that do <strong>not</strong> matter: having a Medicare Supplement (Medigap) policy, and having a standalone Part D drug plan. Both sit on top of Original Medicare, so people with Plan G or Plan N and a drug plan qualify like anyone else on Original Medicare. Railroad retirees, whose Part B runs through the Railroad Retirement Board rather than Social Security, should look for the Board's own notice; its Medicare line is 877-772-5772.</p>

    <div class="twocol">
      <div class="yes"><b>Gets the $90</b>
        <ul>
          <li>Original Medicare with a Medigap policy</li>
          <li>Original Medicare with a standalone drug plan</li>
          <li>Original Medicare and still working with employer coverage, if Part B is active</li>
          <li>Original Medicare, premium deducted from Social Security or paid quarterly by mail</li>
        </ul>
      </div>
      <div class="no"><b>Does not get it</b>
        <ul>
          <li>Any Medicare Advantage plan (HMO, PPO, Special Needs Plan), even though you pay Part B too</li>
          <li>Part B premium paid by Kentucky Medicaid or a Medicare Savings Program (QMB, SLMB, QI)</li>
          <li>Income above $109,000 single or $218,000 joint on your 2024 return (IRMAA)</li>
          <li>Living outside the United States</li>
        </ul>
      </div>
    </div>

    <h2>Why Medicare Advantage members are left out</h2>
    <p>This is the question we expect to be asked most, because Advantage members pay the same $202.90 Part B premium as everyone else. The answer is in the law that created the pot of money. Congress set up the <strong>Medicare Improvement Fund</strong> in 2008 and wrote that it may be used "to make improvements under the original Medicare fee-for-service program under Parts A and B." The administration is relying on that clause, and it is the reason the payment stops at the Original Medicare boundary. The lowest-income seniors are excluded because Medicaid already pays their premium, so a premium rebate would go to the state rather than to them. Higher-income seniors are excluded by policy choice.</p>
    <p>In Kentucky that boundary cuts deep. According to the CMS enrollment file for August 2026, <strong>562,671 of the state's 1,012,834 Medicare beneficiaries, 55.6 percent, are on an Advantage plan.</strong> In Fayette County it is 30,598 of 56,114. In Clark County it is 61.7 percent and in Anderson County 62.3 percent. If you live in Central Kentucky, the person next to you at church is more likely not to get the payment than to get it.</p>
    __VIZ_KY__
    <p class="vstamp">The 320,000 figure is our estimate, not a published count. Nationally, 20.8 million of roughly 29 million Original Medicare enrollees qualify, about 72 percent; we applied that share to Kentucky's 450,163. Kentucky's higher proportion of people on both Medicare and Medicaid (about 179,000 statewide, per KFF) may push the true number lower.</p>

    <h2>Where the money comes from, and why now</h2>
    <p>The Medicare Improvement Fund is an unusual pot. Congress created it in 2008 with about $2 billion, meant for improvements to the traditional Medicare program, and then spent the next seventeen years raising and lowering its balance on paper to offset other bills. The Congressional Budget Office reported in 2023 that not a dollar had ever actually been spent from it. The rebate will use roughly $1.9 billion of it, most of the balance, in one go.</p>
    <p>The administration's stated reason is affordability: the Part B premium rose from $185.00 to $202.90 this year, a 9.7 percent jump, the largest in several years, and the White House fact sheet frames the $90 as help with that bill. Critics, including the senior Democrat on the Senate Finance Committee, point to the timing, a month before the November 3 midterm elections, and the Associated Press described the payment as an election-season promise that leaves most beneficiaries out. KFF's analysts note a precedent: in September 2020 the same President announced $200 prescription drug cards for 33 million seniors, which were never sent and were abandoned in January 2021 over funding and legal problems. This time the money exists and the deposits are moving, which is the practical difference.</p>
    <p>One honest unknown. The 2008 statute's own example of an "improvement" is adjusting payments to doctors and hospitals, not sending checks to patients, and whether direct payments fit the law has been questioned but not tested. No lawsuit had been filed as of October 8. If one is filed later, it would affect future payments, not money already deposited.</p>

    <h2>What $90 does and does not do</h2>
    __VIZ_PREM__
    <p>Ninety dollars is real money, and for someone on a fixed income it is a couple of tanks of gas or most of a month's Medigap Plan N premium in Fayette County. It is also 44 percent of one month's Part B premium, and under four percent of a year's. It does not lower the premium going forward. The 2026 Medicare Trustees report projects the 2027 standard premium at $209.50, an increase of about $6.60 a month or $79 a year, and KFF's point is that the increase alone would consume the $90 within about fourteen months. Private forecasters expect the 2027 figure to come in higher, between $216 and $219. CMS announces the real number in November, and we will update this page when it does.</p>
    <p>Three practical details that are still unsettled, and we would rather say so than guess:</p>
    <ul>
      <li><strong>Taxes.</strong> Neither the IRS nor CMS had published guidance as of October 8. Commentators treat it as a rebate of a premium you paid, which matters only if you itemize medical expenses on your return; if you take the standard deduction there is nothing to do.</li>
      <li><strong>Other benefits.</strong> We found no guidance on whether the $90 counts as income for programs such as SNAP. The people most affected by that question, those on Medicaid, are excluded from the payment in the first place. If you report income to a program, ask that program.</li>
      <li><strong>Timing of eligibility.</strong> CMS has not said what date it used to decide who was on Original Medicare. Nothing in its guidance suggests a second payment for people who change coverage later, so there is no $90 to be gained by switching now.</li>
    </ul>

    <h2>What it means for the decision you are about to make</h2>
    <p>The Annual Enrollment Period opens October 15 and runs through December 7. Your Annual Notice of Change arrived last month. Those are the documents that decide what next year costs you. The $90 is not one of them.</p>
    <p>If you are on an Advantage plan and feel shortchanged, that is understandable, but switching to Original Medicare to "get the rebate" would be a mistake: the payment has already gone out, and the real question about Original Medicare is whether you can qualify for and afford a Medigap policy, which in Kentucky depends on your health unless you are in a guaranteed-issue window. Our guide to <a href="/articles/switching-medicare-advantage-to-medigap/">switching from Medicare Advantage to Medigap</a> walks through that. If you are on Original Medicare and received the $90, enjoy it, and still read the <a href="/articles/medicare-advantage-premium-deductible-copay-coinsurance-explained/">cost rows on your drug plan's notice</a> like any other year.</p>
    <p>For a plain look at where Part B and Part D costs are heading next year, including the $700 drug deductible and the $2,400 out-of-pocket cap, see <a href="/articles/medicare-changes-2027-kentucky/">what changes for Kentucky Medicare in 2027</a>.</p>

    <h2>The phone calls you are about to get</h2>
    <p>Every government payment with a dollar figure in the headline becomes a script for scammers within days, and this one has three features they love: a round number, a short window, and 40 million people who did not get it and are wondering why. Kentucky is already one of the heaviest Medicare robocall markets. Here is what to expect and how to handle it.</p>
    <div class="stage"><span class="num">1</span><span class="st"><b>"We need to verify your information to release your $90."</b>Nobody needs anything from you. The payment is automatic and has already been sent to the bank account or address Social Security has on file. Hang up.</span></div>
    <div class="stage"><span class="num">2</span><span class="st"><b>"You were missed. Give us your Medicare number and we will file for you."</b>There is no filing. If you believe you qualified and received nothing, call Social Security yourself at 1-800-772-1213 starting October 15, or 1-800-MEDICARE (1-800-633-4227) for eligibility questions. Use the numbers on your Medicare card, not a number someone gives you.</span></div>
    <div class="stage"><span class="num">3</span><span class="st"><b>"Switch to this plan and you'll get your $90 too."</b>No plan can get you the rebate, and a sales call that uses it as a hook is breaking Medicare's marketing rules. Our guide on <a href="/articles/stop-medicare-phone-calls-kentucky/">stopping Medicare sales calls in Kentucky</a> has the Attorney General's line and the no-call steps.</span></div>
    <div class="stage"><span class="num">4</span><span class="st"><b>A letter or email "from the President."</b>This one is real: CMS says a letter or email from the President will follow the payment in mid-October. The genuine one asks you for nothing. If a message with that heading asks you to click, call, confirm or pay, it is not the genuine one.</span></div>
    <div class="stage"><span class="num">5</span><span class="st"><b>A paper check.</b>Also real for people without direct deposit. It comes from the U.S. Department of the Treasury, later in October, with the memo "Medicare Improvement Fund Payment; $90 Payment to Offset October Premium." A check that asks you to call a number to "activate" it is not from the Treasury.</span></div>
    <p>Report anything suspicious to the Kentucky Senior Medicare Patrol (1-800-994-9422, or text 844-796-5678) or the Kentucky Attorney General's consumer line at 1-888-432-9257.</p>

    <div class="callout"><b>The one-sentence version to tell a neighbor.</b>It is a one-time $90 from a fund Congress set up in 2008, it goes only to people on Original Medicare who pay their own standard Part B premium, it arrives on its own with nothing to sign, and no caller, text or plan can get it for you.</div>

    <div class="note">
      <div class="who">
        <img src="/assets/austin-tyler.jpg" alt="Austin Tyler" width="600" height="750">
        <div><b>A note from Austin</b><span>Licensed Kentucky Medicare agent, Lexington</span></div>
      </div>
      <p>If you are one of my Advantage clients and you are wondering what you did wrong: nothing. The line was drawn by the 2008 law, not by anything on your account, and more than half of Kentucky is on the same side of it as you.</p>
      <p>If you are on Original Medicare and the $90 showed up, good. Please do not let it change how you read your drug plan's notice this month. The Part B premium will take it back by the end of next year, and the decisions that actually move your budget are the ones you make between October 15 and December 7.</p>
    </div>

    <h2 id="faq">Common questions from Kentucky</h2>
    <div class="faq">
      <h3>Who qualifies for the $90 Medicare payment?</h3>
      <p>People enrolled in Medicare Part B who are in Original Medicare rather than a Medicare Advantage plan, who pay their own Part B premium (not paid by Medicaid or a Medicare Savings Program), who pay the standard premium rather than an income-related surcharge, and who live in the United States. CMS estimates about 20.8 million people qualify nationally. Having a Medigap policy or a standalone drug plan does not affect eligibility.</p>
      <h3>Why didn't I get the $90 if I'm on a Medicare Advantage plan?</h3>
      <p>The money comes from the Medicare Improvement Fund, which the 2008 law restricts to improvements under the original fee-for-service Medicare program. The administration applied that limit, so Advantage enrollees are excluded even though they pay the same Part B premium. In Kentucky, 562,671 of 1,012,834 Medicare beneficiaries, about 56 percent, are on Advantage plans and do not receive the payment.</p>
      <h3>When does the $90 Medicare payment arrive and how?</h3>
      <p>Most eligible people receive a $90 direct deposit from the Social Security Administration on or around October 8, 2026. People without direct deposit receive a paper check from the U.S. Treasury later in October, mailed to the address Medicare has on file, with the memo "Medicare Improvement Fund Payment; $90 Payment to Offset October Premium." A letter or email from the President follows in mid-October. There is no application.</p>
      <h3>How do I check on my $90 Medicare payment?</h3>
      <p>Call the Social Security Administration at 1-800-772-1213 beginning October 15, 2026, for payment status. For questions about whether you qualify, call 1-800-MEDICARE (1-800-633-4227). Use those numbers directly; do not use a number from a call, text or email about the payment.</p>
      <h3>Is the $90 Medicare rebate a scam?</h3>
      <p>The payment itself is real and automatic. Any contact that asks you to verify information, pay a fee, share your Medicare or bank details, click a link or switch plans to receive it is a scam. Medicare and Social Security will not call, text or email asking for information to release the payment. Report suspicious contacts to the Kentucky Senior Medicare Patrol at 1-800-994-9422.</p>
      <h3>Does the $90 payment lower my Medicare premium next year?</h3>
      <p>No. It is a one-time payment and does not change the Part B premium, which is $202.90 a month in 2026. The 2026 Medicare Trustees report projects the 2027 premium at about $209.50, an increase of about $79 a year, which would use up the $90 in roughly fourteen months. CMS announces the actual 2027 premium in November.</p>
    </div>

    <div class="endcta">
      <h3>Questions about what this means for your plan?</h3>
      <p>Whether you got the $90 or not, the Annual Enrollment Period is the thing that matters this month. Bring your Annual Notice of Change and I will go through next year's numbers with you, no charge, and tell you plainly whether your plan still fits.</p>
      <div class="row">
        <a class="btn" href="/review/">Get a free plan review &rarr;</a>
        <p class="callline">Or call me directly: <a href="tel:18596186443">(859) 618-6443</a></p>
      </div>
    </div>

    <section class="recap">
      <h2>Quick recap</h2>
      <div class="recap-item">A one-time $90 Part B rebate, announced October 2 and deposited from October 8, going to about 20.8 million people nationally from the never-before-used Medicare Improvement Fund.</div>
      <div class="recap-item">Eligible: Original Medicare, paying your own standard Part B premium, living in the U.S. Medigap and standalone drug plans do not matter.</div>
      <div class="recap-item">Not eligible: Medicare Advantage members, people whose premium Medicaid pays, IRMAA payers, people abroad. In Kentucky that excludes the 56 percent on Advantage plans; roughly 320,000 Kentuckians receive it, by our estimate.</div>
      <div class="recap-item">Nothing to apply for. Direct deposit via Social Security, or a Treasury check later in October. Status line 1-800-772-1213 from October 15.</div>
      <div class="recap-item">$90 is 44 percent of one month's premium and under 4 percent of a year's. The projected 2027 increase of about $79 a year would absorb it; CMS announces the real figure in November.</div>
      <div class="recap-item">Taxes, benefit-program treatment and the legal basis are unsettled. We will update as guidance appears.</div>
      <div class="recap-item">Expect scam calls. No one can release, file for or get you the $90. Decide your 2027 coverage on your Annual Notice of Change, not on this payment.</div>
    </section>

    <section class="kcheck">
      <h2>Test what you learned</h2>
      <p class="kc-sub">Five quick questions. Pick an answer to see if you're right, and why.</p>
      <div id="kcheck"></div>
    </section>
    <script>window.KCHECK = __KCHECK__;</script>

    <div class="sources">
      <b>Sources</b>
      CMS, "Medicare Improvement Fund Premium Rebate Frequently Asked Questions" (eligibility, delivery, status line, check memo, presidential letter) and the White House fact sheet of October 2026, as reported by the Associated Press via PBS NewsHour and ABC News (October 7 to 8), CNN (October 3), NBC News, STAT, CNBC (October 5), CBS News, Kiplinger, The Hill and the Dallas Morning News &middot;
      KFF, "The Trump Administration's $90 Payment to Medicare Beneficiaries, Reminiscent of a Similar Proposal Six Years Ago, May Not Offset Rising Costs" (Juliette Cubanski), October 2026 &middot;
      CNBC, January 14, 2021, and Axios, October 2020, on the $200 drug discount cards &middot;
      Social Security Act section 1898 (Medicare Improvement Fund); Congressional Budget Office, 2023 &middot;
      CMS Medicare Advantage penetration file, August 2026, Kentucky extract (county and state counts) &middot;
      KFF state indicator, number of dual-eligible individuals, Kentucky, 2026 &middot;
      2026 Medicare Trustees report (2027 Part B projection $209.50).
      Checked October 8, 2026. The Kentucky recipient figure is our estimate and is labeled as such.
    </div>

    <p class="stamp"><b>Written and reviewed by Austin Tyler</b>, licensed Kentucky agent, NPN 20234188, Kentucky DOI license #1187780. Federal facts from the CMS FAQ and White House fact sheet via the outlets above; Kentucky counts from the CMS enrollment file, August 2026.</p>

    <p class="disclaim">This article is general information, not advice for your specific situation, and it describes a federal payment that Tyler Insurance Group has no role in administering. Eligibility and payment details are as published by CMS on the dates noted and may change. No specific plan is named or recommended. Tyler Insurance Group is not connected with or endorsed by the United States government or the federal Medicare program. We do not offer every plan available in your area. Currently we represent 6 organizations which offer 158 products in your area. Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance Program (SHIP) to get information on all of your options.</p>
"""
for k, v in [("__VIZ_ELIG__", VIZ_ELIG), ("__VIZ_KY__", VIZ_KY), ("__VIZ_PREM__", VIZ_PREM)]:
    assert BODY.count(k) == 1, k; BODY = BODY.replace(k, v)

KCHECK = [
 {"q": "You are on a Medicare Advantage HMO and pay the standard Part B premium. Do you get the $90?",
  "options": ["Yes, everyone on Part B gets it", "No, Advantage enrollees are excluded", "Only if you also have a drug plan", "Only if you call to request it"], "answer": 1,
  "why": "The fund that pays for the rebate is limited by the 2008 law to the original fee-for-service Medicare program, so Advantage enrollees are excluded even though they pay Part B too."},
 {"q": "You are on Original Medicare with a Plan G Medigap policy. Does the Medigap policy affect your eligibility?",
  "options": ["Yes, Medigap holders are excluded", "No, you are still in Original Medicare", "Only Plan N holders qualify", "Only if the Medigap premium is under $200"], "answer": 1,
  "why": "Medigap and standalone drug plans sit on top of Original Medicare and do not change eligibility. The exclusions are Advantage plans, Medicaid-paid premiums, IRMAA and living abroad."},
 {"q": "Someone calls saying they need your Medicare number to release your $90. What is the right move?",
  "options": ["Give it, since the payment is real", "Ask them to call back later", "Hang up; the payment is automatic and nobody needs anything from you", "Pay the small processing fee"], "answer": 2,
  "why": "There is no application, verification or fee. The money goes to the account or address Social Security already has. Check status yourself at 1-800-772-1213 from October 15."},
 {"q": "Does the $90 lower your Part B premium in 2027?",
  "options": ["Yes, by $90 a year", "Yes, by $7.50 a month", "No, it is a one-time payment", "Only for Medigap holders"], "answer": 2,
  "why": "It is a single payment. The 2027 premium is projected at about $209.50, up roughly $79 a year, which would use up the $90 in about fourteen months."},
 {"q": "Roughly what share of Kentuckians on Medicare are on an Advantage plan and therefore excluded?",
  "options": ["About one in ten", "About one in four", "A little over half", "Nearly all"], "answer": 2,
  "why": "The CMS enrollment file for August 2026 shows 562,671 of 1,012,834 Kentucky Medicare beneficiaries, 55.6 percent, on Advantage plans."},
]
body_html = BODY.replace("__KCHECK__", json.dumps(KCHECK, ensure_ascii=False))

out = re.sub(r'(<nav class="crumb" aria-label="Breadcrumb">).*?(</nav>)',
             r'\1<a href="/">Home</a> &rsaquo; <a href="/articles/">Learning Center</a> &rsaquo; <a href="/articles/on-medicare/">Already on Medicare</a> &rsaquo; '
             + CRUMB_LABEL + r'\2', out, count=1, flags=re.S)
out = re.sub(r'<span class="tag">.*?</span>', '<span class="tag">Already on Medicare · Costs &amp; Savings · Local Kentucky</span>', out, count=1, flags=re.S)
out = re.sub(r'<h1>.*?</h1>', f'<h1>{H1}</h1>', out, count=1, flags=re.S)
out = re.sub(r'(Local Kentucky Medicare agent · )[^<]*(</div>)', r'\1October 8, 2026 · 10 min read\2', out, count=1)
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
        node.update({"headline": H1, "description": DESC, "datePublished": "2026-10-08", "dateModified": "2026-10-08",
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

os.makedirs(DST_DIR, exist_ok=True)
open(f"{DST_DIR}/index.html", "w", encoding="utf-8").write(out)
print(f"wrote {DST_DIR}/index.html ({len(pairs)} FAQ, {len(KCHECK)} kcheck)")
