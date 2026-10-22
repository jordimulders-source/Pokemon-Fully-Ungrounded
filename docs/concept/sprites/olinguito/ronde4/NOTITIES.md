# Olinguito (Dark-starter, fase 1): ronde 4, als Gen 3-sprite

Jordi over ronde 3: "dichter in de buurt", en als schets voltooid qua kleurgebruik en algemeen design. Zijn punten van kritiek:
- de verhoudingen kloppen niet helemaal;
- de ogen zijn geen typische Pokémon-ogen;
- de vormen zijn wat clumsy;
- de shading is niet zoals bij Pokémon;
- hij staat er niet dynamisch genoeg bij (geen perspectief).

Het moet meer een Gen 3-sprite worden. Het design en de kleuren van ronde 3 blijven: kastanje, zwarte handschoenen, wasbeermasker, gouden ogen, groene doek, gebundelde lange klauwen en een gouden munt. Het palet (`normal.pal`) is gelijk aan ronde 2 en 3.

Bestanden: `anim_front.png`, `normal.pal`, `thumbnails.png` (drie Gen 3-oogtypes op dezelfde kop), `compare.png` (ronde 3 en 4 naast GBA-originelen op 3×, 1× en in silhouet), `varianttest.png` en `bron/`.

Reproduceren (vanuit deze map):
```
python3 bron/build.py .
python3 bron/thumbs.py thumbnails.png
python3 bron/compare.py anim_front.png ../ronde3/anim_front.png compare.png
python3 bron/varianttest.py anim_front.png varianttest.png
python3 ../../../../../tools/concept/sprites/check.py . --stage 1
```

## Waar ik van leerde (GBA-originelen, per pixel bekeken)
- **Poochyena** (een donker gezicht met een sluwe blik, precies onze situatie): het oog is 6×2 en heeft **geen zwarte rand eromheen**. De bovenste rij is het zwarte ooglid, met **één witte glanspixel boven de pupil**, en daarnaast de iris in schaduw. De onderste rij is donkere iris, een zwarte pupil voorin (naar de snuit), en dan een iris van licht naar middel. Het verste oog is 2–3 pixels met dezelfde glans.
- **Teddiursa en Zigzagoon:** een rond zwart oog met 1 witte glans. Dat is lief, maar zegt niets over het type.
- **Teddiursa en Sentret (verhoudingen):** in fase 1 is de kop ±50–60% van de hoogte, het lijf is klein en de pootjes zijn kort en stomp.
- **Sneasel, Meowth, Aipom en Treecko (perspectief en dynamiek):** het lijf staat in driekwart. De verre ledematen zijn kleiner, een tint donkerder en liggen deels achter het lijf. De houding is actief: schuin, een stap, armen uit, en de staart als tegengewicht.
- **Shading (Teddiursa, Poochyena):** egale vlakken in 3 stappen. Het basisvlak, een vast schaduwvlak langs onder en rechts, een donkere binnenrand van 1 px onderaan, en daaronder het zwart. Daarbij komt slagschaduw onder voorliggende delen (onder de kop, onder een arm) en een klein, strak hooglicht linksboven. Er zijn geen zachte verlopen.

## Wat er veranderde t.o.v. ronde 3
- **Pose (dynamiek, driekwart):** hij sluipt op zijn tenen. Het lijf leunt schuin naar voren, de kop steekt vooruit en de dichtste achterpoot zet een stap op de teen. De verre achterpoot is naar achteren gestrekt en donkerder. De staart staat als een S erachter.
  - Frame 1: de verre arm komt achter de kop vandaan, kleiner en donkerder, en de klauwhand hangt voor de borst. De dichtste hand klemt de munt tegen de borst.
  - Frame 2: de verre klauwhand steekt naar voren ("geef op") en de dichtste arm gaat omhoog na het opgooien van de munt. De ogen zijn dichtgeknepen en de bek staat open met de hoektand.
- **Verhoudingen:** de kop is ±48% van de hoogte. Het lijf is klein en peervormig, en de poten zijn stompjes met zwarte sokken.
- **Ogen:** het Poochyena-type (A in `thumbnails.png`), 6×3 bij het dichtste oog: een zwaar zwart lid, een witte glans boven de pupil voorin en een gouden iris in drie tinten. Het verste oog is smaller, met dezelfde glans. B (rond zwart) en C (ovaal met spleetpupil) staan ernaast. B is lief maar typeloos; C is alert maar minder sluw.
- **Shading:** een nieuwe render-modus `Canvas.render3()` in `tools/concept/sprites/shapepaint.py` doet de Gen 3-regels hierboven: een vast schaduwvlak, een donkere binnenrand onderaan, slagschaduw onder voorliggende delen (per object uit te zetten met `nocast`) en een strak hooglicht. Het hooglicht is kleiner dan in ronde 3. De interne lijnen zijn beperkt tot echte overlappingen; de dij heeft geen lijn meer.
- **Vormen:** kleinere en strakkere vormen. De doek is kleiner, met een knoop die naar achteren waait. De snuit is korter, met een neus van 2×2 en een korte grijns met hoektand. De klauwen zijn gebundeld zoals in ronde 3, maar dunner (1 px met 1 px zwart ertussen), passend bij de kleinere poten.

## check.py (`--stage 1`)
- **Geen FOUT.**
- OK: hoogte 51, breedte 52, oppervlak 1408, licht links −0,23 en boven −0,01, binnenlijnen zwart 0,091 (binnen de Hoenn-spreiding, in ronde 3 was dit 0,15), 8 losse pixels, verschil frame 1-2 0,582.
- LET OP **schaduwtinten 0,75**: de grote donkere vlakken (handschoenen, sokken, masker, ringen) tellen mee als schaduw, en de slagschaduw onder de kop en de armen komt erbij. Op de vacht zelf ligt ±45% in de schaduw.
- LET OP **rand zwart 0,74 / rand linksboven 0,19**: de donkere ledematen en klauwen liggen aan de rand (Dark), net als in ronde 3.
- LET OP **dithering 1,4%**: bewust egale vlakken.
- LET OP geen `back.png` en geen `icon.png`.
- species_info: `.frontPicSize = MON_COORDS_SIZE(64, 56)`, `.frontPicYOffset = 4`.

## Wat ik zelf nog niet goed vind
- **Grootte:** hij is groter dan ronde 3 (51×52) door de uitgestrekte staart en de klauwhand. Voor een basisvorm is dat aan de grote kant (Teddiursa en Sentret zijn veel kleiner; Treecko is 48 hoog). Eventueel de staart compacter maken.
- **Masker:** in het gezicht leest het als twee ringen rond de ogen en dus nog wat als een bril, omdat beide vlekken een donkere onderrand hebben. Een masker dat naar achteren uitloopt tot één vlek (Zigzagoon heeft een band die naar achteren breder wordt) kan beter.
- **Werkwijze:** dit is nog steeds een opbouw uit vormen met regels voor de schaduw, en daarna handwerk aan gezicht, munt en klauwen. Echte Gen 3-kwaliteit (bijvoorbeeld vacht als getande rand in twee tinten, zoals bij Zigzagoon en Poochyena) vraagt een laatste ronde met de hand per pixel over deze basis. Dat raad ik aan zodra Jordi de pose en de verhoudingen goedkeurt.
- **Lijf en dij:** die lopen nog wat in elkaar over tot een zak. De knie of de dij mag duidelijker.
