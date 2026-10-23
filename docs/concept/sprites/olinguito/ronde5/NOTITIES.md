# Olinguito (Dark-starter, fase 1): ronde 5, met de hand per pixel

Volgende stap na ronde 4 (Jordi: iets beter, nog niet perfect). Hij moest meer een Gen 3-sprite worden: kloppende verhoudingen, echte Pokémon-ogen, nette vormen, Gen 3-shading en een dynamische 3/4-pose. Het design en het palet van ronde 4 blijven (`normal.pal` is ongewijzigd).

Bestanden: `anim_front.png` (64×128, 2 frames), `normal.pal`, `compare.png` (ronde 4 en 5 naast Treecko, Torchic, Mudkip, Cyndaquil, Totodile, Teddiursa, Zigzagoon, Poochyena, Sneasel en Meowth: GBA-originelen op 3×, 1× en als silhouet), `zoom.png` (6× met raster) en `bron/`.

## Werkwijze
1. `bron/render.py` legt alleen de grote vormen neer (kop, oren, lijf, dij, poten, staart, halsdoek). De shading gebeurt met Gen 3-sikkels: het masker min een verschoven kopie. Dat geeft een smal hooglicht linksboven, een schaduwsikkel van 2 px rechtsonder en een donkere binnenrand van 1 px, zonder kussenshading. De omlijning is selout: linksboven in de donkerste vachttint, rechtsonder zwart. Alles staat op 0,88× van de eerste opzet.
2. `bron/handwerk.txt` is het handwerk per pixel, toegepast met `bron/patch.py`. Met de hand gemaakt zijn de hele kop (oren, ogen, masker, snuit, neus, mond met hoektand), de arm met de handschoen, de klauwen, de munt, de halsdoek voorlangs, het lijf, de dij, de poten met sokken en teenklauwen, en de staartbasis. Frame 2 is een kopie van frame 1 met eigen handwerk.
3. Reproduceren vanuit deze map: `python3 bron/render.py r.txt`, dan `python3 bron/patch.py r.txt bron/handwerk.txt bron/anim_front.txt`, dan `python3 ../../../../../tools/concept/sprites/ascii_sprite.py load bron/anim_front.txt normal.pal anim_front.png`.

## Wat er veranderde t.o.v. ronde 4
- **Verhoudingen:** 42×44 px (ronde 4: 51×52). Dat is precies de Hoenn-mediaan voor fase 1 en zo groot als Totodile en Cyndaquil. De kop (met oren) is ±50% van de hoogte en het lijf is klein en gehurkt, met een ronde dij.
- **Pose:** driekwart, sluipend in een hurkhouding. De kop is iets gekanteld (het verre oor lager), de klauwhand hangt naar voren en de verre poot stapt naar achteren. De staart krult op als tegengewicht en de halsdoekpunten wapperen naar achteren.
- **Ogen:** echte Pokémon-ogen: een staand ovaal (dichtbij 5×5, veraf 3×4 binnenin) met een zwarte rand, een zwarte pupil naar voren, een witte glans van 2 px, en een gouden iris die onderaan lichter wordt. Het ooglid is aan de buitenkant dikker en de binnenhoek zakt, net als de V-wenkbrauw van Sneasel en Poochyena. Zo kijkt hij sluw maar blijft hij schattig.
- **Masker:** het masker is niet meer grijspaars maar donkerbruin (vachttint 4). Het loopt als vachttekening rond de ogen, over de neusbrug en naar achteren uit. Het is geen bril of band meer.
- **Klauwen:** drie gebogen haken als één groep. Elke nagel is 2 px breed (ivoor met een crèmekleurige schaduwkant) en loopt naar een punt van 1 px, met 1 px zwart ertussen. In het silhouet zie je een klauwhand, geen kam.
- **Frame 2:** de munt is opgegooid (met een glinstering) en de hand gaat omhoog. De ogen zijn dicht in een zelfvoldane boog, de bek staat open en de buik is te zien.

## check.py (`--stage 1`)
- Geen FOUT. OK: hoogte 42, breedte 44, oppervlak 1052, 15 kleuren, 6 losse pixels, verschil frame 1-2 0,30 (aan de lage kant, binnen p10).
- LET OP **rand zwart 0,61, schaduwtinten 0,66, binnenlijnen zwart 0,14**: dat komen door de donkere handschoenen, sokken, het masker en de zwarte lijntjes tussen de nagels. Het hoort bij het Dark-ontwerp, net als in ronde 3 en 4.
- LET OP **licht onder 0,22**: de lichte klauwen, munt en teenklauwen zitten onderaan. Het ligt aan de compositie, niet aan de lichtrichting.
- species_info: `.frontPicSize = MON_COORDS_SIZE(48, 56)`, `.frontPicYOffset = 9`.

## Wat ik zelf nog zwak vind
- **Lijf en achterpoten:** het lijf is nog wat langgerekt en vlak, en de dichte voet is een lange sok-balk. Een spriter zou de dij en de voet nog ronder maken.
- **Frame 2:** het verschil met frame 1 is maar 0,30 (alleen de arm, het gezicht en de munt veranderen). De staart en de poten bewegen niet mee. De open bek is op 1× nauwelijks te zien.
- **De munt in frame 2** is vrij hoekig (7×9). Hij leest als een munt, maar een gedraaide ellips zou mooier zijn.
- **Het masker** is nu subtiel. Op 1× zie je vooral de ogen. Als Jordi het masker nadrukkelijker wil (richting Robin Hood), kan het een tint donkerder of breder naar achteren.
- De ringen van de staart komen nog uit de vormenstap en zijn niet per pixel bijgewerkt.
- Achterkant en icoon ontbreken nog.
