# Nachtaap fase 2: kleursprite ronde 1

**Bestanden:**
- `nachtaap.png`: 64×64, geïndexeerd (mode P), palet van 16 kleuren, index 0 transparant, opgeslagen met transparency=0. Index 15 is een reserve (zwart, ongebruikt).
- `normal.pal`: JASC-palet, dezelfde volgorde als de PNG.
- `vel.png`, met:
  - de sprite op 4× op licht en op donker;
  - de onderlaag (3D-poppetje) op 4×;
  - fase 1 (goedgekeurd) op 4× en 1×;
  - de sprite op 1× (licht en donker) en op 3×;
  - Lairon, Sableye, Aipom, Grumpig en Mismagius op 3×, en alles op 1× op licht en op donker.
- In `bron/`:
  - `raster.txt`: het met de hand getypte raster, als `y x pixels`, één letter per kleur. Het is per onderdeel opgebouwd (lijf, kené, staart, arm, dij/voet, verre hand, nabije hand, kop, oren); latere regels overschrijven eerdere.
  - `bouw.py`: zet het raster om naar PNG en PAL, en controleert alpha-diff, open randen, losse pixels en het aantal kleuren.
  - `bouw_uitvoer.txt`: de uitvoer van die controle.
  - `alpha_bewijs.py`: een losse controle tegen `silhouet_bevroren.txt` en `.npy`.
  - `vel.py`: maakt `vel.png`.
  - `raster_grid.txt`: het eindraster als 64×64 tekst.

## Bevroren silhouet: alpha-bewijs
- `bouw.py`: **alpha-diff 0**, 1459 px (silhouet 1459 px). Er zijn 0 open randen.
- `alpha_bewijs.py`, onafhankelijk van het raster: het leest de PNG en vergelijkt index ≠ 0 met het silhouet. Uitkomst: **diff txt 0, diff npy 0**, 1459 px. De PNG is mode P, 64×64, met transparency 0.
- Er is dus niets verschoven of bijgetekend, ook niet 1 px.
- De verre ledematen (`o` in `verre_ledematen.txt`) zijn gekleurd in de schaduwtint en gescheiden met de omlijningsbasis:
  - verre hand (x 3–14, y 55–60): crème-schaduw `e`, met de crème-omlijning `t`;
  - het stukje bij x 23–25, y 57: de verre achtervoet, zichtbaar onder de elleboog. Ook `e`/`t`, met de selout `d` erboven als scheiding (geen zwart).

## Game Freak-studie (`anim_front.png` + `normal.pal`, bekeken op 6–10×)
| | tinten per kleurgroep | omlijning / selout | licht | ogen / patroon | wat ik overneem |
|---|---|---|---|---|---|
| **Lairon** (pose) | staal: f8f8f8, c0d0d8, 9898b0, 788090; lijf: a8a8a8, 888888, 686868, 404040 | zwart 101010 onder en tussen de platen; aan de lichtkant van de platen 404850/788090 | linksboven; de bovenkant van de platen is het lichtst | klein blauw oog (68b8f8) in een donkere kas; vlekken als vlakken met een eigen rand | kop laag vooraan en de romp erachter als bol die naar rechtsonder in de schaduw draait; de kop is een eigen onderdeel met een donkere lijn tegen het lijf |
| **Sableye** (donker violet) | 9088d0, 7060b0, 383078 + selout 181038 + zwart | selout donkerviolet 181038 aan de lichtkant, zwart onder en rechts | linksboven, met een duidelijk hooglicht op kop en schouder | grote ronde edelsteenogen: witte glans linksboven, lichte ring, donkere rand | een violet in 3 tinten met een violette selout (geen grijs); een rond oog met glans linksboven |
| **Mismagius** (donker violet, ogen) | violet b060b0, 805080, 584060, 302038 + zwart | zwart rond de schaduwkant, 302038 als selout | linksboven; grote schaduwvlakken | geel oog met een rode pupil in een donkere kas; de kas is de donkerste tint van de vacht, geen zwart vlak | een oog dat in een donkere kas zit, die overloopt in de vacht (onderrand in de selout) |
| **Aipom** (paarse aap) | violet b878d8, a058c0, 8040a8, 502068; crème f8e8a0, d8b070, b88860, 886840 | 502068 bovenop als selout, zwart onder; crème met een bruine omlijning 886840 | linksboven | crème gezicht en handen met een eigen bruine selout; staart als een cilinder met een lichte en een donkere kant | crème handen met een eigen bruinige omlijning (`t`); vingers gescheiden door de omlijningstint, niet door zwart |
| **Grumpig** (Psychic) | roze e0a0d8, d080c8, b860a8; zwart lijf 606060, 383838, 101010 | zwart, met grijs aan de lichtkant van de zwarte delen | linksboven | parels als kleine bollen: glans + basis + schaduw | de "parel" van het oog: glans linksboven, lichte reflectie rechtsonder |

**Samengevat:**
- 3 tinten per kleurgroep, plus een eigen donkere selout per groep (violet bij violet, bruin bij crème).
- Zwart alleen aan de schaduwkant: onder en rechts.
- Licht linksboven; de romp is een bol met de schaduw rechtsonder.
- Ogen hebben een glans linksboven, een lichtere iris tegenover de glans en een kas die overloopt in de vacht.
- Patronen (Zigzagoon-strepen, Lairon-vlekken) zijn kleurvlakken zonder zwarte rand, die meeschaduwen met de vorm.

## Palet (16, index 0 transparant)
| # | letter | kleur | gebruik |
|---|---|---|---|
| 0 | . | 98d0a0 | transparant (zoals Game Freak) |
| 1 | k | 1c1424 | omlijning aan de schaduwkant, pupil, bovenlid (zwart met een violette zweem) |
| 2 | d | 32224e | vacht-selout (lichtkant), onderrand van de oogkas, neus en mond, scheiding van de verre delen |
| 3 | s | 45306a | vacht schaduw; = verre kant van het poppetje |
| 4 | b | 5e4488 | vacht basis; = lijf van het poppetje (donkerder dan fase 1: 764cac) |
| 5 | l | 8268b4 | vacht licht; ook het snoetje |
| 6 | m | 9e8acc | lila midden: kené in de schaduw, snoet-hooglicht, maanrand in de schaduw |
| 7 | n | cec2ec | lila licht: kené in het licht, maan schaduw |
| 8 | w | f8f8f8 | maan, glans in het oog |
| 9 | r | 7a1430 | iris donker (bovenkant) |
| 10 | i | c8243c | iris (karmijn) |
| 11 | j | f06a70 | iris licht (reflectie onder) |
| 12 | c | f0e0c4 | crème licht: handen, voeten, binnenkant van het oor |
| 13 | e | d0b696 | crème schaduw, verre hand en verre voet |
| 14 | t | 92725c | crème-omlijning (selout van handen en voeten, vingerlijnen) |
| 15 | – | 000000 | reserve, ongebruikt |

**Luma per stap van de vacht:** 24 / 44 / 61 / 83 / 120. Dat zijn gelijkmatige stappen. De basis zit onder fase 1 (99), zoals Jordi wilde ("iets donkerder").

**Zwart-aandeel:** 180 van 1459 px (0,12). Dat is laag, omdat de bovenrand overal de violette selout heeft. Op donker blijft de omtrek leesbaar door de lichtere vacht.

## Opbouw per onderdeel
- **Lijf:**
  - een grote bol met de selout `d` langs de hele boven- en linkerrand en zwart rechts en onder;
  - een groot hooglicht `l` linksboven dat de ronding volgt (grens 27, 28, 28, 28, 27, 26, 25, 23, 21, 19);
  - een schaduwband rechts die met de bol van het achterlijf meebuigt (x 42 → 44 → 42 → 31, van boven naar onder);
  - de buik onderaan in de schaduw.
- **Kené:** in de vachtkleur getekend, zonder zwarte rand:
  - een ruggengraatlijn ±2 px binnen de bovenrand (van achter de kop tot de staartbasis);
  - daaraan drie getrapte dwarsbanden (stappen van 2 px recht omlaag en 2 px opzij, zoals Shipibo-lijnen);
  - in het licht in `n`, verderop in `m`, op het achterlijf in `l`; de banden worden naar achteren korter en donkerder;
  - geen wit, dus rustiger dan de maan.
- **Staart:**
  - een cilinder: links de selout en het licht, rechts de schaduw en zwart;
  - de spiraal heeft een buitenring van 3 px en een binnenkrul met een rond kopje (x 53–56, y 12–13);
  - de dunne stukken van 2 px zijn alleen omlijning (`dk`), zoals de pseudo-omlijning in de gids.
- **Kop:**
  - een eigen bol met een `d`-lijn bovenop tegen het lijf, en zwart rechts tegen de rug;
  - een slagschaduw `s` van 1–2 px op het lijf rechts van de kop.
- **Maan:**
  - de enige witte vlak op de kop, zoals in de onderlaag: ronde bovenkant (6 → 10 → 14 → 16 px breed);
  - de punten wijzen omlaag langs de buitenkant van beide ogen (tot y 46); de ogen vallen over de onderrand van de maan;
  - het violette middenstuk bolt in tot y 41;
  - wit linksboven, lila `n` en `m` aan de rechterkant (de schaduwkant van de kop).
  - Er is verder geen bleek vlak op de kop.
- **Ogen:**
  - groot en rond, zoals fase 1: het verre oog 6 × 7 px, het nabije 7 × 7 px (verre kant iets smaller, geen kopie);
  - een zwart bovenlid en zwarte zijkanten in de maan; de onderkant van de kas in `d`, zodat het oog overloopt in de vacht;
  - de iris is karmijn: donker `r` boven, `i` in het midden, licht `j` onder;
  - een witte glans van 3 px linksboven;
  - een ronde pupil van 2 × 2 px in het midden, met iris eromheen: hij kijkt recht in de camera en staart;
  - geen zware irisrij onder het lid, dus niet slaperig;
  - het lid is recht, niet schuin, dus niet boos.
- **Snoet, neus en mond:**
  - het snoetje is iets lichter violet (`l` met `m` linksboven);
  - de neus is 2 px `d`;
  - de mond is een korte rechte lijn van 3 px `d` (neutraal).
- **Oren:**
  - nabij (rechts): 4 × 6 px met crème `c`/`e` en een zwarte rand aan de schaduwkant;
  - ver (links): een klein crème bolletje achter de kopomtrek.
- **Nabije arm:**
  - de schouder is een bolling rechts van de kop, met licht linksboven en een rand die bolt (x 31–32);
  - de elleboog zit onder de kin; de onderarm loopt naar de hand;
  - de onderkant van de arm is een `d`-lijn boven de verre voet.
- **Handen en voeten:**
  - crème met de selout `t` en zwart aan de onderkant (dichtbij);
  - de vingers zijn gescheiden met `t`: nabije hand 3 vingers, verre hand 2 vingertoppen plus een knokkellijn;
  - de achtervoet heeft één teenlijn;
  - de dij is een eigen bol met een `d`-lijn aan de voorkant.

## §0-checklist (SPRITING.md) en harde eisen (SPRITE_NORM.md)
1. **Diagonaal:** het lijf staat 40° en de kop 80° (bevroren); de kop draait meer naar de kijker dan het lijf. Het verre oog is smaller, het verre oor zit achter de kopomtrek. **ok**
2. **Ledematen geteld:**
   - nabije arm: schouder, elleboog, onderarm en hand;
   - verre hand: in de schaduwtint, links en hoger;
   - nabije achterpoot: dij en voet;
   - verre achtervoet: het stukje onder de elleboog (`o`);
   - twee oren, twee ogen, de staart.
   - Alles is verbonden, met omlijning tussen de delen. **ok**
3. **Geen rechte lijnen:** de omtrek is bevroren. Binnenin is de rechte verticale schaduwgrens (12 rijen op x 41) vervangen door een grens die de bol volgt. De lange diagonale armlijn uit de eerste opzet las als een riem en is vervangen door een bolle schouder. **ok**
4. **Ogen geïntegreerd:** bovenlid, iris donker boven en licht onder, glans en reflectie. De kas loopt onderaan over in `d`. Het verre oog is geen kopie: 1 px smaller, en de pupil zit anders. Volgens de onderlaag zijn de ogen kraaloog-rond, geen snuitdier, dus twee ogen. **ok**
5. **Leest op 1× als de soort:** naast fase 1, Aipom, Sableye en Lairon leest hij als een gehurkte violette aap met een wit maangezicht, rode starende ogen en een spiraalstaart. Herkenbaar dezelfde lijn als fase 1: violet, groot rood-roze oog, crème oortjes en handen, de spiraal. **ok**
6. **Formaat:** bevroren (1459 px, ≈ 1,54 × fase 1). **ok**
7. **Pose niet stijf:** bevroren (Lairon-pose; de handen staan op verschillende hoogte). **ok**

**Harde eisen 7–10:**
- Ogen: zie punt 4. **ok**
- Kenmerken leesbaar op 1×: de maan, de ogen, de spiraal en de kené (als lichte lijnen). Geen klodders. **ok**
- Omlijning per kleurgroep: violette selout bij de vacht, `t` bij crème, zwart alleen aan de schaduwkant. Licht van linksboven. **0 open randen** (gecontroleerd met een script). **ok**
- Geen Chernobyl:
  - het gezicht is compleet: maan, ogen, snoet, neus, mond en oren;
  - er zijn geen crème vlakken uit het niets: crème zit alleen op handen, voeten en in het oor, zoals in het poppetje en in fase 1;
  - geen borstvlak, geen gezichtsschijf. **ok**

**Losse pixels** (een kleur zonder een buur van dezelfde kleur): 19. Het zijn allemaal bewuste pixels:
- iriskleuren in de ooghoeken;
- de vinger- en teenlijnen;
- de staartkern van 1 px;
- het puntje van de maan;
- de hoekpixels van het oor.
Er is geen ruis in de vlakken.

**Afgekeurd (SPEC), niet herhaald:**
- geen borstvlak;
- geen bleke gezichtsschijf;
- geen twee kleine sikkels;
- geen maan op de flank;
- geen sterren of maanfasen;
- de staart is geen rechte lijn.

## Bekeken op 1× en 3× naast echte sprites
Zie `vel.png`. Op 1× en op donker blijven de maan en de rode ogen het eerste wat je ziet, en de spiraal leest. Op 3× zijn te zien:
- de bol van het lijf (hooglicht linksboven, schaduw rechtsonder);
- de schouder van de nabije arm;
- de kené als een rustig getrapt patroon.

Bij Sableye/Aipom vergeleken is de vacht donkerder, zoals gevraagd. Ze oogt niet plat, door het grote hooglichtvlak en de schaduwband.

## Eerlijk: wat ik heb gerepareerd en wat een keuze voor Jordi is
**Gerepareerd in deze ronde (uit mijn eigen keuring van de eerste opzet):**
- de diagonale armlijn die als riem las;
- de kaarsrechte schaduwgrens;
- de rechter maanpunt, die in het lila wegviel (nu wit → lila, symmetrisch met de linker);
- de verre hand, die als een plankje met streep las (nu vingertoppen met een knokkellijn);
- 3 open randen;
- een rechte hooglichtgrens op de rug.

**Smaakkeuzes voor Jordi (geen gebrek, wel af te stemmen):**
- **Kené-sterkte:** nu bewust rustig, lila zonder wit (Jordi: "rustiger dan de maan"). In het poppetje zijn de banden wit en dik. Wil hij ze sterker, dan is dat één letter per pixel (`m` → `n`).
- **Oogring:** de ring is helemaal donker, zoals in het poppetje. Dat geeft de starende blik. Een lichtere onderrand (`s` in plaats van `d`) maakt hem zachter.
- **Hoe ver de maanpunten omlaag gaan:** nu tot halverwege het oog, zoals in de onderlaag.

**Nog niet gedaan (buiten deze opdracht):** frame 2, de rugsprite, het icoon, de shiny en de data.

## Lessen
- **Verdeel de onderlaag eerst in kleurklassen per 4×4-blok (meerderheid) en zet ze naast de silhouetrijen.** Zo zie je per pixel waar maan, oog, snoet, oren en kené horen. Let erop dat een silhouet met omlijning ±1 px ruimer is dan de onderlaag: kenmerken iets naar buiten schuiven, niet de omtrek.
- **Een armrand als één lange 45°-lijn over het lijf leest als een riem.** Een bolle schouder naast de kop, een elleboog onder de kin en een korte onderarm naar de hand lezen wel als een arm, ook als het grootste deel achter de kop zit.
- **Een gekleurd oppervlak (maan) dat tegen de schaduwkant van de kop ligt, valt weg als je het alleen in de schaduwtinten zet.** Houd de punt van de maan in wit → lila, zodat beide punten even goed lezen.
- **Een lange dunne crème vorm met een omlijning rondom en een vlakke tint leest als een plankje.** Eén knokkellijn dwars en één inkeping bij de toppen maken er vingers van, zonder extra kleuren.
- **`bouw.py` niet via `| head` draaien:** dan breekt de pipe vóór het opslaan en blijft er een oude PNG staan. Schrijf de uitvoer naar een bestand.
- **Teken de vachtlaag als volle rijen** (selout + tinten + omlijning, met de lengte gecontroleerd tegen het silhouet) en zet daar de onderdelen overheen. Dan is alpha-diff 0 vanzelf, en elke telfout geeft meteen een melding met coördinaat.
