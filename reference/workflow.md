> One section of the `incubator-reference.md` reference index — see it for the full section map.

## Workflow

### Intake

Seeds arrive from `Projects/Router/` with frontmatter and Original Capture. The router does not interpret the capture — /refine-seed handles that before /develop. See `Projects/Router/router-spec.md` for classification and routing behavior.

### Refining a Seed (Stage 1 prep)

**Trigger:** Human says "refine-seed [idea name]" or equivalent. Run before /develop.

**What it does:** Interprets the raw seed's intent — determines whether the idea is a capability gap or an experience improvement, drafts header fields (core insight, problem, who cares, strategic connection), surfaces related ideas for potential consolidation, and aligns with the human before /develop runs. This is where ambiguous seeds get clarified so the synthesis agent has clean inputs.

### Developing an Idea (Stage 1→2)

**Trigger:** Human says "develop [idea name]" or equivalent. Seed should be refined first via /refine-seed.

**Architecture:** Orchestrator + synthesis agent. The /develop skill is an orchestrator that handles research and procedure. The develop-synthesis agent (`.claude/agents/develop-synthesis.md`) handles strategic judgment in an isolated context.

**Orchestrator flow:**
1. Read the seed file and verify refinement (structured fields present)
2. Research autonomously across three streams:
   - **Stream A:** Strategy docs, NPS data, customer evidence
   - **Stream B:** Market intelligence, competitive landscape, web research
   - **Stream C:** Cross-domain discovery via /cross-domain (JPD query)
3. Build a synthesis handoff document consolidating all research
4. Dispatch to the develop-synthesis agent (Opus, isolated context) to produce the TL;DR card
5. Post-synthesis: buildable surface check, theme governance, title revision, artifact critic, self-critique
6. Present completed TL;DR for human review

### Drafting (Stage 2→3)

**Trigger:** Human says "draft [idea name]" and specifies output format (strategy doc or brief).

**Agent behavior:**
1. Read idea card (TL;DR) and all attached research
2. Evaluate sufficiency: enough context to draft every template section?
3. If gaps exist: identify what's missing, propose how to fill (research, human input, internal docs)
4. If sufficient: create output document at `Output/{idea-name}-{format}.md` using the appropriate template
5. Self-critique against validation checklist before presenting
6. Update idea card frontmatter: `stage: drafting`, `output-file:` path — do NOT modify idea card body

### Refining (Stage 3→4)

**Trigger:** Automatic after Stage 3 draft is presented.

**Behavior:** Works on the output document (not the idea card). Follows the collaboration protocol from incubator-approach.md:
1. Establish north star alignment on the draft
2. Iterate section-by-section based on human feedback
3. Self-critique between iterations
4. Validate voice against persona guide
5. Check strategic connections for realism (not overstated)
6. As many feedback loops as needed — quality over speed
7. If direction shifts significantly, update the idea card to reflect new framing
