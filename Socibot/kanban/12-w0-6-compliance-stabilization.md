---
id: 12
status: in_progress
priority: P0
blocked_by: []
tags:
  - socibot
  - compliance
  - dsgvo
  - dod-blocker
  - persona-a-blocker
created: 2026-04-29
---

# W0.6 — Compliance-Stabilisierung (vor W0.5 + W0.75)

**Eingeschoben** zwischen W0 und W0.5. Risk-Check-v2 wurde von einem Sonnet-Agent ungeplant implementiert. Code-Review (Opus) + DSGVO-Review zeigen erhebliche Lücken. Persona-A-Production aktuell **NO-GO**.

## Critical-Fixes (P0, Hard-Block für Persona-A-Production)

### DSGVO-Critical
- [x] **C-01** `.gitignore` ergänzt um `data/compliance_audit.jsonl`, `data/compliance_cache.json`, `data/compliance_overrides.jsonl`, `data/*.jsonl`, `data/*.db*` (Edit done 2026-04-29)
- [ ] **C-02** Auth-Checks in allen `/compliance/*`-Routes via `session.get("user_id")`. `/audit` auf `current_user_id`-Scope einschränken. `/prune-audit` mit `ADMIN_SECRET`-Gate (analog `billing.py` Z.197)
- [ ] **C-03** Layer-2-Opt-Out (`skip_layer2: bool` im Request-Body). PII-Strip-Warning im UI vor Compliance-Check. AVV-Doku-Update in [DSGVO_NOTES.md](C:/Users/pc105/Desktop/Social%20media%20Bot/docs/DSGVO_NOTES.md): Anthropic als Sub-Auftragsverarbeiter mit SCCs. Onboarding-Pflicht-Checkbox "Anthropic-Transfer + Schweigepflicht-Hinweis"

### Code-Critical
- [ ] **B1** File-Locks für `compliance_audit.jsonl` + `compliance_cache.json` + atomares `tmp+rename` (Pattern aus [connections_service.py:217-230](C:/Users/pc105/Desktop/Social%20media%20Bot/dashboard/services/connections_service.py#L217) portieren)
- [ ] **B2** Absolute Pfade: `_REPO_ROOT = Path(__file__).resolve().parent.parent.parent` statt `Path(".")` (analog `connections_service.py:66-71`)
- [ ] **B5** Persona aus `client/brand_knowledge.json` (single source of truth, nicht Request-Body). Cost-Cap pro User/Monat für Layer-2-Calls (z.B. €5/Monat default)

### Pipeline-Critical (sonst totes Lib-Code)
- [ ] **N1** `check_compliance_v2()` in [variant_service.py:142](C:/Users/pc105/Desktop/Social%20media%20Bot/dashboard/services/variant_service.py#L142) Generation-Pipeline einhängen. Nach `_generate_with_instruction()`, vor User-Anzeige

## High-Fixes (P1, vor Customer-Launch)
- [ ] **HIGH-01** Cache speichert `matched_text` ([compliance_service.py:568-573](C:/Users/pc105/Desktop/Social%20media%20Bot/dashboard/services/compliance_service.py#L568)) → vor Cache-Save zu `""` setzen
- [ ] **HIGH-02** `user_id` aus `session` statt Request-Body in `/check` + `/override`
- [ ] **HIGH-03** Justification als Hash in Audit-JSONL, Klartext nur in encrypted DB (Phase 2)
- [ ] **HIGH-04** `/prune-audit` Operator-Gate (siehe C-02)
- [ ] **HIGH-05** Layer-2-Fallback **fail-closed** für `arzt`/`heilpraktiker` (HIGH_RISK_PERSONAS): bei Exception → `risk_level="medium", blocking=True` statt `low`/`False`
- [ ] **N2** `_prune_audit()` als APScheduler-Job in [bot/scheduler.py](C:/Users/pc105/Desktop/Social%20media%20Bot/bot/scheduler.py) registrieren (täglich 04:30, analog [retention.py](C:/Users/pc105/Desktop/Social%20media%20Bot/bot/jobs/retention.py))

## Pattern-Sprint (W1.5, eigener Sprint NACH W0.6)
- [ ] **B3** UWG5-02 (Anwalt) blockt legitime "kostenlose Erstberatung"-Posts
- [ ] **B4** HEILPRG-02 verfehlt eigenes example aus JSON (Reihenfolge-Bug)
- [ ] **B3-extra** Realistic Pattern-Audit mit Anwalt + Heilpraktiker als Reviewer (NICHT AI-generated patterns)
- [ ] Test-Set durch **realistic Posts** ersetzen — nicht mehr Pattern-Examples (Tautologie)
- [ ] Soll-Werte: Layer-1 Recall ≥70%, Layer-1+2 Recall ≥95%, FP-Rate ≤10%

## Was bleibt gut

Architektur, Dataclass-Struktur, Audit-Trail-Konzept (hash-only-Idee), Layer-Gating-Idee, Cache-Invalidation — solide Basis. Patches sind nicht trivial, aber kein "weg-und-neu".

## Reihenfolge

```
1. C-01 (.gitignore)            — DONE 2026-04-29
2. B1+B2 (locks + paths)        — 1-2h
3. C-02 (auth + scoping)        — 1-2h
4. B5 (persona + cost-cap)      — 2-3h
5. N1 (pipeline-integration)    — 1h
6. HIGH-01..05                  — 2-3h
7. C-03 (Layer-2-opt-out + AVV) — 2h Code + Operator-AVV-Aufgabe
8. N2 (prune-cron)              — 30min
9. PATTERN-SPRINT W1.5          — separater Sprint, 1-2 Tage
```

## Skills
- [security-dsgvo-reviewer](C:/Users/pc105/.claude/agents/security-dsgvo-reviewer.md) Pflicht nach jedem Fix
- [claude-api](C:/Users/pc105/.claude/skills/claude-api/) für Layer-2-Optimierung
- Code-Reviewer (Opus) Pflicht über Sonnet-Implementer-Output
