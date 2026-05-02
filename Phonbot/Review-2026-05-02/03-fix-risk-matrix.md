# Phonbot Review 2026-05-02 - Fix-Risk-Matrix

## Empfohlene Reihenfolge
1. HIGH-03 Onboarding Google Calendar Connect: niedriger Fix-Aufwand, hoher sichtbarer Nutzerimpact.
2. LOW-01 Phone-Fetches ueber Wrapper: niedriger Fix-Aufwand, reduziert falsche UI-Zustaende nach Token-Ablauf.
3. MEDIUM-02 Billing Race: transaktional sauber fixen, danach Tests gegen Webhook/Sofort-Sync.
4. MEDIUM-03 Backfill Resume/Truncation: operativ wichtig, kleiner API-Scope.
5. HIGH-02 BroadcastChannel Session Coordination: mittlerer Frontend-Architektur-Scope, gut testbar mit Multi-Tab-Simulation.
6. MEDIUM-01 Calendar Multi-Provider Status/Disconnect: braucht API-/UX-Entscheidung, daher nicht neben kleinen Fixes verstecken.
7. HIGH-01 Voice Tenant Scope: sicherheitsrelevant, aber Migration/Ownership-Modell vorher entwerfen.
8. MEDIUM-04 Admin Audit Coverage: isoliert, aber Datenschutz-Logging bewusst parametrieren.

## Regression-Risiken
HIGH-01 Voice Tenant Scope: Risiko, bestehende Agents mit Retell-Builtins oder alten Clone-IDs zu blockieren. Schutz: Builtin-Allowlist plus Migration/Grandfathering fuer bestehende configs.

HIGH-02 BroadcastChannel: Risiko, Refresh-Deadlocks oder Token-Verlust in Tabs zu erzeugen. Schutz: Tab-ID, 5s Claim-Timeout, `refresh-success`, `refresh-failed`, `session-cleared`, und Timeout-Fallback auf eigenen Refresh.

HIGH-03 Google Onboarding: geringes Risiko. Schutz: denselben Helper wie CalendarPage nutzen und Button-State/Error-State nicht verlieren.

MEDIUM-01 Calendar Multi-Provider: Risiko, bestehende API-Clients mit Single-Status-Shape zu brechen. Schutz: additive `connections[]`-Response oder explizite Ein-Provider-Migration mit Backcompat-Feldern.

MEDIUM-02 Billing Race: Risiko, Locks falsch zu ordnen und Webhook-Latenz/Deadlocks zu erzeugen. Schutz: kurze Transaktion, `SELECT ... FOR UPDATE` auf `orgs`, monotonic/stale Stripe-Event-Pruefung, keine Netzwerkcalls in der DB-Transaktion.

MEDIUM-03 Backfill: Risiko, bewusst gesetzte Industry zu ueberschreiben. Schutz: Resume nur fuer same-industry oder separaten transcript-only Endpoint; Response um `truncated` und `maxBatchesHit` erweitern.

MEDIUM-04 Admin Audit: Risiko, sensitive Querywerte dauerhaft zu speichern. Schutz: Params whitelist/sanitize; `recordAdminRead` weiter fire-and-forget lassen.

LOW-01 Phone Fetches: Risiko, Import-Zyklen im Frontend zu erzeugen. Schutz: bestehende API-Helper nutzen oder kleinen shared auth-fetch helper extrahieren.

## Kurzbewertung
Die realen Low-Risk-Fixes sind Google-Onboarding, Phone-Fetches, Backfill-Response/Resume und Admin-Audit. Die architektonisch riskanteren Fixes sind Voice-Tenant-Scope, BroadcastChannel und Calendar-Multi-Provider.
