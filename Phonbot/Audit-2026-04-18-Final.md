---
tags: [project, phonbot, audit, final]
status: active
created: 2026-04-18
type: final-readiness-audit
---

# Phonbot Final Readiness Audit — 2026-04-18

> Vierter Pass nach `4a60dfa`. Ziel: Regression-Check aller 11 Phase-3-Fixes + brand-new issues + Production-Readiness-Verdict.

## ✅ Phase-3-Fixes: alle verifiziert deployed

| Fix | Status | Notes |
|-----|--------|-------|
| Cleanup-Cron `processed_*_events` | ✅ | `cleanupOldWebhookDedupKeys()` + 24h setInterval |
| Stripe Update sofort sync | ✅ | `syncSubscription(updated)` direkt nach `stripe.subscriptions.update()` |
| paidPlans Empty-Guard | ✅ | Sentinel `__NO_PAID_PLAN_CONFIGURED__` + stderr warn |
| Env Boot-Throw für 9 Secrets | ✅ | (Agent meldet 9 statt 8 — Commit-Message war off-by-one; TWILIO_ACCOUNT_SID ist drin) |
| `pg_advisory_lock` um migrate | ✅ | dedizierter client + auto-release via session-close |
| Redis AOF-Rotation | ✅ | live: 100% / 67108864 bytes |
| OpenAI-WS `settled` + `ws.terminate()` | ✅ | Event-Race sauber gehandelt |
| billing.ts `console.warn` → Pino | ✅ | `req.log.warn` |
| admin.ts explizite returns | ✅ | |
| Partial unique index | ✅ | `orgs_stripe_customer_id_notnull_uniq` |

**Keine Regressionen.**

---

## 🔴 CRITICAL (wirklich verifizierte neue Findings)

### C1. `migrate()` Fehler lässt API in Prod trotzdem booten
**File:** [index.ts:171-175](../../.openclaw/workspace/voice-agent-saas/apps/api/src/index.ts#L171)
```typescript
try {
  await migrate();
} catch (e) {
  app.log.error({ err: (e as Error).message }, 'DB migration failed — running without database');
}
```
Advisory-Lock-Timeout oder DDL-Deadlock → Log-Entry, aber API läuft weiter ohne garantiertes Schema. Stripe-Webhooks, Voice-Calls werden auf halbmigrierte Tables geschrieben.
**Fix:** In Prod `throw` wenn migrate fehlschlägt. Dev-Fallback (in-memory Stores) bleibt erhalten.

### C2. Keine `unhandledRejection` / `uncaughtException` Handler
**File:** [index.ts](../../.openclaw/workspace/voice-agent-saas/apps/api/src/index.ts) — grep verifiziert: nur SIGINT/SIGTERM, keine Process-Error-Handler.
Eine verworfene Promise ohne `.catch()` irgendwo (in den Crons, Webhooks, Agent-Runtime) → **Node process crasht silent, Sentry sieht nichts**.
**Fix:** Boot-Zeit-Handler die zu Sentry + Pino loggen, dann `process.exit(1)` für Container-Restart.

---

## 🟠 HIGH (offen, real)

### H1. Graceful Shutdown schließt keine laufenden WebSockets
**File:** [index.ts:360-367](../../.openclaw/workspace/voice-agent-saas/apps/api/src/index.ts#L360)
`app.close()` beendet HTTP-Server, aber Twilio-Audio-WS und OpenAI-Realtime-WS werden abgehackt → laufende Calls verlieren Transkript + Abrechnung hängt.
**Fix:** `Promise.race([app.close(), timeout(10_000)])` + explizites Schließen aller aktiven WS.

### H2. Retell Agent Publishing Race (= O4 aus Postfix, noch offen)
**File:** [agent-config.ts:572-573](../../.openclaw/workspace/voice-agent-saas/apps/api/src/agent-config.ts#L572)
`deployToRetell()` vor `writeConfig()` → wenn DB-Schreibvorgang wirft nach Retell-Success, driften DB und Retell auseinander. Umgekehrt wenn Retell-Update danach scheitert.
**Fix:** Nicht trivial (Retell ist nicht in DB-Transaction). Kurzfristig: strukturiertes Logging + Sentry-Alert wenn `writeConfig` nach erfolgreichem Retell-Update failed, dann manuell resynchronisieren.

### H3. Phone-Pool Sync: 6h-Retry bei Failure
**File:** [index.ts:284-288](../../.openclaw/workspace/voice-agent-saas/apps/api/src/index.ts#L284)
Einmaliger catch → nächster Versuch erst in 6h. Orphan-Nummern bleiben zahlungspflichtig.
**Fix:** Exponential backoff (1min → 5min → 30min → 6h).

### H4. Stripe-Webhook Idempotency + Event-Handler nicht transaktional
**File:** [billing.ts:400-489](../../.openclaw/workspace/voice-agent-saas/apps/api/src/billing.ts#L400)
`INSERT processed_stripe_events` committed bevor Event-Handler (z.B. syncSubscription + auto-provision phone) läuft. Wenn Handler wirft, Dedup-Key bleibt → kein Retry.
**Fix:** Wrap both in single BEGIN..COMMIT — oder nur bei erfolgreichem Event-Handler den Dedup-Key inserten.

---

## 🟡 MEDIUM (nice-to-fix)

- **M1:** paidPlans-Warnung via `process.stderr.write` statt Pino → entgeht Sentry
- **M2:** `APP_URL` fallback zu `localhost:5173` in Prod ohne Validation
- **M3:** Cleanup-Interval 90 Tage für `processed_retell_events` zu lang (Retell retriet max 24h) → sollte 7d reichen, spart DB
- **M4:** Cron-Jobs haben keinen Overlap-Schutz (wenn ein Job >6h braucht → nächster Run startet trotzdem)
- **M5:** PII-Redaction-Paths in Pino sind spezifisch (`email`, `phone`, `customerName`), aber inconsistent gefärte Feld-Namen wie `caller_phone` würden durchrutschen — glob `*phone*` wäre robuster

## 🔵 LOW / Info

- Sentry-Integration vorhanden aber `captureException()` nicht in allen cron-catches
- `OPENAI_REALTIME_MODEL` hardcoded default im Code (Fallback-Chain deckt's trotzdem ab)
- tryReserveMinutes CTE ist korrekt aber komplex — Kandidat für Test-Load + Benchmark

---

## 📊 Production-Readiness Score

**Agent-Score:** 6.5/10
**Mein korrigiertes Urteil:** **7.5/10**

Warum höher: Agent wertet F1+F2 gleichwertig mit echten Datenverlust-Bugs. Tatsächlich sind das **Operational Hardening**-Lücken — sie verhindern keine existierenden Bugs sondern machen Debugging schlechter bei künftigen Incidents. Mit den aktuellen Defensive-Measures (Redis-Lock, pg_advisory_lock, Idempotency) sind die Core-Flows robust.

## 🎯 Vor "100 zahlende Kunden" Blockers

**Muss fixen (30 min Arbeit):**
1. **C1** — `migrate()` Fehler in Prod = throw
2. **C2** — `process.on('unhandledRejection'/'uncaughtException')` Handler mit Sentry

**Sollte fixen (2h Arbeit):**
3. **H1** — Graceful WS-Shutdown
4. **H3** — Phone-Sync mit Backoff
5. **H4** — Stripe-Webhook Transaction

**Kann warten:**
6. H2 Retell Publishing Race (selten, kein Datenverlust — nur Sync-Drift)
7. M1-M5 + LOW

---

## 🚀 Verdict

**Mit C1+C2 gefixt: Green-Light für 100 Kunden.**
Ohne: max 30-50 Kunden + aktives Monitoring von `/health` + Sentry-Dashboard.

## Verwandt

- [[Overview|Phonbot]] · [[Phonbot-Gesamtsystem|🧭 Gesamtsystem]]
- **Audit-Serie:** [[Audit-2026-04-18-Deep|Audit 1: Deep]] → [[Audit-2026-04-18-Bugs|Audit 2: Bugs]] → [[Audit-2026-04-18-Postfix|Audit 3: Post-Fix]] → HIER Audit 4
- **Betroffene Module:**
  - C1 migrate() silent-fail / C2 unhandledRejection / H1 Graceful WS-Shutdown / H3 Phone-Sync-Backoff / M1 paidPlans-stderr / M2 APP_URL / M4 Cron-Overlap → [[modules/Backend-Infra]]
  - H2 Retell-Publishing-Race → [[modules/Backend-Agents]]
  - H4 Stripe-Webhook Transaction / M3 Cleanup-Interval → [[modules/Backend-Billing-Usage]]
  - Partial-Unique Index / pg_advisory_lock → [[modules/Backend-Database]]
  - M5 Pino-PII-Paths → [[modules/Backend-Auth-Security]] · [[modules/Backend-Infra]]
- [[../Daily/2026-04-18|Daily]]
