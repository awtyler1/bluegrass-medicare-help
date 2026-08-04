# /schedule/ page concepts (August 2026)

Four design directions for the self-scheduling landing page. Mockups are noindex.
Calendar area is a placeholder sized like the real GoHighLevel widget
(https://link.runonforge.us/widget/booking/d8bRC0hzOnha9XAdaCoD).

- concept-a-split-card.html  : classic split hero, checkmark value bullets, 3-step strip below
- concept-b-trust-wall.html  : social-proof-first (real Google reviews + credential badges), sticky calendar
- concept-c-editorial.html   : dark editorial band with cards lifted over the boundary
- concept-d-letter.html      : personal note from Austin + numbered "what happens on the call"

Build/regenerate: python3 build_mockups.py
When one is chosen: build /schedule/index.html with the real iframe, lazy-loaded
(click-to-load or IntersectionObserver) so the third-party widget never blocks render,
add "Schedule" to nav + footer nav sitewide, and add the URL to sitemap.xml.
