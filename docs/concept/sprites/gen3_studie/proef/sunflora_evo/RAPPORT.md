# Proef tintzones: Sunflora-evolutie (24 nov)

Bron: `docs/concept/sprites/sunflora_evo/af/sunflora_evo.png` (niet aangeraakt). Resultaat: `na.png`, vergelijking: `voor_na.png` (voor | na | Gen 3 Sunflora op 6×; daaronder op 1× ook Sunkern, Solrock en Bellossom). De wijzigingen staan als pixellijsten in `maak.py` (geen kwantiseren, middelen of blur).

## Probleem
De gezichtsschijf had ringen van tinten langs de rand: van buiten naar binnen oranje (5) / donker goud (4) → geel (3) → crème (2) → soms weer geel, en aan de rechterkant twee gele ringen met een crème streep ertussen. Het las als airbrush/kussen. Gen 3 Sunflora: één crème grondtint, één schaduwzone (rechts en onder) met een harde grens, buitenlijn donker.

## Wat er per zone veranderde (76 px, allemaal binnen de schijf, x 17–40, y 17–39)
| Zone | Wat | px |
|---|---|---|
| Lichtkant buitenlijn (linksboven) | de buitenste ring (oranje/geel) wordt één lijn in donker goud 4 (selout), ook bovenop de schijf waar crème direct tegen de stralen lag | 14 |
| Grondtint | gele ringpixels binnen de lichtkant (links, linksboven) en losse gele stipjes rechts → crème 2 | 18 |
| Schaduwzone | één sikkel in geel 3 rechts (2 px boven, 3–4 px midden), die onderaan overgaat in de bestaande gele kinzone; ook linksonder een smalle strook; oranje/goud in de rand van die zone → 3 | 35 |
| Schaduwkant buitenlijn (rechts) | oranje/goud aan de rechterrand → bruin 6; onderaan blijft de bestaande zwarte lijn | 9 |
| Stralen, lijf, blad, voeten | niets | 0 |

Palet ongewijzigd (14 kleuren + transparant), PNG mode P, 64×64.

## Bewijzen (uit `maak.py`)
- Silhouet (transparantiemasker): **diff 0**.
- Gezicht: **diff 0** op 81 bevroren pixels: ogen (1/8/9), mond (6, tong a, de 4 onderin), de wenkbrauwlijn (\_/\_/ in geel, 15 px) en de losse AA-pixels aan de gezichtslijnen (20,27) (19,28) (24,28) (29,28) (34,28) (23,25) (30,25) (31,30) (30,34).
- Geen enkele wijziging buiten het vak x 17–40, y 17–39.

## Wat ik zelf nog zwak vind
- De bevroren AA-stipjes onder de ooguiteinden (19,28) (24,28) (29,28) en naast de mondhoek (31,30) zijn zelf kleine vlekjes zonder richting; ze horen bij het gezicht, dus blijven staan. (34,28) valt nu wel in de schaduwzone.
- De wenkbrauwlijn is in dezelfde geel als de schaduw; rechtsboven ligt de wenkbrauw dicht bij de sikkel, maar ze raken elkaar niet.
- Linksonder (rond x 19–21, y 33–36) is de schaduwstrook smal en hoekig, omdat de zwarte lijn daar al grillig loopt (silhouet en bestaande lijn niet aangeraakt).
- Stralen niet aangepakt: de oranje vlekken in de gele stralen en de gemengde oranje/goud randjes lezen naast Solrock nog onrustig. Dat was buiten deze opdracht (alleen de schijf).
- Geel 3 als schaduw is verzadigder/oranjer dan het khaki van Sunflora; een eigen schaduwkleur kan in slot 15 (nu ongebruikt), maar dat heb ik niet gedaan om het palet gelijk te houden.
