# Medicare enrollment calculator: rules and design spec

Page: `/medicare-enrollment-calculator/` · Engine: `assets/iep-engine.js` · Tests: 48 cases (Node)
Built 16 September 2026. Rules verified by source corroboration (two to three independent sources
per rule; cms.gov, medicare.gov and ssa.gov are blocked for direct fetch from this environment).

## 1. Why it is three questions, not one

A date-of-birth-only calculator gives a **wrong answer** to a large share of people turning 65:

| Who | What a DOB-only tool tells them | What is actually true |
|---|---|---|
| Still working, 20+ employees, group coverage | "Sign up for Part B by [date]" | They can delay Part B with no penalty and no reason to pay $202.90 a month |
| Contributing to an HSA | "Sign up for Part A now, it is free" | Part A ends HSA eligibility and backdates up to 6 months; stopping too late costs a 6% excise tax |
| Already drawing Social Security | "Here is how to sign up" | They will be enrolled automatically; the real question is whether to decline Part B |
| Under 65 on disability | 65th-birthday dates | Medicare starts month 25 of SSDI; the 65th birthday brings a second window |
| Born on the 1st | Standard 7-month window | The whole window shifts one month earlier |

So the tool asks: **date of birth**, **are you already getting Social Security or Railroad
Retirement benefits** (no / retirement / disability / not sure), and **will you or your spouse still
be working at 65 with health insurance from that job** (no / yes / not sure), with two follow-ups
only if working: **20 or more employees?** and **contributing to an HSA?**

Every answer changes the result, not just the dates.

## 2. The rules the engine encodes

| Rule | Encoding | Sources |
|---|---|---|
| Entitlement begins the 1st of the month you turn 65 | `elig = {dob.y+65, dob.m}` | Medicare.gov, SSA, KFF |
| **Born on the 1st: entitlement begins the month before** | `if dob.d === 1: elig -= 1 month` | UHC, AARP, Wellcare, eHealth (example: Dec 1 birthday, IEP Aug 1 to last day of Feb) |
| IEP = 3 months before elig month through 3 months after | `iep = [elig-3, elig+3]` | Medicare.gov, SSA |
| Coverage start (rules since 1 Jan 2023, CAA 2021 / BENES Act) | before elig month: 1st of elig month; in or after: 1st of month after signing up | KFF, Medicare Rights Center, Federal Register, CNBC |
| "Best by" date | last day of the month before the elig month | derived from the above |
| Medigap Open Enrollment | 6 months from the first month you are 65+ and enrolled in Part B; computed from the on-time Part B start | Medicare.gov, NCOA, Humana |
| Part D IEP | same 7 months; penalty is 1% of the national base premium per full uncovered month, after 63 days without creditable coverage | CMS, NCOA, Aetna |
| Part B late penalty | 10% of the premium per full 12-month period, for life. **Not computed in dollars**: it depends on creditable coverage history the tool cannot know. Flagged only. | CMS, NCOA, Humana |
| General Enrollment Period | Jan 1 to Mar 31; coverage 1st of the month after signing up (since 2023) | KFF, Medicare Rights Center |
| Automatic enrollment | receiving SS or RRB benefits at least 4 months before 65: enrolled in A and B automatically, card about 3 months before coverage starts | Medicare.gov, SSA, AARP |
| Working past 65, SEP | 8 months beginning the month after employment or group coverage ends, whichever is first; coverage begins the month after SSA receives CMS-40B and CMS-L564 | SSA, medicareresources.org, UHC |
| COBRA and retiree coverage | do **not** count as coverage from current employment and do not create or pause an SEP | SSA, medicareresources.org |
| Employer size | fewer than 20 employees: Medicare is primary at 65, enroll in A and B during the IEP | SSA, medicareresources.org |
| HSA | Part A backdates up to 6 months (never before the 65th birthday month); stop contributions 6 months before applying | Fidelity, UHC, medicareresources.org |
| Disability under 65 | Medicare at month 25 of SSDI; IEP is 3 months before through 3 months after month 25; ALS has no waiting period; a fresh IEP and Medigap window arrive at 65 | Medicare Interactive, UHC, NCOA |

## 3. What the engine deliberately does not do

- **No penalty dollar amounts.** The Part B penalty depends on months without creditable coverage,
  which requires employment history the tool does not collect. Guessing here is the single most
  likely way to be wrong. It says a penalty may apply and hands the reader to a human.
- **No disability date math.** Month-25 timing depends on the SSDI entitlement date, which people
  rarely know precisely. The disability route explains the rule and routes to a call.
- **No state-specific Medigap rules.** Kentucky's birthday rule and other state protections are
  linked, not computed.
- **Nothing leaves the browser.** No form post, no analytics event carrying the birth date. The
  page says so in the first sentence, because the audience is rightly suspicious of any page that
  asks for a birth date.

## 4. Design

**The whole rule in one glance.** The result is a 7-tile strip: three tiles before the birthday
month, the birthday month, three after. Each tile shows the coverage-start date if you sign up in
that month. Early tiles are green ("on time"), the birthday tile is highlighted, late tiles are
amber. The rule that takes Medicare.gov three paragraphs to explain becomes a row a 68-year-old
reads in five seconds, and the colors are never the only signal: every tile carries the date in
text.

**Reflect the input back in words.** Under the date fields, a live line says "You turn 65 in
March 2027." Typos in a birth year are the most common input error and this catches them before
the result does.

**One question per screen, progress in words.** "Step 2 of 3", a Back link on every step, focus
moved to the step heading on each change, Enter advances.

**Lead with the answer.** The result opens with one sentence: "Your Medicare window opens
December 1, 2026 and closes June 30, 2027." Everything else is beneath it.

**A status badge relative to today.** "Opens in 3 months", "Open now, 4 months left", or "Closed
on June 30, 2026". The reader should know their situation before reading anything else.

**Actions that respect the audience.** Add to calendar (a .ics with three reminders: opens, last
day for on-time coverage, closes), Print, Email me these dates (a mailto with the dates in the
body; no server), and Call. No account, no download of an app.

**The nudge to call is contextual, not a banner.** Every result ends with a call card, but the
working, disability, under-20, HSA and late paths get a stronger one placed where the wrinkle is,
because that is where a phone call changes the outcome.

## 5. Accessibility (WCAG 2.2 AA target)

- Native controls throughout: `<select>`, `<input inputmode="numeric">`, real radios inside
  label cards, `<fieldset>`/`<legend>` on every question.
- Tap targets 52px or taller. Body text 18px. Focus rings visible on every control.
- Primary buttons use coral-dark (#b3431d) on white for 5:1 contrast rather than the lighter
  brand coral.
- Errors announced with `role="alert"` and tied to the field with `aria-describedby`; written in
  plain words with the fix ("February 1961 only has 28 days").
- Results and the live date echo are `aria-live="polite"`.
- No timeouts, no motion beyond a fade, `prefers-reduced-motion` respected.
- Print stylesheet: the tool chrome disappears and the result prints cleanly.

## 6. Test coverage (`iep-test.js`, 48 assertions)

Standard window and all three coverage-start branches; born-on-the-1st against the published
December 1 and April 1 examples; year-boundary wrap; February 29 birthday; invalid dates (day 30
in February, February 29 in a non-leap year, future year, year 1899); every route (standard, auto,
working with flags, disability under and over 65, late with GEP); GEP boundary in February and
April; and the .ics output.

## 7. Refresh checklist

- **Each November:** confirm the Part B premium figure quoted in the penalty explanation.
- **Each January:** re-run the tests with `today` advanced a year; confirm the GEP text.
- **If CMS changes coverage-start rules again**, `coverageStartIfEnrolled` is the only function
  that has to change.
