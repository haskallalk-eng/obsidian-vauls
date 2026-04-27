---
title: 13 — Automation
tags: [socibot, modul, automation]
date: 2026-04-27
source_of_truth: code
---

# 13 — Automation (`automation/`)

## Files

| Datei | Zweck |
|---|---|
| `generate_sample_content.py` | One-shot-Generator für Demo-Content |
| `sample_content.json` | Generated Beispiel-Posts (genutzt von Mediathek-Ideen-Tab!) |
| `image_prompts.json` | Image-Prompt-Templates |

## `generate_sample_content.py` (163 LOC)

Einmaliger Script-Run. Erzeugt Demo-Posts für alle 5 Plattformen via Claude. Schreibt Output zu `automation/sample_content.json`.

**Aufruf:** Manuell, kein Scheduler-Hook.

## `automation/sample_content.json` — VERWENDET PRODUKTIV

Wird **gelesen** von `dashboard/routes/media.py:32-48` (`_ideas_by_platform()`):
- Beim 2026-04-27-Refactor in den Mediathek-Ideen-Tab eingebaut
- Wenn Datei fehlt → empty dict → Empty-State-Banner im UI

**Schema:**

```json
{
  "generated_at": "ISO datetime",
  "platforms": {
    "instagram": [
      {
        "topic": "string",
        "content": "string (Multi-line Caption)",
        "status": "bereit",
        "created_at": "ISO datetime"
      },
      ...
    ],
    "facebook": [...],
    "linkedin": [...],
    "twitter": [...],
    "tiktok": [...]
  }
}
```

**Aktueller Inhalt:** Förderkraft-Demo-Posts vom 2026-03-21 mit DRK-Vertriebs-Kontext. Der ursprüngliche Demo-Set wird im Dashboard als „Ideen" angezeigt — das ist eine Eingewöhnungs-Krücke, **kein Live-Update-Mechanismus**.

→ Findings-Item: Wenn der Kunde nicht „Förderkraft" ist, sieht er trotzdem Förderkraft-Posts unter „Ideen". Der `_ideas_by_platform`-Loader hat keinen Brand-Filter.

## `automation/image_prompts.json`

Templates für Image-Generation. Aktuell **nicht referenziert** im Code (keine Lese-Stelle gefunden). Möglicherweise für `generate_sample_content.py` gedacht oder Future-Use.

## Verbundene Notes

- [[Socibot/modules/06-Dashboard-Routes]] — `media.py` liest `sample_content.json`
- [[Socibot/modules/14-Findings]]
