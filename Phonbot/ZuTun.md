---
title: Phonbot — ZuTun
tags: [phonbot, todo, backlog]
created: 2026-04-21
status: unbearbeitet
note: Sammelnote für offene Aufgaben — wird bei Bedarf in GitHub-Issues überführt
---

# Phonbot — ZuTun

> Unsortierte Liste offener Aufgaben. Noch nicht als GitHub-Issues angelegt — erst beim Umsetzen zu Issues konvertieren.

## 1. Branchen-Seite

### 1.2 Arzt-Branche (Arztpraxis) freischalten — DSGVO-Art.-9-Hürde
- Gesundheitsdaten = **besondere Kategorie** personenbezogener Daten (DSGVO Art. 9). Strengere Anforderungen als die anderen Branchen.
- Braucht:
  - [ ] Explizite Einwilligung im Call-Flow ("Ihr Anruf wird aufgezeichnet und zur Terminbuchung verarbeitet …")
  - [ ] AV-Vertrag mit jedem Arzt-Kunden (Art. 28 DSGVO)
  - [ ] Klärung ob Retell/Twilio/OpenAI als Auftragsverarbeiter für Gesundheitsdaten geeignet sind (Standardvertragsklauseln + TIA für US-Transfers)
  - [ ] Medizinisches Vokabular in System-Prompt (Symptome nicht interpretieren, nur terminieren)
  - [ ] Evtl. zusätzliche Verschlüsselung der Transkripte (aktuell AES-256-GCM nur für OAuth-Tokens)
  - [ ] Opt-in-Schalter pro Org "Gesundheitsdaten-Branche" mit expliziter Warnung im Admin-UI

## 2. Mobile-Optimierung (Handy)
- [ ] Landing-Pages auf iPhone SE (kleine Screens) prüfen
- [ ] Dashboard auf Handy bedienbar machen (aktuell Desktop-first)
- [ ] Chipy-Copilot-Chat auf Handy (Viewport, Scroll, Tastatur überdeckt nichts)
- [ ] Touch-Targets ≥ 44 px (Apple HIG)
- [ ] `<meta viewport>` prüfen + `viewport-fit=cover` für Notch
- [ ] Landscape-Modus testen

## 3. Rollen spezifizieren + Sinn geben
- Aktuell gibt es `role` im JWT-Payload (siehe `apps/api/src/auth.ts`) — aber unklar welche Rollen es gibt und was sie dürfen.
- Zu klären:
  - [ ] Welche Rollen? (owner / admin / member? viewer?)
  - [ ] Rechte-Matrix: Wer darf Agenten deployen, wer darf Billing sehen, wer darf Calls lesen?
  - [ ] Frontend-Gating pro Rolle (Sidebar-Einträge ein-/ausblenden)
  - [ ] Invite-Flow: Wie werden Team-Mitglieder hinzugefügt?
  - [ ] Backend-`requireRole()` als echter Decorator (aktuell sind Rollen-Checks inline, nicht DRY — siehe [[modules/Backend-Auth-Security]])

## 4. Agent-Tools für alle Agents verfügbar machen
- **Problem:** Outbound- und Inbound-Agent haben aktuell unterschiedliche Tool-Sets und parallel existierende Prompt-Pfade.
- [[modules/Backend-Agents]] dokumentiert: `buildRetellTools()` (Retell Custom-Tools, für Inbound + authed Web-Call) vs. `getOpenAITools()` (OpenAI-Functions, für Twilio-OpenAI-Bridge-Callback-Pfad).
- [[modules/Backend-Outbound]] dokumentiert: `/outbound/website-callback` nutzt den hardcodierten `CALLBACK_PROMPT` (twilio-openai-bridge.ts), nicht die normale `agent_configs`-Pipeline.
- Ziel: **Jeder Agent (inbound, outbound, web-call) muss dieselben Tools bekommen** — `calendar.findSlots`, `calendar.book`, `ticket.create`, `transfer_call`.
- Zu klären:
  - [ ] Einheitlicher Tool-Katalog pro Agent (Quelle: `agent_configs.tools`?)
  - [ ] Inbound + Web-Call: OK (über `agent-runtime.ts`)
  - [ ] Outbound-authed-Path: prüfen ob `buildRetellTools` übergeben wird
  - [ ] Outbound-Website-Callback: Umstellung auf normale Agent-Pipeline (statt hardcoded Prompt ohne Tools)
  - [ ] Tool-Dispatch-Normalisierung (`sanitizeToolName` vs. `normalizeIncomingToolName` — siehe agent-tools.ts:109)

## 5. 🐛 Bug: Kalender-Eintrag funktioniert nicht
- Symptom: Agent bestätigt Termin im Call, aber es landet kein Eintrag in Google Calendar / Outlook / Cal.com.
- Zu prüfen:
  - [x] Retell-Webhook `calendar.book` kommt wirklich an? Tools sind für alle Agenten erzwungen und bestehende Retell-LLMs synchronisiert.
  - [x] `decryptConn()` schlägt evtl. silent fehl wenn `ENCRYPTION_KEY` rotiert wurde — Audit-Round-3 (`c549aab`) ersetzt `process.stderr.write` durch `log.error({orgId, provider, field}, 'token decrypt failed (key rotated?)')` → Sentry sieht den Spike.
  - [ ] `calendar_connections.api_key` / Refresh-Tokens gültig?
  - [x] Upstream-API-Response wird geloggt? (nicht nur silent-catch) — Audit-Round-3: Google + Microsoft Token-Refresh-Catches loggen jetzt `log.warn({err, orgId, provider}, 'token refresh failed — connection likely needs reconnect')`. Vorher 5 Monate stille 403er, jetzt strukturiert in Sentry.
  - [x] Zeitzone/Slot-Vertrag: Ohne externe Kalender nutzt der Agent Chipy. Mit externen Kalendern wird nur ein Slot angeboten, wenn Chipy UND jeder externe Kalender frei sind; gebucht wird nur erfolgreich, wenn jeder externe Kalender akzeptiert, danach Chipy.
  - [ ] Auf Prod reproduzieren mit einem Test-Call + Trace-ID

## 6. 🐛 Bug: Kalender-Fehler → kein Fallback auf Ticket via Chipy
- Symptom: Wenn `calendar.book` scheitert, sollte der Agent (Chipy) automatisch ein **Rückruf-Ticket** erstellen mit Kontext + Kundendaten — passiert aktuell nicht.
- Das ist ein zentraler UX-Punkt: "Never drop a customer" = wenn der Kalender down ist, muss wenigstens ein Ticket rausfallen.
- Zu implementieren:
  - [x] In `agent-tools.ts` / `agent-instructions.ts`: bei Tool-Fehler-Response "fall back to ticket.create with full context" — Web/OpenAI-Pfad war schon vorhanden; Retell-`calendar.book` erstellt jetzt bei `bookSlot.ok=false` ein Rückruf-Ticket.
  - [x] Prompt-Instruction erweitern: "Wenn Kalender scheitert, entschuldige dich kurz und erstelle ein Rückruf-Ticket"
  - [ ] Testen: manueller Force-Fail von `calendar.book` (z. B. invalid token) → Ticket MUSS entstehen
  - [x] Retell-Tool-Error-Handling prüfen: statt reiner `{error: …}`-Response bekommt Retell jetzt `status=fallback_ticket_created`, `fallback=true`, `ticketId` und eine klare Message.

## 7. Ticket-Erstellung (allgemein)
- Zu klären/umsetzen:
  - [x] Funktioniert `ticket.create` aktuell robust? Retell-Payload-Auswertung gehärtet: `agent_id` wird jetzt auch aus `call.agent_id` gelesen, Telefonnummer aus `customerPhone|customer_phone|from_number|call.from_number`.
  - [ ] Confirmation-Call-Back-Flow (`/tickets/callback`) — funktioniert die 5/1h Rate-Limit + DACH-Phone-Double-Check?
  - [x] Ticket-Notification-Email (`sendTicketNotification`) ist aktiv in `tickets.ts` via Owner-Lookup nach `createTicket`.
  - [ ] Frontend TicketInbox: Alle States sichtbar? (`open | assigned | done`)
  - [ ] Tickets mit Phone-Nummer die NICHT DACH ist → aktuell blockiert von `isPlausiblePhone`, soll das so bleiben?

## 8. Bug: Outbound-Demo-Agent kann keinen Link schicken
- Ursache: Sales-Agent-Prompt sagte "Soll ich dir den Link schicken?", aber der Retell-Agent hatte kein E-Mail/SMS-Tool. Die Formular-E-Mail wurde nur als Lead gespeichert.
- Umgesetzt:
  - [x] `sendSignupLinkEmail()` in `email.ts` ergänzt.
  - [x] `/demo/callback` und `/outbound/website-callback` schicken den Testlink an die angegebene E-Mail, auch bei 24h-Phone-Dedup.
  - [x] Sales-Agent bekommt `{{signup_link}}` als Dynamic Variable und sagt, dass der Link bereits per E-Mail rausging.
  - [x] Sales-Agent-Redis-Key auf `sales_agent:phonbot:v2` gesetzt, damit kein alter Prompt ohne Link-Regel aus dem Cache weiterläuft.
  - [x] `outbound_calls.org_id` für anonyme Website-Demo-Callbacks nullable migriert.

## Verbundene Notes

- [[Phonbot/Overview]]
- [[Phonbot/Phonbot-Gesamtsystem]]
- [[Phonbot/SEO]]
- [[Phonbot/modules/Backend-Agents]] · [[Phonbot/modules/Backend-Voice-Telephony]] · [[Phonbot/modules/Backend-Outbound]] · [[Phonbot/modules/Backend-Comm-Scheduling]] · [[Phonbot/modules/Backend-Insights-Admin]] · [[Phonbot/modules/Backend-Auth-Security]]

## Narrative

- 2026-04-28 (Round 13): **WEBHOOK_SIGNING_SECRET soft-warn → hard-required** (commit `30bf6ce`). Round 7 hatte's eingeführt + soft-warn dass es bald Pflicht wird. Migration in 3 Schritten: env-var auf prod gesetzt = JWT_SECRET-Wert (zero-impact für Customer weil HMAC-Ableitung deterministisch am Key hängt), Container force-recreate, dann Code-promote in `REQUIRED_PROD_SECRETS`. JWT_SECRET kann jetzt unabhängig rotiert werden ohne Customer-Webhook-Validators zu killen — Codex hat alle JWT_SECRET-Reads im Repo gegengeprüft. `.env.example` erweitert (Codex Blind-spot). Boot-Log frei von WARN/FATAL.
- 2026-04-28 (Round 12): **Pattern-Pool industry-Tag end-to-end** (commit `ad2c164`). Toggle in PrivacyTab persistierte zwar in `orgs.share_patterns`, aber Backend-Pipeline brach an `data->>'industry'`=null ab weil das Feld nie im Schema existierte. Jetzt: `industry: z.string().optional()` in `AgentConfigSchema`, OnboardingWizard setzt `industry: template.id` beim Deploy, `template-learning.ts:processTemplateLearning` + `extractConversationPattern` lesen direkt aus `agent_configs.data->>'industry'`. **Codex Code-Review fand 3 echte Bugs vor Deploy**: Set-Logic kollidierte mit Check-Semantik, LEFT JOIN in extractConversationPattern war ambiguous bei Multi-Agent-Orgs, **Showstopper**: `data->>'templateId'` wird nirgends im Write-Pfad persistiert → mein erster Whitelist-Fallback-Draft war komplett dead code. Pre-Deploy: ganzen Fallback rausgeworfen, dynamic-imports raus, simple direkt-Reads. Templates.ts war in HEAD bereits durch Vaso/Codex Round-12.5 mit `industry`-Tags + `CURATED_INDUSTRY_KEYS`-Export — komplementär zu meiner Arbeit, kein Konflikt. Bekannte Limitation: legacy-orgs ohne industry bleiben unclustered bis Customer setzt manuell oder Backfill läuft.
- 2026-04-28: **Vault auf git** (`haskallalk-eng/obsidian-vauls`, privat, SSH, obsidian-git Plugin v2.38.2 mit auto-backup 5min). Plus **Recording-Toggle End-to-End live** (commits `11285e3` + `7aa46e2`): PrivacyTab.recordCalls wirkt jetzt wirklich — Schema-Feld optional (Codex pre-deploy HIGH-Catch: `default(true)` hätte sich Write-Through-mäßig in Customer-Configs materialisiert), Disclosure-Block in agent-instructions.ts conditional (mit Aufzeichnungshinweis wenn an, ohne wenn aus, KI-Hinweis bleibt immer Pflicht per EU AI Act Art. 50), Retell `data_storage_setting`-Param (`'everything'` vs `'basic_attributes_only'`, Live-Verify gegen prod-Retell-API bestätigt field-name + opt_out_sensitive_data_storage als deprecated), `recording_declined`-Tool nur wenn an registriert. Plus persistente DSGVO-Audit-Tabelle `privacy_setting_changes` (365d-Retention) — Codex Round-11 review hat explizit gesagt log.info → Sentry reicht nicht für Art. 5 Abs. 2 Rechenschaftspflicht weil Sentry-retention plan-abhängig. UI-Banner-Wording „Audio + Transkript werden nicht gespeichert. Anrufmetadaten (Dauer, Datum, Rufnummer) verbleiben für die Minutenabrechnung" (Codex-Empfehlung — präziser als "kein Recording" weil basic_attributes_only Metadaten behält). Drei Codex-Sessions, zwei pre-deploy-bug-catches.
- 2026-04-27 (nachmittags): **Audit-Round-10 — erste echte bidirektionale Cross-Review** (commit `565e47d`). Bisher war Pattern „Claude author → Codex review" über Rounds 6-9. User-Feedback „ich hoffe ihr habt euch auch gegenseitig reviewt" hat das Asymmetrie-Problem auf den Punkt gebracht — Round 10 dreht es um. Codex hat NICE-2 Webhook-Health-Tracking als Author-Pass implementiert (~530s, +257 LOC, 8 Files: `inbound_webhook_health` Tabelle mit Partial-Index, `upsertWebhookHealth` Helper mit discriminated-union, disabled-pre-check + success/failure-UPSERT in fireInboundWebhooks, `GET /agent-config/webhooks-health` für Frontend-Banner, daily cleanup-cron). Codex hat 3 Uncertainties + 1 Edge-Case selbst geflagged — höhere Self-Awareness als erwartet. **Claude's Counter-Review** bestätigte 1× HIGH (Codex Uncertainty #1 — Race wo späte 2xx-Response ein freshly-set disable_until wegwischt → pre-deploy-fix mit CASE-WHEN-disabled_until > now()) + 1× LOW (Endpoint zeigte orphan health-rows → pre-deploy-fix mit liveWebhookIds-Set-Filter); 2 weitere LOW als akzeptable Trade-offs verbucht (DB-Roundtrip-Cost, Edge-Case bei webhook-recreation). Bidirectional review liefert Wert in beide Richtungen: jeder hat Catch-fail-Punkte die der andere nicht. Pattern für Round 11+: abwechseln wo Sinn macht. Module 07 ist jetzt fast komplett geschlossen — nur HIGH-2 (Email-PII UX-Entscheid) + NICE-1 (crm_leads.email NOT NULL Datenmodell-Entscheid) offen.
- 2026-04-27 (mittags): **Audit-Round-9 — Phone-Pool-Konsistenz + Retry-Suggestion-Dedup, ~5 Findings gefixt + deployed (commit `5587d7c`).** Plan-Review-Codex-Pattern aus Round 8 nochmal genutzt: Codex hat 5 Round-9-Items klassifiziert (3 OK, 2 RISIKO, 1 SKIP), Reihenfolge `3 → 2 → 1 → 4`. Item 3 entfernt `INSERT INTO phone_numbers (method='forwarding')` aus `/phone/forward` (dead code seit Round-6, Carrier-Code-Helper bleibt). Item 2 baute `syncTwilioNumbersToDb`-Reverse-Diff: `limit:1000` für volle inventory + 7-Tage-cooldown auf Pool-DELETE + Cap `MAX_POOL_DELETES_PER_RUN = 5` (Codex-Code-Review-Catch). Item 1 (M06-HIGH-2) refaktorierte `autoProvisionGermanNumber`: Pool-Claim ZUERST mit der gleichen `FOR UPDATE SKIP LOCKED`-CTE wie `/phone/provision` + Stale-PII-Reset im CTE; bei Pool-Hit Retell-PATCH oder Import-Fallback (provider_id-Logik aus Round-6); bei Pool-Miss Twilio-Buy mit `bundleSid + addressSid` (DACH-Compliance — Bundle fehlte in der vorherigen Implementation!). **Codex hat in der Code-Review-Phase einen echten HIGH-Bug gefangen**: das Stripe-Webhook-Retry-Race konnte den `existing.rowCount === 0` Idempotency-Check umgehen → Customer mit 2-3 Numbers. Pre-Deploy-Fix: gesamte Body in `pg_advisory_xact_lock` per orgId-Hash gewrappt, Body in `runAutoProvisionBody` extrahiert. Item 4 (M07-LOW-5) ergänzte `checkFixEffectiveness` retry-INSERT mit embedding + SELECT-then-INSERT-Dedup. Module 06 + 07 sind jetzt fast komplett geschlossen — nur Module 06 MEDIUM-3 Twilio-Status-Webhook (Pipeline-Umbau), Module 07 HIGH-2 Email-PII-UX-Entscheid + 1 NICE offen.
- 2026-04-27 (vormittags): **Audit-Round-8 — drei Codex-Sessions (Plan-Review + Code-Review + Verify), 13 Backlog-Findings aus Module 06+07 gefixt + deployed (commit `a38c4c3`).** User-Vorgabe „arbeite ganz viel mit codex … achte nicht mehr kaputt zu machen". Codex-Plan-Review-VOR-Implementation als neue Routine eingeführt — Codex hat Reihenfolge `A → C → B` empfohlen, Blocklist als Quarantine statt Drop, URL/Email-Detection raus. Group A: `classifyPromptFix()` Helper mit length-cap 500 + 8 narrow inject-Regex (eingebaut an 4 INSERT-Sites in insights.ts + Apply-Route-Guard 409 quarantined), `redactPII(transcript)` vor `INSERT INTO demo_calls` + `redactPII()` auf `learning_corrections` Few-shot bevor's an OpenAI geht (DSGVO Q5 closed), globaler Twilio-Verify-Cost-Cap via Redis-Counter (200/h env-tunable). Group C: neue Tabelle `admin_read_audit_log` 365d-Retention, per-route rate-limit 60/min auf `/admin/leads*` + `/admin/demo-calls`, `recordAdminRead()` Helper. Group B: in-memory LRU-Cache für `inboundWebhooks` mit TTL 60s + `invalidateInboundWebhooksCache()` exported (aufgerufen von `writeConfig` UND `/agent-config/new` nach Codex-Q2-Lücke), neuer Endpoint `/insights/admin/embed-backfill` (50er-Batches). **Codex-Code-Review der Round-8-Diff hat zwei echte Bugs vor Deploy gefunden**: Q1 Regex zu breit (`act as a` würde legitime Customer-Prompt „act as a phone agent" matchen) → Patterns auf 8 narrow phrases reduziert; Q2 Cache-Invalidation lückenhaft in `/agent-config/new` → ergänzt. Deploy mit Container-Healthy + DB-Migration `admin_read_audit_log` in prod verifiziert. Codex-Counter-Review-Pattern aus `RULES.md` skaliert in beide Richtungen: Plan-Review-VOR + Code-Review-NACH = robuste Round-Disziplin.
- 2026-04-26 (nachts): **Module 07 (tickets/insights/outbound-insights/inbound-webhooks ~2175 LOC) — zweites Codex-Cross-Review + 13 Befunde gefixt + deployed.** Author-Pass: 0× CRITICAL, 4× HIGH (Prompt-Injection via prompt_fix, PII-Email, silent Retell-Sync, outbound × 5 stderr), 6× MEDIUM, 5× LOW, 2× NICE. Codex-Counter-Review (534s): 3 Severity-Korrekturen (HIGH-1 → Review-Poisoning weil Auto-Apply aus + konkretes Inject-Beispiel; HIGH-2 silent-stderr-Teil falsch; HIGH-4 nur 3+2 statt 5+), 1 klarer Widerspruch (LOW-4 isBlockedPort ist beabsichtigt), 5 Zusatzbefunde: MEDIUM-A Webhook-JWT_SECRET-Fallback (Rotation killt Customer-Sigs silent), **MEDIUM-B Demo-Transkripte 90 Tage Roh-PII** (Kreditkartennummern!), MEDIUM-C Admin-Massenlesepfade ohne Audit-Log + Rate-Limits, LOW-A outbound-insights ohne org_id-WHERE (heute durch UNIQUE geschützt), **LOW-B JSONB-Concat-Comment seit Monaten technisch falsch** (Postgres `||` ist rechts-dominant nicht links). Plus Codex hat zur Q5 (`learning_corrections.original_text` als OpenAI-Few-shot ohne dokumentierte AV) als Compliance-Gap bestätigt. 13 Issues sofort gefixt + deployed in commit `8bcb060`: HIGH-3 Retell-Sync-log + neue DB-Spalten `agent_configs.last_retell_sync_error`/`last_retell_sync_at`, HIGH-4 alle stderr+catches → log, **MEDIUM-2 setPrompt jetzt mit `pg_advisory_xact_lock` per orgId in Transaction** (alle 4 Race-Pfade — applyPromptAddition + consolidatePrompt + evaluateAbTest + checkScoreRollback — serialisiert), **MEDIUM-3 Cleanup-Migration für zombie ab_tests** (`status='cancelled'` für `running AND created_at < 2026-04-23`), MEDIUM-5/6 + MEDIUM-A WEBHOOK_SIGNING_SECRET soft-warn in env.ts (prod-Boot-Log zeigt jetzt loud Warning), LOW-1/2/3/A/B. Verschoben für Round 8: HIGH-1 Prompt-Injection-Filter (UI-Banner + Pattern-Blocklist), HIGH-2 Email-PII-Umbau, MEDIUM-1 Embedding-Backfill-Migration, MEDIUM-4 LRU-Cache, MEDIUM-B Demo-Transkript-Redaction-Pipeline (mit OpenAI-Few-shot-DSGVO-Gap zusammen), MEDIUM-C Admin-Read-Audit-Log. Drei Cross-Reviews mit Codex an einem Tag — Pattern aus `RULES.md` skaliert.
- 2026-04-26 (spätabends): **Erstes echtes Cross-Review mit Codex auf Module 06 (phone.ts + Twilio) + 8 Befunde gefixt.** Author-Pass von Claude (1× CRITICAL + 2× HIGH + 5× MEDIUM + 3× LOW + 1× NICE), Counter-Review via `codex:codex-rescue` Agent (657s Laufzeit). Codex hat Severity bei 3 Befunden korrigiert (CRITICAL-1 → HIGH wegen unbestätigtem Pool-Steal, MEDIUM-2 → HIGH weil Retell-PATCH nirgends `res.ok` prüft, HIGH-1 → MEDIUM weil `/phone/forward` im UI-Pfad nicht benutzt wird). 5 Zusatzbefunde geliefert: HIGH-A (migratePhone-not-wired = aber falsch, ist in `index.ts:216`), HIGH-B (Pool-Rows ohne `provider_id` gehen in PATCH-Pfad statt Import → Nummer „aktiv" im Dashboard ohne Retell-Existenz), **MEDIUM-A (DSGVO-PII-Leak: Pool-Reuse vergisst `customer_number`+`forwarding_type` zu clearen — Org A's Forwarding-Setup leakt an Org B)**, MEDIUM-B (`GET /phone` SELECT fehlt die Loop-Warning-Felder → CapabilitiesTab-Schutz blind), MEDIUM-C (extern gedroppte Twilio-Numbers bleiben tot in DB). Plus Twilio-Doku-Links für Q3 (DACH-Compliance Bundle). 8 echte Issues sofort gefixt + deployed (`9f300d7`): Plan-Check + Cross-Org-Schutz für `/phone/twilio/import`, Retell-PATCH `res.ok`-Checks in 3 Endpoints + Pool-Rollback bei Failure, Pool-Rows Import statt PATCH bei !provider_id, DSGVO-PII-Reset bei Pool-Return + Pool-Reclaim, GET /phone Felder, PLANS.phoneNumbersLimit (eigenes Feld nicht agentsLimit-Reuse, deckt nummer-Plan jetzt mit), 13× stderr.write → log. Verschoben für Round 7: autoProvision Pool-First-Refactor (HIGH-2), Twilio-Status-Webhook für Polling-DoS (MEDIUM-3), DB-vs-Twilio-Diff-Sync (MEDIUM-C), `/phone/forward` Endpoint-Entscheid in Module 09. Cross-Review-Pattern aus `RULES.md` funktioniert: Codex hat real fundierte Befunde + Severity-Korrekturen geliefert die Claude allein nicht gehabt hätte.
- 2026-04-26 (abends): **Audit-2026-04-26 Round-1-bis-5-Fix-Sweep über Module 01–05 + Prod-Deploy.** Ein einziger Commit (`c549aab`) räumt ~22 Befunde aus den Modulen `auth.ts`, `agent-config.ts`, `retell-webhooks.ts`, `traces.ts`, `billing.ts`, `calendar.ts` ab. Highlights: Account-Delete verlangt Passwort-Reauth (HIGH-2 Module 01), Per-User-Brute-Force-Soft-Lock via Redis+Mem-Fallback (MEDIUM-5 Module 01), B2B-Pflicht-Flags Backend-enforced (LOW-1 Module 01), `email_verify_token_expires_at` 14d-TTL inkl. Migration (MEDIUM-1 Module 01), Multi-Agent-Web-Call refused ohne `agentTenantId` (HIGH-1 Module 02), `enforcePlanAgentLimitOnCreate` als Defense-in-Depth in `writeConfig` (HIGH-2 Module 02 — PUT-Bypass tot), `LIMITS`-Hardcode → `PLANS.agentsLimit` (Single Source of Truth), `/agent-config/stats` Rate-Limit 60/min, `analyzeOutboundCall` top-level static-Import, traces.agentId für Multi-Agent-Differenzierung, multilinguale Caller-Phone-Blacklist (DE/EN/ES/FR/IT/NL/TR/PL), Stripe `customer.subscription.deleted` clamped `minutes_used` für Free-Plan-Re-Entry, Calendar-Token-Refresh-Catch loggen jetzt strukturiert (vorher 5 Monate stille 403er), OAuth-Callback-HTML mit `JSON.stringify(appUrl)` (XSS via APP_URL-ENV unmöglich), `decryptConn`-Failures Sentry-sichtbar. **Codex-Helper `checkForwardingVerificationMatch` re-enabled** (TODOs aus Daily 2026-04-27 erledigt — phone.ts ist jetzt mit-committed). Audit-Docs Module 01/02/03/04/05 + INDEX.md mit ✅-Markern aktualisiert. tsc grün, push, prod-Deploy via SSH, Container Healthy, DB-Migration `email_verify_token_expires_at` in prod verifiziert.
- 2026-04-27: **Forwarding-Verification-Session ins Vault.** Codex hat den Hook-Import in `apps/api/src/retell-webhooks.ts` mitsamt Call-Site temporär auskommentiert (`TODO(codex): re-enable once phone.ts checkForwardingVerificationMatch is pushed`), weil das `phone.ts` mit der neuen `checkForwardingVerificationMatch`-Export-Funktion noch lokal-only ist. Konsequenz: der `/phone/verify-forwarding`-Endpoint läuft, pollt aber ins Leere → timeout-ed mit `verified=false` ohne falsche Info. Echte Verifikation ist bis zum Commit+Push offline. Daily-Notes 04-26 (komplett) + 04-27 (kurz) + ZuTun-Punkt 15 (siehe unten) angelegt.
- 2026-04-26: **Rufweiterleitungs-Verifizierung kritisch zerlegt + neuer Loop-Test gebaut.** Alte `/phone/verify-forwarding`-Heuristik in `apps/api/src/phone.ts:819-821` hatte toten else-Branch + falsche Grundannahme (Rufdauer sagt nichts über *wer* abnimmt) + verrauschtes Timing → bias Richtung `'always'` → False-Positive-Loop-Warnungen im Builder. Alte `/phone/verify` setzte `verified=true` allein wenn `client.calls.create()` ohne Throw zurückkam (= Twilio-API hat Request angenommen, sagt 0 über Forwarding). Beides ersetzt durch echten Closed-Feedback-Loop: Verifier-Trunk (`VERIFIER_TWILIO_NUMBER`, eigene Twilio-Nummer NICHT in Retell importiert) ruft Kunden-Nummer mit `<Hangup/>`-TwiML; wenn Carrier weiterleitet → Phonbot-Inbound-Webhook fired; Caller-ID-Match (high = Verifier preserved, medium = Customer-Number-Fallback bei Carrier-Rewrite) setzt Redis-Result-Key; Endpoint pollt 35s. Match-Latenz wird zu `forwardingType` (`<10s = always`, `≥10s = no_answer`). CapabilitiesTab-Loop-Warnung umgestellt auf `verified=true`-Flag statt kaputter Heuristik. `tsc --noEmit` API+Web grün lokal. **Nicht live-getestet** — braucht VERIFIER_TWILIO_NUMBER + echtes Handy mit aktivem `**21*<phonbot-nummer>#`. Bei Misserfolg lieber rauswerfen statt Theater-Endpoint behalten. Lokal-Änderungen noch nicht committed/pushed → siehe ZuTun #15. — Lokale Änderungen (uncommitted)
- 2026-04-23 (nach Mitternacht-Rutsch): **Agent-Builder-Bug-Sweep + Skill/Repo-Tooling.** User-Report „speichern fehlgeschlagen als ich neuen Service gemacht habe" hatte zwei unabhängige Ursachen: HTML-Input-Console-Warning für `"24:00"` (24/7-Preset im Öffnungszeiten-Editor schrieb invalid `to: '24:00'` statt `'23:59'`) + echter 500er war `ZodError services[1].name > 120 chars` (Absatz versehentlich in den Service-Namen gepastet). Beides gefixt (`f30e1c6` + `65220d2`), `maxLength={120}` als Frontend-Prävention. Zwei Prod-Deploys (full api+web, dann web-only) — Prod HEAD jetzt `65220d2`. Dazu Skill-Tooling: neuer `obsidian-session-log`-Skill für Vault-Workflow (Daily-Note-Pattern + ZuTun-Narrative + Wikilink-Conventions + Sync/Backup-Operations) gebaut nach Web-Recherche zu 2025/2026-Obsidian-Best-Practices. `.claude/skills/` als Private-Repo `haskallalk-eng/Claude-skills-usw` aufgesetzt (initial-commit `cae333f`, 217 Dateien, via SSH nach HTTPS-Hang).
- 2026-04-23 (spätabends): **Kalender-Poll-Sync komplett gebaut (Phase C) + ein seit Monaten stiller Produktionsbug aufgedeckt.** Neue `external_calendar_events`-Cache-Tabelle + `calendar-sync.ts`-Modul mit Google delta-sync (`syncToken` + 410-Gone-Fallback), Microsoft `calendarView` und cal.com `/bookings`. Cron alle 5 min, UI-Sektion „Extern" im DayDrawer mit Provider-Label, read-only. Zero-Trust-Review fand einen Mass-Wipe-Bug bei leerer Provider-Response (gefixt in `78a599f`). Daneben: **Google Calendar API war nie im Cloud-Projekt `145652898743` aktiviert** — der Agent-`freeBusy`-Check + `bookSlot`-Spiegelung nach Google schlugen seit Tag 1 still mit 403 fehl, weil `findSlotsForConnection` zwei `catch {}` hatte die den Fehler wegschluckten. Mein Sync war der erste Pfad der den Fehler in `last_sync_error` schrieb → User konnte die API mit einem Klick aktivieren, danach flossen 21 Events sauber durch (inkl. recurring expansion). Silent-Catches gegen `log.warn` getauscht (`d2e5901`). Azure Delegated Permissions (`Calendars.Read` + `Calendars.ReadWrite` + `offline_access` + `openid` + `User.Read`) + Multi-Tenant-Kontotypen + Redirect-URI verifiziert — Outlook-Live-Test steht noch aus. Auch an dem Tag: Doppelt-angezeigte Kalender-Verbindungen im UI zu einer Zeile konsolidiert (`8fcbd9b`), Dashboard-Listen klickbar mit URL-Hash-Deep-Links + `.focus-pulse` (`b5fb7b2`). Prod HEAD `d2e5901`.
- 2026-04-23 (abends): **Voice-Catalog Ehrlichkeits-Sweep + Identity-Card-Cleanup.** 30+ Sprachen bleiben im Picker, aber nur die tatsächlich native-klingenden Voices werden pro Sprache gezeigt — 11labs-Actors fliegen aus allen Nicht-EN-Sprachen, OpenAI fliegt aus allen Nicht-EN-Sprachen. DE/EN haben viele (11/16), FR/ES/IT/TR/PL/NL haben 9 Cartesia native. PT/RU/JA/KO/ZH/HI/SV bekommen 2 Cartesia + `few`-Banner. AR/DA/FI/NO/CS/SK/HU/RO/EL/BG/HR/UK/ID/MS/VI bekommen 3-Voice-Fallback + `none`-Banner (Multilingual mit Accent, Clone empfohlen). Landing-Stats und alle SEO-Files (`llms.txt`, `llms-full.txt`, JSON-LD FAQ) auf „30+ Sprachen" angehoben. Auto-Fallback fängt Legacy-Voice-IDs ab, die nach dem Sweep nicht mehr im Catalog sind (`11labs-Carola`-Regression). Identity-Card: „Deployed"-Badge in den Section-Header rechts gewandert, die nutzlose `Agent: agent_xxx`-ID-Zeile entfernt. Gepusht (`1646502` → `8ad4752`), Prod-Deploy bewusst ausgesetzt bis Termi sein Calendar-Sync-WIP committed hat.
- 2026-04-23: **Großer Agent-Builder + Register-Refactor-Tag.** Retell-Hardening durchgezogen (Recording-Decline scrubbed via post-call DELETE + `webhook_url` endlich gesetzt, `transfer_call`-Naming-Bug gefixt, 45 s Silence-Auto-Hangup + 5 s Goodbye-Gate). Stripe-first Registrierung live (`pending_registrations`-Table, kein User-Insert mehr bei Cancel). Abandoned-Signup-Mail im dark-mode brandedEmail + 10-min-Sweep in `crm_leads`. HTTP/3 in Caddy deaktiviert (`ERR_SSL_PROTOCOL_ERROR`-Fix). Agent-Builder Verhalten-Tab kompletter UX-Rework: Gradient-Dot-Badge statt Counter-Pill, editierbares Suggestion-Textarea, Auto-Apply server-seitig aus, `[MANUAL:<tab>]` Dual-Mode-Banner vorbereitet, Placeholder-Gate (`[…eintragen…]` blockiert Übernehmen), LLM-Insight-Guardrails gegen „Google-Calendar-verbinden"-Empfehlungen. Öffnungszeiten neuer strukturierter Editor mit 2-Wege-Sync zur Kalender-Verfügbarkeit. Phone-Mapping aufgeräumt (17 Rand-Nummern unassignt), 3 Test-User gelöscht, 2 Ghost-Retell-Agents + LLMs via SSH entfernt.
- 2026-04-22: Ursachenanalyse/Fix für Retell-Tools: Tool-Auth akzeptiert jetzt `call.agent_id`, Tool-Trace nutzt `call.call_id`, Tickets/Buchungen nutzen `call.from_number` als Phone-Fallback. Demo-Linkversand per E-Mail ergänzt. `pnpm --filter @vas/api typecheck` und `pnpm --filter @vas/api exec vitest run` grün.
- 2026-04-22: Kalendervertrag live umgesetzt (`0afdd22`): Chipy-only wenn kein externer Kalender verbunden ist; bei externen Kalendern Availability = Schnittmenge aus Chipy + allen externen Kalendern, Booking = alle externen Kalender + Chipy. Health grün.
- 2026-04-22: Retell-Telefonpfad für `calendar.book` um Ticket-Fallback ergänzt (`apps/api/src/retell-webhooks.ts`) und Agent-Instructions gegen falsche Buchungsbestätigung erweitert. `pnpm --filter @vas/api typecheck` grün. Manueller Prod/Test-Call mit invalidem Kalender-Token steht noch aus.
- 2026-04-21: ZuTun-Sammelnote angelegt aus mündlichem Briefing (User). Nichts umgesetzt, nur dokumentiert. Einzelne Punkte werden bei Umsetzung zu GitHub-Issues konvertiert.


## 9. Website: Preise klickbar

- Auf der Landing + den Branchen-Seiten sind die Preise aktuell reiner Text — man klickt drauf und es passiert nichts.
- Zu tun:
  - [ ] Jede Plan-Kachel (Starter/Pro/…) verlinkt auf Sign-up mit vorausgewähltem Plan (`/register?plan=pro`)
  - [ ] Hover/Focus-States konsistent mit bestehenden CTAs (Orange-Glow)
  - [ ] Mobile Tap-Target ≥ 44 px
  - [ ] Analytics-Event `pricing_card_click` für Conversion-Tracking

## 10. UI-Hinweis wenn der Agent dazulernt (Prompt-Erweiterung)

- Das Learning-System erweitert den Prompt im Hintergrund (`analyzeCall` → `prompt_suggestions`), der User merkt davon nichts.
- Zu tun:
  - [ ] Toast oder kleiner Badge im Dashboard wenn ein neuer Vorschlag vorliegt ("Chipy hat aus 3 Anrufen gelernt — anschauen?")
  - [ ] Im Agent-Builder kennzeichnen welche Prompt-Passagen vom Lernsystem stammen (read-only + Quelle "aus Gespräch X vom TT.MM.")
  - [ ] Opt-out pro Agent: Schalter "Kein Auto-Learning"
  - [ ] Diff-Ansicht vorher/nachher bevor der Vorschlag live geht

## 11. Reload bleibt auf gleicher Seite

- Aktuell: bei Reload auf z. B. `/dashboard/agents/builder` landet man auf `/`. Wer ein Formular halb ausgefüllt hat, verliert alles.
- Ursache: Navigation ist state-basiert (kein React-Router, siehe CLAUDE.md §10). Reload verliert den Page-State.
- Zu tun:
  - [ ] URL-Sync: aktueller Page-State in `window.history.pushState` spiegeln (Hash oder Query)
  - [ ] Beim Mount aus `window.location` lesen und den Page-State initialisieren
  - [ ] Deep-Links: z. B. `/?page=builder&tenant=xyz` lädt direkt den Builder
  - [ ] Browser-Back/Forward muss funktionieren (nicht mehr auf Home springen)

## 12. 🐛 Bug: Outbound geht nicht

- Symptom: Outbound-Anrufe (Website-Callback / manueller Outbound aus Dashboard) starten nicht oder brechen ab.
- Zu prüfen:
  - [ ] `/outbound/website-callback` — Turnstile-Token gültig? Hourly-Cap erreicht?
  - [ ] `createPhoneCall` / `triggerBridgeCall` — welches Provider-Fehlerbild (Retell vs. Twilio-Bridge)?
  - [ ] `outbound_calls`-Row entsteht, aber `retell_call_id` bleibt null?
  - [ ] `ALLOWED_PHONE_PREFIXES` blockt die Nummer fälschlich?
  - [ ] Prod-Logs auf `outbound` filtern — letzter erfolgreicher Call?
  - [ ] Reproduzieren mit einer Test-Nummer + Trace-ID

## 13. 🐛 Bug: Kalender bucht doppelt

- Symptom: Ein Termin landet zweimal im selben Kalender.
- Mögliche Ursachen:
  - [ ] `calendar.book` wird durch Retell-Tool-Retries mehrfach ausgelöst → braucht Idempotency-Key auf Tool-Ebene (z. B. `call_id + slotStart` als Dedup)
  - [ ] Chipy-interner Kalender + externer Kalender schreiben beide, obwohl nur einer gedacht ist
  - [ ] Ticket-Fallback + Kalender laufen parallel beim Tool-Error
- Zu tun:
  - [ ] Audit-Log: welche Doppel-Buchungen, selbe `call_id`? Timestamps nebeneinander?
  - [ ] Dedup via `processed_retell_events`-Pattern auch für Tool-Calls (aktuell nur für call_ended)
  - [ ] Test: Same-Slot-Request 2× schnell hintereinander vom Agent → nur 1 Buchung erlaubt

## 14. Öffentliche API-Funktion für Kunden

- Stichwort aus Rohnotiz — vermutlich gemeint: öffentliche REST-API, die Kunden in ihre eigenen Systeme integrieren können.
- Zu klären:
  - [ ] Scope: Termine pullen? Tickets empfangen per Webhook? Call-Events (call_started, call_ended, decline)?
  - [ ] Auth: API-Key pro Org (rotierbar, AES-verschlüsselt wie OAuth-Tokens)
  - [ ] Rate-Limits pro Key
  - [ ] Docs-Seite (OpenAPI / Redoc / einfache MD-Doku)
  - [ ] Abgrenzung: MCP-Server separat (für Claude/GPT-Integrationen) oder im selben Endpoint?

## 15. Forwarding-Verification-Loop-Test fertig stellen

- **Status (2026-04-26 abends):** Helper + Hook sind committed (`c549aab`). `apps/api/src/phone.ts` exportiert `checkForwardingVerificationMatch` + Pending/Result-Helper; `apps/api/src/retell-webhooks.ts` `call_started`-Hook ruft Match wieder auf (Import + Call-Site re-enabled, `TODO(codex)`-Marker entfernt). `/phone/verify-forwarding` ist Architektur-vollständig in prod. **Was noch fehlt, ist ausschließlich der Live-Smoke-Test** mit echter Twilio-Verifier-Nummer + echtem Handy. Wenn der erste Live-Test fehlschlägt → User-Vorgabe: rauswerfen statt halbgares Theater behalten.
- **Architektur (für späteres Re-Lesen):**
  - Verifier-Trunk = eigene Twilio-Nummer, MUSS via `VERIFIER_TWILIO_NUMBER` env gesetzt + NICHT in Retell importiert sein (sonst Loop-Short-Circuit, Endpoint refused via `verifierConflict`-Check)
  - Endpoint speichert Token in Redis-Key `phone-verify:pending:<phonbotNumber>` (TTL 90s)
  - Twilio-Outbound mit `<Hangup/>`-TwiML, Timeout 30s
  - Retell-`call_started`-Hook (`checkForwardingVerificationMatch`) prüft Caller-ID: high=Verifier, medium=Customer-Number-Fallback (Carrier-Rewrite)
  - Match-Latenz < 10s ⇒ `forwardingType='always'`, ≥10s ⇒ `'no_answer'`
  - Endpoint pollt `phone-verify:result:<token>` alle 1.5s, max 35s
  - Best-effort Hangup der Verifier-Outbound am Ende (nicht ringen lassen)
- **Re-Enable-Schritte (in dieser Reihenfolge):**
  - [x] `apps/api/src/phone.ts` lokale Änderungen committen + pushen (Helpers `setPendingForwardingVerification` / `getPendingForwardingVerification` / `clearPendingForwardingVerification` / `setForwardingVerificationResult` / `getForwardingVerificationResult` / `checkForwardingVerificationMatch` exportiert + neuer `/phone/verify-forwarding`-Body + `/phone/verify` für `forwarding`-method ehrlich + Migration-Comment-Update auf `'always' | 'no_answer'`) — commit `c549aab`
  - [x] `apps/api/.env.example` `VERIFIER_TWILIO_NUMBER`-Block committen — commit `c549aab`
  - [x] **Erst NACH dem `phone.ts`-Push:** `apps/api/src/retell-webhooks.ts` Re-Enable: Import-Zeile (`import { checkForwardingVerificationMatch } from './phone.js';`) UND Call-Site-Block im `call_started`-Branch wieder aktivieren — commit `c549aab`
  - [x] Frontend committen: `apps/web/src/lib/api.ts` (`VerifyForwardingResponse`-Type) + `apps/web/src/ui/PhoneManager.tsx` (4-State-Maschine) + `apps/web/src/ui/agent-builder/CapabilitiesTab.tsx` (Loop-Warnung auf `verified`-Flag) — commit `c549aab`
  - [x] `pnpm --filter @vas/api typecheck` + `pnpm --filter @vas/web typecheck` grün — beide EXIT=0 vor commit
  - [ ] Twilio: separate DE-Nummer kaufen, nicht in Retell importieren, in Prod `.env` als `VERIFIER_TWILIO_NUMBER` setzen
- **Live-Smoke-Test:**
  - [ ] Echtes Handy: `**21*<phonbot-nummer>#` aktivieren → Bestätigungston abwarten
  - [ ] Im Dashboard "Weiterleitung testen" → max 35s warten → Banner sollte grün werden mit `forwardingType: 'always'`, `confidence: 'high'`
  - [ ] Wiederholen mit `**61*<phonbot-nummer>#` (CFNR) → Banner grün mit `forwardingType: 'no_answer'`
  - [ ] `##002#` deaktivieren, nochmal testen → Banner amber `not_forwarded`
  - [ ] Bei Fehlschlag: Logs auf `forwarding-verification match check failed` prüfen, Caller-ID im Webhook checken
- **Edge-Cases die nicht testbar sind:**
  - [ ] CFB („Bei Besetzt") — Linie aus der Ferne besetzt zu machen geht nicht. Im UI-Banner darauf hinweisen, dass CFB nur manuell testbar ist.
  - [ ] Carrier mit anonymisierter Caller-ID — weder high- noch medium-confidence Match → User sieht `not_forwarded` trotz aktiver Forwarding. Akzeptabel, manueller Fallback dokumentiert.
- **Abbruch-Kriterium (User-Vorgabe):** Wenn der erste Live-Smoke-Test nach 1-2 Sessions immer noch nicht zuverlässig funktioniert → **rauswerfen statt halbgares Theater behalten**. Endpoint löschen, Frontend-UI zeigt nur die manuelle Test-Anleitung, `verified`-Spalte für `forwarding`-Records bleibt false.