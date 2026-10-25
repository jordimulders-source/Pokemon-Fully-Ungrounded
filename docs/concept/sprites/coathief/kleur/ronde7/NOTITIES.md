# Coathief: kleursprite ronde 7 (afwerking vóór de eindkeuring)

Basis: ronde 6g (Jordi's gum op 6f; Jordi is tevreden). Silhouet 6g = `silhouet/ronde7.txt`. Het nieuwe silhouet is `silhouet/ronde8.txt` (1323 px, netto 0).

Jordi letterlijk: "de onderkant van de staande voorste poot mag nog wat netter afgewerkt worden, iets minder recht, mag klein beetje naar achter buigen en de klauwen mogen iets netter afgewerkt worden".

## Bestanden
- `coathief.png`
- `vel.png`
- `uitsnede.png`
- `onderlaag_6g_7_voorpoten.png`: de voorpoten op 8×, met de onderlaag, 6g en 7 naast elkaar, op licht en op donker, plus 1×.
- `bron/`:
  - `raster.txt` is 6g als volle rijen; dat is de basis;
  - `reparaties.txt` bevat alleen ronde 7;
  - `silhouet_ronde8.py` maakt het nieuwe silhouet;
  - `diff_r6g.py` is de diff tegen 6g;
  - `bouw.py`, `controle.py` en `vel.py`.

## Bewijs
```
controle.py: pixels 1323 | silhouet 1323 (ronde8.txt) | alpha-diff 0 | open randen 0 | losse pixels 0
diff_r6g.py:
zone staande verre voorpoot (x 23-33, y 55-62)  24 px
zone klauwen (x 12-30, y 53-62)                 2 px
totaal 26 | buiten de zones: 0
bevroren gumrand x 31-32, y 48-54 en bovenarm/manchet y < 55: 0 px verschil
```

## Silhouet ronde 8 (ten opzichte van ronde 7)
- **Staande poot:**
  - eraf: (27,57) en (27,58);
  - erbij: (32,57), (32,58), (32,59) en (32,60).
- **Hangende klauwen:**
  - eraf: (16,58), zodat klauw A gelijkmatig taps loopt;
  - eraf: (23,57), zodat klauw B taps loopt.
- De lucht tussen de klauwen en tussen de klauwparen blijft.

## 1. Onderkant van de staande verre voorpoot
- **Buiging:** de onderpoot loopt vanaf de pols schuin naar achter tot een ronde hiel. Voorrand per rij: 27, 27, 28, 28; achterrand per rij: 31, 31, 32, 32, 32, 32, en de onderste rij 31. Zo draagt hij gewicht en buigt hij mee, zoals de voorpoten van Mightyena en Linoone. In 6g was het een rechte kolom op een platte voet.
- **Licht:** de lichtkant y volgt de buiging: x 28 → 29 → 30 en op de voet (30,59). De schaduw m en de k-rand liggen rechts.
- **Voet:** plat op de grond, met een k-onderrand (30–31,61) en een donkere teen (29,59–60) als aanzet van de klauwen.

## 2. Klauwen
Alle vier zijn op dezelfde manier opgebouwd: crème kern c, één glanspixel w, x aan de schaduwkant en op de punt.
- **Klauw A** (opgetilde poot, hangend):
  - linkerrand 19, 18, 18, 17, 17, 16, 16 (segmenten 1, 2, 2, 2);
  - rechterrand 20, 20, 20, 19, 18, 17, 16 (3, 1, 1, 1, 1);
  - glans (19,55), punt (16,60).
- **Klauw B** (opgetilde poot, hangend): rechterrand 23, 23, 22, 22, 21, 20 (2, 2, 1, 1), glans (22,56), punt (20,60).
- **Staande voet, bovenste klauw** (naar voren op de grond): kern (24–26,59), glans (25,59), naar de teen toe n, de onderzijde (25–28,60) x en de punt (22,60) x.
- **Staande voet, onderste klauw:** kern (24–27,61), glans (25,61), x aan de teenkant, punt (21,62) x. Lichter dan in de eerste poging van deze ronde, die als donkere balk las.

## Toets (1×, 8× en 16×, licht en donker)
- De staande poot buigt licht naar achter en staat met een platte voet op de grond. De klauwen liggen ervoor.
- De hangende klauwen zijn gladde, taps toelopende haken.
- Op 1× zijn het twee voorpoten met elk twee klauwen.
- **Tussenstap:** een eerste versie met een uitstulping (achterrand 31, 32, 32, 31) las als een knobbel. Die heb ik vervangen door de doorlopende schuine lijn tot de hiel.
- Ik zie geen zwak punt.
