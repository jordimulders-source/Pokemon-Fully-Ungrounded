# Kelp-/anemoon-Vileplume frontsprite, ronde 6 (kandidaat)

Bestanden: `vileplume_r6.png` (gelaat B, standaard), `vileplume_r6_gelaatA.png`, `vileplume_r6_gelaatC.png`, `kaal.png`, `bouw.py` (`python3 r6/bouw.py` vanuit `vileplume_sprite/`), `uitvoer.txt` (tellingen + tekstraster), `vel.png` (r6 8× | r5 8× | model 8× / close-ups 12×: krater, achterste anemoon L, voorste anemoon VL, elk naast het model / 1× op licht en donker + model 1×).
64×64, geïndexeerd 4 bpp, 16 paletplekken (alle 16 gebruikt, zelfde palet als r4), index 0 transparant, opgeslagen met transparency=0. Figuur x3–59, y1–62 (57×62; de twee buitenste tentakelpunten van L en R liggen op de modelpunten, 1 px verder dan r4).

## Jordi's punten
- "de anemonen zijn niet allemaal even netjes" + over r4 "nu neemt wel de definitie af idd": anemonen opnieuw opgebouwd, alle vijf op dezelfde manier (hieronder).
- "de krater mag wat netter rond": krater = r4-ovaal, **0 px verschil met r4** (geen anemoon mag er nog overheen).
- "Linkerpoot is te recht" → (via coördinator) poot links op het scherm "schuiner", meer naar buiten: rijen y44–59 opnieuw als 3 px (W0-lijn | vulling | zwart), linkerkant x = 25 − 0,27·(y−44): y44 x25 → y59 x21, gelijkmatige trap van ±4 rijen per stap; vulling per rij zoals r4; heup (y41–43) en voetrij-opbouw als r4. Niets anders toegevoegd.
- Gelaat: B standaard (twee 1×2-ogen), A = model (U), C = B zonder balkje; precies als r4 (B↔A 4 px, C↔B 3 px).

## Opbouw per anemoon (VL, VR voor; L, R, T achter; tekenvolgorde T, L, R, krater, VR, VL)
1. **Kroonschijf** = nette ellips, op het model gemeten (cx, cy, a, b in spritepx): VL 25,0/21,5/10,2/6,2 · VR 43,5/20,0/8,8/6,0 · L 14,0/14,0/9,0/5,6 · R 49,0/12,3/8,6/5,4 · T 33,5/6,3/7,4/2,7.
2. **Tentakels (optie A)**: per anemoon 9–11 lichte wiggen (VL 9, VR 9, L 10, T 10, R 11; `python3 r6/bouw.py r6 --tel`) (R3) vanuit het mondje naar de rand; tussen twee tentakels een smalle wig in R1 (rustig vlak, verbreedt naar de rand zoals in het model). Richtingen: voorste anemonen = de 9 klonten uit het model (massamidden van de modeltentakels per sector, als r3/r4); achterste anemonen boven = de **gemeten modelpunten** (`gereedschap/punten.py`: lokale maxima van de silhouetrand; L 7 (twee punten < 1,6 px samengevoegd), R 8, T 8 (waarvan 1 aangevuld in een vlak stuk bovenrand)), onder = de modelklonten. Rond het mondje een lichte ring (1,6 px), zodat het mondje vrij ligt.
3. **Punten** steken uit tot de modelpunt (max. 3 px buiten de rand), 1 px breed in R3, omlijnd (R0 lichtkant, zwart schaduwkant).
4. **Mondje**: ovaal op de bbox van de modelring (VL x22–26 y21–23, VR x40–45 y19–21, L x11–16 y13–15, R x46–51 y11–13, T x31–36 y5–7), ring R0, binnen R3 (model: lichte binnenkant in donkere ring).
5. **Voet** = de kroonellips naar beneden geschoven (lage, licht bolle cilinder: VL 0/3, VR 0,5/3,2, L −1,5/6,5, R 1,5/6,5, T 0/4 px; bolling 0,1), binnen het modelsilhouet, met de tinten van de kale reductie (R1/R2 = modelschaduw).
6. **Randen**: zwart waar een achterste anemoon aan een voorste grenst (donkere rand om elke anemoon); R0-lijn tussen kroon en voet; buitenrand R0 aan de lichtkant, zwart aan de schaduwkant; zwart aan de onderkant tegen het lijf.
7. Keel onder de krater (tussen VL en VR): kale reductie (54 px). 6 ingesloten gaatjes naast de krater → zwart. Ruisstap: 7 losse pixels in de kroon naar de buurtint.

## Niet-modelpixels per zone
- T.o.v. de kale reductie: **anemonen 734** (de hele kroonopbouw is optie A), krater 57 (= r4), lijf+armen 37 (= r4), poten 100 (r4: 56 + linkerpoot).
- T.o.v. r4: anemonen 666, krater **0**, lijf+armen **0**, poten 70 (alleen de linkerpoot; rechterpoot 0, geassert).
- Mondjes 67 px, tentakels 427 px. Elke anemoonpixel is kroon (ellips), tentakel, tussenvlak, mondje, rand of voet; geen andere klassen.

## Toets (`gereedschap/toets.py`)
- 16 kleuren incl. transparant; lichte kleur op de buitenrand 0; lijnpixel midden in een vlak zonder lijnbuur 0; zwart 17,4 %.
- Losse pixels 12, alle bewust: 3 R0-kapjes op de toppen van T-punten (31,1)(33,1)(35,1); 4 zwarte buitenlijnhoekjes (25,5)(15,7)(4,13)(9,24) en R0-hoekje (10,25); 1 lichte punttop (41,5); 3 in de arm-oksel (42–44,35–36) = r4/bevroren.

## Twijfels (eerlijk)
- R heeft 11 tentakels, net boven Jordi's ±8–10 (8 gemeten modelpunten + 3 onder); kan naar 10 door de zijpunt (56,7;13,7) te laten vallen.
- De wiggen maken de kroon "stervormig"; het model heeft meer en dunnere tentakels. Dat is optie A; de lijn tussen "dikke tentakels" en "taartpunten" moet Jordi zien. Smallere wiggen: `--half=0.45`, bredere `--half=0.65`.
- De kroon is lichter dan in het model (tentakels R3 nemen ±55 % van de schijf in); het model oogt roder. `--half` lager maakt hem roder.
- De naad VL|L (x14, y17–25) is nog vrij recht; dat is de zijkant van de voorste cilinder. In het model loopt die rand ook bijna verticaal.
- Close-up L in `vel.png`: de modeluitsnede rechts is verschoven (model_crop knipt buiten het beeld bij x2); de 8×-panelen bovenaan zijn wel goed uitgelijnd.
- Linkerpoot: de trap is regelmatig (4-4-4-4 rijen); of "schuiner" genoeg is, moet Jordi zien (`0.27` in `bouw.py` is de helling).
