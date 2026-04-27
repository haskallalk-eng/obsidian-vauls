---
tags:
  - idea
  - phonbot
  - voice
status: thinking
created: 2026-04-18
---

# Idee: Chipy Voice-Varianten

> [!question] Frage
> Lohnt es sich verschiedene Charakter-Voices für unterschiedliche Branchen anzubieten?

## Kontext

Aktuell: **eine** Default-Voice (`chipy`, Cartesia).

Pro verschiedener Voices:
- Arzt-Praxis will eher beruhigend + professionell
- Handwerker will casual + direkt
- Premium Service will Luxus/deep Voice
- B2B will seriös

Contra:
- Mehr Voices = mehr Maintenance + Training
- Cartesia-Voices kosten pro Clone
- Verwirrt evtl. das Branding (Chipy = DER Phonbot-Character)

## Optionen

1. **Nur Chipy** — Maskottchen, nie ändern. Fokus auf Wiedererkennbarkeit.
2. **3 Preset-Voices** — Chipy (standard), "Dr. Chipy" (seriös), "Kumpel-Chipy" (casual)
3. **Voice Cloning als Premium-Feature** — Agency-Plan only, Kunde bringt eigene Stimme

## Nächste Schritte

- [ ] User-Research: 3-5 bestehende Kunden fragen ob sie andere Voice wollen würden
- [ ] ElevenLabs + Cartesia Pricing für multi-voice checken
- [ ] Entscheidung in [[Phonbot/Decisions]] dokumentieren

## Related

- [[Phonbot/Overview]]
- [[Phonbot/modules/Backend-Voice-Telephony]] — Voice-Catalog + Retell-Integration (wo das landet)
- [[Daily/2026-04-18]] — Idee entstanden
