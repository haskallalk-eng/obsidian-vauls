---
title: Socibot — Modul-Topologie
tags: [socibot, architektur, ist-stand]
date: 2026-04-27
source_of_truth: code
codebase: C:\Users\pc105\Desktop\Social media Bot
---

# Socibot — Modul-Topologie (Ist-Stand 2026-04-27)

> **Quelle:** Code unter `C:\Users\pc105\Desktop\Social media Bot\`. Jede Aussage hier muss in einem konkreten Datei-Pfad nachweisbar sein. Behauptungen ohne Beleg gehören nicht in dieses Vault.

## Stack (verifiziert)

- **Python:** 3.11+ (laut `README.md:38`); bei mir lokal Python 3.14.2 (`python --version` am 2026-04-27)
- **Web-Framework:** Flask (Blueprint-pro-Route), Jinja2-Templates
- **AI-Provider:** Anthropic Claude API (Pflicht), OpenAI (optional für Stable Diffusion / Vision je nach Service)
- **Persistenz:** Datei-basiert (`client/*.json`) + SQLite für Video-Jobs (`data/video_jobs.db`, schreibt im WAL-Modus)
- **Scheduler:** APScheduler (`requirements.txt`)
- **Plattformen:** Instagram, Facebook, LinkedIn, Twitter/X, TikTok — jeweils eigener Adapter unter `platforms/<name>/`
- **Hosting:** Lokales Flask `app.run` auf Port 5000 (Dashboard) + Port 5050 (Form-Server). Kein WSGI in Prod ersichtlich.

## Größe (Ist-Stand)

| Top-Level-Verzeichnis        | LOC       | Files   | Notiz |
|------------------------------|-----------|---------|-------|
| `dashboard/templates/`       | **7.563** | 19      | größter Bereich, Vanilla JS + Jinja2 |
| `dashboard/routes/`          | 2.618     | 18      | 1 Blueprint pro Route-File |
| `dashboard/services/`        | 2.173     | 11      | Service-Layer (Vision, Branding, Learning, Plans, …) |
| `bot/`                       | 1.714     | 8       | Scheduler, Poster, ContentCalendar, DM-Handler, Analytics, Config, Constants |
| `video/`                     | 1.210     | 11      | Video-Engine v4.0 Pipeline + Queue |
| `platforms/`                 | 1.036     | 16      | 5 Plattformen × `<api>` + `<content>` |
| `server/`                    | 710       | 1       | Form-Server (Port 5050) |
| `brand/`                     | 363       | 2       | Brand-Definition |
| `automation/`                | 163       | 1       | Sample-Content-Generator |
| **Summe (Code+Templates)**   | **~18.6k**| ~107    | ohne `__pycache__`, JSON-Daten, Reports |

Quelle der Zahlen: `find … | xargs wc -l` ausgeführt 2026-04-27 02:40.

## Entry-Points

- `start_bot.py` — voller Boot: Scheduler + Dashboard (Port 5000) + Form-Server (Port 5050) als Threads. Verifiziert: liest `bot.config`, prüft `claude.api_key`, ruft `Scheduler(config).run()`.
- `main.py` — Mini-Boot: nur Scheduler, kein Dashboard. Wird im README nicht erwähnt; wirkt wie der Original-Entry vor dem Dashboard.

## Dashboard-Informationsarchitektur (post-refactor 2026-04-27 02:35)

Sidebar laut `dashboard/templates/base.html:487-518`:

```
Hauptbereich:    Dashboard (/)              · Kalender (/calendar/)         · Postfach (/postfach/)
Erstellen:       Erstellen (/erstellen/)    · Mediathek (/media/)
Wachstum:        Analytics (/analytics/)
System:          Marke (/einstellungen/marke) · Billing (/billing/)
Footer:          "Neuen Kunden einrichten" → /fragebogen
```

Aus der Sidebar entfernt aber als Routen erreichbar:
- `/autopilot/` — bleibt registriert (`dashboard/__init__.py:140,157`), Stats jetzt im Calendar-Header eingeblendet
- `/einstellungen/setup` — first-run-only Redirect via `before_request` Handler (`dashboard/__init__.py:65-105`)
- `/composer/`, `/video/` — von der `/erstellen/`-Hub-Page verlinkt

## Geänderte / neue Files in dieser Session (2026-04-27)

| Datei | Aktion | Zweck |
|-------|--------|-------|
| `dashboard/templates/base.html` | edit (Sidebar 487-518) | IA-Refactor |
| `dashboard/routes/erstellen.py` | **neu** | Hub-Route |
| `dashboard/templates/erstellen.html` | **neu** | Hub-Page mit Cards |
| `dashboard/__init__.py` | edit (157-159) | erstellen-Blueprint registriert |
| `dashboard/routes/media.py` | edit (32-58) | Tabs Fotos/Ideen, lädt `automation/sample_content.json` |
| `dashboard/templates/media.html` | edit | Tab-Switcher + Ideen-Panel |
| `dashboard/routes/calendar.py` | rewrite | Monats-Grid, Autopilot-Stats eingebettet |
| `dashboard/templates/calendar.html` | full rewrite | Monats-Grid statt Wochen-Akkordeon |

Diese Änderungen sind im Vault-Hauptverzeichnis (Daily 2026-04-27) zu dokumentieren.

## Modul-Index (separate Notes)

- [[Socibot/modules/01-Entry-Points|01 Entry-Points]] — `main.py`, `start_bot.py`, `requirements.txt`, `.env.example`
- [[Socibot/modules/02-Bot-Core|02 Bot-Core]] — `bot/` — Scheduler, Poster, ContentCalendar, DM-Handler, Analytics, Config, Constants
- [[Socibot/modules/03-Platforms|03 Platforms]] — `platforms/` — IG, FB, LinkedIn, X, TikTok
- [[Socibot/modules/04-Video-Engine|04 Video-Engine]] — `video/` — Pipeline, Queue, Prompts, Image, Video, Audio, Postprocess, Brand-Mapping, Cleanup
- [[Socibot/modules/05-Dashboard-IA|05 Dashboard-IA]] — Sidebar, Routes-Map, before_request-Logik
- [[Socibot/modules/06-Dashboard-Routes|06 Dashboard-Routes]] — pro Blueprint
- [[Socibot/modules/07-Dashboard-Services|07 Dashboard-Services]] — `dashboard/services/`
- [[Socibot/modules/08-Dashboard-Templates|08 Dashboard-Templates]] — `dashboard/templates/`, base.html-Style-System, JS-Patterns
- [[Socibot/modules/09-Brand-System|09 Brand-System]] — `brand/`, `config/brand_style_map.json`, `client/brand_knowledge.json`
- [[Socibot/modules/10-Client-State|10 Client-State]] — `client/*.json`-Dateien
- [[Socibot/modules/11-Data-Storage|11 Data-Storage]] — SQLite + Video-Test-Outputs
- [[Socibot/modules/12-Server-Forms|12 Server & Public]] — `server/form_server.py`, `public/`
- [[Socibot/modules/13-Automation|13 Automation]] — Sample-Content-Generator
- [[Socibot/modules/14-Findings|14 Findings]] — code-belegte Risiken, Hardcodes, Silent-Catches, fehlende Tests

## Verbundene Notes

- [[Socibot/Overview]]
- [[Socibot/Kanban]]
- [[Daily/2026-04-27]] — Refactor-Session
