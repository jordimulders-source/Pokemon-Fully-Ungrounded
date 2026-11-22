# Gloom-regional r4 (eindkeuring volume)

Jordi (20 nov): "ja graag wat meer bolling, schaduw, tinten etc, doe dat in een eindkeuring".

Bestanden: `gloom_r4.png` (64×64, geïndexeerd, index 0 transparant, 16 kleuren incl. transparant), `gloom_r4_8x.png` (wit, NEAREST 512), `vel.png` (r4 | r3 | model), `wissels.py` (r3 → r4, controleert elke oude waarde), `bewijs.py` (diffbewijs).

## Wissels: 133 px, alleen lijftinten (5–8 → 5–8)
Studie vooraf op 8×: Ditto, Gulpin, Grimer, Gloom (Gen 3). Ditto/Gulpin: licht vlak linksboven, groot donkerder onderdeel, schaduwsikkel rechts, diepste tint alleen tegen de rand.
- **Bolling linksboven (20 px midden → licht):** rond lichtvlak rond het linker gesloten oog (x18–23, y27–32), sluit diagonaal aan op de bestaande lipglans.
- **Schaduwsikkel rechts (67 px midden → schaduw):** smal bovenaan (y27 1 px, onder de slagschaduw van de brok), breder naar beneden (5–6 px op y37–39), buigt onder de mond naar de schaduw van de onderkant. De grens loopt als curve, niet evenwijdig aan de rand.
- **Diepe sikkel (26 px schaduw → selout-tint):** onder de rechtervin (slagschaduw van de vin) en langs de rand rechtsonder van lijf en voet, 2 px breed tegen het zwart.
- **Binnenin (7 px schaduw → midden):** de buik onder de mond loopt verder door in midden (y45–46), zodat de onderkant niet één band schaduw is.
- **Vinnen:** linkervin lichte bovenkant (3 px licht, aansluitend op het bestaande tipje); rechtervin onderkant in schaduw (3 px midden → schaduw), punt houdt zijn glans.
- **Voet:** twee eigen lichte lobben linksonder (5 px schaduw → midden) met elk een hooglichtje van 1 px (17,48) en (23,48).

## Palet
Alleen index 8 (lijf licht): (198,108,116) → (204,116,120). Helderheidsstappen lijf nu ±47 → 74 → 104 → 143 (stappen 27/30/39). Index 8 zit ook in de lipglans boven de mond en de vinpuntjes; die pixels zijn niet gewisseld, alleen 1 tint lichter. Index 15 (sintel) en alle lava-indexen ongewijzigd.

## Diffbewijs (`python3 r4/bewijs.py`)
```
palet gewijzigd op indexen: [8]
lavabrok (y<=25, alle pixels): 0
steen/gloed/sintel-pixels overal: 0
zwart (lijn, ogen, mondlijn): 0 | nieuw zwart: 0
ogen (zwart in x18-33, y28-31): 0
kelp (12-14): 0 | nieuw kelp: 0
silhouet (transparant <-> figuur): 0
wissels buiten lijftinten 5-8: 0
totaal gewijzigde pixels: 133
```

## Controle (`gereedschap/controle.py`)
16 kleuren, geen lichte kleur op de buitenrand, geen losse zwarte pixels, zwart 17,9 %. Nieuwe tintvlekjes < 3 px: alleen de twee hooglichtjes op de voet; de rest bestond al in r3.

## Zwakke punten (eerlijk)
- Geen aparte hooglichttint op de grote bolling: het palet is vol (index 15 moet blijven, index 5 zit in de mondring). Bolling en hooglicht zijn daar dezelfde tint (licht). Optie als Jordi een echte glans wil: een kelp-/lijftint delen of de mondring naar schaduw zetten om index 5 vrij te maken (dat raakt de mond, dus alleen met zijn ok).
- Het lichtvlak linksboven en de lipglans raken elkaar diagonaal; samen lezen ze als één groter licht gebied links.
- De onderkant rechts blijft een groot schaduwvlak (zoals in het model en bij Ditto), alleen gebroken door de diepe sikkel en de voetlobben.
