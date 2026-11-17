import re, sys, os, collections
root = sys.argv[1]
files = []
for d, _, fs in os.walk(root):
    for f in fs:
        if f.endswith('.md'): files.append(os.path.join(d, f))
files.sort()
texts = {f: open(f, encoding='utf-8').read() for f in files}
print("files:", len(files), "words:", sum(len(t.split()) for t in texts.values()))

# 1 links
bad = []
for f, t in texts.items():
    for m in re.finditer(r'\]\(([^)]+)\)', t):
        link = m.group(1)
        if link.startswith('http'): continue
        path = link.split('#')[0]
        if not path: continue
        target = os.path.normpath(os.path.join(os.path.dirname(f), path))
        if not os.path.exists(target): bad.append((os.path.relpath(f, root), link))
print("broken links:", len(bad))
for b in bad: print("  ", b)

# 2 cfg keys
cfg = collections.defaultdict(list)
for f, t in texts.items():
    if f.endswith('configuration-register.md'): continue
    for m in re.finditer(r'`cfg:([a-z0-9_.*]+)`(?:\s*\(default ([^)]*(?:\([^)]*\))?[^)]*)\))?', t):
        cfg[m.group(1)].append((os.path.relpath(f, root), m.group(2)))
print("cfg keys:", len(cfg))
for k, v in sorted(cfg.items()):
    defs = set(d for _, d in v if d)
    if len(defs) > 1: print("  CONFLICT", k, defs)
    if len(defs) == 0: print("  no default:", k, [x[0] for x in v])

# 3 terms
terms = ['React Native','Expo','Codex','MCP','MongoDB','Kafka','Redis','PHP','AGENTS.md','ClaudeCode','Gap List','Kubernetes','MinIO','Redpanda','ELK','BigQuery','EAS','Wishlist','wishlist']
for term in terms:
    hits = []
    for f, t in texts.items():
        for i, line in enumerate(t.split('\n'), 1):
            if re.search(r'(?<![A-Za-z])' + re.escape(term) + r'(?![A-Za-z])', line): hits.append((os.path.relpath(f, root), i))
    print(f"term {term!r}: {len(hits)}", hits[:12])

# 4 decisions
reg = texts[[f for f in files if f.endswith('open-decisions.md')][0]]
defined = set(re.findall(r'^\| (D-\d\d) \|', reg, re.M))
used = collections.defaultdict(set)
for f, t in texts.items():
    for d in re.findall(r'(?<![A-Za-z0-9])D-\d\d(?!\d)', t): used[d].add(os.path.relpath(f, root))
print("decisions defined:", len(defined))
print("  used but undefined:", sorted(set(used) - defined))
print("  defined but only in register:", sorted(d for d in defined if used[d] <= {'00-governance/open-decisions.md'}))

# 5 rule ids defined twice (definition = line starting with "- ID " or "| ID |")
defs = collections.defaultdict(list)
for f, t in texts.items():
    for m in re.finditer(r'^(?:- |\| )([A-Z]{2,5}-N?\d+)\b', t, re.M):
        if m.group(1).startswith(('D-','F-','R-','SYS-')): continue
        defs[m.group(1)].append(os.path.relpath(f, root))
dups = {k: v for k, v in defs.items() if len(v) > 1}
print("duplicate rule ids:", dups)
# rule ids referenced but never defined
allids = set()
for f, t in texts.items():
    allids |= set(re.findall(r'\b([A-Z]{2,5}-N?\d+)\b', t))
undefined = sorted(i for i in allids if i not in defs and not i.startswith(('D-','F-','R-','UTF-','SHA-','ISO-','RFC-','CVE-','IQ-','P-','M-','NZ-','ADR-000','SYS-')))
print("referenced but not defined as rule:", undefined)
