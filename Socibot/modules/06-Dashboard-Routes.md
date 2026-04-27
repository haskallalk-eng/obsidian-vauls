---
title: 06 — Dashboard-Routes
tags: [socibot, modul, routes]
date: 2026-04-27
source_of_truth: code
---

# 06 — Dashboard-Routes (`dashboard/routes/`, 2.618 LOC, 18 Files)

> Pro Blueprint: Routes, Daten-I/O, Cross-Modul-Aufrufe, Auffälligkeiten.

## Übersicht

| Datei | LOC | Prefix | Routes | Hauptzweck |
|---|---|---|---|---|
| `analytics.py` | 18 | /analytics | 1 | Charts via bot.analytics |
| `api.py` | 176 | /api | 11 | Status, Queue, Notifications, Research, Generation-Config |
| `approval.py` | 565 | /vorschau | 18 | Approval-Flow + Variants + Learning-Hook |
| `autopilot.py` | 75 | (root) | 1 | Stats-Page (jetzt obsolet, siehe Calendar-Header) |
| `billing.py` | 217 | /billing | 7 | Stripe-Checkout + License-Keys |
| `brand_settings.py` | 315 | /einstellungen | 8 | Token-Mgmt + PDF-Brand-Extract + Submission-Import |
| `calendar.py` | 319 | /calendar | 6 | Monats-Grid + CRUD + Multi-Week-Generate |
| `composer.py` | 108 | /composer | 4 | Post-Editor + Sofort-Posten |
| `erstellen.py` | 34 | /erstellen | 1 | **NEU** Hub für Post+Video |
| `fragebogen.py` | 93 | /fragebogen | 2 | Onboarding-Form |
| `landing.py` | 9 | (root) | 1 | Landing-Page |
| `learning.py` | 78 | /lernen | 4 | Learning-Profile-CRUD |
| `media.py` | 147 | /media | 6 | Upload + Analyse + Tabs Fotos/Ideen |
| `overview.py` | 195 | (root) | 3 | Dashboard-Startseite + /verlauf |
| `postfach.py` | 123 | (root) | 5 | DSGVO-Postfach (Export/Delete by Sender) |
| `preview.py` | 65 | /kunden-vorschau | 4 | Public Client-Approval |
| `video.py` | 98 | (root) | 4 | Video-Engine UI |

## `analytics.py` — minimal

`@bp.route("/")` Z.9–17 → `analytics_view()` lädt `Analytics.get_platform_summary()` für 5 Plattformen, Default 30 Tage. Hardcoded `PLATFORMS` Z.6.

## `api.py` (11 Routes)

| Route | Methode | Zweck |
|---|---|---|
| `/api/status` | GET | Plattform-Token-Konfigurations-Check |
| `/api/queue` | GET | Media-Queue-Liste |
| `/api/queue/<media_id>/approve` | POST | Approve einzelnes Item |
| `/api/queue/<media_id>` | DELETE | Item löschen |
| `/api/notifications` | GET | Notif-Liste |
| `/api/notifications/<nid>/read` | POST | Mark read |
| `/api/notifications/read-all` | POST | Mark all read |
| `/api/generation-config` | GET/POST | Weekly vs JIT + hours_before |
| `/api/research-trends` | POST | Start Background-Research |
| `/api/research-trends` | GET | Letztes Research-Ergebnis |
| `/api/research-apply` | POST | Trends in `brand_knowledge.json` mergen |

**Globale State** Z.117–119: `_research_running` flag + Lock — funktioniert nur Single-Process.

## `approval.py` (565 LOC, 18 Routes)

URL-Prefix `/vorschau`. Alle Routes inklusive (Spitzname Vaso → „Wochen-Approval-Wizard"):
- `/`, `/woche` — Wochenansicht (Z.65–109)
- `/woche-generieren` POST + `/status` GET + `/abbrechen` POST (asynchron, `_gen_status`-Dict mit Lock)
- `/modus` GET/POST — Co-Pilot vs. Autopilot
- `/varianten/<post_id>` POST — 3-Pack A/B/C generieren
- `/varianten-status/<post_id>` GET
- `/variant/waehlen` POST — Markiert beste Variante als `selected`
- `/freigeben/<post_id>` POST — Approval + Learning-Signal
- `/freigeben-alle` POST — Bulk-Approve aller Varianten mit `ai_score >= 0.8`
- `/variant/bearbeiten` POST — Inline-Edit
- `/ablehnen/<post_id>` POST + `/ablehnen-rueckgaengig/<post_id>` POST
- `/regenerieren/<post_id>` POST
- `/approve-media/<media_id>` POST — Media-Queue-Approve
- `/variant/verbessern` POST + `/verbessern-status/<variant_id>` GET — Claude verbessert Variante nach Anweisung
- `/variant/bewerten` POST — ❤️/👍/✏️-Rating als Lern-Signal

**Side-Effects:** schreibt `client/content_calendar.json` an mehreren Stellen (Z.141, 202, 256, …). **Kein atomarer Write** — direkt `Path.write_text()`.

**Findings:**
- Globale `_gen_status` + `_improve_jobs` Dicts mit `_IMPROVE_TTL=300` (5min Cleanup) — fragil bei Multi-Process
- Silent-catch-Ketten bei Learning-Speicherung (Z.264–274, 302–311, 386–391, 556–563)

## `autopilot.py` (75 LOC) — Legacy nach Refactor

`@bp.route("/autopilot/")` Z.61–74 — rendert `autopilot.html` mit Stats. **Funktional** noch erreichbar, aber nicht mehr in Sidebar (siehe 05-Dashboard-IA). Stats-Funktionen (`_bot_running`, `_posting_stats`, `_reply_stats`, `_video_stats`) werden jetzt direkt von `calendar.py:12-17` importiert.

## `billing.py` (217 LOC, 7 Routes)

| Route | Methode | Zweck |
|---|---|---|
| `/billing/` | GET | Plan-Übersicht |
| `/billing/checkout/<plan_key>` | GET | Stripe Checkout-Session erstellen |
| `/billing/success` | GET | Post-Checkout-Landing |
| `/billing/webhook` | POST | Stripe-Webhook (HMAC-signed: `checkout.session.completed`, `invoice.paid/failed`, `subscription.deleted`) |
| `/billing/activate` | POST | License-Key-Aktivierung |
| `/billing/admin/generate-key` | POST | Admin-only via `ADMIN_SECRET` |
| `/billing/status` | GET | JSON-Plan-Status |

**Stripe lazy-loaded** Z.45–52 (`_stripe()` bei Bedarf). Price-IDs aus ENV (Z.36–40): `STRIPE_STARTER_PRICE_ID`, `STRIPE_PRO_PRICE_ID`, `STRIPE_AGENCY_PRICE_ID`.

**Webhook-Auth:** `stripe.Webhook.construct_event()` Z.124 — HMAC-signed via `STRIPE_WEBHOOK_SECRET`.

## `brand_settings.py` (315 LOC, 8 Routes)

URL-Prefix `/einstellungen`. Routes:
- `/marke` GET — Brand-Knowledge + Token-Status
- `/setup` GET — Setup-Wizard (rendert `setup.html`, Standalone)
- `/token-speichern` POST — schreibt `.env` direkt (mit Whitelist Z.153–159 + Newline-Strip Z.19–30 für Injection-Schutz)
- `/token-testen` POST — HTTP-Calls zu Plattform-APIs zum Testen
- `/plattform-pause` POST — pausiert Plattform ohne Token-Löschung
- `/marke/pdf-upload` POST — PDF in `client/brand_pdfs/`, ruft `BrandExtractor.extract_from_pdf()`
- `/marke/bestaetigen` POST — User confirmt extrahierte Brand-Daten
- `/submission-importieren` POST — importiert lokale Form-Submission

**Side-Effects:** schreibt `.env` direkt + ruft `dotenv.load_dotenv(override=True)` (Z.170–171) für Hot-Reload — funktioniert nur im aktuellen Prozess, andere Threads/Worker sehen alten Wert bis Boot.

## `calendar.py` (319 LOC, 6 Routes)

| Route | Methode | Zweck |
|---|---|---|
| `/calendar/` | GET | Monats-Grid mit Autopilot-Stats |
| `/calendar/zeitplan-speichern` | POST | Schedule-Editor speichern |
| `/calendar/mehrwochen-generieren` | POST | 1–8 Wochen generieren |
| `/calendar/add` | POST | Neuen Post planen |
| `/calendar/delete/<post_id>` | POST | Post löschen |
| `/calendar/trigger/<post_id>` | POST | Sofort posten (Background-Thread) |

**Autopilot-Inline-Imports** Z.12–17: `_bot_running`, `_posting_stats`, `_reply_stats`, `_video_stats` direkt aus `dashboard/routes/autopilot.py` importiert. Avoiding extra HTTP-Hop.

**Monats-Grid-Logik:** `_build_month_grid(year, month, by_day)` Z.45–98 — 6-Wochen-Grid, prev/next-Pagination, in_month/is_today/is_past-Flags pro Day.

## `composer.py` (108 LOC, 4 Routes)

- `/composer/` GET — Editor-View, lädt Media-Queue
- `/composer/generate` POST — Claude-Content-Generation
- `/composer/post` POST — Sofort-Posten (Background-Thread)
- `/composer/post-status/<job_id>` GET — Job-Polling

In-Memory `_post_jobs` Dict (Z.12–13, max 50, Lock-geschützt) — keine Persistenz.

## `erstellen.py` (34 LOC) — neu

```python
bp = Blueprint("erstellen", __name__, url_prefix="/erstellen")
VIDEO_DB = Path("data/video_jobs.db")

@bp.route("/")
def hub():
    return render_template("erstellen.html", recent_videos=_recent_video_jobs())
```

`_recent_video_jobs(limit=5)` Z.16–28: SELECT job_id, platform, topic, status, created_at FROM video_jobs ORDER BY created_at DESC LIMIT 5.

**Findings:** Hardcoded Limit 5, silent-catch bei DB-Fehler (Z.27–28).

## `fragebogen.py` (93 LOC, 2 Routes)

- `/fragebogen` GET — rendert standalone Onboarding-Form
- `/fragebogen/submit` POST — schreibt:
  - `client/brand_knowledge.json` (Z.51–66)
  - `client/bot_settings.json` (Z.71–89, pausiert inaktive Plattformen)
  - Invalidiert Brand-Cache via `brand.foerderkraft_brand.invalidate_brand_cache()`

## `learning.py` (78 LOC, 4 Routes)

URL-Prefix `/lernen`. CRUD auf `client/learning_profile.json` via `learning_service`:
- `/` GET — Learning-Page
- `/reset` POST — Profile resetten
- `/global` POST — `always_avoid`/`always_prefer` add/remove
- `/topic` POST — Topics aus approved/rejected entfernen

## `media.py` (147 LOC, 6 Routes)

| Route | Methode | Zweck |
|---|---|---|
| `/media/` | GET | Tabs Fotos/Ideen |
| `/media/upload` | POST | Datei-Upload (Multipart, max 200 MB) |
| `/media/analyze/<media_id>` | POST | Vision-Analyse (Background-Thread) |
| `/media/file/<filename>` | GET | Original ausliefern |
| `/media/processed/<filename>` | GET | Processed ausliefern |
| `/media/status/<media_id>` | GET | Status-Polling |

**Datei-System:** `client/media/<id>.<ext>` + Sidecar `client/media/<id>.json` mit Metadaten. ALLOWED_EXT={.jpg,.jpeg,.png,.mp4,.mov,.webp}. MAX_BYTES=200MB (Z.76).

**Tabs-Logik (post-refactor):** `_ideas_by_platform()` Z.32–48 lädt `automation/sample_content.json` und gibt platform-grouped dict zurück. Tab-Default `?tab=fotos`.

## `overview.py` (195 LOC, 3 Routes)

- `/` GET — Dashboard-Startseite mit Plattform-Summaries (7d), Log-Tail, Cal-Stats, Eskalationen, Video-Stats
- `/api/log` GET — Log-Tail-JSON (8KB Tail)
- `/verlauf/`, `/verlauf` GET — History-View

## `postfach.py` (123 LOC, 5 Routes)

DSGVO-konformes Postfach für DM/Comment-Threads:
- `/postfach/` GET — Liste + Stats
- `/postfach/api/conversations` GET — Full Export
- `/postfach/api/export-by-sender/<sender_id>` GET — Art. 20 Datenportabilität
- `/postfach/api/delete-by-sender` POST — Art. 17 Recht auf Vergessen
- `/postfach/api/resolve` POST — Eskalation als erledigt markieren

## `preview.py` (65 LOC, 4 Routes)

URL-Prefix `/kunden-vorschau`. **Public** (in Skip-Liste).
- `/` GET — Public Client-View, 14 Tage geplante Posts + Media
- `/approve/<post_id>` POST — Approve
- `/reject/<post_id>` POST — Reject
- `/approve-media/<media_id>` POST — Media approve

## `video.py` (98 LOC, 4 Routes)

- `/video/` GET — Queue-Page
- `/video/create` POST — Job in Queue (`VideoQueue.submit`)
- `/video/status/<job_id>` GET — Status-Poll
- `/video/queue` GET — aktive Jobs JSON

`DB_PATH = Path("data/video_jobs.db")`.

## Cross-Modul-Aufrufe (Routes → Module)

| Route | Service | Funktion |
|---|---|---|
| api | notification_service | get_unread, mark_read |
| api | variant_service | get/set_generation_config |
| api | research_agent | run_research_sync, load_latest |
| approval | variant_service | generate_variants, select_variant_static |
| approval | plan_service | can_generate, track_post_generated |
| approval | learning_service | record_approval/rejection/rating |
| brand_settings | brand_extractor | BrandExtractor + extract_from_pdf |
| calendar | autopilot | _bot_running, _posting_stats, _reply_stats, _video_stats |
| calendar | variant_service | get/set_platform_schedules, get_paused_platforms |
| calendar | plan_service | can_generate, track_post_generated |
| composer | brand.foerderkraft_brand | get_brand |
| learning | learning_service | profile-Operationen |
| media | media_processor | MediaProcessor.process |
| media | bot.config | load_config |
| overview | bot.analytics | Analytics.get_platform_summary |
| overview | video.queue | VideoQueue.get_stats |
| video | video.queue | VideoQueue.submit |

## Verbundene Notes

- [[Socibot/modules/05-Dashboard-IA]]
- [[Socibot/modules/07-Dashboard-Services]]
- [[Socibot/modules/18-Routes-Map]]
- [[Socibot/modules/19-Connections]]
