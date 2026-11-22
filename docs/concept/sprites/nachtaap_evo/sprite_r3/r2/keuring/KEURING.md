# Keuring Moonkey r2 (19 nov, onafhankelijk, blind geoordeeld; NOTITIES pas daarna gelezen)
Vergeleken op 8×/12×/14× met het model (`kop_model_sprite_oud.png`, `lijf_model_sprite.png`), de oude sprite en Aipom, Mightyena, Absol, Linoone en Persian (`naast_gen3.png`). Indexen van `r2/normal.pal` (1 zwart, 2 selout, 3/4/5 paars schaduw/basis/licht, 6 lavendel, F blauw). Wissels: `wissels.py` (30 px, `python3 wissels.py ../anim_front.png uit.png` past ze toe op beide frames, met controle van de oude waarde); preview `voorstel_8x.png`.

**1. Trouw aan het model: PASS.** Eigen kale reductie (`natief_eigen.png`, raster 16 px vanaf 15): silhouet buiten de maan/het witte gezicht pixel-gelijk; pose, poten (4, voethoogtes in perspectief), kopvorm, linkeroor, staart en de drie rugwiggen staan exact op de modelplek. Afwijkingen alleen in de toegestane zones (ogen, maan, gezicht uit de oude sprite) en in kleur.
**2. Gen 3-techniek: PASS met kleine punten.** Selout 2 linksboven, zwart rechts/onder, geen open randen, geen lichte kleur op de buitenrand, binnenlijnen grotendeels in 2 die pas onderaan zwart worden (taps), verre voorpoot en verre achterpoot in 3. Paars gebruikt 3/4/5 + 6 als kleine lichtvlek (zoals oud).
**3. Dragonfly Cave-eindronde: goed, na reparatie 1–3 uitstekend.** Licht linksboven consistent (5 op rug en schouder, sikkel 3 rechts/onder). Stappen 5→4 = 37 (Aipom-niveau), 4→3 = 22 (smal, palet is bevroren). Leest op 1× op licht en donker.

| # | Prio | Zone, pixels | Probleem | Reparatie (van → naar) |
|---|---|---|---|---|
| 1 | midden | romp vóór de staartvoet: (37,31),(37,32),(37–38,33),(36–38,34),(36–38,35); (35,34),(34,35),(35,35) | Tweede 6-vlek links van de binnenlijn x39 (naast de 6-vlek bij de staartvoet, die van model + oude sprite is en blijft): twee lavendel vlekken met een lijn ertussen = rommelig, en direct links ervan 3 (licht → schaduw omgekeerd, 3 naast 6 slaat 4/5 over). | vlek 6→5; de drie 3-pixels 3→4. |
| 2 | midden | verre oor (23,39),(24,39) | Banding: 5/4 bovenin, dan een volle rij 3, dan weer 4 (y40–41). | 3→4 (3 blijft op x22 en x25 als rand). |
| 3 | midden | nabije achterpoot (36–39,49),(36–38,50),(37,51) | Dij 4 stopt op een rechte horizontale grens y48/49 en de hele poot eronder is egaal 3: plank, de lichtkant van de poot krijgt geen licht. | 3→4 (ronde overgang dij → poot, rechts blijft 3). |
| 4 | laag | kop/rug-naad (19,35),(20,35); (21,37) | Zwarte binnenlijn begint aan de lichtkant, met een L-hoekje (21,36)+(21,37)+(22,37). | (19,35),(20,35) 1→2; (21,37) 1→5. |
| 5 | laag | bovenrand rug (28,28),(29,28) | Donkere 3 direct onder de bovenlijn tussen de wiggen, terwijl eronder 5 staat (omgekeerd). | 3→5. |
| 6 | laag | staart (49,30) | Losse 2 binnen de staart (4-2-3). | 2→3. |
| 7 | laag | kaakrij (13,54) | 5-5-3-4-3 ruis; de oude sprite had hier 5-5-4-4. Technisch, binnen de kop. | 3→4. |

Ter info (geen FAIL): onderranden buik y54 (x28–35, x37–43) zijn recht, maar komen 1-op-1 uit het model. De lavendel vlek bij de staartvoet (x41–43,y33–36) bewust gelaten: model + oude sprite.
Na de NOTITIES: punt 1 en 3 vallen samen met de zones die de maker zelf noemde (6 bij de staartaanzet, dij/achterpoot); zijn afgeronde 3-sikkel boven de dij is goed, alleen de onderste rijen bleven plat.

**Eindoordeel:** PASS op trouw en techniek; nu goed, na wissels 1–3 (21 px) een uitstekende Gen 3-sprite, naast Aipom/Mightyena niet te onderscheiden in uitvoering. 4–7 zijn polish.
