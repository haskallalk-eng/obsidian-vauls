---
title: Scientific Foundations
type: research-foundation
status: active
tags:
  - mindrails
  - superbrain
  - science
  - learning
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
---

# Scientific Foundations

Diese Note übersetzt wissenschaftliche Prinzipien in konkrete Superbrain-Regeln. Nicht jede Quelle ist "direkt für AI-Agenten" geschrieben; die Anwendung auf Agent-Rollen ist eine bewusste Übertragung auf Mindrails.

## Prinzipien

| Prinzip | Forschungsidee | Anwendung im Superbrain |
|---|---|---|
| Situation Awareness | Gute Entscheidungen brauchen Wahrnehmen, Verstehen und Projektion. | [[Mindrails/Superbrain/01-Orchestrator|Orchestrator]] muss erst Kontext, Systemzustand und mögliche Folgen sammeln, bevor er Rollen aktiviert. |
| Double-Loop Learning | Nicht nur Aktion korrigieren, sondern die zugrunde liegende Annahme. | Nach Fehlern nicht nur "Fix gemacht", sondern Annahme in [[Mindrails/Superbrain/61-Learning-System|Learning System]] aktualisieren. |
| Experiential Learning | Lernen läuft über Erfahrung, Reflexion, Konzeptbildung und Experiment. | Jeder größere Task endet mit "Was ist passiert? Was lernen wir? Was testen wir als Nächstes?" |
| Deliberate Practice | Expertise wächst durch gezielte Übung mit Feedback, nicht durch Wiederholung. | Agenten bekommen Scorecards, messen Outcomes und üben Schwachstellen gezielt. |
| Psychological Safety | Teams lernen besser, wenn Fehler sichtbar gemacht werden dürfen. | Der [[Mindrails/Superbrain/13-Reviewer|Reviewer]] sucht Bugs ohne Schuldzuweisung; der [[Mindrails/Superbrain/10-Debugger|Debugger]] schützt vor Vertuschen. |
| Premortem | Vor Entscheidungen annehmen, dass sie gescheitert sind, und Gründe suchen. | [[Mindrails/Superbrain/04-Challenger-Council|Challenger-Council]] nutzt den Pessimisten vor Deploys, Pricing, Provider-Wechseln und großen Features. |
| Forecast Calibration | Prognosen werden besser, wenn Wahrscheinlichkeiten später ausgewertet werden. | [[Mindrails/Superbrain/50-Forecast-Ledger|Forecast Ledger]] speichert P, Deadline und Ergebnis. |
| Checklists | Checklisten reduzieren Auslassungen, ersetzen aber nicht Urteil. | [[Mindrails/Superbrain/21-Decision-Gates|Decision Gates]] verhindern vergessene Prüfungen, der Orchestrator bleibt verantwortlich. |
| Systems Thinking | Viele Fehler entstehen aus Systeminteraktionen, nicht aus einer einzelnen Ursache. | Debugger vermeidet "eine Root-Cause und fertig" bei Races, Provider-Flows, Prompt+Tool+DB-Ketten. |
| Modern Code Review | Review dient Defektfindung, Wissensaustausch, Designqualität und Wartbarkeit. | Reviewer bewertet Design, Tests, Edge Cases und Systemfit, nicht nur Stil. |

## Was daraus praktisch folgt

- Kein Agent verbessert sich durch "mehr reden"; er verbessert sich durch bessere Cases, bessere Scorecards und geprüfte Lessons.
- Jeder Agent muss eine eigene Metrik haben, sonst wird er zur Persona-Deko.
- Lessons dürfen nicht nur positiv sein. Ein falscher Forecast, ein falscher Bugverdacht oder ein übersehener Regressionstest sind wertvolle Trainingsdaten.
- Lernen passiert auf drei Ebenen: Fix verbessern, Annahme verbessern, Workflow verbessern.

## Wissenschaftliche Quellen

- Endsley, Situation Awareness, Human Factors, 1995: https://doi.org/10.1518/001872095779049543
- Argyris, Double-Loop Learning / "Teaching Smart People How to Learn", HBR, 1991: https://hbr.org/1991/05/teaching-smart-people-how-to-learn
- Kolb, Experiential Learning / Learning Cycle: https://learningfromexperience.com/research-library/
- Ericsson et al., Deliberate Practice and Expert Performance, Psychological Review, 1993: https://doi.org/10.1037/0033-295X.100.3.363
- Edmondson, Psychological Safety and Learning Behavior in Work Teams, 1999: https://doi.org/10.2307/2666999
- Klein, Project Premortem, HBR, 2007: https://hbr.org/2007/09/performing-a-project-premortem
- Mellers/Tetlock et al., Forecasting Tournaments / Good Judgment Project, 2014: https://doi.org/10.1177/0963721414534257
- Haynes et al., Surgical Safety Checklist, NEJM, 2009: https://doi.org/10.1056/NEJMsa0810119
- Leveson, Systems-Theoretic Accident Model, Safety Science, 2004: https://doi.org/10.1016/S0925-7535(03)00047-X
- Bacchelli/Bird, Expectations, Outcomes, and Challenges of Modern Code Review, ICSE 2013: https://doi.org/10.1109/ICSE.2013.6606617
- Sadowski et al., Modern Code Review at Google, ICSE-SEIP 2018: https://doi.org/10.1145/3183519.3183525

