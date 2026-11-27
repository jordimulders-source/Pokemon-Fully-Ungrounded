# Kudu sprite ronde 6 (maker)
Kleine reparaties uit de keuring van r5b. Script `sprite/r6.py` = `r5b.py` + één blok `r6`; vel: `vel6.py` (r6 | r5b | model).
Oog wisselen: `python3 r6.py A|B|C|D`. B staat in `kudu_r6.png`, A/C/D in `kudu_r6_oog{A,C,D}.png` (+ 8x).
Coördinaten hieronder zijn rastercoördinaten (beeld x − 6). Elk punt is eerst op het model gemeten.

## Wat er veranderd is t.o.v. r5b (25 px)
1. **Strengen (13 px → d).** De strengen zijn donker olijf, niet zwart. Met lijn = helderheid < 70 vielen ze onder de drempel; gemeten met < 100 lopen ze door.
   - **Streng op x19:** in het model ononderbroken van rij 26 tot 41 (29-58%). Doorgetrokken: (19,35)-(19,39) en (19,41); (19,40) was al d.
   - **Tweede streng:** gemeten loopt die van x22 (rij 30-33, 47-68%) naar x21 (rij 34-40, 31-70%), dus één kolom naar links. Gezet: (22,30)-(22,33) en (21,34)-(21,36); (21,37)-(21,40) waren al d.
   - **Afwijking van de keurder:** (21,41) blijft M. Daar is maar 23% lijn en de cel is borstvacht.
2. **Losse vachtpixels.**
   - (22,31) ligt op de tweede streng en is nu d (zie 1).
   - **Afwijking van de keurder:** (16,39), (17,39) en (17,40) zijn in het model geen manen maar vacht (66-78%) in de kleur van de halsstrook (184,144,56 / 168,128,64). Ze zijn het einde van de strook naar de borst. Ze worden M zoals de strook, niet manentint.
3. **(9,25):** in het model 0% wit, vachthelderheid 173. Wordt **M** (W → M).
   - **Afwijking van de keurder:** hij vroeg L, maar L begint pas bij 181.
4. **Buiksikkel (32-35,44):** het model geeft hier 152-159, onder de vachtgrens van 160. Wordt D (M → D), zodat de donkere band doorloopt.
5. **Hoornvoet (19-20,15-16):** onderrand van de hoorn en de lijn tussen hoorn en oor, met 30-43% modellijn. Schaduwkant, dus lijn 0 (A → 0). De afwisseling met A op die rand is weg.

## Pixels
- T.o.v. de kale reductie van model A3: 607 van 1362 (vacht 215, manen 149, staal 135, lijn 83, oog 11, donker 11, roze 3).
- T.o.v. r4: 176. Per pixel staat alles in `wijzigingen.txt` (stappen `streng6`, `hals6`, `wit6`, `buik6`, `hoorn6`).
- Niet uit het model: geen nieuwe pixels. Alle 25 komen uit modelmetingen; de kleurkeuze volgt de bestaande grenzen (vacht L ≥ 181, D < 160; lijn 0).
