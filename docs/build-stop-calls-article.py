#!/usr/bin/env python3
"""Build /articles/stop-medicare-phone-calls-kentucky/ by cloning chrome from an
existing article and swapping in new head, schema, body and knowledge check."""
import json, re, os

SRC = "articles/does-baptist-health-take-medicare-advantage/index.html"
DST_DIR = "articles/stop-medicare-phone-calls-kentucky"
URL = "https://www.bluegrassmedicarehelp.com/articles/stop-medicare-phone-calls-kentucky/"

TITLE = "How to Stop Medicare Phone Calls in Kentucky"
H1 = "How to Stop the Medicare Phone Calls: A Kentucky Guide"
DESC = ("Why the Medicare calls got worse in 2026, how to get off the lists, and the Kentucky "
        "enforcement almost nobody uses. From a Lexington agent.")
CRUMB_LABEL = "Stopping Medicare Calls"

src = open(SRC, encoding="utf-8").read()

# ---------------------------------------------------------------- head swaps
out = src
swaps = [
 ("<title>Does Baptist Health Take Medicare Advantage? (2026)</title>", f"<title>{TITLE}</title>"),
 ('<meta property="og:title" content="Does Baptist Health Take Medicare Advantage? (2026)">',
  f'<meta property="og:title" content="{TITLE}">'),
 ('<meta name="twitter:title" content="Does Baptist Health Take Medicare Advantage? (2026)">',
  f'<meta name="twitter:title" content="{TITLE}">'),
]
for a, b in swaps:
    assert out.count(a) == 1, a[:60]
    out = out.replace(a, b)

OLD_DESC = ("Which Medicare Advantage plans are in-network at Baptist Health, UK HealthCare and CHI "
            "Saint Joseph in Lexington, carrier by carrier, verified 2026.")
assert out.count(OLD_DESC) == 3
out = out.replace(OLD_DESC, DESC)

OLD_CANON = "https://www.bluegrassmedicarehelp.com/articles/does-baptist-health-take-medicare-advantage/"
out = out.replace(f'<link rel="canonical" href="{OLD_CANON}">', f'<link rel="canonical" href="{URL}">')
out = out.replace(f'<meta property="og:url" content="{OLD_CANON}">', f'<meta property="og:url" content="{URL}">')

# ---------------------------------------------------------------- extra styles
NEWCSS = """
.note{background:var(--cream2);border:1px solid var(--line);border-radius:14px;padding:24px 24px 20px;margin:30px 0 26px;}
.note .who{display:flex;align-items:center;gap:14px;margin-bottom:14px;}
.note .who img{width:56px;height:56px;border-radius:50%;object-fit:cover;object-position:center top;border:2px solid var(--coral);}
.note .who b{display:block;font-size:16.5px;color:var(--ink);}
.note .who span{font-size:14.5px;color:var(--faint);}
.note p{font-size:17.5px;color:#3b352c;margin-bottom:14px;}
.note p:last-child{margin-bottom:0;}
.help{background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin:0 0 18px;}
.help h3{margin-top:0;font-size:19px;}
.help p{font-size:16.5px;margin-bottom:10px;}
.help .ph{font-weight:700;color:var(--ink);font-size:17.5px;}
.stamp{font-size:14.5px;color:var(--faint);margin:26px 0 0;}
.stamp b{color:var(--mute);font-weight:600;}
"""
out = out.replace("</style>", NEWCSS + "</style>")

# ---------------------------------------------------------------- body
BODY = """
    <p>The number one complaint I hear in this job is not about premiums, or networks, or paperwork. It is this: <strong>"Why will these people not stop calling me?"</strong></p>
    <p>I hear it at kitchen tables all over central Kentucky, usually from someone who has already tried to make it stop. And this year there is a specific reason it feels worse, which is not that you did anything wrong.</p>

    <div class="ans">
      <p><strong>Several federal Medicare marketing rules loosened on October 1, 2026.</strong> Waiting periods that used to slow a sales conversation down are gone, and marketers can now use words like "best" if they can back the claim up.</p>
      <p>What did <em>not</em> change: <strong>nobody may cold-call you about a Medicare Advantage or Part D plan</strong> unless you gave permission. And Kentucky has its own enforcement, separate from the federal registry, that most people here have never used. That is the part worth reading.</p>
    </div>

    <h2>Why the calls got worse this year</h2>
    <p>CMS rewrote several Medicare marketing rules for the 2027 plan year, and the changes took effect <strong>October 1, 2026</strong>. Most of them loosened:</p>
    <ul>
      <li><strong>The 48-hour waiting period is gone.</strong> An agent used to have to wait two days after you signed a Scope of Appointment before talking to you about specific plans. That conversation can now happen the same day.</li>
      <li><strong>The gap between educational and sales events is gone.</strong> A 12-hour separation used to be required between a seminar and a sales meeting at the same location.</li>
      <li><strong>Agents can collect a Scope of Appointment at an educational event</strong>, so you can be signed up for a sales appointment at the seminar itself.</li>
      <li><strong>The disclaimer moved.</strong> The third-party marketing disclaimer must now come before any discussion of benefits, rather than in the first 60 seconds of the call.</li>
      <li><strong>Superlatives are allowed</strong> where the claim can be substantiated, so expect more "best" and "top-rated" language in the ads than last year.</li>
    </ul>
    <p>None of that makes an agent dishonest. What it means is that the built-in pauses between meeting someone and enrolling with them are mostly gone. The pause is yours to take now, and you should take it.</p>

    <h2>Why they have your name</h2>
    <p>Here is the thing that surprises people most: <strong>most of those calls are not from insurance agents at all.</strong> They come from lead generators, companies whose actual product is your contact information. They sell it to several agencies at once, which is exactly why answering one call produces six more.</p>
    <p>The usual sources are a "free Medicare guide" form you filled in online, a reply card from a mailer, a sweepstakes entry, or a data broker who sold a list that includes your birth year. If something asked for your phone number in exchange for Medicare information, it was a lead form, whatever it was called.</p>

    <h2>What is still against the rules</h2>
    <p>This list did not loosen on October 1, and it is the practical test for whether a call is legitimate:</p>
    <ul>
      <li><strong>No cold calls</strong> about Medicare Advantage or Part D without your permission. If you did not ask to be contacted, the call is not compliant.</li>
      <li><strong>No door-to-door visits</strong> you did not agree to in advance.</li>
      <li><strong>No high-pressure tactics.</strong> That prohibition survived the rule changes intact.</li>
      <li><strong>No enrolling you without your explicit consent.</strong></li>
      <li><strong>Medicare will not call you</strong> to ask for your Medicare number, your Social Security number, or your bank details. Neither will a real agent, out of the blue.</li>
    </ul>
    <div class="callout"><b>The one rule that covers most of it.</b>If you did not start the contact, do not give out your Medicare number. Hang up, look the company up yourself, and call back on the number you found. Any agent worth working with will be completely fine with that.</div>

    <h2>Kentucky's part, and it is the piece most people miss</h2>
    <p>Almost everyone I talk to has registered on the national Do Not Call list, been called anyway, and concluded that registering was pointless. It was not pointless. It just is not the whole tool, and in Kentucky the second half is unusually strong.</p>

    <h3>The list itself is federal now</h3>
    <p>Kentucky used to run its own separate No Call list. In 2007 the General Assembly folded it into the <strong>National Do Not Call Registry</strong>, and every number that had been on the Kentucky list was transferred over automatically. So if you registered years ago through the state, you are still on it, and you do not need to register again. New registrations go through the federal registry at <strong>donotcall.gov</strong> or <strong>1-888-382-1222</strong>, and it is free.</p>

    <h3>The enforcement is still Kentucky's, and it has teeth</h3>
    <p>This is the part that gets missed. Merging the list did not hand enforcement to Washington. <strong>The Kentucky Attorney General can prosecute a telemarketer who calls a registered Kentucky number, with fines of up to $5,000 per violation.</strong></p>
    <p>That is per call. It is one of the more aggressive state penalties in the country, and it only gets used when somebody files a complaint. Most people never do, because they do not know the channel exists.</p>
    <div class="callout"><b>Where Kentuckians actually file.</b>The Attorney General's No Call complaint line is <strong>1-866-877-7867</strong>, and complaints can be filed online at <strong>nocall.ky.gov</strong>. Written complaints go to the Office of the Attorney General, 1024 Capital Center Drive, Suite 200, Attn: No Call, Frankfort, KY 40601. For consumer problems beyond telemarketing, the Consumer Protection hotline is <strong>1-888-432-9257</strong>.</div>
    <p>Filing takes a few minutes and you need very little: the date, the time, the number that called, and what they were selling. Write those four things down when it happens rather than trying to remember later.</p>

    <h2>The Kentucky scam alert almost nobody signs up for</h2>
    <p>Kentucky's <strong>Senior Medicare Patrol</strong> runs a text alert service that tells you what is circulating <em>in this state</em>, and I have never once had a client tell me they knew about it.</p>
    <p>Text <strong>KYSMP</strong> to <strong>844-796-5678</strong> and you get one message each Friday at noon describing a scam currently being reported in Kentucky. That is it. One text a week, free, from the state program whose entire job is tracking this.</p>
    <p>If you want a single thing to do after reading this page, that is the one I would pick. Knowing that this week's scam is a fake plan-cancellation call is worth more than any general advice about being careful, because you recognize the script when you hear it.</p>

    <h2>Six things that actually reduce the calls</h2>
    <div class="stage"><span class="num">1</span><span class="st"><b>Register at donotcall.gov</b>Free, takes two minutes, covers landlines and cell phones. It will not stop the outright criminals who already ignore the law, but it removes you from compliant marketing lists and it is what makes Kentucky's $5,000 penalty available to you.</span></div>
    <div class="stage"><span class="num">2</span><span class="st"><b>Say the exact words "put me on your do-not-call list"</b>Then write down the date. Legitimate companies are required to honor that request, and having the date is what gives your complaint standing if they call again.</span></div>
    <div class="stage"><span class="num">3</span><span class="st"><b>Stop filling in online Medicare quote forms</b>One submission can be resold to a dozen buyers, and it counts as the permission that makes calling you legal. If you want a comparison, call an agency directly instead.</span></div>
    <div class="stage"><span class="num">4</span><span class="st"><b>Do not press any key, including the removal one</b>On an illegal robocall, pressing any key confirms a live person answered. That makes your number more valuable, not less. Hang up instead.</span></div>
    <div class="stage"><span class="num">5</span><span class="st"><b>File the Kentucky complaint</b>1-866-877-7867 or nocall.ky.gov. This is the step nearly everyone skips, and it is the only one that carries a penalty behind it.</span></div>
    <div class="stage"><span class="num">6</span><span class="st"><b>Ask your phone carrier about call blocking</b>Most carriers now offer free spam-filtering apps, and both iPhone and Android can silence calls from numbers not in your contacts. That single setting stops more calls than everything else on this list combined.</span></div>

    <h2>Advisor or lead generator: telling them apart in one call</h2>
    <div class="tblwrap">
    <table class="nettbl">
      <tr><th>A licensed agent</th><th>A lead generator or scam call</th></tr>
      <tr><td>Gives a name, an agency, and a license or NPN number when you ask</td><td>Deflects, or names only a vague "Medicare benefits center"</td></tr>
      <tr><td>Tells you which carriers they represent, and admits they do not represent all of them</td><td>Claims to offer everything, or implies they are calling from Medicare</td></tr>
      <tr><td>Asks about your doctors, your prescriptions, and your budget before naming a plan</td><td>Asks for your Medicare number early in the call</td></tr>
      <tr><td>Is happy to be called back on a number you looked up yourself</td><td>Pushes you to decide during this call</td></tr>
      <tr><td>Says "keep what you have" when that is the right answer</td><td>Always finds a reason to switch you</td></tr>
    </table>
    </div>
    <p>One more question that costs nothing to ask: <em>will you still be my point of contact next year?</em> A lead generator cannot answer that, because they were never going to be.</p>

    <div class="note">
      <div class="who">
        <img src="/assets/austin-tyler.jpg" alt="Austin Tyler" width="600" height="750">
        <div><b>A note from Austin</b><span>Licensed Kentucky Medicare agent, Lexington</span></div>
      </div>
      <p>What bothers people most about these calls is not the interruption. It is the feeling that their information got away from them and they cannot get it back. I have sat across from people who stopped answering their phone entirely, including when their own doctor's office was calling.</p>
      <p>So the part I want you to take from this is the Kentucky complaint line, because it is the only step here that puts a cost on the other end. Most people assume nothing happens when they file. In a state with a $5,000-per-violation penalty and an Attorney General's office that handles these, something can.</p>
    </div>

    <h2>Where to report it in Kentucky</h2>
    <div class="help">
      <h3>Kentucky Attorney General, No Call complaints</h3>
      <p>For telemarketing calls to a number on the registry. This is the one with the penalty behind it.</p>
      <p class="ph">1-866-877-7867 &nbsp;·&nbsp; nocall.ky.gov</p>
    </div>
    <div class="help">
      <h3>Kentucky Senior Medicare Patrol</h3>
      <p>For anything that looks like Medicare fraud, and for the weekly Kentucky scam alert. Reach the program through your Area Agency on Aging.</p>
      <p class="ph">1-800-994-9422 &nbsp;·&nbsp; text KYSMP to 844-796-5678</p>
    </div>
    <div class="help">
      <h3>Medicare, and the federal registry</h3>
      <p>To report a plan or agent to Medicare directly, or to register your number.</p>
      <p class="ph">1-800-MEDICARE &nbsp;·&nbsp; donotcall.gov &nbsp;·&nbsp; 1-888-382-1222</p>
    </div>
    <p>If a caller already has your Medicare number and you are worried about how it is being used, that is a different problem with different steps, and our guide to <a href="/articles/medicare-scams-how-to-protect-yourself/">protecting your Medicare number</a> walks through them.</p>

    <h2 id="faq">Common questions from Kentucky</h2>
    <div class="faq">
      <h3>Does Kentucky have its own Do Not Call list?</h3>
      <p>Not a separate one any more. Kentucky's No Call list was merged into the National Do Not Call Registry in 2007, and numbers that were on the state list were transferred automatically, so you do not need to register twice. New registrations go through donotcall.gov or 1-888-382-1222. What Kentucky kept is the enforcement: the Attorney General can prosecute telemarketers who call registered Kentucky numbers, with fines of up to $5,000 per violation.</p>
      <h3>How do I report a Medicare telemarketing call in Kentucky?</h3>
      <p>File with the Kentucky Attorney General's No Call program at nocall.ky.gov or by calling 1-866-877-7867. Written complaints can be mailed to the Office of the Attorney General, 1024 Capital Center Drive, Suite 200, Attn: No Call, Frankfort, KY 40601. Note the date, the time, the calling number, and what was being sold. For calls that look like Medicare fraud rather than nuisance marketing, contact the Kentucky Senior Medicare Patrol at 1-800-994-9422 or Medicare at 1-800-MEDICARE.</p>
      <h3>Is it legal for someone to cold-call me about Medicare?</h3>
      <p>No. Federal rules prohibit unsolicited contact about Medicare Advantage and Part D plans, including cold calls and uninvited door-to-door visits, unless you gave permission to be contacted. Filling in an online form or mailing back a reply card usually counts as giving that permission. High-pressure sales tactics remain prohibited even after the marketing rule changes that took effect October 1, 2026.</p>
      <h3>Why did the Medicare calls get worse in 2026?</h3>
      <p>CMS loosened several marketing rules effective October 1, 2026, for the 2027 plan year. The 48-hour wait between a Scope of Appointment and a sales discussion was removed, the required separation between educational and marketing events was removed, agents may now collect a Scope of Appointment at an educational event, and substantiated superlatives such as "best" are now permitted in advertising. Cold calling, uninvited door-to-door sales, and high-pressure tactics all remain prohibited.</p>
      <h3>How can I tell if a Medicare agent is legitimate?</h3>
      <p>Ask for their name, their agency, and their license or National Producer Number, and ask which insurance carriers they represent. A licensed agent answers all of it, acknowledges they do not represent every company, and will let you call back on a number you look up yourself. They will also ask about your doctors, prescriptions, and budget before recommending anything. Anyone who asks for your Medicare number early, claims to be from Medicare, or pressures you to decide on the call is neither.</p>
      <h3>Will Medicare ever call me?</h3>
      <p>Medicare does not call beneficiaries to ask for a Medicare number, Social Security number, or bank details, and does not sell plans over the phone. If someone says they are from Medicare and asks for that information, hang up and call 1-800-MEDICARE yourself using the number on your card or from Medicare.gov.</p>
    </div>

    <div class="endcta">
      <h3>Tired of not knowing who to trust?</h3>
      <p>I am a licensed agent with an office on Monarch Street in Lexington. You can look me up, call me back on a number you found yourself, and sit across a table from me. There is no cost, and if the plan you have is the right one I will tell you that.</p>
      <div class="row">
        <a class="btn" href="/review/">Talk to a local agent &rarr;</a>
        <p class="callline">Or call me directly: <a href="tel:18596186443">(859) 618-6443</a></p>
      </div>
    </div>

    <section class="recap">
      <h2>Quick recap</h2>
      <div class="recap-item">Federal Medicare marketing rules loosened on October 1, 2026, so this enrollment season moves faster and louder than last year's.</div>
      <div class="recap-item">Cold calls, uninvited door-to-door sales, and high-pressure tactics are all still prohibited.</div>
      <div class="recap-item">Most calls come from lead generators reselling your contact information, not from agents. One online form can produce a dozen callers.</div>
      <div class="recap-item">Kentucky's No Call list merged into the national registry in 2007, so register once at donotcall.gov.</div>
      <div class="recap-item">Kentucky kept enforcement. The Attorney General can fine telemarketers up to $5,000 per violation, and complaints go to nocall.ky.gov or 1-866-877-7867.</div>
      <div class="recap-item">Text KYSMP to 844-796-5678 for a weekly alert on scams being reported in Kentucky.</div>
      <div class="recap-item">Never give your Medicare number to someone who called you first.</div>
    </section>

    <section class="kcheck">
      <h2>Test what you learned</h2>
      <p class="kc-sub">Five quick questions. Pick an answer to see if you're right, and why.</p>
      <div id="kcheck"></div>
    </section>
    <script>window.KCHECK = __KCHECK__;</script>

    <div class="sources">
      <b>Sources</b>
      Kentucky Attorney General, Kentucky "No Call" Law (ag.ky.gov) &middot;
      Kentucky Public Service Commission, Reducing Telemarketing Calls (psc.ky.gov) &middot;
      Senior Medicare Patrol, Kentucky (smpresource.org) &middot;
      Federal Trade Commission, National Do Not Call Registry (donotcall.gov) &middot;
      CMS contract year 2027 Medicare Advantage and Part D final rule, marketing provisions effective October 1, 2026.
      Verified August 2026.
    </div>

    <p class="stamp"><b>Written and reviewed by Austin Tyler</b>, licensed Kentucky agent, NPN 20234188, Kentucky DOI license #1187780. Phone numbers and complaint channels checked in August 2026.</p>

    <p class="disclaim">This article is general information, not advice for your specific situation, and it is not legal advice. Rules, phone numbers, and complaint procedures can change; confirm current details with the agency before relying on them. Tyler Insurance Group is not connected with or endorsed by the United States government or the federal Medicare program. We do not offer every plan available in your area. Currently we represent 6 organizations which offer 158 products in your area. Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance Program (SHIP) to get information on all of your options.</p>
"""

KCHECK = [
 {"q": "Someone calls you out of the blue about a Medicare Advantage plan. Is that allowed?",
  "options": ["Yes, during open enrollment", "No, cold calls about Medicare plans require your prior permission",
              "Yes, if they are licensed", "Only on weekdays"],
  "answer": 1,
  "why": "Federal rules prohibit unsolicited contact about Medicare Advantage and Part D plans unless you gave permission. Filling in an online form or returning a reply card often counts as that permission."},
 {"q": "Does Kentucky still run its own separate Do Not Call list?",
  "options": ["Yes, you must register with both", "No, it merged into the National Do Not Call Registry in 2007",
              "No, Kentucky never had one", "Only for landlines"],
  "answer": 1,
  "why": "Kentucky folded its list into the national registry in 2007 and transferred existing numbers automatically. You register once, at donotcall.gov."},
 {"q": "What can the Kentucky Attorney General do about a telemarketer who calls a registered number?",
  "options": ["Nothing, it is a federal matter now", "Send a warning letter only",
              "Prosecute, with fines up to $5,000 per violation", "Remove your number from more lists"],
  "answer": 2,
  "why": "Merging the list did not move enforcement. Kentucky can fine violators up to $5,000 per call, but only when someone files a complaint at nocall.ky.gov or 1-866-877-7867."},
 {"q": "An illegal robocall offers to remove you from its list if you press a key. What should you do?",
  "options": ["Press it, that is the fastest way off", "Press it twice to confirm",
              "Hang up without pressing anything", "Stay on the line and ask for a supervisor"],
  "answer": 2,
  "why": "Pressing any key confirms a live person answered, which makes your number more valuable and usually increases the calls. Hang up instead."},
 {"q": "What is the fastest way to know which Medicare scam is currently circulating in Kentucky?",
  "options": ["Watch for it on national news", "Text KYSMP to 844-796-5678 for the weekly state alert",
              "Wait for a letter from Medicare", "Ask your pharmacy"],
  "answer": 1,
  "why": "The Kentucky Senior Medicare Patrol sends one text each Friday describing a scam being reported in Kentucky. It is free, and almost nobody signs up for it."},
]

body_html = BODY.replace("__KCHECK__", json.dumps(KCHECK, ensure_ascii=False))

# ---------------------------------------------------------------- assemble
out = re.sub(r'(<nav class="crumb" aria-label="Breadcrumb">).*?(</nav>)',
             r'\1<a href="/">Home</a> &rsaquo; <a href="/articles/">Learning Center</a> &rsaquo; '
             + CRUMB_LABEL + r'\2', out, count=1, flags=re.S)

out = re.sub(r'<span class="tag">.*?</span>', '<span class="tag">Medicare Basics · Local Kentucky</span>',
             out, count=1, flags=re.S)
out = re.sub(r'<h1>.*?</h1>', f'<h1>{H1}</h1>', out, count=1, flags=re.S)
out = re.sub(r'(Local Kentucky Medicare agent · )[^<]*(</div>)',
             r'\1Updated August 19, 2026 · 10 min read\2', out, count=1)

m = re.search(r'(<div class="body">\n)(.*?)(\n  </div>\n</article>)', out, re.S)
assert m, "body block not found"
out = out[:m.start(2)] + body_html.strip("\n") + out[m.end(2):]

# ---------------------------------------------------------------- schema
mm = re.search(r'<script type="application/ld\+json">(.*?)</script>', out, re.S)
d = json.loads(mm.group(1))
faq_html = re.search(r'<div class="faq">(.*?)</div>', out, re.S).group(1)
clean = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()
pairs = [(clean(q), clean(a)) for q, a in re.findall(r"<h3>(.*?)</h3>\s*<p>(.*?)</p>", faq_html, re.S)]

for node in d["@graph"]:
    t = node.get("@type")
    if t == "BlogPosting":
        node["headline"] = H1
        node["description"] = DESC
        node["datePublished"] = "2026-08-19"
        node["dateModified"] = "2026-08-19"
        node["articleSection"] = "Medicare Basics"
        node["mainEntityOfPage"] = {"@type": "WebPage", "@id": URL}
        node["@id"] = URL + "#article"
    elif t == "BreadcrumbList":
        node["itemListElement"] = [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.bluegrassmedicarehelp.com/"},
            {"@type": "ListItem", "position": 2, "name": "Learning Center", "item": "https://www.bluegrassmedicarehelp.com/articles/"},
            {"@type": "ListItem", "position": 3, "name": CRUMB_LABEL, "item": URL}]
    elif t == "FAQPage":
        node["mainEntity"] = [{"@type": "Question", "name": q,
                               "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]
out = out[:mm.start(1)] + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + out[mm.end(1):]

os.makedirs(DST_DIR, exist_ok=True)
open(f"{DST_DIR}/index.html", "w", encoding="utf-8").write(out)
print(f"wrote {DST_DIR}/index.html  ({len(pairs)} FAQ entries, {len(KCHECK)} kcheck questions)")
