# Phonbot Review 2026-05-02 - Modulnotizen

## Auth und Session
Gefundener Bug: Cross-Tab-Refresh/Logout-Koordination fehlt; siehe HIGH-02. Belege: Rotation in `apps/api/src/auth.ts:810-818`, lokales `refreshInFlight` in `apps/web/src/lib/api.ts:43-65`, lokaler Logout in `apps/web/src/lib/auth.tsx:206-222`.

Nicht als harter Bug gezaehlt: Email-Enumeration bei Signup/Checkout, weil das ohne Produkt-Policy nicht eindeutig falsch ist; Belege in `apps/api/src/auth.ts:284-291`, `apps/api/src/auth.ts:331-334`, `apps/api/src/auth.ts:382-388`.

## Voice und Agent Config
Gefundener Bug: Voice-Clone/Voice-Auswahl ist nicht tenant-scoped; siehe HIGH-01. Belege: `apps/api/src/voices.ts:39-46`, `apps/api/src/voices.ts:79-145`, `apps/api/src/agent-config.ts:48`, `apps/api/src/agent-config.ts:691`, `apps/api/src/agent-config.ts:717`, `apps/api/src/agent-config.ts:743`.

Rest-Risiko: Fix darf Default-/Catalog-Voices nicht faelschlich blockieren und muss alte Agent-Konfigurationen mit Clone-IDs migrieren oder grandfathern.

## Calendar
Gefundene Bugs: Onboarding-Google-Connect nutzt falschen Auth-Flow; siehe HIGH-03. Multi-Provider-Status/Disconnect ist inkonsistent; siehe MEDIUM-01.

Akzeptierte Produktlogik, nicht als Bug gezaehlt: `getCheckableConnections` schliesst kaputte Kalender aus und faellt auf Chipy zurueck (`apps/api/src/calendar.ts:385-401`, `apps/api/src/calendar.ts:1541-1559`). Das kann zu Chipy-only Buchungen fuehren, ist im Kommentar aber explizit als Resilience-Entscheidung beschrieben.

## Billing
Gefundener Bug: `syncSubscription` liest Periodenstatus und updated getrennt ohne Lock/Transaktion; siehe MEDIUM-02. Belege: `apps/api/src/billing.ts:497-530`, Aufrufe in `apps/api/src/billing.ts:642-647`, `apps/api/src/billing.ts:762-790`.

Fix-Hinweis: Row-Lock auf `orgs` innerhalb einer Transaktion ist der minimale Scope, sobald `orgId` bekannt ist. Advisory-Lock nur einsetzen, wenn alle Eventpfade vor der Row-Lock-Aufloesung serialisiert werden muessen.

## Insights, Backfill und Admin
Gefundene Bugs: Backfill-Transcript-Phase ist nach Config-Commit nicht ueber denselben Endpoint resumierbar; siehe MEDIUM-03. Admin-Bulk-Read-Audit ist inkonsistent; siehe MEDIUM-04.

Belege: Backfill-Commit/Gate/Batching in `apps/api/src/insights.ts:1586-1713`; Audit-Infra in `apps/api/src/admin.ts:22-35`, `apps/api/src/db.ts:717-729`; fehlende Audit-Calls bei `apps/api/src/admin.ts:636-710`, `apps/api/src/admin.ts:978-1008`, `apps/api/src/admin.ts:1063-1116`.

## Frontend Agent Builder und Onboarding
Gefundene Bugs: Phone-Fetches umgehen Refresh-Wrapper; siehe LOW-01. Google Calendar Onboarding nutzt direkten API-Redirect; siehe HIGH-03.

Belege: direkter `/api/phone`-Fetch in `apps/web/src/ui/agent-builder/AgentListView.tsx:7-18` und `apps/web/src/ui/agent-builder/index.tsx:116-125`; direkter Phone-Provision-Fetch in `apps/web/src/ui/onboarding/OnboardingWizard.tsx:247-268`; direkter Google-Redirect in `apps/web/src/ui/onboarding/OnboardingWizard.tsx:831`.

## Phone
Kein harter Bug im inspizierten Hauptpfad gefunden. Phone-Migration und Twilio-Sync sind beim API-Start verdrahtet (`apps/api/src/index.ts:196`, `apps/api/src/index.ts:223-225`), und Provision/Forwarding-Pfade sind org-/auth-/plan-gebunden im geprueften Code.

Rest-Risiko: direkte Frontend-Fetches koennen Phone-Status falsch darstellen; das ist unter LOW-01 erfasst.

## Tickets
Kein harter Bug im inspizierten Pfad gefunden. Owner-/Org-Aufloesung und Fehlerbehandlung fuer Notification-Mail sind vorhanden.

Rest-Risiko: Ticket-Mail enthaelt je nach Policy PII. Ohne Vorgabe "Mail darf nur Link/ID enthalten" wurde das nicht als Bug gewertet.

## Integrations, Webhooks, Knowledge, Chat, Copilot
Kein harter Bug im inspizierten Pfad gefunden. Integrations/Webhooks haben SSRF-/Timeout-/Body-Schutz; Knowledge-PDF und Agent-Knowledge-Zuordnung sind org-/tenant-scoped; Chat/Copilot haben Auth-/Org-Scope-/Budget-Guards.

Rest-Risiko: SSRF-DNS-Rebinding-TOCTOU ist im Code als v2-Grenze dokumentiert, aber nicht als aktueller Bug gewertet, solange die bestehende Guard-Policy akzeptiert ist.
