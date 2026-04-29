---
id: 10
status: backlog
priority: P1
blocked_by: []
tags:
  - socibot
  - quality
  - onboarding
created: 2026-04-29
---

# Anti-Pattern-Discovery im Onboarding

Onboarding-Schritt: "Pasted 5 Posts die du HASSEST + 1 Satz warum". System lernt explizit was zu vermeiden ist. Negativ-Constraints sind oft wertvoller als Positiv-Beispiele.

## Warum P1
Komplement zu #03 Voice-Few-Shot. Was nicht sein darf, ist oft klarer formulierbar als was sein soll. Geringer Implementation-Aufwand (UI + Prompt-Injection), hoher Quality-Effekt.

## Acceptance
- [ ] Onboarding-Step: 5 Anti-Beispiele + Reason-Free-Text
- [ ] `client/anti_patterns.json` mit Encrypted-Storage falls personenbezogen
- [ ] `prompt_builder.build_avoid_section()` zieht Anti-Patterns + Reasons
- [ ] Editierbar in Settings → Brand-Voice → "Was wir vermeiden"
