---
tags: [project, socibot, mindrails]
status: active
parent: "[[Mindrails/Overview|Mindrails]]"
created: 2026-04-18
updated: 2026-04-30
---

# Socibot — Social Media Automation Bot

> Ein Produkt von [[Mindrails/Overview|Mindrails]].

## Was ist es

AI-getriebenes Social-Media-SaaS für deutsche KMUs. Generiert + plant + postet Brand-konforme Posts auf IG/FB/LinkedIn/X/TikTok. Persona-A-Fokus: **DSGVO-Beratungsbranche** (Anwälte, Steuerberater, Coaches, Heilpraktiker, Therapeuten) — siehe [[Socibot/Marktluecke]].

## Wo liegt der Code

`Desktop/Social media Bot/` — Python 3.11 / Flask / Jinja2 / Vanilla JS / Catppuccin-Mocha-Theme.
Repo: `Hansweier/social-media-saas` (Branch: `master`).

## Stand 2026-05-01

**22 commits ahead** von `origin/master` (lokal, **kein Push**). 10 Wellen, 254 Tests grün, 0 skipped.

| Welle | Commit | Inhalt |
|---|---|---|
| W0 (1-9/9) | `f1c3d72`..`b6bbca1` | Phase-1.1 Auth + Meta-OAuth + DSGVO + UI-Refactor + Compliance v2 |
| W0.6 | `b6bbca1` (gemerged) | Risk-Check v2 Stabilisierung (Locks, Paths, fail-closed, Cost-Cap) |
| W0.75 | `e0b35f3` | API-Key-Frei-Sweep (Customer ohne Token-Forms) |
| W0.5 | `c60e7bb` | Eval/Telemetry-Foundation (Logger+Cost+Judge+Gold-Set) |
| W0.5b | `da07009` | Codex-Quick-Fixes (run_baseline-Signature + Feedback-Hook) |
| W1.5 | `3a6562b` | Pattern-Refresh (UWG5-02 + HEILPRG-02/03) |
| W1.6 | `1e4ea2a` | quality_tier ∈ {standard, premium, maximum} orthogonal zu plan_tier |
| W2 | `5c5ae10` | Tier-Backend: Hook+Body-Split (Premium) + Self-Critique (Maximum) + UI |
| C-03 | `5608f9e` | DSGVO: skip_layer2-Opt-Out + Anthropic-AVV + Onboarding-Pflicht-Checkboxen |
| Codex-P0/P1-Fixes | `4658496` | skip_layer2 server-side enforced, Tier-Merge, Re-Consent-Gate, Regen via TierPipeline |
| W3-Ads.1 (Beta) | `0cd447d` | Meta Boost-Post-Beta — feature-flagged ADS_BETA_ENABLED. ads_service + 5 Persona-Ads-Pattern-Files + is_ad-Compliance-Verschärfung + UI |
| W3 Voice-Few-Shot | `5788038` | Lerneffekt-MVP — Approved Posts als Few-Shot in Generation-Prompt, Decay 30d, Downgrade bei späterem Reject |

**25 Commits ahead. 317 Tests grün. Alle Codex-Findings erledigt — Persona-A-Beta-Launch bedingt tauglich.** Siehe [[Socibot/Codex-Findings-2026-04-30]] + [[Socibot/kanban/13-ads-beta]].

## Aktive Themen

- [[Socibot/ZuTun|🔥 Backlog]] — Push-Review als Top-Item, dann W1.6 → W2 → C-03
- [[Socibot/DoD|✅ Definition of Done]] — 7-Block-Master-Checkliste
- [[Socibot/Marktluecke|🎯 Marktlücke + Persona-A]]
- [[Socibot/Architecture|🏗 Architektur-Snapshot]] — Compliance + Eval-Pipeline
- [[Socibot/Codex-Findings-2026-04-30|🔍 Codex-Findings]] — Pre-W2-Stops
- [[Socibot/Phase-1-1-Smoke-Test|🧪 Phase-1.1 Smoke-Test-Plan]]
- [[Socibot/kanban|📋 Kanban-Board]] — 12 Cards (Quality-Hebel + W0.6 + W0.75)

## Modul-Dokumentation (Stand 2026-04-27, vor heutigen Wellen)

Code-belegte Bestandsaufnahme der Pre-Welle-0-Architektur:

- [[Socibot/modules/00-Overview|00 Topology]] — Stack, LOC, Sidebar-IA
- [[Socibot/modules/20-Summary|20 Master-Summary]] — alles auf einen Blick
- [[Socibot/modules/14-Findings|14 Findings]] — Code-belegte Risiken
- Layer: [[Socibot/modules/15-Layer-Frontend|Frontend]] · [[Socibot/modules/16-Layer-Backend|Backend]] · [[Socibot/modules/17-Layer-Database|Database]]
- Cross-cutting: [[Socibot/modules/18-Routes-Map|Routes-Map]] · [[Socibot/modules/19-Connections|Connections]]

> **Hinweis**: Module-Notes spiegeln Stand 2026-04-27. Heutige Wellen (Auth, OAuth, Compliance v2, Eval-Framework, API-Key-Frei) sind in Module-Notes noch nicht reflektiert. Source-of-Truth für aktuellen Stand: [[Socibot/Architecture]] + Live-Code.

## Pricing & Plans

| Plan | Posts/Monat | Plattformen | Preis |
|---|---|---|---|
| Trial | 30 | 3 | Free |
| Starter | 150 | 3 | €79/Mo |
| Pro | unlimited | 5 | €149/Mo |
| Agency | unlimited | 5 | €349/Mo |

**Quality-Tier-Add-On (geplant W1.6+W2)**: +€20/Mo für Premium auf jedem Plan (Hook+Body-Split + Self-Critique). Maximum-Tier nochmal mehr (Multi-Pass-Refinement).

## Kritische Pre-Live-Customer-Tasks

- [ ] **Push-Review** der 19 Commits (User-Aufgabe, siehe [[Socibot/ZuTun]] #0)
- [ ] **PAT-Cleanup** — `.git/config` hat Klartext-Token in Remote-URL
- [ ] **W1.6** quality_tier orthogonal zum plan_tier (~1-2h)
- [ ] **C-03** Layer-2-Opt-Out + Anthropic-AVV + Onboarding-Pflicht-Checkbox (~2-3h)
- [ ] **W2** Tier-Backend: Hook+Body-Split + Self-Critique + Tier-Router (~4-6h)
- [ ] **Pattern-Audit** mit echtem Anwalt + Heilpraktiker als Reviewer
- [ ] **Echter Baseline-Run** (`tools/eval/run_baseline.py`, ~€5-10 Anthropic-Kosten)
- [ ] **Meta App Review** (Production-Posting)
- [ ] **Hetzner CX32 Deployment** + Domain + SSL

## Verwandt

- [[Daily/2026-04-30]] — alle heutigen Wellen chronologisch
- [[Daily/2026-04-27]] — Sidebar-Refactor + Modul-Doku
- [[Daily/2026-04-18]] — Video-Engine v4.0
