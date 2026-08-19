# Fayette County / Lexington dossier

**Status:** partial. Verified network and CMS data recorded here and shipped to
`/articles/does-baptist-health-take-medicare-advantage/`. A full local page rebuild is **not**
recommended (see "Why we are not rebuilding the city page"). Pull list at the bottom.

Last updated: 19 August 2026.

---

## 1. CMS plan landscape (Tier 1)

Source: **CMS CY2026 Medicare Advantage and Part D Landscape file**, filtered extract at
`data/cms/landscape_CY2026_KY.csv`. Pulled August 2026. Counting rule per
`docs/data-sources.md`: general-enrollment plans are `Contract Category Type` in (`MA`, `MA-PD`);
SNPs are counted separately because most people cannot join them.

| Figure | Value | Confidence |
|---|---|---|
| General-enrollment MA plans, Fayette | **40** | HIGH, direct from file |
| Of those, $0 monthly premium | **21** | HIGH |
| Average monthly premium (the 32 plans carrying a Part D premium) | **$12.90** | HIGH |
| Highest premium | $97.00 | HIGH |
| Plans with no consolidated Part D premium (MA-only) | 8 | HIGH |
| SNP plans, Fayette (separate count) | **25** | HIGH |

**Carriers selling general-enrollment plans in Fayette (7):**

| Carrier | Plans | Parent organization |
|---|---|---|
| Humana | 16 | Humana Inc. |
| UnitedHealthcare | 6 | UnitedHealth Group, Inc. |
| WellCare | 5 | Centene Corporation |
| Anthem Blue Cross and Blue Shield | 5 | Elevance Health, Inc. |
| Aetna Medicare | 4 | CVS Health Corporation |
| Essence Healthcare | 2 | Lumeris Group Holdings Corporation |
| Devoted Health | 2 | Devoted Health, Inc. |

**SNP-only carriers in Fayette** (cannot be bought during general enrollment): Passport Advantage
(Molina, 1 D-SNP) and Abilis Health (BrightSpring, 2). Humana, UnitedHealthcare, WellCare, Aetna,
Anthem and Devoted also sell SNPs here on top of the counts above.

### Two carrier facts worth keeping straight

- **CareSource sells zero Medicare Advantage plans in any Kentucky county for CY2026.** Verified
  against the full state extract, not just Fayette. UK HealthCare lists "CareSource Advantage
  (Medicare)" as accepted, which is true and simply not purchasable here. Do not present it as an
  option. Confidence HIGH.
- **Passport by Molina's only Fayette plan is a D-SNP.** CHI Saint Joseph accepts Passport, but
  that only helps someone with both Medicare and Medicaid. Confidence HIGH.

## 2. MA penetration (Tier 1)

Source: **CMS MA State/County Penetration**, `data/cms/ma-penetration_202608_KY.csv`.

- Fayette: **54.53% MA penetration**, 30,598 of 56,114 eligibles. **78th of 120 Kentucky counties.**
- The contrast that matters: Fayette has the most plans of the four counties we cover and the
  *lowest* take-up. Clark is 61.72% (38th) on 39 plans. Confidence HIGH.

## 3. Hospital networks (Tier 1)

Three systems: **UK HealthCare** (Chandler, Good Samaritan, Markey), **Baptist Health Lexington**
(plus the Hamburg campus), **CHI Saint Joseph Health** (Saint Joseph Hospital, Saint Joseph East).

| Carrier | Baptist | UK | Saint Joseph |
|---|---|---|---|
| Humana | In | In (Choice PPO, Gold Choice PFFS named) | Accepted |
| UnitedHealthcare | **Out since Jan 2024** | In | Accepted |
| WellCare | **Out since Jan 2024** | In | Accepted |
| Anthem | In | In | Accepted |
| Aetna | In | In | Accepted |
| Devoted Health | not published | not published | Accepted, eff. 1/1/2025 |
| Essence | **Out eff. 1/1/2026** | not published | not published |

Sources and dates: Baptist Health's published payer status table (baptisthealth.com) and UK
HealthCare's in-network insurance plans page (ukhealthcare.uky.edu), both checked July 2026. The
Saint Joseph column is the carrier list Saint Joseph confirms it accepts, supplied August 2026.

**Standing caveat.** Only Baptist publishes explicit out-of-network statuses. UK's and Saint
Joseph's lists are positive lists, and Saint Joseph's own page says its list is not complete.
Absence from either is **unconfirmed, not out**. Every published claim on the site follows that
rule: we assert "in" from a positive list, and we assert "out" only from Baptist's table.

**Open:** neither the UK nor the Saint Joseph list has been confirmed as exhaustive. See pull list.

### What it adds up to
- Humana + Aetna + Anthem = **25 of 40 plans** work at all three systems.
- UnitedHealthcare + WellCare = **11 plans** that work at UK and Saint Joseph and fail at Baptist.
- Devoted + Essence = 4 plans with partial or unconfirmed status.

## 4. Local help infrastructure (Tier 2)

- Kentucky SHIP, statewide, free and non-sales.
- Bluegrass Area Agency on Aging and Independent Living, serves Fayette and surrounding counties.
- CHI Saint Joseph plan-status line: (844) 303-9355.

## 5. Why we are not rebuilding the city page

`/medicare-lexington-ky/` is **indexed and ranking at position 7.0** (17 impressions, 0 clicks,
GSC). Winchester and Nicholasville were rebuilt because Google had crawled and refused them. This
page has no such verdict against it, and it is a service page, not an article: its job is the
office, the free-help offer, and the handoff. The August 2026 change was surgical, replacing
"typically have dozens of Medicare Advantage plans" with the verified 40 / 21 at $0 figure and
sharpening the hospital FAQ.

The Lexington network data went instead to
`/articles/does-baptist-health-take-medicare-advantage/`, which already declared itself the
date-stamped source of truth for all three systems, is linked as such from
`/articles/lexington-hospitals-medicare-advantage-networks/` (position 5.33), and had a hole
exactly where the Saint Joseph list belonged.

**Still unresolved:** `/articles/medicare-in-lexington-ky/` was crawled and refused. It overlaps
15 to 23% with eight of its own siblings and reads as a survey of the site's library with a city
name applied (22 mentions of Lexington against 3 of UK HealthCare in 1,563 words). It carries 12
inbound internal links. The recommendation is a 301 into `/medicare-lexington-ky/` with those
links repointed. Awaiting Austin's decision, since it deletes a page he paid for.

## 6. Austin's pull list

1. **Are the UK HealthCare and CHI Saint Joseph carrier lists exhaustive?** Specifically: does
   either system accept **Devoted Health** or **Essence**? Right now both sit in a "not published"
   column, which is honest but weak. A yes or no on four cells finishes the table.
2. **A Fayette County observation.** Winchester's is distrust in a noisy market. Nicholasville's is
   not knowing local help exists. What is different about Lexington people? This is the experience
   paragraph `docs/local-content-standards.md` requires, and no amount of CMS data substitutes for
   it.
3. **A decision on `/articles/medicare-in-lexington-ky/`**: consolidate via 301, or rewrite it to
   the local content standard.
4. **Confirm the Baptist status for Devoted.** Baptist publishes an explicit table, so a carrier's
   absence from it is more meaningful than absence from the other two. Worth one call.
