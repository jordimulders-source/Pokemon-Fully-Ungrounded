# Olinguito fase 1, ronde 7: pixel-over van concept B (Haakstaart) volgens de spritingregels

Opdracht: de Gen 3-frontsprite opnieuw, als **pixel-over** van de vaste modeltekening (`docs/concept/ontwerp/olinguito/concept_B.png`) en aantoonbaar volgens `docs/lessen/SPRITING.md` en de Dragonfly Cave-gids zelf. Feedback van Jordi op ronde 6: de lange klauwen moeten terug (lang, één nette groep); de kop en de streep over de kop stonden schuin en dat oogde gek; de ogen zijn niet Pokémon-achtig.

## Bestanden
- `anim_front.png`: 64×128, 4bpp geïndexeerd, 14 kleuren + transparant (index 0); frame 2 eronder.
- `normal.pal`: JASC-palet.
- `compare.png`: modeltekening, ronde 6, ronde 7 (frame 1 en 2) en Teddiursa, Sentret, Zigzagoon, Aipom en Pikachu op 3× en 1×; onderaan de ogen op 6× naast Eevee, Pikachu, Teddiursa, Zigzagoon, Growlithe en Mareep.
- `bron/delen.py`: **de sprite zelf**, als handgeschreven pixelregels per lichaamsdeel, in tekenvolgorde: staart, lijf, voeten, oren, kop, masker en ogen, snuit, klauwen. Latere delen liggen vóór eerdere. Er wordt niets berekend.
- `bron/sprite.txt`: het samengevoegde raster (uitvoer van `delen.py`), één teken per pixel.
- `bron/stap1_verkleind.txt`: de modeltekening verkleind tot 37×46 (naslag), gemaakt met `bron/verklein.py`. `bron/stap2_grof_v1.txt`: het grove silhouet in vlakke kleuren.
- `bron/render.py`: raster naar png en palet (tekent niets zelf). `bron/compare.py`: vergelijkingsvel (`... compare.py olinguito`).
- Opnieuw maken vanuit de repo-root:
  `python3 docs/concept/sprites/olinguito/ronde7/bron/delen.py docs/concept/sprites/olinguito/ronde7/bron/sprite.txt` en daarna
  `python3 docs/concept/sprites/olinguito/ronde7/bron/render.py docs/concept/sprites/olinguito/ronde7/bron/sprite.txt docs/concept/sprites/olinguito/ronde7`.

## Werkwijze in stappen
1. **Verkleinen:** de modeltekening verkleind tot 46 px hoog als onderlegger (`stap1_verkleind.txt`). Daaruit komen de verhoudingen: kop ±45% van de hoogte, de snuit linksonder, het peervormige lijf en de staart als vraagteken achter de rug.
2. **Grof (v1):** het silhouet met de hand, vlakke kleuren. Fouten die je dan meteen ziet: een vierkante kop, vierkante oortjes, en klauwen die als een kruis van strepen op de buik lagen.
3. **Per deel gladstrijken en arceren (v2):** staart, lijf, voeten, oren, kop, gezicht. De kop is opnieuw rond getekend (segmenten 6-2-2-1-1-2-7 vanaf de bovenkant) en staat **recht**: geen kanteling meer.
4. **Klauwen apart en als laatste (v3)**, zoals de gids het riskante deel (Scorplacks scharen) op een eigen laag doet. De eerste poging (vier klauwen naast elkaar boven een donkere poot) las als een mond met tanden op de buik, precies het probleem uit ronde 6. Oplossing: **drie lange klauwen in een waaier** uit één opgeheven voorpoot, met oranje borst tussen de punten, zodat het geen gebit meer is.
5. **Omlijning nagemeten en bijgesteld:** het aandeel zwart aan de rand was 0,66. De lichtkant van de staartringen en het masker kreeg daarom de bruine basistint als omlijning in plaats van zwart (0,57).
6. **Frame 2:** `FRAME2 30` in het palet: rij 30 valt weg en alles erboven zakt 1 px (ademhaling). Kop, klauwen en haak gaan iets omlaag; de voeten en de staartvoet blijven staan.

## Wat er met Jordi's punten gebeurde
- **Klauwen terug, lang, één groep:** drie klauwen van 4–5 px lang (de rechter het kortst), de buitenste wijken uit (waaier zoals in de tekening). Ze zijn dun, dus met **pseudo-omlijning** (gids): licht crème aan de lichtkant zonder lijn, de schaduwtint en een zwarte lijn alleen aan de schaduwkant. De tweede poot zit verstopt achter de eerste; met twee poten werden het acht strepen.
- **Kop en streep recht:** de kop staat recht op het lijf. Het masker is een horizontale band van 5 rijen met een rechte boven- en onderrand. De blik opzij zit nu alleen in de pupillen (rechts in het oog, naar de staart), niet in een scheve kop.
- **Ogen:** zie checklist punt 6.

## Checklist SPRITING.md, regel voor regel
| regel | hoe toegepast |
|---|---|
| 1. Alles met de hand, geen vormgereedschap | Elke pixel staat als tekenreeks in `delen.py`; geen ellips, polygoon, automatische schaduw of omlijning. |
| 2. Grof, dan per onderdeel gladstrijken | v1 grof; daarna per lichaamsdeel (staart → lijf → voeten → oren → kop → gezicht → klauwen), elk als eigen blok in `delen.py`. Pixel-over op de verkleinde modeltekening; Teddiursa is niet meer als skelet gebruikt. |
| 3. Lijnen en curven | Kop: 6-2-2-1-1-2-7, oplopend zonder hoek; haak: boog van 7 boven, 2-1-1 naar beide kanten; de weerhaak is de enige bewuste punt. Niets gespiegeld: linker- en rechteroor verschillen in vorm en binnenkleur, de ogen zijn 3×3 en 4×4, de voeten verschillen, en de drie klauwen hebben elk een andere lengte en helling. |
| 4. Palet: 3 tinten + omlijning | Oranje a/O/p + P, bruin n/N/B (+ zwart), crème c/C/q, oog Y/y, wit, zwart. Opbouw als bij Teddiursa en Growlithe (licht, basis, schaduw, donkere omlijning), gedraaid naar het oranje van de tekening. Geen extra verlopen. |
| 5. Licht linksboven | Hooglicht op de linkerbovenkant van kop, oren, lijf, staart (linkerkolom) en ringen (n); schaduw rechts en onder. Slagschaduw in de schaduwkleur: kop op de borst (rij p onder de kin), staartboog over de haak (inwendige onderkant p), dij over de buik (q). Ruim hooglicht op kop en borst. |
| 5b. Vacht | De vacht is hier glad gelaten (de modeltekening is glad, en Teddiursa en Sentret ook). Geen dithering. |
| 6. Ogen | Gen 3-bouw (zie de oogrij): dichtbij oog 4×4 met gele iris links en een pupil van 2×2 rechts, een witte glans linksboven op de pupil en een gekleurde reflectie (donkergeel) rechtsonder; de onderste rij iris in donkergeel. Ver oog 3×3 met glans, zonder reflectie (te klein). Geen egale gloeiogen en geen poppenogen. |
| 7. Texturen | Ringen als vlakke banden van verschillende hoogte (2-2-3-3-4, naar de voet toe breder, zoals perspectief), met een lichte linkerkolom; geen schubben of losse haren. |
| 8. Omlijning per kleurgroep | Zwart aan de schaduwkant, P (donkeroranje) en N (bruin) aan de lichtkant, crème q als omlijning van de snuit aan de lichtkant. Klauwen met pseudo-omlijning. Overal 1 px; lichtere pixels alleen aan de binnenkant (lichte buitenrand 0,03: alleen de klauwpunten, bewust). |
| 9. Formaat | 64×128, 2 frames, 14 kleuren + transparant; oranje, bruin, crème en oog hebben eigen indexen. |

## Extra lessen uit de gids zelf (niet in SPRITING.md)
- **Riskante delen apart en eerst ruw (Scorplack):** de klauwen als laatste blok, eerst als ruw idee bekeken en pas daarna afgewerkt; de eerste versie (gebit) is weggegooid.
- **Pixel-over mag afwijken van de tekening als de lijn daar beter van wordt (Scyther):** de staart is dunner (4–5 px) dan in de tekening en de klauwen kleiner, omdat ze anders klonterig worden.
- **Schaduw na de evenaar wordt niet donkerder:** één schaduwtint per kleur; de extra donkere bruintint B alleen aan de schaduwkant van de ringen en voeten, zoals Pikachu de omlijningskleur gebruikt voor de diepste schaduw op de voet.
- **Neutrale segmenten pas vanaf ±6 px:** op de oogjes en de oren dus losser, op kop en haak streng.
- **Glans alleen waar het glanst:** alleen in de ogen (en de hoektand is gewoon wit).
- **Strepen volgen het oppervlak:** het masker en de ringen zijn kleurvlakken zonder eigen omlijning (zoals Zigzagoons en Growlithes tekening), alleen gescheiden door kleur.

## Metingen (frame 1, `../../alpaca/ronde7/bron/meet.py`)
| | oppervlak | puur zwart aan de rand | detail | verzadiging |
|---|---|---|---|---|
| **olinguito r7** | **1061** | **0,57** | 1,68 | 0,63 |
| olinguito r6 | 1106 | 0,60 | 1,88 | 0,67 |
| Teddiursa | 652 | 0,37 | 1,86 | 0,56 |
| Sentret | 941 | 0,59 | 1,53 | 0,52 |
| Aipom | 856 | 0,40 | 2,00 | 0,48 |
| Pikachu | 1082 | 0,55 | 1,33 | 0,82 |

Puur zwart aan de buitenrand: **0,57**, binnen 0,35–0,6. Het oppervlak (1061) ligt boven het doel van 800–950: de staart met haak is ±250 px. Kleiner kan alleen met een kortere staart of een kleinere kop; dat verandert het silhouet uit de tekening, dus niet gedaan.

## Eigen oordeel
- **Beter dan ronde 6:**
  - De kop staat recht en het masker is een rechte band; niets oogt meer scheef.
  - De lange klauwen zijn terug als één waaier van drie.
  - De ogen zijn kleine Gen 3-ogen met glans en reflectie; de zijdelingse blik zit in de pupillen.
  - De staartringen verlopen in hoogte en hebben een lichte kant.
- **Zwak:**
  - **De klauwen lezen op 3× als klauwen,** maar op 1× zijn het drie witte streepjes. Ze vallen op, maar niet meteen als klauwen.
  - Het masker is een brede donkere band; op 1× is het gezicht vooral 'masker + twee gele stippen'. Dat past bij het ontwerp (bandiet), maar het is minder vriendelijk dan Teddiursa.
  - Het oppervlak is te groot (zie boven).
  - De snuit is klein; de neus zit helemaal op de rand.
- Geen blinde test in deze ronde (niet gevraagd).
