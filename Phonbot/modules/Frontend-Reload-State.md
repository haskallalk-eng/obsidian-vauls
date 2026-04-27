---
module: Frontend-Reload-State
scope: "AppGate, Dashboard navigation, URL persistence"
files:
  - apps/web/src/ui/App.tsx
  - apps/web/src/ui/LoginPage.tsx
commit: d7cbccc
tags: [frontend, routing, reload, auth-gate]
updated: 2026-04-23
---

# Frontend-Reload-State

## Ziel

Egal wo der User in der App ist, ein Browser-Reload soll wieder auf derselben Ansicht landen.

## Umsetzung

Dashboard-Seiten nutzen weiterhin URL-Hashes:

- `#agent`
- `#test`
- `#tickets`
- `#logs`
- `#billing`
- `#phone`
- `#calendar`
- `#insights`

Unauthenticated Gates nutzen Query-Parameter:

- `?page=login`
- `?page=register`
- `?page=contact`

`AppGate` liest `page` aus der URL und schreibt Navigationswechsel zurück in die URL. Browser Back/Forward synchronisiert den React-State per `popstate`.

## Wichtig

Vorher wurde `?page=...` beim ersten Rendern entfernt. Dadurch sprang ein Reload von Login/Register/Contact zurück auf Landing. Das wurde geändert: `page` bleibt absichtlich in der URL.

## Dateien

- `apps/web/src/ui/App.tsx`
  - `readGateFromUrl()`
  - `writeGateToUrl()`
  - `navigateGate()`
  - `popstate` Listener für Gate-Sync
- `apps/web/src/ui/LoginPage.tsx`
  - `onModeChange` Prop
  - Login/Register-Tab-Wechsel schreibt URL mit
  - `initialMode` wird bei URL/State-Änderung wieder synchronisiert

## Verifikation

- `pnpm.cmd --filter @vas/web typecheck` grün.
- Live deployt.
- Healthcheck grün.
