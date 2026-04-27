---
title: 08 — Dashboard-Templates
tags: [socibot, modul, frontend]
date: 2026-04-27
source_of_truth: code
---

# 08 — Dashboard-Templates (`dashboard/templates/`, 7.563 LOC, 19 Files)

> Catppuccin-Mocha-Design-System, Vanilla-JS, base.html als Single-Source-of-Truth für Layout + globale Helper.

## Files

| Datei | LOC | Extends | Standalone? |
|---|---|---|---|
| `base.html` | 754 | — | nein (Layout-Master) |
| `overview.html` | 318 | base.html | |
| `analytics.html` | 100 | base.html | |
| `calendar.html` | 800 (rewriten 04-27) | base.html | |
| `composer.html` | 407 | base.html | |
| `erstellen.html` | 174 (neu 04-27) | base.html | |
| `fragebogen.html` | 461 | — | ✅ Standalone (Onboarding) |
| `setup.html` | 460 | — | ✅ Standalone (Initial-Config) |
| `media.html` | 385 (rewriten 04-27) | base.html | |
| `video.html` | 254 | base.html | |
| `autopilot.html` | 176 | base.html | (legacy) |
| `postfach.html` | ~250 | base.html | |
| `landing.html` | ? | base.html | |
| `billing.html` | ? | base.html | |
| `marke.html` | ~200 | base.html | |
| `preview.html` | ? | base.html | (Public Client-View) |
| `lernen.html` | ? | base.html | |
| `verlauf.html` | ? | base.html | |
| `woche.html` | ? | base.html | (Approval-Wizard-Wochenansicht) |

## `base.html` (754 LOC) — Single-Source-of-Truth

### CSS-Variablen (Z.16–35)

Catppuccin Mocha — alle 16 Farben:

```css
--bg:        #11111b   /* Crust */
--sidebar:   #181825   /* Mantle */
--surface:   #1e1e2e   /* Base */
--surface2:  #313244   /* Surface 0 */
--surface3:  #45475a   /* Surface 1 */
--accent:    #cba6f7   /* Mauve (primary) */
--peach:     #fab387   /* Sekundär */
--text:      #cdd6f4
--muted:     #a6adc8
--subdued:   #6c7086
--green:     #a6e3a1
--yellow:    #f9e2af
--blue:      #89b4fa
--red:       #f38ba8
--teal:      #94e2d5
--sidebar-w: 230px
```

### Layout

- `body { display: flex; min-height: 100vh }` (Z.41–46)
- Sidebar `position: fixed; width: 230px; height: 100vh` (Z.49–59)
- Main `margin-left: var(--sidebar-w); flex: 1; padding: 28px 32px` (Z.190–196)
- Mobile: `<1100px` Hamburger-Toggle (Z.324–356), Sidebar `translateX(-100%)` mit `.open`-Klasse

### Komponenten-Patterns

- `.card` Z.201–211 — surface, border, padding, hover
- `.badge.green/red/blue/...` Z.225–234 (8 Varianten)
- `.btn-primary/secondary/ghost/danger`, `.btn-sm/lg/icon` Z.237–276
- `.grid-5/3/2` Z.220–223
- Toast-Container `#toast-container` Z.288 — bottom-right (80px, 24px), slide-in
- Modal-Confirm `#confirm-modal` Z.361–375 — backdrop blur(4px)
- Notif-Bell `#notif-bell` Z.534–549 — fixed bottom-right
- Notif-Drawer Z.551–564 — 320px width, max-height 340px

### Globale JS-Helper (Z.566–751)

| Funktion | Zeile | Zweck |
|---|---|---|
| `escHtml(str)` | 568–572 | XSS-Schutz via createTextNode |
| `toast(msg, type, duration, actionLabel, actionFn)` | 575–592 | success/error/info, optional Button |
| `apiPost(url, data)` | 595–607 | fetch POST + JSON |
| `apiDelete(url)` | 608–621 | DELETE + Error |
| `toggleNotifDrawer()` | 626–630 | UI-Toggle |
| `loadNotifList()` | 632–652 | GET /api/notifications, render |
| `openNotif(id, link)` | 654–659 | Mark read + navigate |
| `readAllNotifs()` | 661–665 | POST /api/notifications/read-all |
| `updateNotifBadge()` | 667–678 | Badge-Counter |
| `btnLoad(btn, text)` / `btnReset(btn)` | 694–699 | Spinner-State |
| `confirmAction(msg, title)` | 702–717 | Promise-basiertes Modal |
| `copyToClipboard(text, label)` | 720–731 | Mit Fallback (textarea) |
| `toggleSidebar()` | 734–737 | Hamburger Mobile |

### Auto-Polling

- `setInterval(updateNotifBadge, 60_000)` Z.681–682 — Notif-Badge alle 60s

## Routen-Template-Map

| Route | Template | Hinweis |
|---|---|---|
| `/` | overview.html | Dashboard-Start |
| `/calendar/` | calendar.html | Monats-Grid (rewriten) |
| `/postfach/` | postfach.html | DSGVO-Postfach |
| `/erstellen/` | erstellen.html | Hub (neu) |
| `/composer/` | composer.html | Editor |
| `/video/` | video.html | Video-Queue |
| `/media/` | media.html | Tabs Fotos/Ideen |
| `/analytics/` | analytics.html | Chart.js |
| `/einstellungen/marke` | marke.html | Brand-PDF + Tokens |
| `/einstellungen/setup` | setup.html | Setup-Wizard (Standalone) |
| `/fragebogen` | fragebogen.html | Onboarding (Standalone) |
| `/billing/` | billing.html | Plans + Stripe |
| `/autopilot/` | autopilot.html | Stats (legacy) |
| `/lernen/` | lernen.html | Learning-Profile |
| `/verlauf/` | verlauf.html | History |
| `/kunden-vorschau/` | preview.html | Public Client-Approval |
| `/landing` | landing.html | Public Landing |
| `/vorschau/` | woche.html (?) | Wochen-Approval |

## Highlight-Templates

### `calendar.html` (800 LOC, post-04-27)

- ~315 LOC inline CSS
- **Autopilot-Strip** Z.6–40: LED-Puls-Animation + Stat-Boxen
- **Monats-Grid** Z.83–150: `.day-cell` mit Status-Dots, today-Highlight, outside/past states
- **Day-Detail-Pane** Z.152–229: Single-Instance unter dem Grid (anders als alte Per-Week-Akkordeons)
- **Approval-Panel** Z.281–292 — eingebettet im Detail-Pane
- ~265 LOC JS — `selectDay`, `selectPost`, Approval-Actions, Add-Modal, Multi-Week-Modal, Schedule-Editor

JS-Endpoints angerufen:
- POST `/vorschau/freigeben/<id>`, `/vorschau/ablehnen/<id>`, `/vorschau/varianten/<id>`
- POST `/calendar/trigger/<id>`, `/calendar/delete/<id>`, `/calendar/add`, `/calendar/mehrwochen-generieren`, `/calendar/zeitplan-speichern`

### `composer.html` (407 LOC)

- Platform-Pills + Plattform-Previews (jeweils CSS-modelliert wie das echte Netzwerk)
- Char-Bar mit Plattform-Limits
- Hashtag-Chips
- Schedule-Modus (Now / Later)
- localStorage-Draft-Save Z.360–394 (`composer_draft_v1`)

JS-Endpoints:
- POST `/composer/generate` (Claude-Content-Gen)
- POST `/composer/post` (Sofort-Posten)
- GET `/composer/post-status/<jobId>` (Polling)
- POST `/calendar/add` (Schedule)
- GET `/vorschau/modus` (Co-Pilot vs Manual)

### `erstellen.html` (174 LOC, neu)

Hub-Page. 2 Cards (Post + Video). `recent_videos`-Liste mit Status-Badges aus `data/video_jobs.db`.

### `media.html` (385 LOC, post-04-27)

- Drag-and-Drop-Upload-Zone
- Tabs Fotos / Ideen (`role="tablist"`, `role="tab"`)
- Tab-Switcher in JS Z.269–280: Display toggle + URL-Querystring update via `history.replaceState`
- Upload via FormData zu `/media/upload`
- Vision-Analyse via POST `/media/analyze/<id>` + Polling `/media/status/<id>`

### `fragebogen.html` (461 LOC, Standalone)

Eigenes HTML-DOCTYPE, kein extends base.html. Catppuccin-Palette inline. 4-Step-Wizard:
1. Brand-Info
2. Tonalität & Stil
3. Plattformen
4. Done

POST `/fragebogen/submit` Z.439.

### `setup.html` (460 LOC, Standalone)

Eigenes HTML-DOCTYPE. 5 Steps:
1. Claude API-Key (mit Test-Button)
2. Plattformen wählen
3. Plattform-Tokens eingeben
4. Email-Notifikationen (optional)
5. Done

`PLATFORM_CONFIGS` Z.250–293 — pro Plattform Hint + Field-Layout.
POST `/einstellungen/token-speichern`, `/einstellungen/token-testen`.

## State-Locations

**Server-Side State:**
- `client/content_calendar.json`, `bot_settings.json`, `brand_knowledge.json`, `learning_profile.json`, `conversations.json`, `notifications.json`, `replied_comments.json`
- `data/video_jobs.db`

**Client-Side State (localStorage):**
- `composer_draft_v1` — Draft-Auto-Save

**UI-Only State (CSS-Klassen / JS-Variablen):**
- Sidebar `.open` (Mobile)
- Tab `.active`, Day `.selected`, Modal `.open`
- `_selectedIso`, `_selPost` (calendar.html JS-Closure-State)

## Frontend ↔ Backend Endpoints (gesamtes Inventar)

Nach Templates gegrept:

| Endpoint | Methode | Aufgerufen aus |
|---|---|---|
| `/api/log` | GET | overview.html (Polling 30s) |
| `/api/notifications` | GET | base.html (Polling 60s) |
| `/api/notifications/<id>/read` | POST | base.html |
| `/api/notifications/read-all` | POST | base.html |
| `/composer/generate` | POST | composer.html |
| `/composer/post` | POST | composer.html |
| `/composer/post-status/<jobId>` | GET | composer.html (Polling) |
| `/calendar/add` | POST | calendar.html, composer.html |
| `/calendar/trigger/<id>` | POST | calendar.html |
| `/calendar/delete/<id>` | POST | calendar.html |
| `/calendar/mehrwochen-generieren` | POST | calendar.html |
| `/calendar/zeitplan-speichern` | POST | calendar.html |
| `/vorschau/freigeben/<id>` | POST | calendar.html |
| `/vorschau/ablehnen/<id>` | POST | calendar.html |
| `/vorschau/varianten/<id>` | POST | calendar.html |
| `/vorschau/modus` | GET | composer.html |
| `/media/upload` | POST | media.html |
| `/media/analyze/<id>` | POST | media.html |
| `/media/status/<id>` | GET | media.html (Polling) |
| `/video/create` | POST | video.html |
| `/video/queue` | GET | video.html (Polling 15s) |
| `/fragebogen/submit` | POST | fragebogen.html |
| `/einstellungen/token-speichern` | POST | setup.html |
| `/einstellungen/token-testen` | POST | setup.html |
| `/einstellungen/submission-importieren` | POST | overview.html |

## Verbundene Notes

- [[Socibot/modules/05-Dashboard-IA]]
- [[Socibot/modules/06-Dashboard-Routes]]
- [[Socibot/modules/15-Layer-Frontend]] — Layer-Sicht auf Frontend
- [[Socibot/modules/18-Routes-Map]]
