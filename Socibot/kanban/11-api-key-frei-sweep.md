---
id: 11
status: pending
priority: P0
blocked_by: []
tags:
  - socibot
  - customer-dod
  - api-key-frei
  - dod-blocker
created: 2026-04-29
---

# W0.75 — API-Key-Frei-Sweep

**Codex-vorgezogen** vor W0.5. Customer-DoD-Hard-Stop: Kunde darf KEINEN API-Key/Token mehr eingeben müssen. Token-Inputs raus, OAuth-Status-Badges + Coming-Soon-Cards rein.

## Warum P0 / Hard-Stop
Persona-A-Vertrauen: Anwälte/Steuerberater/Coaches stellen sich keine Tokens zusammen. Wenn UI nach API-Keys fragt, ist die Conversion verloren. **Vor W0.5** weil Setup/Auth-Pfade sonst zweimal angefasst werden.

## Acceptance

### Frontend (Templates)
- [ ] [marke.html](C:/Users/pc105/Desktop/Social%20media%20Bot/dashboard/templates/marke.html) Z.182-208: Claude-API-Key-Block komplett entfernen
- [ ] [marke.html](C:/Users/pc105/Desktop/Social%20media%20Bot/dashboard/templates/marke.html) Z.320-389: LinkedIn/Twitter/TikTok Token-Forms → Coming-Soon-Cards mit OAuth-CTA
- [ ] [marke.html](C:/Users/pc105/Desktop/Social%20media%20Bot/dashboard/templates/marke.html) Z.392-420: SMTP-Block in Operator-Only-Bereich verschieben (oder behalten als "Erweitert"-Section, nur Operator-Auth)
- [ ] [setup.html](C:/Users/pc105/Desktop/Social%20media%20Bot/dashboard/templates/setup.html) Z.213-225: Step 1 (Claude) komplett raus, Wizard beginnt bei Plattformen-Wahl
- [ ] [setup.html](C:/Users/pc105/Desktop/Social%20media%20Bot/dashboard/templates/setup.html) `PLATFORM_CONFIGS` für LinkedIn/Twitter/TikTok auf `oauth: true` (keine Token-Inputs mehr)
- [ ] [overview.html](C:/Users/pc105/Desktop/Social%20media%20Bot/dashboard/templates/overview.html) Z.173, 185: "Token einrichten" → "Plattformen verbinden", Warning-Banner umformulieren

### Backend (Routes/Services)
- [ ] [brand_settings.py](C:/Users/pc105/Desktop/Social%20media%20Bot/dashboard/routes/brand_settings.py): `_build_token_values()` auf SMTP-Keys reduziert (`NOTIFY_EMAIL`, `SMTP_EMAIL`, `SMTP_PASSWORD`)
- [ ] `save_token()`: `allowed_keys` auf SMTP-Keys reduziert
- [ ] `_test_claude()`, `_test_instagram()`, `_test_facebook()`: entfernt (Claude ist Operator, Meta ist OAuth)
- [ ] `_test_linkedin()`, `_test_twitter()`: behalten *temporär* solange noch .env-basiert (nach OAuth-Replacement entfernen)
- [ ] `/token-speichern` und `/token-testen` Routes: Auth-Gate für Operator-Only ODER auf SMTP-only-Scope reduziert

### .env.example
- [ ] LinkedIn/Twitter/TikTok-Tokens als `# DEPRECATED — ersetzt durch OAuth in Phase 1.3` markieren
- [ ] Klare Trennung Operator-zentral vs. Customer-Legacy

### UI-Wording
- [ ] Header "API-Zugänge verwalten" → "Verbundene Plattformen"
- [ ] "Trag deine Tokens in .env ein" → "Verbinde deine Konten per Klick"
- [ ] Tooltips, Help-Texts auf "Konto verbinden"-Sprache

## Risiken (aus Audit)
- **LinkedIn/Twitter Backend hängt noch an .env-Tokens** ([poster.py](C:/Users/pc105/Desktop/Social%20media%20Bot/bot/poster.py) Z.94-140) — wenn UI weg + kein OAuth, fallen Posts aus. Mitigation: solange Phase 1.3 (LinkedIn/Twitter OAuth) nicht da ist, Plattformen automatisch auf `paused` setzen oder Operator stellt Tokens manuell in .env ein
- **TikTok ist Dead-Code**, sofort entfernbar ([poster.py](C:/Users/pc105/Desktop/Social%20media%20Bot/bot/poster.py) Z.247-253 returnt immer Stub-Error)
- **Meta legacy-fallback** in `_build_token_status()`: bleibt als Backup (OAuth-priority, .env-fallback) — kein Risiko

## Migrations-Reihenfolge (aus Audit-Report)
1. Claude-Block aus marke.html + setup.html (sicherste Änderung, kein Backend-Impact)
2. setup.html PLATFORM_CONFIGS auf `oauth: true` für LI/X/TT
3. marke.html LI/X/TT-Sections durch Coming-Soon-Cards ersetzen
4. brand_settings.py `_build_token_values()` bereinigen
5. brand_settings.py `save_token()` `allowed_keys` reduzieren
6. brand_settings.py `_test_*` für Claude/IG/FB entfernen
7. overview.html Wording aktualisieren

## Test-Plan
- [ ] Manueller UI-Test: kein Token-Input-Feld mehr im Customer-Flow sichtbar
- [ ] LinkedIn/Twitter via .env (Operator-Setup) postet weiterhin
- [ ] TikTok-Removal bricht keinen Test
- [ ] `/token-speichern` ohne Auth gibt 401/403
- [ ] Wizard-Flow funktioniert ohne Step 1

## Skills
- [socibot-design](C:/Users/pc105/.claude/skills/socibot-design/) für Coming-Soon-Cards (Catppuccin-Mocha)
- [design-review](C:/Users/pc105/.claude/skills/design-review/) nach UI-Changes
- [security-dsgvo-reviewer](C:/Users/pc105/.claude/agents/security-dsgvo-reviewer.md) Pflicht (auth-gating)
