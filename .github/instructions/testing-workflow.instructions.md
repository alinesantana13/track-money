---
description: "Use when changing bounded-context use cases or domain entities in track-money. Automatically invoke the unit-test-writer agent to create/update pytest unit tests for the affected context."
applyTo: "app/**/use_cases/**/*.py, app/authentication/_user.py, app/subscription/plan/_plan.py, app/subscription/user/_user.py, app/movement/bank/_bank_account.py"
---

# Unit Test Workflow (Auto)

- When editing files matched by `applyTo`, always invoke the `unit-test-writer` custom agent before finishing.
- The `unit-test-writer` must:
  - mirror changes in `tests/` for the same bounded context (`authentication`, `subscription`, `movement`);
  - cover happy path, explicit error branches, and domain invariants;
  - prioritize core business constraints, especially free-plan account limit rules.
- Keep tests unit-level only (no DB sessions, no HTTP client, no infra adapters).
- After test changes, run `python -m pytest tests/ -v` and report results.
- If tests fail, iterate until failures are resolved or clearly reported with root cause.
