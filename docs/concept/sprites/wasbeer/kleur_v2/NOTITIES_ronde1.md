# Kleur ronde 1 (maker-agent, 2 nov)

Silhouet `../silhouet_v2/direct_s1a.txt` (bevroren, 1682 px); alpha-diff 0 (controle in `rijen_ronde1.py`). Met de hand geschreven rijen (x-start + hex-indices) per onderdeel in `rijen_ronde1.py`, uitvoer `ronde1.txt` (één teken per index, '.' = 0), `ronde1.png` (geïndexeerd, index 0 transparant), palet `ronde1.pal`, vel `vel_ronde1.png` (`vel.py`). Studie: `STUDIE.md`.

**Palet (16):** 0 transparant · 1 omlijning (22,16,16) · 2–3 donker (masker, onderarmen/-benen, staartringen) · 4–7 grijze vacht (selout, schaduw, basis, licht) · 8–9–a crème (schaduw, basis, wit) · b–d buidel (warm grijsbruin) · e–f iris.

**Per onderdeel (volgt de render):**
- **Kop:** één grijze familie met het licht linksboven. Zwart masker (2) over beide ogen en de neusrug (glans 3 op de rug), achter het oog op x 25–26 houdt het op. Witte wenkbrauwband (a, vlek boven het verre oog, smal bij het nabije). Witte snuitrand (a/9). Neus 1 met glans 3. Oren wit met crème schaduw. Ogen: bovenlid 1, iris e/f, glans a linksboven (verre oog 3x2; nabije 1x2).
- **Nabije klauw** (op de borst): 2 klauwen naast elkaar (x 22–23 en 25–26), inkeping x 24 vanaf y 29, met een grijze kleurgrens (4) links en onder tegen de crème buik. De klauw hangt aan de donkere hand/onderarm (2/3) rechts, niet uit de buik.
- **Verre klauw:** crème (8/9) met omlijning 1 aan de schaduwkant, 2 punten met de silhouetinkeping.
- **Buidel:** eigen warme tint (b/c/d), licht linksboven, schaduw rechtsonder. Opening/plooi bovenaan aan de schouderkant (donkere spleet 1/2 onder een flap b). Naad met de rug in b, zonder zwarte lijn (geleidelijk, geen jetpack).
- **Borst/buik:** zachte crème ovaal (8/9) rond en onder de nabije klauw, geen rechthoek.
- **Onderarmen/onderbenen** donker (2/3), **dijen** grijs: de verre dij in 5/4 en de nabije in 6/5. **Staart:** haak donker met een lichte vlek aan de buitenkant, daarna ringen 9/8 en 2.

## Eigen zwakke punten (eerlijk)
- De nabije onderarm leest op 1x als een donkere vlek/gat naast de klauw; het volume is zwak (alleen een kleine glans 3).
- De lijfschaduw is vlak: weinig 7-hooglicht op schouder en dij, weinig kernschaduw. Op 1x oogt de romp grijs-egaal.
- De ogen zijn klein (verre 3x2, nabije 1x2). Het nabije oog zit tegen de rand en leest nauwelijks.
- De neus loopt over in het masker (render idem), dus geen eigen neusvorm.
- Staartringen zijn blokkerig (rechte banden), geen gebogen ringen. De haak leest door de lichte vlek in de kop iets rommelig.
- De inkeping van de nabije klauw loopt 4 rijen door (zoals de render); op 1x leest hij als "m"-hand.
- De kleur is nog niet stuk voor stuk tegen de foto's gelegd (foto 10/11/2/7); alleen tegen de render.
- De controle op losse pixels is grof (schaduwlijnen van 1 px tellen mee); niet elke losse pixel is nagelopen.

## Lessen
- Rijen als (x-start, hexstring) per onderdeel in een script, met een alpha-controle tegen het silhouet: de eerste versie paste meteen (diff 0), en reparaties zijn gerichte vervangingen.
