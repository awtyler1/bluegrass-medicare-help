# Phase 0 — Inventory and Baseline

**Site:** bluegrassmedicarehelp.com
**Audit date:** 2026-08-12
**Method:** Static analysis of the full repository at commit `ab76921`. Every page parsed with
Python's `html.parser` (not regex) for title, meta, canonical, headings, link graph, JSON-LD, images
and word counts. The link graph was walked breadth-first from `/` to derive click depth.

Evidence classes used throughout: **[V] Verified** (measured in this repo or a cited source),
**[I] Inferred** (reasoned from verified evidence), **[T] Requires tool access** (cannot be
established without Search Console, a live crawl, CrUX, or Google Business Profile).

---

## 0.1 Scale of the property

| Metric | Count |
|---|---|
| HTML files in repo | 105 |
| `/mockups/` prototypes (excluded from all analysis below) | 17 |
| Public pages | 88 |
| **Indexable pages** (`robots` lacks `noindex`) | **62** |
| `noindex` pages (paid landing pages, thank-you pages, `/certifications/`) | 26 |
| Articles listed on the Learning Center hub | 37 |
| Learning Center category pages | 6 |
| City pages | 5 |
| `sitemap.xml` entries | 62 |

**[V] The sitemap is exactly correct.** All 62 indexable URLs appear in `sitemap.xml`; zero
`noindex` URLs appear in it; zero sitemap entries point at a page that does not exist. This is
unusual and worth saying plainly: most sites of this size fail this check. It is not a problem.

---

## 0.2 The seed finding: canonical / host conflict

**[V] Repo-side half, confirmed.** Every one of the 72 pages that carries a `<link rel="canonical">`
points at the **apex** domain `https://bluegrassmedicarehelp.com/…`. Zero pages canonicalize to
`www.`. The same is true of `og:url` (68 apex, 20 missing). `robots.txt`, `sitemap.xml` and the
IndexNow workflow (`.github/workflows/indexnow.yml`, `HOST: bluegrassmedicarehelp.com`) are all
apex. Internally the site is 100% consistent on apex.

**[T] Live-side half, NOT confirmed.** The egress proxy in this environment blocks
`bluegrassmedicarehelp.com` and `www.bluegrassmedicarehelp.com` (gateway returns 403 to CONNECT),
so the live host resolution and redirect chain could not be tested. The claim "the page resolves at
`www.`" is unverified here.

**[V] A related and separately serious finding: there is no `CNAME` file in the repository, and
there never has been.** `git log --all -- CNAME` returns nothing. For a GitHub Pages site published
from a branch, the custom domain is normally persisted as a `CNAME` file at the repo root; without
it the custom domain lives only in repo settings and is not version-controlled.

**What to do, in order:**

1. Run these three commands from a machine with normal network access and paste the output back:
   ```
   curl -sSIL https://bluegrassmedicarehelp.com/     | grep -Ei '^(HTTP|location)'
   curl -sSIL https://www.bluegrassmedicarehelp.com/ | grep -Ei '^(HTTP|location)'
   curl -sSIL http://bluegrassmedicarehelp.com/      | grep -Ei '^(HTTP|location)'
   ```
2. Check Search Console: are **both** `bluegrassmedicarehelp.com` and
   `www.bluegrassmedicarehelp.com` verified as properties, and does the `www` property show
   impressions? If it does, the split is real and it is Priority 0.
3. Regardless of the outcome, add a `CNAME` file containing the single chosen host so the domain
   configuration is version-controlled.

If the apex is the canonical host (which all repo evidence points to), the only correct end state is
`www` → apex 301, `http` → `https` 301, and one Search Console property as primary.

---

## 0.3 Click depth and internal link graph

**[V] This is the site's strongest technical asset and it needs no work.**

| Depth from `/` | Indexable pages |
|---|---|
| 0 | 1 |
| 1 | 14 |
| 2 | 47 |
| 3+ | 0 |
| Orphaned | 0 |

- **Zero orphaned pages.** Every indexable URL is reachable from the homepage.
- **Zero broken internal links** across 88 pages. Every internal `href` resolves to a real file.
- **Maximum depth is 2.** Nothing is functionally invisible.

The caveat: depth is flattered by shared chrome. The header and footer alone account for the top of
the in-link table (`/` 300, `/articles/` 218, `/about/` 193, `/kentucky/` 173, `/schedule/` 158).
Strip navigation links and the *editorial* in-link distribution is much thinner — 12 articles have
6 or fewer inbound links, and `/articles/medicare-flex-card-truth/` (2,132 words, a high-intent
commercial-adjacent topic) has exactly **one** inbound link in the entire site. That is the real
internal-linking problem, and it is addressed in Phase 1.

Lowest editorial in-link counts:

| In-links | Page | Words |
|---|---|---|
| 1 | `/articles/medicare-flex-card-truth/` | 2,132 |
| 2 | `/articles/medicare-changes-2027-kentucky/` | 1,596 |
| 3 | `/articles/common-medicare-misconceptions/` | 1,912 |
| 3 | `/articles/turning-65-medicare-roadmap/` | 1,092 |
| 3 | `/articles/does-medicare-cover-nursing-homes/` | 1,547 |
| 3 | `/articles/what-is-a-medicare-advisor/` | 1,300 |
| 4 | `/articles/does-medicare-cover-ozempic-wegovy-zepbound/` | 1,892 |
| 4 | `/articles/medicare-irmaa-high-income-surcharge/` | 1,317 |
| 4 | `/articles/medicare-scams-how-to-protect-yourself/` | 1,742 |
| 4 | `/articles/social-security-when-to-claim/` | 1,313 |

---

## 0.4 The single largest YMYL failure: no visible sourcing

**[V] 56 of 62 indexable pages contain zero outbound links to `cms.gov`, `medicare.gov`, `ssa.gov`
or any `.gov` domain.** Across the entire site there are 8 links to cms.gov, 7 to medicare.gov, 1 to
ssa.gov, and 4 to kff.org. Exactly **one** page (`/articles/does-baptist-health-take-medicare-advantage/`)
contains the string "Source:".

The six pages that cite anything at all:

| Page | .gov/KFF citations | Words |
|---|---|---|
| `/articles/medicare-changes-2026-kentucky/` | 5 | 1,448 |
| `/articles/medicare-changes-2027-kentucky/` | 5 | 1,596 |
| `/articles/medicare-supplement-plan-g-vs-plan-n/` | 4 | 1,523 |
| `/articles/is-medicare-advantage-worth-it/` | 3 | 1,520 |
| `/articles/medicare-irmaa-high-income-surcharge/` | 2 | 1,317 |
| `/articles/medicare-flex-card-truth/` | 1 | 2,132 |

Everything else — including `/articles/medicare-costs-2026/` (which asserts a $202.90 Part B
premium and a $283 deductible), `/articles/medicare-late-enrollment-penalties/` (2,228 words of
penalty math), and `/articles/help-paying-for-medicare/` (Extra Help income limits) — states
specific dollar figures and federal rules with **no citation of any kind**.

This is the highest-leverage finding in Phase 0. It hurts on three independent axes at once:

1. **Quality raters** assess YMYL pages partly on whether claims are supported and verifiable.
2. **AI retrieval systems** disproportionately surface passages that carry a checkable provenance
   chain; an uncited number is a number a retrieval pipeline has no reason to trust over CMS's own.
3. **Real accuracy risk.** With no source link recorded next to each figure, there is no mechanical
   way to re-verify 37 articles when CMS publishes next year's numbers. The annual update becomes
   guesswork.

**[V] Related:** there is no visible "last updated" or "last reviewed" stamp anywhere on the site.
`dateModified` exists in JSON-LD on all 37 articles, but the human-readable byline reads
`Austin Tyler · Local Kentucky Medicare agent · June 9, 2026 · 6 min read` — a publish date, not a
review date, and not labelled as either.

---

## 0.5 CMS / TPMO compliance — inconsistent disclaimers

**[V] The disclaimer is not one string. It is nine.** Counting distinct variants of the
"We do not offer every plan available in your area" sentence across the 88 public pages:

| Occurrences | Variant |
|---|---|
| 93 | …Currently we represent **6 organizations which offer 158 products** in your area. Please contact Medicare.gov, 1‑800‑MEDICARE, or your local SHIP… |
| 12 | …Currently we **serve Kentucky residents.** *(no count at all)* |
| 7 | …6 organizations / 158 products… **This is a solicitation for insurance.** |
| 6 | …For complete details on all your options, contact Medicare.gov or 1‑800‑MEDICARE. *(no count)* |
| 5 | …For complete details, contact Medicare.gov or 1‑800‑MEDICARE. *(no count)* |
| 2 | …Currently we serve Kentucky residents. Please contact Medicare.gov or 1‑800‑MEDICARE… *(no count)* |
| 1 each (3 variants) | "To review all of your options" / "To compare all of your options" / "Any information we provide is limited to the plans we do offer…" *(no count)* |

There are also **17 distinct** phrasings of the government-disclosure sentence, splitting mainly on
"the United States government" (79) vs "the U.S. government" (13+), with two variants that add the
Social Security Administration.

**Why this matters.** CMS's TPMO disclaimer, where a TPMO does not offer every plan in the service
area, requires the count of organizations and products to be stated: *"We do not offer every plan
available in your area. Currently we represent [number] organizations which offer [number] products
in your area."* ([PSM Brokerage — TPMO disclaimer requirements](https://www.psmbrokerage.com/blog/tpmo-disclaimer-requirements-for-insurance-agents-cms-rules-marketing-examples-compliance-guide),
[Action Benefits — Stay compliant with the TPMO disclaimer](https://blog.actionbenefits.com/stay-compliant-with-medicares-tpmo-disclaimer))

**Correction issued during remediation (2026-08-12).** On closer inspection the severity above is
overstated, and the shape of the problem is different. **Every public page already carried the full,
correct disclaimer in its `<footer class="foot">` legal block.** The 27 "incomplete" instances were
*additional in-body* disclaimers (`.disclaim` on articles, `.fineprint` / `.rfine` / `.fine` /
`.tyfine` on landing pages) that stated a *different, shorter* version on the same page as the
correct one. So this was a **self-contradiction problem, not a missing-disclaimer problem** — a page
would say "we represent 6 organizations which offer 158 products" in the footer and "Currently we
serve Kentucky residents" in the body. Still worth fixing, and now fixed, but it was not the
exposure the first pass implied.

The one genuine gap: **`/quiz-65/` had no TPMO disclaimer at all.** Its `.foot` block carried only
the government-disclosure sentence. That page is indexable. Fixed.

Two forward-looking notes, both **[T] verify against the final rule text before acting**:
- CMS has relaxed the "first minute of the call" timing requirement to "before benefits are
  discussed." That is a call-script change, not a website change — no site action.
- For **2027**, the SHIP reference may be removable from the disclaimer. Do **not** remove it now;
  the 2026 plan year language should stay intact through the 2026 AEP.

**Recommendation (detail in Phase 1):** collapse to exactly one disclaimer string, rendered from a
single source, so the counts can never drift. Never shrink it, hide it, or put it behind an
accordion — the fix is typographic, not structural.

**[T] Open compliance question for Austin:** are "6 organizations / 158 products" still accurate for
the 2026 plan year in the Central Kentucky service area? These numbers change with contracting. If
they are stale, the compliant 93 pages are wrong in a different way than the 27 incomplete ones.

---

## 0.6 Title tags and meta descriptions

**[V] 54 of 62 indexable pages have a title tag over 60 characters.** Eleven exceed 90. The longest
is 117 characters. Every article ends with the 26-character suffix `| Bluegrass Medicare Help`,
which is consuming roughly a third of the available pixel width on every single article.

Worst offenders:

| Chars | Page |
|---|---|
| 117 | `/articles/free-medicare-help-lexington-ky/` |
| 112 | `/articles/does-baptist-health-take-medicare-advantage/` |
| 109 | `/articles/medicare-late-enrollment-penalties/` |
| 108 | `/articles/local-broker-vs-captive-agent-vs-call-center/` |
| 106 | `/articles/does-medicare-cover-ozempic-wegovy-zepbound/` |
| 102 | `/articles/help-paying-for-medicare/` |
| 101 | `/articles/medicare-advantage-central-kentucky-counties/` |
| 101 | `/articles/medicare-advantage-plan-ending-kentucky/` |

**[V] 38 of 62 indexable pages have a meta description over 165 characters.** The longest is 343
(`/articles/medicare-advantage-plan-ending-kentucky/`), followed by 289, 284, 280, 276 and 269 —
all Kentucky-specific pages, i.e. the site's most differentiated content is the most truncated.

Full per-page numbers are in `phase-0-tables.md`.

*Correction to an earlier pass: an initial regex-based extraction reported several descriptions as
4–23 characters. That was a parser artifact (the regex terminated on apostrophes inside
double-quoted attributes). Re-parsed with `html.parser`, no meta description on the site is
truncated. The over-length problem is real; the under-length problem was not.*

---

## 0.7 Structural defects on specific pages

**[V]**

| Page | Defect |
|---|---|
| `/help/` | ~~15-word stub that should not exist.~~ **Corrected:** this is a deliberate client-side redirect shim to `/review/` that preserves the query string (`window.location.replace('/review/' + window.location.search)`), with a `meta refresh` fallback, `noindex`, and a cross-canonical to the target. That is a sound pattern on GitHub Pages, which has no server-side 301s. It is working as designed and should stay. The only real gap was that it rendered a marketing link with no TPMO disclaimer if JS was off — fixed. |
| `/about/` | **Zero `<h1>` elements.** The page opens on an `<h2>`. This is the page that carries Austin's `Person` entity, his NPN, and his credibility — and it has no top-level heading. |
| `/supp-advantage/` | Two `<h1>`s, the second one empty. |
| `/quiz-65/` | Two `<h1>`s (the second is the quiz result heading "Your score"). |
| `/404.html` | No Meta Pixel, no GA4, no canonical. |
| 16 pages | No `<link rel="canonical">` at all: `/404.html`, `/certifications/`, and all 14 thank-you pages. |
| 20 pages | Do not load `/assets/site.css` — every paid landing page and its thank-you page. They are visually and structurally detached from the site. |

**[V] Five paid landing pages are ~284 KB of HTML each** (`/keep-your-doctor/`, `/medicare-window/`,
`/free-advisor/`, `/medicare-mail/`, `/two-lists/`), because each embeds two base64 `data:image`
payloads directly in the markup. They are `noindex`, so this is not an SEO problem — it is a
conversion problem, since paid traffic lands there and 284 KB of blocking HTML on a rural Kentucky
LTE connection is a measurable bounce driver. Flagged for Phase 7.

---

## 0.8 Structured data baseline

**[V] Coverage is better than typical, with three specific holes.**

Present and healthy: `BreadcrumbList` on 61 of 62 indexable pages (only `/` lacks one, correctly),
`BlogPosting` on all 37 articles, `FAQPage` on 42 pages, `CollectionPage` on the 6 category pages
plus hubs, `InsuranceAgency`+`LocalBusiness` on `/`. **Zero JSON-LD parse failures across 105 files.**

Holes:

1. **The `Person` entity is a dangling reference on 37 of 39 pages.** All 37 articles set
   `author.@id = https://bluegrassmedicarehelp.com/#austin-tyler` but supply only
   `{@type, @id, name, url}`. The rich definition — `jobTitle`, `knowsAbout`, `sameAs`, `alumniOf`,
   and the NPN as a `PropertyValue` identifier — exists on **`/about/` only**. `/schedule/` has a
   partial. A crawler that fetches an article and does not also fetch `/about/` sees an author with
   no credentials at all. The NPN, the strongest single trust token on the site, appears on exactly
   one page.
2. **`hasCredential` is absent everywhere.** The NPN is modelled as `identifier`, which is
   defensible, but there is no `EducationalOccupationalCredential` and no Kentucky DOI license
   number anywhere on the site, in schema or in visible text.
3. **`areaServed` on the homepage `LocalBusiness` is a single `{"@type":"State","name":"Kentucky"}`.**
   For a business whose entire structural advantage is that Medicare is priced county by county,
   this throws away the county enumeration. There are 5 city pages and a county hub and none of it
   is reflected in the business entity.

**[V] Also flag:** the homepage `LocalBusiness` embeds six first-party `Review` nodes and an
`AggregateRating` of 5.0/6. Self-serving review markup on a `LocalBusiness` — reviews the business
collects and publishes about itself — is outside what Google's structured data policy will render,
and carries a small manual-action risk. The reviews themselves are genuine and should stay on the
page as visible content; the question is only whether they should be marked up. Addressed in
Phase 1.

**[V] Video:** `VideoObject` appears on `/videos/` and 4 articles. `/videos/` embeds 4 YouTube
videos, is 387 words, has zero transcripts and zero `<h3>` structure. Captions unverifiable from
the repo **[T]**.

---

## 0.9 Topic cluster map

**[V] The hub's own accounting is correct.** All 7 topic-card counts on `/articles/index.html`
match the actual `data-cat` membership exactly (basics 14, turning65 5, coverage 12, costs 9,
onmedicare 3, ss 1, local 14). 18 of 37 articles carry more than one category. The topic cards are
real `<a>` links to real static category pages, not JS-only filters — good for crawlability.

**Cluster shape:**

| Cluster | Pillar | Supporting | Health |
|---|---|---|---|
| **Local / Kentucky** (14) | `/kentucky/` | 5 city pages + 14 tagged articles | **Strongest asset, weakest execution** — see 0.10 |
| **Basics** (14) | `/articles/medicare-basics-parts-a-b-c-d/` | 13 | Overloaded — "basics" is being used as a catch-all, not a topic |
| **Coverage choices** (12) | `/articles/medicare-advantage-vs-medigap/` (1,075 words) | 11, several longer than the pillar | **Pillar is too thin to be the pillar** |
| **Costs** (9) | `/articles/medicare-costs-2026/` (802 words) | 8, several 2×–3× longer | **Pillar is too thin to be the pillar** |
| **Turning 65** (5) | `/turning-65/` (site page) + `/articles/turning-65-medicare-roadmap/` | 5 | Split pillar — two pages competing for the same intent |
| **Already on Medicare** (3) | none | 3 | **Underbuilt.** This is the annual-review / AEP audience, the highest-value repeat-business segment |
| **Social Security** (1) | none | 1 | **Effectively a stub cluster** |

### Cannibalization — the specific checks requested

Measured by Jaccard similarity on title + H1 + slug tokens:

- **`/articles/medicare-changes-2026-kentucky/` vs `/articles/medicare-changes-2027-kentucky/` —
  similarity 1.00.** Identical titles apart from the year ("2026/2027 Medicare Changes Every
  Kentuckian Should Know"). Both indexable, both linked, both current. **[I]** These will compete
  directly. As of August 2026 the 2027 page is the forward-looking one that should own the query
  through AEP; the 2026 page should become the archival record. This needs an explicit decision, not
  drift.
- **Costs cannibalization: confirmed but mild.** `/articles/medicare-costs-2026/` (802 words) vs
  `/articles/costs/` (523-word category page), similarity 0.33. The real problem is that the costs
  *pillar* is the shortest substantive page in its own cluster, while
  `/articles/medicare-late-enrollment-penalties/` (2,228 words) and
  `/articles/medicare-irmaa-high-income-surcharge/` (1,317) sit under it.
- **Enrollment cannibalization: confirmed.**
  `/articles/medicare-enrollment-periods-explained/` (1,005 words) vs
  `/articles/medicare-annual-enrollment-period/` (1,548) vs
  `/articles/turning-65-enrollment-window/` (983). Three pages, three overlapping enrollment-window
  explanations, no clear pillar. Similarity 0.30 on the first pair, but the substantive overlap is
  higher than the token overlap suggests.
- **Advantage vs. Medigap cannibalization: confirmed.**
  `/articles/medicare-advantage-vs-medigap/` (1,075) vs
  `/articles/switching-medicare-advantage-to-medigap/` (1,701) vs
  `/articles/is-medicare-advantage-worth-it/` (1,520) vs
  `/articles/medicare-supplement-plan-g-vs-plan-n/` (1,523). The nominal pillar is the shortest of
  the four.
- **Lexington hospital networks:** `/articles/lexington-hospitals-medicare-advantage-networks/`
  (1,373) vs `/articles/does-baptist-health-take-medicare-advantage/` (1,922), similarity 0.33.
  **[I] This one is fine and should stay split** — the Baptist page targets a specific
  entity+carrier question, which is exactly the long-tail conversational shape AI search rewards.
- **Lexington local:** `/articles/medicare-in-lexington-ky/` (1,541) vs
  `/medicare-lexington-ky/` (869) vs `/articles/free-medicare-help-lexington-ky/` (1,929). Three
  Lexington pages across two directories. **[I] Genuine cannibalization risk.**

### Thin pages

14 indexable pages under 600 words. The category pages (`/articles/social-security/` 237,
`/articles/on-medicare/` 323, `/articles/turning-65/` 411, `/articles/costs/` 523) are legitimate
navigational `CollectionPage`s and should not be judged as articles — but `/articles/social-security/`
listing a single article is a category page that does not deserve to exist yet.

---

## 0.10 County and city pages: templated-thinness risk

**[V] Measured body-text similarity between the five city pages** (`difflib.SequenceMatcher` on
word sequences, chrome included):

|  | Nicholasville | Georgetown | Richmond | Winchester |
|---|---|---|---|---|
| **Lexington** | 39.9% | 38.4% | 46.9% | 39.6% |
| **Nicholasville** | — | 64.7% | 69.3% | 67.1% |
| **Georgetown** | — | — | 69.5% | 72.3% |
| **Richmond** | — | — | — | 71.4% |

Lexington is genuinely differentiated. **The other four are 65–72% identical to one another** and
run 598–701 words each. That is the signature of a template with the town name swapped, which is
precisely the pattern current quality guidance treats as scaled low-value content — and it is
attached to the one topic (county-level plan availability) where this site could be uniquely
authoritative.

**[I]** These four pages are currently a liability, not an asset. They should either be rebuilt with
genuinely county-specific substance (hospital network status, actual plan counts, local SHIP and
senior-center contacts, county demographics) or consolidated into `/kentucky/`. Full spec in Phase 4.

---

## 0.11 Navigation: the 5-vs-12 gap

**[V] Measured from the shared chrome.**

- Header `.nav`: logo + **5 content links** (Turning 65?, Learning Center, Videos, Kentucky, About) +
  Schedule CTA + Call.
- Footer `.fnav`: **12 content links** — the 5 above plus **Home, Glossary, Reviews, Quizzes,
  Free Guide, Free Review**.

Six destinations exist only in the footer. **[I]** Two of those six — `/guide/` (Free Guide) and
`/review/` (Free Review) — are lead-capture pages, i.e. conversion assets demoted below the fold on
every page. `/glossary/` is 2,741 words, the third-largest content asset on the site, and is
header-invisible. Meanwhile `/quizzes/` is 202 words and gets equal footer billing.

This is not a navigation problem to solve by adding six items to the header. It is an
intent-modelling problem, and it is Phase 5's central question.

---

## 0.12 Other verified defects

| Finding | Evidence |
|---|---|
| **413 em dashes in body prose** across 42 pages, in direct violation of `CLAUDE.md`'s standing rule. Worst: `/articles/does-medicare-cover-nursing-homes/` (27), `/articles/medicare-in-lexington-ky/` (25), `/articles/` (22). Em dashes also appear in meta descriptions and in the `/quizzes/` title tag. | **[V]** |
| **220 of 322 `<img>` elements lack `width`/`height`** — direct CLS exposure. | **[V]** |
| **97 of 322 `<img>` elements have no `alt` text** — WCAG 2.2 AA 1.1.1 failure. | **[V]** |
| **Only 11 of 322 images use `loading="lazy"`.** | **[V]** |
| **Two `tel:` formats in use:** `tel:18596186443` (245 instances) and `tel:8596186443` (78, all in the legal footer). Three visible phone renderings: `(859) 618-6443` (249), `859-618-6443` (45). NAP consistency issue. | **[V]** |
| **No `llms.txt`.** `robots.txt` is 6 lines: `User-agent: * / Allow: /`, one `Disallow: /certifications/`, one `Sitemap:`. | **[V]** |
| **AI crawlers are not blocked** — the wildcard `Allow: /` permits `GPTBot`, `OAI-SearchBot`, `ClaudeBot`, `PerplexityBot` and `Google-Extended`. No action needed defensively; opportunity in Phase 3. | **[V]** |
| **All content is server-rendered static HTML.** Word counts above were extracted from raw source with no JS execution. There is no client-side content injection anywhere. This is a real advantage for AI retrieval and it is already correct. | **[V]** |
| **IndexNow is wired up** (`.github/workflows/indexnow.yml`) and correctly skips `noindex` and `/mockups/` pages. Feeds Bing, which grounds ChatGPT Search and Copilot. Already correct. | **[V]** |

---

## 0.13 Gap analysis — questions the site does not answer

Derived from the site's own coverage measured against KY-specific query patterns. Sources consulted:
[Kentucky SHIP via CHFS/DAIL](https://brevy.com/medicare/kentucky/plans-and-coverage),
[medicareresources.org on the birthday rule](https://www.medicareresources.org/medicare-eligibility-and-enrollment/the-birthday-rule-a-gift-to-medigap-enrollees/),
[Boomer Benefits state birthday-rule comparison](https://boomerbenefits.com/which-states-have-a-medigap-birthday-rule/).

**[T] Caveat stated plainly:** I could not run keyword or PAA research. Search volume, difficulty,
and actual PAA text require Search Console, Ahrefs/Semrush, and a live SERP scrape. The gaps below
are derived from coverage analysis and the cited KY-specific sources, **not** from volume data.
Treat them as hypotheses to validate, not as a prioritized keyword list.

Gaps where the site has zero coverage:

| Gap | Why it matters here |
|---|---|
| **Medicaid / dual-eligible and Kentucky MSP (QMB, SLMB, QI)** | `/articles/help-paying-for-medicare/` covers Extra Help but there is no Kentucky Medicare Savings Program page and no state application detail. High-need, high-trust, zero competition from national sites. |
| **UK HealthCare / Saint Joseph (CHI) network status** | The site has a Baptist Health page and a general Lexington hospitals page, but UK HealthCare — the largest system in the region — has no dedicated entity page. |
| **Kentucky Medigap under-65 disability rights** | Mentioned in passing in the birthday-rule article's meta description; no standalone page. Kentucky-specific and almost never covered well. |
| **What happens to my Medicare if I move** (in-county, out-of-state, to a KY nursing facility) | No coverage. Common SHIP question, generates a genuine SEP. |
| **Part B give-back / reduction plans** | Adjacent to the flex-card article; heavily advertised on TV in this market; not addressed. |
| **Veterans: VA benefits + Medicare together** | No coverage. Kentucky has a large rural veteran population. |
| **End-stage renal disease / new-2021 MA eligibility** | No coverage. |
| **Medicare + employer coverage past 65 for a spouse** | `/articles/working-past-65-medicare/` covers the enrollee; nothing on the spouse's position. |
| **"Already on Medicare" cluster generally** | Only 3 articles. This is Austin's retention and referral audience. |
| **Social Security cluster** | 1 article. Filing strategy, WEP/GPO repeal effects on KY public retirees, and the Part B premium deduction from the SS check are all uncovered — and KPPA/TRS retirees are already an established audience here. |

---

## 0.14 What I could not access

| Blocked | Needed to unblock |
|---|---|
| Live host resolution, redirect chains, HTTP headers | Egress proxy blocks the domain. Need the three `curl -sSIL` outputs in §0.2, or a crawl from Screaming Frog / Sitebulb. |
| Core Web Vitals field data (LCP, INP, CLS) | CrUX via PageSpeed Insights on the live URLs, plus Search Console → Core Web Vitals → Mobile. Lab-only Lighthouse is insufficient for this audience. |
| Rankings, impressions, CTR, query data | Search Console export: Performance → Queries + Pages, 16 months, both the apex and `www` properties. |
| Whether `www` is a separately-indexed property | Search Console property list. |
| Keyword volume, difficulty, PAA text, competitor gaps | Ahrefs or Semrush, Keyword Explorer + Site Explorer on the top 3 KY Medicare competitors. |
| Google Business Profile state (categories, photos, Q&A, review velocity, post cadence) | GBP dashboard access, or the profile URL. |
| NAP citation consistency across directories | A citation audit tool (BrightLocal / Whitespark) or manual check of the top 20 sources. |
| Whether the 4 YouTube videos have captions and transcripts | YouTube Studio. |
| Whether "6 organizations / 158 products" is current for 2026 | Austin's carrier contracts. |
| Whether Kentucky DOI license number should be published alongside NPN | Austin's preference + KY DOI guidance. |

---

## 0.15 Prioritized actions from Phase 0

| # | Action | Page/Component | Impact | Effort | Risk | Owner | Timeframe |
|---|---|---|---|---|---|---|---|
| 1 | Resolve host canonicalization: confirm live behavior, set one host, 301 all variants, add version-controlled `CNAME` | Sitewide / DNS / repo root | 5 | 2 | Low | Austin + dev | Week 1 |
| 2 | Consolidate the TPMO disclaimer to one exact string with the org/product count; fix the 27 pages missing the count | Shared `.foot` + 27 pages | 5 | 2 | **Compliance** | Austin (verify counts) + dev | Week 1 |
| 3 | Confirm "6 organizations / 158 products" is current for plan year 2026 | Business fact | 5 | 1 | **Compliance** | Austin | Week 1 |
| 4 | Add visible source citations + "Last reviewed by a licensed agent on [date]" to all 37 articles | Article template | 5 | 4 | Low | Austin + dev | Weeks 2–4 |
| 5 | Promote the full `Person` entity (NPN, credentials, `sameAs`) onto every article instead of a dangling `@id` stub | Article JSON-LD template | 4 | 2 | Low | Dev | Week 1 |
| 6 | Add `<h1>` to `/about/`; fix duplicate `<h1>`s on `/supp-advantage/` and `/quiz-65/` | 3 pages | 4 | 1 | Low | Dev | Week 1 | **DONE** |
| 7 | Rewrite 54 over-length titles and 38 over-length meta descriptions | All indexable pages | 4 | 3 | Low | Dev | Weeks 2–4 |
| 8 | Decide 2026-vs-2027 changes page hierarchy before AEP opens | 2 articles | 4 | 1 | Low | Austin | Week 1 |
| 9 | Rebuild or consolidate the 4 templated city pages | Nicholasville, Georgetown, Richmond, Winchester | 4 | 4 | Medium | Austin + dev | Months 2–3 |
| 10 | Editorial internal-linking pass targeting the 12 articles with ≤6 in-links | Article bodies | 3 | 3 | Low | Dev | Weeks 2–4 |
| 11 | Add `width`/`height` to 220 images; `alt` to 97 | Sitewide | 3 | 2 | Low | Dev | Weeks 2–4 |
| 12 | Strip 413 em dashes from body prose | 42 pages | 2 | 2 | Low | Dev | Weeks 2–4 |
| 13 | Normalize `tel:` to one format and visible phone to one rendering | Sitewide | 2 | 1 | Low | Dev | Week 1 |
| 14 | Add `site.css`, Pixel and GA4 to the 20 detached landing/thank-you pages | 20 pages | 2 | 2 | Low | Dev | Weeks 2–4 |

---

## 0.16 Remediation log

**Week 1 batch applied 2026-08-12** (88 files changed, validated: 0 tag-balance failures,
0 JSON-LD parse failures across all 88 public pages):

| Fix | Result |
|---|---|
| TPMO disclaimer consolidated to one exact string | 9 variants → **1**, across 123 instances |
| Government-disclosure sentence normalized | 17 variants → **1** standard, plus 2 justified Social-Security-specific supersets |
| `/quiz-65/` missing TPMO disclaimer | Full legal footer added |
| `/help/` rendering marketing copy with no disclaimer | Disclaimer added; redirect behaviour untouched |
| `/about/` had zero `<h1>` | Mission statement promoted to `<h1>`; CSS updated so rendering is pixel-identical |
| `/about/` had `BreadcrumbList` schema but no visible breadcrumb | Visible `.crumb` added, matching the house pattern |
| `/supp-advantage/`, `/quiz-65/` had two `<h1>`s | Quiz result heading demoted to `<h2 id="scoreHead">`; CSS selector retargeted so rendering is unchanged |
| `/supp-advantage/` `<h1>` contained `&mdash;` | Replaced with a colon |
| Two `tel:` formats | Normalized to `tel:18596186443` (328 instances) |
| 15 pages missing a canonical | Self-referencing canonicals added (`/404.html` correctly left without one) |

Deliberately **not** changed, pending Austin's input: DNS/`CNAME` and host canonicalization; the
"6 organizations / 158 products" figures themselves.

---

## 0.17 Open questions

1. **Does the live site serve on `www` or apex, and do 301s exist in both directions?** Everything in
   Phase 1 that touches canonicalization depends on this answer.
2. **Are "6 organizations" and "158 products" current for plan year 2026?** If not, 93 pages carry a
   materially inaccurate compliance statement.
3. **Can I have Search Console access (or exports)?** Without it, every ranking, CTR and impression
   claim in later phases is unverifiable, and I will keep labelling them **[T]** rather than
   guessing.
4. **Is there a Google Business Profile, and can I see it?** Phase 4 is largely unwriteable without
   it — GBP drives the map pack, and the map pack is where "Medicare agent near me" is decided.
5. **Should the Kentucky DOI license number be published alongside the NPN?** It is a stronger local
   trust signal than the NPN for a consumer, but it is Austin's call.
6. **What is the intent behind the 11 `noindex` paid landing pages?** Are they all currently running
   traffic, or are some dormant? Five of them are 284 KB. Dormant ones should be deleted, not
   optimized.
7. **Do the four YouTube videos have captions and transcripts?** Required both for WCAG 2.2 AA and
   because YouTube presence correlates strongly with AI-search brand visibility.
8. **Is `/articles/medicare-changes-2026-kentucky/` meant to survive as an archive, or be redirected
   into the 2027 page?** This needs deciding before AEP.
