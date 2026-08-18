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

Nothing pulled yet. Add a row when you drop a file in.

| File | Dataset | Plan year / month | Pulled | Notes |
|---|---|---|---|---|
