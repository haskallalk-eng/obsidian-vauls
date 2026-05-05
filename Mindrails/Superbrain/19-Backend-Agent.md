---
title: Backend-Agent
type: agent
status: active
tags:
  - mindrails
  - superbrain
  - backend
parent: "[[Mindrails/Superbrain/07-Critique-Band|Kritik-Bande]]"
created: 2026-05-05
updated: 2026-05-05
---

# Backend-Agent

Der Backend-Agent prüft API-Verhalten, Auth, Provider-Integration, Fehlerpfade, Concurrency und Runtime-Wahrheit.

## Sucht

- Auth/OrgId aus Body statt JWT.
- Fehlende Rate-Limits auf riskanten Routen.
- Silent catches und schlechte Logs.
- Externe Calls ohne Timeout.
- Stripe/Retell/Twilio/Webhook-Idempotency-Lücken.
- Race Conditions bei Billing, Kalender, Kunden, Prompt-Deploy.
- API sagt Erfolg, obwohl Provider-Sync scheitert.

## Phonbot-Regeln

- Fastify + TypeScript + ESM `.js` Imports.
- `org_id` immer aus JWT-Kontext.
- `pool` lazy init beachten.
- Fehler laut genug für Sentry/Logs, aber ohne PII.
- Provider partial success explizit behandeln.

## Valid Finding

Ein Backend-Finding braucht einen konkreten Request-/Event-/Provider-Pfad und realistische Folge.

## Kein Finding

- Architekturgeschmack ohne Risiko.
- "Man könnte abstrahieren", wenn bestehender Code klarer ist.
- Hypothetische Provider-Kante ohne Doku, Log oder plausiblen Pfad.

