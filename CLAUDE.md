# CLAUDE.md — Mindrails Obsidian Vault

Diese Datei gilt für jede Claude-Session, die im Vault `C:\Users\pc105\Obsidian` arbeitet. Sie beschreibt Vault-Konventionen, NICHT Produkt-Inhalte (die stehen in den jeweiligen Overview-Notes).

## Vault-Topologie

```
Obsidian/
├── README.md                    # Vault-Onboarding (Einstieg für Menschen)
├── Projects Landscape.canvas    # Visual Hub (Whiteboard)
├── Mindrails/
│   ├── Overview.md              # 🏛 SSoT-Hub: einzige zulässige Cross-Tree-Verbindung
│   └── Claude-Skills-und-MCPs.md
├── Phonbot/                     # Produkt-Tree (isoliert)
├── Socibot/                     # Produkt-Tree (isoliert)
├── Kanzleibot/                  # Produkt-Tree (isoliert)
├── Daily/                       # Sessionlog (alle Daten zentral, nie in Produkt-Trees)
├── Inbox/                       # Capture-Stelle für Ungeclustertes
├── Clients/                     # 1 Note pro Klient (+ _Template.md)
└── Ideas/                       # Ideation, projekt-übergreifend
```

## Kernregeln (NICHT brechen)

### 1. Tree-Isolation
**Produkt-Trees dürfen NICHT direkt aufeinander linken.** Einzige zulässige externe Verlinkung aus einem Produkt-Tree heraus: `[[Mindrails/Overview]]`.

- ❌ `[[Phonbot/Overview]]` aus `Socibot/...` → Verstoß
- ✅ `[[Mindrails/Overview]]` aus jedem Produkt → erlaubt
- ✅ `[[Phonbot/Overview]]`, `[[Socibot/...]]` aus `Daily/`, `Mindrails/`, `README.md`, `Projects Landscape.canvas` → erlaubt

### 2. Daily-Notes nur im Vault-Root
**Alle Sessionlogs gehören in `/Daily/`.** Niemals `Phonbot/Daily/`, `Socibot/Daily/` o.ä. anlegen.

- Format: `YYYY-MM-DD.md` (ISO-Datum, keine Lokalformate)
- Spezialform: `YYYY-MM-DD-<topic>.md` (z.B. `2026-04-23-Codex-Session.md`) — auch ins Root-Daily/.

### 3. Hub-Pflicht im Frontmatter
Jede Produkt-Overview-Note (`Phonbot/Overview.md`, `Socibot/Overview.md`, `Kanzleibot/Overview.md`) MUSS:

```yaml
---
tags: [project, <productname>, mindrails]
status: active
parent: "[[Mindrails/Overview|Mindrails]]"
created: YYYY-MM-DD
---
```

### 4. Inhalt nicht ändern bei Vault-Wartung
Bei reinen Struktur-/Naming-Refactorings (Move, Rename, Frontmatter-Add): Inhalt der Notes UNANGETASTET lassen. Sachlichkeit beibehalten oder verbessern, nie verwässern.

## Sessionlog-Pattern (jede Arbeits-Session)

Eine Session hinterlässt **immer zwei Spuren**:

1. **Daily-Note** `Daily/YYYY-MM-DD.md` — chronologisch, mit Wikilinks zu betroffenen Produkt-Notes.
2. **Produkt-Narrative** in `<Produkt>/ZuTun.md` (oder vergleichbar) — projektbezogen, mit Backlink zur Daily-Note.

Beide verlinken sich gegenseitig (`[[Daily/2026-04-28]]` ↔ `[[Phonbot/ZuTun]]`).

Nie auslassen mit "war nur Kleinkram" — auch 5-Minuten-Sessions werden dokumentiert.

## Naming-Konventionen

| Bereich | Konvention | Beispiel |
|---|---|---|
| Daily | `YYYY-MM-DD.md` oder `YYYY-MM-DD-<topic>.md` | `2026-04-28.md` |
| Phonbot Module | `<Layer>-<Topic>.md` (kein Nummer-Prefix) | `Backend-Database.md` |
| Socibot Module | `<NN>-<Topic>.md` (Nummer-Prefix 00–20) | `04-Video-Engine.md` |
| Audits | `Audit-YYYY-MM-DD-<scope>.md` im Produkt-Root | `Audit-2026-04-18-Deep.md` |
| Templates | `_Template.md` (Underscore-Prefix) | `Clients/_Template.md` |
| Frontmatter-Tags | lowercase, keine Spaces | `tags: [project, phonbot]` |

## Hub-Note-Pflichten

`Mindrails/Overview.md` ist Single-Source-of-Truth für die Produkt-Landschaft:
- Verlinkt zu allen aktiven Produkten (`[[Phonbot/Overview]]`, `[[Socibot/Overview]]`, `[[Kanzleibot/Overview]]`)
- Enthält Compliance-Regeln, Kontakt, Vault-Meta
- Wird aktualisiert wenn neue Produkte hinzukommen oder bestehende ihren Status ändern

`Mindrails/Claude-Skills-und-MCPs.md` ist Reference-Note für Skills/MCPs — wird gepflegt wenn neue Skills auftauchen (siehe Hinweis am Ende dieser Note).

## Capture & Cleanup

- **Inbox/**: Neue Idee/Notiz die noch keinen Tree hat → `Inbox/<topic>.md`. Spätestens nach 1 Woche entweder in Tree verschieben oder löschen.
- **Ideas/**: Längerlebige projekt-übergreifende Ideen.
- **Clients/**: Pro Klient `Clients/<CompanyName>.md` (Template `_Template.md` als Vorlage).

## Was Claude bei Vault-Arbeit beachten muss

1. **Vor jedem Move/Rename**: Wikilinks per Grep auf Treffer prüfen (`Grep` mit Pfad-Pattern, multiline=false reicht für `[[link]]`-Form).
2. **Bare-Name-Wikilinks** (`[[Frontend-Reload-State]]` ohne Pfad-Prefix) resolven via Obsidian's globalen Filename-Index → bleiben nach Move funktional, solange Filename eindeutig.
3. **Pfad-Wikilinks** (`[[Phonbot/modules/Frontend-Reload-State]]`) müssen nach Move in JEDER referenzierenden Note manuell aktualisiert werden.
4. **Frontmatter-Konsistenz**: Beim Anlegen neuer Produkt-Notes immer Hub-Pflicht-Frontmatter (siehe Regel 3).
5. **Git-Backup**: Vault ist git-tracked. Bei Unsicherheit: kleine atomare Commits, leichter rückrollbar.

## Aktive Produkte (Snapshot, kann veralten — siehe Mindrails/Overview.md für SSoT)

| Produkt | Code-Pfad | Status |
|---|---|---|
| Phonbot | `~/.openclaw/workspace/voice-agent-saas` | active, deployed (phonbot.de) |
| Socibot | `Desktop/Social media Bot` | active, Test-Run pending |
| Kanzleibot | `~/.openclaw/workspace/kanzleibot` | active, im Aufbau |

---

**Pflege-Hinweis:** Wenn neue strukturelle Vault-Konventionen entstehen (neuer Tree, geänderte Daily-Pattern, neue Frontmatter-Pflicht), diese Note updaten. Inhaltliche Produkt-Details gehören NICHT hierher — die stehen in den Produkt-Overview-Notes.
