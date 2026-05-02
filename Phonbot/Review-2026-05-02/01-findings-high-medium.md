# Phonbot Review 2026-05-02 - Findings

## HIGH-01 Voice clone ist nicht tenant-scoped
Beleg: `apps/api/src/voices.ts:39-46` liefert fuer jeden authentifizierten User `listVoices()` ungefiltert aus dem Retell-Account. `apps/api/src/voices.ts:79-145` erstellt Clone-Voices, speichert aber keine `orgId`-Ownership. `apps/api/src/agent-config.ts:48` akzeptiert beliebige Voice-IDs, und `apps/api/src/agent-config.ts:691`, `apps/api/src/agent-config.ts:717`, `apps/api/src/agent-config.ts:743` geben diese ID an Retell weiter.

Warum echter Bug: geklonte Stimmen sind tenant-spezifische Audio-/Identitaetsassets. Der Code hat weder Registry noch Ownership-Pruefung; dadurch koennen andere Tenants gelistete Clone-IDs sehen und in eigenen Agents verwenden.

Fix-Risiko: mittel-hoch. Eine org-scoped Voice-Registry braucht Migration/Backfill und muss eingebaute Retell-Voices, kuratierte Empfehlungen und bestehende Agent-Konfigurationen weiter erlauben.

## HIGH-02 Auth refresh rotiert pro Cookie, aber Cross-Tab ist nicht koordiniert
Beleg: `apps/api/src/auth.ts:810-818` rotiert Refresh-Tokens per `DELETE ... RETURNING` und gibt bei fehlendem Token 401. Frontend coalesct nur im Tab via modul-lokalem `refreshInFlight` in `apps/web/src/lib/api.ts:43-65`; bei 401 wird lokal Token geloescht/redirected in `apps/web/src/lib/api.ts:75-87`. `AuthProvider` bootstrapped ebenfalls direkt per Refresh in `apps/web/src/lib/auth.tsx:83-101`, `apps/web/src/lib/auth.tsx:123-154`; Logout bleibt lokal in `apps/web/src/lib/auth.tsx:206-222`.

Warum echter Bug: zwei Tabs mit demselben Refresh-Cookie koennen parallel refreshen. Der erste gewinnt und rotiert, der zweite sieht den geloeschten Token und loescht Cookie/Session lokal. `rg` findet keinen `BroadcastChannel` in `apps/web/src/lib/api.ts` oder `apps/web/src/lib/auth.tsx`.

Fix-Risiko: mittel. BroadcastChannel/Lock braucht Tab-ID, Claim-Timeout, Success/Failed und Session-Cleared; falsche Implementierung kann Deadlocks, Token-Leaks zwischen Tabs oder Redirect-Loops erzeugen.

## HIGH-03 Onboarding Google Calendar Connect navigiert auf JWT-geschuetzten API-Redirect
Beleg: `apps/api/src/index.ts:182-189` authentifiziert API-Routen nur per `req.jwtVerify()`. `apps/api/src/calendar.ts:1765-1789` schuetzt `/calendar/google/connect` mit `app.authenticate`. Der korrekte JSON-Flow existiert in `apps/api/src/calendar.ts:1734-1758` und wird auf der CalendarPage in `apps/web/src/ui/CalendarPage.tsx:896` genutzt. Onboarding nutzt dagegen direkte Browser-Navigation in `apps/web/src/ui/onboarding/OnboardingWizard.tsx:831`.

Warum echter Bug: bei `window.location.href = '/api/calendar/google/connect'` sendet der Browser keinen Authorization-Header. Refresh-Cookie hilft nicht, weil `authenticate` nicht aus dem Refresh-Cookie liest. Ergebnis ist 401 statt OAuth-Redirect im Onboarding.

Fix-Risiko: niedrig. Onboarding sollte wie CalendarPage `getGoogleCalendarAuthUrl()` nutzen; dabei Loading/Error-State beibehalten.

## MEDIUM-01 Calendar Status/Disconnect kollabiert Multi-Provider auf eine beliebige Connection
Beleg: DB/Code erlauben mehrere Provider pro Org (`apps/api/src/calendar.ts:133-154`). Booking/Synchronisation lesen alle Connections ueber `getAllConnections`/`getCheckableConnections` in `apps/api/src/calendar.ts:354-401` und `apps/api/src/calendar.ts:1541`. Status nutzt aber `SELECT ... LIMIT 1` in `apps/api/src/calendar.ts:345-351` und `apps/api/src/calendar.ts:1976`. Disconnect loescht alle Provider mit `DELETE FROM calendar_connections WHERE org_id = $1` in `apps/api/src/calendar.ts:2024-2040`.

Warum echter Bug: ein Tenant kann mehrere Kalender-Provider haben, aber UI/API-Status zeigt nur einen beliebigen Provider. Ein vermeintliches Disconnect fuer den sichtbaren Provider entfernt alle Kalender-Integrationen.

Fix-Risiko: mittel. Entweder API auf `connections[]` erweitern oder Produktentscheidung "nur ein Provider" technisch erzwingen; beide Varianten brauchen Frontend-/API-Kompatibilitaet.

## MEDIUM-02 Billing `syncSubscription` hat Read-Then-Update-Race beim Periodenwechsel
Beleg: `apps/api/src/billing.ts:497-510` liest `current_period_end` separat, setzt daraus `resetMinutes`, und `apps/api/src/billing.ts:512-530` updated danach `orgs` inklusive optional `minutes_used = 0`. Derselbe Sync laeuft nach Sofort-Sync in `apps/api/src/billing.ts:642-647` und aus Webhooks in `apps/api/src/billing.ts:762-790`.

Warum echter Bug: parallele `syncSubscription`-Calls koennen beide denselben alten Periodenwert lesen und danach konkurrierend updaten. Besonders riskant ist ein stale Stripe-Event gegen Sofort-Sync oder Renewal-Reset gegen laufende Nutzung; letzter Writer gewinnt ohne Lock/Transaktion.

Fix-Risiko: mittel. `SELECT ... FOR UPDATE` auf `orgs.id` in einer Transaktion reicht, sobald `orgId` bestimmt ist; ein Advisory-Lock pro Org ist nur noetig, wenn vor der Row-Lock-Aufloesung oder ueber mehrere Tabellen/Eventpfade serialisiert werden muss. Zusaetzlich sollte stale-event/monotonic-period-Logik geprueft werden.

## MEDIUM-03 Backfill industry/transcripts ist nach Config-Commit nicht ueber denselben Endpoint resumierbar
Beleg: Phase 1 setzt `agent_configs.data.industry` in einer Transaktion und committet in `apps/api/src/insights.ts:1586-1659`. Danach blockiert `row.industry` weitere Laeufe mit `ALREADY_TAGGED` in `apps/api/src/insights.ts:1601-1607`. Phase 2 laeuft danach best-effort in Batches in `apps/api/src/insights.ts:1667-1697`. Der harte Cap liegt bei `MAX_BATCHES = 1000` in `apps/api/src/insights.ts:1678-1679`, die Response gibt aber nur `transcriptsUpdated` zurueck in `apps/api/src/insights.ts:1705-1713`.

Warum echter Bug: Crash, Partial-Run oder 1M-Cap nach Config-Commit kann unvollstaendige Transcript-Daten hinterlassen, waehrend ein Rerun des gleichen Admin-Flows durch `ALREADY_TAGGED` abgewiesen wird.

Fix-Risiko: niedrig-mittel. Resume-Endpoint oder same-industry-resume plus Response-Felder `truncated`/`maxBatchesHit` sind gut isoliert; wichtig ist, keine fremde oder bewusst gesetzte Industry zu ueberschreiben.

## MEDIUM-04 Admin Bulk-Read-Audit ist inkonsistent
Beleg: Audit-Infra existiert in `apps/api/src/admin.ts:22-35` und `apps/api/src/db.ts:717-729`. Auditiert sind u.a. `/admin/leads`, `/admin/leads/stats`, `/admin/demo-calls` in `apps/api/src/admin.ts:164`, `apps/api/src/admin.ts:209`, `apps/api/src/admin.ts:301`. Nicht auditiert sind weitere bulk/cross-org GETs wie `/admin/learnings` in `apps/api/src/admin.ts:636-710`, `/admin/learnings/corrections` in `apps/api/src/admin.ts:978-1008`, `/admin/users` in `apps/api/src/admin.ts:1063-1081` und `/admin/orgs` in `apps/api/src/admin.ts:1085-1116`.

Warum echter Bug: die Tabelle ist explizit fuer cross-org Admin-GETs dokumentiert, aber neuere Admin-Leseendpunkte mit potentiell sensiblen Inhalten schreiben keinen Audit-Eintrag.

Fix-Risiko: niedrig-mittel. `recordAdminRead` ist fire-and-forget; Regression-Risiko liegt vor allem darin, sensitive Query-Inhalte versehentlich in `params` zu persistieren oder Routen-Latenz durch falsches Awaiting zu erhoehen.

## LOW-01 Frontend Phone-Fetches umgehen den zentralen Refresh-Wrapper
Beleg: zentraler 401-Refresh steckt in `apps/web/src/lib/api.ts:68-94`; `getPhoneNumbers()` nutzt ihn in `apps/web/src/lib/api.ts:387-388`. Agent Builder ruft `/api/phone` aber direkt auf in `apps/web/src/ui/agent-builder/AgentListView.tsx:7-18` und `apps/web/src/ui/agent-builder/index.tsx:116-125`. Onboarding-Provision nutzt ebenfalls direkten Fetch in `apps/web/src/ui/onboarding/OnboardingWizard.tsx:247-268`.

Warum echter Bug: nach Access-JWT-Ablauf refreshen diese Pfade nicht. Bei `/api/phone` wird zudem `r.ok` nicht geprueft; 401-JSON kann als leere `items`-Liste interpretiert werden und UI faelschlich "keine Nummer" anzeigen.

Fix-Risiko: niedrig. Auf vorhandene API-Helpers oder gemeinsamen Fetch-Wrapper umstellen; auf Import-Zyklen und bestehende Onboarding-Fehlertexte achten.

## Nicht als harter Bug gewertet: Email Enumeration bei Signup/Checkout
Beleg: Register/Checkout geben bei existierender Mail 409 zurueck in `apps/api/src/auth.ts:284-291`, `apps/api/src/auth.ts:331-334`, `apps/api/src/auth.ts:382-388`; Forgot-Password vermeidet Enumeration bewusst in `apps/api/src/auth.ts:614-630`, `apps/api/src/auth.ts:657`.

Bewertung: echtes Security-/Privacy-Risiko, aber nicht eindeutig Bug ohne Produkt-/UX-Policy, weil viele Signup-Flows Duplicate-Mail sichtbar machen. Fix-Risiko waere mittel-hoch wegen Checkout- und Account-Recovery-UX.
