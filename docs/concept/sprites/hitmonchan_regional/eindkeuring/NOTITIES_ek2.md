# ek2: controle rechte lijnen (krabbel_ek1) + wachtvuist los van de schouder

Jordi (letterlijk): "super vet, dit leest allemaal als rechte lijnen, ik zeg niet dat het fout is gezien het een ijssculptuur is, maar kijk of het klopt".
Extra punt van Jordi (letterlijk): "en de rechtervuist moet aan de bovenkant nog iets duidelijker los van de schouder, maar dat is denk ik vooral kleurtinten en een lijn".

**Resultaat:** `ek2.png` (64×64, geïndexeerd, dezelfde 7 kleuren + transparant), `ek2_8x.png`, `vel2.png` (ek1 8× | ek2 8× | model; 1×/2× licht en donker; diff), script `ek2.py` (asserts: silhouet gelijk, oogzone rij 18–26 × x33–43 gelijk, geen nieuwe kleur), log per pixel in `ek2_log.txt`.
**10 pixels gewijzigd, alleen de tint. Silhouetdiff 0, gezicht niet aangeraakt.**

## Meting
- De krabbel is ek1 op 9,97× (offset x −69,5, y +10; gefit op de spritekleuren). De groene lijnen zijn per lijn omgerekend naar spritecoördinaten.
- De sprite is gelegd op het natieve model (`sprite/natief_q.npy`, 50×81) via dezelfde stuksgewijze afbeelding als `meet.py`. Rijen 24–32 en kolommen 28–38 staan 1-op-1, de rest op ±0,75 (rijen onder 32 op 0,776).
- Per lijn zijn de run-lengtes in model en sprite geteld. Een run van n modelcellen hoort ±0,75·n spritepixels te worden.

## Per groene lijn
| # | waar (sprite) | modelmeting | oordeel | gedaan |
|---|---|---|---|---|
| 1 | linkerrand kuif/hoofd, x28 r13–19 (7 px, tint 2) | kol 21 r17–25: 9 cellen recht verticaal (r17 als 4, daarna 2). Daarboven een schuin stuk kol 23→22→21, dat in de sprite ook schuin staat ((29,11), (28,12)). 7×0,75 + 2 (1-op-1) = 7,25 | **recht in het model** | niets |
| 2 | binnenrand opgeheven onderarm, x24 r18–19, x25 r20–26 (7 recht) | een trap kol 16 r24–25, kol 17 r26–27, kol 18 r28–32, kol 19 r33–37 (2/2/5/5). De rijen staan hier 1-op-1, dus de langste modelrun = 5 px. Kol 17 en 18 vielen in de verkleining allebei in x25, waardoor er 7 recht werden | **niet recht: fout van de verkleining** | trap 4/5/4: x24 r18–21, x25 r22–26, x26 r27–30. (24,20), (24,21): 4→1 (M_donker 1); (25,20), (25,21): 1→2 (model kol 18 = 2, M_gem 2). De onderarm wordt daar 1 px smaller, zoals in het model (dat vernauwt ook op r26–27: 6 en 5 cellen) |
| 3 | kinlijn horizontaal, r29 x32–37 (6 navy) | r36 kol 27–32: 6 cellen navy recht (→ 5,75 px) | **recht in het model** | niets |
| 4 | onder de kin, r30 x32–39 (8× tint 2) + verticaal x39 r30–34 (2) / x40 r32–34 (1) | r37 kol 27–34: 8 cellen 2 recht (→ 7,75 px). Verticaal kol 34 r37–43: 7 cellen 2 (→ 5,4), kol 35 r40–43: 4 cellen navy (→ 3,1) | **recht in het model** (het "schuine stuk" in de krabbel is deze rechte hoek) | niets |
| 5 | verticaal links van de wachtonderarm/heup, x42 r35–43 (9 px 1/2) | kol 37 r44–54: 11 cellen recht (→ 8,5 px). Op r51 zit één witte glanscel (7) in de lijn, aan alle vier kanten omringd door navy | **recht in het model**, op één glanspunt na | niets. Optie voor Jordi: (42,41) 1→7 neemt die glans over (oppervlak 7 = 0,66, lijn = 0,63). In de sprite is dat een losse witte stip, helemaal ingesloten door navy |
| 6 | riem bovenrand, r37 x25–34 (10 navy recht) | r46: navy kol 18–20, dan **3,4,3,2** (kol 21–24, een lichte inkeping), dan navy kol 25–29 (5 cellen → 3,75 px). De langste modelrun op deze rand is 8 cellen (r47, → 6,25 px) | **niet recht: de verkleining had de inkeping dichtgezet** | (28,37) 1→3, (29,37) 1→3, (30,37) 1→2: de inkeping van het model. Nu navy 3 / inkeping 3 / navy 4 |
| 7 | riem onderrand, r38 x28–37 (10 navy) | r47 navy kol 21–28 + r48 navy kol 26–30 (trap omlaag op x31,5, maar r48 valt maar voor 0,2 in sprite-r39) + r47 kol 31–32 navy. De onderrand loopt dus doorlopend over x28–37 | **in het model doorlopend**. De trap valt binnen een subpixel | niets. Rij 37 en 38 vormen nu geen strak parallellogram meer, door de inkeping bij lijn 6 |
| 8 | rechterrand voorste voet, x19 r56–61 (6 navy) | kol 10 r70–76: 7 cellen recht verticaal (→ 5,4 px), daarna een stap naar kol 9 (r77 = sprite r61, valt nog in x19) | **recht in het model** | niets |

## Extra: wachtvuist (rechts) bovenkant los van de schouder
- **Meting:** de naad schouder/kubus is in het model één navy cel dik (r31 kol 38 → r35 kol 33). Aan de kubuskant ligt een band in tint 3 (r32 kol 38, r33 kol 37, r34 kol 36, r35 kol 35). Die naad en die band staan al in ek1. Het bovenvlak van de kubus is in het model licht: r32 kol 39–43 = 7, **r33 kol 38–45 = 6/7**. In ek1 was de rij onder het witte bovenvlak (r27 x43–45) 5, net als de schouder. Daardoor liep het linkerdeel van de kubus in tint door in de schouder. (43,27) was in de kale reductie r5 wel 6, maar is in r6 weggeontkorreld. M_gem zegt voor x43–45 6,6,6.
- **Gedaan:** (43,27), (44,27), (45,27): 5→6. Het lichte bovenvlak loopt nu tot tegen de naad, zodat de volgorde schouder 4/5 → navy → 3 → kubus 6/7 is. Er is geen nieuwe lijn bijgekomen: de navy naad + band 3 stond er al.
- **Niet gedaan (gemeten):** de bovenrand van de kubus (r25 x44–46, tint 4) is in het model (76,142,172), dichter bij 4 dan bij 3, en blijft dus 4. Vindt Jordi de bovenkant nog niet los genoeg, dan zijn er twee opties. (a) Die 3 px 4→3 zetten, als donkerder selout van de kubus (kleur mag afwijken van het model). (b) (41,26) 4→3 aan de schouderkant (M_gem 3), zodat de naad taps verdonkert.

## Samenvatting
Lijnen 1, 3, 4, 5 en 8 en de riem-onderrand (7) zijn **in het model ook recht**: dat is het ijssculptuur-ontwerp van Gemini, en ze zijn gelaten. Twee lijnen waren te recht door de verkleining. Lijn 2 (de onderarm, 7 recht, model max 5) is nu een trap. Lijn 6 (de riem-bovenrand, 10 recht) heeft nu de lichte inkeping uit het model terug. Bij de wachtvuist is het lichte bovenvlak terug tot tegen de naad met de schouder.
