# Onweerswolk-Swablu frontsprite, ronde 3

Jordi over r2: "hoofd is nog steeds blurry, evenals de belijning van de bovenste donkere wolk en de voelsprieten, maar je hoeft alleen nog maar kleur, belijning, schaduw te fixen".
Bestanden: `swablu_r3.png` (64×64, geïndexeerd, index 0 transparant, 14 kleuren incl. transparant), `swablu_r3_8x.png` (op wit), `vel.png` (r3 | r2 | model op 8× / close-ups 12× kop en sprieten naast het model, gemaakt met `ZONES=kop python3 gereedschap/vel.py ...` / 1× op 4 achtergronden + model 1×), `bouw.py` (bouwt op `sprite_r2/swablu_r2.png`).
**Silhouet bevroren:** alpha-diff met r2 = 0 (`bouw.py` weigert elke wijziging buiten het silhouet). Alleen kleur, lijn en schaduw.

## Wijzigingen t.o.v. r2: 59 px
**Kop (29 px)**
- Omlijning boven (6): (24,24) (25,24) (26,23) (30,24) vogel donker → zwart; (23,25) wolk → zwart (diagonaal (22,26)-(23,25)-(24,24)); (24,25) wolk midden → kop midden (model v2w8, rand van de bol; 1 px om de lijn strak te houden). Nu één zwarte ring zoals het model.
- Lijn links van snavel en kin (5): wisselde zwart/midden/diep/zwart. (21,29) (21,30) (20,32) → zwart; (20,30) (20,31) → wolk licht zoals de bol ernaast (model = bol).
- Snavelrand (5): (22–25,27) en (26,28) → zwart. De snavel heeft nu een gesloten zwarte rand (model: zwarte rand om de snavel); wit raakte eerst de kop zonder lijn.
- Los zwart onder de snavel (1): (23,33) → kop midden (model K2v8 = kin).
- Onderrand kop/onderwolk (12): rij 37 x23–33 wisselde vogel donker/diep/midden/zwart en is nu één lijn wolk diep (model: donkergrijze rand tussen lijf en onderwolk). (31,36) (32,36) diep → vogel donker (lijf, sikkel onderaan). De V-inkepingen zijn nu één pixel diep op hun modelplek: (28,38) en (33,38). (29,38) → wolk midden.
- Tonen binnen de kop: de band-meerderheid zat al in r2 (vogel licht/midden/donker volgens modelbanden). Hooglicht linksboven en sikkelschaduw rechtsonder blijven.

**Bovenste donkere wolk en wolkranden (15 px)**
- Lijn kop/donkere wolk (1): knik weg, (35,27) zwart → wolk diep (vulling). De lijn loopt nu (33,26)(34,27)(34,28)(35,29)(35,30)(36,31).
- Bovenrand donkere wolk (3): (37–39,26) diep → zwart. (36–40,26) is nu één zwarte lijn; de vulling is één tint wolk diep.
- Rand lichte bollen tegen donkere wolk/lijf (8): de randpixel van de bol → wolk midden (selout van de lichte bollen; het model heeft daar een grijze 'D'-rand). Wit lag eerst direct tegen diep/vogel.
- Rand bollen/onderwolk rechts (1): (38,39) diep → zwart (gat in de zwarte lijn).
- Rand linker bol/onderwolk (2): (16,35) → bol licht, (16,36) → diep. De lijn loopt nu als één diagonaal in wolk diep: (19,35)-(15,36).

**Voelsprieten (6 px)**
- Linker steel: (25,18) vogel donker → vogel midden. De steel is nu één kleur als 1 px diagonaal (25,18)-(27,23), met zwart aan de schaduwkant (27,21) (28,22) (28,23).
- Rechter steel: 1 px diagonaal in vogel midden (33,18)(32,19)(31,20)(30,21)(29,22). Zwarte onderrand (32,20) (33,20) (31,21). De bestaande pixels aan de lichtkant ((31,19) (30,20) (29,21), silhouet bevroren) zijn selout vogel donker.

**Vonken (9 px)**
- Geel + één schaduwtint: per pixel stemmen de gele modelpixels (oker L<180 tegen geel), meerderheid wint. Oker staat nu alleen waar het model oker heeft. Lichtgeel komt niet meer voor (index 12 ongebruikt in het palet).

## Controle
Alpha-diff met r2 = 0. Per materiaal ≤ 3 tinten + lijn/selout. Wolk: lichte bollen wit/licht + selout midden; onderwolk midden/donker/diep; donkere wolk diep + zwart. Vogel licht/midden/donker. Vonken geel/oker. Snavelwit + glans.

## Twijfels
- **Snavel** heeft nu een volledig gesloten zwarte rand (boven 4 px). Op 1× leest dat sterk, bijna als een ring. Het model heeft daar wel een zwarte rand, maar dunner.
- **Rechter steel:** door het bevroren silhouet staat aan de lichtkant een rij vogel donker. Als 1 px is hij dus niet helemaal kaal; dat oplossen kan alleen met een silhouetwijziging (3 px weg).
- **Linker vonk** is klein (10 px) en voor de helft oker.
