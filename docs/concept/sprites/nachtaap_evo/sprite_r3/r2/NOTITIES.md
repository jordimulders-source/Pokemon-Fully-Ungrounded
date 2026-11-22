# Moonkey r2: kleur/volume naar Gen 3 (19 nov)

Vanaf r1; alleen tinten binnen bestaande vlakken. Draaien vanuit `sprite_r3/`: `python3 r2/bewerk2.py` (`-v` drukt elke pixel af), daarna `python3 r2/vel.py`.

## Bevroren (bewijs: `export.py`, faalt anders)
- **Alpha-diff met r1: 0** (silhouet ongewijzigd, geen pixel van/naar transparant).
- **Pixeldiff kop: 0**: alles binnen de kopomtrek vanaf de nek omhoog (`proef.kopmasker`: x ≤ 24, y33–55, zonder de rugbult boven/rechts van de koplijn op y33–36). Ogen, maan, mond en linkeroor ongewijzigd.
- Geen nieuwe kleuren of lijnen: palet = oude palet, 15 kleuren + transparant.

## Wijzigingen (netto 97 px verschil met r1; 101 logregels, enkele pixels twee keer gezet; alleen tintwissels binnen paars 3/4/5/6)
| Zone | px | Wat |
|---|---|---|
| licht/volume lijf | 62 | zoals de oude sprite: 5 linksboven op de rugbult (tussen en onder de eerste wiggen), 4 op de flank, 3 als sikkel achter/rechts en onder op de buik tussen voorpoot en dij. Grenzen zijn cirkelbogen rond lichtpunt (21,30) (y × 1,3), dus de sikkels volgen de bult; geen banding, geen pillow. Rugwiggen (F) op hun plek, tint ongewijzigd (zoals oud: één lichtblauw). |
| sikkel rechts | 13 | 4 → 3 op de 2 (y37–43) / 3 (y44–53) pixels binnen de rechterbuitenlijn. |
| achterpoot | 17 | een tint donkerder dan de nabije voorpoot (die houdt 5 bovenaan / 4): bovenkant dij 4 (licht), onderkant y49–51 3 (schaduw onder, sluit aan op de sikkel); de losse modelpixel 5 (38,47) → 4. Geen vormwijziging. De schaduwgrens boven de dij is afgerond ((39,43),(40,43) → 4, (43,44) → 3): de 3-sikkel loopt x42,41,40,41,43 en buigt om de bovenkant van de dij. |
| rug→staartaanzet | 9 | (41,35) 3 → 6: lavendel vlakje (41–43,34–35) in één stuk. Staartvoet y33–36 (x45–48): de losse 2-lijnpixels binnen de staart → 3/4, zodat hij loopt als de staart erboven (5 links, 4, 3 rechts, dan de lijn). De binnenlijn bult/staart en de blauwe wig blijven één doorlopende lijn. |
| verre voorpoot | 0 | was al 3 (donkerder dan de nabije). |
| nabije voorpoot | 0 | had al de lichte bovenkant 5 uit het model. |

## Controle
- ≤3 tinten per kleurgroep + lijn (lijf 3/4/5 met 6 als hooglicht bij de staartaanzet, zoals oud), geen lichte kleur op de buitenrand, geen open randen, geen losse lijnpixels.
- De losse pixels in de staartaanzet zijn weg. Over: oogglans, neus, krulpunt (53,14), oorpixels (23–24,38), 1-px lijnstukjes op diagonalen, teenpixels (allemaal kop/model, bevroren of r1).

## Zwakke punten die ik zelf nog zie
- (Zelf gerepareerd: de rechte tintgrens boven de dij is afgerond, zie achterpoot.)
- De 5/4-grens onder de bult loopt op y36→37 over ±6 px vrij recht (x19–28); in de oude sprite zit daar ook zo'n grens.
