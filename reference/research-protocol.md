> One section of the `incubator-reference.md` reference index — see it for the full section map.

## Research Protocol

When an idea needs more context than what's available:

**Strategy doc queries:** Targeted Grep on the product strategy and design strategy documents (paths configured in .claude/instance.md under Configuration > External References). Never load full files into context. When citing strategy docs in Research Summary bullets, link to the external URL (also in .claude/instance.md Configuration) so references are navigable outside the Incubator.

**Market intelligence:** Web search for competitors, TAM, technology trends. Synthesize with sources.

**Cross-domain discovery:** /develop Stream C invokes `/cross-domain` to query the JPD project for ideas from other product domains with functional overlap. Signals are classified as Direct overlap, Enabler/dependency, or Convergence. Results persist as `Research/{idea-name}/cross-domain-signals.md`. The curated output (maximum 5 signals) is written to a dedicated `### Cross-Domain Signals` section on the TL;DR card by the /develop orchestrator (Step 5b) — it does not flow through the synthesis agent. The full artifact is read by /jpd-push for the JPD Cross-Domain Signals section.

**When to pause and ask:** If research reveals the idea lacks strategic foundation, or if critical context can only come from the human (stakeholder conversations, internal politics, undocumented priorities), stop and surface the gap explicitly.

### Foundation Assessment

An optional research verdict recording whether development research established a strategic foundation for the idea. When present, it appears in the development research trail (`Research/{idea-name}/development-research.md`) as a summary line. Valid values:

- **Strong** — research established a solid strategic foundation; the idea is well-grounded.
- **Moderate** — foundation is present but partial; proceed with noted gaps.
- **Weak** — research concluded the idea lacks a strategic foundation.

A **Weak** verdict is a hard stop-gate for `/draft` (Step 2 and Stop Rules): drafting halts and reports what the research found. When no Foundation Assessment is present in the research, `/draft` treats the gate as not fired and proceeds.
