---
id: 5
status: backlog
priority: P0
blocked_by: []
tags:
  - socibot
  - quality
  - learning-loop
created: 2026-04-29
---

# Reject-Reason-Mining → nächste Generation konditionieren

Jede Reject-Reason wird in `client/post_feedback.json` gespeichert. Nächster Generation-Prompt enthält:
> "User hat letzte 5 Posts mit folgenden Gründen abgelehnt: [zu salesy, zu lang, kein konkretes Beispiel]. Vermeide diese Muster."

## Warum P0
Selbstverbessernde Schleife ohne Manual-Tuning. Je mehr User reject, desto besser wird das System. Kostet fast nichts (paar Tokens extra im Prompt).

## Acceptance
- [ ] `client/post_feedback.json` Schema: `{user_id, post_id, action: "approve|reject", reason, generated_at, hook_strategy}`
- [ ] Reject-Dialog: Reason-Picker (zu salesy / zu lang / nicht mein Tone / generic / faktisch falsch / sonstiges + Free-Text)
- [ ] `prompt_builder.build_avoid_section()` zieht letzte 5-10 Rejects mit Reasons
- [ ] UI: "Was wir aus deinen Rejects gelernt haben" als Live-Display in Settings
- [ ] Override: User kann Pattern explizit löschen ("vergessen")
