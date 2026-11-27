# Sauna-yeti – sprite ronde 6 (maker)

Jordi over r2: "het enige vanaf r2 wat beter moet zijn de lijnen die ik getekend heb, minder recht, de bovenste steen die ik heb omcirkeld moet wat beter afgemaakt en de stalen band van de emmer moet iets dikker, dan is die goed genoeg voor de eindkeuring" (markering `referenties/jordi_r2_punten.png`).

`sauna_yeti_r6.png` = **r2 precies** (palet, stenen, gezicht, vacht; niets uit r3/r4/r5) + 38 px in vijf zones, elk gemeten op `natief.png` (zelfde afbeelding cel → spritepixel als r1/r2). `bouw.py` controleert met een assert dat de diff buiten de zones 0 is; met argument `log` print hij elke pixel met reden. `vel.png`: r6 | r2 | model op 8×; daaronder 12× r6 | r2 | model voor emmer (rand + band), arm, onderkant en steen (het model hier exact met dezelfde celafbeelding als de meting); 1× op licht/donker naast fase 2.

| zone | px | wat (gemeten) |
|---|---|---|
| 1 emmerbovenrand (X29–41, rij 11–12) | 8 | modeldekking rij 11 X32–35 = 44 % (bovenkant emmer op y 11,56; zijkanten 12,0–12,4). Drempel 40 % i.p.v. 50 %: (32–35,11) → # (randtint r2); daaronder (32,12) b, (33–35,12) d = gemeten houtgemiddelde. De rand bolt nu op in het midden. |
| 5 stalen band (X27–41, rij 15–19) | 12 | modelband 4 cellen hoog = 1,6 px. Per kolom de 2 rijen het dichtst bij het zwaartepunt van de bandcellen: (28,16)(29,16)(32,17)(33,17)(34,16)(35,16)(36,18)(37,18)(38,17)(39,19)(40,19)(41,19) → g. X30–31 blijven 1 px (model daar 2 cellen = 0,8 px, boven het houten lipje); X27 rij 16 is buitenlijn, blijft. |
| 2 arm-binnenlijn (X43–47, rij 32–49) | 7 | zwart waar een zwarte modelcel (L<70) valt. Model: schuin in van linksboven, x 45,37 (rij 34–40), 45,78 (41–42), 46,18 (43–44), 46,59 (45–47), 46,99–47,40 (48). Nieuw K (was l): (43,32)(44,32)(44,33) bovenaan, (46,47)(46,48)(47,48)(46,49) onderaan. Buitenste armcontour (46–48, 35–37) niet aangeraakt. |
| 3 onderkant (X16–30, rij 54–56) | 7 | contour per kolom op de rij van het gem. y van de zwarte modelcellen: X16 55,12 → rij 55; X17–24 54,3–54,7 → 54; X25–26 55,12 → 55; X27–30 55,5–55,9 → 55. Nieuw K (16,55)(25,55)(26,55)(27,55, was l); (16,54)(25,54)(26,54) → m (gemeten sneeuw). Runs nu 4–8–6 i.p.v. 3–11–4. |
| 4 bovenste buiksteen (X24–32, rij 34–41) | 4 | vorm ≥ 40 % steen (r2: 45 %) → (30,39) erbij, rand, gloed 33 % → K. Naad: binnenpixel met ≥ 2 gloedcellen (de modelnaad is 1 cel = 0,4 px en haalt nooit 40 % aandeel; zelfde regel als lijnen): (27,36) 3 cellen, (27,37) 2 → o (was g). Geel op het hoogste geelaandeel: (29,39) o → y (18 %). Overige pixels kwamen met dezelfde regels op hun r2-tint uit. |

## Controle
16 kleuren incl. transparant (r2-palet), bbox x1–62, y11–60 (emmer 1 rij hoger), diff buiten de vijf zones 0 (assert).

## Zelf nog zwak
- **Armlijn:** het model zelf staat op x 45,37 over rij 34–40; de meting geeft daar dus nog steeds 7 px recht onder elkaar. Minder recht komt alleen van de schuine aanloop bovenaan en de knik onderaan. Wil Jordi meer kromming, dan is dat een afwijking van het model: eerst vragen.
- **Onderkant:** rij 54 X17–24 blijft 8 px recht (model 54,3–54,7 over die breedte).
- **Steen:** de modelsteen bestaat uit twee brokken met één naad; op 6×6 px leest de naad als 2 oranje pixels + 1 geel, het brokkenpatroon is niet zichtbaar.
- Emmerrand rij 11 hangt op een drempel van 40 % (dekking 44 %).
