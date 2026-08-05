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
3. Summary, 150 to 200 words, using the phrases people actually search
4. Chapters (timestamps)
5. Booking link + phone
6. One-line credentials (an E-E-A-T signal, worth the space)
7. Hashtags
8. CMS disclaimer

**Keep it to two links.** The matching article and the booking page. It is tempting
to list every related article, but a description with eight links reads as spam to a
human even when YouTube does not care, and it splits the click until nobody takes
any of them. Related reading belongs on the article, which is what the first link is
for. Aim for roughly 2,000 to 2,600 characters all in, against YouTube's 5,000 limit.

Only the first two or three lines show before "show more," so the hook and the
primary link go at the very top.

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

Written against the actual transcript, so the description and the video match.

Two links only: the matching article and the booking page. An earlier draft carried
eight and read like a link farm. More links do not mean more clicks, they mean the
click gets split until nobody takes any of them. Everything else the video sets up
lives on the article, which is where a reader who wants more should end up anyway.

```
Medicare covers 80% of your Part B costs. What almost nobody tells you is that
Original Medicare has no cap on the other 20%.

Full written breakdown: https://bluegrassmedicarehelp.com/articles/medicare-advantage-vs-medigap/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap

A Medicare Supplement and a Medicare Advantage plan are two different answers to
that one problem. On a $100 bill, the 20% is manageable. On a $100,000 cancer
treatment it is $20,000, and unlike employer or Affordable Care Act plans, Original
Medicare has no maximum out-of-pocket to stop it.

A Medicare Supplement, also called Medigap, is pay regardless. A premium every
month, the insurance company covers your 20%, no networks, any doctor in the country
who accepts Medicare, and generally no referrals. It does not include drug, dental,
vision, or hearing coverage, so a separate Part D drug plan goes with it.

A Medicare Advantage plan is Part C. Think C for complete: medical, drugs, dental,
vision, and hearing on one card. Pay as you go with copays, and a maximum
out-of-pocket built in. The trade-off is the network, and often referrals.

Neither one is better. It comes down to your health, your doctors, and your
prescriptions.

CHAPTERS
0:00 Advantage or Supplement: the same job, done differently
0:17 The 80/20 gap in Original Medicare
0:49 Why Original Medicare has no out-of-pocket maximum
1:40 A $100,000 bill and the $20,000 you would owe
2:10 Two answers to the same problem
2:27 Medicare Supplement: no networks, go anywhere
3:24 "Pay regardless": the premium is due either way
3:43 What a Supplement does not cover
4:14 Medicare Advantage (Part C): one card for everything
4:50 "Pay as you go": copays and a max out-of-pocket
5:31 The trade-off: networks and referrals
6:12 Talk it through with a local advisor

Want someone to walk through your own doctors and prescriptions? Book a free
30-minute review: https://bluegrassmedicarehelp.com/schedule/?utm_source=youtube&utm_medium=video&utm_campaign=ma-vs-medigap
Or call the office at (859) 618-6443.

Austin Tyler is a licensed insurance agent with Tyler Insurance Group, a local
Medicare advisory firm in Lexington, Kentucky.

#Medicare #MedicareAdvantage #Medigap

We respect your privacy. This is a solicitation for insurance. Tyler Insurance
Group is not connected with or endorsed by the United States government or the
federal Medicare program. We do not offer every plan available in your area.
Currently we represent 6 organizations which offer 158 products in your area.
Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance
Program (SHIP) to get information on all of your options.
```

### Chapter timestamps

Confirmed against the finished cut, not estimated. Source beats:

| Time | Beat in the video |
|---|---|
| 0:00 | Intro, Advantage vs. Supplement overview |
| 0:17 | The gaps in Original Medicare, the 80/20 split |
| 0:49 | No max out-of-pocket on Original Medicare |
| 1:16 | The 80/20 split applied to a serious illness |
| 1:40 | The $100,000 bill and the $20,000 exposure |
| 2:10 | Same problem, two different solutions |
| 2:27 | Medigap explained, no networks, flexibility |
| 3:00 | Supplement recap, monthly premium, no referrals |
| 3:24 | "Pay regardless" |
| 3:43 | No drug, dental, vision, or hearing coverage |
| 4:14 | Transition to Medicare Advantage |
| 4:28 | Part C as "complete", everything in one plan |
| 4:50 | "Pay as you go", the copay concept |
| 5:13 | Advantage plans do have a max out-of-pocket |
| 5:31 | Tied to the plan's network |
| 5:55 | Referral requirements |
| 6:12 | Invitation to reach out |
| 6:24 | Outro, contact info |

Nineteen beats is too granular for a chapter list, so the published chapters merge
them into twelve. The 1:16 illness setup folds into the $100,000 payoff at 1:40, the
3:00 recap folds into the Supplement section at 2:27, the 5:13 max out-of-pocket
folds into the copay section at 4:50, and 6:24 folds into the invitation at 6:12.

YouTube rules the merged list still satisfies: first chapter is 0:00, there are at
least three, and the shortest gap is 17 seconds against a 10 second minimum. If any
timestamp is wrong, chapters silently stop working, so confirm once after publishing.

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

## Published

| Field | Value |
|---|---|
| Title | Medicare Advantage vs. Medicare Supplement: What Is the Difference? (2026) |
| URL | https://youtu.be/5kUI3xlSHVM |
| Video ID | 5kUI3xlSHVM |
| Duration | 6:53 (413s, `PT6M53S`) |
| Published | 5 August 2026 |
| Article | `/articles/medicare-advantage-vs-medigap/` |

## After upload: what gets built

- [x] Video embedded at the top of the matching article, click-to-play against a
      thumbnail so it costs nothing on page load and sets no cookies until played
      (`youtube-nocookie.com`). Verified: only the thumbnail is requested before a
      click, the player only after.
- [x] `VideoObject` JSON-LD added to that article's `@graph`, including all twelve
      chapters as `Clip` nodes so Google can surface key moments
- [x] Video sitemap extension added to the article's `sitemap.xml` entry
- [ ] Cross-links from the related articles. The articles have no shared
      related-links block, so each needs its own placement. Separate pass.
- [ ] `/videos/` library page, once there are three or more videos

## Next videos

Working down `docs/video-priority-list-2026.md`. Number 3 is the Baptist Health
network video, which is the one no national channel can shoot.
