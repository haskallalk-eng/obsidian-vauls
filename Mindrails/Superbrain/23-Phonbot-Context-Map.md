---
title: Phonbot Context Map
type: context-map
status: active
tags:
  - mindrails
  - superbrain
  - phonbot
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
---

# Phonbot Context Map

Diese Map gibt dem Superbrain schnellen Zugriff auf Phonbot, ohne Produktwissen jedes Mal neu zu rekonstruieren.

## Einstieg

- [[Phonbot/Overview|Phonbot Overview]] - Produkt, Stack, aktive Themen.
- [[Phonbot/Phonbot-Gesamtsystem|Phonbot Gesamtsystem]] - code-basierte Systemkarte.
- [[Phonbot/ZuTun|Phonbot ZuTun]] - offene Produkt- und Audit-Aufgaben.
- [[Phonbot/SEO|Phonbot SEO]] - SEO-/AI-Discovery-Stand.
- [[Phonbot/Pricing|Phonbot Pricing]] - Plan- und Preismodell.

## Technische Module

- [[Phonbot/modules/Backend-Agents|Backend Agents]] - Agent-Konfig, Retell/OpenAI Tools, Prompts.
- [[Phonbot/modules/Backend-Voice-Telephony|Backend Voice Telephony]] - Retell, Twilio, Voice, Number Provisioning.
- [[Phonbot/modules/Backend-Billing-Usage|Backend Billing Usage]] - Stripe, Minuten, Planlimits.
- [[Phonbot/modules/Backend-Comm-Scheduling|Backend Comm Scheduling]] - Kalender, E-Mail, Scheduling.
- [[Phonbot/modules/Backend-Database|Backend Database]] - Tabellen, Beziehungen, Migrationen.
- [[Phonbot/modules/Backend-Auth-Security|Backend Auth Security]] - Auth, Cookies, Security.
- [[Phonbot/modules/Frontend-Pages|Frontend Pages]] - UI-Seiten.
- [[Phonbot/modules/Frontend-Shell|Frontend Shell]] - App-Shell, Navigation, Layout.
- [[Phonbot/modules/Shared-Infra-Tests|Shared Infra Tests]] - Tests, Infra, Packages.

## Phonbot-Invarianten

- Telefonie ist das Kernvertrauen: wenn ein Anruf falsch endet, wirkt das Produkt kaputt.
- Prompt-Settings müssen wirklich in Retell/OpenAI Runtime landen.
- Kalender- und Kundenlogik müssen sauber zusammenspielen, sonst bucht die KI unrealistische Termine.
- Billing-UI darf keine einmaligen Minuten als monatlich missverständlich darstellen.
- Tenant-Isolation ist Pflicht.
- Friseur-UX braucht einfache Sprache, klare Defaults und erklärende Hinweise.

## Vor jeder Phonbot-Aufgabe laden

| Aufgabe | Erst lesen |
|---|---|
| Prompt/Agent | Overview, Backend Agents, Voice Telephony, ZuTun |
| Kalender | Backend Comm Scheduling, Backend Database, Frontend Pages |
| Kundenmodul | Backend Database, Backend Agents, Frontend Pages |
| Billing | Pricing, Backend Billing Usage, Backend Database |
| SEO | SEO, Frontend Pages, Overview |
| Security/DSGVO | Backend Auth Security, Frontend Shell, Overview, ZuTun |

## Verbindung zum Superbrain

- Business-Entscheidungen: [[Mindrails/Superbrain/02-Business-Coach|Business-Coach]].
- AI-/Voice-Trends: [[Mindrails/Superbrain/03-AI-Welt-Coach|AI-Welt-Coach]].
- Code-Fixes: [[Mindrails/Superbrain/20-Workflows|Bugfix Workflow]].
- Launch-Entscheidungen: [[Mindrails/Superbrain/21-Decision-Gates|Decision Gates]].

