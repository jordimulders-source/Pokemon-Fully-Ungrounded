# Coathief: kleursprite ronde 6b (voorpoten volgens de labelkaart van de onderlaag)

Basis: ronde 6. Silhouet `silhouet/ronde4.txt` (bevroren). Kleurindeling volgens `silhouet/labels_voorpoten.txt`.

## Bestanden
- `coathief.png`
- `vel.png`
- `uitsnede.png`
- `onderlaag_r6_r6b_voorpoten.png`: de voorpoten op 8×, met de onderlaag, ronde 6 en ronde 6b naast elkaar, op licht en op donker, plus de hele sprite op 1×.
- `kaart_vs_r6b.png`: de kaart naast 6b. Waar de kleur van het label afwijkt, zou een rode rand staan; er is geen enkele.
- `bron/`:
  - het blok "ronde 6b" staat onderaan `reparaties.txt` (rijen 50–62 over x 8–33 met de hand);
  - `diff_r6.py` geeft het verschil met ronde 6;
  - `kaart.py` maakt de kaartvergelijking en de uitsnede;
  - `controle.py`.

## Bewijs
```
controle.py: pixels 1321 | silhouet 1321 | alpha-diff 0 | open randen 0 | losse pixels 0
diff_r6.py:  zone voorpoten (x 8-33, y 48-62)  59 px | buiten de zone: 0
kaart.py:    afwijkingen van de kaart: []
```

## Wat er staat (per label)
- **v, vacht:** de roodbruine bovenarm en borst rechts naast de opgetilde poot (x 27–32, y 50–54), in d/b met een k-rand rechts. Rijen 48–49 waren al vacht of kin en zijn ongewijzigd.
  - (20–21,49) staan op de kaart als v, maar zijn de k-onderrand van de kin. Die blijft k; dat valt binnen de omlijning van de vacht.
- **N, opgetilde poot:** in de nabije tinten (y, Y, z, m, k).
  - Hij komt van onder de kin (y 50) en loopt compact omlaag tot de pols (y 54–56).
  - (27,53–55) is de achterkant van de onderarm, donker vóór de staande poot.
- **c, klauwen van de opgetilde poot:** twee grote hangende crème klauwen (y 54–60), gescheiden door een x-naad op x 20 (y 55–56) en daaronder door lucht.
  - glans op (19,55) en (22,56);
  - x aan de schaduwkant en op de punten (16,60) en (20,60).
- **F, staande poot:** in de schaduwtint, met de lichtkant y links en een knik bij de pols (y 57–58).
- **c, klauwen van de staande voet:** twee grote crème klauwen die naar voren op de grond liggen, zoals op de onderlaag.
  - **Bovenste:** (24–28,59), met de punt naar links op (22–24,60) en een glans op (25,59).
  - **Onderste:** (24–29,61), met de punt op (21–24,62) en een glans op (26,61).
  - Daartussen ligt een donkere x-band op (25–28,60).
  - Er zit een x-punt en x-rand tussen de klauwen van de twee poten, zodat ze niet samenvloeien.
  - Ze zijn iets gedempter dan aan de opgetilde poot: meer n en x.

## Toets (1× en 8×, licht en donker)
- Op 1× zie je twee voorpoten met elk twee lichte klauwen.
- De staande poot heeft zijn klauwen naar voren op de grond en lijkt daardoor te stappen.
- De hangende klauwen van de opgetilde poot zitten erboven en links ervan.
- Het geheel volgt de onderlaag. Geen brokjes; ik zie geen zwak punt.
