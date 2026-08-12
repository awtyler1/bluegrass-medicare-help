# Bluegrass Medicare Help — Landing Page Spec

A drop-in reference for spinning up **new landing pages** that look, read, and behave
exactly like the live site. Hand this file to a Claude project and it has everything it
needs to build an on-brand page from scratch.

- **Company:** Tyler Insurance Group **dba** Bluegrass Medicare Help
- **Location:** 1029 Monarch Street, Suite 110, Lexington, KY 40513
- **Phone:** (859) 618-6443 → link as `tel:18596186443`
- **Domain:** `https://www.bluegrassmedicarehelp.com` (GitHub Pages, served at root)
- **Tech:** Static HTML + CSS + vanilla JS. No build step, no frameworks, no npm.
- **Audience:** Kentucky seniors turning 65 or already on Medicare.
- **Philosophy:** **guide → educate → help.** Educate first, convert second.

> Network note: the build environment blocks stock-photo / image CDNs. All illustration
> is **inline SVG drawn in code**. Real photos of Austin / Lexington / clients are
> welcome when supplied and beat both stock and illustration for trust.

---

## 1. Design philosophy (apply to every page)

- **Senior-first and intuitive.** Big tap targets (min ~44–58px), whole cards/tiles
  clickable via `<a>` (never a `<div>` with a tiny link). Generous font sizes. Plain
  English, zero jargon.
- **Show, don't just label.** Section headers and topic tiles get a **custom illustrated
  inline SVG scene** in the brand palette, not bare text + pills.
- **Educate first, convert second.** Lead with the answer/value; the call-an-agent CTA
  comes after value is delivered.
- **No dead ends.** Every page carries the shared top nav, footer nav, and a back path.
  It should feel like a premium, finished site.
- **Voice:** warm, local, plain-spoken. "A real Kentucky agent, not a call center."
  Minimal em dashes in prose; a relatable scenario helps.

---

## 2. Brand tokens (paste into every page's inline `:root`)

```css
:root{
  --cream:#f4efe7; --cream2:#faf6ef; --warm:#efe6d6; --ink:#2a2620; --dark:#1f1d1a;
  --coral:#d05528; --coral-d:#b3431d; --mute:#5f594f; --faint:#938c80;
  --line:#e2d9c8; --white:#fff; --green:#3a7d52;
  --serif:'Fraunces',Georgia,serif; --sans:'Source Sans 3',-apple-system,sans-serif;
  --hand:'Caveat',cursive;
}
```

| Token | Hex | Use |
|---|---|---|
| `--coral` / `--coral-d` | `#d05528` / `#b3431d` | Primary action color, hover/active |
| `--green` | `#3a7d52` | Success, checkmarks, "free" badges |
| `--cream` / `--cream2` / `--warm` | `#f4efe7` / `#faf6ef` / `#efe6d6` | Page + card backgrounds |
| `--ink` / `--dark` | `#2a2620` / `#1f1d1a` | Body text / darkest (footer, theme-color) |
| `--mute` / `--faint` | `#5f594f` / `#938c80` | Secondary text / hints, fine print |
| `--line` | `#e2d9c8` | Borders, dividers |

**Fonts:** **Fraunces** (serif — all headings) + **Source Sans 3** (sans — body).
`Caveat` (`--hand`) is optional, only when a handwritten accent is wanted (e.g. home page).

**Type scale (landing page):** h1 `33px` mobile → `44px` ≥880px, serif 600, `letter-spacing:-.6px`.
Sub/lead `17.5px` mute. Question headings (`.q`) `27px` serif 500. Body `16–18px`, line-height `1.6`.

---

## 3. Required on every public page

Order inside `<head>`:

1. `<meta charset>`, responsive viewport **with `viewport-fit=cover`**, favicon
   (`/assets/logo-mark.png`), `apple-touch-icon`, `<meta name="theme-color" content="#1f1d1a">`.
2. **Meta Pixel** ID `27176602235306137` (full snippet, see §7).
3. **GA4** `G-NF57CZ802N` (gtag snippet, see §7).
4. `<title>`, `<meta name="description">`.
5. Google Fonts preconnect + Fraunces/Source Sans 3 stylesheet link.
6. `<link rel="stylesheet" href="/assets/site.css">` (shared chrome — load it, don't
   duplicate it). Page-specific CSS goes in a single inline `<style>` after it.
7. SEO/social block: `canonical`, `robots`, OG tags, Twitter tags, JSON-LD `@graph`.

Required in `<body>`, in order:

- `<a class="skip-link" href="#main">Skip to content</a>`
- `.ustrip` location bar → `.nav` sticky header → `<main id="main">` → `.fnav` footer
  nav → `.foot` legal footer.
- Mobile-nav toggle script (small IIFE, see §6).

**Paths are always root-relative:** `/assets/...`, `/articles/...`, `/review/`, etc.

**Indexing:**
- Public pages: `<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">`
- Thank-you pages and anything under `/mockups/`: `<meta name="robots" content="noindex, nofollow">`

**Always add the new public URL to `/sitemap.xml`.** (Thank-you pages stay out of the sitemap.)

---

## 4. Page anatomy & file conventions

- One folder per page, served as a clean directory URL:
  `/<slug>/index.html` → `https://www.bluegrassmedicarehelp.com/<slug>/`.
- A conversion landing page has a matching **thank-you** page at `/<slug>/thankyou/index.html`.
- Current live pages for reference:

| URL | Type | Funnel / purpose |
|---|---|---|
| `/` | Home | Two-door hero (turning 65 vs already on Medicare) |
| `/review/` | Landing | 5-step "Free Medicare Review" funnel |
| `/guide/` | Landing | 3-step "Free Kentucky Medicare Guide" lead magnet |
| `/quiz-65/` | Landing | "Kentucky Medicare Quiz" funnel |
| `/supp-advantage/` | Landing | "Advantage vs Supplement Quiz" funnel |
| `/help/` | Redirect | 301-style meta+JS redirect to `/review/` |
| `/articles/` | Learning Center | Topic cards + filterable article list |
| `/quizzes/` | Index | Hub of quizzes |
| `/<slug>/thankyou/` | Thank-you | Confirmation + fires conversion events |

**Shared nav links (keep this set & order):** Learning Center (`/articles/`),
Quizzes (`/quizzes/`), Free Guide (`/guide/`), Free Review (`/review/`). Mark the current
page with `class="active" aria-current="page"`.

A landing page body typically is:
`.ustrip` → `.nav` → `<main class="rmain">` ( h1 + `.rsub` + `.rscene` SVG + `.funnel`
card + `.rtrust` bullets + `.rfine` CMS disclaimer ) → `.fnav` → `.foot`.

---

## 5. The multi-step funnel (lead form pattern)

Every conversion page uses the same animated, one-question-at-a-time card. Structure:

- `.funnel` card → `.progress`/`.pbar` bar + `.pstep` ("Step 1 of N") → `<form>` of
  `.step` blocks (`data-step="1..N"`, first has `is-active`).
- **Text steps** use `.inp` inputs + a `.cta` button carrying `data-go="<next>"`.
- **Choice steps** use `.opts[data-field="x"]` containing `.opt` buttons with `data-val`;
  selecting one auto-advances after ~180ms and stores the value.
- **Back** buttons carry `data-back="<prev>"`.
- Final step collects contact info, requires the **consent checkbox**, then submits.

**Steps differ per funnel** (review = 5: name → stage → ZIP → priority → contact;
guide = 3: name → stage → email/ZIP/phone). Reuse the CSS/JS, change the questions.

**Field conventions:** placeholders in `UPPERCASE`, every input has `aria-label` +
correct `autocomplete` (`given-name`, `family-name`, `postal-code`, `tel`, `email`).
ZIP is `inputmode="numeric" maxlength="5"`. Validate name + 5-digit ZIP + phone before submit.

**Submit flow (vanilla JS, no libraries):**
1. Require phone + consent checkbox (`alert()` if missing).
2. Disable button, set `.sending`, show "Sending…".
3. `fetch(GHL_WEBHOOK_URL, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) })`.
4. On success **or** failure (`.catch`), call `finish()` so the user never gets stuck.
5. `finish()` fires `fbq('track','Lead',{content_name:'<Funnel Name>'})` then redirects to
   `/<slug>/thankyou/?n=<firstName>`.

**Lead payload shape:**
```js
var payload = {
  firstName, lastName, email, phone, zip,
  medicareStage: state.stage,      // from the "stage" choice step
  topPriority: state.priority,     // funnel-specific fields as needed
  bestTimeToCall: bt,
  consentGiven: true,
  consentText: CONSENT_TEXT,       // full TCPA text, stored verbatim
  consentTimestamp: new Date().toISOString(),
  source: '<Funnel Name>',         // e.g. 'Free Medicare Review'
  pageUrl: window.location.href
};
```

**GoHighLevel (GHL) webhook** — base is shared, the trailing UUID is **per funnel**.
Create a NEW webhook trigger in GHL for each new funnel; never reuse another page's UUID.
```
https://services.leadconnectorhq.com/hooks/Sk1fSSIS0T4wBpJiADrK/webhook-trigger/<UNIQUE-UUID>
```
| Funnel | `source` | webhook UUID |
|---|---|---|
| Free Medicare Review (`/review/`) | `Free Medicare Review` | `fd91eae1-1237-43bf-9ec3-0822cab210d6` |
| Kentucky Medicare Guide (`/guide/`) | `Kentucky Medicare Guide - Landing Page` | `b2b5e80c-e2ce-4479-aa96-613e9abe0bfe` |
| Kentucky Medicare Quiz (`/quiz-65/`) | `Kentucky Medicare Quiz` | `f96944a6-10c1-40b4-853a-4c3c370d6c3d` |
| Advantage vs Supplement (`/supp-advantage/`) | `Advantage vs Supplement Quiz` | `1916f80e-cc2d-42b6-81b3-aedffe7a75c2` |

---

## 6. Shared chrome (copy verbatim — same on every page)

**Location strip + sticky nav** (the `.active`/`aria-current` page changes per page):

```html
<a class="skip-link" href="#main">Skip to content</a>

<div class="ustrip">
  <div class="wrap">
    <span>📍 <strong>Lexington, Kentucky</strong> &nbsp;·&nbsp; Serving Fayette &amp; surrounding counties</span>
    <span class="rate"><span class="stars">★★★★★</span> 5.0 on Google</span>
  </div>
</div>

<nav class="nav">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Bluegrass Medicare Help home">
      <img class="brand-logo" src="/assets/logo.png" alt="Bluegrass Medicare Help" height="46"
           onerror="this.style.display='none';this.nextElementSibling.style.display='flex';">
      <span class="brand-fallback"><span class="mark">B</span><span class="wm">Bluegrass<small>Medicare Help</small></span></span>
    </a>
    <div class="navlinks" id="navlinks">
      <a href="/articles/">Learning Center</a>
      <a href="/quizzes/">Quizzes</a>
      <a href="/guide/">Free Guide</a>
      <a href="/review/">Free Review</a>
    </div>
    <a class="navcta" href="tel:18596186443"><svg class="cta-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>Call</a>
    <button class="navtog" id="navtog" aria-label="Open menu" aria-expanded="false" aria-controls="navlinks">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
  </div>
</nav>
```

**Footer nav + legal footer** (the CMS disclaimer text is required and must not be edited):

```html
<nav class="fnav" aria-label="Footer">
  <div class="wrap">
    <a href="/" class="fnav-logo" aria-label="Bluegrass Medicare Help home"><img src="/assets/logo.png" alt="Bluegrass Medicare Help" onerror="this.closest('.fnav-logo').style.display='none'"></a>
    <div class="fnav-links">
      <a href="/">Home</a>
      <a href="/articles/">Learning Center</a>
      <a href="/quizzes/">Quizzes</a>
      <a href="/guide/">Free Guide</a>
      <a href="/review/">Free Review</a>
    </div>
    <a class="fcall" href="tel:18596186443"><svg class="cta-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg> Call (859) 618-6443</a>
  </div>
</nav>

<footer class="foot">
  <div class="wrap">
    <div class="fnm">Tyler Insurance Group</div>
    1029 Monarch Street, Suite 110, Lexington, KY 40513<br>
    <a href="tel:8596186443">(859) 618-6443</a> · <a href="https://www.tylerinsurancegroup.com">tylerinsurancegroup.com</a>
    <div class="disc">
      We respect your privacy. This is a solicitation for insurance. Tyler Insurance Group is not connected with or endorsed by the United States government or the federal Medicare program. We do not offer every plan available in your area. Any information we provide is limited to those plans we do offer in your area. Please contact Medicare.gov or 1-800-MEDICARE to get information on all of your options.
    </div>
  </div>
</footer>
```

**Mobile-nav toggle** (put just before `</body>`):

```html
<script>
(function(){
  var tog=document.getElementById('navtog'), links=document.getElementById('navlinks');
  if(tog&&links){
    tog.addEventListener('click',function(){var open=links.classList.toggle('open');tog.setAttribute('aria-expanded',open?'true':'false');});
    links.addEventListener('click',function(e){if(e.target.tagName==='A'){links.classList.remove('open');tog.setAttribute('aria-expanded','false');}});
  }
})();
</script>
```

The "phone" SVG above is the canonical Call icon — reuse it for every Call control
(`.navcta`, `.fcall`, `.btn`) with `class="cta-ico"`.

---

## 7. Tracking snippets (paste verbatim into `<head>`)

**Meta Pixel** (ID `27176602235306137`):
```html
<!-- Meta Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '27176602235306137');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=27176602235306137&ev=PageView&noscript=1"
/></noscript>
<!-- End Meta Pixel Code -->
```

**GA4** (`G-NF57CZ802N`):
```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NF57CZ802N"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-NF57CZ802N');
</script>
```

**Conversion events:**
- On lead submit (landing page JS): `fbq('track','Lead',{ content_name:'<Funnel Name>' });`
- On the thank-you page `<head>`, after the `gtag('config'...)` line, add:
  `gtag('event', 'generate_lead', { form_location: '<funnel_slug>' });`

---

## 8. Thank-you page pattern

- `<meta name="robots" content="noindex, nofollow">`, same head/chrome as the landing page.
- Fires `generate_lead` in `<head>` (the landing page already fired `fbq Lead` before redirect).
- Hero: green animated `.ty .check` ✓ → `.kick` eyebrow → `h1` ("You're all set! 🎉")
  → `.lead` ("Austin has your request…") → `.next` "What happens next" card →
  `.actions` (Call CTA + "Back to home" + "Read guides while you wait").
- Personalize the headline from the `?n=` query param (sanitize: strip non-letters,
  cap length) — see `/review/thankyou/index.html` for the exact snippet.
- "No dead ends": always include Home + Learning Center links.

---

## 9. Required legal / compliance (YMYL — do not improvise)

- **CMS disclaimer** (the `.foot .disc` text in §6) appears on every public page, verbatim.
- **TCPA consent checkbox** is required on every lead form. Short label shown to the user
  + a full `CONSENT_TEXT` string stored verbatim in the payload with an ISO timestamp.
  Block submit until checked.
- The page-level `.rfine` disclaimer near the funnel: *"Tyler Insurance Group is not
  connected with or endorsed by the U.S. government or the federal Medicare program. We do
  not offer every plan available in your area. Currently we serve Kentucky residents…"*
- **Accuracy:** verify every dollar figure / enrollment rule against CMS / SSA before
  publishing. Today's plan year context is **2026**.

---

## 10. Accessibility & UX baseline

- Skip link first in `<body>`; `<main id="main">` as the skip target.
- `:focus-visible` outline is coral (in `site.css`) — don't remove it.
- Respect `prefers-reduced-motion` (handled in `site.css`; don't add motion that ignores it).
- Tap targets ≥44px; `.opt` choices are 58px. Use `<a>`/`<button>`, never clickable `<div>`.
- Every icon-only control has `aria-label`; decorative SVG gets `aria-hidden="true"`.
- Mobile nav collapses ≤860px; the hamburger toggles `aria-expanded`.

---

## 11. Validation before publishing

Run these checks (the repo build expects them):
- HTML tag balance (`html.parser`).
- `json.loads` on each JSON-LD block.
- Internal links resolve to a real file/route.
- Inline SVG is well-formed (`xml.dom.minidom`).
- `sitemap.xml` parses (`xml.dom.minidom`) and contains the new public URL.

---

## 12. Checklist — adding a new landing page

1. Create `/<slug>/index.html` (copy `/review/` or `/guide/` as the base).
2. Swap `<title>`, meta description, canonical, OG/Twitter, JSON-LD `@graph` for the new URL.
3. Keep all tracking snippets (§7) and shared chrome (§6); set the right nav link `.active`.
4. Write the hero h1/`.rsub`, draw a fitting inline-SVG `.rscene`, build the funnel steps.
5. Create a **new GHL webhook** and set `GHL_WEBHOOK_URL`, `source`, and the `fbq` `content_name`.
6. Build `/<slug>/thankyou/index.html` (`noindex`), wire `generate_lead` `form_location`.
7. Add the public URL to `/sitemap.xml`.
8. Run the §11 validations.
9. Commit + push to the working branch. **Do not open a PR unless asked.**

---

## 13. Asset inventory (`/assets/`)

| File | Use |
|---|---|
| `site.css` | Shared chrome (header/nav/footer), a11y baseline, recap + knowledge-check styles. **Link, don't copy.** |
| `site.js` | Renders the end-of-article knowledge check from `window.KCHECK` (articles only). |
| `logo.png` | Full wordmark logo (nav + footer), `height:46` in nav, `54` in footer. |
| `logo-mark.png` | Square mark — favicon / apple-touch-icon. |
| `og-image.png` | 1200×630 social share image. |
| `austin-tyler.jpg` | Photo of the agent (trust sections). |
| `kentucky-hero.jpg` | Lexington/KY hero photo. |

Brand fallback: if `logo.png` fails to load, the inline `onerror` reveals a coral
monogram + wordmark so the header never breaks.
