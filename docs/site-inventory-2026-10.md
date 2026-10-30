# Site inventory and keep, merge, cut plan (30 October 2026)

95 pages. No traffic data was available in this session (GA4 and Search Console are not
connected), so decisions rest on overlap measurements, internal links, freshness and purpose.
Check GA4 landing-page sessions for the last 90 days before retiring anything with search value.

Overlap = share of distinctive vocabulary (words over five letters) the smaller page shares with
the larger. Above about 45 percent the two pages are answering the same question.

## 1. Restyle (done on this branch, not yet live)

Every page now uses the homepage design: white pages, navy text, the accessible coral
(#cf461e, white text 4.6:1), cool light panels, Figtree headings, no handwriting font, pill
buttons, and no Fraunces or Caveat font downloads. Done by remapping the shared colour and font
tokens each page defines (`docs/restyle-pages-v3.py`); page structure is unchanged.
All 95 pages tag-balanced, 74 JSON-LD blocks parse, pixel and GA4 present on every live page.

## 2. Keep as is (restyled)

| Group | Pages |
|---|---|
| Core | `/`, `/about/`, `/reviews/`, `/review/`, `/schedule/`, `/guide/`, `/turning-65/` |
| Learning Center | `/articles/` and topic hubs basics, coverage, costs, on-medicare, turning-65 |
| Tools | `/medicare-enrollment-calculator/`, `/glossary/`, `/quizzes/`, `/quiz-65/`, `/supp-advantage/`, `/videos/` |
| Local | `/kentucky/` and the five county pages |
| Articles | 33 of 41 (everything not listed in section 3) |
| Plumbing | `/certifications/` (internal, noindex); redirect shims `/help/`, `/articles/medicare-in-lexington-ky/`; thank-you pages for live landers |

## 3. Merge (fold the weaker page into the stronger, 301 the old URL)

| Retire | Into | Overlap | Why |
|---|---|---|---|
| lexington-hospitals-medicare-advantage-networks | does-baptist-health-take-medicare-advantage | 49% | Baptist article already has the three-system network table |
| annual-medicare-review-aep | medicare-annual-enrollment-period | 68% | Same season, same reader; the checklist becomes a section |
| medicare-changes-2026-kentucky | medicare-changes-2027-kentucky | 57% | 2026 is ending; the 2027 piece supersedes it |
| turning-65-medicare-roadmap | `/articles/turning-65/` hub | 44% vs window | The hub becomes the roadmap; one front door for turning 65 |
| free-medicare-help-lexington-ky | `/medicare-lexington-ky/` | 34% | Same intent ("free help in Lexington"); resources become a section |
| local-broker-vs-captive-agent-vs-call-center | what-is-a-medicare-advisor | 35% | Same question: who should help me, and how they are paid |
| medicare-advantage-central-kentucky-counties | `/kentucky/` | 43% | County plan counts belong on the county guide |
| `/articles/social-security/` topic hub | `/articles/turning-65/` hub | n/a | A topic page with one article; the article moves under Turning 65 |

Result: 41 articles become 34, the Learning Center loses one thin topic, and the turning-65 and
Lexington paths each get a single front door. Each merge keeps the best material from both pages,
updates internal links, the Learning Center rows and counts, and the sitemap, and adds a 301.

Not merged on purpose: medicare-enrollment-periods-explained (the umbrella page for every
window), what-medicare-does-not-cover (a high-volume search question in its own right),
common-medicare-misconceptions, and the dental, five-terms and costs articles.

## 4. Update, not cut

- `medicare-costs-2026` and `medicare-irmaa-high-income-surcharge`: refresh to 2027 figures when
  CMS announces the Part B premium in November; move to year-neutral URLs with 301s.
- `medicare-annual-enrollment-period` title still says 2026.

## 5. Paid landing pages (Austin to decide)

Ten ad landers, each with a thank-you page, all noindex and all wired to the lead webhook. Which
ones are running ads cannot be seen from the code.

| Lander | Created | Notes |
|---|---|---|
| free-advisor, keep-your-doctor, medicare-mail, medicare-window, two-lists | Jul 2026, edited Sept | Current generation |
| find-your-plan | Sept 2026 | Newest; GoHighLevel mapping |
| done-for-you | Jul 2026 | Last edited Aug |
| keep-your-doctors, local-medicare-help, talk-to-austin | Jul 2026, untouched since Aug | Older, simpler; keep-your-doctors is the losing half of an A/B test per the authority strategy doc |

Recommendation: retire any lander with no ad spend in the last 60 days (with its thank-you page),
redirecting each to `/review/` so old ad links still land somewhere useful.

## 6. Outcome (30 October 2026, approved by Austin)

- All eight merges done. Sections and questions moved: emergencies and Lexington hospitals into the
  Baptist article; ANOC, 4-point check and Advantage Open Enrollment into the AEP article (duplicate
  ANOC video dropped); the side-by-side table, three questions and a new visible FAQ into the advisor
  article; the full free-help directory with phone numbers into the Lexington page; the county
  comparison steps and three questions into the Kentucky page; the six-step roadmap onto the
  Turning 65 topic page, which also takes the Social Security article. 2026 changes redirects to 2027.
- All ten paid landing pages and their thank-you pages removed (Austin is not running them), plus
  the photo only they used. Each address redirects to `/review/`. Three article buttons that pointed
  at `/talk-to-austin/` now point at `/review/`.
- 58 permanent redirects in `vercel.json`. Pages: 95 to 67. Articles: 41 to 34. Sitemap: 59 URLs.
- Topic pages are now generated from the Learning Center (`docs/build-hubs.py`).
- `/schedule/` now embeds the Tyler Insurance Group booking calendar
  (link.tylerinsurancegroup.com group widget) in place of Calendly.
