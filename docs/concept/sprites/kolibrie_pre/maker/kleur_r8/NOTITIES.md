# Kolibrie pre-evo – kleur ronde 8 (op r7b) (maker, 3 nov)

Jordi, letterlijk:
- "r7b is de beste, maar waarom hangt er opeens een blauw achtig puntje onderin het hoofd?"
- "de snavel is nog niet helemaal goed aan de binnenkant overigens"
- "dat vlekje ziet er niet uit"
- "het starly oog is prima, plus dat de kleur boven het oog nog verandert. Alleen misschien nog net iets hoger boven het oog doen? Of juist net iets lager, de plek van het oog is vooral goed in r7b"

De keuring van r7a/r7b volgt nog. Bevroren: het Starly-oog en de plek ervan (r7b).

## Bestanden
- **r8 (kapgrens zoals r7b):** `rijen_r8.txt` → `raster.txt` → `kolibrie_pre.png`.
- **Varianten van de kapgrens** (verder identiek):
  - `rijen_r8_hoger.txt` → `raster_hoger.txt` → `kolibrie_pre_hoger.png`;
  - `rijen_r8_lager.txt` → `raster_lager.txt` → `kolibrie_pre_lager.png`.
- `maak.py` bouwt alle drie en bewijst de alpha-diff en het bevroren oog. `palet.py`, `normal.pal`, `controle.py`.
- `vergelijk_8x.png`: bek r7b | r8 (licht en donker) naast Pelipper, Wingull, Spearow, Taillow en foto 3 (gespiegeld).
- `kapgrens_8x.png`: de drie koppen op 8× naast elkaar (hoger | zoals r7b | lager), plus elk op 1× op licht en donker.

## 1. Keelvlekje weg
- Er zit geen blauwgroen meer in de sprite. De plek (21–22, y21–22) is keel: `6` op y21, en `6 5` op y22 naar de schaduw onder de kop toe. Dezelfde opbouw als de rest van de keel: licht onder de bek, `5` naar de koplijn.
- Paletplekken 8 en 9 kwamen vrij en zijn nu de mondbinnenkant (zie 2).

## 2. Binnenkant van de snavel
**Plan**, naar foto 3 (brede gele mondrand langs beide helften, roze en donker binnenin) en de echte open bekken op 8× (Pelipper: gele snavel met donkere mondlijn en rode binnenkant; Spearow/Taillow: snavelhelften met eigen lichte vulling en donkere rand).

**Fout in r7/r7b:** het oranje D stond aan de **bovenkant** van de bovensnavel (de rechterpixel van elke rij is daar de bovenrand), niet aan de gaapkant. Dat las als losse kleurpixels.

**Nu:**
| deel | opbouw |
|---|---|
| bovensnavel (y12–16) | bovenrand `1`, vulling `F`, gaapkant de mondrand `D`, aan de basis `D C C` (13–15,16) |
| keelopening (y17–18) | donker `9` (150,40,84) achterin en aan de rand, roze `8` (236,120,146) ervoor: (13–14,17) `99`, (15,17) `8`; (13,18) `9`, (14–15,18) `88` |
| mondhoek | geel `C` (16,17) en (16,18) |
| ondersnavel (y19–21) | bovenrand geel `C` over de hele lengte (13–16,19) met `D` aan de punt, vulling `F` (12–14,20), mondhoek `D C`, onderrand `1` |

Zo lezen boven- en ondersnavel als twee helften, met daartussen een gele rand en een roze/donkere keel.

**Omtrek:** **3 px erbij** in de bekzone, elk 1 px naast de oude rand: (13,17) en (13,18) (keelopening 1 px verder naar voren) en (12,19) (ondersnavelrand). Verder gelijk aan r7b.

## 3. Kapgrens boven het oog: drie varianten
- **Zoals r7b (r8):** de koepellijn `2` ligt direct op het oog (y13).
- **Hoger:** de koepel 1 px hoger (top y12). Tussen kaplijn en oog komt een rij licht gezicht `5`, aan de zijkanten zakt de lijn mee (y13–15). Het kruinhooglicht wordt een rij korter.
- **Lager:** boven het oog geen lijn meer; de kap loopt door tot het ooglid, dat dan de grens is. Aan de zijkanten zakt de lijn 1 px (links y14–16, rechts y14).
- **Alleen rij 12–16 verschilt tussen de drie** (alleen de kapgrens).
- **Oog bevroren:** de 21 oogpixels (x21–25, y14–18, zonder de vier hoekjes) zijn in alle drie **0 px** anders dan r7b (`maak.py` meet dit).

## Diff en checks
- **r8 tegen r7b:** 24 px.
  - 20 in de snavel en mond;
  - 4 aan de keel (vlekje weg, keelschaduw).
- **Alpha-diff tegen r7b:** 3 (bewust, zie 2), voor alle drie de varianten.
- **Open randen** (`controle.py`, streng):
  - (13,17) en (13,18) `9`: de donkere keelopening, die zelf de rand van de mond vormt (dun deel, zoals `D` bij de gaap). Bewuste uitzondering.
  - (25,43) `F`: de teen, door de keurder toegestaan.
- **Losse pixels:** alleen bewust (onderkant van het oog, mondrand D aan de punt, veerrand, teentje). In "hoger" ook (19,12) `4`, het restje kruinlicht.
- 737 px; aandeel zeer donker 0,187.
- **Zelf bekeken** op 8× naast de echte bekken en foto 3, en op 1× op licht en donker (`kapgrens_8x.png`):
  - De open bek leest als twee snavelhelften met een gele rand en een roze keel, ook op donker.
  - Het blauwgroene puntje is weg.

## Wat nog niet klopt
Ik zie geen open punten. Welke kapgrens het wordt, kiest Jordi.

## Lessen
- Bij een snavel die schuin omhoog-links wijst, is de **rechter**pixel van elke rij de bovenrand en de **linker** de gaapkant. Mondkleur hoort links (gaapkant), anders lijkt het een losse kleurpixel bovenop.
- Een open bek in 3/4 leest door drie lagen: gele rand langs beide helften, een donkere keelopening en een lichte vulling van de snavelhelften zelf.
