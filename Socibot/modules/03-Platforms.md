---
title: 03 — Platforms
tags: [socibot, modul, platforms]
date: 2026-04-27
source_of_truth: code
---

# 03 — Platforms (`platforms/`, 1.036 LOC, 16 Files)

> 5 Plattformen × `<platform>_api.py` (REST-Wrapper) + `<platform>_content.py` (Claude-Content-Generator) + leeres `__init__.py`.

## File-Map

| Plattform | API-Wrapper (LOC) | Content-Gen (LOC) | Status |
|---|---|---|---|
| Instagram | `instagram_api.py` (114) | `instagram_content.py` (112) | ✅ Production |
| Facebook | `facebook_api.py` (105) | `facebook_content.py` (103) | ✅ Production |
| LinkedIn | `linkedin_api.py` (92) | `linkedin_content.py` (124) | ✅ Production |
| Twitter/X | `twitter_api.py` (102) | `twitter_content.py` (118) | ✅ Production |
| TikTok | `tiktok_api.py` (73) | `tiktok_content.py` (103) | ⚠️ **Stub** — Upload nur 2-stufig init, kein Chunk-Upload |

## Inkonsistente API-Schnittstellen

Es gibt **kein gemeinsames Interface**. `Poster` (`bot/poster.py:104–117`) macht Switch-Case pro Plattform.

| Funktion | IG | FB | LinkedIn | Twitter | TikTok |
|---|---|---|---|---|---|
| Text-Post | ❌ | `post_text()` Z.22 | `post_text()` Z.18 | `post_tweet()` Z.22 | ❌ |
| Image-Post | `post_image()` Z.24 | `post_with_image()` Z.32 | `post_with_image()` Z.37 | ❌ | ❌ |
| Video-Post | `post_reel()` Z.48 | ❌ | ❌ | ❌ | `upload_video()` Z.19 (Stub) |
| Get Comments | Z.72 | Z.54 | Z.60 | ❌ | Z.53 |
| Reply Comment | Z.81 | Z.64 | Z.66 | ❌ | ❌ |
| Get Mentions | Z.87 | ❌ | ❌ | Z.39 | ❌ |
| Send DM | Z.96 (nutzt FB-Endpoint!) | Z.84 | Z.76 | Z.62 | ❌ |
| Insights | Z.106 | `get_page_insights()` Z.95 | ❌ | `get_tweet_metrics()` Z.94 | `get_video_insights()` Z.64 |

**Auffälligkeit Instagram-DM:** `instagram_api.py:96–103` ruft `https://graph.facebook.com/v18.0/me/messages` (FB-Endpoint, nicht Instagram). Cross-Plattform-Token-Gleichheit erforderlich.

## REST-API-Endpoints (verifiziert)

| Plattform | Base-URL | Auth |
|---|---|---|
| Instagram | `https://graph.instagram.com/v18.0` | Bearer `INSTAGRAM_ACCESS_TOKEN` |
| Facebook | `https://graph.facebook.com/v18.0` | Bearer `FACEBOOK_ACCESS_TOKEN` |
| LinkedIn | `https://api.linkedin.com/v2` | Bearer `LINKEDIN_ACCESS_TOKEN` |
| Twitter | `https://api.twitter.com/2` | OAuth1 (4 Felder) + Bearer für Read |
| TikTok | `https://open.tiktokapis.com/v2` | Bearer `TIKTOK_ACCESS_TOKEN` |

## Content-Generators — konsistentes Muster

Jeder `<platform>_content.py` exportiert (verifiziert über alle 5):
- `__init__(api_key)` — Anthropic-Client + Brand-Voice via `brand.foerderkraft_brand.get_brand_context(platform)` + `get_platform_voice(platform)`
- `generate_post()` / `generate_caption()` / `generate_tweet()` — Haupt-Content
- `reply_to_comment()` + `reply_to_dm()` — Engagement
- Plattform-Spezialisierungen: IG `generate_hashtags()` (Z.97); LinkedIn `generate_outreach_message()` (Z.41), `generate_job_post()` (Z.101); Twitter `generate_thread()` (Z.37), `generate_sales_tip()` (Z.97); TikTok `generate_video_script()` (Z.11), `generate_content_ideas()` (Z.61); FB `generate_ad_copy()` (Z.79)

## Claude-Calls inventarisiert (insgesamt 25)

Alle nutzen `bot.constants.CLAUDE_MODEL` (`"claude-sonnet-4-6"`).

| File | Funktion | Zeile | Max Tokens |
|---|---|---|---|
| `instagram_content.py` | caption | 34–38 | 600 |
| `instagram_content.py` | story | 52–56 | 100 |
| `instagram_content.py` | reply_to_comment | 70–74 | 100 |
| `instagram_content.py` | reply_to_dm | 90–94 | 300 |
| `instagram_content.py` | hashtags | 106–110 | 200 |
| `facebook_content.py` | post | 34–38 | 600 |
| `facebook_content.py` | reply_to_comment | 52–56 | 150 |
| `facebook_content.py` | reply_to_dm | 72–76 | 300 |
| `facebook_content.py` | ad_copy | 97–101 | 300 |
| `linkedin_content.py` | post | 34–38 | 700 |
| `linkedin_content.py` | outreach | 56–60 | 150 |
| `linkedin_content.py` | reply_to_comment | 74–78 | 150 |
| `linkedin_content.py` | reply_to_dm | 94–98 | 300 |
| `linkedin_content.py` | job_post | 118–122 | 600 |
| `twitter_content.py` | tweet | 30–34 | 150 |
| `twitter_content.py` | thread | 54–58 | 800 |
| `twitter_content.py` | mention_reply | 72–76 | 100 |
| `twitter_content.py` | dm_reply | 90–94 | 150 |
| `twitter_content.py` | sales_tip | 112–116 | 100 |
| `tiktok_content.py` | video_script | 35–39 | 800 |
| `tiktok_content.py` | caption | 54–58 | 200 |
| `tiktok_content.py` | content_ideas | 79–83 | 800 |
| `tiktok_content.py` | comment_reply | 97–101 | 80 |
| `dm_handler.py` (cross) | intent_detection | 141–145 | 30 |
| `dm_handler.py` (cross) | response_gen | 219–223 | 300 |

**Kein Retry-Layer um Anthropic-Calls** — wenn API-Limit oder Timeout, fliegt Exception bis zum Scheduler hoch (silent-catch dort, log.error).

## Längen-Constraints (Plattform-spezifisch, hardcoded in Prompts)

- IG Caption max 300 Wörter
- IG Story max 50 Wörter
- IG Hashtags 15 default, 8–10 thematisch
- FB Post max 400 Wörter
- LinkedIn Post max 1300 Zeichen
- LinkedIn Outreach max 300 Zeichen
- LinkedIn Comment max 2 Sätze
- Twitter Tweet max 255 Zeichen (paranoides Limit, eigentlich 280)
- Twitter Thread Tweet max 260 Zeichen
- Twitter Mention-Reply max 200 Zeichen
- TikTok Caption max 150 Zeichen
- TikTok Default Ideas-Count 10

## TikTok-Stub Details

`tiktok_api.py:19–41` — `upload_video`:
1. ✅ POST `/post/publish/video/init/` (Init-Schritt) implementiert
2. ❌ Chunk-Upload (PUT zu Upload-URL) **fehlt**
3. ❌ Publish-Schritt fehlt

→ TikTok-Posts werfen `{success: False, error: "Video-Upload noch nicht implementiert"}` (`bot/poster.py:178-180`).

## Verbundene Notes

- [[Socibot/modules/02-Bot-Core]] — Poster + Scheduler, die Plattform-APIs aufrufen
- [[Socibot/modules/09-Brand-System]] — `get_brand_context()` + `get_platform_voice()`, von allen Content-Gens benutzt
- [[Socibot/modules/14-Findings]] — Inkonsistenz-Risiken
