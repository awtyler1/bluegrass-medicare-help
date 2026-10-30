# Page standards (October 2026)

Every page on bluegrassmedicarehelp.com follows these rules. They come from how Devoted Health
structures its site (from knowledge of the site and search results; devoted.com is outside the build
network, so it was not inspected live) and from the senior-usability research in
`docs/homepage-audit-2026-10.md`.

## What Devoted does, and what we take from it

1. **Each page has one job.** Devoted's Find a Plan page offers exactly two routes: answer a few
   questions, or call a licensed agent. Nothing else competes.
2. **The header is a phone number and one button.** Navigation is a handful of task-named links.
3. **Contact lives in one place.** Phone, hours, booking and call-back sit on a single page, not
   spread across several forms.
4. **Audience pages are guides with one action.** "New to Medicare" content leads with what to do
   next, in order, and ends with the same single action.
5. **Pages are assembled from a few repeating blocks** (hero, steps, cards, list, questions, final
   call band) in soft colour bands, so every page feels like the same site.

## The site, by job

| Job | Page | Primary action |
|---|---|---|
| Orientation | `/` | Search the guides (call is secondary) |
| Turning 65 | `/turning-65/` | Book a free review |
| Learn | `/articles/` and topic pages, 34 articles | Read; one end-of-article review link |
| Local | `/kentucky/` and five county pages | Book a free review |
| Talk to us (the only contact page) | `/schedule/` | Pick a time; call and call-back sit beneath it |
| Trust | `/about/`, `/reviews/` | Book a free review |
| Tools | calculator, glossary, quizzes, videos, free guide | Use the tool |
| Campaigns | `/plancheck/` | Its own campaign action (managed separately) |

Retired in this pass, each with a 301: the five-step `/review/` form and `/help/` (now the
call-back on `/schedule/`), the Turning 65 quote form, `/articles/turning-65/` (folded into
`/turning-65/`), and the old `/articles/medicare-in-lexington-ky/` redirect page.

## Rules every page meets

- **One primary button** per screen, always the coral pill. Everything else is a text link.
- **Header:** four links (Turning 65, Learning Center, Your County, About), the phone number, and
  "Book a free review". Phones show one coral Call button and the menu.
- **Hero:** one headline, one sentence, one action. No more than one supporting line under it.
- **Body:** built from the shared blocks only (steps, cards, list rows, question accordion, final
  band). Section headings say what the section is.
- **Questions** use the accordion and carry matching FAQPage schema.
- **Footer:** one row of ten links, then the legal footer with the CMS disclaimer.
- **Firm voice** ("we", "our advisors"); reader-voice buttons stay first person.
- **Phones first:** the page's primary action is the first thing after the hero on a phone.

## Build order after any content change

`build-homepage-v3.py` → `update-chrome-v4.py` → `build-turning65-v3.py` → `build-hubs.py`
→ `firm-voice-v3.py` → `restyle-pages-v3.py`. Every step is idempotent.
