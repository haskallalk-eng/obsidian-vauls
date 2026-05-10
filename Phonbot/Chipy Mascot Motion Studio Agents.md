# Chipy Mascot Motion Studio Agents

Status: 2026-05-10. Wiederverwendbare Agenten-Struktur fuer Chipy-Clips, 3D-Heroes und Mascot-Animationen.

## Team-Setup

| Agent | Aufgabe | Muss verhindern |
|---|---|---|
| Design Director | Mascot-Silhouette, Material, Orange/Cyan-Licht, Logo-Frisur | Hamster/Roboter/Alien/Generic-SaaS |
| Motion Director | Timing, Drehung, Reveal-Reihenfolge, Kamera, Ease | Bounce, hektische Partikel, billige Sticker-Motion |
| Technical Renderer | Rendering-Ansatz, Performance, Preview/Final-Profil | Full-HD-Blur/I-O-Lock, schwere Dependencies ohne Nutzen |
| Brand Critic | Finaler Phonbot-Fit, Lesbarkeit, Props, USP | Props unklar, Logo-Haar falsch, Purple Drift |

## Verbindungslogik

1. Design Director definiert die unverhandelbare Figur.
2. Motion Director legt die 6-8s Dramaturgie fest.
3. Technical Renderer entscheidet Preview-vs-Final und macht Performance-Grenzen klar.
4. Brand Critic prueft Standbild und Clip gegen Phonbot-DNA.
5. Codex setzt erst danach um und iteriert mit Standbildern.

## Aktuelle Clip-Dramaturgie

- `0.0-0.6s`: dunkle Buehne, Kristall allein, schwache Bodenreflexion.
- `0.6-2.4s`: kontrollierte Kristall-Drehung, dann frontaler Lock.
- `2.4-3.4s`: Kalender und Telefon kommen raeumlich dazu.
- `3.4-4.4s`: Props docken visuell an, Augen gehen freundlich an.
- `4.4-5.4s`: Phonbot-Flammenlogo entsteht als leuchtende Glas-Frisur.
- `5.4-7.0s`: Hero-Pose mit ruhigem Shimmer.

## Preview-Ausgabe

- Script: `scripts/render_chipy_crystal_reveal_preview.py`
- Output: `assets/video/chipy-crystal-reveal-preview-v2.mp4`
- Format: 1280x720, 24 FPS, 7 Sekunden.

## Finale Checkliste

- Kristall ist vor den Props allein erkennbar.
- Drehung wirkt wie Premium-Reveal, nicht wie Spielzeug.
- Telefon und Kalender sind sofort als Calls + Terminlogik lesbar.
- Gesicht ist dunkel genug, Augen sind freundlich sichtbar.
- Logo-Frisur kommt als letzter Identitaetsmoment.
- Orange links, Cyan rechts, kein Purple Drift.
- Standbild funktioniert als Brand-Asset.
