"""Count Page IDs by zone and priority in sitemap.md and write the table into the file.
Usage: python3 count_pages.py <prd-root>"""
import re, sys, os, collections
root = sys.argv[1]
path = os.path.join(root, '09-information-architecture', 'sitemap.md')
text = open(path, encoding='utf-8').read()
ID = re.compile(r'^(SF|SL|AD|SYS)-[A-Z0-9-]+$')
pages = {}
for line in text.split('\n'):
    if line.startswith('|'):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        ids = [c for c in cells if ID.match(c)]
        pris = [c for c in cells if c in ('P0', 'P1', 'P2')]
        if ids and pris: pages.setdefault(ids[0], pris[0])
    m = re.match(r'^#{2,4} .*— ((?:SF|SL|AD|SYS)-[A-Z0-9-]+) \((P[012])\)', line)
    if m: pages.setdefault(m.group(1), m.group(2))
zones = collections.OrderedDict([('SF', 'Storefront (incl. public seller and static pages)'), ('SL', 'Seller Dashboard'), ('AD', 'Admin Panel'), ('SYS', 'System and technical routes')])
count = {z: collections.Counter() for z in zones}
for pid, pri in pages.items(): count[pid.split('-')[0]][pri] += 1
rows = ['| Zone | P0 | P1 | P2 | Total |', '|---|---|---|---|---|']
tot = collections.Counter()
for z, name in zones.items():
    c = count[z]; tot.update(c)
    rows.append(f"| {name} | {c['P0']} | {c['P1']} | {c['P2']} | {sum(c.values())} |")
rows.append(f"| **Total** | **{tot['P0']}** | **{tot['P1']}** | **{tot['P2']}** | **{sum(tot.values())}** |")
table = '\n'.join(rows)
block = '<!--COUNTS-->\n' + table + '\n<!--/COUNTS-->'
if '<!--/COUNTS-->' in text:
    text = re.sub(r'<!--COUNTS-->.*?<!--/COUNTS-->', block, text, flags=re.S)
else:
    text = text.replace('<!--COUNTS-->', block)
open(path, 'w', encoding='utf-8').write(text)
print(table)
