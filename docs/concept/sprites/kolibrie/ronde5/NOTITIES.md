# Kolibrie ronde 5: volume in de shading en een Pokémon-oog (24 okt)

Uitgangspunt: `eind/kolibrie.png` (goedgekeurd). Jordi letterlijk: "Middelste versie erg mooi. Alleen het is nog net iets te 2d qua shading. Plus het oog is nog niet helemaal pokemon. Vergelijken met wat andere Sprites? Oog moet wel klein blijven". Aanvulling: "Een kolibrie moet echt kleine ogen hebben dus zoek naar pokemon met minimale ogen".

Bestanden:
- `kolibrie.png`: 64×64, P-modus, 16 kleuren, index 0 transparant, 1000 px (gelijk aan eind).
- `teken.py`: eind-raster als tekst plus de met de hand getypte bewerkingen per rij (`EDITS`, `EYE`, `EDITS_LIJF`, `EDITS_VLEUGEL`, `EDITS_STAART`).
- `check.py`: alpha-bewijs, telling, palet, open randen.
- `vel.png`: eind en ronde 5 op 4×, 2× en 1× (licht en donker); 9×9-oog-uitsneden op 8× van de kolibrie en 18 echte vogels; 1× en 2× naast Swellow, Taillow, Honchkrow, Murkrow, Fearow, Crobat, Ho-Oh, Articuno, Corviknight en Kilowattrel.

## Alpha-bewijs
`python3 check.py`:
- alpha-verschillen: **0** (silhouet en omtrek identiek, 1000 ondoorzichtige pixels)
- omgekleurde pixels: 102 (alleen binnen het silhouet; 4 daarvan zijn wit → bijna-wit, zie palet)
- omgekleurde pixels naast transparant: **geen** (de omlijning is niet aangeraakt, dus geen nieuwe open randen)
- 16 indices in gebruik, index 0 transparant

## Palet
- Eén nieuwe tint: **index f = (96, 80, 140)**, het hooglicht van de fluweelzwarte kop en de vleugelwortel (tussen basis `3` en lichtrand `4`).
- Daarvoor is puur wit (`f`, 4 px: oogglans en drie vlamkernen) samengevoegd met bijna-wit `e` (240,238,255). Op 1× niet te zien.
- Kleurkeuze per onderdeel ongewijzigd: fluweelzwarte kop, gedempt violet lijf, blauwgroene glans, vleugels van fluweel naar doorschijnend bleek, slierten met zielevlammetjes.

## Oogstudie (8×-uitsneden op het vel)
| sprite | kop | grootte (incl. omlijning) | omlijning | pupil | glans | iris / oogwit | plaats t.o.v. snavel |
|---|---|---|---|---|---|---|---|
| **Corviknight** | donker blauwzwart | 2×2 + zwart lid | zwart bovenlid, verder kop | geen aparte; zwart ernaast | 1 px roze (lichtste tint van de iris), linksboven | 2 px diep rood | vlak boven/achter de snavelwortel |
| **Kilowattrel** | zwart | 3×3 | geen; contrast doet het werk | 1 px zwart | grijs/wit aan de rand | felle cyaan ring om de pupil | direct boven de snavelwortel |
| Doduo | lichtbruin | 3×3 | grijze anti-alias | 2×2 zwart | 1 px wit in het midden-links | geen (zwart kraaloog) | ruim boven de snavel |
| Ducklett | lichtblauw | 2×2 | donkerblauw | 1 px | witte pixels eromheen | wit | boven de snavelwortel |
| Wingull | wit | 2×1 | grijs eronder | geen | 2 px bijna wit | — (streepje) | boven de snavelwortel |
| Spearow | oranje | 3×3 | zwart rondom | 1 px zwart | — | wit oogwit | boven de snavelwortel |
| Natu | groen | 3×3 | donkergrijs | 2×2 zwart | 2 px wit (onder) | grijze lichtpixel linksboven | achter de snavel |
| Xatu | groen | 3×2 | zwart (halfdicht) | grijs | — | grijs | achter de snavel |
| Corvisquire | donker olijf | 3×3 | donkerrood | — | wit eronder (masker) | rood | boven de snavelwortel |
| Honchkrow | donkerblauw | 3×3 | witte rand (oogwit) | 1 px zwart | wit | 1 px rood | boven de snavelwortel |
| Murkrow | donker groenzwart | 4×4 | rood | 1 px donkerrood | 2 px wit | rood | boven de snavelwortel |
| Chatot | zwart | 3×3 | lichte ring (bijna wit) | 1 px zwart | — | — | boven de snavel |
| Swellow | blauw | 3×2 | donker bovenlid | 1 px zwart | — | wit oogwit | boven/achter de snavel |
| Taillow | blauw | 3×3 | navy | 1–2 px zwart | — | wit/grijs | boven de snavel |
| Fearow | oranje | 3×3 | bruine wenkbrauw | 1–2 px zwart | — | wit oogwit | boven de snavelwortel |
| Pidgeot | bruin | 3×3 | donkerbruin | 1 px zwart | — | wit oogwit | boven/achter de snavel |
| Starly | wit | 3×5 | zwarte ring | — | wit midden | — | boven de snavel |

**Patroon:**
- Kleine vogeloogjes zijn 2×2 tot 3×3, met of zonder lid.
- Op een **lichte** kop is het oog een donker kraaltje met één witte pixel (Doduo, Natu).
- Op een **donkere** kop (Corviknight, Kilowattrel, Honchkrow, Murkrow, Chatot) is het oog nooit een donkere stip. Het leest door een **verzadigde of lichte iriskleur** rond een zwarte pupil (rood, cyaan of wit), met een **donker bovenlid** en een lichtste pixel linksboven.
- Het oog staat altijd vlak boven of achter de snavelwortel.
- De eind-versie had alleen een witte stip met een donker lid. Zonder iris las die als een gaatje in de kop en niet als oog.

**Toegepast:** het Corviknight/Kilowattrel-patroon in de blauwgroene kleur van de keelglans. Het oog blijft 2 breed × 3 hoog, inclusief het lid:
```
rij 25:  1 1    bovenlid (donkerst), ongewijzigd
rij 26:  e 1    glans linksboven (licht van linksboven), pupil
rij 27:  9 a    iris: donker blauwgroen links, licht blauwgroen rechtsonder (weerkaatsing tegenover de glans)
```
- Er zijn maar 2 pixels veranderd: (10,27) `2`→`9` en (11,27) `6`→`a`.
- Plaats, grootte en lid zijn gelijk aan eind: (10–11, 25–27), boven de snavelwortel.

## Volume per onderdeel (en de gids-regel erbij)
Licht van linksboven (gids "Shading Rounded Surfaces": hooglicht aan de lichtkant, schaduwgrens op de "evenaar", schaduw daarna egaal; geen kussenshading).

- **Kop (bol):**
  - Hooglicht `f` als klein rond vlekje op de schedel linksboven: (9–11,21), (8–11,22), (8–9,23).
  - Het vlekje volgt de ronding van de lichtrand, maar raakt die links niet. Regel: "highlight klein, waar het licht loodrecht valt".
  - Schaduw `2` onder een schuine evenaar van (15,24) naar (8,30), op wang, keel en achterhoofd (rechtsonder).
  - Daardoor is de kop niet meer één vlak `3`. Boven is licht en onder donker, en het oog zit precies op de evenaar.
  - De lichtrand `4` (omlijnings-hooglicht) en de snavel zijn niet aangeraakt.
- **Lijf (de borst bolt naar de kijker):**
  - Het verticale streepje `8` is vervangen door een schuin ovaal hooglicht op de borst, (13–20, 26–31), dat de bolling volgt. Regel: "R/S gebruikt veel hooglichtkleur".
  - De schaduw `6` is van 1 px langs de buik uitgebreid tot een egale band onder de evenaar, die van de borst (13,33) schuin oploopt naar de staartwortel (37,38). Regel: "schaduw start abrupt op de evenaar en wordt daarna niet donkerder".
  - Het lijf heeft nu drie duidelijke zones: licht linksboven, basis in het midden, schaduw onder.
  - De slagschaduwen bleven staan: de vleugelwortel op de rug (`666`) en de kop op de borst (`66` langs de nek). Regel: "slagschaduw altijd volledig in de schaduwkleur".
  - Geen weerkaatst licht aan de onderrand: de gids zegt dat officiële sprites dat weglaten, en het zou druk worden.
- **Vleugelwortel dichtbij (welving):**
  - De losse donkere streepjes in het fluweel (rij 24–26) zijn één doorlopende welving geworden.
  - Hooglicht `f` direct onder de voorrand `4` (rij 21–23).
  - Basis `3` in het midden.
  - Schaduw `2` aan de rechter- en onderkant, waar de wortel van het licht af in het lijf buigt (rij 25–29).
- **Verre vleugelwortel:** onveranderd. Die had al een cilinderverloop (`4`-`3`-`2`-`1`) en hoort als verre kant meer in de schaduw te liggen.
- **Slierten (cilinders):**
  - S3 en S2 hadden al een licht- en een schaduwkant (`1`-`7`-`8`-`5` diagonaal).
  - S1 is waar hij 2 rijen dik is (x 51–55) onderaan `6` geworden: lichtkant `7` boven, schaduwkant `6` onder.
  - De staartwortel had al `8` boven, `7` in het midden en `6` onder.
- **Keelglans:**
  - Ongewijzigd: `a` aan de lichtkant, `9` aan de schaduwkant.
  - Een glanspixel `e` heb ik geprobeerd en weer weggehaald: op 1× las die als tweede oog.

## §0 en de norm
- 1 (3/4): ok, ongewijzigd.
- 2 (delen): ok, ongewijzigd.
- 3 (curven): ok, omtrek ongewijzigd. De nieuwe schaduwgrenzen lopen in treden van 1–3 px, zonder hoeken.
- 4 (ogen geïntegreerd): ok. Bovenlid donkerst, iris donker/licht, glans; geen bril. Het oog is klein gebleven.
- 5 (silhouet): ok, alpha 0.
- 6 (formaat): ok, 1000 px.
- 7 (pose): ok, ongewijzigd.
- Norm 9 (omlijning, licht linksboven, geen open randen): ok. Er is geen randpixel veranderd; de lichtrichting is nu overal consequent.

## Eigen 1×-toets
- Naast eind (vel, 1× en 2×, licht en donker) leest ronde 5 ronder.
  - De borst bolt naar voren en de buik draait weg in de schaduw.
  - De kop is een bol met een lichte schedel en een donkere keel.
  - De vleugelwortel welft.
- Niet drukker: er zijn geen extra kleurvlakken bijgekomen, alleen grotere en duidelijkere zones met dezelfde tinten.
- Het oog leest op 1× en 2× als een klein blauwgroen kraaloog met een glanspunt, net als Kilowattrel en Corviknight ernaast. Het is geen witte stip meer.
- Ook op donker blijft het zichtbaar, door het blauwgroen.

## Wat nog niet klopt / open voor Jordi
- **Oogkleur:** blauwgroen is mijn keuze, zodat het oog bij de keelglans aansluit (Kilowattrel-patroon). Een echte kolibrie heeft een zwart oog; rood (Corviknight) of bleek lavendel (Ghost) kan ook. Het gaat dan om alleen 2 pixels.
- Op de kleinste weergave (1× op licht) is het lijfhooglicht duidelijk, maar het kophooglicht `f` is subtiel. Dat is bewust: de kop moet fluweelzwart blijven.
- Verder vind ik geen zwakke punten. Er is geen open rand, het silhouet is identiek en het gezicht oogt niet vreemder dan in eind.

## Lessen
- Een donkere kop heeft een oog met een gekleurde of lichte iris nodig (Corviknight, Kilowattrel). Een witte stip op een donkere kop leest als een gaatje.
- Een glanspixel bij de kop (keelglans) kan op 1× als tweede oog lezen. Houd glanspixels weg uit de buurt van het oog.
- "Te 2D" zat vooral in te smalle zones: hooglicht als streepje en schaduw als randje van 1 px. Brede zones met dezelfde tinten, gescheiden door een schuine evenaar, geven volume zonder extra kleuren.
