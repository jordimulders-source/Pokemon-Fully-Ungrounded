# Overdracht: satelliet-lijn fase 2 (nieuwe sessie)
Start hier. Lees eerst `CLAUDE.md`, dan `docs/lessen/SPRITE_KERN.md`, `docs/lessen/GEMINI.md` en `satelliet_lijn/SPEC.md` (alle besluiten van Jordi letterlijk).

## Stand (23 nov)
- Lijn: Steel/Cosmic, pure machines met één oog, wit/paars à la Mewtwo, cyber. Fase 1 Spoetnik-bolletje **af** (`fase1/af/satelliet_fase1.png`, ±985 px, klein gekozen). Fase 2 = satelliet, fase 3 = ruimtestation (misschien). Jordi: fase 1 wordt onderdeel van fase 2 en 3, steeds kleiner deel van het geheel.
- Alleen designs (geen methode, lore, namen). Type per fase nog open.
- Fase 2 startprompt: `fase2/gemini/PROMPT_r1.md` (Jordi plakt in Gemini, nieuw gesprek, geen bijlage).

## Werkwijze die werkte bij fase 1
- Gemini-rondes: elke ronde een volledig nieuwe startprompt met alle feedback (r1–r7); Jordi kiest; model bevroren in `faseN/model/model_gekozen.png`.
- Model bewerken in het natieve raster (`fase1/model/natief.py` fit de pitch, `bewerk_r7.py` als voorbeeld); Gemini telt herhaalde onderdelen slecht (5 antennes): zelf tellen.
- **Formaat vóór ronde 1 met Jordi afspreken** (fase 1 moest na 3 rondes kleiner). Referentie: Beldum 672 → Metang 1578 → Metagross 1651, Magnemite 367 → Magneton 1474 px (`graphics/pokemon/<soort>/anim_front_gba.png`).
- Sprite: één maker-agent (kale reductie, niets hertekenen, reparaties per pixel), keurder, dan Dragonfly Cave-eindkeuring met omlijningsronde; pas daarna naar Jordi (64×64 + 8×).
- Jordi's eisen uit fase 1 die ook hier gelden: bol mooi rond, geen onnodige zwarte pixels, antennes/dunne delen nooit 1 px, oog zonder glans, consistent palet met fase 1 (`fase1/af/`).
