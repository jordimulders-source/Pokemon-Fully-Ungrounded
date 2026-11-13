# Charlatan-Alakazam: kleur r12b (rechterbovenarm duidelijker)

Basis: `basis_r12.txt`. In r12 was de grijze rechterbovenarm op 8× niet te zien. Jordi: "rechts dan ook he grappenmaker, bovenarm".

Bouwen: `python3 r12b.py`, daarna `python3 vel.py`. Silhouet gelijk (alpha-diff 0), pixeldiff alleen in x33–41, y27–35.

## V1: arm 3 px (15 px gewijzigd)
- De arm loopt over x37–39, rij 29–32, met de elleboog op (39–40,33). Licht linksboven: a (37–38,29) en (37,30), daaronder b en rechts c.
- De nieuwe linkeromlijning ligt op x36 (rij 29–31) en (37,32), (38,33).
- **Om zwart lijf tussen front en arm te houden** is het witte front op rij 29–31 1 px smaller gemaakt: (34,29–31) is van w naar o gegaan en (35,29–31) van o naar k.
  - Zo blijft er 1 px zwart (x35) plus omlijning. Dat raakt het witte front, maar alleen binnen de toegestane zone.
  - Rij 32–35: zwart (36,32–33), (37,33–34) zoals voorheen.

## V2: breedte zoals het model (7 px gewijzigd)
- Gemeten met `q.py`: in het model is de arm x37–38 op rij 29, x38–39 op rij 30–31, x39 op rij 32 en x40 op rij 33. Er loopt een lijn op x37 (rij 30b–31). Dat is de vorm van r12.
- Alleen lichter gemaakt voor contrast: a (37–38,29) en (38,30), daarna b.
  - Het model heeft hier D/B. De afwijking naar a is gedaan om contrast te krijgen.

## Controle
- Beide varianten: alpha-diff 0, open randen 0, losse o 0, geen nieuwe clusters < 3 px.

## Zwak punt
- V2 blijft 2 px breed; op 8× zie je hem nu wel, maar smal.
- V1 leest duidelijker als arm, maar kost 1 px wit front op rij 29–31.
