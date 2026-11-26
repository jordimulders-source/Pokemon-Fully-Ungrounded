# Keuring sneeuwmonster r2 (onafhankelijke keurder, 26 nov)

Eerst blind geoordeeld (model-bbox op dezelfde schaal naast r2 en r1 op 12×, 1× naast elkaar, Snorunt/Spheal `_gba` en Skinguin op 4×), pas daarna NOTITIES.md gelezen.

## Oordeel: BIJNA

**Eis 1, trouw aan het model: ja.** Silhouet tegen het model (model-bbox met BOX naar 28×42): 6 px alleen-sprite, 1 px alleen-model, allemaal op de rand. Tintverdeling per pixel volgt de modelhelderheid (de horizontale schaduw onder de kop, de sikkel rechts, de donkere linkerrand van het lijf en de pluklijntjes (L 123–150 in het model) staan er echt in). Knopen: 4×5 en 4×4, zelfde vorm als het model (smal topje, glans 8 bovenaan). Niets toegevoegd of weggelaten. De mond staat nog open (SPEC).

**Eis 2, Gen 3: ja, op één plek na.** Sneeuwtinten 249/228/195 + lijn 118 + zwart 32: stappen 21/33, zoals Snorunt (235/213/180) en Spheal-buik (255/230/213/196). Zwart aan de schaduwkant, blauwe selout links/boven, binnenlijnen in de donkerste sneeuwtint en taps. Het ene zwarte pixel (27,15) op de lichte kant staat ook zwart in het model (natief (41–42,22–23) = L 6–8, de spleet onder het linkerbolletje), dus terecht. Op 1× leest hij als een Gen 3-sprite naast Snorunt.

**Volume:** de kop heeft nu een echte sikkel (5 → 4 → 3 rechts, buigt mee met de kop) en het lijf een bolling midden-links met sikkel rechts/onder; dat is beter dan r1 (kop 5 → 3 zonder overgang, lijf bijna effen 5). **Eén fout:** onder de kop heeft de gauss-verzachting de lichte bolling weggevreten. Het model is op rij 27–29 licht (L 238–243), r2 maakt er middentint (4) van; daardoor wordt de nekschaduw een rechte horizontale band van 4 rijen (rij 28–31) in plaats van de ronde onderkant van de kop. r1 had hier de modeltinten.

**Ogen:** lezen als donkere steentjes, behalve links: de "glans" (23,23) is gewone sneeuw (5) en raakt het witte gezicht, zodat het oog een hap uit de bovenkant krijgt en met (23,22) schuin/boos leest.

**Sneeuwpluk:** leest op 8× als middenbol met twee bolletjes (lijntjes uit het model); op 1× als kuifje, zoals het model op 1× ook. Goed genoeg; zie optionele punt 3.

**Oogvariant: LB_RB (= r2).** Gemeten op het model (BOX naar spritegrootte): linkeroog donker op x23–24 (y23–25), x22 is al half sneeuw; rechteroog donker op x30–32 (y23–26), x33 is sneeuw (L > 212). LA voegt (23,23)/(22,24) toe en RA (33,24)/(33,25): beide een kolom breder dan het model; RA leest op 12× bovendien als plusje. LB_RB volgt het model het best.

**r1 of r2 qua lijfvolume:** r2, mits reparatie 1 (dan heeft r2 overal het betere volume en de kin weer de modelvorm van r1).

## Reparaties
1. **Kin/onderkant kop: neem de tinten over uit het model (= r1), 4 → 5:** rij 27: (22,27), (23,27), (33,27), (34,27); rij 28: x23–26 en x29–33; rij 29: x25–32. Rij 30–31 (de schaduw 3) blijven. Daarmee buigt de lichte bolling weer tot rij 29 door en wordt de nekband 2 rijen in plaats van 4.
2. **Linkeroog, tintkeuze:** (23,23) 5 → 8 (de steenglans-tint van de knopen), zodat het oog één rond steentje is zonder hap; vorm verder ongewijzigd.
3. *(Optioneel, tintkeuze, Jordi/Claude beslist)* pluklijntjes taps laten eindigen zoals in het model (eindpixels daar L 134–167): (31,14), (33,14) en (28,17) van 2 → 3. Op 8× lezen (31,14) en (33,14) nu als twee puntjes onder de middenbol.

Na 1 en 2: PASS wat mij betreft. Niet veranderen: silhouet, knopen, rechteroog (incl. witte glans (31,24), staat zo in het model), armlijnen, voetjes.
