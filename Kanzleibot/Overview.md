---
tags:
  - project
  - kanzleibot
  - mindrails
status: active
parent: "[[Mindrails/Overview|Mindrails]]"
created: 2026-04-21
code_path: ~/.openclaw/workspace/kanzleibot
scope: DE-Kanzleien (Rechtsanwalts-SaaS)
compliance: DSGVO + BRAO + §43a Verschwiegenheit
region: EU-only
---

# Kanzleibot — Rechtsanwalts-SaaS

> Ein Produkt von [[Mindrails/Overview|Mindrails]].

> [!info] TL;DR
> SaaS für deutsche Anwaltskanzleien. ReFa-Augmentation (Rechtsanwaltsfachangestellte): KI-gestützte Mandats-Bearbeitung, Dokumenten-Workflows, Fristen-Management.

## Was ist es

SaaS-Plattform, die den klassischen ReFa-Workflow in Kanzleien augmentiert — nicht ersetzt. Fokus: Dokumenten-Automatisierung, Mandats-Onboarding, Fristen- und Akten-Management.

## Wo liegt der Code

`~/.openclaw/workspace/kanzleibot`

## Compliance-Posture

> [!warning] Rechtsanwalts-Geheimhaltung = non-negotiable
> - **§ 43a BRAO:** Anwalts-Verschwiegenheit absolute Pflicht
> - **DSGVO Art. 9:** besondere Kategorien (Gesundheits-/Straf-/Religions-Daten in Mandaten)
> - **EU-only Hosting** — keine US-Transfers ohne SCCs + TIA
> - **Pseudonymisierung Pflicht** bei LLM-Verarbeitung von Mandats-Inhalten (Namen → Tokens vor Upload)

## Zielgruppe

- Einzel- und Kleinkanzleien (2–10 Anwälte)
- Mid-Size-Kanzleien (10–50)
- **Nicht:** Großkanzleien mit eigenem Legal-Tech-Stack

## Stack (tentativ — verifizieren!)

_Noch nicht audited — beim ersten Deep-Dive im Code prüfen._

| Layer | Wahrscheinlich |
|-------|----------------|
| API | TBD |
| Web | TBD |
| DB | Supabase/Postgres (EU-Region) |
| LLM | TBD (OpenAI EU / Mistral / Claude über EU-Endpoint?) |
| Telefonie | ggf. Phonbot-Integration für Kanzlei-Telefonie |

## Offene Themen

- [ ] Erster Code-Audit (module-by-module, code-basiert)
- [ ] Modul-Notes anlegen unter `[[Kanzleibot/modules/]]`
- [ ] Pseudonymisierungs-Pipeline dokumentieren
- [ ] DSGVO-AVV-Liste (Sub-Processoren) aufsetzen
- [ ] BRAO § 43a Compliance-Check mit Anwalt abstimmen

## Status

Frühe Phase. Kein öffentliches Produkt. Codebase noch nicht audited.

## Verwandt

- [[Mindrails/Overview|Mindrails]] — Dachfirma
- [[README]] — Vault-Index
