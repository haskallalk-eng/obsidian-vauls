---
title: 16 — Layer Backend
tags: [socibot, layer, backend]
date: 2026-04-27
source_of_truth: code
---

# 16 — Layer: Backend

> Alles, was im Python-Prozess läuft (Flask + Bot + Video-Engine).

## Prozess-Modell (verifiziert in `start_bot.py`)

**Ein einziger Python-Prozess** mit drei Threads:

1. **Main-Thread:** Bot-Scheduler (`bot.scheduler.Scheduler.run()` blocking) — schreibt `bot.log`
2. **Daemon-Thread `dashboard`:** Flask-App auf Port 5000 (`app.run(use_reloader=False)`)
3. **Daemon-Thread `form-server`:** `server/form_server.py` auf Port 5050

⚠️ **Single-Process-Limitation:** Alle In-Memory-State-Dicts (siehe `_post_jobs`, `_gen_status`, `_research_running`) funktionieren nicht über Worker-Boundary. Production-Deploy via gunicorn/uwsgi mit >1 Worker würde State-Drift erzeugen.

## Schichten

```
┌──────────────────────────────────────────────────────────────┐
│ FLASK-ROUTING (dashboard/__init__.py + 18 Blueprints)       │
├──────────────────────────────────────────────────────────────┤
│ ROUTE-FILES (dashboard/routes/*, 2.618 LOC)                 │
│   - Validation, Templating, kleine Workflows                │
├──────────────────────────────────────────────────────────────┤
│ SERVICE-LAYER (dashboard/services/*, 2.173 LOC)             │
│   - AI-Vision, Branding, Learning, Plans, Variants, Research│
├──────────────────────────────────────────────────────────────┤
│ BOT-CORE (bot/*, 1.714 LOC)                                 │
│   - Scheduler (Job-Loop), Poster, ContentCalendar, DM       │
├──────────────────────────────────────────────────────────────┤
│ PLATFORM-ADAPTER (platforms/*, 1.036 LOC)                   │
│   - 5 Plattformen × api+content                              │
├──────────────────────────────────────────────────────────────┤
│ VIDEO-ENGINE (video/*, 1.210 LOC)                           │
│   - Queue, Pipeline, AI-Stages, Postprocess                 │
├──────────────────────────────────────────────────────────────┤
│ INFRASTRUKTUR (config, brand, server, automation)           │
│   - .env, brand_knowledge, brand_style_map, form_server     │
└──────────────────────────────────────────────────────────────┘
```

**Flussrichtung der Calls:**
- Routes → Services → Bot/Video → Platform-Adapter → externes API
- Routes → Bot direkt (für ContentCalendar/Analytics ohne Service-Layer)
- Services → andere Services (z.B. media_processor → ai_vision + image_branding)

## Externe APIs (alle code-belegt)

| Service | Wo aufgerufen | Auth | ENV |
|---|---|---|---|
| Anthropic Claude | 25+ Stellen (siehe 03-Platforms) | API Key Header | `CLAUDE_API_KEY` |
| OpenAI DALL-E | `dashboard/services/ai_vision.py:122` | Bearer | `OPENAI_API_KEY` |
| Claude Agent SDK (WebSearch+WebFetch) | `dashboard/services/research_agent.py:58` | API Key | `CLAUDE_API_KEY` |
| Stripe | `dashboard/routes/billing.py:88,124` | Secret Key | `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` |
| Supabase REST | `dashboard/services/supabase_sync.py:38,65` | Bearer + apikey | `SUPABASE_URL`, `SUPABASE_ANON_KEY` |
| Instagram Graph v18.0 | `platforms/instagram/instagram_api.py` | Bearer | `INSTAGRAM_ACCESS_TOKEN` |
| Facebook Graph v18.0 | `platforms/facebook/facebook_api.py` | Bearer | `FACEBOOK_ACCESS_TOKEN` |
| LinkedIn v2 | `platforms/linkedin/linkedin_api.py` | Bearer | `LINKEDIN_ACCESS_TOKEN` |
| Twitter v2 | `platforms/twitter/twitter_api.py` | OAuth1 + Bearer | 5 ENVs |
| TikTok Open API v2 | `platforms/tiktok/tiktok_api.py` | Bearer | `TIKTOK_ACCESS_TOKEN` |
| fal.ai (Flux 2 Pro) | `video/image_gen.py:52` | API Key | `FAL_KEY` |
| fal.ai (Kling 3.0) | `video/video_gen.py:60` | API Key | `FAL_KEY` |
| Mubert | `video/audio.py:43` | API Key | `MUBERT_API_KEY` |
| FFmpeg (lokal) | `video/postprocess.py:145` | — | system PATH |
| Gmail SMTP | `bot/dm_handler.py:86`, `bot/scheduler.py:131` | App-Password | `SMTP_EMAIL`, `SMTP_PASSWORD` |

## Hintergrund-Jobs (Backend-only, kein Frontend-Trigger)

Alle in `bot/scheduler.py:setup_schedule()` (Z.540–571), via `schedule`-Lib:

| Job | Frequenz | Methode |
|---|---|---|
| Posting | täglich at(t) | `_post_platform()` per Plattform/Zeit |
| Engagement-Reply | 15min | `check_and_reply()` |
| Media-Queue-Poll | 5min | `post_approved_media()` |
| JIT-Variant-Gen | 30min | `_check_jit_generation()` |
| Supabase-Sync | 5min | `_sync_supabase()` |
| Video-Queue-Poll | 15min | `_process_video_queue()` |
| Video-Cleanup | 03:00 | `_cleanup_video_media()` (= `video.cleanup.cleanup_old_media`) |
| Daily-Report | 21:00 | `daily_report()` (Email + stdout) |
| Weekly-Plan | Mo 07:00 | `weekly_plan()` |

## Backend-State (in-memory, NICHT-persistent über Restart)

| State-Var | Datei | Zweck | Restart-Robust? |
|---|---|---|---|
| `_post_jobs` | composer.py:12 | Sofort-Post-Tracking | ❌ |
| `_gen_status` | approval.py:22 | Wochen-Generierung | ❌ |
| `_improve_jobs` | approval.py:24 | Inline-Improve TTL=300s | ❌ |
| `_research_running` | api.py:117 | Single-Flight-Lock | ❌ |
| `Scheduler._last_post_at` | scheduler.py | Cool-Down-Tracking | ❌ |
| `_brand_cache` | brand/foerderkraft_brand.py:13 | TTL=60s | ✅ rebuilt nach Restart |
| `VideoQueue._active` | queue.py | aktive Worker-Futures | ✅ DB recovery |

**Persistent (auf Disk):**
- Alle `client/*.json`-Dateien (siehe 10-Client-State)
- `data/video_jobs.db` (siehe 11-Data-Storage)
- `bot.log`

## Locks (Backend-Concurrency)

| Lock | File | Schützt |
|---|---|---|
| `threading.Lock` | bot/content_calendar.py:10 | content_calendar.json (atomic write) |
| `threading.Lock` | dashboard/services/notification_service.py:14 | notifications.json |
| `threading.Lock` | dashboard/services/learning_service.py:84 | learning_profile.json (in-method) |
| `threading.Lock` | dashboard/services/variant_service.py | bot_settings.json (writes) |
| `threading.Lock` | dashboard/services/plan_service.py | bot_settings.json (writes) |
| `threading.Lock` | dashboard/routes/composer.py | _post_jobs |
| `threading.Lock` | dashboard/routes/approval.py | _gen_status, _improve_jobs |
| `threading.Lock` | dashboard/routes/api.py | _research_running |
| `threading.Lock` | video/queue.py:26 | _active dict |

→ **Kein zentraler State-Lock, mehrere Files haben jeweils eigenen Lock auf gleicher JSON-Datei.** Das ist nicht thread-safe (Lock-A kann während Lock-B unique-write nicht blockieren).

## Logging

- Hauptlog: `bot.log` via `logging.FileHandler` in `bot/scheduler.py:60`
- Flask-Werkzeug-Log auf stdout (default)
- Kein zentrales Log-Format-Convention — manche Stellen nutzen `process.stdout.write`, andere `logger.info`

## Verbundene Notes

- [[Socibot/modules/02-Bot-Core]]
- [[Socibot/modules/06-Dashboard-Routes]]
- [[Socibot/modules/07-Dashboard-Services]]
- [[Socibot/modules/04-Video-Engine]]
- [[Socibot/modules/17-Layer-Database]]
- [[Socibot/modules/19-Connections]]
