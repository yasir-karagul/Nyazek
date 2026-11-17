import re, os, sys, collections
root = sys.argv[1]
rows = {}
order = []
for d, _, fs in sorted(os.walk(root)):
    for f in sorted(fs):
        if not f.endswith('.md') or f == 'configuration-register.md': continue
        p = os.path.join(d, f); t = open(p, encoding='utf-8').read()
        for m in re.finditer(r'`cfg:([a-z0-9_.*]+)`(?:\s*\(default ([^)]*(?:\([^)]*\))?[^)]*)\))?', t):
            k, dflt = m.group(1), m.group(2)
            rel = os.path.relpath(p, os.path.join(root, '00-governance')).replace(os.sep, '/')
            name = f[:-3]
            if k not in rows:
                rows[k] = [dflt, name, rel]; order.append(k)
            elif dflt and not rows[k][0]:
                rows[k] = [dflt, name, rel]
manual = {
 'buybox.w_price': '40', 'buybox.w_performance': '35', 'buybox.w_delivery': '20', 'buybox.w_1p': '5',
 'identity.session_*': 'customer 30 d sliding; seller 12 h idle / 7 d absolute; admin 30 min idle / 12 h absolute',
 'returns.abuse_proof_threshold': 'set in closed beta', 'returns.abuse_restrict_threshold': 'set in closed beta',
 'shipping.free_threshold': 'set under D-21',
}
owners = collections.OrderedDict([
 ('money','Finance Manager (dual control)'),('events','Super Admin'),('buybox','Catalog Manager + Super Admin'),('search','Catalog Manager'),
 ('catalog','Catalog Manager'),('media','Catalog Manager'),('pricing','Catalog Manager / Finance Manager'),('promo','Marketing Manager'),
 ('cart','Super Admin'),('checkout','Fraud/Risk Manager'),('customers','Super Admin'),('orders','Super Admin (dual control)'),('inventory','Super Admin'),
 ('shipping','Finance Manager (dual control)'),('logistics','Logistics Manager'),('cod','Fraud/Risk Manager; fees and remittance with Finance'),
 ('returns','Super Admin'),('disputes','Super Admin (dual control)'),('reviews','Support lead'),('loyalty','Marketing Manager (dual control for rates)'),
 ('ads','Marketing Manager'),('notifications','Marketing Manager'),('support','Support lead'),('kyc','Seller Manager / Compliance'),
 ('sellers','Seller Manager'),('performance','Seller Manager (dual control)'),('payments','Finance Manager'),('refunds','Finance Manager (dual control)'),
 ('escrow','Finance Manager (dual control)'),('wallet','Finance Manager'),('payout','Finance Manager (dual control)'),('commission','Finance Manager (dual control)'),('content','Content Manager'),('identity','Super Admin'),
 ('risk','Fraud/Risk Manager'),('privacy','Compliance'),('backoffice','Super Admin (dual control)'),('firstparty','Finance Manager with the accountant'),
])
groups = collections.OrderedDict((k, []) for k in owners)
for k in order:
    g = k.split('.')[0]
    groups.setdefault(g, []).append(k)
out = []
out.append("""# Configuration Register

**Authoritative for:** the list of platform configuration values (`cfg:` keys), their proposed defaults and owners. The behaviour each value controls is defined in the linked document, which is authoritative for its meaning.

- Values are stored in the `backoffice` configuration store: typed, validated, audited, with an effective-from time ([admin-governance](../05-trust/admin-governance.md) §5).
- Every default below is a **proposal**. The owner ratifies the set once (D-36 in [open-decisions](open-decisions.md)); values marked "closed beta" are tuned with real data before public launch.
- Many values can be overridden per category, courier, governorate or seller where the linked document says so. Every value can also be overridden per market ([market-expansion](../01-product/market-expansion.md) §3); the defaults below are the Iraq values.
- This file is generated from the `cfg:` markers in the documents and checked in CI: a key used in a document but missing here, or listed here but unused, fails the documentation check.

""")
total = 0
for g, keys in groups.items():
    if not keys: continue
    out.append(f"## `{g}`\n\nOwner: {owners.get(g, 'Super Admin')}\n\n| Key | Proposed default | Defined in |\n|---|---|---|\n")
    for k in keys:
        dflt, name, rel = rows[k]
        dflt = dflt or manual.get(k, '–')
        out.append(f"| `{k}` | {dflt} | [{name}]({rel}) |\n")
        total += 1
    out.append("\n")
out.append(f"Total keys: {total}.\n")
open(os.path.join(root, '00-governance', 'configuration-register.md'), 'w', encoding='utf-8').write(''.join(out))
print("written", total, "keys; groups without owner:", [g for g in groups if g not in owners])
