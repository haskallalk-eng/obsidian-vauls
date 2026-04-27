---
title: 20 — Master-Summary
tags: [socibot, summary, master]
date: 2026-04-27
source_of_truth: code
---

# 20 — Master-Summary (Ist-Stand 2026-04-27)

> **Eine Datei, die alles zusammenfasst.** Wer den Socibot-Code beurteilen will, ohne 19 Detail-Notes zu lesen, liest diese.

## TL;DR

Socibot ist ein **Single-Process Python-Flask Self-Host Social-Media-AI-SaaS** mit ~18.6k LOC, der Posts für 5 Plattformen (IG/FB/LinkedIn/X/TikTok) automatisiert generiert, plant, freigibt, postet und Engagement (DMs/Comments) per Claude beantwortet. Zusätzlich gibt es eine **Video-Engine v4.0** mit fal.ai+Mubert+FFmpeg-Pipeline und SQLite-Job-Queue.

**State der Codebase** (verifiziert):
- 4 Plattformen produktiv, **TikTok ist Stub** (Upload nicht implementiert).
- **Keine Auth** im Dashboard außer Onboarding-Skip-Liste.
- **Race Conditions** auf zentralen JSON-Files (kein atomic-Write außer in `bot/content_calendar.py`).
- **Brand-Hardcoding** auf „Förderkraft" in 4 Code-Stellen trotz `brand_knowledge.json`-Override.
- **Documentation-Drift**: 8+ ENV-Vars im Code, nicht im `.env.example`.
- **Veraltetes Claude-Modell** `claude-sonnet-4-6` (vermutlich Typo).

Letzter Refactor (2026-04-27): IA-Restructure — Sidebar-Reduction, neuer `/erstellen/`-Hub, Mediathek-Tabs (Fotos/Ideen), Calendar als Monats-Grid mit eingefoldetem Autopilot.

## Stack

| Schicht | Tech |
|---|---|
| Sprache | Python 3.11+ (lokal 3.14.2) |
| Web | Flask 3.x + Jinja2 (Server-Side-Rendered + Vanilla-JS) |
| AI | Anthropic Claude (~25 Calls), OpenAI DALL-E (Vision), fal.ai (Flux 2 Pro + Kling 3.0), Mubert |
| Scheduler | `schedule`-Lib (kein APScheduler trotz README) |
| Persistence | JSON-Files in `client/`, SQLite WAL für Video-Queue |
| Payment | Stripe (Checkout + Webhook + License-Keys) |
| Frontend | Catppuccin-Mocha-Theme, Vanilla-JS, kein Build-Step |
| Hosting | `python start_bot.py` (lokales `app.run`, nicht WSGI) |
| Mailing | Gmail SMTP_SSL Port 465 |
| External Sync | Supabase REST (Customer-Submissions) |

## Größe

| Bereich | LOC | Files |
|---|---|---|
| `dashboard/templates/` | 7.563 | 19 |
| `dashboard/routes/` | 2.618 | 18 |
| `dashboard/services/` | 2.173 | 11 |
| `bot/` | 1.714 | 8 |
| `video/` | 1.210 | 11 |
| `platforms/` | 1.036 | 16 |
| `server/` | 710 | 1 |
| `brand/` | 363 | 2 |
| `automation/` | 163 | 1 |
| **Total** | **~18.6k** | ~107 |

## Architektur

```
┌─────────────────────────────────────────────────────────────────┐
│                  python start_bot.py                            │
│                                                                  │
│  Main-Thread             Daemon-Thread          Daemon-Thread   │
│  ────────────────        ────────────────       ────────────── │
│  bot.scheduler.run()     Flask Dashboard         Form-Server    │
│  blocking:30s            :5000                   :5050          │
│  schedule.run_pending()  18 Blueprints          /fragebogen     │
│  ↓                       ~85 Routes              /submit        │
│  Posting / Engagement /                                         │
│  Reports / Cleanup /                                            │
│  Video-Queue / Sync                                             │
└─────────────────────────────────────────────────────────────────┘

Persistence:
  client/*.json (12 zentrale Files + Sub-Dirs)
  data/video_jobs.db (SQLite WAL)
  .env (mutiert vom Setup-Wizard)
  bot.log
```

## Sidebar-IA (Ist-Stand 2026-04-27, post-refactor)

```
Hauptbereich: Dashboard · Kalender · Postfach
Erstellen:    Erstellen (Hub) · Mediathek (Fotos/Ideen-Tabs)
Wachstum:     Analytics
System:       Marke · Billing
Footer:       "Neuen Kunden einrichten →" /fragebogen
```

Aus der Sidebar entfernt aber erreichbar: `/autopilot/`, `/einstellungen/setup`, `/composer/`, `/video/`, `/landing`, `/kunden-vorschau/`, `/lernen/`, `/vorschau/`.

## Daten-Flüsse (Mini-Cheat-Sheet)

| Use-Case | Komponenten-Kette |
|---|---|
| Post automatisch erstellt | Scheduler → ContentCalendar → variant_service → Claude → Variants in `content_calendar.json` |
| Post freigeben | UI → /vorschau/freigeben → ContentCalendar.update_post → learning_service.record_approval |
| Post posten | Scheduler `at(t)` → Poster → platforms/<x>_api → Plattform-API → Status-Update in Calendar |
| DM beantworten | Scheduler/15min → platforms/<x>_api.get_comments → DMHandler.handle → Claude (Intent+Response) → conversations.json → reply_to_comment |
| Video erstellen | UI → /video/create → VideoQueue.submit → ThreadPool → pipeline.run_pipeline → fal.ai+Mubert+FFmpeg → media/output/<job>.mp4 |
| Brand bestätigen via PDF | UI → /einstellungen/marke/pdf-upload → brand_extractor → Claude Vision → brand_knowledge.json |
| Customer Onboarding extern | Form-Server :5050 → submissions/*.json → User klickt /einstellungen/submission-importieren → brand_knowledge.json + bot_settings.json |
| Stripe Subscription | UI → /billing/checkout → Stripe → /billing/webhook → plan_service.activate_plan → bot_settings.json |
| Trends recherchieren | UI → /api/research-trends → research_agent (Claude Agent SDK + WebSearch+WebFetch) → research_suggestions.json |

## Externe Abhängigkeiten

| Service | Zweck | Pflicht |
|---|---|---|
| Anthropic Claude | Content-Gen, Intent, Vision, Tool-Use | ✅ |
| Instagram Graph v18.0 | IG Posts + Engagement | (per Plattform) |
| Facebook Graph v18.0 | FB Posts + Engagement | (per Plattform) |
| LinkedIn v2 | LinkedIn Posts | (per Plattform) |
| Twitter API v2 | Tweets + DMs | (per Plattform) |
| TikTok Open API v2 | Video-Upload | ❌ Stub |
| OpenAI DALL-E | Bilder wenn Brand-Fit niedrig | optional |
| fal.ai (Flux 2 Pro, Kling 3.0) | Video-Engine | für Video-Feature |
| Mubert | Musik im Video | optional, non-fatal |
| FFmpeg lokal | Video-Postprocess | für Video-Feature |
| Stripe | Subscription | für Paid-Plans |
| Supabase | Customer-Onboarding | optional |
| Gmail SMTP | Eskalations-Email | optional |

## Größte Stärken (code-belegt)

- ✅ **Lern-Engine ist real:** 614 LOC `learning_service.py` mit 4 Signal-Quellen (Approval/Rejection/Rating/Performance) + Meta-Analyse via Claude (4-Stil-Regeln-Destillation)
- ✅ **Variant-A/B/C-Pattern** mit Brand-fit-Scoring
- ✅ **Plan-Gates** mit 4 Tiers, Feature-Flags, License-Key-HMAC, Stripe-Integration
- ✅ **Video-Engine** ist ambitioniert: parallele AI-Stages, EU AI Act Art. 50(2) Compliance-Metadata, Workspace-TTL-Cleanup, Crash-Recovery via processing→queued
- ✅ **DSGVO-Postfach:** Art. 17 + Art. 20 Endpoints implementiert
- ✅ **Catppuccin-Theme konsistent** über alle Templates
- ✅ **XSS-Schutz** via globalen `escHtml`-Helper
- ✅ **Onboarding-Wizard** Standalone mit Live-Token-Test
- ✅ **Co-Pilot vs. Autopilot-Mode** mit `auto_approve_threshold`

## Größte Schwächen (alle code-belegt, vgl. 14-Findings)

- 🔴 **Keine Auth** — Single-User-Self-Host-Annahme
- 🔴 **Race Conditions** auf JSON-State (nur 1 atomic-Write-Stelle)
- 🔴 **TikTok ist Stub aber im Schedule** → Posts schlagen periodisch fehl
- 🔴 **Brand-Hardcoding `förderkraft|drk|rotes kreuz` in variant_service**
- 🟠 **Documentation-Drift** ENV-Vars
- 🟠 **Veraltetes Claude-Modell** (`claude-sonnet-4-6` Typo?)
- 🟠 **In-Memory-State** für Background-Jobs (nicht restart-safe)
- 🟠 **Eskalierte DM-Threads** bekommen weiter Replies
- 🟡 **Silent-Catches** überall
- 🟡 **`cost_ledger`-Schema unbenutzt**
- 🟡 **Keine SQLite-Indexes**
- 🟡 **Mediathek-Ideen-Tab zeigt fremde DRK-Posts** für andere Kunden

## Aktive Refactor-Drift

Die 13 uncommitted Files (Stand 2026-04-27) zeigen aktive Polierung der UI-Schicht: 4 Dashboard-Routes (overview, autopilot, postfach, video), 5 Templates, `bot/dm_handler.py`, Video `postprocess.py`+`queue.py`, `public/index.html`. Wirkt nach „UI-Politur + Video-Queue-Tweak"-Sprint.

## Modul-Index

- [[Socibot/modules/00-Overview]]
- [[Socibot/modules/01-Entry-Points]]
- [[Socibot/modules/02-Bot-Core]]
- [[Socibot/modules/03-Platforms]]
- [[Socibot/modules/04-Video-Engine]]
- [[Socibot/modules/05-Dashboard-IA]]
- [[Socibot/modules/06-Dashboard-Routes]]
- [[Socibot/modules/07-Dashboard-Services]]
- [[Socibot/modules/08-Dashboard-Templates]]
- [[Socibot/modules/09-Brand-System]]
- [[Socibot/modules/10-Client-State]]
- [[Socibot/modules/11-Data-Storage]]
- [[Socibot/modules/12-Server-Forms]]
- [[Socibot/modules/13-Automation]]
- [[Socibot/modules/14-Findings]]
- [[Socibot/modules/15-Layer-Frontend]]
- [[Socibot/modules/16-Layer-Backend]]
- [[Socibot/modules/17-Layer-Database]]
- [[Socibot/modules/18-Routes-Map]]
- [[Socibot/modules/19-Connections]]

## Verbundene Vault-Notes

- [[Socibot/Overview]] — Hochlevel-Status
- [[Socibot/Kanban|Kanban]] — UTM-Funnel-Tracking offen
- [[Daily/2026-04-27]] — Refactor-Session
