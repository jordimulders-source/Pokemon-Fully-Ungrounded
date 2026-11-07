# Kolibrie pre-evo – kleur ronde 8 (op r7b) (maker, 3 nov)

Jordi, letterlijk:
- "r7b is de beste, maar waarom hangt er opeens een blauw achtig puntje onderin het hoofd?"
- "de snavel is nog niet helemaal goed aan de binnenkant overigens"
- "dat vlekje ziet er niet uit"
- "het starly oog is prima, plus dat de kleur boven het oog nog verandert. Alleen misschien nog net iets hoger boven het oog doen? Of juist net iets lager, de plek van het oog is vooral goed in r7b"

Daarnaast de r7-keuring (`kleur_r7/KEURING.md`): r7b TERUG met B1 (draai leest niet), B2 (kaplijn als kader rond het oog), B3 (voorhoofdcurve).
Bevroren: het Starly-oog en zijn plek uit r7b.

## Bestanden
- **r8, kapgrens zoals r7b:** `rijen_r8.txt` → `raster.txt` → `kolibrie_pre.png`.
- **Varianten van de kapgrens** (verder identiek):
  - `rijen_r8_hoger.txt` → `raster_hoger.txt` → `kolibrie_pre_hoger.png`;
  - `rijen_r8_lager.txt` → `raster_lager.txt` → `kolibrie_pre_lager.png`.
- `maak.py` bouwt alle drie en bewijst de alpha-diff en het bevroren oog. `palet.py`, `normal.pal`, `controle.py`.
- `vergelijk_8x.png`: bek en kop van r7b en r8 (licht en donker) op 8× naast Pelipper (open bek), Wingull, Spearow, Taillow en foto 3 (gespiegeld).
- `kapgrens_8x.png`: de drie koppen op 8× naast elkaar (hoger | zoals r7b | lager), elk ook op 1× op licht en donker.
- `vel.png`: r7b, r8 en de twee varianten naast Taillow en Starly op 3× en 1×, licht en donker.

## 1. Keelvlekje weg
- Er zit geen blauwgroen meer in de sprite. De plek (21–22, y21–22) is gewone keel: `6`, naar de koplijn toe `5`.
- Paletplekken 8 en 9 zijn nu de mondbinnenkant: roze 8 (236,120,146) en donker 9 (150,40,84).

## 2. Snavel: draai (keuring B1) en binnenkant (Jordi), in één keer
**Plan**, naar foto 3 (brede gele rand langs beide helften, roze binnenin) en de echte bekken op 8× (Pelipper: gele snavel met donkere mondlijn en rode binnenkant; Taillow: een brede, korte snavel die ín het gezicht zit).

**Fout in r7b:**
- De snavel stak met zijn volle lengte uit de omtrek. De bovensnavel was 7 px en steil.
- Het oranje stond aan de bovenkant van de bovensnavel in plaats van aan de gaapkant.

**Nu** (alleen x 9–18, y 11–21):
| deel | r8 |
|---|---|
| bovensnavel | 5 px, bijna horizontaal (tip 10,14), zoals Taillow. Bovenrand `1` (11–14,13), vulling `F` (11–14,14), aan de gaapkant de gele rand `DDD CC` (11–15,15). De basis is omlijnd met `1` (15,14) en (16,15) en zit in het gezicht |
| keelopening | wig die naar de mondhoek smaller wordt: donker `9` aan de open kant (14,16) (13–14,17) (13,18), roze `8` erachter (15,16) (15,17) (14–15,18) |
| mondhoek | geel `C`, (16,16–18) |
| ondersnavel | 4 px. Gele bovenrand `DD CCC` (12–16,19), vulling `F` (12–15,20), onderrand `1` (11–16,21) |
| voorhoofd en wang | lopen boven en onder de snavel door tot aan de bekbasis. Het gezicht is één licht vlak van snavel tot oog |

**Afwijking van het keurdersvoorstel:** ik heb geen aparte "verre wang" als kolom links van de mond gemaakt (x12–14, y14–20). Dat heb ik geprobeerd: een gele rand aan de verre kant, die de mond aan alle kanten insloot. Op 8× en 1× las dat als een vierkant doosje/ring in plaats van een snavel. De draai zit nu in de korte, vlakke snavel die ín het gezicht begint (zoals Taillow) en in de mond die je in perspectief ziet.

**Omtrek t.o.v. r7b:** 14 px gewijzigd, allemaal in x 9–18, y 11–21:
- (18,11) weg: B3;
- (16,12) weg: voorhoofdcurve;
- de oude lange snaveltip (9–10,12) (10,13) (10,21) weg;
- het verloop van de korte snavel, de keelopening en de onderrand: (13–14,13) (10,14) (11,15) (13,16–18) (12,19).

Lijf en oog zijn gelijk.

## 3. Kapgrens als kleurgrens (keuring B2), drie standen
- **Geen donkere kaplijn meer:** de koepel `2` rond het oog is weg. Kap `B`/`E` en gezicht `4`/`5` worden alleen door kleur gescheiden, zoals bij Taillow. Boven het oog doet het zwarte ooglid het werk.
- Achter het oog naar de nek is de oude lijn `E` (kapschaduw) geworden.
- Het voorhoofd is selout `2` waar het aan de lucht grenst.

| stand | wat verandert (alleen y13–15) |
|---|---|
| **zoals r7b** (`kolibrie_pre.png`) | kap tot en met y13 boven het oog; links van het oog vanaf y14 gezicht `4`/`5`, rechts kap tot (25–26,14) |
| **hoger** (`_hoger`) | 1 px hoger: y13 boven en naast het oog al gezicht (`44 55555 44`), rechts (25–26,14) gezicht `44` |
| **lager** (`_lager`) | 1 px lager: kap tot op het ooglid, ook (16–21,14) en (17–18,15) en (26–28,15) kap |

**Oog bevroren:** de 21 oogpixels (x21–25, y14–18, zonder de vier hoekjes) zijn in alle drie **0 px** anders dan r7b (`maak.py`). Het oog staat op x22–24, zoals de keurder vroeg.

## 4. Voorhoofdcurve (keuring B3)
(18,11) en (16,12) zijn weg en het voorhoofd loopt nu 23-21-19-17-15 (stappen van 2). Waar de lucht grenst is (17–18,12) en (15–16,13) selout `2`.

## Checks
- **Alpha-diff tegen r7b:** 14 (zie 2); kleurdiff tegen r7b: 57.
- **Open randen** (`controle.py`, streng):
  - (14,16), (13,17) en (13,18) `9`: de donkere keelopening, die zelf de rand van de open mond vormt (dun deel, zoals `D` bij de gaap). Bewuste uitzondering.
  - (25,43) `F`: de teen, door de keurder toegestaan.
- **Losse pixels:** alleen bewust (selout-hoekjes van het voorhoofd, onderkant van het oog, mondhoek `D` onderaan, veerrand, teentje).
- 734 px; aandeel zeer donker 0,188.
- **Zelf bekeken** op 8× (r7b naast r8), op 3× en op 1× naast Taillow en Starly, licht en donker:
  - De korte, platte snavel zit nu in het gezicht en de kop draait daardoor meer naar de kijker dan in r7b.
  - De open bek leest als twee snavelhelften met een gele rand en een roze keel.
  - Zonder de donkere koepel staat het oog vrij in het gezicht en leest het niet meer als bril.

## Wat nog niet klopt
Ik zie geen open punten. Welke kapgrens het wordt, kiest Jordi.

## Lessen
- Bij een snavel die schuin omhoog-links wijst, is de rechterpixel van elke rij de bovenrand en de linker de gaapkant. Mondkleur hoort aan de gaapkant.
- Een mond die aan alle kanten met geel omrand is, leest als doosje. Een open bek blijft open aan de voorkant: geel langs beide helften en donker in de opening.
- 3/4 bij een vogelkop komt van een korte, brede snavel die ín het gezicht begint (Taillow), niet van een snavel die lager zit.
- Een kleurgrens tussen kap en gezicht leest rond; een donkere lijn op dezelfde plek leest als bril.
