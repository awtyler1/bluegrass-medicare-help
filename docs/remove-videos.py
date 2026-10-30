#!/usr/bin/env python3
"""Take every video off the site (October 2026; idempotent).
Removes the click-to-play players, their transcripts, VideoObject schema, the loader scripts and the
video CSS. /videos/ itself is retired with a 301 to /articles/ in vercel.json."""
import glob, json, re

def strip_css(css):
    """Drop rules whose selectors are all video selectors, then any @media block left empty."""
    vid = re.compile(r'\.(?:sc)?vid|\.vtx')
    def rule(m):
        sels = [s for s in re.sub(r'/\*.*?\*/', "", m.group(1), flags=re.S).split(",") if s.strip()]
        return "" if sels and all(vid.search(s) for s in sels) else m.group(0)
    css = re.sub(r'/\* video:.*?\*/\s*', "", css, flags=re.S)
    # a plain rule is a selector list (no @, no braces) followed by one {...} block
    while True:   # repeat: removing the rules inside an @media block leaves it empty for the next pass
        new = re.sub(r'(?:^|(?<=[{};]))([^{}@;]*?)\{[^{}]*\}[ \t]*', rule, css)
        new = re.sub(r'@media[^{]*\{\s*\}[ \t]*\n?', "", new)
        if new == css:
            return css
        css = new

def strip_schema(m):
    d = json.loads(m.group(1))
    g = d.get("@graph")
    if isinstance(g, list):
        d["@graph"] = [n for n in g if n.get("@type") != "VideoObject"]
        for n in d["@graph"]:
            n.pop("video", None)
    elif d.get("@type") == "VideoObject":
        return ""
    compact = '","' in m.group(1)[:200] or '":"' in m.group(1)[:200]
    out = json.dumps(d, ensure_ascii=False, separators=(",", ":")) if compact else json.dumps(d, ensure_ascii=False)
    return '<script type="application/ld+json">' + out + "</script>"

changed = []
for p in sorted(glob.glob("**/index.html", recursive=True)):
    if p.startswith(("mockups/", "dist/", "videos/")):
        continue
    h = open(p, encoding="utf-8").read(); o = h
    # players: article/about figure, schedule section
    h = re.sub(r'<section class="wrap"[^>]*>\s*<figure class="vid">.*?</figure>\s*</section>', "", h, flags=re.S)
    h = re.sub(r'[ \t]*<figure class="vid">.*?</figure>\n?', "", h, flags=re.S)
    h = re.sub(r'[ \t]*<section class="scvid">.*?</section>\n?', "", h, flags=re.S)
    h = re.sub(r'<details class="vtx">.*?</details>\n?', "", h, flags=re.S)
    # click-to-play loaders
    h = re.sub(r'<script>\s*/\*[^*]*\*/\s*\(function\(\)\{\s*var b=document\.getElementById\(\'(?:about|sc)?vid(?:btn)?\'\);.*?</script>\n?', "", h, flags=re.S)
    h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', strip_schema, h, flags=re.S)
    h = re.sub(r'<style>(.*?)</style>', lambda m: "<style>" + strip_css(m.group(1)) + "</style>", h, flags=re.S)
    h = re.sub(r'\s*<p class="lcstart">Prefer to watch\?[^<]*<a href="/videos/">Video Library</a>\.</p>', "", h)
    h = h.replace('<a href="/videos/">Videos</a>', '')
    if h != o:
        open(p, "w", encoding="utf-8").write(h); changed.append(p)

css = open("assets/site.css", encoding="utf-8").read(); new = strip_css(css)
if new != css:
    open("assets/site.css", "w", encoding="utf-8").write(new); changed.append("assets/site.css")
print("pages without video:", len(changed))
