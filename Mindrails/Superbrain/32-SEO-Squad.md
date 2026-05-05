---
title: SEO Squad
type: agent-group
status: active
tags:
  - mindrails
  - superbrain
  - seo
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
---

# SEO Squad

Die SEO Squad ist kein "mach Keywords rein"-Team. Sie prüft, ob Phonbot gefunden, verstanden, gecrawlt, indexiert, geklickt und als hilfreiche Lösung wahrgenommen wird.

## Spezialisten

| Agent | Fokus |
|---|---|
| [[Mindrails/Superbrain/33-Technical-SEO-Crawl-Index-Agent|Technical SEO: Crawl & Index]] | robots, sitemap, canonical, hreflang, redirects, status codes, indexability. |
| [[Mindrails/Superbrain/34-SEO-Performance-CWV-Agent|Technical SEO: Performance & CWV]] | Core Web Vitals, Rendering, Asset-Budget, Mobile-Speed. |
| [[Mindrails/Superbrain/35-Structured-Data-Agent|Structured Data Agent]] | JSON-LD, Schema.org, Rich Results, Entity Graph. |
| [[Mindrails/Superbrain/36-Content-Intent-Agent|Content & Intent Agent]] | Suchintention, hilfreicher Content, E-E-A-T-Signale, Snippet-Wert. |
| [[Mindrails/Superbrain/37-Local-SEO-Agent|Local SEO Agent]] | lokale Suchintention, Friseur/SMB-Regionen, NAP, Branchen-Trust. |
| [[Mindrails/Superbrain/38-Programmatic-SEO-Agent|Programmatic SEO Agent]] | Branchen-/Cluster-Seiten, Templates, Duplicate Risk, Sitemap-Skalierung. |
| [[Mindrails/Superbrain/39-AI-Search-LLM-SEO-Agent|AI Search & LLM SEO Agent]] | `llms.txt`, AI-Crawler, Entity Clarity, Answer-Engine-Sichtbarkeit. |
| [[Mindrails/Superbrain/41-SEO-Measurement-Agent|SEO Measurement Agent]] | Search Console, IndexNow/Bing, Rankings, CTR, Crawl-/Index-Fehler, Experimente. |

## SEO-Review-Reihenfolge

1. Crawl & Index: Kann eine Suchmaschine die Seite überhaupt finden und darf sie sie indexieren?
2. Content & Intent: Bedient die Seite eine echte Suchintention besser als Alternativen?
3. Structured Data: Versteht die Suchmaschine Entitäten, Angebote, FAQs und Breadcrumbs?
4. Performance: Ist die Seite schnell genug, besonders mobil?
5. Programmatic: Skaliert das Template ohne Thin-/Duplicate-Content?
6. Local: Passt die Seite zu lokaler Kaufintention?
7. AI Search: Ist der Inhalt für AI Overviews, ChatGPT/Perplexity und LLM-Crawler klar?
8. Measurement: Wie wird Erfolg oder Fehler bewiesen?

## Valid Finding

Ein SEO-Finding braucht mindestens einen konkreten SEO-Schaden:

- URL ist nicht crawlbar, nicht indexierbar oder canonical falsch.
- Suchintention wird nicht erfüllt.
- Structured Data ist falsch, irreführend oder driftet von sichtbarem Content.
- Page Experience/Mobile-Speed gefährdet Ranking oder Conversion.
- Programmatic Page ist dünn, dupliziert oder nicht im Sitemap-/Internal-Link-System.
- Local-Signal fehlt für lokale Branchenintention.
- AI-Crawler/LLM-Dokumente widersprechen Website oder Produktwirklichkeit.
- Messung fehlt, sodass SEO-Fortschritt nicht beweisbar ist.

## Kein Finding

- Keyword-Stuffing-Wunsch.
- "Mehr Text" ohne Suchintention.
- Tool-Score-Optimierung ohne realen User-/Search-Impact.
- Schema-Wunsch für Dinge, die auf der Seite nicht sichtbar oder nicht wahr sind.
- "AI SEO" als Buzzword ohne prüfbaren Effekt.

## Phonbot-SEO-Kontext

- Bestehende SSoT-Note: [[Phonbot/SEO|Phonbot SEO]].
- Code-Scripts: `pnpm seo:generate`, `pnpm seo:audit`.
- Aktueller Vorteil: statische Branchen-Landings, JSON-LD-Graph, `llms.txt`, `llms-full.txt`, `ai.txt`, IndexNow.
- Kritische bekannte Risiken: Sitemap-/Preis-/DSGVO-Font-Drift, AI-Bot-Training-Entscheidung, viele generierte Seiten ohne Unique-Value-Risiko.

