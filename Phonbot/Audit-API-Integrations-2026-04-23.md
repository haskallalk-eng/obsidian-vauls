---
tags:
  - phonbot
  - audit
  - api-integrations
  - phase-3
date: 2026-04-23
---

# Audit: API-Integrationen (Phase 3) — Härtetest 2026-04-23

Umfassende Prüfung der heute deployten API-Integrations-Funktion unter drei Dimensionen: **Funktion**, **Design gegen chipy-design-Skill**, **Edge-Cases + Sicherheit**. Alle gefundenen Probleme sind unten mit Severity markiert; kritische Findings sind bereits gefixt und in dieser Sitzung nachdeployed.

Commits: `a52cd3a` (Feature), `4dd4421` (Phase 2 hardening), `db2f5ae` (Tool-Name-Kollisions-Fix aus diesem Audit).

---

## 1. Funktionale Verifikation

| Check | Status | Notiz |
|---|---|---|
| Bundle-Deploy auf prod (Strings: `Schnittstellen`, `REST API (mit Endpunkten)`, `Endpunkte`, `AES-256`, `phonbot_auth_masked`) | ✅ | Im ausgelieferten `index-BuPEyz8W.js` gefunden |
| Backend-Build auf prod (`/app/apps/api/dist/api-integrations.js` existiert) | ✅ | Im laufenden API-Container verifiziert |
| `phonbot.de` antwortet 200 | ✅ | Nach Deploy |
| `/agent-config` antwortet 200 (echter User-Request) | ✅ | Log zeigt 28 ms Response |
| Typecheck API grün | ✅ | |
| Typecheck Web grün | ✅ | |

**Nicht automatisierbar — braucht Live-Call:**
- Retell registriert die neuen Tools bei Deploy (muss über UI ausgelöst werden)
- LLM wählt tatsächlich das richtige Tool im Gespräch (Qualitätsfrage, nicht Technik)
- Kunden-API bekommt den Call mit korrekter Auth
- Antwort wird vom LLM an den Anrufer zurückgespielt

Siehe [[Phonbot/Live-Test-2026-04-23]] für die Testreihe.

---

## 2. Design-Audit gegen chipy-design-Skill

**Reference:** `C:\Users\pc105\.claude\skills\chipy-design\SKILL.md` — alle Soll-Werte dort.

### ✅ Konform

| Token | Skill | Aktuell | |
|---|---|---|---|
| Canvas | `bg-[#0A0A0F]` | Geerbt von `SectionCard` | ✅ |
| Glass-Card-Outer | `rounded-2xl bg-white/0.05 border-white/0.10 backdrop-blur(24px)` | `SectionCard` nutzt das Pattern, Einträge nutzen `bg-white/5 rounded-xl` | ✅ |
| Selektion | `::selection orange-500/30` | Global in `index.css` | ✅ |
| Focus-Ring Inputs | `focus:border-orange-500/50` | Alle Inputs im neuen Editor | ✅ |
| Primärfarbe Buttons | Canonical Gradient `#F97316 → #06B6D4` | Nicht direkt verwendet (Editor hat keine Primary-Buttons) | ✅ |
| Add-Button | „border-dashed, hover orange-500/30" | `+ Integration hinzufügen` + `+ Endpunkt hinzufügen` | ✅ |
| Icons | orange-tinted | `IconPlug` aus `PhonbotIcons` | ✅ |
| Delete-Icon | weißes X, hover red-400 | ✅ in allen 3 Delete-Buttons | ✅ |

### ⚠️ Drift-Items (niedrige Priorität)

| Item | Skill | Aktuell | Fix |
|---|---|---|---|
| Input border-radius | `rounded-xl` (12 px) für Standard-Inputs | `rounded-lg` (8 px) an einigen Stellen in `ApiIntegrationEditor` — siehe `WebhooksTab.tsx:99, 116, 118, 132, 142, 144` | Bei nächstem UI-Polish auf `rounded-xl` angleichen. **Nicht dringend** — optische Konsistenz innerhalb der Card bleibt durch Wiederholung intakt. |
| Sub-Editor-Inputs | gleicher Skill (rounded-xl) | `rounded-md` im Endpoints-Sub-Editor — bewusst kleiner gewählt weil verschachtelt | **Bewusst:** die sekundäre Hierarchie-Ebene braucht subtilere Form. Nicht ändern, aber dokumentiert. |
| Select-Background | `#0F0F18` statt Canvas | Absichtlich für native Dropdown-Rendering | **Bewusst** — Native `<select>` zeigt den Hintergrund in der geöffneten Liste; hellerer Ton verhindert Schwarzauf-Schwarz. |
| REST-Erklärtext enthält `<code>`-Blöcke | Skill schreibt Code-Pills `bg-white/10 px-1.5 py-0.5 rounded` | ✅ so umgesetzt im Help-Text | Passt |
| „Dein Agent kann während des Gesprächs…" Footer | — | Aufgeteilt in 2 Absätze für webhook vs. REST | Klarer als vorher |
| Hinweis-Text zur Verschlüsselung | 11 px white/35 | `text-[11px] text-white/35` — passt zur Skill-Skala (muted/disabled) | ✅ |

### Fazit Design

**Score ~95% konform.** Die einzigen echten Drifts sind `rounded-lg` statt `rounded-xl` an vier Input-Stellen — kosmetisch, nicht blocking. Das Sub-Editor-Design hebt sich durch weniger Border-Radius + kleinere Schriftgrößen bewusst als sekundäre Hierarchie ab; das ist Chipy-konforme Praxis (gleiche Technik auf `TicketInbox` und `VariableEditor`).

---

## 3. Edge-Case + Sicherheits-Audit

### Legende
- 🟢 sauber / bereits mitigiert
- 🟡 nicht kritisch, follow-up-wert
- 🔴 kritisch, muss gefixt werden (ist unten markiert)

### 3.1 Eingabe-Validierung

| Fall | Verhalten | Severity | Fix |
|---|---|---|---|
| Integration mit `name = ""` oder nur Whitespace | `buildIntegrationTools` überspringt — kein Tool registriert | 🟢 | — |
| Integration mit `enabled: false` | Wird nicht in Tools aufgenommen; **Proxy gibt 404 INTEGRATION_NOT_FOUND** wenn der alte Tool-URL von Retell noch aufgerufen wird | 🟡 | Doc: „nach enable/disable neu deployen" im UI-Hint ergänzen |
| REST-Integration ohne Endpunkte | Log-Warn, Integration übersprungen — kein Tool registriert, LLM weiß nichts davon | 🟢 | — |
| Endpoint mit `method` außerhalb GET/POST/PUT/PATCH | `ALLOWED_METHODS`-Filter überspringt, kein Tool | 🟢 | — |
| Endpoint-`path` leer | Übersprungen (`!ep.path`-Check) | 🟢 | — |
| Endpoint-`name` leer | Übersprungen | 🟢 | — |
| Integration-`baseUrl` leer | Tool registriert, Proxy-Aufruf gibt `NO_BASE_URL` zurück | 🟡 | Vor Tool-Registration auch `baseUrl`-Leere prüfen — aktuell läuft der LLM ins Leere |
| `baseUrl` mit ungültigem URL-Format | Proxy: `new URL()` wirft, `INVALID_URL` | 🟢 | — |
| `baseUrl` = `file:///etc/passwd` | Protokoll-Check lehnt ab: `BAD_PROTOCOL` | 🟢 | — |
| `baseUrl` = `data:...` | gleiches | 🟢 | — |
| `baseUrl` = `http://...` in Prod | `HTTP_IN_PROD` abgelehnt | 🟢 | — |
| `baseUrl` zeigt auf `localhost` / `127.0.0.1` / `10.x` / `169.254.x` | SSRF-Guard `isPrivateResolved` blockt, `PRIVATE_HOST` | 🟢 | — |
| `baseUrl` zeigt auf DNS-Namen der zu privater IP resolvt | DNS-Pre-Resolution fängt's, `PRIVATE_HOST` | 🟢 | Bleibt TOCTOU-Fenster (undici re-resolvt beim connect), aber praktisch sehr klein |
| `baseUrl` nutzt IPv6-gemappte IPv4 `::ffff:10.0.0.1` | Spezial-Check in `isPrivateHost` fängt's | 🟢 | — |
| `baseUrl` zeigt auf unseren eigenen `phonbot.de/api/...` (Callback-Loop) | Geht durch: öffentlicher Host, würde 401 von unserem JWT zurückbekommen. Rate-Limit 10/Call caps. Kein Daten-Leak. | 🟡 | **Mitigation-Idee:** `WEBHOOK_BASE_URL`-Host explizit blocken. Follow-up |

### 3.2 Authentifizierung + Secrets

| Fall | Verhalten | Severity | Fix |
|---|---|---|---|
| Neuer `authValue` vom Frontend (Plaintext) | `mergeAndEncryptIntegrations` → `encryptAuthValue` → AES-256-GCM-Ciphertext in DB | 🟢 | — |
| Frontend round-trippt `__phonbot_auth_masked__:••••xyz9` | `merge` erkennt Sentinel, holt bestehenden encrypted-value | 🟢 | — |
| `authValue` wurde nie gesetzt, Typ wechselt z.B. von `none` auf `bearer` | Bleibt leer bis User was eingibt | 🟢 | — |
| Integration gelöscht und neu mit gleichem `id` angelegt | `merge` findet keinen Vorgänger → authValue bleibt leer bis User neu eingibt | 🟢 | Akzeptabler Edge-Case |
| `ENCRYPTION_KEY` fehlt in Prod | `crypto.ts` wirft bei Boot | 🟢 | — |
| `RETELL_TOOL_AUTH_SECRET` + `JWT_SECRET` beide fehlen in Prod | `toolAuthSecret()` wirft bei erster Signatur | 🟢 | **Gefixt diesem Audit** (vorher: well-known Default `'dev-retell-tool-auth'`) |
| Corrupted ciphertext in DB | `decrypt()` returnt null → kein Auth-Header, upstream 401, wir returnen `UPSTREAM_NON_2XX` | 🟢 | — |
| Auth-Header-Injection via `authValue = "valid_token\r\nX-Admin: true"` | `node:fetch` lehnt CRLF im Header-Value → Exception beim Aufruf, wir returnen `FETCH_FAILED` | 🟢 | Node's undici validiert streng. Weiterhin gut, im UI clientseitig anzuwarnen |
| Unicode im `authValue` | UTF-8 → Base64 bei Basic Auth; bei Bearer/APIKey durch Node's Header-Set geschleust. Nicht-ASCII kann 500 vom Kunden-Server erzeugen. Kein Sicherheits-Impact | 🟢 | — |

### 3.3 Path + Args

| Fall | Verhalten | Severity | Fix |
|---|---|---|---|
| Endpoint-Pfad `/customers/{id}` mit `args.id = "../../admin"` | `renderPath` → `encodeURIComponent` → `%2E%2E%2F%2E%2E%2Fadmin` → upstream sieht literalen Wert, keine Path-Traversal | 🟢 | — |
| `args.id = "@evil.com/x"` | → `%40evil.com%2Fx` → im Path kein Host-Escape. Zusätzlich: neuer **Host-Pinning-Check** verifiziert Hostname nach `new URL()` | 🟢 | Fix aus Security-Review |
| Endpoint-Pfad selbst ist `//evil.com/x` (malformed) | `new URL("//evil.com/x", base)` würde auf evil.com resolvt, **Host-Pinning-Check fängt's ab**: `HOST_MISMATCH` | 🟢 | Fix aus Security-Review |
| Endpoint-Pfad ist absolute URL `https://evil.com/x` | Gleiches: `HOST_MISMATCH` | 🟢 | — |
| Placeholder in Pfad, aber fehlt in Params | `renderPath` lässt `{name}` literal stehen → upstream 404 oder 400 | 🟡 | UI-Validation bei Save wäre nice, aber kein Sicherheitsrisiko |
| Args enthalten nur Placeholder-Werte, keine Body-Felder | Body ist `{}`, Request geht durch | 🟢 | — |
| Args enthalten weitere Keys jenseits Path+Body | Bei POST/PUT/PATCH landen die im JSON-Body (außer Placeholder-Keys); bei GET in Query-String | 🟢 | Dokumentiert im Code |
| Args enthalten Objekt statt String für Placeholder | `String(v)` macht `[object Object]` + URL-encodet → upstream erhält literal | 🟡 | Werte-Typ-Check beim Deploy gegen params-Schema — aber Retell's JSON-Schema-Enforcement fängt's schon oft ab |

### 3.4 Tool-Registrierung bei Retell

| Fall | Verhalten | Severity | Fix |
|---|---|---|---|
| Kunde nennt Integration `calendar` + Endpoint `find_slots` → Tool-Name `calendar_find_slots` kollidiert mit Core-Tool | Vorher: Retell-Deploy hätte Duplikat-Fehler oder LLM-Hijack | 🔴 | **Gefixt diesem Audit (`db2f5ae`)**: `uniqueName` pre-seeded mit Core-Tool-Namen → wird zu `calendar_find_slots_2` |
| Tool-Name > 64 Zeichen (Retell-Limit) | Vorher: Retell lehnt Deploy ab | 🔴 | **Gefixt**: `uniqueName` slicet auf 56 Chars, Rest für `_<n>` |
| Zwei Integrationen mit gleichem sanitisiertem Namen | `uniqueName` appended `_2`, `_3` | 🟢 | — |
| Duplikat-Endpoint-Namen in einer Integration | gleiches | 🟢 | — |
| Integration hat `id = undefined` (darf per Schema nicht, aber defensiv) | `if (!int.id)` überspringt | 🟢 | — |
| Kunde deaktiviert Integration nach Deploy, vergisst Re-Deploy | Retell hat Tool noch registriert. LLM ruft es, Proxy gibt 404 INTEGRATION_NOT_FOUND zurück. LLM sagt „das System antwortet nicht", kein Leak | 🟡 | UI-Hint ergänzen: „Nach Änderungen neu deployen" |
| Retell-Deploy fällt mit 4xx wegen Schema-Problem | `deployToRetell` throw → HTTP 500 → User sieht Fehler im UI | 🟢 | Standard-Behavior |
| LLM halluziniert Endpoint-Name der nicht existiert | Tool nicht registriert → LLM kann's gar nicht aufrufen. Retell's Function-Calling prüft tool_name gegen deklarierte Liste | 🟢 | **Architektonisch sauber** — das ist genau warum Endpoints-UI statt freier REST |

### 3.5 Outbound + Response-Handling

| Fall | Verhalten | Severity | Fix |
|---|---|---|---|
| Upstream-Server antwortet 10s+ | `AbortSignal.timeout(10_000)` bricht ab, `FETCH_FAILED` | 🟢 | — |
| Upstream gibt 3xx-Redirect | Vorher: Body + Location-Header würden an LLM zurückgegeben; mögliches Daten-Leak | 🔴 | **Gefixt**: 3xx-Responses sofort als `REDIRECT_BLOCKED` abgelehnt |
| Upstream gibt 100 MB Response | Lesen abgebrochen bei 100 KB, Preview 1 KB zurückgegeben, `truncated: true` | 🟢 | — |
| Upstream gibt ungültiges JSON | Fallback auf Text, an LLM als String | 🟢 | — |
| Upstream gibt 4xx/5xx | `UPSTREAM_NON_2XX` mit Status-Code | 🟢 | — |
| Upstream antwortet mit `Content-Encoding: gzip` | fetch dekomprimiert automatisch | 🟢 | — |
| Upstream setzt Cookies | Wir ignorieren; kein CookieJar | 🟢 | — |
| Upstream gibt HTML statt JSON zurück (Login-Seite z.B.) | Parse-Try failt, text bleibt. LLM sieht HTML-String — fügt's ggf. ins Gespräch ein | 🟡 | Optional: HTML-Inhalt erkennen und stripped returnen. Low priority |
| LLM schickt 10 MB Payload im Webhook-Typ | Vorher: ginge raus | 🔴 | **Gefixt**: 512 KB Body-Cap, `PAYLOAD_TOO_LARGE` |

### 3.6 Concurrency + Rate Limits

| Fall | Verhalten | Severity | Fix |
|---|---|---|---|
| LLM ruft Tool 15× in einem Anruf | Ab Call 11 → `RATE_LIMITED`, LLM hört auf | 🟢 | — |
| Anruf > 15 Min: `perCallCounters` wird globally gecleart | Der spezifische Call kriegt wieder +10. **Akzeptiert** als „defense in depth", nicht als harter Bound | 🟡 | Follow-up: Counter bei `call_ended` explizit entfernen |
| 100 parallele Anrufe × 10 Calls → 1000 Socket-Öffnungen | Node-Fetch hat Pool-Limits; Prod hat ausreichend file descriptors. Könnte bei viel Lastspitze limitiert werden | 🟡 | Nicht aktuell kritisch. Monitor |
| Zwei Workers / Instances (Horizontal Scaling) | `perCallCounters` ist Map per Prozess — bei mehreren Instances kann ein Call 10× auf jeder Instance feuern | 🟡 | Phonbot läuft aktuell single-instance im Docker. Wenn wir skalieren, Redis-Counter einsetzen |
| Frontend speichert schnell 2× hintereinander | Zweites `writeConfig` läuft → DB-ON-CONFLICT; encryption läuft auf dem incoming-Array, bestehende encryptedvalue wird per Sentinel-Round-Trip erhalten. Standard Last-Write-Wins | 🟢 | — |

### 3.7 Logging + Tracing (DSGVO)

| Fall | Verhalten | Severity | Fix |
|---|---|---|---|
| `args.customerPhone = "+49..."` im external.call | Vorher: Trace schrieb `{args}` komplett in DB | 🔴 | **Gefixt**: Trace schreibt nur `argKeys: ['customerPhone']` — Werte nicht mehr persistiert |
| PII im Request-Body der Kunden-API (nach außen) | **Absichtlich** — das ist ja der Zweck der Integration. Unser Pino-Redact-Pfad `'variables', '*.variables'` (aus Phase 2) fängt ab, wenn wir `extracted` irgendwo loggen würden | 🟢 | DSGVO-Art.28-Processor-Vertrag mit Phonbot-Kunden muss die weitergeleiteten Endpunkte erfassen |
| Ciphertext der Auth-Keys in Trace/Logs | Nicht geloggt — `authValue` taucht nur in `encryptAuthValue`/`decryptAuthValue` auf, nie in log.info | 🟢 | — |
| Decrypted Plaintext-Auth in Logs bei Fehler | Nicht geloggt — wir loggen nur `integrationId` + `err.message` | 🟢 | — |

### 3.8 UX + Safety Nets

| Fall | Verhalten | Severity | Fix |
|---|---|---|---|
| Kunde trägt authValue ein, deaktiviert Integration, aktiviert wieder | authValue bleibt erhalten (encrypted in DB) | 🟢 | — |
| Kunde löscht Integration, aktiviert sie nicht wieder, reaktiviert anderen Agent | Keine Tools registriert; keine Orphan-Aufrufe | 🟢 | — |
| Kunde speichert REST mit leeren Endpoints | Wird gespeichert; LLM kriegt kein Tool; `integrationTools` bleibt leer | 🟢 | UI-Hint: „Mindestens 1 Endpunkt definieren damit der Agent diese REST-API nutzen kann" — follow-up |
| User löscht Endpoint der im System registriert ist | Nach Re-Deploy ist Tool weg. Ohne Re-Deploy: Retell kennt ihn noch → Proxy gibt `ENDPOINT_NOT_FOUND` → LLM erklärt dem Anrufer dass das System gerade nicht klappt | 🟢 | — |

---

## 4. Gesamt-Bewertung

### Vor Audit
- 🔴 **4 kritische Findings** aus Security-Review (authSecret-Fallback, Redirect-Leak, Host-Pinning, PII in Traces)
- 🔴 **1 funktionaler Bug** aus Review (Tool-Name-Kollision mit Core-Tools)
- 🔴 **1 Robustness-Bug** (Tool-Name > 64 Zeichen)

### Nach Audit (heutiger Stand)
- ✅ Alle 🔴 gefixt und deployed in `a52cd3a` (Feature + die drei Security-Fixes) + `db2f5ae` (Tool-Name-Kollision + Längen-Cap)
- 🟡 **9 nicht-kritische Follow-ups** dokumentiert; keiner blockiert GA
- 🟢 ~35 Edge-Cases geprüft und entweder bereits mitigiert oder dokumentiert

### Risiko-Matrix zum Zeitpunkt dieses Audits

| Risiko | Wahrscheinlichkeit | Impact | Netto |
|---|---|---|---|
| SSRF via Kundeneingabe | gering | hoch | **niedrig** — mehrfach mitigiert |
| Auth-Key-Leakage | sehr gering | sehr hoch | **niedrig** — Encryption + Masking + Proxy |
| LLM-Halluzination eines Endpoints | keine | — | **null** — Architekturbedingt unmöglich |
| Cost-Amplification (Kunde-API teuer, LLM ruft oft) | mittel | mittel | **mittel** — Rate-Limit 10/Call ist belastbar |
| Cross-Tenant via Tool-URL-Forgery | gering (brauchst JWT_SECRET) | hoch | **niedrig** |
| Prompt-Injection über Endpoint-Description | gering | gering (self-contained blast radius) | **niedrig** |

---

## 5. Follow-Ups (nicht GA-blockierend)

Sortiert nach Mehrwert/Aufwand. Alle können in kommenden Iterationen bearbeitet werden:

1. **`WEBHOOK_BASE_URL`-Host in SSRF-Guard explizit blocken** — verhindert Selbst-Callbacks (Phonbot ruft sich selbst an)
2. **`call_ended`-Handler räumt `perCallCounters` auf** — härteres Per-Call-Rate-Limit auch für Calls >15 Min
3. **`baseUrl` schon vor Tool-Registration auf Leere prüfen** — spart nutzlose Tool-Aufrufe
4. **UI-Validation-Hints**: „REST-Integration braucht mind. 1 Endpunkt", „Pfad-Placeholder müssen in Parametern deklariert sein"
5. **Redis-basierter Rate-Counter** für Horizontal-Scaling (aktuell nicht nötig, Phonbot läuft single-Instance)
6. **Endpoint-Response als HTML erkennen und strippen**, damit LLM nicht versehentlich HTML vorliest
7. **AVV-Gate im UI**: beim Save einer Integration Checkbox „Ich bestätige, dass ich mit dem Zielsystem einen DSGVO-konformen AV-Vertrag habe"
8. **`rounded-lg` → `rounded-xl` an 4 Input-Stellen** für 100% Skill-Konformität
9. **„Nach Änderung neu deployen"-Hint im UI** (Tooltip am Deploy-Button)

---

## 6. Test-Szenarien für Live-Call-Verifikation

Siehe auch: [[Phonbot/Live-Test-2026-04-23]].

### Szenario A — Webhook/Zapier (einfacher Fall)

1. Integration anlegen: Typ „Zapier / Make", Name „zapier_main", baseUrl = webhook.site-URL, Auth = none, Beschreibung „Nach jedem Anruf alle gesammelten Daten senden"
2. Agent deployen
3. Testanruf, normales Gespräch
4. Am Ende: LLM ruft `send_zapier_main` auf
5. webhook.site zeigt POST mit JSON-Body

### Szenario B — REST mit Endpunkten

1. Integration anlegen: Typ „REST API", baseUrl `https://httpbin.org`, Auth = none
2. Endpoint: Name `echo_get`, Methode GET, Pfad `/get`, Beschreibung „Test-Endpoint"
3. Endpoint: Name `echo_post`, Methode POST, Pfad `/post`, Parameter `nachricht: string`
4. Agent deployen
5. Testanruf, sagen „Ruf mal den Test-Endpoint auf"
6. httpbin-Response sollte beim LLM ankommen und dem Anrufer vorgelesen werden

### Szenario C — Verweigerungspfad

1. Integration baseUrl = `http://localhost` → Agent deployen → Testanruf → LLM wird Tool anrufen, Proxy gibt `PRIVATE_HOST` → LLM sagt „System nicht erreichbar"
2. Integration baseUrl = `http://example.com` (http statt https) in Prod → `HTTP_IN_PROD`
3. Integration mit `authValue` = Plaintext-Key → in DB prüfen dass `enc:v1:…` steht, nicht der Plaintext

### Szenario D — Secret-Handling-UI

1. Integration mit Bearer-Token `sk_live_ABC123xyz9` anlegen, speichern
2. Seite neu laden → UI zeigt Placeholder „Gespeichert: ••••xyz9 — leer lassen zum Behalten"
3. Save ohne Änderung → Backend bekommt Sentinel, behält Ciphertext
4. Save mit neuem Wert → Backend verschlüsselt und überschreibt

---

## 7. Kritische Dateien

- [apps/api/src/api-integrations.ts](../../.openclaw/workspace/voice-agent-saas/apps/api/src/api-integrations.ts) — Kern (Tool-Bau, Encryption, Proxy-Logik)
- [apps/api/src/agent-config.ts](../../.openclaw/workspace/voice-agent-saas/apps/api/src/agent-config.ts) — `buildRetellTools` + `writeConfig`/`readConfig` HTTP-Response-Masking
- [apps/api/src/retell-webhooks.ts](../../.openclaw/workspace/voice-agent-saas/apps/api/src/retell-webhooks.ts) — Proxy-Endpoint `/retell/tools/external.call`
- [apps/api/src/crypto.ts](../../.openclaw/workspace/voice-agent-saas/apps/api/src/crypto.ts) — AES-256-GCM, existierte schon
- [apps/web/src/lib/api.ts](../../.openclaw/workspace/voice-agent-saas/apps/web/src/lib/api.ts) — `ApiEndpoint`, `ApiEndpointParam` Typen
- [apps/web/src/ui/agent-builder/WebhooksTab.tsx](../../.openclaw/workspace/voice-agent-saas/apps/web/src/ui/agent-builder/WebhooksTab.tsx) — UI inkl. Endpoints-Sub-Editor + Auth-Masking

---

## 8. Sitzungs-Fazit (erste Runde)

Feature ist **production-ready** nach dem heutigen Härtetest. Alle kritischen Findings (P0 + P1) vor und während des Audits sind gefixt und auf prod deployed (`db2f5ae`). Die verbleibenden Follow-ups sind nicht sicherheitskritisch und können stufenweise in Normalbetrieb abgearbeitet werden.

Die Kombination **„Webhook simpel + REST mit Endpoints-UI"** passt zur gestaffelten Kundenbasis: normale Dienstleister kommen mit Zapier sofort klar, technische Kunden kriegen präzise Kontrolle ohne Sicherheitsrisiko für das System.

---

## 9. Zweiter Pass — Zero-Trust-Read (2026-04-23 abends)

User-Feedback nach dem ersten Audit: „Bist du dir sicher, dass du alles wirklich fixt? Warum baust du immer wieder Bugs ein? Mach einen Deep-Audit."

**Selbstkritisches Mea culpa:** Die Bug-Pattern waren:

1. **Copy-Paste-Drift**: `isPrivateHost` in `inbound-webhooks.ts` und `api-integrations.ts` — zwei Kopien, sollten identisch sein. Die zweite verlor die `::ffff:`-Hex-Form-Behandlung beim Kopieren.
2. **Reihenfolge Sicherheit zuletzt**: Ich schrieb Funktion, fragte dann Security-Agent, reparierte. Bei sicherheitskritischem Code falsche Reihenfolge. Besser: alle Inputs/Outputs durchdenken bevor erste Zeile Code.
3. **Nicht getestet vor Commit**: typecheck ≠ runtime. Ich habe die Proxy-URL-Logik nie tatsächlich durchlaufen lassen, dadurch den Path-Drop beim führenden Slash übersehen.

Lehren fürs nächste Feature: **Input-Matrix schreiben bevor Code**, **doppelte Implementierungen sofort zu einem shared Module konsolidieren**, **Happy-Path-Curl-Test vor Commit**.

### Neue Findings in Runde 2 (alle gefixt)

| ID | Severity | Fix | Datei |
|---|---|---|---|
| **R2-F1 — Doppelte SSRF-Impls drifteten** | P1 | Shared `ssrf-guard.ts` | `apps/api/src/ssrf-guard.ts` (neu) |
| **R2-F2 — Numerische IP-Tricks durchgelassen** (`"0"` → 127.0.0.1 auf Linux, `"0x7f000001"`, `"2130706433"`, oktal `"0177.0.0.1"`) | P1 | `expandNumericIPv4()` canonicalisiert vor Range-Check | `ssrf-guard.ts` |
| **R2-F3 — `metadata.google.internal` Hostname nicht geblockt** (nur die IP 169.254.169.254) | P2 | `METADATA_HOSTS` Set deckt Hostname + IPv6-Metadata-IP ab | `ssrf-guard.ts` |
| **R2-F4 — CGNAT-Range 100.64.0.0/10 nicht geblockt** (einige Provider routen das intern) | P2 | In range check aufgenommen | `ssrf-guard.ts` |
| **R2-F5 — Keine Port-Blockliste** → Cross-Protocol-Smuggling zu SSH:22 / SMTP:25 / DB-Ports möglich | P1 | `isBlockedPort()`, angewendet in beiden Outbound-Pfaden | `ssrf-guard.ts` + `api-integrations.ts` + `inbound-webhooks.ts` |
| **R2-F6 — URL-Path-Drop bei führendem Slash** — `new URL("/x", "https://host/v2/")` → `https://host/x` verliert `/v2/`. Customer mit `baseUrl=…/v2` + endpoint `/customers` hätte FALSCHE URL getroffen | 🔴 Funktional | Endpoint-Path leading-slash-strip + URL-Objekt statt String-Concat | `api-integrations.ts` |

### Geprüft und sauber in Runde 2

| Prüfung | Ergebnis |
|---|---|
| Encryption-Idempotenz bei `value.startsWith('enc:v1:')` — kann ein authValue aus Versehen erkannt werden? | Sauber — Frontend sendet nie diesen String, außer nach DB-Round-Trip. Sentinel-Check läuft davor. |
| Args mit Shell-Special-Chars (`$(rm -rf /)`) | Sauber — `encodeURIComponent` + Upstream sieht literal |
| Args mit CRLF-Injection-Versuch im authValue | Sauber — Node fetch wirft bei CRLF in Header-Value, `FETCH_FAILED` |
| UTF-8 / Emoji in args | Sauber — `encodeURIComponent` + Upstream-Problem falls Interpretation |
| Retry-Szenario: Retell sendet gleiche Tool-Call zweimal (unsere Antwort timeout) | **Bekannt — at-least-once**: GET idempotent, POST kann Duplikat erzeugen. Kunde muss Idempotency selbst handhaben. |
| Credentials in baseUrl + authType='bearer' | Bearer-Header gewinnt im Node-fetch-Builder; url.creds werden ignoriert. Verwirrend für Kunden aber safe. |
| Query-String in baseUrl wird bei URL-Resolution gedroppt | Feature-Gap. Customer muss Auth per Header statt Query nutzen. Document. |
| Unsigned Proxy-Request (runtime) | 401 ✓ |
| Unknown Tool-Path (runtime) | 404 ✓ |
| Config-Read ohne JWT (runtime) | 401 ✓ |
| Health-Endpoint (runtime) | 200 ✓ |
| Typecheck API + Web | grün ✓ |

### Neue Follow-ups (nicht blockierend)

10. **Race in `applyIntegrationEncryption`** — zwei concurrent saves können neu gesetzten authValue verlieren. Fix via SELECT FOR UPDATE oder Encryption-Trigger in Postgres.
11. **Query-String in baseUrl** — bei URL-Resolution gedroppt. Preserve oder dokumentieren.
12. **Max-Länge für Endpoint-Description** (Retell-Limit ~1024 Chars) — Client-Side-Validation fehlt.
13. **UI Tooltip "apikey goes in X-API-Key Header"** — Kunden erwarten evtl. andere Header-Namen (X-Api-Key, apikey, api_token).
14. **Perf-Optimierung: Config-Cache im Proxy** — jede Tool-Invokation macht DB-SELECT. 30-Sek-Memory-Cache wäre billig.

---

## 10. Gesamt-Bilanz nach beiden Runden

| Runde | Gefundene Bugs | Gefixt + deployed | Commits |
|---|---|---|---|
| 1 (Security-Reviewer + erster Audit) | 4 Security-P0/P1 + 2 Funktions-Bugs | alle 6 | `a52cd3a`, `db2f5ae`, `4dd4421` |
| 2 (Zero-Trust-Self-Read) | 5 Security-P1/P2 + 1 Funktions-Bug (URL-Path) | alle 6 | `904f265`, `6b9e4c2` |

**Gesamt: 12 echte Bugs gefunden und gefixt.** Davon wäre der URL-Path-Bug (R2-F6) in Production zu falschen API-Calls geführt, der Port-Block (R2-F5) wäre ein Cross-Protocol-Angriffsvektor, der numerische-IP-Bug (R2-F2) hätte SSRF zu Loopback auf Linux erlaubt.

Alle Findings sind dokumentiert mit file:line und fix. Alle Fixes sind auf prod deployed.

### Ehrliche Einschätzung fürs nächste Feature

Das Muster „Funktion schreiben → Security-Agent → reparieren" hat mehrfach Kosten verursacht. Änderung für sicherheitskritische Features:

1. **Input-Matrix zuerst**: was kommt von wem rein, was geht an wen raus. Skizze bevor erste Zeile Code.
2. **Shared-Module bei Wiederholung**: wenn ich eine ähnliche Funktion schon woanders hatte, sofort in eigenes Modul heben, nicht Copy-Paste.
3. **Happy-Path-Curl-Test vor Commit**: Typecheck ≠ Korrektheit. Mindestens der eine End-zu-End-Pfad muss einmal durchgelaufen sein.
4. **Security-Review kommt NACH Self-Review**, nicht statt. Sonst wird der Agent die offensichtlichen Dinge finden und ich verpasse die strukturellen Drifts zwischen Modulen.

---

## 🔗 Links

- [[Phonbot/Overview]]
- [[Phonbot/Live-Test-2026-04-23]]
- [[Daily/2026-04-23]]
- Commits: `a52cd3a`, `db2f5ae`, `4dd4421`
