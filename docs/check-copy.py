# Copy checks for anything that ships. Run before publishing.
#   python3 docs/check-copy.py
#
# Hard failures are things that would go out wrong:
#   - British spellings in US consumer copy ("enrol" for "enroll")
#   - em dashes inside a fenced block in docs/, since those blocks are copy meant
#     to be pasted into YouTube, a blog editor or a Word doc
# Em dashes already sitting in older HTML are reported as a backlog count, not a
# failure, so this stays useful instead of always red.
import re, sys, glob, os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

BRITISH = (r'\b(enrol|enrols|enrolment|realise\w*|organise\w*|recognise\w*|colour\w*|'
           r'behaviour\w*|honour\w*|favourite|normalise\w*|prioritise\w*|apologise\w*|'
           r'summarise\w*|categorise\w*|minimise\w*|maximise\w*|licence|practise|'
           r'centre|cheque)\b')

ALLOW = {'docs/check-copy.py', 'docs/youtube-video-playbook.md'}  # these state the rule

def strip_code(t):
    return re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)

fails = 0
html = [p for p in glob.glob('**/*.html', recursive=True) if not p.startswith('mockups/')]
docs = sorted(glob.glob('docs/*.md'))

for p in html + docs:
    body = strip_code(open(p, encoding='utf-8').read())
    if p in ALLOW:
        continue
    for m in re.finditer(BRITISH, body, re.I):
        print('BRITISH SPELLING  %s:%d  "%s"'
              % (p, body[:m.start()].count('\n') + 1, m.group(0)))
        fails += 1

# paste-ready blocks in docs must be spotless
for p in docs:
    text = open(p, encoding='utf-8').read()
    for m in re.finditer(r'```.*?```', text, re.S):
        block = m.group(0)
        # diagrams and code are not copy anyone pastes into a publishing box
        if re.search(r'[\u2500-\u257f]', block) or block.lstrip('`').startswith(('html', 'js', 'python', 'css')):
            continue
        n = block.count('—') + block.count('&mdash;')
        if n:
            print('EM DASH IN PASTE BLOCK  %s:%d  x%d'
                  % (p, text[:m.start()].count('\n') + 1, n))
            fails += n

legacy = sum(strip_code(open(p, encoding='utf-8').read()).count('—') for p in html)
pages = sum(1 for p in html if '—' in strip_code(open(p, encoding='utf-8').read()))

print('checked %d files. %d failures.' % (len(html) + len(docs), fails))
print('backlog: %d em dashes across %d published pages (pre-existing, not a failure)'
      % (legacy, pages))
sys.exit(1 if fails else 0)
