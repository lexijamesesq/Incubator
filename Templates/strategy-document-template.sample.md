# [Strategy Name]

*This document provides directional guidance across a domain, defining priorities and approaches that inform multiple initiatives over time. It establishes strategic context that Product Briefs reference as "Strategic Anchors," enabling teams to make aligned decisions independently without prescribing detailed solutions.*

**Last Updated:** [Date]
**Owner:** [Name, Role]
**Domain:** [Product area or cross-functional domain]

---

## Strategic Thesis

Establish the core strategic direction that inspires teams to think differently while directing them toward a clear outcome. Focus on market differentiation over competitor parity.

*Example:*

Platform-first route architecture enables teams to build domain-specific foraging intelligence on shared foundations rather than building inflexible, one-off cache maps. As the shared component library grows, development accelerates and consistency compounds — creating institutional knowledge and reusability that competitors starting from scratch cannot match.

---

## Problem & Opportunity

Diagnose the current state: what exists, what's broken, why now matters. Focus on root causes, not symptoms.

* What patterns are teams using today?
* What's broken or inefficient?
* What's the opportunity?
* Why does timing matter now?
* What patterns are we moving away from?

*Example:*

Today, each foraging team builds route maps independently, creating fragmented experiences that blend into the competitive landscape. Teams build generic data displays — cache lists, yield charts, territory filters — that look like every other foraging platform. Without coordinated direction, we're building commodity maps when we need differentiated intelligence. Competitors can easily copy individual features, and customers see route tools as interchangeable table stakes. With the unified sensor network providing a shared foundation, we now have the platform to build differentiated intelligence that competitors can't replicate. The opportunity is shifting from "maps that show data" to "maps that understand context and guide decisions" — the kind of intelligence that makes switching costs high and creates lasting competitive advantage.

---

## Strategic Priorities

Define 3-5 key priorities that guide decision-making in this domain.

### [Priority 1 Name]

**Opportunity**

[What's the problem or opportunity space? 1-2 paragraphs]

**Strategic Advantage** *(optional)*

[Why are we uniquely positioned to win here? What differentiation do we have? 1 paragraph]

**How We Might Approach This**

[Explore the solution landscape: What are the options? What are the trade-offs? What should teams consider? This is the strategic thinking space. 3-5 paragraphs]

*Example:*

### Tiered Customization Model

**Opportunity**

Competitors force users into binary choices: accept rigid route maps or build custom from scratch. This creates switching moments where customers evaluate alternatives. We can differentiate by offering graceful progression — users start with intelligent defaults, then customize without leaving our ecosystem. The opportunity is creating lock-in through flexibility: the more they invest in customization within our platform, the harder it becomes to switch to competitors' binary models.

**Strategic Advantage**

Unlike competitors who force "use our map" or "build your own," we can offer progression: start with intelligent defaults, customize through configuration, extend with community templates, or generate with AI. This flexibility becomes defensible when combined with our ecosystem and shared community templates — creating network effects competitors can't replicate.

**How We Might Approach This**

We have four potential paths, each with different differentiation value:

**In-house colony development** where colonies fork and maintain their own instances creates zero differentiation — they leave our ecosystem entirely. This is defensible only as enterprise tier escape valve, not a strategic path.

**Custom development partnerships** where we build bespoke maps for strategic accounts creates one-off differentiation but doesn't compound. Each custom build is sunk cost that competitors can copy. This is services revenue, not product differentiation.

**Community template distribution** creates network effects — power users share templates, others discover and adopt them, which attracts more template creators. This compounds over time and is hard for competitors to replicate without existing community. Requires us to build template packaging system, but leverages existing infrastructure.

**AI-generated maps** from natural language ("Show me caches near water sources with high yield") creates the highest differentiation — competitors would need both AI capability AND our data patterns to replicate. Significant investment and assumes we can generate reliable visualizations, but creates the most defensible moat.

The strategic choice: **Start with community templates (proven community model), design for AI generation (highest differentiation).** Templates create near-term lock-in through invested customization, while AI architecture positions us for long-term moat competitors can't cross.

### [Priority 2 Name]

**Opportunity**

[1-2 paragraphs]

**Strategic Advantage** *(optional)*

[1 paragraph]

**How We Might Approach This**

[3-5 paragraphs exploring options, trade-offs, strategic thinking]

---

## What Success Looks Like

How will we know this strategy is working? Focus on business outcomes and platform health.

*Example:*

**Switching costs increase measurably:** Customers invest in community templates and customizations within our ecosystem. Support sees questions shift from "how do I export this data to build my own map?" to "how do I extend this template?" Churn analysis shows foraging intelligence cited as reason for renewal.

**Competitive win/loss shifts:** Sales wins increase when map demos are part of sales cycle. Win/loss analysis shows "foraging intelligence" cited as decision factor. Competitors attempt to copy surface features but can't replicate community template library or contextual intelligence.

**Network effects compound:** Community foraging templates grow month-over-month. Power users contribute templates that others adopt. Template adoption creates flywheel — more users means more templates means more lock-in.

**Product becomes sticky:** Map usage correlates with retention. Customers using customized maps have measurably lower churn than those using defaults. Feature requests shift from "add basic charts" to "extend AI recommendations."

---

## Looking Beyond

Where could this strategy lead in the future? What opportunities exist beyond the immediate strategic priorities? This section captures forward-thinking possibilities that aren't core to the current strategy but represent natural evolution or compounding opportunities.

*Example:*

**AI-Powered Data Transformation**
Today's route builders force colonies to navigate complex UIs that never satisfy everyone. What if colonies could describe data transformations in natural language — "Calculate retrieval rate for caches placed near water vs. open terrain" or "Export foraging data grouped by season with yield percentages" — and get working transformations without building UI features? AI could handle data transformation, report generation, and export formatting based on examples and natural language descriptions, making data access truly flexible without building complicated report builders that become maintenance burdens.

---

## Boundaries & Dependencies

### Strategic Boundaries

*What this strategy covers / does NOT cover / connects to:*

*Example:*

**Covers:**
- Route mapping and foraging intelligence patterns across all foraging products
- Tiered customization approaches, component architecture, data visualization patterns

**Does NOT cover:**
- Cache construction or storage design (separate domain)
- Territory-specific boundary features (owned by separate team)
- Data pipeline architecture (see Data Platform Strategy)

**Related strategies:**
- Design Strategy - Applies platform principles specifically to foraging maps
- Product Strategy - Foraging maps implement broader platform-first approach

### Key Dependencies

*What must exist for this strategy to succeed:*

*Example:*

**Technical:** Platform foundation with stable APIs; shared component library infrastructure; community template packaging system
**Organizational:** Product teams must have autonomy to choose platform components; clear ownership model for cross-team contributions
**Resource:** Dedicated platform team to maintain shared components
**Knowledge:** Documentation showing how to use/extend components; design system with foraging map patterns

---

## Open Questions & References

### Open Questions

| Question / Assumption | Owner | Target Date |
|----------------------|-------|-------------|
|  |  |  |

### References

**Conversations:**
-

**Research & Data:**
-

**Related Documents:**
-
