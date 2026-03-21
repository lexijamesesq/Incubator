# Incubator Approach

**Purpose:** Unified methodology for developing strategic ideas from seed through finished document. Covers both output formats (strategy documents and product briefs) with shared methodology that branches at the output format decision point.

**Based on:** Research synthesis from Rumelt (Strategy Kernel), Perri (Escaping Build Trap), Torres (Continuous Discovery), and practitioner approaches. Refined through iterative collaboration on real documents.

**Companion files:**
- `persona.md` — Voice and style (applies Stage 2 onward)
- `Templates/strategy-document-template.md` — Strategy output template
- `Templates/product-brief-template-v2.md` — Brief output template

---

## When to Use Which Output Format

**Use Strategy Document when:**
- You need to drive a specific outcome across multiple initiatives
- Defining direction for multiple initiatives over time
- Establishing principles teams apply independently
- Providing decision-making frameworks for a domain
- Setting platform-level or cross-product direction
- Time horizon: multi-quarter to multi-year

**Use Product Brief when:**
- Defining a single initiative with clear scope
- Aligning triads (Product, Design, Engineering) before work begins
- Establishing success for one feature/project
- Scoping EAP and GA milestones
- Time horizon: single initiative (weeks to months)

**Key difference:** Strategies guide many decisions across initiatives. Briefs frame one initiative for execution.

**Language difference:**
- Strategy: "When teams face X decision, apply Y principles to drive Z outcome"
- Brief: "We believe building X feature will achieve Y outcome because Z"

**If you can't articulate the specific outcome you're driving:** You probably don't need a strategy document. Write a brief instead, or just let teams execute.

### Decision Tree for Borderline Cases

When an idea doesn't cleanly fit either format:

```
Does this idea require coordinating multiple initiatives or teams?
├── YES → Does it need to set principles teams apply independently?
│   ├── YES → Strategy Document
│   └── NO → Is it one initiative with clear scope that needs multi-team alignment?
│       ├── YES → Product Brief (the coordination is execution, not strategy)
│       └── NO → Probably needs to be split into multiple documents
└── NO → Does it define a single initiative for triad execution?
    ├── YES → Product Brief
    └── NO → Is it an exploration or research question?
        ├── YES → Not ready for either format. Do more Phase 1 work first.
        └── NO → Ask: "What decision does this document enable?"
            If you can't answer, you don't need a document yet.
```

**Common borderline scenarios:**

| Scenario | Resolution |
|----------|-----------|
| Platform initiative that affects multiple products | Strategy Document — it needs principles teams apply independently |
| Single feature that requires cross-team coordination | Product Brief — the coordination is execution detail, not strategic direction |
| Idea that's "too big for a brief but too focused for a strategy" | Usually means the scope isn't clear. Sharpen scope first, then choose format. |
| Infrastructure/developer experience initiative | Strategy Document if it sets patterns for how teams build; Product Brief if it's a specific tool or capability |
| Exploration with unclear outcome | Neither — do Phase 1 context gathering first. The format becomes obvious once you understand the idea. |

---

## Core Philosophy

### 1. Strategy Is Not Goals (Rumelt)
Strategy must explain both WHERE to play and HOW to win. Bad strategy lists aspirational goals without addressing obstacles or approach.

**Good strategy:** "By establishing platform-first patterns (HOW), we enable faster development (WHERE) through reusable components (advantage)"

**Bad strategy:** "We will be the leader in dashboarding" (goal without approach)

### 2. Diagnosis Before Direction (Rumelt + Reddit)
Most strategy failures come from weak diagnosis. Must honestly assess current state, identify what's broken, understand why existing approaches aren't working. This applies to both strategy documents (Context & Opportunity) and briefs (Problem & Opportunity).

### 3. Outcomes Over Outputs (Perri + Torres)
Strategy focuses on value created (outcomes), not features shipped (outputs). Whether a strategy doc or a brief, the output should be a "deployable decision-making framework" that enables team action.

### 4. Guiding Principles, Not Prescriptive Solutions (Rumelt + Perri)
Provide direction and constraints that channel decisions, not exact features to build. Strategies enable independent team action. Briefs frame problems for triads to solve — they don't prescribe solutions.

### 5. Strategic Leverage Matters
Beyond solving problems, identify multiplicative advantages — differentiation, platform effects, compounding value that creates sustainable competitive advantage. Show how one move unlocks value across multiple dimensions simultaneously.

### 6. Continuous Validation (Torres)
Identify opportunities and assumptions to test, not prescribe specific solutions. Multiple solutions can address the same opportunity.

### 7. Template Intent Over Template Mechanics
Don't copy a template's format — embody its intent. When a template shows a narrative paragraph, it's saying "tell a story that flows naturally," not "write exactly one paragraph." Read template examples for tone, voice, flow, and emphasis.

### 8. Realistic Over Aspirational
Be honest about impact and alignment. If a strategic connection is weak, acknowledge it modestly rather than overstating.

- **Overstated**: "This initiative advances our design goals around Assessment as Platform Signal and proves Intent Recognition & Assessment Creation..."
- **Realistic**: "For design goals, this supports contextual workflow integration—making third-party content feel native rather than bolted on. The impact is modest but real: one less fragmented experience."

If you can't genuinely connect an initiative to a strategic anchor, say so plainly or acknowledge the connection is indirect. Fabricating alignment undermines credibility.

### 9. AI Limitations: Acknowledge, Don't Fake
When AI genuinely can't validate something (platform adoption patterns, cross-team coordination dynamics, long-term business impact, technical feasibility at scale), acknowledge it explicitly rather than faking it. Strategy documents have MORE unknowns than briefs — they guide long-term decisions across teams with emergent outcomes. Honesty about uncertainty builds trust.

**Template for acknowledgment:**
> **Note:** This [strategy/brief] was drafted with AI assistance using available documents and conversations. [Specific limitation] should be validated by [human role] before proceeding.

### 10. Connect to Business Outcomes
Every strategic output should connect to MAU × ARPU = ARR (usage, retention, revenue). Show how design and platform decisions drive business value. This applies to both format types — speak in terms that resonate with Product, Engineering, and executive leadership.

### Applying Core Philosophy: Self-Critique Patterns

These principles are only useful if you can catch violations while writing. For each principle, here's the concrete self-critique pattern:

| Principle | While Writing, Ask | If the Answer Is No |
|-----------|-------------------|---------------------|
| 1. Strategy ≠ Goals | "Does this explain HOW, not just WHERE?" | Add the mechanism. "We will lead in X" → "We will lead in X by doing Y, which works because Z." |
| 2. Diagnosis Before Direction | "Have I explained what's broken and why?" | Stop drafting solutions. Write the diagnosis first. If you can't diagnose, you need more context (return to Phase 1). |
| 3. Outcomes Over Outputs | "Am I describing value created or features shipped?" | Reframe. "Build modular widgets" → "Enable teams to compose custom views without engineering support." |
| 4. Principles Not Solutions | "Am I directing or prescribing?" | Remove implementation details. Keep the strategic direction, let teams decide how. |
| 5. Strategic Leverage | "Does this show one move creating multiple outcomes?" | Look for the multiplicative angle. If it's genuinely linear (do X → get Y), that's fine — don't force it. But most strategic moves have compound effects worth surfacing. |
| 6. Continuous Validation | "Am I stating assumptions as facts?" | Add "[assumption — needs validation]" markers. List in Open Questions. |
| 7. Template Intent | "Am I filling a template or embodying its purpose?" | Re-read a completed example section. Match the tone and flow, not the structure. |
| 8. Realistic Over Aspirational | "Would a skeptical VP challenge this claim?" | Downgrade: "advances" → "supports." "Proves" → "contributes to." If the connection is weak, say "modest but real." |
| 9. AI Limitations | "Am I faking knowledge I don't have?" | Add the disclaimer template. Flag for human validation. Better to say "I don't know" than to fabricate. |
| 10. Business Outcomes | "Can I trace this to MAU, ARPU, or ARR?" | Find the connection or acknowledge it's indirect. "This improves teacher workflow" → "This improves teacher workflow, which drives daily active usage (MAU) through reduced friction." |

**Usage:** Run this table as a checklist during Phase 3 self-critique, before presenting any section. It takes 2 minutes and catches the most common violations.

---

## Collaboration Protocol

Documents require iterative collaboration. **Never draft an entire document in one sweep.**

### Phase 1: Prep — Gathering Context

**Goal:** Build shared understanding deep enough that both human and Claude can identify the strategic core of the idea before any drafting begins.

**This phase solves a specific problem:** Claude starts every session cold. Without structured context gathering, the first 2-3 draft iterations are wasted discovering what the human already knows. Phase 1 front-loads that discovery.

#### Context Gathering Sequence

Work through these in order. Each builds on the previous.

**1. Strategic landscape** — What already exists around this idea?
- Read Design Strategy and Product Strategy for relevant priorities (Grep for theme keywords — never full-file load for product_strategy_assessments.md)
- Read 2026 OKRs for organizational priority connections
- Check for existing incubator ideas in the same space (themes, domain overlap)
- Check for completed documents that address adjacent territory

**2. Problem grounding** — What's actually broken?
- What pain points exist? For whom? How do we know?
- What's the current workaround? What does it cost (time, quality, opportunity)?
- Is this a problem the organization feels, or one the human has diagnosed that others haven't seen yet?
- What evidence exists beyond intuition? (customer data, support tickets, team feedback, competitive pressure)

**3. Human context** — What does the human know that isn't written down?
- Stakeholder dynamics, organizational politics, timing factors
- Conversations that shaped thinking but aren't documented
- Prior attempts to address this problem and why they stalled
- Who cares about this and who would resist it

**4. Scope and boundaries** — What is this, and what isn't it?
- What output format fits? (See "When to Use Which Output Format" decision criteria)
- What's in scope vs. explicitly out?
- What are the hard constraints vs. open design space?
- What level of ambition is appropriate given organizational context?

#### Sufficiency Threshold

Phase 1 is complete when you can answer YES to all four:

1. **Can you articulate the problem in one sentence without hedging?** If you need "might" or "potentially," you don't understand the problem yet.
2. **Can you name the strategic connection?** Not "this relates to our priorities" — which specific priority, and through what mechanism?
3. **Can you identify who cares and why?** Not generic stakeholders — specific roles with specific stakes.
4. **Can you explain what's different about this idea vs. what already exists?** If you can't differentiate it, you haven't gathered enough context or the idea needs sharpening.

If any answer is NO: ask the human targeted questions to fill the gap. Do not proceed to Phase 2 with gaps — they compound downstream.

#### Output

A context summary (verbal or written) covering:
- Problem statement (one sentence, no hedging)
- Strategic connection (specific priority + mechanism)
- Key stakeholders and their stakes
- Scope boundaries
- Open questions flagged for Phase 2 resolution

**Time:** This phase takes as long as it takes. Rushing it wastes 3x the time in revision cycles later.

### Phase 1.5: Brain Dump Synthesis

**Goal:** Extract the strategic core from unstructured human thinking. This is where Claude earns its keep.

**When to use:** When the human has thinking they haven't articulated formally — ideas from conversations, reactions to competitors, intuitions about market shifts, or connections they see but haven't written down. The human says something like "let me just dump what I'm thinking" or starts talking through ideas without clear structure.

**Why this exists:** The highest-value strategic insights often arrive as messy, nonlinear brain dumps. The human sees connections between organizational dynamics, market signals, stakeholder conversations, and domain expertise — but hasn't distilled them into strategic framing. Claude's job is to be the synthesis engine that extracts and structures what the human already knows.

#### The Loop

```
Human provides unstructured thinking
    ↓
Claude synthesizes into structured framing
    ↓
Human validates, corrects, extends
    ↓
Repeat until strategic core crystallizes
```

**Round 1 — Listen and extract:**
- Let the human talk. Do not interrupt with questions or structure.
- After the dump, synthesize what you heard into:
  - **Core insight** (one sentence — what is the central idea?)
  - **Problem diagnosis** (what's broken that this addresses?)
  - **Strategic connection** (how does this connect to current priorities?)
  - **Tension or contradiction** (what's unresolved in the thinking?)
- Present this synthesis and ask: "Is this the right core, or am I missing the real point?"

**Round 2 — Refine and challenge:**
- Based on corrections, revise the synthesis.
- Surface what's implicit: "You seem to be saying X — is that the strategic bet?"
- Identify the strongest thread: "The most powerful angle I'm hearing is [X] because [reason]. Is that where the energy is?"
- Flag gaps: "I don't have enough to connect this to [specific priority]. Can you tell me more about [specific question]?"

**Round 3+ — Converge:**
- Each round should narrow, not expand. If it's expanding, the core isn't identified yet.
- Stop when you can state the strategic core in one confident sentence and the human says "yes, that's it."
- If the human keeps adding new dimensions after 3+ rounds, pause and ask: "Are we looking at one idea or several? I'm hearing [X], [Y], and [Z] — which is the primary bet?"

#### Quality Signals

**Synthesis is working when:**
- The human says "yes, that's what I mean" or "exactly"
- Each round gets sharper, not broader
- The human starts building on your synthesis rather than correcting it
- Connections emerge that neither party saw individually

**Synthesis is failing when:**
- The human keeps saying "no, that's not quite it"
- Rounds are adding complexity without convergence
- Claude is imposing framework language on organic thinking
- The human's energy drops (you're losing the thread)

**When synthesis fails:** Stop trying to synthesize. Ask the human directly: "What's the one thing about this idea that excites you most?" Start from that anchor instead of from structure.

#### Output

The synthesis loop produces input for Phase 2 (North Star). Specifically:
- A crystallized one-sentence core insight
- Problem diagnosis grounded in the human's context
- Strategic connection validated by the human
- Open tensions flagged for resolution during drafting

This is NOT a formal document — it's shared understanding. The human and Claude should be on the same page about what this idea IS before any drafting begins.

### Phase 2: North Star Alignment

**Goal:** Lock the strategic through-line before investing in detailed drafting. The through-line is the thread that connects every section — if it breaks, the document falls apart.

**What "aligned" means:** Human and Claude agree on (1) what the core bet is, (2) why it matters strategically, and (3) what outcome it drives. This should be expressible in 2-3 sentences. If it takes a paragraph to explain the direction, alignment isn't there yet.

#### Through-Line Identification

Before drafting any sections, establish the through-line:

1. **State the strategic bet** — What are we betting on, and why? One sentence.
2. **State the mechanism** — How does this bet create value? One sentence.
3. **State the outcome** — What changes if this succeeds? One sentence.

**Example:**
- **Bet:** Assessment data is more valuable when it flows across products than when it's siloed.
- **Mechanism:** An interoperability layer lets assessment insights inform instruction across products simultaneously.
- **Outcome:** The organization becomes the assessment platform — not just an assessment tool — making switching costs structural, not just contractual.

The through-line is: data portability → platform value → competitive moat. Every section of the document should advance this thread. If a section doesn't connect, it either needs reframing or doesn't belong.

#### Format-Specific North Star Sections

**For strategy docs — draft these FIRST:**
1. **Strategic Thesis** — The bet and mechanism in 1-2 sentences
2. **Context & Opportunity** — The diagnosis that makes this bet necessary now

Present these together. Iterate until the human confirms direction. Do NOT proceed to Strategic Priorities until the thesis and diagnosis are locked. Changing these later invalidates all downstream work.

**For briefs — draft these FIRST:**
1. **Initiative Hypothesis** — The bet as "We believe [initiative] will [outcome] by [approach]"
2. **Problem & Opportunity** — The narrative diagnosis (one flowing paragraph)
3. **Strategic Anchors** — Why this connects to current priorities

Present these together. The hypothesis should feel inevitable after reading the problem statement and anchors. If it doesn't, one of the three is off.

#### Alignment Signals

**Aligned (proceed to Phase 3):**
- Human responds with "yes" or "that's right" without caveats
- Human starts building on the framing ("and that also means...")
- The through-line is clear enough to state in one sentence
- Human can explain the direction to a peer without referencing the draft

**Not yet aligned (iterate):**
- Human says "I don't see why this matters" → Diagnosis is weak. Return to problem grounding.
- Human says "that's not quite it" → Through-line is off. Ask: "What's the part I'm missing?"
- Human adds significant new context → Synthesis isn't complete. Return to Phase 1.5.
- Diagnosis feels generic (could apply to any domain) → Not specific enough. Ask: "What makes this specifically about [domain] and not a general industry problem?"
- Strategic connection isn't clear → Mechanism is weak. Ask: "How exactly does this create value for your organization specifically?"

#### Red Flag Response Actions

| Red Flag | Response |
|----------|----------|
| "I don't see why this matters" | Don't argue — the diagnosis is weak. Ask: "What would make this matter? What's the version of this that you'd fight for?" |
| "This could describe any company" | Differentiation is missing. Ask: "What does your organization have or know that makes you uniquely positioned here?" |
| "That's technically right but misses the point" | You've captured the surface, not the insight. Ask: "What's the thing about this that gets you excited? Start there." |
| "We already tried this" | Context gap. Ask: "What was different about the previous attempt? What's changed since then?" |
| Human keeps adding new dimensions | Scope is unclear. Pause: "Are we looking at one strategic bet or several? Let's pick the primary one." |

### Phase 3: Section-by-Section Drafting

**Goal:** Build the document iteratively with feedback loops.

Draft one section, get feedback, refine, then move to the next. Apply learnings from one section's feedback to other sections proactively. One section at a time.

**Self-Critique Protocol (MANDATORY BEFORE PRESENTING):**

Before presenting ANY draft section:

1. **Run full validation** — Check against the format-specific Validation Checklist AND Persona Guidelines
2. **Identify issues** — Note everything that fails validation
3. **FIX issues immediately** — Revise the draft, don't ask permission
4. **Validate fixes** — Re-check against checklists
5. **THEN present** — Only show work after self-correction

**DO NOT:**
- Present draft, identify issues, then ask "should I fix these?"
- Present draft and wait for user to identify issues you should have caught
- Ask permission to apply documented best practices
- Rely solely on user feedback instead of self-validation

**Proactive Application Mindset:**

The self-critique protocol only works if you internalize principles deeply enough to apply them independently:

- **Study working examples BEFORE drafting** — Deeply analyze WHY a completed section works (voice, flow, strategic vantage point) before drafting the next one
- **Embody voice until deviations sound wrong immediately** — Not "check against checklist afterward" but internalize persona deeply enough that corporate language sounds wrong as you write it
- **Find root cause after 3rd correction** — If corrected repeatedly for the same issue, stop and ask "why do I keep doing this?" Fix the underlying pattern, not just the instance
- **Treat user's time as precious** — Don't present work that violates documented principles you already have

**Feedback Loops: As Many as It Takes**

There is no target number of iterations. The goal is quality and alignment, not speed:
- Expect multiple rounds of refinement on most sections
- Not rush to "finish" before it's actually right
- Apply learnings from one section's feedback to other sections proactively
- Ask clarifying questions when feedback reveals misunderstood intent

#### Through-Line Maintenance During Drafting

The through-line established in Phase 2 must survive contact with detailed section work. As you draft each section, check:

**Before drafting a section:**
- State (to yourself) how this section advances the through-line
- If you can't, either the section needs reframing or the through-line needs updating
- Some sections are structural (Boundaries, References) — they support but don't advance. That's fine, but the core narrative sections must all pull in the same direction.

**After drafting a section:**
- Read the section and ask: "If someone read only this section, would they understand the strategic direction?"
- Check: does this section's language reinforce or contradict the thesis/hypothesis?
- Check: are you introducing new strategic claims not grounded in the diagnosis?

**When the through-line breaks:**
The through-line will sometimes break during drafting — a section reveals that the original framing was incomplete or wrong. This is valuable, not a failure.

- If a section requires a strategic claim the diagnosis doesn't support → the diagnosis needs updating, not the section needs forcing
- If two sections pull in different directions → one of them is off-strategy. Identify which and flag for human decision.
- If new information from research changes the strategic core → pause drafting, return to Phase 2, re-establish alignment. Do not silently drift.

**The test:** At any point during drafting, you should be able to state the through-line in one sentence. If you can't, alignment has drifted. Stop and re-anchor.

### Phase 4: Validation & Refinement

**Goal:** Ensure the document is deployable and ready for stakeholders.

**Activities:**
1. Full validation pass using format-specific checklist
2. Cross-section consistency check
3. Voice alignment against persona guide
4. Strategic connections checked for realism (not overstated)
5. Final refinements based on feedback

**Output:** Completed document ready for review/publishing.

---

## Working with Source Material

Documents are informed by conversations, transcripts, stakeholder interviews, and existing documents — but source material is **raw material for strategic thinking**, not content to copy.

### Treating Transcripts and Conversations

**Transcripts are informal conversations to mine for insights, not requirements documents to implement.**

**What to do:**
- Extract strategic insights and decided approaches
- Identify what matters strategically (leverage points, constraints, opportunities)
- Apply strategic thinking patterns from this methodology
- Synthesize raw ideas into clear strategic framing

**What NOT to do:**
- Copy language verbatim from conversation
- Treat every mentioned idea as equal priority
- Include implementation details that belong in briefs (when writing strategy)
- Present options that were already decided in conversation

**Example:**
- Transcript says: "Yeah, we should probably do like 8-12 widgets, maybe 15, and use Zoe's framework since it's already there"
- Strategy doc says: "The approach builds a data visualization design system: 8-12 core widget types maintained through an internal open source model"

### Business Context Validity for Examples

Strategic examples must reflect actual business and customer patterns, not just what's technically possible.

**Validate examples against:**
- **Customer patterns:** Do customers actually use products this way?
- **Business model:** Does this align with how we go to market?
- **Actual usage:** Would this scenario realistically occur?
- **Strategic value:** Does this example show the multiplicative benefit we're claiming?

### Connecting to Organizational Context

Strategic language gains power when it connects to broader initiatives the organization already understands.

**Look for opportunities to:**
- Reference similar approaches in other domains
- Position as analogous to known patterns
- Use organizational language that stakeholders recognize
- Connect to broader platform initiatives

### Working with Strategy Documents as Reference

**Location:** `Professional/Strategic Context/`

**Key documents:**
- Product strategy document (path from CLAUDE.md Configuration > External References — large file, use targeted Grep, never load full)
- Design strategy document (path from CLAUDE.md Configuration > External References)
- OKRs / organizational goals (path from CLAUDE.md Configuration > External References)

**Usage patterns:**
- Use targeted searches (Grep) for specific priorities, principles, or initiatives
- Reference specific sections, not entire docs
- Validate strategic connections before drafting

**Don't Over-Quote:** Referencing strategy is good. Extensively quoting or paraphrasing strategy docs makes documents dense and hard to read. Synthesize the intent, don't transcribe the words.

### When to Stop Refining

**Signs you should stop:**
- Content meets length guidelines
- Flows naturally when read aloud
- Specific and concrete (no vague abstractions)
- Aligns with persona voice and strategic principles
- Stakeholder feedback is "this looks good" not "this needs work"

**Signs you're overthinking:**
- Changing phrasing without improving clarity
- Debating word choices that don't affect meaning
- Adding explanatory detail that doesn't change understanding
- Addressing style preferences rather than strategic issues

---

## Research Protocol

### When to Conduct Research

**Research First (Before Drafting):**
- Product/design strategy exists but doesn't cover this domain
- Strategic anchors are unclear or need validation
- Market intelligence needed (competitor analysis, TAM, technology trends)
- Cross-product validation required
- Technical feasibility questions
- Stakeholder context missing

**Red Flags That Signal Insufficient Context:**
- Can't articulate the problem/diagnosis without making assumptions → research first
- Strategic leverage/alignment feels fabricated → validate before drafting
- Platform implications unclear → investigate cross-product patterns
- Don't understand why this matters to the business → research value prop
- Success measures are guesses → validate what's measurable

### Research Approaches & Tools

**1. Gemini CLI for Large-Context Operations**

Use when:
- Task requires massive context that would pollute working context window
- Need synthesis/transformation of large data sets (multi-hundred-page docs)
- Can specify output format and get back compact, actionable results
- Multi-step queries across Atlassian (Confluence/Jira)

Benefits: 96% context reduction, structured output (JSON, CSV, tables), multi-step workflows.

**2. Agent Tool with Explore Agent**

Use when:
- Searching for precedent documents with similar patterns
- Discovering existing implementations or patterns
- Understanding organizational structure from documentation
- Finding related work across project directories

**3. Web Search + Synthesis**

Use when:
- Competitor capability research needed
- Market sizing or TAM validation required
- Technology trend analysis
- Industry standards or best practices

### Research-Driven Decision Points

| Scenario | Action |
|----------|--------|
| Can't articulate problem/diagnosis without assumptions | Research pain points, validate problem exists |
| Strategic connections feel fabricated | Validate against strategy docs, confirm alignment |
| Cross-product check reveals duplication | Investigate thoroughly before proceeding |
| Technical feasibility unclear | Research integration approach, platform constraints |
| Market opportunity uncertain | Research TAM, competitor positioning, trends |
| Success measures are guesses | Research what metrics are tracked, what's measurable |

**What to say when context is insufficient:**

> "Before I draft [section], I need to research [specific gap]. Should I:
> 1. Search Confluence/Jira using Gemini CLI for [specific context]
> 2. Use Explore agent to find precedent documents or implementations
> 3. Conduct web research on [competitor/market/best practices]
> 4. Draft with explicit assumptions and flag for validation"

### Context Optimization

**For high-context work, use forked context via:**
- Gemini CLI (external tool, returns compact results)
- Agent tool with specialized agents (separate context window)

This preserves working context for core drafting and iterative refinement.

### Research Sufficiency Threshold

**When is research "enough" to start drafting?**

Research is sufficient when you can draft every section of the target template without writing "TBD" or making unsupported claims. Specifically:

**For Strategy Documents, you need:**
- Problem diagnosis grounded in evidence (not intuition alone)
- At least one validated strategic connection (direct or adjacent, with mechanism)
- Enough competitive/market context to make credible differentiation claims
- Specific enough understanding to write "How We Might Approach This" with rationale

**For Product Briefs, you need:**
- Concrete user pain point with evidence (customer data, support tickets, observed behavior)
- Strategic anchors that can be stated with honest mechanisms (not stretched)
- Enough technical context to identify real risks and constraints
- Clear enough scope to write JTBD at the outcome level

**When to draft with gaps vs. research more:**

| Signal | Action |
|--------|--------|
| Can articulate problem but not mechanism | Draft with [NEEDS MECHANISM] markers — mechanism often emerges during drafting |
| Can't articulate problem at all | Research more. Don't draft into a void. |
| Strategic connection exists but strength is unclear | Draft honestly: "supports" not "advances." Flag for human validation. |
| No competitive context | Do 3-5 targeted web searches. If still nothing, note "competitive landscape unclear" and proceed. |
| Technical feasibility uncertain | Draft with explicit feasibility questions in Open Questions. Don't fake technical confidence. |
| Missing stakeholder context | Ask the human. This can't be researched — it requires organizational knowledge. |

**The 30% rule:** If more than 30% of the template sections require unsupported claims, you don't have enough context to draft. Return to Phase 1 or conduct targeted research.

---

## Iteration & Feedback Patterns

### Expect Iteration

Documents require multiple rounds of refinement. This is normal and expected:
- Strategic Priorities / core sections often take 3-4 iterations
- Diagnosis/framing sections may need 2-3 passes
- Success measures get refined as you validate what's measurable

**Quality over speed.** There is no prize for finishing quickly.

### When You Receive Feedback

**Good response pattern:**
1. Understand the principle behind the feedback (not just the specific request)
2. Check if the issue appears elsewhere in the document
3. Propose the fix and explain your reasoning
4. Apply the learning to future sections

**If feedback reveals misunderstanding:**
- Ask clarifying questions to understand intent
- Re-read source materials
- Acknowledge the gap explicitly

**If feedback points to a pattern:**
- Check if same issue appears in other sections
- Apply the learning proactively across the document

**If feedback suggests starting over:**
- Don't defend the draft — understand why it's off
- Identify root cause (wrong framing? weak diagnosis? wrong level?)
- Start fresh with corrected understanding

### When to Push Back vs. Accept

**Accept when:**
- You've misunderstood template intent
- You've overstated alignment or impact
- You've included metrics that don't prove value
- Your approach conflicts with the methodology
- User has context you don't (organizational dynamics, history, stakeholder concerns)

**Push back when (rare):**
- Feedback asks for prescriptive solutions where the document should enable decisions
- Requested detail level is too tactical (or too abstract) for the format
- Suggestion conflicts with research-backed strategic thinking
- Scope creep would make the document too broad to be actionable
- Feedback would undermine the document's ability to align its audience

**Gray area — Discuss:**
- Tension between aspirational and realistic tone
- Uncertain about strategic leverage claim
- Conflicting feedback from different sources
- Unsure if example is helpful or distracting

### Collaboration Techniques

**Ask clarifying questions early:**
- "When you say 'platform-first,' do you mean X or Y?"
- "Should this section emphasize technical approach or business outcomes?"
- "Is this diagnosis accurate or am I missing context?"

**Offer options when uncertain:**
- "I see two approaches: A (more aspirational) or B (more tactical). Which fits better?"
- "Should I cut to focus on X, or expand to cover Y?"

**Show your reasoning:**
- "I'm framing this as opportunity because [reasoning]. Does that align?"
- "I kept JTBD detailed because it defines scope through user needs. Want it more concise?"

**Validate assumptions:**
- "I'm assuming teams currently do X. Is that accurate?"

---

## Output Format: Strategy Document

### Why Create a Strategy Document

You create a strategy document because **you want to drive a specific outcome that won't happen naturally without strategic direction.**

Without strategy, teams will make locally optimal decisions that don't add up to the outcome you need. They'll fragment, duplicate, or miss the opportunity entirely.

**Examples of outcomes worth strategic direction:**
- **Differentiation:** Making your product indispensable vs. interchangeable
- **Market disruption:** Changing how users think about a problem space
- **De-risking:** Ensuring mission-critical work doesn't fail
- **Platform leverage:** Creating compounding value through reusable patterns
- **Speed to market:** Coordinating to move faster than competition

**Every section should connect to that outcome:**
- Strategic Thesis states the outcome
- Context & Opportunity explains why current state won't achieve it
- Strategic Priorities define choices that drive toward it
- Success measures evidence you're achieving it

### Collaboration Phase Mapping

How the collaboration phases apply to strategy document sections:

| Phase | Sections | Goal |
|-------|----------|------|
| Phase 1 (Prep) | — | Gather context: read strategy docs, understand problem space, identify connections |
| Phase 1.5 (Brain Dump) | — | If human has unstructured thinking to synthesize, extract strategic core |
| Phase 2 (North Star) | Strategic Thesis + Context & Opportunity | Lock the through-line. Do NOT proceed until these are approved. |
| Phase 3 (Drafting) | Strategic Priorities (one at a time) | Draft each priority independently, maintaining through-line. This is where depth lives. |
| Phase 3 (Drafting) | What Success Looks Like | After priorities are solid — success measures must connect to priority outcomes |
| Phase 3 (Drafting) | Looking Beyond | After success measures — speculative but grounded in the strategy foundation |
| Phase 3 (Drafting) | Boundaries & Dependencies | Can draft anytime after Phase 2 — scope clarity helps all other sections |
| Phase 4 (Validation) | Full document | Cross-section consistency, voice check, through-line integrity |

**Key sequencing rule:** Strategic Priorities must be drafted one at a time in Phase 3, not all at once. Each priority gets its own feedback loop before moving to the next. Learnings from one priority's feedback should be applied proactively to subsequent priorities.

---

### Section-by-Section Guidance

#### Strategic Thesis

**Purpose:** Inspire teams to think differently while directing them toward a clear outcome. Focus on market differentiation over competitor parity.

**What to include:**
- A reframing or provocative insight that shifts thinking
- A clear outcome direction that makes us indispensable, not interchangeable
- Differentiation from competitors

**What to avoid:**
- Mechanical "teams should do X" statements without inspiration
- Generic goals without approach ("We will be the best")
- Competitor parity positioning ("We'll match feature X")

**Self-check:**
- Does this make teams see the problem differently?
- Is the outcome clear and differentiated?
- Does this inspire toward market leadership, not feature parity?

**Example:**
"Assessment dashboards should feel like they understand what teachers need before they ask — transforming data overload into actionable next steps that save hours and improve outcomes, making the platform indispensable rather than interchangeable."

---

#### Context & Opportunity

**Purpose:** Diagnose current state honestly — what exists, what's broken, why now matters.

**Length:** 150-250 words (one flowing narrative)

**Structure:**
1. **Current state** — What patterns exist today? What are teams doing?
2. **What's broken** — Why aren't current approaches working? Be specific.
3. **The opportunity** — What becomes possible if we address this?
4. **Why now** — What's changed to make this the right time?
5. **Patterns we're moving away from** — What should teams stop doing?

**Tone:** Realistic and honest. This is diagnosis, not aspiration.

**What to avoid:**
- Weak diagnosis (Rumelt's #1 cause of bad strategy)
- Confusing symptoms with root causes
- Aspirational language — save that for Strategic Priorities
- Blaming teams for current state

**Self-check:**
- Would teams recognize this diagnosis as accurate?
- Does this identify root causes, not just symptoms?
- Is timing/opportunity clear?
- Does this set up Strategic Priorities logically?

**Common pitfall:** Spending 2 sentences on current state then jumping to "here's what we should build." Take time for thorough diagnosis.

---

#### Strategic Priorities

**Purpose:** Define 3-5 strategic capabilities or outcomes that guide decisions. Priorities are NOT solutions — they're the strategic focus areas teams will develop solutions within.

**Naming priorities:**
- GOOD: "Configurable Dashboard Experiences" (capability to enable)
- GOOD: "Assessment as Platform Signal" (outcome to achieve)
- BAD: "Build Modular Widget Framework" (that's a solution)

**Structure for EACH priority:**

**1. Opportunity** (required)
- **Length:** 1-2 paragraphs
- **Content:** Why does this capability matter? What becomes possible? Who benefits?
- **Tone:** Opportunity identification

**2. Strategic Advantage** (optional)
- **Length:** 1 paragraph
- **Content:** Why are we uniquely positioned to deliver this? Platform effects, ecosystem advantages, unique assets, compounding value
- **Use when:** You have clear competitive differentiation
- **Skip when:** Advantage isn't clear or capability is table stakes

**3. How We Might Approach This** (required — THE MEAT)
- **Length:** 2-4 paragraphs
- **Content:**
  - **Open with strategic vantage point** — Establish the lens through which you're evaluating the approach
  - What's the recommended approach? (State it directionally)
  - Why does this approach work? (Strategic rationale)
  - What are key considerations or constraints?
  - What becomes possible? (Close with implications)
- **Flow pattern:** Strategic vantage point → Explore approach through that lens → Show trade-offs → Close with what becomes possible
- **This is where you get opinionated.** Show strategic thinking, explain reasoning, provide direction.
- **Anti-pattern:** Listing options without establishing strategic vantage point first

**Total length per priority:** 300-500+ words

**Tone:** Confident and directional. You're providing strategic guidance, not facilitating a debate.

**Self-check:**
- Are priorities named as capabilities/outcomes, not solutions?
- Does "How We Might Approach This" show strategic thinking?
- Are you being directional and confident, not tentative?
- Do priorities work together coherently as a portfolio?

---

#### What Success Looks Like

**Purpose:** How will we know this strategy is working? Success measures must connect directly to strategic priorities — if a metric doesn't trace back to a priority, it doesn't belong.

**Format:** Unified narrative with bold outcome statements followed by specific metrics/signals.

**What to include:**
- **Business outcomes:** MAU, engagement, retention, revenue impact
- **Platform outcomes:** Adoption rates, efficiency gains, reusability metrics
- **Quality outcomes:** Usability scores, performance, design system health
- **Developer experience:** Velocity improvements, satisfaction
- **Market differentiation:** Customer perception, competitive positioning

Integrate both leading indicators (early signals) and long-term outcomes naturally within each outcome statement.

**How to write measurable but not reductive metrics:**
- Pair quantitative metrics with qualitative signals: "Dashboard adoption rate (quantitative) + teacher-reported time savings in workflow surveys (qualitative)"
- Distinguish leading indicators (early validation) from lagging outcomes (proof of lasting value)
- Every metric should answer: "If this number moves, does it prove the strategy is working?" If not, it's the wrong metric.

**How to weight outcomes when resources are constrained:**
- Prioritize metrics that validate the strategic thesis first (the core bet)
- Second priority: metrics that demonstrate the multiplicative effect (one move → multiple outcomes)
- Last: metrics that track execution quality (important but not strategic)

**Example (from assessment strategy):**
> **Instructional decision velocity increases measurably.** Teachers using insight-driven assessment tools make instructional adjustments 2x faster than those using raw score reports. Leading indicator: time-to-first-action after viewing assessment results. Lagging outcome: student growth metrics in classrooms using guided insights vs. raw data.

**What to avoid:**
- Vanity metrics that don't drive outcomes ("number of dashboards created")
- Only business metrics — include quality, sentiment, adoption
- Metrics that are easy to game ("assessment completion rate" without quality signal)
- Success measures unrelated to strategy priorities
- Metrics nobody is currently tracking and nobody will set up tracking for

**Self-check:** For each metric, ask: "Who will track this, how, and what decision does it inform?" If you can't answer all three, the metric isn't actionable.

---

#### Looking Beyond

**Purpose:** Capture forward-thinking opportunities beyond immediate strategy. This section plants seeds — it shows where the current strategy leads if it succeeds.

**Length:** 1-3 forward-thinking scenarios, each 75-150 words.

**Tone:** Speculative but grounded. These should feel like inevitable next steps if the strategy works, not disconnected moonshots.

**The grounding test:** Each scenario must:
1. Build on a specific capability created by the current strategy (name it)
2. Describe what becomes possible that isn't possible today
3. Connect to a business outcome (even speculatively)

**Example (grounded):**
> **From insights to intervention.** If assessment dashboards successfully shift from data display to actionable guidance (Priority 1), the natural next step is closing the loop entirely: the system not only recommends what to reteach, but provides the remediation content. Assessment becomes the trigger for a personalized learning path — positioning the platform as the system that connects measurement to mastery, not just measurement to a report.

**Example (ungrounded — avoid):**
> "We could also explore blockchain-based credential verification, AI-generated assessment items, VR assessment environments, and gamified learning pathways."

**What separates good from bad:** Good scenarios tell a story about compounding value. Bad scenarios list technologies or features without strategic logic.

**What to avoid:** Listing every possible future feature, disconnected ideas, detailed implementation plans, commitments or timelines, technology name-dropping without strategic rationale.

---

#### Boundaries & Dependencies

**Purpose:** Clear scope and explicit prerequisites.

**Two subsections:**

**1. Strategic Boundaries**
- What this strategy COVERS
- What this strategy explicitly DOES NOT COVER
- Related strategies this connects to

**2. Key Dependencies**
- Technical dependencies (platforms, APIs, capabilities)
- Organizational dependencies (roles, teams, processes)
- Resource dependencies (time, budget, headcount)
- Knowledge dependencies (research, validation, expertise)

**Common pitfall:** Assuming dependencies will magically appear. Be explicit.

---

#### Open Questions & References

**Two subsections:**

**1. Open Questions** (Table format)

| Question | Owner/Decision Maker | Target Date |
|----------|---------------------|-------------|
| Should we expand to X domain? | [Name] | Q2 2026 |

**2. References** (Categorized links)
- Conversations, Research & Data, Related Documents

**Maintenance:** Keep current. Archive resolved questions.

---

### Strategy Validation Checklist

Run this checklist before presenting ANY draft section. Each item has a concrete test — not just a reminder.

#### Voice & Persona (CHECK FIRST — most common failure mode)

| Check | Test | Pass | Fail |
|-------|------|------|------|
| Confident and declarative | Read each sentence: does it state or hedge? Circle every "could," "might," "potentially." | Zero hedge words, or hedges are deliberate (genuine uncertainty) | Any accidental hedging → rewrite as declarative |
| Natural flow | Read aloud. Does it sound like explaining to a peer, or reading a corporate memo? | Sounds conversational, has rhythm | Sounds stiff, choppy, or mechanical → rewrite for flow |
| Concrete and specific | Highlight every abstract phrase. Can you replace it with a name, number, or example? | Every claim has specifics | Any "significant advantages" or "meaningful impact" without specifics → add them |
| No banned words | Search for: leverage, synergies, holistic, robust, utilize, meaningful, proven | Zero hits | Any hit → replace with plain language |
| Multiplicative framing | Does the opportunity/advantage show compounding value (one move → multiple outcomes)? | At least one multiplicative frame in thesis or priorities | Only linear framing (do X → get Y) → reframe |
| Length | Check against format-specific length guidelines | Within range | Over → cut 20%. Under → likely superficial, add depth |

#### Strategic Quality

| Check | Test | Pass | Fail |
|-------|------|------|------|
| Rumelt test | Does the thesis explain WHERE + HOW, not just WHERE? | Clear approach/mechanism, not just aspiration | "We will be the leader in X" without how → add mechanism |
| Perri test | Are priorities outcomes/capabilities, not outputs/features? | Named as capabilities to enable | "Build X system" → reframe as capability |
| Diagnosis depth | Does Context & Opportunity identify root causes, not symptoms? | Root cause named, not just "current state is bad" | Only symptoms → dig deeper |
| Through-line integrity | Can you state the strategic thread in one sentence? Does every section connect? | One sentence captures it, all sections advance it | Can't state it, or sections contradict → re-anchor |
| Strategic realism | Are connections honest? Would a VP challenge any claim? | Every connection has a specific mechanism | Any "this advances X" without explaining how → downgrade or add mechanism |
| Cross-functional | Would PM, Design, AND Engineering each see how this applies to them? | All three perspectives addressed | Single-discipline framing → add perspectives |

#### Completeness

| Check | Test | Pass | Fail |
|-------|------|------|------|
| Every section has substance | Read each section: does it have real content or is it a placeholder? | All sections have specific, grounded content | Any section feels thin or generic → add substance or flag as gap |
| Success measures are measurable | For each metric: could you set up tracking for this today? | All metrics reference trackable signals | Any metric that can't be measured → replace or flag |
| Dependencies are explicit | Are prerequisites stated as facts, not hopes? | Named dependencies with owners | "Assumes X will be available" without who/when → specify |
| AI limitations acknowledged | Where you genuinely can't validate, have you said so? | Explicit acknowledgment where applicable | Faked certainty on things you can't verify → add disclaimer |

---

### Strategy Common Pitfalls

**1. Confusing Strategy with Goals**
Writing "We will be the leader in dashboarding" without explaining HOW. Strategy = WHERE + HOW, not just WHERE.

**2. Weak Diagnosis**
Spending 2 sentences on current state then jumping to solutions. Most strategy failures start here (Rumelt).

**3. Writing Product Brief Language**
"We believe building X will achieve Y" is initiative framing, not strategy. Use: "When teams face X decision, they should apply Y principles."

**4. Prescribing Solutions**
"Teams must use component library X" → "Teams should prioritize reusable components over custom solutions"

**5. Feature Lists as Priorities**
Strategic Priority = "Build modular widget system with 8-12 patterns" → Should explain why modular approach creates platform advantage and how teams should think about decisions.

**6. Ignoring Strategic Leverage**
Solving problems without explaining differentiation or multiplicative advantage.

**7. Forgetting Cross-Functional Perspectives**
Writing strategy from a single discipline lens. Consider how PM, Design, and Engineering each apply strategic priorities.

**8. Unmeasurable Success**
Success measures that sound good but can't actually be tracked.

**9. Aspirational Tone Everywhere**
Writing "What if" language in Context/Diagnosis sections. Use hybrid tone: realistic diagnosis, aspirational priorities.

**10. Scope Creep**
Trying to solve every related problem in one strategy. Use Boundaries section.

---

### Strategy Length Guidelines

**Brief sections:**
- Strategic Thesis: 1-2 sentences
- Boundaries & Dependencies: Bulleted lists, clear and direct

**Comprehensive sections:**
- Strategic Priorities: 300-500+ words EACH (this is where you invest depth)
- Context & Opportunity: 150-250 words

**Contextual balance:**
- What Success Looks Like: Unified narrative, can be comprehensive if tied to priorities
- Open Questions: Table format keeps it scannable

**Red flags:**
- Strategic Thesis longer than 3 sentences → too much
- Strategic Priorities under 200 words per priority → too brief, likely superficial
- Boundaries longer than 10 bullets per list → scope too unclear
- Context section over 300 words → likely includes too much detail

---

### When to Revise Strategy

Strategy documents are living artifacts. They need revision when the assumptions they're built on change. This section defines when to trigger a revision cycle vs. when to let the existing strategy stand.

**Trigger a revision when:**
- **Market shifted:** A competitor launched something that changes competitive positioning, a regulatory change created new constraints or opportunities, or a technology shift enabled something previously infeasible
- **Organizational priorities changed:** OKRs updated, leadership direction shifted, resource allocation changed significantly
- **Strategy failed its own success measures:** Metrics moved in the wrong direction or didn't move at all after reasonable execution time
- **Key assumptions proved wrong:** Research, customer data, or execution experience invalidated a core assumption the strategy depends on
- **Teams can't apply it:** Multiple teams report that strategic priorities don't help them make decisions — the strategy is too abstract, too stale, or too disconnected from reality

**Don't revise when:**
- A single initiative didn't work (that's initiative-level learning, not strategy failure)
- Someone disagrees with the direction (that's a conversation, not a revision trigger)
- New opportunities appear that aren't in the current strategy (add to Looking Beyond or start a new strategy — don't dilute the current one)
- Style or tone preferences changed (that's editing, not revision)

**Revision process:**
1. Identify which assumption or condition changed
2. Assess impact: does this affect the thesis, a specific priority, or just execution details?
3. If thesis-level: full revision cycle starting from Phase 2 (re-establish North Star)
4. If priority-level: revise the affected priority and check downstream impact (success measures, dependencies)
5. If execution-level: update the relevant section without changing strategic direction

**Staleness check:** If a strategy document hasn't been referenced or applied in 6+ months, it's either working invisibly (good) or irrelevant (bad). Check with teams: "Are you using this to make decisions?" If not, either revise or archive.

---

## Output Format: Product Brief

Product briefs provide **just enough structure** for the triad (Product, Design, Engineering) to align on the problem, define the opportunity, and establish shared direction **before detailed work begins.**

This is the core mandate:
- **Frame the problem space** clearly enough that the triad can align
- **Establish strategic context** so everyone understands why this matters
- **Define success** so the team knows what they're building toward

NOT:
- Write a comprehensive specification
- Prescribe solutions or implementation details
- Provide exhaustive documentation

**Key insight**: If the triad can't start working after reading the brief, you haven't framed enough. If they're overwhelmed by detail, you've framed too much.

### Collaboration Phase Mapping

How the collaboration phases apply to product brief sections:

| Phase | Sections | Goal |
|-------|----------|------|
| Phase 1 (Prep) | — | Gather context: understand the initiative, identify strategic connections |
| Phase 1.5 (Brain Dump) | — | If human has unstructured thinking about the initiative, extract the core bet |
| Phase 2 (North Star) | Initiative Hypothesis + Problem & Opportunity + Strategic Anchors | Lock direction. The hypothesis should feel inevitable after reading problem + anchors. |
| Phase 3 (Drafting) | Jobs to be Done | After Phase 2 — JTBD defines scope through user needs |
| Phase 3 (Drafting) | What Success Looks Like (Success Signals) | After JTBD — validation signals for POC/prototype phase |
| Phase 3 (Drafting) | EAP: Learning Milestone | After success signals — actionable learnings, not adoption metrics |
| Phase 3 (Drafting) | GA: GTM Milestone | After EAP — lasting value metrics, not vanity metrics |
| Phase 3 (Drafting) | Guardrails & Constraints | Can draft anytime after Phase 2 — scope clarity helps all sections |
| Phase 3 (Drafting) | Risks & Challenges + Open Questions | Can draft anytime — working logs that evolve |
| Phase 4 (Validation) | Full brief | Template alignment, voice check, "just enough structure" test |

**Key sequencing rule:** Phase 2 for briefs involves THREE sections (not two like strategy docs). All three must be presented together and approved before moving to Phase 3. The hypothesis, problem narrative, and strategic anchors form a unit — they need to reinforce each other.

---

### Section-by-Section Guidance

#### Initiative Hypothesis

**Format**: "We believe [initiative] will [outcome] by [approach]"

Keep it simple: One sentence that captures the core bet. Don't add caveats, conditions, or extensive explanation here. The rest of the brief provides that.

**Example:**
> We believe enabling instructors to integrate third-party simulation content into Canvas Assessments and Assignments will significantly increase authentic assessment adoption and demonstrate real-world skill application by making immersive, interactive assessment experiences as easy to create and evaluate as traditional quizzes, while unlocking marketplace revenue and partnership opportunities.

---

#### Problem & Opportunity

**Template intent**: Tell a story in narrative form. One paragraph (150-250 words) that flows:
1. **Who struggles** and what they're trying to accomplish
2. **Current painful workflow** (specific, concrete)
3. **Behavioral consequence** (what people do or don't do as a result)
4. **Opportunity when solved** (what becomes possible)

**Anti-pattern**: Creating subsections with headers ("The Problem," "The Opportunity," "The Business Case"). This breaks the narrative flow.

**Example structure:**
> Instructors want to [goal] but today they must [painful steps]. Each partner has [fragmentation details]. Many instructors [avoidance behavior] because [pain point]. When [solution vision], instructors can [outcome] and institutions can [value].

**What to include:** Concrete workflow details, specific user behaviors, clear connection between problem and opportunity.

**What to exclude:** Market sizing details (unless critical), competitive positioning details (save for Strategic Anchors), multiple paragraphs with structured arguments.

**Cross-product check**: If you genuinely can't validate that similar functionality doesn't exist elsewhere, add the AI limitations disclaimer. Don't fake this.

---

#### Strategic Anchors

**Template intent**: Brief narrative paragraphs (not bullet points) that answer four questions:
1. How does this advance our product goals?
2. How does this advance our design goals?
3. What larger outcome does this contribute to?
4. What is the impact if we don't do this?

**Length**: ~300-400 words total, 3-4 flowing paragraphs.

**Structure:**
1. **Paragraph 1** (Product goals): Connect to product strategy/priorities — be specific (Priority Loop X, OKR Y).
2. **Paragraph 2** (Design goals): Connect to design strategy — be realistic. If impact is modest, say so.
3. **Paragraph 3** (Larger outcomes): Connect to business outcomes (revenue, retention, competitive position).
4. **Paragraph 4** (Impact if we don't): What risks emerge or opportunities are missed?

**Anti-patterns:**
- Bullet-pointed lists under each question
- Extensive quotations from strategy documents
- Overstating design impact when connection is weak

**Strategic context reference:**

**Design Strategy — Five Priorities:**
1. Intent Recognition & Assessment Creation
2. Instructional Decision Support
3. Context-Aware Configuration
4. Trust-Led Growth
5. Assessment as Platform Signal

**Product Strategy — Key Themes:**
- AMS as unified foundation (Learnosity-powered)
- Unifying Canvas Quizzes and MasteryConnect
- Marketplace/partnership strategy
- Authentic assessment capabilities

---

#### Jobs to be Done

**Template intent**: Define what users need to accomplish. Focus on capabilities and outcomes, not features. JTBD defines scope through user needs — it's the section that answers "what are we actually solving for?"

**This section can be comprehensive.** Unlike Problem & Opportunity, JTBD benefits from detail because it defines scope through user needs. More specificity here = clearer design space for the triad.

**Structure by persona:** Instructors (primary), Students, Administrators, Partners/Other as relevant. Only include personas with distinct jobs — don't add personas for completeness.

**Format**: "When [user] wants to [goal], they need to be able to: [capability list]"

**Scoping JTBD:**
- Include jobs that the initiative directly addresses (in scope)
- Include jobs that the initiative must not break (protect current workflows)
- Exclude jobs that are deferred to future phases (put these in Guardrails)
- If a persona has more than 5-6 jobs, you're probably mixing primary and secondary. Split or defer.

**Keep capabilities outcome-focused:**
- GOOD: "Discover simulation content aligned to their course outcomes"
- BAD: "Click a button to open marketplace and filter by subject"
- GOOD: "Understand at a glance which students are struggling with specific concepts"
- BAD: "View a color-coded heatmap of student scores"

**How JTBD connects to Risks & Challenges:** If a job is critical but you're uncertain about feasibility, it should appear in both sections — as a job in JTBD and as a risk in Risks & Challenges. This makes the connection between user needs and execution risks explicit.

**Example (instructor persona):**
> When an instructor wants to **assess applied learning through simulation**, they need to be able to:
> - Discover simulation content aligned to their course outcomes without leaving Canvas
> - Preview the student experience before assigning
> - Configure grading criteria that map simulation performance to their rubric
> - See student simulation results alongside traditional assessment results in one view

---

#### Success Signals (in "What Success Looks Like")

**Purpose**: How will we know we're heading in the right direction during POC/prototyping?

**Focus on validation signals:**
- Usability testing outcomes
- Qualitative feedback
- Stakeholder alignment
- Critical issues discovered

**Not adoption metrics.** This is before launch — you're validating the approach, not measuring results.

---

#### EAP: Learning Milestone

**Critical principle**: Focus on **actionable learnings**, not adoption metrics.

**Wrong:** "Whether instructors actually use simulations vs. continuing traditional methods" (measures outcomes)

**Right:** "How instructors discover simulations when they have real course context (what filters matter?)" / "Where they get stuck during configuration" / "What grading expectations partners don't meet" (reveals actionable insights)

**Structure:**
1. **What do you want to learn**: Specific questions about workflow, friction, expectations, feasibility
2. **What needs to be in the EAP**: Minimum capabilities to surface those learnings
3. **What customers/segments**: Mix that reveals different friction points

**EAP customer insight**: Include institutions that **want** to use the feature but haven't due to current barriers — they reveal different friction than those with existing workarounds.

---

#### GA: GTM Milestone

**Critical principle**: Focus on **lasting value metrics**, not vanity metrics.

**Metrics that prove lasting value:**
- Sustained usage (not trial)
- Satisfaction/NPS
- Retention impact
- Problem resolution (pain point drops in feedback)
- Business viability (revenue)

**Metrics that don't prove lasting value:**
- Initial adoption ("% who tried it once")
- Supply-side metrics ("number of partners integrated")
- Activity without context ("assessments created")

Keep the table focused: 5-7 metrics that genuinely answer "did this bet pay off?"

---

#### Guardrails & Constraints

**Purpose**: Prevent scope creep by defining clear boundaries. Guardrails are different from scope: scope says what you're building, guardrails say what you're NOT building and what rules apply.

**Two subsections:**
1. **For This Phase** (what's in scope and what rules apply)
2. **For Future Phases** (what's explicitly deferred and why)

**The distinction:** Scope = "we're building assessment marketplace integration." Guardrails = "we design for multiple content types, not just simulations" and "designer determines prototype fidelity needed to tell a coherent story."

**Make constraints actually constrain.** Don't hedge with "assume X but question if needed." Either something is a constraint or it's an exploration area.

- **Wrong**: "Assume Learnosity CQT is the integration method, but question this if UX demands it"
- **Right**: "Learnosity CQT is the integration method (constraint)"
- **Wrong**: "Keep the prototype lightweight"
- **Right**: "Designer determines what's needed to tell a coherent story" (lets scope speak for itself)

**When guardrails create false constraints:** If a guardrail prevents the triad from solving the problem effectively, it's a false constraint. Test: "If we removed this guardrail, would the solution space improve dramatically?" If yes, reconsider.

**Let the designer determine scope**: Instead of prescribing "lightweight" or "minimal," frame as "designer determines what's needed to tell a coherent story." Reference existing work when available.

---

#### Risks & Challenges

**Categories:** Technical, Adoption, Partnership, Dependency (cross-team), Market.

**Be specific:** "Learnosity CQT may not support partial credit" is better than "technical integration might be complex."

---

#### Open Questions & Decisions

**This is a working log.** Table with Question | Decision | Date.

**What belongs here:** Technical approach decisions, UX patterns needing validation, business model choices deferred, integration points with unclear solutions.

**Update the "Decision" column as the brief iterates** — this shows progress.

---

#### Documents & Resources

**Structure:** Group by category (Discovery & Research, Strategic Context, Market Intelligence, Technical References).

**Format:** Simple bulleted lists with document names and locations. Do NOT add extensive annotations or summaries.

---

### Brief Validation Checklist

Run this checklist before presenting ANY draft section. Each item has a concrete test.

#### Template & Voice

| Check | Test | Pass | Fail |
|-------|------|------|------|
| Problem & Opportunity is narrative | Is it one flowing paragraph, 150-250 words? No subheadings? | Single paragraph, natural story flow | Multiple paragraphs, headers, or bullet lists → rewrite as narrative |
| Strategic Anchors are paragraphs | Are they 3-4 narrative paragraphs answering the four anchor questions? | Flowing paragraphs, not lists | Bullet points under each question → rewrite as prose |
| Voice check | Read aloud: confident and declarative? No hedge words? | Matches persona — explaining to peers | Corporate memo tone → rewrite |
| "Just enough structure" test | If the triad read this, could they start working? Are they overwhelmed? | Clear enough to act on, concise enough to absorb | Too vague to act on → add specifics. Too detailed → cut. |

#### Content Quality

| Check | Test | Pass | Fail |
|-------|------|------|------|
| Strategic alignment is realistic | For each strategic connection: can you explain the mechanism in one sentence? | Every connection has a specific "because" | Any connection that requires stretching → downgrade to "supports" or "modest but real" |
| EAP = actionable insights | Do EAP learning goals reveal HOW and WHERE, not WHETHER? | Questions about friction, discovery, workflow | "Whether users adopt" → reframe as "Where users get stuck" |
| GA = lasting value | Do GA metrics prove the bet paid off? Not just activity? | Sustained usage, satisfaction, retention, revenue | "% who tried it" or supply-side metrics → replace with value metrics |
| Guardrails actually constrain | Is every constraint a real boundary, or hedged with escape clauses? | Hard constraints stated as facts | "Assume X unless Y" → either constrain or make it an open question |
| JTBD scope is clear | Do jobs define what users need to accomplish, not features to build? | Outcome-focused capabilities | Feature descriptions ("click button to...") → reframe as outcomes |

#### Collaboration Readiness

| Check | Test | Pass | Fail |
|-------|------|------|------|
| Open questions are specific | Could someone investigate each question independently? | Each question has clear scope and implied method | Vague questions ("How should we handle X?") → sharpen |
| Triad can start | After reading, does each role know what to investigate first? | PM sees the opportunity, Design sees the problem space, Eng sees the constraints | Any role would say "so what do I do?" → add clarity |
| No prescribed solutions | Are problems framed, or are you telling triads what to build? | Problem space defined, solution space open | Implementation details in JTBD or Problem section → remove |

---

### Brief Common Pitfalls

**1. Over-Structuring Narrative Sections**
Adding headers, subheadings, and bullet points where the template shows flowing paragraphs. Write one narrative paragraph that tells the story naturally.

**2. Stretching Strategic Alignment**
Claiming an initiative "advances" or "proves" strategic principles when the connection is weak. **Test:** Can you explain in 1-2 sentences exactly how this initiative advances the principle? If not, scale back to "supports," "contributes to," or acknowledge impact is "modest but real."

**3. Verbosity Without Purpose**
Adding context, explanation, or justification that doesn't help the triad align. Problem & Opportunity exceeding 300 words is a red flag. Ask: "Does this help align, or am I over-explaining?"

**4. Measuring Activity Instead of Learning (EAP)**
EAP learning goals that are adoption metrics. "Whether they use it" measures outcomes. "Where they get stuck" reveals actionable insights.

**5. Vanity Metrics Instead of Value (GA)**
GA metrics including initial trial, supply-side indicators, or activity without proof of value.

**6. Hedged Constraints**
Guardrails that aren't actually constraints. Either make it a constraint or an exploration area.

**7. Prescribing Solutions**
Telling designers or engineers how to solve problems rather than framing the problem space. The brief frames problems. The triad solves them.

**8. Insufficient Collaboration Readiness**
The brief looks complete but the triad can't actually start working. Common causes:
- Open questions are too vague for anyone to investigate ("How should we handle grading?" vs. "Does Learnosity CQT support partial credit scoring, and if not, what's the workaround?")
- Missing context on what each role should focus on first (PM: validate market opportunity; Design: map instructor workflow; Engineering: assess integration feasibility)
- Prescribed solutions buried in problem framing (JTBD that describe features, not outcomes)

**Test:** After drafting, ask for each triad role: "If I were this person, would I know what to do next Monday morning?" If the answer is vague for any role, add specificity.

---

### Brief Length Guidelines

**Brief sections:**
- Initiative Hypothesis: One sentence
- Problem & Opportunity: 150-250 words, one narrative paragraph

**Comprehensive sections:**
- Jobs to be Done: Detail helps define scope through user needs
- Risks & Challenges: Surfacing known issues is valuable
- Open Questions: Working log should capture all ambiguities

**Contextual balance:**
- Strategic Anchors: 300-400 words, 3-4 narrative paragraphs
- Success metrics: Enough to know what success looks like, not exhaustive
- Guardrails: Clear boundaries without excessive detail
- EAP/GA: Follow template structure (paragraph + table typically sufficient)

---

### Brief Edge Cases

#### When to Call Something "Lightweight" vs. Letting Scope Speak

Terms like "lightweight POC" can be confusing when the scope actually includes multiple priorities, cross-product integration, and substantial validation.

**Resolution pattern:**
- If scope is genuinely minimal (single workflow, single product, concept validation only) → "lightweight POC" is accurate
- If scope has multiple priorities or substantial validation needs → either remove "lightweight" and say "proof-of-concept focused on [specific goal]" or frame as "designer determines what's needed to tell a coherent story"

**Key principle**: Don't let the word "lightweight" create false constraints. Let the scope speak for itself.

#### Platform and Infrastructure Initiatives

Platform and infrastructure ideas (domain: platform or cross-product) create specific challenges for both formats because their value is indirect — they enable capabilities rather than delivering user-facing outcomes directly.

**Strategy Document considerations:**
- The diagnosis must explain why the platform gap matters to end users, not just to engineers
- Strategic priorities should be framed as capabilities that enable multiple product teams, not as technical projects
- Success measures need both platform metrics (adoption, reuse, velocity) AND downstream user metrics (the things the platform enables)
- "How We Might Approach This" should explain the platform pattern, not just the first implementation

**Product Brief considerations:**
- Problem & Opportunity must connect infrastructure needs to user pain points: "Instructors can't [outcome] because [platform gap] forces [workaround]"
- JTBD should include both direct users (developers, platform team) AND downstream users (teachers, students) affected by the capability
- Success signals must include downstream impact, not just platform adoption: "Teams build on this" is necessary but not sufficient — "and users experience [improvement]" is the real success
- Guardrails should clarify: are you building the platform capability, or also the first product implementation? These are different scopes.

**Common mistake:** Writing platform initiatives in pure technical language. The document still needs to speak in business-outcome terms — the audience is VPs and ELT, not engineers. "Unified assessment data layer" → "One view of student mastery across all assessment tools, enabling instructors to see the full picture without switching between three products."

---

### Appendix: Brief Conversation Examples

#### Example 1: Problem & Opportunity Evolution

**First attempt** (~500 words, multiple paragraphs with structure):
> ### The Problem
> K-12 and Higher Ed instructors across STEM, nursing... [extensive detail]
>
> ### The Opportunity
> When we solve this... [separate paragraph]

**Feedback**: "This is shorter, but shorter isn't specifically what I asked for. Read the example and understand if you're embodying the intent."

**Final version** (~200 words, one flowing paragraph):
> Instructors in STEM, nursing, business, and career-technical programs want to assess students through simulations—virtual labs, patient care scenarios, business cases—but integrating simulation content into Canvas assessments requires leaving the platform...

**Lesson**: Template intent is narrative flow, not structured argument.

#### Example 2: Strategic Anchors — Design Goals

**First attempt** (overstated):
> This initiative advances our design goals around "Assessment as Platform Signal"... It proves "Intent Recognition & Assessment Creation"...

**Feedback**: "I feel you are reaching and what you wrote is a stretch. Make it realistic."

**Final version** (realistic):
> For design goals, this supports contextual workflow integration—making third-party content feel native rather than bolted on. The impact is modest but real: one less fragmented experience.

**Lesson**: Be honest about modest impact rather than stretching connections.

#### Example 3: EAP Learning Goals

**First attempt** (adoption metrics): "Whether instructors actually discover and use simulations..."

**Final version** (actionable insights): "How instructors discover simulations when they have real course context (what filters and metadata matter most?); where they get stuck or confused during configuration..."

**Lesson**: EAP should reveal actionable insights, not just measure what happened.

#### Example 4: GA Metrics

**First attempt** (vanity): "% of institutions with at least one simulation-based assessment created"

**Final version** (value-focused): "Simulation-based assessment creation rate (sustained usage); Instructor NPS for simulation workflow; Retention impact..."

**Lesson**: Focus GA metrics on proving the bet paid off (sustained value), not measuring activity.

#### Example 5: Guardrails Contradiction

**First attempt** (contradictory): "Do not prescribe specific content partners" + "validate with PhET, Labster, vSim"

**Final version** (resolved): "Design for simulation types that scale across partnerships, not bespoke solutions. We'll validate with specific partners but the design should accommodate diverse content."

**Lesson**: Resolve contradictions by clarifying: design generically, validate specifically.

---

## Template Modifications / Intellectual Heritage

This approach synthesizes:
- **Rumelt** (Strategy Kernel: Diagnosis + Guiding Policy + Coherent Actions)
- **Perri** (Outcomes over outputs, deployable decision-making framework)
- **Torres** (Continuous discovery, opportunity mapping, assumption testing)
- **Reddit practitioner** (Research → Validate → North Star → Levers → Application)

With additional emphasis on:
- **Strategic Leverage** thinking (multiplicative advantage, platform effects)
- **Cross-disciplinary integration** (PM/Design/Engineering perspectives)
- **Hybrid aspirational/realistic tone** (stretch thinking meets constraints)
- **Platform/ecosystem thinking** (developer experience, adoption, reusability)
- **Quality & experience outcomes** (design quality, sentiment, usability alongside business metrics)
- **"Just enough structure"** mandate for briefs (frame problems, don't prescribe solutions)

---

## References

**Methodology sources:**
- [Good Strategy Bad Strategy Summary (Lenny's Newsletter)](https://www.lennysnewsletter.com/p/good-strategy-bad-strategy-richard) — Rumelt's Strategy Kernel
- [Good Strategy Bad Strategy Notes (Jeff Zych)](https://jlzych.com/2018/06/27/notes-from-good-strategy-bad-strategy/) — Rumelt detailed notes
- [Escaping the Build Trap Summary (Medium)](https://t-ziegelbecker.medium.com/a-summary-of-escaping-the-build-trap-by-melissa-perri-d247f943a7b3) — Perri's outcomes-over-outputs framework
- [Teresa Torres Continuous Discovery Framework (Userpilot)](https://userpilot.com/blog/continuous-discovery-framework-teresa-torres/) — Opportunity mapping and assumption testing
- Reddit r/ProductManagement: Product Strategy Advice — Practitioner 6-step process (archived from Bear)
