# Coathief: kleursprite ronde 1

## Bestanden
- `coathief.png`: 64×64, mode P, 16-kleurenpalet (14 in gebruik), index 0 transparant, opgeslagen met transparency=0.
- `vel.png`: de sprite op 4× (licht en donker) en 1× (licht en donker), naast:
  - de onderlaag;
  - de olinguito (fase 1, goedgekeurd) op 4×, 2× en 1×;
  - Linoone, Furret, Mightyena, Houndour en Zigzagoon op 4× en 1×.
- `uitsnede.png`: kop met voorpoten en de staartkrul, op 8×.
- `bron/`:
  - `raster.txt`: met de hand getypt, `y x0 pixels`, per onderdeel.
  - `reparaties.txt`: handreparaties na de eerste blik, in hetzelfde formaat; ze overschrijven `raster.txt`.
  - `bouw.py`: letter naar paletindex, plus de controle tegen het silhouet. Het schrijft ook `raster_grid.txt`.
  - `controle.py`: alpha-diff, open randen per kleurgroep en losse pixels.
  - `vel.py`: maakt het vel en de uitsnede.
  - `zoom.py`: een 8×-weergave om zelf te kijken.
  - `klassen.py` / `klassen.txt`: de kleurvlakken van de onderlaag (4×4-meerderheid), afgebeeld op het 64-raster. Alleen als kaart gebruikt; er is niets uit gekopieerd.

Opnieuw bouwen: `python3 bron/bouw.py && python3 bron/controle.py && python3 bron/vel.py` (vanuit deze map of vanuit de repo, de paden zijn absoluut gemaakt).

## Alpha-bewijs (bevroren silhouet `silhouet/ronde1.txt`)
`controle.py` leest de PNG zelf terug en vergelijkt elke pixel (index ≠ 0) met `#`:
```
pixels 1297 | silhouet 1297 | alpha-diff 0
kleuren gebruikt: 14 | transparency = 0
open randen: 0 []
losse pixels (zonder buren): 0 []
```
`bouw.py` controleert daarnaast dat elke pixel precies één keer in `raster.txt` staat. Reparaties mogen alleen pixels binnen het silhouet overschrijven; anders meldt het script een fout.

## Game Freak-studie (anim_front_gba, eerste frame, op 6–10×)
| | tinten per groep | selout / zwart | licht | vorm volgen | donker vlak op de kop | oog |
|---|---|---|---|---|---|---|
| **Linoone** | vacht 4 + donkerbruin + zwart | zwart onder en rechts, donkerbruin aan de lichtkant | linksboven, de rug is het lichtst | strepen volgen de lijfboog | – | klein: zwarte rand, glans linksboven, lichter onderaan |
| **Furret** | crème 3 + bruin 3 (9c624a, 7b4139, 4a1818) | bruin als selout, zwart spaarzaam | linksboven | **banden volgen de ronding** (boogvormig, elke band met een licht en een schaduwkant) | – | kraaloog met glans |
| **Houndour** (zwart dier) | "zwart" = 524a4a basis, 393131 en 292020 schaduw, 8b7b7b hooglicht, 101010 omlijning | zwart rondom, maar binnen de lichtkant meteen de lichte grijstint | linksboven: lichte grijze randjes aan de bovenkant van kop en rug | – | **de zwarte kop is nooit egaal zwart**: warm donkergrijs met een licht randje linksboven en een donkerder onderkant | – |
| **Mightyena** | donker 4 (4a526a, 313141, 202029 + zwart) + grijs 3 | zwart aan de schaduwkant | linksboven | vacht in plukken aan de rand | donkere kop met een grijze snuit, volume via 2–3 donkere tinten | rood oog met zwart bovenlid |
| **Zigzagoon** | vacht 4 + zwart | bruin aan de lichtkant | linksboven | kartelgrens | masker donkergrijs met een donkerdere kern, niet zwart | klein bruin oog met witte stip, in het masker |

**Toegepast:**
- de bivakmuts is warm donkergrijs (z) met een lichte rand (y/Y) linksboven, schaduw (m) onder en achter, en zwart (k) alleen aan de onder- en achterkant;
- de staartringen volgen de krul en hebben elk een licht- en een schaduwkant (n/c/w en m/y/z);
- selout aan de lichtkant: d voor de vacht, m voor de donkere delen, n voor de lichte ringen;
- het mini-oog volgens de Corviknight-les: zwart bovenlid, glans linksboven en een lichtere iris tegenover de glans.

## Palet (16, index 0 transparant)
| # | letter | kleur | gebruik |
|---|---|---|---|
| 0 | . | 98d0a0 | transparant (zoals de olinguito) |
| 1 | k | 140c0a | omlijning, schaduwkant; neus |
| 2 | m | 2a201c | bivakmuts schaduw, selout van de donkere delen |
| 3 | z | 40352f | bivakmuts basis: kop, onderpoten, donkere staartringen |
| 4 | y | 5e5048 | bivakmuts licht |
| 5 | Y | 8a7a6c | bivakmuts hooglicht (randje linksboven, glans op de neus), 6 px |
| 6 | d | 5e3216 | vacht schaduw en selout |
| 7 | b | 8e5226 | vacht basis (warm roodbruin) |
| 8 | l | b87636 | vacht licht (goudbruin) |
| 9 | h | d8a058 | vacht hooglicht |
| 10 | n | a48660 | crème schaduw, selout van de lichte ringen, oorrand |
| 11 | c | dcc49a | crème basis: ringen, vlekken, klauwen |
| 12 | w | f6eedc | crème licht, glans in het oog |
| 13 | r | 6a1c14 | oog donker roodbruin (de olinguito-iris) |
| 14 | i | b04a2c | iris licht (onderkant) |
| 15 | x | 3a1e10 | reserve (ongebruikt) |

Per groep zijn er 3 tot 4 tinten plus omlijning. De donkere tinten worden gedeeld door de kop, de onderpoten en de donkere staartringen (één bivak-familie). Aandeel k: 161 van 1297 px (0,12). De gemiddelde helderheid is 79; dat is net als Mightyena (74) aan de donkere kant, wat past bij Dark en een zwarte kop.

## Wat waar zit (per onderdeel)
- **Kop (bivakmuts):**
  - lichte rand (y, Y) langs het voorhoofd en de neusbrug;
  - z als basis, m achter en onder de kaak;
  - k-omlijning onder;
  - de naad met de bruine hals is gebogen: hij bolt uit bij y 37–40, met een paar m-pixels als vachtplukje over de naad. Geen rechte balk.
- **Neus:** zwart (k) met één glanspixel Y.
- **Oog:** 3×3 op (18–20, 39–41):
  - bovenlid `kkk` met een m-staartje;
  - `w r r` / `r i i`: glans linksboven, en de iris donker boven en lichter onder, tegenover de glans.
- **Coati-vlekken:**
  - boven het oog: (18–20, 37–38), `wc`/`ccn`;
  - onder en achter het oog: (20–22, 43–45), `wc`/`ccn`/`n`.
  - Ze zijn met een donkere rij van het oog gescheiden (eerste versie: vlek-oog-vlek in één kolom las als een mondje met tanden).
- **Oren:** klein en rond, met een n-rand. Het nabije oor zit rechts (x 20–24), het verre is een stukje links (x 16–17).
- **Lijf:**
  - rug licht (l, h) met een hooglicht op de schouder;
  - een schouderbol met een gebogen d-contour;
  - de dijbol rechts met een hooglichtsikkel linksboven;
  - de buik en de verre dij in de schaduw (d), met een boogvormige bovenrand;
  - de rechterkant van het achterlijf d, de omlijning k.
- **Poten:** alle onderpoten in de bivak-tinten.
  - Nabije poten: y-licht links, k rechts.
  - Verre poten: m met een z-streep, gescheiden met k.
  - De verre voorpoot is vanaf y 50 donker (eerst een bruin blok).
- **Klauwen:**
  - nabije voorpoot: 2 lange crème haken van 5 rijen, met w links, c in het midden en n rechts en aan de punt;
  - verre voorpoot: 2 kleine crème klauwen op de grond.
- **Staart:**
  - 4,5 donkere ringen plus een donkere punt, die de krul volgen;
  - elke ring heeft een selout links (n of m), een lichtstreep (w of y), de basis, schaduw en k rechts;
  - de ringgrenzen verspringen 1 px (links eerder dan rechts) en volgen zo de kanteling van de staart, net als op de onderlaag;
  - aan de basis zit een donkere ring op het achterlijf (onderlaag).

## SPRITING §0, checklist
1. **Diagonaal 3/4:** bevroren silhouet (B1: lijf 42°, kop 52°). ok
2. **Ledematen en oren geteld en verbonden:**
   - 4 poten, elk in een eigen kolom met lucht of een k-scheiding;
   - 2 oren;
   - 1 oog, want de snuit is lang.
   - ok
3. **Geen rechte lijnen:**
   - de omtrek is bevroren;
   - binnenin zijn de naad van de muts, de schaduwgrens van de buik, de schouder- en de dijcontour gebogen of gekarteld;
   - de hooglichtrand op de neusbrug volgt de (diagonale) omtrek.
   - ok
4. **Oog geïntegreerd:** bovenlid, iris donker boven en licht onder, glans. Klein (3×3), zoals op foto 6–8. Geen platte rode stip. ok
5. **Leest op 1× als de soort:** zie het vel. Een coati: zwarte kop met lichte oogvlekken, geringde staart omhoog, donkere poten en lichte klauwen. ok
6. **Formaat:** 1297 px, binnen 1100–1550 (fase 2) en ±1,1× de olinguito (1174). Het silhouet is bevroren. ok
7. **Pose:** bevroren, met één opgetilde voorpoot. ok

## SPRITE_NORM, harde eisen
1. **Leest op 1× als een echte Pokémon:** naast Linoone, Furret, Mightyena, Houndour en Zigzagoon op 1× (licht en donker) leest hij als dezelfde soort sprite. ok
2. **3/4 links-voor, één oog, neus vooraan:** ok (silhouet bevroren). De zwarte neus is het meest linkse punt.
3. **Alle ledematen tellen op 1×:** 4 poten, de verre in de schaduwtint; de verre voorpoot is nu ook bovenaan donker, zodat hij als poot leest. ok
4. **Geen Escher:**
   - de nabije voorpoot ligt over de verre (k-scheiding op x 26, y 50–52);
   - de nabije achterpoot staat los van de verre (k op x 41–42).
   - ok
5. **Lijf:** het silhouet is bevroren. Het kleurwerk volgt bollen (schouder, dij, rug) in plaats van rechte banden. ok
6. **Kop:** bevroren silhouet. ok
7. **Ogen:** zie §0.4. ok
8. **Kenmerken op 1×:**
   - lange snuit met zwarte neus;
   - bivakmuts met vlekken;
   - geringde staart;
   - 2 lange klauwen aan de opgetilde poot;
   - kleine klauwen aan de verre poot.
   - ok
9. **Omlijning:**
   - per kleurgroep, k aan de schaduwkant;
   - licht linksboven;
   - `controle.py`: 0 open randen. De klauwpunten zijn 1–2 px dunne pseudo-omlijning: crème met n aan de schaduwkant, zonder k eromheen. Het silhouet laat geen ruimte voor een buitenrand.
   - ok
10. **Geen Chernobyl:**
    - de eerste versie had vlek-oog-vlek in één kolom, en dat las als een mond met tanden: gerepareerd;
    - geen crème vlakken uit het niets (oorrand, oogvlekken, ringen en klauwen zijn allemaal echte coati-kenmerken);
    - 0 losse pixels.
    - ok

## Jordi's punten
- Lange snuit en staart met patroon: ok, de ringen volgen de krul.
- Klauwen: ok, 2 lang en 2 klein.
- Bivakmuts C met lichte vlekken boven en onder het oog: ok. Het is geen gesloten kring.
- Neus zwart: ok.
- Oog kleiner, geen rode stip: 3×3 Pokémon-oog. ok
- *Nasua nasua*:
  - warm roodbruin lijf;
  - donkere onderpoten;
  - crème/donker geringde staart;
  - oren met een lichte rand.
  - ok
- Geen tas: ok.

## Zelf bekeken (1×, 2×, 4× en 8×, naast de olinguito en de Gen 3-sprites)
- **Dezelfde lijn als de olinguito:**
  - de olinguito-masker is uitgegroeid tot een bivakmuts;
  - hetzelfde donkere roodbruine oog;
  - dezelfde lichte klauwen;
  - dezelfde pixelstijl: selout, 3 tinten per groep, licht linksboven.
  - Coathief is groter, langer en brutaler (kop laag, klauw geheven).
- **Voor Jordi (smaak, geen fout):** het lijf is warmer en oranjer dan de doffe bruine olinguito. Dat volgt de SPEC (*Nasua nasua*, warm roodbruin) en de onderlaag. Wil Jordi de lijn nog dichter bij fase 1, dan kunnen b, l en h een tikje doffer. Dat zijn alleen paletwaarden; geen pixel verandert.
- **Op een donkere achtergrond** gaan de zwarte kop en de onderpoten meer op in de achtergrond, net als bij Houndour en Mightyena. De lichte randjes houden de vorm leesbaar.
- Ik heb geen open punten gevonden die ik als zwak zou noemen.

## Lessen
- **Vlek-oog-vlek in één kolom leest als een mond met tanden.** Zet de vlekken schuin (boven het oog, en onder het oog naar achteren) en laat een donkere rij tussen vlek en oog.
- **Een zwarte kop krijgt volume** met een lichtrandje (2 tinten) langs de lichtkant binnen een zwarte omlijning (Houndour), niet met een lichte vlek in het midden.
- **De naad tussen een donkere kop en een bruin lijf** moet uitbollen (de achterkant van de schedel) en geen 2 px donkere kolom krijgen: anders wordt het een helm.
- **Een tussengebied tussen twee poten in vachtkleur** (het bruine bovenstuk van de verre voorpoot) leest op 4× als een blok. Begin de donkere poot hoger.
- **Een reparatiebestand in hetzelfde formaat als het raster** (dat het raster overschrijft, met een controle binnen het silhouet) houdt de bron leesbaar en elke wijziging traceerbaar.
- **Klauwen van 2 px:** gebruik w/c/n zonder k ertussen. Met een k in de klauw zelf werden het losse spikkels.
