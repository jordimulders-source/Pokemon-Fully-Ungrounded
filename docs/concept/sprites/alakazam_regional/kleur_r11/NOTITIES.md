# Charlatan-Alakazam: kleur r11 (onderarmen zwart, bovenarmen grijs, zoals het model)

Basis: `basis_L1.txt` (= `../kleur_r9/var_L1.txt`; zonder r10). Jordi: "nu heb je van een arm een hand gemaakt. dat klopt ook niet, het model had de onderarm zwart gemaakt en de bovenarmen grijs, laten we dat doen, dat past goed bij de originele alakazam, kijken we hoe dat eruit ziet. Dan hoef je de vorm niet aan te passen".

Bouwen: `python3 r11.py` (schrijft `var_r11.txt/.png` en bewijst de diff), daarna `python3 vel.py`. Modelklasse per pixel: `python3 kaart.py x0 y0 x1 y1 [raster]`.

## Wijzigingen (alleen kleur; tinten per pixel uit de modelklasse)
- **Links, bovenarm grijs** (x13–18, rij 28–32; model B/C/D):
  - rij 28 is een schaduwband d onder de plaat;
  - daaronder b links en c/d rechts.
  - Afwijkingen van de modeltint (ruis weggehaald): (15,28) C→d, (16,29) B→c, (15,30) B→c, (15,32) D→c.
- **Links, onderarm zwart** (x12–20, rij 34–39; model K): n linksboven, m, k rechts en onder. (16,39) was o, en het model is daar K, dus nu k.
  - De lijnen naar de hand blijven waar het model ze heeft: rij 38 x12–15, (15,39) en rij 40 x16–19.
- **Rechts, bovenarm grijs**: (39,30–32) en (40,33) b (model B). De plaat (37–38,29) en (38,30–31) blijft zwart.
- **Rechts, onderarm zwart** (x40–48, rij 32–37; model K): n boven, m, k onderaan.
  - (39,34) m→o (model: lijn); (41,37) d→o (silhouetrand).
  - De grens met de hand is de bestaande lijn x48 (model D/K → C bij x49).
- Schouderplaten, rug en zijkanten zijn ongewijzigd.

## Controle
- 93 px gewijzigd, 0 buiten de armzones (x11–21, y26–40 en x36–49, y28–38).
- Handen ongewijzigd: in de handen is geen kaart- of vingerpixel veranderd. (48,36–37) zijn onderarm (model K).
- Alpha-diff 0. Open randen 0. Losse o 0.
- Clusters < 3 px: 9. Geen ervan is nieuw; ze stonden al in r9.

## Zwak punt
- De grijze bovenarm rechts is maar 4 px: een smalle strook tussen de zwarte plaat en de zwarte onderarm, net als in het model.
