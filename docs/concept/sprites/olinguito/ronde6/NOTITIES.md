# Olinguito ronde 6: Gen 3-frontsprite van fase 1 (concept B, Haakstaart)

Eerste pixelronde volgens de nieuwe werkwijze (`../../KEURING_RONDE5.md` §3) op het goedgekeurde ontwerp `docs/concept/ontwerp/olinguito/concept_B.png`.

## Bestanden
- `anim_front.png`: 64×128, 4bpp geïndexeerd, 16 kleuren, index 0 transparant. Frame 1 boven, frame 2 onder.
- `normal.pal`: JASC-palet (16 kleuren).
- `compare.png`: modeltekening naast frame 1 en 2 en zes echte Gen 3-sprites (Teddiursa, Sentret, Zigzagoon, Aipom, Cyndaquil, Totodile), op 3× en 1×.
- `blindtest.png`: de rij van de laatste blinde test (nr. 8 is de olinguito). `blindtest_ronde1.png` en `blindtest_ronde2.png`: de rijen van de eerdere rondes (nr. 3 en nr. 10).
- `bron/pixels.py`: de sprite als handgeschreven pixelregels per onderdeel (staart, haak, lijf, voeten, kop, accentpixels). `bron/render.py` zet ze om naar de png en bevat het palet. Opnieuw maken vanuit de repo-root: `python3 docs/concept/sprites/olinguito/ronde6/bron/render.py docs/concept/sprites/olinguito/ronde6/bron/pixels.py uit.png`. De uitkomst is byte-gelijk aan `anim_front.png`.

## Werkwijze
- **Skelet: Teddiursa** (`graphics/pokemon/teddiursa/anim_front_gba.png`). Daarvan komen de zithouding, de ronde kop van ±22×21 px, de kop/lijf-verhouding (kop ±45% van de hoogte) en het formaat van ogen en snuit. Zigzagoon is het voorbeeld voor het masker als één vachtband over de ogen.
- **Palet:** de rampopbouw komt uit Teddiursa's `normal_gba.pal`. Dat is een vachtramp van 5 stappen, een lichte crèmeramp van 3 stappen en een donkere omlijning. Alleen de tint is gedraaid, naar een licht oranjebruin.

  | index | kleur | onderdeel |
  |---|---|---|
  | 1 | glans | vacht |
  | 2 | licht | vacht |
  | 3 | basis | vacht |
  | 4 | schaduw | vacht |
  | 5 | diep | vacht, ook omlijning aan de lichtkant |
  | 6, 7, 8 | licht, basis, schaduw | crème (snuit, buik, klauwen, binnenoor) |
  | 9, A | chocolade en donker | masker, sokken, staartringen, weerhaak |
  | B, C | goud en goud donker | ogen |
  | D | wit | glans en hoektand |
  | E | klauwschaduw | klauwen |
  | F | omlijning donker | omlijning aan de schaduwkant |

  Elk onderdeel heeft zo zijn eigen indexen, ook voor latere kleurvarianten.
- **Met de hand:** elke pixel staat als regel in `bron/pixels.py`. Er is geen automatische schaduw, omlijning of vorm. Het script plakt alleen de regels op elkaar en schuift het geheel naar het midden van het vak.
- **Pose:** de olinguito zit in driekwart naar links. De kop is iets gekanteld: het dichtbije oor staat lager en het masker loopt schuin. De kop steekt 2 px voor het lijf uit, zodat de houding een S vormt van kop via lijf naar staart. De ogen kijken opzij, naar de staart. De voorpoten liggen gevouwen voor de borst, met de klauwen omlaag. De staart staat rechtop achter de rug, eindigt in een haak met een donkere weerhaak en wordt naar de basis toe dikker.
- **Frame 2:** de haak zwaait open, klaar om te grissen. De rest van de sprite blijft stil.

## Metingen (frame 1, `keuring_ronde5/scripts/metrics.py`)
| | olinguito r6 | Gen 3 (Teddiursa / Sentret / Cyndaquil / Skitty) |
|---|---|---|
| oppervlak | **1106** | 652 / 941 / 819 / 934 |
| donkere buitenrand | 0,61 | 0,37 / 0,60 / 0,13 / 0,38 |
| detail (kleurwissels per px) | 1,88 | 1,86 / 1,53 / 1,59 / 1,83 |
| losse accentpixels per px | 0,11 | 0,17 / 0,13 / 0,10 / 0,21 |
| verzadiging | 0,67 | 0,56 / 0,52 / 0,71 / 0,51 |

Het oppervlak ligt boven het doel van 800–950. Ongeveer 230 px daarvan is de staart met de haak, die voor het ontwerp nodig is. Kleiner kan alleen met een kleinere kop of een kortere staart. Dat is een keuze voor de volgende ronde.

## Afwijkingen van de modeltekening
- **Klauwen:** in de modeltekening wijzen de klauwen omhoog, als een waaier voor de buik. Dat is twee keer geprobeerd. Op 1× lazen de donkere poten met witte punten als een tweede gezicht of als een mond met tanden op de buik. Daarom liggen de poten nu gevouwen voor de borst en hangen de klauwen omlaag. Gevouwen zijn ze nog steeds, maar ze zijn kleiner dan in de tekening. Dit kan Jordi beter beoordelen.
- **Staart:** de staart is dunner dan in de tekening (3–4 px vacht). Met de dikte uit de tekening wordt de sprite nog groter.
- **Ogen:** de ogen zijn kleiner dan in de tekening (2×2 goud met pupil en glans). Dat is Gen 3-formaat, zoals bij Teddiursa.

## Blinde test
Er was geen Agent-tool beschikbaar. Daarom heeft elke ronde een **verse cloudsessie zonder context** (Claude Code Remote) het plaatje opgehaald uit een privé-artifact (https://claude.ai/artifact/W22TwCygXLwQyyhFKttvJD) en de vraag beantwoord: "13 GBA-frontsprites, twaalf officieel (RSE), één nep: welke en waarom?" De rij bestond steeds uit Treecko, Torchic, Mudkip, Zigzagoon, Aipom, Skitty, Teddiursa, Poochyena, Sentret, Whismur, Electrike, Cyndaquil + de olinguito, op een willekeurige plek, 2×.

- **Ronde 0 (ongeldig):** het plaatje als base64 in de opdracht kwam beschadigd aan, en de keurder zag maar de helft.
- **Ronde 1 (tussenversie, nr. 3): meteen aangewezen,** met 70% zekerheid binnen ±3 s. De redenen:
  - geen bekende RSE-soort, "mengsel van Sentret en wasbeer";
  - de omlijning is overal even dik en donker;
  - de schaduw ligt in nette, regelmatige banden;
  - de pose is stijf en frontaal.

  Aangepast: het outline-donker is lichter, de kop is opnieuw gearceerd met clusters en dithering in plaats van schuine banden, en de kop staat naar voren.
- **Ronde 2 (nr. 10): meteen aangewezen,** met 85% zekerheid binnen ±3 s. De redenen:
  - lijf stijf, bijna symmetrisch en blokvormig;
  - vlakke schaduw met weinig tussentinten;
  - geen selectieve omlijning;
  - pootjes klein en vaag;
  - staart met herhalende ringen.

  Aangepast:
  - het lijf is opnieuw getekend in driekwart: buik naar links, rug in de schaduw, een grote dichtbije dij linksonder en een verre poot half erachter;
  - de omlijning aan de lichtkant (bovenkant kop, oren, schouders) is lichter (selout);
  - er zijn extra tussentinten op de wangen.
- **Ronde 3 (eindversie, nr. 8): niet als eerste aangewezen.** De keurder koos de echte Sentret (nr. 12, 75%). De olinguito was tweede keus (15%), "lijkt op Sentret, maar verzadigder oranje, donker maskervlak, dunne losgetekende staart met gelijke streepjes". Op tekenstijl alleen vond hij ook Sentret het meest afwijkend.

**Eerlijke lezing:** in ronde 1 en 2 viel de sprite er binnen 3 seconden uit. In ronde 3 niet meer, maar hij stond nog wel op de shortlist. De keurder herkent alle RSE-soorten en weet dus dat een onbekende soort verdacht is. Ronde 3 laat vooral zien dat de stijl niet meer duidelijk afwijkt. Er is één keurder per ronde gebruikt, dus het blijft een indicatie.

## Eigen oordeel
- **Beter dan ronde 4/5:**
  - geen spullen meer;
  - een ronde teddybeerkop met het masker als vachtband in plaats van een bril;
  - een licht, warm palet;
  - de dief zit in de haakstaart en de zijdelingse blik.

  Op 1× leest hij als één dier met één duidelijk silhouet: ronde kop plus vraagteken-staart.
- **Zwak:**
  - de klauwen zijn klein, en dat is Jordi's kerneis. Hier wijkt het het meest af van de tekening;
  - het oppervlak (1106) is te groot;
  - de staart is nog vrij regelmatig: gelijke ringen en een rechte paal;
  - het masker is een egaal donker vlak;
  - frame 2 is subtiel; alleen de haak beweegt.
- **Volgende ronde:** één laag tegelijk. Eerst laat Jordi de klauwkeuze (omhoog zoals in de tekening, of gevouwen omlaag) en het formaat goedkeuren, daarna pas de afwerking: ringen met variatie en een dikkere voet, een masker met een lichte rand en minder verzadiging.

## Fase 2 en 3
`docs/concept/ontwerp/olinguito/lijn.png` (script `scripts/lijn.py`) is een ruwe modeltekening van de hele lijn in dezelfde stijl als concept B.
- **Fase 2, coati:** loopt op vier poten met de snuit omhoog. De staart staat rechtop als herdersstaf met dezelfde weerhaak, en hij heeft lange graafklauwen.
- **Fase 3, krabbenetende wasbeer:** staat rechtop. De staart loopt als gespannen boog over de schouder, en de haak is de pijlpunt. Hij heeft een puntige vachtkap uit de kruin en het masker als Robin Hood-masker. De klauwen zijn dolken. Er is geen kleding: alles is vacht.
- **Kleur:** per fase dieper, van oranjebruin via roodbruin naar warm donkerbruin.

Fase 2 en 3 zijn nog niet goedgekeurd.
