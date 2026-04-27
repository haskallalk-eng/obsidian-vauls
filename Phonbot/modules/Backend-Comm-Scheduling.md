---
module: Backend-Communication-Scheduling
repo: voice-agent-saas
path_root: apps/api/src
files: 5
total_lines: 2508
external_services: [Resend, Cal.com, Google Calendar, Microsoft Graph, Cloudflare Turnstile, Retell]
created: 2026-04-20
---

# Backend – Communication & Scheduling

Modul umfasst alle Ausgangskommunikation (Email via Resend), öffentliche Entry-Points (Chat-Widget, Kontaktformular, Demo) und das komplette Scheduling-Subsystem (Google/Microsoft OAuth, Cal.com API, eingebauter "Chipy"-Kalender).

Registriert in `apps/api/src/index.ts:189-207` über `registerChat`, `registerDemo`, `registerCalendar`, `registerContact` + `migrateCalendar` in der Migration-Schleife (`index.ts:207`).

---

## Dateien im Modul

| Datei | Zeilen | Rolle |
|---|---:|---|
| [[#email.ts]] | 218 | Resend-Wrapper + transaktionale/CRM-Email-Templates |
| [[#chat.ts]] | 130 | Authenticated Chat-Widget-API (Org-scoped) |
| [[#contact.ts]] | 69 | Public Contact-Form → Resend |
| [[#demo.ts]] | 343 | Public Demo (Web-Call + Sales-Callback) mit Turnstile |
| [[#calendar.ts]] | 1748 | Google/Microsoft OAuth, Cal.com, Chipy-Scheduler |

---

## email.ts

Resend-SDK-Wrapper (`apps/api/src/email.ts:8`). Alle Mails gehen durch `send()` (`email.ts:82`) mit `sendWithTimeout()` (`email.ts:65`) — 10s Race gegen Resend-SDK-default von ~300s, um Fastify-Worker nicht zu blockieren. Late-Rejection-Swallow via `.catch()` um Unhandled-Rejection-Prozess-Crash zu verhindern (`email.ts:72-74`).

### ENV
- `RESEND_API_KEY` (`email.ts:4`) — ohne Key ist `resend = null` → `send()` no-op (Dev-Mode).
- `EMAIL_FROM` default `Phonbot <noreply@phonbot.de>` (`email.ts:5`)
- `APP_URL` default `https://phonbot.de` (`email.ts:6`)

### Exportierte Funktionen
| Funktion | Zeile | Betreff | Trigger |
|---|---:|---|---|
| `sendVerificationEmail` | 96 | "E-Mail bestätigen — Phonbot" | `auth.ts:150`, `auth.ts:399` (Signup + Resend) |
| `sendPasswordResetEmail` | 106 | "Passwort zurücksetzen — Phonbot" | `auth.ts:279` (1h-TTL) |
| `sendTicketNotification` | 119 | "Neues Ticket: {name/phone}" | **ungenutzt** (kein Caller gefunden) |
| `sendWelcomeEmail` | 145 | "Willkommen bei Phonbot!" | `auth.ts:154` (nach Verification) |
| `sendPlanActivatedEmail` | 164 | "{Plan}-Plan aktiviert — Phonbot" | `billing.ts:481` (Stripe-Webhook) |
| `sendUsageWarningEmail` | 183 | "{percent}% Kontingent verbraucht — Phonbot" | `usage.ts:265-266` (dynamic import) |
| `sendPaymentFailedEmail` | 205 | "Zahlung fehlgeschlagen — Phonbot" | `billing.ts:523` |

### Template
`brandedEmail()` (`email.ts:12`) — dark-mode HTML-Shell, `#0A0A0F` Background, Orange-Cyan-Gradient-CTA, Chipy-Logo aus `${APP_URL}/chipy.svg`. Alle User-Inputs via `escapeHtml()` aus `./utils.js`.

### Referenzen
- Eingehend: `auth.ts`, `billing.ts`, `usage.ts`, Test-Mocks in `__tests__/auth-flow.test.ts:82-84`
- Ausgehend: Resend API, `./utils.js:escapeHtml`

---

## chat.ts

**Alle Endpoints AUTHENTICATED** (`chat.ts:46`) — JWT `orgId` wird serverseitig aus `req.user` gezogen, NIE aus Body/Query. Zuvor unauth → PII-Leak + Cost-Abuse (Kommentar `chat.ts:42-45`).

### Routen
| Method | Path | Zeile | Rate-Limit | Notes |
|---|---|---:|---|---|
| POST | `/chat` | 52 | 10/min | Body: `{ sessionId, text (≤4000) }` → `runAgentTurn` |
| GET | `/chat/:sessionId/history` | 109 | default | Org-scoped `getMessages` |
| DELETE | `/chat/:sessionId` | 117 | default | Org-scoped `clearSession`, 204 |
| GET | `/chat/sessions` | 126 | default | Liste aller Org-Sessions |

### Daily-Budget
`enforceDailyChatBudget()` (`chat.ts:19`) — Redis-backed `budget:chat:{orgId}:{YYYY-MM-DD}` mit atomic `INCR + EXPIRE 86400` Pipeline (`chat.ts:28-31`). Default **300 Requests/Tag/Org** via `CHAT_DAILY_BUDGET_PER_ORG`. Fail-open bei Redis-Hiccup (`chat.ts:36`). Kommentar am Code erklärt Bug: Alte Version hatte Race zwischen `INCR` und conditional `EXPIRE`, wo abgebrochene Verbindung den Counter ewig leben ließ → Lockout.

### Error-Handling
`SESSION_ID_COLLISION` (`chat.ts:87`) → 409 statt 500 (cross-tenant session-id-reuse).

### Referenzen
- Eingehend: `index.ts:189` (`registerChat`)
- Ausgehend: `./traces.js` (`appendTraceEvent`), `./agent-runtime.js` (`runAgentTurn`), `./session-store.js`, `./redis.js`, `./auth.js` (`JwtPayload`)

---

## contact.ts

**Public** Endpoint. Rate-Limit 5 / 10min (`contact.ts:26`).

### Route
| Method | Path | Zeile |
|---|---|---:|
| POST | `/contact` | 25 |

### Payload & Schutz
- Zod `ContactBody` (`contact.ts:12`): `email` required + valid, `message` 1..5000, `name` optional ≤200
- Header-Injection-Schutz: `sanitizeHeaderValue()` (`contact.ts:20`) strippt `\r\n\0` + komprimiert Whitespace, kappt auf 200 chars → verhindert Bcc/Cc-Injection über `name`-Feld
- Alle User-Inputs im HTML via `escapeHtml()`
- CONTACT_TO default `info@mindrails.de` (`contact.ts:7`)
- `replyTo: safeEmail` gesetzt
- Wenn `resend === null`: Drop mit Log (`messageLen`, `hasEmail`) — **kein** Plaintext-Log von `message` (DSGVO, `contact.ts:36-38`)

### Kein Turnstile!
Rein Rate-Limit-basiert. Das ist verglichen mit `demo.ts` schwächer.

### Referenzen
- Eingehend: `index.ts:203`
- Ausgehend: Resend API, `./utils.js`

---

## demo.ts

Landingpage-Demo, komplett ohne Auth. **Doppelter Schutz**: per-IP-Rate-Limit + globale Redis-Hourly-Cap + Cloudflare Turnstile + CRM-Dedup.

### ENV
- `DEMO_GLOBAL_HOURLY_CAP` default 200 (`demo.ts:185`)
- `RETELL_OUTBOUND_NUMBER` für Sales-Callback (`demo.ts:313`)
- `ALLOWED_PHONE_PREFIXES` default `+49,+43,+41` (DACH, `demo.ts:279`)
- `RETELL_LLM_MODEL` default `gpt-4o-mini` (`demo.ts:64, 128`)

### Routen
| Method | Path | Zeile | Rate-Limit | Turnstile |
|---|---|---:|---|:---:|
| GET | `/demo/templates` | 203 | default | — |
| POST | `/demo/call` | 214 | 10/h | YES |
| POST | `/demo/callback` | 251 | 10/h | YES |

`/demo/leads` wurde entfernt — stattdessen `/admin/leads` (`demo.ts:342`).

### `/demo/call` (Web-Call)
1. Zod `DemoCallBody` mit `templateId`-Whitelist gegen `TEMPLATES` (`demo.ts:164-167`) — verhindert unbounded Retell-Agent-Erzeugung ("each unknown templateId creates a new Retell LLM + Agent → cost")
2. `enforceGlobalDemoCap('call')` ZUERST (sub-ms Redis) — spart 5s Turnstile-Call bei Cap-Hit (`demo.ts:223-230`)
3. `verifyTurnstile(turnstileToken, req.ip)` (`demo.ts:234`) — Dev ohne `TURNSTILE_SECRET_KEY` no-op, Prod fail-closed 403
4. `getOrCreateDemoAgent()` → Retell `createWebCall`

### `/demo/callback` (Outbound Sales-Call)
1. Zod `DemoCallbackBody` mit Unicode-Regex `/^[\p{L}\p{N}\s'-]+$/u` auf `name` → Prompt-Injection-Mitigation (Name wird in Agent-Prompt interpoliert, `demo.ts:174-180`)
2. Turnstile
3. Global Cap
4. Phone-Normalisierung zu E.164 + DACH-Whitelist (`demo.ts:273-283`)
5. **CRM-Dedup**: `SELECT FROM crm_leads WHERE phone = $1 AND created_at > now() - interval '24 hours'` (`demo.ts:290-293`) — Rückgabe trotzdem 200 um Enumeration zu verhindern (`demo.ts:295-297`)
6. INSERT `crm_leads (source='demo-callback', status='new')` (`demo.ts:306-309`) — DSGVO: 90-Tage-Auto-Delete via `cleanupOldLeads()` (`db.ts`)
7. `createPhoneCall` via Retell mit Sales-Agent → bei Success UPDATE `crm_leads SET status='contacted', call_id`

### Demo-Agent-Caching
- `readDemoAgent / writeDemoAgent` (`demo.ts:21, 31`) — Redis `demo_agent:{templateId}` + In-Memory Map (cap 1000 mit LRU-Evict `demo.ts:33-36`), 24h TTL
- `getOrCreateDemoAgent()` (`demo.ts:49`) mit in-process `pendingDemoCreate`-Map → Single-flight gegen N parallele Cold-Cache-Requests

### Sales-Agent
- `getOrCreateSalesAgent()` (`demo.ts:120`, exportiert) — Redis `sales_agent:phonbot` mit 7-Tage-TTL (verhindert stale agent_id nach Retell-Account-Rotation, `demo.ts:145-147`)
- System-Prompt: "Chipy von Phonbot" auf Deutsch, max 2-3 Sätze, branchenspezifische Beispiele (Friseur/Handwerker/Arzt), Gespräch <2 Minuten (`demo.ts:92-113`)
- Registriert sich als outbound agent auf `RETELL_OUTBOUND_NUMBER` (`demo.ts:150-153`)
- Auch genutzt in `outbound-agent.ts:623-625`

### Referenzen
- Eingehend: `index.ts:193`, `outbound-agent.ts:623` (dynamic import)
- Ausgehend: `./retell.js`, `./templates.js:TEMPLATES`, `./db.js`, `./redis.js`, `./captcha.js:verifyTurnstile`

---

## calendar.ts

**1748 Zeilen** — größte Datei im Modul. Drei parallele Provider + eingebautes "Chipy"-System:

1. **Google Calendar** – OAuth 2.0 + Calendar API v3
2. **Microsoft Graph** – OAuth 2.0 + Graph v1
3. **Cal.com** – API-Key (nicht OAuth), v1 API
4. **Chipy** – eigene Tabellen `chipy_schedules`, `chipy_blocks`, `chipy_bookings`

### ENV
- `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI` (`calendar.ts:1138-1141`)
- `MICROSOFT_CLIENT_ID`, `MICROSOFT_CLIENT_SECRET`, `MICROSOFT_REDIRECT_URI` (`calendar.ts:1465-1468`)
- `OAUTH_STATE_SECRET` — Prod-`throw` wenn fehlt (`calendar.ts:29`); dev-fallback `JWT_SECRET`, dann `'dev-oauth-state'`
- `APP_URL`

### Outbound-Fetch-Policy
`calFetch()` (`calendar.ts:16-19`) mit 10s `AbortSignal.timeout` default. Alle Google/MS/Cal.com-Calls gehen da durch → kein hängender Upstream pint Fastify-Worker (`CAL-04`).

### OAuth State — HMAC mit SEPARATEM Secret
`signOAuthState` (`calendar.ts:35`), `verifyOAuthState` (`calendar.ts:46`):
- `OAUTH_STATE_KEY` bewusst NICHT = `JWT_SECRET` → JWT-Leak ≠ OAuth-State-Forgery
- 16-Byte `nonce` + 600s TTL
- **Replay-Schutz**: Redis `oauth_state_used:{nonce}` mit `SET NX EX` (`calendar.ts:69-76`) — double-click / leaked URL → rejected. Bei Redis-down fail-open (dev), bei Redis-reachable aber SET-failed fail-CLOSED (kein silent-catch `calendar.ts:64-68`)
- `timingSafeEqual` auf HMAC

### Encryption at Rest
Alle Tokens + Cal.com-Keys via `encrypt/decrypt` aus `./crypto.js` (AES-256-GCM) (`calendar.ts:6`). `decryptConn()` (`calendar.ts:217`) loggt `[calendar] decrypt * failed` statt silent-empty-string (`CAL-07`). Transparent-Kompat für Legacy-Plaintext-Rows.
→ siehe [[Backend-Auth-Security]] `crypto.ts`.

### DB-Schema (`migrateCalendar` `calendar.ts:100`)
```
calendar_connections (
  id, org_id UUID FK orgs(id) ON DELETE CASCADE,
  provider TEXT DEFAULT 'google',     -- 'google'|'microsoft'|'calcom'
  access_token TEXT, refresh_token TEXT, token_expires_at TIMESTAMPTZ,
  calendar_id TEXT DEFAULT 'primary',
  email TEXT,
  api_key TEXT,   -- Cal.com (encrypted)
  username TEXT   -- Cal.com
)
-- UNIQUE (org_id, provider)   cal_conn_org_provider_uniq

chipy_schedules (org_id PK FK orgs, schedule JSONB, updated_at)
chipy_blocks (id, org_id, date, start_time TIME, end_time TIME, reason)
  -- UNIQUE (org_id, date) WHERE start_time IS NULL  chipy_blocks_fullday_uniq
chipy_bookings (id, org_id, customer_name, customer_phone, service, notes, slot_time)
  -- UNIQUE (org_id, slot_time)   chipy_bookings_org_slot_uniq
```
Migration renamed legacy `chippy_*` → `chipy_*` (`calendar.ts:138-143`, User-Quote: "CHIPY immer so"). Pre-Index-Cleanup dedup via `DELETE USING WHERE a.id < b.id` (`calendar.ts:197-206`).

→ siehe [[Backend-Database]].

### Top-15 wichtigste Funktionen

| # | Funktion | Zeile | Beschreibung |
|---|---|---:|---|
| 1 | `registerCalendar` | 1137 | Entry: alle Routen + OAuth-Setup |
| 2 | `migrateCalendar` | 100 | Schema + Chippy→Chipy-Migration, FullDay-Unique-Index |
| 3 | `signOAuthState` / `verifyOAuthState` | 35/46 | HMAC-CSRF-Token + Nonce-Replay-Schutz |
| 4 | `getValidToken` (Google) | 423 | Token-Refresh mit Redis-Lock `cal:refresh:google:{orgId}` (CAL-02) |
| 5 | `getValidMsToken` (Microsoft) | 263 | dito für MS, 5min-Pre-Expiry-Check |
| 6 | `decryptConn` | 217 | In-place-Decrypt aller sensitiven Felder mit Fail-Warn |
| 7 | `findFreeSlots` | 804 | **public export** — merged alle Provider + Chipy, Chipy-Blocks authoritative über externe Quellen |
| 8 | `bookSlot` | 972 | **public export** — multi-provider fan-out + Chipy-Mirror-Record; Fallback-only-Chipy wenn extern failt |
| 9 | `findSlotsForConnection` | 911 | Dispatch `calcom`/`microsoft`/google → freeBusy-Query |
| 10 | `bookSlotForConnection` | 1051 | Dispatch: `msBookSlot` / `calcomBookSlot` / Google Calendar `/events` POST |
| 11 | `msFindSlots` | 336 | `graph.microsoft.com/v1.0/me/calendar/getSchedule` (Prefer `Europe/Berlin`) → FreeSlots |
| 12 | `calcomFindSlots` | 673 | `api.cal.com/v1/availability?apiKey=` – beide Response-Varianten (`slots`-Map oder `busy[]`) |
| 13 | `calcomBookSlot` | 737 | `api.cal.com/v1/bookings` POST, tz=`Europe/Berlin`, lang=`de` |
| 14 | `calcomGetEventTypes` | 784 | `api.cal.com/v1/event-types` – event_types[] für Default-Pick |
| 15 | `generateFreeSlots` / `generateChipySlots` | 499/615 | 30-min-Grid, 8-18h / Chipy-Schedule, Fail-closed bei Invalid-Date (CAL-11) |

### Routen-Tabelle (16 Endpoints)

| Method | Path | Zeile | Auth | Notes |
|---|---|---:|:---:|---|
| GET  | `/calendar/google/auth-url`       | 1154 | JWT | returns `{url}` |
| GET  | `/calendar/google/connect`        | 1185 | JWT | 302 → Google Consent |
| GET  | `/calendar/google/callback`       | 1217 | state-HMAC | Zod-capped `code≤1000,state≤500` (CAL-06); autoclose-HTML |
| POST | `/calendar/calcom/connect`        | 1323 | JWT | Body: `apiKey` 10..200 (CAL-03) + optional `username`, validiert via `/v1/me` |
| GET  | `/calendar/status`                | 1386 | JWT | connected/provider/email/eventTypes/chipy; expired-Flag wenn Token-Refresh scheitert |
| DEL  | `/calendar/disconnect`            | 1444 | JWT | `DELETE FROM calendar_connections WHERE org_id` |
| GET  | `/calendar/microsoft/auth-url`    | 1475 | JWT |  |
| GET  | `/calendar/microsoft/callback`    | 1504 | state-HMAC | warnt wenn kein `refresh_token` (offline_access nicht granted, CAL-13) |
| GET  | `/calendar/chipy`                 | 1613 | JWT | schedule + blocks + upcoming bookings (LIMIT 50) |
| PUT  | `/calendar/chipy`                 | 1645 | JWT | `ChipyScheduleSchema` Zod (CAL-09) |
| POST | `/calendar/chipy/block`           | 1668 | JWT | `ChipyBlockSchema` date YYYY-MM-DD (CAL-09) |
| DEL  | `/calendar/chipy/block/:id`       | 1684 | JWT | org-scoped |
| GET  | `/calendar/chipy/bookings`        | 1693 | JWT | ?from&to range (default 90d) |
| POST | `/calendar/chipy/bookings`        | 1709 | JWT | 409 bei `23505`-Unique-Violation → `SLOT_TAKEN` |
| DEL  | `/calendar/chipy/bookings/:id`    | 1741 | JWT | org-scoped |

### Google OAuth Scopes (`calendar.ts:1144-1147`)
`calendar.events` + `calendar.readonly` — offline-access + `prompt=consent` (Force refresh_token)

### MS Graph Scopes (`calendar.ts:1469`)
`Calendars.ReadWrite offline_access User.Read`

### Security-Hardenings im Code (nummeriert via CAL-xx)
- CAL-02 Redis-Lock gegen Token-Refresh-Race (both providers)
- CAL-03 Max-Length-Caps auf apiKey (max 200 DB/upstream)
- CAL-04 10s Timeout auf allen Outbound-Calls
- CAL-06 Query-Length-Cap auf OAuth-Callback-Params (anti-POST-flood)
- CAL-07 Decrypt-Failure-Logging statt silent-empty
- CAL-09 Zod auf Chipy-Schedule/Block (anti-prototype-pollution + DB-size)
- CAL-11 Fail-closed bei Invalid-Date-Busy-Periods
- CAL-13 Warn bei MS-callback ohne refresh_token

### Referenzen
- Eingehend:
  - `index.ts:23, 195, 207` (`registerCalendar`, `migrateCalendar`)
  - `agent-tools.ts:5, 136, 151` (`findFreeSlots`, `bookSlot` für LLM-Tools im Voice-Agent)
  - `retell-webhooks.ts:18, 282, 343` (`findFreeSlots`, `bookSlot` bei Retell-Tool-Webhooks)
- Ausgehend:
  - `./db.js` — `pool`
  - `./auth.js` — `JwtPayload`, `app.authenticate`
  - `./crypto.js` — `encrypt/decrypt` (AES-GCM) → [[Backend-Auth-Security]]
  - `./redis.js` — Locks + Nonce-Replay
  - Google OAuth + Calendar API v3
  - Microsoft login + Graph v1
  - Cal.com v1 API

---

## Externe Services — Zusammenfassung

| Service | Datei(en) | Auth | Timeout | Encryption |
|---|---|---|---|---|
| Resend | email.ts, contact.ts | API-Key env | 10s `sendWithTimeout` | — |
| Cal.com | calendar.ts | Per-Org API-Key in DB | 10s `calFetch` | AES-256-GCM on api_key |
| Google Calendar | calendar.ts | OAuth 2.0 + refresh | 10s | AES-256-GCM on access/refresh_token |
| Microsoft Graph | calendar.ts | OAuth 2.0 + refresh | 10s | AES-256-GCM on access/refresh_token |
| Cloudflare Turnstile | demo.ts (via `./captcha.js`) | Secret env | — | — |
| Retell | demo.ts | API-Key env | — | — |

---

## Public / Unauthenticated Endpoints (kritisch)

> Diese Endpoints sind **ohne JWT** erreichbar. Bei Änderungen zuerst Rate-Limits + Turnstile + Global-Cap prüfen.

| Endpoint | Datei:Zeile | Rate | Turnstile | Extra-Schutz |
|---|---|---|:---:|---|
| `POST /contact` | contact.ts:25 | 5 / 10min | — | Header-Sanitize |
| `POST /demo/call` | demo.ts:214 | 10/h | YES | Global 200/h, Template-Whitelist |
| `POST /demo/callback` | demo.ts:251 | 10/h | YES | Global 200/h, DACH-Whitelist, 24h-CRM-Dedup, Name-Regex |
| `GET /demo/templates` | demo.ts:203 | default | — | — |
| `GET /calendar/google/callback` | calendar.ts:1217 | default | — | HMAC-State + Nonce-Replay |
| `GET /calendar/microsoft/callback` | calendar.ts:1504 | default | — | HMAC-State + Nonce-Replay |

---

## Verbundene Notes

- [[Backend-Auth-Security]] — `crypto.ts` (AES-GCM) für OAuth-Tokens + Cal.com-Keys, `./auth.js:JwtPayload`, `app.authenticate`
- [[Backend-Database]] — `calendar_connections`, `chipy_schedules`, `chipy_blocks`, `chipy_bookings`, `crm_leads` (Schema + Migrations + 90d-Cleanup)
- [[Backend-Voice-Runtime]] — `agent-runtime.ts:runAgentTurn`, `agent-tools.ts` (→ `findFreeSlots`, `bookSlot`), `retell-webhooks.ts` (→ `findFreeSlots`, `bookSlot`)
- [[Backend-Billing]] — `billing.ts` (→ `sendPlanActivatedEmail`, `sendPaymentFailedEmail`), `usage.ts` (→ `sendUsageWarningEmail`)
- [[Backend-CRM]] — `crm_leads` Insert in `demo.ts:306`, Sales-Callback-Flow
- [[Backend-Outbound]] — `outbound-agent.ts:623` teilt sich `getOrCreateSalesAgent`

---

## Mermaid – Dataflow

```mermaid
flowchart TB
    subgraph Public[Public / No-Auth]
        contact[/POST /contact/]
        demoCall[/POST /demo/call/]
        demoCb[/POST /demo/callback/]
        gCb[/GET /calendar/google/callback/]
        msCb[/GET /calendar/microsoft/callback/]
    end

    subgraph Authed[JWT-Auth]
        chat[/POST /chat/]
        calStatus[/GET /calendar/status/]
        calcomConn[/POST /calendar/calcom/connect/]
        chipyCRUD[/CRUD /calendar/chipy/*/]
    end

    subgraph Services[External]
        resend[(Resend)]
        gcal[(Google Calendar)]
        msgraph[(MS Graph)]
        calcom[(Cal.com)]
        turnstile[(Turnstile)]
        retell[(Retell)]
    end

    subgraph DB[(Postgres)]
        conns[calendar_connections]
        chipy[chipy_* tables]
        leads[crm_leads]
    end

    subgraph Redis[(Redis)]
        budget[budget:chat:*]
        oauth[oauth_state_used:*]
        locks[cal:refresh:*]
        demoCache[demo_agent:*]
    end

    contact -->|sanitize headers| resend
    demoCall --> turnstile
    demoCall --> demoCache
    demoCall --> retell
    demoCb --> turnstile
    demoCb --> leads
    demoCb --> retell
    gCb -->|HMAC+nonce| oauth
    gCb -->|AES-GCM tokens| conns
    msCb -->|HMAC+nonce| oauth
    msCb -->|AES-GCM tokens| conns

    chat --> budget
    chat -->|runAgentTurn| retell
    calStatus --> conns
    calStatus --> gcal
    calStatus --> msgraph
    calStatus --> calcom
    calcomConn -->|validate /v1/me| calcom
    calcomConn -->|AES-GCM api_key| conns
    chipyCRUD --> chipy

    subgraph AgentTools[agent-tools.ts / retell-webhooks.ts]
        findSlots[findFreeSlots]
        book[bookSlot]
    end

    findSlots --> conns
    findSlots --> chipy
    findSlots --> gcal
    findSlots --> msgraph
    findSlots --> calcom
    book --> conns
    book --> chipy
    book --> gcal
    book --> msgraph
    book --> calcom

    emailFns[email.ts functions]
    emailFns --> resend
    emailFns -.-> |auth.ts signup/reset/verify| chat
    emailFns -.-> |billing.ts webhooks| chat
    emailFns -.-> |usage.ts 80%/100%| chat

    getValidToken -.-> locks
    getValidMsToken -.-> locks
    conns -.->|decrypt via crypto.ts| findSlots
    conns -.->|decrypt via crypto.ts| book
```

---

## Offene Punkte / Gaps aus dem Read

- `sendTicketNotification` (`email.ts:119`) hat KEINEN Caller im Codebase (ggf. toter Code oder geplantes Feature).
- `/contact` nutzt KEIN Turnstile — nur Rate-Limit 5/10min. Konsistent mit `/demo/*` wäre ein Turnstile-Gate.
- `bookSlotForConnection` (`calendar.ts:1051`) nutzt bei Cal.com-Pfad `eventTypes[0]` ohne Matching auf `service` → potenzielle UX-Irritation wenn Kunde mehrere Event-Types hat.
- Microsoft-Path benutzt für Slot-Generierung `email` aus conn-row, das ist beim Falsch-Case unbound.
- Chipy-Slots verwenden nur `startH` / `endH` und ignorieren Minuten-Anteil von Schedule (z.B. `09:30` wird als `9` interpretiert) — `calendar.ts:633-634` liest nur das erste Array-Element.

---

## Verwandt

- [[Phonbot/Phonbot-Gesamtsystem|🧭 Gesamtsystem]] · [[Phonbot/Overview|Phonbot Overview]]
- **Abhängig von:** [[Backend-Auth-Security]] (AES-256-GCM crypto.ts für OAuth/Cal-Tokens), [[Backend-Database]] (`calendar_connections`, `chipy_*`, `crm_leads`), [[Backend-Agents]] (Demo-Templates)
- **Wird genutzt von:** [[Backend-Voice-Telephony]] (Retell-Tool `calendar.findSlots/book`), [[Backend-Outbound]] (`/outbound/website-callback` triggert email)
- **Frontend:** [[Frontend-Pages]] (CalendarPage, TicketInbox, Landing CallbackSection/DemoSection)
- **Findings:** [[Audit-2026-04-18-Deep]] H5 (God-Object calendar.ts 1745 LOC), [[Audit-2026-04-18-Bugs]] H7 (timestamp-Mix DST)
