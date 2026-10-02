# C-SNP research: Central Kentucky, plan year 2027

Evidence base for `/articles/chronic-condition-medicare-advantage-plans-kentucky/`. Compiled
2 October 2026. Two to three independent sources per figure; cms.gov, medicare.gov and ky.gov
are blocked for direct fetch from this environment, so figures come from search-snippet
corroboration and must be re-checked against the primary PDF before any refresh.

## 1. The two 2027 plans (from the Summaries of Benefits Austin supplied)

| | Aetna Medicare Chronic Care (HMO C-SNP) | Anthem Chronic Care Advantage (HMO C-SNP) |
|---|---|---|
| Contract / plan | H0628-044 | H9525-022 |
| Plan year | 1 Jan to 31 Dec 2027 | 1 Jan to 31 Dec 2027 |
| Qualifying conditions | diabetes mellitus, chronic heart failure, and/or cardiovascular disorders, verified by a physician | diabetes mellitus, cardiovascular disorders, and/or chronic heart failure |
| Includes Part D | yes | yes |
| Service area | 18 KY counties: Clark, Fayette, Franklin, Garrard, Jessamine, Laurel, Madison, McCreary, Montgomery, Nicholas, Pulaski, Rockcastle, Russell, Scott, Taylor, Wayne, Whitley, Woodford | statewide list including every Central KY county we cover |
| Type | HMO | HMO |

Neither plan ID appears in the CY2026 landscape extract (`data/cms/landscape_CY2026_KY.csv`),
which confirms both are new for 2027. **Pull the CY2027 landscape file** (guide in
`docs/data-sources.md`) to confirm county availability from CMS rather than from the carrier
document before the September 2027 refresh.

**Compliance line.** Plan names, carriers, plan year, qualifying conditions, service area and
the verification requirement are eligibility facts drawn from the public Summary of Benefits.
The article quotes **no premiums, copays, allowances or supplemental benefits**. Quoting those
is plan-specific marketing content that needs carrier approval. Keep it that way on refresh.

## 2. C-SNPs already sold in our counties in 2026 (CMS CY2026 landscape)

| Plan | Carrier | Conditions | Type | Fayette / Clark / Jessamine / Scott / Madison |
|---|---|---|---|---|
| UHC Complete Care KY-6 (H5253-182) | UnitedHealthcare | diabetes, CHF, cardiovascular | HMO-POS | all five |
| Devoted C-SNP Choice Plus 004 / Premium 006 (H5718) | Devoted | diabetes, CHF, cardiovascular | PPO | Fayette, Clark, Jessamine, Scott, Woodford (not Madison) |
| Humana Gold Plus Chronic Kidney Disease (H5619-170) | Humana | CKD | HMO | all five |
| Anthem Kidney Care (H9525-011) | Anthem | CKD | HMO-POS | all five |

So C-SNPs are not new to Kentucky. What is new for 2027 is Aetna and Anthem each adding a
diabetes / heart plan. **No chronic lung disorder (COPD) C-SNP** appears in the 2026 Kentucky
file, and neither 2027 plan covers it. The article says so explicitly, because COPD is the
condition Kentuckians are most likely to assume qualifies.

## 3. Eligibility rules (corroborated)

- CMS recognizes 15 chronic-condition categories a C-SNP may target. The **cardiovascular
  disorders** group is limited to cardiac arrhythmias, coronary artery disease, peripheral
  vascular disease and chronic venous thromboembolic disorder. Hypertension alone is not in it.
  (CMS SNP FAQ, Medicare Managed Care Manual ch. 16-B, Healthgrades, Milliman.)
- Must have Part A and Part B, live in the service area, and have the condition **verified by
  the treating physician**. Under the CY2025 final rule the plan must contact the applicant's
  physician; verification is due **within 60 days** of the effective date or the member is
  disenrolled at the end of the second month and returned to Original Medicare, with a two-month
  SEP to pick another plan. (Medicare Interactive, Aetna C-SNP FAQ, UHC provider notice,
  Peoples Health provider blog.)
- **SEP:** a person with a qualifying condition can join a C-SNP at any time of year, not only
  in the Annual Enrollment Period. (Medicare Interactive, Aetna FAQ, 24help.)

## 4. Kentucky 65-plus health burden

| Measure | Figure | Source and date |
|---|---|---|
| Diagnosed diabetes, KY adults 65+ | **25.0%** (2023); 27.2% and 27.6% in other recent report years | KY Dept for Public Health 2025 Diabetes Report; KyBRFS 2018 |
| COPD, KY adults 65+ | **19.2%** (2024); 19.4% (2019); 20.2% (2018) | KY DPH COPD prevalence 2024; KyBRFS |
| Coronary heart disease, KY adults 65+ | **13.0% to 15.5%** across recent BRFSS years | KyBRFS 2017 and later |
| KY adult diabetes (all ages) | 13.7% (2023) | America's Health Rankings |
| KY adult COPD (all ages) | 11.0%, **ranked 48th of 50** | America's Health Rankings 2025 |
| KY in the 2025 Senior Report | **46th overall, 49th in health outcomes** | America's Health Rankings 2025 Senior Report |
| Medicare FFS beneficiaries nationally | diabetes about 28%, heart failure 16%, CKD 15%, COPD 12%; **68% have two or more chronic conditions** | CMS Chronic Conditions chartbook; Springer HQLO |
| Fayette County | 56,114 Medicare-eligible; 30,598 on Medicare Advantage (54.53%) | CMS MA penetration, August 2026 extract |

Use ranges and name the year. The "about one in four" framing for diabetes at 65+ is
supported by three report years (25.0, 27.2, 27.6). Do not present county-level diabetes
figures; the only county figure found (U.S. News, Fayette 10.2% all ages) is a different
denominator and was single-source.

## 5. Austin's observation, as given

"Many people would hear chronic condition and not think that's them; in reality they could
qualify." Used as the spine of the piece. The targeting rationale (largest MAPD enrollment by
carrier) stays internal and is not referenced on the page.

## 6. Refresh checklist

- September 2027: CY2028 landscape file, re-verify both plans still exist and their counties.
- Re-check the 60-day verification rule against the current CMS enrollment guidance.
- Re-pull KY DPH diabetes and COPD reports for the newest 65+ figures.
