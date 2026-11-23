# Eindkeuring Gnomini – sprite r4 A (22 nov)

Gekeurd: `../sprite_r4/gnomini_A.png` (64×64, 14 kleuren incl. achtergrond). Model: `../r2/gemini_r2.png`. Bevroren besluiten uit `SPEC.md` (gebogen roze/blauw-grens met donkerblauwe streep, ronde armpjes, smoother lijf, muts) niet beoordeeld als ontwerp.
Meetscript: `meet.py` (tekenkaart, clusters < 3 px, randkleuren). Vellen: `gnomini_A_8x_raster.png` (8×, rood raster per 8 px), `vergelijk_1x_3x.png` (naast Igglybuff, Whismur, Azurill, Smoochum, Jigglypuff), `model_crop.png`.

## Oordeel: **PASS** (met 5 kleine pixelreparaties, geen ervan blokkerend)

## Volume eerst
Elk groot vlak heeft volume: muts licht linksboven (4 → 3) met schaduwflank rechts (2) en een taps vouwlijntje; neus met hooglicht linksboven en sikkel rechtsonder; roze bol met slagschaduw onder de rand van de muts en een hooglicht op de bolling; blauwe broek met licht (w) linksboven, middentoon en schaduw rechtsonder. Geen pillow shading, geen effen twee-kleurenvlak.

## Techniek
- **Tinten:** lila 4 (104/130/174/194), roze 4 (105/139/183/206), blauw 4 (96/133/173/205) incl. selout. Stappen 20–44, in de buurt van Taillow. OK.
- **Belijning:** 1 px; zwart aan de schaduwkant (rechts en onder), gekleurde selout aan de lichtkant (lila op de muts, donkerroze op de armpjes, donkerblauw op de linkervoet). Geen lichte kleur op de buitenrand behalve één pixel (zie 4). Twee plekken met zwart/kleur om en om (zie 1, 2).
- **Licht:** consequent linksboven. De lichte onderkant van de rechtervoet komt uit het model (trouw).
- **Dithering/ruis:** geen dithering. Clusters < 3 px zijn bijna allemaal lijnpixels (selout, vouwlijn, streep); echte losse pixels: (38,47) en (41,52).
- **Jaggies:** muts-rechterrand en lijfflanken vloeiend. Linkerrand muts wisselt selout 2/1/2/1 (rij 19–35), zichtbaar alleen op 8×.
- **Formaat:** box x 15–48, y 18–58 (34×41), staat op de grond onderin; even groot als Whismur/Jigglypuff, iets groter dan Igglybuff/Smoochum: past bij een kleine eerste fase.
- **1×-leesbaarheid:** muts, neus, armpjes, roze/blauw en voetjes lezen direct; silhouet duidelijk anders dan de referenties. Staat naast echte Gen 3-sprites zonder op te vallen.

## Pixelreparaties (x,y vanaf 0 linksboven)
| # | Pixel | Nu | Wordt | Waarom | Prioriteit |
|---|---|---|---|---|---|
| 1 | (44,47) | donkerroze a (172,72,102) | zwart K (24,20,32) | onderrand armpje R, schaduwkant, tussen zwart: om en om | hoog |
| 2 | (20,38) | donkerlila 1 (112,95,138) | zwart K | linkerlijn van de neus is verder zwart; lila ertussen = om en om | middel |
| 3 | (38,47) | lichtblauw z (122,188,232) | blauw y (82,148,197) | losse lichte pixel in de schaduwzone onder de streep | middel |
| 4 | (44,42) | roze b (213,102,136) | donkerroze a | lichtere pixel op de buitenrand van armpje R, selout breekt | laag |
| 5 | (41,52) | donkerblauw x (56,109,142) | blauw y | losse donkere pixel bovenop de rechtervoet, ingesloten door zwart | laag |

Optioneel (niet nodig voor PASS): (24,25) lila 2 → 1, zodat de linkerrand van de muts niet 1/2/1 wisselt.

## Ter info voor de eigenaar (geen keuringspunt)
- De neus heeft dezelfde roze als het lijf en leest op 1× vooral door zijn zwarte lijn; dat is een bewuste keuze (open punt "neuskleur" in SPEC).
