# Olinguito-lijn: ontwerpronde (zonder pixels)

Dark-starter: olinguito → coati → krabbenetende wasbeer (van kleine dief naar Robin Hood, lange klauwen in elke vorm; zie `POKEMON.md`).
Werkwijze volgens `sprites/KEURING_RONDE5.md` §3: eerst drie ontwerpen als modeltekening, Jordi kiest er één, en dat ontwerp ligt daarna vast voor de pixelrondes.

Bestanden:
- `concept_A.png`, `concept_B.png`, `concept_C.png`: fase 1 als modeltekening (256×256, vlakke kleuren, donkere omlijning, 3/4-pose naar links) met een ruwe silhouetschets van fase 2 en 3 ernaast.
- `vergelijking.png`: de drie concepten naast Totodile, Cyndaquil, Teddiursa, Zigzagoon, Sneasel en Poochyena (Gen 3, 3×), met per soort 1× in kleur, 1× silhouet en 2× silhouet. Voor de 1×-weergave is elk concept verkleind tot een oppervlak van ±900 px (Gen 3-starters gemiddeld 808).
- `scripts/`: `lib.py` (vormen: ellips, Catmull-Rom-blob, bezier, klauw, buis; omlijning per vorm), `concepts.py` (de tekeningen), `sheets.py` (de vellen). Draaien vanuit de repo-root: `python3 docs/concept/ontwerp/olinguito/scripts/sheets.py`.

Voor alle drie geldt hetzelfde (dat zijn de lessen uit de keuring):
- **Geen spullen:** geen sjaal, munt, armband of bril. Het masker is één vachtband over de ogen (Zigzagoon), zonder ring om elk oog.
- **De kop van een teddybeer:** rond, met ronde oren en een korte snuit. De kop is ±45% van de hoogte en het lijf is klein (Teddiursa, Cyndaquil).
- **Palet van 4 hoofdkleuren:** oranjebruin (de echte olinguito), crème (snuit, buik, klauwen), chocoladebruin (masker, sokken, staartringen) en goudgeel (alleen de ogen, het enige accent dat gloeit). Het palet is licht en verzadigd. Het donker zit alleen in de tekening van de vacht.
- **Dark zit in de lichaamstaal:** halfdichte of zijdelingse ogen, een scheve grijns met een hoektand en een pose die iets verbergt.

## A: Klauwdief
- **Idee:** een ronde teddybeer met één lichaamsdeel dat te groot is: drie lange, gebogen, crèmekleurige klauwen aan elke voorpoot. Hij staat half rechtop. Eén hand houdt hij met de klauwen omhoog naast zijn kop, de andere hangt omlaag.
- **Waarom het Pokémon leest:** hetzelfde principe als Makuhita's handen en Sneasels klauwen: het kenmerk ís anatomie en bepaalt het silhouet. Verder is het lijf simpel (peer + bol + buis). Het is de directe uitwerking van Jordi's eis 'langere klauwen'.
- **Dark:** de klauwen zelf, de sluwe halfdichte ogen in het masker en de grijns met de hoektand.
- **Evolutie:** de coati houdt een klauwpoot vooruit en zijn staart rechtop. De wasbeer staat rechtop: de klauwen van één hand wijzen vooruit als dolken, die van de andere hand omlaag. De Robin Hood zit in de houding en de klauwen, niet in kleding.

## B: Haakstaart
- **Idee:** hij zit braaf rechtop met de klauwen voor zijn buik gevouwen en kijkt opzij. Achter zijn rug staat de geringde coati-staart rechtop, en die eindigt in een haak met een donkere weerhaak die dingen weggrist.
- **Waarom het Pokémon leest:** het vraagteken-silhouet is ook op 1× het duidelijkst van de drie (zie `vergelijking.png`). Het verhaal komt uit de lichaamstaal: de voorkant is onschuldig, de achterkant steelt (show, don't tell, zoals Purrloin).
- **Dark:** het contrast tussen braaf en grijpend, het masker, de zijdelingse blik en de weerhaak.
- **Zwak punt:** een staart als silhouet ligt dicht bij Sentret en Aipom. De klauwen zijn hier tweede kenmerk, en Jordi wilde juist de klauwen.
- **Evolutie:** de coati heeft een staart als herdersstaf. Bij de wasbeer loopt de staart als een boog over de schouder.

## C: Borstelrug
- **Idee:** hij sluipt laag op vier poten. Masker, oren en een getande manenvacht vormen samen één donkere tekening die van de kruin over de nek tot de rug loopt (tweekleurig, zoals Poochyena). In de eindvorm groeit die vacht uit tot een kap met een punt en een mantel met een getande zoom: Robin Hood uit het eigen lijf (facet 8 van `SPRITE_PLAN.md`).
- **Waarom het Pokémon leest:** het is een tweekleurige vachttekening met een getande rand en het silhouet is de borstelige rug. Het leest als een dier, niet als een dier met kostuum. De manen hebben bewust dezelfde kleur als het masker en de sokken (een aparte paarse tint leek op een pruik en is eruit gehaald).
- **Dark:** de donkere zadelvacht, de sluippose en de smalle ogen.
- **Zwak punt:** op 1× lijkt het silhouet op Zigzagoon en Cyndaquil (borstelige rug), en ook Zigzagoon is een wasbeerachtige met een masker. Het risico is dat het een 'Zigzagoon-variant' wordt. De klauwen zijn klein.

## Eigen keuring (criteria uit KEURING_RONDE5)
| | A Klauwdief | B Haakstaart | C Borstelrug |
|---|---|---|---|
| type uit anatomie, geen spullen | ja (klauwen) | ja (staart + houding) | ja (vachttekening) |
| één kenmerk dat het silhouet maakt | klauwhand | vraagteken-staart | getande rug |
| leesbaar op 1× | redelijk: de klauwen worden 2–3 punten | best | goed, maar Zigzagoon-achtig |
| babyverhoudingen | ja | ja | ja (kop iets kleiner door de lange romp) |
| eigen gezicht t.o.v. Gen 3 | Teddiursa + Zigzagoon-masker | idem | te dicht bij Zigzagoon |
| Jordi's eis 'lange klauwen' | kern | bijzaak | bijzaak |
| leest als 'dier met kostuum' | nee | nee | nee (na het weghalen van de paarse kap) |

Tijdens het tekenen afgekeurd en vervangen: een eerste C met een paarse 'kap' over kop en nek en een lange punt naar achteren. Die las als pruik of capuchon, dus als kleding. Hij is vervangen door manen in dezelfde donkere vachtkleur als het masker.

## Voorkeur: A (Klauwdief)
- Het is het enige concept waarin het vaste kenmerk van de hele lijn (lange klauwen) ook het kenmerk van het silhouet is. Daardoor groeit de lijn vanzelf: kleine dief → coati die graaft en klimt → wasbeer met klauwen als dolken. Er is geen extra element nodig dat later moet verdwijnen.
- Het silhouet ligt het verst van bestaande Gen 3-soorten af (C lijkt op Zigzagoon, B op Sentret).
- Het risico zit op 1×: de klauwen moeten groot genoeg blijven (in de pixelronde 3 klauwen van ±8–10 px met crème + één schaduwtint, niet als dunne waaier; zie de klacht 'nagels te los' in `FEEDBACK.md`). Daarom hebben de klauwen in deze tekening een brede voet die in de poot overloopt.
- Optioneel: de rechtopstaande coati-staart uit B kan in fase 2 terugkomen als houding (coati's lopen echt zo), zonder dat het een tweede ontwerpkenmerk wordt.

Na Jordi's keuze: het gekozen concept is de modeltekening. De pixelronde gebruikt Teddiursa (kop) + Zigzagoon (lijf, masker) als skelet en neemt de rampopbouw over uit hun `normal_gba.pal` (KEURING_RONDE5 §3).

## Hele lijn
`lijn.png` (script `scripts/lijn.py`): ruwe modeltekening van fase 1–3 voor concept B (coati met herdersstaf-staart, Robin Hood-wasbeer met de staart als boog over de schouder). Nog niet goedgekeurd. De eerste pixelronde van fase 1 staat in `docs/concept/sprites/olinguito/ronde6/`.
