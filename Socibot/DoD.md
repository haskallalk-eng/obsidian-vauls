---
title: Socibot — Definition of Done
type: dod
status: active
parent: "[[Socibot/Overview]]"
created: 2026-04-29
updated: 2026-04-29
related:
  - "[[Socibot/kanban/02-meta-oauth-phase-1-1]]"
  - "[[Socibot/Phase-1-1-Smoke-Test]]"
  - "[[Mindrails/Overview]]"
---

# Socibot — Definition of Done

> Lebende Master-Checkliste. Vier Ebenen: Code → Quality → Customer → Launch.
> Wenn ein Punkt unklar wird, hier eintragen statt im Kopf behalten.

## Lesart

| Ebene | Frage | Wer wendet an |
|---|---|---|
| **Code-DoD** | Darf dieser Commit gepusht werden? | Claude/Operator pro Commit |
| **Quality-DoD** | Darf dieses Feature in `master`? | Pro Feature-Branch / Phase |
| **Customer-DoD** | Darf ein zahlender Kunde es nutzen? | Pre-Beta / Pre-Pricing |
| **Launch-DoD** | Darf der Bot gegen echte Meta-Live-Accounts laufen? | Pre-Launch (App-Review) |

---

## 1 — Code-DoD (per Commit)

- [ ] `python -m py_compile` auf jeder geänderten `.py` clean
- [ ] Keine Plaintext-Secrets im Code/Repo (`grep -r "EAA\|sk-ant\|sk_live"` clean)
- [ ] `requirements.txt` aktualisiert wenn neue Imports
- [ ] Logs via `logging` (nicht `print`), keine User-Tokens im Log-Output
- [ ] Aussagekräftige Commit-Message (Imperativ, "what" + "why" wenn nicht trivial)
- [ ] `client/connections.json`, `.env`, `data/*.db*` in `.gitignore`
- [ ] Keine 100-Zeilen-Lambdas, keine kommentar-erklärten Hacks ohne Issue-Link

## 2 — Quality-DoD (per Feature)

- [ ] Acceptance-Criteria aus Kanban-Card erfüllt (jede Checkbox)
- [ ] Code-Review durchgelaufen (Self-Review oder Subagent)
- [ ] **security-dsgvo-reviewer**-Agent gelaufen wenn user-facing oder personenbezogene Daten
- [ ] Manueller End-to-End-Smoke-Test (Composer → Post → Result), ODER dokumentiert warum nicht
- [ ] Doku in Obsidian: Module-Note (`Socibot/modules/...`) ODER Kanban-Card aktualisiert
- [ ] Daily-Note + Produkt-Narrative-Eintrag (Wikilink-Verlinkung)
- [ ] Commit gepusht (kein lokaler "fertig"-Stand mit 60+ uncommitted Files)
- [ ] requirements.txt installierbar in frischer venv (`pip install -r requirements.txt`)

## 3 — Customer-DoD (pre-Pricing-Launch)

Was ein zahlender Kunde **ohne Operator-Eingriff** können muss:

### 3.1 Account & Onboarding
- [x] Account erstellen (Register / Login) — *Code da, uncommitted*
- [ ] Onboarding-Wizard: Brand-Settings + erste Page-Verbindung in <10min
- [x] DSGVO Account-Delete (Art. 17) — *Phase 1.1 ✓*
- [ ] Datenschutzerklärung + Impressum erreichbar — *uncommitted: `public/datenschutz.html`, `public/impressum.html`*

### 3.2 Plattform-Anbindung (ohne API-Key-Eingabe)
- [x] Instagram + Facebook via OAuth-Klick — *Phase 1.1 ✓*
- [ ] LinkedIn via OAuth-Klick — *aktuell: Token-Eingabe-Form*
- [ ] Twitter/X via OAuth-Klick — *aktuell: Token-Eingabe-Form*
- [ ] TikTok-Posting funktional — *aktuell: Stub in `_post_tiktok()`*

### 3.3 Content-Generierung
- [x] AI generiert Posts aus Brand-Knowledge (Claude)
- [x] Variant-System (mehrere AI-Vorschläge pro Post)
- [x] Inline-Approval (✓/✗ direkt im Calendar)
- [x] Brand-PDF-Upload + Vision-Analyse
- [ ] Video-Engine v4.0 verifizierter End-to-End-Run (Claude → Flux 2 → Kling 3 → FFmpeg → Upload)
- [ ] MUBERT_API_KEY gesetzt (sonst Video ohne Musik)
- [ ] Montserrat-Bold.ttf in `media/fonts/`

### 3.4 Posting & Engagement
- [x] Scheduler postet auf IG/FB
- [x] Comment-Auto-Reply mit Intent-Detection (Commit `3a1a6cc`)
- [x] DM-Auto-Reply (Code da)
- [ ] DM-Auto-Reply mit Meta-Webhooks (Phase 1.2) — *aktuell: Polling*
- [x] Token-Expiry-Banner (proaktiv 14d vorher) — *Phase 1.1 ✓*
- [x] 190/102-Handler (markiert Connection invalid + Notification) — *Phase 1.1 ✓*

### 3.5 Billing
- [x] Stripe-Subscription-Checkout (Starter/Pro/Agency)
- [x] Plan-Limits enforced (`plan_service`)
- [ ] Stripe-Webhook in Produktion verifiziert (`checkout.session.completed`, `invoice.paid`, etc.)
- [ ] Trial → Bezahlpflicht-Übergang getestet
- [ ] License-Key-Generation für Agency-Plan getestet

## 4 — Launch-DoD (pre-Live-Customer)

Was vor dem **ersten echten Kunden** erfüllt sein muss:

### 4.1 Meta-Compliance
- [ ] **Meta App Review** bestanden (Permissions: `pages_manage_posts`, `instagram_content_publish`, `pages_manage_engagement`, `pages_read_engagement`, `instagram_manage_comments`, `instagram_manage_insights`)
- [ ] Demo-Video für App-Review (5–7min, alle Permissions annotiert) gedreht
- [ ] Privacy-Policy-URL in Meta-App-Konfiguration eingetragen
- [ ] Test-User → Live-Mode Übergang dokumentiert
- [ ] Phase-1.2-Scopes (`pages_messaging`, `instagram_manage_messages`) als separater Review eingereicht ODER als "kommt später" kommuniziert

### 4.2 DSGVO
- [x] AVV-Vorlage mit Meta dokumentiert — *`docs/DSGVO_NOTES.md`*
- [ ] AVV mit Stripe abgeschlossen (Standard-DPA reicht)
- [ ] AVV mit Anthropic geprüft (Datenfluss-Klarheit: User-Content → Claude)
- [x] Retention-Policy für `connections.json` (90d nach `expires_at`) — *Phase 1.1 ✓ via `bot/jobs/retention.py`*
- [x] Account-Delete-Flow (Art. 17) — *Phase 1.1 ✓*
- [ ] Auskunfts-Flow (Art. 15) — Daten-Export für User
- [ ] Cookie-Banner (oder Begründung warum nicht — nur First-Party-Session-Cookies?)

### 4.3 Smoke-Test
- [ ] **TC-01 bis TC-14 aus [[Socibot/Phase-1-1-Smoke-Test]] alle GREEN** — Operator-Run mit Meta Test-User
- [ ] Stripe-Live-Mode End-to-End mit echter Test-Karte
- [ ] Video-Engine Erst-Run dokumentiert (Job-ID, Output-File, Upload-Result)

### 4.4 Deployment & Ops
- [ ] Hetzner CX32 (oder vergleichbar) provisioniert
- [ ] Domain + SSL (Let's Encrypt automatisiert)
- [ ] gunicorn workers≥2 → `pip install filelock>=3.13` Pflicht
- [ ] Backup-Strategie für `client/connections.json`, `data/*.db`, `client/users.json` (täglich, off-site)
- [ ] Error-Monitoring (Sentry oder strukturiertes File-Log + tägliche Inspect)
- [ ] Rate-Limit-Handling für Meta API (Error-Codes 4 = Rate Limit)
- [ ] Nightly Refresh-Job in Production-Schedule registriert (`refresh_meta_tokens` 03:01)
- [ ] Retention-Job in Production-Schedule registriert (04:00)
- [ ] Email-Versand für Notifications getestet (`SMTP_*` Env-Vars)

### 4.5 Hardening (Phase-1.1-Review-Bundle)
- [x] CSRF auf POST-Routes (flask-wtf) — *Phase 1.1 ✓*
- [x] CSP-Header
- [x] SECRET_KEY persistent über Restart
- [x] Fernet-Encryption für Tokens at-rest
- [x] HMAC-State für OAuth (Replay-Schutz hart)
- [x] filelock für `.env`, `connections.json`, `bot_settings.json`
- [ ] **filelock-Paket in `requirements.txt` und installiert** — *aktuell: graceful-fallback aktiv, Warning im Log*

---

## Reifegrad-Snapshot — 2026-04-29

| Block | Status | Anteil-DoD |
|---|---|---|
| Account & Onboarding | 🟡 in Arbeit (uncommitted) | 60% |
| Meta OAuth | ✅ Phase 1.1 funktional fertig | 95% |
| Andere Plattformen (LI/X/TT) OAuth | ❌ noch Token-Forms | 0% |
| Video Engine v4.0 | 🟡 implementiert, kein verifizierter Run | 70% |
| Content-Generation | ✅ funktional | 95% |
| Posting + Engagement | 🟡 IG/FB ja, TikTok-Stub | 70% |
| DM/Comment-Auto-Reply | ✅ funktional (Polling) | 80% |
| Billing | 🟡 Code da, Live-Test fehlt | 70% |
| DSGVO | 🟡 Hard-Stops fertig, AVV-Doku-Lücken | 75% |
| Hardening | ✅ Phase 1.1 ✓ | 95% |
| Deployment | ❌ lokal | 0% |
| Meta App Review | ❌ ausstehend | 0% |

**Customer-DoD ≈ 70%** (war 62% am 28.04, OAuth-Phase hat +8% gebracht)
**Launch-DoD ≈ 35%** (App-Review + Deployment sind die größten Brocken)

---

## Phasen-Roadmap

| Phase | Inhalt | Status | Kanban |
|---|---|---|---|
| **1.1** | Meta OAuth ohne API-Key-Eingabe | ✅ funktional fertig (vorbehaltlich Smoke-Test-Operator-Run) | [[Socibot/kanban/02-meta-oauth-phase-1-1]] |
| **1.2** | Meta-Webhooks + DM-Auto-Reply (Send) | offen | — |
| **1.3** | LinkedIn / X OAuth-Replacement | offen | — |
| **1.4** | TikTok Posting (über Buffer-API als Bridge) | offen | — |
| **2.0** | Multi-Tenant (resolve_token pro User statt single active) | offen, Architektur trägt | — |
| **2.1** | Meta-Webhooks für Comments (statt Polling) | offen | — |
| **3.0** | Video-Engine v4.0 verifizierter Erst-Run + MUBERT-Anbindung | offen | — |
| **L** | Launch-DoD Block 4.1–4.5 | offen | — |

---

## Pflege

- **Wenn ein DoD-Punkt erfüllt wird:** Checkbox setzen + Datum in Narrative im jeweiligen Kanban-Card
- **Wenn ein neuer Blocker auftaucht:** als neuer Eintrag im passenden Block, NICHT in Memory
- **Reifegrad neu schätzen:** alle 2 Wochen ODER nach jedem Phasen-Abschluss
- **Diese Note ist SSoT.** Wenn Memory-Snapshot oder Kanban abweicht, gewinnt diese Note.
