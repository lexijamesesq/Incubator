# Query

Read-only. Answers a question against the database for the configured domain. Never writes — never invokes `write-finding`, `write-findings`, or `upsert-competitor`, and never applies the Write Protocol section of `write-gate.md` (its Insufficiency & Degradation section still applies — see below).

## The Discriminator

Apply this test verbatim:

> Would a correct answer contain any sentence whose truth rests on a relationship between rows, rather than on the content of one row? Yes → analyze. No → query.

In this skill's collapsed command-pattern model, "analyze" is not a separate top-level command pattern — it's the relationship-question branch below, handled inside this same `query.md` playbook. "Yes" routes there; "No" routes to the simple-lookup branch.

**Simple lookup** (the "No" branch) — the question is about ONE named competitor, answerable in a single round-trip. Route to `lookup-competitor` (find/confirm the competitor) and/or `query-competitor` (the deep-dive). One command, maybe two if you need the ID first — never a third.

Examples: "What tier is [competitor]?" "What's [competitor]'s pricing model?"

**Relationship question** (the "Yes" branch) — the question requires reasoning ACROSS competitors, capabilities, or findings: a comparison, a gap, a pattern that only shows up when you look at multiple rows together. Route to `query-landscape` (competitors + findings for a capability set) and/or `query-gaps` (which competitor/capability pairs have no findings). Your final answer STATES the relationship — never just paste the raw query output back at the user.

Examples: "Which competitors cover [capability] but have no [capability] findings?" "How does [competitor A]'s positioning compare to [competitor B]'s?"

**Re-routing mid-answer.** If you start down the simple-lookup branch and discover the honest answer requires deriving a claim across rows (a comparison, a synthesized pattern) rather than just returning a fact from one competitor's profile — stop, don't force the single-lookup shape. Re-route to the relationship-question branch and run the right command instead. A derived claim never comes out of a simple-lookup round-trip.

## Command Reference

| Command | When |
|---|---|
| `lookup-competitor` | Resolve a name to an ID, or confirm a competitor exists, before a deep-dive. |
| `query-competitor` | Full profile + linked findings for one named competitor. |
| `query-landscape` | Competitors + findings for a given capability set — the landscape view. |
| `query-gaps` | Which competitor/capability pairs have zero findings — the gap view. |

## Insufficiency

If the database can't answer — no finding, no competitor row, no capability tag covers what's asked — say so and name what's specifically missing. See `write-gate.md` § Insufficiency & Degradation for the full principle; it applies here even though `query` never writes.

## Never

- Fan out into `query-landscape`/`query-gaps` for what's actually a single-entity question — that's the discriminator's most common failure mode.
- Return raw rows with no relationship stated when the question asked for a comparison.
- Write anything. If the question turns out to need new information the database doesn't have, that's a `research` ask, not a `query` — hand it back to the translation layer rather than trying to answer from thin air.
