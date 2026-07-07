> Split verbatim from `incubator-reference.md` on 2026-07-07 — one section of the reference index. See `incubator-reference.md` for the full section map.

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
