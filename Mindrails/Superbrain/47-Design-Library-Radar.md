---
title: Design Library Radar
type: radar
status: active
tags:
  - mindrails
  - superbrain
  - design
  - github
parent: "[[Mindrails/Superbrain/48-Design-Skill-Squad|Design Skill Squad]]"
created: 2026-05-05
updated: 2026-05-05
last_checked: 2026-05-05
---

# Design Library Radar

Dieses Radar sammelt hochwertige GitHub-/Open-Source-Design-Ressourcen. Es ist keine Einkaufsliste. Jede Ressource muss durch [[Mindrails/Superbrain/46-GitHub-Skill-Scout|GitHub Skill Scout]] gehen.

## Aktuelle Kandidaten

| Ressource | Warum interessant | Vorsicht |
|---|---|---|
| shadcn/ui - https://github.com/shadcn-ui/ui | Sehr populär, copy-paste Komponenten, Tailwind/Radix, starke DX. | Nicht 1:1 Look übernehmen; Phonbot-DNA muss bleiben. |
| Radix Primitives - https://github.com/radix-ui/primitives | Accessible unstyled primitives für robuste Dialoge, Selects, Menus. | Low-level; Design muss selbst gebaut werden. |
| Tailwind CSS / Headless UI - https://github.com/tailwindlabs | Passt grundsätzlich zu Phonbot/Tailwind; Headless UI für A11y primitives. | Phonbot nutzt Tailwind 4; Integration immer version-sicher prüfen. |
| Magic UI - https://github.com/magicuidesign/magicui | Gute Motion-/Marketing-Komponenten, viele moderne Effekte. | Hohe AI-Slop-Gefahr, Motion-Budget strikt prüfen. |
| Mantine - https://github.com/mantinedev/mantine | Vollständige React-Component-Library mit vielen Hooks/Komponenten. | Kann visuell/stilistisch schwerer in Phonbot passen; Dependency-Bloat prüfen. |
| HeroUI - https://github.com/heroui-inc/heroui | Moderne React UI Library, vormals NextUI. | Ästhetik kann stark fremd wirken; nur Patterns scouten. |
| Chakra UI - https://github.com/chakra-ui/chakra-ui | Reife accessible React UI Library. | CSS-in-JS/Designsystem-Fit für Phonbot vorsichtig prüfen. |
| Lucide Icons - https://github.com/lucide-icons/lucide | Konsistente SVG-Icon-Familie, gut für UI-Icons. | Icon-Stil muss mit bestehenden PhonbotIcons harmonieren. |
| Motion - https://github.com/motiondivision/motion | Hochwertige Animationen für React/Web. | Nur nutzen, wenn Motion echten UX-Nutzen hat und Bundle/Perf passt. |

## Bewertungsnotizen

- shadcn/ui hatte beim Check 2026-05-05 ca. 113k GitHub Stars, MIT, aktuelle Releases.
- Magic UI hatte beim Check 2026-05-05 ca. 20k+ Stars, MIT, moderne Marketing-Komponenten.
- Mantine lag beim Check bei ca. 31k Stars und vielen Releases.
- Stars sind Momentaufnahme und kein Qualitätsbeweis.

## Phonbot-Nutzungsregel

Externe Libraries liefern höchstens:

- Interaction Pattern.
- Accessible Primitive.
- Animation-Idee.
- Component API Inspiration.
- Edge-Case-Idee.

Sie liefern nicht:

- Phonbot-Farben.
- Phonbot-Spacing.
- Phonbot-Mascot-Regeln.
- Phonbot-Tone of Voice.
- fertige Ästhetik.
