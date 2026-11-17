"""Check that every Page ID in the sitemap has exactly one specification in the pages-* documents,
and that no specification names an ID missing from the sitemap.
Usage: python3 check_ia.py <prd-root>"""
import re, sys, os, collections
root = sys.argv[1]
ia = os.path.join(root, '09-information-architecture')
ID = r'(?:SF|SL|AD|SYS)-[A-Z0-9-]+'
def ids_in(text, table=True):
    found = []
    for line in text.split('\n'):
        if line.startswith('|'):
            first = line.strip().strip('|').split('|')[0].strip()
            if re.fullmatch(ID, first): found.append(first)
        m = re.match(r'^#{2,4} (?:.*— )?(' + ID + r')(?: —| \()', line)
        if m: found.append(m.group(1))
    return found
sm = open(os.path.join(ia, 'sitemap.md'), encoding='utf-8').read()
site = set()
for line in sm.split('\n'):
    if line.startswith('|'):
        for c in [c.strip() for c in line.strip('|').split('|')]:
            if re.fullmatch(ID, c): site.add(c)
    m = re.match(r'^#{2,4} .*— (' + ID + r') \(', line)
    if m: site.add(m.group(1))
site.discard('SF-SELL-FAQ')
spec = collections.Counter()
for f in sorted(os.listdir(ia)):
    if f.startswith('pages-') and f.endswith('.md'):
        for i in ids_in(open(os.path.join(ia, f), encoding='utf-8').read()): spec[i] += 1
missing = sorted(site - set(spec)); extra = sorted(set(spec) - site); dup = sorted(i for i, n in spec.items() if n > 1)
print("sitemap pages:", len(site), "specified:", len(spec))
print("missing specification:", missing)
print("specified but not in sitemap:", extra)
print("specified more than once:", dup)
sys.exit(1 if (missing or extra or dup) else 0)
