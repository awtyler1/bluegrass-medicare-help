# The $90 Medicare Part B payment: research record

Evidence base for `/articles/90-dollar-medicare-payment-kentucky/`. Compiled 8 October 2026.
cms.gov, whitehouse.gov and kff.org could not be fetched directly from the build container, so
every item below is corroborated by at least two independent outlets quoting the CMS FAQ
("Medicare Improvement Fund Premium Rebate Frequently Asked Questions") or the White House
fact sheet. Re-read the CMS FAQ directly before any refresh.

## 1. What it is (confirmed, 3+ sources each)

| Fact | Detail | Sources |
|---|---|---|
| Amount | one-time $90 per eligible person; the President's post said "nearly $100", the fact sheet and CMS say $90 | White House fact sheet, CMS FAQ via AP/PBS, NBC, CNN, KFF |
| Announced | Friday 2 October 2026 | CNN (3 Oct), STAT (4 Oct), Healthcare Dive |
| Official name | Medicare Improvement Fund premium rebate / "Part B premium rebate" | CMS FAQ, Kiplinger, Dallas Morning News |
| Purpose stated by the administration | to help cover the Part B premium, which rose to $202.90 in 2026 | White House fact sheet, CNBC |
| Funding | Medicare Improvement Fund, created by Congress in 2008 (Supplemental Appropriations Act 2008 sec. 7002, Social Security Act sec. 1898), about $2 billion to $2.2 billion, never previously spent; the rebate uses roughly $1.9 billion | AP/PBS, KFF, NewsNation, CBO 2023 via Hoodline |
| Recipients | about 20.8 million (CMS); "more than 20 million" (White House); of about 62.9 million Part B enrollees | CMS via AP, CBS, The Hill, KSN |
| Delivery | direct deposit through the Social Security Administration on or about 8 October; paper check from the U.S. Treasury later in October for people without direct deposit (including people who pay Part B directly); check memo: "Medicare Improvement Fund Payment; $90 Payment to Offset October Premium" | CMS FAQ via Kiplinger, Dallas Morning News, Yahoo, United Medicare Advisors |
| Follow-up | an email or letter from the President in mid-October | CMS FAQ via Kiplinger, Healthcare Dive, Gilman Agency |
| Application | none; nothing to do | CMS FAQ via all outlets |
| Status line | Social Security 1-800-772-1213, from 15 October; eligibility questions 1-800-MEDICARE | CMS FAQ via CBS, KSN, Boston Globe |
| Railroad retirees | RRB handles Part B for railroad families; rrb.gov carries a "$90 Medicare Premium Rebates" notice; RRB line 877-772-5772 | RRB site via search; inference flagged in article |

## 2. Who is eligible and who is not (CMS wording via secondary sources)

Eligible: enrolled in Part B, in Original (fee-for-service) Medicare, living in the United States,
not receiving Medicaid help with the Part B premium, not paying an income-related monthly
adjustment amount (IRMAA).

Not eligible: Medicare Advantage enrollees ("Beneficiaries enrolled in Medicare Advantage are
not eligible"), people whose Part B premium is paid by Medicaid (full duals and Medicare
Savings Program enrollees: QMB, SLMB, QI), IRMAA payers (income above $109,000 single or
$218,000 joint on the 2024 return), people living outside the U.S.

Medigap and standalone Part D do not affect eligibility (still Original Medicare).

Why Advantage is excluded: the 2008 statute limits the fund to "improvements under the original
Medicare fee-for-service program under Parts A and B." The administration cites that clause;
critics note the statute's example is provider-payment adjustment, not beneficiary checks.
No official legal determination has been published; no court challenge found as of 8 Oct.

## 3. Kentucky numbers

| Measure | Figure | Source |
|---|---|---|
| Kentucky Medicare eligibles | 1,012,834 | CMS MA penetration file, August 2026 extract (`data/cms/ma-penetration_202608_KY.csv`) |
| Enrolled in Medicare Advantage (excluded) | 562,671 (55.6%) | same |
| Original Medicare | 450,163 (44.4%) | same |
| Dual-eligible Kentuckians (Medicaid pays Part B) | about 179,000 (89,286 full, 89,869 partial), split between Advantage and Original unknown | KFF 2026 state indicator |
| IRMAA payers | about 7 to 8 percent of Part B enrollees nationally; likely lower in Kentucky | Trustees report via The Finance Buff, Kiplinger |
| Fayette County Original Medicare | 25,516 of 56,114 (MA 54.5%) | CMS extract |
| Clark / Jessamine / Scott / Madison Original Medicare | 3,344 / 5,166 / 4,609 / 7,865 | CMS extract |

**Our estimate** (labeled as such on the page): nationally 20.8 million of roughly 29 million
Original Medicare enrollees qualify, about 72 percent. Applied to Kentucky's 450,163 that is
roughly 320,000 Kentuckians, about one in three people on Medicare in the state. Kentucky's
higher dual-eligible share could push it lower. No state-by-state count had been published by
CMS as of 8 October. Fayette on the same ratio: roughly 18,000.

## 4. The money in context

| | Figure |
|---|---|
| Part B standard premium 2024 / 2025 / 2026 | $174.70 / $185.00 / $202.90 |
| 2026 increase | $17.90 a month, 9.7 percent |
| $90 as a share of one month | 44 percent |
| $90 as a share of a year of premiums ($2,434.80) | 3.7 percent |
| 2027 projection (Trustees) | $209.50, up $6.60 a month, about $79 a year (KFF's framing) |
| Private forecasts for 2027 | $216 to $219 |
| 2020 precedent | $200 drug discount cards announced 24 Sept 2020 for 33 to 39 million people; never sent; abandoned Jan 2021 over funding, legal and logistics problems | CNBC Jan 2021, Axios, KFF |

## 5. Open items (say so on the page)

- Tax treatment: no IRS or CMS guidance found. Commentators treat it as a premium rebate
  (relevant only to itemizers claiming medical expenses).
- Whether it counts as income for SNAP or other programs: no guidance found.
- Eligibility snapshot date: CMS has not said what enrollment date was used. Nothing suggests a
  second run for people who change coverage later.
- Legal authority: disputed; no formal challenge found as of 8 October.

## 6. Refresh checklist

- Mid October: confirm the presidential letter has gone out and what it says; watch for a CMS
  state-by-state count; watch for an IRS note on tax treatment; watch for any court filing.
- November: replace the 2027 Part B projection with the announced figure and recompute the
  "how long until the raise eats the $90" line.
