# r5 checklist (zelftoets maker)
Basis r4. Bouw `bouw.py`; tuinbroekvorm gemeten op het model met `model_tuinbroek.py` (crème + zandkleurige lijnen in r10_k8 natief,
oppervlakteaandeel per spritepixel ≥ 0,5 = borststuk; lijnaandeel ≥ 0,3 = lijn); toets `overlay.py` → `overlay_tuinbroek.png`; runs/vlakken `../sprite_r4/meet.py`.

| Citaat | Toets | Uitslag |
|---|---|---|
| "ja als de tuinbroek niet zoals het model nagemaakt wordt qua vorm is de sprite niet geslaagd" | overlay modelomtrek borststuk + bandjes | model 164 px, sprite 164 px, afwijkend **0 px** (bandjes 0, borststuk boven 0, borststuk onder 0). Modellijnen (zoom onder de bolletjes, zijlijnen bandjes, zak, onderzoom): 46/46 px |
| "het moet gewoon een tuinbroekvorm zijn" | borststuk + bandjes + broek als aparte vormen | borststuk (model) los van de broek door een tailleband (F, 1 px, doorlopend) direct onder de modelonderzoom; rechts bruine romp tussen borststuk en arm; links ligt het borststuk in het model tegen de lijfrand (romp alleen x19, r34-37) |
| "A maar moet netter" / broek "puur inkleuren" | broek vanaf de taille tot de enkels binnen de bestaande buik/beenvormen | ja; benen, sikkels, manchetten = r4 |
| "geen rechte lijnen" | runs > 3 px | niet in de broek. Wel rechte runs die 1-op-1 uit het model komen: rand rechterbandje/borststuk kol 37 r31-36 (6), bovenrand midden r31 x30-34 (5), zoom r34 x26-33, zak r36 x26-33, onderzoom r42 x25-30 (+ band r43 eronder). Het model gaat hier voor; Jordi laten kiezen of die lijnen een ronding moeten krijgen |
| "Het moeten geen effen vlakken zijn" | schaduw 7/6/F | borststuk: modellijnen + sikkel op de rechterrand; broek r4 (sikkels dijen/scheen/kruis). Licht crème 4-buren: broek 262 px, borststuk 104 px (door zoom en zak in drie stroken). ±40 px-regel: niet gehaald |
| "het bovenlichaam moet geen pixelblur zijn" | per deel licht linksboven + één sikkel | rechterschouder: lichtvlak (5) linksboven r28-30, schaduwsikkel (3) langs de rechterrand, breder naar onder; plooi/armcontour/lichtvlak onderarm r4; linkerarm: licht ook rechts van de vouwlijn |
| kraag/gezicht/stam/potlood/staart/klep/silhouet diff 0 t.o.v. r4 | script | y<27 0, potlood 0, silhouet 0. Kraagzone 2 px: (36,30) crème→vacht en (38,30) lijn→crème, omdat het rechterbandje in het model daar ligt. Ook 3 zwarte bolletjespixels (23,31),(24,32),(33,32) → crème/lijn (model). Botst met "diff 0"; gekozen voor Jordi's modelregel |
| tanden wit, ogen Bibarel, neus rood | diff | 0 |
| techniek | palet, clusters | 15 kleuren + transparant; losse crèmepixels <3: (38,30) (modellijn topje bandje), (42,44) (r1) |

Per zone t.o.v. r4 (148 px, buiten zones 0): bandjes 14, borststuk 49, romp 3, tailleband 24, broek 21, rechterarm 34, linkerarm 3.
