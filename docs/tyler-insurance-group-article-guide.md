# Tyler Insurance Group — article cross-post guide

**Standing workflow:** every article we publish on Bluegrass Medicare Help also gets a
**Tyler Insurance Group (TIG) version** — same topic, rewritten for the parent agency and a
national audience. TIG operates in many states, so the TIG version must NOT be Kentucky-specific.

This is the reference for producing that TIG version. Keep it in sync if the brand changes.

---

## 1. Brand colors (from the official TIG logo)

Sampled directly from `TylerInsure_PMS_LOGO.pdf`. These are the TIG brand colors — **not** the
Bluegrass coral/green palette.

| Token | Hex | Use |
|-------|-----|-----|
| **TIG gold** | `#dbcf86` | primary brand color — headings accent, one of the two "choice" colors, key illustration objects |
| **TIG gold-dark** | `#b0a154` | outlines/borders on gold, darker accents |
| **TIG gold-tint** | `#efe8cf` / `#f6f4ea` | light backgrounds, soft fills |
| **TIG gray** | `#7e8082` | secondary brand color — the other "choice" color, neutral objects |
| **TIG gray-dark** | `#5c5e60` | outlines/borders on gray, body-ish accents |
| **White** | `#ffffff` | text on gold or gray blocks (matches the logo: white "TYLER" on gold) |

Notes:
- The logo sets **white text on the gold block** — that white-on-gold treatment is on-brand, so
  reuse it for signage/labels inside illustrations. Prefer white-on-gray for small body-size text
  (better contrast).
- Fonts stay the same as Bluegrass: **Fraunces** (serif headings) + **Source Sans 3** (sans body).

## 2. Voice & content rules

- **Agency voice, not first-person.** Use "we / our team / our licensed agents," never "I / Austin."
  Byline is `Tyler Insurance Group · Updated <Month Year>`.
- **National, not local.** Remove every Kentucky / Lexington / Bluegrass / Fayette reference and any
  local hospital names. Generalize state-specific rules (e.g. Medigap underwriting) to "in most
  states," naming a few example states rather than KY.
- **Every article gets its own distinct opener.** Do NOT reuse a template hook across articles
  (e.g. don't start multiple pieces with "It's the question our team hears most…"). Write a fresh,
  topic-specific opening each time so the library reads like a real editorial collection.
- Keep the shared structure: **quick-answer box → sections → callouts → recap → 5-question FAQ →
  CTA → disclaimer.**
- **CTA** ends with the agency: "Our licensed agents can…" and `Call Tyler Insurance Group:
  (859) 618-6443`.
- **Disclaimer** (required, Medicare marketing): general-info + not endorsed by the U.S. government
  + "we do not offer every plan in your area" + Medicare.gov / 1-800-MEDICARE. Cite CMS for figures
  and note state rules vary.
- **YMYL accuracy:** verify all dollar figures / rules against CMS / SSA, same as the Bluegrass site.

## 3. Deliverable formats

For each TIG article, produce BOTH:
1. **Styled HTML doc** — self-contained, brand fonts via Google Fonts, a "how to use" paste note at
   the top, then the article. This is for pasting into the TIG website editor (headings, bold,
   tables, lists carry over). Uses the doc CSS pattern established in the scratchpad HTML files.
2. **Editable Word `.docx`** — generated with `python-docx`; Heading 1/2/3 styles, real table,
   numbered/bulleted lists, shaded callout/quick-answer boxes, gold/gray-aware accents.

Both must be verified free of Kentucky/Bluegrass/Lexington references before sending.

## 4. Illustration rules

- **1200×630 inline SVG** (doubles as hero + Open Graph / social card). Also export a PNG for
  social and the Word doc. Validate with `xml.dom.minidom` and render to confirm.
- **Use the TIG palette** (gold `#dbcf86` + gray `#7e8082` + white + soft `#f6f4ea` background),
  NOT coral/green. Map any two-way "choice" to gold vs. gray.
- **Compliance for drug/plan topics:** concept over product. NO real drug packaging or brand logos,
  NO before/after or weight-loss-result imagery, NO alarming needle close-ups. Generic pens/pills,
  signposts, icons, price badges are fine.

## 5. Produced so far

- `Does Medicare Cover Ozempic, Wegovy & Zepbound? The 2026 GLP-1 Bridge` — HTML + docx + gold/gray
  illustration (pen + capsule + "$50/month" badge).
- `Medicare Advantage vs. Medigap: The Real Difference` — HTML + docx + gold/gray illustration
  (fork-in-the-road signpost: gold "Medigap" / gray "Advantage").
