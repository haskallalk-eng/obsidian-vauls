---
id: 2
status: doing
priority: High
blocked_by: []
tags:
  - socibot
  - oauth
  - meta
  - dod-blocker
created: 2026-04-28
updated: 2026-04-28
---

# Phase 1.1 — Meta OAuth (Instagram + Facebook)

DoD-Blocker #1 aus der Gap-Analyse: Kunde soll **ohne API-Key-Eingabe** seine IG/FB-Konten verbinden. Aktuell muss er Tokens händisch aus `developers.facebook.com` rauskopieren — genau das killen wir.

## Job Story
**When** ein Kunde Socibot zum ersten Mal einrichtet, **I want to** dass er nur auf "Mit Meta verbinden" klickt, sich bei Facebook einloggt und seine Page wählt, **so I can** ihn ohne technische Hürde aktivieren.

## Acceptance Criteria
- [ ] Per-User Connection-Store mit Fernet-Encryption (`client/connections.json`, AES via `cryptography.fernet`)
- [ ] `/auth/meta/connect` — generiert HMAC-signierten State, redirect zu Meta OAuth Dialog
- [ ] `/auth/meta/callback` — Code → Long-Lived User-Token → `/me/accounts` → Page-Liste
- [ ] `/auth/meta/select-page` — User wählt Page(s), Connection persistiert
- [ ] `/auth/meta/disconnect` — lokal löschen + `DELETE /me/permissions` an Meta (revoke)
- [ ] `/auth/meta/repick` — andere Page wählen ohne kompletten Reconnect
- [ ] Token-Resolver `connections_service.resolve_token(platform)` — lazy, von poster/scheduler aufgerufen, NICHT `load_config()`-Hook
- [ ] Auto-Refresh APScheduler-Job, daily 03:00, refresht Tokens mit `expires_at < now + 14d`
- [ ] `setup.html` Step 3 + `marke.html`: IG/FB-Token-Inputs ersetzt durch CTA + Status-Badge
- [ ] `bot_settings.json` bekommt `active_connection_user_id` (kein last-write-wins; Bestätigungs-Dialog wenn 2. User verbindet)
- [ ] `.env.example`: `META_APP_ID`, `META_APP_SECRET`, `META_REDIRECT_URI`, `SOCIBOT_FERNET_KEY`
- [ ] `docs/META_APP_SETUP.md` — Walkthrough für Operator (Meta App Console, Redirect-URI, Test-User vs. Live)
- [ ] Edge-Case dokumentiert: IG ohne FB-Page → klare Fehlermeldung im Selector

## Architektur

### 1. Storage: `client/connections.json` mit Fernet
Schema (per User):
```json
{
  "<user_id>": {
    "instagram": {
      "access_token": "<encrypted>",
      "account_id": "...",
      "page_id": "...",
      "ig_username": "@firma",
      "page_name": "Firma GmbH",
      "token_expires_at": "2026-06-27T...",
      "connected_at": "2026-04-28T...",
      "meta_user_id": "..."
    },
    "facebook": {...}
  }
}
```
Fernet-Key in `.env` als `SOCIBOT_FERNET_KEY`. Bei Erststart fehlt → autogen via `Fernet.generate_key()` + zurückschreiben in `.env`.

**Echter Grund für Encryption (nicht DSGVO-Theater):** `connections.json` landet versehentlich in Git, Backups, Log-Dumps, `tar`-Archiven. Plaintext = Token-Leak. Fernet macht das harmlos. Migration später teurer als jetzt.

### 2. Token-Resolution lazy, nicht via `load_config()`
**Reviewer-Feedback:** `load_config()`-Hook ist versteckte Kopplung — Reload nach Reconnect, mutierender globaler State, Refresh unmöglich elegant.

**Stattdessen:** `connections_service.resolve_token(platform) -> {token, account_id, ...} | None`. Wird in `bot/poster.py` und `bot/scheduler.py` an genau den Stellen aufgerufen, wo Posts gesendet werden. Eine Zeile pro Plattform. Bestand bleibt ~95% unangetastet, Refresh wird trivial (Resolver checkt `expires_at` lazy bei jedem Call).

### 3. Single-Tenant-Safety
Aktuell läuft der Scheduler-Thread ohne Flask-Session → er muss wissen, *welche* Connection er nutzt. Nicht last-write-wins (Footgun: User B verbindet → User A's geplante Posts gehen plötzlich auf User B's Page = potenzielles Datenleck).

**Stattdessen:** `bot_settings.json` → `active_connection_user_id`. Beim ersten Connect: dieser User wird active. Beim 2. Connect-Versuch eines anderen Users: Bestätigungs-Dialog ("Es gibt bereits eine aktive Verbindung — übernehmen oder abbrechen?"). Multi-Tenant kommt in Phase 2.

### 4. OAuth-Flow konkret
```
GET /auth/meta/connect
  → state = hmac_sha256(user_id + nonce + ts, SECRET_KEY)
  → 302 https://www.facebook.com/v18.0/dialog/oauth?
        client_id=META_APP_ID
        &redirect_uri=META_REDIRECT_URI
        &state=<state>
        &scope=pages_show_list,pages_manage_posts,pages_read_engagement,pages_manage_engagement,instagram_basic,instagram_content_publish,instagram_manage_comments,business_management
        &response_type=code

GET /auth/meta/callback?code=...&state=...
  → state-HMAC validieren (CSRF)
  → POST /v18.0/oauth/access_token (Code → Short-Lived User-Token)
  → GET /v18.0/oauth/access_token?grant_type=fb_exchange_token (→ Long-Lived 60d)
  → GET /me/accounts (→ Pages mit Long-Lived Page-Tokens)
  → Für jede Page: GET /<page_id>?fields=instagram_business_account
  → Render Page-Selector

POST /auth/meta/select-page {page_id}
  → connections_service.save_user_connection(user_id, "facebook", {...})
  → save IG conn falls page hat ig_business_account
  → Wenn 1. User: setze active_connection_user_id
  → Wenn 2. User: render Bestätigungsdialog vor Save
  → 302 /einstellungen/marke

POST /auth/meta/disconnect
  → DELETE /me/permissions an Meta (revoke)
  → connections_service.delete_user_connection
```

### 5. Scopes — bewusst ohne `pages_messaging` und `instagram_manage_messages`
Reviewer-Punkt: DM-Scopes triggern App-Review **deutlich härter** (Live-Demo + Privacy-Policy-Review). Phase 1.1 = Posting + Comments. DMs in Phase 1.2 wenn Auto-Reply-Send-Logik ohnehin gebaut wird.

### 6. Auto-Refresh-Job
APScheduler `daily 03:00`: für jede Connection mit `expires_at < now + 14d` → `oauth/access_token?grant_type=fb_exchange_token`. Failed refresh → Notification an User per E-Mail (`notification_service`). Killt eine ganze Klasse stiller Fehler ("Posts gehen seit 2 Wochen nicht raus weil Token abgelaufen").

## Risiken

| Risiko | Mitigation |
|---|---|
| Meta App Review für Production | Dev-Mode + Test-Users genügen für jetzt. Review erst vor echtem Customer-Launch. |
| `redirect_uri` Mismatch (Localhost vs. Prod) | `META_APP_SETUP.md` dokumentiert beide URIs als separate Einträge. |
| State CSRF wenn Flask-Session-Storage | HMAC-signierter State (selbst-validierend), kein Session-Storage. |
| User-B-Connect überschreibt User-A | `active_connection_user_id` in bot_settings + Confirm-Dialog. |
| IG ohne FB-Page existiert nicht | Selector zeigt klare Fehlermeldung wenn Pages-Liste leer oder keine Page IG-verknüpft. |
| Webhook-Subscription nicht in 1.1 | Polling akzeptiert für MVP, dokumentiert. Phase 2 = Meta Webhooks. |

## Files

**NEW:**
- `dashboard/services/connections_service.py` — Storage + Resolver + Encryption
- `dashboard/routes/oauth_meta.py` — connect/callback/select-page/disconnect/repick
- `dashboard/templates/oauth_meta_select.html` — Page-Selector
- `docs/META_APP_SETUP.md` — Operator-Walkthrough

**MOD:**
- `bot/config.py` — KEIN Hook; bleibt unverändert (lazy-Resolver-Approach)
- `bot/poster.py` — `connections_service.resolve_token("instagram"|"facebook")` an Post-Stellen
- `bot/scheduler.py` — gleiches für Poll-Stellen
- `dashboard/__init__.py` — `oauth_meta_bp` registrieren
- `.env.example` — `META_APP_ID`, `META_APP_SECRET`, `META_REDIRECT_URI`, `SOCIBOT_FERNET_KEY`
- `dashboard/templates/setup.html` — IG/FB-Section → CTA-Button
- `dashboard/templates/marke.html` — gleiche Ersetzung
- `dashboard/routes/brand_settings.py` — `_build_token_status` checkt connections + .env
- `bot/scheduler.py` — APScheduler `daily 03:00` Auto-Refresh-Job

## Related
- [[Socibot/Overview]]
- [[Socibot/modules/19-Connections]]
- DoD-Gap-Analyse 2026-04-28 (Conversation-Log)

## Narrative
- 2026-04-28: Erstellt nach DoD-Gap-Analyse (62% Reifegrad, OAuth ist Top-Blocker). Plan extern reviewed (Plan-Subagent), Feedback eingearbeitet: lazy Token-Resolution statt load_config-Hook, Fernet-Encryption von Anfang an, Scope-Reduktion (DMs raus), HMAC-State, Token-Revoke bei Disconnect, Auto-Refresh-Job, active_connection_user_id statt last-write-wins. (by @termi)
- 2026-04-28: Quality-Pipeline aktiviert — `connections_service.py` als Foundation gebaut (Fernet, lazy resolver, HMAC-state, iter_meta_connections), parallel dispatched: Plan-Re-Review (Reviewer #2), Code-Review von connections_service.py, plus 4 Implementation-Tracks (oauth-route, UI-refactor, poster/scheduler-wiring + APScheduler-refresh-job, docs+env). Nach Return: pro Track ein Code-Reviewer + security-dsgvo-reviewer. (by @termi)

- 2026-04-28 — **Review-Findings integriert (Critical Issues)**:
  - **Race-Condition im `resolve_token`**: zwei Threads konnten parallel refreshen + überschreiben. Fix: atomares `_lock` um `_needs_refresh + Refresh + Save`-Block.
  - **Fernet-Key war HMAC-Secret**: Key-Sharing-Anti-Pattern. Fix: separates `SOCIBOT_HMAC_SECRET` autogeneriert.
  - **State-Parser brach bei Punkten in user_id**: `state.split(".")` mit count-Check. Fix: `|`-Separator + base64-uid + `split("|")` mit `len(parts)==4`-Check.
  - **`_get_fernet` Init-Race**: zwei Threads konnten parallel Key autogenerieren. Fix: `_init_lock` mit Double-Checked-Locking.
  - **`_write_env_key` ohne Lock**: gunicorn-multi-worker-Race. Fix: `_env_lock`.
  - **Page-Token vs User-Token Confusion**: Page-Tokens sind nicht via `fb_exchange_token` refreshbar — nur User-Tokens. Fix: User-Token separat unter `_meta_user`-Key gespeichert (`save_meta_user_token` / `get_meta_user_token`); Refresh re-fetcht `/me/accounts` → frische Page-Tokens.
  - **Relative Paths**: CWD-abhängig. Fix: `Path(__file__).resolve().parent.parent.parent`.
  - **`_needs_refresh` bei fehlendem expires_at**: gab False zurück → kein Refresh. Fix: defensive True.
  - **Schema-Versioning fehlte**: kein Migrationspfad. Fix: `_schema_version: 1` Top-Level.
  - **`v18.0` hardcoded**: Meta deprecated aggressiv. Fix: `META_API_VERSION` ENV mit Default v18.0.
  - **Disconnect ohne Internet steckt fest**: synchron `DELETE /me/permissions`. Fix in oauth_meta.py: lokales Delete passiert immer, Meta-Revoke best-effort.
  - **OAuth-Route-Agent zurück** (alle Edge-Cases implementiert: Meta-Abbruch, leere Pages, Single-Tenant-Takeover, Repick, Token-Logging-Schutz). PATCH nötig: in `/callback` zusätzlich `save_meta_user_token(user_id, long_token, expires, meta_user_id)` aufrufen, damit der nightly Refresh-Job einen User-Token zum Refreshen hat.

- 2026-04-28 — **Quality-Pipeline ROUND 2** dispatched: 3 Implementer (UI-refactor, poster/scheduler-wiring + APScheduler-refresh, docs) + 6 Specialists (Alternative-Architektur-Explorer, Scope-Wachhund, Security-DSGVO-Reviewer, Industry-Best-Practices-Researcher, API-Version-Risk-Analyst, Code-Reviewer für OAuth-Route-Agent-Output). (by @termi)

- 2026-04-28 — **Round-2 Returns + Synthesis:**
  - **Implementer A (UI):** ✅ setup.html, marke.html, brand_settings.py mit OAuth-Cards + Status-Badges + Disconnect-Buttons. 3 Open Points: disconnect-Response-Format (Redirect statt JSON), Import-Pfad-Sanity, token_status-Counter.
  - **Implementer B (poster wiring + refresh-job):** ✅ poster.py + scheduler.py mit `resolve_token`-First-/.env-Fallback. `bot/jobs/refresh_meta_tokens.py` neu, registriert daily 03:01 (Codebase nutzt `schedule`-lib statt APScheduler — passt sich an). Open: `_apis`-Cache invalidiert nicht bei mid-run-Refresh (Single-Tenant ok).
  - **Implementer C (docs):** ✅ .env.example mit META_*-Section + DEPRECATED-Markern, `docs/META_APP_SETUP.md` 10-Sektionen-Walkthrough.
  - **Alt-Arch (D):** Verdict — passend für Phase 1.1, SQLite/SQLAlchemy bei Multi-Tenant, Connection-Broker erst bei separaten Deployments. **Sofort:** filelock für .env-Writes (gunicorn-multi-worker), Health-Endpoint, Audit-Trail.
  - **Scope-Wachhund (E):** **`business_management` raus** (nicht nötig für /me/accounts mit instagram_business_account-Field, halbiert App-Review-Zeit), **`instagram_manage_insights` rein** (vermeidet Re-Auth in Phase 2, gleiche Review-Kategorie). Phase-1.2-Vorbereitung: pages_messaging + instagram_manage_messages separater Review-Request, 14-30d.
  - **Security-DSGVO (F):** **BLOCK** — folgendes vor Ship fixen:
    - **P0** `client/connections.json` fehlt in .gitignore — Token-Leak-Vektor
    - **P1** Long-Lived User-Token im Flask-Session-Cookie nach Token-Exchange — sofort persisten via `save_meta_user_token`, nicht in Session legen
    - **P1** POST-Routes ohne CSRF-Tokens (SameSite=Lax mitigiert teilweise — flask-wtf trotzdem nachreichen)
    - **P1** 500-Handler leakt `str(e)` an Browser
    - **P1** SECRET_KEY autogen-Logik instabil — Sessions nach Restart kaputt, gunicorn-Workers haben verschiedene Keys
    - **P2** HMAC-State Replay-Schutz: Session-State-Check soft, soll hart abgelehnt werden
    - **P2** `/repick` nutzt Page-Token für `/me/accounts` — falsche Token-Semantik (User-Token erforderlich)
    - **P2** Disconnect löscht `_meta_user`-Bucket nicht wenn alle Plattform-Connections weg
    - **P2** Keine CSP-Header
    - **P3** `meta_oauth_service._BASE` hardcodet `v18.0` trotz `META_API_VERSION` env (v18 deprecated)
    - **DSGVO:** Retention-Policy für connections.json fehlt; Takeover ohne User-A-Notification (Transparenz Art. 5(1)(a)); Account-Delete-Flow Art. 17 fehlt; AVV mit Meta in Datenschutzerklärung dokumentieren

- 2026-04-28 — **Critical/High Patches angewendet** (Phase A):
  - `.gitignore` ergänzt um `client/connections.json` (P0)
  - `meta_oauth_service.py`: `_BASE` und `build_oauth_url` lesen `META_API_VERSION` env (Default v22.0, da v18 deprecated); `_SCOPES` aktualisiert: `business_management` raus, `instagram_manage_insights` rein
  - `connections_service.py`: `delete_user_connection` löscht `_meta_user` mit, wenn alle Meta-Plattformen weg (P2-4)
  - `dashboard/__init__.py`: SECRET_KEY autogen via `_ensure_env_secret` (P1-4); 500-Handler entfernt `{{ error }}` und loggt nur (P1-3); CSP-Header gesetzt (P2-3)
  - oauth_meta.py multi-patch in nächstem Step (P1-1 Token-aus-Session, P2-1 Hard-Session-State-Check, P2-2 /repick-User-Token, P2-4 _meta_user-Cleanup, Imports-Update). (by @termi)

- 2026-04-29 — **API-Version-Risk-Analyst (H) + Industry-Researcher (G) zurück:**
  - **H (CRITICAL):** v18.0 ist seit Jan 2026 SUNSET. `_BASE` in meta_oauth_service.py war hardcoded und ignorierte META_API_VERSION-ENV. Fix: `_API_VERSION = os.getenv("META_API_VERSION", "v22.0")` als Single-Source-of-Truth, `_BASE` und `build_oauth_url`-Dialog-URL nutzen es. Default v18.0 → v22.0 in connections_service.py auch geändert.
  - **H (Phase 1.2 Hinweis):** `instagram_content_publish` wird in `instagram_business_content_publish` umbenannt (alter Scope deprecated Jan 2025) — bei Phase-1.2-App-Review prüfen. `media_type=VIDEO` muss `REELS` sein (deprecated Nov 2023 für IG-Posts).
  - **H (Monitoring):** Error-Code 2635 = Version Sunset, 190 = Token Invalid, 100/33 = Endpoint Not Found, 4 = Rate Limit. Alert ab 3 Hits/10min.
  - **G (Industry-Patterns):** "Mit Meta verbinden"-Single-Button-Flow ✓ (haben wir), Page-Selector als Card-Liste ✓ (haben wir). **Adoption empfohlen:**
    - Search-Filter im Page-Selector ab >10 Pages
    - Disconnect-Confirm-Dialog mit klarem Wording ✓ (haben wir via JS confirm)
    - Token-Expiry-Banner im Dashboard 14d vorher (proaktiv > reaktive E-Mail à la Buffer)
    - **Permission-Scope-Verify im /callback** (Top-Vermeidung-Failure-Mode bei Buffer/Hootsuite — User unticken Permissions im Meta-Dialog)
    - 190/102-Handler im Poster: connection-invalid markieren + Reconnect-Alert
  - **G (App-Review-Tips):** Mixpost-Use-Case-Texte als Vorlagen für Permission-Begründungen, Demo-Video-Struktur 5-7min mit Permission-Annotations, NICHT future-use-Permissions einreichen.

- 2026-04-29 — **Phase-A-Patches angewendet** (Critical/High Security + Scope + API-Version):
  - `.gitignore` ergänzt um `client/connections.json` (P0)
  - `meta_oauth_service.py`: `_API_VERSION = os.getenv("META_API_VERSION", "v22.0")` Single-Source-of-Truth; `_SCOPES`: `business_management` raus, `instagram_manage_insights` rein
  - `connections_service.py`: `META_API_VERSION` Default v22.0; `delete_user_connection` löscht `_meta_user`-Bucket wenn alle Meta-Plattformen weg (P2-4)
  - `dashboard/__init__.py`: SECRET_KEY autogen via `_ensure_env_secret` (P1-4); 500-Handler entfernt `{{ error }}` und loggt nur (P1-3); CSP-Header gesetzt (P2-3)

- 2026-04-29 — **Phase-B-Patches** (oauth_meta.py multi-patch):
  - Imports: private `_load_settings/_save_settings/_settings_lock` raus; `clear_active_user_id`, `get_meta_user_token`, `save_meta_user_token` rein
  - `/callback`: Long-Lived User-Token wird SOFORT via `save_meta_user_token` persistiert (Fernet-encrypted at rest), NICHT mehr in Session-Cookie geschrieben (P1-1 fixed)
  - `/callback`: Session-State-Check HART ablehnen wenn missing/mismatch (P2-1 Replay-Schutz)
  - `/repick`: nutzt `get_meta_user_token` statt Page-Token für `/me/accounts`-Aufruf (P2-2)
  - `/disconnect`: nutzt clean `set_active_user_id`/`clear_active_user_id` API statt private Internals

- 2026-04-29 — **Offene Tasks** (Tasks #11-#16 erstellt):
  - CSRF-Tokens auf POST-Routes (flask-wtf) — P1-2
  - Permission-Scope-Verify im /callback — Industry G + Failure-Mode-Vermeidung
  - Token-Expiry-Banner im Dashboard — Industry G
  - 190/102-Handler im Poster — Industry G
  - DSGVO: Account-Delete + Retention + AVV-Doku — DSGVO-4/5/6
  - filelock für .env-Writes (gunicorn-multi-worker) — Alt-Arch D + Security
  - End-to-end Smoke-Test mit Meta Test-User

- 2026-04-29 — **Quality-Pipeline ROUND 3** abgeschlossen — 4 parallele Hardening-Agents:
  - **CSRF (#11)** ✅ flask-wtf in requirements + CSRFProtect global init in __init__.py + csrf_token in allen POST-Forms (oauth_meta_select.html) + X-CSRFToken-Header in Disconnect-Fetch-Calls (marke.html, setup.html). Meta-Tag `<meta name="csrf-token">` in base.html + setup.html. Graceful degradation falls flask-wtf nicht installiert.
  - **Hardening-Bundle (#12, #14, #16)** ✅
    - `filelock` cross-process Lock auf .env, connections.json, bot_settings.json (graceful fallback auf threading-only wenn filelock nicht installiert)
    - `mark_connection_invalid(user_id, platform, reason)` in connections_service.py
    - 190/102-OAuthException-Erkennung in poster.py via `_check_meta_oauth_error`-Helper (Stops Retry, markiert Connection invalid, pusht Admin-Notification)
    - `REQUIRED_SCOPES` + `OPTIONAL_SCOPES` in meta_oauth_service.py + `get_me_permissions()`
    - Permission-Verify im /callback (warning-and-continue bei API-Errors, hard-block nur bei explicit declined)
  - **DSGVO-Bundle (#15)** ✅
    - NEU `dashboard/routes/account.py` GET/POST `/einstellungen/konto/loeschen` mit 9-Schritt-Delete (revoke at Meta + delete connections + clear conversations/notifications + clear active_user + delete user + session.clear)
    - NEU `dashboard/templates/account.html` mit Confirm-Input "LÖSCHEN" + JS-Guard
    - NEU `bot/jobs/retention.py` `cleanup_expired_connections_job()` — daily 04:00 schedule, löscht Tokens >90d nach expires_at
    - `confirm_takeover` schickt Notification an alten Active-User (`type: "meta_takeover"` in notifications.json)
    - `connections_service.delete_user_meta_token` + `user_service.delete` als Public Helpers
    - NEU `docs/DSGVO_NOTES.md` mit AVV-Vorlagentexten (Meta Platforms Ireland, Art. 6(1)(b), EU-US DPF, Art. 17 Recht auf Löschung, Retention-Erklärung)
  - **Banner (#13)** ⏳ Agent läuft (Token-Expiry-Banner für marke.html + setup.html)
  - **Smoke-Test-Plan (#10)** ✅ `Obsidian/Socibot/Phase-1-1-Smoke-Test.md` — 14 Test-Cases (Happy-Path + 13 Edge/Negative-Tests) + Acceptance-Criteria + bekannte Beschränkungen. Operator-Execution steht aus (Meta Test-Users müssen angelegt werden).

- 2026-04-29 — **PHASE 1.1 STATUS: FUNKTIONAL FERTIG** (vorbehaltlich Banner + Smoke-Test-Execution).
  - Erfüllt Customer-DoD-Punkt #1: "Kunde kann ohne API-Key-Eingabe Meta-Konten verbinden — Klick → Login → Page wählen → fertig"
  - Vorhanden für Phase 1.2 (DM-Reply): Architektur trägt, Scopes inkremental hinzufügbar, Webhooks fehlen noch, Auto-Send fehlt noch
  - Vor Customer-Launch nötig: Meta App Review (Live-Demo-Video + Privacy-Policy-Update — siehe `docs/META_APP_SETUP.md` Sektion 6+7)
