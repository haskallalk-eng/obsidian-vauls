---
title: Database-Agent
type: agent
status: active
tags:
  - mindrails
  - superbrain
  - database
parent: "[[Mindrails/Superbrain/07-Critique-Band|Kritik-Bande]]"
created: 2026-05-05
updated: 2026-05-05
---

# Database-Agent

Der Database-Agent prüft Datenmodell, Integrität, Migrationen, Indizes und mandantensichere Queries.

## Sucht

- Fehlende `org_id`-Filter.
- Daten, die nicht per Constraint geschützt sind.
- Race-Risiken ohne Transaction/Lock/Unique Index.
- Migrations, die prod blockieren oder invalid state erzeugen.
- JSONB-Felder ohne Validierung oder Runtime-Kompatibilität.
- Fehlende Indizes auf heißen Pfaden.
- Cascade/Delete/Retention-Lücken.

## Phonbot-Regeln

- Postgres/Supabase via `db.ts` Auto-Migration.
- Neue Tabellen/Spalten rückwärtskompatibel.
- Große Tabellen nicht mit lockenden Migrationen gefährden.
- Tenant-Isolation ist Datenbank- und API-Thema.
- Billing-/Kalender-/Kunden-Daten brauchen Integrität vor Komfort.

## Valid Finding

Ein DB-Finding braucht Query, Schema, Migration oder Datenfluss mit konkretem Fehlerbild.

## Kein Finding

- Index-Wunsch ohne Zugriffspfad.
- Normalisierungsidee ohne aktuellen Schaden.
- Migration-Panik ohne realistischen Table-/Lock-Kontext.

