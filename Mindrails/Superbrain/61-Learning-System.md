---
title: Superbrain Learning System
type: learning-system
status: active
tags:
  - mindrails
  - superbrain
  - learning
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
---

# Learning System

Das Superbrain lernt nicht automatisch wie ein trainiertes Modell. Es lernt über strukturiertes Gedächtnis, Scorecards, Auswertung und wiederverwendbare Lessons.

## Lernarten

| Ebene | Frage | Beispiel |
|---|---|---|
| Single-Loop | War die Aktion falsch? | Test fehlte -> Test ergänzen. |
| Double-Loop | War die Annahme falsch? | "UI speichert nicht" war eigentlich API-500 wegen DB-Schema. |
| Workflow-Loop | War der Prozess falsch? | Erst Prompt geändert, aber Cache/Retell-Deploy-Wirkung nicht geprüft -> neues Decision Gate. |

## Gedächtnistypen

| Gedächtnis | Inhalt | Speicherort |
|---|---|---|
| Case Memory | konkrete Bugs, Kundenfälle, Incidents, Fixes | Daily, ZuTun, Review-Notes |
| Pattern Memory | wiederkehrende Fehlerklassen | Agent-Dateien und [[Mindrails/Superbrain/62-Agent-Scorecards|Agent Scorecards]] |
| Decision Memory | getroffene Entscheidungen, verworfene Optionen | Decision Records / Daily |
| Forecast Memory | Prognosen mit Deadline und Ergebnis | [[Mindrails/Superbrain/50-Forecast-Ledger|Forecast Ledger]] |
| Source Memory | belastbare Quellen und Vertrauensniveau | [[Mindrails/Superbrain/90-Research-Sources|Research Sources]] |
| Customer Reality Memory | echte Kundenwünsche, Beschwerden, Kaufgründe | [[Phonbot/ZuTun|Phonbot ZuTun]], Daily, Kunden-Notes |

## Lernzyklus pro Task

1. Before: passende Agent-Scorecard lesen.
2. During: Belege sammeln, nicht nur Schlussfolgerungen.
3. After: Outcome einordnen: funktioniert, teilweise, falsch, unklar.
4. Lesson: maximal 1-3 wiederverwendbare Regeln notieren.
5. Update: Scorecard, Forecast, Decision Gate oder Workflow anpassen.
6. Prune: schwache Lessons löschen oder mit stärkeren Cases zusammenführen.

## Lesson-Format

```md
### Lesson
- Datum:
- Agent:
- Kontext:
- Was war die alte Annahme?
- Was hat die Realität gezeigt?
- Neue Regel:
- Beleg:
- Gilt für:
- Confidence:
- Revisit:
```

## Qualitätsregeln fürs Lernen

- Keine Lesson ohne konkreten Fall oder Quelle.
- Eine Lesson muss eine zukünftige Entscheidung verändern können.
- Wenn eine Lesson nur "besser aufpassen" sagt, ist sie zu schwach.
- Wenn zwei Lessons widersprechen, entscheidet die neuere/besser belegte oder beide bleiben mit Bedingungen stehen.
- Forecasts müssen ausgewertet werden, sonst sind sie nur Meinung mit Prozentzeichen.

## Monatlicher Learning Review

- Welche 3 Lessons wurden mehrfach bestätigt?
- Welche 3 Agenten haben Scorecard-Schwächen?
- Welche Forecasts sind fällig?
- Welche Quellen sind veraltet?
- Welche Workflows erzeugen noch Blind Spots?

