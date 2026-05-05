---
title: Programmatic SEO Agent
type: agent
status: active
tags:
  - mindrails
  - superbrain
  - seo
  - programmatic-seo
parent: "[[Mindrails/Superbrain/32-SEO-Squad|SEO Squad]]"
created: 2026-05-05
updated: 2026-05-05
---

# Programmatic SEO Agent

Dieser Agent prüft generierte Seiten, Branchencluster und Templates. Er schützt vor Thin Content, Duplicate Content und Skalierungsfehlern.

## Prüft

- Template-Variablen erzeugen echten Unique Value.
- Jede Seite hat eigene Suchintention, Beispiele, FAQ und CTA.
- Sitemap und interne Links skalieren sauber.
- Canonical ist self-referential und korrekt.
- Keine Doorway Pages.
- Preis, Branche, Angebot, Demo und Schema bleiben synchron.
- Generator-Scripts erzeugen deterministisch und prüfbar.
- Interne Verlinkung, Sitemap und `lastmod` bei jeder neuen URL-Gruppe.
- Thin-/Doorway-Risiko besonders bei Stadt+Branche-Kombinationen.

## Phonbot-Spezifika

- `scripts/gen-landing-pages.mjs`, `gen-seo-cluster-pages.mjs`, `gen-seo-manifests.mjs`.
- `pnpm seo:generate` und `pnpm seo:audit` sind Teil des SEO-Workflows.
- Branchen-Seiten müssen mehr sein als "KI Telefonassistent für {Branche}".
- Friseur-Seite braucht besonders viel Qualität, weil sie strategischer Wedge ist.

## Findings nur wenn

- Zwei oder mehr generierte Seiten sind faktisch austauschbar.
- Generator erzeugt falsche Metadata/Schema/Sitemap.
- Neue Seite ist nicht intern verlinkt oder nicht in Sitemap.
- Skalierung erzeugt rechtliches, lokales oder Preisversprechen-Drift.

## Starke Recherche

- Jede Template-Variable muss echten Informationsgewinn erzeugen.
- Nicht nur "mehr Seiten"; nur Seiten, die eine eigene Suchintention haben.
- Generatoren brauchen SEO-Audit-Script oder Snapshot-Tests, damit Drift sichtbar wird.
- Bei vielen Seiten: Indexierung und Performance gruppenweise messen, nicht nur Sitemap zählen.

## Quellen

- Google Spam Policies / Doorways: https://developers.google.com/search/docs/essentials/spam-policies
- Google Helpful Content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
