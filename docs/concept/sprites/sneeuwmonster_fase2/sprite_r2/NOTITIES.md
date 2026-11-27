# Sneeuwmonster fase 2 – sprite ronde 2 (maker)

`sneeuwmonster2_r2.png` = ronde 1 + twee technische reparaties (14 px t.o.v. r1; `bouw.py`, `vel.png` = r2 | r1 | model).
Werkwijze, palet en alle beschermde zones (ogen, mond, baardfranje, stenen): zie `../sprite_r1/NOTITIES.md` (ongewijzigd).

## Wijzigingen t.o.v. r1
1. **Selout volgt de randnormaal** (12 px): lichtkant = de lege 8-buren wijzen naar linksboven (nx+ny<0); linksonder en rechts = zwart. In r1 stonden op de linkerrand van kop en arm losse zwarte pixels tussen de gekleurde selout (zwart/blauw om en om op één rand, SPRITE_KERN): (19,17), (17,23), (17,26), (8,38), (9,43), (15,47), (16,50), (16,54) en de bovenrand van de emmer (33,3), (39,4), (42,5), (44,6), (46,7) zijn nu één doorlopende lijn per kant.
2. **Bultpixel bovenop de emmer weg**: (35,3) had in het model 54 % achtergrond (grensgeval) en stond los van de rand; nu loopt de bovenrand glad x30–33 → rij 4. Silhouet verder = kale reductie.

## Afwijkingen van de kale reductie (302 px, `zones.py`)
emmer 55 · ogen 20 · mond 8 · baardfranje 62 · stenen 35 · omlijning/vacht 122 (buitenlijn + ontkorrelen) — per zone uitgelegd in r1.

## Gemeten en bewust zo gelaten
- **Rechterhelft emmer donker**: gemeten per spritepixel (meerderheid van de drie houttonen): x39–47, rij 9–17 is in het model 90–100 % donker hout + zwarte duiglijnen. Duigen tekenen zou hertekenen zijn; ze lezen in het model alleen als zwart-op-donker.
- **Hand rechts en armlijn links**: lijnprofiel van het model (aandeel lijnpixels per spritepixel) naast de sprite gelegd: de handlijn (x38–41 rij 34–46, rij 47 x41–50) en de armstrengen links (x9–16 rij 37–51) staan op de modelplekken.

## Maat en controle
bbox x8–55, y3–58 (48×56), 1780 px; 16 kleuren incl. transparant; geen lichte kleur op de buitenrand; losse zwarte pixels alleen (34,25) (zwart mondeindje uit het model) en (23,40) (rand onderste steen).

## Zelf nog zwak
- Stenen: binnen 5×5 px blijft de zigzagscheur van het model een paar oranje/gele pixels rechts-midden; leest als gloeiende steen, niet als scheurnetwerk.
- Linkerarm: strengen in tint 2/3/5 vrij druk (wel modelplekken; niet gladgestreken, zie de regel "rustiger = pixelblur").
- Ogen 4×5 en 5×5: rond met afgesneden hoeken; op 8× is het linkeroog een beetje een plusje.
