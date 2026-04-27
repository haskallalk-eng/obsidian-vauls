---
module: Backend-Outbound-Demo-Only
scope: "Outbound product decision and live config"
related:
  - Backend-Outbound
tags: [backend, outbound, demo, caddy, product-decision]
updated: 2026-04-23
---

# Backend-Outbound-Demo-Only

## Produktentscheidung

Outbound soll vorerst nur als Demo-/Landingpage-Rückruf existieren. Kunden sollen keinen eigenen Outbound-Agent im Dashboard bauen oder starten können.

## Aktueller Soll-Zustand

- Demo-/Website-Callback bleibt aktiv.
- Customer-Outbound im Dashboard bleibt deaktiviert.
- `CUSTOMER_OUTBOUND_ENABLED=false` live.
- Die Outbound-Dashboard-Seite ist nicht als Kundenfeature sichtbar.

## Was in der Session passiert ist

Kurzzeitig wurde Customer-Outbound zu breit aktiviert und als Dashboard-Seite sichtbar gemacht. Nach Klärung wurde das zurückgedreht bzw. durch spätere Commits wieder entfernt.

Wichtig: Der Outbound-Agent wurde nicht neu gebaut. Es ging um bestehende Demo-/Outbound-Flows und Live-Konfiguration.

## Live-Konfig

- `WEBHOOK_BASE_URL=https://phonbot.de`
- `CUSTOMER_OUTBOUND_ENABLED=false`

`WEBHOOK_BASE_URL` muss auf `phonbot.de` zeigen, nicht auf alte ngrok-URLs, damit Webhooks/TwiML öffentlich erreichbar sind.

## Verwandte Datei/Notiz

- [[Backend-Outbound]]
- `apps/api/src/outbound-agent.ts`
- `apps/api/src/demo.ts`
- `Caddyfile`
