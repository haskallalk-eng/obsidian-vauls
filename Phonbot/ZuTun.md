---
title: Phonbot — ZuTun
tags: [phonbot, todo, backlog]
created: 2026-04-21
status: unbearbeitet
note: Sammelnote für offene Aufgaben — wird bei Bedarf in GitHub-Issues überführt
---

# Phonbot — ZuTun

> Unsortierte Liste offener Aufgaben. Noch nicht als GitHub-Issues angelegt — erst beim Umsetzen zu Issues konvertieren.

## Session-Log

### 2026-05-01 — DSGVO-Compliance-Akte komplett + Prod-Deploy + Supabase-Switch + UG-Klarstellung
Siehe [[Daily/2026-05-01]].

**Geänderte Dateien (zentral):** `apps/web/public/{avv,sub-processors,impressum,datenschutz}/index.html`, `compliance/{README.md,vvt.md,dpa-checklist.md,mindrails-dpa-template.md,tias/*.md,dpa-requests/*.eml,dpas/{ionos,retell,resend}/*.pdf}`, `apps/api/src/{voice-catalog.ts,index.ts,db.ts}`, `apps/api/package.json`, `Caddyfile`, `scripts/{init-missing-secrets,set-env-var}.mjs`

- AVV (Art. 28 DSGVO Volltext) + Sub-Processor-Liste live unter [phonbot.de/avv/](https://phonbot.de/avv/) und [phonbot.de/sub-processors/](https://phonbot.de/sub-processors/) — `69cfd63`/`0f52771`
- 8 vorausgefüllte TIAs (Schrems II) für US-Sub-Processors + VVT (Art. 30 DSGVO) + Mindrails-DPA-Vorlage zum Mitschicken — `515fba4`
- Hetzner → IONOS überall, Caddy `/calendar/*` → API Routing-Fix, Compliance-Files alle auf GF Hans Waier — `515fba4`/`6ac012e`
- DE-Voice-Catalog 11 → 19 Stimmen via 8 ElevenLabs Multilingual-v2 HQ-Voices (Sarah/Charlotte/Matilda/Lily + Daniel/Brian/Adam/James) — `036b5ae`
- 3 DPAs gesigned: IONOS-AVV, Retell (DocuSign-Self-Service), Resend (DocuSign) — `9a84747`
- Dev-Setup Windows-fixed: `pnpm exec tsx` + `dns.setDefaultResultOrder('ipv4first')` im App-Code — `6dab681`
- Branch `round-14-industry-backfill` → master gemerged + push erfolgreich — `2cc23d6`
- **Prod-Deploy** via SSH (87.106.111.213): git pull + Container-Build + Helper-Skripte für Secrets via SSH-stdin-Pipe (Werte nie im Chat) + Caddy hard-restart. Smoke-Test live: `/health` 200, `/avv/` 200, `/sub-processors/` 200, `/calendar/google/callback` 302
- **Supabase-Account-Switch** (alter Acc hatte falsche E-Mail): neue DB `jnqpkkzuveoeipsborwp.supabase.co`, Service-Role-Key im Chat geleakt + sofort rotiert. Lokales Setup mit DB_REJECT_UNAUTHORIZED=false (Windows-Cert-Bundle-Issue) und auskommentiertem Upstash-REDIS_URL → In-Memory-Fallback
- **Provider-Accounts auf privat-E-Mail** `haskalla.lk@gmail.com` registriert (Supabase, GitHub, etc.) — Compliance via Company-Feld dokumentiert; Mittelfristig auf Mindrails-Business-E-Mail umziehen wenn UG eingetragen

**KRITISCHE ERKENNTNIS am Session-Ende:** User hat **noch keine Mindrails UG** — läuft als Kleingewerbe (Hans Waier, Einzelunternehmer). Alle bisherigen DPAs + AVV + Impressum mit „Mindrails UG (haftungsbeschränkt)" sind technisch ungültige Verträge (Entity existiert nicht). UG-Migration kommt später wenn Geld da ist.

**Offen:**
- [ ] Compliance-Rebuild auf „Hans Waier, Einzelunternehmer" — 20+ Files mit „Mindrails UG" zu ändern, Impressum: HRB raus + §19 UStG-Hinweis statt USt-IdNr. Habe gerade Impressum Sektion 1+2 begonnen
- [ ] 3 schon-signierte DPAs (IONOS/Retell/Resend) re-signen sobald Compliance-Naming auf Hans Waier umgestellt
- [ ] 8 weitere DPAs gesigned (Supabase/OpenAI/Twilio/Stripe/Sentry/ElevenLabs/Cloudflare/Cartesia)
- [ ] Sobald UG eingetragen: alle Compliance-Texte auf UG-Naming umstellen, neue HRB-Nummer + USt-IdNr ins Impressum, alle Sub-Processoren via DPA-Update auf neuen Vertragsträger transferieren

### 2026-04-30 (2) — Prompt-Qualität (Zahlen/Email-Spelling/Selbstreflexion) + Email-Bug-Visibility
Siehe [[Daily/2026-04-30]] (Session 2).

**Geänderte Dateien:** `apps/api/src/{platform-baseline,demo,email}.ts`
- Platform-Baseline: Zahlen-Diktion (ziffer-für-ziffer), Email-Provider-Whitelist (~30 DACH-Provider erlauben Auto-Erkennung; Custom-Domain = Buchstabier-Pflicht), DIN-5009-Trigger expliziter
- DEMO_END_INSTRUCTIONS: Selbstreflexion-Sektion (Chipy weiß sich als KI-Demo, antwortet auf Meta-Fragen, max 1-2 Antworten dann zurück zur Demo)
- email.ts: `send()` returnt jetzt `{ok, error}` — Resend-Fehler nicht mehr verschluckt
- demo.ts /demo/callback: signup-link-email-Aufrufe loggen via Pino Erfolg/Fehler

**Cache-Keys v5→v6** (demo+sales) damit baseline-Update wirkt.

**Offen:**
- [ ] Commit + Push + Deploy
- [ ] Resend-Dashboard auf Bounces/Domain-Verification prüfen
- [ ] Pino-Logs auf Prod filtern nach `kind: 'signup_link'` → echte Fehlerursache lesen
- [ ] Falls Admin-Override für `__platform__`/`__global__`/`__sales__` aktiv: über `/admin/demo-prompts` PUT mit null/null oder UI-"Restore Default" → sonst sehen die Code-Defaults nichts

### 2026-04-30 (1) — Demo-Voice-Cache-Bump + Sensitivity-Drosselung
Siehe [[Daily/2026-04-30]].

**Geänderte Datei:** `apps/api/src/demo.ts`
- `getOrCreateDemoAgent` und `getOrCreateSalesAgent` bekommen explizit `interruptionSensitivity: 0.5` (war implizit 1.0 via env-default). Demo-Web-Calls auf wechselnder Audio-Qualität führten bei 1.0 zu Fehl-Interruptions — Agent wirkte zappelig.
- Cache-Keys v4→v5 (`demo_agent:v5:*`, `demo_agent_meta:v5:*`, `sales_agent:phonbot:v5`). Erzwingt Recreation aller gecachten Agents → bekommen aktuelle Voice (Hassieb-Kalla) **und** neue Sensitivity. Alte v4-Patterns sind in `flushDemoAgentCache` Cleanup-Liste eingetragen.
- **Paying-Tenants nicht betroffen** — `updateAgent` setzt `interruption_sensitivity` nur explizit (RET-08), nie als Side-Effect.

**Offen:**
- [ ] Commit + Push auf master
- [ ] Manueller Deploy: `ssh root@87.106.111.213 'cd /opt/phonbot && bash scripts/deploy.sh'`
- [ ] Optional: Wenn 0.5 in der Praxis zu zaghaft wirkt → 0.6 testen. Wenn weiterhin zu zappelig → 0.4. Aktuell mittiger Default.
- [ ] Optional: Mehr deutsche HQ-Stimmen klonen (jeder Sprecher = neuer Eintrag in `DE_VOICES` mit `provider: 'elevenlabs', surchargePerMinute: 0.05`).

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

## Audit Round 14 — Industry-Backfill + Tests + M1 actor (2026-04-30)

Pattern: Plan-Review → Code → Codex-Review → HIGH-Fixes → Verify-Pass → Commit. Strict ab R14, nachdem Plan-Review bei R11–R13 übersprungen wurde.

**Zwei Code-Änderungen ausserhalb der „normalen" Backfill-Story:**
1. `writeConfig(config, orgId?, actorUserId?)` — dritter Param. `privacy_setting_changes.changed_by` zeichnet jetzt den echten User auf, nicht mehr den Org-Surrogat. M1-Fix aus Codex-Plan-Review. PUT/POST-Routes ziehen `userId` aus dem JWT.
2. `deriveWebhookSecret(tenantId, webhookId): Buffer` als named export aus [[Phonbot/Backend-Inbound-Webhooks|inbound-webhooks.ts]] — vorher inline im Hot-Path, nicht testbar. Dead-code-Duplikat (hex-returning Variante) gelöscht.

**Backfill-Endpoint** `POST /admin/agents/backfill-industry`:
- platform-admin-only (`payload.admin && payload.aud === 'phonbot:admin'` — derselbe strikte Gate wie [[Phonbot/Backend-Admin|admin.ts]])
- per-route rate-limit 30/min
- `pg_advisory_xact_lock(sha1(tenantId).bigint)` serialisiert concurrent admin-double-submits — die ganze SELECT-write-write-Sequenz läuft in einer einzigen `pool.connect()`-Transaction
- Industry-Validierung gegen `CURATED_INDUSTRY_KEYS` aus [[Phonbot/Backend-Templates|templates.ts]]: arbitrary strings 400'en
- 404 wenn Tenant nicht existiert; 409 wenn Industry schon gesetzt (kein Overwrite); dryRun-Branch returnt counts ohne Writes
- `jsonb_set(data, '{industry}', to_jsonb($1::text))` — atomar, kein Read-Modify-Write
- M4-Fix: parallel `UPDATE call_transcripts SET industry WHERE org_id = ... AND (industry IS NULL OR industry = '')` — sonst bleibt das Cross-Org-Learning-Pool-Mapping für historische Calls leer

**Tests (13/13 grün):**
- [[Phonbot/Tests/webhook-secret-derivation|webhook-secret-derivation.test.ts]] — pinned die Precedence-Regel die R13 in env.ts hard-required gemacht hat. Bewacht gegen Customer-Webhook-Validator-Bruch bei JWT-Rotation.
- [[Phonbot/Tests/agent-instructions-recording|agent-instructions-recording.test.ts]] — pinned dass recordCalls=false den Aufzeichnungshinweis-Block aus dem System-Prompt rauslässt + recordCalls=undefined als legacy-on behandelt wird.
- [[Phonbot/Tests/template-learning-industry|template-learning-industry.test.ts]] — pinned dass ohne `industry`-Tag kein Cross-Org-Pool-Read passiert (early-return) und dass der `share_patterns`-Consent-Gate vor allem anderen sitzt.

**Codex Code-Review (1. Pass):** 0 Blocker, 2 HIGH, 4 MEDIUMs, 5 LOW. Vor Commit gefixt:
- A1 (Race) → advisory-lock + tx-Wrap
- A4 (Auth) → aud-check
- A6 (rate-limit) → 30/min
- D2 (env-leak in test) → afterAll unstubAllEnvs

**Codex Verify-Pass (2. Pass):** „verify-pass clean, ship".

**Commit:** `01858ca` auf feature-branch `round-14-industry-backfill` gepusht (master-direkt-push war hart geblockt, deshalb Branch + PR). PR-URL: https://github.com/haskallalk-eng/voice-agent-phonbot/pull/new/round-14-industry-backfill — manuell öffnen weil `gh` CLI nicht installiert ist.

**Bewusst auf R15 verschoben:**
- M2 `RETELL_TOOL_AUTH_SECRET` hard-required (Pflicht bevor JWT_SECRET rotiert wird, sonst brechen Retell-Tool-URLs)
- M3 Stripe-deleted/pause/resume-Branches: nutzen noch `sub.metadata.orgId` statt des `stripe_customer_id`-Mappings
- A3 batched call_transcripts-UPDATE für sehr grosse Tenants
- E1/E2/E3 Integration-Tests für Backfill-Route + privacy_setting_changes-Persistenz + Concurrency-Regression
- (c) Verify-Forwarding live-smoke — Hardware-only, nicht durch Claude testbar
- (d) JWT_SECRET-Rotation — operativ, User-Go nötig

[[Daily/2026-04-30]]

## Audit Round 15 — RETELL_TOOL_AUTH_SECRET soft-warn + Stripe customer_id resolver (2026-04-30)

Pattern: User hat Plan-Review übersprungen ("ok weiter"), Code direkt geschrieben, Codex-Code-Review danach.

**M2 — RETELL_TOOL_AUTH_SECRET (env.ts soft-warn):** Identisch zur R7→R13-Migration für WEBHOOK_SIGNING_SECRET. Existing Retell-Agents in prod haben ihre tool_sig mit JWT_SECRET signiert — hard-required ohne migration-period würde sie alle brechen. Diese Round nur die Warning + .env.example-Doku; Promotion zu REQUIRED_PROD_SECRETS in einer Folge-Round wenn prod migriert ist. Code in agent-config.ts:554 + retell-webhooks.ts:271 unverändert.

**M3 — Stripe customer_id-Resolver (billing.ts):** `resolveOrgIdFromSubscription(sub)` exportiert. Vier Stripe-Webhook-Branches umgestellt (deleted/paused/resumed/created) — jeder mit log.warn+skip wenn der Resolver null returnt. syncSubscription:402-418 bleibt mit eigener Inline-Form (mutiert orgId im Verlauf, Resolver-Shape passt nicht).

**Tests (8 cases):** [[Phonbot/Tests/billing-resolve-orgid|billing-resolve-orgid.test.ts]] — DB-vs-metadata precedence (match + mismatch mit Warn-Assert), metadata-fallback bei DB-miss, null-bei-beiden-leer, no-DB-call wenn customer fehlt, expanded-Customer + DeletedCustomer.

**Codex Review:** 1 HIGH (stale Mock-Export-Names im Test) + 2 LOWs (Warn-Assert fehlte, DeletedCustomer-Case fehlte). Tests liefen trotz HIGH grün weil der Resolver-Pfad die fehlenden Email-Functions nie aufruft — latenter Bug für künftige Webhook-Branch-Tests. Alle drei vor Commit gefixt.

**Verifikation:** pnpm typecheck clean, 21/21 audit-tests grün (R14: 13 + R15: 8).

**Commit:** `494c0d5 feat(audit-round-15): RETELL_TOOL_AUTH_SECRET soft-warn + Stripe customer_id resolver`, gestapelt auf `round-14-industry-backfill`. Beim Merge des PR landen R14 + R15 zusammen.

**R16-Backlog:**
- RETELL_TOOL_AUTH_SECRET → REQUIRED_PROD_SECRETS (nach prod-env-Migration)
- Subscription pause/resume Integration-Tests via Fastify-inject + raw stripe-event-fixtures
- Last-resort `WHERE stripe_subscription_id = $1` Fallback wenn meta+customer beide leer (Codex MEDIUM B4)
- A3 batched UPDATE call_transcripts (für sehr grosse Tenants)
- E1/E2/E3 Integration-Tests für Backfill-Route + privacy_setting_changes-Persistenz

[[Daily/2026-04-30]]

## Audit Round 16 — backfill batched + 3-tier resolver + integration tests (2026-04-30)

Pattern: Codex Plan-Review zuerst (synchron), dann Code, dann Codex-Review (war im Cooldown bei der zweiten Sitzung — Self-Review ergänzt). Alle vier deferred Items aus R15 angepackt; E2 deferred zu R17 weil Codex es als „lower-leverage" eingestuft hatte.

**(3) Last-resort `stripe_subscription_id` fallback** (Codex MEDIUM B4 aus R15) in [[Phonbot/Backend-Billing|billing.ts]]: 3-tier-chain customer-mapping → metadata.orgId → subscription-id-mapping. Schritt 3 fängt Import-Orphan-Edge-Cases (Stripe-CLI / support-team-subs ohne metadata + ohne customer-mapping) — sonst no-op-silent. Returnt null nur wenn alle drei misses.

**(4) Backfill phase-1/phase-2 split** (Codex Plan-Review HIGH C): in [[Phonbot/Backend-Insights|insights.ts]] gab's einen kritischen Caveat — batching INNERHALB des advisory-xact-locks defeats den Purpose, weil der Lock bis COMMIT hält. Fix: Phase 1 (configs UPDATE) committed + released den Lock; Phase 2 (transcripts) läuft danach als auto-committed `pool.query`-Loop in 1000er-Batches mit 1M-Row hard-ceiling. `client.release()` exakt einmal via try/finally; Phase 2 nutzt `pool` direkt. Idempotency-Caveat dokumentiert inline: ein mid-batch crash hinterlässt partial-backfill den der zweite admin-call NICHT resumen kann (config-409-gate triggert) — separater `/admin/agents/backfill-transcripts` Endpoint im R17-backlog.

**(2) Stripe webhook integration tests** (Codex Plan-Review HIGH D): „NICHT constructEvent mocken" — die security-kritische Logik IST der raw-body+signature-verify-pfad. Stattdessen `Stripe.webhooks.generateTestHeaderString` mit fixture-secret. 5 cases: invalid-sig 400, paused→UPDATE, resumed→UPDATE, unresolvable-orgId→warn+skip (deckt expliziet alle 3 resolver-tiers miss), dedup-200.

**(E1+E3) Backfill-route Integration-Tests** (10 cases, decken: auth/aud-gating, curated-key-validation, 404/409, dryRun-no-write, happy-path mit Phase-1/Phase-2-wiring + release-once-assertion, advisory-lock SQL + deterministische key-derivation pin, post-lock-release-simulation).

**Mock-State-Leak gefunden + behoben**: in den Stripe-webhook-tests hatte `vi.clearAllMocks()` nicht gereicht — clears call-history aber NICHT die `mockResolvedValueOnce`-Queue. Ein Test feedete dann residual fixtures aus dem vorherigen Test, was zu falscher 'org-real'-Zuordnung führte. Fix: `mockReset()` per-spy.

**Verifikation:** pnpm typecheck clean, 134/136 vitest run (38/38 audit-tests, R14: 13 + R15: 8 + R16: 17). Die 2 pre-existing auth-flow-Failures sind nicht von R16.

**Codex Code-Review:** Cooldown-bedingt offen — Self-Review der HIGH-/MEDIUM-Punkte aus dem Plan-Review ergab keine Blocker. Selbst-Finding: ein Partial-Index `call_transcripts(org_id) WHERE industry IS NULL OR industry = ''` würde Phase-2-Loop bei 100k+-Tenants drastisch beschleunigen. Schiebe ich auf R17 statt mid-round Schema-Add.

**Commit:** `967b1c7 feat(audit-round-16): backfill batched + 3-tier resolver + integration tests`. Stack auf `round-14-industry-backfill`. Beim Merge des PR landen R14+R15+R16 zusammen (3 Commits, 13 Files, +1490/-90).

**R17-Backlog:**
- Partial Index `call_transcripts(org_id) WHERE industry IS NULL OR industry = ''` für Phase-2 Performance bei riesigen Tenants
- Separater `/admin/agents/backfill-transcripts` Endpoint für resumable transcript-only-backfill nachdem config-row getagged ist
- E2: `privacy_setting_changes.changed_by` Integration-Test via `PUT /agent-config` (lower leverage per Codex)
- 2026-04-26-Audit-Ledger noch offen: `auth HIGH-1`, `billing MEDIUM-1/4`, `calendar MEDIUM-1/2/4`, `tickets HIGH-2` (per R16 Plan-Review F)
- `subscription.deleted` mit `minutes_used`-cap Test (deleted-Variant der stripe-webhook-pause-resume tests)
- RETELL_TOOL_AUTH_SECRET → REQUIRED_PROD_SECRETS (nach prod-env-Migration durch User)
- Codex Code-Review für R16 nachholen (Cooldown war beim Commit aktiv — agent-id `a14ed78cdb08a53a6` reusable nach 20:50)

[[Daily/2026-04-30]]

## Audit Round 17 — Partial Index + deleted-Tests + Privacy-Audit-E2 (2026-05-01)

Branch-Wirrwarr zuerst entwirrt: master enthält R14+R15+R16 via Merge `2cc23d6`. Codex Plan-Review war auf einem stale Snapshot gegründet (behauptete Items fehlten die schon drin sind). Nach Filter wurden 4 Items real angepackt:

1. **Partial Index** `idx_transcripts_org_industry_null` in db.ts für Phase-2-Loop. Codex BLOCKER: muss `CONCURRENTLY` sein, sonst ACCESS-EXCLUSIVE-Lock auf call_transcripts beim ersten prod-rollout. Try/catch-wrapped — failed CONCURRENTLY (kann INVALID-Index hinterlassen) schreibt stderr-WARN, Boot-clean.
2. **subscription.deleted Tests** (2 cases). Pre-existing fixture-bug aufgedeckt: `makeSubscriptionEvent` brauchte `.plan.interval` weil syncSubscription:526 ohne zweites optional-chain liest. paused/resumed waren „lucky" weil sie syncSubscription gar nicht aufrufen. Test-Queues straffer (3 fixtures statt 6) — vorher leftover-fixtures haben echte flow drift maskiert.
3. **E2 Privacy-Audit-Test** (privacy-audit-changed-by.test.ts, 4 cases) — pinned dass `INSERT INTO privacy_setting_changes` die userId aus JWT kriegt (M1-Fix R15). 14 vi.mock()-Calls. primeFlipQueue matched echte Query-Order: tenantIdAvailableOrOwned → loadOwnedConfigRow → enforcePlanAgentLimitOnCreate.SELECT-1 (early-return) → prev recordCalls SELECT → UPSERT → INSERT privacy.
4. **INDEX.md Status-Tabelle** — was seit 2026-04-26 gefixt, was offen.

**Codex Code-Review:** 1 BLOCKER (CONCURRENTLY) + 2 MEDIUM + 4 LOW + 3 NIT. BLOCKER + B-MEDIUM Test-Queue-Cleanup + C-LOW Test-Comment vor Commit gefixt.

**Verifikation:** typecheck clean, 49/49 audit-tests grün (R14:13 + R15:8 + R16:17 + R17:11), 2 pre-existing auth-flow unrelated.

**Commit:** `99aafc3 feat(audit-round-17): partial index + deleted-event tests + privacy audit E2` auf neuem branch `round-17-tech-debt`. PR-URL: https://github.com/haskallalk-eng/voice-agent-phonbot/pull/new/round-17-tech-debt

**R18-Backlog:**
- `/admin/agents/backfill-transcripts` Endpoint für Phase-2-Crash-Recovery (R16-known-limitation)
- `customer.subscription.updated` Route-Test (Companion zu deleted)
- **auth HIGH-1** Refresh-Token Cross-Tab-Race — BroadcastChannel Frontend-Refactor
- **billing MEDIUM-1** mid-cycle Plan-Downgrade `minutes_used` cap
- **calendar MEDIUM-1/2/4** aus 2026-04-26 Audit
- Composite `(org_id, id) WHERE` partial index als R17-NIT — nach erstem prod-Backfill messen
- tickets HIGH-2 (PII im Email-Body) — UX-Konsens vom User nötig

[[Daily/2026-05-01]]

## Audit Round 18 — Backfill-Recovery + Downgrade-Cap + 10 Tests (2026-05-02)

Pattern: Codex Plan-Review → Code → Codex Code-Review → 2 MEDIUM-Fixes → Commit.

**Implementiert:**
1. **`POST /admin/agents/backfill-transcripts`** ([insights.ts](C:/Users/pc105/.openclaw/workspace/voice-agent-saas/apps/api/src/insights.ts)) — Companion zu /admin/agents/backfill-industry für Phase-2-Crash-Recovery (R16 known-limitation). Body `{ orgId, industry?, dryRun? }`. industry derived via SELECT DISTINCT wenn omitted, 409 AMBIGUOUS_INDUSTRY wenn org-configs disagree (Codex Plan-Review B: eine org kann mehrere agent_configs haben). Same batched-loop wie R16-Phase-2.
2. **billing MEDIUM-1 mid-cycle Plan-Downgrade `minutes_used` cap** ([billing.ts](C:/Users/pc105/.openclaw/workspace/voice-agent-saas/apps/api/src/billing.ts)). Pre-UPDATE SELECT widened um minutes_limit zu lesen (Codex C: kein zweiter round-trip). Wenn `newLimit < oldLimit` UND nicht resetMinutes → composition `minutes_used = LEAST(minutes_used, $7::int)` inline. Atomic.
3. **subscription.updated Tests** (3 cases) plus 6 Tests für /admin/agents/backfill-transcripts.

**Codex Code-Review fand 2 MEDIUMs:**
- **B2**: silent free-fallback bei unknown stripe price.id wurde durch R18 destruktiv (würde minutes_used auf 30 cappen wenn ops eine neue Stripe-Price-ID vergisst). Fix: log.warn + suppress LEAST-clause wenn matchedPlan null. Plus regression-Test.
- **C2**: Test-Fixture nutzte fragile unknown-price→free fallback statt echte Starter-PRICE-ID. Fix: STRIPE_PRICE_STARTER env-stub + neuer `priceId`-Param in makeSubscriptionEvent. Plus bind-checks ($2='starter', $7=360).

**Verifikation:** typecheck clean, 151/153 vitest run (2 pre-existing auth-flow). 59/59 audit-tests grün insgesamt (R14:13 + R15:8 + R16:17 + R17:11 + R18:10).

**Commit:** `e8767e5 feat(audit-round-18): backfill-transcripts endpoint + downgrade cap + tests` auf neuem branch `round-18-recovery-and-downgrade`. PR-URL: https://github.com/haskallalk-eng/voice-agent-phonbot/pull/new/round-18-recovery-and-downgrade

**R19-Backlog:**
- billing MEDIUM-4 (syncSubscription SELECT-then-UPDATE race ohne tx — Codex D1)
- auth HIGH-1 BroadcastChannel cross-tab refresh-token race — Frontend-Refactor: BEIDE api.ts UND auth.tsx-Bootstrap müssen channelled werden, nicht nur api.ts (Codex Plan-Review D)
- calendar MEDIUM-2/4 (MEDIUM-1 ist eigentlich schon atomar via Unique-Index, per Codex Plan-Review E)
- backfill-transcripts: org-scoped advisory_xact_lock (Codex A2 LOW), `truncated/maxBatchesHit`-flag (A3 NIT), ORG_NOT_FOUND vs NO_INDUSTRY_CONFIGURED disambiguation (A1 LOW)
- tickets HIGH-2 (PII im Email-Body) — UX-Konsens vom User nötig

[[Daily/2026-05-02]]

## Audit Round 19 — Backfill-Polish + syncSubscription tx (2026-05-02)

Codex Plan-Review empfahl R19 = backfill-polish (A1+A2+A3) + syncSubscription FOR UPDATE wrap (billing MEDIUM-4). Calendar + BroadcastChannel ausdrücklich nach R20.

**Implementiert (4 Items):**
1. **A1 ORG_NOT_FOUND disambiguation** in [insights.ts](C:/Users/pc105/.openclaw/workspace/voice-agent-saas/apps/api/src/insights.ts) — EXISTS-check vor industry-derive. typo'd orgId kriegt klar 404 ORG_NOT_FOUND statt misleading NO_INDUSTRY_CONFIGURED.
2. **A2 pg_try_advisory_lock auf dedicated client** — Codex Code-Review fand BLOCKER: lock via pool.query, unlock via pool.query → verschiedene connections, unlock no-op auf B, A behält lock 30s. Fix: `lockClient = await pool.connect()` so dass try_advisory_lock + alle batch UPDATEs + unlock alle die same connection nutzen. 423 LOCKED bei contention.
3. **A3 truncated/maxBatchesHit flag** — surface MAX_BATCHES-hit im response + log.warn.
4. **billing MEDIUM-4 syncSubscription tx** in [billing.ts](C:/Users/pc105/.openclaw/workspace/voice-agent-saas/apps/api/src/billing.ts) — pre-UPDATE SELECT + UPDATE jetzt in single client.connect()-tx mit BEGIN/SELECT FOR UPDATE/UPDATE/COMMIT. Vorher konnte webhook+sofort-sync-race beide period_end lesen → beide resetMinutes=true → double-wipe. FOR UPDATE serialisiert.

**Codex Code-Review:** 1 BLOCKER (advisory_lock connection-share) + 4 LOW + 1 MEDIUM (test-fixture brittleness — R20-backlog). BLOCKER vor commit gefixt.

**Tests:** 19/19 backfill + 11/11 webhook = 30/30. Plus mockRelease-assertions die die BLOCKER-fix pinnen (exactly one client.release in finally, auch bei LOCKED early-return).

**Verifikation:** typecheck clean, 153/155 vitest (2 pre-existing). Audit-Tests R14:13 + R15:8 + R16:17 + R17:11 + R18:10 + R19:8 = 67 grün insgesamt.

**INDEX.md:** billing MEDIUM-1 + MEDIUM-4 als GEFIXT markiert.

**Commit:** `5fdb14a feat(audit-round-19): backfill-transcripts polish + syncSubscription tx` auf neuem branch `round-19-polish-and-tx`. PR-URL: https://github.com/haskallalk-eng/voice-agent-phonbot/pull/new/round-19-polish-and-tx

**R20-Backlog:**
- **auth HIGH-1 BroadcastChannel** Frontend-Refactor (Codex Plan-Review D: 4-message-type handshake, 10-15s claim timeout, BEIDE api.ts + auth.tsx-Bootstrap channelen)
- calendar MEDIUM-2 (silent-skip bei broken connections)
- calendar MEDIUM-4 (multi-provider booking eventId arbitrary nach erst-success ordering)
- ticket HIGH-2 (PII Email — UX-Konsens)
- Test-fixture builder für pool/client query split (Codex R19 review E)
- composite (org_id, id) WHERE partial index nach prod-measurement
- RETELL_TOOL_AUTH_SECRET → REQUIRED_PROD_SECRETS promotion (User-Go nötig)

[[Daily/2026-05-02]]

---

- **Abbruch-Kriterium (User-Vorgabe):** Wenn der erste Live-Smoke-Test nach 1-2 Sessions immer noch nicht zuverlässig funktioniert → **rauswerfen statt halbgares Theater behalten**. Endpoint löschen, Frontend-UI zeigt nur die manuelle Test-Anleitung, `verified`-Spalte für `forwarding`-Records bleibt false.