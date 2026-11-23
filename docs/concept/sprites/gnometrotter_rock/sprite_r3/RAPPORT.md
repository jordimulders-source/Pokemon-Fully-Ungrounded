# Gnometrotter Rock – sprite r3 (23 nov)

Basis: r2, plus de 8 punten uit `../keuring_r2/KEURING.md`. Silhouet t.o.v. r2: 0 px verschil. Lever: `gnometrotter_rock.png`, `gnometrotter_rock_8x.png`, `vel.png` (r3 | r2 | model op 8×; 1× licht/donker; naast Gnomini/Gnomad).

## Werkwijze (`meet.py` + `r3.py`)
Per spritepixel gemeten op het model (gedeelde geometrie): het aandeel donkere modelpixels (lum < 80) en de helderheid van de rest. De tinten van lijf, benen, muts en haar komen rechtstreeks uit die helderheid; de lijnen staan waar het donker-aandeel een lokaal maximum is (1 px). Daarna een 3×3-meerderheidsfilter (muts 5×5) binnen het onderdeel tegen dambord, en losse stipjes weg. Baard, riem/gesp, stok, zolen, neus en hand R zijn r2.

## De 8 punten
1. **Voetballen + grens dij/voet:** benen 11 waar het model licht is (≥ 150), anders 10; grenslijn 9 uit het model (links rij 50, x 17–25; rechts rij 50–51, x 41–48). Linkervoet x 17–22 licht, x 23–27 midden: zo meet het model.
2. **Broek:** alle r2-lijnen en krabbels weg; alleen modellijnen (donker-aandeel ≥ 0,22, lokaal maximum): onderrand riem, binnenrand rechterdij x 38 (y 43–47), naadje linkerdij, kruis.
3. **Schouderovaal R:** eigen ovaal (het r2-facet onder (45,24), x 40–49, y 22–28), lijn 6 rondom inclusief de onderrand, vulling 8, glans 15 op de 4 lichtste modelpixels.
4. **Haar R:** lichte modelpixels (≥ 165) in x 32–40, y 15–18 bij het plukje; vlak 13/12 uit de helderheid; lijn 2 aan de mutskant waar het model donker is.
5. **Linkerarm:** rij 31 lijn 6, rij 32 tint 8, rij 33 tint 7 (x 11–17); scheiding vuist|arm op x 10; de lichte randpixels (5,30) (4,31) (15,31) en de losse 7 (8,32) zijn weg.
6. **Muts:** tinten 5/4/3 uit de helderheid (lichte kruin tot x 32, zoals gemeten); plooi- en vouwlijnen uit het model in tint 2 (rond x 35–38, y 7–10 en x 28–30, y 11–13).
7. **Hooglicht lijf:** 15 op de lichtste modelplek buiten het ovaal (rond (37,33)) plus de glans op het ovaal; 7 px 15 in het lijf.
8. **Haar L:** 13 waar het model licht is (bovenkant), 12 eronder.

## Afwijking t.o.v. r2
417 px: lijf 128, broek/benen 172, muts+rugkam 80, haar R 14, arm L 15, haar L 8. Silhouet 0.

## Pixels die niet rechtstreeks uit het model komen
- Linkerarm: de tinten 8/7 per rij en de scheidingslijn op x 10 (keurpunt 5; het model meet daar één middentint).
- Hooglicht: 15 op de 4 lichtste pixels (ovaal) en 3 rond (37,33) (lijf), plaats wel gemeten.
- Haar R onderrand tegen het gezicht in lijn 2; lijn om haar R op de mutskant: (36,14) (39,16) (32,18) (41,18).
- Vlak/tint verder: regels op de modelmeting (geen vorm getekend). Gesp, oogstrook en de overige outline highlights: zoals r1/r2.

## Controle
64×64 P, transparant 0, 15 kleuren, zwart 9,6 %, geen losse zwarte pixels; één lichte randpixel (53,35) (outline highlight hand R). Vlekjes < 3 px: lijnstukjes aan de rand (9 op de rechterflank van de broek, 2 bij het haar).

## Eigen zwakke punten
- Losse 9-pixels tegen de buitenlijn van de broek (dubbele lijn) weggehaald: (48,40) (49,45) (20,49) (28,52); over: (49,36) (45,39) (rand riem/broek rechts, 1 px).
- De rechterdij/-voet leest op 8× als één blauw blok met een dunne grenslijn; het model heeft daar een ronder verschil.
