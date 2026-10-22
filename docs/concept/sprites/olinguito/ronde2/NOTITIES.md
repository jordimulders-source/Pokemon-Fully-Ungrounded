# Olinguito (Dark-starter, fase 1): ronde 2 "Zakkenroller"

Bestanden: `anim_front.png` (64×128, 2 frames, geïndexeerd, index 0 transparant), `normal.pal` (JASC), `thumbnails.png` (drie silhouetten vooraf), `compare.png` (ronde 1 en 2 naast Nickit, Purrloin, Sneasel, Galar-Zigzagoon, Impidimp, Treecko, Torchic en Mudkip; 3×, 1× en silhouet op 2× en 1×), `varianttest.png` (proef albino, zwart en zilver), `bron/`.

Reproduceren (vanuit deze map):
```
python3 bron/thumbs.py thumbnails.png
python3 bron/build.py .
python3 bron/compare.py anim_front.png ../anim_front.png compare.png
python3 bron/varianttest.py anim_front.png varianttest.png
python3 ../../../../../tools/concept/sprites/check.py . --stage 1
```
`build.py` gebruikt het nieuwe hulpscript `tools/concept/sprites/shapepaint.py`: vormen per onderdeel, een schaduwsikkel rechtsonder via een verschoven masker, selout, binnenlijnen tussen overlappende delen en haakklauwen per pixel (met zwart ertussen). Het gezicht, het masker en de munt zijn met de hand getekend als ASCII-patches.

## Werkwijze: eerst silhouetten (`thumbnails.png`)
- **A Zakkenroller:** zittend, Jordi's pose, een bungelende klauwpoot, een munt op schoot, een geringde krulstaart en een halsdoekknoop.
- **B Sluiper:** laag op vier poten (Nickit-houding), met de staart hoog.
- **C Taxateur:** rechtop, en houdt de munt tegen zijn oog.

Gekozen: **A**. Jordi waardeerde de pose, en de bungelende haken breken de omtrek het sterkst. B leest in het zwart als Nickit of een kat. C is leuk, maar daarbij gaat de pose verloren. De pluk ("kroontje") uit thumbnail A heb ik in de uitwerking weggelaten (zie de keuzes hieronder).

## Ontwerp: dier × idee × type
- **Dier:** de olinguito, met een rond teddyhoofd, ronde oortjes, een korte snuit en een lange staart.
- **Idee:** een zakkenroller, het begin van Robin Hood. Hij draagt zwarte **inbrekershandschoenen** tot de elleboog en zwarte sokken, een **donker masker** over de ogen (in de coati wordt dat een band, in de wasbeer het Robin Hood-masker) en een **groene bandietendoek** met een knoop opzij (in fase 3 de kap of cape). Zijn buit is een **gouden munt**, niet langer een bes.
- **Type (Dark):** de basis is warm-donker kastanje met zwart (de Nickit-methode). Het felste van de sprite zijn de **gouden ogen in het donkere masker**. De ogen zijn halfgesloten, met zware leden en een spleetpupil, en hij heeft een scheve grijns met één hoektand. De klauwen zijn lange **haken** zoals bij Sneasel, en de staart heeft donkere ringen en een donkere punt.
- **Klauwen (Jordi):** 7–10 px lang, gekromd als haken, ivoor met een goudschaduw en zwart omlijnd. De drie bungelende klauwen waaieren uit, zodat ze ook in het silhouet als losse haken lezen. Twee klauwtoppen pakken de munt vast en de achtervoet heeft twee klauwen. Bij het verkleinen bleven de klauwen en ogen even groot in pixels; ze zijn dus relatief langer en groter dan in ronde 1.
- **Kleur (Jordi: donkerder):** de vacht is kastanje `#A45A31` (basis) / `#7B4129` / `#4A2920`, tegen het oranjebruin van ronde 1. Het geheel is duidelijk donkerder, maar dankzij het goud, het ivoor en de groene doek niet modderig.
- **Frame 1:** de sluipende inbreker, Jordi's pose. De verste poot bungelt voor de borst met hangende haken, en de dichtste poot klemt de munt op schoot.
- **Frame 2, "hehe":** de ogen zijn dichtgeknepen tot gouden boogjes, de bek staat open met de hoektand, beide klauwpoten zijn wijd gespreid en de munt draait in de lucht (smal, op zijn kant). De staart zwiept verder uit en de kop gaat 1 px omhoog.
- **Kleurendriehoek van het trio:** de olinguito is donker en warm (kastanje en zwart, accent goud), naast de lichte alpaca (wit, cacao, rood) en de koele, middelhelle nachtaap (lavendel, magenta).

Keuzes die ik zelf maakte:
- **Geen pluk op de kop.** Ik heb drie versies geprobeerd. Samen met de oren gaf elke pluk een "kroontje" van drie punten, waardoor de kop als kat of vos las. Met ronde oortjes blijft hij een olinguito, en het silhouet breekt al op de klauwen, de staart en de doekknoop.
- **De staart heeft een spitse donkere punt, geen getande.** De getande variant las als een derde, donkere hand.
- **Geen wenkbrauw.** Op deze maat werd het een losse streep op het voorhoofd. Het zware ooglid draagt de sluwe blik al.
- **Verkleind** met factor 0,84 (alles in `build.py` loopt via `T()`): van 55 px hoog naar **45×47**, met een oppervlak van 1264 px. Ronde 1 was 1130 px, Treecko 967 en de Hoenn-p90 is 1674. Zo houdt de lijn ruimte om te groeien (de eindvorm wordt ±2×).

## Paletindeling (8 paletten, SPRITE_PLAN §5)
| index | kleur | wat | groep |
|---|---|---|---|
| 0 | `#7BD5A4` | transparant | |
| 1 | `#C5835A` | vacht: hooglicht | `vacht` |
| 2 | `#A45A31` | vacht: **basis** (meest gebruikt) | `vacht` |
| 3 | `#7B4129` | vacht: schaduw | `vacht` |
| 4 | `#4A2920` | vacht: donkerst (selout, binnenlijnen arm/doek, mondbinnenkant) | `vacht` |
| 5 | `#5A4A5A` | donker: **basis** (handschoenen, sokken, masker, staartringen, binnenoor) | `donker` |
| 6 | `#312039` | donker: schaduw en onderrand van het masker | `donker` |
| 7 | `#E6D5A4` | crème: **basis** (snuit, buik) | `creme` |
| 8 | `#B4946A` | crème: schaduw | `creme` |
| 9 | `#FFEEC5` | ivoor: klauwen, glans op de munt | `goud` |
| 10 | `#F6C541` | goud: iris, munt | `goud` |
| 11 | `#AC8329` | goud: schaduw (klauwbasis, munt, pupilrand) | `goud` |
| 12 | `#4A9C5A` | halsdoek: **basis** | `halsdoek` |
| 13 | `#296A41` | halsdoek: schaduw | `halsdoek` |
| 14 | `#FFFFFF` | wit: oogglans, hoektand | |
| 15 | `#101010` | omlijning, pupillen, neus, mond | |

Receptvorm: `{'vacht': [1, 2, 3, 4], 'donker': [5, 6], 'creme': [7, 8], 'goud': [9, 10, 11], 'halsdoek': [12, 13]}`, met wit op 14 en de omlijning op 15.
- **Bewuste afwijking van §5 punt 5 (ogen een eigen groep):** het budget was op, dus de iris, de munt en de klauwen vormen samen één groep, het **gouden accent**. Een variant verschuift daardoor de hele "glinstering" in één keer (zilveren klauwen, munt en ogen; zie `varianttest.png`, onderste rij). Dat lijkt me voor een dief juist passend. Wil Jordi aparte oogkleuren, dan moet een vachttint weg (bijvoorbeeld index 1, de hooglichttint, die maar 4–8 px gebruikt).
- In de groep `goud` is de lichtste tint (9, ivoor) de meest gebruikte, omdat de klauwen groot zijn. Het recept heeft dan `'_base': {'goud': 10}` nodig, of een donker doel.
- In de groepen `donker`, `creme` en `halsdoek` ligt de basis op de lichtste tint (ramps van 2). Dat past bij §5.3, omdat er geen apart hooglicht is.
- **Proef** (`varianttest.png`): bij een albino- en een zwarte vacht blijven alle lijnen staan. Bij een zwarte vacht vallen het masker en de ringen weg als `donker` niet meekleurt: een zwarte variant moet `donker` dus lichter of gekleurd maken (bijvoorbeeld ringen in leiblauw).

## check.py (`--stage 1`)
- **Geen FOUT.**
- OK: hoogte 45, breedte 47, oppervlak 1264, 15 kleuren, rand rechtsonder 0,095, licht boven/onder 0,019, 9 losse pixels, verschil frame 1-2 0,596 (Hoenn-mediaan 0,618).
- LET OP **rand: aandeel zwart 0,76** en **rand linksboven: helderheid 0,16**: dit hoort bij het Dark-ontwerp. De handschoenen, sokken, klauwen (rondom zwart, zodat ze los blijven) en de ringen liggen aan de rand, en hun selout is per definitie bijna zwart. Hoenns eigen Dark-soorten (Poochyena, Mightyena) zitten ook > 60%. Op de vacht en de crème werkt de selout wel: daar is de rand linksboven de donkerste vachttint.
- LET OP **licht links/rechts −0,455** (net buiten p10 −0,424): het licht valt sterk van links. Dat komt door de lichte klauwen en snuit links en de donkere staart rechts, dus het ligt aan de compositie, niet aan het licht.
- LET OP **aandeel schaduwtinten 0,66**: de grote donkere vlakken (handschoenen, masker en ringen, index 5/6) tellen als schaduw. Op de vacht zelf ligt ±40% in de schaduw.
- LET OP **dithering 1,3%** (p10 1,5%): bewust bijna geen dithering, want egale vlakken waren juist het punt van Jordi's kritiek.
- LET OP **binnenlijnen zwart 0,13** (p90 0,113): dat komt door de zwarte lijntjes tussen en rond de klauwen, die nodig zijn om ze op 1× als losse haken te lezen.
- LET OP geen `back.png` en geen `icon.png`: die vielen niet onder deze opdracht.
- species_info: `.frontPicSize = MON_COORDS_SIZE(56, 48)`, `.frontPicYOffset = 4`.

## Checklist Pokémon-design (SPRITE_PLAN)
- [x] **Dier × idee × type:** het dier is een kleine beer- of wasbeerachtige met een lange geringde staart. Het idee is een dief met masker, handschoenen, bandietendoek en buit. Het type is donker met gouden ogen, een grijns en haken. Of iemand zonder uitleg "dief" én "Dark" zegt, moet een echte blinde test bij Jordi uitwijzen.
- [x] **Type met minstens drie middelen:** een warm-donker palet met zwart, gloeiende gouden ogen in een donker masker, halfgesloten ogen met een grijns en hoektand, klauwen, en de sluiphouding met buit.
- [~] **Basisvorm:** een bol hoofd op een peervormig lijf, met stompjes als poten. De armen zijn nog vrij "echte" buizen. Het is minder sterk gestileerd dan Torchic of Mudkip, maar wel eenvoudiger dan ronde 1.
- [x] **Eén iconisch kenmerk dat het silhouet breekt:** de lange haakklauwen (in elke vorm van de lijn). Het masker en de doek zijn ondersteunend.
- [x] **Silhouettest** (`compare.png`, onderste rijen): frame 1 leest door de uitwaaierende haken niet meer als Sentret of eekhoorn, en is in het zwart ook niet te verwarren met Nickit, Purrloin of Sneasel. Frame 2, met gespreide klauwen en een munt, is het meest uniek.
- [x] **Kleur:** drie hoofdkleuren (kastanje, bijna-zwart en crème) en één accent (goud), met de groene doek als tweede, kleiner accent. Het helderheidscontrast is groot.
- [x] **Gezicht:** grote ogen met glans en een ooglid dat de houding geeft (zelfvoldaan en sluw). Frame 2 is een karaktermoment.
- [x] **Vooruitwijzing:** het masker wordt het Robin Hood-masker, de doek de groene kap of cape, de klauwen blijven, de ringen worden de coatistaart en de munt wordt "geven aan de armen".
- [x] **Starters:** naast de starters valt hij niet weg als "het dier zonder thema", en hij is duidelijk donkerder dan de alpaca en de nachtaap.
- [x] **Andere Pokémon van hetzelfde dier** (vergelijkbare soorten: Sentret, Zigzagoon en Galar-Zigzagoon): het verschil zit in het palet, het masker, de ogen en de haken, net zoals bij Galar-Zigzagoon.
- [x] **Gespriet, niet geïllustreerd:** egale vlakken, schaduwsikkels en geen vachtruis.

## Wat ik zelf nog niet goed vind
- **De munt in frame 1** wordt deels bedekt door de rechter bungelende klauw en de grijpende klauwtoppen. Op 1× lees je een gouden vlek met een teken, niet meteen een munt. Een grotere munt of een munt iets hoger op de buik kan beter.
- **De verste arm** is een vrij dikke donkere worst. Dat leest als een handschoen, maar er zit weinig vorm in (geen elleboog of pols).
- **Het masker** heeft een rechte bovenrand en leest ook een beetje als een zonnebril of skibril. Een masker met uitgesneden kijkgaten (de ogen in een lichtere ring) of met wapperende punten zou meer "inbreker" zijn.
- **De kop** heeft weinig hooglicht (index 1 wordt maar 4–8 px gebruikt). Hij kan iets "frisser", met een groter hooglicht linksboven.
- **De halsdoekknoop** rechts valt in het silhouet tegen de staart weg.
- De ivoren klauwen lijken in frame 2 aan de rechterkant (tegen de staart) wat op een vork.
- `back.png` en het icoon ontbreken nog. Die volgen pas na Jordi's akkoord op de front.
