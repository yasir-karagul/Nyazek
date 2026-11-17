# Security review — ADR-0005: Decision authority delegated to Claude (second re-review)
Date: 2026-11-17 · Reviewer agent: `security-reviewer` (fresh context) · Scope: narrow re-review of the current working-tree text of `docs/adr/0005-decision-authority-delegated-to-claude.md` points 2.4 and 3.2; `CLAUDE.md` rule "Nothing unrecorded" (and "Delegated decisions" for context); `docs/reviews/README.md` "From finding to task"; `tasks/MASTER_TASKS.md` rows T-0053, T-0061, T-0062, T-0063. Questions in T-0061 checked against the Disposition of `docs/reviews/documentation/2026-11-17-T-0060-ia-detail.md`. Only new critical or major problems are reported. Uncommitted; the repository has no commits. · Follows up: `docs/reviews/security/2026-11-17-adr-0005-delegation-rereview.md`

## Verdict
approve

Summary: All four findings from the previous re-review are resolved. Claude can no longer declare invalid, downgrade or defer a critical or major security or architecture finding; a dispute blocks the task for the owner, and the reviews README says the same. Point 3.2 now sets the stricter reading as the baseline, says the list is not exhaustive, and names privacy-audit and claude-workflow §4. `CLAUDE.md` defers to ADR-0005 points 3.11, 2 and 4 instead of stating a narrower rule. T-0063 is `backlog` behind T-0062, and T-0053 depends on T-0063. No new critical or major problem was found.

## Status of earlier findings

| Finding | Status | Evidence in current text |
|---|---|---|
| F-SEC-012 (major) | Resolved | ADR-0005 point 2.4, last sentence: "Claude never declares invalid, lowers the severity of, or defers a critical or major finding from the security or architecture reviewer; if Claude disputes one, the task becomes `blocked` until the owner rules." `docs/reviews/README.md` "From finding to task" states the same rule and cites point 2.4. This covers both reviewers and all three ways around the block (invalid, downgrade, defer). |
| F-SEC-013 (minor) | Resolved | Point 3.2 measures loosening "against the stricter reading of the current documents where they are silent or disagree". The list says "among others" and names privacy-audit and the claude-workflow §4 guardrails. The T-0061 row reserves questions 3, 14 and 18 under point 3.2. Question 15 (step-up factor for phone-OTP Customers) is not named in the row, but the ADR's stricter-reading baseline and "when in doubt, reserved" now govern it: choosing no step-up or a weaker factor than the specifications require is reserved by the ADR text itself. The row is an aid, not the control, so this is not raised as a finding. The author may add question 15 to the row for clarity. |
| F-SEC-014 (minor) | Resolved | `CLAUDE.md` "Nothing unrecorded" now points to ADR-0005 point 3.11 for reserved categories and point 2 for the rest (point 2.4 makes the security review mandatory for dependencies). The second sentence matches point 4 without the "to make a change pass" qualifier. Account creation and paid resources (point 3.5) are not named in that rule, but the "Delegated decisions" rule points every session to the whole of point 3. |
| F-SEC-015 (note) | Resolved | T-0063 is `backlog` with dependency T-0062, which is consistent with ADR-0003 decision 4. T-0053 (task-set acceptance, the gate before implementation) depends on T-0052 and T-0063, so technical enforcement is proposed before implementation opens. |

## Findings

| ID | Severity | Location | Finding | Recommended fix |
|---|---|---|---|---|

No new critical or major findings. The next finding ID remains F-SEC-016.

## Not reviewed
- Only the changed passages listed in the scope were read. The rest of ADR-0005 was read for context but not re-reviewed.
- F-SEC-010 (review reports and status changes not append-only; commits wait for the owner) remains consciously deferred, as recorded in the previous report, and is not re-raised.
- The agent and skill files under `.claude/` were not checked for resistance to re-scoping.
- No code exists, so no enforcing code could be located for any checklist item. All conclusions concern governance text.
