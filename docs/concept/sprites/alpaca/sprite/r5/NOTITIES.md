# Palpaca r5 (19 nov): eindronde kleur, schaduw en belijning (Dragonfly Cave)

Jordi (letterlijk): "ja de hele sprite is echt veel beter nu, ik vind hem goed genoeg om naar de eindronde te sturen voor kleur, schaduw en belijning, dragonflycave. Alleen de torso mist nog een beetje perspectief" · "en er zit 1 willekeurige zwarte sprite bovenin de laatste poot".

## Bestanden
- `palpaca.png` (r5), `normal.pal` (16 kleuren incl. transparant).
- `vel.png`: model | r5 | r4 (8x, zelfde hoogte) · torso 12x: model op spriteraster | r5 | r4 · kop 12x: r5 | r4 · 1x en 2x op licht en donker.
- `scripts/bouw_r5.py` (r4 → r5, alle wijzigingen met coördinaten), `scripts/check.py` (losse pixels per kleur), `scripts/zoom.py`, `scripts/vel.py`, `scripts/px.py`/`modelkop.py` (modelraster, uit r4).

## Controle
- **Alfa-diff met r4 = 0 px** (assert in `bouw_r5.py`); geen randpixel weggehaald.
- 77 px anders dan r4; daarvan 4 buiten de torso-rijen 37–50: (24,17), (17,52), (44,54), (45,56).
- Vorm, gezicht, kuif, oog en binnenlijnen van de kop ongewijzigd (alleen (24,17) lijnkleur).

## Losse zwarte pixel (Jordi)
- **(42,47)**: zwarte 1 midden in de bovenkant van de verre achterpoot, zonder lijnbuur → verre-pootschaduw F. MOET.

## Torso-perspectief (Jordi's punt) — MOET
Torso met de hand herschreven, rijen 39–49, x 21–44 (`T` en `P` in `bouw_r5.py`):
- **Borst naar de kijker, licht linksboven**: hooglicht 2 als ovaal op de borst (y 39–43, x 22–26, smaller naar onder) in plaats van de vlekjes van r4.
- **Rug**: hooglicht als bol boven op de rug (y 39 x 32–38, y 40 x 34–37, y 41 x 35–36) i.p.v. een rechte band langs de rugrand.
- **Verre flank donkerder, sikkel**: schaduwband aan de achterkant smal bovenaan, breder naar onder: y 41 x 40–41 (4/5, slagschaduw van de staart), y 42–44 x 40/41–42 (4, rand 5), y 45 x 38–42 (4 4 4 5 5), y 46 x 38–40 en y 47 x 38–39 overgaand in de dij.
- **Buik in schaduw, rafelig (wol)**: 4 met gekartelde bovengrens y 45–48 tussen voorpoot en dij (x 29–33), en achter de geheven voorpoot (x 23–26, y 46–48); 5 vlak boven de buikrand.
- **Schaduw waar de poten in het lijf overgaan**: nabije voorpoot: lijn taps van (21,45) 4 → (22,46)/(22,47) 5 → (23,48) 6 → (24,49) 1; nabije achterpoot: plooi (33,47) 5, (33,48) 5, (33,49) 6 voor de dij, dij-hooglicht (35–36, 46–47).
- **Verre achterpoot onder het lijf**: binnenlijn (41,46) 6, (40,47) 6 sluit aan op (39,48) 1 (lijf over verre poot).
- Voorpoot-voorkant (x 27–28, y 47–49) licht als doorlopende streep naar de staande voorpoot (model: daar licht).

## Dragonfly Cave-punten
| Punt | MOET/MAG | Wat ik deed |
|---|---|---|
| Kleurramp wol: tinten niet te dicht bij elkaar | MOET | 2 en 3 lagen in r4 15 luma uit elkaar (onzichtbaar op 1x). Nieuw: 2 = 255 253 245, 3 = 238 231 210, 4 = 210 200 174, 5 = 176 163 138, lijn 6 ongewijzigd. Luma 253/231/200/164/113, stappen 22/31/36/51 (r4: 15/28/36/56). Warme hue-shift (crème → oker → bruin) behouden. |
| Verre poot donker vs zachte lijn | MOET | F was 124 109 88 ≈ lijn 6 (124 112 92); nu 112 97 78 (luma 99 tegen 113), B 154 137 113 blijft. |
| Losse vlekjes y 43 en y 47–49 | MOET | weg: (27,43) 2, (23–25,43) 2-groepje, (34,47) 4, (39,47) 4, (35,49) 4, (32,50) 5 en de 2/5-ruis (23–29, 47–49) opgenomen in de nieuwe torsoschaduw. `check.py`: geen losse wolpixels meer in de torso. |
| Losse pixels halsbandschaduw | MAG | (26,38) 5 → 4, (30,38) 2 → 3. |
| Zwart en zachte lijn niet om en om op één rand | MOET | (24,17) kruin tussen de oren 1 → 6; (36,37) rugbultje 1 → 6; (22,37) halsband links (lichtkant) 1 → 6; (17,52) handschoen links 1 → donkerrood A (rode groep lijnt in A op de lichtkant). |
| Verre achterpoot linkerrand | MOET | was 1/6/1/6 door elkaar; nu boven (in de lijfschaduw) zwart: (44,54) 6 → 1, onder selout 6: (45,56) 1 → 6. |
| Selout lichtkant / zwart schaduwkant | MOET (check) | borst x 21 en rug y 38 zachte lijn 6, buik/achterkant/rechterkant kop zwart: klopt, niets aan veranderd. |
| Geen pillow shading / banding | MOET | hooglichten als ovaal/bol, schaduw alleen aan rechter- en onderkant (sikkel), band aan de achterkant met wisselende breedte. |
| Jaggies | MAG | silhouet bevroren (alfa-diff 0); geen randpixels verplaatst. |

## Resterende zwakke punten
- Het silhouet van de romp is hoekig (rechte rug, rechte achterkant x 43–44); binnen alfa-diff 0 kan schaduw dat maar deels breken. Ronder zou randpixels kosten (keuze voor Jordi).
- Het verschil 2/3 is op 1x subtiel (bewust: wit dier, veel hooglicht volgens R/S-stijl).
- Kop niet herzien op "hoekig" (opdracht: kop blijft); alleen de lijnkleur op de kruin.
- Niet gekeurd door een onafhankelijke keurder.
