# Olinguito (Dark-starter, fase 1): ronde 3

Feedback van Jordi op ronde 2: "olinguitos nagels zijn te los van elkaar nu". Hij was het ook eens met de zwakke punten die ik zelf had genoemd: het masker leek op een skibril, de munt was op 1× onleesbaar en de verste arm was vormloos. De pose, de kleuren en het concept van ronde 2 kwamen goed over en blijven.

Bestanden: `anim_front.png` (64×128, geïndexeerd, index 0 transparant), `normal.pal` (ongewijzigd t.o.v. ronde 2), `thumbnails.png` (drie klauwhanden in kleur en silhouet), `compare.png` (ronde 1, 2 en 3 naast Nickit, Purrloin, Sneasel, Galar-Zigzagoon, Impidimp, Treecko, Torchic en Mudkip; 3×, 1× en silhouet), `varianttest.png` en `bron/`.

Reproduceren (vanuit deze map):
```
python3 bron/thumbs.py thumbnails.png
python3 bron/build.py .
python3 bron/compare.py anim_front.png ../anim_front.png ../ronde2/anim_front.png compare.png
python3 bron/varianttest.py anim_front.png varianttest.png
python3 ../../../../../tools/concept/sprites/check.py . --stage 1
```

## Wat er veranderde
- **Klauwen: één klauwhand in plaats van losse stokjes.** Een nieuwe `bundle()` in `build.py` tekent de nagels van één poot met dezelfde kromming, vlak naast elkaar, met 1 px zwart ertussen. De basis is dik (ivoor met een goudschaduw) en de punt dun. De lengtes verschillen een beetje: de middelste nagel is het langst. Ik heb drie varianten vergeleken (`thumbnails.png`):
  - **A:** haken samen omlaag en naar voren;
  - **B:** recht omlaag hangend, alleen de punten gekruld;
  - **C:** nagels naar voren, onder elkaar, met overhangende punten.

  Gekozen is **C**. In kleur én in het silhouet leest hij als één poot met lange nagels (een gebundelde haak), en het blijft de sluiphouding van de inbreker: de poot voor de borst, de nagels hangen over. De achtervoet en de grijpende poot bij de munt hebben ook gebundelde nagels.
- **Frame 2:** de verste klauwhand steekt naar voren ("geef op"), met de nagels samen naar voren gekromd. De dichtste hand is omhoog geheven, met de nagels samen omhoog, onder de opgegooide munt. De staart zwiept verder naar rechts, zodat hij de klauwen niet raakt.
- **Masker:** de rechte band is een organisch bandietenmasker geworden. Het zijn twee afgeronde oogvlekken met een smalle brug over de neus, een kleine "traan" onder elk oog en een zachte punt naar achteren. Boven en onder de brug zie je vacht. De schaduwtint (6) zit alleen aan de onderrand. Zo leest het als een vachttekening (wasbeer) en niet als een bril.
- **Munt:** groter (±10 px) en vrij op schoot, nu met de hand getekend (`coin()`): een zwarte rand, een ring die linksboven licht en rechtsonder donker is, een goud vlak, een geslagen kruisteken en een glansje. Twee nageltoppen van de grijpende poot liggen over de rechterrand. Op 1× lees je een gouden munt. In frame 2 draait de munt schuin (een smalle ellips) met hetzelfde teken.
- **Verste arm:** heeft nu vorm. De bovenarm loopt schuin omlaag naar een zichtbare elleboog, daarna volgt de handschoen tot de pols en een gedraaide poot.
- Grootte, palet en kleuren zijn gelijk aan ronde 2 (45 hoog, 49 breed, 1272 px).

## Paletindeling
Dezelfde als in ronde 2 (zie `../ronde2/NOTITIES.md`). Recept: `{'vacht': [1, 2, 3, 4], 'donker': [5, 6], 'creme': [7, 8], 'goud': [9, 10, 11], 'halsdoek': [12, 13]}`, met wit op 14 en de omlijning op 15. De munt gebruikt nu bewust alle drie de goudtinten (ring 9/11, vlak 10, teken 11). In `goud` blijft ivoor (9) de meest gebruikte tint, dus het recept heeft `'_base': {'goud': 10}` nodig. Volgens `varianttest.png` blijven de lijnen bij een albino-, zwarte en zilveren variant staan. Een zwarte vacht moet wel ook `donker` meekleuren.

## check.py (`--stage 1`)
- **Geen FOUT.**
- OK: hoogte 45, breedte 49, oppervlak 1272, 15 kleuren, licht boven/onder −0,061, 9 losse pixels, verschil frame 1-2 0,629 (Hoenn-mediaan 0,618).
- LET OP **rand zwart 0,77 / rand linksboven 0,16**: de handschoenen, de klauwen (rondom zwart) en de ringen liggen aan de rand. Dat hoort bij het Dark-ontwerp (Poochyena en Mightyena zitten > 60%).
- LET OP **licht links/rechts −0,43**: de lichte klauwen en snuit zitten links en de donkere staart rechts; het ligt aan de compositie.
- LET OP **schaduwtinten 0,67**: de donkere vlakken (handschoenen, masker, ringen) tellen als schaduw.
- LET OP **dithering 1,3%**: bewust egale vlakken.
- LET OP **binnenlijnen zwart 0,15**: dat zijn de zwarte lijntjes tussen de gebundelde nagels. Zonder die lijntjes worden de nagels één ivoren vlek.
- LET OP geen `back.png` en geen `icon.png`: die vielen niet onder deze opdracht.
- species_info: `.frontPicSize = MON_COORDS_SIZE(56, 56)`, `.frontPicYOffset = 4`.

## Checklist Pokémon-design
Zoals in ronde 2 (dier × idee × type, minstens drie Dark-middelen, één iconisch kenmerk, kleur 3 + accent, gezicht met ooglid, vooruitwijzing), met deze verbeteringen:
- **Het iconische kenmerk** (de klauwen) leest nu als één klauwhand: in het silhouet zie je een poot met haken, geen kam.
- **Silhouettest:** zwart op 1× is hij een rondoorige sluiper met een haakhand en een geringde krulstaart. Hij is niet te verwarren met Sentret, Nickit, Purrloin of Sneasel. In frame 2 maakt de munt in de lucht hem uniek.
- **Vooruitwijzing:** het masker is nu een echte wasbeertekening. Dat leidt beter naar het Robin Hood-masker in fase 3 dan de band van ronde 2.
- **De buit leest als buit** op 1×.

## Wat ik zelf nog niet goed vind
- **Klauwhand C in frame 1** lijkt in houding op de grijpende hand in frame 2. Het verschil zit vooral in de munt, de ogen en de bek. Als Jordi de bungelende versie van ronde 1/2 mist, is variant A het alternatief (zelfde bundel, nagels omlaag): in `build.py` `frame1('A')`.
- **De tranen onder de ogen** geven een ietwat vermoeide of sluwe blik. Dat past bij een dief, maar Jordi moet zeggen of het niet te "moe" oogt.
- **De nagels** zijn ivoor met goud. In het zwart staan de bundels er goed in, maar in kleur kunnen ze op 1× nog iets lichter tegen de handschoen.
- Achterkant en icoon ontbreken nog.
