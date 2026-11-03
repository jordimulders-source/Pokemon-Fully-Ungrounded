# Kolibrie pre-evo – kleur ronde 6: belijning en oog als Gen 3 (maker, 3 nov)

Jordi over r5, letterlijk: "vind je dit echt af? Is dit wel gekeurd? Waar is de belijning voor de vorm van het hoofd. Het lijkt nu gewoon een tekening, maar geen sprite. Vergelijk het eens goed met de andere pokemon. Het oog is niet helemaal goed".
Aanvulling, letterlijk: "taillow heeft wel een modernere sprite gekregen, maar die is desalniettemin erg mooi, dus dien mag je best aanhouden. Hij mag voor deze vorm best wel een gedefinieerd oog hebben idd, die bij de kolibrie dan mysterieuzer wordt".
Maatstaf is dus Taillow (`graphics/pokemon/taillow`). Bevroren als ontwerp: kleurfamilie, onderdelen, de korte open bek en de keelveertjes. Basis is r5.

## Bestanden
- `rijen_r6.txt`: met de hand, één teken per paletindex.
- `raster.txt`, `kolibrie_pre.png`, `normal.pal`.
- `vergelijk_8x.png`: r5 | r6 | Taillow | Pidgey op 8×.
- `vel.png`: r5 en r6 op 8× met raster; r6 op 3× en 1× naast Taillow, Swablu, Wingull, Natu, Pidgey en Starly, licht en donker.
- Scripts: `bouw.py`, `palet.py`, `controle.py`, `vel.py`.

## Plan: welke lijnen Taillow en Pidgey hebben en r5 niet (8×)
| onderdeel | Taillow / Pidgey | r5 | r6 |
|---|---|---|---|
| buitenlijn | bijna-zwart rondom; alleen bovenop de kop een subtiele selout | donker violet, aan de lichtkant een lichtere 2: vaag | bijna-zwart violet `1` (20,14,30) rondom; selout `2` alleen op kruin en voorhoofd (y9–14) |
| vorm van de kop | Taillow: donkere lijn van achterhoofd/nek naar de keel; de kop is een eigen ronde vorm boven het lijf | geen; kop en lijf lopen in elkaar over | binnenlijn `2` van de nekknik (32,21) in een bolle boog naar de inkeping in de borst (19–22,25): stappen 1-2-3-5-4. Keel en keelveertjes zitten binnen de kop, de borst eronder |
| kap | Taillow: rood voorhoofd en blauwe kruin als vlakken met een harde grens | alleen tintverschil | kapnaad `2` van de snavelbasis schuin naar het oog (18–23, y14–16) en van achter het oog naar de nek (29–31, y18–20); gaat over in de koplijn |
| vleugel | helemaal omlijnd in zwart, met veerlijnen in een donkere tint | alleen een tint en de rugrand | voorrand en bovenkant in `1` (een gebogen schouder y24–25, dan de voorrand tot de punt). Twee veerlijnen `2` diagonaal naar de punt: (37,32)–(40,35) en (35,34)–(39,38). Lichte voorrand `4` alleen bij de schouder (y25–29). Schaduw E aan de rugkant |
| buik/borst | Taillow: witte buik met een eigen lijn tegen het lijf; Pidgey: borst tegen de vleugel met een donkere lijn | alleen tint | grens `2` (lichter dan de buitenlijn) van de vleugel (30,32) in een boog naar onderen tot (25,39). Erboven sluit de vleugellijn de borst af |
| oog | Taillow: donker omlijnd, met een duidelijke witte glans, staat scherp in het gezicht | een zachte donkere vlek met lila onderkant | 5×5 rond (hoekjes in kap- of gezichtskleur), zwart omlijnd met pupil `1`, witte glans van 3 px linksboven (25–26,15)+(25,16), kleine iris E (26,17) en een witte reflectie (27,17). Helder, open en vriendelijk, zoals Jordi wil; het mysterieuze kleine oog blijft voor de eindvorm |
| bek | Taillow/Pidgey: eigen vorm met donkere lijn, lichtere boventint, het geel omlijnd | bovensnavel deels zonder lijn | bovensnavel helemaal `1` omlijnd met een lichte boventint F (130,122,156). Ondersnavel en gaap: geel C, omlijnd met D naar de gaap en `1` aan de onderkant |
| contrast | licht, middel en donker duidelijk verschillend | buikschaduw 5 te dicht bij 6 | 5 donkerder (186,176,224); aandeel zeer donker 0,203 (was 0,137; Taillow en Natu ±0,27) |

## Diff tegen r5: 138 px
Vooral de nieuwe lijnen:
- buitenlijn van 2 naar 1 aan de linker- en onderkant;
- koplijn, kapnaad, vleugelomlijning en veerlijnen, buikgrens;
- oog en bek.

Daarnaast het palet:
- 1 donkerder;
- 5 donkerder;
- 7 wit (ook glans);
- F nu snavelboventint (de glans gebruikt 7).

## Omtrek tegen silhouet r2
- Gelijk aan r5: +3 px van r4, namelijk (17,12), (34,21), (35,22) voor curves.
- −1 px van de r5-keuring: (17,36).
- In r6 geen nieuwe omtrekwijziging (alpha-diff tegen r5: 0).

## Checks (`controle.py`, streng)
- Alpha-diff tegen silhouet r2: 4 (zie hierboven, allemaal uit eerdere goedgekeurde rondes); tegen r5: 0.
- **Open randen: 0** (naast transparant alleen 1, 2, A of D).
- Losse pixels alleen bewust:
  - glans en iris in het oog, ooghoekjes;
  - keelveertjes;
  - licht puntje op de nabije poot;
  - tenen.
- 734 px; aandeel zeer donker 0,203; 15 kleuren plus index 0.
- **Zelf bekeken op 8× naast Taillow en Pidgey en op 3× en 1×, op licht en donker:**
  - r6 valt er niet meer uit als tekening: elk onderdeel (kop met kap, oog, bek, keel, borst, vleugel, staart, pootjes) is een omlijnde vorm, zoals bij Taillow.
  - Het oog is helder en scherp.
  - Op 1× leest hij als een lila vogeltje met een open gele bedelbek.

## Wat nog niet klopt
Ik zie geen open punten.

## Lessen
- "Gen 3" is niet alleen een nette buitenlijn. Elk onderdeel heeft een eigen gesloten vorm met een binnenlijn (kop, kap, vleugel, buik). Zonder binnenlijnen blijft het een tekening, hoe schoon de vlakken ook zijn.
- De koplijn hoort van de nek naar de inkeping in de borst te lopen: die inkeping in het silhouet is precies waar kop en lijf samenkomen.
- Een helder Pokémon-oog = zwarte omlijning en pupil, een witte glans linksboven van 2–3 px en een kleine tweede reflectie rechtsonder. Een iris in een middentint maakt het zacht en vaag.
