# Vuurduivel fase 1, sprite r5

**Sprite:** `vuurduivel_r5.png` (64×64, 4-bit, 16 kleuren incl. transparant). Basis = `sprite_r3/vuurduivel_r3.png`.
**Vel:** `vel.png` = r5 8× | r3 8× | model op dezelfde schaal; gezicht 16× (model links, r5 rechts, zelfde raster); 1× en 2× op licht en donker.
**Script:** `wijzig_r5.py` (r3-raster + benoemde reparaties) → `raster_r5.txt` → `bouw.py`. Elke pixel met reden in `wijzigingen_r5.txt`.
**Diff t.o.v. r3:** 66 px. Silhouet (alpha) 4 px: (14,22) hoornpunt, staartstam (44,46)/(46,46)/(47,45).
Palet: index 14 (mondbruin, ongebruikt) = hoornrood (190,45,46), index 15 = hoornlicht (233,100,94); beide gemeten in het model (bb2d2e / e8645f).

## A. Glimpje in de pupil (Jordi)
**Studie Gen 3 (`anim_front_gba.png`, 8–12×):** het glimpje zit in Gen 3 meestal bovenin (Pikachu, Marill, Smoochum). Met een glimpje onderin de pupil: **Taillow** (pupil ±3×3, glimpje 1 px linksonder, aan de rand van de pupil), **Furret** en **Electrike** (pupil ±3×3, glimpje in de onderste rij, zwart erboven en opzij), **Mudkip** (kleine pupil 2×3). De pupil is daar steeds ≥ 2×2 zwart rondom het glimpje; het wit raakt het oogwit nooit.
- Rechteroog: glimpje **(24,33)**, de linkeronderhoek van de pupil (neuskant). Dat is ook precies de plek van het glimpje in het model (33.0–33.1, x24b). Buren: zwart boven en rechts, d onder en links; raakt het oogwit niet.
- Linkeroog: glimpje **(18,34)**, de rechteronderhoek van de pupil (neuskant). Buren: zwart boven en links, d rechts, m onder; raakt het oogwit niet.
- Pupil 1 px groter in de donkere vlaktint d, (23,33) en (19,34), zodat het wit IN de pupil leest en niet als los wit vlekje. Het model heeft daar een donker randje (33.0 x24a; 33.1 x19a/34.1 x18b).

## B. Keurder-MOET (keuring_r3)
1. **Ogen V-lid + amandel**
   - Rechteroog: het lid volgt de modelwenkbrauw, die schuin naar de neus zakt: (25–26,29), (24–25,30), (23–27,31). Het oude vlakke lid op rij 29–30 rechts is weg.
   - Rechteroog: oogwit (26–28,32) + (27–28,33), dus 5 px in plaats van 7. Rij 31 is lid, zoals de lidlijn van het model op 31.0.
   - Linkeroog: het lid stijgt naar buiten. (16,30) is erbij, dus het lid loopt (15–16,30) → (15–18,31) → (18–19,32).
   - Linkeroog: oogwit (16–17,32) + (16,33), 3 px. (16,34) werd d, zodat het wit een amandel onder het lid is. De pupil zit aan de neuskant.
   - (26,28) blijft m. Anders loopt de wenkbrauw vast aan de onderrand van de hoorn (in het model zit daar een halve px tussen).
2. **Mond**
   - Gemeten in het natieve raster: de mond is op rij 37/38/39 6/5/3 breed, met diagonale zijkanten. Bovenrand en U-onderkant staan in r3 al op modelmaat, dus die zijn niet veranderd.
   - Linker mondhoek omhoog via het lachkuiltje van het model: (19,35) zwart (model 35.0 x19b).
   - KAN: de losse l-pixel (20,35) wordt m.
3. **Tanden: GEMETEN, het model wint van de keurder**
   - In het model is de grote tand **rechts**: x24b–25a, y36–37, ±11×9 modelpx.
   - Het kleine tandje staat **links**: x19b–20a, y37, ±8×8 modelpx.
   - r3 had dit al goed: (24,36–37) groot, (20,37) klein. Niet omgedraaid.
   - (25,37) r wordt R: het mondinterieur naast de tand is donkerrood, zoals het model.
4. **Hoorns:** de kegels zijn per pixel uit het model gehaald (2×2-cellen van het natieve raster), met eigen hoornrood/hoornlicht in plaats van haar-r en tong-p.
   - Links: punt (15,22). (14,22) is weg, zodat het één punt is. Lichte kant h links, zwart aan de haarkant (16,23), (17,24), (18,25), en voet (15–18,26–27).
   - Rechts: punt (26,21). Basis 3 breed (25–27, 24–26), zwart rechts en onder (rij 27 = modelrand 27.0), links bovenaan R (model).
   - Zwart aan de schaduw/haarkant en donkerrood R aan de lichtkant volgen het model en de Gen 3-selout-regel.
5. **Haar**
   - (20,19) zwart wordt R.
   - Rechts: vlamtong 2 loopt nu als één tong door naar linksonder (34–35,27) O, zoals het model. (36,27) wordt r, de schaduw tussen tong 2 en 3, dus geen O-r-O-r meer op rij 27.
6. **Staartpunt:** beide lobben hebben een schone R-onderrand: links (43,44)–(44–45,45), rechts (49,44)–(47–48,45). Inkeping (46,44) R. De stam komt in de inkeping aan, (46,45) zwart, en loopt via (45–46,46) naar beneden. (44,46) is weg, dus de stam hangt niet meer aan de linkerlob.

## C. KAN
Alleen (20,35) (zie 2). Torso, broek en hoef zijn niet aangeraakt.

## Pixels die niet uit het model komen
- Glimpjes en de d-pixels (23,33) en (19,34): Jordi's wens. De plek van het rechterglimpje valt wel samen met het model.
- Leden 2 px dik (Haunter-techniek uit r3).
- Hoornpunt links 1 px, (14,22) weg: punt i.p.v. twee platte R's.
- Staartpunt: de toegestane schoppenpunt.
- Mondinterieur rood i.p.v. mondbruin (uit r3; kleur mag afwijken).

## Zelf gezien (1×–3×)
Het gezicht leest als ondeugende lach: twee schuine ogen in een V, met wit en een pupil met glimpje, plus een open mond met een grote tand rechts. De hoorns zijn nu twee duidelijke rode kegels, los van het haar.
Twijfel voor de keurder: het rechteroog is kleiner dan in r3 (5 px wit, wat de modelmaat is). Op 1× zijn het smalle, samengeknepen ogen.
