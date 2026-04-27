---
title: Phonbot — SEO Status
tags: [phonbot, seo, marketing, status]
created: 2026-04-21
status: code-basiert
---

# Phonbot — SEO Status

> Ist-Zustand basierend auf Code (`apps/web/`, `Caddyfile`). Jede Aussage mit Datei-Referenz.

## Executive Summary

Phonbot hat ein **sehr weit entwickeltes Technical-SEO-Setup** — über dem, was man in diesem Produkt-Reifegrad erwarten würde. Schwerpunkte: deutschsprachige Long-Tail (Branchen × Funktion), AI/LLM-Discovery-Optimierung (`llms.txt`-Standard, explizite Bot-Allowlist), reiche strukturierte Daten (12-teiliger JSON-LD-Graph).

**Score subjektiv:** ~8,5/10. Zwei DSGVO-relevante Inkonsistenzen + veraltete Sitemap-Daten = die Lücken.

## 1. Technical SEO

### Robots & Sitemap
- `apps/web/public/robots.txt` — Allowlist für GPTBot, OAI-SearchBot, ChatGPT-User, CCBot, anthropic-ai, ClaudeBot, PerplexityBot, Perplexity-User, Google-Extended, Applebot-Extended. Disallows `/dashboard`, `/admin`, `/onboarding`, `/api/`.
- `apps/web/public/sitemap.xml` — 8+ URLs (Home, 6 Branchen-Landings, Legal-Seiten) mit `lastmod: 2026-04-18`, `changefreq`, `priority`, `xhtml:alternate hreflang`, `image:image`. **⚠ Lastmod-Drift:** wird nicht automatisch regeneriert.
- `apps/web/public/ai.txt` — AI-Training-Policy (llmstxt.org-Standard).
- IndexNow-Key: `.indexnow-key` (Repo-Root) + `apps/web/public/0973a7e744015672cf1dbd9408bb83254a7a532fc480ef96.txt` — für Bing/Yandex Push-Indexing.

### URL-Hygiene (Caddyfile:64-67)
- 301-Redirects `/friseur` → `/friseur/` (Trailing-Slash-Kanonisierung) für alle 6 Branchen-Slugs.
- `@textfiles`-Matcher erzwingt `Content-Type: text/plain` für `llms.txt`, `llms-full.txt`, `ai.txt`, `robots.txt`, `humans.txt` (Caddyfile:42-50).
- `manifest.webmanifest` mit korrektem Content-Type (Lighthouse) — Caddyfile:56.

### Security-Headers (Caddyfile:5-20)
Vollständig: CSP, HSTS (1 Jahr), X-Content-Type-Options, X-Frame-Options SAMEORIGIN, Referrer-Policy, Permissions-Policy (`microphone=(self)`). `-Server` Header stripped.

## 2. On-Page (apps/web/index.html)

### Meta-Tags
- `<title>` mit Keyword-Long-Tail: *„KI-Telefonassistent 24/7 auf Deutsch · DSGVO-konform | Phonbot"* (index.html:12).
- `<meta description>`: 155 Zeichen, enthält Zielbranchen + USP (index.html:13).
- `<meta keywords>`: 10 Long-Tails (index.html:14). **Hinweis:** Google ignoriert `keywords` seit 2009 — harmlos, aber leer.
- `<meta robots>`: `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1`.
- `<link rel="canonical" href="https://phonbot.de/">`.
- `hreflang`: `de`, `de-DE`, `x-default` — alle auf Root (index.html:18-20).

### Open Graph + Twitter (index.html:27-44)
Vollständig: `og:type website`, `og:locale de_DE`, `og:site_name`, `og:url`, `og:title`, `og:description`, `og:image` (1200×630 PNG, mit `:alt`). Twitter-Card: `summary_large_image`. PWA-Manifest, Apple-Touch-Icon, Theme-Color.

### AI/LLM-Discovery (index.html:22-24)
- `<link rel="alternate" type="text/markdown" href="/llms.txt">` — Concise-LLM-Dokument.
- `<link rel="alternate" type="text/markdown" href="/llms-full.txt">` — Full-LLM-Dokument.
- Folgt dem **llmstxt.org-Standard** — noch selten im deutschen SaaS-Markt, SEO-Vorteil für AI-Overview / Perplexity / ChatGPT-Browse.

## 3. Structured Data (JSON-LD @graph, index.html:63-277)

12-teiliger `@graph` in einem einzigen `application/ld+json`-Script:

| # | @type | Zweck |
|---|---|---|
| 1 | `Organization` | Phonbot + `parentOrganization: Mindrails UG` (Berlin, Scharnhorststr. 8) |
| 2 | `LocalBusiness` | Adresse, Telefon, Öffnungszeiten Mo-Fr 9-18, priceRange €€ |
| 3 | `SoftwareApplication` | 5 Offers (Free / Nummer 8,99 € / Starter 79 € / Pro 179 € / Agency 349 €) |
| 4 | `WebSite` | `de-DE`, publisher → Organization |
| 5 | `FAQPage` | **9 Q&A-Paare** (technisches Wissen, Rufweiterleitung, Tickets, Kalender, DSGVO, Branchen, Sprachen, Laufzeit, Überschreitung) |
| 6 | `BreadcrumbList` | Home-Root |
| 7 | `HowTo` | 3-Schritte-Setup (Template → Daten → Live), totalTime=PT2M |
| 8 | `Service` ×3 | Terminbuchung, 24/7 Anrufannahme, Ticketing |
| 9 | `WebPage` | Mit `speakable` für Google-Assistant (h1, h2, .hero-subtitle) |

Der `@id`-Graph verknüpft alle Entities sauber (publisher, provider-Refs).

## 4. Industry Landing Pages

Generator: `scripts/gen-landing-pages.mjs` — erzeugt 6 statische SEO-Landings nach `apps/web/public/<slug>/index.html`:

| Slug | URL | Branche |
|---|---|---|
| `friseur` | phonbot.de/friseur/ | Friseursalons |
| `handwerker` | phonbot.de/handwerker/ | Handwerksbetriebe |
| `arztpraxis` | phonbot.de/arztpraxis/ | Arztpraxen |
| `reinigung` | phonbot.de/reinigung/ | Reinigung/Cleaning |
| `restaurant` | phonbot.de/restaurant/ | Gastronomie |
| `autowerkstatt` | phonbot.de/autowerkstatt/ | KFZ-Werkstätten |

Jede Landing ist **statisch gerendert** (nicht SPA) → maximale Indexierbarkeit. Enthält: eigenes `<title>`, `description`, canonical, hreflang, OG-Tags, branchen-spezifisches JSON-LD `Service`-Schema mit `parentOrganization → Mindrails UG`, und eigene Copy (H1, Dialog-Beispiel, Features, Savings-Rechnung).

## 5. Cross-Product SEO-Strategie

Mindrails als Dachmarke wird konsequent im SEO-Graph genannt:
- Root `JSON-LD Organization.parentOrganization` = `Mindrails UG` (mit URL `mindrails.de`, Gründer, Adresse).
- Legal-Modal (`LegalModal.tsx:78-80`) nennt Socibot als Schwesterprodukt: *„Mindrails UG… Weitere Produkte: Socibot (in Entwicklung)."* — **gewollt** für Konzerntransparenz + Mindrails-Domain-SEO. Im Vault sind die Produkte getrennt (siehe [[Mindrails/Overview]]), im Code / in der Live-Sichtbarkeit wird die Mindrails-Klammer aber bewusst sichtbar gemacht.

## 6. Performance-Hinweise (SEO-Ranking-Faktor)

- `<link rel="preconnect" href="https://api.retellai.com">` (index.html:9).
- `<link rel="dns-prefetch" href="https://api.retellai.com">` (index.html:10).
- Caddy strikt cached statische Web-Assets (nginx-Stage im Web-Dockerfile, 1y immutable).
- Root-Dokument nutzt **keine** Google Fonts CDN — explicit in Kommentar: *"S-03: NO Google Fonts CDN (removed for DSGVO; CSS fallback is system-ui)"* (index.html:53-54).

## 7. Lücken & Findings

### 🟡 DSGVO-Inkonsistenz
- **Branchen-Landings laden Google Fonts CDN** (`apps/web/public/friseur/index.html:21-23`): `<link href="https://fonts.googleapis.com/css2?family=Inter...">` + preconnect. Das widerspricht der `S-03` Policy im Root-`index.html` (kein Google-Fonts-CDN aus DSGVO-Gründen). Sollte self-hosted werden, sonst ist die Mühe im Root-Dokument wieder zunichte.
- **CSP im Caddyfile:9 erlaubt `fonts.googleapis.com` + `fonts.gstatic.com`** — passt zu den Landing-Pages, nicht zum Root-Dokument. Gleicher Widerspruch.

### 🟡 Preis-Drift
- Root `SoftwareApplication` Offers nennt **Starter 79 €** (index.html:117).
- Branchen-Landing Friseur sagt **„Ab 49 €/Monat"** (friseur/index.html:6 + JSON-LD Offer price=49).
- Entweder 49 € ist eine alte Teaser-Kampagne oder ein fehlerhafter Copy-Carry-Over. Kunden die über `/friseur/` kommen und dann den Haupt-Pricing-Block sehen, bemerken die Diskrepanz.

### 🟡 Sitemap-Lastmod veraltet
- `sitemap.xml` hat `lastmod: 2026-04-18` hartkodiert für alle URLs (`apps/web/public/sitemap.xml`). Keine Build-Step-Aktualisierung — Google crawlt weniger oft, wenn Lastmod stale bleibt.

### 🟡 Robots.txt erlaubt alle AI-Bots — auch Training
- `ai.txt` existiert aber steuert nur *Training*, nicht Crawling. `Allow: /` für `CCBot`, `GPTBot`, `anthropic-ai` bedeutet: Inhalt darf von diesen Bots abgerufen UND für Training verwendet werden (sofern `ai.txt` das nicht einschränkt). Bewusste Entscheidung für AI-Overview-Sichtbarkeit — aber ggf. gegenprüfen ob man Training wirklich erlauben will (vs. nur Suche).

### 🟢 Minor
- `<meta keywords>` — tote Signal-Quelle seit 2009. Cost = 0, aber auch Benefit = 0.
- `<link rel="alternate" type="application/rss+xml">` verweist auf die Homepage — kein echter RSS-Feed. Harmlos, aber unsauber.

## 8. Quellen (Dateien)

- `apps/web/index.html` — Root-Dokument, JSON-LD
- `apps/web/public/robots.txt`
- `apps/web/public/sitemap.xml`
- `apps/web/public/llms.txt`, `llms-full.txt`, `ai.txt`, `humans.txt`
- `apps/web/public/{friseur,handwerker,arztpraxis,reinigung,restaurant,autowerkstatt}/index.html`
- `apps/web/public/{impressum,datenschutz,agb}/` — statische Legal-Pages
- `scripts/gen-landing-pages.mjs` — Landing-Page-Generator
- `Caddyfile` — Redirects, Content-Type, Security-Headers
- `.indexnow-key` + `apps/web/public/0973a7e7...txt` — IndexNow-Key

## 9. Verbundene Notes

- [[Phonbot/Overview]]
- [[Phonbot/Phonbot-Gesamtsystem]]
- [[Phonbot/modules/Frontend-Shell]] — LegalModal + Design-System
- [[Phonbot/modules/Shared-Infra-Tests]] — Caddyfile + Web-Dockerfile

## 10. Nächste Schritte (Vorschlag)

- [ ] Google Fonts in Branchen-Landings self-hosten (DSGVO-Alignment, siehe §7 Inkonsistenz)
- [ ] Preis-Drift 49 € vs. 79 € auflösen (korrekten Starter-Preis in Branchen-JSON-LDs einsetzen)
- [ ] Sitemap-Generator im Build-Step (z. B. `pnpm build` ruft ein kleines Script, das `lastmod` = Commit-Datum der jeweiligen Source-Datei setzt)
- [ ] `<meta keywords>` entfernen (keine Wirkung, unnötiges Noise)
- [ ] Entscheidung dokumentieren: Training-Erlaubnis für GPTBot/ClaudeBot/CCBot → falls nur Search gewünscht, `ai.txt` entsprechend schärfen

## 11. Changelog

- 2026-04-21: Erster SEO-Status-Snapshot, code-basiert aus `apps/web/` + `Caddyfile` extrahiert.
