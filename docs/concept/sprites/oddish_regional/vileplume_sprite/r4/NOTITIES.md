# Kelp-/anemoon-Vileplume frontsprite, ronde 4

Bestanden: `vileplume_r4.png` (gelaat B), `vileplume_r4_gelaatA.png`, `vileplume_r4_gelaatC.png`, `gelaat_varianten.png` (A/B/C naast het model), `kaal.png`, `bouw.py` (`python3 r4/bouw.py` vanuit `vileplume_sprite/`), `vel.png` (r4 8× | r3 8× | model 8× / close-ups 12× krater, anemoon VL, lijf+poten / 1×).
64×64, geïndexeerd 4 bpp, 16 paletplekken, index 0 transparant (transparency=0). Alle 16 plekken in gebruik: index 7 (was W1, kwam niet voor) is nu donkergrijs voor de krater, gemeten als mediaan van de neutrale modelpixels L 18–52 in de kom. Figuur x4–58, y1–62 (55×62).

## Reparaties (coordinator + Jordi over r3)
1. **Kroon + voet.** Kroonrand per anemoon per 20° gemeten: 95e percentiel van het tentakelmateriaal (R3 + R0), licht gladgestreken. Binnen de kroon de tussenkleur (R2, bij T R1). Onder de kroon (onderste helft) de voet uit de kale reductie (R2/R1 zoals in het model; tentakelresten → modelschaduw). Tussen kroon en voet een R0-lijn waar geen tentakelpunt ligt.
2. **Tentakels:** 9 per anemoon, bij elke anemoon hetzelfde opgebouwd. Richting = massamidden van de modeltentakels per sector. Onder lopen ze tot de kroonrand, boven en opzij tot de modelpunt (97e percentiel), daar steken ze uit. Taps: de eerste 30 % is 2 px breed (2e pixel aan de lichtkant), daarna 1 px. Doorlopende R0-lijn aan de schaduwkant. Tussen de tentakels is de tussenkleur te zien.
3. **Krater:** nette ovaal met de maten van het model. Buitenrand natief x82–118 y48–67 → zwart. Gloed natief x88–112 y53–60 → 3 rijen: bovenste rij roodoranje, oranje rand, geel hart. Lichtgrijze bovenrand. Bruine band direct onder de gloed. Donkergrijze onderwand. De keel eronder blijft de kale reductie.
4. **Linkerpoot: niet aangepast.** De middenlijn van het model is per spriterij gemeten. Kijkerslinks: y41 28,1 → knie y46–48 24,6 → y56–58 25,9 → voet y60 25,5. Kijkersrechts: van 34,7 gelijkmatig naar 40,0. Bij beide poten valt die lijn in r3 al binnen de middenpixel, en het model is onder de knie zelf vrijwel recht. Uit de meting blijkt dus niet welke poot "te recht" is of wat er anders moet. **Vraag aan Jordi:** welke poot, en wat wil hij zien (meer knik, schuiner)?
5. **Gelaat** (enige vrije afwijking). Het model heeft geen ogen, alleen een ondiepe U. Die bestaat uit twee donkere puntjes bovenaan (natief x86–87 en x94–95, y102–103) en een balkje eronder (x88–93, y104–105); in de sprite x25 en x29 op y33, balkje x26–28 op y34. Ik lees de twee puntjes als de ogen, maar dat is mijn lezing.
   - A = model (U, als r3).
   - **B (standaard)** = puntjes als ogen, 1×2 zwart zoals kleine Gen 3-ogen. Ten opzichte van A veranderd: (25,32) W4→zwart, (25,33) W0→zwart, (29,32) W4→zwart, (29,33) W0→zwart. 4 px; het balkje blijft.
   - C = B zonder balkje: (26–28,34) W0→W4. 7 px ten opzichte van A.

## Telling
- Ten opzichte van de kale reductie: 807 px. Anemonen 657 (mondjes 67, incl. ring), krater 57, lijf+armen 37, poten 56.
- Ten opzichte van r3: 492 px. Anemonen 431, krater 57, lijf+armen 4 (gelaat B), poten 0.
- Lijf en poten zijn bevroren op r3, behalve het gelaat; pixeldiff 0 is met een assert in `bouw.py` gecontroleerd.

## Toets
- 16 kleuren incl. transparant. Lichte kleur op de buitenrand: 0. Zwart 15,8 %.
- 2 zwarte pixels zonder lijnbuur: (35,28) is de grens VL/VR in de voet, (32,30) de grens anemoon/lijf. Bewust.

## Resterende twijfels
- De kroon van de voorste anemonen leest op 8× nog wat vlekkerig: de voet van de tentakels (2 px) en de R0-lijnen liggen dicht op elkaar. Tentakels van 1 px over de hele lengte ogen schoner (`python3 r4/bouw.py 0`), maar zijn dan niet meer taps.
- De achterste anemonen (L, T, R) hebben bovenaan nu punten, maar het silhouet is minder stekelig dan in het model.
- Of de ogen in B/C bedoeld zijn: zie punt 5.
- Linkerpoot: zie punt 4.
- Index 7 is hergebruikt voor donkergrijs; in een latere ronde kan de kale reductie W1 weer gebruiken, en dan klopt die index niet meer.
