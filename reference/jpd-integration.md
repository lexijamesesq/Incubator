> Split verbatim from `incubator-reference.md` on 2026-07-07 — one section of the reference index. See `incubator-reference.md` for the full section map.

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
jira-sidecar-url: null  # Google Doc URL for the Research Sidecar; populated by /jpd-push on first push
```

### Sync-Back

No automated sync-back. Any external status changes in JPD (workflow progression, roadmap priority updates, PM feedback) are learned conversationally and incorporated manually if they shift strategic direction. The incubator is not a continuous system of record — JPD push is one-directional for visibility.
