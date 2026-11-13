# Sneeuwbolslak (fase 1, Ice) – SPEC

Lijn: slak met sneeuwbol als huisje → spiraal met ijskorst → langwerpige komeet (vorm Interloper), Ice → Ice → Ice/Cosmic. Citaten en voorstellen: `docs/concept/IDEEEN.md` (Sneeuwbol-Pokémon). Prompts en Gemini-rondes: `gemini/PROMPT.md`.

## Jordi (letterlijk)
- "de sneeuwglobe moet wel een soort hybride zijn, kan niet alleen een bol zijn."
- "zorg er wel voor dat het in een sprite uit te beelden blijft."
- Prompt-keuzes: "1c en 2a" (minuscuul huisje in de bol, lijf lichtblauw-wit); "voetstuk mag blijven"; "meer sneeuwvlokken".
- Op r3: "eerst kwam 1, die vond ik wat overdreevn, is door de vlokvorm beter. vertaalt dat naar een sprite denk je? Anders kan je zelf een hybride vorm maken"
- Op de hybride: "de vlokken zijn prima, bol ietsje blauwer misschien zodat het verschilt van het lichaam? Maar miscshien kan je alvast beginnen met de sprite bouwen end an hebben we beter beeld bij hoe het vertaalt. Houd de poedelmot methode aan, niet opnieuw dingen gaan tekenen, buiten wat we afgesproken hebben"

## Model
- `gemini/r3b_gemini.png` (pitch 10,24 → natief, past in 64×64) + plusvlokken (`sprite/hybride_v1.png`).
- Afgesproken wijzigingen: vlokken als plusjes/pixels (goedgekeurd), bol ietsje blauwer. Verder niets hertekenen.

## Sprite
- `sprite/onderlaag.py`: natief raster, achtergrond weg, kwantisering naar 13 kleuren + transparant (seeds per kleurgroep), 4 anti-aliasrestjes naar de lijntint.
- `sprite/bolblauw.py`: binnenkleur van de bol eigen paletkleur, A (206,225,240) / B (194,216,238). Vel: `sprite/r1_vel.png`.
- Open: maat (slak 63×51, vult het vak; fase 1 is normaal kleiner).
- Jordi: "b en hij moet uiteraard kleiner, maar dat is niet moeilijk toch?" → bol B gekozen. Maattest (`sprite/maattest.py`, vel `sprite/maattest_vel.png`): 40, 46 en 52 px breed; silhouet blijft, ogen/huisje/omlijning moeten daarna met de hand (maker).
- Jordi: "46 prima". Startbestand maker: `sprite/start46.png` (verkleind uit r1_B, nog niet opgeschoond). Geen nieuw Gemini-model: model alleen tot de richting staat (SPRITE_KERN).
- r4 (`gemini/r4_gemini.png`, Jordi: "is dit kleiner?"): nee, zelfde pixelmaat (10,24) en exact dezelfde omvang als r3b (195–839 × 246–767); niet gebruikt.
