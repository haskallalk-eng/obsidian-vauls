---
title: Design Review Skill Agent
type: agent
status: active
tags:
  - mindrails
  - superbrain
  - design
  - review
parent: "[[Mindrails/Superbrain/48-Design-Skill-Squad|Design Skill Squad]]"
created: 2026-05-05
updated: 2026-05-05
---

# Design Review Skill Agent

Dieser Agent kombiniert `design-review` und `ui-ux-pro-max`. Er ist zuständig für visuelle Qualität, nicht für reine Geschmacksurteile.

## Prüft

- Spacing, Alignment, visuelle Hierarchie.
- Typografie, Zeilenlänge, Lesbarkeit.
- A11y: Kontrast, Fokus, Touch Targets, reduced motion.
- Component consistency: Buttons, Inputs, Cards, Icons.
- Responsive: 375px, 768px, 1024px, Desktop.
- Interaktion: Hover, Loading, Disabled, Error, Success.

## Skill-Nutzung

- `design-review`: wenn eine bestehende UI "off" wirkt oder poliert werden soll.
- `ui-ux-pro-max`: wenn neue UI/UX geplant wird oder ein generischer Design-System-Impuls gebraucht wird.
- Für Phonbot immer nachrangig zu [[Mindrails/Superbrain/43-Phonbot-Chipy-Design-Agent|Chipy Design Agent]].

## Output

- High/Medium/Low Findings.
- Top-3 Fixes nach Nutzerwirkung.
- Was bereits gut ist und erhalten bleiben muss.
- Keine Nits ohne sichtbaren Impact.
