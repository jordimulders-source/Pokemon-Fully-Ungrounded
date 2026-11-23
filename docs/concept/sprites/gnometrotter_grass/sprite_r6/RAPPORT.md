# Gnometrotter Grass r6 (maker, 23 nov)

Basis: `../sprite_r5/gnometrotter_grass.png`. Script `maak_r6.py` (→ `gnometrotter_grass.png`, `_8x.png`, `vel.png` = model | r5 | r6 | Rock af, `log_r6.txt` met elke gewijzigde pixel t.o.v. r5; assert: geen pixel buiten de zones). `meet.npz` = meting uit r5.
Jordi over r5: "grass gaat de goede kant op, alleen de rechte lijnen mogen wat minder recht, onthoud het perspectief" · "vergeet de benen en de rechterarm niet".

| Zone | px t.o.v. r5 |
|---|---|
| lijf (romp) | 78 |
| benen | 50 |
| rechterarm (keuring_r5 punt A, = Rock af) | 43 |
| linkerhand (punt B) | 2 |
| mutsrand (punt D) | 3 |
| rechterhand (60,36) | 1 |
| rest | 0 |

## Romp
- Duigen op de gemeten modelposities (naad ±29,5–31 en ±35, nerf ±37,6, naad ±43 onder de schouder), in perspectief gebogen: links van het tonmidden (x ±37) buigen ze naar links (x 31→30→31, 35→34→35), rechts ervan naar rechts (nerf 37→38→37, naad 44→43 naar de riem). Het model zelf is daar bijna recht; de buiging is de perspectief-aanvulling op Jordi's vraag.
- Licht/donker: bogen rond een lichtpunt linksboven (horizontaal 1,25× uitgerekt) → gebogen grens, geen rechte kolom.
- Sikkel in 6: onderste rij boven de riem (x ≥ 31) en de rechterrand waar het lijf achter de schouder wegdraait (rij 29–36). De nerf op x 29 is weg (dubbel met de naad).

## Benen
- Ribbel linkerdij als boog om de bol (bovenrand → diagonaal naar de kruisvouw), in 10.
- Grenslijnen dij|voet als boog (voetbol bolt naar boven): L x 20–27 (midden rij 48, randen rij 49), R x 41–47 (midden rij 49, randen rij 50). De rechte onderrandnaad van de rechterdij (rij 47) is vervallen: hij lag direct boven de grenslijn (dubbele donkere band).

## Niet gedaan
Punt C (neusboog, wacht op Jordi) en E–K (muts, blad, riem, laarzen, zolen).
