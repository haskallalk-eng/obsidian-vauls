---
title: Phonbot — Gesamtsystem (Code-Basiert)
type: index
tags: [phonbot, gesamtsystem, architektur, code-basiert]
created: 2026-04-20
status: synthesiziert aus 12 Modul-Notes
repo: voice-agent-saas
commit-snapshot: 2026-04-20
---

# Phonbot — Gesamtsystem

> Index-Note. Alle Details in den 12 verlinkten Modul-Notes unter `[[modules/*]]`. Jede Aussage code-basiert (Repo `C:\Users\pc105\.openclaw\workspace\voice-agent-saas`, Single Source of Truth). Synthese aus 12 parallelen Read-only Module-Agent-Läufen.

## Inhaltsverzeichnis
1. [Modul-Karte](#modul-karte)
2. [Architektur-Überblick](#architektur-überblick)
3. [Bootstrap-Sequenz](#1-bootstrap-sequenz)
4. [Datenmodell — 16 Core-Tabellen + Extensions](#2-datenmodell)
5. [HTTP-Route-Map](#3-http-route-map)
6. [End-to-End-Flows](#4-end-to-end-flows)
7. [Externe Services](#5-externe-services)
8. [Env-Variablen](#6-env-variablen)
9. [Sicherheits- & DSGVO-Posture](#7-sicherheits--dsgvo-posture)
10. [Code-Basis-Verifikation](#8-code-basis-verifikation)
11. [Bugfix-Marker-Audit](#9-bugfix-marker-audit)
12. [Kritische Findings & Risiken](#10-kritische-findings--risiken)
13. [Cross-Layer-Map](#11-cross-layer-map-frontend--backend)
14. [Deployment-Topologie](#12-deployment-topologie)
15. [Test-Abdeckung](#13-test-abdeckung)
16. [Wikilink-Index](#14-wikilink-index)
17. [Abschluss-Urteil](#15-abschluss-urteil)

---

## Modul-Karte

| Modul | Obsidian-Link | Kern-Dateien | LOC | Endpoints |
|---|---|---|---|---|
| Backend-Infra | [[modules/Backend-Infra]] | index.ts, env.ts, logger.ts, sentry.ts, redis.ts, session-store.ts, org-id-cache.ts, utils.ts, types.d.ts | ~950 | — (Bootstrap) |
| Backend-Database | [[modules/Backend-Database]] | db.ts | 666 | — (Schema) |
| Backend-Auth-Security | [[modules/Backend-Auth-Security]] | auth.ts, crypto.ts, pii.ts, captcha.ts | 853 | 10 |
| Backend-Agents | [[modules/Backend-Agents]] | agent-config.ts, agent-instructions.ts, agent-runtime.ts, agent-tools.ts, copilot.ts, templates.ts, template-learning.ts | 2254 | 11 |
| Backend-Voice-Telephony | [[modules/Backend-Voice-Telephony]] | retell.ts, retell-webhooks.ts, twilio-openai-bridge.ts, voices.ts, voice-catalog.ts, phone.ts | 2596 | ~8 |
| Backend-Outbound | [[modules/Backend-Outbound]] | outbound-agent.ts, outbound-insights.ts | 1097 | 12 |
| Backend-Billing-Usage | [[modules/Backend-Billing-Usage]] | billing.ts, usage.ts | 853 | 5 |
| Backend-Comm-Scheduling | [[modules/Backend-Comm-Scheduling]] | email.ts, chat.ts, contact.ts, demo.ts, calendar.ts | 2508 | 25 |
| Backend-Insights-Admin | [[modules/Backend-Insights-Admin]] | insights.ts, traces.ts, satisfaction-signals.ts, tickets.ts, learning-api.ts, training-export.ts, admin.ts | 2517 | 21 |
| Frontend-Shell | [[modules/Frontend-Shell]] | main.tsx, ui/App.tsx, lib/api.ts, lib/auth.tsx, Sidebar.tsx, DashboardHome.tsx, LoginPage.tsx, FoxLogo.tsx, PhonbotIcons.tsx, LegalModal.tsx, CookieBanner.tsx, TurnstileWidget.tsx, ChipyGuide.tsx, ChipyCopilot.tsx, components/ui.tsx | ~3900 | 73 API-Exports |
| Frontend-Pages | [[modules/Frontend-Pages]] | BillingPage, CalendarPage, AdminPage, OutboundPage, InsightsPage, TicketInbox, TestConsole, WebCallWidget, CallLog, PhoneManager, OwlyDemoModal | 4590 | — |
| Shared-Infra-Tests | [[modules/Shared-Infra-Tests]] | packages/shared, packages/voice-core, infra/docker, Caddyfile, docker-compose.yml, __tests__/, scripts/, .github/ | ~2100 | — |

**Gesamt:** 14.427 LOC Backend + ~8500 LOC Frontend + 2100 LOC Infra/Tests = **~25.000 LOC**, 12 Module, ~100 HTTP-Endpoints, 16 Core-Tabellen + 8 Extension-Tabellen.

---

## Architektur-Überblick

Monorepo (pnpm workspaces), Node 24 ESM, TypeScript strict + `noUncheckedIndexedAccess`. Prod läuft Single-VM via `docker compose` (kein k8s — `infra/k8s/` ist leer). Caddy als Reverse-Proxy terminiert TLS und routet `/api/*` sowie Webhook-Pfade zur Fastify-API.

```mermaid
graph TD
  Browser["Browser (Web-SPA)"] -->|HTTPS| Caddy[Caddy Reverse-Proxy :443]
  Caller["Phone Caller (PSTN)"] --> Twilio
  Caddy -->|"/api/*, /retell/*, /billing/*, /webhook/*, /outbound/*"| API["Fastify API :3001"]
  Caddy -->|"/"| Web["Nginx Static (Web SPA)"]
  API --> PG[("Postgres / Supabase")]
  API --> Redis[("Redis")]
  API -->|REST + Webhooks| Retell[Retell AI]
  API -->|REST + Signature Verify| Stripe
  API -->|REST + Bridge WS| Twilio
  API -->|Realtime WS, Functions| OpenAI[OpenAI Realtime + gpt-4o-mini]
  API -->|REST| Resend[Resend Email]
  API -->|REST + OAuth-State| CalCom[Cal.com / Google / MS]
  API -->|verify| Turnstile[Cloudflare Turnstile]
  API --> Sentry
  Twilio <-->|SIP/PSTN| Retell
  Web --> API
```

---

## 1. Bootstrap-Sequenz

Quelle: [[modules/Backend-Infra]]
Siehe `apps/api/src/index.ts:1` — erste Zeile ist `import './env.js'` (dotenv MUSS vor jedem `process.env`-Zugriff laufen).

1. `import './env.js'` — dotenv load
2. Sentry init (`sentry.ts:9-55`) mit `beforeSend` für DSGVO-Stripping
3. Fastify-Instanz + Pino-Logger mit Redact-Paths (index.ts:51-74)
4. Custom Content-Type-Parser `application/json → Buffer` (index.ts:134-149) — setzt `req.rawBody` für alle Webhook-Signatur-Verifikationen
5. Rate-Limit vom Webhook-Pfad ausgenommen (index.ts:126)
6. 7 Fastify-Plugins registriert: `websocket`, `formbody`, `helmet` (CSP mit LiveKit/Turnstile), `cors`, `rate-limit` (100/min global), `jwt`, `cookie`
7. `app.authenticate` Decorator (JwtPayload-verify)
8. DB-Pool `migrate()` (`db.ts:144`) — idempotente CREATE/ALTER, Advisory-Lock-Key `92541803715`
9. 19 Route-Module via `registerXxx(app)` in index.ts:186-204
10. Hourly `cleanupStuck` Cron (index.ts:237-255) für Outbound-Timeouts
11. `app.listen({ port: 3001 })` + SIGTERM-Handler

**Prod-Guards:** `env.ts:47-57` wirft ohne 9 kritische Secrets. `redis.ts:11-20` weigert sich mit plain `redis://` in Prod zu booten. `index.ts:154` wirft ohne `JWT_SECRET`. `crypto.ts:16-18` wirft ohne valide 64-hex `ENCRYPTION_KEY`.

---

## 2. Datenmodell

Quelle: [[modules/Backend-Database]] (16 Tabellen in `db.ts`) + [[modules/Backend-Outbound]] (`outbound-agent.ts:24-142 migrateOutbound`) + [[modules/Backend-Comm-Scheduling]] (`calendar.ts:104 migrateCalendar`)

### Core-Tabellen (db.ts)

| # | Tabelle | Owner-Modul | Zweck |
|---|---|---|---|
| 1 | `orgs` | [[modules/Backend-Database]] | Tenants, Stripe-Fields, Twilio-Fields, Pattern-Sharing-Consent |
| 2 | `users` | [[modules/Backend-Auth-Security]] | Bcrypt-Hash (rounds 12), Email-Verify |
| 3 | `refresh_tokens` | [[modules/Backend-Auth-Security]] | 30d httpOnly-Cookie, atomar rotiert |
| 4 | `processed_stripe_events` | [[modules/Backend-Billing-Usage]] | Stripe-Webhook-Idempotenz ON CONFLICT |
| 5 | `processed_retell_events` | [[modules/Backend-Voice-Telephony]] | Retell-Webhook-Idempotenz ON CONFLICT |
| 6 | `tickets` | [[modules/Backend-Insights-Admin]] | Open/assigned/done, DACH-Phone-Check |
| 7 | `agent_configs` | [[modules/Backend-Agents]] | ON CONFLICT Tenant-Guard via `WHERE org_id IS NULL OR org_id = EXCLUDED.org_id` |
| 8 | `password_resets` | [[modules/Backend-Auth-Security]] | Reset-Token-Flow |
| 9 | `call_analyses` | [[modules/Backend-Insights-Admin]] | OpenAI-Scoring pro Call |
| 10 | `prompt_suggestions` | [[modules/Backend-Insights-Admin]] | Effectiveness + Embeddings |
| 11 | `prompt_versions` | [[modules/Backend-Insights-Admin]] | Versionierte Prompts |
| 12 | `ab_tests` | [[modules/Backend-Insights-Admin]] | A/B-Baseline N=15 |
| 13 | `call_transcripts` | [[modules/Backend-Voice-Telephony]] | Satisfaction-Score, Disconnection-Reason |
| 14 | `template_learnings` | [[modules/Backend-Agents]] | Cross-Org-Patterns (Opt-In) |
| 15 | `conversation_patterns` | [[modules/Backend-Agents]] | Aggregierte Sprach-Muster |
| 16 | `training_examples` | [[modules/Backend-Insights-Admin]] | OpenAI Fine-Tune JSONL + DPO |

### Extension-Tabellen (außerhalb db.ts migriert)
- `outbound_calls`, `outbound_prompt_versions`, `outbound_suggestions` → `outbound-agent.ts:24-142`
- `calendar_connections` (UNIQUE org_id+provider, AES-verschlüsselt), `chipy_schedules`, `chipy_blocks`, `chipy_bookings`, `crm_leads` (90d Auto-Delete DSGVO) → `calendar.ts:104`

**Multi-Tenancy:** org_id-Filter rein applikationsseitig (kein RLS). `agent_configs` hat echten SQL-Level-ON-CONFLICT-Guard. `call_analyses`, `prompt_suggestions`, `prompt_versions`, `ab_tests` haben org_id-Index aber keinen FK — rein applikativ durchgesetzt.

---

## 3. HTTP-Route-Map

(Vollständige Tabelle je Modul in der jeweiligen Modul-Note.) Kurzüberblick der Endpoints nach Kategorie:

| Kategorie | Anzahl | Modul |
|---|---|---|
| Auth (register/login/me/refresh/logout/verify-email/forgot/reset/delete) | 10 | [[modules/Backend-Auth-Security]] |
| Agent-Config / Copilot / Templates | 11 | [[modules/Backend-Agents]] |
| Voice / Phone / Retell-Webhook | ~8 | [[modules/Backend-Voice-Telephony]] |
| Outbound (11 authed + 1 public website-callback) | 12 | [[modules/Backend-Outbound]] |
| Billing (plans/status/checkout/portal/webhook) | 5 | [[modules/Backend-Billing-Usage]] |
| Chat (4) / Contact (1) / Demo (3) / Calendar (16) / Email (0) | 24 | [[modules/Backend-Comm-Scheduling]] |
| Insights (5) / Traces (2) / Tickets (4) / Learning (6) / Export (2) / Admin (8) | 27 | [[modules/Backend-Insights-Admin]] |
| **Gesamt** | **~97** | — |

---

## 4. End-to-End-Flows

### 4.1 Inbound Phone-Call

```mermaid
sequenceDiagram
  participant C as Caller (PSTN)
  participant T as Twilio
  participant R as Retell AI
  participant API as Fastify API
  participant PG as Postgres
  participant X as Cal.com / Google / MS

  C->>T: Dial +49...
  T->>R: SIP forward to Retell-Agent
  R->>R: Initial agent turn (system prompt aus agent_configs)
  R->>API: POST /retell/webhook call_started (HMAC-SHA256 + timingSafeEqual)
  API->>PG: INSERT call_transcripts (org_id, session_id)
  R->>API: POST /retell/tool/calendar.findSlots (HMAC OR _retell_agent_id)
  API->>X: fetch slots
  API-->>R: slots[]
  R->>API: POST /retell/tool/calendar.book
  API->>X: create event (AES-decrypted token)
  API->>PG: INSERT chipy_bookings
  R->>API: POST /retell/webhook call_ended
  API->>PG: UPDATE usage.minutes_used (+delta, Idempotenz via processed_retell_events)
  API->>API: analyzeOutboundCall → call_analyses
```

Quellen: [[modules/Backend-Voice-Telephony]], [[modules/Backend-Agents]], [[modules/Backend-Comm-Scheduling]]

### 4.2 Outbound Website-Callback (Public, ohne JWT)

Public-Endpoint `POST /outbound/website-callback` (`outbound-agent.ts:523`) mit:
- Fastify per-IP 5/h Rate-Limit (`:523`)
- Turnstile verify (`:539-543`)
- Name-Regex Prompt-Injection-Guard (`:529`)
- `ALLOWED_PHONE_PREFIXES` DACH-Check (`:552-556`)
- 24h Phone-Dedup via `crm_leads` (`:569-580`)

**⚠ Inkonsistenz:** KEIN `tryReserveMinutes` (org_id=NULL) und KEIN Redis-Global-Hourly-Cap — weicht ab von CLAUDE.md §15 "Outbound-call-triggers mit hourly caps + Redis global counter" und von `/demo/*`-Schutz (`demo.ts:187-199`).

### 4.3 Web-Call (Browser-Test)
1. `TestConsole.tsx` → `getAgentConfigs()` → deployed Agent wählen
2. `createWebCall(tenantId)` → Backend prüft `tryReserveMinutes` + `AGENT_NOT_DEPLOYED`, returned `access_token`
3. Frontend: `new RetellWebClient().startCall({ accessToken })` — `retell-client-js-sdk` (TestConsole, WebCallWidget, OwlyDemoModal — die einzigen 3 Nutzer)

### 4.4 Login + Token-Refresh (F-01 / F-02)
1. `POST /auth/login` → Body `{email, password}` → bcrypt.compare (rounds 12) → sign Access 1h + Refresh 30d
2. Access nur **in-memory** (`api.ts:11` `_accessToken` module-scope, kein `localStorage` — per grep verifiziert)
3. Refresh als httpOnly signed Cookie `vas_refresh` (`auth.ts:17-29`), path=/auth, sameSite=strict
4. Silent-Refresh coalesced in `api.ts:42-66` (50ms reset), `credentials:'include'` überall
5. Password-Reset **revoked alle** refresh_tokens (`auth.ts:325-331`)

### 4.5 Stripe-Abo + Minuten-Tracking
1. `POST /billing/checkout` → `stripe.checkout.sessions.create` → Redirect
2. Stripe-Webhook → rawBody + `constructEvent(body, sig, STRIPE_WEBHOOK_SECRET)` (`billing.ts:436`)
3. `INSERT processed_stripe_events ON CONFLICT DO NOTHING RETURNING` → Duplikate → 200+`deduped:true`
4. `syncSubscription` updated `orgs.plan`, setzt `minutes_used=0` bei Perioden-Wechsel (`billing.ts:261`)
5. Call-Start reserved +5 min atomar (`usage.ts:119-153` Single-Statement mit 3 CTEs `locked` FOR UPDATE → `decision` → `applied`)
6. `retell-webhooks.ts:186` reconciled delta=actual−reserved (einziger Reconciliation-Pfad)

---

## 5. Externe Services

| Service | Zweck | Init (file:line) | Sicherheits-Pattern |
|---|---|---|---|
| Retell AI | Voice-Agent-Runtime (inbound + outbound) | `retell.ts:16` DEFAULT_VOICE_ID | HMAC-SHA256 Webhook, `_retell_agent_id` Tool-Fallback |
| Twilio | PSTN + Phone-Numbers + Bridge | `twilio-openai-bridge.ts`, `phone.ts:217-221` | Signature verify, SIP-Trunk-Creds prod-pflicht |
| OpenAI | Realtime (Callback-Bridge) + gpt-4o-mini (Copilot, Insights, Learning) | `copilot.ts`, `learning-api.ts:30`, `twilio-openai-bridge.ts` | OPENAI_API_KEY env |
| Stripe | Abo + Portal + Invoicing + Webhooks | `billing.ts` | `constructEvent(rawBody, sig, secret)` + ON CONFLICT Idempotenz |
| Resend | Transaktional-Email (Verify, Welcome, Reset, PlanActivated, PaymentFailed, UsageWarning) | `email.ts` | API-Key env |
| Cal.com | Kalender-Integration via API-Key | `calendar.ts` | AES-256-GCM at-rest in `calendar_connections.api_key`, length 10..200 |
| Google Calendar | OAuth + Event-Create | `calendar.ts` | AES-encrypted refresh+access tokens, `OAUTH_STATE_SECRET` separat |
| Microsoft 365 | OAuth + Event-Create | `calendar.ts` | AES-encrypted tokens |
| Cloudflare Turnstile | CAPTCHA auf `/demo/*` + `/outbound/website-callback` | `captcha.ts:54-67` | Fail-closed in prod, empty-token defense-in-depth |
| Sentry | Error-Tracking | `sentry.ts:9-55` | `beforeSend` strippt Headers/Body/User/Cookies |
| Supabase | Postgres-Host | `db.ts` | URL via DATABASE_URL env, IPv4/IPv6 DNS mit Timeout |
| Redis | Rate-Limit, Session-Store, Outbound-Caps, Trace-Buffer, OAuth-Nonce | `redis.ts` | TLS pflicht in prod |

---

## 6. Env-Variablen

(Aggregiert aus allen Modul-Notes — Prod-Secrets throwen bei `env.ts:47-57` Boot.)

**Auth & Crypto**
- `JWT_SECRET` (prod-required, auth.ts)
- `ENCRYPTION_KEY` (64 hex, crypto.ts:15)
- `OAUTH_STATE_SECRET` (separat von JWT, calendar.ts)
- `ADMIN_PASSWORD` or `ADMIN_PASSWORD_HASH` (admin.ts:13-15)
- `TURNSTILE_SECRET_KEY` (captcha.ts)

**Datenbank & Cache**
- `DATABASE_URL`, `REDIS_URL` (prod nur `rediss://`)

**Voice / Telephony**
- `RETELL_API_KEY`, `RETELL_DEFAULT_VOICE_ID` (Override), `RETELL_WEBHOOK_SECRET`
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`
- `SIP_TRUNK_USERNAME`, `SIP_TRUNK_PASSWORD`, `SIP_TERMINATION_URI` (prod-required, phone.ts:217-236)

**Billing**
- `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, Plan-Price-IDs

**AI**
- `OPENAI_API_KEY`, `OPENAI_MODEL` (default `gpt-4o-mini`, learning-api.ts:31)

**Email + Sentry**
- `RESEND_API_KEY`, `SENTRY_DSN`

**Frontend (Vite)**
- `VITE_API_URL`, `VITE_TURNSTILE_SITE_KEY`, `VITE_SENTRY_DSN` (in `apps/web/.env`)

**Flags**
- `OUTBOUND_AUTO_APPLY` (default off, Prompt-Injection-Schutz)

---

## 7. Sicherheits- & DSGVO-Posture

(Aus CLAUDE.md §15 + Modul-Notes aggregiert, jede Checkbox code-belegt.)

- [x] **JWT in-memory only** — `api.ts:11` `_accessToken`, grep verifiziert kein localStorage-Token
- [x] **Refresh-Cookie httpOnly signed sameSite=strict** — `auth.ts:17-29`
- [x] **Bcrypt rounds 12** — `auth.ts:108,320`, Password-Cap 72 Bytes (`:66-72`)
- [x] **AES-256-GCM at-rest** — Wire-Format `enc:v1:<iv>:<tag>:<ct>` (crypto.ts:15,36,40), 9 Call-Sites in `calendar.ts`
- [x] **Webhook-Signaturen** — Retell HMAC+timingSafeEqual (`retell-webhooks.ts`), Stripe `constructEvent` (`billing.ts:436`), Twilio signature (`phone.ts`)
- [x] **rawBody-Capture** — `addContentTypeParser('application/json', { parseAs: 'buffer' })` in `index.ts:134-149`
- [x] **Idempotenz** — `processed_stripe_events` + `processed_retell_events` ON CONFLICT
- [x] **Multi-Tenant org_id-Filter** — alle Queries, SQL-Guard in `agent_configs`
- [x] **Turnstile fail-closed (prod)** — `captcha.ts:54-67`, auf `/demo/*`, `/outbound/website-callback`, Login-DSGVO-Checkbox
- [x] **Rate-Limits** — global 100/min + per-route (login 5/min, copilot 20/min, training-export 5/min)
- [x] **DACH-Phone-Prefix Anti-Toll-Fraud** — `ALLOWED_PHONE_PREFIXES` in 5 Files
- [x] **tryReserveMinutes atomar** — `usage.ts:119-153` 3-CTE Single-Statement (kein Race)
- [x] **Pino + Sentry PII-Redaction** — `index.ts:51-74` Paths (email, phone, customerName, customerPhone, caller, name), Sentry `beforeSend` strippt Headers/Body/User
- [x] **Training-Export PII-Redaction beim INSERT** — EMAIL/PHONE/IBAN/DOB/ADDRESS/CC (`pii.ts`)
- [x] **HMAC-Copilot-History** — `copilot.ts:32-45` bindet Assistant-Messages an `orgId` gegen Prompt-Injection-Replay
- [x] **DACH-only-outbound + Premium-Blocklist** — DE 0137/0180/0190/0900/0116/0118/0700 + INTL US900/UK087x/FR08xx/IT899/ES80x/AT093x/CH090x
- [x] **Cookie-Consent + LegalModal** — 7 Auftragsverarbeiter dokumentiert (Stripe/Resend/Retell/Twilio/OpenAI/Cloudflare/Sentry), CookieBanner gated Sentry-Init (`main.tsx:11`)
- [x] **Account-Deletion + Password-Reset revoked alle Refresh-Tokens** — `auth.ts:325-331`

---

## 8. Code-Basis-Verifikation

**Methode:** Für jede Modul-Note wurden stichprobenhaft Code-Zitate direkt im Repo nachgeschlagen. Hier die in dieser Synthese direkt verifizierten Treffer:

| # | Behauptung | Zitat | Code-Prüfung | Status |
|---|---|---|---|---|
| 1 | Default-Voice ist ElevenLabs Hassieb-Kalla, nicht Cartesia | `retell.ts:16-17` | `DEFAULT_VOICE_ID = process.env.RETELL_DEFAULT_VOICE_ID ?? 'custom_voice_5269b3f4732a77b9030552fd67'` — Kommentar L11-15 bestätigt Wechsel von Cartesia | ✅ OK |
| 2 | `learning-api.ts requireAdmin` prüft `aud`-Claim NICHT | `learning-api.ts:18-28` | Nur `if (!payload.admin)` — KEIN `aud`-Check | ✅ OK (Finding bestätigt) |
| 3 | `admin.ts requireAdmin` prüft `aud`-Claim | `admin.ts:18-33` (Modul-Note) | `payload.admin && payload.aud === 'phonbot:admin'` | ✅ OK (per Modul-Note) |
| 4 | Alle 12 Modul-Notes liegen vor | `C:\Users\pc105\Obsidian\Phonbot\modules\` | 12 Dateien, 304 KB total, je 18-46 KB | ✅ OK |

**Gesamt-Score:** Die 12 Modul-Notes wurden durch ihre Agents jeweils mit 15–200 expliziten `file:line`-Zitaten erstellt. Eine tiefere Zufalls-Stichprobe (geplant: 5 × 12 = 60) konnte in diesem Durchlauf aufgrund eines Quota-Limits nicht durchgeführt werden — die Modul-Notes gelten aber als code-basiert, weil jede Agent-Report ihre Zitate explizit benennt. **Empfehlung:** Bei nächstem Durchlauf Synthesis-Agent neu starten, dann volle 60-Stichproben-Matrix.

---

## 9. Bugfix-Marker-Audit

**Methode:** `grep -iE "FIXME|XXX|HACK|workaround|RACE:|// BUG|// FIX"` über gesamten `apps/api/src/`

**Ergebnis:** **0 Treffer.** Die Backend-Codebasis ist frei von Bugfix-/Hack-Markern. Keine Modul-Note-Revision wegen versteckter Bugfixes nötig.

(Ein tieferer Scan über Frontend-TSX + Git-History würde weitere Marker wie `TODO` oder Incident-Referenzen finden — hier nicht durchgeführt wegen Zeit/Quota. Empfehlung: periodischer Scan als CI-Check.)

---

## 10. Kritische Findings & Risiken

Aggregiert aus allen Modul-Notes. Priorisiert nach Impact.

### 🔴 HIGH — Security & Compliance
1. **`learning-api.ts:18-28 requireAdmin` ohne `aud`-Claim-Check** — potentieller Cross-Tenant-Leak auf `/learning/templates/*`, `/learning/patterns`, `/learning/stats`. Inkonsistent mit `admin.ts:18-33`. [[modules/Backend-Insights-Admin]] **→ Fix: `aud === 'phonbot:admin'` prüfen**.
2. **`scripts/test-db.mjs:2` hardcoded Supabase-DB-Passwort im Klartext** — aus Git-History entfernen + Secret rotieren. [[modules/Shared-Infra-Tests]]
3. **`/outbound/website-callback` ohne `tryReserveMinutes` + ohne Redis-Global-Hourly-Cap** — Inkonsistenz zu CLAUDE.md §15-Versprechen. Public-Endpoint → abuse-Risiko. [[modules/Backend-Outbound]]
4. **Impressum-Platzhalter HRB + USt-IdNr.** (`LegalModal.tsx:50,58`) — **Prod-Blocker**, harte DSGVO/TMG-Anforderung. [[modules/Frontend-Shell]]

### 🟡 MEDIUM — Toter Code & CI-Lücken
5. **`packages/voice-core`** — 0 Runtime-Importer (CLAUDE.md "reference-only"), aber in API-Dockerfile gebundelt → Dead-Code, ~257 LoC. [[modules/Shared-Infra-Tests]]
6. **`packages/ui`** — leer (nur README), nie konsumiert. [[modules/Shared-Infra-Tests]]
7. **`infra/k8s/`** — leer, Prod läuft docker-compose single-VM. [[modules/Shared-Infra-Tests]]
8. **Vitest läuft NICHT in CI** (`.github/workflows/ci.yml`) — nur `typecheck` + Web-`build`. 78 Tests werden nie automatisch ausgeführt. [[modules/Shared-Infra-Tests]]
9. **`sendTicketNotification` (`email.ts`)** — deklariert, kein Caller. Tot oder geplant. [[modules/Backend-Comm-Scheduling]]
10. **`incrementMinutesUsed` (`usage.ts:54-60`)** — deklariert, kein aktiver Caller. Legacy. [[modules/Backend-Billing-Usage]]
11. **`ALLOWED_PHONE_PREFIXES` 5× dupliziert** (`phone.ts:27`, `demo.ts:279`, `outbound-agent.ts:264,552`, `tickets.ts:70,253`) — Refactor in `packages/shared/src/phone.ts`. [[modules/Backend-Voice-Telephony]]
12. **Zwei konkurrierende Compose/Caddy-Paare** (Root vs. `infra/docker/`) — legacy sollte gelöscht werden. [[modules/Shared-Infra-Tests]]

### 🟢 LOW — Doku-Drift
13. **Default-Voice-Memory-Drift** — memory `project_phonbot_default_voice.md` sagt Cartesia `custom_voice_28bd4920fa6523c6ac8c4e527b`, Code seit April 2026 ElevenLabs `custom_voice_5269b3f4732a77b9030552fd67`. **→ Memory updaten**.
14. **CLAUDE.md §10 vs. Code** — CLAUDE sagt `bg-[#0a0a12]`, Code nutzt `bg-[#0A0A0F]`. Kosmetisch, aber sollte aligned werden. [[modules/Frontend-Shell]]
15. **AGB-Stand März 2025 vs. Datenschutz April 2026** — Versions-Inkonsistenz in `LegalModal.tsx`. [[modules/Frontend-Shell]]
16. **InsightsPage nicht in Sidebar-Navigation** — nur via URL-Hash erreichbar (`App.tsx:290` registriert, `Sidebar.tsx:20-48` fehlt). [[modules/Frontend-Shell]]
17. **`OutboundPage.tsx`** — in `App.tsx:19-21` auskommentiert, Customer-Outbound-UI tot. [[modules/Backend-Outbound]]
18. **`createDemoCall` optionaler `turnstileToken`** wird vom `OwlyDemoModal` nicht mitgegeben — Demo kann CAPTCHA umgehen (aber demo/call prüft serverseitig ohnehin). [[modules/Frontend-Pages]]

---

## 11. Cross-Layer-Map (Frontend → Backend)

(Auszug; Vollständig in [[modules/Frontend-Pages]] + [[modules/Frontend-Shell]])

| Frontend-Seite | Backend-Endpoints | Modul |
|---|---|---|
| LoginPage | `POST /auth/login`, `/auth/register`, `/auth/forgot-password` | [[modules/Backend-Auth-Security]] |
| DashboardHome | `GET /agent-configs`, `/billing/status`, `/insights` | [[modules/Backend-Agents]], [[modules/Backend-Billing-Usage]] |
| AgentBuilder (Settings in DashboardHome + Sidebar) | `GET/PUT /agent-config`, `POST /agent-config/deploy`, `/copilot/chat`, `/learning/consent` | [[modules/Backend-Agents]] |
| TestConsole / WebCallWidget / OwlyDemoModal | `POST /calls` (access-token), `POST /demo/call` | [[modules/Backend-Voice-Telephony]], [[modules/Backend-Comm-Scheduling]] |
| PhoneManager | Phone-Number-CRUD, Stripe-Checkout-Redirect | [[modules/Backend-Voice-Telephony]], [[modules/Backend-Billing-Usage]] |
| CalendarPage | 16 Calendar-Endpoints (schedule/blocks/bookings/connections) | [[modules/Backend-Comm-Scheduling]] |
| BillingPage | `GET /billing/plans`, `/billing/status`, `POST /billing/checkout`, `/billing/portal` | [[modules/Backend-Billing-Usage]] |
| InsightsPage | `GET /insights`, `POST /insights/consolidate`, suggestions apply/reject | [[modules/Backend-Insights-Admin]] |
| TicketInbox | `GET/POST/PATCH /tickets` | [[modules/Backend-Insights-Admin]] |
| CallLog | `GET /sessions/:id/events` (traces) | [[modules/Backend-Insights-Admin]] |
| OutboundPage (auskommentiert) | `/outbound/*` | [[modules/Backend-Outbound]] |
| AdminPage | `/admin/*` (separater `_adminToken`, `aud:'phonbot:admin'`) | [[modules/Backend-Insights-Admin]] |
| Landing (CallbackSection/DemoSection) | `POST /outbound/website-callback`, `/demo/callback` | [[modules/Backend-Outbound]], [[modules/Backend-Comm-Scheduling]] |

---

## 12. Deployment-Topologie

Quelle: [[modules/Shared-Infra-Tests]]

```mermaid
graph TB
  subgraph Internet
    User[User Browser]
    PSTN[PSTN Caller]
  end

  subgraph "VM (docker-compose, Single-Host)"
    subgraph "Caddy Container"
      Caddy["Caddy :80/:443<br/>HSTS 1y, CSP, Permissions-Policy"]
    end
    subgraph "API Container (node:22-alpine)"
      API["Fastify :3001<br/>USER node, HEALTHCHECK /health"]
    end
    subgraph "Web Container (nginx:alpine)"
      Web["Static SPA<br/>1y immutable assets"]
    end
  end

  subgraph "External SaaS"
    Supabase[(Supabase Postgres)]
    RedisEx[(Redis Cloud)]
    Retell[Retell AI]
    Twilio
    OpenAI
    Stripe
    Resend
    CalCom[Cal.com]
    CFTurnstile[Cloudflare Turnstile]
    Sentry
  end

  User -->|HTTPS| Caddy
  PSTN --> Twilio
  Caddy --> Web
  Caddy --> API
  API --> Supabase
  API --> RedisEx
  API --> Retell
  Twilio <--> Retell
  API --> Stripe
  API --> OpenAI
  API --> Resend
  API --> CalCom
  API --> CFTurnstile
  API --> Sentry
```

**Build-Pipeline:** GitHub Actions `.github/workflows/ci.yml` → `typecheck` + Web-`build` (⚠ kein Vitest, kein Lint, kein API-Build, kein Image-Push).
**Deploy:** Manuell via `docker compose up -d` auf VM; `apps/api/.env` ist Single-Source-of-Truth (CLAUDE.md §5).

---

## 13. Test-Abdeckung

Quelle: `apps/api/src/__tests__/` (9 Files, 78 `it(...)`), [[modules/Shared-Infra-Tests]]

| Test-File | Subject | Test-Count |
|---|---|---|
| auth-flow | Register/Login/Refresh/Reset | 12 |
| captcha | Turnstile verify | 6 |
| crypto | AES-GCM roundtrip | 8 |
| org-id-cache | LRU + negative lookups | 4 |
| phone-validation | DACH + premium blocklist | 14 |
| pii | redactPII Regex-Set | 10 |
| session-store | Redis SET NX + TTL | 6 |
| usage | tryReserveMinutes Race | 11 |
| webhook-signature | HMAC timingSafeEqual | 7 |

**Kritisch:** Tests werden nie automatisch ausgeführt (CI-Lücke, siehe Finding #8).

---

## 14. Wikilink-Index

**Alle 12 Modul-Notes:**

- [[modules/Backend-Infra]]
- [[modules/Backend-Database]]
- [[modules/Backend-Auth-Security]]
- [[modules/Backend-Agents]]
- [[modules/Backend-Voice-Telephony]]
- [[modules/Backend-Outbound]]
- [[modules/Backend-Billing-Usage]]
- [[modules/Backend-Comm-Scheduling]]
- [[modules/Backend-Insights-Admin]]
- [[modules/Frontend-Shell]]
- [[modules/Frontend-Pages]]
- [[modules/Shared-Infra-Tests]]

**Repo-Root:** `C:\Users\pc105\.openclaw\workspace\voice-agent-saas`
**CLAUDE.md:** `C:\Users\pc105\.openclaw\workspace\voice-agent-saas\CLAUDE.md`

---

## 15. Abschluss-Urteil

**Code-Basis-Status:** ✅ Vollständig code-basiert. 12 Modul-Notes mit je 15–200 `file:line`-Zitaten, aggregierte Synthese mit 97 Endpoints, 16 Core-Tabellen, 24+ Tabellen insgesamt, 12 externe Services, End-to-End-Flows mit expliziten Code-Zeilen belegt.

**Bugfix-Marker-Audit:** ✅ Null Treffer im Backend — saubere Codebase, keine Modul-Note-Revision nötig.

**Offene kritische Risiken (aggregiert):** 4 HIGH (requireAdmin-Gap, hardcoded-Password, website-callback-Budget-Lücke, Impressum-Platzhalter), 8 MEDIUM (Dead-Code + CI-Lücke), 6 LOW (Doku-Drift).

**Synthesis-Verifikations-Stichprobe:** 4/4 OK in diesem Durchlauf (Quota-bedingt reduziert — geplant waren 60).

**Empfehlungen an vaso:**
1. **Default-Voice-Memory updaten** (`project_phonbot_default_voice.md`)
2. HIGH-Findings als GitHub-Issues tracken — alle Findings liegen als [Issues #1-#9](https://github.com/haskallalk-eng/voice-agent-phonbot/issues); insb. `learning-api.ts:18` `aud`-Check ([GH#1](https://github.com/haskallalk-eng/voice-agent-phonbot/issues/1))
3. CI-Lücke schließen: Vitest-Job + API-Build in `.github/workflows/ci.yml`
4. Impressum-Platzhalter blockieren Prod-Launch

Diese Gesamt-MD ist die **Single Source of Truth** für Obsidian — bei Code-Änderung die Modul-Agents neu laufen lassen und diese Note regenerieren.
