---
id: 1
status: backlog
priority: Normal
blocked_by:
  - Socibot Test-Run
tags:
  - socibot
  - growth
  - utm
created: 2026-04-18
updated: 2026-04-21
---

# UTM-Funnel-Tracking für Social-Content

Socibot-Posts sollen zu trackbaren Klicks auf Landing-Pages führen, damit der Content-ROI messbar wird.

## Job Story
**When** Socibot Content postet, **I want to** Klicks mit UTM-Parametern trackbar machen, **so I can** Content-ROI pro Kampagne messen.

## Acceptance Criteria
- [ ] UTM-Scheme definieren (`?utm_source=socibot&utm_campaign=X&utm_content=Y`)
- [ ] Socibot Video-Engine Templates mit CTA-Link-Builder
- [ ] Analytics-Pipeline (extern oder Socibot-intern) zählt UTM-Klicks
- [ ] Dashboard: Source → Landing → Konversion

## Blocker
Socibot Test-Run steht noch aus ([[Socibot/Overview]]).

## Related
- [[Socibot/Overview]]
- [[Socibot/Kanban]]

## Narrative
- 2026-04-18: Erste Skizze.
- 2026-04-21: Socibot-interne Task, Ziel-Landing-Verweise entfernt (Cross-Projekt-Isolation im Vault — Produkte teilen im Vault nur die Mindrails-Klammer). (by @claude)
