---
name: nyazek-documentation-review
description: Checklist and procedure for an independent documentation review in Nyazek. Use when a task tagged `docs` reaches `in-review`, or when the PRD, ADRs, implementation guide, CLAUDE.md, MASTER_TASKS or IMPLEMENTATION_STATUS change in a way that needs checking.
---

# Nyazek documentation review

**Inputs:** the task ID, the changed documents, and the documents they link to or depend on.

**Procedure**

1. List the changed documents and what each is authoritative for.
2. Work through the checklist. For PRD files, run `python3 docs/prd/_tools/check_docs.py docs/prd` and include its result; if `cfg:` keys or Page IDs changed, confirm `gen_config_register.py` and `count_pages.py` were re-run (their output must leave the files unchanged) and that `check_ia.py` passes (every Page ID has exactly one page specification).
3. Write the report in the format and location defined in `docs/reviews/README.md`.
4. Do not modify the documents under review.

**Checklist**

- **Accuracy:** statements match the code, the approved PRD and accepted ADRs; nothing describes behaviour that does not exist as if it did.
- **Single source:** each fact lives in one place; no restated content that can drift; no contradiction between documents.
- **Right document:** tasks only in `MASTER_TASKS.md`; high-level progress only in `IMPLEMENTATION_STATUS.md`; "how" in the guide; "what and why" in the PRD and ADRs; `CLAUDE.md` stays concise.
- **Structure:** the guide remains one topic per file; every guide file is listed in its `README.md`; no document has grown into a catch-all.
- **Links:** all relative links resolve; referenced task, finding and ADR IDs exist.
- **Decisions:** owner-level choices appear as open decisions or ADRs, never decided silently in prose.
- **Clarity:** a reader with only this document and its links can act on it; terms match the PRD glossary ("Customer", never "buyer").
- **Page specifications:** each cites rule IDs that exist and say what the specification claims; a specification never states a rule the domain document does not contain.
- **Status hygiene:** task statuses, dates and phase states are current and agree with each other.
