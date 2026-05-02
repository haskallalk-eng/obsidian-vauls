---
id: 13
status: in_progress
priority: P1
blocked_by: []
tags:
  - socibot
  - ads
  - meta-marketing-api
  - beta
  - persona-a
created: 2026-05-02
---

# Ads-Beta — Meta Boost-Post-Funktion

Beta-Modul für Meta Ads (Boost-Post). Nach Approve eines Posts kann Customer ihn als Bezahlt-Post pushen. Feature-flagged via `ADS_BETA_ENABLED=true` in `.env` — Default OFF.

## Job Story

**When** ein Customer einen Post approved hat und mehr Reichweite will, **I want to** ihn mit einem Klick als Boost-Post launchen können (Audience aus brand_knowledge automatisch, Budget aus Plan-Limits), **so I can** Reichweite skalieren ohne Meta-Ads-Manager zu öffnen.

## Architektur

```
Approved-Post
   │
   │ Klick "Boost €X"
   ▼
┌──────────────────────────────────┐
│ Compliance-Pre-Check (verschärft) │  is_ad=True
│ Layer 1: Ads-spezifische Patterns │  (BORA-§7 enger als BORA-§6)
│ Layer 2: PFLICHT für Ads (egal    │  (BOStB §10 nur bei Ads)
│         welcher Plan-Tier)        │
└──────────────────────────────────┘
       │
       ├── Hard-Block? → kein Boost möglich
       ▼
┌──────────────────────────────────┐
│ Audience-Generation               │
│ Aus brand_knowledge.json:         │
│ - core_service → Interest-IDs    │
│ - location → Geo-Targeting       │
│ - target_audience → Age + Gender │
└──────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│ Budget-Cap-Check                  │
│ Plan-Limits aus plan_service:    │
│ - Trial: max €5/Boost            │
│ - Starter: max €20/Boost         │
│ - Pro: max €50/Boost             │
│ - Agency: unlimited              │
│ Plus monatliches Cumulative-Cap   │
└──────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────┐
│ Meta Marketing API Call           │
│ POST /act_<account>/ads          │
│ creative_id aus existing post     │
│ targeting + budget + objective    │
└──────────────────────────────────┘
       │
       ▼
   ads_history.jsonl (Audit)
```

## Acceptance Criteria

### Backend
- [ ] `dashboard/services/ads_service.py` — Meta Marketing API Wrapper
  - `boost_post(post_id, budget_eur, duration_days, audience_override=None)`
  - `get_boost_status(boost_id)`
  - `cancel_boost(boost_id)`
  - `get_user_boost_history(user_id)`
  - `estimate_audience_size(brand_knowledge, location)`
- [ ] `meta_oauth_service.py` — neuer optionaler Scope `ads_management` + `ads_read` + `business_management`
  - Separate `/auth/meta/connect-ads`-Route (nicht im Default-Onboarding)
  - User wählt explizit: "Auch Ads-Berechtigung erteilen?"
- [ ] `compliance_service.check_compliance_v2()` neuer Param `is_ad: bool = False`
  - Ad-Mode: Layer-2 Pflicht egal Plan-Tier (Ads sind höheres Risiko)
  - Ad-spezifische Patterns: BORA-§7 verschärft, BOStB §10 strenger, BORA-§43b harter Block
- [ ] Persona-Pattern-Erweiterungen:
  - `compliance/anwalt.json`: ADS-BORA-7 (zusätzlich zu BORA-6 für organische Posts)
  - `compliance/steuerberater.json`: ADS-BOStB-10
  - `compliance/heilpraktiker.json`: ADS-HWG-11 strenger
  - `compliance/arzt.json`: ADS-MBO-Ä-27
  - `compliance/coach.json`: keine spezifischen Ads-Verschärfungen (UWG reicht)

### Frontend
- [ ] `dashboard/routes/ads.py` — Boost-Routes
  - GET `/ads/` — Boost-History-Page
  - POST `/ads/boost/<post_id>` — Boost-Trigger
  - GET `/ads/status/<boost_id>` — Status-Check
  - POST `/ads/cancel/<boost_id>` — Cancel
- [ ] Boost-Button im Approval-Flow (`approval.py` Variant-Card)
  - Nur sichtbar wenn `ADS_BETA_ENABLED=true` UND Customer hat ads_management-Connection
  - Mit Compliance-Vorschau (zeigt is_ad=True-Block falls nötig)
- [ ] `dashboard/templates/ads.html` — Boost-Konfigurations-Modal
  - Budget-Slider mit Plan-Limits
  - Duration (1-7 Tage)
  - Audience-Override-Option (Advanced)
  - Compliance-Pre-Check-Anzeige
  - Cost-Estimate

### DSGVO + Audit
- [ ] `data/ads_history.jsonl` — append-only Audit (FileLock + 90d retention)
  - Felder: ad_id, user_id, post_id, budget, duration, started_at, completed_at, spend, reach
- [ ] Onboarding-Erweiterung: separate Pflicht-Checkbox für Ads (Meta Marketing-API + DSGVO)
- [ ] `docs/DSGVO_NOTES.md` — Ads-Section mit Marketing-API-Datenfluss

### Feature-Flag
- [ ] `ADS_BETA_ENABLED=true` in `.env.example` (Default leer = aus)
- [ ] Beta-Banner in `ads.html` und im Approval-Flow

### Tests
- [ ] `tests/test_ads_service.py` — Mock Meta Marketing API
- [ ] `tests/test_ads_compliance.py` — is_ad=True Verschärfung verifizieren

## Beta-Limitationen

- **App-Review nötig** für Production (Meta-Permissions `ads_management` + `ads_read`)
- **Nur deutsche Targeting-Locations** (Audience-Builder MVP)
- **Keine A/B-Test-Splits** (eine Variant → ein Boost, kein Split)
- **Keine Performance-Reports** (Phase 2: Spend-/Reach-Polling-Job)
- **Keine TikTok/LinkedIn-Ads** (nur Meta — andere Plattformen separater Sprint)

## Risiken

| Risiko | Mitigation |
|---|---|
| Meta App Review für ads_management = 14-30d Wait | Beta-Flag default OFF, Operator-only-Test bis Review durch |
| BORA-§7 / BOStB §10 strenger bei Ads als bei Posts | Layer-2 Pflicht für Ads, eigene Pattern-Sets |
| Customer überschreitet Budget-Cap | Plan-Limit + monatliches Cumulative-Cap, beide hart enforced |
| Bezahlte Boost wird abgelehnt von Meta (Compliance) | `get_boost_status` pollt + zeigt Error im UI |
| Audience zu klein (Specificity-Trap) | `estimate_audience_size` zeigt Range vor Boost-Confirm |

## Phase-Roll-out

- **W3-Ads.1 (heute)**: Backend + Compliance + Basic-UI mit Feature-Flag
- **W3-Ads.2** (separater Sprint): Performance-Reports, A/B-Splits, Budget-Optimierung
- **W3-Ads.3** (Phase 2): LinkedIn-Ads (separate Marketing API), Cross-Platform-Reports

## Verwandte Notes
- [[Socibot/Overview]]
- [[Socibot/DoD]] — bekommt neuen Block "Ads-Quality"
- [[Socibot/Marktluecke]] — Persona-A-Anwälte werben restriktiv (BORA-§43b)
- [[Socibot/Architecture]] — Ads-Pipeline ergänzen
