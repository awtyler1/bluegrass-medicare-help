# Homepage audit and redesign directions, October 2026

Scope: the bluegrassmedicarehelp.com homepage as of 30 October 2026, reviewed at phone width
(500px headless), tablet and desktop (1366px). Reference site named by Austin: greyoakdental.com
(could not be opened from the build container; worked from its indexed structure and Austin's
description: calm, one hero, one booking action, services grid, team, reviews, location).

## 1. What the best small-practice and content sites do now

These are the working principles, with the source of each. Vendor blogs are marked as such.

1. **Pass the five-second test.** A first-time visitor must be able to say what you do, where,
   why to trust you, and what to do next without scrolling. (Home-care marketing guidance,
   vendor; echoed by NN/g homepage research.)
2. **One primary action, repeated.** Pick the single thing you want most visitors to do and make
   every other action visibly secondary. Repeat the primary at top and bottom. (Vendor
   guidance; NN/g on call-to-action hierarchy.)
3. **Trust in the first screen, through specifics.** Credentials, review count and rating, a
   real photo of the real person, and the physical address outweigh brand photography.
   (2026 healthcare design guides, vendor; CMS marketing rules make credentials mandatory anyway.)
4. **Fewer, larger, calmer.** Older adults make more errors on dense pages, read light or small
   text poorly, and struggle with hover-only cues, dropdowns and sliders. Body text 18px or
   larger, targets 44px or larger (WCAG 2.2 AAA; 24px is the AA floor), high contrast, one idea
   per screen on a phone. (NN/g *UX Design for Seniors*, 3rd ed.; W3C WAI older-users research.)
5. **Predictable patterns beat clever ones.** Standard nav, standard card grid, plain headings
   that say what the section is. No tilted photos, handwriting fonts or novelty layouts; those
   read as "someone's side project" to a 68-year-old. (NN/g; Grey Oak Dental is a good example
   of the calm version.)
6. **Mobile is the primary design, not an adaptation.** Google indexes the phone version. Most
   seniors reach a local site from a phone after a Google search or a mailed letter. Single
   column, thumb-zone action bar, no horizontal scroll. (Google mobile-first indexing.)
7. **Consistency is a trust signal.** One illustration style, one card style, one button style.
   Mixed systems read as unfinished. (NN/g visual consistency research.)
8. **Content hubs need a front door, not a feed.** A site that is a library for a whole state
   should make the library the obvious thing, with a human beside it, instead of burying the
   library under the sales pitch. (Observed on public-library, NPR and gov.uk patterns.)

## 2. Audit of the current homepage

| # | Finding | Evidence | Principle |
|---|---|---|---|
| 1 | **Eight actions before the first scroll ends on a phone.** Nav Book, nav Call, hero phone plate, two door buttons, "just call" link, calculator link, portrait phone plate. | Phone screenshot, first 1,900px | 2 |
| 2 | **The phone number appears eight times on one page.** Repetition past two or three stops reading as confidence and starts reading as pressure. | `grep tel:` count 8 | 2 |
| 3 | **No sentence says what the site is.** The hero is about Austin ("a neighbor, not a call center"). Nothing says "Kentucky's plain-English Medicare guide, free help from a licensed local agent." A first-timer cannot tell it is a statewide information hub. | Hero copy | 1 |
| 4 | **Lexington-only framing contradicts the statewide goal.** Top strip: "Lexington, Kentucky · Serving Fayette & surrounding counties." Office section: "You can drive to my office." County help is one link at the bottom of the office section. | `.ustrip`, `.officesec` | 1, 8 |
| 5 | **Seven sections, each with a different visual system.** Illustrated story tiles, numbered step cards, a tan note box with handwriting, review cards with avatar circles, a map card, a landscape banner. The tilted portrait card and the Caveat script font add novelty. | Desktop screenshot | 5, 7 |
| 6 | **Section headings are clever, not scannable.** "Three steps, and most of them are mine." "The free part is real. Here's why." "Don't take our word for it." "You can drive to my office." A senior scanning for "costs" or "my county" finds no handle. | Section h2s | 5 |
| 7 | **The Learning Center, the actual hub, is the last section.** Forty-plus guides are represented by one banner at the bottom. The four "What's on your mind" cards do the job partly but sit under a 1,900px hero. | Section order | 8 |
| 8 | **The embedded Google map fails for some visitors** and renders as a grey box with a broken-page icon in the test render; it is also an iframe that slows the page. | Phone screenshot, office section | 3, 6 |
| 9 | **First-person voice ("I", "my office") on a page branded as an organization** (Bluegrass Medicare Help / Tyler Insurance Group). Fine in Austin's note boxes; confusing as the voice of the whole site when the site claims statewide reach. | Copy | 3 |
| 10 | **Strengths to keep:** real photo of Austin; licence numbers in the hero; 5.0 Google rating with named reviewers; the "turning 65 / already on Medicare" split; 18px body floor; sticky mobile call bar; TPMO disclaimer; brand palette and type. | | |

Net: the page is not unprofessional in its parts. It is unprofessional in its *sum*: too many
competing things, no single statement of purpose, and a visual system that changes every
section. The fix is subtraction and hierarchy, not new features.

## 3. What all three directions share

- One sentence of purpose in the hero, naming Kentucky and "free help from a licensed agent."
- One primary action (Call) in coral, repeated once at the end; everything else secondary.
- Trust row in the first screen: 5.0 Google, 1,000+ Kentuckians helped, KY licence number.
- Statewide framing; Lexington office stated as a fact, not the headline.
- Five or six sections, each with a plain heading that names its content.
- One illustration style (simple line glyphs), one card style, no tilt, no script font.
- Body 19px, headings large, tap targets 56px, single column on phones, sticky call bar.
- The Learning Center and county finder visible without hunting.
- Nav cut to four items plus Call. "Videos", "Glossary", "Quizzes" move to the footer.
- Austin's first-person voice kept inside one clearly marked "A note from Austin" block.

## 4. The three directions

**A. The Front Desk.** Closest to Grey Oak Dental. Calm, photo-led hero with one call button,
three "where are you" doors, four most-needed guides, county finder, reviews, a short
about-and-office block. Best if Austin's priority is the call.

**B. The Library.** The Learning Center is the front door: a question box and six topic tiles
fill the first screen, with a slim "ask a real person" bar under them. Timely items ("this
month in Medicare") and tools follow, then county help, then Austin and reviews. Best for the
statewide-hub ambition and for SEO, since the homepage links to every topic.

**C. The Kitchen Table.** One question, three very large answers ("I'm turning 65", "I already
have Medicare", "I'm helping a parent or spouse"), then a short "what happens when you call,"
reviews, a plain list of guides, counties. The simplest page of the three and the most
phone-like; the most senior-friendly if the goal is to get the right person to the right path
in one tap.

Recommendation: **B's structure with A's hero discipline** is the strongest fit for "a hub for
information for all of Kentucky" that still converts; C is the safest if Austin wants the
least cognitive load above all. Mockups are in `/mockups/home-v3/` and as private artifacts for
phone review.

## 5. Round 2 (30 October 2026): direction B chosen, Devoted lessons, brighter palettes

### What Devoted Health's site does well

devoted.com could not be opened from the build container (host not in the session's allowed
network). The points below come from knowledge of the site and from search results, not a live
inspection on this date. Re-check once the host is allowed.

1. **One job per screen.** The hero carries a single task and the phone number, and little else.
2. **The phone number lives in the header with a label**, not as a bare icon, so it is always one
   glance away without being repeated down the page.
3. **Large, friendly headings and very short paragraphs.** Most sections are a heading, one or
   two sentences and an action.
4. **Colour-blocked sections.** Soft full-width tints separate sections instead of borders, rules
   and boxed cards, which is a large part of why it feels calm.
5. **Warm photography of real-looking older adults**, never clip-art. (We should use real photos
   of Austin, the office and Kentucky clients with consent, not stock.)
6. **Pill-shaped buttons and one signature colour** used for every action, so "what can I tap"
   is never in doubt.
7. **Generous white space.** Fewer things per screen; nothing competes with the primary action.

What we deliberately do not copy: Devoted's signature orange-red and heart mark. We are an
independent agency that may represent Devoted among other carriers, and CMS marketing rules
for third-party marketing organizations prohibit materials that could mislead about who we are
or imply a carrier's endorsement. Our site should look like us, not like a carrier.

Applied to mockup B (version 2): labelled phone number in the header, a rounded search pill in
the hero, a single "Austin picks up" line instead of a second big button, colour-blocked bands,
borderless white cards with soft shadow, pill buttons, a coloured final call band.

### Colour

The logo is a deep teal-blue (about #1a5572) and a red (about #d9493d). The current site uses
cream, coral and green and never uses the logo's blue, which is part of why it reads as
assembled rather than designed. Four palettes were built and checked against WCAG 2.2 contrast:

| Palette | Action colour | White text on action | Body text on page | Notes |
|---|---|---|---|---|
| **Logo blue** (recommended) | #1f62a8 | 6.2:1 | 16.3:1 | Matches the logo; blue reads as trust and calm; red kept as a small accent from the logo |
| Meadow green | #1c7a4b | 5.3:1 | 15.8:1 | "Bluegrass" in feel; sunflower and sky tints |
| Bright coral | #d2481f | 4.5:1 | 15.0:1 | Closest to the current brand, on white; nearest to Devoted's orange |
| Current | #d05528 | 4.2:1 (passes only as large text) | 13.1:1 | Cream background lowers contrast and reads dated |

All three new palettes put every text pairing at 4.5:1 or better and body text at 7:1 or better
(AAA). Heading type can be toggled between the current serif and a rounded sans (Figtree) to
test the friendlier Devoted-style feel.
