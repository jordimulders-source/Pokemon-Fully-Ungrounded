# Coathief: kleursprite ronde 5 (klauwen aan de staande verre voorpoot)

Basis: ronde 4. Het silhouet is nu `silhouet/ronde3.txt` (1333 px). Het verschil met ronde 4 zit alleen in de zone x 18–26, y 57–62.

## Bestanden
- `coathief.png`
- `vel.png`
- `uitsnede.png`
- `r4_vs_r5_voorpoten.png`: beide voorpoten op 8×, ronde 4 naast ronde 5, op licht en op donker.
- `voorstel_silhouet_klauw2.png`: mijn voorstel voor een kleine silhouetwijziging, alleen als schets (zie "Eerlijk").
- `bron/`:
  - het blok "ronde 5" staat onderaan `reparaties.txt`;
  - `diff_r4.py` is de diff tegen ronde 4;
  - `bouw.py` en `controle.py` werken met `silhouet/ronde3.txt`; de klauwzone in `controle.py` loopt nu tot x 25.

## Bewijs
```
controle.py: pixels 1333 | silhouet 1333 | alpha-diff 0 | open randen 0 | losse pixels 0
diff_r4.py:  zone klauwen verre voorpoot (x 18-26, y 57-62)  14 px | buiten de zone: 0
```

## Wat er staat
- **Aanzet:** de donkere tenen van de voet (26,59), (25,60) en (24,61) blijven. (24,60) is ook teen (m).
- **Klauw 1 (boven):** een diagonale haak van de teen naar linksvoor-onder, met:
  - kern c en glans w op (24,59);
  - (25,59) n bij de teen;
  - (21–22,60) c, met de schaduwkant (23,60) x;
  - (20,61) n en de punt (19,61) x.
- **Klauw 2 (onder):** (22–23,61) zijn m, als donkere teenvoet onder klauw 1. Ze scheiden de twee klauwen. De klauw zelf ligt op de grond: (22–23,62) c, met de punt (21,62) x.
- De klauwtjes zijn gedempter dan aan de opgetilde poot: één glans en meer n en x.

## Getoetst (1× en 8×, licht en donker)
Ik heb drie versies geprobeerd:
- **klauw 2 als blok** `cc` / `xxx`: las als een brokje;
- **klauw 2 als dambord** `xc` / `xcx`: las als een kruimel;
- **de huidige versie:** een donkere teenvoet met een lichte klauw op de grond.

**Klauw 1** leest op 8× en 1× duidelijk als een klauw aan de voet, op licht en op donker.

## Eerlijk
- **Klauw 2 leest op 8× als een tweede klauw op de grond. Op 1× is hij een kleine lichte streep onder klauw 1**, die vooral als "meer klauw" leest, minder als een aparte tweede haak.
  - De oorzaak ligt in het silhouet: klauw 2 (22–23,61) ligt direct onder klauw 1 (21–23,60), zonder lucht ertussen.
- **Voorstel voor Claude** (silhouet, 3 px): haal (22,61) en (23,61) weg en voeg (24,62) toe.
  - Dan ligt klauw 2 als haak onder de teen langs de grond, (24,62) → (21,62).
  - Er is dan een rij lucht tussen de twee klauwen.
  - Op 8× leest dat als twee evenwijdige klauwen (schets in `voorstel_silhouet_klauw2.png`, rechts).
  - Bevriest Claude dit, dan kleur ik het in een paar pixels na.

## Les
- **Twee klauwen van 1–2 px boven elkaar lezen pas als twee** als er een rij lucht of een donkere teen tussen zit. Een donkere scheiding binnen het silhouet helpt, maar lucht werkt beter.
