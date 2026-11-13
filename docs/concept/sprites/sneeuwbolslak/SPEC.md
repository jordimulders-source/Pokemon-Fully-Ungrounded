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
- r5 (`gemini/r5_gemini.png`): wél kleiner, natief 42×35 (`sprite/r5_natief64.png`, vergelijking `sprite/r5_vs_46.png`). Ogen en omlijning schoner; vlokken bijna weg, huisje een vlek, kop/lijf iets anders dan r3b.
- Maker (46 px): `sprite/maker/r2.png` + `vel_r2.png`; silhouet = start46 (diff 0), palet r1_B, ogen 6×6 met L-pupil, huisje 10×8, 4 plusvlokken + losse pixels. Zwakke punten maker: geen rij oogwit onder het ooglid; huisje vereenvoudigd.
- Jordi op r2: "op de ogen na ben ik tevreden, die zijn een beetje te groot deel van de oogballen nu lijkt" → `sprite/ogen_pupil.py`: r3_A (pupil 2 px, diff 2), r3_B (pupil 1 px, diff 4); vel `sprite/maker/vel_r3.png`.
- Jordi op de pupilvarianten: "nee een ander type oog, dit is alle 3 niet mooi" → maker maakt probeersels met ogen pixel voor pixel uit echte sprites (lotad, wurmple, slugma/magcargo, surskit, shellos/gastrodon, sliggoo/goomy).
- Jordi: "surskit is de enige die redelijk past, dus ga maar voor die en stuur hem naar de eindkeuring" → `sprite/r4_surskit.png`.
- Eindkeuring (verse keurder, `sprite/keuring/keurvel_r4.png`): PASS met 2 MOET-pixels, door Claude toegepast: (41,45) 14→4, (52,32) 3→4. MAG (43–44,24 selout in zwarte rand) blijft uit trouw aan het model. Ter info: witte binnenlijn tussen voetje en lijf (18,47–49) komt uit het model. **Af: `af/sneeuwbolslak.png` + `af/sneeuwbolslak_8x.png`.**
- Na "af" (13 nov), Jordi: "wacht, de bovenkant van de bol is niet rond genoeg zie ik nu," · "sowieso zijn de lijnen te strak en te zwart, ik was te vroeg" · "komt niet overeen met andere gen 3 sprites" · "fix dat nog". Rondere bovenrand: `sprite/rond/rond_A.png` (cirkelfit, 27 px, alleen rijen 23–31); lijnen: verse maker in `sprite/lijn/`.
