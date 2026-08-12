import re, json, os, html as _html
os.chdir('/home/user/bluegrass-medicare-help')
TX = json.load(open('docs/video-transcripts.json', encoding='utf-8'))

def transcript_html(vid, heading_id):
    """Progressive-disclosure transcript. The text lives in the raw HTML either
    way, so crawlers and AI retrieval get it whether or not anyone expands it."""
    t = TX.get(vid)
    if not t: return ''
    paras = ''.join('<p>%s</p>' % _html.escape(x) for x in t['paras'])
    return ('<details class="vtx"><summary id="%s">Read the transcript</summary>'
            '<div class="vtxbody"><p class="vtxnote">Lightly edited for readability.</p>'
            '%s</div></details>' % (heading_id, paras))
src = open('articles/index.html', encoding='utf-8').read()

def grab(pat):
    m = re.search(pat, src, re.S)
    assert m, 'NO MATCH: ' + pat
    return m.group(0)

USTRIP = grab(r'<div class="ustrip".*?</div>\s*</div>')
NAV    = grab(r'<nav class="nav".*?</nav>')
# the source page marks itself active; strip that so /videos/ does not claim to be /articles/
NAV    = NAV.replace(' class="active" aria-current="page"', '')
NAV    = NAV.replace('<a href="/videos/">Videos</a>',
                     '<a href="/videos/" class="active" aria-current="page">Videos</a>')
FNAV   = grab(r'<nav class="fnav".*?</nav>')
FOOT   = grab(r'<footer class="foot".*?</footer>')
PIX    = grab(r'<script>\s*!function\(f,b,e,v,n,t,s\).*?</noscript>')
GA     = grab(r'<script async src="https://www\.googletagmanager\.com.*?</script>\s*<script>\s*window\.dataLayer.*?</script>')
FONTS  = grab(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?rel="stylesheet">')
m = re.search(r'<script>[^<]*navtog.*?</script>', src, re.S)
NAVJS = m.group(0) if m else ''

VIDEOS = [
 dict(id='Fl0OClAwgj8', title="Medicare Annual Notice of Change (2026): Don't Throw It Away",
      dur='1:37', iso='PT1M37S', date='2026-08-12', shown='August 12, 2026',
      blurb='Your plan has to mail it by September 30, and it is the one letter that says exactly what changes in January. Ignore it and you find out at the pharmacy counter.',
      art='/articles/medicare-annual-enrollment-period/'),
 dict(id='Qoee2FUy7LY', title='Do You Need a Medicare Advisor? What You Actually Get',
      dur='2:05', iso='PT2M5S', date='2026-08-10', shown='August 10, 2026',
      blurb='On your own it is a weekend of cross-checking drug lists and networks. With an advisor it is about 30 minutes, and it costs nothing either way.',
      art='/articles/what-is-a-medicare-advisor/'),
 dict(id='NfmmHa-sN0M', title='Turning 65? What You Need to Know About Medicare',
      dur='3:11', iso='PT3M11S', date='2026-08-06', shown='August 6, 2026',
      blurb='The seven-month window, whether you can delay if you are still working, the three ways to sign up, and what Part A and Part B each cover.',
      art='/articles/turning-65-enrollment-window/'),
 dict(id='5kUI3xlSHVM', title='Medicare Advantage vs. Medicare Supplement: What Is the Difference?',
      dur='6:53', iso='PT6M53S', date='2026-08-05', shown='August 5, 2026',
      blurb='Medicare covers 80% of your Part B costs and Original Medicare caps nothing. Two very different answers to that one problem, and the trade-offs both ways.',
      art='/articles/medicare-advantage-vs-medigap/'),
 dict(id='tsKZm1X8wEo', title='What Does It Cost to Work with a Medicare Advisor?',
      dur='1:01', iso='PT1M1S', date='2026-08-04', shown='August 4, 2026',
      blurb='Nothing. The commission is already built into plan pricing whether you use an advisor or not, so the premium is the same either way.',
      art='/articles/free-medicare-help-lexington-ky/'),
]

HERO_SVG = '''<svg class="heroart" viewBox="0 0 520 300" role="img" aria-label="Illustration of a person watching a short Medicare video on a screen">
        <ellipse cx="260" cy="272" rx="196" ry="15" fill="#e2d9c8" opacity=".75"/>
        <rect x="118" y="52" width="284" height="176" rx="14" fill="#2a2620"/>
        <rect x="130" y="64" width="260" height="140" rx="7" fill="#faf6ef"/>
        <rect x="150" y="86" width="118" height="11" rx="5.5" fill="#e2d9c8"/>
        <rect x="150" y="106" width="86" height="9" rx="4.5" fill="#efe6d6"/>
        <circle cx="308" cy="134" r="35" fill="#d05528"/>
        <path d="M299 118 L328 134 L299 150 Z" fill="#faf6ef"/>
        <rect x="150" y="170" width="180" height="7" rx="3.5" fill="#efe6d6"/>
        <rect x="150" y="170" width="74" height="7" rx="3.5" fill="#3a7d52"/>
        <rect x="228" y="228" width="64" height="26" rx="5" fill="#2a2620"/>
        <rect x="196" y="252" width="128" height="10" rx="5" fill="#1f1d1a"/>
        <circle cx="72" cy="150" r="27" fill="#efe6d6" stroke="#d05528" stroke-width="3"/>
        <circle cx="72" cy="141" r="10" fill="#5f594f"/>
        <path d="M55 168c3-11 9-16 17-16s14 5 17 16z" fill="#5f594f"/>
        <path d="M432 96c14 0 24 10 24 23s-10 23-24 23h-4l-13 11v-11h-3c-14 0-24-10-24-23s10-23 24-23z" fill="#3a7d52"/>
        <circle cx="422" cy="119" r="3.4" fill="#faf6ef"/><circle cx="433" cy="119" r="3.4" fill="#faf6ef"/><circle cx="444" cy="119" r="3.4" fill="#faf6ef"/>
      </svg>'''

cards = []
for i, v in enumerate(VIDEOS):
    cards.append('''        <article class="vcard">
          <button class="vthumb" id="vb{i}" type="button" data-vid="{id}" data-title="{title}"
            aria-label="Play the video, {title}, {dur}">
            <img src="https://i.ytimg.com/vi/{id}/maxresdefault.jpg" alt="" width="1280" height="720"
              loading="lazy" decoding="async"
              onerror="this.onerror=null;this.src='https://i.ytimg.com/vi/{id}/hqdefault.jpg';">
            <span class="vplay" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>
            <span class="vdur">{dur}</span>
          </button>
          <div class="vbody">
            <h2>{title}</h2>
            <p class="vdate">{shown}</p>
            <p class="vblurb">{blurb}</p>
            <a class="vread" href="{art}">Read the full article<span aria-hidden="true"> &rarr;</span></a>
            {tx}
          </div>
        </article>'''.format(i=i, tx=transcript_html(v['id'], 'tx%d' % i), **v))

items = []
for i, v in enumerate(VIDEOS, 1):
    items.append({"@type": "ListItem", "position": i, "item": {
        "@type": "VideoObject", "name": v['title'], "description": v['blurb'],
        "thumbnailUrl": ["https://i.ytimg.com/vi/%s/maxresdefault.jpg" % v['id']],
        "uploadDate": v['date'], "duration": v['iso'],
        "embedUrl": "https://www.youtube.com/embed/" + v['id'],
        "contentUrl": "https://youtu.be/" + v['id'],
        "url": "https://bluegrassmedicarehelp.com" + v['art'],
        "publisher": {"@type": "Organization", "name": "Tyler Insurance Group"},
        "creator": {"@type": "Person", "@id": "https://bluegrassmedicarehelp.com/#austin-tyler",
                    "name": "Austin Tyler"},
        "transcript": " ".join(TX[v['id']]['paras']) if v['id'] in TX else None}})
    if items[-1]['item']['transcript'] is None: del items[-1]['item']['transcript']

graph = {"@context": "https://schema.org", "@graph": [
  {"@type": "CollectionPage", "@id": "https://bluegrassmedicarehelp.com/videos/",
   "url": "https://bluegrassmedicarehelp.com/videos/", "name": "Medicare Video Library",
   "description": "Short, plain-English Medicare videos from Austin Tyler, a licensed local agent in Lexington, Kentucky.",
   "isPartOf": {"@type": "WebSite", "@id": "https://bluegrassmedicarehelp.com/#website",
                "name": "Bluegrass Medicare Help", "url": "https://bluegrassmedicarehelp.com/"},
   "inLanguage": "en-US"},
  {"@type": "ItemList", "name": "Medicare videos",
   "itemListOrder": "https://schema.org/ItemListOrderDescending",
   "numberOfItems": len(VIDEOS), "itemListElement": items},
  {"@type": "BreadcrumbList", "itemListElement": [
   {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://bluegrassmedicarehelp.com/"},
   {"@type": "ListItem", "position": 2, "name": "Videos", "item": "https://bluegrassmedicarehelp.com/videos/"}]}]}

CSS = '''<style>
/* base (site.css supplies tokens + header/footer chrome only) */
*{margin:0;padding:0;box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;}
body{font-family:var(--sans);color:var(--ink);background:var(--cream);line-height:1.65;-webkit-font-smoothing:antialiased;}
img{max-width:100%;display:block;}
a{color:var(--coral-d);text-decoration:none;}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px;}
.foot{background:var(--dark);color:#9a948c;padding:30px 0 36px;font-size:13px;line-height:1.7;margin-top:48px;}
.foot .fnm{color:var(--cream);font-weight:600;font-size:15px;margin-bottom:6px;font-family:var(--serif);}
.foot a{color:#bdb6ac;}
.foot .disc{margin-top:14px;padding-top:14px;border-top:1px solid #333;color:#918b80;font-size:12px;}
.crumb{padding:18px 0 0;font-size:15px;}
/* hero */
.vhero{background:var(--cream2);border-bottom:1px solid var(--line);padding:40px 0;margin-top:16px;}
.vhero .wrap{display:grid;grid-template-columns:1.12fr .88fr;gap:34px;align-items:center;}
.vhero h1{font-family:var(--serif);font-weight:500;font-size:46px;line-height:1.08;letter-spacing:-1px;color:var(--ink);margin-bottom:14px;}
.vhero p{font-size:19px;color:var(--mute);max-width:520px;}
.heroart{width:100%;height:auto;}
/* cards */
.vlist{padding:44px 0 10px;}
.vgrid{display:grid;grid-template-columns:repeat(2,1fr);gap:30px;}
.vcard{background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;display:flex;flex-direction:column;}
.vthumb{display:block;position:relative;width:100%;padding:0;border:0;background:var(--dark);cursor:pointer;}
.vthumb img{width:100%;height:auto;display:block;opacity:.88;transition:opacity .25s ease;}
.vthumb:hover img,.vthumb:focus-visible img{opacity:1;}
.vthumb:focus-visible{outline:3px solid var(--coral);outline-offset:-3px;}
.vplay{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:64px;height:64px;border-radius:50%;
  background:var(--coral);display:flex;align-items:center;justify-content:center;box-shadow:0 8px 24px rgba(0,0,0,.35);transition:background .2s ease;}
.vplay svg{width:25px;height:25px;margin-left:4px;fill:#fff;}
.vthumb:hover .vplay,.vthumb:focus-visible .vplay{background:var(--coral-d);}
.vdur{position:absolute;right:11px;bottom:11px;background:rgba(20,18,15,.86);color:#fff;font-size:13.5px;font-weight:700;padding:3px 9px;border-radius:5px;}
.vframe{position:relative;width:100%;aspect-ratio:16/9;background:#000;}
.vframe iframe{position:absolute;inset:0;width:100%;height:100%;border:0;}
.vbody{padding:22px 24px 24px;display:flex;flex-direction:column;flex:1;}
.vbody h2{font-family:var(--serif);font-weight:600;font-size:23px;line-height:1.24;color:var(--ink);}
.vdate{font-size:14.5px;color:var(--faint);margin-top:6px;}
.vblurb{font-size:16.5px;color:var(--mute);margin-top:11px;}
.vread{display:inline-block;margin-top:auto;padding-top:16px;font-weight:700;font-size:16.5px;}
.vread:hover{text-decoration:underline;}
/* closing call to action */
.vcta{margin:46px 0 0;background:var(--warm);border:1px solid var(--line);border-radius:18px;padding:34px 30px;text-align:center;}
.vcta h2{font-family:var(--serif);font-weight:600;font-size:29px;color:var(--ink);margin-bottom:10px;}
.vcta p{font-size:17.5px;color:var(--mute);max-width:620px;margin:0 auto 20px;}
.vbtns{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;}
.vbtn{display:inline-flex;align-items:center;gap:9px;background:var(--coral);color:#fff;font-weight:700;font-size:17px;padding:15px 26px;border-radius:11px;}
.vbtn:hover{background:var(--coral-d);}
.vbtn.alt{background:var(--green);}
.vbtn.alt:hover{filter:brightness(.92);}
.vnote{font-size:14px;color:var(--faint);text-align:center;margin:26px 0 0;font-style:italic;}
@media(max-width:900px){
  .vhero .wrap{grid-template-columns:1fr;gap:22px;} .vhero h1{font-size:34px;}
  .heroart{max-width:420px;margin:0 auto;}
  .vgrid{grid-template-columns:1fr;}
}
@media(prefers-reduced-motion:reduce){.vthumb img{transition:none;}}
</style>'''

PLAYER_JS = '''<script>
/* each card loads its player only when someone presses play */
(function(){
  Array.prototype.forEach.call(document.querySelectorAll('.vthumb'), function(b){
    b.addEventListener('click', function(){
      var d=document.createElement('div');
      d.className='vframe';
      var f=document.createElement('iframe');
      f.src='https://www.youtube-nocookie.com/embed/'+b.getAttribute('data-vid')+'?autoplay=1&rel=0';
      f.title=b.getAttribute('data-title');
      f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      f.setAttribute('allowfullscreen','');
      d.appendChild(f);
      b.parentNode.replaceChild(d, b);
      if(typeof gtag==='function'){gtag('event','video_play',{video_title:b.getAttribute('data-title')});}
    });
  });
})();
</script>'''

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<link rel="icon" type="image/png" href="/assets/logo-mark.png">
<link rel="apple-touch-icon" href="/assets/logo-mark.png">
<meta name="theme-color" content="#1f1d1a">
''' + PIX + '\n' + GA + '''
<title>Medicare Videos: Plain-English Answers from a Lexington Agent | Bluegrass Medicare Help</title>
<meta name="description" content="Short Medicare videos from Austin Tyler, a licensed agent in Lexington, Kentucky. Turning 65, Medicare Advantage vs. Supplement, and what working with an advisor costs. Each one paired with the full written guide.">
''' + FONTS + '''
<link rel="stylesheet" href="/assets/site.css">
<link rel="canonical" href="https://bluegrassmedicarehelp.com/videos/">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bluegrass Medicare Help">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="Medicare Videos: Plain-English Answers from a Lexington Agent">
<meta property="og:description" content="Short Medicare videos from a licensed local agent in Lexington, Kentucky. Each one paired with the full written guide.">
<meta property="og:url" content="https://bluegrassmedicarehelp.com/videos/">
<meta property="og:image" content="https://bluegrassmedicarehelp.com/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Medicare Videos: Plain-English Answers from a Lexington Agent">
<meta name="twitter:description" content="Short Medicare videos from a licensed local agent in Lexington, Kentucky.">
<meta name="twitter:image" content="https://bluegrassmedicarehelp.com/assets/og-image.png">
<script type="application/ld+json">''' + json.dumps(graph, ensure_ascii=False) + '''</script>
''' + CSS + '''
</head>
<body>
''' + USTRIP + '\n' + NAV + '''

<main id="main">
  <div class="wrap"><p class="crumb"><a href="/">&larr; Home</a></p></div>

  <section class="vhero">
    <div class="wrap">
      <div>
        <h1>Medicare, explained out loud.</h1>
        <p>Short videos on the questions people actually call about, from a licensed agent here in Lexington. Every one is paired with the full written guide, so you can watch it, read it, or both.</p>
      </div>
      ''' + HERO_SVG + '''
    </div>
  </section>

  <section class="vlist">
    <div class="wrap">
      <div class="vgrid">
''' + '\n'.join(cards) + '''
      </div>

      <section class="vcta">
        <h2>Still have a question?</h2>
        <p>If your question is not answered above, ask it. There is no cost, and no obligation to change anything.</p>
        <div class="vbtns">
          <a class="vbtn" href="/schedule/">Book a free 30-minute review</a>
          <a class="vbtn alt" href="tel:18596186443">Call (859) 618-6443</a>
        </div>
      </section>

      <p class="vnote">New videos are added as they are recorded. Nothing here is a plan recommendation; it is general Medicare education.</p>
    </div>
  </section>
</main>

''' + FNAV + '\n' + FOOT + '\n' + PLAYER_JS + '\n' + NAVJS + '''
</body>
</html>
'''
os.makedirs('videos', exist_ok=True)
open('videos/index.html', 'w', encoding='utf-8').write(html)
print('written videos/index.html bytes=%d  navjs=%s' % (len(html), bool(NAVJS)))
