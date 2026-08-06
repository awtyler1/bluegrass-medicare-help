# Marks up hard words inside article bodies so a reader can tap one and get the
# plain-English meaning without leaving the page. Definitions are read straight
# out of /glossary/ so the two can never drift apart.
import re, os, glob, html
os.chdir('/home/user/bluegrass-medicare-help')

# ---- 1. read the published glossary as the single source of truth -------------
g = open('glossary/index.html', encoding='utf-8').read()
TERMS = {}
for m in re.finditer(r'<article class="gterm" id="t-([^"]+)"[^>]*>\s*<h3>(.*?)</h3>\s*<p class="gdef">(.*?)</p>', g, re.S):
    slug, head, dfn = m.group(1), m.group(2), m.group(3)
    name = re.sub(r'<span class="gaka">.*?</span>', '', head, flags=re.S).strip()
    TERMS[name.lower()] = (slug, name, re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', dfn)).strip())
print('glossary terms available:', len(TERMS))

# ---- 2. the words actually worth interrupting a sentence for ------------------
# phrase -> glossary key. Longest first so the specific beats the general.
WANT = {
 'out-of-pocket maximum': 'out-of-pocket maximum', 'maximum out-of-pocket': 'out-of-pocket maximum',
 'out-of-pocket max': 'out-of-pocket maximum', 'MOOP': 'out-of-pocket maximum',
 'medical underwriting': 'medical underwriting', 'underwriting': 'medical underwriting',
 'guaranteed issue': 'guaranteed issue',
 'late enrollment penalty': 'late enrollment penalty',
 'creditable coverage': 'creditable coverage',
 'prior authorization': 'prior authorization',
 'Annual Notice of Change': 'annual notice of change', 'ANOC': 'annual notice of change',
 'Explanation of Benefits': 'explanation of benefits',
 'Medicare Savings Program': 'medicare savings program',
 'benefit period': 'benefit period',
 'allowed amount': 'allowed amount',
 'excess charges': 'excess charges',
 'step therapy': 'step therapy',
 'star rating': 'star rating',
 'coinsurance': 'coinsurance',
 'deductible': 'deductible',
 'formulary': 'formulary',
 'IRMAA': 'irmaa',
 'copay': 'copay',
 'referral': 'referral',
}
PHRASES = sorted(WANT.keys(), key=len, reverse=True)
CAP = 7          # marks per article, so a page never turns into a field of buttons
SKIP = re.compile(r'</?(a|h1|h2|h3|h4|h5|h6|script|style|button|option|select|textarea)\b', re.I)

def mark(region):
    """Walk the HTML, only ever touching text that is not inside a link, heading or control."""
    parts = re.split(r'(<[^>]+>)', region)
    depth, used, n = 0, set(), 0
    for i, part in enumerate(parts):
        if part.startswith('<'):
            m = SKIP.match(part)
            if m:
                depth += -1 if part.startswith('</') else (0 if part.endswith('/>') else 1)
                depth = max(0, depth)
            continue
        if depth or not part.strip() or n >= CAP:
            continue
        for phrase in PHRASES:
            if n >= CAP: break
            key = WANT[phrase]
            if key in used or key not in TERMS: continue
            slug, name, dfn = TERMS[key]
            pat = re.compile(r'(?<![\w-])(' + re.escape(phrase) + r')(?![\w-])',
                             0 if phrase.isupper() else re.I)
            mm = pat.search(part)
            if not mm: continue
            # an anchor, not a button: with no JS it still takes you to the glossary entry
            btn = ('<a class="gt" href="/glossary/#t-%s" data-n="%s" data-d="%s" aria-expanded="false">%s</a>'
                   % (slug, html.escape(name, quote=True), html.escape(dfn, quote=True), mm.group(1)))
            part = part[:mm.start()] + btn + part[mm.end():]
            used.add(key); n += 1
        parts[i] = part
    return ''.join(parts), n

changed, total = 0, 0
for p in sorted(glob.glob('articles/*/index.html')):
    s = open(p, encoding='utf-8').read()
    if 'class="gt"' in s: continue
    if '<div class="body">' not in s: print('  no body:', p); continue
    start = s.index('<div class="body">')
    end = s.index('</article>') if '</article>' in s else s.index('<nav class="fnav"')
    new, n = mark(s[start:end])
    if not n: continue
    s = s[:start] + new + s[end:]
    # every article needs the shared script for the panel to open
    if '/assets/site.js' not in s:
        s = s.replace('</body>', '<script src="/assets/site.js"></script>\n</body>', 1)
    open(p, 'w', encoding='utf-8').write(s)
    changed += 1; total += n
print('marked %d terms across %d articles' % (total, changed))
