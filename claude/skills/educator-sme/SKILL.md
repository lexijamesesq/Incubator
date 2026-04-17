---
name: educator-sme
description: This skill should be used when the user asks to "get educator feedback on [idea]", "educator evaluation of [idea]", "teacher perspective on [idea]", "classroom reality check for [idea]", or "educator SME review of [idea]". Evaluates a strategic idea through the lens of a veteran educator — 20+ years K-12 and higher ed — focused on pedagogical practice, classroom reality, and adoption likelihood.
argument-hint: [idea-name]
context: fork
agent: educator-sme
disable-model-invocation: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - WebSearch
  - WebFetch
  - Bash(date:*)
  - Bash(python3 scripts/research-db.py:*)
---

# /educator-sme — Educator SME Evaluation

Evaluates a strategic idea through the lens of a veteran educator with 20+ years spanning K-12 and higher ed. Produces an unfiltered assessment of pain point validity, adoption realism, and classroom impact. This is an enrichment agent — it adds a research artifact without changing the idea's stage.

## Invocation

```
/educator-sme [idea-name]
```

- Required argument: the name of an idea file in `Ideas/`
- Works on ideas at any stage (seed, developing, drafting, refining)
- Examples: `/educator-sme foraging-intelligence`, `/educator-sme cache-optimization`

## Arguments

Parse `$ARGUMENTS` to resolve the target idea file.

**Resolution rules:**

| Input | Behavior |
|-------|----------|
| Empty | List all ideas in Ideas/, ask user to select |
| `idea-name` | Resolve to `Ideas/{idea-name}.md` |
| `idea-name.md` | Strip `.md`, resolve as above |

**Fuzzy matching:** If exact match fails, list all `.md` files in Ideas/ and find filenames containing the argument as a substring (case-insensitive). If exactly one match, use it. If multiple matches, present options and ask user to pick. If zero matches, report and exit.

## Persona

This skill runs in the educator-sme agent's context. The agent carries the full veteran educator persona (20+ years K-12 and higher ed), domain calibration framework, evaluation dimensions, and quality standards. See `.claude/agents/educator-sme.md`.

## Execution Flow

Execute these steps in order. Stop and report errors at any step rather than continuing with bad data.

### Step 0: Parse Arguments

1. Read `$ARGUMENTS`
2. If empty: use `Glob` to list all `.md` files in `Ideas/`. Read the first 20 lines of each to extract the idea title from the body content. Present all ideas to the user (any stage) and ask them to select one. If no ideas exist, report "No ideas found in Ideas/" and exit.
3. If provided: attempt to resolve `Ideas/{argument}.md`
   - Try exact match first (with and without `.md` extension)
   - If not found, try fuzzy substring match against all filenames in Ideas/
   - If exactly one fuzzy match, use it
   - If multiple fuzzy matches, present options and ask user to pick
   - If zero matches, report "Idea file not found: {argument}. Available files in Ideas/: {list}" and exit

### Step 1: Load Context

Read the idea file at the resolved path — full content (frontmatter + body).

Extract:
- **Core insight** — from the body content
- **Problem statement** — from `Problem it addresses` if present (Stage 2+), or infer from core insight (Stage 1)
- **Domain** — from frontmatter `domain` field, used for K-12 vs. higher ed calibration:
  - `assessments` — evaluate both K-12 and higher ed perspectives
  - `platform` — evaluate from downstream classroom impact
  - `cross-product` — evaluate both segments, note where they diverge

**Shared research baseline:** Read `Research/shared/assessments/customer-evidence.md` if it exists. Use within-TTL entries as known starting points for customer pain signals and adoption evidence — do not rediscover patterns already documented there. Treat past-TTL entries as directional only. If the file does not exist, proceed without it.

**Database augmentation:** Additionally, query the strategy research database for structured customer evidence and educator-relevant findings:
```bash
python3 scripts/research-db.py query-landscape --json '{"capabilities": ["cap-slug-1", "cap-slug-2"]}'
```
Derive capability slugs from the idea's `themes` field. Database findings supplement the shared research file. During Step 4 (Optional Research), if web research surfaces a competitor or methodology, use `query-competitor` for a targeted deep-dive on what the database already knows about it.

Context exclusions (strategy docs, OKRs, persona guide, competitive data, business framing) are enforced by the agent's scope constraints.

### Step 2: Calibrate Perspective

Calibrate your perspective based on the idea's domain field using your domain calibration framework (K-12, higher ed, platform/infrastructure).

### Step 3: Evaluate (5 Dimensions)

Work through your five evaluation dimensions (Pain Point Validity, Adoption Realism, Workflow Integration, The Skeptic's Objection, The Champion's Argument) with educator-grounded specificity. Every claim must connect to a concrete classroom reality.

**Dimension-to-output mapping:**
- Pain Point Validity → "Pain Point Analysis" section
- Adoption Realism → "Adoption Assessment" verdict + "Adoption Barriers" section
- Workflow Integration → Folds into both "Pain Point Analysis" (current state) and "Adoption Barriers" (transition friction)
- The Skeptic's Objection → "What Would Make Educators Skeptical" section
- The Champion's Argument → "What Would Make Educators Champions" section

The "Strongest Use Case" and "Suggested Refinements" output sections synthesize across all five dimensions.

### Step 4: Optional Research

If the idea makes specific pedagogical claims or references methodologies that need validation, use `WebSearch` to check:
- Educator sentiment on the specific methodology (e.g., "teacher opinions on standards-based grading")
- Research on similar interventions and their adoption rates
- Adoption data for comparable edtech tools
- Educator community discussions (Reddit r/Teachers, education blogs, union publications)

If the idea is straightforward enough to evaluate from educator experience alone, skip this step and note "No external research needed — evaluation based on educator practice knowledge."

### Step 5: Write Research Artifact

1. Use `Bash(date:*)` to get today's date in YYYY-MM-DD format
2. Create directory if needed: `Research/{idea-name}/`
   - Use `Glob` to check if it exists first
   - If not, create it with `Bash(date:*)` — actually, use the Write tool which will create parent directories
3. Write `Research/{idea-name}/educator-evaluation.md` with this structure:

```markdown
---
type: incubator/research
research-type: educator-sme-evaluation
idea: {idea-name}
date: {YYYY-MM-DD}
domain-calibration: {k12 | higher-ed | both | platform-downstream}
---

# Educator SME Evaluation: {Idea Title}

**Evaluated:** {YYYY-MM-DD}
**Idea stage at evaluation:** {stage from frontmatter}
**Domain calibration:** {K-12 / Higher Ed / Both / Platform (downstream impact)}

## Adoption Assessment: {High / Medium / Low}
**Verdict:** {One direct sentence.}

## Pain Point Analysis
{2-3 sentences on problem reality and severity from an educator's daily experience.}

## Adoption Barriers
{Specific friction points — concrete workflow realities, not abstractions. What specifically makes this hard to adopt?}

## What Would Make Educators Skeptical
{The eye-roll reaction. Be blunt. Channel the veteran teacher who's seen it all.}

## What Would Make Educators Champions
{The excitement moment. Be specific — describe the scenario, not the feature.}

## Strongest Use Case
{One concrete scenario: role, context, what happens, outcome. Make it vivid.}

## Suggested Refinements
{2-3 specific adjustments that address the barriers identified above. Actionable, not vague.}

## Research Notes
{If Step 4 was performed: queries, findings, sources. If skipped: "Evaluation based on educator practice knowledge — no external research needed."}
```

4. Update the idea file's frontmatter: append the research artifact path to the `research: []` array.
   - Read the idea file to get current frontmatter
   - The path to append is: `Research/{idea-name}/educator-evaluation.md`
   - If `research` already contains this path (re-evaluation), the new file overwrites the old one; do not duplicate the path in the array
   - Use `Edit` to update the frontmatter — find the `research:` line and update it
   - Do NOT modify any other frontmatter fields
   - Do NOT modify the idea body content
   - Do NOT change the idea's stage

### Step 6: Present Results

Present the evaluation to the user in this format:

```
Educator SME Evaluation: {idea-name}

**Adoption Assessment: {High / Medium / Low}**
{One-sentence verdict}

**Pain Point Analysis:**
{2-3 sentences}

**Adoption Barriers:**
{Specific friction points}

**The Skeptic Says:**
{Eye-roll reaction}

**The Champion Says:**
{Excitement moment}

**Strongest Use Case:**
{Concrete scenario}

**Suggested Refinements:**
{2-3 adjustments}

**Impact dimension signals:**
- Customer sentiment: {what this evaluation suggests — high/medium/low signal and why}
- User experience: {what this evaluation suggests — high/medium/low signal and why}

Research artifact written to: Research/{idea-name}/educator-evaluation.md
Idea frontmatter updated: research array now includes educator evaluation path.
```

After presenting the above, review your findings against the shared research capture heuristic: **Sourced + Durable + Decision-relevant + Shared** (applies to pain point evidence, adoption patterns, and educator sentiment that would benefit other ideas). Write qualifying findings directly to `Research/shared/assessments/customer-evidence.md` using the entry schema defined in the file header. Each entry's `Source:` field must include the specific URL from your web search — the most specific available page (press release, research page, blog post), not a homepage. If no stable URL exists, use the most authoritative available page. If no findings qualify, skip this step. Note in the presentation which entries were added:

> **Shared research updated:** `customer-evidence.md`: +{N} entries ({brief descriptions})

**Database write-back:** Additionally, write qualifying findings to the strategy research database:
```bash
python3 scripts/research-db.py write-findings --json '{
  "findings": [
    {
      "claim": "...",
      "evidence": "...",
      "confidence": "high|medium|low",
      "source_url": "...",
      "source_description": "...",
      "ttl_months": 12,
      "topic": "customer-evidence",
      "category": "pain-signal|research-validation|adoption-signal",
      "capabilities": ["slug-1", "slug-2"],
      "competitor_id": null
    }
  ]
}'
```

Note: The impact dimension signals are advisory — they indicate what this evaluation suggests for the `customer-sentiment` and `user-experience` frontmatter fields, but this skill does NOT modify those fields. That's done during the development workflow or manually by the human.

## Stop Rules

| Condition | Action |
|-----------|--------|
| Idea file not found | Fuzzy match attempt, then report available files and exit |
| Idea too abstract for educator lens | Report: "This idea is too abstract to evaluate from a classroom perspective. To proceed, ground it in a specific educator workflow or student outcome." Ask human to refine. |
| No meaningful educator touchpoint | Report: "This idea is pure infrastructure with no downstream classroom impact I can evaluate. The educator perspective doesn't apply here." Exit cleanly. |
| Research directory creation fails | Report the error and exit |
| Idea file has malformed frontmatter | Report parsing issue with specifics, exit |

## Error Handling Summary

| Condition | Behavior |
|-----------|----------|
| No argument and no ideas exist | Report "No ideas found in Ideas/" and exit |
| Idea file not found | Report with available filenames from Ideas/ listing, exit |
| Frontmatter cannot be parsed | Report parsing issue, exit |
| Domain field missing from frontmatter | Default to "both" (K-12 and higher ed), note the assumption |
| Research directory already exists | Proceed — write/overwrite the evaluation file |
| Educator evaluation already exists | Overwrite with fresh evaluation, do not duplicate research path in frontmatter |
| WebSearch returns no relevant results | Note "No relevant educator sentiment found for {query}" and continue with practice-based evaluation |

## Scope Boundaries

This skill does NOT:
- Change the idea's stage (enrichment only)
- Modify the idea body content
- Modify impact dimension frontmatter fields (advisory signals only)
- Recommend go/no-go decisions (that's a human decision)

