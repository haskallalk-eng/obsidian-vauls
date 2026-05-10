# Chipy 3D Motion Workflow

Status: 2026-05-10. Phonbot-spezifischer Ablauf fuer Mascot, 3D Hero, Scroll Animation und animierte Assets.

## Fixe Referenz

- Mascot-Quelle: `[[Chipy Crystal Mascot Reference]]`
- Assets: `assets/mascot/chipy-crystal-mascot-hero.png`, `assets/mascot/chipy-crystal-mascot-variants.png`
- Skill: `C:\Users\pc105\.codex\skills\chipy-3d-motion`
- Design-Baseline: `C:\Users\pc105\.codex\skills\chipy-design`

## Entscheidungsbaum

1. UI oder Produktoberflaeche: `chipy-design` + Browser/Playwright.
2. Mascot-Variante oder Mood: `imagegen` mit Crystal-Mascot-Reference.
3. Editierbares Design/Handoff: Figma Tools und Figma Skills.
4. Scroll-/Hero-Bewegung: Motion Studio MCP + CSS/React/Motion Implementierung.
5. Erklaervideo/Social Clip: Remotion MCP + Remotion-Projekt.
6. Echte interaktive 3D Szene: erst planen, dann Three.js/R3F bewusst einbauen.

## Akzeptanzkriterien

- Orange/Cyan Glow bleibt sichtbar und ausgewogen.
- Logo-Haar ist klar als Phonbot-Flamme erkennbar.
- Mascot wirkt premium, kristallin, freundlich und nicht generisch.
- Animation hat Zweck: Aufmerksamkeit, Erklaerung oder Orientierung.
- Mobile Ansicht funktioniert ohne abgeschnittene Props.
- Reduced-Motion-Fallback existiert bei starken Bewegungen.
- Performance wird vor Deploy geprueft, besonders bei 3D/Video.

## Standard-Prompt fuer visuelle Konzepte

Crystalline glass mascot for Phonbot called Chipy, faceted black obsidian body, split orange fire glow on the left and cyan electric glow on the right, friendly closed glowing eyes, Phonbot flame logo as hair on top of the head, holding a phone receiver and a calendar, premium dark product design, luminous glass refractions, clean high-end 3D brand mascot, no purple, no cartoon hamster, no generic robot.

## Review-Fragen

- Sieht man sofort Telefon/Termin/AI-Assistent?
- Ist die Silhouette auch klein noch wiedererkennbar?
- Passt die Bewegung zur Funktion oder ist sie nur Deko?
- Wird der Claim/USP staerker, oder klaut die Animation Aufmerksamkeit?
- Ist die Umsetzung wartbar in unserem Frontend?
