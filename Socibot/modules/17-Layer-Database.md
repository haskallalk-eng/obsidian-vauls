---
title: 17 — Layer Database
tags: [socibot, layer, database, persistence]
date: 2026-04-27
source_of_truth: code
---

# 17 — Layer: Persistence

> Socibot persistiert Daten an drei Orten: SQLite (1 Tabelle aktiv, 1 tote), JSON-Files (12 zentrale + 1 Verzeichnis voll), und das `.env` (mutiert von Setup-Wizard).

## Persistence-Lagen-Inventar

```
┌──────────────────────────────────────────────────────────────────┐
│ data/                                                            │
│   video_jobs.db (SQLite WAL)                                    │
│     - video_jobs   (genutzt)                                    │
│     - cost_ledger  (totes Schema, kein INSERT)                  │
├──────────────────────────────────────────────────────────────────┤
│ client/                                                          │
│   bot_settings.json          → Mode, Plan, Schedules, Pause     │
│   brand_knowledge.json       → User-Brand                       │
│   content_calendar.json      → Posts                            │
│   conversations.json         → DM/Comment-Threads (90d retent.) │
│   notifications.json         → In-App-Notifs                    │
│   replied_comments.json      → IG-Comment-Dedup-Set max 500     │
│   learning_profile.json      → Learning-Engine                  │
│   research_suggestions.json  → Letztes Research-Ergebnis        │
│   analytics.json             → Track-Daten                      │
│   reports/weekly_*.json      → write-once Wochen-Reports        │
│   submissions/*.json         → form-server Eingangskanal        │
│   media/<id>.<ext>           → Upload-Originale                 │
│   media/<id>.json            → Sidecar-Metadaten                │
│   media/queue/<id>.json      → Approval-Queue-Manifeste         │
│   media/processed/<id>.jpg   → Branded-Outputs                  │
│   brand_pdfs/<file>.pdf      → Brand-PDF-Uploads                │
├──────────────────────────────────────────────────────────────────┤
│ .env                                                             │
│   - mutiert beim Setup-Wizard via                               │
│     dashboard/routes/brand_settings.py:149-174 (regex+rewrite)  │
│   - Hot-Reload via dotenv.load_dotenv(override=True) (Z.170)    │
├──────────────────────────────────────────────────────────────────┤
│ bot.log                                                          │
│   - logging.FileHandler aus bot/scheduler.py:60                 │
│   - Tail-Read von /api/log + autopilot._bot_running heuristik   │
├──────────────────────────────────────────────────────────────────┤
│ media/                                                           │
│   workspace/<job_id>/         → Pipeline-Temp-Files (TTL 1h)   │
│   output/<job_id>.mp4         → fertige Videos (TTL 48h)       │
│   fonts/                      → Montserrat-Bold.ttf etc.       │
│   luts/                       → Color-LUTs für FFmpeg          │
└──────────────────────────────────────────────────────────────────┘
```

## SQLite-Schema vollständig

`data/video_jobs.db` — angelegt von `video/queue.py:38-63`.

```sql
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=5000;

CREATE TABLE IF NOT EXISTS video_jobs (
    job_id           TEXT PRIMARY KEY,
    client_id        TEXT NOT NULL,
    platform         TEXT NOT NULL,
    topic            TEXT NOT NULL,
    calendar_post_id TEXT DEFAULT '',
    status           TEXT NOT NULL DEFAULT 'queued',
    created_at       TEXT NOT NULL,
    started_at       TEXT,
    finished_at      TEXT,
    error            TEXT,
    cost_cents       INTEGER DEFAULT 0,
    output_path      TEXT,
    retry_count      INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS cost_ledger (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id   TEXT NOT NULL,
    job_id      TEXT NOT NULL,
    api_name    TEXT NOT NULL,
    cost_cents  INTEGER NOT NULL,
    created_at  TEXT NOT NULL
);
```

**Indexes:** Keine über Primary Key hinaus.

**Status-Werte (`status`):** `queued | processing | done | failed`. Übergänge in `video/queue.py:120-166`.

**`cost_ledger` ist totes Schema** — kein einziger INSERT (siehe 14-Findings § M4).

## JSON-Schemas verlinkt

Alle Schemas in [[Socibot/modules/10-Client-State]] dokumentiert.

## Read/Write-Matrix (Persistence-Layer)

| Datei | Reader | Writer |
|---|---|---|
| `bot_settings.json` | autopilot, calendar, fragebogen, learning, plan_service, variant_service | fragebogen, plan_service, supabase_sync, variant_service |
| `brand_knowledge.json` | api, brand_settings, fragebogen, learning, ai_vision, brand_extractor, content_calendar, dm_handler, research_agent, video/queue, alle Content-Gens (indirekt via brand-Service) | api, brand_settings, brand_extractor, fragebogen, supabase_sync |
| `content_calendar.json` | approval, calendar, composer, overview, postfach, preview | approval, calendar, composer (alle direkt; nur ContentCalendar-Klasse atomic) |
| `conversations.json` | overview, postfach | postfach, dm_handler |
| `learning_profile.json` | learning, learning_service | learning_service |
| `notifications.json` | api | notification_service |
| `replied_comments.json` | scheduler | scheduler |
| `research_suggestions.json` | api | research_agent |
| `analytics.json` | (overview indirekt) | analytics |
| `media/queue/*.json` | api, approval, composer, media, preview | api, approval, composer, media, media_processor |
| `media/<id>.json` (sidecar) | learning, media, overview | media, media_processor |
| `submissions/*.json` | brand_settings, overview | server/form_server |
| `data/video_jobs.db` | erstellen, video, queue | queue (CRUD) |
| `.env` | bot/config (load_dotenv) | brand_settings (Setup-Wizard) |
| `bot.log` | autopilot, overview | bot/scheduler |

## Atomic-Write-Praxis

- **Atomic implementiert:** `bot/content_calendar.py:112-128` (tmp + os.replace, mit Lock)
- **Direct write_text überall sonst** — kein zentrales Util

## Migrations / Schema-Evolution

- **JSON-Files:** keine Versionierung außer in `learning_profile.json:version=2` (`learning_service.py:72-77` mit silent-migrate-Block)
- **SQLite:** `CREATE TABLE IF NOT EXISTS` in `_init_db()` — funktioniert für Add-Column nicht (würde fehlschlagen). Aktuell aber kein Migrations-Hook implementiert.

## Backup-Strategie (verifiziert)

**Es gibt keine.** Keine Backup-Routinen, keine Snapshot-Job-Konfig, keine zweite Schreib-Stelle.

→ Bei `client/`-Loss: alle Posts, Konversationen, Lerndaten weg.

## Verbundene Notes

- [[Socibot/modules/10-Client-State]]
- [[Socibot/modules/11-Data-Storage]]
- [[Socibot/modules/14-Findings]] — Race Conditions, fehlendes Atomic-Pattern
