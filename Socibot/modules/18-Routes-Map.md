---
title: 18 — Routes-Map (alle Pfade)
tags: [socibot, routes, urls]
date: 2026-04-27
source_of_truth: code
---

# 18 — Routes-Map (vollständig, code-belegt)

> ~85 Routes über 18 Blueprints. Reihenfolge: alphabetisch nach Prefix.

## Konvention

- **`(root)`** = Blueprint hat keinen URL-Prefix; Routen wie `/postfach/`, `/video/` werden direkt in der Blueprint registriert.
- **Auth?** = (P)ublic / (S)kip im before_request / sonst leer

## Vollständige Liste

### `(root)` — Overview-Blueprint (`overview.py`)

| Methode | Pfad | Handler | Auth | Template |
|---|---|---|---|---|
| GET | `/` | `overview()` | S (skip-after-onboarding) | `overview.html` |
| GET | `/api/log` | `log_tail()` | S | JSON |
| GET | `/verlauf/`, `/verlauf` | `history()` | S | `verlauf.html` |

### `(root)` — Autopilot-Blueprint (`autopilot.py`)

| GET | `/autopilot/` | `autopilot_page()` | | `autopilot.html` |

### `(root)` — Landing-Blueprint (`landing.py`)

| GET | `/landing` | `landing()` | P (Skip-Liste) | `landing.html` |

### `(root)` — Postfach-Blueprint (`postfach.py`)

| Methode | Pfad | Handler |
|---|---|---|
| GET | `/postfach/` | `postfach_page()` |
| GET | `/postfach/api/conversations` | `postfach_api()` |
| GET | `/postfach/api/export-by-sender/<path:sender_id>` | `postfach_export_by_sender()` |
| POST | `/postfach/api/delete-by-sender` | `postfach_delete_by_sender()` |
| POST | `/postfach/api/resolve` | `postfach_resolve()` |

### `(root)` — Video-Blueprint (`video.py`)

| Methode | Pfad | Handler |
|---|---|---|
| GET | `/video/` | `video_page()` |
| POST | `/video/create` | `video_create()` |
| GET | `/video/status/<job_id>` | `video_status()` |
| GET | `/video/queue` | `video_queue_api()` |

### `/analytics` — Analytics-Blueprint (`analytics.py`)

| GET | `/analytics/` | `analytics_view()` | | `analytics.html` |

### `/api` — API-Blueprint (`api.py`)

| Methode | Pfad | Handler |
|---|---|---|
| GET | `/api/status` | platform-Status |
| GET | `/api/queue` | media-queue list |
| POST | `/api/queue/<media_id>/approve` | media-queue approve |
| DELETE | `/api/queue/<media_id>` | media-queue delete |
| GET | `/api/notifications` | notif list |
| POST | `/api/notifications/<nid>/read` | mark read |
| POST | `/api/notifications/read-all` | mark all read |
| GET, POST | `/api/generation-config` | weekly/jit + hours_before |
| POST | `/api/research-trends` | start research |
| GET | `/api/research-trends` | last result |
| POST | `/api/research-apply` | merge to brand |

→ Skip-Liste enthält `/api/` → **alle `/api/*`-Routes sind public** (siehe 14-Findings § C1).

### `/billing` — Billing-Blueprint (`billing.py`)

| Methode | Pfad | Handler |
|---|---|---|
| GET | `/billing/` | `billing_overview()` |
| GET | `/billing/checkout/<plan_key>` | `checkout()` |
| GET | `/billing/success` | `checkout_success()` |
| POST | `/billing/webhook` | `stripe_webhook()` (HMAC-signed) |
| POST | `/billing/activate` | `activate_license()` |
| POST | `/billing/admin/generate-key` | `admin_generate_key()` (ADMIN_SECRET) |
| GET | `/billing/status` | `plan_status()` |

→ **Skip-Liste enthält `/billing` → public.** Webhook ist HMAC-gesichert, Admin-Endpoint via `ADMIN_SECRET`.

### `/calendar` — Calendar-Blueprint (`calendar.py`)

| Methode | Pfad | Handler |
|---|---|---|
| GET | `/calendar/` | `calendar_view()` (Monats-Grid + Autopilot-Strip) |
| POST | `/calendar/zeitplan-speichern` | `save_schedule()` |
| POST | `/calendar/mehrwochen-generieren` | `generate_multi_week()` |
| POST | `/calendar/add` | `add_post()` |
| POST | `/calendar/delete/<post_id>` | `delete_post()` |
| POST | `/calendar/trigger/<post_id>` | `trigger_post()` (Background-Thread) |

### `/composer` — Composer-Blueprint (`composer.py`)

| Methode | Pfad | Handler |
|---|---|---|
| GET | `/composer/` | `composer_view()` |
| POST | `/composer/generate` | `generate()` |
| POST | `/composer/post` | `post_now()` (Background-Thread) |
| GET | `/composer/post-status/<job_id>` | `post_status()` |

### `/einstellungen` — Brand-Settings-Blueprint (`brand_settings.py`)

| Methode | Pfad | Handler |
|---|---|---|
| GET | `/einstellungen/marke` | `brand_page()` |
| GET | `/einstellungen/setup` | `setup_wizard()` (S Skip-Liste) |
| POST | `/einstellungen/token-speichern` | `save_token()` (S Skip-Liste) |
| POST | `/einstellungen/token-testen` | `test_token()` (S Skip-Liste) |
| POST | `/einstellungen/plattform-pause` | `toggle_platform_pause()` |
| POST | `/einstellungen/marke/pdf-upload` | `pdf_upload()` |
| POST | `/einstellungen/marke/bestaetigen` | `confirm_brand()` |
| POST | `/einstellungen/submission-importieren` | `import_submission()` |

### `/erstellen` — Erstellen-Blueprint (`erstellen.py`, **neu 04-27**)

| GET | `/erstellen/` | `hub()` | | `erstellen.html` |

### `/fragebogen` — Fragebogen-Blueprint (`fragebogen.py`)

| Methode | Pfad | Handler | Auth |
|---|---|---|---|
| GET | `/fragebogen`, `/fragebogen/` | `show()` | P (Skip-Liste) |
| POST | `/fragebogen/submit` | `submit()` | P (Skip-Liste) |

### `/kunden-vorschau` — Preview-Blueprint (`preview.py`)

| Methode | Pfad | Handler | Auth |
|---|---|---|---|
| GET | `/kunden-vorschau/` | `client_preview()` | P (Skip-Liste) |
| POST | `/kunden-vorschau/approve/<post_id>` | `approve_post()` | P |
| POST | `/kunden-vorschau/reject/<post_id>` | `reject_post()` | P |
| POST | `/kunden-vorschau/approve-media/<media_id>` | `approve_media()` | P |

### `/lernen` — Learning-Blueprint (`learning.py`)

| Methode | Pfad | Handler |
|---|---|---|
| GET | `/lernen/` | `learning_page()` |
| POST | `/lernen/reset` | `reset_profile()` |
| POST | `/lernen/global` | `update_global()` |
| POST | `/lernen/topic` | `update_topic()` |

### `/media` — Media-Blueprint (`media.py`)

| Methode | Pfad | Handler |
|---|---|---|
| GET | `/media/` | `media_view()` (Tabs Fotos/Ideen) |
| POST | `/media/upload` | `upload()` (max 200 MB) |
| POST | `/media/analyze/<media_id>` | `analyze()` (Background-Thread) |
| GET | `/media/file/<path:filename>` | `serve_file()` (S Skip-Liste) |
| GET | `/media/processed/<path:filename>` | `serve_processed()` (S Skip-Liste) |
| GET | `/media/status/<media_id>` | `analyze_status()` |

### `/vorschau` — Approval-Blueprint (`approval.py`) — 18 Routes

| Methode | Pfad | Handler |
|---|---|---|
| GET | `/vorschau/`, `/vorschau/woche` | `week_view()` |
| POST | `/vorschau/woche-generieren` | `generate_week()` |
| GET | `/vorschau/woche-generieren/status` | `generate_week_status()` |
| POST | `/vorschau/woche-generieren/abbrechen` | `cancel_week_generation()` |
| GET, POST | `/vorschau/modus` | `mode_endpoint()` |
| POST | `/vorschau/varianten/<post_id>` | `generate_variants()` |
| GET | `/vorschau/varianten-status/<post_id>` | `variant_status()` |
| POST | `/vorschau/variant/waehlen` | `select_variant()` |
| POST | `/vorschau/freigeben/<post_id>` | `approve_post()` |
| POST | `/vorschau/freigeben-alle` | `approve_all_confident()` |
| POST | `/vorschau/variant/bearbeiten` | `edit_variant()` |
| POST | `/vorschau/ablehnen/<post_id>` | `reject_post()` |
| POST | `/vorschau/ablehnen-rueckgaengig/<post_id>` | `undo_reject()` |
| POST | `/vorschau/regenerieren/<post_id>` | `regenerate()` |
| POST | `/vorschau/approve-media/<media_id>` | `approve_media()` |
| POST | `/vorschau/variant/verbessern` | `improve_variant()` |
| GET | `/vorschau/variant/verbessern-status/<variant_id>` | `improve_variant_status()` |
| POST | `/vorschau/variant/bewerten` | `rate_variant()` |

## Form-Server (separater Prozess auf Port 5050)

| Methode | Pfad | Quelle |
|---|---|---|
| GET | `:5050/fragebogen` | `server/form_server.py` (HTML-Form) |
| POST | `:5050/fragebogen/submit` | speichert in `client/submissions/` |

## Nicht-Flask Public Statics (vermutlich Vercel)

- `public/index.html`
- `public/datenschutz.html`
- `public/impressum.html`

→ Werden vom Flask-Server NICHT ausgeliefert (keine Route gefunden). Nur Vercel-Deploy.

## Zähler

| Kategorie | Anzahl |
|---|---|
| Total Flask-Routes | ~85 |
| Public (durch Skip-Liste) | 12+ |
| Background-Worker-Triggers | 9 (Scheduler-Jobs) |
| Form-Server-Routes | 2 |
| External Webhooks empfangen | 1 (`/billing/webhook`) |

## Verbundene Notes

- [[Socibot/modules/05-Dashboard-IA]]
- [[Socibot/modules/06-Dashboard-Routes]]
- [[Socibot/modules/14-Findings]] — Auth-Lücke
