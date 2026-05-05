---
title: Mindrails Superbrain
type: moc
status: active
tags:
  - mindrails
  - superbrain
  - agents
parent: "[[Mindrails/Overview|Mindrails]]"
created: 2026-05-05
updated: 2026-05-05
source_of_truth: true
---

# Mindrails Superbrain

> [!info] Zweck
> Dieses Superbrain ist die Steuerzentrale für Strategie, Produkt, Code-Qualität, AI-Trends und Risiko. Es soll Entscheidungen besser machen, nicht nur Notizen sammeln.

## Startpunkte

- [[Mindrails/Superbrain/01-Orchestrator|Orchestrator]] - entscheidet, welche Teil-Gehirne arbeiten und welche Belege nötig sind.
- [[Mindrails/Superbrain/02-Business-Coach|Business-Coach]] - versteht Mindrails/Phonbot als Geschäft, sucht Umsatz, Fokus und Moat.
- [[Mindrails/Superbrain/03-AI-Welt-Coach|AI-Welt-Coach]] - beobachtet die AI-Welt, macht Forecasts und übersetzt Trends in Produktentscheidungen.
- [[Mindrails/Superbrain/04-Challenger-Council|Challenger-Council]] - Realist, Pessimist, Optimist, Risiko-Anwalt und Kunden-Anwalt.
- [[Mindrails/Superbrain/05-Team-Operating-System|Team Operating System]] - wie alle Rollen als Team zusammenarbeiten.
- [[Mindrails/Superbrain/06-Task-Routing-Matrix|Task Routing Matrix]] - welche Rollen bei welchem Auftrag führen.
- [[Mindrails/Superbrain/23-Phonbot-Context-Map|Phonbot Context Map]] - Einstieg in das konkrete Produktwissen.

## Ausführungs-Gehirne

- [[Mindrails/Superbrain/10-Debugger|Debugger]] - beweist erst, dass ein Bug echt ist, bevor gefixt wird.
- [[Mindrails/Superbrain/11-Engineer|Engineer]] - entwirft robuste Lösungen mit Blast-Radius, Datenmodell und Rollback.
- [[Mindrails/Superbrain/12-Coder|Coder]] - implementiert minimal, lesbar und testbar.
- [[Mindrails/Superbrain/13-Reviewer|Reviewer]] - sucht echte Regressionsrisiken und falsche Annahmen.
- [[Mindrails/Superbrain/14-QA-Tester|QA-Tester]] - baut Verifikation, Regression und Edge-Case-Suiten.
- [[Mindrails/Superbrain/15-Security-Privacy|Security & Privacy]] - prüft Trust Boundaries, DSGVO, Secrets, Abuse und sichere Defaults.

## Betriebssystem

- [[Mindrails/Superbrain/20-Workflows|Workflows]] - Bugfix, Feature, Strategie, Incident, Release.
- [[Mindrails/Superbrain/21-Decision-Gates|Decision Gates]] - Go/No-Go-Regeln für Code, Deploy, Produkt und Strategie.
- [[Mindrails/Superbrain/22-Source-Verification|Source Verification]] - Quellenprüfung, Recency, Lateral Reading, Confidence.
- [[Mindrails/Superbrain/24-Project-Knowledge-Base|Project Knowledge Base]] - aktueller Projektkontext zu Mindrails, Phonbot und Socibot.
- [[Mindrails/Superbrain/25-Codebase-Loading-Protocol|Codebase Loading Protocol]] - wie das Team Code und Worktrees sicher lädt.
- [[Mindrails/Superbrain/30-Handoffs|Agent Handoffs]] - saubere Input-/Output-Verträge zwischen Teil-Gehirnen.
- [[Mindrails/Superbrain/40-Templates|Templates]] - wiederverwendbare Formate für Reviews, Forecasts, Decisions, Postmortems.
- [[Mindrails/Superbrain/50-Forecast-Ledger|Forecast Ledger]] - konkrete Prognosen mit Wahrscheinlichkeit, Deadline und Score.
- [[Mindrails/Superbrain/51-Signal-Radar|Signal Radar]] - wöchentliche AI-/Markt-/Wettbewerbs-Signale.
- [[Mindrails/Superbrain/60-Scientific-Foundations|Scientific Foundations]] - wissenschaftliche Grundlagen hinter den Agent-Methoden.
- [[Mindrails/Superbrain/61-Learning-System|Learning System]] - wie das Superbrain aus Fällen, Outcomes und Lessons besser wird.
- [[Mindrails/Superbrain/62-Agent-Scorecards|Agent Scorecards]] - Metriken und Lernsignale für jede Rolle.
- [[Mindrails/Superbrain/90-Research-Sources|Research Sources]] - verwendete Quellen und warum sie relevant sind.

## Kernregeln

1. Realität schlägt Meinung: jede wichtige Aussage braucht Quelle, Code-Fund, Kundensignal oder klar markierte Hypothese.
2. Business-Coach und AI-Welt-Coach sind die höchste Strategie-Ebene; Coder/Reviewer dienen der Umsetzung.
3. Keine Halluzinations-Fixes: wenn Information nicht aus Code, Vault, Tooling oder Quelle ableitbar ist, wird gefragt oder als Annahme markiert.
4. Pessimismus ist ein Werkzeug, kein Lebensgefühl: der Pessimist muss Risiken beweisen, der Optimist muss Chancen beweisen.
5. Forecasts werden nachgehalten. Eine falsche Prognose ist nützlich, wenn sie später sauber ausgewertet wird.
6. Agenten lernen nur über überprüfte Outcomes, Scorecards und wiederverwendbare Lessons, nicht über lose Bauchgefühl-Erinnerungen.

## Datenzugriff

- Interner Kontext: [[Mindrails/Overview]], [[Phonbot/Overview]], [[Phonbot/Phonbot-Gesamtsystem]], [[Phonbot/ZuTun]], [[Phonbot/modules/Backend-Agents]], [[Phonbot/modules/Backend-Voice-Telephony]], [[Phonbot/modules/Backend-Billing-Usage]], [[Phonbot/modules/Backend-Comm-Scheduling]].
- Code-Kontext: `C:\Users\pc105\.openclaw\workspace\voice-agent-saas`.
- Projektwissen: [[Mindrails/Superbrain/24-Project-Knowledge-Base|Project Knowledge Base]] und [[Mindrails/Superbrain/25-Codebase-Loading-Protocol|Codebase Loading Protocol]] vor größeren Code-/Produktaufgaben laden.
- Externe Recherche: offizielle Anbieter-Dokumentation, NIST/OWASP/OECD/Stanford/OpenAI/Google/GitHub, danach belastbare Marktquellen.
- Produktion/SSH/Stripe/GitHub: nur wenn die konkrete Aufgabe es verlangt und der Zugriff verfügbar ist.

## Cadence

- Täglich: neue Signale oder Entscheidungen in [[Mindrails/Superbrain/51-Signal-Radar|Signal Radar]] oder [[Mindrails/Superbrain/50-Forecast-Ledger|Forecast Ledger]] notieren.
- Wöchentlich: Business-Coach + AI-Welt-Coach + Challenger-Council über die wichtigsten offenen Entscheidungen laufen lassen.
- Vor jedem größeren Code-Fix: Debugger -> Engineer -> Coder -> Reviewer -> QA/Security.
- Monatlich: Quellen in [[Mindrails/Superbrain/90-Research-Sources|Research Sources]] auf Aktualität prüfen.
- Monatlich: [[Mindrails/Superbrain/62-Agent-Scorecards|Agent Scorecards]] auswerten und schlechte Rollen gezielt nachtrainieren.
