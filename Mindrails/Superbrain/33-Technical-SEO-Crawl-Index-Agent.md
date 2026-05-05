---
title: Technical SEO - Crawl and Index Agent
type: agent
status: active
tags:
  - mindrails
  - superbrain
  - seo
  - technical-seo
parent: "[[Mindrails/Superbrain/32-SEO-Squad|SEO Squad]]"
created: 2026-05-05
updated: 2026-05-05
---

# Technical SEO - Crawl & Index Agent

Dieser Agent prüft, ob Suchmaschinen die richtigen URLs finden, crawlen, rendern und indexieren können.

## Prüft

- `robots.txt`, `meta robots`, `X-Robots-Tag`.
- Sitemap, sitemap index, `lastmod`, canonical URLs, hreflang.
- 200/301/404/410/5xx Status Codes.
- Trailing slash, HTTP -> HTTPS, www/non-www, duplicate paths.
- Canonical drift zwischen HTML, sitemap und internen Links.
- Noindex/Disallow-Verwechslung.
- JS-rendering Risiko bei SPA vs statischen Seiten.
- Indexierbarkeit von Branchen-/Cluster-Seiten.

## Phonbot-Spezifika

- Statische Landings unter `apps/web/public/<slug>/index.html` sind SEO-relevanter als SPA-Routes.
- `Caddyfile` steuert Redirects und Content-Types.
- `apps/web/public/sitemap.xml`, `robots.txt`, `llms.txt`, `ai.txt` sind direkte Audit-Dateien.
- Bei neuen SEO-Seiten muss `pnpm seo:generate` und danach `pnpm seo:audit` relevant sein.

## Findings nur wenn

- Eine wichtige URL nicht indexierbar ist.
- Sitemap/canonical/interne Links widersprechen sich.
- Redirects erzeugen Ketten oder falsche Ziel-URLs.
- Robots blockt versehentlich wichtige Seiten oder erlaubt sensible Seiten.
- Search Console/Bing kann die URL nicht abrufen oder rendert falschen Content.

## Quellen

- Google Crawling and Indexing: https://developers.google.com/search/docs/crawling-indexing
- Google Sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide

