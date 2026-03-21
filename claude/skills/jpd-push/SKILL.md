---
name: jpd-push
description: This skill should be used when the user asks to "push [idea] to JPD", "push [idea name]", "jpd push [idea]", or "push [idea] to JPD". Pushes a developed idea to JPD for stakeholder visibility. One-directional push with human review gate.
argument-hint: [idea-name]
context: conversation
disable-model-invocation: false
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash(date:*)
  - mcp__atlassian__createJiraIssue
  - mcp__atlassian__editJiraIssue
  - mcp__atlassian__transitionJiraIssue
---

# /jpd-push — Push Idea to JPD

Pushes a developed idea to JPD for stakeholder visibility. One-directional — no automated sync-back. Supports first push (create) and re-push (update).

## Invocation

```
/jpd-push [idea-name]
```

- Required argument: the name of a developing-or-later idea file in `Ideas/`
- If no argument provided: list eligible ideas and ask user to pick
- Examples: `/jpd-push ai-cohort-peer-intelligence`, `/jpd-push assessment-marketplace`

## Arguments

Parse `$ARGUMENTS` to resolve the target idea file.

**Resolution rules:**

| Input | Behavior |
|-------|----------|
| Empty | List all developing-or-later ideas in Ideas/, ask user to select |
| `idea-name` | Resolve to `Ideas/{idea-name}.md` |
| `idea-name.md` | Strip `.md`, resolve as above |

**Fuzzy matching:** If exact match fails, list all `.md` files in Ideas/ and find filenames containing the argument as a substring (case-insensitive). If exactly one match, use it. If multiple matches, present options. If zero matches, report and exit.

## Execution Flow

### Step 0: Load Configuration

Read `jira-config.md` from the Incubator project root (`Professional/Incubator/jira-config.md`). All Jira connection details, field IDs, and option IDs used in this skill come from that file. Do not proceed if the file cannot be read.

### Step 1: Load and Validate

Read the idea file. Verify all push prerequisites:

**Required for push:**
- `stage` is `developing`, `drafting`, `refining`, or `complete`
- All five impact dimensions are non-null (`customer-sentiment`, `user-experience`, `revenue-potential`, `industry-disruption`, `strategic-alignment`)
- Body contains populated sections: Core insight, Problem it addresses, Who cares, Strategic connection, Opportunity Assessment table, Research Summary

**If any prerequisite fails:** Report exactly what's missing and exit. Do not proceed with incomplete ideas.

### Step 2: Detect Push Type

Check the idea's frontmatter for `jira-key`:

- **`jira-key` is null or absent:** This is a **first push** — will create a new issue.
- **`jira-key` has a value (e.g., {issue-key}):** This is a **re-push** — will update the existing issue.

Report which type this is before proceeding.

### Step 3: Prepare Payload

Extract and transform the idea content into JPD fields:

**Summary:** The idea title from the H2 heading (e.g., `## Cohort and Peer Intelligence` becomes `Cohort and Peer Intelligence`).

**Description:** Restructure the TL;DR body into JPD-compatible headings. Content is transferred verbatim — no generative rewriting. Only the heading structure changes. Exclude `### Original Capture` (internal provenance only). If a Cross-Domain Signals section will be included (see Step 3a), strip any cross-domain bullets from the Research Summary to avoid redundancy — the dedicated section is the single place for that data in JPD.

Map the TL;DR sections into this structure:

```markdown
## What
{Core insight text — verbatim, strip bold label prefix}
{Problem it addresses text — verbatim, strip bold label prefix}

## Who
{Who cares text — verbatim, strip bold label prefix}

## Why
{Strategic connection text — verbatim, strip bold label prefix}

## Opportunity Assessment
{Table — verbatim from card}

## Research Summary
{Findings — verbatim from card}

## Cross-Domain Signals
{Include ONLY if cross-domain research exists — see Step 3a below. Omit section entirely if no research artifact found.}

## Thought Outline
{Content — verbatim from card}

## Buildable Surface
{Include ONLY if Buildable Surface section exists on the card. Transfer verbatim. Omit section entirely if not present on card.}

## Open Questions
{Content — verbatim from card}
```

"Strip bold label prefix" means: `**Core insight:** Assessment platforms treat...` becomes `Assessment platforms treat...` — remove the `**Label:** ` prefix since the heading now provides the context.

**Link translation:** Idea cards may use internal file paths for strategy doc references. Before building the description, replace these with external URLs so links resolve in Jira. The link translation table is configured in CLAUDE.md under Configuration > External References — each external reference entry includes both a local path and an external URL. Match on the local path substring within markdown links and replace with the corresponding external URL, preserving the link text.

Apply to the entire description body.

**Step 3a: Cross-Domain Signals section (conditional)**

Check if a cross-domain research artifact exists at `Research/{idea-name}/cross-domain-signals.md`. If it does not exist, omit the Cross-Domain Signals section entirely from the description.

If it exists, read it and extract the relevant signals (those classified as Direct overlap, Enabler/dependency, or Convergence). Build the section as:

```markdown
## Cross-Domain Signals
{N} ideas from other domains with possible functional overlap:
- [{issue-key}]({Atlassian base URL from jira-config.md}/browse/{issue-key}) {summary} ({Domain Label}) — {Signal type}: {Connection sentence}

Domain Label is a derived field from the cross-domain research artifact (Brand → Product Domain → Squad inference → Squad name). Omit the parenthetical entirely if no domain label is available for a signal.

{If convergence groups exist, add:}
Convergence: {Group description — which teams, what shared need, one sentence on what it means}
```

Each issue key is a clickable link to the JPD item within the Atlassian environment. Content is transferred from the research artifact — no generative rewriting.

**Executive Summary:** The Core insight sentence, plain text only (strip bold markers).

**AI Feature:** If `themes` array contains any value starting with `ai-`, set to `1` (numeric). Otherwise omit.

**Domain Objective:** Select the single best-fit objective based on the idea's content and impact dimensions. Objective labels and their option IDs are in `jira-config.md > Domain Objective Mapping`.

Format as: `[{"id": "{option_id}"}]`

Use the impact dimensions as signals to select the best-fit objective from the mapping table. When ambiguous, pick the strongest signal and note the reasoning.

**Labels:** The `themes` array values from frontmatter, as-is.

**Static fields:** Apply all static field values from `jira-config.md > Static Field Values`. That table defines the field ID, option ID, and format for each static field (Product Brand, Product Domain, Squad, Product Surface Area, 2026 Roadmap Priority, Quarter Active).

### Step 4: Human Review Gate

Present the complete proposed payload to the human:

```
**Push preview: {idea-name}**
Type: {First push | Re-push to {jira-key}}

**Summary:** {title}

**Executive Summary:** {core insight}

**Domain Objective:** {objective label} — {one-line rationale}

**AI Feature:** {Yes | No}

**Labels:** {comma-separated themes}

**Static fields:** {list each static field from jira-config.md with its configured value}

**Description body:**
{the extracted description, shown in full}

---
Confirm to push, or provide overrides (e.g., "change Surface Area to X", "change Roadmap Priority to Y").
```

**Wait for human confirmation.** Do not push without explicit approval.

**Overrides:** If the human provides overrides for Surface Area, Roadmap Priority, or Domain Objective, apply them. The human may also edit the description body or Executive Summary before push.

### Step 5: Push

**First push:**

Call `mcp__atlassian__createJiraIssue` with:
- `cloudId`: Cloud ID from `jira-config.md > Connection`
- `projectKey`: project key from `jira-config.md > Connection`
- `issueTypeName`: `Idea`
- `summary`: the prepared summary
- `description`: the prepared description body
- `additional_fields`: object containing all custom fields:
  - All static fields from `jira-config.md > Static Field Values` (field IDs and option IDs as specified there)
  - Executive Summary field ID and format from `jira-config.md > Dynamic Field Mappings`: string value
  - Domain Objective field ID from `jira-config.md > Dynamic Field Mappings`, option ID from `jira-config.md > Domain Objective Mapping`: multi-checkbox array
  - AI Feature field ID from `jira-config.md > Dynamic Field Mappings`: `1` (numeric, omit if not applicable)
  - `labels`: themes array (e.g., `["ai-capabilities"]`)

After successful creation, extract the issue key from the response.

Transition the issue to "1 - Opportunity Identification" using `mcp__atlassian__transitionJiraIssue` with the transition ID from `jira-config.md > Transition`. This moves the issue from the default "Backlog" status into the proper workflow state.

Update the idea file frontmatter:
- Add or update `jira-key: {issue-key}`
- Add or update `jira-pushed-at: {today's date YYYY-MM-DD}` — use `Bash(date:*)` to get today's date

**Re-push:**

Call `mcp__atlassian__editJiraIssue` with:
- `cloudId`: Cloud ID from `jira-config.md > Connection`
- `issueIdOrKey`: the existing `jira-key`
- `fields`: object containing all fields being updated (same structure as additional_fields above, plus `summary`, `description`, `labels`)

Before pushing, show a diff of what changed since the last push (compare current payload to what was previously pushed — if this is the first re-push and no prior payload is stored, note "First re-push — showing full payload").

Update `jira-pushed-at` in frontmatter.

### Step 6: Report

```
Push successful: {idea-name}

**JPD Issue:** {issue-key}
**URL:** {Atlassian base URL from jira-config.md}/browse/{issue-key}

Local frontmatter updated:
- jira-key: {issue-key}
- jira-pushed-at: {date}
```

## Re-push Guidance

**Re-push warranted when:**
- Strategic direction shifts
- Impact dimensions change significantly
- Human explicitly requests

**Re-push NOT warranted when:**
- Output doc gains detail (that's Stage 3+ work, separate from the card)
- Minor wording refinements

## Error Handling

| Condition | Behavior |
|-----------|----------|
| No argument and no eligible ideas | Report "No developing-or-later ideas found" and exit |
| Idea file not found | Report with available filenames, exit |
| Idea at seed stage | Report "Idea is at seed stage — develop it first with /develop" and exit |
| Missing impact dimensions | Report which dimensions are null, exit |
| Missing TL;DR sections | Report which sections are incomplete, exit |
| Atlassian API error on create | Report the error. Do not update frontmatter. Exit. |
| Atlassian API error on edit | Report the error. Do not update frontmatter. Exit. |
| Human declines at review gate | Exit without pushing |

## Scope Boundaries

This skill does NOT:
- Develop ideas (that's `/develop`)
- Draft output documents (that's `/draft`)
- Sync back from JPD (sync-back is conversational and ad-hoc)
- Push seeds (must be developing or later)
- Push without human review
- Modify the idea card body (only adds/updates `jira-key` and `jira-pushed-at` in frontmatter)
- Manage initiative hierarchy in JPD (initiatives are local only)
