# Charlatan-Alakazam: af_r2 (reparaties eindkeuring)

Basis: `basis_af_r1.txt` (= `../af_r1/raster.txt`). FAIL van de eindkeurder alleen op de afwerking: aan de lichtkant was 58 % van de buitenlijn zwart (o); echte Gen 3-sprites zitten op 3–23 %.

Bouwen: `python3 af2.py` (controleert per pixel de verwachte oude letter, schrijft `raster.txt` en de diff per zone), `python3 pal.py raster.txt alakazam_charlatan.png alakazam_charlatan_8x.png`, `python3 vel.py`. Meten: `python3 lichtkant.py raster.txt [x]` en `python3 controle.py raster.txt`.

## Selout aan de lichtkant (`lichtkant.py`)
Lichtkant = randpixel met een transparante buur links of boven en geen transparante buur rechts of onder.

| sprite | lichtkant zwart |
|---|---|
| af_r1 | 58 % (67 van 115) |
| **af_r2** | **18 % (21 van 116)** |
| Alakazam | 7 % |
| Kadabra | 23 % |
| Sneasel | 20 % |
| Umbreon | 5 % |
| Gardevoir | 3 % |

Er zijn 21 o-pixels aan de lichtkant over. Dat zijn de snorstrengen (opdracht: blijven o), de binnenhoeken bij de armen, de onderkant van de kaarten en het verre been.

## Wijzigingen tegen af_r1 (66 px, 0 px buiten de zones)
Alle verwachte oude letters klopten (geen afwijkingen gemeld door `af2.py`).

| zone | px | wat |
|---|---|---|
| 1 selout grijs | 17 | o→d: (29,7), (22,16), (21,17), bovenarm (14,29), (13,30), (12,31), (12,32), dij (20,43), (20,44), (19,45), rechterhand (51,27), (50,28), (49,29), (49,30), (48,31), (47,31); **extra (30,7)** o→d: anders bleef die als losse o in de oorinkeping staan |
| 1 selout verre scheen | 8 | o→**d** (opdracht zei c): (32,49–52), (31,53–54), (30,55), (29,56). Gemeten: c (145) op de buitenrand is een lichte kleur aan de rand (controle: open rand; SPRITE_KERN: geen lichte kleur op de buitenrand). d is de selout van grijs, zoals bij Alakazam |
| 2 selout zwart | 22 | o→k: linkerplaat (15,19), (16,19), (17–20,18), (14,20), (13,21), (13,22), (12,23), (12,24); flank (14,27), (14,28); (11,34); nabije knie (18,46–50); verre onderarm (41–43,33) |
| 3 hooglicht | 6 | b→a: dij (22,40–42), bovenarm (13,31), (13,32) en **extra (14,30)**: zonder die pixel is de a op de bovenarm maar 2 px. Past op de vorm: een cilinder van links belicht, hooglicht één pixel binnen de rand |
| 4 banding bovenarm | 4 | (16,29) c→b, (17,29) d→c, (15,30) c→b, (16,30) d→c. De bovenarm loopt nu a/b/c per rij in plaats van b/c/d |
| 5 schaduwkant hand | 4 | d→o: (11,43), (12,43), (13,44); **extra (11,42)** d→c: anders een los d-vlakje van 1 px |
| 6 deuk kop | 2 | (23,13) erbij als d, (24,13) d→b. Linkerrand van de kop nu x23 op rij 11–15. **Silhouet +1 px** |
| 7 onderarm | 3 | (42,38) en (49,38) transparant, (42,37) k→o. Onderrand nu 5 px (rij 37) → 6 px (rij 38) met ronde hoeken in plaats van 4 → 8; omlijning dicht (k grenst overal aan o). **Silhouet −2 px** |

## Controle (`controle.py raster.txt`)
- Het script is aangepast, niet de sprite: k mag aan de rand (selout van zwart). Het silhouet om tegen te meten is `meet_r2.npz`: meet5 plus de gemelde correcties uit af_r1 ((23,3) eraf) en af_r2 ((23,13) erbij, (42,38) en (49,38) eraf).
- Kleuren 11 + transparant. Open randen 0. Losse o 0. Alpha-diff 0 tegen dat silhouet.
- Clusters < 3 px: 9. Acht zijn dezelfde als in af_r1 (dunne delen: snorkrul, kaartrand, vingerlijnen, teenlijn, klauwen, selout). Nieuw is (11,34) k: een selout-pixel op de linkerbovenhoek van de nabije onderarm. Het is omlijning en geen tintvlakje.

## Zwakke punten
- (11,34) k staat alleen. Op 8× leest het als omlijning; als de keurder het als vlakje telt, kan het terug naar o (de lichtkant komt dan op 19 %).
- De bovenrand van de linkerplaat in k leest op 8× iets minder scherp tegen de achtergrond dan o. Op 1× is het in orde.
- Uit af_r1 blijven: grijze buik grotendeels b, het zwart vervaagt op een donkere achtergrond.
