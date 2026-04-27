---
title: 19 — Connections (Modul-Graph)
tags: [socibot, connections, dependencies, graph]
date: 2026-04-27
source_of_truth: code
---

# 19 — Connections (alle Inter-Modul-Verbindungen)

> Wer importiert wen, wer ruft wen, wer schreibt wohin. Alles per `grep` + Read verifiziert.

## Modul-Dependency-Graph

```
                                ┌────────────┐
                                │ start_bot  │
                                └─────┬──────┘
                                      │ load_config
                                      ▼
                           ┌─────────────────────┐
                           │  bot/config         │
                           └──────────┬──────────┘
                                      │ get_platform_schedules
                                      ▼
                  ┌───────────────────────────────────┐
                  │ dashboard/services/variant_service│
                  └───┬──────────────────────────┬────┘
                      │ generate_intelligence    │ uses
                      ▼                          ▼
       ┌─────────────────────────┐   ┌──────────────────┐
       │ dashboard/services/     │   │ brand/           │
       │   learning_service      │   │  foerderkraft    │
       └──────────┬──────────────┘   └──────┬───────────┘
                  │ writes                  │
                  ▼                         ▼
                  client/learning_profile.json
                  client/brand_knowledge.json
                  client/bot_settings.json

start_bot ─► Scheduler (bot/scheduler.py) ─► Poster (bot/poster.py) ─► platforms/<x>_api.py
                                          ─► DMHandler (bot/dm_handler.py) ─► <x>_api.get_comments etc.
                                          ─► Analytics (bot/analytics.py) ─► writes client/analytics.json
                                          ─► VideoQueue.submit (video/queue.py) [periodic]
                                          ─► supabase_sync.sync_submissions [periodic]
                                          ─► variant_service (over content_calendar)

Routes  ─► services  ─► (bot.* | video.* | brand.*)  ─► JSON or DB
```

## Cross-Module Imports (pro Datei)

### bot/scheduler.py importiert (Z.17–22)
- `bot.poster.Poster`
- `bot.content_calendar.ContentCalendar`
- `bot.dm_handler.DMHandler`
- `bot.analytics.Analytics`
- `bot.constants`
- `video.cleanup.cleanup_old_media`
- Optional (lazy): `dashboard.services.variant_service`, `dashboard.services.notification_service`, `dashboard.services.supabase_sync`, `video.queue.VideoQueue`, alle 5 Plattform-APIs

### bot/poster.py importiert
- `tenacity.retry`, `stop_after_attempt`, `wait_exponential`, `retry_if_exception_type`
- Alle 5 `platforms/<x>_api` + `<x>_content`

### bot/content_calendar.py importiert
- `brand.foerderkraft_brand.BRAND, get_platform_voice`
- `bot.constants`
- Lazy: `dashboard.services.variant_service.get_platform_schedules`

### bot/dm_handler.py importiert
- `anthropic`
- `brand.foerderkraft_brand.get_brand_context, BRAND`
- `bot.constants.CLAUDE_MODEL`

### platforms/*/`<x>_content.py` importieren
- `anthropic`
- `brand.foerderkraft_brand.get_brand_context, get_platform_voice, BRAND`
- `bot.constants.CLAUDE_MODEL`

### dashboard/__init__.py importiert
- 18 Blueprints (siehe 06-Dashboard-Routes)
- `brand.foerderkraft_brand.get_brand` (Context-Processor)

### dashboard/routes/calendar.py importiert (post 04-27)
- `bot.content_calendar.ContentCalendar`
- `bot.poster.Poster`
- `bot.config.load_config`
- `bot.constants`
- **Cross-Route-Import:** `dashboard.routes.autopilot._bot_running, _posting_stats, _reply_stats, _video_stats` (Z.12–17)
- `dashboard.services.variant_service`, `dashboard.services.plan_service`

→ Calendar→Autopilot ist eine direkt-Import-Verschmelzung statt cleaner Service-Layer.

### dashboard/routes/erstellen.py importiert (neu 04-27)
- `sqlite3`, `pathlib`, `flask`
- Keine Cross-Module-Imports

### dashboard/routes/composer.py importiert
- `bot.poster.Poster`
- `bot.config.load_config`
- `bot.constants`
- `bot.content_calendar`, `bot.analytics`, `brand.foerderkraft_brand`

### dashboard/services/learning_service.py importiert
- `bot.config.load_config`
- `anthropic`

### dashboard/services/research_agent.py importiert
- `claude_agent_sdk` (externes Package)
- `dashboard.services.notification_service`

### dashboard/services/supabase_sync.py importiert
- `requests`
- `dashboard.services.notification_service`
- `brand.foerderkraft_brand` (`invalidate_brand_cache`)

### video/queue.py importiert
- `video.models.VideoJob, JobStatus`
- Lazy: `video.pipeline.run_pipeline, PipelineError` (Z.116)

### video/pipeline.py importiert
- `video.models, brand_mapping, prompt_builder, image_gen, video_gen, audio, postprocess`

### video/prompt_builder.py importiert
- `anthropic`
- `bot.constants.CLAUDE_MODEL`
- `brand.foerderkraft_brand.get_brand_context` (importiert, **aber nicht im Body benutzt** Z.58–141 — Note)

## State-Schreib-Kreuztabelle

| State-Datei | Writer (verifiziert) |
|---|---|
| `client/bot_settings.json` | fragebogen, plan_service, supabase_sync, variant_service |
| `client/brand_knowledge.json` | api(/research-apply), brand_settings, brand_extractor, fragebogen, supabase_sync |
| `client/content_calendar.json` | approval (multi-write), calendar (multi-write), composer, ContentCalendar (atomic) |
| `client/conversations.json` | dm_handler, postfach (delete-by-sender, resolve) |
| `client/learning_profile.json` | learning, learning_service |
| `client/notifications.json` | notification_service |
| `client/replied_comments.json` | scheduler |
| `client/research_suggestions.json` | research_agent |
| `client/analytics.json` | analytics |
| `client/reports/weekly_*.json` | analytics |
| `client/media/queue/*.json` | api, approval, composer, media, media_processor |
| `client/media/<id>.<ext>` | media (Upload) |
| `client/media/<id>.json` (Sidecar) | media, media_processor |
| `client/media/processed/<id>.jpg` | image_branding |
| `client/brand_pdfs/*.pdf` | brand_settings |
| `client/submissions/*.json` | server/form_server |
| `data/video_jobs.db` | queue (CRUD) |
| `.env` | brand_settings (Setup-Wizard) |
| `bot.log` | logging.FileHandler in scheduler |

## API-Call-Routes (extern)

```
ContentGen-Path:
  Routes (calendar/composer/api/approval) ─►
    variant_service.generate_variants ─►
      anthropic.messages.create  (with intelligence_context from learning_service)

Engagement-Path:
  Scheduler.check_and_reply ─►
    platforms/<x>_api.get_comments ─► HTTP API
    DMHandler.handle ─►
      anthropic.messages.create (intent + response)
    platforms/<x>_api.reply_to_comment ─► HTTP API

Posting-Path:
  Scheduler._post_platform ─►
    Poster.post ─►
      platforms/<x>_content.generate_<post>  ─► anthropic.messages.create
      platforms/<x>_api.post_*               ─► HTTP API

Video-Path:
  Routes (video/erstellen) ─► video.queue.submit ─►
    pipeline.run_pipeline ─►
      brand_mapping.resolve_style          (config/brand_style_map.json)
      prompt_builder.build_prompts         ─► anthropic (Tool Use)
      image_gen.generate_image             ─► fal.ai Flux
      video_gen.generate_video             ─► fal.ai Kling
      audio.generate_music                 ─► Mubert
      postprocess.composite_video          ─► subprocess(ffmpeg)

Onboarding-Path:
  External Form ─► server/form_server :5050 ─► client/submissions/*.json
  User clicks „Importieren" ─►
    brand_settings./submission-importieren ─►
      _map_submission_to_brand ─► brand_knowledge.json + bot_settings.json + invalidate_brand_cache

Brand-PDF-Path:
  brand_settings./marke/pdf-upload ─►
    brand_extractor.extract_from_pdf ─► anthropic Vision (PDF base64) ─►
      save_brand_knowledge ─► brand_knowledge.json

Research-Path:
  api./research-trends POST ─►
    research_agent.run_research_sync ─► claude_agent_sdk (WebSearch+Fetch)
                                     ─► research_suggestions.json
                                     ─► notification_service.push
  api./research-apply POST ─►
    brand_knowledge.json (merge)

Billing-Path:
  Stripe Webhook ─► billing./webhook ─► plan_service.activate_plan/deactivate_plan ─► bot_settings.json
  Stripe Checkout-Redirect ─► billing./checkout/<plan> ─► stripe.checkout.Session.create

Notification-Path:
  Many writers (research_agent, supabase_sync, scheduler) ─►
    notification_service.push ─► notifications.json
  Frontend Polling 60s ─► /api/notifications ─► notification_service.get_unread

Cleanup-Path:
  Scheduler 03:00 ─► video.cleanup.cleanup_old_media ─►
    media/workspace/* (TTL 1h)
    media/output/* (TTL 48h)
```

## Inter-Service-Calls

| Caller | Callee | Funktion |
|---|---|---|
| `media_processor` | `ai_vision` | analyze_image, generate_dall_e_image |
| `media_processor` | `image_branding` | apply_branding |
| `variant_service` | `learning_service` | generate_intelligence_context |
| `research_agent` | `notification_service` | push |
| `supabase_sync` | `notification_service` | push |
| `supabase_sync` | `brand.foerderkraft_brand` | invalidate_brand_cache |
| `learning_service` | `bot.config` | load_config |
| `brand_extractor` | `brand.foerderkraft_brand` | (Fallback `BRAND`) |

## Routes ↔ Services

Siehe [[Socibot/modules/06-Dashboard-Routes]] § Cross-Modul-Aufrufe.

## Frontend ↔ Backend

Siehe [[Socibot/modules/08-Dashboard-Templates]] § Frontend ↔ Backend Endpoints und [[Socibot/modules/15-Layer-Frontend]].

## Verbundene Notes

- Alle Module-Notes 02-13
- [[Socibot/modules/16-Layer-Backend]]
- [[Socibot/modules/17-Layer-Database]]
- [[Socibot/modules/14-Findings]]
