---
title: 11 — Data-Storage
tags: [socibot, modul, data, sqlite]
date: 2026-04-27
source_of_truth: code
---

# 11 — Data-Storage (`data/`)

> SQLite + Test-Outputs.

## `data/video_jobs.db` (SQLite, WAL)

Schema in `video/queue.py:38-63`:

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

**Pragmas:** `journal_mode=WAL`, `busy_timeout=5000` (Z.32–33).

**Indexes:** Keine. Query `SELECT … WHERE status='queued' ORDER BY created_at ASC` (Z.94–97) wird mit wachsender Job-Zahl langsamer.

**`cost_ledger` ist totes Schema** — kein einziger INSERT im gesamten Codebase. Cost wird auf `video_jobs.cost_cents` aggregiert.

**WAL-Files sichtbar:** `data/video_jobs.db-shm`, `data/video_jobs.db-wal` (vgl. `git status`).

### Wer schreibt

- `video/queue.py:78-82` (INSERT)
- `video/queue.py:120-122,133-135,156-159,163-165,68-70` (UPDATEs für status-Übergänge + Recovery)

### Wer liest

- `video/queue.py:175-188,190-206,208-222` (Stats, Status, Recent)
- `dashboard/routes/erstellen.py:16-28` (Recent Videos für Hub)
- `dashboard/routes/video.py:12-32` (Queue-Page, Status-Polling)

## `data/test_prompt.json`

Manuelles Test-Fixture für Prompt-Builder. Top-Level-Struktur:

```json
{
  "style": {
    "primary_tone": "professionell",
    "image":  { "lighting", "colors", "composition" },
    "video":  { "camera_move", "duration_sec", "energy" },
    "audio":  { "mood", "genre", "bpm_range" },
    "color":  { "lut", "grain" },
    "text":   { "font", "highlight_color", "position" }
  }
}
```

Verifiziert via Read 2026-04-27. Keine Code-Stelle liest die Datei direkt — wahrscheinlich für manuelle Pipeline-Tests via Python-REPL.

## `data/video_test/`

Outputs vorheriger Pipeline-Tests. Verifiziert vorhanden:
- `fake_kling_output.mp4`
- `final_composite.mp4`
- `final_with_ai_meta.mp4`

Keine Code-Referenz — Test-Artifacts.

## Verbundene Notes

- [[Socibot/modules/04-Video-Engine]] — Schema-Owner
- [[Socibot/modules/10-Client-State]]
- [[Socibot/modules/17-Layer-Database]]
