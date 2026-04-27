---
tags: [project, phonbot, audit, security, business]
status: active
created: 2026-04-18
type: deep-audit
audit_scope: architecture + security + dsgvo + cost + scaling
---

# Phonbot Deep Audit — 2026-04-18

> 3 parallele Audits (Architektur, Security/DSGVO, Cost/Scale) + Cross-Check-Verifikation der Top-Findings im Code.

Link: [[Overview|Phonbot Overview]] · [[../Daily/2026-04-18|Daily]]

---

## 🔴 VERIFIZIERTE CRITICALS — SOFORT handeln

### C1. Alle Production-Secrets im Klartext auf Dev-Rechner
**File:** `apps/api/.env`
**Agent hat die Datei gelesen** → DB-Passwort, Twilio Auth-Token, OpenAI Key, Retell Key, Resend, Google/Microsoft OAuth Secrets, LiveKit, Deepgram, ElevenLabs, Stripe Webhook Secret.
**Fix:** ALLE 12 Keys rotieren. Dann Secret-Manager (1Password/Vault). Pre-commit-Hook `gitleaks` installieren.

### C2. Silent-Swallow `.catch(() => {})` — 51 Vorkommen in 21 Dateien
**Verifiziert:** `51 total occurrences` (Agent meldete 36 — tatsächlich schlimmer).
Betroffen u.a.: auth.ts (7x), calendar.ts (6x), insights.ts (8x), AdminPage.tsx (6x).
**Impact:** Fehler sind für Sentry unsichtbar → Silent-Production-Incidents.
**Fix:** Jeder `.catch(() => {})` → `.catch(err => app.log.warn({ err }, 'context'))` ODER explizit kommentieren warum intentional.

### C3. Twilio Webhook-Signatur fehlt auf TwiML/Status-Callback
**Verifiziert:** grep nach `validateRequest` / `x-twilio-signature` → **0 files**.
**File:** `apps/api/src/twilio-openai-bridge.ts:141, 166`
**Impact:** Angreifer mit Session-UUID kann CallStatus faken → Billing-Manipulation.
**Fix:** `twilio.validateRequest()` in beiden Routes.

---

## 🟠 HIGH — vor Launch

### H1. CAPTCHA fail-open bei leerem Token (intentionaler Tradeoff)
**File:** [captcha.ts:64-67](../../.openclaw/workspace/voice-agent-saas/apps/api/src/captcha.ts)
Der Code lässt leere Tokens durch (dokumentierter Kompromiss wegen Ad-Blocker-UX). Primary Defense ist Rate-Limit + hourly global-cap (200). Security-Agent flagged als Critical, aber **der Entwickler hat das bewusst so gebaut**.
**Entscheidung:** OK lassen wenn globaler Cap + DACH-Whitelist greift. Monitoring auf "empty token"-Logs einrichten.

### H2. Redis ohne Passwort (aber Netzwerk-isoliert)
**docker-compose.yml:** Redis nur im Docker-Netzwerk, kein public-port. Comment am Top: "only Caddy is exposed". Kein Panic-Case, aber Defense-in-Depth fehlt. **Fix:** `--requirepass` in compose-file ergänzen.

### H3. DSGVO — fehlende Sub-Processor in Datenschutzerklärung
**File:** `apps/web/src/ui/LegalModal.tsx`
Fehlen: **Twilio, OpenAI, Cloudflare Turnstile**. OpenAI verarbeitet ganze Call-Transcripts → Art. 28 Pflicht.
**Bußgeldrisiko:** bis 10 Mio € / 2% Jahresumsatz (Art. 83 Abs. 4).
**Fix:** SCCs/AVV formal mit allen 3 abschließen + Datenschutzerklärung ergänzen.

### H4. § 201 StGB — kein Recording-Hinweis im Agent-Prompt
Retell nimmt Calls auf, aber `buildAgentInstructions()` enthält keinen Hinweis am Gesprächsanfang. **Strafbar bis 3 Jahre Freiheitsstrafe.**
**Fix:** Erste Prompt-Instruction: "Dieses Gespräch wird aufgezeichnet und von einem KI-System verarbeitet."

### H5. God-Object: calendar.ts (1745 Zeilen)
258 Top-Level Items, zyklomatische Komplexität >>50.
**Fix:** Split in 4 Module (google/microsoft/cal-com/core).

### H6. Test-Coverage ~6% (9 Test-Files für 154 Source-Files)
**Impact:** Refactors = Blind-Flight. Billing/Webhooks/Phone ungetestet.
**Fix:** Ziel 50% Coverage für kritische Paths; CI-Gate.

---

## 🟡 MEDIUM — Backlog 30 Tage

- **M1:** `billing.ts:374-378` Stripe paused/resumed liest `sub.metadata.orgId` ohne DB-Cross-Check (andere Cases machen es richtig)
- **M2:** `learning-api.ts:18-28` fehlt `aud`-Claim-Check (nur `payload.admin`)
- **M3:** Insights/Conversation-Patterns speichern PII aus Transcripts ohne `redactPII()`
- **M4:** Kein Account-Lockout nach N Fehlversuchen (nur IP-Rate-Limit)
- **M5:** Fehlende DB-Indizes auf `org_id`-Spalten (agent_configs, calendar_connections, tickets)
- **M6:** Retell `call_ended` Webhook ohne Idempotency — Duplicate reconcile möglich
- **M7:** React: 302 useState vs. nur 29 useMemo/useCallback — Re-Render-Spam
- **M8:** OnboardingWizard.tsx (1159 Zeilen) + 17 useState in einer Komponente
- **M9:** `.env`-Vars nicht via Zod validiert (Tippfehler = Runtime-Crash)
- **M10:** Transcripts unverschlüsselt at-rest (AES-256-GCM nur für OAuth)

---

## 💰 BUSINESS / COST-PROGNOSE

### Pricing-Modell (verifiziert in billing.ts:24-67)
| Plan | €/Mo | Min/Mo | Overage €/Min | Rohmarge* |
|------|------|--------|---------------|-----------|
| Free | 0 | 30 | 0 | N/A (Akquisition, -€2.40) |
| Nummer | 8.99 | 70 | 0.22 | **38% — knapp** |
| Starter | 79 | 360 | 0.22 | **64% ✓** |
| Pro | 179 | 1000 | 0.20 | **55% ✓** |
| Agency | 349 | 2400 | 0.15 | **45% ✓** |

\*Rohmarge bei ~€0.080 COGS/Min (Retell + OpenAI + Twilio)

### 3 Szenarien
| Szenario | MRR | Variable Kosten | Fix | Ergebnis |
|----------|-----|-----------------|-----|----------|
| **A: 10 Kunden × 500 Min** | €1.630 | €440 | €3.000 | **−€1.810 (loss)** |
| **B: 100 Kunden × 1000 Min** | €14.660 | €8.367 | €2.914 | **+€3.379 (23% Marge)** ✓ |
| **C: 1000 Kunden × 2000 Min** | €169.050 | €164.226 | €6.050 | **−€1.226** 🔴 |

**Kritische Einsicht:** Bei 1000 Kunden explodieren die COGS linear (Retell-Preise), während Umsatz nur sub-linear wächst (Plan-Mix). **Aktuelles Pricing skaliert nicht über 200–300 Kunden profitabel.**

### Break-Even
~**25 Pro-Plan-Kunden** ODER **40 Starter-Kunden** → ~€4.700 MRR.

---

## 🧨 SCALING-BOTTLENECKS (Priorisiert)

1. **Postgres Connection Pool** — 20 Slots; bricht bei ~100 concurrent Calls. Fix: PgBouncer + Supabase Pro (€100/mo).
2. **Redis Memory** — Dedup-Keys mit 30d-TTL → 1 Mio Keys/Monat. Fix: TTL auf 24h reduzieren oder Upstash Pro (€50/mo).
3. **Fastify Single-Thread** — kein Cluster-Mode. Webhook-Spikes = Queue-Backlog. Fix: PM2 Cluster + Bull-Queue.
4. **Twilio Pool** — MAX_POOL_SIZE=3 Nummern. Fix: auf 10 erhöhen.
5. **Retell Webhook ohne Idempotency** — Duplicate `call_ended` → doppelte Abrechnung. Fix: `retell_processed_events` Tabelle.

---

## ⚠️ BUSINESS-RISIKEN

1. **Vendor-Lock-In Retell** — 100% Dependency; Migration ~€50k. Mitigation: Volume-Discount verhandeln.
2. **Toll-Fraud trotz DACH-Whitelist** — kein per-Org Daily-Cap für Paid-Kunden (nur Demo geschützt). Potenzial-Schaden €5–20k/Incident.
3. **Chargebacks** — Voice-Quality ist subjektiv; Stripe-Risk bei >2% Rate.
4. **Retell-Outage = Komplett-Downtime** — kein Fallback implementiert. Worst-case Uptime: 99.7%.
5. **OpenAI EU-Transfer** — US-Company, SCC nötig, ggf. Schrems-III-Risiko bei Policy-Änderung.

---

## 📊 SCORES
- **Security-Score:** 7.5/10 (Solide Basics, aber P0 Secrets + P1 Twilio-Sig)
- **DSGVO-Score:** 5/10 (Sub-Processor unvollständig, Recording-Hinweis fehlt, Transcript-Encryption fehlt)
- **Code-Quality:** 6/10 (funktional, aber Monolith-Files + 6% Tests)
- **Business-Modell:** 7/10 (solide bis 200 Kunden, über 500 braucht Pricing-Revision)

---

## 🎯 TOP-5 NEXT STEPS (Reihenfolge)

1. **Secrets rotieren** (heute, 2h) — alle 12 Credentials
2. **Twilio Webhook-Signatur** (1h) — `validateRequest` in `twilio-openai-bridge.ts`
3. **51 Silent-Catch fixen** (4–6h) — structured logging überall
4. **DSGVO: Sub-Processor + Recording-Hinweis** (1 Tag) — LegalModal.tsx + agent-instructions.ts
5. **Per-Org Daily-Call-Cap** (3h) — Toll-Fraud-Schutz für Paid-Kunden

**Geschätzter Gesamtaufwand P0+P1:** ~3 Arbeitstage

---

## Verwandt

- [[Overview|Phonbot Overview]] · [[Phonbot-Gesamtsystem|🧭 Gesamtsystem]]
- **Spätere Audit-Durchläufe:** [[Audit-2026-04-18-Bugs|Audit 2: Bug-Hunt]] · [[Audit-2026-04-18-Postfix|Audit 3: Post-Fix]] · [[Audit-2026-04-18-Final|Audit 4: Final]]
- **Betroffene Module:**
  - C1 Secrets / H2 Redis → [[modules/Backend-Infra]] · [[modules/Shared-Infra-Tests]]
  - C2 Silent-Catch → alle Module (insb. [[modules/Backend-Auth-Security]], [[modules/Backend-Comm-Scheduling]], [[modules/Backend-Insights-Admin]])
  - C3 Twilio-Signatur / H4 Recording-Hinweis → [[modules/Backend-Voice-Telephony]] · [[modules/Backend-Agents]]
  - H3 Sub-Processor / DSGVO → [[modules/Frontend-Shell]] (LegalModal)
  - H5 God-Object calendar.ts → [[modules/Backend-Comm-Scheduling]]
  - H6 Test-Coverage → [[modules/Shared-Infra-Tests]]
  - M2 `learning-api.ts` aud-Gap / M3 PII-Patterns → [[modules/Backend-Insights-Admin]]
  - M5 DB-Indizes → [[modules/Backend-Database]]
  - M6 Retell-Idempotency → [[modules/Backend-Voice-Telephony]]
  - M10 Transcript-Encryption → [[modules/Backend-Voice-Telephony]] · [[modules/Backend-Auth-Security]]
- [[../Daily/2026-04-18|Daily 2026-04-18]]
- Code-Root: `C:/Users/pc105/.openclaw/workspace/voice-agent-saas`
