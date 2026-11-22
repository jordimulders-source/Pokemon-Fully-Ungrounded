# Vuurduivel fase 1, sprite r1

**Sprite:** `vuurduivel_r1.png` (64×64, 4-bit palet, 15 kleuren incl. transparant op index 0). Figuur x12–50, y13–62: **50 px hoog**, 39 breed, voeten onderin (y62).
**Vel:** `vel.png` = r1 8× | kale reductie 8× | model op dezelfde schaal; daaronder het gezicht op 12× naast het model; 1× op wit, lichtgroen, donkerblauw, zwart.

## Werkwijze (model overgenomen, niet hertekend)
1. `natief.py`: pitch gemeten met randsterkte. 8,53 en 4,27 scoren bijna gelijk, dus de echte cel is **4,267 px (1024/240)**. Het natieve figuur is 78×99.
2. `reductie.py`: exact 2× verkleinen (fase x+0, y+1 gekozen; die hield het oogwit het best). Elke natieve pixel krijgt de dichtstbijzijnde modelkleur (k-means op het model). Een spritepixel is figuur bij ≥2 van de 4 pixels. Kleur: zwart als ≥2 zwart (lijnen blijven), anders de meest voorkomende kleur. Bij gelijkstand wint de donkerste, behalve in vuur: daar wint de lichtste. Vlampunten tellen al mee vanaf 1 van de 4 pixels.
3. `schoon.py`: amber telt als geel naast geel, anders als oranje. Losse pixels gaan op in hun buren, ook vlamvlekjes < 3 px in het haar. Buitenlijn van 1 px: zwart rond lijf, vacht en poten. Rond de vlammen een tint donkerder dan de vlamkleur (geel → oranje → rood → donkerrood), want het model heeft daar geen zwarte lijn. Resultaat: `kaal.png` / `raster_auto.txt`.
4. `wijzig.py` + `wijzig_extra.py`: reparaties per pixel, elk met reden. De volledige lijst staat in `wijzigingen.txt`.
5. `controle.py`: 15 kleuren, geen lichte kleur op de buitenrand, geen losse zwarte pixels.

Palet (alles gemeten op het model): zwart 3,1,1 · grijs 27 / 51 / 72 (de drie lijftinten van het model) · vuur 108,19,20 / 162,41,41 / 242,113,57 / 252,208,89 · bruin 76,51,36 / 101,69,52 / 139,102,75 · tong en hoornlicht 198,98,92 · oogwit 248,246,236 · mond binnen 127,56,50.

## Pixels die niet uit de kale reductie komen (96 van 949 wijken af)
Allemaal naar de natieve modelcellen, behalve de staartpunt:
- **Ver oog (6):** de reductie verloor het oogwit. Bovenlid (16,32) en (18,32), oogwit (16,33), (17,33) en (17,34), pupil rechts (18,33).
- **Nabij oog (4):** los wit reepje (24,33) weg (1 natieve px; las als tand), bovenlid (25,31) en (28,31), oogwit (28,33).
- **Neus (1):** (20,35) lichtgrijs puntje, zoals het model.
- **Tong (1):** (22,38) roze, zodat de tong 4 breed is zoals in het model.
- **Rechterhoorn (13):** de hoorn ging op in het rode haar. Punt (26,21), linkerrand donkerrood (24–25, y22–25), lichtstreep (25–26, y22–24) in hoornlicht, rechterrand zwart (27, y22–24), zoals het model.
- **Linkerhoorn (2) + haar (3):** (14,24) gekleurde selout aan de lichtkant. (18,24), (17,24) en (19,19): zwart of mondbruin werd donkerrood op dezelfde lijnplek.
- **Rechteroor (1):** binnenlijn (37,31) in donkergrijs in plaats van een losse zwarte pixel.
- **Benen en hoeven (16):** de randregel maakte de dunne benen zwart. Linkerdij (20,55), linker onderbeen (25,57) en (26,57), linkervoet (22,58), (21,59) en (22,59), hoef (22,60). Rechter onderbeen en hoef y58–62 krijgen 3 px bruin, zoals het model, met donkere hoefband y60 en de lichtkant in donkerbruin.
- **Staartpunt (68, de enige toegestane afwijking):** de gereduceerde vlampunt is gewist. Er staat nu een massieve schoppenpunt (`pijl.py`, variant B) op dezelfde plek: bbox x42–50, y36–45, stam bij x45–46. Kleuren: geel bij de punt, oranje in het midden, rood bij de basis, randen een tint donkerder en donkerrood aan de schaduwkant. Variant A (schuin, punt rechtsboven zoals het model) staat in `variant_pijl_schuin.png`. Die las meer als een vlam of hart, daarom B.

Verder niets getekend: lijfschaduw, haarvlammen, vacht, armen en staartlijn komen uit de reductie.

## Zelf geziene zwakke punten
- **Wenkbrauwen** (V-vorm, 2–3 px zwart op grijs 51) staan op de modelplek, maar lezen zwak. In het model lezen ze door de fijne lijnen.
- **Bovenrand van het haar** wisselt donkerrood, rood en oranje af, omdat de rand een tint donkerder is dan de vlam eronder. Dat volgt de streken van het model. Ik heb een rand in één donkerrode tint geprobeerd: die was zwaarder en verder van het lichte model, dus de huidige rand blijft. Een keurder kan dit nog wegen.
- **Vlampunten** zijn minder spits dan in het model (dunne punten van 1–2 natieve px vallen weg bij 2×). Het silhouet volgt de reductie.
- **Tintvlekjes < 3 px** zijn vooral randstukjes van de vlammen en de spade, plus oogwit, tand en neus (bewust). Rond het lijf zijn er geen.
