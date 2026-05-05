---
title: Agent Handoffs
type: methodology
status: active
tags:
  - mindrails
  - superbrain
  - handoffs
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
---

# Agent Handoffs

Handoffs verhindern, dass Teil-Gehirne aneinander vorbeiarbeiten.

## Standard-Handoff

```md
## Auftrag

## Kontext

## Bereits geprüft

## Nicht anfassen

## Gewünschter Output

## Belegstandard
```

## Debugger -> Engineer

- Symptom.
- Repro oder Beleg.
- Root-Cause.
- Betroffene Dateien/Module.
- Ähnliche Risikostellen.
- Test, der den Bug pinnen sollte.

## Engineer -> Coder

- Zielverhalten.
- Patch-Korridor.
- Betroffene Dateien.
- Invarianten.
- Tests.
- Rollback-/Migration-Hinweise.

## Coder -> Reviewer

- Diff-Zusammenfassung.
- Warum minimal.
- Tests gelaufen.
- Nicht getestete Risiken.
- Stellen, die besonders kritisch sind.

## Reviewer -> Coder

- Findings nach Severity.
- Pro Finding: Datei/Zeile, Schadenspfad, Repro, konkrete Fix-Richtung.
- Keine Stilwünsche als Bugs tarnen.

## Business-Coach -> AI-Welt-Coach

- Entscheidung oder These.
- Zielkunde.
- Metrik.
- Marktannahmen.
- Welche AI-/Regel-/Kosten-Signale relevant sind.

## AI-Welt-Coach -> Forecast Ledger

- Präzise Aussage.
- Wahrscheinlichkeit.
- Deadline.
- Base Rate oder Vergleich.
- Quelle.
- Was würde die Prognose falsifizieren?

