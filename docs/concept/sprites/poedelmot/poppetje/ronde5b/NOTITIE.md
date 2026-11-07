# Poedelmot poppetje, ronde 5b (5 nov): alleen de ogen

Leidraad 6, "met grote donkere ogen, beetje venomoth achtig", was in ronde 5 niet voldaan: de ogen leken op stipjes.
De rest is pixel voor pixel ronde 5. Op 1× is het alfaverschil 0 en zitten alle 110 gewijzigde pixels in het kopvak.

## Wat er veranderd is
- **Maat:** `OOG` = (-0.82, -0.22, ±0.56), straal 10 (ronde 5: straal 8), gemeten naar de tak-foto en Venomoth. Zie de meting onderaan `vel.png` en in de keuring.
- **Facetrand:** een iets lichtere rand op het oog als facetglans (in `shade_aders`, normaal-z < 0,55, #55506A).
- **Glans:** één kleine glans linksboven op het nabije oog, geplaatst vanuit de kijkrichting, zodat hij geen pupil wordt.
- **Meting:** `oogmeting()` meet de oog- en kopbreedte op de render.

## Bestanden
- `pop3d_poedelmot_r5b.py`.
- `poppetje_45.png` en `poppetje_45_1x.png`.
- `vel.png`: het geheel (werk en 1× naast Butterfree en Venomoth), vak 1 (ogen) en de meting.
- `keurvel_45.png` + `keurvel_45.png.keuring.md`: eigen keuring met de leidraad opnieuw afgevinkt.

## Zwakke punten
- **Op 1× raken de ogen elkaar:** dan zie je één donkere band zonder wol ertussen.
- **De facetrand** is op 1× nauwelijks te zien.
