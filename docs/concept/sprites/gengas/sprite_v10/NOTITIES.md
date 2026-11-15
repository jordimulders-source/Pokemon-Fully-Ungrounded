# Gengas sprite v10a / v10b (15 nov) – stormvlek in plaats van spiraal
Jordi: "probeer maar 2". De spiraal wordt een ovale stormvlek zonder spiraal (Grote Rode Vlek): liggend ovaal in de band, iets donkerdere rand, lichtere kern, bestaande tinten, geen zwarte omlijning.
Keten: `python3 v10.py && python3 maak.py && python3 vel.py`. **Diff t.o.v. v9 buiten x 33–48, y 26–42 = 0** (gemeten); reden per pixel in `raster_v10a/b.txt.log`.
- Ovaal 11×7 op x37–47, y32–38 (de plek van de spiraal, 1 px naar rechts zodat links de lichte strook vrij blijft). Kern linksboven van het midden (licht van linksboven).
- De rand is alleen aan de schaduwkant (rechtsonder) donker. Aan de lichtkant gaat de vlek met één tintstap over in de band, net als de bandranden elders.
- **v10a (lichter dan de band):** vulling l, kern v, rand m (licht) en b (schaduw).
- **v10b (donkerder/roder):** vulling b, kern m, rand b (licht) en a (schaduw).
- Spiraallijn buiten het ovaal → l: de lichte stroom loopt er boven (rij 31–32) en onder (rij 39–40) omheen.
Zwakke punten (eigen): het buigen van de band om de vlek is maar licht zichtbaar (alleen de l-stroom boven en onder); het ovaal is vrij regelmatig (pilvorm, randen 7 px recht); in v10b leest de m-kern op 2× bijna als band die door een ring schijnt.
