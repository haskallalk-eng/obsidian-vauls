---
title: Codex-Findings 2026-04-30
type: review
status: active
parent: "[[Socibot/Overview]]"
created: 2026-04-30
related:
  - "[[Socibot/DoD]]"
  - "[[Socibot/ZuTun]]"
---

# Codex-Findings — 3 Reviews am 2026-04-30

Codex (`codex:codex-rescue`) wurde dreimal als unabhängiger Reviewer eingesetzt:

1. **Strategy-Review** vor Wellen-Start (Pre-Implementierung)
2. **Sanity-Check** nach Plan-Revision (Mid-Implementierung)
3. **Final-Review** der 3 großen Wellen W0.6+W0.75+W0.5 (Post-Implementierung)

Plus Opus-Code-Reviews + DSGVO-Reviews pro Welle.

## Review #1 — Strategy-Review (Pre-W0)

**Verdikt**: tragfähig, aber zu feature-lastig + zu wenig messbar.

**Top-5 Lücken** (alle akzeptiert + integriert):
- **C-1 (Critical)**: Eval/Telemetry fehlt komplett → führte zur Einführung von **W0.5 Eval-Framework**
- **C-2 (Critical)**: Risk-Check zu schwach (pure Regex) → führte zu **Hybrid Layer 1+2** mit Claude-Branchen-Reviewer
- **H-3 (High)**: Voice-Few-Shot kippt in Token-Bloat (5-20 Posts in jedem Prompt) → wurde in W3b zurückgestellt mit klarer Mechanik (Style-Memory + Retrieval + Caps + Decay)
- **H-4 (High)**: W2 AI-Zeremonie ohne Nachweis → Hook-Split nur ab Premium, Self-Critique nur ab Maximum
- **M-5 (Medium)**: Plan zu feature-lastig → Voice-Recording raus, Tiefen-Onboarding gekürzt auf 3 Pflichtfragen

## Review #2 — Sanity-Check (revidierter Plan)

**Verdikt**: bedingt tragfähig.

**Reihenfolgen-Korrektur**: API-Key-Frei-Sweep aus W1 auf **W0.75** vorziehen (Customer-DoD-Hard-Stop früh schließen, sonst werden Setup/Auth-Pfade zweimal angefasst).

Plus: W0.5-Rubric misst Stilqualität, NICHT Regeltreue → Compliance-Metriken (`Risk-Recall`, `False-Block-Rate`, `Override-Rate`) ergänzen — dokumentiert in [[Socibot/DoD]] Block 2.5.

## Review #3 — Final-Review nach W0.6+W0.75+W0.5

**Verdikt**: Foundation strukturell in Ordnung, aber W2 ist noch kein dünner Aufbau darauf — Tier-Modell, Baseline und Telemetrie haben echte Inkonsistenzen.

### 5 P0/P1-Findings

#### P0 — Tier-Vokabular-Mismatch

`cost_tracker.py` kennt nur `trial/starter/pro/agency`. `premium/maximum` als Quality-Tier existieren nirgendwo. W2-Pricing nicht ausdrückbar bis Tier-Vokabular end-to-end existiert.

**Files**: 
- `dashboard/services/cost_tracker.py:29` (`TIER_EXPECTED_EUR_PER_VARIANT` dict)
- `dashboard/routes/eval_dashboard.py:58`
- `dashboard/services/plan_service.py:5`

**Fix-Plan**: W1.6 — `quality_tier ∈ {standard, premium, maximum}` als orthogonalen Param zum plan_tier. Default `standard`. Kein Tier-Reshuffle der Plans.

#### P0 — Baseline-Pfad nicht vertrauenswürdig (FIXED in W0.5b `da07009`)

`run_baseline.py` rief `log_generation()` mit alter Mock-Signatur auf (`output_text/score/label` statt `output_full/tokens_in/tokens_out/latency_ms/model_used`). Baseline-Runs hätten silently mit WARN-Logs geloopt.

**Status**: ✅ gefixt in W0.5b. Vollständige Signatur, plus echte Latency-Messung via `time.monotonic()`.

#### P1 — Compliance-Floor instabil (TEILWEISE FIXED in W1.5 `3a6562b`)

- `UWG5-02` (Anwalt): blockierte JEDE legitime „kostenlose Erstberatung" (BVerfG-konform) → Pattern jetzt nur Trigger wenn kostenlos+Erstberatung+Garantieversprechen kombiniert ✅
- `HEILPRG-02` (Heilpraktiker): verfehlte das eigene example aus dem JSON (Reihenfolge-Bug) → Bidirektionales Pattern ✅
- `HEILPRG-03` neu: Implicit-Heilversprechen für Schmerz/Migräne/etc. als soft_block ✅

**Restlücke**: „garantieren VOR kostenlos" wird nur via Layer-2 Claude-Pass gefangen (semantisch zu komplex für Regex). Echtes Pattern-Audit mit Anwalt + Heilpraktiker als juristische Reviewer bleibt User-Aufgabe (siehe [[Socibot/ZuTun]] #4).

#### P1 — Eval-Telemetrie nicht an User-Outcomes gekoppelt (FIXED in W0.5b `da07009`)

`record_user_feedback()` wurde nirgends in `approval.py` aufgerufen. Der `log_entry_id` im Variant-Dict war nie zu Approval/Rejection-Outcomes verknüpft → kein RLHF-Loop.

**Status**: ✅ Hook in `approve_post()` und `reject_post()` (fail-open).

#### P1 — C-03 nicht end-to-end

`skip_layer2`-Param ist im aktuellen Tree NICHT auffindbar. Der W0.6-Sonnet-Agent hat es im Service-Docstring dokumentiert aber nicht implementiert.

**Files**:
- `dashboard/services/compliance_service.py:664` (Docstring nennt skip_layer2, Code hat keinen)
- `dashboard/routes/compliance.py:81`
- `public/index.html:212` (Onboarding-Disclosure-Platzhalter)
- `public/datenschutz.html:43` (Anthropic-AVV-Hinweis-Platzhalter)

**Fix-Plan**: C-03-Welle (Pre-Live-Customer):
1. `skip_layer2: bool = False`-Param in `check_compliance_v2()` durchschleifen
2. Onboarding-Pflicht-Checkbox: „Ich bin einverstanden dass Posts an Anthropic (USA) zur Compliance-Prüfung übertragen werden + Schweigepflicht §203 StGB"
3. AVV mit Anthropic abschließen (https://privacy.anthropic.com/de/policies/dpa)
4. Datenschutzerklärung erweitern: Anthropic Inc., 548 Market St SF CA 94104, Sub-Auftragsverarbeiter, SCCs nach Beschluss 2021/914/EU
5. UI-Toggle „Tiefen-Compliance-Prüfung" mit Layer-2-Opt-Out

## 3 Stops vor W2

| # | Stop | Status |
|---|---|---|
| 1 | Baseline-Runner reparieren + 250-Case-Run | ✅ Code in W0.5b. Run noch nicht ausgeführt (~€5-10) |
| 2 | W1.5 Pattern-Refresh (UWG5-02 + HEILPRG-02) | ✅ in W1.5 `3a6562b`. Audit mit echten Reviewern noch User-Aufgabe |
| 3 | premium/maximum als first-class quality_tier | ❌ W1.6 offen |

C-03 ist parallel-fähig zu W2, kein Stop.

## Architektur-Drift-Beobachtungen

Codex hat folgende Storage-Patterns in der Foundation identifiziert — nicht Bug, aber Inkonsistenz:

- `compliance_service` nutzt **JSONL + JSON-Cache** mit FileLock
- `eval_logger` nutzt **JSONL** mit FileLock + atomic-tmp-rename
- `cost_tracker` nutzt **SQLite** mit WAL-Mode
- `connections_service` nutzt **JSON** mit FileLock + atomic-tmp-rename

Ist akzeptable Spezialisierung pro Service-Bedarf, aber Wartung wird komplexer wenn 4 verschiedene Storage-Pattern parallel existieren. Bei Phase-2-Multi-Tenant könnte ein einheitliches DB-Layer (Postgres oder SQLite-shared) sinnvoll werden.

## Hidden-Risk-Matrix

| Risk | Wahrscheinlichkeit | Mitigation |
|---|---|---|
| `filelock` nicht in `requirements.txt` → Race-Conditions bei gunicorn workers≥2 | Hoch in Production | `pip install filelock>=3.13` als Pre-Live-Step |
| `flask-wtf` nicht installiert → CSRF inaktiv | Hoch in Production | `pip install flask-wtf` als Pre-Live-Step |
| Cost-Cap €5/User/Monat zu hoch oder zu niedrig | Mittel | Ein Monat Real-Daten dann adjusten |
| Eval-Logger-JSONL wächst bei 100 Active-Users × 30 Variants/day = 3000/day | Mittel | 90d-Retention reicht. Rotation-Job ist registriert. Bei >100k entries/month: SQLite-Migration prüfen |
| Opus-Judge wird Anthropic-deprecated | Niedrig kurzfristig | `JUDGE_MODEL` als ENV-override existiert |
| Pricing Add-On €20/Mo nicht verkaufbar | Mittel | Erst nach W1.6 mit echten Tier-Daten validieren |

## Verwandte Notes

- [[Socibot/Overview]] — Stand-Hub
- [[Socibot/DoD]] — Master-Checkliste
- [[Socibot/ZuTun]] — Backlog
- [[Socibot/Architecture]] — Pipeline-Snapshot
- [[Daily/2026-04-30]] — Tageschronologie
