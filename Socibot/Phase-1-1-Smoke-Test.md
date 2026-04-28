---
title: Phase 1.1 OAuth — Smoke-Test-Plan
type: test-plan
phase: 1.1
created: 2026-04-29
related:
  - "[[kanban/02-meta-oauth-phase-1-1]]"
---

# Phase 1.1 Smoke-Test — Meta OAuth End-to-End

Manueller End-to-End-Test, **bevor** Phase 1.1 als shipped markiert wird. Wird mit einem Meta Test-User durchgeführt (App im Development-Mode), nicht mit echten Customer-Accounts.

## Vorbereitung

### Server-Side
- [ ] `pip install -r requirements.txt` — bringt `flask-wtf` und `filelock` mit
- [ ] `.env` befüllt mit `META_APP_ID`, `META_APP_SECRET`, `META_REDIRECT_URI=http://localhost:5000/auth/meta/callback`, `META_API_VERSION=v22.0`
- [ ] Erststart: `SOCIBOT_FERNET_KEY`, `SOCIBOT_HMAC_SECRET`, `SECRET_KEY` werden autogeneriert + in `.env` persistiert (verifizieren!)
- [ ] `client/connections.json` ist in `.gitignore` und nicht commited
- [ ] Server startet ohne Errors. Log enthält:
  - `[csrf] CSRFProtect aktiv`
  - keine ImportError für filelock

### Meta-Side (siehe `docs/META_APP_SETUP.md`)
- [ ] Meta App im Dev-Mode angelegt, App-Type "Business"
- [ ] Facebook Login for Business + Instagram Graph API als Produkte hinzugefügt
- [ ] OAuth Redirect-URI byte-genau registriert: `http://localhost:5000/auth/meta/callback`
- [ ] App-Roles: 1-2 Test-User angelegt (Roles → Test Users → Add)
- [ ] Test-User hat eine eigene Test-FB-Page (automatisch beim Anlegen)
- [ ] Falls IG getestet wird: IG Business Account mit Test-FB-Page verbunden

---

## TC-01 — Happy-Path End-to-End

**Ziel:** Frischer User connected → Page wählen → Post veröffentlichen → Disconnect.

1. **Login** als frischer Test-User in Socibot (`/register` → `/fragebogen` durchklicken).
2. Navigiere zu **`/einstellungen/marke`**.
   - **Erwartet:** Meta-Card zeigt "Mit Meta verbinden"-Button (lila-Akzent), KEIN grünes Status-Badge.
3. **Klick auf "Mit Meta verbinden"**.
   - **Erwartet:** Redirect zu `https://www.facebook.com/v22.0/dialog/oauth?client_id=...&scope=pages_show_list,pages_manage_posts,...,instagram_manage_insights&...`.
   - URL-Check: `business_management` ist NICHT in den Scopes.
4. **Login bei Meta als Test-User**, alle Permissions akzeptieren (NICHT Häkchen abwählen).
5. **Erwartet:** Redirect zurück zu `/auth/meta/callback?code=...&state=...`, dann `/auth/meta/select-page`.
6. Page-Selector zeigt **mindestens eine Page** mit Name + IG-Badge (falls verbunden).
7. **Klick auf "Auswählen"** bei der Test-Page.
   - **Erwartet:** Redirect zu `/einstellungen/marke?connected=meta`. Grünes Banner "Meta verbunden!" oben.
   - Meta-Card zeigt Status-Badge "✓ Verbunden als {{ ig_username or page_name }}" + "Trennen"-Button.
8. **Verifiziere `client/connections.json`:**
   - User-Bucket existiert mit Keys `_meta_user`, `facebook`, optional `instagram`.
   - `_meta_user.access_token_encrypted` ist Fernet-Ciphertext (NICHT Plaintext-Token).
   - Alle Connection-Dicts haben `expires_at` ~60d in der Zukunft.
9. **Verifiziere Browser-DevTools → Application → Cookies/Storage:**
   - Cookie `session` ist gesetzt. **Im Cookie-Wert (decoded) darf KEIN `user_token` stehen** (P1-1-Fix).
10. **Post-Test:** Erstelle einen FB-Post via Composer → "Post now". Checke Test-FB-Page-Wall.
    - **Erwartet:** Post erscheint live.
11. **Disconnect:** Klick auf "Trennen"-Button bei FB-Card → Confirm-Dialog → bestätigen.
    - **Erwartet:** Status-Badge weg, "Mit Meta verbinden"-Button zurück.
    - **Verifiziere:** `connections.json` enthält den User-Bucket nicht mehr (oder zumindest kein `facebook`-Eintrag).
    - **Bei Meta nachschauen:** Settings → Apps → Socibot → wenn revoke geklappt hat: App nicht mehr gelistet.

---

## TC-02 — Edge: User bricht OAuth-Dialog ab

1. Klick auf "Mit Meta verbinden".
2. Bei Meta: **"Cancel" / "Abbrechen"** klicken.
3. **Erwartet:** Redirect zu `/auth/meta/callback?error=access_denied&...`.
4. Render der Error-Page mit Text "Du hast den Zugriff bei Meta nicht erteilt. Klicke erneut auf 'Mit Meta verbinden' und bestätige alle Berechtigungen."
5. Keine Connection in `connections.json` angelegt.

---

## TC-03 — Edge: User declines Permission im Dialog

1. Klick auf "Mit Meta verbinden".
2. Bei Meta: **Häkchen abwählen** für `pages_manage_posts` (oder eines der REQUIRED_SCOPES).
3. Permissions submitten.
4. **Erwartet:** Permission-Verify-Block im `/callback` greift. Render Error-Page "Du hast nicht alle nötigen Berechtigungen erteilt. Fehlende Scopes: pages_manage_posts. Bitte erneut verbinden und ALLE Berechtigungen aktiviert lassen.", HTTP 400.
5. Keine Connection angelegt.

---

## TC-04 — Edge: User hat keine FB-Page

Test-User ohne FB-Page anlegen oder bestehende Pages temporär entfernen.

1. Klick "Mit Meta verbinden" → Login → akzeptieren.
2. **Erwartet:** Page-Selector zeigt Error-State: "Keine Facebook-Seite gefunden — Erstelle zuerst eine FB-Seite und verbinde deinen Instagram Business Account damit, dann starte den Verbindungsvorgang erneut."

---

## TC-05 — Edge: Page ohne IG-Account

User mit FB-Page aber **ohne** verknüpften IG Business Account.

1. OAuth-Flow durchgehen.
2. **Erwartet:** Page-Selector zeigt FB-Page-Card aber ohne IG-Badge. Banner-Warnung: "Keine deiner Facebook-Seiten hat einen verknüpften Instagram Business Account..."
3. Auswahl funktioniert; nur FB-Connection wird angelegt, kein `instagram`-Eintrag in `connections.json`.

---

## TC-06 — Single-Tenant-Takeover

1. User A connected → Posts laufen → `active_connection_user_id` in `bot_settings.json` zeigt User A.
2. User B (anderer Account) loggt ein, klickt "Mit Meta verbinden", durchläuft Flow.
3. Bei Page-Auswahl: **Erwartet** Confirm-Takeover-Dialog "Es gibt bereits eine andere aktive Verbindung — Übernehmen oder Abbrechen?"
4. Bestätigen.
5. **Erwartet:**
   - `active_connection_user_id` zeigt jetzt User B.
   - `client/notifications.json` enthält neuen Eintrag mit `user_id: <user_a_id>`, `type: "meta_takeover"`.
   - User A's Inbox/Postfach zeigt diese Notification beim nächsten Login.

---

## TC-07 — Repick (andere Page wählen)

User hat schon connected, will andere Page wählen.

1. `/auth/meta/repick` aufrufen (Link in marke.html — falls UI existiert; sonst direkt URL).
2. **Erwartet:** Pages werden via `get_meta_user_token` → `/me/accounts` neu gefetcht (NICHT via Page-Token — der hätte falsche Scope-Semantik).
3. Selector erscheint. Andere Page wählen → bestehende Connection wird überschrieben.

---

## TC-08 — CSRF-Schutz

**Negativtest** — bestätigt dass CSRF aktiv ist.

```bash
curl -X POST http://localhost:5000/auth/meta/disconnect \
  -H "Content-Type: application/json" \
  --cookie "session=<gültige-session>" \
  -d '{"platform":"facebook"}'
```

**Erwartet:** HTTP 400 (oder 403) "The CSRF token is missing." Wird von flask-wtf abgefangen, BEVOR der Route-Handler läuft.

Mit gültigem `X-CSRFToken`-Header (aus `<meta name="csrf-token">` der HTML-Page geholt): muss durchlaufen, HTTP 200 + `{ok: true}`.

---

## TC-09 — Token-Expiry-Banner (proaktive UX)

**Setup:** In `connections.json` manuell den `_meta_user.expires_at` auf einen Wert <14d in der Zukunft setzen, dann **neu starten / Page reloaden**.

1. Navigiere zu `/einstellungen/marke`.
2. **Erwartet:** Gelbes Warning-Banner über der OAuth-Card: "Meta-Token läuft in N Tagen ab. Erneuere die Verbindung um Posting-Unterbrechungen zu vermeiden. [Jetzt erneuern →]".
3. Setze `expires_at` auf Vergangenheits-Datum → reload → **Erwartet:** Roter Error-Banner "Meta-Verbindung abgelaufen. Posts werden nicht mehr veröffentlicht."

---

## TC-10 — 190/102-Handler im Poster (Token-Invalid)

**Setup:** Manuell den `_meta_user.access_token_encrypted` in `connections.json` korrumpieren (1 Zeichen ändern), oder bei Meta die App-Permissions widerrufen während Connection lokal aktiv bleibt.

1. Trigger Post via Composer "Post now".
2. **Erwartet:**
   - Meta antwortet mit `{"error":{"code":190,...}}`.
   - `_check_meta_oauth_error` greift in `bot/poster.py` → `mark_connection_invalid` wird aufgerufen.
   - `connections.json` für die `facebook`-Connection: `token_status: "invalid"`, `invalid_reason: "OAuth token invalid"`, `invalid_at: <timestamp>`.
   - Admin-Notification per `notification_service.push` mit Subject "Meta-Connection invalid".
3. Reload `/einstellungen/marke`: Banner "Meta-Token ungültig: ... [Erneut verbinden →]".

---

## TC-11 — Nightly Refresh-Job

**Setup:** `_meta_user.expires_at` auf einen Wert <14d in der Zukunft setzen.

1. Manuell ausführen:
   ```bash
   python -c "from bot.jobs.refresh_meta_tokens import refresh_meta_tokens_job; print(refresh_meta_tokens_job())"
   ```
2. **Erwartet:**
   - Token wird via `fb_exchange_token` refreshed (neues `expires_at` ~60d).
   - `/me/accounts` wird neu gefetcht → frische Page-Tokens.
   - `connections.json`: `_meta_user`, `facebook` (und ggf. `instagram`) haben neue `access_token_encrypted` + neues `expires_at`/`token_expires_at`.
   - Output: `{refreshed: 1, failed: 0, errors: []}`.

---

## TC-12 — Account-Delete (DSGVO Art. 17)

1. Login als Test-User mit Verbindungen + Posts.
2. Navigiere zu `/einstellungen/konto`.
3. Tippe "LÖSCHEN" ins Confirm-Feld → Submit.
4. **Erwartet:**
   - Meta `revoke_permissions` wird best-effort aufgerufen (Log: `[meta_oauth] DELETE /me/permissions`).
   - User wird aus `users.json` entfernt.
   - User-Bucket aus `connections.json` entfernt (inklusive `_meta_user`).
   - User-spezifische Einträge in `conversations.json` und `notifications.json` entfernt.
   - `active_connection_user_id` cleared falls dieser User aktiv war.
   - Session destroyed, Redirect zu `/landing?account_deleted=1`.

---

## TC-13 — SECRET_KEY-Persistenz (Multi-Worker-Safety)

1. `.env` enthält `SECRET_KEY` (autogeneriert beim ersten Start).
2. Server stoppen + neu starten.
3. **Erwartet:** Bestehende Sessions bleiben gültig (User muss sich nicht neu einloggen).
4. **Erwartet auch:** `.env` zeigt **denselben** `SECRET_KEY` wie vorher — nicht ein neuer.

---

## TC-14 — Retention-Job

**Setup:** In `connections.json` manuell den `_meta_user.expires_at` auf >90d in der Vergangenheit setzen.

1. Manuell ausführen:
   ```bash
   python -c "from bot.jobs.retention import cleanup_expired_connections_job; print(cleanup_expired_connections_job())"
   ```
2. **Erwartet:** Connection wird gelöscht. Output: `{cleaned: 1, errors: []}`.

---

## Acceptance: Phase 1.1 = shipped wenn

- [ ] TC-01 bis TC-14 alle GREEN
- [ ] App-Log enthält keinen einzigen Token-Plaintext (grep auf `EAA` und `access_token=`)
- [ ] `client/connections.json` in `.gitignore`, nicht commited
- [ ] Operator-Doku `docs/META_APP_SETUP.md` Step-by-Step funktioniert (zweiter Operator validiert)
- [ ] Bekannt: für **Live Customers** vor Customer-Launch zusätzlich Meta App Review starten (Phase 1.1 läuft im Dev-Mode mit Test-Users)

## Bekannte Beschränkungen (akzeptiert)

- **Single-Tenant:** Active-User-Pattern. Beim Übergang zu Multi-Tenant (Phase 2) wird `connections_service.resolve_token` pro User aufgelöst statt single global. Migration ist additiv (kein Breaking Change am Public-API).
- **filelock optional:** Bei fehlender Installation läuft cross-process-Safety nicht. Standard-Setup mit gunicorn workers=1 ist ok; ab workers>1 zwingend `pip install filelock`.
- **DM-Scopes Phase 1.2:** `pages_messaging` und `instagram_manage_messages` sind bewusst NICHT in 1.1. Auto-Reply-Send + Webhook-Listener kommen in Phase 1.2 mit separater App-Review-Einreichung.
- **Page-Token-Refresh:** Page-Tokens werden NICHT direkt refreshed (Meta-API erlaubt nur User-Token-Refresh). Nightly Job refresht User-Token + re-fetcht `/me/accounts` für frische Page-Tokens.
