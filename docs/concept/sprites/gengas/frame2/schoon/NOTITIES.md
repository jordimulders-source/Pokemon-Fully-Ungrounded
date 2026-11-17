# Gengas frame 2 (combi_c): opschoning van de rotatie-artefacten (16 nov)

Bron: `../combi_c_anim_front.png` (frame 2 = nearest-neighbour-rotatie 10° rechtsom van `sprite_v15/lijf_zonder_manen_v15.png`, 3 px omhoog, manen erop).
Script: `schoon.py` (draaien vanuit de repo-root). Uitvoer: `combi_c_anim_front_schoon.png` (64×128), `voor_na.png`, `combi_c_v_slide_schoon.gif` (zelfde `render`/`vslide` als `combi_c.py`), `gewijzigd.txt` (elke pixel: y,x: oud -> nieuw; y in frame 2, 0..63).

## Werkwijze: overnemen, niet tekenen
- Bij de rotatie gingen pixels verloren of werden ze verdubbeld (in ogen, tanden en lippen). Er is niets met de hand getekend: ogen en grijns zijn **letterlijk uit frame 1 overgenomen**, op de plek waar de 10°-rotatie ze neerzet.
- **Ogen:** elk oog als één geheel verplaatst (links: 6 omhoog; rechts: 4 omhoog, dx 0, zoals in de rotatie). Daardoor is het pixelpatroon precies dat van frame 1.
- **Grijns:** opgedeeld in 4 vaste stroken (lijf-kolommen 8–19, 20–24, 25–34, 35–36), elk met de rotatieverschuiving van het midden van die strook (dy −6/−5/−4/−3, dx −1). Elke tand en elke scheiding is daarmee pixel voor pixel die van frame 1. De helling komt uit trapjes van 1 px op de naden. Die naden liggen vlak vóór een tandscheiding, zoals een spriter een schuine grijns zou trappen.
- Bij het overnemen bleven de omlijning (pixels met een transparante buur), de manen en de transparante pixels altijd onaangeroerd.
- Een RotSprite-variant is ook geprobeerd. Die geeft schonere randen, maar breekt tandscheidingen en de omlijning (o.a. (31,7) en (42,10)) en is daarom niet gebruikt.

## Gewijzigde pixels: 118
| Plek | px | Wat |
|---|---|---|
| Linkeroog | 8 | Er stond een rode pixel boven de 9-kolom (26,11) en (30,11) ontbrak. De wenkbrauwdiagonaal (2) loopt weer zoals in frame 1 en een verdwaalde 2 op (24,11) is weg. |
| Rechteroog | 16 | Een gat in de lichte vlek (28,29), een 9 midden in de lichte vlek (29,30), de onderrand 9999 met een `a` erin (33,25–30) en de ooglidlijn 22 lag 1 px verschoven. Het oog is nu het patroon van frame 1. Twee overgebleven 2'en rechts van het oog, (26,32) en (27,32), zijn weg (door de oogverplaatsing). |
| Grijns + lippen | 81 | Een 5 in de bovenlip (37,23), een 2 midden in de tanden (38,23), gebroken en dubbele scheidingen (8/e) en het lichtgrijze hoekje links (nu op (35,10), zoals frame 1). De mondhoek rechts (e + witte punt + zwarte lijn) en de 6-band onder de onderlip volgen nu frame 1. |
| Losse randpixels | 13 | Zie hieronder. |

Losse reparaties (y,x in frame 2):
- (37,8) 1→6: dubbele omlijning links naast de grijns.
- (40,10) 3→5: randje naast de grijns (frame 1: 1-5-5).
- (43,11), (44,11) 3→1: gat in de omlijning linksonder.
- (46,46), (49,16), (51,40) →1: trapjes in de omlijning onderaan zonder hoekpixel (lijn was niet 8-verbonden).
- (30,52) leeg→1: deuk van 1 px met een gat in de omlijning rechts (silhouet +1).
- (10,53) 5→1, (12,54) 7→1: de oorpunt rechts heeft weer een gesloten zwarte punt zoals frame 1 (de lijn was onderbroken tussen (12,55) en (13,53)).
- (18,59) leeg→6, (18,61) 6→leeg: het puntje `66` van de gasarm zweefde los (1 px gat). Het staat nu 1 px naar links en zit weer vast, zoals in frame 1 (silhouet: +1 en −1).
- (37,34) 1→5: dubbele zwarte lijn in de rechtermondhoek (naad van strook 3/4).
- (43,24) 8→2: een tandscheiding stak door de onderlip (naad van strook 2/3).

## Controles (asserts in het script)
- Frame 1 ongewijzigd; alle 418 maanpixels pixel voor pixel gelijk; geen nieuwe paletindex.
- Silhouet: 3 px verschil ((30,52) erbij, (18,59) erbij, (18,61) eraf). Grootte, positie, hoek en manen zijn ongewijzigd.
- Niet aangeraakt: de banden en tinten in de bol (alleen waar ze binnen de overgenomen oog- en grijnsstroken vallen), het oorpluimpje linksboven, het bultje links op (32–33,6) (een vloeiende rondingspiek, geen fout) en de selout aan de bovenkant.

## Open / voor de keurder
- Het oog staat letterlijk zoals in frame 1 (niet 10° gekanteld binnen het oog). Kantelen kan alleen door het oog te vervormen, en de opdracht was "zelfde pixelpatroon".
- Het bultje links op rij 32–33 (x6) is bewust blijven staan. Zie je het als een rotatietrapje, dan is het 2 px weghalen.
