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

Written against the actual transcript. Every claim below is something Austin says
in the video, so the description and the video match.

```
Medicare covers 80% of your Part B costs. What almost nobody tells you is that
Original Medicare has no cap on the other 20%. A Medicare Supplement and a Medicare
Advantage plan are two different answers to that one problem.

Full written breakdown: https://bluegrassmedicarehelp.com/articles/medicare-advantage-vs-medigap/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap

Most people on Medicare have already chosen between these two, whether they realized
it or not. In this video I walk through what each one is actually doing.

Start with the gap. On a $100 bill, Medicare pays its share and you cover the rest,
which sounds manageable. But employer plans and Affordable Care Act plans all have a
maximum out-of-pocket, a safety net where the billing stops. Original Medicare has
no such cap. Run the same math on a $100,000 cancer treatment and the 20% is
$20,000, with nothing to stop it. That is the problem both plan types exist to fix.

A Medicare Supplement, also called Medigap, is pay regardless. You send a premium
every month and the insurance company picks up your 20%. There are no networks, so
you can see any doctor in the country who accepts Medicare, which is roughly 99% of
them, and generally no referrals. You pay that premium whether you use it or not,
even if you are the healthiest person you know. A Supplement does not include drug,
dental, vision, or hearing coverage, so a separate Part D drug plan has to go with it.

A Medicare Advantage plan is Part C. Think C for complete: medical, drugs, dental,
vision, and hearing wrapped into one plan and one card. It is pay as you go, with a
flat copay when you actually use something, and every Advantage plan has a maximum
out-of-pocket built in. The trade-off is the network. The plan decides which doctors
it will pay for, and many still require referrals, though some carriers are dropping
that.

Neither one is better. It comes down to your preferences, your lifestyle, your
health today, your doctors, and your prescriptions.

CHAPTERS
(estimated from the transcript, check against the finished cut)
0:00 Advantage or Supplement: the same job, done differently
0:29 The 80/20 gap in Original Medicare
0:54 Why no max out-of-pocket is the real risk
2:02 Neither one is better, it depends on you
2:28 Medicare Supplement (Medigap): pay regardless, go anywhere
4:00 What a Supplement does not cover
4:30 Medicare Advantage (Part C): one card, pay as you go
5:52 The trade-off: networks and referrals
6:53 Talk it through with a local advisor

KEEP READING
The different types of Supplement plans, Plan G vs. Plan N: https://bluegrassmedicarehelp.com/articles/medicare-supplement-plan-g-vs-plan-n/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap
The Part D drug plan that pairs with a Supplement: https://bluegrassmedicarehelp.com/articles/medicare-part-d-prescription-drug-plans/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap
Which Lexington hospitals take Medicare Advantage: https://bluegrassmedicarehelp.com/articles/lexington-hospitals-medicare-advantage-networks/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap
The Kentucky Medigap Birthday Rule: https://bluegrassmedicarehelp.com/articles/kentucky-medigap-birthday-rule/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap
Turning 65 soon, and when to enroll: https://bluegrassmedicarehelp.com/articles/turning-65-enrollment-window/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap

TALK IT THROUGH
Book a free 30-minute review: https://bluegrassmedicarehelp.com/schedule/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap
Or call the office at (859) 618-6443.

ABOUT
Austin Tyler is a licensed insurance agent with Tyler Insurance Group, a local
Medicare advisory firm in Lexington, Kentucky. We help seniors and people turning 65
compare their Medicare options against the doctors they already see and the
prescriptions they already take.

#Medicare #MedicareAdvantage #Medigap

We respect your privacy. This is a solicitation for insurance. Tyler Insurance
Group is not connected with or endorsed by the United States government or the
federal Medicare program. We do not offer every plan available in your area.
Currently we represent 6 organizations which offer 158 products in your area.
Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance
Program (SHIP) to get information on all of your options.
```

### Chapter timestamps

The times above assume a 7:30 runtime. They come from where each section sits in the
transcript, so if the finished cut is a different length, scale them. Percentage
through the video for each chapter:

| % in | Chapter |
|---|---|
| 0.0% | Advantage or Supplement: the same job, done differently |
| 6.4% | The 80/20 gap in Original Medicare |
| 11.9% | Why no max out-of-pocket is the real risk |
| 27.0% | Neither one is better, it depends on you |
| 33.0% | Medicare Supplement (Medigap): pay regardless, go anywhere |
| 53.3% | What a Supplement does not cover |
| 59.9% | Medicare Advantage (Part C): one card, pay as you go |
| 78.3% | The trade-off: networks and referrals |
| 91.8% | Talk it through with a local advisor |

YouTube rules: the first chapter must be 0:00, there must be at least three, and each
must run at least 10 seconds. If a timestamp is off, chapters silently stop working,
so it is worth scrubbing the video once to confirm.

### Tags

YouTube keyword tags (Details, "Show more", Tags field):
`medicare advantage vs medicare supplement, medicare supplement vs advantage,
medigap vs medicare advantage, medicare advantage or medigap, which medicare plan
is better, medicare supplement explained, medicare advantage explained, medicare
80 20 gap, medicare max out of pocket, medicare 2026, turning 65 medicare,
medicare help kentucky, medicare lexington ky`

### One accuracy note for future videos

The video says "Medicare will cover you 80% of your medical bills." That is right for
**Part B** (doctor visits, outpatient care, tests) after the annual deductible.
**Part A** hospital coverage does not work as an 80/20 split: it has a deductible per
benefit period and daily coinsurance once a stay runs long. The description above is
worded as "80% of your Part B costs" so the written version stays precise.

The headline point, that Original Medicare has no out-of-pocket maximum, is correct
for both parts and is the thing worth repeating.

Worth a pinned comment or a line in a follow-up video, not a re-shoot.

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
