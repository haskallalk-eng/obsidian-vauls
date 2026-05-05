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
| "SEO", "Ranking", "Landingpage" | [[Mindrails/Superbrain/32-SEO-Squad|SEO Squad]] | Business-Coach, Content, Technical SEO, Structured Data, Measurement | SEO-Audit, Prioritäten, Umsetzung/Tests. |
| "finale SEO-Bewertung", "SEO-Stand", "ist SEO fertig" | [[Mindrails/Superbrain/42-SEO-Final-Evaluation-Protocol|SEO Final Evaluation Protocol]] | SEO Squad, Measurement, AI Search, Structured Data, Content | Endscore, Score-Caps, Belege, Restrisiko, naechster Hebel. |
| "Core Web Vitals", "Sitemap", "robots", "canonical", "structured data" | passende Technical-SEO-Rolle | Frontend, Backend, Measurement | technisches SEO-Finding mit Datei/URL/Check. |
| "AI Search", "LLM SEO", "llms.txt", "AI Overview" | [[Mindrails/Superbrain/39-AI-Search-LLM-SEO-Agent|AI Search & LLM SEO Agent]] | Content, Structured Data, Source Verification | AI-Discovery-Check, Entity- und Quellenklarheit. |
| "Design Skill", "chipy", "look like Phonbot", "UI schöner" | [[Mindrails/Superbrain/48-Design-Skill-Squad|Design Skill Squad]] | Chipy Design, UI, UX, Frontend | Design-System-konforme UI-Lösung. |
| "GitHub Skills", "gute UI Library", "hoch bewertet" | [[Mindrails/Superbrain/46-GitHub-Skill-Scout|GitHub Skill Scout]] | Design Library Radar, Source Verification, Security | Repo-/Skill-Evaluation mit Gate. |
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
