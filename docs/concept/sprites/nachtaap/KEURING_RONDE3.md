# Keuring nachtaap, ronde 3 (onafhankelijk)

Gekeurd: `ronde3/anim_front.png` (2 frames van 64×64, 15 kleuren + transparant).
Vergeleken met de Gen 3-originelen (`anim_front_gba.png`) van Treecko, Torchic, Mudkip, Abra, Ralts, Natu, Spoink, Meditite, Wynaut, Duskull, Chimecho en Aipom, en met Espurr/Munna/Elgyem, op 1×, 2×, 4× en 8×.

Plaatjes:
- `keuring/r3_naast_gen3_4x.png`: beide frames naast Torchic, Mudkip, Ralts, Aipom, Natu, Spoink en Espurr.
- `keuring/r3_frames_8x_raster.png`: beide frames op 8× met pixelraster.

## Cijfers

| | cijfer |
|---|---|
| Pokémon-echtheid | **5,5 / 10** |
| Gen 3-consistentie | **5 / 10** |

Kort: het is een schoon, aaibaar, duidelijk paars Psychic-wezentje. Op ware grootte springt hij er tussen de Gen 3-sprites wel uit. Hij ziet eruit als een **pluchen speeltje of vinylfiguurtje** (frontaal, symmetrisch, kop op een rechthoekig blok, glimmende anime-ogen), niet als een Gen 3-sprite van een dier.

## 1. Echte Pokémon of fanart?

Wat goed werkt:
- Groot hoofd, klein lijf, één sterk accent (spiraalstaart). Dat is precies de formule van een eerste fase.
- Het silhouet is op 1× herkenbaar: ronde kop, oortjes, krul.
- Het palet is beheerst: één hoofdkleur met roze en cyaan als accent. Dat doen de echte sprites ook.

Waardoor hij als fanart oogt:
- **De pose is volledig frontaal en spiegelsymmetrisch.** Geen enkele Gen 3-starter of Hoenn-babymon staat zo. Treecko, Torchic, Mudkip en Aipom staan allemaal in een 3/4-aanzicht naar links, met het gewicht op één kant. Gen 3 kent alleen bij bewust 'objectachtige' soorten een recht vooraanzicht (Baltoy, Lunatone, Chimecho, Duskull ongeveer). Bij een aap voelt het stijf, als een product.
- **Het lijf is een rechthoek met rechte zijkanten** (kolommen 19 en 38 lopen ±8 rijen kaarsrecht naar beneden) met horizontale banden van index 3/4 erover. Het leest als een vaas, een robotje of een mok, niet als een zittend dier. De armen in frame 1 zijn niet als armen te herkennen: het zijn verticale stroken tegen de zijkant, die opgaan in het blok. De voeten zijn een plat voetstuk.
- **De ogen zijn in de stijl van Littlest Pet Shop/chibi:** ronde marineblauwe bollen met een diagonale glimstreep en een cyaan reflectie onderin. Gen 3 tekent ogen veel eenvoudiger: een donkere vorm met één of twee witte pixels (Torchic, Mudkip, Ralts, Abra), of een iris met een harde pupil (Treecko). Grote ogen zijn bij een nachtaap terecht, maar de rendering is te 'glossy'.
- **Drie identieke roze juweeltjes** (voorhoofd + twee oren) plus een edelsteen op de borst. Eén 'psychisch orgaan' is Pokémon (Espeon, Ralts' hoorn, Spoinks parel). Vier losse sieraden is fanart-versiering: het leest als 'versierd', niet als 'zo gegroeid'.
- De spiraalstaart is een perfecte, even dikke (3 px) wiskundige spiraal van 1,5 slag. Dat oogt als vectorwerk. Aipoms staart (en die van Mudkips vin) wordt naar het eind toe smaller en heeft een organische S-curve.

Zou hij tussen Gen 3 opvallen? Ja. Vooral de rechte stand, het blokvormige lijf en de ogen.

## 2. Leest hij als Psychic? Mysterieus/zachtaardig?

- **Psychic: ja, meteen** (lavendel, roze, een juweel, een spiraal). Misschien zelfs té letterlijk: elk cliché tegelijk.
- **Zachtaardig: ja** in frame 1 (grote, zachte ogen, geen mond, witte snuit).
- **Mysterieus: nauwelijks.** Niets verwijst naar de nacht of naar 'iets weten wat jij niet weet': geen lichtgevende ogen, geen schaduw over de bovenkant, geen maanvorm. Het is 'schattig', niet 'raadselachtig'. Vergelijk Natu (die strakke blik zonder emotie) of Espurr (half dichte, starende ogen): daar komt het mysterie uit **wat de ogen doen**, niet uit sieraden.
- **Nachtaap: matig.** De witte wenkbrauwvlekken zijn er, maar het belangrijkste kenmerk van een nachtaap ontbreekt: de **drie donkere strepen** (één tussen de ogen omhoog, twee langs de zijkanten van het gezicht), die het masker vormen. De oren zijn ronde knopjes met een roze stip en lezen als schroefjes of antennes. Zonder uitleg denk je eerder aan een galago, een koboldmaki of een kat.

## 3. Techniek naast Gen 3

**Formaat en verhoudingen.** De begrenzing is 48×42 (frame 2: 50×42). Dat is groot voor een eerste fase (Torchic 33×47, Mudkip 40×41, Ralts 23×35), maar de verhouding kop:lijf (±1:1 in hoogte, kop breder) past bij een babystarter. Het lijf is te hoekig, niet te klein.

**Silhouet.** De kop en de staart zijn goed. Het onderlijf is een rechthoek met een platte voet: het slechtste deel van het silhouet. Er zit geen ruimte tussen arm en lijf en geen schouderlijn.

**Lijnwerk (selective outlining).** De zwarte omlijning (16,16,16) is Gen 3-correct. Maar:
- De bovenkant van de kop is omlijnd met **index 3** (131,115,189). Dat is de schaduwtint van het lijf zelf, dus de kop smelt bovenaan weg tegen een lichte achtergrond. Gen 3 laat de omlijning aan de lichtkant wel lichter worden, maar dan naar een donkere tint van de kleur (hier index 4, (74,57,106)), niet naar de middentoon. Kijk naar de bovenkant van Mudkips kop of Aipoms oren: donker gekleurd, nooit de middentoon.
- Binnenlijnen zijn te zwaar. De ogen hebben een volle zwarte ring plus marineblauw, en het borstjuweel heeft een zwarte ring: daardoor worden het 'gaten' in de vorm. Gen 3 gebruikt binnen de vorm donkere tinten van de eigen kleur, geen zwart (behalve bij de ogen).
- De onderkant (voeten) heeft een dubbele zwarte rand (rijen 56–57), wat zwaar en plat oogt.

**Shading.** Het licht komt consequent van linksboven, goed. Maar de schaduw volgt de vorm niet: het lijf heeft horizontale strepen van index 3 en 4 (rijen 46–55), die ringen of plooien suggereren in plaats van een bolle buik. Gen 3 schaduwt in een halve maan langs de rechteronderkant van elke bolle vorm (Mudkips lijf, Torchics borst) met een klein, scherp hooglicht linksboven. Het hooglicht van de kop (index 1 linksboven) is goed van plaats, maar te groot en te vlak.

**Kleuren en palet.** Er worden 15 kleuren gebruikt; prima. Het lavendel heeft weinig contrast tussen 1, 2 en 3, en daardoor oogt het op 1× wat wazig. De cyaan oogreflectie en het cyaan juweel vechten om de aandacht met de roze stippen: drie accentkleuren op een klein figuur. Index 14 (puur wit) wordt maar 4× gebruikt; dat is prima als hooglicht.

**Leesbaarheid op ware grootte.** Kop en staart: goed. Lijf: een paarse vlek met een cyaan stip. De ogen domineren alles.

**Pose, dynamiek, perspectief.** Er is geen perspectief: alles staat recht naar voren, en beide voeten en de staart staan op dezelfde lijn. Er is geen gewichtsverdeling en geen 3/4-draai van de kop.

**Frame 1 → 2.** De zwaaiende hand is een goed idee (vriendelijk, een healer in de dop), al is de hand een los roze klauwtje. Maar **de ogen veranderen** van zachte, donkere bollen naar starende, lichte ogen met een speldenknoppupil. Daardoor wordt hij in frame 2 een geschrokken of ietwat gestoord ander wezen. In Emerald-animaties blijven de oogvorm en het karakter gelijk: frame 2 is een rek, een sprongetje of een andere armhouding (Torchic, Mudkip). Als het oogeffect 'psychische kracht' moet betekenen, kies dan een gloed in hetzelfde oog (bijvoorbeeld het cyaan van onderin naar boven laten lopen), geen andere pupil.

## 4. Wat er moet gebeuren voor een 8+

Op volgorde van effect:

1. **3/4-pose.** Draai de kop ±20° naar links: het linkeroog smaller/verder weg, het rechteroog groter, de snuit naar links verschoven. Zet het lijf schuin (rechterschouder hoger of verder naar voren). Voorbeelden: Aipom (zelfde diersoort-familie!), Treecko en Mudkip. Dit is veruit de grootste stap naar 'echt'.
2. **Een zittend dierenlijf in plaats van een blok.** Een peervormige romp (smal bij de nek, breed bij de heupen), daaronder gebogen achterpoten met dijen die als een bolletje zichtbaar zijn, en voetjes met 2–3 teenpixels. Armen als aparte vormen met een donkere scheiding (index 4) tegen het lijf, de handjes vóór de borst gevouwen óf om het juweel heen. Haal de horizontale banden uit de romp.
3. **Nachtaapmasker.** Een donkere streep (index 4) van tussen de ogen naar het voorhoofd, en twee donkere strepen langs de buitenkant van de ogen naar de kaken, met het wit erboven als 'wenkbrauwen'. Dat is meteen herkenbaar en geeft vanzelf iets mysterieus (masker = geheim), zonder sieraden.
4. **Minder sieraden.** Kies één psychisch kenmerk: óf het juweel op het voorhoofd (zoals een derde oog), óf het borstjuweel. Haal de roze stippen uit de oren en maak de oren tot echte, kleine afgeronde schelpjes met een donkere binnenkant (nachtapen hebben kleine, verborgen oren: 2–3 px uitsteeksel is genoeg).
5. **Gen 3-ogen.** Houd ze groot (dat ís de nachtaap), maar: een donkere iris zonder volle zwarte ring, met 1 witte glimpixel linksboven en hooguit 1–2 pixels lichter blauw onderin. Geen diagonale glimstreep. Voor het mysterie: halve oogleden (de bovenste 2 rijen van het oog in de lijfkleur), zoals Espurr en Natu. Dan is hij rustig en raadselachtig in plaats van verbaasd.
6. **Staart organisch maken.** Taps toelopend (3 px aan de basis, 2 px aan het eind), met een S-bocht vanaf de heup vóór de krul, en een onregelmatige krul (de binnenste slag kleiner en niet perfect rond). Het roze in de krul mag blijven als het enige accent, of de staartpunt licht op in plaats van de oren.
7. **Omlijning aan de lichtkant naar index 4**, niet naar index 3 (bovenkant van de kop, de linkeroren, de linkerschouder). Zwarte binnenlijnen rond het juweel vervangen door index 4/13. Enkele zwarte onderrand in plaats van een dubbele.
8. **Schaduw als halve maan** langs de rechteronderkant van kop, romp en dij (index 3, de rand index 4), met een klein hooglicht van 2–4 pixels index 1 linksboven op kop en buik. Meer contrast tussen 1/2/3 (bijvoorbeeld index 3 een stap donkerder en blauwer) zodat hij op 1× niet wazig is.
9. **Frame 2 dezelfde ogen geven** als frame 1. Laat alleen de arm zwaaien, met eventueel een lichte rek omhoog (de kop 1 px hoger) of een krul die strakker wordt. Teken de hand als een ronde handpalm met 3 vingerpixels (zie de hand van Aipoms staart), in lijfkleur met een donkere rand, niet roze.

Met punt 1–3 en 5 kom je volgens mij op een 7. Met de rest (lijn, schaduw, frame 2) op een 8.
