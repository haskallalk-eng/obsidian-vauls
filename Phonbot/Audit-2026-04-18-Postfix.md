---
tags: [project, phonbot, audit, postfix]
status: active
created: 2026-04-18
type: regression-audit
---

# Phonbot Post-Fix Audit — 2026-04-18

> Nach `16b4314` + `4d1975c` + `23d14d6`: Regression-Check + Fresh-Sweep.
> Ergebnis: **Alle Kernfixes korrekt deployed**, aber neue Findings durch Code-Churn aufgetaucht.

## ✅ Was nachweislich clean ist

| Fix | Status | Verifikation |
|-----|--------|--------------|
| Retell Idempotency | ✅ | `processed_retell_events` Table + INSERT ON CONFLICT korrekt platziert |
| Redis maxmemory/LRU/AOF | ✅ | docker-compose command line korrekt, live config bestätigt (512MB) |
| OAuth fail-closed | ✅ | silent catch entfernt, outer try/catch fängt Redis-Errors → null |
| Billing Period EPOCH | ✅ | `EXTRACT(EPOCH)::bigint` + `Number() !==` Vergleich, DST-safe |
| Sekundengenaue Abrechnung | ✅ | `Math.round((x/60000)*100)/100` korrekt, NUMERIC(10,2) in DB |
| Stripe Customer TOCTOU | ✅ | Transaction + FOR UPDATE verhindert Orphan-Customer |
| Phone-Pool Cron (6h) | ✅ | setInterval + bestehender Redis-Lock |
| tryReserveMinutes CASE | ✅ | 4 Decisions atomisch, 12/12 Tests grün, FOR UPDATE serialisiert Races |
| Stripe Status-Blocklist | ✅ | incomplete/unpaid ergänzt, konsistent in SQL + JS |
| Plan-Wechsel Proration | ✅ | subscriptions.update statt Duplicate-Checkout |
| OpenAI Fallback-Chain | ✅ | 3 Models, Probe-Handler korrekt entfernt vor Return |

**Regression-Check auf `Math.ceil`:** nur noch in Kommentaren + nicht-Billing Code (Insights-Thresholds). ✓

---

## 🟠 HIGH — noch offen nach den Fixes

### O1. `processed_retell_events` + `processed_stripe_events` wachsen unbegrenzt
Kein Cleanup-Job. Bei 10k Calls/Mo = 300k Rows/Mo = 3.6M/Jahr. Langzeit-Performance-Problem.
**Fix:** Cleanup-Cron analog zu `cleanupOldTranscripts()` — 90 Tage retention für beide Tabellen.

### O2. Stripe Subscription-Update Race (UX-Stale)
Nach `stripe.subscriptions.update()` antwortet API "success", aber `customer.subscription.updated` Webhook kommt erst ~500ms-2s später → User sieht in `/billing/status` noch alten Plan bis Webhook-Sync.
**Fix:** Die API-Response von `stripe.subscriptions.update()` enthält bereits die updated sub — sofort `syncSubscription(newSub)` aufrufen, dann antworten.

### O3. `tryReserveMinutes` Empty `paidPlans` Edge-Case
Wenn alle PLANS `overchargePerMinute === 0` (Config-Fehler) → `paidPlans = []` → `plan = ANY([])` immer false → alle Paid-Plan-User werden zu hard_blocked.
**Fix:** Assert `paidPlans.length >= 1` beim Boot, oder explizit `paidPlans = paidPlans.length ? paidPlans : ['__NEVER__']` damit SQL wenigstens nicht falsch erlaubt.

### O4. Twilio-Pool + Retell-Agent-Sync Race (überholter Finding aus Bug-Audit)
Separat, nicht durch Fixes gelöst. Bei Race zwischen DB-Write und Retell-API-Update kann Agent "published in DB" sein aber in Retell noch unknown → Calls routen falsch.
**Fix:** Retell-Update in Transaction, rollback bei Fehler. Komplexer, nicht trivial.

---

## 🟡 MEDIUM — Hygiene

### M1. `pg.types.setTypeParser(1700, ...)` betrifft ALLE NUMERIC
Parser ist global — jede künftige NUMERIC-Spalte wird automatisch zu JS number. Aktuell keine Kollision, aber Tripwire für spätere Column-Additions.
**Fix:** Custom Query-Wrapper oder explizite Cast-Strategie pro Spalte.

### M2. `as unknown as string` Type-Lies
`db.ts:13` und `billing.ts:198` — TypeScript-Escape-Hatches. Runtime OK, aber ein Refactor könnte silent brechen.
**Fix:** Proper Types definieren, nicht casten.

### M3. `billing.ts:468` console.warn statt app.log.warn
Umgeht Pino-Redaction + Sentry.
**Fix:** `req.log.warn` nutzen.

### M4. `stripe_customer_id UNIQUE` bei NULL-Semantik
Postgres behandelt mehrere NULL nicht als unique violation. Wenn FOR UPDATE Lock fehlschlägt (DB-Disconnect), können 2 Customer parallel erstellt werden.
**Fix:** Partial Unique Index: `UNIQUE (stripe_customer_id) WHERE stripe_customer_id IS NOT NULL`.

### M5. `chargeOverageMinutes().catch(() => ...)` silent swallow
Kommentar sagt "logged inside", aber das `logged inside` nutzt `process.stderr.write`, nicht Pino → kein Sentry.
**Fix:** `.catch((err) => app.log.warn({ err }, 'chargeOverage failed'))`.

### M6. Missing required-env validation in prod
`RETELL_API_KEY`, `OPENAI_API_KEY`, `TWILIO_AUTH_TOKEN` boot ohne Throw wenn fehlen → App läuft, aber alle Calls scheitern silent.
**Fix:** Zod-validated env-check bei Boot, Throw bei Missing in prod.

### M7. Migration-Race bei Multi-Replica Deploy
2 API-Replicas → `migrate()` parallel → theoretisch Races bei `ADD CONSTRAINT IF NOT EXISTS`.
**Fix:** `pg_advisory_lock(fixed_id)` um die Migration.

### M8. Redis AOF ohne Rotation-Config
`--appendonly yes` aktiviert, aber keine `auto-aof-rewrite-percentage` → AOF-File kann unbegrenzt wachsen.
**Fix:** `--auto-aof-rewrite-percentage 100 --auto-aof-rewrite-min-size 64mb`.

### M9. OpenAI-WS Cleanup-Race
Bei gleichzeitigem `open` + `error` Event könnte die WS als "connected" zurückkommen aber defekt sein (Fallback würde dann nicht triggern).
**Fix:** Bei non-`open` outcome explizit `ws.close()` UND Listener-cleanup idempotent machen.

---

## 🔵 LOW — Dokumentation

- `OPENAI_REALTIME_MODEL` nicht in `.env.example`
- `admin.ts:requireAdmin` fehlt explizites `return` nach `reply.send()` (implizit OK, aber fragil)
- `agent_configs.data jsonb` ohne DB-Level Check-Constraint (Zod auf App-Ebene fängt's)
- AGB-Versionierung: § 5 im Code erwähnt, aber keine Version-Pin

---

## 🎯 Empfohlene Nächste Fix-Runde (Priorität)

1. **Cleanup-Jobs für `processed_*_events`** (30 min) — O1, schnellster Win
2. **Stripe Update sofort syncen** (20 min) — O2, behebt UX-Stale
3. **Empty paidPlans Guard** (10 min) — O3, defensive
4. **console.warn → app.log.warn in billing.ts** (5 min) — M3
5. **Env-Validation für kritische Secrets** (15 min) — M6
6. **stripe_customer_id Partial Unique Index** (10 min) — M4
7. **Redis AOF Rotation** (2 min) — M8
8. **OPENAI_REALTIME_MODEL in .env.example** (1 min) — LOW

**Gesamt: ~1.5h für die 8 schnellen Wins.**

---

## Verwandt

- [[Overview|Phonbot]] · [[Phonbot-Gesamtsystem|🧭 Gesamtsystem]]
- **Audit-Serie:** [[Audit-2026-04-18-Deep|Audit 1: Deep]] → [[Audit-2026-04-18-Bugs|Audit 2: Bugs]] → HIER Audit 3 → [[Audit-2026-04-18-Final|Audit 4: Final]]
- **Betroffene Module:**
  - O1 Event-Cleanup / O2 Stripe-UX-Race / O3 paidPlans / M1 NUMERIC-Parser / M2 Type-Lies / M3 console.warn / M4 Partial-Unique / M5 chargeOverage-Swallow → [[modules/Backend-Billing-Usage]]
  - O4 / H2 Retell-Sync-Race → [[modules/Backend-Agents]] · [[modules/Backend-Voice-Telephony]]
  - M6 Env-Validation / M7 Migration-Lock / M8 AOF-Rotation / M9 OpenAI-WS-Cleanup → [[modules/Backend-Infra]]
- [[../Daily/2026-04-18|Daily]]
