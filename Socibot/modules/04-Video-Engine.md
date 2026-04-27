---
title: 04 — Video-Engine
tags: [socibot, modul, video]
date: 2026-04-27
source_of_truth: code
---

# 04 — Video-Engine v4.0 (`video/`, 1.210 LOC, 11 Files)

> ThreadPool-basierte Video-Generierungspipeline: Brand-Style → Claude-Prompts → fal.ai Flux → fal.ai Kling → Mubert → FFmpeg.

## Files

| Datei | LOC | Zweck |
|---|---|---|
| `__init__.py` | 1 | Package-Marker |
| `models.py` | 37 | `VideoJob`, `JobStatus`, `StepResult` Dataclasses |
| `queue.py` | 222 | ThreadPool + SQLite-Queue + Retry |
| `pipeline.py` | 133 | Orchestrator (5 Steps) |
| `image_gen.py` | 112 | fal.ai Flux 2 Pro Bild-Generierung |
| `video_gen.py` | 161 | fal.ai Kling 3.0 Image→Video |
| `audio.py` | 113 | Mubert Musik-Generierung |
| `prompt_builder.py` | 141 | Claude Tool-Use für strukturierte Prompts |
| `brand_mapping.py` | 61 | Tone → Visual-Style-Mapping (config/brand_style_map.json) |
| `postprocess.py` | 185 | FFmpeg Compositing + AI-Metadata (EU AI Act) |
| `cleanup.py` | 44 | Workspace-Cleanup (1h) + Output-Cleanup (48h) |

## Pipeline-Flow (vollständig code-belegt)

```
queue.submit(client_id, platform, topic)
  │  (queue.py:72-85: INSERT INTO video_jobs, _try_dispatch)
  ▼
ThreadPool worker (max=2)  ─── queue.py:_run_job (114-136)
  │
  ▼
pipeline.run_pipeline(job, brand_config)  ─── pipeline.py:26-125
  │
  ├─ Step 1: resolve_style(brand_config)
  │   brand_mapping.py:21-49 → liest config/brand_style_map.json,
  │   maps tone_keywords (z.B. "professionell") auf {image, video, audio, color, text}
  │
  ├─ Step 2: build_prompts(brand_config, style, topic, platform)
  │   prompt_builder.py:58-141 → Claude Tool-Use mit strict JSON-Schema:
  │     image_prompt (EN), image_negative (EN),
  │     video_motion (EN), hook_text (DE ≤6W),
  │     main_text (DE ≤10W), cta_text (DE ≤5W),
  │     caption (DE), hashtags[3-5]
  │
  ├─ Step 3: generate_image(prompt, ...)  ─── image_gen.py:14-86
  │   POST queue.fal.run/fal-ai/flux-pro/v1.1-ultra
  │   → media/workspace/{job_id}/base.png (1080x1920)
  │   Retry: 3× Exponential-Backoff (5/10/20s)
  │   Cost: 8 cents
  │
  ├─ Step 4 (parallel via ThreadPool max=2):
  │   ├─ generate_video(image_path, motion_prompt, duration_sec≤10)
  │   │   video_gen.py:15-95
  │   │   1. Upload PNG: rest.alpha.fal.ai/storage/upload/initiate (mit Fallback)
  │   │   2. POST queue.fal.run/fal-ai/kling-video/v2/standard/image-to-video
  │   │   3. Polling 5s/10s, Timeout 600s
  │   │   → media/workspace/{job_id}/raw.mp4
  │   │   Cost: 56c (≤5s) oder 112c (≤10s)
  │   │
  │   └─ generate_music(mood, genre, duration+2s)
  │       audio.py:14-90
  │       POST api.mubert.com/v2/TTMRecordTrack + Polling
  │       → media/workspace/{job_id}/music.mp3 (optional, Timeout 90s)
  │       Cost: 7 cents
  │       NON-FATAL: Pipeline läuft auch ohne Musik (pipeline.py:90-101)
  │
  └─ Step 5: composite_video(...)
      postprocess.py:14-162 → subprocess ffmpeg
      Filter-Chain: scale 1080x1920, crop, eq +contrast/sat,
        vignette, film grain, drawtext (hook 0-2.5s, main 2.5s..end-2.5s,
        cta last 3s), amix audio + fade-in/out, libx264 crf=18 preset=slow
      EU AI Act Art. 50(2) Metadata: comment="AI-generated...",
        encoder="Socibot Video Engine v4.0", genre="AI-generated"
      → media/output/{job_id}.mp4
      Timeout 300s

  ▼
queue.py:_on_complete (138-148)
  │  UPDATE status='done', cost_cents=N, finished_at=...
  │  workspace cleanup (pipeline.py:127-133, in finally)
  │
  ▼  (on Exception)
queue.py:_handle_failure (150-166)
  │  retry_count < MAX_RETRIES=2 → status='queued', retry_count++
  │  retry_count >= 2 → status='failed', error=str(exc)
  ▼
_try_dispatch (next job)
```

## SQLite-Schema (`data/video_jobs.db`)

`queue.py:38-63` — beide Tabellen sind `IF NOT EXISTS`-idempotent.

```sql
CREATE TABLE IF NOT EXISTS video_jobs (
    job_id TEXT PRIMARY KEY,
    client_id TEXT NOT NULL,
    platform TEXT NOT NULL,
    topic TEXT NOT NULL,
    calendar_post_id TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'queued',  -- queued/processing/done/failed
    created_at TEXT NOT NULL,
    started_at TEXT,
    finished_at TEXT,
    error TEXT,
    cost_cents INTEGER DEFAULT 0,
    output_path TEXT,
    retry_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS cost_ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT NOT NULL,
    job_id TEXT NOT NULL,
    api_name TEXT NOT NULL,
    cost_cents INTEGER NOT NULL,
    created_at TEXT NOT NULL
);
```

**WAL aktiv** (`queue.py:32`): `PRAGMA journal_mode=WAL`, `PRAGMA busy_timeout=5000`.

⚠️ **`cost_ledger` ist totes Schema** — kein einziges INSERT im Code. Cost wird aggregiert auf `video_jobs.cost_cents` geschrieben.

## Concurrency

- `MAX_WORKERS = 2` (queue.py:19)
- `MAX_RETRIES = 2` (queue.py:20)
- ThreadPoolExecutor mit `thread_name_prefix="video"`
- `_lock = threading.Lock()` schützt `_active`-Dict (Z.26)
- Sub-Pipeline (Video+Music): nochmal eigener ThreadPool max=2 (`pipeline.py:65-101`)

**Recovery bei Crash** (`queue.py:66-70`): Beim Boot werden alle Jobs mit `status='processing'` auf `status='queued'` zurückgesetzt — kein Job bleibt stuck.

## Cost-Konstanten (alle hardcoded)

| Step | Cents | File:Line |
|---|---|---|
| Image (Flux 2 Pro) | 8 | image_gen.py:11 |
| Video ≤5s (Kling 3.0) | 56 | video_gen.py:11 |
| Video ≤10s (Kling 3.0) | 112 | video_gen.py:12 |
| Music (Mubert) | 7 | audio.py:11 |
| Postprocess | 0 | — |

**Standard-Job-Kosten** (8s Video + Musik): 8 + 112 + 7 = **127 Cents** (~1.27€).

## ENV-Vars (alle Pflicht außer MUBERT)

| Variable | Required | File:Line | Verhalten bei Missing |
|---|---|---|---|
| `CLAUDE_API_KEY` | ✅ | prompt_builder.py:73 | RuntimeError |
| `FAL_KEY` | ✅ | image_gen.py:31, video_gen.py:34 | StepResult(success=False) → Pipeline-Abort |
| `MUBERT_API_KEY` | ⚠️ optional | audio.py:33 | Music wird übersprungen (Pipeline läuft weiter, Video ohne Track) |

**Fehlt im `.env.example`** (vgl. 01-Entry-Points).

## Cleanup-Strategie (`cleanup.py`)

- `media/workspace/{job_id}/` — TTL **1 Stunde** (Default)
- `media/output/{job_id}.mp4` — TTL **48 Stunden** (Default)
- Lösch-Trigger: `Scheduler` täglich 03:00 (`bot/scheduler.py:565`)
- Windows-File-Locking-Tolerance: `_safe_delete()` mit 3 Retries × 2s Delay (`cleanup.py:35-44`)

## Brand-Style-Mapping (`brand_mapping.py`)

Liest `config/brand_style_map.json`, mapt `tone_keywords` (z.B. „professionell") auf:

```json
{
  "image":  {"lighting", "colors", "composition"},
  "video":  {"camera_move", "duration_sec", "energy"},
  "audio":  {"mood", "genre", "bpm_range"},
  "color":  {"lut", "grain"},
  "text":   {"font", "highlight_color", "position"}
}
```

Fallback-Style (wenn JSON fehlt) — `brand_mapping.py:52-61` mit harten Defaults: Montserrat-Bold, weiß, bottom_center, neutral_sharp LUT, 90–110 BPM ambient, slow zoom, low energy.

## Stärken & Schwächen

**Stärken (code-belegt):**
- Recovery bei Crash via `processing→queued`-Reset
- Try-Finally für Workspace-Cleanup
- Retry-Logik in image_gen + audio
- EU AI Act Art. 50(2) Compliance-Metadaten in Output-MP4
- Music-Fehlertoleranz (non-fatal)
- WAL-Modus für Concurrency

**Schwächen (alle code-belegt, vgl. 14-Findings):**
- `cost_ledger`-Schema definiert aber unbenutzt (queue.py:55-63 vs. Code)
- `MAX_WORKERS=2` hardcoded — kein Skalieren
- `MAX_RETRIES=2` hardcoded
- FFmpeg-Timeout 300s reicht für 10s-Output, würde bei längeren Videos brechen
- Mubert-Polling fix 3s ohne Backoff (audio.py:97)
- Kein DB-Index auf `video_jobs(status, created_at)` — bei vielen Jobs würde SELECT langsam
- ENV-Vars `FAL_KEY` + `MUBERT_API_KEY` sind nicht im `.env.example` dokumentiert

## Verbundene Notes

- [[Socibot/modules/02-Bot-Core]] — Scheduler ruft `_process_video_queue` alle 15min, `_cleanup_video_media` täglich
- [[Socibot/modules/06-Dashboard-Routes]] — `video.py` Route + `erstellen.py` Hub
- [[Socibot/modules/09-Brand-System]] — `config/brand_style_map.json`, gelesen von brand_mapping
- [[Socibot/modules/11-Data-Storage]] — `data/video_jobs.db`-Details
