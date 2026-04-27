---
title: 10 — Client-State
tags: [socibot, modul, state, client]
date: 2026-04-27
source_of_truth: code
---

# 10 — Client-State (`client/`)

> File-basierter State. Keine Datenbank außer `data/video_jobs.db`.

## Files (verifiziert)

| Datei | Zweck | Lese-Lock | Schreib-Lock | Atomic Write |
|---|---|---|---|---|
| `client/bot_settings.json` | Mode, Plan, Schedules, Pause-States | nein | per `_lock` in plan/variant_service | ❌ Direct |
| `client/brand_knowledge.json` | Brand-Identität (User-Override) | nein | nein | ❌ Direct |
| `client/content_calendar.json` | Posts mit Status, Variants, Approval | nein | `threading.Lock` in `bot/content_calendar.py:10` | ✅ tmp+`os.replace` (`content_calendar.py:112-128`) |
| `client/conversations.json` | DM/Comment-Threads, 90d Retention | nein | nein | ❌ Direct |
| `client/notifications.json` | In-App-Notifs | `threading.Lock` (`notification_service.py:14`) | wie lesen | ❌ Direct |
| `client/replied_comments.json` | Dedup-Set max 500 | nein | nein | ❌ Direct |
| `client/learning_profile.json` | Learning-Engine | `threading.Lock` (`learning_service.py:84`) | wie lesen | ❌ Direct |
| `client/research_suggestions.json` | Letztes Agent-Research-Result | nein | nein | ❌ Direct |
| `client/analytics.json` | Track-Daten (von `bot/analytics.py`) | nein | nein | ❌ Direct |
| `client/reports/weekly_YYYYMMDD.json` | Weekly-Reports | nein | nein | ❌ Direct (write-once) |
| `client/submissions/<file>.json` | Form-Server-Submissions | nein (read-only von Routes) | server schreibt | ❌ Direct |
| `client/media/<id>.<ext>` + `<id>.json` | Upload-Originale + Sidecar | nein | nein | ❌ Direct |
| `client/media/queue/<id>.json` | Approval-Queue-Manifeste | nein | nein | ❌ Direct |
| `client/media/processed/<id>.jpg` | Branded-Outputs | nein (binary) | nein | ❌ Direct |

## Schemas (verifiziert)

### `bot_settings.json`

```json
{
  "mode": "copilot" | "autopilot",
  "copilot_settings": {
    "variants_count": 3,
    "auto_approve_threshold": 0.85,
    "weekly_review_day": "Sonntag",
    "weekly_review_time": "18:00"
  },
  "autopilot_settings": {
    "veto_window_minutes": 60
  },
  "paused_platforms": ["facebook", "linkedin", "tiktok", "twitter"],
  "plan": "trial" | "starter" | "pro" | "agency",
  "plan_expires": "ISO-Date",
  "stripe_customer_id": "cus_…",
  "stripe_subscription_id": "sub_…",
  "posts_this_month": 12,
  "month_reset_date": "ISO-Date",
  "activated_at": "ISO-Date",
  "platform_schedules": {
    "instagram": { "days": ["MON", ...], "times": ["09:00", ...] },
    ...
  }
}
```

### `content_calendar.json` (via `bot/content_calendar.py`)

Top-Level: `{ "posts": [...] }`. Pro-Post:

```json
{
  "id": "uuid",
  "platform": "instagram|facebook|linkedin|twitter|tiktok",
  "topic": "string",
  "content": "string|null",
  "scheduled_time": "ISO datetime",
  "status": "geplant|generiert|freigegeben|gepostet|abgelehnt|fehler",
  "approval_status": "pending|freigegeben|abgelehnt",
  "variants": [
    { "variant_id": "8-char", "type": "A|B|C", "label": "...",
      "content": "...", "topic": "...", "ai_score": 0.0..1.0,
      "generated_at": "ISO", "selected": bool }
  ],
  "approval_note": "string?",
  "rejection_reason_category": "string?",
  "rejection_reason_text": "string?",
  "post_id": "string? (von Plattform nach Post)"
}
```

### `learning_profile.json` (via `learning_service.py`)

```json
{
  "version": 2,
  "updated_at": "ISO",
  "per_platform": {
    "instagram": {
      "approved_topics": [...],
      "approved_styles": [...],
      "rejected_topics": [...],
      "rejected_styles": [...],
      "rejection_reasons": [...],
      "approval_history": [
        { "post_id", "topic", "variant_type", "ai_score",
          "content_len", "excerpt", "timestamp", "approval_note" }
      ],   // max 200
      "performance_data": [
        { "post_id", "topic", "excerpt", "likes", "comments",
          "shares", "reach", "saves", "engagement_rate", "timestamp" }
      ],   // max 100
      "rejection_history": [...],   // max 100
      "learned_patterns": { "approval_rate": 0.0..1.0, "preferred_type": "A|B|C", ... },
      "style_analysis": "Claude-generated 4-Regeln-Text",
      "style_analysis_at": "ISO",
      "interactions_since_meta": 0
    },
    "facebook": {...},
    ...
  },
  "global": {
    "always_avoid": [...],
    "always_prefer": [...]
  }
}
```

### `conversations.json` (via `dm_handler.py`)

Top-Level Liste:

```json
[
  {
    "platform": "instagram|facebook|...",
    "sender_id": "string",
    "sender_name": "string",
    "type": "comment|dm",
    "message": "string",
    "intent": "job_interesse|preis_anfrage|...",
    "response": "string",
    "escalate": bool,
    "timestamp": "ISO"
  }
]
```

90-Tage-Retention enforced in `dm_handler.py:97-114`.

### `notifications.json`

Liste mit:

```json
[
  { "id": "uuid",
    "type": "approval|generation|posted|error|...",
    "message": "string",
    "post_id": "string?",
    "platform": "string?",
    "scheduled_time": "ISO?",
    "link": "/url?",
    "read": bool,
    "created_at": "ISO" }
]
```

Rotation: Ungelesene unbegrenzt, gelesene max 80 (`notification_service.py:29`).

### `replied_comments.json`

Top-Level: `{ "instagram_comments": ["id1", "id2", ...] }` — Set-Storage als Liste, max 500 Einträge (`scheduler.py:311`).

### `research_suggestions.json`

```json
{
  "generated_at": "ISO",
  "trends": [
    { "title", "summary", "source_url" }
  ],
  "topics": [
    "string",
    ...
  ]
}
```

Max 10 Topics × 200 Zeichen (verifiziert in `api.py` Zeilen 161–162).

### `submissions/<filename>.json`

Form-Submissions vom externen Form-Server (Port 5050). Schema in `server/form_server.py:50-100` `_map_submission_to_brand()`. Wird von `dashboard/routes/brand_settings.py:255-314` `/einstellungen/submission-importieren` POST gelesen.

### `analytics.json`

Schema nicht im Detail dokumentiert, aber `bot/analytics.py:17-36` zeigt:
- Top-Level: `{ "posts": [...], "interactions": [...] }`
- Posts: `{ post_id, platform, topic, timestamp, likes, reach, comments, engagement_rate }`
- Interactions: `{ platform, type (dm|comment|mention), intent, timestamp }`

### `reports/weekly_YYYYMMDD.json`

Generiert von `bot/analytics.py:161-176` `generate_weekly_report()`. Inhalt nicht im Detail verifiziert.

## Race-Condition-Hotspots

**Höchstes Risiko:**
- `content_calendar.json` — 6+ Routes schreiben, nur Bot-internal `ContentCalendar` hat Lock (Z.10). Routes wie `approval.py` schreiben direkt mit `Path.write_text()` — kein Lock-Sharing.
- `brand_knowledge.json` — 5 Schreibstellen ohne gemeinsamen Lock

**Mittleres Risiko:**
- `bot_settings.json` — `plan_service` und `variant_service` haben jeweils eigene Locks; cross-process unsafe
- `notifications.json` — Lock nur innerhalb `notification_service`

**Atomic-Pattern existiert nur** in `bot/content_calendar.py:112-128` (tmp + `os.replace`). Kein anderer Schreiber nutzt es.

## Verbundene Notes

- [[Socibot/modules/02-Bot-Core]]
- [[Socibot/modules/06-Dashboard-Routes]]
- [[Socibot/modules/07-Dashboard-Services]]
- [[Socibot/modules/14-Findings]]
- [[Socibot/modules/17-Layer-Database]]
