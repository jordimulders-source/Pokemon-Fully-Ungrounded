# Keuring r23 → r24 (16 nov, verse keurder)

**Oordeel: PASS (r24).** Vel: `vel.png` (8× r24 | r23 | r19 | model; 2× en 1×; koeienvanger 12×: r24 (< variant A) | < variant B | r23 | r19 | model).

## Bevroren
- r23 vs r20: 122 px verschil, allemaal binnen x2–26 / y45–57; **buiten de zone (x0–30, y44–60) diff 0** (script).
- r24 (`sprite_r23/fix.py`): 15 px, alleen in de zone; asserts: buiten de zone gelijk aan r23 én r20, geen nieuwe paletindex.

## Hoofdvraag (1×/2× eerst)
- **r23 vs r19: beter.** In r19 las de koeienvanger op 2× als vlekkerige grijze massa; in r23 staan er duidelijke platen, met een harde onderrand. Hij is wel iets drukker, met meer zwarte binnenlijnen, maar dat volgt het model (dat is zelf donker en vol).
- **Volgt Jordi's schets (lijnen2):** rechte linkerrand (x2) ja; "^" ja; ruit ja; "<" ja; rechte rechterrand met een hoekige onderhoek ja.
- **Fouten in r23:**
  - De rechterrand is dubbel zwart: x24 en x25 op y47–53. Op y46–48 is het zelfs een zwart blok van 3 breed (x24–27).
  - Na sluiten van (54,25) liep de onderhoek niet meer hoekig door.

## Reparaties r24 (15 px)
- **"<" van 5 naar 3 px** (Jordi: "3 pixels ipv 5"). Variant A blijft (22,50), (21,51), (22,52) (x,y). (23,49) wordt plaattint A, (23,53) wordt C. Variant B, de "<" één kolom naar rechts (`variant_B.png`, 21 px), staat ernaast. Ik koos A: die staat midden in de rechterplaat en verandert minder pixels.
- **Eén rechterrand op x25** (zoals r20). x24 wordt plaat (C, schaduwkant, bovenin B/A). (54,25) en (55,25) worden zwart, zodat de onderhoek hoekig is. Bovenhoek: een schuin stapje (47,27)-(48,26)-(49,25). Daarvoor zijn (47,24–26) en (48,24–25) plaattinten geworden.
- Geen nieuwe 1-px-tintvlekjes: (48,25) is B, aansluitend op de B-rij.

## MAG (niet gedaan, buiten het budget)
- (49,3–4): horizontaal selout-streepje van 2 px vanuit de linkerrand. Het kan een naad zijn; laten tenzij Jordi het ziet.
- De zwarte kloof x12–14, y52–53 is 3 px breed. Die komt uit het model (de donkere spleet bij de middentand).
