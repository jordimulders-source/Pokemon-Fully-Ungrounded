# Viscacha frontsprite, kleur ronde 4 (maker-agent)
r3 (keurder PASS) is bevroren buiten de zones hieronder; het handwerk staat in `reparaties_r4.py` (op het r3-raster).
Jordi letterlijk: "ja je houdt zoveel mogelijk het gemini model vast"; "het enige dat anders mag van gemini is dat het oog luier mag, zoals een echte viscacha".

## Diff r3→r4 (76 px)
| zone | px | wat |
|---|---|---|
| 1 oog (Drowzee) | 21 | Oog pixel voor pixel van Drowzee (`graphics/pokemon/drowzee/anim_front.png`, x26–32, rij 16–19): lidlijn bovenop, smalle spleet van 2 rijen, achterhoek lager (zwaar lid schuin over het oog), onderlidlijn. Alleen herkleurd: lidlijn 6→1, 7→2 (lidrand/voorhoek) en 3 (onderlid), wit C→E (donker oog), pupil F→1, vacht A→5/4. Eén glanspixel D op (12,26), anders leest de spleet als slapend. Op x9–15, rij 25–29; het oude Emolga-oog is weg (restpixels → vacht 5/4). |
| 2 oren | 21 | Nabij oor: rondere, bredere schelp; top 3 px (19–21,12), rechterkant 1 px verder (x23 op rij 15–17), grotere binnenschelp B/C. Ver oor: top 3 px (6–8,12) en 1 px breder links (x5 op rij 13–14). |
| 3 snuitpluk | 6 | Gele pluk uit Gemini terug op de snuitpunt: punt (2–3,26) in 8, geel 9 op (3–4,27) en (3,28), aan de onderkant zonder lijn vast aan de snuit. |
| 4a staartaanzet | 15 | Onderrand als aflopende trap 3–4–4: (47–49,48), (50–53,47), (54–57,46). |
| 4b verre voet | 3 | Hiel en teen 1 px rond: (22,58) en (29,58) weg, (29,57) → 1. |
| 4c scheen | 3 | 3-strook taps: (47,56), (47,57) en (47,58) → 4, zodat de scheen geen buis met drie strepen meer is. |
| 4d schouder | 7 | Zachte schouderovergang 4 achter de voorpoot: (21,34–36), (22,36) en (24,37–39). |

**Silhouet t.o.v. r3** (21 px; nieuw bestand `silhouet/silhouet_r4.txt`):
- Oren erbij: (19,12), (18,13), (17,14), (23,15), (23,16), (23,17), (6,12), (5,13), (5,14).
- Snuitpluk erbij: (2,26), (3,26).
- Staartaanzet weg: (50–54,48), (54–56,47).
- Verre voet weg: (22,58), (29,58).

## Afwijkingen van Gemini
- **Oog** (door Jordi toegestaan): luier, met zwaar lid, zoals een echte viscacha (foto's `referenties/jordi_foto*`).
- Wangpluk iets kleiner (zoals in r3, tegen het kraageffect), snorharen weg en geen vachtpiek op de rug (zoals in r3).

## Controle (`controle_uitvoer.txt`)
- Open randen 0, losse pixels 0.
- Clusters < 3 px: alleen oogpixels (E, D) en de gele kern (57,12) in de pluimtop.
- 16 kleuren incl. transparant; png = raster.
- Keurvel: `vel.png` (werk naast `gemini64.png`, de kopuitsneden van beide foto's (`foto1_kop.png`, `foto2_kop.png`), Drowzee als bron van het oog en Pachirisu).

## Zwakke punten
1. De glanspixel D is op 8× vrij groot ten opzichte van de spleet. Zonder glans leest het oog als dicht; met glans iets minder loom. Keurder: kijken of hij weg moet.
2. De snuitpluk zit vlak naast de neus; op 1× is het een gele stip op de snuitpunt. Hij zit vast en heeft geen vonkvorm, maar of hij als vonk leest is een oordeel voor de keurder of Jordi (weglaten = de 6 px terugzetten).
3. De top van het verre oor is plat over 3 px (rond genoeg?).
Niets gecommit.
