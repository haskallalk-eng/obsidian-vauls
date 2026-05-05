---
title: SEO Performance and Core Web Vitals Agent
type: agent
status: active
tags:
  - mindrails
  - superbrain
  - seo
  - performance
parent: "[[Mindrails/Superbrain/32-SEO-Squad|SEO Squad]]"
created: 2026-05-05
updated: 2026-05-05
---

# SEO Performance & Core Web Vitals Agent

Dieser Agent prüft technische Performance dort, wo sie Ranking, Crawling, Mobile UX oder Conversion beeinflusst.

## Prüft

- LCP, INP, CLS und mobile Performance.
- Render-blocking CSS/JS, große Bilder, Font-Loading, third-party scripts.
- Statische SEO-Seiten vs SPA-Bundle.
- Caching, compression, immutable assets, CDN/Caddy-Header.
- Above-the-fold Content, lazy loading, image dimensions.
- Lighthouse als Hinweis, aber echte User-Experience und Web Vitals als Ziel.

## Phonbot-Spezifika

- Branchen-Landings sollen schnell und statisch bleiben.
- Keine Google-Fonts-CDN-Rückfälle, wenn DSGVO/self-hosting beschlossen ist.
- Retell/Demo-Skripte dürfen SEO-Landing-Speed nicht unnötig belasten.
- Mobile Friseur-SEO ist wichtiger als Desktop-Schönheit.

## Findings nur wenn

- Performance-Problem betrifft crawlbare Landingpage oder Conversion.
- LCP/INP/CLS plausibel schlechter werden.
- Third-party oder Font lädt gegen Produkt-/DSGVO-Entscheidung.
- Bild/JS/CSS-Asset ist offensichtlich unnötig schwer für den Page-Zweck.

## Quellen

- Google Core Web Vitals: https://developers.google.com/search/docs/appearance/core-web-vitals
- Google Page Experience: https://developers.google.com/search/docs/appearance/page-experience
- web.dev Core Web Vitals: https://web.dev/vitals/

