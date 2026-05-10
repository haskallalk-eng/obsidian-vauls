# Codex Design Research Stack

Status: 2026-05-10, aktive Codex-Toolchain fuer Phonbot/Chipy Design, 3D, Motion und Review.

## Ziel

Codex soll bei Designfragen nicht nur "huebsch machen", sondern gezielt entscheiden:

- Ist das eine UI-/UX-Aufgabe?
- Braucht es Figma als editierbares Design?
- Braucht es Browser-/Playwright-QA?
- Braucht es ein statisches 3D-Bild, echte Web-3D, oder ein animiertes Video?
- Welche Quelle ist offiziell genug, damit man ihr trauen kann?

## Bereits aktive Plugins

- `figma@openai-curated`: Figma Design Context, Screenshots, Canvas-Write, Design-System-Suche, Code Connect.
- `browser-use@openai-bundled`: lokaler Browser fuer UI-Review, responsive Tests und Interaktionen.
- `github@openai-curated`: PRs, Issues, CI und Publish-Workflows.
- `gmail@openai-curated`, `stripe@openai-curated`: Business-/Ops-Kontext.
- `documents`, `presentations`, `spreadsheets`: Dokumente, Decks, Tabellen.
- `imagegen`: Bitmap-Konzepte, Illustrationen, Mascot-Varianten.

## Installierte Skills

- `chipy-design`: Phonbot/Chipy Design-DNA.
- `chipy-3d-motion`: neue Spezialisierung fuer Mascot, 3D Hero, Scroll Animation und Video.
- `figma`, `figma-use`, `figma-implement-design`, `figma-generate-design`.
- `figma-code-connect-components`, `figma-create-design-system-rules`, `figma-create-new-file`, `figma-generate-library`.
- `playwright`, `playwright-interactive`, `screenshot`.
- `speech`, `transcribe`, `pdf`.

## Aktiv konfigurierte MCPs

Aus `codex mcp list`:

- `context7`: `npx -y @upstash/context7-mcp@latest`
- `remotion`: `npx -y @remotion/mcp@latest`
- `motion-studio`: `npx -y https://api.motion.dev/registry.tgz?package=motion-studio-mcp&version=latest`

Hinweis: Neue MCPs/Skills werden in einer laufenden Codex-Session eventuell erst nach Restart voll sichtbar.

Kostenregel: Keine Abo-abhaengigen Design-MCPs global installieren. Primaer nutzen: vorhandenes `imagegen`, lokale Python/OpenCV/Pillow-Skripte, Browser/Playwright, Figma nur wenn bereits verbunden, Remotion/Motion fuer Code-Animationen.

## Einsatzmatrix

| Aufgabe | Primaer nutzen | Zweite Ebene | Nicht direkt tun |
|---|---|---|---|
| Phonbot UI polish | `chipy-design`, Browser | Playwright/Screenshot | Generisches SaaS-Layout bauen |
| Figma-Datei umsetzen | Figma Tools + Figma Skills | Browser QA | Komponenten blind nachbauen |
| Neues Mascot/3D Still | `chipy-3d-motion`, `imagegen` | Figma fuer Handoff | Hamster/Robot-Mascot nutzen |
| Scroll Animation | `motion-studio`, Browser | Context7 fuer Motion/React Doku | Heavy 3D nur fuer Deko |
| Produktvideo | `remotion` | Presentations fuer Storyboard | Einmalige Wegwerf-Animation ohne System |
| Library-Fragen | `context7` | Web/Official Docs | Aus altem Modellwissen raten |
| Echte Web-3D Szene | Three.js/R3F nach Recherche | Browser Perf QA | 3D Dependency ohne Nutzen |

## Quellen und Trust-Entscheidungen

- Figma MCP ist offiziell und bietet Design Context, Canvas-Write, Code Connect und Design-System-Workflows: https://developers.figma.com/docs/figma-mcp-server/
- Remotion MCP ist offiziell, installiert per `@remotion/mcp@latest`, und dient als Doku-/Kontextserver fuer programmatische Videos: https://www.remotion.dev/docs/ai/mcp
- Motion Studio MCP ist offiziell und gibt Zugriff auf aktuelle Motion-Doku, Beispiele und Animation-Kontext; Motion+ kann fuer volle Features noetig sein: https://motion.dev/docs/studio-ai-context
- Context7 liefert aktuelle Library-Doku, weist aber selbst darauf hin, dass Projektinhalte community-bezogen geprueft werden muessen: https://github.com/upstash/context7
- Photoshop MCP wurde wieder entfernt, weil er lokal installiertes Adobe Photoshop voraussetzt und damit nicht zur "nur bestehendes Codex/OpenAI-Abo"-Regel passt.

## Bewusst nicht global installiert

- Blender MCP: stark fuer 3D, aber fuehrt lokalen Blender/Python-Code aus. Nur isoliert in einem Pilotprojekt.
- Photoshop MCP: braucht Adobe Photoshop lokal und ist deshalb nicht Teil des Standard-Stacks.
- ComfyUI MCP: Open Source, aber braucht lokalen ComfyUI-Server/GPU-Setup; erst installieren, wenn bewusst ein lokales Modell-Studio aufgebaut wird.
- Photopea MCP: potenziell kostenlos/browserbasiert, aber nicht noetig fuer sichere Standardarbeit; nur bei konkretem Editierbedarf testen.
- Three.js Devtools MCP: sinnvoll bei echter Three.js/R3F-Szene, aber projektbezogen installieren.
- Framer MCP Plugin: nuetzlich fuer Framer, aber Marketplace-/Tunnel-Vertrauen vorher pruefen.
- Scenario/Invideo: Cloud-Asset/Video-Generatoren, erst Datenschutz/IP/Kosten pruefen.
- Rive MCP: alter MCP-Pfad ist nicht die bevorzugte Zukunft, daher beobachten.
- GSAP Community MCP: unklare Trust-Signale; fuer GSAP lieber offizielle Doku/Context7.

## Arbeitsregel

Bei jeder Designaufgabe zuerst Ziel und Output-Typ klaeren. Dann kleinstes wirksames Tool waehlen: Code/Browsing fuer UI, Figma fuer editierbares Design, Imagegen fuer Still-Konzepte, Remotion fuer Video, Motion fuer UI-Animation, echte 3D nur wenn Interaktivitaet oder Markenwirkung den Aufwand rechtfertigt.
