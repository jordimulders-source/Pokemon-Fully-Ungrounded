# Coathief: kleursprite ronde 5b (klauw 2 van de staande voorpoot)

Basis: ronde 5, op het aangepaste silhouet `silhouet/ronde3.txt` (1332 px). In het silhouet zijn (22,61) en (23,61) weggehaald en is rij 62 nu x 21–24.

## Bestanden
- `coathief.png`
- `vel.png`
- `uitsnede.png`
- `r4_r5_r5b_voorpoten.png`: beide voorpoten op 8× en de hele sprite op 1×, ronde 4, 5 en 5b naast elkaar, op licht en op donker.
- `bron/`:
  - het blok "ronde 5b" staat onderaan `reparaties.txt`;
  - `diff_r5.py` geeft het verschil met ronde 5;
  - `controle.py`.

## Bewijs
```
controle.py: pixels 1332 | silhouet 1332 | alpha-diff 0 | open randen 0 | losse pixels 0
diff_r5.py:  zone klauw 2 (x 18-26, y 59-62)  3 px | buiten de zone: 0
```
De 3 px zijn de twee pixels die uit het silhouet zijn gehaald, (22–23,61), en de nieuwe (24,62).

## Wat er staat
- Klauw 2 is een haak onder de teen langs de grond: (24,62) n bij de teen (24,61), dan (22–23,62) als crème kern c, en de punt (21,62) in x.
- Tussen klauw 1 (y 59–61, diagonaal) en klauw 2 (y 62) zit nu een rij lucht.

## Toets (1× en 8×, licht en donker)
- Op 8× zijn het twee aparte klauwen aan de voorkant van de voet, de ene diagonaal en de andere langs de grond, allebei vast aan de donkere tenen.
- Op 1× zie je aan de staande voet twee kleine lichte klauwstreepjes, net als de twee lange aan de opgetilde poot.
- Het brokje of de kruimel van ronde 1 en 5 is weg.
