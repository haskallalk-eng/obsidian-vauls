---
id: 6
status: backlog
priority: P1
blocked_by: []
tags:
  - socibot
  - quality
  - anti-drift
created: 2026-04-29
---

# Originalitäts-Check gegen letzte 30 Posts

Vor User-Anzeige: Embedding-Diff (sentence-transformers oder Anthropic-Embeddings) gegen die letzten 30 eigenen Posts. Wenn cosine-similarity > 0.85 → automatisch regenerieren mit "Diversifikations-Hint".

## Warum P1
Verhindert "alle Posts klingen gleich"-Drift, der nach Wochen unweigerlich auftritt. Industry-Pattern aus Repurposing-Tools (FeedHive).

## Acceptance
- [ ] Embedding-Service `dashboard/services/post_embeddings.py` mit Cache
- [ ] `client/post_embeddings.json` (oder SQLite) hält letzte 30 Embeddings pro Brand
- [ ] Pipeline: nach Generation → Similarity-Check → wenn >0.85 → max 2 Regenerations mit "Mache deutlich anders als bisherige Posts"-Hint, sonst durchwinken
- [ ] Threshold im UI konfigurierbar (Diversitäts-Slider mappt darauf)
