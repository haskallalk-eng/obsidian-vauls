---
title: 15 — Layer Frontend
tags: [socibot, layer, frontend]
date: 2026-04-27
source_of_truth: code
---

# 15 — Layer: Frontend

> Alles, was im Browser läuft. Templates + JS + CSS + Browser-State.

## Bestandteile

- **19 Jinja2-Templates** (`dashboard/templates/`, 7.563 LOC)
- **2 Standalone-HTMLs** (`fragebogen.html`, `setup.html` — kein extends)
- **Public-Statics** (`public/index.html`, `datenschutz.html`, `impressum.html`)
- **Inline-CSS** überall, **kein eigenes CSS-File**
- **Inline-JS** überall, **kein eigenes JS-File**
- **External CDN:** Lucide-Icons + Chart.js (analytics.html)

## Design-System (verifiziert in `base.html:16-35`)

**Catppuccin Mocha** — komplette 16-Farben-Palette als CSS-Vars. Keine Tailwind, kein Build-Step. Direkter Stylesheet-Pfad pro Page über `<style>`-Block.

## Globale JS-Helper (`base.html:566-751`)

| Helper | Zweck |
|---|---|
| `escHtml(str)` | XSS-Schutz |
| `toast(msg, type, duration, actionLabel, actionFn)` | Notification-Pattern |
| `apiPost(url, data)`, `apiDelete(url)` | fetch-Wrapper |
| `confirmAction(msg, title)` | Promise-Modal |
| `copyToClipboard(text, label)` | Clipboard mit Fallback |
| `btnLoad(btn, text)`, `btnReset(btn)` | Spinner-State |
| `toggleSidebar()` | Mobile Hamburger |
| `loadNotifList()`, `updateNotifBadge()` | Notif-Drawer |

## State im Frontend

**Persistent (localStorage):**
- `composer_draft_v1` — `composer.html:360-394` Auto-Save

**Ephemer (JS-Closure):**
- `_selectedIso`, `_selPost` (`calendar.html`)
- `_editTimes` (Schedule-Editor in calendar.html)
- `_post_jobs` Tracker im Composer-Backend (Z.12-13 in `composer.py`)

**URL-State:**
- `?tab=fotos|ideen` (`media.html`) via `history.replaceState`
- `?year=YYYY&month=MM` (`calendar.html`) via Link-Navigation
- `?p=instagram|...` (`calendar.html` Plattform-Filter)

## Auto-Polling (alles Frontend-getrieben)

| Endpoint | Intervall | Wo gefeuert |
|---|---|---|
| `/api/notifications` | 60s | base.html (Bell-Counter) |
| `/api/log` | 30s | overview.html (Log-Tail) |
| `/video/queue` | 15s | video.html (Queue-Status) |
| `/composer/post-status/<id>` | bedarfsweise | composer.html (nach Submit) |
| `/media/status/<id>` | bedarfsweise | media.html (nach Analyse-Start) |
| `/vorschau/varianten-status/<id>` | bedarfsweise | (calendar.html, ggf. woche.html) |

## Form-Wizards (Standalone)

### `fragebogen.html` (461 LOC)

Onboarding 4-Step. Eigenes DOCTYPE (kein extends base). Validierung in JS: `pulse()`, `showInlineError()`. Submit: POST `/fragebogen/submit`.

### `setup.html` (460 LOC)

Initial Token-Wizard 5-Step. Pro Plattform spezifische Field-Konfigs in `PLATFORM_CONFIGS` (Z.250–293). Test-Buttons rufen POST `/einstellungen/token-testen` für Live-Validierung.

## Komponenten-Inventar (verifiziert)

### Komponenten in `base.html`

- Sidebar mit SVG-Logo (Socibot-Katze, Z.446-474)
- Brand-Tag in Sidebar (Z.482-485)
- Sidebar-Section-Header (Z.113-120)
- Toast-Container (Z.288-310)
- Confirm-Modal (Z.361-375)
- Notif-Bell + Drawer (Z.534-564)
- Hamburger (Z.344-356, mobile)

### Komponenten in `calendar.html` (post-04-27)

- Autopilot-Strip mit LED-Puls
- Plat-Tabs
- Schedule-Editor-Panel (collapsible)
- Month-Navigation (‹ Monat YYYY ›)
- Month-Grid (7 Spalten × 5–6 Zeilen)
- Day-Detail-Pane (single instance)
- Approval-Panel
- Status-Legende
- Archive-Sektion (collapsible 12 Monate)
- Add-Modal, MultiWeek-Modal

### Komponenten in `composer.html`

- Platform-Pills mit Plattform-Farben
- Compose-Area mit Char-Bar
- Plattform-Previews (visuelles Mock pro Netzwerk)
- Hashtag-Chips
- Schedule-Modus-Switch (Now/Later)

### Komponenten in `media.html` (post-04-27)

- Upload-Zone (Drag-and-Drop)
- Media-Tabs (Fotos/Ideen mit `role="tab"`)
- Media-Grid mit AI-Analysis-Panels
- Idea-Cards (collapsible content)

### Komponenten in `video.html`

- Queue-Banner (aktive Jobs, scrollbar)
- Video-Grid (9:16 Aspect-Ratio Cards)
- Create-Overlay (Topic + Platform-Select)

## Frontend → Backend HTTP-Endpoints

Vollständige Liste siehe `08-Dashboard-Templates` § „Frontend ↔ Backend Endpoints" und `18-Routes-Map`.

## A11y / Mobile (verifiziert)

- `:focus-visible` mit Outline 2px solid accent (`base.html:395-400`)
- `role="grid"` auf Calendar-Grid
- `role="tablist"`, `role="tab"` auf Media-Tabs
- Mobile-Breakpoints: 1100px, 900px, 600px (`base.html:324-341`)
- Hamburger ab <600px

**Lücken:**
- Kein `aria-current` auf aktiver Sidebar-Nav
- Kein `aria-live` für Toast-Container
- `<button>`-Elemente teils mit `onclick`-Inline-Handler statt `addEventListener`

## Browser-Support

- ES2017+ (async/await, optional chaining)
- `URL`-API
- `history.replaceState`
- localStorage
- Promise

→ Modern-only. Kein IE-Fallback.

## Verbundene Notes

- [[Socibot/modules/05-Dashboard-IA]]
- [[Socibot/modules/08-Dashboard-Templates]]
- [[Socibot/modules/16-Layer-Backend]]
