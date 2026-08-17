# Local content standards: county and town pages

Applies to every page or article about a specific Kentucky county or town (city pages,
`/kentucky/`, county articles, hospital network guides). Sits alongside
`docs/writing-standards.md` (True, Useful, Clear) and adds the local bar on top.

Why this exists: Google crawled our five city pages in July 2026 and refused to index two of
them (Winchester, Nicholasville). Those two were 65 to 72 percent identical to their siblings,
a template with the town name swapped. The three that survived were the more differentiated
ones. Google independently confirmed what the audit predicted: templated local pages are a
liability. This document defines what replaces them.

## The bar

> **Every local claim must be (a) decision-relevant, (b) verifiable, (c) dated.**

Two tests before a local page ships:

1. **The Texas test.** Could a content writer at a national Medicare site, sitting in another
   state, produce this paragraph without making a phone call? If yes, cut it or replace it.
   Generic Medicare rules with a town name attached fail this test.
2. **The nod test.** Would a longtime resident of that county read the page and nod, because it
   describes the place they actually live: their hospital, their pharmacy situation, their
   employer's retiree plan? If a paragraph would read the same for any county in America, it
   does not belong on a county page.

"Hard to know" is not the standard by itself. **Hard to know AND it changes the reader's
Medicare decision** is the standard. Local color that carries no decision weight (naming the
hospital CEO, the courthouse, the high school mascot) is decoration. Sprinkled decoration on
template text is exactly the pattern Google's spam policies describe as doorway pages. Never
use decoration as a substitute for substance; use a local detail only when it is attached to a
fact the reader acts on.

## What counts, ranked by decision weight

### Tier 1: changes which plan they pick (every county page needs several of these)

1. **Plan counts for that county, this plan year.** Number of Medicare Advantage plans, number
   of $0-premium plans, number of D-SNPs, number of stand-alone Part D plans. Source: the CMS
   landscape files or Medicare.gov plan finder, pulled fresh each AEP and dated on the page.
   Counts differ by county, which is the entire point of county pages.
2. **Hospital and system network status.** The hospital residents of that county actually use
   (Clark Regional in Winchester, Saint Joseph Jessamine, Georgetown Community, Baptist Health
   Richmond), and which carriers' MA networks include it, verified and dated. Include where
   people really go: many Jessamine County residents use Lexington hospitals, so Lexington
   network status belongs on the Nicholasville page too.
3. **Big medical groups and clinics, at the practice level.** Whether the large local practices
   (for example Lexington Clinic and the major primary care groups) accept Original Medicare
   and which MA networks they are in. Name practices and systems, not individual physicians
   (see cautions). Every acceptance claim carries a verification date.
4. **Pharmacy landscape.** Which pharmacies in town are preferred cost-share on the major Part D
   plans, which are standard, what closed recently, which is the only 24-hour option, whether
   the county has a pharmacy desert problem. Preferred vs standard pharmacy status changes real
   out-of-pocket costs and nobody national covers it at town level.
5. **Dental, vision, hearing reality check.** MA dental networks are thin outside Lexington. A
   dated, phone-verified finding like "we called every general dentist in Winchester in
   September 2026; N of M accept any Medicare Advantage dental network" is content no national
   site has and no AI can fabricate. Prefer aggregate findings over naming who accepts what;
   if a practice is named, date it.
6. **Employer and retiree context.** The county's major employers and how their retiree coverage
   interacts with Medicare: Toyota in Scott County, school districts (TRS/MEHP) everywhere,
   state and county government (KPPA), the hospital systems themselves. "If you retired from
   Toyota, here is how that coverage meets Medicare" is hyper-local, high-intent, and already
   our strongest content pattern (the KPPA and TRS guides are among our best-ranking pages).
7. **County enrollment data.** CMS publishes MA enrollment and penetration by county. "About X
   percent of Clark County Medicare beneficiaries are on Medicare Advantage, and carrier Y has
   the largest share" is public data almost no one surfaces, refreshed annually, and a natural
   citation magnet for AI answers.
8. **Geography quirks that change eligibility or plan sets.** Zip codes that straddle county
   lines (a Lexington mailing address does not always mean Fayette County), drive times to
   in-network specialists, dialysis and cardiology access, where the nearest Social Security
   office actually is and how long appointments run.

### Tier 2: builds trust and proves presence

9. **Anonymized client patterns.** "Of the Winchester households we helped last year, the
   deciding factor was almost always whether Clark Regional was in network." Real experience,
   aggregated, no names, no PII, no outcomes promised. This is the Experience half of E-E-A-T
   and cannot be replicated by a call center.
10. **One kitchen-table observation per page.** A specific, true thing Austin knows from sitting
    with people in that county: the plan everyone seems to arrive with, the benefit people
    there ask about first, the misconception that keeps coming up locally. One is enough.
11. **Local help infrastructure, with real details.** The county senior center by name with its
    address and phone, the SHIP counseling schedule, the Area Agency on Aging contact, where
    and when Austin holds local office hours or events. Details that are checkable by calling.
12. **What changed locally this year.** Plan exits, carrier and hospital contract disputes
    (these make local news), a pharmacy closure, a new clinic. Seasonal: refresh every AEP.
13. **Disaster and weather SEPs when relevant.** Kentucky has had FEMA-declared floods and
    tornadoes; affected counties get Special Enrollment Periods. Knowing which counties
    qualified and until when is Kentucky-specific expertise.

### Tier 3: color (use at most sparingly, only attached to a fact)

Landmarks, history, mascots, named individuals who are not the author. Allowed only when the
detail carries a Tier 1 or 2 fact ("the new cardiology wing at Clark Regional" is fine when
the point is network access). A page built on Tier 3 is a doorway page and does not ship.

## Cautions (compliance and accuracy)

- **Do not name individual physicians as recommendations.** Practices and systems only.
  Individual doctors move, retire, and close panels; a stale named claim is a YMYL accuracy
  failure and can read as endorsement. If an individual is ever named, it is with their
  practice, a verification date, and never as advice to choose them.
- **Hospital executives, by name, are trivia.** Skip unless the person is the news (a CEO
  announcing a network dispute is a fact; a CEO existing is not).
- **Plan counts and network facts are educational; named-plan benefits are marketing.** Stating
  how many plans exist in a county and which networks include a hospital is factual content.
  Quoting a named plan's benefits or premiums edges into content that can require carrier
  approval and CMS filing. Stay on the factual side; send benefit specifics to the
  consultation.
- **Every local fact gets a source and a date.** Verified by phone: say so, with the month.
  From CMS files: name the file and year. From Austin's client experience: framed as
  experience, aggregated, no PII. **Never fabricate a local detail.** An invented local fact
  is worse than a generic page; one resident noticing kills the credibility the page exists
  to build.
- **Freshness stamp.** Every county page carries "Reviewed by a licensed agent, [Month Year]"
  and gets re-verified every September before AEP, when the new landscape files land.

## Minimum bar to publish

A county or town page ships only if it has:

- [ ] At least **5 Tier 1 items**, each sourced and dated
- [ ] At least **1 phone-verified fact** ("we called, [month year]")
- [ ] At least **1 anonymized experience paragraph** (Tier 2, item 9 or 10)
- [ ] Local help contacts (Tier 2, item 11)
- [ ] A named human author with credentials, and a review stamp
- [ ] Zero paragraphs that fail the Texas test
- [ ] Body similarity to every sibling county page **under 40 percent** (measure it; the
      audit scripts in `docs/audit-2026/` show how). Lexington passed at 38 to 47 percent and
      was indexed; the pages at 65 to 72 percent were refused.

If the dossier for a county is not filled in yet, the county keeps a section on `/kentucky/`
instead of a standalone page. A thin standalone page is worse than no page.

## The county dossier (what Austin collects per county)

Copy this list per county. Most of it is one afternoon: two or three phone calls, the CMS
plan finder, and what Austin already knows.

1. Plan counts (MA total, $0 premium, D-SNP, PDP) from the plan finder, with pull date
2. Hospital(s) residents use + carrier network status for each, with verification date
3. Top 2 or 3 medical groups + Medicare / MA acceptance, verified by a call to billing
4. Pharmacy notes: preferred networks, closures, 24-hour, independents
5. Dental ring-around result (calls made, how many accept MA dental)
6. Top employers + retiree coverage interaction (Toyota, schools, KPPA, hospital)
7. Senior center + SHIP schedule + AAA contact, with phone numbers
8. County MA penetration and top carrier share (CMS enrollment file)
9. Zip/county-line quirks and specialist drive times
10. What changed this year (exits, disputes, closures)
11. One kitchen-table observation and one anonymized client pattern

## Why this also wins AI search

Retrieval systems disproportionately cite sources with information unavailable elsewhere,
stated in liftable, self-contained passages. A dated table of county plan counts, a
carrier-by-hospital network grid, and a phone-verified dentist count are exactly that. Put
the facts in tables with a stated verification date, lead each section with the direct
answer, and these pages become the citation magnets the strategy calls for. The same work
that satisfies Google's quality systems is the work that gets quoted by ChatGPT and
Perplexity when someone asks "how many Medicare Advantage plans are there in Clark County
Kentucky."
