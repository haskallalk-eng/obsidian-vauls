---
title: Agent Scorecards
type: scorecards
status: active
tags:
  - mindrails
  - superbrain
  - learning
  - agents
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
---

# Agent Scorecards

Scorecards machen die Teil-Gehirne nützlich. Jede Rolle hat Ziel, Messung, Lernsignal und Update-Regel.

## Globaler Score

| Feld | Bewertung |
|---|---|
| Outcome | Hat die Empfehlung/Arbeit real funktioniert? |
| Evidence | Waren Belege stark genug? |
| Specificity | War der Output konkret umsetzbar? |
| Risk Control | Wurden Nebenwirkungen erkannt? |
| Learning | Wurde eine wiederverwendbare Lesson erzeugt? |

Bewertung: 0 = fehlte, 1 = schwach, 2 = brauchbar, 3 = stark.

## Business-Coach

- Ziel: Fokus, Umsatzhebel und Moat klarer machen.
- Gute Outputs: klare Zielgruppe, Metrik, Experiment, Nicht-Ziel, Zahlungs-/Retention-Logik.
- Lernsignal: Experiment gewinnt/verliert, Kunde zahlt/nicht, Supportlast steigt/sinkt.
- Update-Regel: Wenn eine Business-Annahme 2x falsch war, Forecast oder Moat-These ändern.

## AI-Welt-Coach

- Ziel: AI-/Markt-Signale in Phonbot-Entscheidungen übersetzen.
- Gute Outputs: Signal, Quelle, Relevanz, Prognose, Experiment.
- Lernsignal: Forecast-Auswertung, Provider-Änderung, echte Call-Qualität, Kostenentwicklung.
- Update-Regel: Fällige Forecasts auswerten, Wahrscheinlichkeiten kalibrieren, alte Quellen markieren.

## Challenger-Council

- Ziel: blinde Flecken vor teuren Entscheidungen finden.
- Gute Outputs: konkrete Failure-Modes, Eintrittspfad, Gegenmaßnahme, Abbruchkriterium.
- Lernsignal: Welches Risiko trat wirklich ein? Welches war nur Lärm?
- Update-Regel: Pessimist wird bestraft für unbelegte Angst, belohnt für echte präventive Catches.

## Debugger

- Ziel: echte Root-Cause statt Symptomfix.
- Gute Outputs: Repro, Beleg, kein-Bug-Prüfung, ähnliche Fehlerklasse.
- Lernsignal: Fix beseitigt Bug dauerhaft oder Rückfall tritt auf.
- Update-Regel: Jeder Rückfall erzeugt neue Pattern-Lesson.

## Engineer

- Ziel: robuste Lösung mit geringem Blast-Radius.
- Gute Outputs: Invarianten, Datenfluss, Edge Cases, Rollback, Tests.
- Lernsignal: Regression, Migrationserfolg, Supportlast, Betriebsrisiko.
- Update-Regel: Übersehene Schnittstelle wird in Context Map oder Decision Gate ergänzt.

## Coder

- Ziel: minimaler, wartbarer Patch.
- Gute Outputs: kleiner Diff, bestehende Patterns, sichtbare Fehler, Tests.
- Lernsignal: Reviewer-Findings, Testflakiness, spätere Refactor-Kosten.
- Update-Regel: Wiederholte Review-Findings werden zu Coding-Regel.

## Reviewer

- Ziel: echte Bugs finden und Nicht-Bugs vermeiden.
- Gute Outputs: File:Line, Schadenspfad, Repro, Severity, Fix-Richtung.
- Lernsignal: Finding war echter Bug, false positive oder übersehenes Risiko.
- Update-Regel: False positives senken Confidence; echte Catches werden als Pattern gespeichert.

## QA-Tester

- Ziel: realistische Verifikation mit gutem Test-Mix.
- Gute Outputs: Must-run Tests, Edge Cases, Live-Smokes, Restrisiko.
- Lernsignal: Bug trotz Test grün, flaky Test, fehlender E2E-Pfad.
- Update-Regel: Jede escaped Regression erweitert Edge-Case-Matrix.

## Security & Privacy

- Ziel: Tenant-, Daten-, Abuse- und Compliance-Risiken früh sehen.
- Gute Outputs: Trust Boundary, Datenart, Schadenspfad, Minimalfix.
- Lernsignal: Security-Finding, Datenschutz-Rückfrage, Log-/PII-Fund, Provider-Regeländerung.
- Update-Regel: Neue Datenart oder Providerwirkung muss in Checkliste und Context Map.

## SEO Squad

- Ziel: organische Auffindbarkeit und AI-Discovery mit messbarer Business-Wirkung verbessern.
- Gute Outputs: URL/Query/Intent, technischer Befund, Fix-Richtung, Messplan, Revisit-Datum.
- Extra Lernsignal: gefundene oder uebersehene Drift zwischen Website, Pricing, JSON-LD, Legal-Entity und LLM-Dateien.
- Pflicht bei Endbewertungen: [[Mindrails/Superbrain/42-SEO-Final-Evaluation-Protocol|SEO Final Evaluation Protocol]] anwenden und Score-Caps offen nennen.
- Lernsignal: Indexierung, Rankings, CTR, Impressions, Conversions, Search-Console-Fehler, Rich-Result-Status.
- Update-Regel: Jede SEO-Änderung ohne messbaren Effekt wird als Hypothese neu bewertet; jeder technische SEO-Regressionstyp wird in die passende Spezialrolle aufgenommen.

## Scorecard-Eintrag

```md
### Agent Score Entry
- Datum:
- Task:
- Agent:
- Outcome 0-3:
- Evidence 0-3:
- Specificity 0-3:
- Risk Control 0-3:
- Learning 0-3:
- Was war stark?
- Was war schwach?
- Neue Lesson:
- Nächstes Training:
```
