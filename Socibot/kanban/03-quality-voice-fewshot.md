---
id: 3
status: backlog
priority: P0
blocked_by: []
tags:
  - socibot
  - quality
  - persona-a
  - top-roi
created: 2026-04-29
---

# Voice-Few-Shot aus echten User-Posts

User pasted im Onboarding 10-20 "Gold-Standard"-Posts (eigene oder fremde Beispiele die ihm gefallen). Diese landen als **konkrete Reference-Examples in JEDEM Generation-Prompt**, nicht als abstrakte Beschreibung.

## Warum P0
Größter Quality-Sprung pro Aufwand. Examples > Descriptions ist eines der robustesten LLM-Patterns. Jasper macht's mit Brand-Voice, viele Konkurrenten nicht.

## Acceptance
- [ ] Onboarding-Step "Voice-Sample" — Paste-Area für 5-20 Posts, optional URL-Scrape
- [ ] `client/voice_samples.json` mit Encrypted-Storage falls personenbezogen
- [ ] `prompt_builder` injiziert die Top-5 Beispiele als Few-Shot-Examples in Generation-Prompt
- [ ] Editierbar nach Onboarding (Settings → Voice-Samples)
- [ ] Weighting: User kann pro Sample ⭐⭐⭐ vergeben → höher gewichtete kommen häufiger als Few-Shot
- [ ] Vergleichs-A/B: Posts mit Few-Shot vs. ohne, Quality-Score messbar besser

## Persona-A-Spezifik
Beratungsbranche hat sehr individuelle Sprache (autoritär vs. nahbar) — Examples > Description gilt hier doppelt.
