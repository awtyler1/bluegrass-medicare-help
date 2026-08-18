# CMS data extracts

Filtered extracts of public CMS files, used to build and refresh the county pages in
`docs/dossiers/`. The pull guide, including links and click paths, is `docs/data-sources.md`.

## Naming convention

```
<dataset>_<planyear-or-YYYYMM>_KY.csv
```

Examples:

```
landscape_CY2026_KY.csv              plan-level, all KY counties
landscape_CY2027_KY.csv              next year, for the diff
ma-penetration_202608_KY.csv         county penetration, August 2026
enrollment-by-contract_202608_KY.csv carrier share by county
```

Keep the previous plan year alongside the new one. The diff between them is what produces
"here is exactly which plans left your county this year," which is the most useful sentence on
a county page in October.

## Rules

- **Filter to Kentucky before committing.** The raw national files run to hundreds of megabytes.
  Raw archives are gitignored.
- **CSV, not XLSX.** It diffs and compresses properly in git.
- **Never edit an extract by hand.** If a number looks wrong, re-pull it. A hand-edited data file
  is indistinguishable from a fabricated one six months later.
- **Record the pull date** in `MANIFEST.md` when you add a file, so every published figure can be
  traced to a dated source.

## Manifest

| File | Dataset | Plan year / month | Pulled | Notes |
|---|---|---|---|---|
| `landscape_CY2026_KY.csv` | MA and Part D Landscape | CY2026, Aug 2026 refresh | 2026-08-18 | 6,789 KY rows from 138,260 national. 24 of 52 columns kept |
| `ma-penetration_202608_KY.csv` | MA State/County Penetration | Aug 2026 | 2026-08-18 | All 120 KY counties |
| `contract-info_202608_KY.csv` | CPSC Contract Info | Aug 2026 | 2026-08-18 | 1,660 rows, 35 KY contracts. Maps contract ID to parent organization |

### Still to pull

- **CY2025 landscape file.** Diffing it against CY2026 names exactly which plans left each county,
  which is the most useful thing a county page can say in October.
- **CPSC Enrollment file** (enrollment by contract/plan/state/county). `contract-info` gives the
  carrier *names*; the enrollment file gives the *member counts* needed for county market share.
- **CY2027 landscape file**, expected late September 2026.

### Reading the landscape file

It ships as `.xlsb` (Excel binary), which needs `pyxlsb`:

```
pip install pyxlsb
```

`Contract Category Type` separates `MA`, `MA-PD`, `SNP` and `PDP`. **Count non-SNP plans (MA plus
MA-PD) for the headline "how many plans in my county" figure**, and report SNPs separately, since
most people cannot join them. That definition reproduces the published third-party counts exactly:
Clark County 39 plans, 20 at $0, $13.32 average.
