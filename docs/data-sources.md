# CMS data sources: what to pull, where it lives, what it answers

The county pages in `docs/dossiers/` are built on public CMS files. This is the pull list.

**Caveat on the links:** these URLs came from web research in an environment where direct page
fetching was blocked, so they are unverified. CMS reorganizes its site periodically. **If a URL
404s, use the click path instead**, which is stable even when slugs change.

Drop downloaded files in `data/cms/`. See that folder's README for naming and the size warning.

---

## The fastest path if you only do one thing

**Medicare.gov Plan Finder**, https://www.medicare.gov/plan-compare/

Enter ZIP **40391** (Winchester) or **40356** (Nicholasville), choose the county when prompted,
and it will show the count of Medicare Advantage plans and Part D plans available. This takes
two minutes and resolves the single most important missing number on both county pages.

It is not a downloadable dataset, so it will not let you diff year over year or compute market
share. For that you need the files below. But it settles "how many plans in this county" today.

---

## 1. CY2026 MA and Part D Landscape file (the money file)

**What it answers:** every MA and Part D plan available in each county, with premium, plan type
and SNP type. Confirms Clark County's 39 plans, gets Jessamine's missing count, resolves the
$0-premium conflict, and confirms or corrects the "47 plans in Fayette" figure the site repeats
in eight places.

**The important trick:** keep each year's extract and diff consecutive years by county. That
tells you *exactly which plans left Clark and Jessamine*, which is the single most useful thing
you can tell someone in October. The CY2026 Kentucky extract is already in `data/cms/`, so
pulling CY2027 in late September completes the pair. There is no need to go back for CY2025:
that diff looks backward at a plan year that is nearly over.

**These files are large.** Run any download through `docs/filter-cms-file.py` to cut it to
Kentucky before moving it anywhere.

- Released 26 September 2025 for CY2026. **CY2027 expected late September 2026**, roughly five
  weeks out.
- Click path: cms.gov, then search **"Medicare Advantage and Part D landscape"**, or navigate
  Data & Research, then Medicare Advantage / Part D.
- Filter to State = KY, County = Clark, Jessamine, Fayette, Scott, Madison, Woodford, Bourbon.

## 2. MA State/County Penetration (monthly)

**What it answers:** the percentage of each county's Medicare beneficiaries who are on Medicare
Advantage. Resolves the Clark County enrollment conflict (2,987 vs 5,249). Statewide Kentucky is
reported around 55% against a national ~51%, but the county figure is the one worth publishing.

- URL as found: https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data/ma-state/county-penetration
- Click path: cms.gov, Data & Research, Statistics Trends and Reports, **Medicare Advantage/Part
  D Contract and Enrollment Data**, then **MA State/County Penetration**.
- Files are named like `MA State County Penetration 2026 08`. **Download the Abridged version**,
  which drops counties with fewer than 11 enrollees.
- Updated monthly. Pull the latest month each September.

## 3. Monthly Enrollment by Contract/Plan/State/County

**What it answers:** carrier market share within a county. Which carrier actually has the most
Clark County members. This is the "about X% of Clark County beneficiaries are on Medicare
Advantage, and carrier Y has the largest share" statistic, which is public and almost nobody
surfaces at county level.

- URL as found: https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data/monthly-enrollment-contract/plan/state/county
- Click path: same CMS section as file 2.
- **You have to join contract H-numbers to parent organizations yourself.** The companion
  "Monthly Enrollment by Contract/Plan/State/County" and the contract-level files carry the
  organization name. H5619 is Humana, for example.
- **This is the largest file of the set.** See the size warning below.

## 4. Medicare Monthly Enrollment (data.cms.gov)

**What it answers:** clean county totals split Original Medicare vs Medicare Advantage, and PDP
vs MA-PD. Good for a simple chart and easier to work with than file 3.

- https://data.cms.gov/summary-statistics-on-beneficiary-enrollment/medicare-and-medicaid-reports/medicare-monthly-enrollment
- Has a browser preview and filtering, so you may not need to download it at all.

## 5. KFF State Health Facts (cross-check only)

**What it answers:** state-level MA penetration, useful as a sanity check against file 2.

- https://www.kff.org/medicare/state-indicator/enrollees-as-a-of-total-medicare-population-by-plan-type/

---

## Non-CMS primary sources worth keeping

These are the citable sources for facts already on the site:

| Fact | Source |
|---|---|
| TRS MEHP moved from UnitedHealthcare to Humana, 1 Jan 2026 | `trs.ky.gov` MEHP 2026 Update PDF |
| KPPA 2026 options and the $199.94 contribution basis | `kyret.ky.gov`, Medicare Plan Year 2026 page |
| Baptist Health MA network status | baptisthealth.com, Billing, Medicare Advantage. They publish a payer status table PDF. **Screenshot and date it**, since it changes without notice |
| UK HealthCare in-network plans | ukhealthcare.uky.edu, Payment and Insurance, In-Network Insurance Plans |
| CHI Saint Joseph accepted insurance | chisaintjosephhealth.org, Patients and Guests, Health Insurance Options |
| Kentucky SHIP | chfs.ky.gov, DAIL, SHIP. Statewide line 877-293-7447 |
| Bluegrass Area Agency on Aging | bgaaail.org. ADRC 859-266-1116, intake 866-665-7921 |

---

## The annual refresh, September

Every September, before AEP opens on 15 October:

1. Pull the **new landscape file** (CY2027 expected late September 2026) and diff it against
   CY2026 by county.
2. Pull the latest **penetration** and **enrollment** files.
3. Update every county page's plan counts and the "what changed this year" section, and move the
   review stamp forward.
4. Re-verify the hospital network table by phone. Carrier and hospital contracts change in the
   autumn, which is exactly when readers care.
5. Re-check the Baptist, UK HealthCare and CHI Saint Joseph network pages and re-date them.

Being first with accurate new-year county numbers is a durable citation advantage. National
sites publish state-level figures in October; almost none publish county-level.

---

## Size warning before you commit anything

The monthly enrollment files are large, in the hundreds of megabytes uncompressed, because they
carry every contract, plan and county in the United States. **Do not commit the raw downloads.**

`data/cms/.gitignore` excludes raw archives. The workflow is:

1. Download the raw file anywhere on your machine.
2. Filter to Kentucky, or to the counties we cover.
3. Save the filtered extract into `data/cms/` with the naming convention in that folder's README.
4. Commit only the extract.

If a filtered Kentucky extract is still large, keep it as CSV rather than XLSX and it will
compress well in git.
