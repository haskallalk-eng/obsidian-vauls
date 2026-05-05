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
| [[Mindrails/Superbrain/42-SEO-Final-Evaluation-Protocol|SEO Final Evaluation Protocol]] | Endscore, Score-Caps, Beleg-Hierarchie, finale SEO-Entscheidung. |

## SEO-Review-Reihenfolge

1. Crawl & Index: Kann eine Suchmaschine die Seite überhaupt finden und darf sie sie indexieren?
2. Content & Intent: Bedient die Seite eine echte Suchintention besser als Alternativen?
3. Structured Data: Versteht die Suchmaschine Entitäten, Angebote, FAQs und Breadcrumbs?
4. Performance: Ist die Seite schnell genug, besonders mobil?
5. Programmatic: Skaliert das Template ohne Thin-/Duplicate-Content?
6. Local: Passt die Seite zu lokaler Kaufintention?
7. AI Search: Ist der Inhalt für AI Overviews, ChatGPT/Perplexity und LLM-Crawler klar?
8. Measurement: Wie wird Erfolg oder Fehler bewiesen?
9. Final Evaluation: Welche Bewertung ist nach Belegen erlaubt, und welche Score-Caps greifen?

## Finale SEO-Bewertung

Eine finale SEO-Aussage darf nie nur aus `pnpm seo:audit` oder einer alten Vault-Notiz kommen. Die SEO Squad muss unterscheiden:

- crawlbar: Live-URL ist technisch abrufbar und indexierbar.
- indexiert: Suchmaschine hat die URL im Index oder Search Console/Bing bestätigt es.
- rankingfähig: Inhalt, Intent, Links, Performance und SERP-Realität passen.
- messbar: Baseline, Zielquery, URL-Gruppe und Revisit-Datum existieren.

Wenn Preis, Legal-Entity, `llms.txt`, `ai.txt`, JSON-LD oder sichtbarer Content voneinander abweichen, ist das ein Drift-Finding und begrenzt die Endbewertung.

## Recherchemodus

Vor größeren SEO-Entscheidungen wird frisch geprüft:

- Offizielle Google Search Central Docs für Crawl/Index, Structured Data, Helpful Content und Core Web Vitals.
- Search Console/Bing-Daten, wenn Zugriff vorhanden ist.
- Live-SERP und Wettbewerber für die konkrete Query, nicht generische SEO-Meinung.
- Phonbot-Code: `apps/web/public`, `apps/web/index.html`, SEO-Generator-Scripts, `Caddyfile`.
- Phonbot-Vault: [[Phonbot/SEO|Phonbot SEO]], [[Phonbot/Pages|Pages]], [[Phonbot/Pricing|Pricing]].
- AI-Crawler-Doku, wenn `llms.txt`, `ai.txt` oder Robots-Regeln betroffen sind.
- Finale Bewertung: [[Mindrails/Superbrain/42-SEO-Final-Evaluation-Protocol|SEO Final Evaluation Protocol]] anwenden.

## SEO-Experiment-Logik

Jede SEO-Änderung braucht:

- URL oder URL-Gruppe.
- Zielquery oder Suchintention.
- Hypothese.
- Änderung.
- Baseline: Indexstatus, Impressions, CTR, Position, Conversion oder technischer Auditstatus.
- Revisit-Datum.
- Ergebnis: gewonnen, verloren, neutral, unklar.

## Phonbot-Friseur-SEO-Anspruch

Für Friseur-SEO muss die Seite konkret zeigen:

- verpasste Anrufe und Terminverlust,
- Mitarbeiter-/Betriebskalender,
- Stammkunden/Neukunden,
- Rückrufnummer, gewünschte Leistung, Terminwunsch,
- Farbe/Chemie-Allergie-/Vorbehandlungslogik,
- klare DSGVO-/KI-Hinweise,
- einfache Aktivierung ohne Telefonie-Fachwissen.

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
