---
title: Project Knowledge Base
type: project-context
status: active
tags:
  - mindrails
  - superbrain
  - projects
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
last_checked: 2026-05-05
---

# Project Knowledge Base

Diese Note speist das Team mit Projektwissen. Sie ist ein Snapshot und muss bei größeren Projektänderungen aktualisiert werden.

## Mindrails

- Dachmarke und Entscheidungs-Hub: [[Mindrails/Overview|Mindrails]].
- Kontakt: `info@mindrails.de`.
- Produkte bleiben im Vault getrennte Trees; Querverbindungen laufen über Mindrails.
- Hauptaufgabe des Superbrain: Fokus, Geschwindigkeit und Qualität über mehrere Produkte hinweg erhöhen.

## Phonbot

- Produkt: Voice-Agent SaaS für Unternehmen, live auf `phonbot.de`: [[Phonbot/Overview|Phonbot]].
- Code: `C:\Users\pc105\.openclaw\workspace\voice-agent-saas`.
- Stack: Fastify 5, TypeScript, React 19, Tailwind 4, Vite, Supabase/Postgres, Redis, Retell AI, OpenAI, Stripe, Twilio, Resend.
- Architektur: Web -> API -> DB/Stripe/Retell; Retell führt Voice-Agent und Tools aus.
- Kritische Invarianten: Multi-Tenant `org_id`, keine PII-Logs, JWT access in memory, refresh cookie httpOnly, ESM `.js` Imports, keine doppelten Deklarationen, typecheck nach TS/TSX.
- Design: Phonbot dark glass, Orange als Hauptfarbe, Chipy/Hamster, keine lila Hauptästhetik.
- Betrieb: Production `root@87.106.111.213`, `/opt/phonbot`, Deploy nur nach User-Go und sauberem Push/Status.
- Snapshot 2026-05-05: Code-Repo hat umfangreiche uncommitted Änderungen in API/Web und untracked `calendar-availability.test.ts` plus `docs/function-tool-validation-2026-05-05.md`; vor jedem Fix Worktree prüfen.
- Wichtigste Vault-Notes: [[Phonbot/Phonbot-Gesamtsystem]], [[Phonbot/ZuTun]], [[Phonbot/modules/Backend-Agents]], [[Phonbot/modules/Backend-Voice-Telephony]], [[Phonbot/modules/Backend-Billing-Usage]], [[Phonbot/modules/Backend-Comm-Scheduling]], [[Phonbot/modules/Frontend-Pages]], [[Phonbot/SEO]], [[Phonbot/Pricing]].

## Socibot

- Produkt: AI-Social-Media-SaaS für deutsche KMUs, Persona-A-Fokus DSGVO-Beratungsbranche: [[Socibot/Overview|Socibot]].
- Code: `C:\Users\pc105\Desktop\Social media Bot`.
- Stack laut Vault: Python 3.11, Flask, Jinja2, Vanilla JS, Catppuccin-Mocha-Theme.
- Kern: Posts generieren, planen und posten für IG/FB/LinkedIn/X/TikTok.
- Compliance-Fokus: DSGVO, Beratungsbranchen, Pattern-Audit, Meta App Review.
- Snapshot 2026-05-05: Repo ist `master...origin/master [ahead 26]` und dirty; viele Dashboard-/Route-/Template-Dateien geändert, neue Ideas-/Client-/Eval-Dateien und Tests untracked. Nicht pushen/committen ohne explizite Anweisung.
- Wichtigste Vault-Notes: [[Socibot/Architecture]], [[Socibot/ZuTun]], [[Socibot/DoD]], [[Socibot/Marktluecke]], [[Socibot/Codex-Findings-2026-04-30]], [[Socibot/kanban/13-ads-beta]].

## Projektübergreifende Regeln

- Produkt-Trees nicht direkt gegenseitig verlinken; Mindrails ist die Klammer.
- Kein Deploy, Push oder Commit ohne klare User-Anweisung.
- Bei dirty Worktrees zuerst fremde/unrelated Änderungen erkennen.
- Code-Wahrheit schlägt Vault-Snapshot; Vault-Snapshot dient nur als Einstieg.
- Wenn Projektstatus unsicher ist: neu prüfen, nicht aus dieser Note raten.
