---
module: Frontend-Agent-Builder-Icons
scope: "Phonbot custom icons in agent builder"
files:
  - apps/web/src/ui/PhonbotIcons.tsx
  - apps/web/src/ui/agent-builder/shared.tsx
  - apps/web/src/ui/agent-builder/KnowledgeTab.tsx
commit: 8a57a08
tags: [frontend, design-system, icons, agent-builder]
updated: 2026-04-23
---

# Frontend-Agent-Builder-Icons

## Änderung

Das Symbol neben `Wissen` wurde ersetzt:

- vorher: Brain/IconBrain
- jetzt: hauseigenes `IconKnowledge`

Das neue Symbol zeigt mehrere dezente Bücher übereinander, mit kleinem Lesezeichen auf dem oberen Buch.

## Wo verwendet

- Agent-Builder Tab `Wissen`
- SectionCard `Wissensquellen`

## Dateien

- `apps/web/src/ui/PhonbotIcons.tsx`
  - `IconKnowledge` neu gezeichnet als Bücherstapel mit Bookmark
- `apps/web/src/ui/agent-builder/shared.tsx`
  - Wissen-Tab nutzt `IconKnowledge`
  - Re-export von `IconKnowledge`
- `apps/web/src/ui/agent-builder/KnowledgeTab.tsx`
  - Section `Wissensquellen` nutzt `IconKnowledge`

## Verifikation

- `pnpm.cmd --filter @vas/web typecheck` grün.
- Commit `8a57a08` live deployt.
- Healthcheck grün.
