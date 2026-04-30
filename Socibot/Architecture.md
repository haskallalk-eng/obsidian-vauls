---
title: Socibot Architektur-Snapshot
type: architecture
status: active
parent: "[[Socibot/Overview]]"
created: 2026-04-30
---

# Socibot — Architektur (Stand 2026-04-30 nach Welle 0–W1.5)

Aktuelle Architektur nach 19 Commits. Ergänzt die Pre-Welle-0-Module-Notes ([[Socibot/modules/16-Layer-Backend]] etc.) — die sind seit 2026-04-27 nicht aktualisiert.

## Top-Level-Layout

```
Desktop/Social media Bot/
├── bot/                       # Core-Bot, Scheduler, Posting
│   ├── jobs/                  # NEU: Cron-Jobs (refresh_meta, retention, compliance, eval)
│   ├── poster.py              # OAuth-priority + .env-fallback
│   ├── scheduler.py           # schedule-Library, alle Cron-Hooks zentral
│   └── ...
├── compliance/                # NEU: 5 Persona-Regelwerke (Anwalt, Arzt, etc.)
│   ├── anwalt.json            # BORA, BRAO, UWG-Patterns
│   ├── arzt.json              # HWG, MBO-Ä-Patterns
│   ├── heilpraktiker.json     # HWG, HeilprG-Patterns
│   ├── coach.json             # PsychThG, HWG-Patterns
│   └── steuerberater.json     # StBerG, BOStB-Patterns
├── dashboard/
│   ├── routes/
│   │   ├── auth.py            # NEU: register/login/logout
│   │   ├── account.py         # NEU: DSGVO Art. 17 Account-Delete
│   │   ├── oauth_meta.py      # NEU: Click-to-Connect IG/FB
│   │   ├── compliance.py      # NEU: /compliance/check|override|audit
│   │   ├── eval_dashboard.py  # NEU: /eval/ Operator-Dashboard
│   │   ├── erstellen.py       # NEU: Composer + Video-Generator-Hub
│   │   └── ...
│   ├── services/
│   │   ├── connections_service.py  # NEU: Fernet-encrypted OAuth-Tokens
│   │   ├── meta_oauth_service.py   # NEU: Meta OAuth-Flow + Token-Refresh
│   │   ├── compliance_service.py   # NEU: Hybrid Layer 1+2 Risk-Check v2
│   │   ├── eval_logger.py          # NEU: DSGVO-konformes Generation-Logging
│   │   ├── cost_tracker.py         # NEU: Tier-Drift-Alerts mit SQLite-History
│   │   ├── llm_judge.py            # NEU: Opus als Quality-Judge
│   │   ├── user_service.py         # NEU: User-Auth + Account-Delete
│   │   └── ...
│   └── templates/                  # marke.html + setup.html W0.75-refactored
├── data/
│   ├── critique_rubric.json        # NEU: Quality-Rubric (5 Dimensionen)
│   ├── compliance_reasons.json     # NEU: Reason-Code-Tabelle (13 Codes)
│   ├── compliance_audit.jsonl      # gitignored, hash-only Audit-Trail
│   ├── compliance_cache.json       # gitignored, 24h-Cache
│   ├── compliance_cost_log.jsonl   # gitignored, Layer-2-Cost-Tracking
│   ├── generation_log_YYYY-MM.jsonl # gitignored, Fernet-encrypted
│   └── eval/                       # gitignored, Baseline-Snapshots
├── tools/eval/                     # NEU: CLIs
│   ├── generate_gold_set.py        # 250-Case Test-Set
│   ├── run_baseline.py             # Baseline-Runner mit Generator+Judge
│   └── compare_baseline.py         # Regression-Block-Tool (-5% Drift = exit 1)
├── tests/                          # 165 Tests grün, 0 skipped
└── client/                         # gitignored, User-State (brand_knowledge etc.)
```

## Compliance-Pipeline (Layer 1 + 2 Hybrid)

```
Generation-Output
       │
       ▼
┌──────────────────────────────────┐
│ Layer 1 — Deterministic (Regex)  │  ~50ms
│ Pattern-Set aus compliance/<persona>.json
│ Hard-Blocks: BORA-6, HWG-3, etc.
│ Soft-Blocks: subtle violations
└──────────────────────────────────┘
       │
       ├── Hard-Block? → Reject (kein Override)
       │
       ▼
┌──────────────────────────────────┐
│ Layer 2 — Claude-Judge           │  ~2-3s
│ Gating:
│   - Tier ≥ premium ODER
│   - Persona ∈ HIGH_RISK (arzt, heilpraktiker)
│   - + api_key vorhanden
│   - + Cost-Cap nicht erreicht
│ Branchen-spezifisches Reasoning
│ Reason-Codes (HWG-3, BORA-6, etc.)
│ Fail-closed für arzt/heilpraktiker
└──────────────────────────────────┘
       │
       ├── Risk=high → Hard-Block
       ├── Risk=medium → Soft-Block (User-Override mit Justification + Audit-Log)
       └── Risk=low → Warning (Post wird trotzdem published)

Persona kommt aus client/brand_knowledge.json (single source of truth, NICHT Request-Body)
Cost-Cap €5/User/Monat (`LAYER2_COST_CAP_EUR_PER_MONTH`)
DSGVO-Audit: hash-only Content, 90d-Retention via täglich 04:30 Cron
```

## Eval-Pipeline (W0.5)

```
Generation-Call (variant_service._generate_with_instruction)
       │
       │  returns (content, meta) — meta hat tokens, latency, model
       ▼
┌──────────────────────────────────┐
│ eval_logger.log_generation()      │
│ - HMAC-pseudo user_id            │
│ - Fernet-encrypted prompt+output │
│ - SHA-256 topic_hash             │
│ - JSONL-Append + FileLock        │
│ → log_entry_id im Variant-Dict   │
└──────────────────────────────────┘
       │
User-Approval/Rejection (approval.py)
       │
       ▼
┌──────────────────────────────────┐
│ eval_logger.record_user_feedback │  ← W0.5b-Hook
│ - In-place Update via tmp+rename │
│ - Action + Reason persistiert    │
└──────────────────────────────────┘

Async tools/eval/run_baseline.py:
  → Gold-Set (250 Cases, 5×5×10) durchspielen
  → llm_judge.score_output() (Opus als Judge — Bias-Reduktion)
  → BaselineSnapshot mit per-Persona/Platform/Dimension-Aggregation

Async tools/eval/compare_baseline.py:
  → BEFORE.json vs AFTER.json
  → Regression-Block bei Persona-Drift > 5%
  → Exit 1 für CI-Hook

Operator-Dashboard /eval/:
  → cost_tracker.get_dashboard_data() — aktuelle Tier-Costs vs. Sollwerte
  → Drift-Alerts (warn ≥15%, alert ≥30%)
  → Daily-Snapshot via Cron 04:40
```

## Auth + OAuth-Flow (Phase 1.1)

```
Customer → /register → user_service.create_user()
                     → users.json (gitignored)

Customer → /einstellungen/marke
       → Click "Meta verbinden" → /auth/meta/connect
                                → HMAC-signed state
                                → redirect zu Facebook OAuth-Dialog
                                → /auth/meta/callback?code=...
                                → Fernet-encrypted Token-Storage
                                → connections_service.save_user_connection()
                                → /auth/meta/select-page
                                → connections.json (gitignored, encrypted at-rest)

Bot-Posting:
  poster.py → connections_service.resolve_token("instagram"|"facebook")
            → Lazy-Refresh wenn expires_at < +14d
            → Fallback auf .env nur bei OAuth-Fehlern
            → Nightly Refresh-Job 03:01 (Cron)
            → 90d-Retention für expired connections

Customer → /einstellungen/konto/loeschen (DSGVO Art. 17)
       → Meta-Permission-Revoke (best-effort)
       → users.json + connections.json + alle User-State weg
```

## Operator-Gating

Backend-Routes für Token-Operations sind via `_is_operator_request()` geschützt:
```
1. ENV-Flag OPERATOR_MODE_ENABLED=true (Dev-Convenience)
   ODER
2. ADMIN_SECRET als Header `X-Admin-Secret` ODER Body-Field `admin_secret`
```

Customer kann nur SMTP-Keys schreiben (`/einstellungen/token-speichern` mit allowed_keys ⊆ SMTP). LinkedIn/Twitter-Tokens sind temporär Operator-only via .env, bis Phase 1.3 OAuth-Flows bringt.

## Concurrency-Sicherheit

| File | Lock | Pattern |
|---|---|---|
| `client/connections.json` | `_lock` (RLock) + FileLock | tmp+rename atomic write |
| `client/bot_settings.json` | `_settings_lock` + FileLock | tmp+rename |
| `data/compliance_audit.jsonl` | `_audit_lock` + FileLock | append + atomic prune |
| `data/compliance_cache.json` | `_cache_lock` + FileLock | tmp+rename |
| `data/compliance_cost_log.jsonl` | `_cost_lock` + FileLock | append |
| `data/generation_log_YYYY-MM.jsonl` | `_log_lock` + FileLock | append + tmp+rename für Updates |
| `data/eval/cost_history.db` | SQLite WAL-Mode | per-row-locking |
| `.env` (Key-Autogen) | `_env_lock` + FileLock | tmp+rename |

**Risiko**: `filelock` ist NICHT in `requirements.txt` — Service degradiert silent auf threading-only. Bei `gunicorn workers≥2` (Production) zwingend `pip install filelock>=3.13`.

## Cron-Schedule

| Zeit | Job | Zweck |
|---|---|---|
| 03:00 | `_cleanup_video_media` | Video-Temp-Files |
| 03:01 | `_run_meta_token_refresh` | Long-Lived-Token-Refresh (täglich, refresh wenn expires < +14d) |
| 04:00 | `_run_retention_cleanup` | Connections älter 90d nach `expires_at` |
| 04:30 | `_run_compliance_audit_pruning` | Compliance-Audit-Trail-Retention |
| 04:35 | `_run_eval_log_rotation` | Generation-Logs > EVAL_LOG_RETENTION_DAYS |
| 04:40 | `_run_eval_cost_snapshot` | Tier-Cost-Drift-Snapshot pro Tier |
| 21:00 | `daily_report` | Tagesreport |
| alle 5min | `post_approved_media` | Posting-Queue |
| alle 5min | `_sync_supabase` | Customer-Submissions importieren |
| alle 15min | `check_and_reply` | DM/Comment-Auto-Reply |
| alle 15min | `_process_video_queue` | Video-Pipeline |
| alle 30min | `_check_jit_generation` | Just-in-Time Variant-Generation |

## Storage-Pattern-Inventar

| Pattern | Wo | Begründung |
|---|---|---|
| **JSON + FileLock + tmp+rename** | connections.json, bot_settings.json, compliance_cache.json, users.json | Niedrige Schreibrate, atomic-write reicht |
| **JSONL append-only** | compliance_audit.jsonl, compliance_cost_log.jsonl, generation_log_*.jsonl | Hohe Append-Rate, Reads selten |
| **SQLite WAL** | video_jobs.db, post_embeddings.db (geplant), cost_history.db | Hohe Such-Rate, Trends, Aggregation |

Codex-Beobachtung: 4 Storage-Patterns parallel ist akzeptable Spezialisierung, aber Wartung wird komplexer. Phase-2-Multi-Tenant könnte ein einheitliches DB-Layer sinnvoll machen.

## Verwandte Notes

- [[Socibot/Overview]] — Aktueller Stand
- [[Socibot/Codex-Findings-2026-04-30]] — Review-Ergebnisse
- [[Socibot/DoD]] — Definition of Done
- [[Socibot/modules/16-Layer-Backend]] — Pre-Welle-0-Architektur (veraltet, nur als Vergleich)
