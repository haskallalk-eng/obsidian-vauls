---
title: 07 — Dashboard-Services
tags: [socibot, modul, services]
date: 2026-04-27
source_of_truth: code
---

# 07 — Dashboard-Services (`dashboard/services/`, 2.173 LOC, 11 Files)

> Service-Layer zwischen Routes und Daten. Vision/Branding/Learning/Plans/Variants/Research.

| Datei | LOC | Hauptaufgabe |
|---|---|---|
| `__init__.py` | minimal | Package-Marker |
| `ai_vision.py` | 141 | Claude Vision + DALL-E (OpenAI) |
| `brand_extractor.py` | 126 | PDF → Brand-Knowledge via Claude |
| `image_branding.py` | 144 | PIL-basiertes Brand-Overlay-Rendering |
| `learning_service.py` | 614 | **Lernmaschine** — Signals + Meta-Analyse |
| `media_processor.py` | 114 | Bild-Pipeline-Orchestrator |
| `notification_service.py` | 91 | In-App-Notifs |
| `plan_service.py` | 305 | Subscription + Feature-Gates |
| `research_agent.py` | 139 | Claude Agent SDK → WebSearch + WebFetch |
| `supabase_sync.py` | 188 | Supabase-Submission-Import |
| `variant_service.py` | 321 | A/B/C-Variant-Generation + Schedules |

## `ai_vision.py` (141 LOC)

`AIVisionService.analyze_image(path)` Z.52–115:
- Claude-Call (Vision) — Eingabe-Bild + Brand-Context → JSON-Output mit `brand_fit_score` (0–10), `decision` (apply_branding|generate_dalle), `dall_e_prompt`, `suggested_caption_topics`
- Brand-Context aus `client/brand_knowledge.json` (Z.16, 64) — fallback Z.22–23

`generate_dall_e_image(prompt)` Z.117–140:
- OpenAI DALL-E 3 via `requests` POST `/v1/images/generations`
- Auth via `OPENAI_API_KEY` (im Code, nicht im `.env.example`)

## `brand_extractor.py` (126 LOC)

`BrandExtractor.extract_from_pdf(pdf_path)` Z.43–83:
- Lädt PDF, sendet base64 an Claude Vision
- Erwartet strukturierten JSON: `brand_name, industry, mission, values, usp, tone_keywords, content_pillars, target_audience`

`save_brand_knowledge(facts, source_filename)` Z.85–95 — schreibt `client/brand_knowledge.json` mit Metadaten:
```json
{ ..., "extracted_from": filename, "extracted_at": iso, "confirmed_by_user": false }
```

`load_brand_knowledge()` static Z.108–125 — fallback auf `brand.foerderkraft_brand.BRAND` wenn Datei fehlt.

## `image_branding.py` (144 LOC)

`ImageBrander.apply_branding(source, output, options)` Z.70–107:
1. Resize/Crop auf Plattform-Größe (`PLATFORM_SIZES` Z.55–62: IG 1080×1080, FB 1200×630, LinkedIn 1200×627, Twitter 1200×675, TikTok 1080×1920)
2. Unten Brand-Bar (18% Höhe) mit Akzent-Streifen
3. Logo-Paste oder Brand-Text-Drawing
4. JPEG-Save bei Quality 92

Brand-Farben aus `client/brand_knowledge.json` Z.42, Fallback Indigo-Palette Z.47.
Logo aus `brand/assets/logo.png` (Z.99) — optional.

## `learning_service.py` (614 LOC) — Herzstück

**`client/learning_profile.json`** ist die Persistenz-Datei. Threading-Lock-geschützt (Z.84–89).

### Signal-Quellen (alle in JSON gespeichert)

1. **`record_approval(post_id, platform, topic, variant_type, ai_score, content, note)`** Z.145–205
   - Append zu `approval_history` (max 200, Z.177)
   - Update `learned_patterns` (approval_rate, preferred_type, …)
   - Triggert Meta-Analyse alle `META_ANALYSIS_INTERVAL=20` Interaktionen (Z.197–202)

2. **`record_rejection(post_id, platform, topic, variant_type, reason_category, reason_text)`** Z.208–260
   - Topic geht nach 2× Ablehnung in `rejected_topics` (Z.234–239)
   - Stil-Hinweise extrahiert (Z.243–250)

3. **`record_rating(post_id, platform, variant_type, rating, content)`** Z.263–298 — ❤️/👍/✏️

4. **`record_performance(post_id, platform, topic, content, likes, comments, shares, reach, saves)`** Z.301–368
   - Top-Performer als Style-Vorbilder markiert (Z.348–359)

### Meta-Analyse (Z.373–438)

- Im Background-Thread (Z.200–202)
- Nimmt 5 beste Approval-Posts + 3 Top-Performer
- Claude (Haiku schnell) destilliert 4 Stil-Regeln
- Speichert in `style_analysis` + `style_analysis_at`

### `generate_intelligence_context(platform)` Z.443–547

Zentrale Funktion für alle Content-Gens. Baut human-readable Kontext:
- Approval-Rate, bevorzugter Variant-Type
- Häufigste Ablehnungsgründe → konkrete Anweisungen
- Top-Topics + zu vermeidende Topics
- Meta-Analyse-Stilregeln
- Mindestens 3 Interaktionen, sonst leerer String

→ Wird von `variant_service.generate_variants()` Z.195–198 in den Prompt injiziert.

## `media_processor.py` (114 LOC)

Pipeline-Klebstoff für Media-Upload:
1. Vision-Analyse (`AIVisionService.analyze_image`)
2. Decision:
   - `brand_fit_score >= 5` → `ImageBrander.apply_branding`
   - Sonst → DALL-E generieren oder Fallback auf Branding
3. Sidecar-Update + Queue-Manifest in `client/media/queue/<media_id>.json`

## `notification_service.py` (91 LOC)

Datei: `client/notifications.json`. Lock-geschützte CRUD:
- `push(notif_type, message, post_id, platform, scheduled_time, link)` — Dedup via (post_id + type)
- Rotation: Ungelesene unbegrenzt, Gelesene max 80 (Z.29)

## `plan_service.py` (305 LOC)

**PLANS-Dict** Z.19–60:

| Plan | Posts/Monat | Plattformen | DM-Handler | Vision | Research | Preis (laut Code) |
|---|---|---|---|---|---|---|
| trial | 30 | 3 | ❌ | ❌ | ❌ | Free 14d |
| starter | 150 | 3 | ❌ | ✅ | ❌ | €79/Mo |
| pro | ∞ | 5 | ✅ | ✅ | ✅ | €149/Mo |
| agency | ∞ | 5 | ✅ | ✅ | ✅ | €349/Mo |

**Funktionen:**
- `get_plan_info()` Z.109–161 — gibt Status + Limits zurück
- `can_generate()` Z.164–181 — Tuple `(allowed, reason)`
- `can_use_feature(feature)` Z.184–192
- `track_post_generated()` Z.195–200 — inkrementiert Zähler
- `activate_plan(...)` Z.203–228 — von Stripe-Webhook + License-Activate
- `deactivate_plan()` Z.231–238
- `validate_license_key(key)` Z.254–292 — HMAC-SHA256 Format `SZB-P-YYYYMM-XXXXXXXX`
- `generate_license_key(plan, year, month)` Z.295–304

**Storage:** `client/bot_settings.json` (Auto-Reset bei Monats-Wechsel, Z.129–139).

## `research_agent.py` (139 LOC)

Claude Agent SDK (`claude_agent_sdk`-Package). `run_research_sync()` Z.84–128:
- Async-Wrapper über anyio
- Agent mit Tools: WebSearch, WebFetch
- Max 10 Turns
- Output: 8 Content-Topics, gespeichert in `client/research_suggestions.json`
- Sendet Notification

## `supabase_sync.py` (188 LOC)

Pull-basierter Sync von Customer-Onboarding-Submissions:
1. `fetch_new_submissions()` Z.31–56 — `GET /rest/v1/onboarding_submissions?imported=false`
2. `import_submission(sub)` Z.80–162 — Mappt → `brand_knowledge.json` + `bot_settings.json`
3. `mark_imported(id)` Z.59–77 — `PATCH ?id=eq.<id>` `imported=true`
4. `sync_submissions()` Z.165–187 — vom Scheduler alle 5min aufgerufen

Auth: `SUPABASE_URL`, `SUPABASE_ANON_KEY` aus `.env`. Silent-fail wenn nicht konfiguriert (Z.53–55).

## `variant_service.py` (321 LOC)

Zwei Bereiche:

### Variants-Generation (`generate_variants(platform, topic, count=3)` Z.142–177)

3-Pack:
- **A** (Empfohlen): Standard-Winkel, Brand-fit-optimiert
- **B** (Alternativ): Anderer Winkel
- **C** (Frisch): Neues Thema komplett

Pro Variant: `variant_id` (uuid[:8]), `type`, `label`, `content`, `topic`, `ai_score (0..1)`, `selected: bool`.

**Scoring** Z.236–254 (heuristisch, **kein ML**):
- Basis 0.7
- Längen-Penalty -0.15 wenn > Limit×1.1
- Brand-Keywords +0.04 pro Match (max +0.2)
- Hashtags (IG/TikTok) +0.05

⚠️ **Hardcoded Brand-Keywords** Z.248: `["förderkraft", "drk", "rotes kreuz", "haustür", "außendienst", "spende", "förder"]` — sollte aus `brand_knowledge.json` kommen, ist aber für den Original-Kunden „Förderkraft" eingebrannt.

### Schedule + Pause-Mgmt

- `get_paused_platforms()` Z.79–81 → liest `bot_settings.json`
- `get_platform_schedules()` Z.119–121, `set_platform_schedule(p, days, times)` Z.124–134
- `get_generation_config()` Z.99–105, `set_generation_config(mode, hours_before)` Z.108–116

→ Wird von `bot/config.py:41-43` als bevorzugte Quelle für Scheduler-Config verwendet.

### Improve Variant (`improve_variant(platform, current_content, instruction)` Z.256–299)

Inline-Verbesserung via Claude. Wird aus Approval-UI gerufen.

## Cross-Service-Calls

| Caller-Service | Callee | Funktion |
|---|---|---|
| media_processor | ai_vision | analyze_image, generate_dall_e_image |
| media_processor | image_branding | apply_branding |
| variant_service | learning_service | generate_intelligence_context |
| research_agent | notification_service | push |
| supabase_sync | notification_service | push |
| supabase_sync | brand.foerderkraft_brand | invalidate_brand_cache |

## Verbundene Notes

- [[Socibot/modules/06-Dashboard-Routes]] — wer-ruft-wen
- [[Socibot/modules/14-Findings]] — Race Conditions, Hardcodes
- [[Socibot/modules/19-Connections]] — Dependency-Graph
