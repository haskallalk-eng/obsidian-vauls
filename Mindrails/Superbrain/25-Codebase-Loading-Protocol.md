---
title: Codebase Loading Protocol
type: protocol
status: active
tags:
  - mindrails
  - superbrain
  - code
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
---

# Codebase Loading Protocol

Dieses Protokoll verhindert, dass das Team mit altem oder falschem Codewissen arbeitet.

## Reihenfolge bei Code-Aufgaben

1. Projekt aus [[Mindrails/Superbrain/24-Project-Knowledge-Base|Project Knowledge Base]] identifizieren.
2. Git-Status prüfen.
3. Projekt-Regeln lesen: `CLAUDE.md`, `AGENTS.md`, README oder Vault-Overview.
4. Relevante Dateien mit `rg` finden.
5. Nur nötige Dateien/Zeilen lesen.
6. Worktree-Schutz: keine fremden Änderungen überschreiben.
7. Erst dann planen oder editieren.

## Phonbot Loadout

- Pfad: `C:\Users\pc105\.openclaw\workspace\voice-agent-saas`.
- Erst lesen: `CLAUDE.md`, `package.json`, passende Vault-Module.
- Check-Kommandos: `pnpm check`, bei Bedarf `pnpm --filter @vas/api exec vitest run`, `pnpm --filter @vas/api build`, `pnpm --filter @vas/web build`.
- Design-Regeln: Orange, Dark Glass, Chipy, API über `apps/web/src/lib/api.ts`, keine React-Router-Annahme.
- Backend-Regeln: ESM `.js`, `org_id` aus JWT, `pool` Guard, externe fetches mit Timeout, keine silent catches.

## Socibot Loadout

- Pfad: `C:\Users\pc105\Desktop\Social media Bot`.
- Erst lesen: Vault [[Socibot/Overview|Socibot Overview]], [[Socibot/Architecture]], [[Socibot/DoD]], dann README/Projektregeln im Code.
- Vor Push/Commit: ahead/dirty Zustand beachten.
- Tests laut Vault zuletzt stark ausgebaut; aktuelle Test-Kommandos im Code prüfen, nicht aus Erinnerung raten.

## Evidence Contract

Code-Befunde brauchen:

- Datei und Zeile.
- Aktueller Branch/Git-Status, falls relevant.
- Ob die Datei uncommitted geändert ist.
- Warum es ein echter Bug oder ein echtes Risiko ist.
- Fix-Risiko und Testplan.

## Team-Verhalten bei Unsicherheit

- Debugger sagt: "Nicht genug Beleg", statt Fehler zu erfinden.
- Engineer sagt: "Blast-Radius unklar", statt großen Patch zu starten.
- Business-Coach sagt: "Metrik fehlt", statt Feature schönzureden.
- Security sagt: "Datenfluss unbekannt", statt Compliance zu behaupten.
