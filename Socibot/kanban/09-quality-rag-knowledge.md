---
id: 9
status: backlog
priority: P1
blocked_by: []
tags:
  - socibot
  - quality
  - rag
  - persona-a
created: 2026-04-29
---

# Internal Knowledge Base (RAG aus User-Dokumenten)

User uploaded eigene Whitepapers, Blogposts, Bücher, Newsletter-Archive, FAQs → Embeddings → Vector-Storage → Generation-Prompts pullen relevante Snippets als Context.

## Warum P1
Macht aus "generic Coach-Post" einen "Coach-X-spezifischen Post mit echtem Wissen". Hebt Quality auf Level "Brand-Author schreibt selbst".

## Acceptance
- [ ] Upload-UI in `marke.html` (Multi-File: PDF/DOCX/TXT/MD, max 50MB)
- [ ] `dashboard/services/knowledge_rag.py` — Chunk + Embed + Store (lokal SQLite + sqlite-vec, NICHT Cloud, DSGVO)
- [ ] Generation-Pipeline: Top-3 Relevant-Snippets per Embedding-Search → in Prompt als Context
- [ ] User sieht in jedem generierten Post welcher Snippet zitiert wurde (Quellen-Transparenz)
- [ ] Lösch-Funktion + Re-Index pro Dokument
