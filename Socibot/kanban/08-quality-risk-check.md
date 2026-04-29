---
id: 8
status: backlog
priority: P0
blocked_by: []
tags:
  - socibot
  - quality
  - persona-a
  - compliance
  - dod-blocker
created: 2026-04-29
---

# Risk-Check für Beratungsbranche (HWG / UWG / Anwalts-Werbung)

Pre-Publish-Pass: jeder Post wird gegen branchen-spezifische Verbots-Listen + Heilversprechen-Filter + Werbe-Recht-Checks gefahren. Bei Treffer → Hard-Reject + User-Hinweis warum.

## Warum P0 / DoD-Blocker für Persona A
Bei Anwalt/Arzt/Heilpraktiker/Coach mit Heilversprechen-Bereich ist das KEIN Quality-Bonus, sondern **Pflicht**. Sonst Abmahnungs-Gefahr und Customer-Verlust am Tag 1. Dealbreaker für Persona A.

## Acceptance
- [ ] `dashboard/services/compliance_checker.py`
- [ ] Branchen-spezifische Regel-JSONs:
  - `compliance/anwalt.json` — UWG, BORA-§7 Werbeverbote, Erfolgsversprechen
  - `compliance/arzt.json` — HWG, Heilversprechen-Filter, BÄK-Werberichtlinien
  - `compliance/heilpraktiker.json` — HWG verschärft
  - `compliance/coach.json` — Heilversprechen-Filter (oft falsch genutzt von Coaches)
  - `compliance/steuerberater.json` — BOStB Werbeverbote
- [ ] Pipeline: nach Generation → vor Approval-Anzeige → Compliance-Pass
- [ ] Bei Treffer: Hard-Reject + User sieht "Warum nicht: HWG §3 verbietet 'heilt' bei Heilmitteln" + Link auf Erklärung
- [ ] User kann Override mit Disclaimer "Auf eigenes Risiko, ich habe das geprüft"
- [ ] Audit-Log aller Override-Entscheidungen für DSGVO/Compliance-Doku
