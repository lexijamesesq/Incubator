A Claude Code project that turns raw strategic ideas into executive-ready documents through a structured pipeline with agent-assisted development at each stage. Built for product leaders who generate ideas faster than they can translate them into the strategy docs and product briefs that organizations act on.

## Installation

Clone the repo, then set up the Claude Code directory:

```
mv claude .claude
```

Copy the sample config and fill in your paths:

```
cp CLAUDE.sample.md CLAUDE.md
```

### Required configuration

| Field | Location | What to set |
|-------|----------|-------------|
| `role` | CLAUDE.md > Configuration | Your title and domain, e.g. "Director of Product Design (Assessments)" |
| `strategic_context.product_strategy` | CLAUDE.md > Configuration | Path and URL to your product strategy document |
| `strategic_context.design_strategy` | CLAUDE.md > Configuration | Path and URL to your design strategy document |
| `strategic_context.okrs` | CLAUDE.md > Configuration | Path to your OKRs / organizational goals |
| `persona.md` | Project root | Replace with your own voice and writing style guide |

### Optional configuration

| Field | Location | What to set |
|-------|----------|-------------|
| `metrics.nps_product_a`, `metrics.nps_product_b` | CLAUDE.md > Configuration | Paths to NPS analysis directories for your products |
| `jira-config.md` | Project root | Copy from `jira-config.sample.md`, fill in your Atlassian cloud ID, project key, field IDs, and option IDs for JPD integration |
| `claude/skills/cross-domain/org-structural-reference.md` | Skills directory | Copy from `org-taxonomy.sample.md`, fill in your org's product brands, domains, and squads for cross-domain discovery |

## What's Included

### Core pipeline

| Artifact | Type | What it does |
|----------|------|-------------|
| `/refine-seed` | Skill | Interprets a raw seed's intent, drafts header fields, classifies capability-vs-experience framing, surfaces related ideas, and aligns with you before development |
| `/develop` | Skill | Orchestrates research across strategy docs, market intelligence, and related ideas, then dispatches to the synthesis agent to produce a TL;DR card (Stage 1 to 2) |
| `/develop-synthesis` | Skill + Agent | Strategic synthesis engine that transforms a seed + research handoff into a TL;DR card with opportunity assessment, research summary, and thought outline (runs on Opus) |
| `/draft` | Skill | Creates a first template-aligned output document (strategy doc or product brief) from a developed idea card (Stage 2 to 3) |
| `/refine` | Skill | Iteratively refines an output document through section-by-section collaboration, voice alignment, and strategic realism checks (Stage 3 to 4 to 5) |
| `/jpd-push` | Skill | Pushes a developed idea to Jira Product Discovery for stakeholder visibility, with re-push support |
| `artifact-critic` | Agent | Checks TL;DR cards and output documents for structural conformance, voice conformance, and rating calibration (runs on Sonnet) |

### Enrichment agents

These add research artifacts to an idea without changing its stage. Invokable standalone or called by `/develop` during orchestration.

| Artifact | Type | What it does |
|----------|------|-------------|
| `/cross-domain` | Skill | Queries your JPD project for ideas from other product domains with functional overlap |
| `/edtech-sme` | Skill + Agent | Evaluates an idea against edtech market dynamics, competitive landscape, buyer behavior, and technology trends |
| `/educator-sme` | Skill + Agent | Evaluates an idea through the lens of a veteran educator focused on pedagogical practice, classroom reality, and adoption likelihood |
| `/tam-estimate` | Skill + Agent | Produces defensible TAM/SAM/SOM estimates using top-down and bottom-up methodologies |
| `/divergent-thinking` | Skill + Agent | Generates 3-5 unexpected, nonlinear connections by following structural pattern similarity across domains |
| `/buildable-surface` | Skill + Agent | Detects principle-shaped ideas and generates distinct product approach candidates; no-ops on feature-shaped ideas |

### Reference documents

| File | What it does |
|------|-------------|
| `incubator-reference.md` | Stage model, two-track architecture, frontmatter schema, templates, workflow, research protocol, initiative schema, JPD integration |
| `incubator-approach.md` | Unified methodology for strategy docs and product briefs (Rumelt, Perri, Torres synthesis) |
| `persona.md` | Voice and style guide governing all output from Stage 2 onward |
| `Templates/strategy-document-template.md` | Output template for strategy documents |
| `Templates/product-brief-template-v2.md` | Output template for product briefs |

## Configuration

The system separates what you configure from what skills handle.

**You configure:**
- `CLAUDE.md` -- your role, paths to external strategy documents, OKRs, NPS directories
- `persona.md` -- your writing voice and style
- `jira-config.md` -- your Atlassian connection details (optional, for JPD integration)
- `Templates/` -- your organization's output document conventions

**Skills handle:**
- Stage transitions and frontmatter updates
- Research orchestration (strategy doc queries, web search, cross-domain discovery)
- Opportunity assessment with calibrated rubrics
- Artifact generation following your templates and voice
- JPD push formatting and field mapping

See `CLAUDE.sample.md` for the full configuration contract with placeholder values.

## Usage

The pipeline runs left to right: capture (external), then refine-seed, develop, draft, refine.

```
/refine-seed foraging-intelligence
```
Interprets the seed, drafts structured fields, surfaces related ideas, presents for your alignment.

```
/develop foraging-intelligence
```
Researches and synthesizes into a TL;DR card with opportunity assessment and impact dimensions.

```
/draft foraging-intelligence
```
Prompts for output format (strategy doc or product brief), creates a first draft in `Output/`.

```
/refine foraging-intelligence
```
Iterates on the output document section-by-section until you approve it as complete.

Enrichment agents run independently at any time:
```
/edtech-sme foraging-intelligence
/educator-sme foraging-intelligence
/tam-estimate foraging-intelligence
/cross-domain foraging-intelligence
/divergent-thinking foraging-intelligence
```

Push to Jira Product Discovery when the idea is mature:
```
/jpd-push foraging-intelligence
```

## How It Works

Ideas move through five stages: **Seed** (raw capture with frontmatter), **Developing** (researched TL;DR card), **Drafting** (first output document), **Refining** (iterative collaboration), and **Complete** (human-approved).

The system uses a two-track architecture. Idea cards in `Ideas/` progressively accumulate content through Stages 0-2 and serve as scannable, shareable artifacts. Output documents in `Output/` are separate files created at Stage 3, linked from the idea card via frontmatter.

Seven custom agents handle specialized reasoning: `develop-synthesis` (Opus) does the strategic judgment work, `artifact-critic` (Sonnet) checks conformance, and five domain-specific agents provide enrichment research. The `/develop` skill orchestrates research and agent dispatch.

Human decision authority is preserved at every meaningful gate. Seeds develop autonomously, but all stage transitions beyond Stage 1, output format decisions, and final approvals require human initiation or sign-off.

## Customization

The system ships with domain knowledge tuned for education technology and assessment products. To adapt it:

- **Different product domain:** Update `persona.md` with your voice, update the agent personas in `claude/agents/` (especially `edtech-sme.md`, `educator-sme.md`, `tam-estimate.md`) with your market's domain knowledge, and update the organizational taxonomy in `claude/skills/cross-domain/`.
- **Different output formats:** Replace or modify the templates in `Templates/` and update `incubator-approach.md` with your methodology.
- **Without JPD integration:** Skip `jira-config.md` setup. The `/jpd-push` and `/cross-domain` skills are self-contained and can be ignored.
- **Without enrichment agents:** Each enrichment agent is independently invokable. Remove any you don't need from `claude/skills/` and `claude/agents/` without affecting the core pipeline.

## Security

Review skills before installing. They load into Claude's context and execute with your permissions. Audit the contents of `claude/skills/` and `claude/agents/` before use.

## License

MIT. See [LICENSE](LICENSE).
