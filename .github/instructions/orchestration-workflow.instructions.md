---
description: "Use when changing Python code in track-money and coordinate the full pipeline via change-orchestrator."
applyTo: "app/**/*.py"
---

# Orchestration Workflow

- For code changes in `app/**/*.py`, invoke the `change-orchestrator` agent before finishing the task.
- The pipeline order is mandatory: `ddd-monolith-reviewer` -> `unit-test-writer` -> `commit-assistant`.
- Stop the flow if review reports blocking issues or if tests fail.
- Commit stage only happens after user approval.
