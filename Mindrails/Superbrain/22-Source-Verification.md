---
title: Source Verification
type: methodology
status: active
tags:
  - mindrails
  - superbrain
  - research
  - verification
parent: "[[Mindrails/Superbrain/00-Superbrain-Index|Superbrain]]"
created: 2026-05-05
updated: 2026-05-05
---

# Source Verification

Source Verification sorgt dafür, dass Recherche nicht zu hübsch klingenden Behauptungen wird.

## Quellen-Hierarchie

1. Primärquelle: offizielle Docs, Gesetzestext, Anbieter-Doku, wissenschaftlicher Report, Code.
2. Sekundärquelle: seriöse Analyse mit klaren Daten und Methoden.
3. Marktmeinung: VC/Consulting/Blog, nützlich für Signale, nicht als Wahrheit.
4. Social/Forum: nur als Hinweis auf Problemklasse, nie alleinige Entscheidungsbasis.

## Prüfregeln

- Recency prüfen: AI-/Provider-/Rechtsquellen können schnell veralten.
- Lateral Reading: Quelle, Autor, Interessen und Gegenquellen prüfen.
- Exakte Claims notieren: keine schwammigen "AI wird alles verändern"-Sätze.
- Relevanz für Phonbot ableiten: Was ändert sich an Produkt, Vertrieb, Risiko oder Code?
- Confidence vergeben: High, Medium, Low.

## Source Card

```md
### Quelle
- URL:
- Typ: Primär / Sekundär / Marktmeinung / Signal
- Datum / Last checked:
- Claim:
- Beleg:
- Relevanz für Mindrails/Phonbot:
- Gegenargument / Unsicherheit:
- Confidence:
```

## Red Flags

- Keine Datumsangabe bei zeitkritischen AI-Claims.
- Anbieter behauptet Marktführerschaft ohne Benchmark.
- Report vermischt Adoption, Umsatz und Interesse.
- Quelle verkauft direkt das Produkt, das sie bewertet.
- Zitat aus Sekundärquelle, obwohl Primärquelle verfügbar ist.

## Gute Standardquellen

- AI/Strategie: Stanford AI Index, OECD, NIST AI RMF, OpenAI Docs.
- Engineering/Security: NIST SSDF, OWASP, Google Engineering Practices, GitHub Docs.
- Zuverlässigkeit: Google SRE.
- Quellenprüfung: Purdue OWL, SIFT/Lateral Reading.
- Obsidian: offizielle Obsidian Help.

