---
title: Phonbot — Alle Seiten (Inventory)
type: index
tags: [phonbot, pages, inventory]
created: 2026-04-22
status: live on phonbot.de
---

# Phonbot — Page Inventory

> Vollständige Übersicht aller auslieferbaren Seiten. Drei Ebenen: **Static HTML** (public/*/index.html, SEO-first), **SPA Public Routes** (React, öffentlich erreichbar) und **SPA Authed Routes** (hinter JWT-Login).

## Übersicht

| # | URL | Typ | Auth | Datei | Nav |
|---|---|---|---|---|---|
| 1 | `/` | React SPA — Landing | public | [index.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/landing/index.tsx) | ✅ NavHeader |
| 2 | `/?page=contact` | React SPA — Kontakt | public | [ContactPage.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/landing/ContactPage.tsx) | ✅ NavHeader |
| 3 | `/?page=login` | React SPA — Login/Register | public | [LoginPage.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/LoginPage.tsx) | ❌ Minimal |
| 4 | `/?page=register` | React SPA — Register | public | [LoginPage.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/LoginPage.tsx) (tab switch) | ❌ Minimal |
| 5 | `/?reset=<token>` | React SPA — Reset Password | token-gated | [ResetPasswordPage.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/ResetPasswordPage.tsx) | ❌ Minimal |
| 6 | `/#home` | React SPA — Dashboard | authed | [DashboardHome.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/DashboardHome.tsx) | ❌ Sidebar |
| 7 | `/#agent` | React SPA — Agent Builder | authed | [agent-builder/](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/agent-builder/) | ❌ Sidebar |
| 8 | `/#test` | React SPA — Test Console | authed | [TestConsole.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/TestConsole.tsx) | ❌ Sidebar |
| 9 | `/#tickets` | React SPA — Ticket Inbox | authed | [TicketInbox.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/TicketInbox.tsx) | ❌ Sidebar |
| 10 | `/#logs` | React SPA — Call Log | authed | [CallLog.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/CallLog.tsx) | ❌ Sidebar |
| 11 | `/#billing` | React SPA — Billing | authed | [BillingPage.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/BillingPage.tsx) | ❌ Sidebar |
| 12 | `/#phone` | React SPA — Phone Manager | authed | [PhoneManager.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/PhoneManager.tsx) | ❌ Sidebar |
| 13 | `/#calendar` | React SPA — Calendar | authed | [CalendarPage.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/CalendarPage.tsx) | ❌ Sidebar |
| 14 | `/#insights` | React SPA — Insights | authed | [InsightsPage.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/InsightsPage.tsx) | ❌ Sidebar |
| 15 | `/onboarding` (auto) | React SPA — Onboarding Wizard | first-login | [OnboardingWizard.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/onboarding/OnboardingWizard.tsx) | ❌ Minimal |
| 16 | `/admin` (hash) | React SPA — Admin Panel | admin JWT | [AdminPage.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/AdminPage.tsx) | ❌ Sidebar |
| — | — | — | — | — | — |
| 17 | `/friseur/` | Static HTML | public | [public/friseur/index.html](../../.openclaw/workspace/voice-agent-saas/apps/web/public/friseur/index.html) | ✅ Unified |
| 18 | `/handwerker/` | Static HTML | public | [public/handwerker/index.html](../../.openclaw/workspace/voice-agent-saas/apps/web/public/handwerker/index.html) | ✅ Unified |
| 19 | `/arztpraxis/` | Static HTML | public | [public/arztpraxis/index.html](../../.openclaw/workspace/voice-agent-saas/apps/web/public/arztpraxis/index.html) | ✅ Unified |
| 20 | `/reinigung/` | Static HTML | public | [public/reinigung/index.html](../../.openclaw/workspace/voice-agent-saas/apps/web/public/reinigung/index.html) | ✅ Unified |
| 21 | `/restaurant/` | Static HTML | public | [public/restaurant/index.html](../../.openclaw/workspace/voice-agent-saas/apps/web/public/restaurant/index.html) | ✅ Unified |
| 22 | `/autowerkstatt/` | Static HTML | public | [public/autowerkstatt/index.html](../../.openclaw/workspace/voice-agent-saas/apps/web/public/autowerkstatt/index.html) | ✅ Unified |
| 23 | `/impressum/` | Static HTML | public | [public/impressum/index.html](../../.openclaw/workspace/voice-agent-saas/apps/web/public/impressum/index.html) | ✅ Unified |
| 24 | `/datenschutz/` | Static HTML | public | [public/datenschutz/index.html](../../.openclaw/workspace/voice-agent-saas/apps/web/public/datenschutz/index.html) | ✅ Unified |
| 25 | `/agb/` | Static HTML | public | [public/agb/index.html](../../.openclaw/workspace/voice-agent-saas/apps/web/public/agb/index.html) | ✅ Unified |

## Nav-Arten — wann welche

### NavHeader (React, `apps/web/src/ui/landing/NavHeader.tsx`)
Voller Landing-Header mit Demo/Features/Preise/FAQ/Branchen-Dropdown/Kontakt + Login/CTA + Mobile-Drawer. Sticky.
- Benutzt auf: `/`, `/?page=contact`.
- Nutzt `PhonbotBrand` (FoxLogo + Phon-white + bot-orange→cyan).

### Unified Static Nav (`scripts/_nav.mjs` → `NAV_STYLE + NAV_HTML`)
1:1-HTML-Port der NavHeader — gleiche Items, Icons, Colors, Sticky-Verhalten, Mobile-Drawer.
Interaction-JS ist in [public/nav.js](../../.openclaw/workspace/voice-agent-saas/apps/web/public/nav.js) (hamburger + dropdown).
- Benutzt auf: alle 6 Branchen + 3 Legal Pages (insg. 9 statische Seiten).
- Auto-generiert via `node scripts/gen-landing-pages.mjs` (Branchen) + `node scripts/sync-legal-nav.mjs` (Legal, Marker-basiert).

### Sidebar (React, `apps/web/src/ui/Sidebar.tsx`)
Links-Sidebar für authed App. Zeigt `PhonbotBrand` (sm) + Nav-Items + Logout. Nicht Sticky (permanent sichtbar).
- Benutzt auf: alle 10 authed Routes (home/agent/test/tickets/logs/billing/phone/calendar/insights/admin).

### Minimal (kein Header)
LoginPage / ResetPasswordPage / OnboardingWizard haben nur einen zentrierten Card-Layout ohne Nav — by design (Focus auf den Flow).

## Invarianten (damit Claude das nicht wieder vergisst)

- **Alle 2 öffentlichen Nav-Bars müssen visuell identisch sein** (Landing NavHeader.tsx ↔ static `_nav.mjs`). Bei Änderung an einer Seite muss die andere nachgezogen werden.
- **Alle statischen Seiten teilen eine Nav-Quelle** (`scripts/_nav.mjs`) — manuelle Duplikate vermeiden.
- Nav ist **überall sticky** (`sticky top-0 z-50` / `position:sticky;top:0;z-index:50`).
- `PhonbotBrand` ist **die einzige Source für den Wortmarken-Look** — keine inline Duplikate (vgl. 2026-04-22 Drift-Fix in LoginPage.tsx:89 + ResetPasswordPage.tsx:39).
- **Kein Breadcrumb** auf Static-Pages (entfernt 2026-04-22, weil redundant zum Branchen-Dropdown). JSON-LD BreadcrumbList bleibt für SEO.

## Deploy

Static-HTML-Änderungen landen über den **web**-Container:
```
ssh root@87.106.111.213
cd /opt/phonbot
git pull origin master
docker compose build web && docker compose up -d web
```
Kein full-rebuild nötig — web ist separater Dockerfile, Rebuild-Zeit ~1-2 min.

Bei Änderungen in `apps/api/`: `docker compose build api && docker compose up -d api`.
Full deploy (beide + cache-free): `bash scripts/deploy.sh`.

## Links

- Nav-Source: [scripts/_nav.mjs](../../.openclaw/workspace/voice-agent-saas/scripts/_nav.mjs)
- Branchen-Generator: [scripts/gen-landing-pages.mjs](../../.openclaw/workspace/voice-agent-saas/scripts/gen-landing-pages.mjs)
- Legal-Sync: [scripts/sync-legal-nav.mjs](../../.openclaw/workspace/voice-agent-saas/scripts/sync-legal-nav.mjs)
- Branchen-Daten: [shared.ts TEMPLATES](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/landing/shared.ts)
- Wordmark: [FoxLogo.tsx PhonbotBrand](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/FoxLogo.tsx)
- Gesamtsystem: [[Phonbot-Gesamtsystem]]
- Overview: [[Overview]]
