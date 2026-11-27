# Guaraná fase 2, ronde 16 (start r15)

Jordi (letterlijk): "deze zijn allemaal niet rond en er zijn nu iets teveel ogen tov de vorige ronde naar driekwart gezet, ik wil alleen midden links,
rechtsboven midden, linksonder rechts en linksboven rechts" (aantekening `sprite_r15/jordi_niet_rond.png`) + "de rest blijft hetzelfde".

Bestanden: `guarana2_r16.png`, `normal.pal` (= r15), `voor_jordi_r16_8x.png` (fase 1 | r16 | r15), `afstand.png`, `zone.npy` (waar r16 van r15 mag afwijken).
Bouwen vanuit `guarana_fase2/`: `PYTHONPATH=sprite_r15 python3 sprite_r16/bouw16.py && python3 sprite_r16/vel16.py`.
bouw16 bouwt de trossen opnieuw op (bouw15 + wijzigingen) en neemt daarvan **alleen de zone** over in r15; de rest is r15.

## Pixeldiff
- 138 px anders dan r15, **0 px buiten de zone** (script-check). Zone = de omcirkelde vruchten (r15- en r16-vorm) + de stempels van de ogen
  waarvan de kijkrichting terug moest, plus 1 px rand voor de buitenlijn. Alle ogen staan op dezelfde plek als in r15.

## 1. Niet rond (omcirkeld)
- Middelste tros, de twee onderste vruchten **g** (links) en **h** (rechts): waren spitse peren achter de andere; nu volle ronde vruchten (9 px), vóór d/f.
- Rechtertros onderaan, **v** en **w** (rond de overlap R5–s–onder): waren spitse peren; nu volle ronde vruchten (9 px), vooraan in de tros.
  w is helemaal zichtbaar; v ligt erachter (rechtsboven van w) en wordt deels afgedekt. Elk heeft een eigen ronde rand, hooglicht en sikkel.

## 2. Driekwart alleen bij a–d
| Jordi | oog (tabel) | sjabloon |
|---|---|---|
| (a) "midden links": linkertros, middelste oog | **D** | F1A (fase 1-oog, bovenste) |
| (b) "rechtsboven midden": middelste tros, rechtsboven | **b (M1)** | F1B (fase 1-oog, onderste) |
| (c) "linksonder rechts": rechtertros, linksonder | **u (R5)** | F1B |
| (d) "linksboven rechts": rechtertros, linksboven | **p (RT)** | F1A |
- Dit waren in r15 al de fase 1-kopieën; ongewijzigd.
- De andere ogen zijn terug naar de pupilplek van r14 (schil zoals r15): **e** en **s** pupil links (r14 'l'), **F** pupil rechtsonder/onder (r14 'd').
- Afwijking van "zoals r14": de kleine ogen **C** en **R1** hadden in r14 een diagonale pupil naar linksonder. Dat zou weer driekwart zijn, dus nu dezelfde
  r14-oogvorm met de pupil links (2 px). L2 en R2 blijven midden. A, H1 en M2 (half dicht) zijn ongewijzigd.

## 3. Oogrand
Zoals r15: F1A/F1B met de fase 1-schil (zwart rechts/onder), de andere ogen lijnrood rondom.

## Oogtabel (offset = pupilmidden − witmidden; wit-bbox = wit + pupil)
| tros | oog | sjabloon | wit-bbox (x0,y0)-(x1,y1) | pupil-bbox | offset (dx,dy) | in sprite |
|---|---|---|---|---|---|---|
| L | C | KL14 | (13,27)-(15,29) | (13,28)-(14,28) | (-0.5,+0.0) | 17/17 px |
| L | A | HALF7 | (1,26)-(5,27) | (1,26)-(2,26) | (-1.5,-0.5) | 23/23 px |
| L | B (L2) | MIDDEN | (9,23)-(12,26) | (10,24)-(11,25) | (+0.0,+0.0) | 24/24 px |
| L | D | F1A | (6,29)-(10,33) | (7,31)-(8,32) | (-0.5,+0.5) | 38/38 px |
| L | F | D14 | (11,34)-(15,37) | (13,36)-(14,37) | (+0.5,+1.0) | 30/30 px |
| M | M2 | HALF6 | (21,20)-(24,21) | (21,20)-(22,20) | (-1.0,-0.5) | 17/18 px |
| M | a (H1) | HALF7 | (24,16)-(28,17) | (24,16)-(25,16) | (-1.5,-0.5) | 23/23 px |
| M | b (M1) | F1B | (32,13)-(36,17) | (33,15)-(34,16) | (-0.5,+0.5) | 39/39 px |
| M | e | L14 | (30,21)-(34,24) | (30,22)-(31,23) | (-1.5,+0.0) | 30/30 px |
| R | r (R1) | KL14 | (42,26)-(44,28) | (42,27)-(43,27) | (-0.5,+0.0) | 16/17 px |
| R | p (RT) | F1A | (46,22)-(50,26) | (47,24)-(48,25) | (-0.5,+0.5) | 38/38 px |
| R | q (R2) | MIDDEN | (53,25)-(56,28) | (54,26)-(55,27) | (+0.0,+0.0) | 24/24 px |
| R | s | L14 | (47,29)-(51,32) | (47,30)-(48,31) | (-1.5,+0.0) | 28/30 px |
| R | u (R5) | F1B | (43,32)-(47,36) | (44,34)-(45,35) | (-0.5,+0.5) | 39/39 px |
- s en R1: 2 en 1 schilpixel(s) vallen samen met de schil van p/u (wit en pupil heel).

## Controle
- Rood lijn/schaduw/midden/licht: 42,2/10,7/35,5/11,6. Schaduw is iets onder de marge (r15: 14,5), want de vier nieuwe vruchten liggen vooraan
  en hebben minder naden. Buiten de zone mocht ik niets aanpassen.
- Zelf bekeken op 8× en 2×: de omcirkelde plekken zijn nu ronde bollen zonder kruisende naden. Alleen de vier a–d-ogen kijken linksonder.
  Niet keurder-getoetst.
