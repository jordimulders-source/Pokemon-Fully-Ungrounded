# Viscacha kleur ronde 8: alleen de 4 benoemde reparaties op r7
Basis `raster_r7.txt`; `r8.py` past alleen de zones aan. Pixeldiff per zone (`pixeldiff.txt`): snorharen/gezicht 10, pluim 10, voorpoten 23, nabij oor 5; **buiten de zones 0**. Daarnaast is paletkleur F (snorharen) lichter gemaakt (zie 1).

## 1. Snorharen en gezicht
- Tint F gemeten: lijnkern in het model (107–126, 96–116, 85–107). In de sprite is één lijn van 1 px twee keer zo dik als in het model, dus F is een middentint: (140,124,104), was (118,102,88). Het is niet de omlijning.
- Nabije kant, 3 lijnen van 1 px. Boven en midden delen de wortel (6,36), onder begint bij de snuithoek (7,37). De dubbele wortelpixel (6,35) en het uiteinde (0,41) zijn weg. Tussen de lijnen zit overal minstens 1 rij leeg.
- Verre kant, 2 lijnen: boven (13–14,35) → (15–17,36) → (18–19,37) → (20–21,38) → (22,39); onder takt af bij (15,37) → (16,38) → (17–18,39) → (19,40) … (22,43). De dubbele wortel (13–14,36) is weg en daar is weer vacht/crème gezet.
- Op neus-Y, lip, kinnetje en kinlijn staat geen snorhaarpixel; die zijn niet gewijzigd.

## 2. Pluim
- Punten van 1 px: F1 (58,14), F2 (54,16), F4 (50,22). F3 is (58,20) + (59,20): de punt wijst opzij, dus de bovenste rij heeft rand + kerf.
- Bleek A tegenover rand 8: 32 : 17 (≈ 1,9 : 1, gemeten model ≈ 2 : 1). Er is A gezet waar 9 stond: (56,18–20), (57,21), (55–56,23).
- Kerven 1 px breed, langer zoals in het model: F2/F1 op x54 r17–19, F4 op x51 r23–24.

## 3. Voorpoten
- Twee teenlijntjes in middentint 3, niet in 1.
- Nabije poot: lijnen op x22 en x24 (r50–51); de rechterrand gaat terug naar x25 om ruimte te maken (0,5 px buiten de gemeten rand).
- Verre poot: (13,49) en (15,49), met de middelste teen ertussen.

## 4. Nabije oor
- Top breed en rond volgens de buitenrand van het model: r17 loopt nu van x21 tot x26 (was x22–25, met een afgeknipte hoek), linkerrand op r18 x20. De rechterrand blijft x26 (r17–21).

## Controle
- 16 kleuren, png = raster, geen open randen.
- Losse pixels: alleen snorhaarlijnen.
- Buiten het model: 7 randpixels (3 nieuw door de bredere nabije poot).
- Masker niet gevuld: (59,14) en (53,16), omdat de vlampunten nu 1 px zijn.

## Eigen zwakke punten
1. Waar de 2 verre snorharen beginnen (x13–19, r35–38) lopen ze nog dicht langs elkaar over de grijze crème (6) van de bef. Op 8× is dat lichter dan in r7, maar het blijft een donkerder vlek. In het model liggen ze daar ook dicht op elkaar.
2. De teenlijntjes van de verre poot (middentint op 4) zijn op 1× nauwelijks te zien.
3. De pluim leest op 8× nog als één geheel, met smalle kerven tussen de vlammen. Het model laat meer wit tussen de vlampunten zien.
