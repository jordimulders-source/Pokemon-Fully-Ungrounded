# Lama fase 2: kleur ronde 4b (zelfde maker, 3 nov)

Reparatieronde op ronde 4, met precies de 9 reparaties uit `../ronde4/KEURING.md` en de besluiten van Claude. Het hele raster is met de hand getypt in `bron/lama_raster.txt` (één letter per pixel). Er is één oog; de A/B/C-varianten vervallen. Palet en `normal.pal` zijn gelijk aan ronde 4.

## Bestanden
- `lama.png` (indexed, 16 kleuren, index 0 transparant) en `normal.pal`.
- `raster_grid.txt`, `diff_silhouet.txt` (afwijkingen t.o.v. ronde 6 met de dekking van het model en de reden per pixel, plus een kaart), `vel.png`.
- Scripts in `bron/` (alleen bouwen, controleren en kijken): `bouw.py`, `controle.py` (uitvoer in `controle_uitvoer.txt`) en `vel.py`.

## Reparaties en kosten (diff t.o.v. ronde 4: 246 px; budget ±225)
| # | wat | px | waarvan omtrek |
|---|---|---|---|
| R1+R2 | **Lijf:** lichtkoepel `h` op borst en schouder en een tweede op het achterwerk. `h` gaat van 2 % naar 6 % van de hele sprite (±12 % van het lijf). Ronde schaduwsikkel b→s langs achterwerk en buik. Grens licht/midden als 5 hangende wolbollen op y38–39 (x14–20, 22–26, 28–32, 34–38, 40–42). Losse spikkels weg. **Omtrek:** wolbogen binnen ±1 px: borst x13 y34–37 en y41, achterwerk x51 y30 en y32–34 met een insnoering op x50 y36, en een insnoering in de rug op x42 y26. | 144 | 11 |
| R3 | **Hals:** stippelkolom vervangen door 2 lichte C-bogen (y20–22, y24–26) en een lichtplek op de schouder (y27–28); gladde schaduwband rechts (b b s d). De hals blijft recht. | 27 | 0 |
| R4 | **Staart:** pluim van 5×3, schuin naar achteren (top x49–50 y23), met een `h`-kruin, een donkere voet (`s`) en 1 px lucht aan de rugzijde (x46 y25–26). | 12 | 5 |
| R5 | **Verre achterpoot:** eigen donkere tint (`d`/`s`) vanaf y44, met een doorlopende `k`-scheiding naar de nabije poot. Eigen hoef (`v`/`n`) op x48–49 y58–59, rechts van de nabije hoef. | 25 | 1 |
| R6 | **Handschoenen:** de verre is donkerder (r/m, geen `o`). De nabije houdt `o`-licht linksboven. Doorlopende `k`-lijn x21–22 y57–60. De verre nagel staat nu op (24,61). | 6 | 0 |
| R7 | **Doek:** bovenhoeken afgerond (−x29 en −x37 op y25). Plooi in het rood (`m` op x35 y30–33). Licht linksboven (`o`). De zoom hangt in het midden door (`m` x31–36 y34; de hoeken liggen hoger op y33). Hij leest nu als trommel/zadeltas, zoals het model. | 27 | 2 |
| R8 | **Oog:** het lid van B (zakt achteraan) met de iris van C (`n`, liggende pupil `kk`, crème lichtje vóór-onder) en de wal van B. | 5 | 0 |
| R9 | **Open randen:** pseudo-omlijning (§8) blijft op het oor van 2 px en de nagels van 1 px; die lezen op 1×. Twee nieuwe randpixels omlijnd (staart x48 y24 en buik x14 y41). | (in R1/R4) | |

**Over budget:** 246 in plaats van ±225 px. Het meeste zit in het lijf (+24, door de lichtkoepel die het grootste deel van de borst bestrijkt), de doek (+15, plooi en doorhangende zoom) en de verre achterpoot (+13, de hele strook kreeg een nieuwe tint).

## Controles (`bron/controle_uitvoer.txt`)
```
mode P | transparency 0 | palet 16 | kleuren 16 (incl. transparant) | 1167 px
silhouet t.o.v. ronde 6: +14 / -10 (24 px), alle <= 1 px van de 50%-grens van het model (diff_silhouet.txt)
open randen 0 (pseudo-omlijning §8: oor x17 y3/7/8, nagels (24,61), (14,62), (16,62))
diff t.o.v. ronde 4: kop/oren buiten de oogzone 0 px | halsband + pompons 0 px | oog 5 px
verdeling: l 20 %, b 16 %, d 16 %, s 12 %, k 9 %, h 6 %
```

## Bekeken op 1×, 3× en 4× (vel.png), naast Mareep, Flaaffy, Girafarig en de alpaca
- **Lijf:** het lijf leest als één zachte wolmassa met licht linksboven en een ronde schaduw rechtsonder. De omtrek heeft bollen op borst en achterwerk, dus het is geen plank meer. Het blijft langer en rechter dan Mareep: dat is de lamavorm van het model.
- **Hals:** recht en zacht, met lichte bogen in plaats van stippels.
- **Staart:** een eigen pluim achter op de rug.
- **Doek:** leest als doek of zadeltas met een plooi, niet als koffer.
- **Oog:** op 1× een grijsbruin, half geloken oog onder een zwaar lid; geen streepje.
- **Poten:** de verre achterpoot leest op 3× als donkere poot met een eigen hoef. Op 1× is hij smal, want het model laat hem maar 1–2 px breed zien.
- **Handschoenen:** op 3× gescheiden door de zwarte lijn; de verre is donkerder.

## Lessen
- Een lichtkoepel in de lichtste tint (±12 % van het lijf) geeft meer volume dan veel middentint met spikkels. Mareep werkt zo.
- Wolbollen op de grens licht/midden in twee rijen (5 breed, dan 3 breed en gecentreerd) lezen als wol. Eén rij met afwisselende pixels leest als een band.
- Een plooi plus een doorhangende zoom maakt van een rechthoek een doek; franje maakt er druppels van.
- Tel na elk met de hand getypt rijstuk de lengte na: een rij die 1 px te lang is, zet stilletjes pixels buiten het silhouet (hier x51 y37–39). De controle met de 50%-dekking vangt dat.
