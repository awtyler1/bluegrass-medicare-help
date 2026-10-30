"""2026 header and footer markup (Devoted pattern: phone number plus one primary action).
apply(html) is idempotent; used by update-chrome-v4.py and the page builders."""
import re

TEL = "tel:18597858289"; PN = "(859) 785-8289"
PHONE_SVG_RE = r'<svg class="cta-ico"[^>]*>(?:(?!</svg>).)*?<path d="M22 16\.92.*?</svg>'
FOOT_LINKS = ('<div class="fnav-links"><a href="/articles/">Learning Center</a><a href="/turning-65/">Turning 65</a>'
              '<a href="/kentucky/">Your County</a><a href="/glossary/">Glossary</a>'
              '<a href="/quizzes/">Quizzes</a><a href="/guide/">Free Guide</a><a href="/reviews/">Reviews</a>'
              '<a href="/about/">About</a><a href="/schedule/">Book a free review</a></div>')

def apply(h):
    # header: [phone] [Book a free review]; phone first so desktop reads "number, then the one button"
    m = re.search(r'(\s*)<a class="navbook" href="/schedule/"[^>]*>.*?</a>(\s*)<a class="navcta" href="tel:18597858289"[^>]*>(.*?)</a>', h, re.S)
    if m:
        svg = re.search(PHONE_SVG_RE, m.group(3), re.S)
        icon = svg.group(0) if svg else ""
        new = (f'{m.group(1)}<a class="navcta" href="{TEL}" aria-label="Call {PN}">{icon}<span class="nc-lbl">Call</span>'
               f'<span class="nc-num">{PN}</span></a>{m.group(2)}<a class="navbook" href="/schedule/">Book a free review</a>')
        h = h[:m.start()] + new + h[m.end():]
    h = re.sub(r'<div class="fnav-links">.*?</div>', FOOT_LINKS, h, count=1, flags=re.S)
    return h
