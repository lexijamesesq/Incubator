# Research

Web + database. Investigates a topic — competitor positioning, a capability gap, a market question the database can't yet answer — and stages candidate findings for the operator's write approval. Always operates under `write-gate.md` in full (Insufficiency & Degradation AND Write Protocol).

## Protocol

1. **Check what's already known.** Before searching the web, run the relevant `query` commands (`query-competitor`, `query-landscape`, `query-gaps`) to see what the database already has — don't re-research a finding that's already there and current.
2. **Search.** Use `WebSearch`/`WebFetch` to investigate the gap. Look for concrete, sourced claims — named competitors, specific numbers, named capabilities — not vague market-trend summaries.
3. **Curate before staging.** Per `write-gate.md` § Model layer: not every search result is worth persisting. Recommend which candidates to write and which to drop, with a stated reason for each — a low-confidence rumor with no corroborating source is a candidate to flag as insufficient-to-write, not to force into the database anyway.
4. **Label provenance.** Everything staged here is agent-discovered — label it as such per `write-gate.md` § Provenance boundary.
5. **STAGE: present the curated candidates as a formatted diff/proposal and STOP.** Do not invoke `write-finding`, `write-findings`, or `upsert-competitor` in this step. For each candidate, present claim, evidence, source, confidence, ttl_months, and which competitor/capability it attaches to. State plainly: "Here's what I'd write — confirm to proceed." This is the turn's last action — you do not reach for a write command in the same turn you present the staged candidates.
6. **Only after explicit operator confirmation**, invoke the write command(s) that match what you staged. A vague or ambiguous reply is not confirmation — if the operator's response doesn't clearly approve, ask again rather than proceeding.
7. **If insufficient, say so.** If research turns up nothing solid enough to stage, report that plainly — don't manufacture a finding to have something to show.

**Step 5 is not optional and not a judgment call.** Curating well (step 3) and labeling provenance correctly (step 4) do not substitute for staging and stopping. Invoking `write-finding`, `write-findings`, or `upsert-competitor` before the operator has explicitly confirmed the staged proposal is a hard failure of this playbook — regardless of how well-curated the candidates are.

## Write Commands This Playbook May Reach

`write-finding`, `write-findings`, `upsert-competitor` — all three sit outside the auto-approved Bash scope; all three require the harness permission prompt. Never pass `force_create` or `force_category_change` — see `write-gate.md` § Never set force flags autonomously.
