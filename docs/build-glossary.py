# Builds /glossary/ : plain-English Medicare terms with worked examples and
# a single shared visual language for the money terms.
import re, json, os
os.chdir('/home/user/bluegrass-medicare-help')
src = open('articles/index.html', encoding='utf-8').read()

def grab(pat):
    m = re.search(pat, src, re.S)
    assert m, 'NO MATCH: ' + pat
    return m.group(0)

USTRIP = grab(r'<div class="ustrip".*?</div>\s*</div>')
NAV    = grab(r'<nav class="nav".*?</nav>').replace(' class="active" aria-current="page"', '')
FNAV   = grab(r'<nav class="fnav".*?</nav>')
FOOT   = grab(r'<footer class="foot".*?</footer>')
PIX    = grab(r'<script>\s*!function\(f,b,e,v,n,t,s\).*?</noscript>')
GA     = grab(r'<script async src="https://www\.googletagmanager\.com.*?</script>\s*<script>\s*window\.dataLayer.*?</script>')
FONTS  = grab(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?rel="stylesheet">')
m = re.search(r'<script>[^<]*navtog.*?</script>', src, re.S)
NAVJS = m.group(0) if m else ''

YOU, PLAN, NOTYET, INK, MUTE = '#d05528', '#3a7d52', '#e2d9c8', '#2a2620', '#5f594f'

def bar(segs, caption):
    """One shared picture for every money term: a bar of who pays what.
    segs = [(label, pct, colour)]. Learn to read one, you can read them all."""
    W, H, Y = 480, 34, 30
    out = ['<svg class="gart" viewBox="0 0 480 104" role="img" aria-label="%s">' % caption]
    x = 0.0
    for label, pct, col in segs:
        w = W * pct / 100.0
        out.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="%s"%s/>'
                   % (x, Y, w, H, col, ' rx="6"' if (x == 0 or abs(x + w - W) < 0.5) else ''))
        if w > 52:
            out.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="14" font-weight="700" '
                       'fill="%s">%s</text>' % (x + w / 2, Y + 22, '#fff' if col != NOTYET else MUTE, label))
        x += w
    out.append('<rect x="0" y="%d" width="%d" height="%d" fill="none" stroke="#d8cfbd" rx="6"/>' % (Y, W, H))
    out.append('<text x="0" y="16" font-size="13.5" font-weight="700" fill="%s">%s</text>' % (MUTE, caption))
    # key
    out.append('<rect x="0" y="80" width="13" height="13" rx="3" fill="%s"/>' % YOU)
    out.append('<text x="19" y="91" font-size="13" fill="%s">you pay</text>' % MUTE)
    out.append('<rect x="86" y="80" width="13" height="13" rx="3" fill="%s"/>' % PLAN)
    out.append('<text x="105" y="91" font-size="13" fill="%s">the plan pays</text>' % MUTE)
    out.append('</svg>')
    return ''.join(out)

def tiers():
    rows = [('Tier 1  generic', '$', PLAN), ('Tier 2  preferred brand', '$$', '#5a9a70'),
            ('Tier 3  brand', '$$$', '#c98a5e'), ('Tier 4  specialty', '$$$$', YOU)]
    out = ['<svg class="gart" viewBox="0 0 480 150" role="img" aria-label="A drug list sorted into four price tiers">']
    out.append('<text x="0" y="14" font-size="13.5" font-weight="700" fill="%s">The same list, four price steps</text>' % MUTE)
    for i, (name, cost, col) in enumerate(rows):
        y = 26 + i * 30
        out.append('<rect x="0" y="%d" width="330" height="24" rx="5" fill="%s" opacity=".18"/>' % (y, col))
        out.append('<rect x="0" y="%d" width="6" height="24" rx="3" fill="%s"/>' % (y, col))
        out.append('<text x="16" y="%d" font-size="14" fill="%s">%s</text>' % (y + 17, INK, name))
        out.append('<text x="344" y="%d" font-size="15" font-weight="700" fill="%s">%s</text>' % (y + 17, col, cost))
    out.append('</svg>')
    return ''.join(out)

def network():
    o = ['<svg class="gart" viewBox="0 0 480 150" role="img" aria-label="Doctors inside the plan network cost less than doctors outside it">']
    o.append('<text x="0" y="14" font-size="13.5" font-weight="700" fill="%s">Inside the circle, or outside it</text>' % MUTE)
    o.append('<circle cx="150" cy="88" r="52" fill="%s" opacity=".13"/>' % PLAN)
    o.append('<circle cx="150" cy="88" r="52" fill="none" stroke="%s" stroke-width="2.5"/>' % PLAN)
    for cx, cy in [(126, 74), (172, 74), (150, 104)]:
        o.append('<circle cx="%d" cy="%d" r="12" fill="%s"/>' % (cx, cy, PLAN))
        o.append('<circle cx="%d" cy="%d" r="4.4" fill="#faf6ef"/>' % (cx, cy - 3))
        o.append('<path d="M%d %dc1.6-5 4.6-7.6 %d-7.6s6.4 2.6 8 7.6z" fill="#faf6ef"/>' % (cx - 8, cy + 9, 8))
    o.append('<text x="150" y="34" text-anchor="middle" font-size="13.5" font-weight="700" fill="%s">in network</text>' % PLAN)
    o.append('<text x="150" y="154" text-anchor="middle" font-size="13" fill="%s"></text>' % MUTE)
    o.append('<circle cx="330" cy="88" r="12" fill="%s"/>' % YOU)
    o.append('<circle cx="330" cy="85" r="4.4" fill="#faf6ef"/>')
    o.append('<path d="M322 97c1.6-5 4.6-7.6 8-7.6s6.4 2.6 8 7.6z" fill="#faf6ef"/>')
    o.append('<text x="330" y="34" text-anchor="middle" font-size="13.5" font-weight="700" fill="%s">out of network</text>' % YOU)
    o.append('<text x="330" y="122" text-anchor="middle" font-size="13" fill="%s">costs more,</text>' % MUTE)
    o.append('<text x="330" y="138" text-anchor="middle" font-size="13" fill="%s">or is not covered</text>' % MUTE)
    o.append('</svg>')
    return ''.join(o)

A = '/articles/'
# (term, also-known-as, definition, example, illustration, link, link text)
GROUPS = [
("What you pay", "pay", [
 ("Premium", "", "What you pay every month just to have the coverage, whether you use it or not.",
  "Most people pay $202.90 a month for Part B in 2026. If you draw Social Security it comes straight out of that check.",
  bar([('premium', 100, YOU)], 'A premium is due every month, used or not'), A+'medicare-costs-2026/', '2026 Medicare costs'),
 ("Deductible", "", "The amount you pay yourself first, before the plan starts paying its share.",
  "Part B has a $283 deductible in 2026. Your first doctor bills of the year come out of your pocket until you have paid $283. After that, the plan starts helping.",
  bar([('you pay first', 28, YOU), ('then the plan helps', 72, PLAN)], 'You pay up to the deductible, then coverage kicks in'), A+'medicare-costs-2026/', '2026 Medicare costs'),
 ("Copay", "copayment", "A flat dollar amount for a visit or a prescription. You know the number before you walk in.",
  "$20 every time you see your primary care doctor. Not 20 percent of the bill. Twenty dollars, whatever the bill turns out to be.",
  bar([('$20 you', 12, YOU), ('the rest is the plan', 88, PLAN)], 'A copay is a fixed amount, whatever the bill'), '', ''),
 ("Coinsurance", "", "A percentage of the bill instead of a flat amount. The bigger the bill gets, the bigger your share gets.",
  "Original Medicare pays 80 percent of a Part B bill and leaves you 20 percent. On a $100 bill that is $20. On a $100,000 cancer treatment it is $20,000. Same percentage, very different number.",
  bar([('you 20%', 20, YOU), ('Medicare 80%', 80, PLAN)], 'Coinsurance is a share of the bill, so it grows with the bill'), A+'medicare-advantage-vs-medigap/', 'Advantage vs. Medigap'),
 ("Out-of-pocket maximum", "MOOP, max out of pocket", "The most you can be made to pay in one year. Once you hit it, the plan pays everything covered for the rest of the year.",
  "This is the safety net, and Original Medicare on its own does not have one. Every Medicare Advantage plan does. It is the single biggest reason people add a Supplement or choose an Advantage plan.",
  bar([('you pay', 42, YOU), ('cap reached, plan pays it all', 58, PLAN)], 'A cap on your year, then the plan takes over'), A+'medicare-advantage-vs-medigap/', 'Advantage vs. Medigap'),
 ("Allowed amount", "Medicare-approved amount", "The price Medicare has decided a service is worth. Your share is worked out from this number, not from the sticker price on the bill.",
  "A clinic bills $300. Medicare says the service is worth $180. Your 20 percent is $36, not $60.", '', '', ''),
 ("Assignment", "accepts assignment", "A doctor who accepts assignment has agreed to take Medicare's price as full payment and not bill you extra.",
  "Almost all doctors accept assignment. It is worth asking once at a new office, because it is the difference between a predictable bill and a surprise one.", '', '', ''),
 ("Excess charges", "Part B excess charges", "The small number of doctors who have not agreed to Medicare's price can add up to 15 percent on top.",
  "A $180 service could come with an extra $27. Some Supplement plans cover this and some do not, which is one of the real differences between plan letters.", '', A+'medicare-supplement-plan-g-vs-plan-n/', 'Plan G vs. Plan N'),
 ("Benefit period", "", "How Part A counts a hospital stay. It starts the day you go in and ends once you have been out for 60 days in a row.",
  "The Part A hospital deductible is $1,736 per benefit period in 2026, not per year. Go in twice in one year with more than 60 days between, and you pay it twice.",
  bar([('stay', 22, YOU), ('60 days out resets it', 45, NOTYET), ('new stay, new deductible', 33, YOU)], 'Part A counts stays, not calendar years'), A+'medicare-costs-2026/', '2026 Medicare costs'),
]),
("The parts of Medicare", "parts", [
 ("Original Medicare", "", "Part A and Part B together, run by the federal government. This is what you get when you first sign up.",
  "It covers a lot, but it has no cap on what you can owe and no drug coverage. That gap is what everything else is built to fill.", '', A+'medicare-basics-parts-a-b-c-d/', 'Parts A, B, C and D'),
 ("Part A", "hospital insurance", "Anything inside the hospital. Inpatient stays, skilled nursing after a stay, hospice, some home health.",
  "For most people over 65 it costs nothing each month, because you already paid for it through payroll taxes while you worked.", '', A+'medicare-basics-parts-a-b-c-d/', 'Parts A, B, C and D'),
 ("Part B", "medical insurance", "Anything outside the hospital. Your primary care doctor, specialists, tests, scans, outpatient surgery.",
  "This is the part with the monthly premium, $202.90 for most people in 2026.", '', A+'medicare-basics-parts-a-b-c-d/', 'Parts A, B, C and D'),
 ("Part C", "Medicare Advantage", "A private plan that takes over running your Medicare, usually bundling drugs, dental, vision and hearing into one card.",
  "Think C for complete. One card everywhere. The trade is a network of doctors and, often, referrals and prior authorization.", '', A+'medicare-advantage-vs-medigap/', 'Advantage vs. Medigap'),
 ("Part D", "prescription drug plan, PDP", "Drug coverage. It is either bought on its own to sit alongside Original Medicare, or built into a Medicare Advantage plan.",
  "If you go the Supplement route, a separate Part D plan has to go with it. A Supplement does not cover drugs.", '', A+'medicare-part-d-prescription-drug-plans/', 'Part D drug plans'),
 ("Medigap", "Medicare Supplement", "A private policy that pays the share Original Medicare leaves you. No networks, and generally no referrals.",
  "You pay a premium every month whether you use it or not. In return you can see any doctor in the country who takes Medicare, and your share of the bill is largely handled.", '', A+'medicare-advantage-vs-medigap/', 'Advantage vs. Medigap'),
]),
("Doctors and hospitals", "doctors", [
 ("Network", "in network, out of network", "The list of doctors and hospitals a plan has agreed to pay for. Stay inside it and you pay the plan's normal share. Go outside and you pay more, or everything.",
  "This is the question to settle before you enroll, not after. Check your own doctors and your own hospital by name.",
  network(), A+'lexington-hospitals-medicare-advantage-networks/', 'Which Lexington hospitals take Advantage'),
 ("HMO", "", "A plan type that keeps you inside its network and usually asks you to pick a primary care doctor who refers you onward.",
  "Often the lowest premium. The right fit if your doctors are all in the network and you do not travel much.", '', '', ''),
 ("PPO", "", "A plan type that still has a network but will pay something toward doctors outside it.",
  "Usually costs more than an HMO. Worth it if you split time between states or want fewer rules about who you see.", '', '', ''),
 ("Referral", "", "Permission from your primary care doctor before the plan will pay for a specialist.",
  "Original Medicare and Supplements generally do not need one. Many Advantage plans do, though some carriers are dropping the requirement.", '', '', ''),
 ("Prior authorization", "pre-auth", "The plan has to approve a test, procedure or drug before it will pay. Your doctor sends the request and you wait.",
  "This is one of the real day-to-day differences between plan types. It is worth asking how often a plan uses it before you enroll.", '', '', ''),
 ("Star rating", "", "A one to five score CMS gives each Advantage and Part D plan for things like customer service and how well members are cared for.",
  "Useful as a tiebreaker, not as a reason to pick. A four-star plan your doctor is not in is still the wrong plan.", '', '', ''),
]),
("Prescriptions", "drugs", [
 ("Formulary", "drug list", "The list of drugs one plan covers. Every plan has its own, and they change every January.",
  "Two plans with the same premium can price your exact medication very differently. This is why the drug list matters more than the premium.",
  tiers(), A+'medicare-part-d-prescription-drug-plans/', 'Part D drug plans'),
 ("Tier", "", "The price step a plan puts each drug on. Lower tiers are the cheap generics, higher tiers are brand and specialty drugs.",
  "The same pill can sit on tier 2 with one plan and tier 4 with another. That is a real difference in what you pay.", '', '', ''),
 ("Step therapy", "", "The plan wants you to try a cheaper drug first, and only covers the one your doctor asked for if the cheaper one does not work.", "", '', '', ''),
 ("Quantity limit", "", "A cap on how much of a drug the plan will cover at one time, like 30 pills a month.", "", '', '', ''),
 ("Out-of-pocket drug cap", "catastrophic coverage", "Once your own spending on covered drugs hits $2,100 in 2026, you pay nothing more for them for the rest of the year.",
  "This is new and it is a big deal. Before 2025 there was no ceiling at all on what a Part D year could cost you.",
  bar([('you pay up to $2,100', 46, YOU), ('then $0 for the rest of the year', 54, PLAN)], 'Part D now has a ceiling'), A+'medicare-part-d-prescription-drug-plans/', 'Part D drug plans'),
 ("Donut hole", "doughnut hole, coverage gap", "Gone. It was eliminated in 2025 and replaced by the $2,100 out-of-pocket cap. If someone is still explaining the donut hole to you, their information is out of date.",
  "People still search for this, which is exactly why it is worth saying plainly: there is no longer a gap phase where your costs jump.", '', A+'common-medicare-misconceptions/', 'Common Medicare myths'),
 ("Creditable coverage", "", "Drug coverage at least as good as Part D. Having it means you can delay Part D without a penalty later.",
  "Employer plans usually count, and they send you a letter each year saying so. Keep that letter.", '', A+'working-past-65-medicare/', 'Working past 65'),
 ("Medicare Prescription Payment Plan", "M3P", "An option to spread your drug costs over the year in monthly instalments instead of paying a large amount at the pharmacy at once.",
  "It does not lower the total. It smooths it out, which helps if one expensive month would be the problem.", '', '', ''),
]),
("Timing and enrollment", "timing", [
 ("Initial Enrollment Period", "IEP", "Your seven-month window around your 65th birthday: three months before, your birthday month, and three months after.",
  "Sign up in the first three months and coverage starts the first day of your birthday month. Wait until after and it starts later.",
  bar([('3 months before', 43, PLAN), ('birth month', 14, YOU), ('3 months after', 43, NOTYET)], 'Seven months, and the early part is the good part'), A+'turning-65-enrollment-window/', 'The 7-month window'),
 ("Annual Enrollment Period", "AEP, open enrollment", "October 15 to December 7 every year. Anyone can change their Advantage or Part D plan, and the change starts January 1.",
  "This is the one window everybody gets. It is also when plans publish their changes for the coming year, so it is the time to check the drug list again.", '', A+'medicare-annual-enrollment-period/', 'The Annual Enrollment Period'),
 ("Medicare Advantage Open Enrollment", "MA OEP", "January 1 to March 31, for people already in an Advantage plan. One change allowed.",
  "This is the safety valve if January arrives and the plan you picked is not working out.", '', A+'medicare-enrollment-periods-explained/', 'Enrollment periods explained'),
 ("Special Enrollment Period", "SEP", "A window that opens because something happened: you moved, you lost employer coverage, your plan left the county.",
  "These are the exceptions that let you act outside the normal calendar. If something changed, ask, because you may have a window you do not know about.", '', A+'medicare-advantage-plan-ending-kentucky/', 'If your plan is ending'),
 ("General Enrollment Period", "GEP", "January 1 to March 31, for people who missed their first window entirely.",
  "It works, but a late enrollment penalty usually comes with it.", '', '', ''),
 ("Medigap open enrollment", "", "The six months starting when your Part B begins. During it, no Supplement can turn you down or charge you more for your health.",
  "This is the most valuable six months in Medicare and most people do not know it is running.", '', A+'kentucky-medigap-birthday-rule/', 'The Kentucky birthday rule'),
 ("Medical underwriting", "", "Health questions. An insurer reviewing your history and deciding whether to accept you, and at what price.",
  "This is the catch nobody mentions when you first choose. Leaving an Advantage plan for a Supplement later can mean answering these questions, and the answer can be no.", '', A+'switching-medicare-advantage-to-medigap/', 'Switching back to a Supplement'),
 ("Guaranteed issue", "GI rights", "Situations where a Supplement has to accept you, no health questions asked.",
  "Your first six months on Part B is the big one. Kentucky also gives you a window around your birthday each year.", '', A+'kentucky-medigap-birthday-rule/', 'The Kentucky birthday rule'),
 ("Late enrollment penalty", "", "A permanent addition to your premium for signing up late without other coverage. It does not go away.",
  "The Part B penalty is 10 percent for every full year you could have had it and did not, and you pay it for as long as you have Medicare.", '', A+'turning-65-enrollment-window/', 'The 7-month window'),
]),
("Help paying for it", "help", [
 ("Extra Help", "Low Income Subsidy, LIS", "A federal program that pays most of your Part D costs if your income and savings are modest.",
  "Applying is free and takes about twenty minutes at ssa.gov. A lot of people who qualify never apply.", '', A+'help-paying-for-medicare/', 'Help paying for Medicare'),
 ("Medicare Savings Program", "MSP", "A state program that can pay your Part B premium for you.",
  "In Kentucky this is worth over $200 a month back in your pocket in 2026. You apply through kynect.", '', A+'help-paying-for-medicare/', 'Help paying for Medicare'),
 ("QMB", "Qualified Medicare Beneficiary", "The most generous level of Medicare Savings Program. It pays your premiums and protects you from most cost sharing.",
  "If you have QMB, providers are not allowed to bill you for Medicare deductibles and coinsurance.", '', A+'help-paying-for-medicare/', 'Help paying for Medicare'),
 ("Dual eligible", "", "Someone who has both Medicare and Medicaid.",
  "There are special plans built only for people in this situation, and they usually cover far more.", '', '', ''),
 ("IRMAA", "income-related monthly adjustment amount", "An extra charge on Part B and Part D if your income is above the threshold. It is based on your tax return from two years ago.",
  "Two years ago matters. If you have retired since then and your income dropped, you can ask Social Security to use the newer figure.", '', A+'medicare-irmaa-high-income-surcharge/', 'The IRMAA surcharge'),
]),
("Mail you will get", "mail", [
 ("Annual Notice of Change", "ANOC", "The letter every Advantage and Part D plan sends each September saying exactly what is changing in January.",
  "It is the most ignored important letter in Medicare. The changes to look for are the drug list and your doctors.", '', A+'annual-medicare-review-aep/', 'Your annual review'),
 ("Evidence of Coverage", "EOC", "The long booklet with the full rules of your plan. The ANOC is the summary of what changed; this is the detail.", "", '', '', ''),
 ("Explanation of Benefits", "EOB", "Not a bill. A summary from your plan of what was billed, what it paid, and what you may owe.",
  "The words 'this is not a bill' are usually printed on it, and people still panic. Read the bottom line, then wait for the actual bill.", '', '', ''),
 ("Medicare Summary Notice", "MSN", "The Original Medicare version of an Explanation of Benefits, sent every three months.", "", '', '', ''),
 ("Denial and appeal", "", "A plan refusing to pay, and your right to challenge it. There are several levels and deadlines at each one.",
  "A lot of denials are paperwork problems, not real refusals. Do not assume the first no is final.", '', '', ''),
 ("Non-renewal", "plan termination", "Your plan telling you it will not be offered in your county next year. The letter arrives in early October.",
  "It is not a cancellation of your Medicare. It does open a special window, and doing nothing usually means being moved somewhere you did not choose.", '', A+'medicare-advantage-plan-ending-kentucky/', 'If your plan is ending'),
]),
]

def slug(t):
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')

rows, defined, count = [], [], 0
for gname, gid, terms in GROUPS:
    rows.append('      <h2 class="ghead" id="g-%s">%s</h2>' % (gid, gname))
    rows.append('      <div class="glist">')
    for term, aka, dfn, ex, art, link, linktext in terms:
        count += 1
        search = re.sub(r'[^a-z0-9]+', ' ', (term + ' ' + aka + ' ' + dfn + ' ' + ex).lower()).strip()
        rows.append('        <article class="gterm" id="t-%s" data-s="%s">' % (slug(term), search))
        rows.append('          <h3>%s%s</h3>' % (term, ('<span class="gaka">also called %s</span>' % aka) if aka else ''))
        rows.append('          <p class="gdef">%s</p>' % dfn)
        if ex:
            rows.append('          <p class="gex"><b>For example:</b> %s</p>' % ex)
        if art:
            rows.append('          %s' % art)
        if link:
            rows.append('          <p class="gmore"><a href="%s">%s<span aria-hidden="true"> &rarr;</span></a></p>' % (link, linktext))
        rows.append('        </article>')
        defined.append({"@type": "DefinedTerm", "name": term,
                        "description": dfn + ((' For example: ' + ex) if ex else ''),
                        "inDefinedTermSet": "https://www.bluegrassmedicarehelp.com/glossary/",
                        "termCode": slug(term),
                        "url": "https://www.bluegrassmedicarehelp.com/glossary/#t-" + slug(term)})
    rows.append('      </div>')

chips = ''.join('<a class="gchip" href="#g-%s">%s</a>' % (g[1], g[0]) for g in GROUPS)

graph = {"@context": "https://schema.org", "@graph": [
  {"@type": ["CollectionPage", "DefinedTermSet"], "@id": "https://www.bluegrassmedicarehelp.com/glossary/",
   "url": "https://www.bluegrassmedicarehelp.com/glossary/",
   "name": "Medicare Terms in Plain English",
   "description": "Every Medicare and health insurance word you are likely to meet, explained without jargon, with a worked example for each.",
   "isPartOf": {"@type": "WebSite", "@id": "https://www.bluegrassmedicarehelp.com/#website",
                "name": "Bluegrass Medicare Help", "url": "https://www.bluegrassmedicarehelp.com/"},
   "inLanguage": "en-US", "hasDefinedTerm": defined},
  {"@type": "BreadcrumbList", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.bluegrassmedicarehelp.com/"},
   {"@type": "ListItem", "position": 2, "name": "Learning Center", "item": "https://www.bluegrassmedicarehelp.com/articles/"},
   {"@type": "ListItem", "position": 3, "name": "Glossary", "item": "https://www.bluegrassmedicarehelp.com/glossary/"}]}]}

HERO = '''<svg class="heroart" viewBox="0 0 480 280" role="img" aria-label="Illustration of a confusing insurance letter being turned into plain language">
        <ellipse cx="240" cy="256" rx="170" ry="13" fill="#e2d9c8" opacity=".7"/>
        <rect x="52" y="40" width="164" height="200" rx="9" fill="#fff" stroke="#e2d9c8" stroke-width="2" transform="rotate(-5 134 140)"/>
        <g transform="rotate(-5 134 140)" fill="#e2d9c8">
          <rect x="72" y="66" width="112" height="9" rx="4.5"/><rect x="72" y="88" width="124" height="7" rx="3.5"/>
          <rect x="72" y="104" width="104" height="7" rx="3.5"/><rect x="72" y="132" width="118" height="7" rx="3.5"/>
          <rect x="72" y="148" width="88" height="7" rx="3.5"/><rect x="72" y="176" width="120" height="7" rx="3.5"/>
          <rect x="72" y="192" width="76" height="7" rx="3.5"/>
        </g>
        <text x="132" y="128" font-size="15" font-weight="800" fill="#d05528" transform="rotate(-5 134 140)">COINSURANCE</text>
        <text x="128" y="176" font-size="15" font-weight="800" fill="#d05528" transform="rotate(-5 134 140)">FORMULARY</text>
        <path d="M232 140h34" stroke="#5f594f" stroke-width="3" stroke-linecap="round"/>
        <path d="M258 132l10 8-10 8" fill="none" stroke="#5f594f" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        <rect x="284" y="52" width="150" height="176" rx="9" fill="#faf6ef" stroke="#3a7d52" stroke-width="2.5"/>
        <circle cx="359" cy="96" r="24" fill="#3a7d52"/>
        <path d="M348 96l7 8 14-15" fill="none" stroke="#faf6ef" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
        <rect x="304" y="140" width="110" height="9" rx="4.5" fill="#2a2620"/>
        <rect x="304" y="162" width="94" height="7" rx="3.5" fill="#e2d9c8"/>
        <rect x="304" y="178" width="102" height="7" rx="3.5" fill="#e2d9c8"/>
        <rect x="304" y="200" width="62" height="9" rx="4.5" fill="#d05528"/>
        <rect x="366" y="200" width="48" height="9" rx="4.5" fill="#3a7d52"/>
      </svg>'''

CSS = '''<style>
*{margin:0;padding:0;box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;}
body{font-family:var(--sans);color:var(--ink);background:var(--cream);line-height:1.65;-webkit-font-smoothing:antialiased;}
img{max-width:100%;display:block;}
a{color:var(--coral-d);text-decoration:none;}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px;}
.foot{background:var(--dark);color:#9a948c;padding:30px 0 36px;font-size:13px;line-height:1.7;margin-top:48px;}
.foot .fnm{color:var(--cream);font-weight:600;font-size:15px;margin-bottom:6px;font-family:var(--serif);}
.foot a{color:#bdb6ac;}
.foot .disc{margin-top:14px;padding-top:14px;border-top:1px solid #333;color:#918b80;font-size:12px;}
.crumb{padding:18px 0 0;font-size:15px;}
.ghero{background:var(--cream2);border-bottom:1px solid var(--line);padding:38px 0;margin-top:16px;}
.ghero .wrap{display:grid;grid-template-columns:1.15fr .85fr;gap:34px;align-items:center;}
.ghero h1{font-family:var(--serif);font-weight:500;font-size:44px;line-height:1.09;letter-spacing:-1px;margin-bottom:14px;}
.ghero p{font-size:19px;color:var(--mute);max-width:540px;}
.heroart{width:100%;height:auto;}
/* search */
.gsearch{position:sticky;top:var(--navh,66px);z-index:20;background:var(--cream);border-bottom:1px solid var(--line);padding:16px 0;}
.gsearch .wrap{display:flex;flex-direction:column;gap:12px;}
.gfield{position:relative;}
.gfield svg{position:absolute;left:16px;top:50%;transform:translateY(-50%);width:21px;height:21px;stroke:var(--faint);fill:none;stroke-width:2.2;}
#gq{width:100%;font-family:var(--sans);font-size:19px;padding:16px 18px 16px 48px;border:2px solid var(--line);
  border-radius:12px;background:#fff;color:var(--ink);}
#gq:focus{outline:none;border-color:var(--coral);}
.gchips{display:flex;flex-wrap:wrap;gap:9px;}
.gchip{font-size:15px;font-weight:600;padding:7px 15px;border-radius:999px;background:var(--warm);color:var(--ink);border:1px solid var(--line);}
.gchip:hover{background:var(--coral);color:#fff;border-color:var(--coral);}
.gcount{font-size:15px;color:var(--faint);}
/* terms */
.gbody{padding:34px 0 10px;}
.ghead{font-family:var(--serif);font-weight:600;font-size:29px;margin:34px 0 18px;padding-top:8px;color:var(--ink);}
.ghead:first-child{margin-top:0;}
.glist{display:grid;grid-template-columns:repeat(2,1fr);gap:22px;align-items:start;}
.gterm{background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px 24px;}
.gterm:target{border-color:var(--coral);box-shadow:0 0 0 3px rgba(208,85,40,.16);}
.gterm h3{font-family:var(--serif);font-weight:600;font-size:22px;color:var(--ink);line-height:1.25;}
.gaka{display:block;font-family:var(--sans);font-size:14.5px;font-weight:400;color:var(--faint);margin-top:2px;}
.gdef{font-size:17px;margin-top:9px;}
.gex{font-size:16px;color:var(--mute);margin-top:11px;padding:12px 14px;background:var(--cream2);border-left:3px solid var(--coral);border-radius:0 8px 8px 0;}
.gex b{color:var(--ink);}
.gart{width:100%;height:auto;margin-top:15px;display:block;}
.gmore{margin-top:13px;font-size:16px;font-weight:700;}
.gnone{display:none;text-align:center;padding:44px 20px;background:#fff;border:1px solid var(--line);border-radius:14px;}
.gnone b{display:block;font-family:var(--serif);font-size:22px;margin-bottom:8px;}
.gnone p{color:var(--mute);font-size:17px;}
/* closing */
.gcta{margin:46px 0 0;background:var(--warm);border:1px solid var(--line);border-radius:18px;padding:34px 30px;text-align:center;}
.gcta h2{font-family:var(--serif);font-weight:600;font-size:29px;margin-bottom:10px;}
.gcta p{font-size:17.5px;color:var(--mute);max-width:640px;margin:0 auto 20px;}
.gbtns{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;}
.gbtn{display:inline-flex;align-items:center;gap:9px;background:var(--coral);color:#fff;font-weight:700;font-size:17px;padding:15px 26px;border-radius:11px;}
.gbtn:hover{background:var(--coral-d);}
.gbtn.alt{background:var(--green);}
.gnote{font-size:14px;color:var(--faint);text-align:center;margin:26px 0 0;font-style:italic;}
@media(max-width:860px){
  .ghero .wrap{grid-template-columns:1fr;gap:20px;} .ghero h1{font-size:33px;}
  .heroart{max-width:400px;margin:0 auto;}
  .glist{grid-template-columns:1fr;}
}
</style>'''

JS = '''<script>
/* keep the search bar parked directly under the sticky header at any size */
(function(){
  var nav=document.querySelector('.nav');
  if(!nav) return;
  function set(){ document.documentElement.style.setProperty('--navh', Math.round(nav.getBoundingClientRect().height)+'px'); }
  set();
  window.addEventListener('resize', set);
  if(window.ResizeObserver) new ResizeObserver(set).observe(nav);
})();
/* filter as you type: people arrive holding a letter with one word on it */
(function(){
  var q=document.getElementById('gq'), terms=[].slice.call(document.querySelectorAll('.gterm')),
      heads=[].slice.call(document.querySelectorAll('.ghead')),
      lists=[].slice.call(document.querySelectorAll('.glist')),
      none=document.getElementById('gnone'), count=document.getElementById('gcount'),
      total=terms.length, t=null;
  function run(){
    var raw=q.value.trim(),
        words=raw.toLowerCase().replace(/[^a-z0-9]+/g,' ').trim().split(' ').filter(Boolean),
        shown=0;
    terms.forEach(function(el){
      var hay=el.getAttribute('data-s');
      var hit = !words.length || words.every(function(w){ return hay.indexOf(w) > -1; });
      el.hidden = !hit; if(hit) shown++;
    });
    lists.forEach(function(l,i){
      var any=[].slice.call(l.querySelectorAll('.gterm')).some(function(e){return !e.hidden;});
      l.hidden=!any; if(heads[i]) heads[i].hidden=!any;
    });
    none.style.display = shown ? 'none' : 'block';
    count.textContent = words.length
      ? (shown + (shown===1?' term':' terms') + ' matching "' + raw + '"')
      : (total + ' terms, in plain English');
  }
  q.addEventListener('input', function(){ clearTimeout(t); t=setTimeout(run, 90); });
  q.addEventListener('search', run);
  run();
})();
</script>'''

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="icon" type="image/png" href="/assets/logo-mark.png">
<link rel="apple-touch-icon" href="/assets/logo-mark.png">
<meta name="theme-color" content="#1f1d1a">
''' + PIX + '\n' + GA + '''
<title>Medicare Terms in Plain English: A Glossary With Real Examples | Bluegrass Medicare Help</title>
<meta name="description" content="Every Medicare word you are likely to meet, explained without jargon. Deductible, coinsurance, formulary, prior authorization and more, each with a plain example and a simple picture of who pays what.">
''' + FONTS + '''
<link rel="stylesheet" href="/assets/site.css">
<link rel="canonical" href="https://www.bluegrassmedicarehelp.com/glossary/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bluegrass Medicare Help">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="Medicare Terms in Plain English: A Glossary With Real Examples">
<meta property="og:description" content="Deductible, coinsurance, formulary, prior authorization and more, each with a plain example and a simple picture of who pays what.">
<meta property="og:url" content="https://www.bluegrassmedicarehelp.com/glossary/">
<meta property="og:image" content="https://www.bluegrassmedicarehelp.com/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Medicare Terms in Plain English">
<meta name="twitter:description" content="Every Medicare word you are likely to meet, explained without jargon, with a real example for each.">
<meta name="twitter:image" content="https://www.bluegrassmedicarehelp.com/assets/og-image.png">
<script type="application/ld+json">''' + json.dumps(graph, ensure_ascii=False) + '''</script>
''' + CSS + '''
</head>
<body>
''' + USTRIP + '\n' + NAV + '''

<main id="main">
  <div class="wrap"><p class="crumb"><a href="/articles/">&larr; Learning Center</a></p></div>

  <section class="ghero">
    <div class="wrap">
      <div>
        <h1>Medicare, without the jargon.</h1>
        <p>Most people are not confused about Medicare. They are confused about the words. Here is every term you are likely to run into, in plain English, with a real example and a simple picture of who pays what.</p>
      </div>
      ''' + HERO + '''
    </div>
  </section>

  <section class="gsearch">
    <div class="wrap">
      <div class="gfield">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4.3-4.3" stroke-linecap="round"/></svg>
        <label for="gq" class="sr-only" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);">Search Medicare terms</label>
        <input id="gq" type="search" placeholder="Type a word from your letter, like coinsurance" autocomplete="off">
      </div>
      <div class="gchips">''' + chips + '''</div>
      <p class="gcount" id="gcount" role="status" aria-live="polite"></p>
    </div>
  </section>

  <section class="gbody">
    <div class="wrap">
''' + '\n'.join(rows) + '''
      <div class="gnone" id="gnone">
        <b>No match for that one.</b>
        <p>Try a shorter word, or just call and read us the sentence. We will tell you what it means, free, at <a href="tel:18596186443">(859) 618-6443</a>.</p>
      </div>

      <section class="gcta">
        <h2>Still holding a letter that makes no sense?</h2>
        <p>Read it to us over the phone. No cost, no obligation, and no assumption that you should already know this.</p>
        <div class="gbtns">
          <a class="gbtn" href="/schedule/">Book a free 30-minute review</a>
          <a class="gbtn alt" href="tel:18596186443">Call (859) 618-6443</a>
        </div>
      </section>

      <p class="gnote">Dollar figures are the 2026 amounts, verified against CMS. Definitions are general Medicare education, not advice about any one plan.</p>
    </div>
  </section>
</main>

''' + FNAV + '\n' + FOOT + '\n' + JS + '\n' + NAVJS + '''
</body>
</html>
'''
os.makedirs('glossary', exist_ok=True)
open('glossary/index.html', 'w', encoding='utf-8').write(html)
print('glossary written: %d terms, %d bytes' % (count, len(html)))
