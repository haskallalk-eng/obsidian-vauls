---
tags: [meta]
created: 2026-04-18
---

# Dein Obsidian Vault

Willkommen in deinem persönlichen Zweithirn.

## Struktur

- **[[Mindrails/Overview|Mindrails]]** — Dachfirma, verbindet alle Produkte (einzige Klammer)
- **[[Inbox]]** — Schnelle Einfälle, noch unsortiert. Wöchentlich durchgehen.
- **[[Phonbot]]** — Voice Agent SaaS (eigener isolierter Tree)
- **[[Socibot]]** — Social Media Bot (eigener isolierter Tree)
- **[[Kanzleibot]]** — Rechtsanwalts-SaaS (eigener isolierter Tree)
- **[[Daily]]** — Daily Notes (optional, `YYYY-MM-DD.md`)
- **[[Clients]]** — Kundeninfos (je Client ein File)
- **[[Ideas]]** — Halbgare Ideen, Produktvisionen

> [!note] Vault-Regel
> Produkte sind im Vault **getrennte Trees** ohne direkte Wikilinks zueinander. Die einzige Verbindung ist [[Mindrails/Overview|Mindrails]] als Hub. Code-Bug-Tasks gehören ins jeweilige GitHub-Repo, nicht in den Vault.

## Einstiegspunkte

- 🏢 [[Mindrails/Overview|Mindrails]] — Produkte-Hub
- 🧭 [[Phonbot/Phonbot-Gesamtsystem|Phonbot Gesamtsystem]] — Code-basierte Single-Source-of-Truth (12 Module, 97 Endpoints)
- 📅 [[Daily/2026-04-21]] — letzte Session

## Wie du's nutzt

1. **Obsidian runterladen**: https://obsidian.md (kostenlos, 60 Sek)
2. Beim Start → *Open folder as vault* → `C:\Users\pc105\Obsidian` wählen
3. Fertig. Du siehst alle Files + Graph View

## Wie Claude damit arbeitet

Claude hat die **obsidian-markdown**, **obsidian-bases**, **obsidian-cli**, **json-canvas** Skills drauf. Er kann:

- Neue Notizen anlegen mit korrekten Wikilinks `[[Notiz]]`
- Bases bauen (Datenbank-Views deiner Notizen)
- Canvases (Whiteboard-Modus) generieren
- Deinen Vault durchsuchen + organisieren

Beispiel-Prompts:
- "Speichere das als Notiz in Phonbot"
- "Fass alle Notizen zu Phonbot zusammen"
- "Bau mir einen Canvas mit meinem Socibot-Plan"
- "Mach ne Daily Note für heute"

## Wichtig

- **Nichts committen** — das ist dein privater Vault, gehört nicht in Git
- **Backup**: Dropbox/iCloud Sync auf den Ordner, fertig
- Claude liest/schreibt Files direkt — du musst Obsidian nicht offen haben
