---
module: Backend-Auth-Refresh-Cookies
scope: "Login persistence after browser refresh"
files:
  - apps/api/src/auth.ts
  - apps/web/src/lib/auth.tsx
  - Caddyfile (server-local legacy route)
commits:
  - 64ba0f5
  - 1524f44
tags: [backend, auth, cookies, caddy, refresh]
updated: 2026-04-23
---

# Backend-Auth-Refresh-Cookies

## Problem

Nach Browser-Refresh flog der User aus dem Login.

Ursache: Der Refresh-Cookie wurde mit `Path=/auth` gesetzt. Die Browser-URL für API-Requests ist aber `/api/auth/refresh`, weil Caddy `/api` erst serverseitig strippt. Cookie-Path-Matching passiert im Browser vor dem Proxy. Deshalb wurde der Cookie bei `/api/auth/refresh` nicht mitgeschickt.

## Fix

Backend:

- Refresh-Cookie-Pfad auf `/api/auth` geändert.
- Alte Cookies mit `Path=/auth` werden beim Clear zusätzlich entfernt.
- Helper `clearRefreshCookie(reply)` räumt beide Pfade auf.

Frontend:

- Auth-Bootstrap versucht zuerst `/api/auth/refresh`.
- Falls das fehlschlägt, versucht er einmal Legacy `/auth/refresh`.
- Damit können alte Browser-Sessions mit altem Cookie-Pfad noch migriert werden.

Caddy live:

- Legacy Route `/auth` und `/auth/*` wird zur API geroutet.
- Test ergab nach Fix: `POST https://phonbot.de/auth/refresh` gibt API-Response `401 {"error":"No refresh token"}` statt nginx/SPA. Das bestätigt korrektes Routing.

## Dateien

- `apps/api/src/auth.ts`
  - `REFRESH_COOKIE_PATH = '/api/auth'`
  - `LEGACY_REFRESH_COOKIE_PATH = '/auth'`
  - `clearRefreshCookie()`
- `apps/web/src/lib/auth.tsx`
  - `fetchJson(url, init)`
  - `tryRefresh()` mit Fallback `['/api/auth/refresh', '/auth/refresh']`

## Verifikation

- `pnpm.cmd --filter @vas/api typecheck` grün.
- `pnpm.cmd --filter @vas/web typecheck` grün.
- Live deployt.
- Healthcheck grün.

## Manuell noch testen

Mit echtem User:

1. Einloggen.
2. Auf beliebige Dashboard-Seite gehen, z.B. `#calendar`.
3. Browser refreshen.
4. Erwartung: User bleibt eingeloggt und landet wieder auf derselben Ansicht.
