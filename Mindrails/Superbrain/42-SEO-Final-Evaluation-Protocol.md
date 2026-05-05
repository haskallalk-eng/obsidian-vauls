---
title: SEO Final Evaluation Protocol
type: protocol
status: active
tags:
  - mindrails
  - superbrain
  - seo
  - evaluation
parent: "[[Mindrails/Superbrain/32-SEO-Squad|SEO Squad]]"
created: 2026-05-05
updated: 2026-05-05
---

# SEO Final Evaluation Protocol

Dieses Protokoll macht aus vielen SEO-Checks eine belastbare Endbewertung. Es verhindert, dass "Audit gruen" mit "SEO ist fertig" verwechselt wird.

## Wahrheits-Hierarchie

Bei Widerspruechen gilt diese Reihenfolge:

1. Live-Website: Statuscode, Header, HTML, robots, sitemap, canonical, sichtbarer Content.
2. Produkt-Code und Generatoren: `apps/web`, `scripts/*seo*`, `Caddyfile`, Build-/Deploy-Output.
3. Messdaten: Google Search Console, Bing Webmaster Tools, IndexNow, Analytics, Conversion-Daten.
4. Offizielle Quellen: Google Search Central, Bing, schema.org, Anbieter-Dokumentation.
5. Obsidian-Notizen: Kontext und Historie, aber nicht automatisch aktuelle Wahrheit.
6. Annahmen: immer als Annahme markieren.

## Pflichtdimensionen

| Dimension | Muss beantwortet werden |
|---|---|
| Crawl & Index | Sind wichtige URLs live erreichbar, crawlbar, canonical korrekt und in der Sitemap? |
| Index Realitaet | Sind wichtige URLs in Google/Bing sichtbar oder wenigstens zur Indexierung eingereicht? |
| Content & Intent | Bedient jede Seite eine konkrete Suchintention besser als generische SaaS-Copy? |
| Structured Data | Stimmen JSON-LD, sichtbarer Content, Preise, Legal-Entity und Angebote ueberein? |
| Programmatic SEO | Haben generierte Seiten echten Unique Value und keine Doorway-/Duplicate-Risiken? |
| Local SEO | Gibt es lokale Trust-Signale ohne fake-local Versprechen? |
| AI Search / LLM SEO | Stimmen `llms.txt`, `llms-full.txt`, `ai.txt`, robots und Website-Wahrheit ueberein? |
| Performance / CWV | Sind mobile LCP, INP, CLS und Asset-Budget plausibel oder gemessen? |
| Measurement | Gibt es Baseline, Zielqueries, URLs, Revisit-Datum und Business-Metrik? |
| Conversion | Fuehrt organischer Traffic zu Demo, Signup, Nummer, Call oder Beratung? |

## Score-Regeln

- 9-10: technisch sauber, inhaltlich stark, messbar, keine Drift, erste reale Such-/Conversion-Daten vorhanden.
- 7-8: gute SEO-Basis, kleine Drift-/Measurement-Luecken, noch nicht voll bewiesen.
- 5-6: nutzbar, aber wichtige Signale fehlen oder widersprechen sich.
- 3-4: technische oder inhaltliche Risiken blockieren Wachstum.
- 1-2: wichtige Seiten sind nicht crawlbar, falsch, irrefuehrend oder nicht messbar.

## Score-Caps

Diese Probleme begrenzen die Endbewertung, auch wenn andere Bereiche gut aussehen:

- Wichtige URLs `noindex`, blockiert oder nicht live erreichbar: maximal 4/10.
- Preise, Legal-Entity oder Produktversprechen widersprechen sich: maximal 6/10.
- `llms.txt`/`ai.txt` widersprechen Website oder Pricing: maximal 7/10.
- Keine Search-Console-/Bing-/Indexdaten verfuegbar: maximal 8/10.
- Programmatic-Seiten ohne Unique Value oder mit Doorway-Risiko: maximal 6/10.
- Keine Conversion-Messung fuer SEO-Landings: maximal 8/10.

## Finale Ausgabe

Jede finale SEO-Bewertung muss enthalten:

```md
## Finale SEO-Bewertung

- Gesamt-Score:
- Confidence:
- Nicht live verifiziert:
- Groesster Hebel:
- Groesstes Risiko:

| Dimension | Score | Status | Beleg | Naechste Aktion |
|---|---:|---|---|---|

## Findings

1. [Prioritaet] Problem - konkreter SEO-Schaden - Beleg - Fix.

## Messplan

- URL-Gruppe:
- Zielquery / Suchintention:
- Baseline:
- Revisit-Datum:
- Erfolgskriterium:
```

## Phonbot-Pflichtchecks

Vor einer finalen Phonbot-SEO-Aussage:

- `pnpm seo:audit` ausfuehren oder als nicht ausgefuehrt markieren.
- Live pruefen: `/`, `/branchen/`, wichtigste Branchen-URLs, `/robots.txt`, `/sitemap.xml`, `/llms.txt`, `/ai.txt`.
- `Phonbot/SEO` gegen Live/Code pruefen und als Snapshot markieren, falls veraltet.
- Preise gegen Billing/Plan-Quelle, JSON-LD, sichtbare UI und LLM-Dateien vergleichen.
- Betreiber-/Legal-Entity gegen Impressum, JSON-LD, `ai.txt`, `llms.txt` vergleichen.
- Google/Bing-Indexstatus nicht aus technischen Checks ableiten. Ohne GSC/Bing nur "crawlbar", nicht "indexiert" behaupten.

## Lernregel

Jede uebersehene SEO-Drift wird in die passende Spezialrolle und in `scripts/seo-audit.mjs` aufgenommen, wenn sie automatisch pruefbar ist.
