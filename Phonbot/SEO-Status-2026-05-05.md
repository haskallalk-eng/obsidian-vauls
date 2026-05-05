---
title: Phonbot SEO Status 2026-05-05
type: status
tags:
  - phonbot
  - seo
  - superhirn
  - status
created: 2026-05-05
source: Mindrails/Superbrain/42-SEO-Final-Evaluation-Protocol
---

# Phonbot SEO Status 2026-05-05

Bewertung nach [[Mindrails/Superbrain/42-SEO-Final-Evaluation-Protocol|SEO Final Evaluation Protocol]].

## Kurzurteil

Phonbot ist technisch stark crawlbar und fuer AI-/LLM-Discovery deutlich sauberer als vor der Korrektur. Die groesste konkrete Drift zwischen Website, Pricing, `llms.txt`, `llms-full.txt` und `ai.txt` wurde behoben und in `scripts/seo-audit.mjs` als Regression-Gate abgesichert.

Aktueller Arbeits-Score: 7.5/10.

Score-Cap bleibt: Ohne echte Google Search Console/Bing-/Conversion-Daten maximal 8/10, weil Indexierung, CTR und Ranking-Wirkung nicht beweisbar sind.

## Behobene Drift

- Nummer-Plan ist jetzt einheitlich: 8,99 EUR/Monat, 100 Gesamt-Freiminuten einmalig, danach 0,22 EUR/Min.
- Starter/Professional/Agency bleiben monatliche Kontingente: 360 / 1.000 / 2.400 Min pro Monat.
- `ai.txt` nennt wieder die richtige Legal-Entity: Hans Ulrich Waier (Einzelunternehmer), Berlin.
- Jahresrabatt ist nicht mehr pauschal 20 %, sondern ca. 15-18 % je nach Plan.
- `llms.txt` nutzt Stand 5. Mai 2026 statt April 2026.

## Neue Schutzregel

`pnpm seo:audit` prueft jetzt zusaetzlich:

- Legal-Entity in Root-JSON-LD, `llms.txt`, `llms-full.txt`, `ai.txt`.
- Nummer-Plan-Wahrheit mit 100 einmaligen Gesamt-Freiminuten.
- Verbotene alte Muster: April-2026-Preisstand, 70 Min/Monat fuer Nummer, `haftungsbeschraenkt`, pauschale 20-%-Jahresrabatt-Copy.
- Basispreise/Minuten fuer Starter, Professional und Agency in den LLM-Dateien.

## Verifikation

- `pnpm --filter @vas/web build`: bestanden.
- `pnpm seo:audit`: bestanden, 0 warnings, 0 failures.
- `pnpm --dir apps/web typecheck`: bestanden.
- `git diff --check`: bestanden; nur CRLF-Warnungen.

## Offene SEO-Grenzen

- Google/Bing-Indexstatus ist ohne Search Console/Bing Webmaster nicht beweisbar.
- Core Web Vitals wurden in dieser Runde nicht als Feld- oder Lighthouse-Daten gemessen.
- Ranking- und Conversion-Wirkung brauchen Zielqueries, Baseline und Revisit-Datum.

## Naechster Messplan

- URL-Gruppe: `/`, `/branchen/`, `/friseur/`, `/handwerker/`, `/reinigung/`, `/restaurant/`, `/autowerkstatt/`, `/selbststaendig/`.
- Zielqueries: "ki telefonassistent", "ki telefonassistent friseur", "telefonassistent handwerker", "telefonservice friseursalon", "ki anrufannahme".
- Baseline: Search Console Indexstatus, Impressions, CTR, Position; Bing Indexstatus; organische Demo-/Signup-Conversions.
- Revisit: 14 Tage nach Deploy und Sitemap-Resubmission.
- Erfolg: wichtige URLs indexiert, erste passende Impressions, keine AI-/Pricing-Drift im Audit, mindestens ein organischer Demo-/Signup-Pfad messbar.
