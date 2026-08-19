# Madison County / Richmond dossier

**Status:** research draft. CMS half verified and dated. Phone-verified facts and the experience
paragraph still needed. Page not yet rebuilt. Pull list at the bottom.

Compiled 19 August 2026.

**Why this county is next.** `/medicare-richmond-ky/` is 621 words and **70.6% identical to
`/medicare-georgetown-ky/`**, the same template failure that got Winchester and Nicholasville
refused. It contains no plan count, no dated fact, and no verified network status. Every sentence
in it could have been written by someone who has never been to Richmond. It survived indexing;
that is not the same as being safe.

---

## 1. CMS plan landscape (Tier 1)

Source: **CMS CY2026 MA and Part D Landscape file**, extract at `data/cms/landscape_CY2026_KY.csv`,
pulled August 2026. General-enrollment plans are `Contract Category Type` in (`MA`, `MA-PD`); SNPs
counted separately.

| Figure | Madison | Confidence |
|---|---|---|
| General-enrollment MA plans | **35** | HIGH |
| Of those, $0 premium | **17** | HIGH |
| Average monthly premium (27 priced plans) | **$14.56** | HIGH |
| SNP plans (separate) | 23 | HIGH |
| MA penetration | **59.52%**, 11,564 of 19,429 eligibles, **47th of 120** | HIGH |

**Carriers (5):** Humana 15, UnitedHealthcare 6, WellCare 5, Anthem 5, Aetna 4.

### The two facts that make this county different

1. **Madison is the only one of our five counties where Devoted Health does not sell.** Devoted
   sells in 87 Kentucky counties, including Fayette, Clark, Jessamine and Scott, and not here.
   Madison has **the fewest plans and the highest average premium** of the five as a result.
   Confidence HIGH, direct from the file.
2. **Madison's local hospital is a Baptist Health hospital, and Baptist's payer table is
   published.** Baptist Health's Medicare Advantage payer status table covers Baptist Health
   hospitals and Baptist Health Medical Group providers **statewide**, which includes Baptist
   Health Richmond. Applied to Madison's plan menu:

   | Carrier | Plans in Madison | Baptist Health status |
   |---|---|---|
   | Humana | 15 | In-network |
   | Anthem | 5 | In-network |
   | Aetna | 4 | In-network |
   | UnitedHealthcare | 6 | **Out since January 2024** |
   | WellCare | 5 | **Out since January 2024** |

   **11 of Madison County's 35 plans, 31 percent of the menu, are out-of-network at the county's
   own hospital.** That is the strongest single finding available for this page and it needs no
   new research, only confirmation (see pull list). Essence is also out at Baptist, but Essence
   does not sell in Madison, so it is irrelevant here and should not be mentioned.

   Note the contrast with Clark County, and it is the opposite shape: in Winchester the local
   hospital takes UnitedHealthcare and WellCare and **Lexington** is where they fail. In Richmond
   the local hospital is the one that fails. Same two carriers, inverted geography. That is a
   genuinely different page, not a reworded one.

## 2. Employer and retiree context (Tier 1, item 6)

- **Eastern Kentucky University** is the county's anchor employer. KY public university retirees
  interact with KPPA / KERS; confirm which system EKU staff fall under before publishing.
  Confidence LOW, needs verification.
- Madison County Schools retirees fall under **TRS Medicare Eligible Health Plan**, which moved
  from UnitedHealthcare to Humana on 1 January 2026. Confidence HIGH (already sourced for the
  Clark page).

## 3. Geography

Richmond sits on I-75 roughly 26 miles south of Lexington. Berea is the county's second town and
is far enough south that the Lexington-versus-local calculation differs there. Worth checking
whether Berea residents use Baptist Health Richmond or drive elsewhere. Confidence LOW.

## 4. Pull list for Austin

1. **Confirm Baptist Health Richmond follows the statewide Baptist payer table.** One call. If it
   does, the 31 percent finding is the page's headline. If Richmond is contracted separately, the
   whole section changes. **Do not publish the table above until this is answered.**
2. **Which carriers does Baptist Health Richmond accept?** Ask for the full list, and ask
   explicitly whether it is complete. (The WellCare correction on the Winchester page came from
   assuming a partial list was exhaustive.)
3. **Madison County experience paragraph**, and it has to pass the one-county test in
   `docs/local-content-standards.md`: swap "Madison" out and the sentence must stop being true.
   The circumstance to draw on is probably the inverted network trap, that the local hospital is
   the one that rejects a third of the plans sold here, which is the reverse of what people
   expect. Not a feeling about Richmond people.
4. **Pharmacy landscape in Richmond and Berea.** Preferred vs standard cost-share on the major
   Part D plans.
5. **EKU retiree coverage**: which state system, and does it change the Medicare conversation.
