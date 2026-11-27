# Regionale Staryu (chocolate chip-koekje) frontsprite, ronde 1 (kandidaat)

Bestanden: `staryu_r1.png` (64×64, mode P, index 0 transparant, 14 kleuren incl. transparant), `kaal.png` (kale reductie), `vel.png` (r1 8× | kaal 8× | model op dezelfde schaal 8× / close-ups 12× bovenarm, juweel, linkerarm, rechterarm, benen (sprite | model) / 1× op wit, crème, donker, zwart + model 1× + Gen 3 Staryu en Starmie 1×), `bouw.py`.
Gereedschap (`../gereedschap/`, gekopieerd van Dundragoon en aangepast): `pitch.py`, `natief.py` (→ `natief.png`), `klassen.py` (zwart/chocolade/deeg/juweel per modelpixel), `gemeen.py` (schaal, palet, overlap), `vel.py`, `raster.py`, `controle.py`, `zones.py`.
Bouwen: `cd staryu_regional/staryu && python3 sprite_r1/bouw.py` (`kaal` als argument toont alleen de kale reductie).

## Metingen
- **Rasterpitch:** randsterkte per kolom/rij gaf één kam op **10,24 px** (1024/100), fase x 9,25 / y 9,20 (zelfde Gemini-raster als Dundragoon); visueel bevestigd op een 4×-uitsnede van het juweel (cellen ±10 px). Natief raster 99×99, figuur x13–86, y11–86 (**74×76**, 3128 px).
- **Schaal 0,56** (1,79 natieve px per spritepixel). Figuur in de sprite **x11–51, y12–54 (41×43), 981 px**. Gen 3 Staryu (`anim_front_gba.png`): 43×44, 910 px. Het koekje is boller dan de puntige Staryu, dus iets meer pixels bij dezelfde maat. Niet gespiegeld.

## Wat uit het model komt (kale reductie, `kaal.png`)
Klassen per natieve pixel (`klassen.py`): zwart (L<38), juweel (rood: R−G>70, B≈G), chocolade (donker en laag verzadigd, incl. de roze chipglans), deeg (de rest). Zwart dat niet aan de achtergrond grenst is de donkere onderrand van chips/juweel en telt als chip-rand of juweel. Daarna oppervlakteweging per spritepixel:
- achtergrond als < ½ pixel figuur; **zwart wint** vanaf 30 %;
- **juweel wint** vanaf 35 %, tint = de meest voorkomende modeltint in het vak (geen gemiddelde, anders vervloeien de strepen);
- **chocolade wint** vanaf 35 %: glans (8) als ≥ 18 % lichtroze, rand (6) als ≥ 40 % van de chip uit de zwarte onderrand komt, anders chipmidden (7);
- anders deeg, tint naar de gemiddelde modelhelderheid (drempels 140/188).
Silhouet, alle 11 chips, het juweel met glans en strepen, de lichte linkerkanten en de schaduwbanden onder/rechts komen allemaal uit deze reductie.

## Pixels die afwijken van de kale reductie: 165 px (silhouet-diff 0)
Per zone (`zones.py`): **bovenarm 31, linkerarm 35, rechterarm 21, juweel 18, benen 60.** Per stap (`bouw.py`):
- **buitenlijn (72 px):** geen open of lichte rand; achtergrond rechts/onder → zwart (schaduwkant), lichtkant → selout 2 (donkerste koektint). Zwart uit het model blijft zwart.
- **barstjes (58 px):** de 1-px barst- en naadlijnen van het model (donker deeg L<135, dun: ≤ 11 donkere deegpixels in de 5×5-buurt, ≥ 3 px van de rand, lijnstuk ≥ 6 natieve px) vielen bij 0,56× weg. Elke modelpixel van zo'n lijn is naar zijn spritepixel geprojecteerd en daar deegschaduw (3) geworden, alleen op midden/licht deeg. Vorm en plek komen dus 1-op-1 uit het model; niets met de hand.
- **ontkorrelen deeg (24 + 13 px):** tintvlekjes < 3 px in het deeg nemen de buurtint van het deeg aan (na de barstjes nog een ronde alleen voor midden/licht, barstlijnen bevroren). Chips en juweel niet aangeraakt.
- **chipglans (8 px):** per lichtroze glanscluster van het model precies één glanspixel op de gemeten plek (in de chip, dichtstbijzijnde chippixel); glans van de reductie op andere plekken → chipmidden. 10 glanspixels in 11 chips (zoals het model: één chip heeft geen lichtpuntje).
- **juweelrand (3 px):** het model heeft een gesloten ring (boven/links donkerrood, onder/rechts donkerst); de reductie liet onderaan 3 gaten. Randpixels van het juweel → 10 (boven/links) of 9 (onder/rechts).
- Geen andere pixels die niet uit het model komen; niets getekend.

## Palet (index: kleur)
0 transparant (152,208,160) · 1 zwart (24,16,16) · deeg 2 selout (150,80,32) 3 schaduw/barst (200,120,48) 4 midden (228,160,72) 5 licht (244,198,118) · chocolade 6 rand (56,26,18) 7 midden (102,54,36) 8 glans (206,160,140) · juweel 9 donkerst (92,18,24) 10 donkerrood (178,34,40) 11 rood (228,60,56) 12 licht (244,128,122) 13 glans (252,212,204). 14 kleuren, 2 vrij.
Gemeten modeltinten: deeg (185,99,39) / (224,160,64) / (243,193,112); chip (64,32,16), glans (199,151,124)–(241,227,220); juweel (90,19,23) / (165,30,35) / (225,50,50) / (245,125,120) / (252,205,198). Chipmidden en juweelrood iets lichter/helderder dan het model voor contrast (kleur mag afwijken).

## Controle (`controle.py`)
64×64, mode P, transparency 0, 14 kleuren; per groep ≤ 3 tinten + lijn/selout (juweel heeft 5 tinten: ring, ring, rood, licht, glans, zoals het model); geen lichte kleur op de buitenrand; geen losse zwarte pixels; zwart 8,1 % van de figuur.
Vlekjes < 3 px die over zijn: chip-rand/-midden (chips zijn 3–5 px groot, rand is een 1-px boog), chipglans (bewust 1 px), juweelstrepen en -glans (1-px diagonalen uit het model), 5 barststukjes (deel van een schuine 1-px lijn, tellen per 4-buur als los) en 2 middendeeg-pixels.

## Eerlijke twijfels
- **Juweel:** ring, glans linksboven en een lichte diagonaal komen uit het model, maar de streep-in-het-snoepje leest op 8× nog als wat onrustig rood/donkerrood (8×8 px voor een patroon dat in het model 14×14 is). Op 1× leest het als glanzend rood juweel.
- **Barstjes:** de naden van het juweel naar de inkepingen zijn als lijn te zien; de kortere barstjes op de armen zijn soms 2–3 px stukjes. Ze staan op de modelplekken, maar op 8× kan het wat korrelig ogen. Zonder deze stap (zie `kaal.png`) zijn de barstjes vrijwel weg.
- **Chips** zijn 3–5 px; sommige worden een beetje hoekig (bijv. de chip linksonder het juweel, x19–24 y30–35). Vorm = reductie, niet bijgewerkt.
- **Deegvolume:** licht linksboven en schaduw rechtsonder volgen het model per arm; er is geen eigen volume toegevoegd. De lichte tint ligt soms in losse plukjes (zoals in het model).
- **Maat:** 981 px tegen 910 bij Gen 3 Staryu; bij 0,53× zou het ±880 px zijn maar dan worden chips 3 px en vallen glanspixels weg.
