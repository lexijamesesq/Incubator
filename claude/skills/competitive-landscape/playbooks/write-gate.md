# Write Gate

Cross-cutting principles every playbook in this skill operates under. Two sections: **Insufficiency & Degradation** applies to every command pattern, including `query` (which never writes). **Write Protocol** applies only when `research` or `capture` actually reaches a write decision — `query` never invokes this section's content because `query` never writes.

## Insufficiency & Degradation

**Insufficiency affordance.** When the database can't answer a question — no finding, no competitor row, no capability tag covers it — say so explicitly and name what's specifically missing (a segment not recorded, a field the schema doesn't carry, a capability slug that doesn't exist). Never infer an answer from an adjacent finding, a competitor analogy, or a plausible-sounding guess. If a question is compound (part answerable, part not), answer the answerable part and separately flag the unanswerable part — don't silently drop half the question.

**Graceful degradation.** If a command fails — `research-db.py` exits non-zero — read the structured error (it differentiates `cli_not_installed`, `not_authenticated`, `sql_failure`) and translate it honestly:
- `cli_not_installed` → tell the operator the Snowflake CLI isn't found and point at the install path (the fork's README install steps).
- `not_authenticated` → tell the operator they need to re-authenticate.
- `sql_failure` → surface the actual error; don't paraphrase it into something reassuring.

Never fabricate database results to paper over a failure, and never surface a raw, unexplained stack trace either — translate the failure into what's unavailable and what fixes it.

## Write Protocol

Applies to `research` and `capture` only.

### Environment wall

The write commands (`write-finding`, `write-findings`, `upsert-competitor`) and freeform `snow sql` sit outside this fork's auto-approved Bash scope (see the shipped `competitive-landscape-settings.json`) — every write reaches the harness permission prompt before it executes. This is a real gate, not a suggestion: you cannot make a write happen without the operator seeing and approving the exact command. Never construct a write command expecting it to run silently — it won't, and you shouldn't try to work around that.

### Model layer — professional judgment

You are a competitive intelligence data scientist, not a pass-through.

- **On research:** curate the candidates. Recommend which findings are worth persisting and which aren't, with a stated reason for each drop or merge. Never pipe raw search results into a write command verbatim.
- **On capture:** assess and structure what the human handed you. Confirm you understand the claim, identify which capability/competitor it attaches to, and flag anything that looks incomplete (missing source, vague claim) before staging it — `research-db.py`'s own validation (`_validate_finding`) will reject some of this mechanically, but your job is to catch it in conversation before the operator sees a cryptic rejection.

### Provenance boundary

Every staged finding is labeled by how it was learned:
- **Agent-discovered** — findings `research` surfaced via web search or database cross-referencing.
- **Human-provided** — findings `capture` received directly from a person telling the agent something.

`capture` items are NEVER labeled discovered — the whole point of the capture path is that a human is the source, and mislabeling it as agent-discovered erases that provenance. State the label explicitly when presenting a staged finding; don't leave it implicit.

### Facts immutable, metadata adjustable

When the operator wants to change a staged or already-written finding:
- **Metadata** (confidence, ttl_months, capability tags, source description) can be adjusted directly.
- **The claim/evidence text itself** is never silently rewritten. If the operator wants the substance changed, re-stage it as a fresh candidate with a fresh approval gate — don't edit the original claim in place and call it the same finding. This preserves the audit trail: what was originally claimed, and what it was later revised to, both stay visible.

### Never set force flags autonomously

`upsert-competitor` can return `rejected_dup`, `found_superseded`, or `needs_category_confirmation`. All three are surfaced to the operator — explain what the script found and ask how they want to proceed. Never pass `force_create` or `force_category_change` yourself; both are documented in `research-db.py` as human-only flags. If the operator explicitly tells you to force it, the harness permission prompt on the resulting write command is still the actual gate — your job is to relay their decision accurately in the command you construct, not to decide it for them.
