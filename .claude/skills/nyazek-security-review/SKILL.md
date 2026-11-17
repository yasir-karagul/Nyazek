---
name: nyazek-security-review
description: Checklist and procedure for an independent security review of a Nyazek task. Use when a task tagged `security` reaches `in-review`, or when a change touches authentication, authorization, payments, wallet, ledger, personal data, file uploads, dependencies, secrets, infrastructure or CI.
---

# Nyazek security review

**Inputs:** the task ID and file, the diff or files in scope, and the sections of `docs/prd/05-trust/` and the security guide files the task links to.

**Procedure**

1. Map what the change exposes: entry points, data read or written, trust boundaries crossed, privileges used.
2. Work through the checklist. For each item, find the enforcing code; "probably handled elsewhere" is a finding until located.
3. Write the report in the format and location defined in `docs/reviews/README.md`. For each finding give a concrete failure scenario.
4. Do not modify the code under review. Never copy a secret or personal data into the report.

**Checklist**

- **Authentication and sessions:** every non-public entry point authenticates; tokens and sessions expire and can be revoked.
- **Authorization:** enforced server-side on every action; a customer, seller or staff member cannot reach another party's data (check object-level access across sellers and tenants).
- **Input and output:** all external input validated; no injection (SQL, command, template, path); output encoded for its context; uploads checked for type, size and content.
- **Money:** amounts, prices, commissions and balances are computed server-side; operations are idempotent; no client-supplied value is trusted; ledger entries are not editable.
- **Personal data:** collected and exposed only as the PRD allows; absent from logs, errors and analytics; protected in transit and at rest.
- **Secrets:** none in code, configuration files, commits, logs or test fixtures.
- **Dependencies and supply chain:** each new dependency is justified, maintained and pinned; no unreviewed scripts.
- **Abuse:** rate limits and anti-automation where an action can be spammed or enumerated; audit entries exist for sensitive actions.
- **Errors:** failures close safely and reveal nothing useful to an attacker.
- **Infrastructure and CI:** least privilege; no widened network exposure; no check or gate weakened.
