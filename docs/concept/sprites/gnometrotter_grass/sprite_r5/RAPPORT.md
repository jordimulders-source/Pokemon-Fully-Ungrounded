# Gnometrotter Grass r5 (maker, 23 nov)

Basis: `../sprite_r4/gnometrotter_grass.png` (neus, schouder, linkerhand goedgekeurd door de coördinator). Alleen de lijfzone opnieuw.
Scripts: `meet.py` (per spritepixel uit `../hybride/model_hybride.png` met de gedeelde geometrie: aandeel donkere lijnpixels, lum < 115 roze / < 100 blauw → `meet.npz`), `maak_r5.py` (maakt `gnometrotter_grass.png`, `_8x.png`, `vel.png` = model | basis | r4 | r5, en `log_r5.txt` met elke gewijzigde pixel t.o.v. r4).

| Zone | t.o.v. r4 | t.o.v. basis (hybride r2) |
|---|---|---|
| neus | 0 | 41 |
| schouder | 0 | 34 |
| linkerhand | 0 | 49 |
| lijf | 142 | 224 |
| rest | 0 | 0 |

Geen nieuwe zwarte pixels; alleen indexen 6/7/8/15 en 9/10/11; palet ongewijzigd.

## Romp
- Naden gemeten: kolommen met een keten van ≥ 4 pixels donk ≥ 0,45. Gevonden x 29, 31 en 35; x 29 en 31 zijn dezelfde (verdubbelde) modelnaad, de langste (x 31, 14 rijen) blijft. Naden x 31 en x 35 in 6.
- Nerf gemeten: zwakke maar doorlopende modellijn (kolomgemiddelde donk ≥ 0,12 over ≥ 8 rijen): x 37 (de spijkerstrook in het model) en x 29 (naast de baard), in 7 waar het licht is. (x 42 viel weg als los vlakje.) De lijn op x 43 in het model is de opgebogen riemrand, geen naad: niet gebruikt.
- Volume: één ton, tinten in bogen rond een lichtpunt linksboven (31,22): 15 (r < 3), 8 (r < 12,5), 7 daarbuiten → sikkel rechts en onder die de bolling volgt, geen diagonale paneelgrens. Rij 19 (schaduw onder de muts) is r4 gebleven.

## Benen
- Volume per bol zoals r4 (11 linksboven, 10, 9 sikkel), grenslijnen dij/voet uit r4 (GEDEELD).
- Ribbels/naden gemeten: ketens van ≥ 4 pixels donk ≥ 0,42; per lijn één tint (grotendeels in het licht → 10, anders 9). Resultaat: bovenrand linkerdij (rij 43), diagonale ribbel linkerdij, onderrand rechterdij (rij 47, 9).
- Losse vlakjes < 3 px in de lijfzone weggewerkt.

## Neusboog (alleen gemeten, niets veranderd)
Materiaalindexen, aantal en dichtstbijzijnde kleur (RGB-afstand):
2 (72,50,36) 135 px → 5: 39,9 · 3 (112,82,58) 238 px → 2: 55,7 · 4 (152,118,84) 66 px → 6: 53,3 · 5 (38,70,42) 170 px → 12: 37,1 · 12 (58,98,56) 98 px → 5: 37,1 · 13 (104,150,80) 186 px → 4: 57,8 · 14 (176,210,120) 123 px → 4/13: ±102.
Geen enkel paar valt zonder zichtbaar verschil samen: het dichtste is 5/12 (Δ 37, helderheid ±60 tegen ±84); 12 is de middentint van muts en baardblad, dus 12→5 kost de muts een tint. 2/5 (Δ 40) is bruin tegen groen.
