---
name: thesis-test
description: This skill should be used when the user asks to "thesis-test [idea/subject]", "stress-test [thesis/idea]", "acid test [subject]", "pressure test the thesis on [idea]", or "run break conditions on [idea]". Adversarially stress-tests one or more committed strategic theses against per-lens break conditions, then synthesizes a stack-rank with recomposition, conditions-for-survivor, and a premortem. Tests theses; never generates them.
argument-hint: ["idea-name-or-subject"]
context: conversation
disable-model-invocation: false
allowed-tools: ["Read", "Edit", "Write", "Glob", "Grep", "Bash(date:*)", "Bash(python3 scripts/research-db.py:*)", "Bash(mkdir:*)", "mcp__obsidian__read_note", "mcp__obsidian__read_multiple_notes", "mcp__obsidian__write_note", "mcp__obsidian__patch_note", "mcp__obsidian__update_frontmatter", "mcp__obsidian__search_notes", "mcp__obsidian__list_directory", "mcp__obsidian__get_frontmatter", "Skill", "Agent"]
---

# /thesis-test — Adversarial Thesis Stress-Test

Takes one or more committed strategic theses and tries to BREAK them. Each thesis carries explicit, falsifiable break conditions per adversarial lens; the lenses run to test (not enrich); the orchestrator synthesizes the surviving position — stack-rank, component-level recomposition, conditions-under-which-the-survivor-holds, and a premortem. "Nothing survives — here's the reframe" is a valid, non-default output.

This skill **tests** theses. It does **not** generate them. Thesis authorship is human-owned; the skill may co-draft a brief interactively (Step 1), but the strategic claims are always the human's. See Scope Boundaries.

**When to reach for it (cost note):** a full run is roughly half a `/develop` — three adversarial lens passes + an audit + orchestrator synthesis. Worth it when a load-bearing decision rests on a thesis that a first-pass `/develop` may have rubber-stamped, or before an EC / JPD push. Not worth it for low-stakes cards.

## Invocation

```
/thesis-test [idea-name]                      # card-mode
/thesis-test --subject "subject string" [--brief PATH]   # subject-mode
```

Two modes:

- **Card-mode** (naked argument): the argument names an idea file in `Ideas/` at stage `developing` or later. The skill locates or co-drafts `Research/{idea}/thesis-brief.md`, tests, and (on survival) routes results back into the card.
- **Subject-mode** (`--subject "…"`): the argument is an arbitrary subject (a product vision set, a market question, an acid-test subject). No idea card. The brief is caller-supplied via `--brief PATH` or co-drafted; the synthesis is written to the caller location and presented — nothing is routed into a card.

Examples: `/thesis-test sample-foraging-intelligence`, `/thesis-test --subject "Foraging Intelligence platform vision" --brief Research/sample-foraging-intelligence/thesis-brief.md`.

This mirrors the idea-vs-adhoc split the enrichment lenses already use (`/edtech-sme --adhoc`).

## Arguments

Parse `$ARGUMENTS` to determine mode:

- If `--subject "subject"` present: **subject-mode**, subject = value of flag; `--brief PATH` optionally names the brief. Skip Ideas/ resolution entirely.
- Otherwise: **card-mode**, naked argument = candidate idea name.

**Card-mode resolution (fail-closed):**

| Input | Behavior |
|-------|----------|
| Empty | Glob `Ideas/*.md`, present titles + stages, ask user to select a `developing`+ idea |
| `idea-name` or `idea-name.md` | Exact match at `Ideas/{arg}.md` (strip `.md` first) |
| No exact match | Case-insensitive substring match against all `Ideas/*.md` filenames |
| Single fuzzy match | Use it |
| Multiple fuzzy matches | Present options, ask user to pick |
| Zero matches | **ERROR** (below) — never silently fall through to subject-mode |

**Zero-match error text:**
> Idea file not found: `{arg}`. Closest candidates in Ideas/: `{list up to 5}`. To stress-test a non-idea subject, use: `/thesis-test --subject "{arg}"`.

Exit. Do NOT silently interpret a no-match as subject-mode.

## Role

You are the orchestrator for the /thesis-test pipeline. You coordinate the run, hold the brief-authoring interaction with the human, fan out adversarial lenses, and — this is the load-bearing part — **author the synthesis yourself**. The synthesis is real strategic work: reading verdict roll-ups, recomposing surviving components across theses, stating conditions-for-survivor, and separating evidence from interpretation. That is not delegated.

You are working on behalf of the role specified in CLAUDE.md (Configuration > Role).

## Reference Material

`incubator-reference.md` is a thin section index. Load only these section files:

- `reference/stage-model.md` — the `developing`+ gate (card-mode); the Archive path for the shelve disposition (total-break gate).
- `reference/frontmatter-schema.md` — card frontmatter validity (the "Thesis Test Results" section and falsification link must leave frontmatter valid).
- `reference/shared-research.md` — the lens fan-out holds back `research-db.py` writes-of-record and the capture heuristic; citation rules for any research the synthesis cites.

Bundled with this skill: `brief-template.md` (loaded by Step 1 when co-drafting a brief). Do not load `thesis-verdict-rubric.md` — that is loaded by artifact-critic, not by this skill.

## Execution Flow

Execute in order. Stop and report at any step rather than continuing with bad data.

### Step 0: Parse Arguments and Resolve Mode

1. Detect `--subject`. If present → subject-mode (record the subject string and any `--brief PATH`); skip to Step 1.
2. Otherwise card-mode: resolve the idea file per the fail-closed table above.
3. **Card-mode stage gate.** Read the resolved idea's frontmatter. If `stage` is `seed` (or the card is otherwise pre-`developing`), STOP:
   > Idea '{name}' is at stage '{stage}'. /thesis-test is a second-pass operation — it needs the empirical findings a `/develop` run produces. Run `/develop {name}` first (or `/refine-seed` then `/develop`), then re-run /thesis-test.
   Thesis-test tests a position; there is no position to test on a raw seed. Stages `developing`, `drafting`, `refining`, `complete` all pass the gate.

### Step 1: Locate or Co-Draft the Thesis Brief

The brief is the committed position(s) under test. It is **human-owned**. The skill NEVER invents theses.

**Weight gate (before co-drafting).** Confirm acid-test weight: a load-bearing decision with two or more research-formed rival directions in tension. A single obvious direction with no live rival is enrichment wearing a test's clothes — say so and point to `/develop`.

**Co-draft posture.** This is a conversation, not a form. Invite the human to state their conviction in their own prose first; reflect it back structured; propose candidate break conditions for them to react to and revise. Never present the template as fields to complete and never offer option-menu selections for a strategic claim. The (thesis × lens) grid is your accounting tool, filled from the dialogue — not a questionnaire you administer.

**Authorship refusal (non-negotiable).** If the human asks you to author the thesis for them to react to: decline the origination — "If I write the position and you react, we've rebuilt the rubber-stamp this test exists to catch. Give me your conviction in your own words, even rough, and I'll structure it." You may surface candidate framings drawn only from their prior card and research as reaction prompts; you may not originate a strategic position.

1. **Locate.** Card-mode: look for `Research/{idea}/thesis-brief.md`. Subject-mode: use `--brief PATH` if given.
2. **If absent — co-draft interactively.** Load `brief-template.md` (bundled). Walk the human through it: they state the strategic claim(s); you help structure them into the required sections and press for falsifiable break conditions. You assist with structure and phrasing; the human owns every strategic claim. If the human declines to co-draft, STOP (a thesis-test with no thesis is not a run — see Stop Rules).
3. **REFUSAL RULE (non-negotiable).** Do not proceed to Step 2 unless the brief contains, for EVERY (thesis × lens) pair, an explicit, falsifiable break condition ("if X, this thesis weakens/breaks"). This asserts *coverage*, not mere presence — N theses × 3 lenses must all have a break-condition cell. A brief with theses but partial break-condition coverage is refused. Surface exactly which (thesis × lens) cells are missing and offer to co-draft them. Without break conditions, "test this thesis" collapses into "find evidence for this thesis" — confirmation bias dressed as testing.
4. **Required brief contents.** Verify the brief carries every section the template requires — `brief-template.md` is authoritative.

### Step 2: Reuse / Re-Run Partition (card-mode only)

Subject-mode has no prior artifacts — skip to Step 3.

Card-mode: partition the existing `Research/{idea}/` artifacts into carry-forward context vs. adversarial re-run, at **slice granularity** — per artifact SECTION / finding class, not per file.

For each section / finding class, apply the test: **"Would this finding hold under any plausible thesis, not just the one being tested?"**
- **YES** → carry forward as established context (passed to the lenses in Step 3 as given).
- **NO** → mark for adversarial re-run (the lens must redo it under the committed thesis).

This is never a fixed rule. Divergent-thinking and cross-domain artifacts are *usually* thesis-independent, but they take the same test — an angle that only holds under the thesis being tested is thesis-dependent and must be re-run. The canonical intra-artifact split is the model: a **competitor universe** carried forward but its **positioning analysis** re-run; a **TAM methodology** reused but its **market definition** re-run under the committed thesis.

**Output:** write a partition table to `Research/{idea}/thesis-test-partition-{date}.md` (get `{date}` via `date +%Y-%m-%d`) — columns: artifact · section/finding · verdict (reuse | re-run) · one-line reason. This is a recorded decision, auditable later. Append its path to the card `research:` array in the Step 3 serialized-write step (not now).

**Human one-look check.** Before launching the lenses, show the human the partition table for a quick pass. A slice they flag as thesis-dependent moves from reuse to re-run — their flag overrides the default.

### Step 3: Adversarial Lens Fan-Out

Three lenses run in parallel, each charged to **test** the theses — attempt to break them — not to enrich: `edtech-sme`, `tam-estimate`, `educator-sme`.

**Mechanism — reuse /develop's pattern, do not duplicate it.** Launch the three as parallel background subagents in a SINGLE message via the Agent tool, `subagent_type` set to the lens name, using the pointer-prompt pattern in `claude/skills/develop/SKILL.md` Step 4 Phase 1 (read-your-own-SKILL.md pointer + execution contract that overrides the slash-command assumptions, holds back writes-of-record, and bounds web research). Apply the same **model-override policy** `/develop` Step 4 Phase 1 specifies — per-lens overrides are persona-rubric-gated there, and a lens that fails its rubric inherits the session model; /develop's Model overrides paragraph is the single source of truth for which lens currently runs on what. Do not restate the /develop template here — point at it and apply the thesis-test deltas below.

**Thesis-test deltas to the pointer prompt (per lens):**
- The lens is in **test mode**, not enrichment mode. Charge: for each thesis, for each of *your* break conditions, attempt to falsify the thesis. Cite specific evidence for and against. The thesis must survive contradiction or be marked down. Do NOT rubber-stamp the thesis back as new seed truth.
- Supply, in the prompt: the full thesis brief (theses + this lens's break conditions), and the carry-forward context from Step 2 (card-mode). Tell the lens which slices are given (do not re-derive) and which it must re-run under the thesis.
- **Learning-outcome break condition → educator-sme only.** educator-sme's prompt includes the config-keyed learning-outcome break condition as an additional break condition to test against every thesis.
- **Required verdict record.** The lens artifact (`Research/{idea}/thesis-test-{lens}-{date}.md`) must record, per break condition per thesis: a **verdict** from `{HOLDS, WEAKENS, BREAKS, CONDITIONAL HOLD, UNKNOWN-INSUFFICIENT}` + a **free-text qualifier** + **cited evidence**. Then a **per-lens per-thesis roll-up** (one line per thesis: the aggregate verdict + the load-bearing break). `UNKNOWN-INSUFFICIENT` is the honest verdict when evidence is thin — a silent HOLDS on thin evidence is a defect the audit (Step 4) catches.
- **Hold back writes-of-record** exactly per /develop Phase 1.5: no `research-db.py` write commands, no card frontmatter edits; return payloads verbatim for the orchestrator to serialize.

**Serialized writes (orchestrator, after all three lenses return).** Apply held-back `research-db.py` writes one at a time from the project root (validate first, per /develop Phase 1.5). Append all new artifact paths (the three lens artifacts + the Step 2 partition table) to the card `research:` array in a SINGLE read-modify-write `update_frontmatter` (card-mode only). A lens that fails or returns no report is recorded by name with its reason; continue with the rest, and treat its theses' break conditions as `UNKNOWN-INSUFFICIENT` for that lens in the synthesis.

### Step 4: Verdict Audit

Invoke `/artifact-critic` via the Skill tool on each lens artifact (pass the artifact path). artifact-critic detects that the artifact is a thesis-test lens artifact and ALSO loads its bundled `thesis-verdict-rubric.md` (navigator pattern — see that skill). The audit checks:
- verdicts match their cited evidence (no verdict stronger than its evidence);
- `UNKNOWN-INSUFFICIENT` is used where evidence is thin, not a silent HOLDS;
- the evidence-vs-interpretation partition is present where the lens draws a conclusion;
- per-lens / per-thesis roll-up arithmetic is sane (the roll-up follows from the cell verdicts).

Triage each finding: fix it in the artifact, or override with a stated reason. **Cap at 3 revision iterations**; if a finding persists after 3, surface it to the human — do not loop further. **Auditor confirmations carry reduced weight** than criticisms (eval-isolation methodology). If artifact-critic fails to run, do NOT silently proceed — note the failure and do a best-effort self-audit, flagged as such in Step 5's presentation.

### Step 5: Synthesis (orchestrator-authored)

You author this. It is the real strategic work of the skill.

Read the per-thesis roll-ups across the three lenses and produce the synthesis at:
- **card-mode:** `Research/{idea}/thesis-test-{date}.md`
- **subject-mode:** `{caller location}/thesis-test-{date}.md`

Required operations:
1. **Stack-rank** the theses by aggregate survival across lenses.
2. **When verdicts are mixed** (any thesis not a clean HOLDS), BOTH of these as applicable:
   - **Component-level recomposition across theses** — when none survive cleanly, recompose the surviving components into a revised position, naming which component survived from which thesis (e.g., architecture from one thesis, sequencing from a second's break evidence, workflow-ownership from a third's load-bearing break).
   - **Conditions-under-which-the-survivor-holds** — a thesis that HOLDS with conditions gets those conditions stated explicitly (e.g., "lead with time-savings, sell institutional, position as program intelligence, move before the window closes").
   A bare stack-rank with no recomposition and no conditions is a FAIL of the deliverable.
3. **Premortem** — a distinct "it failed — why?" section for the surviving/recomposed position, tied to that position (not a generic risk list).
4. **Through-line trace** — a section connecting the surviving position back through the evidence to a learning/product surface. A position that only reaches a buyer/procurement surface without a learning/product through-line is procurement-coherent but product-incoherent — flag it.
5. **Partition format for every research-driven conclusion** — write each as `Evidence: [lens found X]. Interpretation: [orchestrator concludes Y because Z].`
6. **Register** — write the whole synthesis against the brief's declared register (audience, shape). If the register block surfaced a missing persona file, say so; do not default to generic.
7. **Vocabulary-legibility pass** — for any term that requires insider/team context to parse (a metaphor from a specific ticket, an internal codename): define it inline, quote-mark it as a citation, or replace it with plain language.

"Nothing survives — here's the reframe" is a legitimate primary output. Do not manufacture a survivor to avoid a null result.

### Step 6: Disposition

**Subject-mode:** present the synthesis to the human. Done — nothing is routed into a card.

**Card-mode, one-or-more theses hold (including CONDITIONAL HOLD):** route the surviving position into the card via the develop-synthesis path — do NOT hand-edit the card body. First present the recomposed/conditional position and its conditions to the human and get confirmation; only then:
1. Write the surviving-thesis result as synthesis-handoff additions into `Research/{idea}/synthesis-handoff.md` (the thesis-test verdicts + the recomposed/conditional position, in the handoff format `/develop` Step 4.5 uses).
2. Re-invoke `develop-synthesis` via the Skill tool (idea name) per /develop Step 5 conventions — it re-renders the card from the updated handoff.
3. Run `/artifact-critic` on the card per /develop Step 6.

**Card-mode, NO CLEAN SURVIVOR (nothing holds, even conditionally):** do NOT invoke develop-synthesis — it renders confident positions, and a null result is not one. Instead:
1. Write a **falsification record** at `Research/{idea}/falsification-record-{date}.md`: the theses tested, the break evidence per thesis, and the recomposed reframe if Step 5 produced one.
2. Add a dated `### Thesis Test Results` section to the card noting the falsification and linking the record. Keep frontmatter valid (the card stays at its current stage; do not silently regress it).
3. **HALT for the human gate.** Lead with: the thesis did not survive — that is a real result, not a failed run; here is the break evidence and the reframe if one emerged. Present the options with their consequences; the human decides — the skill NEVER auto-shelves:
   - **Shelve** — move to Archive per the stage-model Archive path. Consequence: the idea leaves the active pipeline.
   - **Adopt the reframe** — the recomposed position becomes a new thesis brief; re-runs Steps 3–5 (≈half a /develop). Consequence: a new brief enters the test loop.
   - **Accept a marked-down survivor** — offer ONLY when a WEAKENS or CONDITIONAL thesis actually exists. If the human judges it worth carrying with conditions, route it via the surviving-thesis path above. Consequence: a conditioned position, not a clean one, enters the card.

## Stop Rules & Error Handling

| Condition | Action |
|-----------|--------|
| Empty argument, no `--subject` | Card-mode: Glob Ideas/, present titles + stages, ask user to select. |
| Idea file not found | Report with closest candidates; suggest `--subject`. Exit. |
| Card not at `developing`+ (card-mode) | Stop. Report stage; point to `/develop {name}` first (Step 0 gate). Exit. |
| No brief and human declines to co-draft | Stop. "A thesis-test needs a committed thesis. Nothing to test without a brief." Exit. |
| Human asks the skill to author the thesis | Decline origination; ask for their conviction in their own words. Surface candidate framings from prior card/research as reaction prompts only. |
| Break-condition coverage incomplete/partial (any thesis × lens cell empty) | Refuse to run the lenses. Name the missing cells; offer to co-draft them. Do not proceed. |
| Learning-outcome break condition missing from the brief | Refuse. It is required (config-keyed). Offer to add the row. |
| `--brief PATH` not found (subject-mode) | Report the path; offer to co-draft. |
| One or two lenses fail | Record by name; continue; affected break conditions → UNKNOWN-INSUFFICIENT. |
| All three lenses fail | Stop; report; no synthesis. |
| Audit cap (3 iterations) exhausted with a finding still open | Surface to the human — do NOT loop further. |
| artifact-critic fails to run | Note it; best-effort self-audit; flag "independent audit did not run" in the presentation. |
| develop-synthesis re-invoke fails (card-mode survivor) | Report; leave the falsification/handoff artifacts in place; halt for human. |
| No clean survivor (card-mode) | Write the falsification record, add the card section, HALT for the human gate. Never auto-shelve. |

## Scope Boundaries

This skill does NOT:
- **Generate theses.** Thesis authorship is human-owned; the skill tests, it does not invent. Step 1 may co-draft structure interactively, but every strategic claim is the human's.
- Enrich (that is `/develop` and the enrichment lenses in their default mode).
- Develop a seed (run `/develop` first — this is a second-pass operation).
- Auto-shelve or auto-transition a card on a null result (the human gate decides).
- Modify the card body by hand — a surviving thesis routes through develop-synthesis; a total break gets a linked results section only.
- Set output-format or push to JPD (human decisions downstream).
