# Hoatzin fase 2, r13 (19 nov): alleen de kop, op r12

`sh alles.sh` = `kop13.py A` op `../r12/hoatzin.png` → check → export → vel (r13 | r12 | model | Archeops | Braviary, kop 12x r13 | model | r12).
Pixeldiff t.o.v. r12: 76 px, **0 buiten de kopzone** (x4-19, y16-28), silhouet 4 px (snavelpunt).

Gemeten op het model (`modelgrid.py 2 14 22 30 40`): blauwe vlek x10.0-16.0 × y19.5-25.5 (6x6); oog met ring en iris x11.5-13.75 × y20.6-23.75;
snavel zichtbaar x6.4-10 × y22-27.5 (hoogte ± de blauwe vlek, lengte ±0.6× de vlek), haakpunt (7.1, 27.3), bekspleet y25.5.

| punt | r13 |
|---|---|
| 1 oog/gezicht | geen zwarte ring meer. Oog 3x3 (x11-13, y21-23): rood, zwarte pupil in het midden, glans (F) linksboven, donkerblauwe hoek (8) rechtsonder. Ligt direct in het blauw. Blauwe vlek 6x6 met ronde hoeken (y20 x11-14, y21-24 x10-15, y25 x11-14); 9 vlak, 8 als rand rechts en onder. Het palet heeft maar 2 blauwtinten (16 kleuren vol). |
| 2 snavel | naar de modelmaat: x5-10, y22-28; 3 grijstinten (F rug, E midden, 2 onderkant/haak), bekspleet 1 px zwart (y25, x8-10), lichte onderkaak, gehaakte punt linksonder tot y28. |
| 3 kruin | donkere ronde kruin (2) met een bruine boog (6) linksboven; alleen in de bovenste rij (y16) de veerbases van F1-F5 (7/6). |

check.py: dambord 0, om-en-om 0, zwarte klonten 0.
Varianten van het oog in `kop13.py` (A = gekozen; B pupil naar voren; C onderhoeken donkerblauw).
Zwak: de vlek blijft op 6 px vrij hoekig, en met 2 blauwtinten is er geen lichte kant linksboven.
