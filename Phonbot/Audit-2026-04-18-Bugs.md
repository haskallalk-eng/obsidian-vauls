---
tags: [project, phonbot, audit, bugs, future-risk]
status: active
created: 2026-04-18
type: deep-bug-audit
audit_scope: latent-bugs + future-risks + data-integrity
---

# Phonbot Bug-Audit — 2026-04-18 (zweiter Pass)

> 3 parallele Audits: Latent-Bugs (Race/Edge-Cases), Future-Risks (API/Dependency-Drift), Data-Integrity (Billing/Webhooks/Migrations) + Code-Verifikation der umstrittenen Claims.

Siehe auch: [[Audit-2026-04-18-Deep|erster Deep-Audit (Security/DSGVO/Cost)]]

---

## ✅ CROSS-CHECK ERGEBNISSE

**Verifiziert korrekt:**
- `Math.ceil(callDurationMs / 60000)` → [retell-webhooks.ts:121](../../.openclaw/workspace/voice-agent-saas/apps/api/src/retell-webhooks.ts#L121) — Billing rundet IMMER auf. 61s = 2 Min abgerechnet.
- Redis ohne `maxmemory` / `maxmemory-policy` → docker-compose.yml nicht konfiguriert.
- `.catch(() => {})` in Critical Paths (weiterhin 51 Vorkommen — termi fixed grad)

**Agent-Fehler korrigiert:**
- Phone-Pool hat BEREITS `FOR UPDATE SKIP LOCKED` → [phone.ts:418-423](../../.openclaw/workspace/voice-agent-saas/apps/api/src/phone.ts#L418). Agent 1 flagged als Race, falsch. Agent 3 hatte Recht: Edge-Case ist nur "Pool leer → fallback zu Kauf" Race mit Twilio-Duplicate.

---

## 🔴 CRITICAL BUGS (jetzt oder bald Geldverlust)

### C1. Call-Duration Over-Billing via Math.ceil
**File:** [retell-webhooks.ts:121](../../.openclaw/workspace/voice-agent-saas/apps/api/src/retell-webhooks.ts#L121)
```typescript
const minutes = Math.ceil(callDurationMs / 60000);  // 61s → 2 min!
```
**Impact:** Alle Calls werden aufgerundet. Bei 1000 Calls/Mo, ∅ 1:30 Duration → ~10% Über-Billing.
**Unklar:** Ist das Policy (wie Festnetz früher) oder Bug? Prüfen ob AGB das als "minutengenau aufgerundet" deklariert.
**Fix falls Bug:** `Math.ceil(callDurationMs / 60000 - 0.05)` oder Duration als Dezimal abrechnen.

### C2. Stripe Customer Race (TOCTOU)
**File:** [billing.ts:77-93](../../.openclaw/workspace/voice-agent-saas/apps/api/src/billing.ts#L77)
Zwei parallele Checkout-Sessions auf gleiche Org → zwei Stripe-Customer erstellt, zweiter überschreibt DB → erste Customer ist orphan, wird aber trotzdem abgerechnet (falls auch Subscription attached).
**Fix:** `SELECT ... FOR UPDATE` in Transaction.

### C3. `tryReserveMinutes()` nicht-atomarer Fallback
**File:** [usage.ts:50-117](../../.openclaw/workspace/voice-agent-saas/apps/api/src/usage.ts#L50)
Step 1 (atomic UPDATE mit Cap-Check) scheitert → Step 2 ist SELECT + separates UPDATE → 10 parallele Calls auf Paid-Plan können beliebig über Limit reservieren.
**Fix:** Single atomic UPDATE mit CASE-Expression (siehe Agent-Report).

### C4. Retell `call_ended` ohne Idempotency
**File:** [retell-webhooks.ts](../../.openclaw/workspace/voice-agent-saas/apps/api/src/retell-webhooks.ts) — kein `processed_retell_events`
Wenn Retell webhook retries (Netzwerk-Glitch), wird `reconcileMinutes()` 2x aufgerufen → Overage-Charge doppelt.
**Impact bei Pro-Kunde mit Overage:** €9 → €28 pro Retry-Incident.
**Fix:** `CREATE TABLE processed_retell_events (call_id TEXT PRIMARY KEY)`, `INSERT ... ON CONFLICT DO NOTHING` vor reconcile.

### C5. OpenAI Realtime Preview-Model hardcoded
**File:** [twilio-openai-bridge.ts:60](../../.openclaw/workspace/voice-agent-saas/apps/api/src/twilio-openai-bridge.ts#L60)
```typescript
const OPENAI_REALTIME_MODEL = process.env.OPENAI_REALTIME_MODEL ?? 'gpt-4o-realtime-preview-2024-12-17';
```
Preview-Models werden bei OpenAI typisch nach 6-12 Monaten sunsetted. Wenn sunset → alle Voice-Bridges 404 ohne Fallback.
**Fix:** Env-Var setzen (✓ möglich), aber auch Fallback-Logic bei 404.

---

## 🟠 HIGH (innerhalb 6 Monaten Schmerz)

### H1. Stripe Webhook Event-Ordering Race
`customer.subscription.created` kann VOR `checkout.session.completed` ankommen → Plan wird aktiv obwohl Payment noch pending. **Impact:** Minuten-Reservation auf nicht-bezahlter Sub möglich.
**Fix:** Plan-Activation nur bei `invoice.payment_succeeded`, nicht bei `subscription.created`.

### H2. Billing-Period Reset via JS-Date-Vergleich
[billing.ts:166-174](../../.openclaw/workspace/voice-agent-saas/apps/api/src/billing.ts#L166):
```typescript
if (oldEnd && new Date(oldEnd).getTime() !== currentPeriodEnd * 1000) { resetMinutes = true; }
```
Postgres `TIMESTAMPTZ` → JS `Date` → ms-Vergleich mit Stripe Unix-Sec × 1000. DST-Übergänge + Timezone-Conversions → Reset wird ggf. NICHT ausgeführt. **Impact:** Alte `minutes_used` bleibt, User sofort in Overage.
**Fix:** `SELECT EXTRACT(EPOCH FROM current_period_end)::int` und auf Date-Level vergleichen.

### H3. Refresh-Token Rotation Double-Consume
[auth.ts:407-460](../../.openclaw/workspace/voice-agent-saas/apps/api/src/auth.ts#L407)
Network-Retry nach erfolgreichem DELETE → 401 obwohl Rotation eigentlich geklappt hat → User loop-out.

### H4. OAuth-State Replay bei Redis-Down
[calendar.ts:66-74](../../.openclaw/workspace/voice-agent-saas/apps/api/src/calendar.ts#L66)
`.catch(() => 'OK')` → wenn Redis down wird der Check übersprungen (fail-open).
**Fix:** `catch { return null }` — fail-closed.

### H5. Session-Store Cross-Tenant Collision bei Redis-Expiry
[session-store.ts](../../.openclaw/workspace/voice-agent-saas/apps/api/src/session-store.ts) — Edge-Case wenn Session-Key expired zwischen 2 Tabs mit gleicher SessionID aber verschiedenen Tenants → Message-History-Leak möglich.

### H6. Redis ohne maxmemory-Policy
`docker-compose.yml` → bei OOM: "OOM command not allowed". **Rate-Limit + OAuth + Dedup brechen gleichzeitig** → Production-Crash.
**Fix:** `command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru`

### H7. Calendar-Timestamp Mix (`timestamp` vs `timestamptz`)
Teils `timestamptz`, teils `timestamp`, teils `text` (`preferred_time`). DST-Übergänge → Off-by-1-hour, Retention-Jobs löschen falsch.

### H8. Multiple Stripe-Subscriptions pro Org
Plan-Change verlässt alte Subscription aktiv in Stripe (wird nicht gecancelt). **Impact:** Doppel-Abrechnung bei jedem Upgrade.
**Fix:** Alte Sub explizit canceln vor neuem Checkout.

### H9. Outbound-Calls "stuck in calling" Cleanup-Job
[index.ts:233](../../.openclaw/workspace/voice-agent-saas/apps/api/src/index.ts#L233) — setInterval, silent-catch. Bei Deploy/Restart nicht gestartet → Calls bleiben ewig `'calling'` im Dashboard.

### H10. Agent-Config Sync-Race (DB vs. Retell)
[phone.ts:494-515](../../.openclaw/workspace/voice-agent-saas/apps/api/src/phone.ts#L494) Retell-Update fire-and-forget nach DB-Commit. Wenn Retell fehlschlägt: DB sagt Agent X, Retell sagt Agent Y → Calls routen falsch.

---

## 🟡 MEDIUM (nett zu fixen)

### M1. Retell v2-API-Endpoints hardcoded
[retell.ts:27](../../.openclaw/workspace/voice-agent-saas/apps/api/src/retell.ts#L27) — wenn Retell v2→v3 macht, viele Call-Sites brechen.
**Fix:** Versionierung zentralisieren, Zod-Response-Validation.

### M2. OpenAI-Model hardcoded
`gpt-4o-mini` als Default in mehreren Dateien. Wenn OpenAI retired: Chat + Insights fallen aus.

### M3. Stripe SDK ohne explizite apiVersion
`new Stripe(STRIPE_SECRET)` — nutzt SDK-Default. Bei SDK-Update ändert sich API-Version → Webhook-Shape-Drift.
**Fix:** `new Stripe(secret, { apiVersion: '2024-10' })`.

### M4. Call-Transcript `analyzeCall()` läuft trotz ON CONFLICT
[retell-webhooks.ts:141-164](../../.openclaw/workspace/voice-agent-saas/apps/api/src/retell-webhooks.ts#L141) — Insert skipped aber OpenAI-Analyse läuft trotzdem. Webhook-Retry = doppelte OpenAI-Kosten pro Call.

### M5. Encryption-Key-Rotation = All OAuth-Tokens unreadable
Kein Dual-Key-Support. Key leak → neuer Key = alle Calendar-Integrations kaputt.

### M6. Phone-Pool Orphan-Leak
Bei Org-Delete: Nummer zurück in Pool (org_id=NULL), aber `trimPool()` läuft nicht automatisch. Twilio berechnet weiter. **Schaden:** €1-3/Nummer/Monat.

### M7. `useEffect` Empty-Dep Stale Closures
[InsightsPage.tsx:340](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/InsightsPage.tsx#L340), OutboundPage — setState auf unmounted components.

### M8. Float-Precision in Overage
`3.7 min × 0.15 € × 100 = 55.5 cents → Math.round = 56`. Bei 1000+ Monats-Overages akkumuliert sich Drift.

### M9. `tenant_id` text vs. `org_id` uuid Legacy
Tickets-Schema mischt alte text-Spalte mit neuem UUID-FK. Check-Constraint fehlt.

### M10. `plan_status` ohne CHECK-Constraint
Code könnte ungültige Status setzen (`'paid'` statt `'active'`), DB akzeptiert → Downstream-Bugs.

### M11. Demo-Cap ohne Lock
`DEMO_GLOBAL_HOURLY_CAP=200`, Redis INCR ohne Lock → Race kann 201-210 statt 200 erlauben. Low-Volume aber echt.

### M12. Stripe Proration bei Plan-Wechsel
Plan-Change mitten in Periode: inkludierte Minuten werden nicht proportional übertragen. User zahlt für 2 volle Plan-Periods.

### M13. DNS-Resolution Timeout 5s blockiert Boot
[db.ts:22](../../.openclaw/workspace/voice-agent-saas/apps/api/src/db.ts#L22) — 5s DNS-Wait. Bei DNS-Lag → Server-Boot hängt.

---

## 🔵 FUTURE-RISK / ZEITBOMBEN (ETA 6-18 Mo)

| # | Zeitbombe | ETA | Impact |
|---|-----------|-----|--------|
| F1 | OpenAI Realtime Preview Sunset | 3-6 Mo | All voice calls down |
| F2 | Retell v2 API Breaking-Change | 6-12 Mo | All agent-configs broken |
| F3 | OpenAI Model-Retirement (`gpt-4o-mini`) | 6-12 Mo | Chat + Insights 500 |
| F4 | Redis OOM (no maxmemory) | 3-6 Mo | Production-Crash |
| F5 | Stripe API-Version Drift | 6-12 Mo | Doppel-Charges |
| F6 | DB timestamp vs. timestamptz Mix | 3-6 Mo | GDPR + Billing-Drift |
| F7 | React 19 → 20 Migration | 12-18 Mo | Build-Failure |
| F8 | Tailwind 4 → 5 Migration | 6-12 Mo | CSS bricht |
| F9 | Fastify 5 → 6 Plugin-API | 12+ Mo | All routes break |
| F10 | Cal.com API-Instability (jung) | Jederzeit | Booking fehlschlägt silent |

---

## 🎯 TOP-10 Fixes (priorisiert nach Geldverlust × Wahrscheinlichkeit)

1. **Retell `call_ended` Idempotency-Table** (C4) — 2h Arbeit, spart €5-10k/Mo Doppel-Charges
2. **Math.ceil → policy klären oder fixen** (C1) — AGB prüfen, ggf. €30/Mo/Org Über-Billing
3. **`tryReserveMinutes()` atomic CASE-Expr** (C3) — 3h, verhindert unbegrenztes Overshooting
4. **Stripe Customer Race Transaction** (C2) — 2h, Orphan-Customer-Cleanup
5. **Stripe Event-Ordering Guard** (H1) — 4h, `trialing` bis `payment_succeeded`
6. **Redis `maxmemory 512mb + allkeys-lru`** (H6) — 1 Zeile YAML, verhindert Production-Crash
7. **OAuth-State Fail-Closed bei Redis-Down** (H4) — 10 min, Sicherheits-Hardening
8. **`processed_retell_events` Table + Migration** — 2h
9. **Billing-Period EPOCH-Compare statt new Date** (H2) — 30 min
10. **Phone-Pool `trimPool()` cron-triggered** (M6) — 1h, €10-50/Mo orphan-fees

**Gesamt-Aufwand P0+P1:** ~20h Engineering für ~€10-15k/Mo Schadens-Vermeidung.

---

## 🛡️ Proaktive Mitigations (keine akute Fixe)

- **Monitoring:** Uptime-Kuma extern (nicht auf gleichem VPS)
- **Alerting:** Sentry-Alerts wenn `.catch(err => log.warn)` plötzlich hohe Rates zeigt
- **Dependency-Freeze:** React, Tailwind, Fastify auf Majors pinnen (nicht `^`)
- **API-Monitoring:** Monthly grep nach Retell/OpenAI/Stripe Changelog-Diff
- **Schema-Lock:** DB-Migrations versioniert (nicht nur `IF NOT EXISTS`)
- **Load-Test:** Parallel 50x `tryReserveMinutes` → reproducibler Race-Test in CI
- **Chaos-Engineering:** Redis disconnect simulieren → welche Pfade brechen?

---

## Verwandt

- [[Overview|Phonbot]] · [[Phonbot-Gesamtsystem|🧭 Gesamtsystem]]
- **Audit-Serie:** [[Audit-2026-04-18-Deep|Audit 1: Deep]] → HIER Audit 2 → [[Audit-2026-04-18-Postfix|Audit 3: Post-Fix]] → [[Audit-2026-04-18-Final|Audit 4: Final]]
- **Betroffene Module:**
  - C1 Math.ceil / C2 Stripe-Race / C3 tryReserveMinutes / H1 Event-Ordering / H2 Billing-Period / H8 Stripe-Multi-Subs / M3 Stripe-SDK / M8 Float / M11 Demo-Cap / M12 Proration → [[modules/Backend-Billing-Usage]]
  - C4 Retell-Idempotency / C5 OpenAI-Preview / H10 Agent-Sync / M1 Retell-API / M4 analyzeCall / F1-F2 → [[modules/Backend-Voice-Telephony]]
  - H3 Refresh-Rotation / H4 OAuth-State / H5 Session-Store → [[modules/Backend-Auth-Security]]
  - H7 Timestamp-Mix / M5 Encryption-Rotation → [[modules/Backend-Comm-Scheduling]]
  - H6 Redis maxmemory / H9 Cleanup-Cron / M13 DNS-Timeout → [[modules/Backend-Infra]]
  - M6 Phone-Pool Orphan → [[modules/Backend-Voice-Telephony]]
  - M9 tenant_id Legacy / M10 plan_status Constraint → [[modules/Backend-Database]]
  - M7 useState-Spam → [[modules/Frontend-Pages]]
- [[../Daily/2026-04-18|Daily]]
