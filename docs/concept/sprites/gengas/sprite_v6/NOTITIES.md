# Gengas sprite v6 (15 nov) – ogen en grijns 1-op-1 Gengar, geen kom meer

Jordi: "ogen en mond zijn nog niet goed" · "lijkt net alsof ze indeuken" · "en linkeroog is slordig" · (na v5) "de ogen zijn echt extreem lelijk, pupillen op willekeurige posities, dat kan echt niet" · "de mond is ook slordig".
Keten: `python3 v6.py && python3 maak.py && python3 vel.py` (v6.py leest `../sprite_v5/raster.txt`; elke pixel met reden in `raster.txt.log`).
**Diff v5 → v6 buiten de zone x 8–33, y 28–47: 0** (v6.py meet en print het). 522 pixelwijzigingen in de zone.

## Wat er gebeurde
1. Oud modelgezicht weg: alle K/E/R/W/H/a-pixels in de kaders van linkeroog (x12–18, y29–36), rechteroog (x23–32, y29–37) en grijns (x13–32, y37–46); gaten gevuld van buiten naar binnen met de meest voorkomende lijftint van de buren (m/b/l/u uit v5). Daarmee ook de losse K (24,46) weg (MAG 3).
2. Indeuken: band in de zone één tint lichter (b→m, rij 29–40), lichte wig tussen de ogen (l/u, x19–26) en u-ring boven het linkeroog → m. Overgang: bovenrand van de band loopt rond op (rij 28 x24–25 m, x26–33 blijft b; (33,29) blijft b omdat (34,29) buiten de zone b is). Randschaduw links (x8) a→b. Losse a (10,37) → m.
3. Ogen en grijns = Gengars Gen 3-pixels (`graphics/pokemon/gengar/anim_front.png`, selectie zoals `model/gezicht.py`: idx 1–7, e, f, en d grenzend aan wit/rood). Ogen als paar dx −5, dy +3; grijns dx −5, dy +6 (middelpunten op de v5-plek; Gengars onderlinge oogstand blijft, grijns staat 3 rijen lager dan bij Gengar zoals in v5/het model).
   Tinten: rood 6/5 en wit 1 exact (palet E/R/W op Gengars waarden gezet; kwamen alleen in het gezicht voor), tandlijn 3 → G (100,99,98; Gengar 106,98,123), tandschaduw 7 en 2 → H (186,185,183), lijn e → a, zwart f → K, d (schaduw naast oog/mond) → b. 16 tekens incl. transparant, geen nieuwe tint.

## Zwakke punten (eigen)
- Gengar-tint 2 (222,213,222) heeft geen eigen slot: samen met 7 als H, dus 3 tandschaduwpixels iets donkerder dan bij Gengar.
- De d→b-pixels rond de ogen zijn losse 1–2-px-clusters b in vlak m (zo staan ze bij Gengar ook, als oogselout).
- Rechts onder de grijns blijven twee losse l-pixels (31,43), (30,44) uit v5 tussen grijnslijn en onderband.
- Het gezicht ligt nu op een vrij vlak m-veld; de donkere band stopt op rij 28 recht boven het rechteroog.
