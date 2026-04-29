---
id: 7
status: backlog
priority: P1
blocked_by: []
tags:
  - socibot
  - quality
  - context-aware
created: 2026-04-29
---

# Trend + Saison + Datum-Kontext im Prompt

System injiziert in Generation-Prompt: aktuelles Datum, Wochentag, Quartalsphase, deutsche Feiertage, branchen-spezifische Saisonalität (Steuerberater: vor Steuererklärungs-Frist, Anwalt: vor Gerichts-Sommerpause, Coach: vor Jahreswende).

## Warum P1
Posts wirken zeitnah, nicht generisch. Implementations-Aufwand niedrig — keine externe API nötig, nur Datum + Lookup-Tabelle.

## Acceptance
- [ ] `dashboard/services/temporal_context.py` mit Branchen-Kalender-JSON
- [ ] Kalender-JSON pro Persona-A-Branche (Anwalt, Steuerberater, Coach, Therapeut, Heilpraktiker)
- [ ] `prompt_builder.build_temporal_section()` injiziert Kontext
- [ ] Optional: Trend-Hashtag-Snapshot (manuell aktualisiert wöchentlich, kein Live-Scrape — DSGVO-Pflicht)
