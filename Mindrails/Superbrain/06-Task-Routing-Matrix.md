---
title: Task Routing Matrix
type: routing
status: active
tags:
  - mindrails
  - superbrain
  - routing
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
---

# Task Routing Matrix

Diese Matrix sorgt dafür, dass das Team jede Aufgabe gemeinsam, aber nicht chaotisch bearbeitet.

## Routing nach User-Intent

| User sagt | Lead | Team | Output |
|---|---|---|---|
| "fix", "geht nicht", Fehlerkonsole | Debugger | Engineer, Coder, Reviewer, QA | Root-Cause, Patch, Tests, Restrisiko. |
| "prüf/review/deep" | Reviewer | Debugger, Security, QA, Engineer | Findings zuerst, echte Bugs, File:Line. |
| "plane" | Orchestrator | Business/Engineer/AI je nach Thema, Challenger | Plan, Risiken, Fragen, Stop/Go. |
| "SEO", "Ranking", "Landingpage" | Business-Coach | AI-Welt-Coach, QA, Reviewer, Source Verification | SEO-Audit, Prioritäten, Umsetzung/Tests. |
| "Prompt", "Agent", "Retell", "Stimme" | AI-Welt-Coach | Engineer, QA, Business, Security | Prompt-/Runtime-Plan, Evals, Deploy-Wirkung. |
| "Kalender", "Kunden", "Termin" | Engineer | Debugger, QA, Business, Coder | Datenfluss, UX, API/DB/Prompt-Wirkung. |
| "Billing", "Stripe", "Minuten" | Engineer | Debugger, Security, Reviewer, QA | Transaktions-/Race-/UI-Prüfung. |
| "DSGVO", "AVV", "Legal" | Security & Privacy | Business-Coach, Source Verification, Reviewer | Rechts-/Datenfluss, Risiken, Actions. |
| "was soll ich tun" | Business-Coach | AI-Welt-Coach, Challenger-Council | Strategieoption, Entscheidung, Experiment. |
| "lerne daraus", "speichern" | Learning System | Orchestrator, Scorecards | Lesson, Forecast, Decision oder Context-Update. |

## Projekt-Routing

| Projekt | Hauptteam | Immer beachten |
|---|---|---|
| [[Phonbot/Overview|Phonbot]] | Engineering Cell + Business-Coach | Live-Produkt, Telefonie-Vertrauen, Tenant-Isolation, Retell/Stripe/Kalender, Deploy-Vorsicht. |
| [[Socibot/Overview|Socibot]] | Product/Growth Cell + Engineering Cell | Viele lokale Commits ahead, Compliance-Fokus, Tests/Push-Review, Persona-A. |
| [[Mindrails/Overview|Mindrails]] | Strategy Cell + Knowledge Cell | Dachmarke, Fokus, Kapital, Positionierung, projektübergreifende Priorisierung. |

## Eskalationsregeln

- Production, Zahlung, PII, Tenant-Daten oder SSH: Security & Privacy muss mitprüfen.
- Kunde betroffen: Business-Coach bewertet Kommunikation und Schaden.
- Uncommitted Worktree: Engineer/Reviewer prüfen fremde Änderungen vor Codearbeit.
- Prognose/Markt/Provider: AI-Welt-Coach + Source Verification.
- Unklare Fakten: Orchestrator fragt oder markiert Hypothese.

## Stop-Kriterien

- Wichtige Datei nicht lesbar.
- Codezustand widerspricht Vault-Stand.
- Fix würde fremde uncommitted Arbeit überschreiben.
- Produkt-/Rechtsentscheidung hängt an fehlender User-Entscheidung.
- Externe Quelle ist zu alt oder nicht belastbar für eine aktuelle Aussage.
