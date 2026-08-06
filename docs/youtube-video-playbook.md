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

## Video: "What Does It Cost to Work with a Medicare Advisor" (1:01)

Published 4 August 2026 | https://youtu.be/tsKZm1X8wEo | ID `tsKZm1X8wEo` | 1:01
Campaign slug: `advisor-cost`

This one answers an objection rather than teaching a topic, so the primary link is
the booking page, not an article. Reverse of the usual order.

**No chapters.** YouTube needs at least three and the video is 61 seconds. Three
chapter marks on a one minute video is clutter, and the key-moments benefit in search
is nil at that length.

**Length.** Roughly 1,200 characters. A one minute video does not earn a 2,700
character description, and padding it out with keywords readers will not see is the
kind of thing that makes a channel look automated.

### Description (paste as-is)

```
What does it cost to sit down with a Medicare advisor? Not a penny. No checkbook, no
bill, ever.

Book a free 30-minute review: https://bluegrassmedicarehelp.com/schedule/?utm_source=youtube&utm_medium=video&utm_campaign=advisor-cost

Here is how that works. Independent Medicare advisors are paid a commission by the
insurance company you enroll with, and that commission is already built into the
plan's pricing whether you use an advisor or not. The premium is the same either way.
So the choice is not "pay for help or save money." It is "use the help that is
already paid for, or leave it on the table."

What you actually get for it: someone who sits down with your current situation, your
doctors, and your prescriptions, and points you toward the plan that fits, acting as
an advocate between you and the insurance company.

More free Medicare help in Lexington, including the state's SHIP counselors and other
resources that cost nothing: https://bluegrassmedicarehelp.com/articles/free-medicare-help-lexington-ky/?utm_source=youtube&utm_medium=video&utm_campaign=advisor-cost

Or call the office at (859) 618-6443.

Austin Tyler is a licensed insurance agent with Tyler Insurance Group, a local
Medicare advisory firm in Lexington, Kentucky.

#Medicare #MedicareHelp #Turning65

We respect your privacy. This is a solicitation for insurance. Tyler Insurance
Group is not connected with or endorsed by the United States government or the
federal Medicare program. We do not offer every plan available in your area.
Currently we represent 6 organizations which offer 158 products in your area.
Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance
Program (SHIP) to get information on all of your options.
```

### Tags

`what does a medicare advisor cost, medicare agent fees, is a medicare broker free,
how do medicare agents get paid, medicare broker commission, free medicare help,
independent medicare agent, medicare advisor lexington ky, medicare help kentucky`

### Two compliance notes on this one

**"Contracted with most large carriers in the state of Kentucky and really the nation
as a whole."** This sits in tension with the disclaimer the same description carries,
which states we represent 6 organizations and do not offer every plan in the area.
Breadth-of-representation claims are exactly what CMS looks at in agent marketing.
The disclaimer resolves it in writing, but the safer spoken line in future videos is
something like "we are contracted with the major carriers serving this area," with
the specific count left to the disclaimer.

**"Unbiased as possible."** An advisor paid by carriers describing the advice as
unbiased is a claim worth softening. "Independent" and "we represent you, not one
carrier" say the same thing without asserting an absence of incentive that the
compensation model does not support. The description above uses "advocate," which is
the word from the video that carries no such claim.

Neither is worth a re-shoot on a 61 second video. Both are worth adjusting in the
next one.

### Where it is embedded

- `/articles/free-medicare-help-lexington-ky/`, under the heading "And the free help
  that comes with a sales angle: agents like me". Placed there rather than at the top
  of the article on purpose: that article's whole credibility rests on leading with
  the government counsellors who have no sales angle, so a video about hiring an
  agent belongs in the section that owns that trade-off, not above it.
- `/schedule/`, as "What does this cost?" between the badge row and the FAQ. Below
  the calendar, so the booking widget is still the first thing on the page.

Full `VideoObject` schema and the sitemap video entry live on the article only. Two
pages claiming to be the canonical home of one video splits the signal, so the
schedule page carries a plain embed.

### Accuracy note

The description says commissions are built into plan pricing so the premium is the
same either way. That is correct, and for Medicare Advantage and Part D the maximum
commission is set by CMS. Medigap commissions are not CMS-set, they are regulated at
state level, so the description avoids attributing the rate-setting to CMS.

## Video: Turning 65 overview

Published 6 August 2026 | https://youtu.be/NfmmHa-sN0M | ID `NfmmHa-sN0M` | 3:11
Campaign slug: `turning-65`

Embedded at the top of `/articles/turning-65-enrollment-window/` (canonical, with the
`VideoObject`, nine chapters as `Clip` nodes, and the sitemap video entry) and inside
the "There is a window around your 65th birthday" band on `/turning-65/` as a plain
embed, directly under the paragraph it illustrates.

### Title

> **Turning 65? What You Need to Know About Medicare (2026)**

"Turning 65" is the phrase this audience actually types, so it leads. 54 characters,
so nothing truncates anywhere. The year gives a reason to re-shoot it annually.

Alternative if a longer-tail angle is wanted:
**Turning 65 and Medicare: When to Enroll and What It Costs (2026)**

### Where it goes

1. **`/articles/turning-65-enrollment-window/`** as the canonical home. The article is
   "When to Sign Up for Medicare: Your 7-Month Initial Enrollment Period" and already
   covers the window, working past 65, and the lifetime penalty, which is the spine of
   the video. Full `VideoObject` plus the sitemap video entry go here.
2. **`/turning-65/`** as a plain embed. It is the destination behind "Turning 65?" in
   the nav and it is a conversion page, so a video of Austin explaining the window is
   worth more there than anywhere else on the site for trust.

As before, schema on one page only so nothing splits the signal.

### Description (paste as-is)

Three links rather than the usual two, because the video makes two explicit promises
("I wrote the full turning 65 guide, I'm gonna link that below" and "on our website
there's a link where you can do a deeper dive in these key differences") and then
gives a phone CTA. Every link answers something said out loud.

```
Turning 65 in the next year? You get a seven-month window to enroll in Medicare with
no penalty and no gap in coverage, and it opens three months before your birthday
month, not on it.

The full write-up on the window: https://bluegrassmedicarehelp.com/articles/turning-65-enrollment-window/?utm_source=youtube&utm_medium=video&utm_campaign=turning-65

Here is what this video covers.

First, whether you even need to take Medicare at 65. If you are still working and have
qualifying coverage, or you are on a working spouse's coverage, you can usually delay
without a penalty.

If you do need to enroll, the window is three months before your 65th birthday month,
the birth month itself, and three months after. Enroll in the first three months and
your coverage starts the first day of your birth month. It pays to be proactive here.
There are three ways to sign up: call Social Security, visit a local office, or do it
online, which takes most of our clients 15 to 20 minutes.

Then there is what you are actually enrolling in. Part A is your hospital coverage,
and for most people over 65 it costs nothing each month, because you already paid for
it through payroll taxes during your working life. Part B is your medical coverage,
anything outside the hospital, and the standard premium is $202.90 a month in 2026.
Higher earners pay more, and some state programs will cover it for you. If you are
already drawing Social Security, it comes straight out of your check.

Last, the decision nobody warns you about: Medicare Advantage or a Medicare Supplement.
There are real trade-offs both ways, and it is worth understanding before you pick.

The deeper dive on Advantage vs. Supplement: https://bluegrassmedicarehelp.com/articles/medicare-advantage-vs-medigap/?utm_source=youtube&utm_medium=video&utm_campaign=turning-65

CHAPTERS
0:00 Do you have to take Medicare at 65, or can you delay?
0:25 Your seven-month enrollment window
0:42 Why to enroll three months early
1:01 Three ways to sign up, and the fastest one
1:20 Part A: your hospital coverage
1:44 Part B: your medical coverage and what it costs in 2026
2:11 How the premium comes out of your Social Security check
2:31 Advantage or Supplement: the next decision
2:42 Where to get help

Want someone to look at your situation? Call the office at (859) 618-6443, or book a
free 30-minute review: https://bluegrassmedicarehelp.com/schedule/?utm_source=youtube&utm_medium=video&utm_campaign=turning-65

Austin Tyler is a licensed insurance agent with Tyler Insurance Group, a local
Medicare advisory firm on Beaumont Circle in Lexington, Kentucky.

#Medicare #Turning65 #MedicareEnrollment

We respect your privacy. This is a solicitation for insurance. Tyler Insurance
Group is not connected with or endorsed by the United States government or the
federal Medicare program. We do not offer every plan available in your area.
Currently we represent 6 organizations which offer 158 products in your area.
Please contact Medicare.gov, 1-800-MEDICARE, or your local State Health Insurance
Program (SHIP) to get information on all of your options.
```

### Chapters

Eleven source beats merged into nine. The 2:35 guide mention and the 2:59 office
sign-off fold into neighbouring chapters rather than getting their own marks, since
neither is something a viewer would skip to. Shortest gap is 11 seconds against
YouTube's 10 second minimum, first mark is 0:00, so the list is valid.

### Tags

`turning 65 medicare, medicare when you turn 65, what to do when you turn 65,
medicare enrollment period, 7 month enrollment window medicare, medicare part a and
part b explained, part b premium 2026, do i need medicare if i am still working,
how to enroll in medicare online, medicare help lexington ky`

### Accuracy check

- **$202.90 Part B premium for 2026** matches the figure used in 47 places across this
  site. Consistent, and correctly framed in the video as the standard premium with
  higher earners paying more.
- **Part A at no cost** is right for people with 40 quarters of Medicare-covered work.
  The video says "typically," which covers the exception.
- **The seven-month window** and **coverage starting the first day of the birth month**
  are both correct. One edge case not mentioned and not worth a re-shoot: if a birthday
  falls on the 1st of a month, Medicare treats it as the prior month, so the window and
  the start date shift back by one.

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
- [x] `/videos/` library page, live at `/videos/`

## The video library

`/videos/` lists every video newest first, each card playing in place (click-to-play,
nocookie) with a link through to the matching article. Linked from the footer nav on
every page and from the top of the Learning Center.

Schema is `CollectionPage` + `ItemList` of `VideoObject`, and each item's `url` points
at the **article**, not at `/videos/`. The library is a front door; the articles are
what should rank.

**Adding a video:** add a `.vcard` block to the `.vgrid` in `/videos/index.html`
(newest first), add the matching entry to the `ItemList` in the JSON-LD, bump
`numberOfItems`, and give the new button a unique `id`. The player script binds to
every `.vthumb`, so nothing else needs touching.

## Next videos

Working down `docs/video-priority-list-2026.md`. Number 3 is the Baptist Health
network video, which is the one no national channel can shoot.
