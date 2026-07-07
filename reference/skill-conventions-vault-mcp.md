> Split verbatim from `incubator-reference.md` on 2026-07-07 — one section of the reference index. See `incubator-reference.md` for the full section map.

## Skill Conventions: Vault MCP Access

**Rule:** Any skill or agent whose execution may touch vault `.md`, `.markdown`, `.txt`, `.base`, or `.canvas` files MUST declare the relevant Obsidian MCP tools explicitly in both `allowed-tools` (skill spec) and `tools` (agent spec). Do not rely on inheritance from the parent context.

**Why:** The vault redirect hook (`~/bin/dotty/.claude/hooks/vault-mcp-redirect.sh`) is a `PreToolUse` blocker on `Read`, `Edit`, `Write`, and `Grep` for vault-parsed file extensions. It exits with code 2 and tells the caller to use Obsidian MCP equivalents. A skill or agent without explicit MCP tools will be blocked silently when the hook fires — and inheritance behavior in forked subagent contexts is undocumented and fragile. Past failure: `artifact-critic` declared only `Read, Glob, Grep` in both spec layers and could not read the vault card it was meant to critique. Develop-synthesis is the only agent that has historically declared MCP explicitly and worked reliably.

**How to apply:** When creating or updating a skill that reads, writes, or edits vault content, include the full set of Obsidian MCP tools relevant to its operations. Common combinations:

| Operation | Required Obsidian MCP tools |
|---|---|
| Read one note | `mcp__obsidian__read_note` |
| Read batch (≤10) | `mcp__obsidian__read_multiple_notes` |
| Read frontmatter only | `mcp__obsidian__get_frontmatter` |
| Search content / frontmatter | `mcp__obsidian__search_notes` |
| List directory contents | `mcp__obsidian__list_directory` |
| Targeted string replace | `mcp__obsidian__patch_note` |
| Frontmatter update | `mcp__obsidian__update_frontmatter` |
| Tag add/remove | `mcp__obsidian__manage_tags` |
| Create/overwrite/append/prepend | `mcp__obsidian__write_note` |
| Delete | `mcp__obsidian__delete_note` |

For non-vault file types within the vault tree (`.json`, images, PDFs, scripts, YAML, binaries) generic tools are fine — the hook does not parse those. For move/rename operations the Obsidian CLI via Bash is required (wikilink-safe).

**Verification:** When updating a skill's `allowed-tools`, also update the agent's `tools` field if the skill has an associated agent definition. The two should match for vault operations. The `develop-synthesis` agent definition is the canonical reference example.
