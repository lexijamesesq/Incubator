---
name: edtech-sme
description: This skill should be used when the user asks to "get market analysis for [idea]", "edtech evaluation of [idea]", "competitive analysis for [idea]", "market perspective on [idea]", or "edtech SME review of [idea]". Evaluates a strategic idea against edtech market dynamics, competitive landscape, buyer behavior, and technology trends from an industry analyst perspective.
argument-hint: [idea-name]
context: fork
agent: edtech-sme
disable-model-invocation: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - WebSearch
  - WebFetch
  - Bash(date:*)
---

# /edtech-sme — EdTech Market Analysis (Enrichment Agent)

Evaluates a strategic idea against edtech market dynamics, competitive landscape, buyer behavior, and technology trends. Produces a research artifact from an outside-in industry analyst perspective. This is an enrichment agent — it does NOT change the idea's stage.

## Invocation

```
/edtech-sme [idea-name]
```

- Required argument: the name of an idea file in `Ideas/`
- Works on ideas at any stage (seed, developing, drafting, refining)
- If no argument provided: list available ideas and ask the user to pick
- Examples: `/edtech-sme foraging-intelligence`, `/edtech-sme cache-optimization`

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

This skill runs in the edtech-sme agent's context. The agent carries the full industry analyst persona, domain knowledge (competitors, buyer dynamics, dual-role entities), evaluation framework, and quality standards. See `.claude/agents/edtech-sme.md`.

**Output serves two purposes:**
- **Enrichment:** Feeds into the idea's `industry-disruption`, `revenue-potential`, and `strategic-alignment` impact dimension assessments
- **Research artifact:** Preserved at `Research/[idea-name]/edtech-market-analysis.md` for reference during drafting and refining stages

## Execution Flow

Execute these steps in order. Stop and report errors at any step rather than continuing with bad data.

### Step 0: Parse Arguments

1. Read `$ARGUMENTS`
2. If empty: use `Glob` to list all `.md` files in `Ideas/`. Present all ideas to the user (with their stage from frontmatter) and ask them to select one. If no ideas exist, report "No ideas found in Ideas/" and exit.
3. If provided: attempt to resolve `Ideas/{argument}.md`
   - Try exact match first (with and without `.md` extension)
   - If not found, try fuzzy substring match against all filenames in Ideas/
   - If exactly one fuzzy match, use it
   - If multiple fuzzy matches, present options and ask user to pick
   - If zero matches, report "Idea file not found: {argument}. Available files in Ideas/: {list}" and exit

### Step 1: Load Context

Read the idea file at the resolved path — full content including frontmatter and body.

Extract from the idea file:
- **Core insight** — the central idea being evaluated
- **Themes** — from frontmatter `themes: []` array
- **Domain** — from frontmatter `domain:` field
- **Stage** — from frontmatter `stage:` field (for reporting, not gating)
- **Existing research** — from frontmatter `research: []` array (to avoid duplicating work)

**Shared research baseline:** Read `Research/shared/assessments/competitive-landscape.md` if it exists. Use within-TTL entries as known starting points — do not rediscover competitors already documented there. Treat past-TTL entries as directional only (relevant categories and framing, not current positioning). If the file does not exist, proceed without it.

Context exclusions (strategy docs, OKRs, persona guide, approach docs) are enforced by the agent's scope constraints.

### Step 2: Frame Market Lens

Before researching, frame the idea through your market lens — product category, buyer, competitive frame, and technology bets.

If the idea spans multiple product categories, identify all relevant categories for expanded competitor scanning.

If the idea is too abstract for market analysis — no discernible product concept, buyer, or competitive frame — fire the stop rule (see Stop Rules section).

### Step 3: Research Competitive Landscape

Use `WebSearch` to gather current market intelligence. Execute 4-6 targeted searches derived from the idea's themes, competitive frame, and product category.

**Search targets:**
- Competitor features and recent product launches in the relevant category
- Acquisitions, mergers, and strategic partnerships in edtech assessment
- Analyst commentary (EdSurge, EdTech Magazine, Gartner, HolonIQ)
- Regulatory developments (state/federal assessment mandates, accessibility requirements, AI policy in education)
- Platform shifts and technology trends (AI in assessment, interoperability standards like QTI/LTI, competency-based education movement)

**When the idea spans multiple product categories**, expand the competitor scan to include adjacent-category players. Name specific companies from each relevant category — do not limit to direct assessment competitors.

**Research quality standards:**
- Name competitors, cite specific products, reference real dynamics
- Capture source URLs for all findings
- Flag any knowledge that is more than 18 months old
- Prioritize depth over breadth — 4 strong findings beat 8 shallow ones

**Cross-idea awareness:** If your competitive research reveals that the same competitor landscape applies to another idea you've seen in the Ideas/ directory (from the argument resolution step), note it in the artifact: "Competitive overlap: similar landscape applies to [other-idea-name]." This is informational only — do not modify the other idea's files.

If `WebSearch` returns no relevant results for a query, note it and try an alternative search angle. If no competitive data is found across all searches, proceed with low-confidence flags (see Error Handling).

### Step 4: Evaluate (4 Dimensions)

Using the idea context and research findings, evaluate across your four dimensions: Market Fit, Competitive Positioning, Technology Risk, and Go-to-Market.

For Competitive Positioning, build a competitor comparison table with specific companies, their relevant capabilities, and how your organization would compare (Differentiation / Parity / Behind). Write a positioning narrative: 2-3 sentences on where your organization lands.

For Technology Risk, rate as Low / Medium / High. For ideas with emerging technology themes, explicitly assess the gap between current capability and institutional deployment readiness.

### Step 5: Assess Strategic Timing

Analyze the market window with specific signals:
- Is the market moving toward this idea or away from it?
- What external forces (regulatory, technological, competitive) create urgency or reduce it?
- Is there a first-mover advantage, or is fast-follower safer?
- Specific timing signals: funding cycles, regulatory deadlines, competitor roadmap signals, technology maturity curves

### Step 6: Write Research Artifact

1. Get today's date using `Bash(date:*)`: `date +%Y-%m-%d`
2. Create directory `Research/{idea-name}/` if it does not exist (use `Bash` to `mkdir -p`)
3. Write the research artifact to `Research/{idea-name}/edtech-market-analysis.md`

**Artifact structure:**

```markdown
---
type: incubator/research
agent: edtech-sme
idea: {idea-name}
created: {YYYY-MM-DD}
confidence: high | medium | low
---

# EdTech Market Analysis: {Idea Title}

**Idea:** {Core insight from idea file}
**Analysis date:** {YYYY-MM-DD}
**Confidence level:** {High/Medium/Low — High: strong data across all dimensions. Medium: gaps in 1-2 dimensions. Low: thin data, limited competitive intelligence.}

## Market Fit Assessment: {Strong / Moderate / Weak}

{One-sentence verdict.}

{2-4 sentences of supporting analysis. Buyer-centric: willingness to pay, not product excitement. Reference specific market signals.}

## Competitive Positioning

| Competitor | Relevant Capability | Comparison |
|------------|---------------------|------------|
| {Name} | {What they do} | {Differentiation / Parity / Behind} |

**Positioning narrative:** {2-3 sentences. Where your organization lands relative to competitors. Honest assessment.}

## Technology Risk: {Low / Medium / High}

{2-3 specific sentences. Maturity for institutional deployment, integration requirements, build/buy/partner considerations.}

## Go-to-Market Considerations

{3-4 sentences: buyer alignment, pricing model, sales channel, regulatory factors.}

## Strategic Timing

{2-3 sentences on market window. Specific signals — regulatory deadlines, competitor moves, technology maturity, funding cycles.}

## Key Risks

- {Specific market risk 1}
- {Specific market risk 2}
- {Specific market risk 3}
- {Specific market risk 4 — if applicable}

## Opportunity Signal Strength: {Strong / Moderate / Weak}

{One synthesizing sentence connecting market fit, competitive positioning, technology risk, and timing to overall opportunity quality. Connect to MAU x ARPU = ARR where applicable.}

## Research Sources

- {Source 1 with URL}
- {Source 2 with URL}
- {Source 3 with URL}
```

4. Update the idea file frontmatter: append `Research/{idea-name}/edtech-market-analysis.md` to the `research: []` array

   **Frontmatter update rules:**
   - Read the current frontmatter to get the existing `research:` array
   - Append the new path to the array (do not overwrite existing entries)
   - If the path already exists in the array (from a previous run), replace it rather than duplicating
   - Do NOT change any other frontmatter fields (especially `stage:`)
   - Use `Edit` to make the targeted frontmatter change

### Step 7: Present Results

Present the completed analysis to the user with:

```
EdTech market analysis complete: {idea-name}

**Market Fit:** {Strong/Moderate/Weak} — {one-sentence verdict}

**Top Competitors:**
- {Competitor 1}: {capability} — {Differentiation/Parity/Behind}
- {Competitor 2}: {capability} — {Differentiation/Parity/Behind}
- {Competitor 3}: {capability} — {Differentiation/Parity/Behind}

**Technology Risk:** {Low/Medium/High} — {one-sentence summary}

**Key Risks:**
- {Risk 1}
- {Risk 2}

**Opportunity Signal Strength:** {Strong/Moderate/Weak} — {synthesizing sentence}

**Impact dimension implications:**
- industry-disruption: {Suggested Low/Med/High based on competitive positioning}
- revenue-potential: {Suggested Low/Med/High based on market fit and go-to-market}
- strategic-alignment: {Suggested Low/Med/High based on timing and market direction}

**Research artifact:** Research/{idea-name}/edtech-market-analysis.md
**Confidence:** {High/Medium/Low}
```

After presenting the above, review your findings against the shared research capture heuristic: **Sourced + Durable + Decision-relevant + Shared** (applies to competitor entries, market dynamics, and positioning data that would benefit other ideas). Write qualifying findings directly to `Research/shared/assessments/competitive-landscape.md` using the entry schema defined in the file header. Each entry's `Source:` field must include the specific URL from your web search — the most specific available page (press release, feature page, report), not a homepage. If no stable URL exists, use the most authoritative available page. If no findings qualify, skip this step. Note in the presentation which entries were added:

> **Shared research updated:** `competitive-landscape.md`: +{N} entries ({brief descriptions})

## Stop Rules

| Condition | Action |
|-----------|--------|
| Idea too abstract for market analysis (no discernible product concept, buyer, or competitive frame) | Report: "This idea is too abstract for market analysis. To evaluate market dynamics, I need a clearer product concept — what would the buyer be purchasing?" Ask human to refine before rerunning. Exit. |
| No competitive data found across all searches | Proceed with low-confidence flags on all dimensions. Write artifact noting data limitations. Present results with explicit confidence warnings. |

**Note:** Unlike the Development Session Workflow, this agent does NOT have stop rules for weak ideas or thin strategic connections. The EdTech SME evaluates whatever it receives — a weak market fit is a valid finding, not a reason to stop. Even ideas with no competitive landscape or unclear product concepts get an honest "Weak" assessment rather than a refusal to evaluate.

## Error Handling

| Condition | Behavior |
|-----------|----------|
| No argument and no ideas exist | Report "No ideas found in Ideas/" and exit |
| Idea file not found | Fuzzy match against available filenames. If no match, report with available filenames and exit |
| Idea too abstract for market lens | Report what is missing (product concept, buyer persona, competitive frame) and ask human for refinement. Exit. |
| No competitive data available | Write artifact with low confidence flags on all dimensions. Note data limitations explicitly in each section. |
| WebSearch returns no results for a query | Note the failed query, try alternative search angle. If all searches fail, proceed with low confidence. |
| Research directory creation fails | Report error with specifics, exit |
| Frontmatter update fails | Report error, note the research artifact was written successfully and the frontmatter path needs manual addition. Exit. |

## Scope Boundaries

This skill does NOT:
- Change the idea's stage (enrichment only)
- Modify the idea body content (only appends to `research:` frontmatter array)
- Recommend go/no-go decisions (that is a human decision)

