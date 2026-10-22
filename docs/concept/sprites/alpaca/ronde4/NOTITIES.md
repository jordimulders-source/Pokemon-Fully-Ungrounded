# Alpaca ronde 4: dezelfde alpaca, opnieuw getekend als Gen 3-sprite

Feedback op ronde 3 (Jordi):
- "dichter in de buurt"; als schets voltooid qua kleurgebruik en algemeen design.
- Maar: de verhoudingen kloppen niet helemaal, de ogen zijn geen typische Pokémon-ogen, de vormen zijn wat clumsy, de shading is niet zoals Pokémon, en hij staat er niet dynamisch genoeg bij. Het moet meer een Gen 3-sprite worden.

Het design en de kleuren van ronde 3 blijven: een alpaca op vier poten, rode bokshandschoenen aan de voorpoten en het mini-bolhoedje.

## Bestanden
- `anim_front.png` (64×128, geïndexeerd, index 0 transparant)
- `normal.pal`
- `thumbnails.png`: drie houdingen als silhouet.
- `compare.png`: ronde 3 en ronde 4 (f1/f2) naast de GBA-sprites van Mareep, Ponyta, Growlithe, Skitty, Electrike, Houndour, Poochyena, Girafarig, Torchic, Mudkip en Treecko. Op 3× en 1×, in kleur en als silhouet.
- `bron/`: `sh bron/build.sh` bouwt alles opnieuw.
  - `alpaca4.py` maakt de vormen met cel-shading.
  - `alpaca4.seg` bevat de kop, de ogen en de krullen met de hand.
  - `thumbs4.py` en `compare4.py` maken de vellen.
  - Nieuw hulpscript: `tools/concept/sprites/celshade.py`.

## Wat ik van de Gen 3-sprites heb overgenomen
Gemeten op de GBA-indexrasters van Torchic, Mudkip, Mareep, Growlithe, Ponyta en Skitty.

**Ogen**
- Mudkip/Torchic-constructie: zwart, met een witte glans van 2 pixels hoog in een kolom aan de lichtkant.
- Het nabije oog is 4 breed en 4 hoog, met afgeronde hoeken.
- Het verre oog is smaller: 3 breed met een glans van 1 kolom, net als Torchics verre oog (`faf/faf/efe`). Zo zit het perspectief al in het gezicht.
- Geen ronde stip-ogen meer.

**Verhoudingen (fase 1)**
- De kop is groot: ±18 breed en 14 hoog, op een figuur van 46 hoog. Dat is ruim een derde van de hoogte, bovenop een korte hals.
- Het lijf is compacter dan in ronde 3. Wolk en rump zijn naar binnen gehaald (breedte 47, oppervlak 1181 tegen 1102 in ronde 3, maar met een grotere kop).

**Perspectief**
- Het lijf staat in driekwart en wijkt naar rechtsachter. De kop is naar de kijker gedraaid (Growlithe).
- De verre poten (voorpoot met handschoen, achterpoot) zijn kleiner, donkerder (alleen tint 6/7, rood alleen 9/a) en staan hoger op het scherm.
- Het verre oor is donkerder dan het nabije, en het verre oorkwastje is kleiner.

**Shading**
- Cel-shading zoals Gen 3, geen verlopen. Elk onderdeel heeft:
  - een egale basistint;
  - een lichte rand van 1–2 px linksboven;
  - een vaste schaduwband langs onder en rechts;
  - een smalle donkerste rand tegen de zwarte omlijning (rechtsonder).
- Omlijning: selout linksboven in de donkerste tint van het onderdeel, zwart rechtsonder.
- In de wol een paar krulboogjes, zoals Mareep die heeft, in plaats van lijnen overal.

**Dynamiek**
- Frame 1 is de dekking: de nabije handschoen staat opgeheven voor de borst, zoals Ponyta een voorbeen optilt, en hij staat op drie poten.
- Frame 2 is de stoot: de handschoen gaat ver naar voren, de kop zakt mee, de oogleden worden plat en boos, en de mond gaat open.

**Strakke vormen**
- Het silhouet is opgebouwd uit cirkels en polygonen op hele pixels, met een geschulpte wolrand.
- check.py telt 7 losse pixels (ronde 3: 13).

## Thumbnails
- **A: dekking.** Gekozen als frame 1: het meest dynamisch, en Fighting zonder dat hij een mensachtige bokser wordt.
- **B: staand op beide handschoenen**, zoals ronde 3. Statisch.
- **C: stoot.** Dit is frame 2.

## Paletindeling (zelfde indeling als ronde 3)
| index | onderdeel | kleur |
|---|---|---|
| 1–4 | wol (licht → selout) | #ffffff #f6eee6 #cdc5d5 #837b94 |
| 5–7 | vacht | #eeac7b #bd7b52 #7b4129 |
| 8–10 | rood (handschoenen, kwastjes) | #ff8b7b #e63939 #9c1831 |
| 11–12 | goud (polsband) | #f6cd52 #bd8b29 |
| 13 | mond | #d54a5a |
| 14 | wit (glans, tand) | #ffffff |
| 15 | omlijning | #101010 |

Recept: `{'wol':[1,2,3,4],'vacht':[5,6,7],'rood':[8,9,10],'goud':[11,12],'mond':[13]}`.

## check.py (`--stage 1`)
Alleen de LET OP's *geen back.png / icon.png*. Verder alles binnen de Hoenn-spreiding, ook de punten die in ronde 2/3 nog afweken:
- hoogte **46** (ronde 3: 47);
- zwart aan de rand 0,563 (was 0,589);
- rand linksboven helderheid 0,276 (was 0,227);
- schaduw 38 %;
- dithering 3,7 %;
- binnenlijnen zwart 4,4 %.

species_info: `.frontPicSize = MON_COORDS_SIZE(48, 48)`, `.frontPicYOffset = 8`.

## Eerlijk: wat nog niet op Gen 3-niveau is
- **De poten** zijn rechte blokjes. Ponyta en Growlithe hebben gebogen poten met gewrichtjes en een duidelijke stap. Bij ons zit de dynamiek vooral in de opgeheven handschoen; de achterpoten staan nog stijf.
- **De wol** is binnenin vrij leeg. Mareep heeft meer en ritmischere krullen en een grotere schaduwmassa onderaan.
- **De gouden polsbanden** zijn blokjes van 2 rijen bovenop de handschoen. Ze kunnen ronder, als een manchet om de pols.
- **De hals** is een rechte witte kolom met weinig vorm.
- **Frame 2:** de arm is een rechte balk naar de handschoen.
- De kop is het sterkste deel, de rest is nog deels gegenereerd. Een volgende ronde zou het lijf en de poten volledig met de hand tekenen over deze basis (het gezicht staat al in `alpaca4.seg`).
- Nog te maken: back, icoon, shiny en de varianten.
