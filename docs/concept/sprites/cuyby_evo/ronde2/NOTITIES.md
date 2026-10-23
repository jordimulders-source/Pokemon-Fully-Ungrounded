# Cuyby-evolutie ronde 2: langhaarcavia als wandelende hooiberg

Ontwerp: `docs/concept/ontwerp/cuyby_evo/ronde2/` (variant B, met een kleine kruinfontein). De sprite is opnieuw begonnen en heeft niets van ronde 1 overgenomen. Hij is per deel met de hand geschreven als run-length-rijen op een absolute x, in `bron/delen_rle.txt`, en de delen staan van achter naar voor:

> verre pootjes → lijf → lokken (scheidingen, haarstreepjes, gekartelde grens) → lokpunten → gezicht → nabije pootjes → kruinfontein → fontein-punt → pony

Er zijn geen vormfuncties, geen automatische schaduw en geen automatische omlijning gebruikt.

## Bouwen (vanuit de repo-root)
```
python3 docs/concept/sprites/cuyby_evo/ronde2/bron/rle.py        # delen_rle.txt -> delen.txt
python3 docs/concept/sprites/cuyby_evo/ronde2/bron/bouw9.py docs/concept/sprites/cuyby_evo/ronde2   # png, pal, rasters + controles
python3 docs/concept/sprites/cuyby_evo/ronde2/bron/vel.py        # compare.png + metingen
```
`bouw9.py` komt uit olinguito ronde 9. Het meldt open randen, rechte randstukken van meer dan 4 px en het zwart-aandeel.

`rle.py` knipt na het tekenen twee kolommen (x 33 en 41) en één rij (y 30) weg, zoals je in een tekenprogramma een strook wegknipt: de eerste opzet was 1487 px. In de bron staan de coördinaten dus van vóór het knippen. De rasters in `bron/raster_f*.txt` tonen het eindresultaat.

## Ontwerp in de sprite
- **Eén vorm:** een lange, lage bult van 52×39 px, waarin kop en lijf geen naad hebben.
- **Vacht:**
  - Vijf scheidingen lopen steil van de rug naar achteren-omlaag, telkens als 'donkerder | scheiding | lichter', want elke lok is links belicht.
  - Bovenaan zijn de scheidingen zacht (d), in het midden stro-omlijning (r) en pas bij de zoom zwart.
  - Drie scheidingen zijn op een plek onderbroken. Daartussen staan korte haarstreepjes (d, en h in het licht) in de haarrichting.
  - De grens tussen basis en schaduw aan de achterkant is gekarteld met losse punten.
- **Achterkant:** drie lokken liggen over elkaar. Elk eindigt in een lichtere punt (s) met een inham eronder, net als bij de staarten van Ninetales.
- **Zoom:** vijf lokpunten hangen tot bijna op de grond en wijzen naar achteren.
- **Fontein:**
  - Uit de kruin schiet één grote lok omhoog die naar achteren overhangt. De lichte punt hangt vrij, met een inham eronder.
  - Binnen de boog is de vacht erachter in de schaduw te zien (d/q).
  - De pony rijst eerst op uit de kruin en valt dan naar voren over het verre oog (Jordi's aanvulling).
- **Gezicht:**
  - Laag vooraan: witte bles en snuit met roze neusje.
  - Cuyby's zwarte vlek met het zwarte rozenblad-oortje. Het oor heeft één roze pixel, want twee lazen als een tweede oog.
  - Een klein nabij oog van 4×4 px met witte glans linksboven, bruine weerkaatsing rechtsonder en een lichte rand (g) in de vlek.
- **Pootjes:** twee nabije pootjes in roze en twee verre in de schaduwtint (P), die net onder de vacht uitkomen.
- **Frame 2:** de vacht golft. De punt van de kruinlok en de vijf lokpunten van de zoom schuiven 1 px naar achteren.

## Checklist (SPRITING.md)
| Regel | Toegepast |
|---|---|
| 1. Geen vormgereedschap | Ja: alles is met de hand geschreven als rijen. Het knippen is een handeling achteraf, geen vormfunctie. |
| 2. Per deel | Ja: negen delen, van achter naar voor. Na elke stap heb ik op 8× en 1× gerenderd. |
| 3. Curven, niet spiegelen | De omtrek van de bult is een trap zonder hoeken. De scheidingen worden geleidelijk steiler. Niets is gespiegeld. Eén recht stuk van 5 px (bovenrand achter de kruin) is gemeld en blijft staan. |
| 4. Palet | Stro h/s/d + q (roest) + r (omlijning), afgeleid van de Ninetales-ramp en iets minder verzadigd. Wit a/b/c + e, zwart g/G, roze p/P, weerkaatsing n en K. 16 kleuren, index 0 transparant. |
| 5. Licht linksboven | Hooglicht op de pony, de kruinlok en de linkerbovenkant. Schaduw (d/q) rechts en onderaan. Slagschaduw binnen de boog van de kruinlok. |
| 6. Ogen | Het nabije oog is klein (4×4) met glans en gekleurde weerkaatsing. Het verre oog zit onder de pony. |
| 7. Vacht gekarteld | Zie 'Vacht' hierboven. Er is geen dithering gebruikt, alleen streepjes en punten. |
| 8. Omlijning | Belichte randen in r of e, de schaduwkant en de zoom in K, overal 1 px. Lichtere tinten staan alleen binnen de omlijning. |
| 12. Geen geamputeerde delen | 4 pootjes, 1 zichtbaar oor (het verre oor zit onder de vacht), 1 zichtbaar oog plus 1 bedekt oog, neus en mond. `bouw9` meldt geen open randen. |
| Kijkrichting | Diagonaal naar links-voor: de snuit steekt schuin uit de vacht en het nabije oog zit achter de bles. Geen zuiver profiel. |

## Metingen (frame 1)
| | oppervlak | b×h | waarvan zwart (rand) |
|---|---|---|---|
| **ronde 2** | 1385 | 52×39 | 0,58 |
| ronde 1 | 1377 | 48×44 | 0,51 |
| Cuyby ronde 3 | 789 | 31×32 | 0,53 |
| Piloswine | 1515 | 42×48 | 0,43 |
| Furret | 1191 | 41×50 | 0,43 |
| Linoone | 1357 | 51×60 | |

Het oppervlak ligt net boven de richtwaarde van 1000–1350, tussen Linoone en Piloswine in. Dat past bij een tweede fase die laag en breed is.

## Eigen oordeel
- **Beter dan ronde 1:**
  - Het leest als een cavia met lange vacht: één lijf, met het gezicht vooraan uit de vacht.
  - Het is geen grasbol meer. De vacht hangt omlaag en eindigt in punten.
  - De familie met Cuyby is direct te zien aan het zwarte oog met het oor, de witte snuit en de roze voetjes.
- **Twijfel:**
  - De kruinlok leest op 1× meer als een knotje of kuif dan als fontein. Een tweede kleine lok die naar voren overhangt, of een bredere waaier, zou het fontein-idee sterker maken, maar maakt het silhouet onrustiger.
  - De scheidingen zijn nog vrij regelmatig verdeeld. Op 3× doet het een beetje aan segmenten denken, en Piloswine gebruikt minder en kortere donkere strengen.
  - De pony is glad, terwijl een paar lokpunten aan de onderrand van de pony hem meer haar zouden maken.
- **Volgende stap (als Jordi de richting goedkeurt):**
  - de scheidingen minder regelmatig verdelen;
  - de pony een gekartelde onderrand geven;
  - de kruinfontein kiezen: één overhangende lok of een kleine waaier.
