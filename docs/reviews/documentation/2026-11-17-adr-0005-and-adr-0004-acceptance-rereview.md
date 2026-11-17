# Documentation review — ADR-0005 and the application of ADR-0004's acceptance (re-review)

Date: 2026-11-17 · Reviewer agent: `documentation-reviewer` (fresh context) · Follows up: `docs/reviews/documentation/2026-11-17-adr-0005-and-adr-0004-acceptance.md` (F-DOC-152 to F-DOC-167)

**Scope (uncommitted working tree, current text):** `docs/adr/0005-decision-authority-delegated-to-claude.md` (rewritten); `CLAUDE.md`; `tasks/MASTER_TASKS.md`; `tasks/_TEMPLATE.md`; `tasks/02-architecture/README.md`; `tasks/03-implementation-guide/README.md`; `tasks/04-task-breakdown/README.md`; `docs/implementation-guide/IMPLEMENTATION_STATUS.md`; `docs/prd/06-platform/technology-stack.md`, `architecture.md`, `infrastructure-devops.md`; `docs/prd/00-governance/release-plan.md`. Read for consistency: ADR-0001 to ADR-0004 headers and owner clauses, `open-decisions.md` register, `claude-workflow.md` §4, `security.md` §9, `risks.md` R-02/R-03, the security review `docs/reviews/security/2026-11-17-adr-0005-delegation.md` and its Disposition, the T-0060 report's Disposition (18 questions).

**Tool results**
- `python -I docs/prd/_tools/check_docs.py docs/prd`: 69 files, 0 broken links, 137 `cfg:` keys (the same four "no default" keys as earlier reports), 47 decisions defined, none used but undefined, no duplicate rule IDs, no undefined rule references. Legacy-term counts are in historical or "why we changed" passages only.
- `python -I docs/prd/_tools/check_ia.py docs/prd`: 293 sitemap pages, 293 specified; none missing, extra or duplicated.
- No `cfg:` keys or Page IDs changed.
- Checked by hand: ADR-0005's links (open-decisions, claude-workflow, security, both review reports) resolve; every ID it cites exists (GRD-1 to GRD-11, AGT-1 to AGT-6, claude-workflow §4.1, D-items in point 3.4, T-0015, T-0032, T-0062, T-0063). The point 3.4 list contains every register item whose Owner column names counsel, the accountant, the PSP or Finance (D-12, D-13, D-14, D-20, D-21, D-26, D-37, D-38, D-42, D-43).

**Prior findings**

| Finding | Result |
|---|---|
| F-DOC-152 | Resolved. "Relation to earlier rules" names ADR-0001 d3, ADR-0002 d4 and d7, ADR-0003 d2, d4, d6, ADR-0004 open items and the PRD guardrails; phase opening is stated (point 1); `CLAUDE.md` "Current phase" points to it |
| F-DOC-153 | Resolved by tracking: the table decides until T-0062 aligns the PRD; T-0062 lists every passage named |
| F-DOC-154 | Resolved: `CLAUDE.md` step 5 and "Reviews by risk", MASTER_TASKS header; T-0061 tagged `docs, security, architecture` |
| F-DOC-155 | Resolved: point 3.2 reserves loosening of ADR-0001 to 0003, ADR-0005, `docs/reviews/README.md`, `.claude/`, `CLAUDE.md` rules and review requirements |
| F-DOC-156 | Resolved: Phase 2 README and T-0021 say the next ADR is 0006 |
| F-DOC-157 | Resolved (Phase 2 exit, T-0031, T-0047, T-0053, Phase 3 README, template Plan and Definition of done) |
| F-DOC-158 | Resolved: T-0015 and T-0032 `blocked`; MASTER_TASKS next-task line and `CLAUDE.md` step 2 agree |
| F-DOC-159 | Resolved: §1 sentences, §2 heading and body, §3.8 (DNS in Route 53), §3.9 |
| F-DOC-160 | Resolved in release-plan; claude-workflow tracked in T-0062 |
| F-DOC-161 | Resolved: architecture §2 note on platform tasks and edge components; technology-stack §3.9 "three container deployables and two static apps" |
| F-DOC-162 | Resolved for "Delegated decisions"; a different restated copy in "Nothing unrecorded" has drifted (F-DOC-168) |
| F-DOC-163 | Resolved: point 3.4 lists reserved items by ID; the register's Owner column is tracked in T-0062 |
| F-DOC-164 | Resolved: Consequences list steps 1, 2, 5, 8 and the current rule names |
| F-DOC-165 | Resolved |
| F-DOC-166 | No action (note) |
| F-DOC-167 | Resolved: "Continuous backup + daily snapshots" |

## Verdict

changes required

## Findings

| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|
| F-DOC-168 | major | `CLAUDE.md` rule "Nothing unrecorded"; ADR-0005 point 3.11 | The rule reads "No new dependency, tool, service or datastore without a recorded decision under ADR-0005 (and the owner's approval when it costs money)". ADR-0005 point 3.11 reserves to the owner, whatever the cost, anything that extends Claude's own reach (MCP servers, plugins, skills, GitHub Actions, CI services), any dependency used by protected paths and any package with install scripts, and requires a security review before any other dependency is installed. The `CLAUDE.md` rule omits both and its parenthesis implies that a free tool needs only a recorded decision. This is the session file Claude reads first, and on the control F-SEC-007 rated major it now gives a more permissive answer than the ADR (the drift pattern of F-DOC-162). | Replace the parenthesis with a pointer, for example "…without a recorded decision under ADR-0005; point 3.11 lists what stays with the owner and when a security review is required", without restating the categories. |
| F-DOC-169 | minor | ADR-0005 point 2.4; `claude-workflow.md` §4.1 | Point 2.4 restates its own area list instead of linking the protected-path list, and the copy omits two protected paths: "risk rules" and "security configuration". A change to either does not trigger the mandatory security and architecture reviews unless its tags do. The security review's Disposition (F-SEC-004) says 2.4 was widened to cover the protected paths. | In 2.4, add "any protected path ([claude-workflow](../prd/08-engineering/claude-workflow.md) §4.1)" to the list, or add the two missing items. This tightens the ADR, so point 3.2 allows it. |
| F-DOC-170 | minor | `tasks/MASTER_TASKS.md` T-0061 ("decided by Claude under ADR-0005"); T-0060 report Disposition questions 3, 14, 18; ADR-0005 point 3.2 | The row says all 18 questions are decided by Claude. Three of them include options that loosen an access control, which point 3.2 reserves: question 3 (a role for engineers to reach system health), question 14 (option "remove those step-ups from the specs") and question 18 (owning roles editing settings rather than Super Admin only). A reader of the row alone would treat these as delegated. | Add to the row: "options that loosen an access or dual-control rule (questions 3, 14, 18) are reserved (ADR-0005 point 3.2) and become a `blocked` item if chosen". |

## Not reviewed

- Whether the rewrite of ADR-0005 only tightens the text the owner accepted, as its "Amends" line and the security Disposition say: the earlier text is not in the repository (nothing is committed), so it cannot be compared. Two items are new in the rewrite or settled in the delegating direction: "opening a phase" (point 1) and the table rows that treat ADR-0002 decisions 4 and 7 as delegated, although the earlier text said the rest of ADR-0001 to ADR-0003 "stays in force". They fit the owner's quoted statement, but point 3 says "when in doubt, an item is reserved". The owner's confirmation of the rewritten text in chat would close the question; it is outside the repository.
- `release-plan.md` §1 still says "Each phase ends with an exit review by the owner" for the delivery phases. ADR-0005 does not mention it, so under "when in doubt, reserved" it stays with the owner. Not raised, because the two documents do not conflict.
- `tasks/_TEMPLATE.md` "Risk tags … (decide the reviewers; see `CLAUDE.md`)" does not mention the point 2.4 additions, but it links `CLAUDE.md`, which states them. Not raised.
- `claude-workflow.md` §4.1 names a `finance` risk tag that `CLAUDE.md` does not define. This predates the scope and is left to T-0062.
- `.claude/agents/` and `.claude/skills/` contents were not checked against ADR-0005 point 2.4.

## Disposition (added by the author, 2026-11-17)

| Finding | Disposition |
|---|---|
| F-DOC-168 | Fixed: CLAUDE.md "Nothing unrecorded" points to ADR-0005 instead of restating it |
| F-DOC-169 | Fixed: point 2.4 includes every protected path in claude-workflow §4.1 |
| F-DOC-170 | Fixed: T-0061 row reserves questions 3, 14 and 18 where they loosen access or security rules |
| Not reviewed (rewrite direction) | Settled: the owner confirmed the rewritten ADR-0005 in chat on 2026-11-17 |
