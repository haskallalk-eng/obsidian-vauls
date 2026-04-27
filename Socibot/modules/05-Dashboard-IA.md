---
title: 05 — Dashboard-IA
tags: [socibot, modul, dashboard, ia]
date: 2026-04-27
source_of_truth: code
---

# 05 — Dashboard-IA & Wiring

> Sidebar-Struktur (post-refactor 2026-04-27), Blueprint-Registrierung, `before_request`-Logik, IA-Map.

## Sidebar (Ist-Stand 2026-04-27 02:35, verifiziert via `dashboard/templates/base.html:487-518`)

```
─── Hauptbereich ─────────────────
  Dashboard            /
  Kalender             /calendar/
  Postfach             /postfach/

─── Erstellen ────────────────────
  Erstellen            /erstellen/    (Hub: → /composer/, → /video/)
  Mediathek            /media/        (Tabs: Fotos, Ideen)

─── Wachstum ─────────────────────
  Analytics            /analytics/

─── System ───────────────────────
  Marke                /einstellungen/marke
  Billing              /billing/

─── Footer ───────────────────────
  Neuen Kunden einrichten →  /fragebogen
```

**Aus der Sidebar entfernt** in dieser Session, aber Routes bleiben aktiv:
- `/autopilot/` — Stats jetzt im Calendar-Header (`calendar.py:107-120`)
- `/einstellungen/setup` — first-run-only Redirect
- `/composer/`, `/video/` — von `/erstellen/`-Hub verlinkt
- `/landing` — eigene Public-Route
- `/kunden-vorschau/` — public Client-Approval-Page
- `/lernen/` — Learning-Profile-Verwaltung
- `/vorschau/` — Approval-Wizard (verlinkt von Calendar-Detail-Pane)

## `dashboard/__init__.py` — Wiring

`create_app()` Z.20–159 macht:

1. **Flask-App** mit `template_folder="templates"` (Z.21)
2. **`SECRET_KEY`** aus ENV oder `secrets.token_hex(32)` (Z.22–23) — instabil zwischen Restarts wenn ENV nicht gesetzt
3. **Upload-Limit** 16 MB (`MAX_CONTENT_LENGTH`, Z.24)
4. **Custom 404 + 500 HTML** inline (Z.26–62)
5. **`@before_request` first-run-Redirect** Z.65–105:
   - **Skip-Liste** Z.69–81: `/einstellungen/setup`, `/einstellungen/token-speichern`, `/einstellungen/token-testen`, `/kunden-vorschau`, `/fragebogen`, `/landing`, `/billing`, `/static`, `/api/`, `/media/file/`, `/media/processed/`
   - **Schritt 1** Z.85–96: Wenn `client/brand_knowledge.json` fehlt oder `confirmed_by_user` und `brand_name` beide leer → Redirect `/fragebogen`
   - **Schritt 2** Z.98–104: Wenn `claude.api_key` Placeholder oder fehlt → Redirect `/einstellungen/setup`
6. **Security-Headers** Z.107–113: `X-Content-Type-Options`, `X-Frame-Options: SAMEORIGIN`, `X-XSS-Protection`, `Referrer-Policy: strict-origin-when-cross-origin`
7. **Brand-Context-Processor** Z.115–123: injiziert `brand_name` und `brand_industry` in jedes Template via `brand.foerderkraft_brand.get_brand()`
8. **Blueprint-Registrierung** Z.125–158 — 18 Blueprints inkl. neuem `erstellen_bp`

## Blueprint-Map

| Datei | Blueprint-Name | Prefix | Routes |
|---|---|---|---|
| `analytics.py` | analytics | /analytics | 1 |
| `api.py` | api | /api | 11 |
| `approval.py` | approval | /vorschau | 18 |
| `autopilot.py` | autopilot | *(root)* | 1 (`/autopilot/`) |
| `billing.py` | billing | /billing | 7 |
| `brand_settings.py` | brand_settings | /einstellungen | 8 |
| `calendar.py` | calendar | /calendar | 6 |
| `composer.py` | composer | /composer | 4 |
| `erstellen.py` | erstellen | /erstellen | 1 |
| `fragebogen.py` | fragebogen | /fragebogen | 2 |
| `landing.py` | landing | *(root)* | 1 (`/landing`) |
| `learning.py` | learning | /lernen | 4 |
| `media.py` | media | /media | 6 |
| `overview.py` | overview | *(root)* | 3 (`/`, `/api/log`, `/verlauf`) |
| `postfach.py` | postfach | *(root)* | 5 (`/postfach/*`) |
| `preview.py` | preview | /kunden-vorschau | 4 |
| `video.py` | video | *(root)* | 4 (`/video/*`) |

**Total: ~85 Routes.** Vollständige URL-Liste siehe `18-Routes-Map`.

## Authentication-Modell (verifiziert, knapp)

**Es gibt keine Login-/Session-Auth in den Routes.** Verifiziert durch:
- Keine `@login_required`/`@auth_required`-Decorator in irgendeiner Route-Datei
- Keine Session-Token-Validierung in `before_request`
- Einziger Schutz ist `before_request`-Redirect zur Onboarding-Sequence (Z.65–105)

→ **Single-Tenant-Annahme:** Socibot ist als Single-User-Self-Host konzipiert. Wer Zugriff auf den Server hat, hat Zugriff auf das Dashboard. ⚠️ Kritisch wenn das Dashboard öffentlich exponiert wird.

## Public Routes (sicherheitsrelevant)

Diese Routes sind in der Skip-Liste oder per Design öffentlich:
- `/landing`
- `/kunden-vorschau/` — externer Kunden-Approval (Read-only Preview + Approve/Reject)
- `/fragebogen`, `/fragebogen/submit` — Onboarding Form
- `/billing/webhook` — Stripe-Webhook (HMAC-signed via Stripe)
- `/api/notifications/*` — fragwürdig: ist auch öffentlich, weil `/api/` in Skip-Liste

→ **Findings-Item:** `/api/*` durchläuft den Onboarding-Skip — wenn jemand `/api/notifications` im Multi-Tenant-Szenario aufruft, gibt es keine Auth. Aktuell kein Risk weil Single-User, aber strukturell schwach.

## Auto-Refresh / Polling-Frequenzen

Verifiziert in Templates:

| Wo | Frequenz | Was wird gepollt |
|---|---|---|
| `base.html:681-682` | 60s | `/api/notifications` (Bell-Counter) |
| `overview.html:295,303` | 30s | `/api/log` (Bot-Log Tail) |
| `video.html:241-248` | 15s | `/video/queue` (aktive Jobs) |
| `composer.html:329` | bedarfsweise | `/composer/post-status/{jobId}` |
| `media.html` | bedarfsweise | `/media/status/{filename}` |

## Geänderte Files (2026-04-27 Session)

| File | Änderung |
|---|---|
| `dashboard/templates/base.html:487-518` | Sidebar IA-Refactor |
| `dashboard/routes/erstellen.py` | **neu** (34 LOC) |
| `dashboard/templates/erstellen.html` | **neu** (174 LOC) |
| `dashboard/__init__.py:140,158-159` | erstellen_bp registriert; Kommentar bei autopilot_bp |
| `dashboard/routes/media.py:32-58` | Tabs Fotos/Ideen, lädt sample_content.json |
| `dashboard/templates/media.html` | Tab-Switcher + Ideen-Panel |
| `dashboard/routes/calendar.py` | Monats-Grid + Autopilot-Stats inline (Imports `autopilot.py`) |
| `dashboard/templates/calendar.html` | Full Rewrite — Month-Grid statt Wochen-Akkordeon |

## Verbundene Notes

- [[Socibot/modules/06-Dashboard-Routes]] — Per-Blueprint-Tiefe
- [[Socibot/modules/08-Dashboard-Templates]] — Template-System
- [[Socibot/modules/18-Routes-Map]] — alle URL-Pfade vollständig
