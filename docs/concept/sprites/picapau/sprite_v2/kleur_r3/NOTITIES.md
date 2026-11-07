# Picapau sprite_v2 kleur r3: notities (maker, 5 nov)

Bestanden: `teken.py` (rij voor rij met de hand overgetrokken van de B1-render, (x, tekens)) → `raster.txt`; `bouw.py` (palet r1/r2) → `picapau.png`, `normal.pal`; `controle.py` → `controle_uitvoer.txt`; `vel.py` → `vel.png` (8x render | r1 | r2 | r3 | Taillow | Pikachu + 1x/2x); `closeup.py` → `closeup.png` (16x per onderdeel: render | r2 | r3); `krabbel_over_r3.png` (Jordi's krabbel op r2 teruggerekend (schaal/offset via oog en kuiftoppen) en in magenta over r3).

Werkwijze: niet meer vanaf r2 bijpatchen, maar de hele sprite opnieuw cel voor cel van de render (50%-dekkingsmasker + labelkaart + renderhelderheid per cel als onderlaag), licht naar linksboven verschoven. Overgenomen: kuiftoppen r3–8 (r5, diff 0), staart r46–57 (r2, diff 0), snavel uit de r3-tussenstand (N-cellen), palet.

## De tien punten van de coördinator (eerlijk)
1. **Kop**: bovenrand nu een boog (3-3-1-1-1 i.p.v. 4 plat), schaduwsikkel rechts/onder, inham waar de kop de rug raakt (r20–21). **Half**: leest als bol, maar nog minder rond dan de render; de kuif blijft optisch met de kop verbonden.
2. **Kuif**: twee kegels met binnenlijn tussen voor- en achterkegel (x34–35, Jordi's lijn) en een schaduwlijn onder de voorste kegel (Jordi's lijn (30,12)–(33,10)); drie afgeronde platte punten achter (r11–13, r16–18, r21–23), 1 rij hoger gezet zoals de render. **Niet ok**: de kegels zijn aan de top (r5–8) nog 2–3 px breed (zo smal is het model op 64 px), dus ze lezen nog als stokjes met een gele voet; groter maken kan alleen buiten het silhouet.
3. **Oog**: Pikachu-opbouw, 4x4, op de rendermaat en -plek (x24–27, r18–21; 1 px naar links t.o.v. r5). **Ok**.
4. **Wang**: ronde schijf 5x5 (x24–28, r23–27), licht linksboven, schaduw rechtsonder. **Ok**.
5. **Snavel**: N-cellen gevuld, kegel met lichte bovenkant (`1`), basis `h`, donkere onderkant `g`/`G`, donkere punt, donkere basis bij het gezicht; verre oog als bultje links boven de snavel ((18,17) k, (19,17) G, (19,16) k). **Ok-ish**: op 1x een bleke snavel met donkere basis, iets slanker dan de render.
6. **Borst/buik/dij**: borstlicht op de bolling, voorrand 1 px naar buiten op r31–33 (render-dekking 0,23–0,48), dijlicht r39–42, brede schaduw rechts en onder, ronde buikonderkant (r45→r47). **Half**: de voorkant is nog vrij recht (het model is op 64 px zo); het bol-zijn komt vooral uit de schaduw, minder uit de omtrek dan in de render. Jordi's lange boog ligt op de omtrek (zie krabbel_over_r3.png).
7. **Vleugel**: ronde schouder (r25–26), voorrand als boog die 1 px over het lijf bolt (x33 r29–31, Jordi's korte boog), elleboog onderaan, slagpennenband tot de staart; **stippen van het model** op de renderplekken: A (35–36, 27–28), B (39–40, 26–27), C (36–37, 31–32), D (41–42, 31–32, schaduwkant `g`), E (42–43, 35). **Ok-ish**: stippen lezen op 1x; de vleugel is iets smaller dan in de render.
8. **Poten**: twee grijze loopbenen recht omlaag uit de dij (nabij x29–31 r44–46, ver x33 r45–46 donker), tenen uitgespreid zoals de render: nabije teen naar links met klauw (25,47), nabije teen naar rechtsvoor (30–32, 48) met klauw (33,48–49), verre teen (33–35, 47) met klauw (36,47)/(37,48). **Ok-ish**: leest als twee pootjes; op 8x nog wat hoekig.
9. **Staart**: knobbel bij de basis (r46–50) en lange punt, ongewijzigd uit r2. **Ok**.
10. **Licht en schaduw**: per onderdeel een bol (kop, kegels, borst, dij, vleugel, staart) met licht linksboven. **Half**: zie 1, 2 en 6.

Jordi's zes punten: 2d **half** (beter dan r2: kopbol, vleugel over lijf, losse poten), driekwart **ok**, perspectief **ok**, klauwen **ok-ish**, shading **half**, snavel **ok-ish**.

## Controle
- Lichte kleur op de buitenrand 0, losse pixels 0. Kleine tintclusters alleen nog in oog-hoeken (Pikachu-oog), de snavelonderrand (diagonale lijn), r5-kuif (32,7–8), één stip (2 px) en vleugelbandlijnen.
- Diff met r2: kuiftoppen 0, staart 0; verder 269 px hertekend.
- **Buiten het silhouet: 40 px** (lijst in controle_uitvoer.txt): kuiftoppen 6 (r5), kuifpunten 13 (punten hoger/langer zoals de render), snavel/verre oog 3, borst 3 ((25,31–33)), buikboog 3, poten/tenen/klauwen 12. Leeg gelaten: 6 ((25,12) kopboog, (38,14) inham tussen kuifpunten, 4 tussen de poten).
- 852 px, 15 kleuren + transparant.

## Zwakke punten (melden, dus niet klaar voor Jordi zonder keuring)
- Kuifkegels aan de top te smal (2–3 px) → lezen niet als "grote kegels".
- Voorkant van de romp nog vrij recht; meer bol kan alleen door de omtrek verder buiten het silhouet te zetten dan de render-dekking toelaat.
- Kop en kuif lezen nog deels als één gele massa.

## Lessen
- Patchen vanaf een vorige ronde hield de fouten vast (smalle snavel, blokvleugel); opnieuw overtrekken vanaf het dekkingsmasker + labels + renderhelderheid per cel ging sneller en volgde het model beter.
- Een krabbel van Jordi terugrekenen naar spritecoördinaten via oog en kuiftoppen (schaal ≈1,014, offset uit de paneellabels) maakt elke lijn toetsbaar; filter de sprite-omlijning eruit.
- Een zoom-uitsnede met tekstrand verschuift de render t.o.v. de sprite niet, maar wel je eigen aflezing: meet posities met een script (vlekken, dekking), niet op het oog.
