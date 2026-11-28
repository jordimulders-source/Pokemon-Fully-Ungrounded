# Shuppetto-icoon (proefrit bak B, 28 nov)

Af: `af/icon.png` (32×64, 2 frames, modus P, index 0 transparant), `af/icon_8x.png` (front 4× + frame 1 en 2 op 8×), `af/icon_anim.gif`.
**Palet: pal0** (`.iconPalIndex = 0`), net als Banette en Shuppet.

## Onmisbare kenmerken (stap 1)
1. Enorm narrenhoofd: het hoofd is het hele icoon (±15 breed, 19 hoog binnen 27×23), met de rode mutspunt omhoog en naar rechts gekruld en de grijze punt die links naar beneden hangt.
2. Rood/grijs-verdeling: links grijs, rechts rood, scheiding (naad) recht door het midden (x 15, in de front x ±30).
3. Zigzaggrijns: donkere zigzagband van 2 px over de hele onderkant van het gezicht, met tanden in de kleur van de helft eronder/erboven (grijs links, rood rechts).
4. Ogen zoals in de front: links rood + geel in een donkere kas, rechts geel met een donkere, schuine ooglidlijn erboven.
Daarnaast (mag eenvoudig): marionettenkruis rechts als grijze X aan de hand, links een klein grijs stompje van het kruis achter de hangende punt; de stofrand (Banettes oude lijf) als grijze klomp met twee voetjes eronder.

## Wat valt weg (lessen 13f, 13h)
- **De twee kleine Shuppets: weg.** Jordi (28 nov), letterlijk: "het gaat onmogelijk zijn om de kleine shuppets in het icoon te zetten bij shuppetto, maar dat is niet erg want Dragapult heeft ook geen kleine Dreepy's".
- **Draden (1 px in de front): weg.** Ze hangen alleen naar de Shuppets toe; zonder Shuppets zijn het losse streepjes. Volgens 13e zouden het stompjes buiten het silhouet worden, maar hier zijn het geen kenmerken van de kop, en ze zouden de breedte (al 27, de grens) overschrijden.
- **Belletjes:** links weg (zou een los donker klontje van 2 px onder de punt zijn); rechts blijft er één donkere pixel (index 14) als bel op de punt van de rode krul, op het kruis.
- **Linkerkruis:** wordt een stompje van 2 px grijs naast de hangende punt (in de front ook grotendeels verstopt).
- **Steekjes op de naad:** de naad is één doorlopende donkere lijn (index 14 in het grijs/rood, 15 in de mond).

## Kleur (pal0, streng)
- Grijs front 184/144/100 → pal0 2 (189) licht / 1 (131,131,115) / 14 (98,98,90) schaduw. Licht linksboven.
- Rood front 208,64,64 → pal0 6 (213,98,65); lichtrand (240,112,100) → 11 (255,180,164) als glans linksboven op de muts; donkerrood (144,40,48) staat niet in pal0 en geen enkel palet heeft een donkerrood; dichtstbijzijnde is 14 (grijs). Gebruikt zoals Voltorb (pal0) het doet: rood plat met een paar pixels 14 rechtsonder. Daarom is de rode helft vrij vlak.
- Mond donkerbruin (72,56,48) → 15 (dichtstbijzijnde). Oog geel (240,216,128) → 5 (246,246,41).
- 7 kleuren in gebruik.

## Check (`icoon_check.py af/icon.png ../af/shuppetto.png`): 16/17 OK
- NEE "omlijning boven donkerder dan onder" (boven 68, onder 67): bewust. Het stijlanker Banette en Shuppet (en Dusclops) gebruiken overal index 15 als omlijning; Banettes eigen icoon zakt op precies dezelfde check (65/65). Met 14 als onderrand verdween de grens tussen het grijs (1) en de lijn (14) in pal0 (te weinig contrast, geprobeerd in g5).
- Hoogte 23 (doel 23), breedte 27 (grens), IoU met de front 0,66 (Shuppets en draden tellen in de front mee), hoekig 0,00, trapjes 55, binnenlijnen 0,23, frame 2 11% anders.
- Bekeken op 8× naast de front en op 4×/1× naast Banette, Shuppet, Dusclops, Dragapult en Voltorb (`g8_vel.png`).

## Frame 2 (stap 7)
Alles boven de voeten 1 px omlaag, de bovenste stofrij valt weg onder de romp, de voeten blijven op rij 29. Gebaar: de rechterhand met het kruis blijft staan (trekt dus 1 px op t.o.v. het lijf: de poppenspeler trekt aan de touwtjes). Eén randpixel onder de hand gesloten. Script: `frame2.py`.

## Rondes en werk
- Onderlaag: `bouw.py` (onderdelen-methode, Shuppets/bel/kruisen als losse delen, kleur = meest voorkomende gemapte kleur) gaf `o1`/`o2`: bruikbaar voor maat en plek (hoofd x 7–21, ogen y 16–17, mond y 19–22, stof x 15–20), maar de omlijning en de mond vielen weg. Daarna met de hand per pixel op die maten getekend als tekstraster (`g*.txt`, `render.py`).
- 8 rondes (g1–g8), allemaal zelf; geen aparte keurder (proefrit). g1 te hoekig/blokkig; g2 vorm naar de onderlaag; g3 mond als zigzag; g4 zigzag berekend (periode 4, 2 px dik); g5 breedte naar 27; g6–g7 hoekigheid (rechte randstukken 0,34 → 0,00: ronde top, hangende oorpunt, bolle rechterkant, twee voetjes) en frame 2; g8 schaduw rood.
- Wat moeite kostte: (1) de mond: een "natuurlijke" zigzag van 1 px leest als ruis, pas een berekende zigzag van 2 px dik met tanden in de helftkleur werkt; (2) breedte: het ontwerp is 60 px breed (kruizen), de grens 27 dwingt de kruizen naar binnen; (3) geen donkerrood in de 6 paletten, dus het rood is vlak; (4) frame 2 met een zwevende soort zonder poten: het gebaar (hand + kruis) moest los van de rest blijven en de rand onder de hand moest weer dicht.

## Wat bak B sneller zou maken
- De stijlanker-soorten eerst als tekstraster printen (zie hun omlijning, oog en palet in 1 minuut) en de omlijningskeuze van de familie direct overnemen, ook als de check daarop NEE geeft.
- Een vaste zigzag/tanden-routine (zoals in `maak_g4.py`) voor monden met tanden; komt vaker voor (Banette-, Gengar-, Spiritomb-achtigen).
- Bij soorten met kleine meelopers (Shuppets, Dreepy's, draden): die meteen als "weg" uit de onderdelen halen (Jordi's Dragapult-regel), dan klopt ook de IoU-check beter als je een front zonder die delen meegeeft.
- `bouw.py` met nearest-mode kleur is alleen goed voor maten; het echte werk is het tekenen van omlijning, mond en ogen per pixel. Een tekstraster + `render.py` (vel met front en buren in één beeld) per ronde werkt snel.
