---
name: Backend DB and model patterns
description: Classes over dicts for DB models; explicit projections in all DB calls
type: feedback
---

Always use dataclass instances, never raw dicts, for DB documents.

**Why:** Raw dicts are not scalable when data models change, provide no type safety, and are difficult to debug.

**How to apply:**
- All DB entity models live in `src/common/models/` as dataclasses (`Player`, `Court`, `Game`, `Place`, `Score`)
- Call `Model.from_doc(doc)` immediately after reading from DB; call `model.to_doc()` when inserting
- Every `find`/`find_one` call must include an explicit projection dict as the second argument
- Define projections as module-level constants (e.g. `COURT_FIELDS_PROJECTION = {"_id": 1, "name": 1, ...}`) near the top of logic files
- Default for existence-only checks: `{"_id": 1}`
- Never fetch more fields than are needed for the operation (respect public/private/secret access levels)
