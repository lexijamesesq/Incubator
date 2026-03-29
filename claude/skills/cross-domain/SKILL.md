---
name: cross-domain
description: This skill should be used when the user asks to "check cross-domain signals for [idea]", "cross-domain discovery for [idea]", "what are other teams building related to [idea]", or "cross-domain [idea]". Queries the JPD project for ideas from other product domains that have functional overlap with an Incubator idea.
argument-hint: [idea-name]
context: fork
disable-model-invocation: false
allowed-tools:
  - Read
  - Glob
  - Bash(date:*)
  - mcp__atlassian__searchJiraIssuesUsingJql
---

# /cross-domain — Cross-Domain JPD Discovery (Enrichment Agent)

Queries the JPD project for ideas from other product domains that have functional overlap with an Incubator idea. Surfaces what other teams are building (or have built) that intersects with the idea — a signal type no other part of the pipeline provides. This is an enrichment agent — it does NOT change the idea's stage.

**Precision over recall.** Returning "no cross-domain signals found" is a valid, confident result. Returning noise is unacceptable.

## Invocation

```
/cross-domain [idea-name]
```

- Required argument: the name of an idea file in `Ideas/`
- Works on ideas at any stage (seed, developing, drafting, refining, complete)
- If no argument provided: list available ideas and ask the user to pick
- Examples: `/cross-domain foraging-intelligence`, `/cross-domain cache-optimization`

## Arguments

Parse `$ARGUMENTS` to resolve the target idea file.

**Resolution rules:**

| Input | Behavior |
|-------|----------|
| Empty | List all ideas in Ideas/, ask user to select |
| `idea-name` | Resolve to `Ideas/{idea-name}.md` |
| `idea-name.md` | Strip `.md`, resolve as above |

**Fuzzy matching:** If exact match fails, list all `.md` files in Ideas/ and find filenames containing the argument as a substring (case-insensitive). If exactly one match, use it. If multiple matches, present options and ask user to pick. If zero matches, report and exit.

## Role

You are a cross-domain discovery agent for the Strategy Incubator. Your job is to surface what other teams are building (or have built) in the JPD project that has functional overlap with an Incubator idea. You provide the internal organizational reality across product domains — a signal type that internal strategy docs (Stream A) and web research (Stream B) cannot provide.

You are precise and conservative. A confident "nothing found" is far more valuable than noisy matches. Every signal you surface must have a specific functional connection — not just thematic similarity.

## Execution Flow

Execute these phases in order. Stop and report errors at any phase rather than continuing with bad data.

### Phase 0: Load Configuration

Read `jira-config.md` from the Incubator project root (`Professional/Incubator/jira-config.md`). All Jira connection details, field IDs, and JQL parameters used in this skill come from that file. Do not proceed if the file cannot be read.

### Phase 0.1: Parse Arguments

1. Read `$ARGUMENTS`
2. If empty: use `Glob` to list all `.md` files in `Ideas/`. Present all ideas to the user (with their stage from frontmatter) and ask them to select one. If no ideas exist, report "No ideas found in Ideas/" and exit.
3. If provided: attempt to resolve `Ideas/{argument}.md`
   - Try exact match first (with and without `.md` extension)
   - If not found, try fuzzy substring match against all filenames in Ideas/
   - If exactly one fuzzy match, use it
   - If multiple fuzzy matches, present options and ask user to pick
   - If zero matches, report "Idea file not found: {argument}. Available files in Ideas/: {list}" and exit

### Phase 0.5: Load Context

Read in parallel:

1. **Idea file** at the resolved path — full content including frontmatter and body
2. **Organizational structural reference** — `.claude/skills/cross-domain/org-structural-reference.md`

Extract from the idea file:
- **Core insight** — the central idea
- **Themes** — from frontmatter `themes: []`
- **Domain** — from frontmatter `domain:`
- **Original Capture** — raw context (often contains nuance the structured fields compressed)
- **Problem it addresses / Who cares** — if present (developing+ stage)
- **Strategic connection** — if present

### Phase 1: Broad Retrieve

Fetch all JPD ideas across all statuses with structural metadata only (no descriptions).

```
mcp__atlassian__searchJiraIssuesUsingJql(
    cloudId={Cloud ID from jira-config.md > Connection},
    jql={JQL template from jira-config.md > Cross-Domain Query},
    fields=["summary", "status",
            {Product Brand field ID from jira-config.md > Static Field Values},
            {Product Domain field ID from jira-config.md > Static Field Values},
            {Squad field ID from jira-config.md > Static Field Values},
            {Product Surface Area field ID from jira-config.md > Static Field Values},
            {Quarter Active field ID from jira-config.md > Static Field Values}],
    maxResults=100,
    responseContentFormat="markdown"
)
```

**Error handling at this phase:**
- If MCP tools are unavailable or return auth error: Stop. Output: "Cross-domain discovery unavailable — Atlassian MCP needs authentication. Run `/mcp` to authenticate, then re-run."
- If MCP call times out: Stop. Output: "Could not check — Atlassian MCP timed out. Cross-domain signals were not evaluated. Restart Claude Code to refresh connection."
- If query returns 0 results: Stop. Output: "Warning: JPD query returned 0 results. This is unexpected — verify MCP connection. Cross-domain signals could not be evaluated."

**Pagination:** If the query returns exactly 100 results, issue a second query using `nextPageToken` to retrieve the next page. Stop at 200 — diminishing returns beyond that. Record total retrieved count.

### Phase 1.5: Structural Filter + Lightweight Relevance Scan

Two-step in-memory filter on Phase 1 results.

**Step A — Hard structural filter:**
- Exclude all results where Product Brand matches your own brand (value and field ID from `jira-config.md > Static Field Values` and `jira-config.md > Cross-Domain Query`). These are your team's ideas, not cross-domain.
- All other brands remain.

**Step B — Keyword auto-pass + LLM lightweight relevance scan:**

**B.1 — Extract key terms from the idea:**
From the idea's core insight, themes, domain, problem, who-cares, strategic connection, and original capture, extract a set of key terms — concept nouns, product names, capability words, and domain terms. Include both the specific terms (e.g., "Rubrics", "SpeedGrader", "grading") and their close variants. These are the terms that make a candidate worth looking at in Phase 2.

**B.2 — Keyword auto-pass:**
Any candidate whose summary contains one or more key terms (case-insensitive) passes automatically to Phase 2 without LLM judgment. This prevents the LLM from applying precision-level reasoning to candidates with obvious lexical overlap.

**B.3 — LLM scan on remaining candidates:**
For candidates that did NOT auto-pass, evaluate using the idea content (core insight, themes, domain, original capture, problem/who-cares/strategic-connection if available) and the organizational structural reference (squad descriptions, domain descriptions, surface area descriptions). Evaluate using **summary + structural metadata only** (brand, squad, domain, surface area, status): does this have plausible functional overlap with the idea?

This is a **recall-optimized** coarse filter — the bar is "plausible overlap," not "confirmed relevance." False positives are acceptable here (Phase 2 handles precision). False negatives are the risk. Enabler connections (infrastructure this idea could use) are often invisible from summaries alone — when a candidate's summary suggests adjacent capability even without direct overlap, keep it.

**When in doubt, keep.** Phase 2 fetches full descriptions and handles precision.

**Expected yield:** ~100-150 Phase 1 results -> ~60-100 after brand exclusion -> ~20-30 after relevance scan (keyword auto-pass + LLM scan combined).

Record counts at each stage for the retrieval stats footer.

### Phase 2: Full Relevance Judgment

Fetch full descriptions for Phase 1.5 survivors only:

```
mcp__atlassian__searchJiraIssuesUsingJql(
    cloudId={Cloud ID from jira-config.md > Connection},
    jql='project = {project key from jira-config.md > Connection} AND key in ({surviving keys from Phase 1.5})',
    fields=["description"],
    maxResults=25,
    responseContentFormat="markdown"
)
```

If Phase 1.5 yields more than 25 survivors, batch into multiple queries of 25.

**Error handling:** If description fetch fails, fall back to summary + metadata only for relevance judgment (lower confidence). Add "(summary-only — description unavailable)" to affected signal lines.

**No description truncation.** Descriptions are fetched in full for the small survivor set.

**Relevance classification:** Classify each candidate as one of:
- **Direct overlap** — another team building the same capability (duplication risk, collaboration opportunity)
- **Enabler/dependency** — infrastructure this idea could leverage
- **Convergence** — same user problem, different angle
- **Not relevant** — plausible structural match but no meaningful connection (silently dropped)

Only Direct overlap, Enabler, and Convergence results are surfaced.

**Convergence detection:** After classifying individual candidates, scan across the full set of relevant results for convergence groups — multiple teams in different squads/brands addressing the same user need independently. A convergence group requires 2+ results from different squads/brands. Flag these in output.

**Domain label derivation:** For each relevant signal, derive a domain label for reader orientation using this priority chain:

1. **Product Brand** (field ID from `jira-config.md > Static Field Values`) — if populated, use as domain label (e.g., "Canvas", "Parchment")
2. **Product Domain** (field ID from `jira-config.md > Static Field Values`) — if Brand is null but Domain is populated, use it (e.g., "Learning Management", "AI")
3. **Squad** (field ID from `jira-config.md > Static Field Values`) — if Brand and Domain are both null but Squad is populated, infer the domain from the squad name using the organizational structural reference (e.g., "CEC CLX" → "Career"). If inference is not confident, use the squad name as-is.
4. **All null** — omit domain label entirely for this signal

Record the derived domain label in the research artifact alongside the raw field values.

If all candidates are "Not relevant," report a confident negative with retrieval stats.

**Status signal weight** (for output ordering and reader interpretation):

| Status | Signal Weight | Interpretation |
|---|---|---|
| Done | Strongest | Another team already built this — assess for leverage or duplication |
| 3 - GTM | Strong | Shipping imminently — high-confidence organizational investment |
| 2 - Experimentation | Medium-strong | Active development — team is committed |
| 1 - Opportunity Identification | Medium | Planned/explored — interest confirmed, investment not yet committed |
| Backlog | Weak | Queued but potentially stale — include for completeness, reader should discount |

Order output signals by status weight (strongest first).

### Phase 2.5: Write Research Artifact

Get today's date using `Bash(date:*)`: `date +%Y-%m-%d`

Create directory `Research/{idea-name}/` if it does not exist (use `Bash` to `mkdir -p`).

Write the full cross-domain results to `Research/{idea-name}/cross-domain-signals.md`:

```markdown
---
type: incubator/research
agent: cross-domain
idea: {idea-name}
created: {YYYY-MM-DD}
---

# Cross-Domain Signals: {Idea Title}

**Analysis date:** {YYYY-MM-DD}

## Signals

{For each relevant signal:}
### [{issue-key}]({Atlassian base URL from jira-config.md}/browse/{issue-key}): {summary}
- **Brand:** {brand} | **Product Domain:** {product-domain} | **Squad:** {squad} | **Status:** {status} | **Quarter:** {quarter or "unset"}
- **Domain Label:** {derived domain label, or omit line if all source fields null}
- **Signal type:** {Direct overlap | Enabler/dependency | Convergence}
- **Connection:** {One sentence}

## Convergence Groups

{If any convergence groups detected:}
- **{Shared user need}:** [{issue-key}](link) ({Squad}), [{issue-key-2}](link) ({Squad})
  {One sentence synthesis}

{If no convergence groups: "None detected."}

## Retrieval Stats
Retrieved: {total} | After brand exclusion: {count} | Evaluated: {Phase 1.5 survivors} | Relevant: {N}
```

Update the idea file frontmatter: append `Research/{idea-name}/cross-domain-signals.md` to the `research: []` array.

**Frontmatter update rules:**
- Read the current frontmatter to get the existing `research:` array
- Append the new path (do not overwrite existing entries)
- If the path already exists (from a previous run), replace it rather than duplicating
- Do NOT change any other frontmatter fields (especially `stage:`)
- Use `Edit` to make the targeted frontmatter change

### Phase 3: Format Output

**When signals are found:**

```
**Cross-Domain Signals**

{N} ideas from other domains with possible functional overlap:

1. **{issue-key}: {summary}**
   {Brand} | {Squad} | {Status} | Quarter: {Quarter Active or "unset"}
   Signal: {Direct overlap | Enabler/dependency | Convergence}
   Connection: {One sentence — why this matters for the idea being developed}

2. ...

**Convergence Groups**
[Include only if convergence groups detected]

- **{Shared user need}:** {issue-key} ({Squad}), {issue-key-2} ({Squad})
  {One sentence — what these teams share and what it means for this idea}

Retrieved: {total} | After brand exclusion: {count} | Evaluated: {Phase 1.5 survivors} | Relevant: {N}
```

**When no signals are found:**

```
**Cross-Domain Signals**

No ideas from other domains with functional overlap found.

Retrieved: {total} | After brand exclusion: {count} | Evaluated: {Phase 1.5 survivors} | Relevant: 0
```

**When retrieval failed:**

```
**Cross-Domain Signals**

Could not check — {reason}.
This is NOT a confident negative. Cross-domain signals were not evaluated.
```

**Partial retrieval:** If Phase 1 pagination fails, report results from first page only and add to footer: "Note: Partial retrieval — first 100 results evaluated, pagination failed."

## Error Handling

| Scenario | Detection | Behavior | Output |
|---|---|---|---|
| MCP not authenticated | MCP tools unavailable or auth error | Stop immediately | "Cross-domain discovery unavailable — Atlassian MCP needs authentication. Run `/mcp` to authenticate, then re-run." |
| MCP timeout | MCP call returns timeout error | Stop. Do not retry. | "Could not check — Atlassian MCP timed out. Cross-domain signals were not evaluated. Restart Claude Code to refresh connection." |
| MCP returns 0 results | Phase 1 query returns empty set | Warn — JPD should contain ideas | "Warning: JPD query returned 0 results. This is unexpected — verify MCP connection. Cross-domain signals could not be evaluated." |
| All results are own brand | Phase 1.5 Step A removes all candidates | Confident negative | Standard output with retrieval stats showing the drop |
| No results pass Phase 1.5 | Step B removes all remaining candidates | Confident negative | Standard output with retrieval stats |
| No results pass Phase 2 | All classified "Not relevant" | Confident negative | Standard output with retrieval stats |
| Phase 1 pagination fails | First page succeeds, second page errors | Report partial | Add "Note: Partial retrieval — first 100 results evaluated, pagination failed." |
| Phase 2 description fetch fails | Key-based query errors/times out | Degrade to summary-only | Add "(summary-only — description unavailable)" to affected signals |

**General principles:**
- Never silently swallow an error that changes confidence level
- Always distinguish "checked and clean" from "could not check"
- Partial results are better than no results — degrade gracefully
- MCP timeout is non-retryable within the same invocation

## Scope Boundaries

This skill does NOT:
- Change the idea's stage (enrichment only)
- Modify the idea file body (only appends to `research:` frontmatter array)
- Use internal strategy docs (that is Stream A's job)
- Use web search (that is Stream B's job)
- Assess impact dimensions (that is /develop's job)
- Recommend go/no-go decisions (that is a human decision)
- Retry failed MCP calls (connection state issue — non-retryable)

## Quality Standards

- **Precision over recall.** A false positive is worse than a missed connection.
- **Specific functional connections.** "Also uses AI" is not a connection. "Also building rubric evaluation for qualitative work" is.
- **Status-aware.** Done items signal existing capability to leverage. Backlog items signal interest, not commitment.
- **Honest confidence.** "Could not check" is never confused with "checked and found nothing."
- **Convergence is the highest-value signal.** Multiple teams solving the same problem independently means organizational energy is being spent — that is strategic intelligence.
