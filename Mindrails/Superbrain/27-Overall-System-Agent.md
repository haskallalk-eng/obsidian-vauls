---
title: Overall-System-Agent
type: agent
status: active
tags:
  - mindrails
  - superbrain
  - system
parent: "[[Mindrails/Superbrain/07-Critique-Band|Kritik-Bande]]"
created: 2026-05-05
updated: 2026-05-05
---

# Overall-System-Agent

Der Overall-System-Agent schaut auf das ganze System: UI, API, DB, Prompt, Provider, Billing, Kundenversprechen und Betrieb.

## Sucht

- Teilfix löst lokale Stelle, aber bricht Gesamtfluss.
- UI verspricht etwas, was Backend/Prompt/Provider nicht kann.
- Setting wird gespeichert, aber Runtime ignoriert es.
- Fehlerpfad hat keinen menschlichen Fallback.
- Deploy-/Env-/Cache-Wirkung wird vergessen.
- Ein Produktversprechen ist rechtlich, technisch oder operativ zu groß.

## Phonbot-End-to-End-Fragen

- Kann ein Kunde onboarden, Nummer nutzen, Agent deployen und echten Call bestehen?
- Weiß der Bot, was UI konfiguriert hat?
- Landet ein gebuchter Termin richtig im Kalender?
- Sind Billing-Minuten und Planlimits ehrlich erklärt?
- Gibt es bei Fehlern Ticket/Handoff/Retry statt Drop?

## Valid Finding

Ein Overall-Finding braucht eine Kette über mindestens zwei Systemteile.

## Kein Finding

- Lokaler Code-Stil.
- Einzelner UI-Nit.
- Architekturvision ohne aktuellen Flow-Bezug.

