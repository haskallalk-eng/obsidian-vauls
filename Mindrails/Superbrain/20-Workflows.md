---
title: Superbrain Workflows
type: workflow
status: active
tags:
  - mindrails
  - superbrain
  - workflow
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
---

# Workflows

## Team-Start

1. [[Mindrails/Superbrain/01-Orchestrator|Orchestrator]] klärt Projekt, Ziel und Constraints.
2. [[Mindrails/Superbrain/06-Task-Routing-Matrix|Task Routing Matrix]] bestimmt Lead und Pflichtrollen.
3. [[Mindrails/Superbrain/24-Project-Knowledge-Base|Project Knowledge Base]] lädt Projektkontext.
4. Bei Code: [[Mindrails/Superbrain/25-Codebase-Loading-Protocol|Codebase Loading Protocol]] ausführen.
5. Team arbeitet im passenden Modus aus [[Mindrails/Superbrain/05-Team-Operating-System|Team Operating System]].

## Bugfix

1. [[Mindrails/Superbrain/10-Debugger|Debugger]] beweist den Bug und grenzt ihn ein.
2. [[Mindrails/Superbrain/11-Engineer|Engineer]] bestimmt Fix-Korridor, Blast-Radius und Tests.
3. [[Mindrails/Superbrain/12-Coder|Coder]] implementiert minimal.
4. [[Mindrails/Superbrain/13-Reviewer|Reviewer]] sucht Regressionen und falsche Annahmen.
5. [[Mindrails/Superbrain/14-QA-Tester|QA-Tester]] verifiziert automatisiert/manuell.
6. [[Mindrails/Superbrain/15-Security-Privacy|Security & Privacy]] prüft, falls Auth, Daten, Billing, Provider oder PII betroffen sind.

## Feature

1. [[Mindrails/Superbrain/02-Business-Coach|Business-Coach]] klärt Kundennutzen und Metrik.
2. [[Mindrails/Superbrain/04-Challenger-Council|Challenger-Council]] attackiert Scope und Risiko.
3. Engineer entwirft Daten-/Runtime-Verhalten.
4. Coder baut kleinste funktionierende Version.
5. QA prüft End-to-End und Settings -> Runtime-Wirkung.
6. Decision Gate entscheidet Ship, Iterate oder Kill.

## Strategie / Marktentscheidung

1. Business-Coach formuliert Entscheidung.
2. [[Mindrails/Superbrain/03-AI-Welt-Coach|AI-Welt-Coach]] aktualisiert Markt-/AI-Kontext.
3. [[Mindrails/Superbrain/22-Source-Verification|Source Verification]] prüft Quellenqualität.
4. Forecast in [[Mindrails/Superbrain/50-Forecast-Ledger|Forecast Ledger]] oder Experiment definieren.
5. Challenger-Council gibt Gegenposition.
6. Entscheidung in einem Decision-Record dokumentieren.

## SEO / Landingpage

1. [[Mindrails/Superbrain/32-SEO-Squad|SEO Squad]] bestimmt betroffene URL-/Seitenklasse.
2. [[Mindrails/Superbrain/33-Technical-SEO-Crawl-Index-Agent|Crawl & Index]] prüft Indexierbarkeit, Sitemap, Canonical, Robots.
3. [[Mindrails/Superbrain/36-Content-Intent-Agent|Content & Intent]] prüft Suchintention und Page-Value.
4. [[Mindrails/Superbrain/35-Structured-Data-Agent|Structured Data]] prüft JSON-LD und Entity-Drift.
5. [[Mindrails/Superbrain/34-SEO-Performance-CWV-Agent|Performance & CWV]] prüft mobile Geschwindigkeit und Web Vitals.
6. Je nach Seite: [[Mindrails/Superbrain/37-Local-SEO-Agent|Local]], [[Mindrails/Superbrain/38-Programmatic-SEO-Agent|Programmatic]], [[Mindrails/Superbrain/39-AI-Search-LLM-SEO-Agent|AI Search]].
7. [[Mindrails/Superbrain/41-SEO-Measurement-Agent|Measurement]] definiert Baseline, Erfolgskriterium und Revisit.

## Customer Incident

1. Symptom, Tenant, Zeitraum und Kundenaussage erfassen.
2. Debugger sucht Transcript/Logs/DB/Provider-Beleg.
3. Business-Coach bewertet Kundenschaden und Kommunikation.
4. Engineer/Coder fixen oder bauen Workaround.
5. QA macht Regression und Live-Smoke.
6. Postmortem, wenn Vertrauen, Daten oder Zahlung betroffen waren.

## Release / Deploy

1. Uncommitted Changes prüfen.
2. Tests/build/lint passend zur Änderung.
3. Reviewer prüft Diff.
4. Security prüft bei sensiblen Änderungen.
5. [[Mindrails/Superbrain/21-Decision-Gates|Decision Gates]]: deployen, warten oder zurückstellen.
6. Nach Deploy: Smoke, Logs, Health, betroffene User-Journey.

## Learning Review nach Arbeit

1. Outcome bewerten: funktioniert, teilweise, falsch oder unklar.
2. Scorecard für beteiligte Agenten aktualisieren.
3. Maximal drei Lessons in [[Mindrails/Superbrain/61-Learning-System|Learning System]] übernehmen.
4. Falls eine Annahme falsch war: Double-Loop-Lesson statt nur Task-Kommentar.
5. Falls ein Gate fehlte: [[Mindrails/Superbrain/21-Decision-Gates|Decision Gates]] aktualisieren.
