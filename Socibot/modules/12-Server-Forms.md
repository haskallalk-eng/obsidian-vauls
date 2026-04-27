---
title: 12 — Server & Public
tags: [socibot, modul, public, forms]
date: 2026-04-27
source_of_truth: code
---

# 12 — Server & Public-Site

## `server/form_server.py` (710 LOC)

**Zweck:** Eigener HTTP-Server (Port 5050) für externes Onboarding-Formular. Wird von `start_bot.py:26-35` als Daemon-Thread gestartet.

**Verzeichnisse (Z.24–46):**
- Submissions-Output: `client/submissions/`
- Brand-Ziel: `client/brand_knowledge.json`

**Public-API:**
- `GET /fragebogen` → HTML-Form (eigene HTML, kein Jinja-Bezug zu Dashboard)
- `POST /fragebogen/submit` → speichert JSON in `client/submissions/<TIMESTAMP>.json`
- Optional Email-Versand

**Helper:**
- `_split_field(val, max_items=8)` Z.50–56 — parst Komma/Semikolon/Newline-getrennte Felder
- `_map_submission_to_brand(data, filename)` Z.58–100 — konvertiert Form-Daten zu `brand_knowledge.json`-Schema (für `dashboard/routes/brand_settings.py:255-314` Submission-Import)

**Hardcoded:**
- LABELS-Dict Z.29–46 — deutsche Feldnamen (erwartete Form-Felder)

**Import-Workflow:**
1. Externe Form (z.B. eigene Website) POSTet zu `:5050/fragebogen/submit`
2. JSON gespeichert in `client/submissions/<TIMESTAMP>.json`
3. User klickt im Dashboard `/einstellungen/submission-importieren` → mappt → schreibt `brand_knowledge.json`

## `public/`

Statische HTML-Dateien außerhalb von Flask-Templates.

| Datei | Zweck | Verifiziert |
|---|---|---|
| `index.html` | Marketing-Landing | Existiert (Path) |
| `datenschutz.html` | DSGVO-Datenschutzerklärung | Existiert |
| `impressum.html` | Impressum | Existiert |
| `.vercel/project.json` | Vercel-Deploy-Config | Existiert |
| `.vercel/README.txt` | Vercel-Notes | Existiert |

**Flask-Wiring:** Keine Route in `dashboard/routes/` liefert `public/`-Files aus. Vermutung: `public/` ist der Vercel-Ziel-Ordner (vgl. `.vercel/`-Subdirectory) und wird separat deployt — nicht aus dem Flask-Server.

**Nicht verifiziert:** Wie `public/index.html` zur Domain kommt. Möglich: Vercel deploys `public/` als marketing-site und `start_bot.py` läuft auf separater VM.

## Verbundene Notes

- [[Socibot/modules/05-Dashboard-IA]] — `landing.py`-Route innerhalb Flask (anderes Konstrukt als `public/`)
- [[Socibot/modules/14-Findings]] — Public-vs-Dashboard-Trennung
