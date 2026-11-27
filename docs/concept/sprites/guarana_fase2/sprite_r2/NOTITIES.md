# Guaraná fase 2, ronde 2 (maker): benoemde reparaties van de coördinator op r1

Bestanden: `guarana2_r2.png` (hoofdversie) + `normal.pal`; variant `guarana2_r2_zwartrand.png` (oogrand rechts/onder zwart, precies zoals fase 1);
`vel.png` (r2 | r1 | model op 8×, trossen 12× naast het natieve model, 1× op 5 achtergronden + variant 1×), `vel_zwartrand.png` (zelfde vel met de variant);
`kaal.png` (kale reductie r2). Bouwen vanuit `guarana_fase2/`: `python3 sprite_r2/kaal.py && python3 sprite_r2/bouw.py && ZWARTRAND=1 python3 sprite_r2/bouw.py && python3 sprite_r2/controle.py && python3 sprite_r2/vel.py sprite_r2/guarana2_r2.png sprite_r2/vel.png sprite_r2/guarana2_r2_zwartrand.png`.
Natief model, oogplekken en silhouet zijn ongewijzigd t.o.v. r1 (`../sprite_r1/natief_model.png`).

## Reparaties
1. **Ooglijn zoals fase 1:** geen lijn meer links/boven het oog: het oogwit grenst direct aan de vrucht (was die pixel geen vruchtrood, dan midden-rood 4).
   Alleen rechts/onder een lijnpixel. In de hoofdversie is dat lijnrood (2) binnen de tros (punt 3: binnenin geen zwart) en zwart alleen op de buitenrand
   aan de schaduwkant. In fase 1 is die pixel zwart: dat is de variant `_zwartrand`. Ook de lidrand van de half dichte ogen is in de hoofdversie lijnrood.
2. **Vruchten:**
   - Vruchttinten gemeten: k-means-mediaan van het vruchtvlees (vlakpixels, zonder lijnen) in het natieve model: 178,54,47 | 223,86,59 | 236,113,79 | 249,144,112.
     De drie fase 1-tinten liggen daar dichtbij (176,56,48 / 224,80,56 / 240,136,104). **Erbij: index 12 oranjerood 236,112,80** (modeltint die ontbrak).
   - Per spritepixel de modeltint met de meeste dekking (geen gemiddelde kleur meer); hooglicht al bij ≥ 25 % (glans, fase 1 r3).
   - In de tros wint vruchtvlees al bij ≥ 30 % dekking, ook als er een modellijn door de pixel loopt. De scheiding tussen vruchten komt uit de vrucht-id's
     (37 vruchten = samenhangende stukken vruchtvlees in het natieve model): 1 px lijnrood op de pixel met de meeste modellijn (64 px).
     Dubbele binnenlijnen (vrucht|2|2|vrucht) → één lijn (6 px).
3. **Zwart:** alleen buitenlijn aan de schaduwkant + pupillen. Zwart totaal 356 → 263 px; zwart binnenin: 0 (gemeten).
   L1/R4: geen zwarte pixels meer aan de lichtkant van de buitenrand (0, gemeten).
4. **Liaan:**
   - Groen per natieve pixel ingedeeld bij de 4 modeltinten (55,87,45 | 76,115,67 | 105,148,89 | 123,167,101); per spritepixel de meeste dekking.
     **Erbij: index 13 middengroen 104,146,86.**
   - Tintvlakjes < 3 px (4-buren) → de meest voorkomende vultint eromheen (zelfde kleurgroep), 3 rondes; hooglicht rood mag klein blijven (glans).
     Het zijn 263 px, in rood en groen samen; ik heb ze niet per groep geteld.
5. M5 weggelaten (akkoord). Half dichte ogen en de overlap L4/L5: zoals in r1.

## Metingen (`controle.py`)
- 62×51, onderkant y51. **12 kleuren incl. transparant** (fase 1-palet + 12 oranjerood + 13 middengroen; index 9 en 11 ongebruikt, 14–15 vrij).
- Lichte tint op de buitenrand: 0. Zwart aan de lichtkant: 0. Alpha-diff t.o.v. kaal: 15 (de dichte gaatjes uit r1).
- Losse zwarte pixels: 5, allemaal pupillen van 1 px (M2, M3, L3, L1, R4). Ze zijn los doordat de rand nu lijnrood is.
- Anders dan r1: 391 px. Anders dan de kale reductie: tros L 143 (ogen 52), M 157 (50), R 174 (81), rest 302.

## Wat ik niet (helemaal) kon oplossen
- **Losse vruchten zijn maar deels leesbaar.** Het model zelf is op 64 px in de trossen al donker: veel lijnen op vruchten van ±7 px (zie `model_64`, middelste paneel).
  Vruchten zonder oog (onderkant van elke tros) hebben nu een eigen rode vorm met hooglicht. Vruchten mét oog zijn vooral oog.
- De ogen zonder donkere rand links/boven lezen in de hoofdversie wat zachter (wit vlak op rood); in de variant met zwarte rand zijn ze scherper maar donkerder.
- Oranjerood (12) wint maar op 9 px de meerderheid. Het model is oranjer door menging binnen de pixels; per pixel wint meestal midden-rood.
- Stam: minder vlekkerig, maar de twist leest nog niet als duidelijke strengen. De strengen in het model zijn ±1 spritepixel breed, met zwarte lijnen ertussen.

## Vragen
- Oogrand rechts/onder: lijnrood (hoofdversie, volgt "binnenin geen zwart") of zwart (variant, precies fase 1)?
