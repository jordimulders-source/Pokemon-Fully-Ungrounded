# Coathief: kleursprite ronde 6 (beide voorpoten opnieuw, silhouet `silhouet/ronde4.txt`)

Basis: ronde 5b. Jordi heeft het nieuwe silhouet goedgekeurd ("ja nu klopt ie"): de opgetilde poot zit compact onder de kin, zoals op de onderlaag.

## Bestanden
- `coathief.png`
- `vel.png`
- `uitsnede.png`
- `onderlaag_r5b_r6_voorpoten.png`: de voorpoten op 8×, met de onderlaag, ronde 5b en ronde 6 naast elkaar, op licht en op donker, plus de hele sprite op 1×.
- `bron/`:
  - het blok "ronde 6" staat onderaan `reparaties.txt`; rijen 53–62 zijn daar over x 8–33 volledig met de hand herschreven;
  - `diff_r5b.py` geeft per zone de verschillen met 5b;
  - `controle.py`.

## Bewijs
```
controle.py: pixels 1321 | silhouet 1321 (ronde4.txt) | alpha-diff 0 | open randen 0 | losse pixels 0
diff_r5b.py: zone voorpoten (x 8-33, y 50-62)  70 px | buiten de zone: 0
```

## Wat er staat
- **Schouder en bovenarmen (y 50–52):** ongewijzigd uit 5b, inclusief de overgang naar de roodbruine schouder.
- **Opgetilde nabije poot (y 53–56):** in de nabije tinten.
  - lichtkant y met een Y-hooglicht op (20,54), en k aan de schaduwkant;
  - de pols krult: bij y 56 schuift het licht naar (21,56);
  - (20,56) is k als donkere naad tussen de klauwaanzetten.
- **Twee hangende klauwen:** crème kern c, w-glans op (17,58) en (21,58), x aan de schaduwkant (rechts) en op de punt.
  - klauw 1: (17–19,57), (16–18,58), (16–17,59), (16,60);
  - klauw 2: (21–23,57), (20–22,58), (20–21,59), (20,60).
- **Staande verre poot (y 53–58):** in de schaduwtint, met de lichtkant y links en een knik bij de pols (y 57–58). De voet (y 59–61) is plat, met een lichte bovenkant, donkere tenen (27,59) en (25,60) en een k-onderrand.
- **Twee gedempte klauwtjes aan de verre voet:**
  - klauw 1, diagonaal: (24,59) c, glans (25,59) w, (26,59) x; dan (23,60) c met x op (22,60) en (24,60);
  - klauw 2, onder de teen langs de grond: (22–23,62) c, (24,62) n en de punt (21,62) x;
  - tussen de twee zit een rij lucht.

## Toets (1× en 8×, licht en donker)
- Op 1× zie je twee donkere voorpoten. De opgetilde zit compact onder de kin met twee hangende lichte klauwen; de staande voet heeft twee kleine lichte klauwtjes.
- Geen brokjes.
- De stand komt overeen met de onderlaag.
- Ik zie geen zwak punt.
