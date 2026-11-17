# Implementation Guide — index

How Nyazek is built, one topic per file. This file is only the index.

**Rules**

- One file per technical topic, grouped in folders created when first needed: `standards/`, `backend/`, `frontend/`, `testing/`, `security/`, `deployment/`.
- A guide file says *how*. Required behaviour stays in `docs/prd/`; decisions and their reasons stay in `docs/adr/`. Link to them instead of restating them.
- Tasks link to the specific guide files they need. Claude reads only those.
- Every new guide file gets a row below in the same change.

**Status:** no guide files yet. They are written after the PRD review and the architecture phase.

| Topic | File | Covers |
|---|---|---|
| Progress | [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) | High-level implementation progress |
