"""Walk the visible author text of a page (skipping reader-voice and verbatim contexts) for the firm-voice rewrite."""
import re

VOID = {'br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'wbr', 'area', 'base', 'col', 'embed', 'param', 'track'}
SKIP_TAGS = {'script', 'style', 'svg', 'head', 'blockquote', 'q', 'label', 'button', 'option', 'summary', 'textarea', 'select', 'title', 'h3', 'cite', 'em', 'i'}
# reader voice, verbatim reviews and transcripts, quiz and form UI, and the legal footer stay as they are
SKIP_CLASS = {'rcard', 'rev', 'vtx', 'vtxbody', 'kcheck', 'kc-q', 'consent', 'fineprint', 'disc', 'disclaim',
              'quiz', 'qopt', 'opt', 'choice', 'chip', 'rq', 'review', 'gquote', 'testimonial', 'stamp', 'sources', 'foot',
              'tsc', 'transcript', 'vidmeta', 'vmeta', 'byline', 'meta', 'author'}
BLOCK = {'p', 'li', 'h1', 'h2', 'h4', 'div', 'td', 'th', 'section', 'article', 'figcaption', 'dd', 'dt'}
TOK = re.compile(r'(<!--.*?-->|<[^>]+>)', re.S)

def walk(html, fn):
    """Apply fn(text, ctx) to each visible author-voice text node; ctx carries sentence-start state."""
    out = []; stack = []; ctx = {"start": True}
    for part in TOK.split(html):
        if not part: continue
        if part.startswith("<!--"): out.append(part); continue
        if part.startswith("<"):
            m = re.match(r'<\s*(/)?\s*([a-zA-Z0-9]+)([^>]*)>', part)
            if m:
                closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
                if tag in VOID or attrs.rstrip().endswith("/"):
                    out.append(part); continue
                if closing:
                    while stack:
                        t = stack.pop()[0]
                        if t == tag: break
                else:
                    cls = set((re.search(r'class="([^"]*)"', attrs) or [None, ""])[1].split())
                    parent_q = bool(stack) and stack[-1][0] == 'div' and stack[-1][2]
                    skip = tag in SKIP_TAGS or bool(cls & SKIP_CLASS) or (tag in ('b', 'strong', 'dt') and parent_q)
                    stack.append((tag, skip, 'q' in cls))
                if tag in BLOCK or tag in ('h3', 'br'): ctx["start"] = True
            out.append(part); continue
        if any(e[1] for e in stack) or not stack:
            out.append(part); continue
        out.append(fn(part, ctx))
    return "".join(out)
