# Gnometrotter Grass r13 (maker, 23 nov)

Basis `../sprite_r12/gnometrotter_grass.png`; alleen de muts (Jordi: "de bladeren lijken niet op bladeren, kijk naar pokemon met bladeren"). Silhouet, nerven/omlijning en palet = r12. Script `maak_r13.py` (→ `gnometrotter_grass.png`, `_8x.png`, `log_r13.txt`, `muts_raster.txt`, `vel.png` = studie-uitsneden Chikorita | Tropius | Shiftry | Swadloon, daaronder model | r12 | r13, muts 12×). Studievel: `studie_blad.png` (sewaddle, swadloon, leavanny, shiftry, leafeon, chikorita, bayleef, tropius, celebi, snivy, servine; eerste frame, 8×).

## Studie: hoe Game Freak een blad op deze maat leest
- **Twee helften, verschillend belicht**: één helft licht (naar het licht/boven), de andere een tint donkerder; de scheiding loopt over de lengte van het blad = de middennerf (Chikorita, Bayleef, Tropius, Shiftry, Leavanny).
- **Middennerf**: op grote bladeren een 1-px lijn, meestal donkerder dan beide helften (Chikorita, Tropius); bij Shiftry licht (bruinroze). Kleine bladeren (Shiftry-blaadjes, Bayleef-kraag) hebben geen eigen nerflijn: de tintgrens is de nerf.
- **Omlijning**: donkerste eigen groen aan de lichtkant, zwart/donkerst aan de schaduwkant en onderrand.
- **Bladpunt**: taps tot 1 px, de nerf loopt niet tot in de punt.
- **Zijnerven**: alleen op heel grote bladeren (Tropius: dunne diagonale lijnen in de schaduwtint); niet op bladeren van muts-formaat. Swadloon: de bladkap is één lichte massa met een paar donkere vouwlijnen, schaduw aan de binnenkant.

## Toegepast (alleen de muts)
| Zone | px t.o.v. r12 |
|---|---|
| muts | 120 |
| rest | 0 (assert) |

- **A linkerblad** (punt boven, voet linksonder): donkere middennerf (5) diagonaal (32,2)→(19,12), taps (niet in de punt); helft linksboven licht 13 met een rand 14 langs de omlijning, helft rechtsonder schaduw 12.
- **B middenblad** (klein): zonder nerflijn; lichte helft links 13, schaduwhelft rechts 12.
- **C rechterkrul**: lichte middennerf (13, zoals Shiftry) (35,2)→(42,12); buitenhelft rechtsboven 12, binnenhelft van het licht af 5.
- **D onderste blad**: lichte bovenhelft 13, schaduwhelft onder 12.
- Muts blijft donkerder dan de baard (muts vooral 12/13/5, baard 14/13).
- Kleiner dan 3 px: alleen nerf- en randpixels (diagonale lijnen) en (36,2), 1 px buitenhelft in de punt van C.
