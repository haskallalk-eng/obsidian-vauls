---
title: Decision Gates
type: governance
status: active
tags:
  - mindrails
  - superbrain
  - decisions
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
---

# Decision Gates

Decision Gates verhindern, dass Momentum mit Wahrheit verwechselt wird.

## Gate 1: Bug ist echt

- Repro, Log, DB-Beleg oder Codepfad vorhanden.
- Alternative "kein Bug / falsche Erwartung / Konfiguration" geprüft.
- Root-Cause benannt.
- Regressionsrisiko bekannt.

## Gate 2: Fix ist sicher

- Minimaler Patch.
- Tests decken den Rückfall ab.
- Keine fremden Worktree-Änderungen überschrieben.
- Tenant/Auth/Billing/PII geprüft, wenn betroffen.
- Rollback oder Safe-Failure bekannt.

## Gate 3: Feature hat Geschäftswert

- Zielkunde klar.
- Metrik klar.
- Settings wirken wirklich in Runtime/Prompt/API.
- UX erklärt Konsequenzen.
- Default ist sicher und verständlich.

## Gate 4: AI-/Prompt-Änderung darf live

- Tenant-spezifische Konfiguration korrekt.
- Cache/Deploy-Wirkung verstanden.
- Prompt sagt nicht, was Tools nicht können.
- Task-level Eval oder Persona-Stress-Test vorhanden.
- Fallback bei Nichtverstehen, Tool-Fehlern und Unsicherheit.

## Gate 5: Strategie-Wette lohnt sich

- Business-Coach sagt: Kundenproblem und Zahlungshebel sind real.
- AI-Welt-Coach sagt: Timing und Technologie sprechen dafür.
- Challenger-Council hat Top-Risiken geprüft.
- Forecast oder Experiment mit Deadline existiert.
- Abbruchkriterium ist klar.

## Gate 6: Deploy

- Working Tree verstanden.
- Build/Test passend.
- Migration/Env/Provider-Effekte bekannt.
- Smoke-Test definiert.
- Kein Deploy, wenn parallele Arbeit oder User-Stopp dagegen spricht.

