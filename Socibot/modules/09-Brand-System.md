---
title: 09 — Brand-System
tags: [socibot, modul, brand]
date: 2026-04-27
source_of_truth: code
---

# 09 — Brand-System

> Drei Quellen: `brand/foerderkraft_brand.py` (Code-Default), `client/brand_knowledge.json` (User-Override), `config/brand_style_map.json` (Tone→Visual).

## `brand/foerderkraft_brand.py` (363 LOC inkl. `__init__.py`)

Klasse: keine, nur Module-Level-Funktionen + Cache.

### Cache (Z.13–16)

```python
_brand_cache: dict | None = None
_brand_cache_time: float = 0
_BRAND_CACHE_TTL = 60   # Sekunden
```

### `_DEFAULTS`-Dict (Z.18–80+)

Hardcoded „Förderkraft GmbH"-Brand mit Keys:
- `name`, `slogan`, `industry`, `core_service`, `founded`, `auftraggeber` (DRK), `mission`
- `values` (5–6 Einträge), `usp` (3–4 Einträge)
- `target_audience: { b2b_clients, recruits, partners }`
- `general_tone: { personality, avoid, always }`
- `platform_voices: { instagram, facebook, linkedin, twitter, tiktok }` — pro Plattform Tone-Hinweise

### Public-Funktionen

- `get_brand()` — gibt Cache zurück, lädt von `client/brand_knowledge.json` falls < 60s alt, sonst Defaults
- `get_brand_context(platform: str)` — formatierter String für Claude-Prompts
- `get_platform_voice(platform: str)` — Tone-Snippet pro Plattform
- `invalidate_brand_cache()` — wird von `fragebogen`, `brand_settings`, `supabase_sync`, `api/research-apply` aufgerufen
- `BRAND` — Module-Level-Konstante (Defaults), wird direkt importiert von Content-Generators

### Verifiziert importiert von

- `bot/content_calendar.py:7` (`BRAND, get_platform_voice`)
- `bot/dm_handler.py:8` (`get_brand_context, BRAND`)
- alle 5 `<platform>_content.py` (`get_brand_context, get_platform_voice, BRAND`)
- `dashboard/services/brand_extractor.py:14` (Fallback)
- `video/prompt_builder.py:8` (importiert, aber nicht verwendet — Note)

## `client/brand_knowledge.json` — User-Override

**Top-Level-Keys** (verifiziert über Test-Datei `TestFirma`):

```json
{
  "brand_name":          "TestFirma",
  "industry":            "string",
  "mission":             "string",
  "slogan":              "string",
  "target_audience":     "string",
  "tone_keywords":       ["professionell"],
  "content_pillars":     ["Updates"],
  "values":              ["..."],
  "usp":                 ["..."],
  "active_platforms":    ["instagram"],
  "confirmed_by_user":   true,
  "onboarded_at":        "ISO-Datum",
  "contact_name":        "string",
  "contact_email":       "string",
  "contact_phone":       "string",
  "source":              "supabase" | "local",
  "supabase_id":         "uuid (optional)"
}
```

### Wer schreibt (verifiziert)

- `dashboard/routes/fragebogen.py:64-65`
- `dashboard/routes/brand_settings.py:93,309`
- `dashboard/routes/api.py:170` (`/api/research-apply`)
- `dashboard/services/brand_extractor.py:93`
- `dashboard/services/supabase_sync.py:118-119`

→ **Race-Condition-Risiko:** 5 Schreibstellen, kein Lock, kein temp+rename. Konfliktszenario: Supabase-Sync schreibt während User per Fragebogen submitted.

### Wer liest

- `bot/content_calendar.py:89-103` (Topic-Override)
- `bot/dm_handler.py:18` (Indirekt via `get_brand`)
- `dashboard/routes/api.py`, `learning.py`, `overview.py`
- `dashboard/services/ai_vision.py:16,64`
- `dashboard/services/brand_extractor.py:100,113`
- `dashboard/services/research_agent.py:20`
- `dashboard/services/variant_service.py` (via `get_brand_context`)
- `video/queue.py:171` (Fallback-Brand-Config bei Job-Run)

## `config/brand_style_map.json`

Maps `tone_keywords` → visuelle / audio Parameter für Video-Engine. Struktur:

```json
{
  "tone_to_image":  { "professionell": {lighting, colors, composition}, "warm": {...}, ... },
  "tone_to_video":  { ... camera_move, duration_sec, energy ... },
  "tone_to_audio":  { ... mood, genre, bpm_range ... },
  "tone_to_color":  { ... lut, grain ... },
  "tone_to_text":   { ... font, highlight_color, position ... }
}
```

### Wer liest

- `video/brand_mapping.py:15` — einzige Lesestelle, `resolve_style(brand_config)` Z.21–49

### Fallback bei Missing JSON

`video/brand_mapping.py:52-61`:

```python
{
  "primary_tone": "professionell",
  "image":  {"lighting": "soft studio lighting", "colors": "muted corporate tones", "composition": "centered"},
  "video":  {"camera_move": "slow zoom in", "duration_sec": 8, "energy": "low"},
  "audio":  {"mood": "corporate", "genre": "ambient", "bpm_range": [90, 110]},
  "color":  {"lut": "neutral_sharp", "grain": 5},
  "text":   {"font": "Montserrat-Bold", "highlight_color": "#FFFFFF", "position": "bottom_center"}
}
```

## `brand/assets/` — Marken-Logo

Optional `logo.png`. Verwendet von:
- `dashboard/services/image_branding.py:99` — wenn vorhanden, wird statt Brand-Text gepasted

## Brand-Hardcoding-Hotspots (code-belegt)

Trotz Brand-System gibt es **hardcoded Förderkraft-Werte**:

| Datei:Zeile | Hardcode |
|---|---|
| `bot/content_calendar.py:100` | Regex `\bFörderkraft\b` für Brand-Name-Substitution |
| `dashboard/services/variant_service.py:248` | Brand-Keyword-Liste `["förderkraft","drk","rotes kreuz","haustür","außendienst","spende","förder"]` |
| `bot/config.py:85` | Default `info@mindrails.de` |
| `brand/foerderkraft_brand.py:18-80` | Komplettes `_DEFAULTS`-Dict mit „Förderkraft GmbH"-Werten |

## Verbundene Notes

- [[Socibot/modules/03-Platforms]]
- [[Socibot/modules/04-Video-Engine]] — `brand_mapping.py`
- [[Socibot/modules/06-Dashboard-Routes]] — Routes, die Brand-State mutieren
- [[Socibot/modules/14-Findings]] — Hardcode-Risiken
