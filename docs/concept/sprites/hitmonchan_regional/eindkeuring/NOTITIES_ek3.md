# ek3: linkeroog zoals in het model (puntje rechts)

Jordi (letterlijk): "het enige wat nog niet helemaal vertaalt is het linkeroog, misschien door een puntje rechts toe te voegen zoals in het model?"
Linkeroog = het oog links in beeld (het verre oog, tussen kuif en opgeheven arm). Het grote rechteroog is niet aangeraakt.

**Resultaat:** `ek3.png` (64×64, geïndexeerd, dezelfde 7 kleuren + transparant), `ek3_8x.png`, `vel3.png` (ek2 8× | ek3 8× | model; close-up van beide ogen op 16× naast het natieve model; 1×/2× op licht en donker), script `ek3.py` (asserts: oude waarde, modelwaarde, linkeroog = model, silhouet gelijk, gezichtszone rij 18–26 × x33–43 gelijk, geen nieuwe kleur), log in `ek3_log.txt`.
**2 pixels gewijzigd, alleen tint. Silhouetdiff 0.**

## Wat het model laat zien (natief_q, cel rij/kol)
Het linkeroog ligt in kol 23–26 × rij 26–28 (net links van de 1-op-1-zone, dus in het ±0,75-deel):
```
        k23 k24 k25 k26
  r26    4   7   1   6
  r27    2   7   2   2   <- k26 = het puntje rechts
  r28    2   6   2   5
```
Donkere rand links (k23), oogwit (k24), pupil (k25, bovenaan navy) en rechts daarvan één donkere pixel (k26 r27): het puntje.

## Wat de sprite had (ek2, x29–32 × rij 20–22)
```
         x29 x30 x31 x32
  r20     4   7   2   6
  r21     2   7   2   5
  r22     2   6   2   5
```
Kol 23, 24 en 25 stonden er al (x29, x30, x31). Kol 26 viel weg in de verkleining (x32 neemt vooral kol 27), en daarmee het puntje. De pupil was bovenaan 2 in plaats van navy (x31 is half kol 25, half kol 26).

## Gezet (x,y oud→nieuw)
- (32,21) 5→2: het puntje rechts (model k26 r27 = 2).
- (31,20) 2→1: pupil bovenaan navy (model k25 r26 = 1).

Daarmee staat het linkeroog (x29–32 × rij 20–22) 1-op-1 gelijk aan het model (k23–26 × r26–28); `ek3.py` controleert dat.

## Ter info
- Wil Jordi alleen het puntje, dan gaat (31,20) terug naar 2.
- Linksboven het oog heeft het model nog een navy cel (k22 r26, de kuifrand die schuin naar het oog loopt). In de sprite valt die in x28/x29 rij 20 (nu 7 en 4) en is er een gat in die diagonaal. Niet gedaan, want dat hoort bij de kuifrand en niet bij het oog. Optie: (28,20) 7→2.
