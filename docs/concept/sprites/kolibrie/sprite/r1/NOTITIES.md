# Soulibri frame 1 + 2, ronde 1 (maker, 19 nov)

Opdracht: `../OPDRACHT.md`. Model overgenomen, niet hertekend: natief raster → spritepixels → technisch opschonen (scripts), per-pixel reparaties in `fix_f1.json` / `fix_f2.json` (met reden, assert op de oude index).

## Bestanden
- `frame1.png`, `frame2.png` (64×64, P, index 0 transparant), `anim_front.png` (64×128), `normal.pal` (JASC), `anim.gif`, `vel.png`.
- `onderlaag_f1.png`, `onderlaag_f2.png` = kale reductie (natief raster → dichtstbijzijnde paletkleur, zwarte modellijn lum<23 blijft index 1).
- `natief_f1.png` (65×63) en `natief_f2.png` (99×99) = teruggehaald Gemini-raster.
- Scripts: `pitch.py` (pitch/fase), `natief.py` (celmidden-mediaan), `bron.py` (onderlaag + modeltoon per frame), `schrap.py` (frame 2-verkleining), `schoon.py` (opschoonregels), `bouw_f1.py`/`bouw_f2.py`, `check.py` (Gen 3-controle), `lever.py` (anim_front, pal, gif, vel), `crop.py`/`kijk.py`/`toon.py` (kijkhulpen). Volgorde: `python3 bron.py && python3 bouw_f1.py && python3 bouw_f2.py && python3 lever.py`.

## Raster
- Frame 1 (`referenties/gemini_gekozen_r4.png`): pitch 15,51 × 15,51, fase x 14,5 / y 14,0 (randsterkte-pieken). Figuur 62×53 natief = 62×53 sprite (1-op-1), geplaatst op (1,6). Rond kop/snavel tekende Gemini halve cellen (7,75 px); de celmidden-mediaan pakt per 15,5-cel één waarde, het oog (glans + 2 teal) kwam er ongeschonden uit.
- Frame 2 (`gemini/r3_frame2_kandidaat.png`): de geschatte 13,2×12 bleek niet te kloppen. Gemeten pieken liggen om de 10/10/10/11 px = **10,24 px vierkant** (1024/100), fase 5,25/5,5. Figuur 75×54 natief (na weghalen van Gemini's grijze anti-aliasrand).

## Schaalbesluit frame 2: ×0,76
Gemeten op de natieve rasters (frame 1 = spritepixels):
| onderdeel | frame 1 | frame 2 natief | verhouding |
|---|---|---|---|
| kophoogte | 13 | 17 | 0,76 |
| kopbreedte | 13 | 16 | 0,81 |
| nabije vleugel (aanzet→punt) | 23 | 29 | 0,79 |
| verre vleugel | 19 | 26 | 0,73 |
| oppervlak vleugels (√) | 395 px | 663 px | 0,77 |
| oppervlak lijf+donker (√) | 702 | 1321 | 0,73 |
| oppervlak hele figuur (√) | 1097 | 1984 | 0,74 |
Snavel (0,62) is bewust niet meegeteld: in frame 2 is hij langer getekend (en Jordi wilde een langere snavel). Mediaan ≈ 0,76 → frame 2 = 57×41 px; past binnen 64×64. Verkleinen door **hele natieve rijen/kolommen te schrappen** (Gengas-methode, `schrap.py`: steeds de rij/kolom die het minst van haar buur verschilt, straf voor clusters; geschrapt x 18 kolommen, y 13 rijen, lijst wordt door `bron.py` geprint). Elke spritepixel is zo een echte modelpixel; oppervlakgemiddelde gaf pap (oog weg, lijnen gebroken). Plaatsing (1,7): kop horizontaal gelijk aan frame 1, lijfzwaartepunt verticaal gelijk (35,0 vs 34,7); de kop zakt 8 px en het lijf schuift 3–4 px naar rechts = de bedoelde duik/krul, geen sprong.

## Palet (gedeeld, 15 kleuren + transparant)
Palet van `af/kolibrie.png`, met één wijziging: index 15 (96,80,140; viel samen met index 11) → **donker blauwgroen (34,86,104)**, de schaduwkant van de schouderglans die in beide modellen staat. Tealgroep is nu 3 tinten (72/123/181 helderheid). Beide frames gebruiken alle 15.

## Afwijkingen van de kale reductie (px)
| zone | frame 1 | frame 2 | wat |
|---|---|---|---|
| kop + oog + snavel | 3 | 10 | f1: 1 lichte randpixel → selout, 2× tint 6→5; f2: oog = hetzelfde 3-px-oog als frame 1 (glans, iris, licht blauwgroen) op de modelplek, 4 lijnpixels onderkant, tint 6→5 |
| kuif | 3 | 7 | f1: witte linkerveer op de buitenrand → lavendel; f2: steel middelste veer donker, tip lavendel, 2 stelen schaduwtint (model hier zelf rommelig) |
| vleugels | 164 | 203 | alleen kleur: modeltoon per pixel naar 3 tinten (nabij c/d/e, ver 4/c/d; drempels 150/168/212 en 150/170), randen → vleugelrand c (Venomoth), losse vlakjes weg. Vorm 0 px gewijzigd |
| lijf + schouder | 12 | 46 | losse vlakjes, tint 6→5 (lijf max 3 tinten), f2: zwarte onderrand (12 px) die bij het schrappen verloren ging |
| staart | 3 | 43 | f1: 3 losse vlakjes; f2: krul direct op de modeltoon naar 1/2/5/7 (licht middenstreng tussen zwarte lijnen, zoals het model) |
| zielvlammen | 3 | 12 | lichte randpixels → c |
| **totaal** | **185** | **319** | silhouet-diff 0 t.o.v. de onderlaag in beide frames |

## Controle (`check.py`)
- Tinten per groep: kop 2/3/11, lijf 5/7/8 (6 alleen in staartslierten en 1 px kuif), teal 15/9/10, licht 12/13/14, lijn 1 + vleugellijn 4. ≤3 per groep.
- Lichte randpixels: alleen de lavendel kuif- en zielvlamtips (bewust: de "vlammetjes").
- Kleine vlakjes: wat overblijft zit in dunne delen (staartslierten, kuif, snavel, halsovergang) waar het model zelf 1-px tintlijnen heeft.

## Zwakke punten (resterend)
1. **Frame 2 kop** leest blokkiger dan het model (rechte linkerrand van 5 px, donkere massa): komt uit het schrappen van rijen/kolommen door de ronde kop. Kan in een volgende ronde door de koprijen/-kolommen met een andere schrapkeuze te nemen of 2–3 randpixels uit het model terug te ronden.
2. **Frame 2 kuif**: het model is daar zelf onscherp (Gemini-AA); de sprite volgt het, maar de drie veren lezen minder helder dan in frame 1.
3. Nabije vleugel frame 2 is wat vlakker/vlekkiger dan in frame 1 (model heeft minder strepen).
4. Lichte kuiftips/zielvlammen hebben geen donkere rand (ontwerp; Gen 3-regel "geen licht op de buitenrand" bewust niet toegepast op de vlammetjes).
5. Model-op-schaal op het vel (frame 2) staat ±1 px verschoven t.o.v. de sprite; alleen een weergavekwestie.
