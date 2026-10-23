# Cuyby (Normal, fase 1): ronde 1

Eerste Gen 3-frontsprite van de cavialijn (`POKEMON.md`: originele Normal-lijn, naam met 'cuy'). Doel: een schattig, rond Pokémon voor de eerste routes, in de rij van Zigzagoon, Skitty, Whismur, Sentret en Bidoof.

Bestanden:
- `anim_front.png` (64×128, 2 frames): **variant A, rozet**.
- `B/anim_front.png`: **variant B, chullo**. Hetzelfde lijf en gezicht en hetzelfde palet; alleen het kenmerk op de kop verschilt.
- `normal.pal` (geldt voor A en B), `compare.png` (A en B naast Zigzagoon, Skitty, Whismur, Taillow, Sentret en Teddiursa als GBA-originelen, en Bidoof, Lechonk en Skwovet zoals ze in de game staan; op 3× en 1×), `zoom.png` / `B/zoom.png` (6× met raster) en `bron/`.

## Ontwerp
- **Basisvorm:** een grote ronde kop met een kort broodvormig lijf erachter. Er is geen nek, net als bij een echte cavia. De kop is ±60% van de hoogte en de pootjes zijn stompjes. Driekwart, kijkt naar links. Het dichtbije oog is groot, het verre oog smal.
- **Kleur:** gember met crème, de klassieke cuy-tekening. De bles loopt over de neusbrug naar een crème snoet en de buik is crème. Verder een roze neus, oortjes en blosjes. Een natuurlijk palet past bij Normal (`SPRITE_PLAN.md`: Normal = beige, bruin, crème, roze); het kenmerk is wat hem een Pokémon maakt.
- **Gezicht:** Pokémon-ogen: een staand ovaal van 4×6 met een witte glans van 2×2 linksboven en een bruine reflectie onderaan. Daarbij een roze driehoekneus, een Y-mondje en een blosje.
- **Kenmerk A, rozet:** Abessijnse cavia's hebben 'rozetten', kruinen waar de vacht in een draaikolk staat. Hier is dat een **kuif van drie plukken in een waaier** op de kruin (silhouetbreker) en een **spiraal op de heup** (geometrische tekening, zoals de buikcirkel van Sentret en de spiraal van Stufful). De spiraal kan in de lijn meegroeien of tot een symbool worden (de *limpia*: genezers 'lezen' de cavia).
- **Kenmerk B, chullo:** de vacht op de kop vormt een **chullo**, de gebreide Andesmuts. Hij heeft een rode pompon, een crème kap, een rode band met een geweven ruitjespatroon en oorflappen met kwastjes. Het is 'kleding uit het eigen lijf' (zoals de cape van Piplup): meteen Zuid-Amerikaans en op 1× goed leesbaar. Het nadeel: het leunt meer op een voorwerp dan op het dier.
- **Frame 2:** de *popcorn*-sprong (cavia's springen van blijdschap recht omhoog). Hij hangt 3 px hoger met de pootjes ingetrokken, de ogen dicht in twee boogjes en het mondje open ('wheek!'). De middelste pluk van de kuif (of de pompon) veert 1 px extra omhoog.

## Werkwijze
1. `bron/render.py A|B uit.txt` legt de vormen neer met Gen 3-cel-shading (`bron/sprlib.py`, naar olinguito ronde 5): een smal hooglicht linksboven, een schaduwsikkel rechtsonder en selout (linksboven de donkerste tint, rechtsonder zwart). Gember en crème zijn één vorm met een toonkaart, zodat de schaduw doorloopt over de kleurgrens.
2. `bron/gezicht.txt` bevat het handwerk per pixel (ogen, neus, mond, blosjes, gezicht van frame 2), toegepast met `bron/patch.py`.
3. Reproduceren (vanuit de repo-root): `python3 docs/concept/sprites/cuyby/ronde1/bron/render.py A r.txt`, dan `python3 docs/concept/sprites/cuyby/ronde1/bron/patch.py r.txt docs/concept/sprites/cuyby/ronde1/bron/gezicht.txt uit.txt`, dan `python3 tools/concept/sprites/ascii_sprite.py load uit.txt docs/concept/sprites/cuyby/ronde1/normal.pal anim_front.png`. Het resultaat staat ook in `bron/anim_front_A.txt` / `_B.txt`. Het vergelijkingsvel komt uit `bron/compare_sheet.py` (werkt ook voor niet-Hoenn-soorten).

## Palet (indexindeling voor de latere varianten, §5)
`{'creme': [1,2,3,4], 'gember': [5,6,7,8], 'roze': [9,10], 'iris': [11], 'wit': [12], 'muts': [13,14]}`, omlijning 15. Variant A gebruikt 13 en 14 niet (13 kleuren); die zijn vrij voor een accent in de lijn.

## check.py (`--stage 1`)
- Geen FOUT. Hoogte 40, breedte 46, oppervlak ±1170 (aan de grote kant voor fase 1, kleiner dan Zigzagoon). 13 kleuren, 8 losse pixels. `.frontPicSize = MON_COORDS_SIZE(48, 48)`, `.frontPicYOffset = 6`.
- LET OP **rand zwart 0,59–0,62**: iets zwarter dan Hoenn (p90 0,58). Dat past bij het in-game-contrast (§0).
- LET OP **licht onder / schaduwtinten**: de crème buik en snoet zitten onderaan, en de meting telt gember 6 (de basis) als 'donkere' tint. Het ligt aan de compositie, niet aan de lichtrichting.
- LET OP **verschil frame 1-2 0,11**: de sprong is een verschuiving, die check.py wegrekent; alleen het gezicht en de pootjes veranderen echt.
- Back en icoon ontbreken nog (pas na de keuze A/B).

## Wat ik zelf nog zwak vind
- **De kuif van A** kan op 1× als een vlammetje of een kroontje lezen (gember met lichte toppen). Hij is nu een waaier, nog geen echte draaikolk. Een rozet die meer krult, of crème punten, maakt hem minder 'Fire'.
- **De heupspiraal** is een getekende lijn (index 8). Op 1× zie je hem, maar hij is nog niet per pixel bijgewerkt (de bocht rechtsonder is wat hoekig).
- **Het lijf** is nog vrij vlak gespiegeld: er is weinig dithering (0%), de schaduwsikkel is overal even breed en de dij van de achterpoot ontbreekt. Een spriter zou de bil ronder maken en een vachtrand (getand) langs de rug geven, à la Zigzagoon.
- **De pootjes** zijn stompjes zonder teenlijntjes. Echte cavia's hebben roze voetjes, en dat accent (index 9/10) kan er nog bij.
- **Frame 2** beweegt als geheel. Een tweede karaktermoment (oortjes omhoog of de kuif uitgewaaierd) zou de animatie sterker maken.
- **Variant B** is op 1× het duidelijkst, maar het idee 'Pokémon met een mutsje' bestaat al (Delibirds zak, Smoochum). Het is ook de vraag of de muts in de evoluties blijft (de chullo als poncho/rol voor de genezer?).
