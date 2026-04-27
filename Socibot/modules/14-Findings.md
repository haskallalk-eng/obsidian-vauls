---
title: 14 — Findings (Code-belegt)
tags: [socibot, findings, risiken]
date: 2026-04-27
source_of_truth: code
---

# 14 — Findings (Ist-Stand 2026-04-27)

> **Strikte Regel dieses Notes:** Jeder Punkt muss mit Datei:Zeile belegt sein. Keine Vermutungen, keine „könnte sein".

## 🔴 CRITICAL

### C1 — Keine Authentication im Dashboard

**Beleg:** Verifiziert über alle 18 Files in `dashboard/routes/`. Keine `@login_required`/`@auth_required`-Decorator. Keine Session-Token-Validierung. `dashboard/__init__.py:65-105` zeigt nur Onboarding-Redirects, keine Auth-Schicht.

**Konsequenz:** Wer den Server erreicht, hat Vollzugriff auf alle Routes inkl. Admin-Endpoints (`/billing/admin/generate-key` Z.191-208 ist nur durch `ADMIN_SECRET`-ENV gesichert, nicht durch User-Session). Im Single-User-Self-Host akzeptabel; im Multi-Tenant- oder öffentlich exponierten Setup kritisch.

### C2 — Race Conditions auf zentralen JSON-Files

**Beleg:** 
- `client/content_calendar.json` wird von 6+ Stellen geschrieben (`approval.py:141,202,256`; `calendar.py:280,297,315`; `composer.py:77-84`). Nur `bot/content_calendar.py:112-128` hat atomic-write (tmp + os.replace) und Lock — alle anderen schreiben mit direktem `Path.write_text()`.
- `client/brand_knowledge.json` wird von 5 Stellen geschrieben (`fragebogen.py:64`, `brand_settings.py:93,309`, `api.py:170`, `brand_extractor.py:93`, `supabase_sync.py:118`).

**Konsequenz:** Bei Concurrent-Writes (Scheduler postet während User approved) → corrupt JSON / verlorene Updates / Last-Writer-Wins. In Multi-Worker-Deploy katastrophal.

### C3 — TikTok-Stub im aktiven Plattform-Set

**Beleg:** `bot/poster.py:178-180` returnt `{success: False, error: "Video-Upload noch nicht implementiert"}`; `platforms/tiktok/tiktok_api.py:19-41` zeigt nur Init-Schritt, kein Chunk-Upload. **Aber** `bot/scheduler.py:544-547` registriert TikTok-Jobs (15:00, 20:00 — `bot/config.py:50`). 

**Konsequenz:** Jeder TikTok-Job schlägt zur Posting-Zeit fehl, läuft durch Tenacity-Retry (4× exp. Backoff Z.97-102 in `poster.py`), wird mit Error geloggt → Tickets/Notifications spammen Kunden, der TikTok aktiv hat.

### C4 — Hardcoded Brand-Keywords in Production-Service

**Beleg:** `dashboard/services/variant_service.py:248`:
```python
["förderkraft", "drk", "rotes kreuz", "haustür", "außendienst", "spende", "förder"]
```
Wird im Variant-Scoring verwendet (Brand-Keyword-Match → +0.04 ai_score pro Hit, max +0.2).

**Konsequenz:** Jeder Nicht-Förderkraft-Kunde bekommt verzerrten ai_score, der seine Brand-Keywords nicht kennt. Auto-Approval-Schwellen (`auto_approve_threshold: 0.85` aus `bot_settings.json`) liefern für andere Kunden falsche Ergebnisse.

## 🟠 HIGH

### H1 — Documentation-Drift bei ENV-Vars

**Beleg:** Im Code referenzierte aber im `.env.example` fehlende ENV-Vars (verifiziert):
- `FAL_KEY` (`video/image_gen.py:31`, `video/video_gen.py:34`)
- `MUBERT_API_KEY` (`video/audio.py:33`)
- `OPENAI_API_KEY` (`dashboard/services/ai_vision.py:122`)
- `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_*_PRICE_ID`, `BASE_URL` (`dashboard/routes/billing.py`)
- `SUPABASE_URL`, `SUPABASE_ANON_KEY` (`dashboard/services/supabase_sync.py:26-27`)
- `LICENSE_SECRET` (`dashboard/services/plan_service.py:245`)
- `ADMIN_SECRET` (`dashboard/routes/billing.py`)

**Konsequenz:** Setup nach `cp .env.example .env` führt zu Socibot, das beim Boot „läuft" aber Video-/Billing-/Supabase-Features stumm fehlschlagen lässt.

### H2 — Veraltetes Claude-Model

**Beleg:** `bot/constants.py:76`: `CLAUDE_MODEL = "claude-sonnet-4-6"`. Stand 2026-04 ist die produktive Sonnet-Linie `claude-sonnet-4-5`. „4-6" ist entweder Typo oder Vorab-Modell. Wird in 25+ Anthropic-Calls verwendet (vgl. `03-Platforms`).

**Konsequenz:** Bei Anthropic-API-404 schlagen alle Content-Gens fehl. Kein Fallback im Code.

### H3 — In-Memory-Job-Tracking ohne Persistenz

**Beleg:** 
- `dashboard/routes/composer.py:12-13` — `_post_jobs: dict` mit Lock, max 50
- `dashboard/routes/approval.py:22-26` — `_gen_status`, `_improve_jobs` mit `_IMPROVE_TTL=300`
- `dashboard/routes/api.py:117-119` — `_research_running` Flag

**Konsequenz:** Bei Flask-Restart sind alle laufenden Jobs verloren. Status-Polling vom Frontend bekommt 404, User sieht „verschwundene" Jobs.

### H4 — TikTok in Platform-Schedules per Default

**Beleg:** `bot/config.py:50` und `bot/content_calendar.py:38` haben TikTok-Defaults. `bot/constants.py:106-108` markiert es als `PLATFORMS_STUB`, aber `_post_platform()` hat keinen Stub-Skip → siehe C3.

**Mitigation existiert:** `bot/scheduler.py:91-94` checkt für Stub-Platforms (verifiziert `_post_platform` Z.80–94). Aber TikTok wird in `paused_platforms` gesetzt im neu erstellten `bot_settings.json` — das ist nur ein Zustand, kein hard-disable.

### H5 — Eskalierte DM-Threads bekommen weiter Replies

**Beleg:** `bot/dm_handler.py:125` setzt `escalate=true` in conversation, aber kein Re-Engagement-Filter im `_reply_*`-Code (verifiziert in `bot/scheduler.py:237-388`). 

**Konsequenz:** Wenn Kunde nach Eskalation („rechtlich") nochmal schreibt, antwortet der Bot wieder — eskalierter Thread wird nicht für weitere Antworten gesperrt.

## 🟡 MEDIUM

### M1 — Silent Catches überall im Codebase

Beispiele (verifiziert):
- `bot/dm_handler.py:90-91` — Email-Send-Failure: nur `log.warning`, Email kann lautlos verloren gehen
- `dashboard/routes/approval.py:264-274,302-311,386-391,556-563` — Learning-Speicherung silent-catches
- `dashboard/services/learning_service.py:204-205,259-260,297-298` — Datei-I/O silent-catches
- `dashboard/services/supabase_sync.py:53-55,76-77,147-149` — Supabase-Errors silent
- `dashboard/services/notification_service.py:18-20` — JSON-Load silent

**Konsequenz:** Bugs werden nicht in Logs sichtbar, Debugging schwierig.

### M2 — Polling-Frequenzen ohne Backoff

- `audio.py:97` — Mubert-Polling fix 3s ohne Backoff
- `video_gen.py:158-159` — nur grobe Umschaltung 5s/10s nach 60s

### M3 — Keine SQLite-Indexes

- `data/video_jobs.db` Schema (`queue.py:38-54`) hat **keine Indexes** außer Primary Key. Query `WHERE status='queued' ORDER BY created_at` (`queue.py:94-97`) wird mit Job-Zahl O(N).

### M4 — `cost_ledger` ist totes Schema

`video/queue.py:55-63` definiert die Tabelle, aber kein einziger INSERT im Code. Cost wird stattdessen auf `video_jobs.cost_cents` aggregiert.

### M5 — Hardcoded `MAX_WORKERS=2`, `MAX_RETRIES=2` in Video-Queue

`video/queue.py:19-20`. Nicht konfigurierbar, kein ENV-Override.

### M6 — `bot/content_calendar.py:100` Brand-Substitution

```python
re.sub(r'\bFörderkraft\b', brand_name, text)
```

Funktioniert nur wenn Source-Texte „Förderkraft" wörtlich enthalten. Generic Templates ohne diesen String werden nicht ersetzt.

### M7 — Mediathek-Ideen-Tab zeigt Förderkraft-Demo

`automation/sample_content.json` enthält DRK-Vertriebs-Demo-Posts vom 2026-03-21. Wird seit 2026-04-27 in `dashboard/routes/media.py:32-48` als „Ideen"-Tab gerendert. **Kein Brand-Filter** → Nicht-Förderkraft-Kunden sehen fremde Inhalte.

## 🔵 LOW / NICE

### L1 — `main.py` ist legacy, README-Pfad inkorrekt

`README.md:63` empfiehlt `python main.py`. Aber `main.py` startet nur den Scheduler ohne Dashboard. Real-World-Entry ist `python start_bot.py` (siehe `01-Entry-Points`).

### L2 — APScheduler-Erwähnung im README, Code nutzt `schedule`

`requirements.txt` listet `schedule>=1.2.0`, nicht apscheduler. README-Stack-Tabelle erwähnt fälschlicherweise APScheduler.

### L3 — `image_prompts.json` ungenutzt

`automation/image_prompts.json` existiert, wird aber nirgendwo gelesen. Dead asset.

### L4 — Comment-Lüge in TikTok-Stub

`platforms/tiktok/tiktok_api.py:19-41` hat keinen Hinweis, dass die `upload_video()`-Implementierung unvollständig ist. Erst der `Poster._post_tiktok` returnt einen Stub-Error.

### L5 — Email-Helper Defaults `info@mindrails.de`

`bot/config.py:85` — Brand-spezifischer Default. Bei Nicht-Mindrails-Setup geht Eskalations-Email an die falsche Adresse, wenn `NOTIFY_EMAIL`-ENV nicht gesetzt.

### L6 — Cleanup `_safe_delete` nutzt `time.sleep(2)` × 3

`video/cleanup.py:35-44`. Bei vielen gelockten Files blockiert das Script bis zu 6s pro File.

### L7 — `client/notifications.json` rotiert Read-Notifs auf 80, Unread unbegrenzt

`dashboard/services/notification_service.py:29`. Bei Bot-im-Idle-Mode kann Unread-Counter unbegrenzt wachsen.

## Cross-Cutting Patterns

### P1 — Dependency-Inversion fehlt

Routes importieren Services direkt (z.B. `calendar.py` → `autopilot.py`-internals via `from dashboard.routes.autopilot import _bot_running`). Macht Tests + Refactoring schwer.

### P2 — JSON-Persistierung als Mono-Strategie

Außer Video-Queue keine DB. Jeder feature-add muss eigene JSON erfinden (siehe `client/`-Verzeichnis: 8+ separate State-Files). Migrations-Strategie nicht erkennbar.

### P3 — Brand-Hardcoding tief in Service-Layer

Trotz `brand_knowledge.json`-Override sind „Förderkraft"-Werte in 4 Code-Stellen hardgecodet (vgl. `09-Brand-System` § Brand-Hardcoding-Hotspots). Multi-Tenant-tauglich ist das nicht.

## Empfehlungen (knapp, code-belegt)

| Priorität | Maßnahme | Welche Files |
|---|---|---|
| C1 | Auth-Layer einbauen (Session/Cookie) | `dashboard/__init__.py:65-105` ergänzen |
| C2 | Atomic-Write-Helper als zentraler Util, alle JSON-Schreibstellen migrieren | new `dashboard/services/json_atomic.py`; alle direct `Path.write_text()` migrieren |
| C3 | TikTok-Posting hinter Plan-Feature-Gate, bis Upload implementiert | `bot/scheduler.py:91-94` Stub-Skip härten |
| C4 | Brand-Keywords aus `brand_knowledge.json` lesen | `dashboard/services/variant_service.py:248` |
| H1 | `.env.example` updaten | `apps/api/.env.example` (gibt's nicht — `.env.example` direkt) |
| H2 | Claude-Model nach `claude-sonnet-4-5` (oder verifizieren ob „4-6" wirklich existiert) | `bot/constants.py:76` |
| H3 | Job-State persistieren (SQLite oder einfache JSON) | `composer.py`, `approval.py`, `api.py` |
| H5 | Eskalierte Threads in `_reply_*`-Methoden überspringen | `bot/scheduler.py:237-388` |

## Verbundene Notes

- [[Socibot/modules/00-Overview]]
- [[Socibot/modules/19-Connections]]
- [[Socibot/modules/20-Summary]]
