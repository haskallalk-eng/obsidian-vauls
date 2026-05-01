---
tags: [project, socibot, backlog]
status: active
parent: "[[Mindrails/Overview|Mindrails]]"
created: 2026-04-30
updated: 2026-04-30
---

# Socibot — ZuTun (Backlog)

## 0. Review der 19 ungepushten Commits (USER)

Master ist 19 commits ahead von origin/master, alles lokal. Vor Push:

1. **Push-Entscheid**: alle 19 zusammen ODER schrittweise (W0-Cluster zuerst, dann W0.6+W0.75+W0.5+W1.5)?
2. **PAT-Issue**: `.git/config` Remote-URL hat Github-PAT (`ghp_...`) im Klartext eingebettet. Wahrscheinlich der suspendierte Hansweier-PAT. Empfehlung:
   ```
   git remote set-url origin https://github.com/Hansweier/social-media-saas.git
   ```
   Plus PAT rotieren auf Github falls noch aktiv. Memory-Notiz sagt aktiver PAT ist auf `haskallalk-eng`.
3. **Welche Commits** zuerst lesen: in der Reihenfolge `f1c3d72` (Auth-Foundation) → `1b30163` (OAuth) → `b6bbca1` (Compliance v2) → `e0b35f3` (API-Key-Frei) → `c60e7bb` (Eval-Framework). W0.5b + W1.5 sind kleine Patches.

## 1. W1.6 — quality_tier orthogonal zum plan_tier (~1-2h)

Codex-P0-Finding: `cost_tracker.py` kennt nur `trial/starter/pro/agency`. `premium/maximum` als Quality-Tier existieren nirgendwo. W2-Pricing nicht ausdrückbar.

**Plan**:
- `eval_logger.log_generation()` neuer Param `quality_tier ∈ {standard, premium, maximum}` (default standard)
- `cost_tracker.py` segmentiert optional nach quality_tier neben plan_tier
- `variant_service.generate_variants()` liest `quality_tier` aus User-Settings (oder Default)
- DoD um Tier-Mechanik erweitern

## 2. W2 — Tier-Backend (4-6h, NACH W1.6)

- Tier-Router (immer aktiv)
- Hook+Body-Split (Premium+)
- Self-Critique-Pass (Maximum)
- Cost-Estimator zeigt €/Variant pro Tier

## 3. C-03 — Layer-2-Opt-Out + AVV + Onboarding ✅ ERLEDIGT 2026-04-30

Alle 5 Tracks implementiert, 52/52 Tests grün. Persona-A (Anwalt/Arzt) Hard-Block aufgehoben.
Details → [[Daily/2026-04-30]].

## 4. W1.5-Folge — Pattern-Audit mit Real-World-Reviewer (USER)

Heute gepatcht (UWG5-02, HEILPRG-02, HEILPRG-03 neu, Test grün). Aber: **realistisches Pattern-Set braucht juristische Validierung**.

- Anwalt-Reviewer für `compliance/anwalt.json` (BORA, BRAO, UWG)
- Heilpraktiker-Reviewer für `compliance/heilpraktiker.json` (HeilprG, HWG)
- Arzt-Reviewer für `compliance/arzt.json` (HWG, MBO-Ä)
- Coach-Reviewer für `compliance/coach.json` (PsychThG-Abgrenzung)
- Steuerberater-Reviewer für `compliance/steuerberater.json` (StBerG, BOStB)

Test-Set durch realistische Posts ersetzen — keine Pattern-Examples (Tautologie-Test).

## 5. Echter Baseline-Run

Nach W1.6: `python tools/eval/run_baseline.py --label "vor-w2" --limit 50` mit echten Anthropic-API-Calls. Geschätzte Kosten: €5-10 pro Run (Generator Sonnet + Judge Opus über 50 Cases). Snapshot als `data/eval/baselines/vor-w2_*.json` lokal halten (gitignored).

## 6. Test-Run Video Engine v4.0

Smoke-Test der gesamten Video-Pipeline: Prompt → Generation → Upload → Post. Steht seit 2026-04-18 aus. Unabhängig von Eval-Framework.

## 7. Push-Setup

Nach Review:
- `git remote set-url` (PAT rauswerfen)
- `git push origin master` (~19 commits)
- ggf. CI/Hooks für Tests

## Verbundene Notes

- [[Socibot/Overview]]
- [[Socibot/DoD]]
- [[Socibot/Marktluecke]]
- [[Socibot/Phase-1-1-Smoke-Test]]
- [[Socibot/modules/14-Findings]]
- [[Socibot/kanban/12-w0-6-compliance-stabilization]]
- [[Socibot/kanban/11-api-key-frei-sweep]]

## Narrative

- **2026-04-30 (C-03)**: C-03 vollständig implementiert — `skip_layer2`-Param in `compliance_service` + Route-Forwarding, DSGVO-Opt-Out-Toggle in `qualitaet.html` + neue Route `/einstellungen/qualitaet/skip-layer2`, Pflicht-Checkboxen (Anthropic-Consent + §203) in `/register` + `auth.py`, `update_fields()` in `user_service`, Anthropic-Sub-AVV in `datenschutz.html` + `DSGVO_NOTES.md`. 52/52 Tests grün. Persona-A-Hard-Block (Anwalt/Arzt) aufgehoben. Kein Commit/Push. → [[Daily/2026-04-30]]
- **2026-04-30 (final)**: 19 commits done. **Wellen heute**: Welle 0 (Phase-1.1-Close, 9 cluster commits f1c3d72..f8666c8), W0.6 (Compliance-v2 + Stabilisierung, b6bbca1), W0.75 (API-Key-Frei-Sweep, e0b35f3), W0.5 (Eval-Framework Integration, c60e7bb), W0.5b (Codex-Quick-Fixes, da07009), W1.5 (Pattern-Refresh, 3a6562b). 165 Tests grün, 0 skipped. **Codex-Verdikt**: Foundation solide, vor W2 noch W1.6 + C-03 nötig. Master 19 ahead, kein Push. → [[Daily/2026-04-30]]
- 2026-04-30 (nacht): W0.5 Track 4 (Gold-Set + Baseline-Tools) implementiert — `tools/eval/generate_gold_set.py` (250 Cases, append-only JSONL), `tools/eval/run_baseline.py` (BaselineSnapshot, Aggregation per Persona/Platform/Dimension), `tools/eval/compare_baseline.py` (CI-Block bei Persona-Regression). 31/31 Tests grün. Alle 4 Tracks fertig. Integration-Step ausstehend. → [[Daily/2026-04-30]]
- 2026-04-30 (abends): W0.5 Track 2 (cost_tracker) implementiert — `dashboard/services/cost_tracker.py` (~260 LOC), `dashboard/routes/eval_dashboard.py`, `dashboard/templates/eval_dashboard.html`, `tests/test_cost_tracker.py` (24/24 grün). Tier-Drift-Alerts (warn>=15%, alert>=30%), SQLite WAL-Mode, Operator-Dashboard `/eval/`. → [[Daily/2026-04-30]]
- 2026-04-30: W0.5 Track 1 (eval_logger) implementiert — `dashboard/services/eval_logger.py` + `bot/jobs/eval_retention.py` + `tests/test_eval_logger.py`. 34/34 Tests grün. Logging-Foundation für Eval-Framework steht. → [[Daily/2026-04-30]]
