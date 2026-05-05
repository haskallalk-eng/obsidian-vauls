---
title: Claude — Skills & MCPs (Mindrails-Kontext)
type: reference
tags: [claude, skills, mcp, meta, tools]
created: 2026-04-22
---

# Claude — Skills & MCPs

> Was Claude in diesem Setup _wirklich_ zur Verfügung hat und wann welches Tool sinnvoll ist. Gefiltert auf Mindrails-Workflows (Phonbot / Socibot + Obsidian-Vault). Rein technisch sind deutlich mehr Skills installiert — hier stehen die, die **im Alltag greifen**.

## Schnell-Entscheidung

> **Du sagst…** → **Ich nehme…**

| Wunsch / Situation | Skill / Agent / MCP |
|---|---|
| „Bau mir eine Seite / Section für Phonbot" | [chipy-design](#chipy-design) |
| „Design-Review / does this look off?" | [design-review](#design-review) |
| „Pre-Launch harter Audit" | [critical-audit](#critical-audit) + [security-review](#security-review) |
| „Neues Feature planen / brainstorm" | [superpowers-brainstorming](#superpowers) + [superpowers-writing-plans](#superpowers) |
| „Multi-Step-Task mit klarem Plan ausführen" | [superpowers-executing-plans](#superpowers) oder [superpowers-subagent-driven-development](#superpowers) |
| „Bug — produziert falsches Ergebnis / crasht" | [superpowers-systematic-debugging](#superpowers) → dann [debugging-code](#debugging-code) |
| „Test-First entwickeln" | [test-driven-development](#tdd) |
| „Landing-Page / Marketing-Seite" | [landing-page](#landing-page) (generisch) ODER [chipy-design](#chipy-design) (Phonbot) |
| „Icons für ein Projekt" | [icon-set-generator](#icon-set-generator) |
| „Favicon-Stack" | [favicon-gen](#favicon-gen) |
| „Farben aus Brand-Hex ableiten" | [color-palette](#color-palette) |
| „Bild AI-generieren" | [ai-image-generator](#ai-image-generator) |
| „CRO / Tracking / A/B Test" | [web-analytics](#web-analytics) |
| „Browser-Test / funktioniert X im UI?" | [webapp-testing](#webapp-testing) + [playwright MCP](#playwright-mcp) |
| „Docs einer Library nachschlagen" | [context7 MCP](#context7-mcp) |
| „URL ausgelesen bekommen" | [defuddle](#defuddle) |
| „Excel / Word / PDF anfassen" | [xlsx](#xlsx) / [docx](#docx) / [pdf](#pdf) |
| „Claude-API-App bauen" | [claude-api](#claude-api) |
| „Obsidian-Vault bedienen" | [obsidian-cli](#obsidian) |
| „Neue Skill schreiben / verbessern" | [superpowers-writing-skills](#superpowers) |
| „Recurring Task / Polling" | [loop](#loop) bzw. [schedule](#schedule) |
| „Settings / Hook / Permission ändern" | [update-config](#update-config) |
| „Fehlertracking Phonbot" | [sentry MCP](#sentry-mcp) |
| „DB-Query auf Phonbot DB" | [supabase MCP](#supabase-mcp) (auth'd) |
| „GitHub Issues / PRs" | [github MCP](#github-mcp) |
| „Security / DSGVO-Audit bei user-facing Feature" | [security-dsgvo-reviewer Agent](#security-dsgvo-reviewer) — **proaktiv!** |
| „Codebase erkunden (>3 Queries)" | [Explore Agent](#explore) |

## 1. Design & UX

### chipy-design
**Trigger:** jede UI/UX-Arbeit an Phonbot. Auto-aktiv bei „phonbot page", „new section", „hero", „glass card", „orange cyan", „chipy", „wie die Homepage / Kontaktseite". **Single Source** für die Phonbot-DNA (Glass, Orange→Cyan, Chipy-Hamster, Sticky-Nav, Noise-Overlay, Pulsing-Orbs).

Enthält: Color-Palette, Typography, Signature-Components, Animation-Library, Mascot-Regeln, Anti-Patterns (Drifts die schon passiert sind), A11y-Floor, State-Matrix, Responsive-Rules, Perf-Guardrails, Content/SEO, Tooltip-Pattern (§18), Z-Index-Skala (§19), Motion-Timing (§20), Cursor-Discipline (§21).

**Niemals:** für ein anderes Produkt als Phonbot (dann generisches `design-system` oder `mindrally-design-systems`).

### design-review
**Trigger:** „review the design", „does this look off", „make it look better", „is this polished". Visuelle Polish-Kontrolle — Typography, Spacing, Hierarchie, Consistency, Interaction-Patterns, Responsive. Nicht zu verwechseln mit UX-Audit.

### design-system (generisch, nicht chipy)
**Trigger:** „extract design system from X", „reverse engineer design". Analysiert fremde Websites / Screenshots via Playwright + HTML und produziert eine `DESIGN.md`. Für Phonbot **nicht** verwenden.

### landing-page
**Trigger:** „create a landing page / coming soon page / one-pager". Generiert eine deployable Single-HTML-Datei mit Tailwind-CDN. Für Phonbot **nicht** verwenden (nutze chipy-design).

### ui-ux-pro-max
**Trigger:** Generic UI-Arbeit wenn kein Projekt-eigener Skill greift. 67 Stile, 96 Paletten, 57 Font-Pairings, Priority-Ranking nach A11y/Touch/Performance. Python-CLI unter der Haube.

### mindrally-ui-design / mindrally-ux-design / mindrally-design-systems
Generische interne Guidelines. Sind teilweise in chipy-design §12/13 schon reinportiert. Für neue Produkte im Mindrails-Ökosystem (vor chipy-Pendant existiert).

### color-palette
**Trigger:** „generate palette from hex X", „brand colors". 11-Shade-Skala + Semantic-Tokens + Dark-Mode + Tailwind-v4-CSS. WCAG-Contrast-Check inklusive.

### icon-set-generator
**Trigger:** „I need icons for X", wenn ein Projekt eine Icon-Familie braucht. Produziert individuelle SVG-Files mit konsistenter Style-Engine. Nicht verwechseln mit Icon-Library-Lookup.

### favicon-gen
**Trigger:** neues Projekt init, Favicon zeigt nicht, iOS-Black-Square. Komplettes Favicon-Set (ICO, SVG, Apple-Touch, Manifest, 192/512 PNG).

### ai-image-generator
**Trigger:** „generate hero image", „AI image", „create OG image". Gemini für Szenen, GPT für transparente Icons. 5-Part-Prompting-Framework, multi-turn Editing.

### frontend-design (plugin)
**Trigger:** wenn distinktive, nicht-generische UI gebraucht wird (bewusste Aesthetic-Direction, keine AI-Slop). Ausgeprägte Typografie, Atmosphere, Motion. Für Phonbot → chipy-design gewinnt.

## 2. Code & Framework

### react-patterns
**Trigger:** „react review / patterns / performance", „why is it slow", „fix waterfall", „reduce re-renders". 50+ React-19-Regeln nach Impact geordnet. Vite + Cloudflare-fokussiert, passt trotzdem für Phonbot.

### mindrally-react
Generic React-Patterns für Mindrails-Projekte.

### mindrally-nextjs-react-typescript
Next.js App Router + Shadcn UI + Radix + Tailwind. Für neue Mindrails-Projekte (Phonbot ist Vite, nicht Next — nicht hier einsetzen).

### mindrally-nextjs-typescript-tailwindcss-supabase
Full-Stack Next.js 14 + Supabase — für neue Full-Stack-Projekte im Mindrails-Ökosystem.

### mindrally-tailwindcss
Tailwind utility-first + responsive patterns. Passt zu Phonbot (Tailwind 4).

### tailwind-theme-builder
**Trigger:** React-Projekt-Init mit Shadcn/UI, Tailwind v4 + `@theme inline`, Dark-Mode-Setup, v3→v4 Migration.

### mindrally-seo-best-practices
Metadata, Indexing, Core-Web-Vitals. Schon in chipy-design §15/16 teilweise portiert.

### mindrally-performance-optimization
SSR, CSS / JS Perf. Überlappt mit react-patterns + chipy-design §15.

### claude-api
**Trigger:** Imports `anthropic`/`@anthropic-ai/sdk`, Claude-API-Fragen, Managed Agents, Caching/Thinking/Compaction/Tool-Use tunen. **Enthält Prompt-Caching by default**. Für Phonbot aktuell nicht relevant (nutzt OpenAI), für Socibot eventuell.

## 3. Dev-Workflow

### superpowers (mehrere)
**Pflicht bei:**
- **brainstorming** — MUSS **vor** Creative Work (neue Features, Komponenten, Behavior). Exploriert Intent + Requirements.
- **writing-plans** — wenn Spec für Multi-Step-Task vorhanden, **BEVOR** Code angefasst wird.
- **executing-plans** — Plan ausführen mit Review-Checkpoints (getrennte Session).
- **subagent-driven-development** — Plan mit unabhängigen Tasks in aktueller Session.
- **dispatching-parallel-agents** — 2+ unabhängige Tasks, keine Shared State.
- **systematic-debugging** — MUSS bei jedem Bug/Testfailure **BEVOR** Fix vorgeschlagen wird.
- **writing-skills** — neue Skills schreiben/editieren/verifizieren (TDD für Docs).

### test-driven-development
**Trigger:** Feature / Bugfix implementieren — **vor** Implementation. Red → Green → Refactor. Paired mit superpowers-systematic-debugging bei Debug-Flows.

### debugging-code
**Trigger:** Programm crasht / produziert falsche Ausgabe / print-statements reichen nicht. Interaktives Debugging — Breakpoints, step-through, Variablen inspizieren, Call-Stack. Erfordert Debugger-Setup.

### critical-audit
**Trigger:** Pre-Launch / „find all weaknesses". Harter Review aus 3rd-Party-Perspektive über Security, A11y, Perf, Design, Error-Handling, Architecture.

### security-review
**Trigger:** vor Merge/Launch — Security-only Review der Pending-Branch-Changes.

### simplify
**Trigger:** nach größerem Code-Wurf, vor Commit. Reviews Code für Reuse/Quality/Efficiency + fixt Issues.

### review (PR-Review)
**Trigger:** „review PR #123 / this PR".

### init (CLAUDE.md)
**Trigger:** neues Projekt / kein CLAUDE.md vorhanden. One-off.

## 4. Content & Dokumente

### pdf
**Trigger:** PDF lesen/bearbeiten/erzeugen/mergen/splitten/OCR. Formular-Fill, Watermark, Verschlüsselung.

### docx
**Trigger:** „Word doc / .docx" — erstellen, lesen, editieren, find-replace, Tables-of-Contents, Letterheads, tracked changes.

### xlsx
**Trigger:** Spreadsheet (.xlsx/.xlsm/.csv/.tsv) als primärer Input oder Output. Cleaning messy data, Formeln, Charting, Konvertierung. Spreadsheet muss das Hauptprodukt sein.

### defuddle
**Trigger:** User gibt URL und will Inhalt lesen. **Statt** WebFetch für Webseiten/Blog-Artikel/Docs — extrahiert cleanes Markdown ohne Nav-Clutter. **Nicht** für `.md`-URLs (direkt WebFetch).

### product-showcase
**Trigger:** „showcase site / marketing-site / explain the app". Multi-Page Marketing-Site mit echten App-Screenshots + GIF-Walkthroughs via Playwright. Für komplexe / agentische Apps.

### web-analytics
**Trigger:** „track / conversion / CRO / A/B test / funnel / heatmap / bounce / CTR / improve conversions". Analytics-Setup, Conversion-Optimierung, Funnel-Analyse für SaaS + Landing.

## 5. Obsidian

### obsidian-cli
**Trigger:** Vault bedienen per CLI — Notes lesen/erstellen/suchen, Properties, Tasks. Plus Plugin-Dev: reload-plugin, JS ausführen, Screenshots, DOM inspizieren.

### obsidian-markdown
**Trigger:** `.md`-Files im Vault mit Obsidian-Flavor — Wikilinks `[[…]]`, Embeds `![[…]]`, Callouts `> [!info]`, Frontmatter, Tags.

### obsidian-bases
**Trigger:** `.base`-Dateien (Datenbank-artige Views). Filter, Formeln, Summaries, Card/Table-Views.

## 6. Config & Ops

### update-config
**Trigger:** „allow X permission", „set ENV=Y", „when X then Y", Hooks, MCP-Setup, Änderungen an `settings.json` / `settings.local.json`. **IMMER** für automatische Behaviors (Memory/Preferences können das nicht).

### keybindings-help
**Trigger:** „rebind ctrl+s", „custom chord", Änderungen an `~/.claude/keybindings.json`.

### fewer-permission-prompts
**Trigger:** „zu viele Permission-Prompts". Scannt Transkripte, baut Allowlist für häufige Bash/MCP-Calls in `.claude/settings.json`.

### loop
**Trigger:** „check every 5 min", „keep running X". Recurring Task — **nicht** für One-Off.

### schedule
**Trigger:** Cron-artig — recurring remote Agent / Trigger mit Schedule.

### statusline-setup
**Trigger:** Custom-Status-Line in Claude Code. Niche.

## 7. Testing

### webapp-testing
**Trigger:** Lokale Web-App via Playwright antesten — Frontend verifizieren, UI-Verhalten debuggen, Screenshots, Browser-Logs.

## 8. Sub-Agents (Agent Tool)

### Explore
**Trigger:** Codebase-Recherche die >3 Queries braucht, breite Exploration, Pattern-Suche. Specify `quick` / `medium` / `very thorough`. Schont den Haupt-Context.

### Plan
**Trigger:** Implementations-Strategie für komplexe Tasks planen. Liefert Step-by-Step-Plan + kritische Dateien + Trade-offs. **Nicht** für kleine Tasks.

### general-purpose
**Trigger:** komplexe Multi-Step-Recherche + Ausführung, Keyword-Suchen wo das erste Grep nicht trifft. All-Tools-Zugriff.

### security-dsgvo-reviewer
**Trigger PROAKTIV:** jedes User-facing Feature, Auth-Flow, Daten-Speicherung, API-Endpoint, Cookie, Tracking, 3rd-Party-Integration, Export. OWASP + DSGVO-Checkliste. **Feedback-Memory sagt: ohne Rückfrage einsetzen** bei EU-Apps mit personenbezogenen Daten.

### claude-code-guide
**Trigger:** Fragen _über_ Claude Code, Claude-Agent-SDK, Claude-API (formerly Anthropic). Features, Hooks, Slash-Commands, MCP-Server, Settings, IDE-Extensions.

## 9. MCP-Server

### context7 MCP
**Trigger:** User fragt zu einer Library / Framework / SDK / CLI / Cloud-Service — **auch** bei bekannten wie React / Next / Prisma / Tailwind / Django. API-Syntax, Config, Version-Migration, Debugging, CLI-Usage. **Bevorzugt** gegenüber Web-Search für Lib-Docs.

**Nicht für:** Refactoring, Scripts from scratch, Business-Logic-Debugging, Code-Review, allgemeine Programmier-Konzepte.

### playwright MCP
**Trigger:** Live-Browser-Automation — Pages aufrufen, Screenshots, click/fill/evaluate/wait. Tabs verwalten, Network-Requests, Console-Logs, File-Upload.

**Hinweis (Memory):** _immer_ an Chrome-Profil `info@mindrails.de` andocken, nicht frisch starten — Logins + Cookies bleiben erhalten.

### github MCP
**Trigger:** GitHub Actions außerhalb der `gh`-CLI. PRs, Issues, Comments, Releases.

**Hinweis (Memory):** Active PAT ist auf `haskallalk-eng`, Hansweier-PAT suspendiert. curl braucht `--ssl-no-revoke` auf Windows.

### sentry MCP
**Trigger:** Error-Analyse bei Phonbot — Issue-Details, Event-Attachments, Replay-Details, Profile-Details, Analyze-with-Seer. Auch: DSN anlegen, Projects/Teams managen.

Phonbot hat Sentry wired (siehe `apps/api/src/sentry.ts`) — bei Prod-Bug hier nachgucken.

### supabase MCP
**Trigger:** DB-Calls gegen Phonbot Supabase. Aktuell nur `authenticate` / `complete_authentication` verfügbar — tieferes Query-Access braucht die Session.

### unframer MCP
**Trigger:** Framer-Sites bauen (CMS, Code-Components, Pages, Styles, Fonts). **Nicht** für Phonbot (React direkt).

### Gmail / Google-Calendar / Google-Drive MCPs
**Trigger:** E-Mails lesen/senden, Threads durchsuchen, Labels, Drafts. Calendar-Events lesen/erstellen/updaten. Drive Files suchen/lesen/erstellen.

### Stripe MCP
Nur `authenticate` / `complete_authentication` verfügbar — tiefere Ops brauchen Auth-Session.

## 10. Proaktiv-Muster (Memory-Regeln)

Diese Memory-Rules feuern automatisch — **nicht** erst auf Anfrage warten:

1. **chipy-design** → bei jeder UI-Arbeit an Phonbot ([project_voice_agent_saas.md](../../.claude/projects/C--Users-pc105/memory/project_voice_agent_saas.md))
2. **security-dsgvo-reviewer** → bei jedem User-facing Feature mit EU/DSGVO-Bezug ([feedback_security_dsgvo_first.md](../../.claude/projects/C--Users-pc105/memory/feedback_security_dsgvo_first.md))
3. **superpowers-brainstorming** → vor Creative-Work / neuen Features
4. **superpowers-systematic-debugging** → bei jedem Bug
5. **superpowers-writing-plans** → bei Multi-Step-Tasks
6. **playwright mit info@mindrails.de** → Chrome-Profil wiederverwenden ([feedback_playwright_chrome_profile.md](../../.claude/projects/C--Users-pc105/memory/feedback_playwright_chrome_profile.md))
7. **Obsidian-Auto-Link** → nach jeder Session Daily-Note + Projekt-Note verlinken ([feedback_obsidian_auto_link.md](../../.claude/projects/C--Users-pc105/memory/feedback_obsidian_auto_link.md))
8. **Skill-Optimization** → nach jeder Skill-Nutzung den Skill selbst verbessern ([feedback_skill_optimization.md](../../.claude/projects/C--Users-pc105/memory/feedback_skill_optimization.md))

## 11. Typische Fehlanwendungen (nicht machen)

- ❌ **critical-audit auf jede kleine Änderung** — nur vor Launch oder bei explizitem Audit-Wunsch.
- ❌ **context7 / Web-Search statt Skill** wenn spezialisierter Skill existiert (z.B. `claude-api` für Anthropic-SDK-Fragen, nicht context7).
- ❌ **Planlos Code schreiben** bei nicht-trivialen Features (→ superpowers-brainstorming + writing-plans).
- ❌ **Eigene Prompts** für Claude-API-Apps ohne Prompt-Caching (→ `claude-api` Skill).
- ❌ **chipy-design für Socibot / Kunden-Seiten** — ist Phonbot-spezifisch.
- ❌ **landing-page für Phonbot-Branchen-Pages** — Gen-Script + chipy-design nutzen.
- ❌ **unsere PLAYWRIGHT ohne info@mindrails.de Chrome-Profil**.
- ❌ **statische Pages für User-facing-Auth-Flows** ohne security-dsgvo-reviewer-Pass.

## Querverweise

- [[Phonbot/Pages|🗂 Phonbot — Page Inventory]]
- [[Phonbot/Pricing|💶 Phonbot — Preisgestaltung]]
- [[Phonbot/Overview|Phonbot Overview]]
- [[Socibot/Overview|Socibot Overview]] — falls vorhanden
- Memory-Pointer: [reference_skills_catalog.md](../../.claude/projects/C--Users-pc105/memory/reference_skills_catalog.md)
- Skill-Datei: [chipy-design SKILL.md](../../.claude/skills/chipy-design/SKILL.md)

---

> **Pflege-Regel:** Wenn ein Skill/MCP in Claude Code neu auftaucht oder sich die Triggers/Outputs ändern, diese Note updaten. Die Memory unter `~/.claude/projects/C--Users-pc105/memory/reference_skills_catalog.md` ist der Einzeiler-Pointer auf diese Note hier — kein zweites Content-Copy.
