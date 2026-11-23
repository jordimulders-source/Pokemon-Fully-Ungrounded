# Fruitvampier (Emolga-lijn fase 3) – sprite r2 (verse maker)

Start: `sprite_r1/A0.png`, `A.png`, `A_geel.png`. Alles is gelijk aan r1 behalve de drie benoemde reparaties van Claude, als
bovenlaag per pixel in `gereedschap/bouw_r2.py`. Bewijs: `gereedschap/controle_r2.py` (pixeldiff per zone t.o.v. r1; stopt met een
fout als er buiten de zones iets verandert, telt ook tintvlakjes < 3 px). Vellen: `gereedschap/vel_r2.py`.
Leveringen: `A0.png`, `A.png`, `A_geel.png` (64×64, geïndexeerd, 16 paletplaatsen, palet ongewijzigd t.o.v. r1, 13–14 kleuren
gebruikt, index 0 transparant), `vel.png`, `kop_probeersels.png`.

## Diff per zone t.o.v. r1 (uitvoer controle_r2.py)
| bestand | vleugel (rij 9–37) | wang (x33–38, rij 43–48) | kap (x21–31, rij 48–51) | buiten de zones |
|---|---|---|---|---|
| A0 | 108 | 6 | – | **0** |
| A | 108 | 6 | 3 | **0** |
| A_geel | 108 | 6 | 3 | **0** |
Silhouet: alleen +2 px, beide in de wang (38,44 en 38,47). Vleugel: silhouet, K-lijnen, geel en wit exact gelijk (script controleert
dat alleen D/E-pixels zijn veranderd).

## 1 Vleugelpakket: volume (108 px, alleen D/E → D/E/G, geen nieuwe kleur)
Ramp = die van fase 2 (D 38/38/52, E 64/64/82, G 98/96/114 + K). Studie: fase 2 (`emolga_evo/af/model.png`), Honchkrow/Murkrow/Umbreon.
Vouwen op de modelplekken (gemeten met K-dekking per spritepixel op `model.png`): de diagonale vouw (rij 16→37), de bovenrand van het
voorpaneel (rij 15–16), de binnenlijn op rij 19 (x24–26) en de lijnen in de linkerstrook bestonden al in r1 en zijn niet aangeraakt.
De tinten volgen nu de vlakken tussen die vouwen:
- **voorpaneel** (licht vlak van het model, 'f'): G-hooglicht linksboven (smalle bovenlaag rij 16–18 en een wig rij 19–24 langs de
  gele linkerrand), E-midden, het onderste vlak (model 'd', naar beneden gedraaid) blijft D = schaduw.
- **rechtervleugel** (model 'd'): G-hooglicht op de bolling rechts van de witte ovaal (rij 12–16, x30–33), E-zone die met de vouw
  meeloopt en naar onder uitdunt (rij 9–24), D-sikkel langs de gele rand, breder naar onder; de onderste strook (rij 25–37) D.
- **linkerstrook**: G-hooglicht bovenaan (21,26 · 21–23,27 · 21–22,28), rest zoals r1; 25,33 E → D (los vlakje van 1 px).
Geen enkele tint < 3 px (G: 4 vlakken, E: 6 vlakken, alle ≥ 3).
Niet uit het model: het licht/donker binnen de vlakken (het model is daar egaal); vorm en vouwen wel.

## 2 Wangplukje rechts (6 px)
Model fijn gemeten (8×8-cellen): pieken met de punt op rij 44 en 46,5–47 tot x38 (dekking 28 % / 47 %), inkepingen op rij 43 en 45,
grijze scheidingslijnen tussen de pieken. Nu: punt 1 = 36,44 B · 37,44 w (model: grijze punt) · 38,44 K; punt 2 = 36,46 W · 36,47 W ·
37,47 B · 38,47 K. Inkeping rij 43 (x37) en rij 45 (x37 K, scheidingslijn N op 36,45) blijven zoals r1. Rand x37 is geen rechte zwarte
kolom meer. Niet 1-op-1: de puntjes zelf zijn K (schaduwkant) waar het model grijs heeft.

## 3 Kap met V (alleen A en A_geel; 3 px) – probeersels in `kop_probeersels.png`
- **P1 (gekozen)**: punt 25,49 zoals r1, V op rij 50 x24–27; rechts daarvan rij 50 x28–30 terug naar de A0-pixels (B; model wit
  202–204). Het wit onder het vizier wordt zo één doorlopende band (rij 48 x24–26, rij 49 x23–24/26–28, rij 50 x28–30) met de donkere
  V als punt naar de ogen; geen losse witte stipjes. 
- P2: hogere V (punt 25,48, rij 49 x24–26, rij 50 x23–27). V groter, maar het wit valt uiteen in losse 1-px stipjes die als
  slagtanden lezen (zelfde probleem als `sprite_r1/tussen/A_v1.png`).
- P3: als P2, kap met G/E-randje linksboven. Kap staat iets los van oor/vizier, maar dezelfde slagtanden en een grijze vlek.
A_geel: het gele vlekje ligt op dezelfde 4 px als in r1 over de V.

## Zwakke punten (eerlijk)
1. **V blijft klein**: de kruin is in het model maar 3 rijen hoog (rij 48–50), dus de V is 1 px punt + 4 px rij. P1 lost de "volle rij"
   op (wit rechts terug), niet de maat. Links loopt de V nog over in de donkere linkerrand/het linkeroor (model: daar donker, 46 en 28).
   Kap en oren hebben alleen de K-lijn van rij 51 als scheiding.
2. Het onderste voorvlak (rij 22–36, x28–38) en de strook rechts van de vouw onder rij 25 zijn nog egaal D (±90 px): bewust als
   schaduwvlak, maar het is wel een groot donker vlak zonder binnentekening.
3. G-hooglicht rechtsboven ligt vlak naast de witte ovaal; op 1× kan dat samen lezen als "grotere lichte vlek".
4. Wangpieken: twee punten (model heeft er 3–4, de onderste vallen op 64 px weg); puntjes in K.
5. Ongewijzigd uit r1 en niet in deze opdracht: voeten (blokje), mondlijn, geen binnenste zwarte lijn langs de rechter gele rand.
