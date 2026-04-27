---
title: 02 — Bot-Core
tags: [socibot, modul, bot]
date: 2026-04-27
source_of_truth: code
---

# 02 — Bot-Core (`bot/`, 1.714 LOC, 8 Files)

> Scheduler-Herz, Posting-Engine, Content-Calendar, DM/Comment-Auto-Reply, Analytics, Config, Konstanten.

## Files

| Datei | LOC | Zweck |
|---|---|---|
| `__init__.py` | 1 | Package-Marker |
| `analytics.py` | 179 | Post-Performance + Interaction-Tracking |
| `config.py` | 95 | ENV-Loading, Posting-Schedule-Defaults |
| `constants.py` | 124 | Enums (PostStatus / ApprovalStatus / Platform / …), `CLAUDE_MODEL` |
| `content_calendar.py` | 273 | Plan-Storage + Wochenplan-Generierung |
| `dm_handler.py` | 260 | Intent-Detection + Auto-Reply via Claude |
| `poster.py` | 191 | Plattform-Switch + tenacity-Retry |
| `scheduler.py` | 599 | `schedule`-basierter Job-Loop, Engagement-Polling, Reports |

## `constants.py` — die zentralen Werte

- `CLAUDE_MODEL = "claude-sonnet-4-6"` (Z.76) — **Model-String veraltet** (vgl. 14-Findings). Aktueller Stand 2026-04: claude-sonnet-4-5 ist die produktive Linie. „4-6" sieht nach Tippfehler oder Vorab-Modell aus.
- `DEFAULT_SCHEDULE` Z.79–85 — Fallback-Zeiten pro Plattform
- `STATUS_ICONS` Z.88–95 — `[KI]`, `[OK]`, etc. für UI/CLI
- `PLATFORMS_ACTIVE` Z.98–103 vs. `PLATFORMS_STUB` Z.106–108 — TikTok ist Stub
- `safe_id(value)` Z.116–118 — Regex `^[a-zA-Z0-9_\-]+$` (Path-Traversal-Schutz)
- `is_placeholder_token(value)` Z.121–123 — Default-Token-Erkennung

## `config.py` — Boot-Loader

`load_config()` Z.54–94:
1. `dotenv.load_dotenv()` Z.6 (Auto-Reload-fähig via `bot.config.reload_config`)
2. Erfordert `CLAUDE_API_KEY` (Z.13–15, sys.exit wenn fehlt)
3. Lädt Schedule via `dashboard.services.variant_service.get_platform_schedules()` (Z.41–43)
4. **Fallback** wenn Service nicht verfügbar — `_build_posting_schedule()` Z.38–51 mit Hardcodes:
   - Instagram 09:00, 18:00 · Facebook 10:00, 17:00 · LinkedIn 08:30, 12:00 · Twitter 09:00, 13:00, 18:00 · TikTok 15:00, 20:00
5. Ergebnis-Dict mit pro-Plattform-Sektion (api_key, account_id, etc.)

`validate_config(config)` Z.11–35:
- Token-Whitelist-Prüfung pro Plattform; bei Placeholder → log.warning
- E-Mail-Default `info@mindrails.de` (Z.85) — hardcoded fallback

## `scheduler.py` — Herzstück (599 LOC)

**Wichtig:** `import schedule` (Z.12) — **kein APScheduler**, obwohl der README das behauptet.

### Registrierte Jobs (`setup_schedule()` Z.540–571)

| Job | Frequenz | Methode | Zeile |
|---|---|---|---|
| Posting pro Plattform/Zeit | täglich `at(t)` | `_post_platform(platform=p)` | 544–547 |
| Engagement-Check (DMs/Comments) | alle 15min | `check_and_reply` | 550 |
| Media-Queue-Poll | alle 5min | `post_approved_media` | 553 |
| JIT-Variant-Generation | alle 30min | `_check_jit_generation` | 556 |
| Supabase-Sync | alle 5min | `_sync_supabase` | 559 |
| Video-Queue-Poll | alle 15min | `_process_video_queue` | 562 |
| Video-Cleanup | täglich 03:00 | `_cleanup_video_media` → `video.cleanup.cleanup_old_media` | 565 |
| Daily-Report | täglich 21:00 | `daily_report` (Email + stdout) | 568 |
| Weekly-Plan | montags 07:00 | `weekly_plan` | 571 |

**Main-Loop** Z.589–591: `while True: schedule.run_pending(); time.sleep(30)` — Granularität 30s.

### Engagement-Polling (`check_and_reply` Z.223)

Pro Plattform eine Methode `_reply_<platform>` (Z.237–388):
- **Instagram** (Z.260–312): max 3 Posts × 5 Comments + 5 Mentions; Dedup via `client/replied_comments.json` (Z.275–312, Cap 500 IDs)
- **Twitter** (Z.314–342): max 5 Mentions
- **Facebook** (Z.344–369): 3 Posts × 3 Comments
- **LinkedIn** (Z.371–388): 3 Comments pro Post
- **Spam-Skip:** Bei Intent `spam` wird kein Reply abgesetzt (Z.300, 338)
- **Eskalations-Email:** bei Intent `beschwerde` oder Keywords (Z.54–57 in `dm_handler.py`)

### Idempotenz-Mechanismen

1. **Instagram Comment-Dedup:** `client/replied_comments.json` (Set, max 500). Ohne dies würde der Bot bei Folgen-Job alle alten Kommentare nochmal antworten.
2. **Spam-Filter:** keine Reply bei Intent="spam"
3. **Conversations-Storage:** Eskalierte Threads kriegen `escalate=true` (Z.125 in `dm_handler.py`) — aber **kein Re-Engagement-Stop nach Eskalation** (Bug-Verdacht: bei Folge-Nachrichten beantwortet Bot wieder).

## `content_calendar.py` (273 LOC)

`ContentCalendar` Klasse — File-State `client/content_calendar.json`.

**Atomic Write:** Z.112–128 mit Thread-Lock (`threading.Lock` Z.10). Schreibt erst in `*.tmp`, dann `os.replace`. → atomarer Save bei einzelnem Prozess. **Aber kein File-Lock für Multi-Process.**

`generate_weekly_plan(start_date)` Z.217–260:
- Iteriert über Plattform-Schedule (`MON 09:00`-Format, Z.34–40 Fallback)
- Topic-Rotation per Hardcode-Liste (Z.44–86): z.B. LinkedIn 7 Themes „5 Dinge die wir gelernt haben"; Brand-Override aus `client/brand_knowledge.json` (Z.88–103)
- Brand-Name-Substitution `\bFörderkraft\b` per Regex (Z.100) — ⚠️ hardcoded

`get_range_posts(start, end)` Z.198 — wird vom Calendar-Routes für Monats-Grid genutzt.

## `poster.py` (191 LOC)

Lazy-Init pro Plattform (Z.32–73): `_get_instagram` / `_get_facebook` / `_get_linkedin` / `_get_twitter` mit Token-Placeholder-Check (`"dein"` als String-Kontain).

`post(platform, content, topic, image_path, video_path)` Z.91–123:
- **Tenacity-Retry** Z.97–102: max 4 Versuche, exponential 5–120s
- Switch-Case pro Plattform (Z.104–117)
- **TikTok-Stub** Z.178–180: `return {"success": False, "error": "Video-Upload noch nicht implementiert"}`
- Failure-Pattern: `{success: False, error: str(e)}`

## `dm_handler.py` (260 LOC) — Auto-Reply

Class `DMHandler.handle(platform, sender_id, message, sender_name)` Z.232.

**Intent-Klassen** (Z.41–51): `job_interesse`, `auftraggeber`, `preis_anfrage`, `info_anfrage`, `beschwerde`, `lob`, `terminanfrage`, `spam`, `sonstiges`.

**Flow:**
1. **Eskalations-Check** Z.54–57 — Keywords `rechtlich, anwalt, klage, beschwerde, betrug, scam, abzocke, stornieren, kündigen, notar`
2. **Intent-Detection** Z.130–147 — Claude-Call max 30 Tokens, fallback `sonstiges`
3. **Brand-Kontext laden** Z.171 — `get_brand_context(platform)` aus `brand/foerderkraft_brand.py`
4. **Response-Gen** Z.219–223 — Claude max 300 Tokens
5. **Persistence** Z.97–114 — `client/conversations.json` mit 90-Tage-Retention

**Email-Eskalation** Z.86–89: Gmail SMTP_SSL Port 465. Silent-catch bei Failure (Z.90–91, nur log.warning) — Email kann lautlos verloren gehen.

## `analytics.py` (179 LOC)

`Analytics.track_post()` Z.38, `track_interaction()` Z.65 — schreiben in `client/analytics.json`. Wöchentliche Reports unter `client/reports/weekly_YYYYMMDD.json` (Z.173).

Optional Signal an `dashboard.services.learning_service.record_performance()` (Z.57–63, silent-catch).

## Daten-Fluss-Karte (bot/)

```
content_calendar.json   ◄── ContentCalendar (read+write atomic)
                        ◄── Scheduler.weekly_plan / _post_platform / post_approved_media
                        ◄── Composer / Approval-Routes (cross-module)

analytics.json          ◄── Analytics.track_*
                        ── Scheduler.daily_report (read)

conversations.json      ◄── DMHandler (read+write, 90d retention)
                        ── Postfach-Route (read, Export DSGVO)

replied_comments.json   ◄── Scheduler._reply_instagram (Dedup-Set max 500)

bot.log                 ◄── logging.FileHandler (Scheduler.__init__ Z.60)
                        ── Autopilot/Overview (Tail-Read für „Bot live?"-Heuristik)

client/media/queue/*.json ◄── Scheduler.post_approved_media
                          ◄── media_processor / approval / preview / composer / api
```

## Verbundene Notes

- [[Socibot/modules/03-Platforms]] — Plattform-APIs, die Scheduler/Poster aufrufen
- [[Socibot/modules/06-Dashboard-Routes]] — Routes, die ContentCalendar mutieren
- [[Socibot/modules/07-Dashboard-Services]] — `variant_service`, `learning_service`, `plan_service`
- [[Socibot/modules/14-Findings]] — bot-spezifische Risiken
