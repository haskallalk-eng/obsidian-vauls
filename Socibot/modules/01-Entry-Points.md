---
title: 01 — Entry-Points
tags: [socibot, modul, entry-points]
date: 2026-04-27
source_of_truth: code
---

# 01 — Entry-Points

> Code-belegte Bestandsaufnahme der Boot-Skripte + Konfigurations-Top-Level. Zeilen-Referenzen relativ zur jeweiligen Datei.

## `start_bot.py` (115 LOC, der reale Entry)

**Was es macht:** Voller Boot mit drei Threads:
1. **Dashboard** auf `0.0.0.0:5000` — `start_dashboard()` Z.38–45 (Flask `app.run(debug=False, use_reloader=False)`)
2. **Form-Server** auf Port 5050 (in eigenem Thread) — `start_form_server()` Z.26–35, lädt `server/form_server.py:run_server`
3. **Bot-Scheduler** (blockierend) — `Scheduler(config).run()` Z.113

**Boot-Sequenz:**
- `print_banner()` Z.48–67 — ASCII-Banner mit Brand-Name aus `brand.foerderkraft_brand.get_brand()` (Fallback "Socibot")
- `load_config()` Z.102 — siehe `02-Bot-Core` § Config
- `check_config(config)` Z.70–97 — Token-Whitelist-Check pro Plattform; CLAUDE_API_KEY Pflicht (Z.89–91, sys.exit(1) wenn fehlt)
- `validate_config(config)` Z.106 — siehe Config-Loader

**Side-Effects:**
- Schreibt UTF-8 stdout (Z.11)
- Setzt `sys.path.insert(0, …)` für relative Imports (Z.18)
- Loggt aktive Plattformen
- Startet `dashboard_thread = threading.Thread(target=start_dashboard, daemon=True)` (Z.109)

## `main.py` (9 LOC — legacy mini-entry)

```python
from bot.scheduler import start_scheduler
from bot.config import load_config
if __name__ == "__main__":
    print("Instagram Bot startet...")
    config = load_config()
    start_scheduler(config)
```

Wird im README **nicht** erwähnt, kein Dashboard. Wirkt wie der Original-Entry vor dem Dashboard-Refactor. Side-Effect: lädt Config, ruft `start_scheduler()` (Wrapper auf `Scheduler(config).run()`).

## `requirements.txt` (14 Einträge)

```text
anthropic>=0.40.0,<1.0.0
requests>=2.31.0,<3.0.0
python-dotenv>=1.0.0,<2.0.0
schedule>=1.2.0,<2.0.0
requests-oauthlib>=1.3.1,<2.0.0
flask>=3.0.0,<4.0.0
pillow>=10.0.0,<11.0.0
openai>=1.0.0,<2.0.0
werkzeug>=3.0.0,<4.0.0
tenacity>=8.2.0,<10.0.0
claude-agent-sdk>=0.1.0
stripe>=7.0.0,<10.0.0
fal-client>=0.5.0,<1.0.0
httpx>=0.27.0,<1.0.0
```

**Beobachtung:** Kein APScheduler — der Scheduler nutzt `schedule` (vgl. `02-Bot-Core` § Scheduler). Im README + README sprechen aber von APScheduler — Diskrepanz.

## `.env.example` (47 LOC)

| Variable | Pflicht | Zweck |
|---|---|---|
| `CLAUDE_API_KEY` | ✅ | Anthropic Messages API + Vision (überall) |
| `NOTIFY_EMAIL` | optional | Eskalations-Email-Empfänger |
| `SMTP_EMAIL`, `SMTP_PASSWORD` | optional | Gmail-SMTP für Notifications |
| `INSTAGRAM_ACCESS_TOKEN`, `INSTAGRAM_ACCOUNT_ID` | per-Plattform | Meta Graph |
| `FACEBOOK_ACCESS_TOKEN`, `FACEBOOK_PAGE_ID` | per-Plattform | Meta Graph |
| `LINKEDIN_ACCESS_TOKEN`, `LINKEDIN_PERSON_ID` | per-Plattform | LinkedIn v2 |
| `TWITTER_BEARER_TOKEN` + 4× OAuth1-Felder | per-Plattform | Twitter API v2 |
| `TIKTOK_ACCESS_TOKEN` | per-Plattform | TikTok Open API (Stub) |
| `SECRET_KEY` | optional | Flask-Session — sonst auto-generiert via `secrets.token_hex(32)` (`dashboard/__init__.py:23`) |

**Im Code verwendete, aber im `.env.example` fehlende ENVs:**
- `FAL_KEY` — `video/image_gen.py:31`, `video/video_gen.py:34`
- `MUBERT_API_KEY` — `video/audio.py:33`
- `OPENAI_API_KEY` — `dashboard/services/ai_vision.py:122` (DALL-E)
- `STRIPE_*_PRICE_ID`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` — `dashboard/routes/billing.py`
- `SUPABASE_URL`, `SUPABASE_ANON_KEY` — `dashboard/services/supabase_sync.py:26-27`
- `LICENSE_SECRET` — `dashboard/services/plan_service.py:245`
- `ADMIN_SECRET` — `dashboard/routes/billing.py` Admin-Endpoint
- `BASE_URL` — `dashboard/routes/billing.py:42`

→ **Documentation-Drift:** Mind. 8 Code-relevante ENV-Vars sind im `.env.example` nicht dokumentiert. Risiko: lokale Setups laufen ohne, fühlen sich unauffällig an, schlagen aber stumm fehl (z.B. Video-Pipeline ohne FAL_KEY → einzelne StepResults success=false, aber kein lautes Boot-Fail).

## `README.md`

Inhalt (verifiziert via Read 2026-04-27): Stack, Quick-Start, ENV-Tabelle. Erwähnt:
- Stack: Python 3.11+, Flask, Claude API, APScheduler, Stripe (✅ stimmt mit Code überein außer „APScheduler"-Discrepanz)
- Quick-Start: `git clone`, venv, `pip install -r requirements.txt`, `cp .env.example .env`, `python main.py`
- **README empfiehlt `python main.py`** (Z.63) — startet aber nur den Scheduler, nicht das Dashboard. Real-World-Entry ist `python start_bot.py` (vgl. Banner-Output bei Boot)

## Verbundene Notes

- [[Socibot/modules/00-Overview]]
- [[Socibot/modules/02-Bot-Core]] — Scheduler-Architektur
- [[Socibot/modules/05-Dashboard-IA]] — first_run-Redirect-Logik im `before_request`-Hook
