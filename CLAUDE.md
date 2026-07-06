# Bluegrass Medicare Help — build guide

Static site (HTML/CSS/vanilla JS) on GitHub Pages, served at the domain root.
Brand: **Tyler Insurance Group** dba **Bluegrass Medicare Help**, Lexington, KY.
Audience: Kentucky seniors approaching or on Medicare. Philosophy: **guide → educate → help.**

## Design philosophy (follow this on every new page/section)
- **Senior-first and intuitive.** Big tap targets, whole cards/tiles clickable (use `<a>`, not a `<div>` with a tiny link). Plain English, no jargon. Generous font sizes.
- **Show, don't just label.** Topic tiles and section headers get a custom **illustrated SVG scene** in the brand palette (see `/articles/` topic cards and `mockups/learn-2/`), not bare text + pills. Illustrations are drawn inline in code (no image downloads — the build network blocks stock-photo CDNs). Real photos of Austin / Lexington / clients are welcome when provided and beat both stock and illustration for trust.
- **Educate first, convert second.** Lead with the answer; the call-to-a-local-agent CTA comes after value is delivered.
- **No dead ends.** Every page has the shared nav + footer nav + a back path. Feels like a premium, finished site.
- **Minimal em dashes** in article prose; include a relatable scenario where it helps.

## Brand tokens (keep consistent)
`--cream:#f4efe7  --cream2:#faf6ef  --warm:#efe6d6  --ink:#2a2620  --dark:#1f1d1a`
`--coral:#d05528  --coral-d:#b3431d  --mute:#5f594f  --faint:#938c80  --line:#e2d9c8  --green:#3a7d52`
Fonts: **Fraunces** (serif, headings) + **Source Sans 3** (sans, body).

## Required on every public page
- Meta Pixel ID **27176602235306137** + GA4 **G-NF57CZ802N** (both in `<head>`).
- `<link rel="stylesheet" href="/assets/site.css">` for shared header/nav/footer/accessibility/knowledge-check styles. Page-specific CSS goes in an inline `<style>`.
- Shared chrome: `.ustrip` location bar, `.nav` header (slim Call `.navcta`), `.fnav` footer nav, `.foot` legal footer with the CMS disclaimer.
- SEO: `<title>`, meta description, `<link rel="canonical">`, OG + Twitter tags, and JSON-LD (`@graph`). Add the new URL to `sitemap.xml`.
- Root-relative paths (`/assets/...`, `/articles/...`).
- Thank-you pages and `/mockups/` are `noindex,nofollow`; public pages are `index,follow`.

## Learning Center (`/articles/`) — current IA (Design 2)
- Hero (`.intro`) → illustrated **topic cards** (`.m2grid`/`.m2cat`, one per category) → list header (`#m2title` + "Show all topics") → scannable **list** (`.lclist` of `.lcrow`).
- Each `.lcrow` carries `data-cat` (basics | turning65 | coverage | costs | onmedicare | ss | local) and `data-date="YYYY-MM-DD"`. `data-cat` may hold **multiple space-separated categories** (e.g. `data-cat="costs local"`) so one article can appear under more than one topic card; the filter matches by membership. JS auto-sorts newest-first; clicking a topic card filters via `window.__lcset(filter,label)` and scrolls to `#guides`.
- **Adding an article:** create `/articles/<slug>/index.html` (copy an existing one — it includes recap + 5-question knowledge check + FAQ schema), add a `.lcrow` to `/articles/index.html` with the right `data-cat`/`data-date`, bump **each** matching topic card's `.m2n` count, and add the URL to `sitemap.xml`.

## Article requirements
- YMYL accuracy: verify all dollar figures / rules against CMS / SSA before publishing.
- End each article with a `.recap` summary and a 5-question knowledge check (`window.KCHECK` array + `<div id="kcheck">` + `/assets/site.js`).
- Include FAQPage + BreadcrumbList + BlogPosting JSON-LD.

## Tyler Insurance Group cross-post (do this for every new article)
Every article published here also gets a **Tyler Insurance Group version** for the parent agency's
national site. See **`docs/tyler-insurance-group-article-guide.md`** for the full spec. In short:
- **Agency voice** ("we / our team / our licensed agents," never "I / Austin"); byline `Tyler Insurance Group`.
- **National, not local** — strip all Kentucky / Lexington / Bluegrass references; generalize state rules.
- **A distinct opener per article** — never reuse a shared template hook.
- Deliver **both** a styled HTML doc (for pasting into the TIG site) and an editable Word `.docx`.
- **TIG brand colors** (from the logo), NOT the Bluegrass coral/green:
  `--tig-gold:#dbcf86  --tig-gold-d:#b0a154  --tig-gray:#7e8082  --tig-gray-d:#5c5e60` + white text; same Fraunces/Source Sans fonts.
- Matching **1200×630 inline-SVG illustration** in the TIG palette; compliance-safe (no drug branding, no before/after).

## Validation before committing
HTML tag balance (`html.parser`), `json.loads` on JSON-LD, internal-link existence, SVG well-formedness (`xml.dom.minidom`), `sitemap.xml` via `xml.dom.minidom`.

## Git
Develop on `claude/admiring-volta-UgBzJ`. Commit + push to that branch. Do NOT open PRs unless asked.
