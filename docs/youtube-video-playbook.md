# YouTube video playbook

How every video gets published, described, and wired back into the site.
Written for the video series in `docs/video-priority-list-2026.md`.

## The one thing to understand about links

Links in a YouTube description are `nofollow`. They pass **no ranking authority** to
the website. Their value is real but different: referral traffic and booked
appointments from people who just watched you explain the thing.

The SEO win runs the other direction. Embedding the video **on the matching article**
with `VideoObject` schema is what can earn a video thumbnail in Google results and
lifts time-on-page for the article. So: write the description for humans and for
YouTube's own search, and let the on-site embed do the SEO work.

## Description structure

Only the first two or three lines show before "show more." Put the hook and the
single most important link there. Everything else is for YouTube's search index
and for the people who expand it.

1. One-sentence hook that repeats the main keyword naturally
2. Primary link (the matching article), with UTM tags
3. Longer summary, 100 to 200 words, using the phrases people actually search
4. Chapters (timestamps) once the video is cut
5. Related reading, 3 to 5 site links
6. Booking + phone
7. Credentials line (this is an E-E-A-T signal, worth the space)
8. CMS disclaimer

## UTM tags

Always tag site links so GA4 separates YouTube traffic from search:

    ?utm_source=youtube&utm_medium=video&utm_campaign=<video-slug>

GA4 reads these automatically. No setup needed on the site.

## Video 2: "Medicare Supplement or Medicare Advantage?"

Matching article: `/articles/medicare-advantage-vs-medigap/`
Campaign slug: `ma-vs-medigap`

### Title

Consider publishing as:

> **Medicare Advantage vs. Medicare Supplement: Which Is Better? (2026)**

"Medicare Advantage vs Medicare Supplement" is the phrasing people type. "X or Y?"
is how people talk, "X vs Y" is how they search. Keeping the year in the title also
gives a clean reason to re-shoot and re-rank it every year.

### Description (paste as-is)

```
Medicare Advantage or Medicare Supplement? This is the single biggest decision you
make when you go on Medicare, and it is very hard to undo later.

Full written breakdown: https://bluegrassmedicarehelp.com/articles/medicare-advantage-vs-medigap/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap

Most people are handed a stack of mail and told the two are basically the same
thing. They are not. A Medicare Advantage plan replaces how your Original Medicare
is administered and usually bundles in drug coverage, with a network and copays as
you go. A Medicare Supplement, also called Medigap, sits alongside Original
Medicare and pays the share Medicare does not, with a higher monthly premium and
far less to think about at the doctor's office.

In this video I walk through the real trade-offs: what each one actually costs in a
year, how networks work, what happens when you travel, what happens if you get
seriously sick, and the part almost nobody explains up front, which is that
switching from Advantage back to a Supplement later can require medical
underwriting. That one detail changes the whole decision for a lot of people.

No plan names, no rankings, no "best plan" nonsense. Just the honest trade-offs so
you can tell which side of the line you are on.

CHAPTERS
0:00 [fill in]

RELATED
The Kentucky Medigap Birthday Rule, explained: https://bluegrassmedicarehelp.com/articles/kentucky-medigap-birthday-rule/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap
Switching from Advantage back to a Supplement: https://bluegrassmedicarehelp.com/articles/switching-medicare-advantage-to-medigap/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap
Plan G vs. Plan N, if you have decided on a Supplement: https://bluegrassmedicarehelp.com/articles/medicare-supplement-plan-g-vs-plan-n/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap
Which Lexington hospitals take Medicare Advantage: https://bluegrassmedicarehelp.com/articles/lexington-hospitals-medicare-advantage-networks/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap

TALK IT THROUGH WITH SOMEONE
Book a free 30-minute review: https://bluegrassmedicarehelp.com/schedule/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap
Or call (859) 618-6443. No cost, no obligation.

ABOUT
Austin Tyler is a licensed insurance agent with Tyler Insurance Group in Lexington,
Kentucky, helping people compare Medicare options against the doctors they already
see and the prescriptions they already take.

We respect your privacy. This is a solicitation for insurance. Tyler Insurance
Group is not connected with or endorsed by the United States government or the
federal Medicare program. We do not offer every plan available in your area.
Currently we represent 6 organizations which offer 158 products in your area.
Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance
Program (SHIP) to get information on all of your options.
```

### Tags / hashtags

Add at the very end of the description: `#Medicare #MedicareAdvantage #Medigap`

YouTube keyword tags (Details, "Show more", Tags field):
`medicare advantage vs medicare supplement, medicare supplement vs advantage,
medigap vs medicare advantage, medicare advantage or medigap, which medicare plan
is better, medicare supplement explained, medicare advantage explained, medicare
2026, turning 65 medicare, medicare help kentucky`

## Compliance note

This video is educational: it names no specific plans, benefits, premiums, or star
ratings. That keeps it in CMS "communications" territory rather than "marketing,"
which is the lighter bucket. The disclaimer above is included anyway because the
description contains a call to contact an agent.

If a future video names a specific plan or its benefits, it becomes marketing
material under CMS rules and the disclaimer is mandatory, not optional. Keep the
plan-specific talk on the phone.

## After upload: what to send

To wire the video into the site, send:

1. **The YouTube URL** (or just the 11-character video ID)
2. **Final title** as published, if it changed
3. **Duration** in mm:ss
4. **Publish date**

Duration and publish date are required fields for `VideoObject` schema. The
thumbnail is derived automatically from the video ID.

Optional but useful: the auto-transcript (open the video, "..." then "Show
transcript", copy). With it, accurate chapter timestamps and pull quotes for the
article can be written without guessing.

## After upload: what gets built

1. Video embedded at the top of the matching article, click-to-play against a
   thumbnail so it costs nothing on page load and sets no cookies until played
   (`youtube-nocookie.com`)
2. `VideoObject` JSON-LD added to that article's `@graph`
3. Video URL added to `sitemap.xml`
4. `/videos/` library page, once there are three or more videos
5. Cross-links from the related articles listed above
