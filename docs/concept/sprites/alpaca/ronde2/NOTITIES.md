# Alpaca ronde 2 ("Wolbokser"): Fighting-starter fase 1

Bestanden:
- `anim_front.png`: 64×128, 2 frames, geïndexeerd, index 0 is transparant.
- `normal.pal`
- `thumbnails.png`: drie silhouetten.
- `compare.png`: ronde 1 en ronde 2 (f1/f2) naast Stufful, Bewear, Makuhita, Riolu, Clobbopus, Treecko, Torchic en Mudkip. Vergroot en op 1×, telkens in kleur en als silhouet.
- `varianttest.png`: een snelle proef met drie paletten (normaal, donker met blauw, albino met goud).
- `bron/`: de bronbestanden. `sh bron/build.sh` bouwt alles opnieuw, byte-identiek gecontroleerd.

## Werkwijze
1. **Thumbnails** (`bron/thumbs.py`):
   - A: viervoeter in de dekking;
   - B: rechtop in bokshouding, met een jab;
   - C: een zittende wolbal met de handschoenen voor zich.

   **Gekozen: B.** A blijft in het zwart een schaap of hond met bollen eraan, en C is een klomp waarin de handschoenen opgaan. Bij B breken de jab-handschoen, de banaanoren met kwastjes en de bolhoedkuif de omtrek. Hij staat rechtop zoals Stufful en Makuhita, en dat wijst al naar de lama en de luchadora.
2. **Procedurele basis** (`bron/alpaca2.py` met de nieuwe `tools/concept/sprites/shapelib.py`):
   - vormen die als bol van linksboven worden belicht, met selout;
   - het wollijf is opgebouwd uit 15 met de hand geplaatste bolletjes, van onder naar boven getekend. Elk hoger bolletje heeft een lavendel boogje langs zijn onderrand. Dat geeft de schubben van Swablu/Altaria/Mareep en een geschulpte buitenrand.
3. **Handwerk** (`bron/alpaca2.seg`, via `tools/concept/sprites/segraster.py`): kop, kuif, oren, kwastjes, wenkbrauwen, ogen en mond pixel voor pixel, plus de aansluiting tussen kin en kraag. Frame 2 gebruikt dezelfde kop, 2 px naar voren en 1 px omlaag, met eigen oren, oogleden en mond.

Nieuwe hulpscripts (alleen toegevoegd, niets bestaands veranderd):
- `shapelib.py` (vormen en belichting);
- `segraster.py` (handraster per segment, met `_` = laten staan en `@ dx dy` voor een verschuiving);
- `ascii_sprite.py` (dump en laad tekstrasters);
- `zoomview.py` (vergroot met coördinaten).

## Ontwerp
- **Dier:** een alpaca. De lange banaanoren, de snoet en de wolvacht maken hem in het zwart een alpaca/lama, geen schaap.
- **Idee:** een kleine bokser. Zacht lijf, harde houding (Stufful/Makuhita-logica).
- **Type (Fighting):**
  - **rode wollen bokshandschoenen** (Clobbopus) met een **gouden polsband**;
  - **wollen V-wenkbrauwen** boven grote ogen met glans;
  - de **dekking**: jab vooruit, achterste handschoen bij de wang;
  - **wit + rood** als uniform.
- **Twist en silhouet:** de handschoenen en de **kuif als mini-bolhoedje** (ronde koepel met een rand die aan de uiteinden opkrult).
- **Vooruitwijzing:**
  - de bolhoedkuif is het zaadje van de bombín. In de donkere proefvariant zie je meteen een zwarte bolhoed;
  - de handschoenen worden de polswraps van de lama (kickboksen) en de luchadora;
  - de rode oorkwastjes worden haar linten en pompons.
- **Frame 2 (actiemoment):** een volle jab naar voren met de achterste handschoen teruggetrokken. Daarbij oren plat naar achteren met wapperende kwastjes, boze oogleden en een open mond (schreeuw). De voeten blijven op dezelfde rij.
- **Kleurendriehoek:** de alpaca is **licht** (warm wit met cacao en rood). Hij laat de donkere (olinguito) en de koele midden-tint (nachtaap) vrij.
- **Fluffier** (Jordi): de wol zit nu in de geschulpte buitenrand en in de schubboogjes, niet meer in ruis. De schaduw is een koel lavendel in plaats van beige, zodat de wol schoon wit leest.

## Paletindeling (voor de varianten, §5)
| index | onderdeel | kleur |
|---|---|---|
| 0 | transparant | #94cd9c |
| 1–4 | **wol** (lijf, kraag, bolhoedkuif, wenkbrauwen; basis = 2, 4 = selout/krullijn) | #fffff6 #f6eee6 #cdc5d5 #837b94 |
| 5–7 | **vacht** (gezicht, snoet, oren, arm, pootjes) | #de9c73 #b4734a #7b4129 |
| 8–10 | **rood**: handschoenen + oorkwastjes | #ff7b6a #e63939 #9c1831 |
| 11–12 | **goud**: polsbanden | #f6c541 #ac7b29 |
| 13 | mond binnenkant | #d54a5a |
| 14 | wit (oogglans, tandje) | #ffffff |
| 15 | omlijning, pupillen | #101010 |

(De waarden zijn afgerond op 15-bit GBA-kleuren. Het wolhooglicht (1) en het glanswit (14) zijn aparte indexen, dus een variant kan ze los kleuren.)

Recept: `{'wol': [1,2,3,4], 'vacht': [5,6,7], 'rood': [8,9,10], 'goud': [11,12], 'mond': [13]}`.

In `varianttest.png` blijven de lijnen staan, ook bij een zwarte wol en een albino-vacht. Let op: als de handschoenen goud worden, verdwijnt de polsband erin. Geef de band in zo'n variant een contrasterende kleur.

## check.py (`--stage 1`)
Geen FOUT. LET OP:
- *Geen back.png en geen icon.png:* die vielen buiten deze opdracht.
- *Rand zwart 0,594* (p90 0,578): bewust in-game-contrast aan de rechter- en onderkant (§0), net als in ronde 1.
- *Fase 1 is groot (h 54, oppervlak 1384):* de oorkwastjes en de bolhoedkuif staan bovenop de kop. Hij valt wel binnen p10..p90 (30..58 / 527..1674), maar ligt ruim boven de mediaan (40 / 912). Zie hieronder.

OK:
- breedte 46 en 15 kleuren;
- licht links −0,39;
- schaduw 40 %;
- dithering 3,7 %;
- 10 losse pixels;
- binnenlijnen zwart 6,9 %;
- verschil tussen frame 1 en 2: 0,49.

species_info: `.frontPicSize = MON_COORDS_SIZE(56, 56)`, `.frontPicYOffset = 3`.

## Checklist Pokémon-design
- [x] **Dier × idee × type:** alpaca (oren, snoet, wol) × bokser (handschoenen, dekking, jab) × Fighting (rood, frons, houding). Nog te toetsen bij iemand die de tekst niet kent.
- [x] **Type met ≥ 3 middelen:** kleur (rood accent op wit), onderdeel (handschoenen + polsband), gezicht (V-wenkbrauwen) en houding (dekking/jab).
- [x] **Basisvorm:** een wolwolk (peer) met een grote kop erop. Geen gewrichten of knieën; de pootjes zijn stompjes.
- [~] **Precies één iconisch kenmerk:** de handschoenen. De bolhoedkuif is een tweede, kleiner kenmerk. Bewust, als zaadje voor fase 3, maar het is er strikt genomen meer dan één.
- [x] **Silhouettest** (`compare.png`): rechtop, banaanoren met bolletjes, een bal vooruit. Hij is niet te verwarren met Wooloo/Mareep of een schaap. Wel een licht konijn/hert-gevoel door de oren; de snoet en de wolrand houden hem alpaca.
- [x] **Kleur:** wit (wol) + cacao (vacht) + rood accent, plus een klein goudaccent. Er is helderheidscontrast tussen de kop en het lijf.
- [x] **Gezicht:** grote ogen met glans, wollen V-wenkbrauwen, en frame 2 als karaktermoment (schreeuw + jab).
- [x] **Vooruitwijzing:** de bolhoedkuif (bombín), de handschoenen (wraps) en de kwastjes (linten). Het vaste kenmerk van de lijn: rode handschoenen/wraps aan de voorpoten.
- [x] **Starters:** naast Treecko/Torchic/Mudkip en de Fighting-soorten valt hij niet weg; hij is de enige lichte, witte figuur met een felrood accent.
- [x] **Zelfde dier bekeken:** Wooloo en Mareep halen hun pluis uit een geschulpte rand. Die techniek is overgenomen, maar met rechtop staan, handschoenen en een gezicht met een frons.
- [x] **Gespriet, niet geïllustreerd:** egale vlakken met een ramp van 3–4 tinten, schubboogjes in plaats van ruis, en 1 px omlijning met selout.

## Wat ik zelf nog niet goed vind
- **Te groot voor fase 1** (54 hoog). Als Jordi hem kleiner wil: de kwastjes direct op de oortop zetten en de kop 2 px in de kraag laten zakken. Dat scheelt ±5 px.
- De **schubboogjes midden op de borst** zijn wat druk, vooral onder de kin (lavendel stipjes). De onderste rijen zijn goed, de bovenste kunnen rustiger.
- De **achterste handschoen** zweeft zonder arm (in frame 1 bij de wang, in frame 2 achter het lijf). Dat is gebruikelijk bij een ronde bokser (Clobbopus), maar hij oogt wat los.
- De **gouden polsband** is maar 2–3 px breed. Er is geen ruimte voor een echte aguayo-streep; het geweven detail valt op 1× weg.
- **Frame 2:** de mond is klein (4×3) en zit dicht op de rode handschoen, dus hij leest minder sterk dan ik wilde. De wapperende kwastjes lezen eerder als een lint.
- De **wenkbrauwen** lezen op 2× goed als een frons, maar zijn pixel voor pixel nog wat rommelig (lavendel randje).
- Nog te maken: back, icoon, shiny en de 6 varianten.
