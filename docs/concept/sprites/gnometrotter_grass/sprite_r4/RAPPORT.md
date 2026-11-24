# Gnometrotter Grass r4 (maker, 23 nov)

Basis: `../sprite_hybride_r2/gnometrotter_grass_hybride.png`. Script: `python3 maak_r4.py` (maakt `gnometrotter_grass.png`, `_8x.png`, `vel.png` = model op schaal | basis | r4, en `log_r4.txt` met elke gewijzigde pixel: zone, x, y, oud→nieuw). Palet en indexen ongewijzigd (gecontroleerd in het script).

| Zone | Gewijzigde px | Wat |
|---|---|---|
| neus | 41 | Neus van Rock af (beide modellen hebben dezelfde neus: centrum 21,3/19,6, 8×8 px). Lichtbaardbladpixels (13/14) blijven ervoor liggen. Rock-index 12 (zeer donker roze) bestaat niet in het Grass-palet → 6. |
| schouder | 34 | Schouderovaal rechts van Rock af (rij 21–28, x 40–49): rond, met omlijning in 6, hooglicht 15 linksboven, 7 rechtsonder. Ligt voor de rugtak (1 bruine pixel op (47,22) overschreven). |
| linkerhand | 49 | Vuist + arm = Rock af (vorm, omtrek, tinten), x 0–19, rij 27–36. Stok blijft van de basis; alleen waar de vuist de stok overlapt (onderrand vuist rij 35) volgt Rock af. Baardblad blijft. Omtrek wijzigt hier (9 px: 0→6/1), zoals Rock af. |
| lijf | 217 | Romp: ton van drie planken met naden in 6 op x 29 en 35 (model: naden 29,5 en ±35), plank A (tussen de baardbladeren) 7, plank B/C 8 met 15 aan de lichte linkerkant bovenaan, 7 onderaan en rechts; rij 19 naast de neus 7 (schaduw onder de muts, was dambord 6/8). Benen: vier bollen (dij L, dij R, onderbeen L, voet R) met 11 linksboven, 10, 9 als sikkel rechtsonder; naden in 9 (kruisvouw, grenslijn dij/voet). Silhouet en buitenrand van de benen gelijk. Alleen indexen 6/7/8/15 en 9/10/11. |
| rest | 0 | Muts, bladbaard, haar, stok, zolen, riem, rugtak pixel voor pixel gelijk. |

## Twijfels
- Neusboog: Jordi wilde bij Rock "een zeer donkere roze tint"; het Grass-palet heeft daar geen vrije index (alle 16 in gebruik), dus 6. Een paletwissel (bijv. 15 of een groene index) zou nodig zijn voor exact Rock.
- Neus rechts op rij 21: baardblad (13) op (25–26,21) blijft ervoor, dus daar geen neusomlijning.
- Romp en benen zijn met regels per plank/bol ingekleurd (niet uit het model gemeten); de modeltextuur (stippen, gebreide ribbels) is bewust weggelaten (paar grote vormen). Benen hebben geen nerf.
