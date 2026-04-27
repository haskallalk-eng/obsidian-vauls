---
title: Phonbot — Preisgestaltung (Stand Code)
type: reference
tags: [phonbot, pricing, plans, billing]
created: 2026-04-22
source: apps/api/src/billing.ts PLANS
---

# Phonbot — Preisgestaltung

> **Ground Truth:** [apps/api/src/billing.ts `PLANS`](../../.openclaw/workspace/voice-agent-saas/apps/api/src/billing.ts). Diese Note ist ein Read-only-Abzug, der regelmäßig gegen den Code geprüft werden sollte. Bei Drift: Code gewinnt, Note nachziehen.

## Plan-Matrix

| Plan | ID | Preis/Monat | Min inklusive | Überschuss/Min | Agenten | Stripe-Env |
|---|---|---:|---:|---:|---:|---|
| **Free** | `free` | 0 € | 30 | _gesperrt_ | 1 | — |
| **Nummer** | `nummer` | 8,99 € | 70 | 0,22 € | 1 | `STRIPE_PRICE_NUMMER` / `STRIPE_PRICE_NUMMER_YEARLY` |
| **Starter** | `starter` | 79 € | 360 | 0,22 € | 1 | `STRIPE_PRICE_STARTER` / `STRIPE_PRICE_STARTER_YEARLY` |
| **Professional** | `pro` | 179 € | 1.000 | 0,20 € | 3 | `STRIPE_PRICE_PRO` / `STRIPE_PRICE_PRO_YEARLY` |
| **Agency** | `agency` | 349 € | 2.400 | 0,15 € | 10 | `STRIPE_PRICE_AGENCY` / `STRIPE_PRICE_AGENCY_YEARLY` |

Alle Preise sind **netto**. Abrechnung sekundengenau (Retell rundet auf volle Sekunden, Stripe rechnet in vollen Minuten — Differenz-Reconciliation siehe `usage.ts` + `retell-webhooks.ts`).

## Wie die Minuten wirklich laufen

1. **Reservierung vor dem Call** — `tryReserveMinutes(orgId, 5)` ([usage.ts:119-153](../../.openclaw/workspace/voice-agent-saas/apps/api/src/usage.ts#L119)) reserviert einen Block von 5 Minuten atomar. Blockiert den Call wenn Plan-Status `incomplete`/`past_due`/`paused`/`canceled` ist oder wenn `minutes_used + 5 > minutes_limit` UND der Plan nicht in den `paidPlans` liegt (dann Overage zulässig).
2. **Reconciliation nach dem Call** — `retell-webhooks.ts:186` ruft `reconcileMinutes(orgId, reserved, actual, agentId)` auf. Differenz `actual − reserved` wird auf `orgs.minutes_used` verrechnet.
3. **Overage** — pro Plan definierter `overchargePerMinute` (nur für `nummer/starter/pro/agency`). Free blockiert bei 30 min ganz.
4. **Perioden-Reset** — bei Subscription-Renewal setzt `syncSubscription` `minutes_used = 0` ([billing.ts:261](../../.openclaw/workspace/voice-agent-saas/apps/api/src/billing.ts#L261)).

## Premium-Voice-Surcharge

Unabhängig vom Plan: Calls mit dem ElevenLabs-Hassieb-Kalla-Clone (`custom_voice_5269b3f4732a77b9030552fd67`) kosten **zusätzlich 0,05 €/Min** oben drauf. Siehe `voice-catalog.ts` → `surchargePerMinute: 0.05` und `chargePremiumVoiceMinutes()` in `billing.ts`. Cartesia-Original-Voice hat keinen Aufschlag.

Also bei einer durchschnittlichen 3-min-Unterhaltung: Plan-Minutenpreis + 0,15 € Aufschlag wenn Premium-Voice. Cost-Prognose im Obsidian-Audit aus April 2026 rechnet damit.

## Front-End-Quellen (sollen die Tabelle oben spiegeln)

- Landing Preise: [apps/web/src/ui/landing/shared.ts `PLANS`](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/landing/shared.ts) → wird auf [apps/web/src/ui/landing/PricingSection.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/landing/PricingSection.tsx) gerendert
- Authed-Billing-Tab: [apps/web/src/ui/BillingPage.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/BillingPage.tsx) (feature-Liste pro Plan, wird aus Backend-`/billing/plans` gefüllt)
- Onboarding-Wizard Plan-Step: [apps/web/src/ui/onboarding/OnboardingWizard.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/onboarding/OnboardingWizard.tsx) (Starter / Pro / Agency Cards)
- Branchen-Landing-Pages: [scripts/gen-landing-pages.mjs](../../.openclaw/workspace/voice-agent-saas/scripts/gen-landing-pages.mjs) → pro Branche hart kodiert in `value.roi`

**Drift-Risiko:** die Branchen-Landings haben die Preise/Minuten **hart reingeschrieben**. Jede Plan-Änderung im Backend muss dort nachgezogen werden. Am 2026-04-22 aufgeräumt (war fälschlich `Starter 49 €/500 Min` und `Pro 149 €/2.000 Min`).

## Welche Branche auf welchen Plan läuft (Empfehlungen auf den Landings)

Stand [gen-landing-pages.mjs](../../.openclaw/workspace/voice-agent-saas/scripts/gen-landing-pages.mjs) BRANCHEN-Array nach 2026-04-22:

| Branche | Empfohlener Plan | ROI-Scenario | Ersparnis p.M. |
|---|---|---|---:|
| Friseur | **Starter** · 79 € · 360 Min | 300 Calls / Monat, ø 1,2 Min | 1.421 € |
| Handwerker | **Pro** · 179 € · 1.000 Min | 200 Calls / Monat, Notdienst-heavy | 1.821 € |
| Arztpraxis | **Pro** · 179 € · 1.000 Min | 500 Calls / Monat, Rezepte + Termine | 1.621 € |
| Reinigung | **Starter** · 79 € · 360 Min | 150 Anfragen / Monat | 1.721 € |
| Restaurant | **Starter** · 79 € · 360 Min | 400 Calls / Monat, Reservierung | 1.621 € |
| Autowerkstatt | **Pro** · 179 € · 1.000 Min | 250 Calls / Monat, Diagnose-heavy | 1.621 € |

Ersparnis = Alternative-Personalkosten (Teilzeit-Rezeption/MFA/Bürokraft ~1.500–2.000 €) minus Plan-Preis.

## Marketing-Tagline (verbindlich)

- Branchen-Landing Header: **„Ab 8,99 €/Monat"** (= Nummer-Plan, der günstigste zahlende Plan mit eigener Nummer)
- Hero-CTA Badge: **„30 Freiminuten"** (Free-Plan-Quota — was User ohne Kreditkarte testen können)
- _Nicht verwenden:_ „Ab 49 €" (alter falscher Starter-Preis), „100 Freiminuten" (war nie in Code)

## Änderungen nachziehen — Checkliste

Wenn im Backend (`billing.ts PLANS`) ein Preis / eine Minute / ein Plan-Name geändert wird:

1. [ ] `apps/web/src/ui/landing/shared.ts PLANS` angleichen
2. [ ] `apps/web/src/ui/BillingPage.tsx` Feature-Strings prüfen (z.B. „360 Minuten / Monat")
3. [ ] `apps/web/src/ui/onboarding/OnboardingWizard.tsx` Plan-Cards prüfen
4. [ ] `scripts/gen-landing-pages.mjs` BRANCHEN[*].value.roi[1] pro Branche anpassen + Ersparnis neu berechnen
5. [ ] `scripts/gen-landing-pages.mjs` description + subtitle Taglines prüfen (aktuell „Ab 8,99 €/Monat")
6. [ ] `node scripts/gen-landing-pages.mjs` + `node scripts/sync-legal-nav.mjs`
7. [ ] Stripe-Dashboard: neue Price-Objekte anlegen + `apps/api/.env` Variablen aktualisieren (`STRIPE_PRICE_*`)
8. [ ] Diese Note (`Pricing.md`) aktualisieren

## Quellen

- Code-Wahrheit: [apps/api/src/billing.ts](../../.openclaw/workspace/voice-agent-saas/apps/api/src/billing.ts)
- Deep-Audit (2026-04-18): [[Audit-2026-04-18-Deep]] Cost-Prognose-Abschnitt
- Gesamtsystem §4.5: [[Phonbot-Gesamtsystem#4-5-Stripe-Abo-Minuten-Tracking]]
