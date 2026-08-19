# Website Structure & Design Deep-Dive: Building for Seniors and for Scale

How the best sites are designed and structured in 2025-2026, whether that feeds ranking, and
exactly what Bluegrass Medicare Help should change. Grounded in a read of the actual codebase
(index.html, articles/index.html, site.css, city pages) plus primary-source research (Nielsen
Norman Group, W3C/WCAG, Google Search Central, Pew, peer-reviewed HCI work).

Prepared July 14, 2026. Companion to `kentucky-authority-strategy-2026.md`.

---

## The one-paragraph answer

**Yes, structure and design feed ranking, but indirectly, and the internet is full of fake
numbers about how much.** Google has said plainly, through John Mueller, that page experience is
"more than a tie-breaker, but it doesn't replace relevance" and that Core Web Vitals "are not
giant factors in ranking." So the honest calibration is: fast, accessible, well-structured pages
win ties among comparable results and get parsed and cited more reliably by Google and AI answer
engines, but they do not out-rank genuinely more relevant, more expert content. **The large
ranking levers for a Medicare site are helpful YMYL content, topical depth, and real E-E-A-T,
not performance micro-tuning.** The good news: your current design is already well-matched to the
evidence. The real work is *information architecture for scale*, where the site has a genuine
structural limit that will bite as it grows. That is where this document spends most of its time.

A note on sourcing, because this topic is unusually polluted: many widely-repeated stats ("Core
Web Vitals are 25-30% of ranking weight," "accessible sites get 37% more traffic," "topic
clusters get 3.2x more AI citations") come from vendor blogs with no primary methodology. They
are marketing, not evidence, and this document does not rely on them. Where a claim is documented
(Google, W3C, NN/g, Pew, peer-reviewed), it is treated as fact; where it is practitioner
consensus, it is labeled as such.

---

## Part 1: Is the site hitting the mark for seniors? (Mostly yes.)

You asked whether the site is hitting the mark. On senior usability, the evidence says you are
closer than you think. Here is the current site measured against the documented specs.

### The specs that matter for a 65+ audience (documented)
- **Body text 16px minimum, 17-20px preferred for sustained reading.** The strongest empirical
  anchor is a 2022 peer-reviewed study (Xu et al., *Frontiers in Psychology*): older adults
  preferred ~17px for intensive reading and 17-20px for articles.
- **Line-height 1.5-1.6x** for body text (aligns with WCAG 1.4.12).
- **Color contrast 4.5:1 for body text, 3:1 for large text and UI** (WCAG 2.2 AA); aim above the
  floor for seniors.
- **Tap targets: 24x24px is the WCAG 2.2 floor; 44-48px is the practical recommendation** for
  seniors and touch (Apple HIG 44pt, Material 48dp).
- **Avoid** sliders, drag actions, hover-only menus, placeholder-only form fields, startling
  motion. WCAG 2.2 specifically added protections here (2.5.7 Dragging, 2.5.8 Target Size, 3.3.7
  Redundant Entry, 3.3.8 Accessible Authentication).
- **Reading level 6th-8th grade** for health content; one idea per sentence.
- **Assume a phone on mediocre bandwidth.** Pew (Jan 2024): 90% of 65+ are online and ~78% own a
  smartphone, but only ~70% have home broadband (lowest of any age group) and only ~14% are
  online "almost constantly." Seniors browse in short, focused sessions, often on phones.

### How the current site scores (from reading the code)
| Spec | Evidence in the code | Verdict |
|---|---|---|
| Body text ≥17px | Article prose is **18px**; homepage note/office copy 17-17.5px | Pass, genuinely good |
| Line-height 1.5-1.6 | `body{line-height:1.6}`; prose blocks 1.55-1.62 | Pass |
| Whole-card tap targets | Topic cards, article rows, quiz tiles are full `<a>` elements | Pass, exactly right |
| Focus visible | `:focus-visible{outline:3px solid coral}` in site.css | Pass |
| Reduced motion | `@media (prefers-reduced-motion:reduce)` zeroes animation | Pass |
| Skip link | Present on every page | Pass |
| No drag/slider UI | Quizzes and filters are tap-only buttons | Pass |
| Font loading | Google Fonts with `display=swap` | Pass (self-hosting would be faster, minor) |
| Analytics deferred | GA4 async; Meta Pixel in `<head>` | Mostly; see perf note |

**Where it falls short of the senior bar (all small, all fixable):**
1. **Chrome text runs 13-15.5px.** The utility strip (13px), nav links (15.5px), article dates
   and category tags (11-13.5px), and review-card body (15.5px) are below the 16px reading floor.
   For non-reading chrome (a date stamp, a tag) this is defensible, but the **utility strip's
   location line and the review-card testimonials are content a senior actually reads**, and they
   should be nudged to 16px+. The 10.5px brand sub-label is decorative but tiny.
2. **Contrast on muted text is unverified.** `--mute:#5f594f` and especially `--faint:#938c80` on
   cream backgrounds should be checked against 4.5:1. `--faint` at 15px is the most likely AA
   failure on the site. This is a five-minute audit with a contrast checker and a token tweak.
3. **The Meta Pixel loads in `<head>`.** On an otherwise near-instant static page, third-party
   tags (Pixel, GA4) are the single most likely drag on INP/LCP. They should load after content.
4. **No visible "last updated" date on articles.** Bylines show a publish date; for YMYL trust
   and AI freshness signals, a visible "Reviewed [Month Year]" is worth more than the publish date
   (more on this under E-E-A-T).

**Bottom line for seniors:** the fundamentals are right and better than most local competitors.
The gaps are a contrast/font-size hygiene pass and deferring third-party scripts, not a redesign.
The single highest-value senior-UX research you could do is almost free: **tree-test the
navigation with three or four actual 68-year-olds** ("find me the page about drug-plan costs")
before scaling the site. NN/g's tree-testing method exists precisely to answer "can a senior find
this from the nav," and it will teach you more than any amount of analytics.

---

## Part 2: The real problem is architecture for scale

This is where the site is not yet built for what you want it to become. Three findings from the
code, in order of how much they will constrain growth.

### Finding 1: The Learning Center categories are not real pages
The seven topic cards (Medicare Basics, Costs & Savings, Local Kentucky, etc.) are not links to
category pages. They are `href="#guides"` anchors that trigger a JavaScript filter over a single
flat list of all 28 articles held in one HTML file. The category "pages" have no URLs.

Why this matters as you scale:
- **There is no `/articles/costs/` or `/articles/local-kentucky/` page to rank.** Category/pillar
  pages are usually the *strongest* rankers on a content site because they target the broad head
  term ("Medicare costs in Kentucky") and accumulate internal links from every article in the
  cluster. You currently have zero of them.
- **There is nothing to link to.** When an article wants to say "see all our Costs guides," it
  can only point at a JavaScript filter state, not a real page. Internal linking, the mechanism
  that builds topical authority, has no category-level target to point at.
- **It does not survive scale.** At 28 articles, one flat filtered list is fine. At 100-150
  articles plus county pages, it becomes a single enormous HTML file that is slow to render, hard
  to hand-maintain, and impossible for a crawler to segment into topics.
- **AI answer engines parse pages, not filter states.** A crawlable, well-structured
  `/articles/turning-65/` hub that answers the broad question and links to the deep-dives is
  exactly the kind of page that gets cited; a `#guides` anchor is invisible to that process.

The fix is the pillar-cluster model, which is the documented consensus IA for content-heavy
educational sites: a **pillar/hub page** per topic gives broad coverage and links down to **cluster
articles** that go deep, and every cluster links back up to its hub. This is not a rewrite of your
content; it is promoting each of the seven categories from a filter into a real hub page with its
own URL, intro, and curated list. The existing filtered index stays as the "all guides" view.

### Finding 2: The navigation has no room for "local"
The nav is five hand-inlined links (Learning Center, Quizzes, Free Guide, Free Review, About) plus
Call, repeated verbatim on every page. There is no "Kentucky" or "Local" entry, even though
hyper-local is the entire brand strategy. This is why the four county pages
(Richmond/Winchester/Nicholasville/Georgetown) are orphaned: there is nowhere in the nav or footer
to put them, so nothing links to them except one article, and Google treats unlinked pages as
unimportant.

As the site grows to a Kentucky hub with county guides, hospital-network guides, and a Medicare
101 events page, a flat five-item nav cannot hold it. The documented pattern for large sites (NN/g,
*Mega Menus Work Well*) is grouped navigation: a small number of top-level entries, each opening
into chunked, related sub-items derived from how users think. You do not need a heavy mega-menu
yet, but you need a **local hub in the nav** and a structure the nav can grow into.

### Finding 3: Breadcrumbs exist only in schema, never rendered
Every article and city page carries `BreadcrumbList` JSON-LD, but no breadcrumb trail is drawn on
the page. So the machine gets the orientation cue and the senior does not. Rendered breadcrumbs
(Home > Learning Center > Costs > This article) are a documented orientation and back-path aid,
they reduce dead ends, and they align the visible page with the schema. This is a small template
addition with outsized usability value on a deep site.

---

## Part 3: The proposed information architecture

A concrete target structure. It preserves everything that works (the flat filtered index, the
senior-first design, the conversion funnels) and adds the scaffolding for scale.

```
Home  /
│
├── Learning Center  /articles/            ← hub of hubs (keep the filtered "all guides" list)
│   ├── Medicare Basics        /articles/basics/         ← NEW real hub pages, one per category
│   ├── Turning 65             /articles/turning-65/         each: intro + curated cluster list
│   ├── Coverage Choices       /articles/coverage/           + links down to articles, up to /articles/
│   ├── Costs & Savings        /articles/costs/
│   ├── Already on Medicare    /articles/on-medicare/    ← rebuild as the AEP/disruption hub
│   ├── Social Security        /articles/social-security/
│   └── Local Kentucky         /articles/kentucky/       ← ties into the Kentucky hub below
│       └── (28 existing articles live under /articles/<slug>/ as today, each tagged to a hub)
│
├── Kentucky Medicare  /kentucky/          ← NEW local pillar (the moat), in the main nav
│   ├── Medicare in Lexington / Fayette County   /medicare-lexington-ky/     ← NEW flagship
│   ├── Richmond / Madison County      /medicare-richmond-ky/       ← existing, de-orphaned
│   ├── Winchester / Clark County      /medicare-winchester-ky/     ← existing, de-orphaned
│   ├── Nicholasville / Jessamine      /medicare-nicholasville-ky/  ← existing, de-orphaned
│   ├── Georgetown / Scott County      /medicare-georgetown-ky/     ← existing, de-orphaned
│   └── (county guides roll out slowly from here, each majority-unique, see risk note)
│
├── Reviews  /reviews/                     ← NEW, captures "Tyler Insurance Group reviews", E-E-A-T
├── Tools    /tools/                       ← NEW hub for calculators (Plan G vs N, IRMAA, hospital lookup)
├── Events   /events/                      ← NEW, Medicare 101 library/senior-center sessions
│
├── Free Guide   /guide/       ┐
├── Free Review  /review/      ├── conversion funnels, unchanged
├── Quizzes      /quizzes/     ┘
│
└── About  /about/
    └── Austin Tyler  /about/austin-tyler/  ← NEW full author/E-E-A-T page, every byline links here
```

**Proposed navigation** (grows from 5 flat links to a scalable grouped structure):
- **Learning Center** (opens the category hubs)
- **Kentucky** (opens Lexington + counties + hospital guides) ← the new local entry
- **Free Help** (Guide, Review, Quizzes grouped)
- **Reviews**
- **About**
- **Call** (unchanged, always visible)

On mobile this stays the existing hamburger; the grouping just organizes the drawer. This is the
minimum nav that can hold a scaling local authority site without becoming a flat wall of links.

---

## Part 4: County/location pages, done without wrecking the domain

This is the highest-stakes structural decision, so it gets its own section. The county-guide system
is the moat (nobody local answers "which 2026 plans keep me in-network at UK HealthCare"), but it
is also the single most likely way to damage the whole site if done wrong.

**The documented risk:** Google's doorway-page policy treats thin, near-duplicate location pages
(a template with the city name swapped) as a spam violation, and the scaled-content-abuse and
helpful-content systems evaluate a site *holistically*. A large tail of thin county pages can
suppress the rankings of the entire domain, including your good articles. This is not a
theoretical risk; it is the documented mechanism behind many local-site penalties.

**The rule that keeps county pages safe** (practitioner consensus, consistent with Google policy):
each location page must carry genuinely unique, locally-specific substance, not a reskinned
template. For a Kentucky Medicare county page, "unique substance" means real, verifiable, local
content:
- Which carriers and roughly how many MA plans are actually available in that county for the year.
- The specific hospitals and systems in that county and their current MA network status (the
  Baptist/UK/CHI in-network question), verified against the provider's own page.
- The county's SHIP contact and Area Agency on Aging (e.g., Bluegrass ADD for Central KY).
- A local scenario or client story true to that county.
- Genuinely county-specific FAQs.

**The discipline:** if you cannot write something true and useful that is specific to that county,
do not publish the page. Grow the set slowly (Fayette first, then the four that already have pages,
then outward), refresh each annually, and never batch-generate. Ten excellent county pages beat
forty templated ones, and forty templated ones can sink the whole domain.

---

## Part 5: Does design/performance actually move ranking? (The honest version)

Direct answer to your question, with the evidence and the debunking, because this is where you will
be told the most nonsense.

**Core Web Vitals are a real but minor, tie-breaker-level signal.**
- The metrics and "good" thresholds (Google, official): LCP ≤ 2.5s, INP < 200ms (INP replaced FID
  on March 12, 2024), CLS < 0.1, at the 75th percentile of real users.
- Google's own calibration (Mueller): page experience is "more than a tie-breaker… but relevance
  is still by far much more important," and CWV "are not giant factors in ranking." The
  page-experience FAQ states a page with subpar experience can still rank highly with great,
  relevant content.
- **Fabricated claims to ignore:** "CWV = 25-30% of ranking weight," "8-15% visibility boost,"
  "March 2026 update made INP equal weight." Google has never published any percentage weight;
  these numbers are invented by vendors. The defensible statement: passing CWV wins ties and,
  more importantly, **converts anxious seniors better** because the page is fast and stable.
- **Your stack is already near-ideal here.** Static HTML on GitHub Pages (HTTPS by default) with
  inline-SVG illustrations (vector, tiny, no image-format or CDN concerns) gives you excellent
  LCP/CLS for free. The one real risk is third-party tags; defer the Pixel and GA4.

**Mobile-first indexing is table stakes.** Google completed mobile-first indexing for 100% of
sites by July 5, 2024; it crawls the smartphone version. Your responsive layout handles this.

**Accessibility is not a confirmed direct ranking factor, but the overlap is real and mechanistic.**
Google has repeatedly said accessibility is not a direct signal (ignore the "+37% traffic" vendor
claims). But the *same* practices that serve a screen reader also serve Googlebot and LLM crawlers:
semantic HTML (`<header>/<nav>/<main>/<article>`, one `<h1>`, logical heading order), descriptive
alt text, link text that makes sense out of context, and valid markup. Google parses page structure
much as a screen reader does, so accessible pages are more crawlable and better understood. That is
an *indirect* SEO benefit and a direct senior-UX benefit from the same work.

**Engagement signals do feed ranking (documented existence, contested mechanics).** The May 2024
Google API leak (verified by SparkToro) revealed NavBoost, a click-based re-ranking system tracking
click quality over a ~13-month window, plus Chrome-derived signals, contradicting years of Google
denials. DOJ antitrust testimony separately confirmed NavBoost's role. What this proves: user
click/engagement behavior *is* used, so design that earns clicks and keeps users satisfied has an
indirect ranking benefit. What it does *not* prove: exact weightings or a tidy "dwell time" dial;
those remain inference. The practical takeaway is unchanged: satisfy the user and the engagement
signal takes care of itself.

**Structure helps AI parsing and citation.** Clean semantic HTML, question-style H2/H3 headings,
answer-first passages (~40-60 words), tables for discrete data, and JSON-LD reduce parser ambiguity
for LLM/RAG systems. The structural logic is documented; the specific "tables get 2.5x more
citations" multipliers are unverified vendor claims. Direction right, numbers not proven.

---

## Part 6: Trust design for YMYL (the multiplier you already control)

For a Medicare (YMYL health + finance) site, trust design is not decoration; it is what makes
Google's raters and AI answer engines willing to surface you, and what makes an anxious senior pick
up the phone. The framework is E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness,
with Trust at the center), the modern descendant of the Stanford Web Credibility guidelines. Every
lever that matters here is content/markup you fully control on a static stack:

- **A real, named, credentialed agent with photo and license info.** You have Austin Tyler; use it
  harder. Ship the full author page (`/about/austin-tyler/`), show the license/NPN, and link every
  byline to it. In 2025 Google elevated "Experience" (firsthand, real-world knowledge) alongside
  formal credentials; a local agent who does this daily is the definition of it.
- **Real local photos** beat stock and illustration for trust (your CLAUDE.md already says this,
  correctly). Keep the inline SVGs for topic scenes, but prioritize real Lexington/office/client
  photos where you have them.
- **Primary-source citations (CMS, SSA, KY DOI) visible on every dollar figure**, not just verified
  in the editing process. Surfacing the citation is what makes the page quotable by an AI engine.
- **Visible "last updated / reviewed" dates.** For annually-changing Medicare numbers, a visible
  "Reviewed July 2026" is a freshness and trust signal that a static publish date is not.
- **Clean, uncluttered layout with no aggressive pop-ups**, and the CMS compliance disclaimer done
  correctly (see the compliance note below).

The point worth internalizing: the same author page, citations, dates, and clean layout serve
E-E-A-T ranking, senior reassurance, and AI-citation-worthiness simultaneously. Trust design is the
highest-leverage work on the site because one effort pays in all three currencies.

---

## Part 7: The design system is right; do not add tooling

A brief reassurance, because it is tempting to over-engineer this. The site uses CSS custom
properties in a `:root` brand-token block in `site.css` (`--coral`, `--ink`, `--line`, etc.). That
is exactly the recommended design-system altitude for a small hand-authored team. Every major
system (Tailwind v4, Material 3, GitHub Primer, Shopify Polaris) ships CSS-variable tokens first;
the documented guidance for a single-codebase team is that "a well-maintained set of CSS variables
may be sufficient." You do not need a token pipeline, a framework, or a build step. The one
maintenance improvement worth making is consolidating the large per-page inline `<style>` blocks
that duplicate rules already in (or that belong in) `site.css`, so brand changes happen in one
place. That is hygiene, not architecture, and it is low priority.

---

## Part 8: Compliance note (flagged, needs your input)

While reading the code I found a compliance gap that is not a design issue but sits in the shared
footer, so it touches every page. **The footer disclaimer is missing required TPMO disclaimer
elements.** The current text says:

> "…We do not offer every plan available in your area. Any information we provide is limited to
> those plans we do offer in your area. Please contact Medicare.gov or 1-800-MEDICARE to get
> information on all of your options."

The current CMS-required TPMO disclaimer (42 CFR 422.2267(e)(41)) for an agency that does not sell
every plan needs the organization/plan counts and the SHIP reference:

> "We do not offer every plan available in your area. Currently we represent [X] organizations
> which offer [Y] products in your area. Please contact Medicare.gov, 1-800-MEDICARE, or your local
> State Health Insurance Program (SHIP) to get information on all of your options."

I did not auto-edit this because it requires **your real carrier-appointment numbers** (the [X] and
[Y]), and the wording changes again for CY2027 marketing (the SHIP sentence is being removed for
materials used on/after October 1, 2026). Give me the two numbers and I will update the disclaimer
site-wide with the exact current-required language, and note the CY2027 variant to swap in this
fall. Verify the final string against the reg and your carrier/FMO guidance before it ships.

---

## Part 9: Prioritized changes (what to actually do)

### High impact / low effort
1. **Render breadcrumbs** on articles and city pages (schema already exists; just draw it).
2. **De-orphan the four county pages** now: footer "Areas we serve" block + a `/kentucky/` hub.
3. **Contrast + font-size hygiene pass:** nudge the utility strip line and review-card text to
   16px, verify `--mute`/`--faint` against 4.5:1, adjust tokens as needed.
4. **Defer the Meta Pixel and GA4** so third-party tags stop being the one perf drag.
5. **Add visible "Reviewed [Month Year]" dates** to articles.
6. **Fix the footer disclaimer** (needs your org/plan counts).

### High impact / higher effort (the scale work)
7. **Build the seven category hub pages** (`/articles/basics/`, `/costs/`, etc.) as real
   pillar pages; keep the filtered "all guides" index as-is. This is the core scale unlock.
8. **Add the `/kentucky/` local pillar** and the Lexington/Fayette flagship page; wire the nav to
   include a Kentucky entry.
9. **Restructure the nav** into the grouped model so it can hold the growing local + tools + events
   sections.
10. **Author page** for Austin at `/about/austin-tyler/`, linked from every byline.
11. **Reviews page** at `/reviews/`.
12. **County-guide system** rolled out slowly, each majority-unique (see Part 4).

### Do not bother
- Chasing a CWV score for a ranking jump (do it for conversion, and you already pass).
- Any design-token tooling, framework, or build step.
- Adding pages you cannot make genuinely locally unique.
- Believing any "X% of ranking" or "Nx more citations" stat without a primary source.

### The one piece of near-free research worth doing
Tree-test the proposed navigation with three or four actual seniors before building it. It is the
cheapest way to confirm the IA works for the people it is for, and it is the one thing analytics
cannot tell you.

---

*Sources: Nielsen Norman Group (UX Design for Seniors 3rd ed.; Mega Menus Work Well; Card Sorting
vs. Tree Testing); W3C WAI (WCAG 2.2 Recommendation, Oct 5 2023; WCAG 3.0 Working Draft, Mar 3
2026); Google Search Central (Core Web Vitals, INP replaced FID Mar 12 2024; mobile-first indexing
complete Jul 5 2024; page-experience FAQ; doorway and scaled-content-abuse policies); John Mueller
statements on page experience; Pew Research (Americans' Use of Mobile Technology and Home Broadband,
Jan 31 2024); Xu et al., Frontiers in Psychology 2022 (font size for older adults); 2024 Google
Content Warehouse API leak via SparkToro (NavBoost); Stanford Web Credibility Project / B.J. Fogg;
Google E-E-A-T / Search Quality Rater Guidelines. Vendor/practitioner statistics without primary
methodology were excluded or explicitly flagged as unverified.*
