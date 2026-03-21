# Jira / JPD Configuration

Configuration for /jpd-push and /cross-domain skills. Copy this file to `jira-config.md` and fill in your organization's values.

## Connection

- **Cloud ID:** `YOUR_ATLASSIAN_CLOUD_ID`
- **Project key:** `YOUR_PROJECT_KEY`
- **Issue type ID:** `YOUR_ISSUE_TYPE_ID`
- **Atlassian base URL:** `https://YOUR_INSTANCE.atlassian.net`

## Static Field Values

These are set the same for every idea pushed to JPD. Update field IDs and option IDs to match your Jira configuration.

| JPD Field | Field ID | Value | Format |
|---|---|---|---|
| Product Brand | customfield_XXXXX | Your Brand (OPTION_ID) | Array: `[{"id": "OPTION_ID"}]` |
| Product Domain | customfield_XXXXX | Your Domain (OPTION_ID) | Array: `[{"id": "OPTION_ID"}]` |
| Squad | customfield_XXXXX | Your Squad (OPTION_ID) | Array: `[{"id": "OPTION_ID"}]` |
| Product Surface Area | customfield_XXXXX | Your Surface Area (OPTION_ID) | Array: `[{"id": "OPTION_ID"}]` |
| Roadmap Priority | customfield_XXXXX | Your Priority (OPTION_ID) | Array: `[{"id": "OPTION_ID"}]` |
| Quarter Active | customfield_XXXXX | Your Default (OPTION_ID) | Single: `{"id": "OPTION_ID"}` |

## Dynamic Field Mappings

These are derived from the idea card content. Update field IDs to match your Jira configuration.

| JPD Field | Field ID | Source |
|---|---|---|
| Summary | summary | Idea title (from H2 heading) |
| Description | description | TL;DR body restructured into JPD headings |
| Executive Summary | customfield_XXXXX | Core insight sentence (plain text) |
| AI Feature | customfield_XXXXX | Set to `1` if applicable, omit otherwise |
| Domain Objective | customfield_XXXXX | Multi-checkbox, mapped from impact dimensions |
| Labels | labels | Array of theme values from frontmatter `themes[]` |

## Domain Objective Mapping

| Objective | Option ID | When to select |
|---|---|---|
| Objective 1 | OPTION_ID | Description of when to select |
| Objective 2 | OPTION_ID | Description of when to select |
| Objective 3 | OPTION_ID | Description of when to select |

## Transition

- **Transition ID:** `YOUR_TRANSITION_ID` (e.g., Backlog → Active)

## Cross-Domain Query

Brand exclusion filter for /cross-domain: exclude results where Product Brand matches your brand.

JQL template:
```
project = YOUR_PROJECT_KEY AND status in ("Done", "Active", "Backlog") ORDER BY updated DESC
```

## Organizational Taxonomy

See `claude/skills/cross-domain/org-taxonomy.sample.md` for the expected format of the organizational taxonomy used by /cross-domain.
