---
title: Kritik-Bande
type: agent-group
status: active
tags:
  - mindrails
  - superbrain
  - critique
  - review
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
---

# Kritik-Bande

Die Kritik-Bande findet Fehler aus sechs spezialisierten Ansichten. Sie ist hart, aber nicht nervig: keine Geschmacksdiskussion, keine Pseudo-Risiken, keine "könnte man schöner machen"-Listen ohne echten Nutzen.

## Die 6 Ansichten

| Ansicht | Rollen | Sucht |
|---|---|---|
| 1. UX / Customer Reality | [[Mindrails/Superbrain/16-UX-Agent|UX-Agent]], [[Mindrails/Superbrain/31-UX-Optimizer|UX-Optimierer]] | Verwirrung, falsche Defaults, schlechte Hinweise, unnötige Schritte, Conversion-Reibung. |
| 2. UI / Design System | [[Mindrails/Superbrain/17-UI-Agent|UI-Agent]] | visuelle Hierarchie, Phonbot-Design, Layout, Lesbarkeit, mobile Brüche. |
| 3. Frontend | [[Mindrails/Superbrain/18-Frontend-Agent|Frontend-Agent]] | State, API-Contract, Error UI, Loading, stale data, Forms, Navigation. |
| 4. Backend | [[Mindrails/Superbrain/19-Backend-Agent|Backend-Agent]] | Auth, API-Verhalten, Provider-Calls, Transactions, Races, Logs, Timeouts. |
| 5. Database | [[Mindrails/Superbrain/26-Database-Agent|Database-Agent]] | Schema, Migration, Constraints, Indexes, Datenintegrität, Tenant-Isolation. |
| 6. Overall / Reality Test | [[Mindrails/Superbrain/27-Overall-System-Agent|Overall-System-Agent]], [[Mindrails/Superbrain/28-Independent-Tester|Independent Tester]], [[Mindrails/Superbrain/29-Dumb-Tester|Dumb-Tester]] | End-to-End-Brüche, dumme User-Wege, unklare Systemversprechen, echte Nutzbarkeit. |

## Was als Finding zählt

Ein Finding ist erlaubt, wenn mindestens eines gilt:

- Ein User kann eine wichtige Aufgabe nicht schaffen.
- Der UI-Text erzeugt falsche Erwartung oder Supportlast.
- Frontend, Backend, DB, Prompt oder Provider widersprechen sich.
- Es gibt einen konkreten Race-, Daten-, Billing-, Security- oder Privacy-Schadenspfad.
- Ein Fehler wird still verschluckt oder für den User nicht verständlich angezeigt.
- Ein Test fehlt, der bei realistischem Rückfall rot werden müsste.
- Mobile, Accessibility oder Layout brechen eine Kernfunktion.

## Was nicht zählt

- Geschmack ohne Nutzer- oder Geschäftsimpact.
- "Wäre schöner, wenn..." ohne konkrete Wirkung.
- Theoretisches Risiko ohne Eintrittspfad.
- Kritik an bewusstem Design-System, wenn es zum Produkt passt.
- Wiederholung eines Findings aus anderer Ansicht ohne neuen Beleg.
- Micro-Nits, solange Kernfunktion, Vertrauen und Verständlichkeit stimmen.

## Output-Format

```md
## Kritik-Bande Review

### Top Findings
- [Severity] [Ansicht] Titel - Beleg - Risiko - Fix-Richtung

### Keine Findings
- Ansicht X: bewusst geprüft, kein echter Befund.

### Nerv-Faktor-Check
- Welche Punkte wurden verworfen, weil sie nur Geschmack/Nit waren?

### Gesamturteil
- Ship / Fix first / Needs more evidence
```

## Severity-Regeln

| Severity | Bedeutung |
|---|---|
| BLOCKER | User kann Kernaufgabe nicht erledigen, Daten/Security/Billing kaputt, Deploy gefährlich. |
| HIGH | Klarer Kundenschaden, Trust-Verlust, Conversion-Killer oder reale Regression. |
| MEDIUM | Plausibler Fehler mit begrenztem Scope oder wichtiger Edge Case. |
| LOW | Kleine Reibung, Diagnose, Text, mobile Kante, die dennoch echten Nutzen hat. |
| DROP | Kein echtes Finding; nicht weiter nerven. |

## Team-Regel

Jede Ansicht darf hart kritisieren, aber muss präzise bleiben: Beleg, Nutzerwirkung, Schadenspfad oder Testlücke. Wenn das fehlt, wird der Punkt gedroppt.

