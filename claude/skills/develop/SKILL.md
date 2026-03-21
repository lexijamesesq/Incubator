---
name: develop
description: This skill should be used when the user asks to "develop an idea", "develop [idea name]", "work on [idea name]", or "move [idea] to developing". Transforms a seed-stage idea into a researched TL;DR nugget (Stage 1→2) by researching strategic context, market intelligence, and related ideas, then delegating strategic synthesis to the develop-synthesis agent.
argument-hint: [idea-name]
context: conversation
disable-model-invocation: false
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - Bash(date:*)
  - Skill
---

# /develop — Seed Development Session (Stage 1→2)

Transforms a seed-stage idea into a researched, assessed TL;DR nugget. Researches strategic context, market intelligence, and related ideas, then delegates strategic synthesis to the develop-synthesis agent running in an isolated context optimized for judgment-heavy work.

## Invocation

```
/develop [idea-name]
```

- Required argument: the name of a seed-stage idea file in `Ideas/`
- If no argument provided: list available seed-stage ideas and ask the user to pick
- Examples: `/develop foraging-intelligence`, `/develop cache-optimization`

## Arguments

Parse `$ARGUMENTS` to resolve the target idea file.

**Resolution rules:**

| Input | Behavior |
|-------|----------|
| Empty | List all seed-stage ideas in Ideas/, ask user to select |
| `idea-name` | Resolve to `Ideas/{idea-name}.md` |
| `idea-name.md` | Strip `.md`, resolve as above |

**Fuzzy matching:** If exact match fails, list all `.md` files in Ideas/ and find filenames containing the argument as a substring (case-insensitive). If exactly one match, use it. If multiple matches, present options and ask user to pick. If zero matches, report and exit.

## Role

You are the orchestrator for the /develop pipeline. You handle research, human interaction, and coordination. Strategic synthesis is delegated to the develop-synthesis agent, which runs in an isolated context with a clean window optimized for judgment-heavy work.

You are working on behalf of the role specified in CLAUDE.md (Configuration > Role). Your output serves two audiences:
- **Internal:** The user uses TL;DR nuggets to prioritize which ideas to develop further
- **External:** TL;DR nuggets may be pushed to JPD for stakeholder visibility via /jpd-push

## Execution Flow

Execute these steps in order. Stop and report errors at any step rather than continuing with bad data.

### Step 0: Parse Arguments

1. Read `$ARGUMENTS`
2. If empty: use `Glob` to list all `.md` files in `Ideas/`. Read each file until the first `###` heading or 40 lines (whichever comes first) to check frontmatter for `stage: seed`. Present seed-stage ideas to the user and ask them to select one. If no seed-stage ideas exist, report "No seed-stage ideas found in Ideas/" and exit.
3. If provided: attempt to resolve `Ideas/{argument}.md`
   - Try exact match first (with and without `.md` extension)
   - If not found, try fuzzy substring match against all filenames in Ideas/
   - If exactly one fuzzy match, use it
   - If multiple fuzzy matches, present options and ask user to pick
   - If zero matches, report "Idea file not found: {argument}. Available files in Ideas/: {list}" and exit

### Step 1: Load Context

Load these files in parallel:

1. **Seed file** at the resolved path — full content
2. **Persona guide** — `persona.md`
3. **OKRs** — Read the OKRs document (path configured in CLAUDE.md under Configuration > External References > `strategic_context.okrs`)
4. **Idea index** — Use `Glob` to list all `.md` files in `Ideas/`, then apply tiered reading:
   - **Complete-stage ideas:** Read frontmatter only (first 25 lines or until `---` closes). Extract: stage, themes, domain. These provide theme vocabulary only — complete ideas are excluded from Step 3 matching.
   - **All other ideas (seed, developing, drafting, refining):** Read until first `###` heading or 40 lines. Extract: frontmatter + header fields (Core insight, Problem, Who cares, Strategic connection). Used for Step 3 matching AND portfolio context in the synthesis handoff.
   From the loaded index, extract all unique `themes` values across all idea files into a **portfolio theme vocabulary** — the canonical set of themes in use. Used in Step 5d to ensure theme reuse.
5. **Shared research baseline** — Read the following files from `Research/shared/assessments/`:
   - `customer-evidence.md` (for Customer Sentiment rating)
   - `competitive-landscape.md` (for Industry Disruption rating)
   - `market-sizing.md` (for Revenue Potential rating)
   Check TTL on each entry: entries within TTL are usable as baseline; entries past TTL are directional only and require reverification during Stream A/B research.

### Step 2: Validate the Seed

Confirm the seed file has:
- `stage: seed` in frontmatter
- Core insight populated in body (non-empty)
- Source populated in body (non-empty)
- Initial strategic connection populated in body (non-empty)
- `domain` set in frontmatter
- `themes` with at least one entry in frontmatter

**If any required field is missing:** Report exactly which fields are missing and exit. Do not proceed with incomplete seeds.

**If `stage` is not `seed`:** Report "Idea '{name}' is at stage '{current-stage}', not 'seed'. This skill only develops seed-stage ideas." and exit.

### Step 3: Verify Seed Refinement

**Prerequisite:** Seeds should be refined via `/refine-seed` before development. Refinement handles intent clarification (capability-absent vs. experience-broken), header field drafting, related ideas matching, and merge/keep decisions.

Check the seed file for refinement indicators:
- **Core insight** populated (non-empty, one sentence)
- **Initial strategic connection** populated (names a priority and mechanism)
- **related-ideas** frontmatter resolved (may be empty if no relations exist — that's valid)

**If header fields are missing or empty:** Report: "Seed '{name}' appears unrefined — Core insight and/or Strategic connection missing. Run `/refine-seed {name}` first to clarify intent and position in the portfolio, then re-run /develop." Exit.

**If header fields are present:** Proceed. The seed has been through intent refinement and is ready for research.

### Step 4: Research

Conduct three research streams sequentially. Prioritize depth over breadth — 3 strong findings beat 10 shallow ones.

**Stream A: Internal Strategic Context**

- Grep the product strategy document (path configured in CLAUDE.md under Configuration > External References > `strategic_context.product_strategy`) for the seed's theme keywords and domain terms. Extract relevant passages. Never load the full file.
- Scan the seed file's `### Original Capture` section for strategic signals, connections, or context that didn't make it into the seed's structured fields. Raw captures often contain intuitive connections and half-formed insights that inform research direction.
- Grep the design strategy document (path configured in CLAUDE.md under Configuration > External References > `strategic_context.design_strategy`) for relevant design priorities.
- Reference the OKRs loaded in Step 1 — identify which 2026 goals this idea would advance.
- **NPS customer signal check:** For the relevant product(s), read the **Top Pain Points** and **The Signal** sections from the 2-3 most recent monthly analysis files in the NPS analysis directories (paths configured in CLAUDE.md under Configuration > External References > `metrics.nps_product_a` and `metrics.nps_product_b`). These sections contain the concise pain points and emerging patterns. If a pain point matches the seed's problem space and deeper evidence is needed, read the **3 Things That Matter** section from that same file for verbatim quotes and trend data. Do not read raw CSV data or full analysis files. NPS findings directly inform the Customer Sentiment dimension rating.
- **Shared research check:** Review entries from `customer-evidence.md` loaded in Step 1 for findings relevant to this idea's problem space. Note which shared entries are within TTL (usable as baseline) versus past TTL (directional only — reverify). Shared customer evidence findings supplement, not replace, the NPS and strategy doc checks above.
- For each finding, note connection strength: **direct** (explicitly named), **adjacent** (related priority, plausible mechanism), or **indirect** (thematic only).

**Stream B: Market Intelligence**

- **Shared research check:** Review entries from `competitive-landscape.md` and `market-sizing.md` loaded in Step 1. Use within-TTL entries as the starting baseline — focus web searches on verifying, extending, or filling gaps rather than rediscovering known landscape. Past-TTL entries are directional only — reverify before relying on them.
- Use `WebSearch` for competitor landscape, market trends, technology enablers, and customer signals.
- Execute 3-5 targeted searches derived from the seed's themes and core insight.
- Capture findings with source URLs.
- Target: named competitors, specific capabilities, market sizing signals, technology shifts.

**Stream C: Cross-Domain Discovery**

Invoke `/cross-domain {idea-name}` to query the JPD project for ideas from other product domains with functional overlap. This runs the standalone cross-domain skill, which:
- Queries across all statuses and brands (excluding your own brand per jira-config.md)
- Classifies signals as Direct overlap, Enabler/dependency, or Convergence
- Detects convergence groups (multiple teams solving the same problem)
- Writes a research artifact to `Research/{idea-name}/cross-domain-signals.md`
- Updates the idea's `research:` frontmatter array

Incorporate the 1-3 strongest signals into the synthesis handoff (Step 4.5). Include inline issue key links for traceability.

If `/cross-domain` reports "could not check" (MCP auth/timeout), note "Cross-domain discovery unavailable — {reason}" in the handoff and continue. Do not block development on MCP availability.

### Step 4.5: Create Synthesis Handoff

After research completes, create the handoff artifact at `Research/{idea-name}/synthesis-handoff.md`. Create the directory if it does not exist.

This artifact is the curated research input for the synthesis agent. Preserve specific data points, named capabilities, URLs, issue keys, and connection strengths — the synthesis agent depends on this specificity.

```markdown
# Research Handoff: {idea-name}

**Date:** {today}
**Idea:** {title from seed}
**Seed core insight:** {from seed body}
**Seed strategic connection:** {from seed body}

---

## Strategic Context (Stream A)

### Product Strategy — {connection strength}
- {Finding with connection strength noted}
- {Finding with connection strength noted}

### Design Strategy — {connection strength}
- {Finding with specific design priority named}

### OKR Connections
- {OKR reference}: {how this idea advances it}

### NPS / Customer Evidence
- {Product} ({date range}): {key finding or "Zero mentions of {topic}"}
- **Key finding:** {synthesis of NPS evidence or absence}

### Shared Research Baseline (within TTL)
- {Finding} ({confidence level})
- {Finding} ({confidence level})

---

## Market Intelligence (Stream B)

### {Topic Cluster}
- {Finding with source URL}
- {Finding with source URL}

### Named Competitors
- **{Competitor} ({Parent}):** {capabilities and gaps} ([Source](url))
- **{Competitor}:** {capabilities and gaps} ([Source](url))

### {Additional Topic Cluster}
- {Findings}

---

## Cross-Domain Discovery (Stream C)

### Key Signals
- **{issue-key}: {Title}** ({Brand}, {Status}) — {description}. {Signal type}.
- **{issue-key}: {Title}** ({Brand}, {Status}) — {description}. {Signal type}.

### Convergence Group
{Description of convergence pattern if detected}

---

## Research Synthesis

**Strategic connection:** {Strong/Medium/Weak}. {1-2 sentence summary of why.}

**Market validation:** {Strong/Medium/Weak}. {1-2 sentence summary.}

**Customer evidence:** {Strong/Medium/Weak}. {1-2 sentence summary. Note latent vs. articulated demand.}

**Competitive gap:** {Confirmed/Partial/Unconfirmed}. {1-2 sentence description of the gap.}

---

## Portfolio Context

### Related Ideas (header fields for differentiation)

{For each related idea identified in Step 3:}

**{idea-name}** ({stage})
- Core insight: {from their card}
- Problem: {from their card}
- Who cares: {from their card}
- Strategic connection: {from their card}
```

Populate from Step 4 research findings. Sections with no findings should note the absence explicitly (e.g., "Zero mentions of {topic} in NPS data" or "Cross-domain discovery unavailable — MCP timeout").

### Step 5: Strategic Synthesis

Invoke the synthesis agent to produce the TL;DR card content.

**Invoke via Skill tool:**
Use the Skill tool with skill name `develop-synthesis`, passing the idea name as the argument.

The develop-synthesis skill runs in an isolated agent context with a clean window. It reads the seed file, the synthesis handoff (created in Step 4.5), the persona guide, the format example, and related ideas context. It produces the completed TL;DR card — frontmatter updates (stage, dimensions) and body content (header fields, opportunity assessment, research summary, thought outline, open questions).

After the agent returns, read the updated idea file to confirm synthesis completed (stage changed to `developing`, impact dimensions populated).

If the agent reports insufficient research or a stop condition, surface it to the user and halt.

### Step 5c: Buildable Surface Check

After synthesis completes, invoke the buildable surface enrichment agent to check whether the Thought Outline is principle-shaped or feature-shaped.

**Invoke via Skill tool:**
Use the Skill tool with skill name `buildable-surface`, passing the idea name as the argument (e.g., `foraging-intelligence`).

The buildable-surface skill runs in an isolated agent context. It reads the idea card and research artifacts, applies a three-signal detection heuristic, and either:
- **No-ops** (feature-shaped) — no section added, proceed to Step 6
- **Fires** (principle-shaped or borderline) — writes a `### Buildable Surface` section between Thought Outline and Open Questions

Either way, proceed to Step 5d. If the skill reports an error (e.g., research too thin for grounded candidates), note it in the Step 9 presentation and proceed.

### Step 5d: Theme Management

Using the portfolio theme vocabulary collected in Step 1 and the research findings from Step 4, assess whether the seed's theme classifications still hold.

**General theme assessment:**
- For each existing theme: does research confirm this idea is substantively about this theme, or was it a surface-signal classification? Remove if incidental.
- For themes in the portfolio vocabulary NOT on the seed: did research reveal a genuine connection the router missed? Add if substantive. Only use existing themes — never invent new ones.
- Minimum one theme per idea.

**ai-capabilities special case:**

Does AI make or break this idea?
- **Requires AI** → add the tag. The feature doesn't work without it.
- **Enhanced by AI** → add the tag. Works without AI, but AI is a natural progressive enhancement — not forced.
- **AI would be forced** → don't add. Solution looking for a problem.

Check the research before deciding — cross-domain signals, buildable surface candidates, and competitive landscape show what the market assumes about the mechanism.

**Record all changes** (additions/removals with one-sentence rationale each) for Step 9 presentation.

### Step 5e: Title Revision

Assessment question: "If someone reads only this title and the Core insight sentence, do they get an accurate picture of what this idea is?"

**Revise when:** research shifted the idea's center of gravity, the router title reflects raw capture framing rather than developed understanding, or the title is too generic to distinguish from other portfolio ideas.

**Keep when:** title is still accurate and specific after research.

**Constraint:** Filename stays stable — it's the identifier across related-ideas, research folders, and jira-key. Only the `## [Heading]` in the body changes.

**Record** before/after for Step 9 presentation.

### Step 6: Critic Review

After writing the card to file, invoke the artifact critic to check structural and voice conformance. This runs in a forked, isolated context to avoid same-pass confirmation bias.

**Invoke via Skill tool:**
Use the Skill tool with skill name `artifact-critic`, passing the completed idea card file path as the argument (e.g., `Ideas/foraging-intelligence.md`).

The artifact-critic skill runs in the artifact-critic agent's isolated context — separate from this session — using only Read, Glob, and Grep. It returns a deviation report.

**Triage the findings:**
For each finding the critic returns, either:
- **Fix it** in the idea file, or
- **Override it** with a stated reason (the deviation is intentional and improves the artifact)

If any findings are overridden, note them in the Step 9 presentation under the confidence assessment so the human has visibility.

### Step 7: Self-Critique

After addressing critic findings, check the completed TL;DR against these criteria that require the full research context. Fix issues directly in the file:

1. **Multiplicative framing:** Does the Thought Outline show compounding value across dimensions? One move unlocking value in multiple directions simultaneously.
2. **Specificity:** Is the language precise? Names and mechanisms over abstractions. Specificity in the card means *precise language*, not *inline data* — N-values, survey sizes, and market figures belong in the research artifact.
3. **Strategic realism:** Are connections honest? Use "supports" not "advances" for indirect connections. Do not overstate alignment.
4. **Business language:** Would a VP understand without translation? No design methodology language.
5. **Completeness:** Every section has real content. No placeholders except Open Questions (which should have genuine unknowns).

Fix all issues directly in the file before proceeding.

**Human review awareness:** After presentation, the human evaluates using the Stage 2→3 review template (`Templates/review-templates.md`). That template focuses on: core framing accuracy, impact dimension credibility, strategic connection reality, output format readiness, and blocking unknowns. Anticipate these checks — if you know a dimension is shaky, say so in your confidence assessment rather than letting the human discover it.

### Step 8: Create Research Artifact

The synthesis handoff was created in Step 4.5. This step creates the full persistent research artifact that includes search queries and raw findings too detailed for the handoff.

1. Create directory `Research/{idea-name}/` if it does not exist
2. Write `Research/{idea-name}/development-research.md` containing:
   - Search queries executed (both Grep patterns and WebSearch queries)
   - Raw findings with sources (URLs, file paths)
   - Synthesis notes connecting findings to the idea
   - Date of research
   Both files persist — `synthesis-handoff.md` is the curated input to the synthesis agent, `development-research.md` is the full research trail for downstream stages.
3. Update the idea file frontmatter `research:` array with paths to both:
   - `Research/{idea-name}/synthesis-handoff.md`
   - `Research/{idea-name}/development-research.md`

### Step 9: Present for Review

Present the completed development to the user with:

```
Development complete: {idea-name}

**Research summary:**
- Internal: {N} strategic connections found ({direct/adjacent/indirect breakdown})
- Market: {N} findings across {N} searches
- Atlassian: {skipped | manual lookup recommended for {reference}}

**Related seeds:** {list or "none found"}

**Classification updates:**
- Title: {unchanged | "Old Title" → "New Title"}
- Themes: {unchanged | added: [x, y], removed: [z] — rationale per change}
- AI Feature (JPD): {Yes — AI is load-bearing | No — core value stands without AI}

**Confidence level:** {High/Medium/Low}
- High: Strong strategic connection + market validation + clear impact path
- Medium: Decent strategic connection but gaps in market data or impact clarity
- Low: Weak connections, thin research, or significant open questions

**Completed TL;DR:**
{Show the full updated file content}

**Recommended next steps:**
- {Contextual recommendations based on confidence level and findings}
- {e.g., "Share TL;DR with leadership for strategic alignment feedback" or "Research gap: need customer data before impact dimensions are credible"}

**Output format recommendation:**
Based on the idea's nature, recommend one of:
- **strategy-doc** — if the idea is a positioning play, narrative framing, multi-product strategic direction, or capability that shapes how multiple products evolve
- **product-brief** — if the idea is a scoped product initiative with specific features, JTBD, timeline dependencies, and a defined deliverable

Present the recommendation with rationale: which signals does this idea exhibit? This is a recommendation — the human decides. The skill does NOT set `output-file` in frontmatter.
```

**Shared research writes:**

After presenting the TL;DR, review all findings from this development session against the shared research capture heuristic (Sourced + Durable + Decision-relevant + Shared). Write qualifying findings directly to the appropriate shared research files using the entry schema defined in the file headers (finding, source, date-discovered, category, ttl, relevant-ideas, origin-idea, origin-context, confidence). If no findings qualify, skip this step.

Note in the presentation which entries were added:
> **Shared research updated:**
> - `competitive-landscape.md`: +{N} entries ({brief descriptions})
> - `market-sizing.md`: +{N} entries ({brief descriptions})

## Stop Rules

At any point during execution, stop and report when:

| Condition | Action |
|-----------|--------|
| Core insight already addressed by existing initiatives | Stop. Report what you found. Classify as "redirect" if initiative is in a different domain, "duplicate" if same domain. |
| No strategic connection can be established honestly | Stop. Report: no connection found after searching strategy docs and OKRs. Classify as "pause" (no foundation). |
| Critical context can only come from human | Stop. Report what's missing and why you cannot research it. Ask the human to provide. |
| Idea too vague to research meaningfully | Stop. Report: core insight too abstract for targeted research. Ask human to sharpen it. |
| Idea serves domain outside Assessments | Stop. Flag for rerouting to appropriate domain leader. Classify as "redirect". |
| Self-declared weakness in strategic connection | Treat as pre-filter signal. Validate quickly (one targeted Grep + one OKR check) before investing in full research. If validation fails, fire stop rule. |

**Minimum strategic connection threshold:** A viable connection requires at least one of:
- (a) Direct reference in product or design strategy docs
- (b) Direct advancement of a named 2026 OKR
- (c) Two or more adjacent connections to named priorities with a plausible mechanism

If none exist, the stop rule fires. When stopping, distinguish between:
- **Redirect:** Idea has merit but belongs in a different domain
- **Pause:** Idea lacks strategic foundation entirely

When stopping, state explicitly: what was found, what is missing, and what would unblock further development.

## Error Handling Summary

| Condition | Behavior |
|-----------|----------|
| No argument and no seed-stage ideas exist | Report "No seed-stage ideas found in Ideas/" and exit |
| Idea file not found | Report with available filenames from Ideas/ listing, exit |
| Idea not at seed stage | Report current stage, exit |
| Missing required frontmatter fields | Report specific missing fields, exit |
| Missing required body sections (core insight, source, strategic connection) | Report specific missing sections, exit |
| Strategy doc Grep returns no results | Note "No matches found in {doc}" as a finding, continue to next stream |
| Web search returns no relevant results | Note "No relevant market intelligence found for {query}" as a finding, continue |
| All research streams empty (zero findings across all three) | Fire stop rule — no strategic foundation. Report and exit. |
| Seed file has malformed frontmatter | Report parsing issue with specifics, exit |
| Related seed has malformed frontmatter | Log under "Index Issues", continue matching other seeds |
| Synthesis agent reports insufficient research | Surface the agent's assessment to the user, halt |
| Synthesis handoff creation fails | Report the error and halt |

## Scope Boundaries

This skill does NOT:
- Perform strategic synthesis — that is the develop-synthesis agent's job
- Refine seeds, clarify intent, or resolve related ideas — that is `/refine-seed`'s job (run it first)
- Create seed files (that is the router's job via `/process-inbox`)
- Decide output format — strategy doc vs. product brief (that is a human decision at Stage 2→3)
- Draft the full document (that is the `/draft` skill, Stage 2→3)
- Run the Sufficiency Evaluator (that is an MLP-phase agent)
- Process inbox items (that is `/process-inbox`)
- Merge or consolidate ideas (that is `/refine-seed`'s job)
- Load full strategy docs into context (Grep only for `product_strategy_assessments.md` and `design_strategy_assessments.md`)
- Invoke Gemini CLI (notes Atlassian references for manual lookup instead)
- Modify the idea file body after Stage 2 — the idea card is the permanent scannable artifact. /develop enriches it (Stage 1→2); subsequent stages create linked output documents.
