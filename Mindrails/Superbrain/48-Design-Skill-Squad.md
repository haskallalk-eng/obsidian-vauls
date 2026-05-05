---
title: Design Skill Squad
type: agent-group
status: active
tags:
  - mindrails
  - superbrain
  - design
  - skills
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
---

# Design Skill Squad

Diese Squad verbindet unsere vorhandenen Design-Skills mit externen, gut geprüften GitHub-Design-/UI-Ressourcen. Sie soll Phonbot schöner, klarer und professioneller machen, ohne das bestehende Design zu verwässern.

## Interne Skill-Agenten

| Agent | Skill-Basis | Aufgabe |
|---|---|---|
| [[Mindrails/Superbrain/43-Phonbot-Chipy-Design-Agent|Phonbot Chipy Design Agent]] | `chipy-design` | Phonbot-DNA verteidigen: Dark Glass, Orange->Cyan, Chipy, unified nav/footer. |
| [[Mindrails/Superbrain/44-Design-Review-Skill-Agent|Design Review Skill Agent]] | `design-review`, `ui-ux-pro-max` | UI kritisch polieren: Hierarchie, Spacing, Typography, A11y, responsive. |
| [[Mindrails/Superbrain/45-Design-Asset-Skill-Agent|Design Asset Skill Agent]] | `color-palette`, `icon-set-generator`, `favicon-gen`, `ai-image-generator` | Farben, Icons, Favicons, OG-/Hero-Assets sauber erzeugen. |
| [[Mindrails/Superbrain/46-GitHub-Skill-Scout|GitHub Skill Scout]] | `skill-installer`, `skill-creator`, GitHub-Recherche | Externe Skills/Repos finden, bewerten, nur nach Gate übernehmen. |
| [[Mindrails/Superbrain/47-Design-Library-Radar|Design Library Radar]] | GitHub/Open-Source-Recherche | Hoch bewertete UI-Libraries und Komponenten-Ideen kuratieren. |

## Pflichtregel

Phonbot gewinnt immer gegen fremde Library-Ästhetik. Externe Komponenten dürfen Ideen liefern, aber die finale UI muss aussehen wie Phonbot, nicht wie ein Shadcn-/Magic-UI-Demo-Klon.

## Wann laden?

- UI/UX für Phonbot: Chipy Design Agent + UX/UI-Agent + Frontend-Agent.
- Landingpage/SEO-Seite: Chipy Design Agent + SEO Squad + Content Intent.
- Neue Designrichtung für anderes Mindrails-Produkt: Design Review Skill Agent + Design Library Radar, nicht Chipy.
- Icons/Favicons/Assets: Design Asset Skill Agent.
- "Guck GitHub nach guten Skills/Libs": GitHub Skill Scout + Design Library Radar.

## Qualitätsgate

Eine externe Ressource ist nur nutzbar, wenn:

- Sie aktiv gepflegt ist.
- Lizenz kompatibel ist.
- Beispiele/Docs gut sind.
- Sie zu unserem Stack passt.
- Sie keine große Dependency-/Bundle-/A11y-Schuld reinzieht.
- Sie unser Design verbessert, nicht ersetzt.
