---
id: 4
status: backlog
priority: P0
blocked_by: []
tags:
  - socibot
  - quality
  - top-roi
created: 2026-04-29
---

# Hook + Body als getrennte Generation-Passes

Aktuell: ein Generation-Call generiert Hook + Body zusammen. Hook ist Nebenprodukt.
Neu: Pass 1 generiert 10 Hook-Optionen → Self-Critique pickt die 3 stärksten → Pass 2 baut Body um den gewählten Hook.

## Warum P0
Hooks sind 80% der Social-Engagement. Separater Hook-Pass produziert messbar bessere Hooks (Industry-Pattern aus Taplio, Magnific).

## Acceptance
- [ ] `prompt_builder` split in `build_hook_prompt` + `build_body_prompt`
- [ ] Pipeline: 10 Hooks → 3 Top-Hooks (per Self-Critique mit expliziten Hook-Quality-Kriterien) → 3 Bodies → User sieht 3 Variants
- [ ] Hook-Strategien-Pool konfigurierbar (siehe Diversitäts-Slider in DoD-Block 6)
- [ ] Cost-Hint: ~2 zusätzliche Calls pro Post → Premium-Tier-Pflicht
