# Capture

Direct-write path for intelligence a human hands the agent — not something the agent went and found. Shares the write-gate with `research`, but the provenance label is different: capture items are human-provided, never agent-discovered. Always operates under `write-gate.md` in full.

## Protocol

1. **Confirm the claim.** Restate what the human told you in your own words before staging it — catch misunderstandings here, not after a bad write.
2. **Identify the attachment point.** Which competitor and which capability slug(s) does this claim attach to? If the human didn't say, ask or infer from context — don't guess silently and stage an unlabeled or mis-attached finding.
3. **Assess and structure, don't just transcribe.** Per `write-gate.md` § Model layer: turn what the human said into a well-formed finding — a real claim (not a stub, not a query-string fragment), evidence, a source description ("Hazel Acorn, verbal" is a valid source description), confidence, and a reasonable ttl_months. `research-db.py`'s own validation (`_validate_finding`) will reject sub-30-char claims, empty capabilities, and missing sources mechanically — catch these in conversation before staging, so the operator sees a clean candidate, not a script rejection.
4. **Label provenance as human-provided.** Never label a capture item as agent-discovered — see `write-gate.md` § Provenance boundary. State explicitly who the source is.
5. **STAGE: present the complete finding as a formatted diff/proposal and STOP.** Do not invoke `write-finding`, `write-findings`, or `upsert-competitor` in this step. State plainly: "Here's what I'd write — confirm to proceed." This is the turn's last action. You do not reach for a write command in the same turn you present the staged finding, no matter how confident you are it's correct.
6. **Only after explicit operator confirmation**, invoke the write command that matches what you staged. A vague or ambiguous reply is not confirmation — if the operator's response doesn't clearly approve, ask again rather than proceeding.
7. **On a follow-up edit** (the operator wants to sharpen or correct the claim after it's staged, or after it's already written): re-stage a fresh candidate reflecting the edit — see `write-gate.md` § Facts immutable, metadata adjustable. Never silently rewrite the original claim in place. This is step 5 again, not a shortcut back to step 6.

**Step 5 is not optional and not a judgment call.** Curating the finding correctly (step 3) and labeling its provenance correctly (step 4) do not substitute for staging and stopping. Invoking `write-finding`, `write-findings`, or `upsert-competitor` before the operator has explicitly confirmed the staged proposal is a hard failure of this playbook — regardless of how well-formed the finding is.

## Write Commands This Playbook May Reach

Same as `research` — `write-finding`, `write-findings`, `upsert-competitor`, all gated by the harness permission prompt. Never pass `force_create` or `force_category_change`.
