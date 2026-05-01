# Incubator Reference

Reference material for Incubator stage work. Load this when doing /develop, /draft, /refine, or any stage transitions. For project state, intake, session protocol, and system overview, see `CLAUDE.md`.

---

## Stage Model

| Stage | Name | What Happens | Who Drives | Entry Criteria | Exit Criteria |
|-------|------|-------------|------------|----------------|---------------|
| 0 | **Capture** | Idea lands in inbox | Human | Exists in inbox | Router has processed it |
| 1 | **Seed** | Router classifies, applies frontmatter, preserves original capture. | System | Classified as professional-strategy | Frontmatter complete, Original Capture preserved |
| 2 | **Developing** | Agents research autonomously — opportunity potential, strategic connections, thought outline. Produces TL;DR nugget. | System + Human trigger | Human initiates "develop idea X" | TL;DR template complete, impact dimensions assessed, research attached |
| 3 | **Drafting** | Sufficiency check: enough context to draft? If no, gather more. If yes, first template-aligned draft. | System | Output format decided, TL;DR reviewed | First complete draft exists, all sections have content, gaps listed |
| 4 | **Refining** | Iterative human-agent collaboration. Section-by-section, voice alignment, strategic realism checks. | Human + System | First draft exists | Passes validation checklist, voice matches persona, human satisfied |
| 5 | **Complete** | Done. Ready for stakeholders. | Human approval | Human signs off | Exported to final location |

---

## Architecture: Idea Cards + Output Documents

The pipeline uses a two-track model:

**Track 1: Idea Cards (Stages 0→1→2) — Progressive Enhancement**
The idea file in `Ideas/` progressively accumulates content. Each stage adds structure on top of what came before — nothing is discarded or overwritten.

- **Stage 0 (Capture):** Raw thought arrives from inbox — unstructured, unedited
- **Stage 1 (Seed):** Router applies frontmatter and preserves the original capture in `### Original Capture` section. /refine-seed interprets the capture and adds structured fields (core insight, source, strategic connection) before /develop runs.
- **Stage 2 (Developing):** /develop adds TL;DR sections (opportunity assessment, research summary, thought outline, open questions). Original capture persists at the bottom.

The idea card is the scannable, shareable artifact. It can be duplicated to Google Docs for peer/VP/ELT visibility into the idea portfolio. The card body freezes by default at Stage 2 — Stages 3+ create linked output documents rather than modifying the card.

**Track 2: Output Documents (Stages 3→4→5) — Linked Artifacts**
When drafting begins, /draft creates a separate output document (strategy doc or product brief) linked from the idea card via `output-file:` in frontmatter. The idea card body is not modified.

- **Stage 3 (Drafting):** /draft creates `Output/{idea-name}-{format}.md`, updates idea card frontmatter with `output-file:` link and `stage: drafting`
- **Stage 4 (Refining):** /refine works on the output document. Idea card unchanged unless direction shifts.
- **Stage 5 (Complete):** Human approves output document. Idea card gets `stage: complete`.

**Card Update Rule:** The idea card is the source of truth for what the idea IS. If downstream work (drafting, refinement, stakeholder feedback) shifts the strategic direction, the card must be updated to reflect the new framing. Updates are deliberate, not automatic. The card's `updated:` timestamp signals when it last changed — a card last updated at Stage 2 tells you the framing has held; a card updated during Stage 4 signals the idea evolved.

**What triggers a card update:**
- Output doc refinement shifts the strategic thesis away from the TL;DR framing
- Research during drafting invalidates or changes an impact dimension rating
- Human feedback reframes the core insight
- Consolidation with another idea changes the scope

**What does NOT trigger a card update:**
- Output doc gaining more detail (depth, not direction)
- Section-level refinements that don't change strategic framing
- Additional research supporting the existing framing

### Consolidation Points

Three natural opportunities for grouping related items:

- **Captures → Seed (0→1):** Router identifies related inbox items and proposes grouping into one seed. Human confirms.
- **Seeds → Developing (1→2):** When development begins, /develop Step 3 scans **all ideas at any stage** — not just seeds — for theme and strategic connection overlap. For each related idea, it compares header fields and recommends merge or keep-separate with rationale. Human decides.
- **Output documents (Stage 3+):** Multiple TL;DR cards can feed into a single output document. This is the natural synthesis point — a strategy doc can draw from several related idea cards. The human decides at drafting time which cards to combine.

All follow system-suggests, human-decides. No autonomous merging.

#### Cross-Stage Detection

/develop Step 3 surfaces related ideas regardless of stage. What you can do depends on where the related idea is:

| Related idea stage | Available actions |
|---|---|
| **Seed** | Merge into one seed, or develop independently |
| **Developing** | Develop independently; both TL;DR cards may feed the same output doc at Stage 3 |
| **Drafting / Refining** | Develop independently; note the relationship for the drafter |
| **Complete** | Reference only — related work already delivered |

**Key rule:** Merge only happens between items at the same stage or when absorbing a lower-stage item. Never merge "up" or disrupt in-progress drafts.

#### Merge Mechanics (Seed + Seed Only)

When the human decides to merge two seeds:

1. **Primary selection:** Human picks, or default to the seed being developed
2. **Frontmatter:** `themes` = union (deduplicated), `domain`/`source` = primary's, `created` = earliest date, `updated` = today
3. **Body:** Keep primary's header fields. Preserve both Original Captures:
   ```
   ### Original Capture
   [Primary's original capture]

   ### Original Capture (merged from: {secondary-name})
   [Secondary's original capture]
   ```
4. **Secondary disposition:** Move to `Archive/` with `stage: archived` and `archived-reason: merged-into-{primary-name}` in frontmatter. Don't delete — provenance survives.
5. **Continue:** Development proceeds on the primary seed with enriched context.

**Merge scope:** Seed + Seed only. Two developing cards don't merge — they stay separate and converge at the output doc layer if the human decides they belong in the same strategy doc or brief.

#### Archive Conventions

Completed idea cards stay in `Ideas/` with `stage: complete`. Completed output documents stay in `Output/`. The `Archive/` directory holds only ideas that exited the pipeline without completing:

- **Merged items:** `stage: archived`, `archived-reason: merged-into-{primary-name}`
- **Shelved items:** `stage: archived`, `archived-reason: {reason}` (human decision to park an idea)

Archive files retain their full frontmatter and body for provenance. They are included in /develop Step 3 scans at the `complete` stage level (reference only).

---

## Frontmatter Schema

```yaml
---
type: incubator/idea
stage: seed | developing | drafting | refining | complete
created: YYYY-MM-DD
updated: YYYY-MM-DD
output-format: null | strategy-doc | product-brief

# Classification
domain: assessments | platform | cross-product
themes: []  # e.g., [authentic-assessment, marketplace, ai-capabilities]
# Theme governance:
# - Themes are provisional at Stage 1. /develop may add or remove at Stage 2 based on research.
# - Vocabulary is closed at /develop time — only use themes already in the portfolio.
#   New themes are created by the router at intake or by explicit human request.
# - ai-capabilities drives JPD "AI Feature" checkbox. /develop must explicitly assess
#   whether AI is load-bearing (see /develop Step 5d).
# - Minimum one theme per idea.

# Impact Dimensions (populated progressively, null until assessed)
customer-sentiment: null | none | low | medium | high
user-experience: null | none | low | medium | high
revenue-potential: null | none | low | medium | high
industry-disruption: null | none | low | medium | high
strategic-alignment: null | none | low | medium | high

# Relationships (human-set only — agents surface candidates, human confirms)
related-ideas: []  # idea filenames without path or extension, e.g., [ai-student-intelligence-model, ai-learning-pattern-recognition]
initiative: null  # parent initiative filename without .md, null if standalone

# Tracking
source: inbox | slack | conversation | meeting
output-file: null  # path to output document (populated at Stage 3)
research: []  # links to local research artifacts
research-ids: []  # UUIDs referencing research_findings rows in Snowflake (populated by /develop)
blocked-by: null  # terse reference — card title or theme blocking stage advancement

# JPD Integration (populated after push, null before)
jira-key: null  # e.g., PROJ-1234
jira-pushed-at: null  # YYYY-MM-DD
---
```

**Impact dimension rationale:** Maps to Director/VP/C-Suite priorities. Customer sentiment → retention. User experience → engagement (MAU). Revenue potential → ARPU. Industry disruption → competitive positioning. Strategic alignment → organizational priority. Translates to MAU x ARPU = ARR.

**TAM / market sizing:** Not a frontmatter field. When market sizing data is relevant and available, include it in the Research Summary or Opportunity Assessment rationale in the body. Many ideas (platform capabilities, positioning plays) don't have a meaningful standalone TAM — forcing the field creates noise.

**Related ideas:** Human-set only. Agents surface relationship candidates during /develop Step 3; the human confirms which relationships are meaningful; the agent writes the confirmed relationships to frontmatter on all affected cards. The agent never autonomously populates this field.

---

## Templates

### Seed Template (Stage 1)

Classification output from the router. Applies frontmatter and preserves the original capture verbatim. Structured fields (core insight, source, strategic connection) are added later by /refine-seed.

```markdown
## [Idea Title]

### Original Capture
[Verbatim original capture content — unedited raw thought from inbox. Preserved for context throughout the pipeline.]
```

### TL;DR Template (Stage 2)

Output of autonomous development. Dual purpose: internal prioritization AND external visibility (pushed to JPD via /jpd-push for peer/VP/ELT review). The idea card body freezes at this state by default — Stages 3+ create linked output documents rather than modifying this content.

```markdown
## [Idea Title]

**Core insight:** [One sentence — confident and declarative]
**Problem it addresses:** [One sentence — what's broken today]
**Who cares:** [Stakeholders/audiences affected]
**Strategic connection:** [How this ties to current priorities — specific, not vague]

### Opportunity Assessment
| Dimension | Rating | Rationale |
|-----------|--------|-----------|
| Customer sentiment | Low/Med/High | [One sentence] |
| User experience | Low/Med/High | [One sentence] |
| Revenue potential | Low/Med/High | [One sentence] |
| Industry disruption | Low/Med/High | [One sentence] |
| Strategic alignment | Low/Med/High | [One sentence] |

### Research Summary
- [Key finding 1 with source]
- [Key finding 2 with source]
- [Key finding 3 with source]

### Cross-Domain Signals
[Organizational awareness section — other teams' work with functional overlap. Written by the /develop orchestrator from the /cross-domain artifact, not by the synthesis agent. Conditional — present only when /cross-domain succeeded and found signals. Format: linked issue keys with signal type and connection sentence. See /cross-domain skill Phase 3 for format spec.]

### Thought Outline
[How this idea might develop — conceptual shape, not document structure]

### Buildable Surface
[generated by /buildable-surface — optional section, present only on principle-shaped ideas where the Thought Outline describes strategic principles rather than a specific buildable capability. Absent on feature-shaped ideas. Format: numbered list of 3-5 distinct product approaches, one sentence each, no sub-labels. See /buildable-surface skill for detection heuristic and generation logic.]

### Open Questions
- [What we still don't know]
```

**Title mutability:** The `## [Idea Title]` heading may be revised by /develop (Step 5e) if research reveals the seed title no longer captures the idea. Filenames remain stable — only the display title in the body changes.

**Original Capture preservation:** The `### Original Capture` section from the seed persists below the TL;DR content. It is not part of the TL;DR template but is preserved in every idea file for provenance and context.

**Card update rule:** The TL;DR content may be updated post-Stage 2 if downstream work (drafting, refinement) shifts the idea's strategic direction. Updates are deliberate — direction shifts, not detail additions. See Architecture section above.

### Output Templates

Strategy documents and product briefs use templates in `Templates/`:
- Strategy: `Templates/strategy-document-template.md`
- Brief: `Templates/product-brief-template-v2.md`

---

## Workflow

### Intake

Seeds arrive from `Projects/Router/` with frontmatter and Original Capture. The router does not interpret the capture — /refine-seed handles that before /develop. See `Projects/Router/router-spec.md` for classification and routing behavior.

### Refining a Seed (Stage 1 prep)

**Trigger:** Human says "refine-seed [idea name]" or equivalent. Run before /develop.

**What it does:** Interprets the raw seed's intent — determines whether the idea is a capability gap or an experience improvement, drafts header fields (core insight, problem, who cares, strategic connection), surfaces related ideas for potential consolidation, and aligns with the human before /develop runs. This is where ambiguous seeds get clarified so the synthesis agent has clean inputs.

### Developing an Idea (Stage 1→2)

**Trigger:** Human says "develop [idea name]" or equivalent. Seed should be refined first via /refine-seed.

**Architecture:** Orchestrator + synthesis agent. The /develop skill is an orchestrator that handles research and procedure. The develop-synthesis agent (`.claude/agents/develop-synthesis.md`) handles strategic judgment in an isolated context.

**Orchestrator flow:**
1. Read the seed file and verify refinement (structured fields present)
2. Research autonomously across three streams:
   - **Stream A:** Strategy docs, NPS data, customer evidence
   - **Stream B:** Market intelligence, competitive landscape, web research
   - **Stream C:** Cross-domain discovery via /cross-domain (JPD query)
3. Build a synthesis handoff document consolidating all research
4. Dispatch to the develop-synthesis agent (Opus, isolated context) to produce the TL;DR card
5. Post-synthesis: buildable surface check, theme governance, title revision, artifact critic, self-critique
6. Present completed TL;DR for human review

### Drafting (Stage 2→3)

**Trigger:** Human says "draft [idea name]" and specifies output format (strategy doc or brief).

**Agent behavior:**
1. Read idea card (TL;DR) and all attached research
2. Evaluate sufficiency: enough context to draft every template section?
3. If gaps exist: identify what's missing, propose how to fill (research, human input, internal docs)
4. If sufficient: create output document at `Output/{idea-name}-{format}.md` using the appropriate template
5. Self-critique against validation checklist before presenting
6. Update idea card frontmatter: `stage: drafting`, `output-file:` path — do NOT modify idea card body

### Refining (Stage 3→4)

**Trigger:** Automatic after Stage 3 draft is presented.

**Behavior:** Works on the output document (not the idea card). Follows the collaboration protocol from incubator-approach.md:
1. Establish north star alignment on the draft
2. Iterate section-by-section based on human feedback
3. Self-critique between iterations
4. Validate voice against persona guide
5. Check strategic connections for realism (not overstated)
6. As many feedback loops as needed — quality over speed
7. If direction shifts significantly, update the idea card to reflect new framing

---

## Voice & Output Standards

All outputs from Stage 2 onward follow `persona.md`. Key principles listed there.

**The "Designers speaking Design" test:** Before any output exits the incubator (Stage 2 TL;DR for external sharing, Stage 5 final doc), verify it speaks in terms that resonate with Product, Engineering, and executive leadership — not design-centric framing requiring translation.

---

## Research Protocol

When an idea needs more context than what's available:

**Strategy doc queries:** Targeted Grep on the product strategy and design strategy documents (paths configured in CLAUDE.md under Configuration > External References). Never load full files into context. When citing strategy docs in Research Summary bullets, link to the external URL (also in CLAUDE.md Configuration) so references are navigable outside the Incubator.

**Market intelligence:** Web search for competitors, TAM, technology trends. Synthesize with sources.

**Cross-domain discovery:** /develop Stream C invokes `/cross-domain` to query the JPD project for ideas from other product domains with functional overlap. Signals are classified as Direct overlap, Enabler/dependency, or Convergence. Results persist as `Research/{idea-name}/cross-domain-signals.md`. The curated output (maximum 5 signals) is written to a dedicated `### Cross-Domain Signals` section on the TL;DR card by the /develop orchestrator (Step 5b) — it does not flow through the synthesis agent. The full artifact is read by /jpd-push for the JPD Cross-Domain Signals section.

**When to pause and ask:** If research reveals the idea lacks strategic foundation, or if critical context can only come from the human (stakeholder conversations, internal politics, undocumented priorities), stop and surface the gap explicitly.

## Shared Research

Cross-idea research findings that compound across pipeline runs. Stored in the Snowflake `research_findings` table, queried via `scripts/research-db.py`.

### Topics

Findings are tagged with a `topic` value that groups them by concern:

| Topic | Contents | Primary Skills |
|---|---|---|
| `customer-evidence` | Pain signals, adoption behavior, research validation | /develop (Stream A), /educator-sme |
| `competitive-landscape` | Named competitors, specific capabilities, competitive gaps | /develop (Stream B), /edtech-sme |
| `market-sizing` | TAM figures, growth rates, segment data | /tam-estimate |

Skills query the database at research start (`query-landscape`) to establish a baseline, then write qualifying findings back (`write-findings`) at the end of the run.

### Capture Heuristic

A finding qualifies for shared research when ALL four criteria are met:
1. **Sourced** — Named, verifiable source with specific data and a URL (the most specific available page — press release, blog post, report page — not a homepage)
2. **Durable** — Useful beyond 3 months (not ephemeral news or announcements)
3. **Decision-relevant** — Tied to a named impact dimension with a specific directional effect
4. **Shared** — Relevant beyond the current idea, or likely relevant to future ideas entering the pipeline

**Don't capture:** General trend statements, single-idea findings (those go in `Research/{idea-name}/`), ephemeral news, unsourced opinions, interpretations or trend extrapolations.

### Governance

- **Autonomous writes:** Skills evaluate findings against the capture heuristic and write qualifying entries directly to Snowflake via `research-db.py write-findings`. The heuristic (Sourced + Durable + Decision-relevant + Shared) is the quality gate — no human confirmation step.
- **Non-retroactivity:** Shared research informs future /develop runs only. New findings do not trigger updates to ideas that have already passed Stage 2. Past cards are revisited only if the human explicitly requests it.
- **TTL by category:** Each entry has a category with a defined TTL (see table below). Reading skills treat expired entries as directional only — reverify before citing.
- **Supersession:** Stale findings are not deleted — the newer finding points to the older via `superseded_by`. Query results filter `superseded_by IS NULL` to retrieve the current view.

### TTL Reference

| Category | TTL |
|---|---|
| `pain-signal` | 12 months |
| `adoption-signal` | 12 months |
| `research-validation` | 24 months |
| `capability-specific` | 12 months |
| `capability-presence` | 18 months |
| `competitive-gap` | 12 months |
| `tam-broad` | 36 months |
| `tam-segment` | 24 months |
| `growth-rate` | 24 months |

### Integration with Idea Cards

Shared findings in the database are NOT linked in the idea frontmatter `research:` array (that stays for per-idea local artifacts). When a shared finding materially influences an idea's Research Summary or impact dimension rating, cite it with the original external source link from the finding's `source_url` — the same format as any other Research Summary citation: `([Source Title](url))`. No internal file paths, no provenance tags. Provenance metadata (origin idea, date created, confidence) stays on the finding row in the database.

### Verification at /draft

/draft must verify shared competitive claims before asserting them in stakeholder-facing documents. Shared findings are a dated baseline — treat as starting point for verification, not settled fact, when the output goes to VP/ELT audiences.

---

## Initiative Schema

Initiatives are structural parents — strategic containers that hold multiple related ideas under a unifying narrative. They are distinct from ideas: initiatives frame the strategic argument, ideas are the discrete proposals within it.

**Examples:**
- "Authentic Assessment for BTS '27" holds 8 child ideas (grading, rubric design, scalability, etc.)
- "Platform AI Intelligence Layer" holds ideas for intelligence models that compose into shared infrastructure

### Initiative Frontmatter

```yaml
---
type: incubator/initiative
stage: seed | developing | drafting | refining | complete
created: YYYY-MM-DD
updated: YYYY-MM-DD

# Classification
domain: assessments | platform | cross-product
themes: []  # Categorization tags, same as ideas

# Initiative-Specific
organizing-question: null  # The central strategic question this initiative answers
strategic-narrative: null  # 2-3 sentences on why these ideas cluster together
child-ideas: []  # Authoritative list of child idea filenames (without path or .md)

# Tracking
source: inbox | slack | conversation | meeting
output-file: null  # Path to initiative-level output document, if one is produced
research: []
blocked-by: null
---
```

**What initiatives do NOT have:** Impact dimensions (`customer-sentiment`, `user-experience`, etc.). Those belong on child ideas. An initiative's strategic value is emergent from its children.

### Child-to-Parent Reference

Child ideas reference their parent via a frontmatter field:

```yaml
initiative: authentic-assessment-bts27  # Initiative filename without .md
```

The initiative card maintains the authoritative `child-ideas:` list. One parent per idea.

### Initiative Stage Model

Initiatives follow the same stage names but with different semantics:

| Stage | Meaning for Initiatives |
|-------|------------------------|
| **Seed** | Framing exists — organizing question, narrative, children identified. Children may still be seeds. |
| **Developing** | Children actively developing. Initiative narrative enriched as research reveals patterns across children. |
| **Drafting** | Decision made: does this initiative produce its own synthesis output doc? If yes, drafting begins. |
| **Refining** | Initiative output doc being refined. |
| **Complete** | Initiative output finalized, or children have shipped individual outputs and the initiative served its organizing purpose. |

### Output Format Heuristic

Initiatives are probable candidates for **strategy docs** — they frame a strategic argument across multiple proposals. Child ideas are probable candidates for **product briefs** — they're discrete, scoped proposals with specific deliverables. This isn't a hard rule (a child idea with broad strategic implications might warrant a strategy doc), but it's the default expectation when choosing output format at the Stage 2→3 gate.

### Initiative File Naming

Same convention as ideas: kebab-case, no special suffix. Distinguished by `type: incubator/initiative` in frontmatter.

### Initiative Body Template

```markdown
## [Initiative Title]

**Organizing question:** [The central strategic question]
**Strategic narrative:** [2-3 sentences — why these ideas compose into something larger than any single one]

### Child Ideas
- [child-idea-1] — [one-line summary of its role in the initiative]
- [child-idea-2] — [one-line summary]
- ...

### Original Capture
[Verbatim original capture if the initiative originated from inbox]
```

---

## JPD Integration

### Purpose

Push developed ideas to JPD for stakeholder visibility. Query JPD during /develop for cross-domain signals.

### Configuration

All Jira/JPD connection details, field IDs, option IDs, and organizational taxonomy are in `jira-config.md` (gitignored — contains org-specific identifiers). See `jira-config.sample.md` for the expected format.

The /jpd-push and /cross-domain skills read from `jira-config.md` at runtime.

**Description body:** Restructure TL;DR into JPD-compatible headings (What/Who/Why + Incubator additions). Content transferred verbatim — no generative rewriting. Exclude Original Capture only. If cross-domain research exists, include as a Cross-Domain Signals section; strip cross-domain bullets from Research Summary to avoid redundancy. See `/jpd-push` skill and INC-015 context doc for full mapping.

### Standard JPD Idea Template

If your JPD project has an official idea template, align push output with its structure. Key fields to check:

- **Required at which stages:** Some fields (Success Measure, Cost of Delay) may only be required at later stages, not at initial Opportunity Identification.
- **Executive Summary:** Typically a pinned field (configured in `jira-config.md > Dynamic Field Mappings`)
- **Description sections:** Usually What (problem statements & hypotheses), Who (audiences), Why (why worth solving), plus stage-specific fields

**Alignment with Incubator push:** Our developing-stage push uses What/Who/Why matching this convention, plus Incubator additions (Opportunity Assessment, Research Summary, Cross-Domain Signals, Thought Outline, Open Questions). We exceed what's expected at Opportunity Identification. Success Measure and Cost of Delay are not relevant at developing stage but become required at Experimentation/GTM — see INC-019 for stage-aware push planning.

**Stage-aware push (future, INC-019):** At later PDLC stages (Experimentation, GTM), re-push should add Success Measure and Cost of Delay per the standard template, condense Thought Outline/Open Questions as unknowns resolve, and link to a Google Doc output document rather than carrying full content inline.

### Push Criteria

Push when an idea reaches **mature developing** (TL;DR complete, impact dimensions assessed). Do not push seeds.

### JPD Sync Tracking (Frontmatter Fields)

Added to idea cards after push:

```yaml
# JPD Integration (populated after push, null before)
jira-key: null  # e.g., PROJ-1234
jira-pushed-at: null  # YYYY-MM-DD
```

### Sync-Back

No automated sync-back. Any external status changes in JPD (workflow progression, roadmap priority updates, PM feedback) are learned conversationally and incorporated manually if they shift strategic direction. The incubator is not a continuous system of record — JPD push is one-directional for visibility.