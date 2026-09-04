---
updated: '2026-05-21'
---
# Persona — superseded by the lexi-persona skill

The persona guide that this sample once templated is no longer a standalone file. Lexi's authorial voice is now the **`lexi-persona`** Agent Skill — a composable navigator handling generate, refine, and review across strategy documents, presentations, weekly updates, and Slack/email.

The skill ships as `lexi-persona` inside the operator's private `operator` Claude Code plugin (installed from her private companion repo, no longer in the public dotty repo) and is the single source of truth for voice. Project skills that still reference a local `persona.md` are pending repoint to invoke the skill directly.
