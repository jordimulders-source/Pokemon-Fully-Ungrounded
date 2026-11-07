# Keuring kolibrie pre-evo, kleur r4: afwerking (onafhankelijke eindkeurder, 2 nov)

Gekeurd: `kolibrie_pre.png` (`normal.pal`, `raster.txt`; png = raster, 0 px verschil). Eerst zelf geoordeeld, daarna pas `NOTITIES.md` en `kleur_r2/KEURING.md` gelezen.
Alleen de **afwerking** (Jordi: "nu moet de belijning nog beter etc, moet nu echt een gen 3 sprite worden"). Silhouet, ontwerp, kleuren, korte snavel en mus-read zijn vast en niet gekeurd.
Vel: `keuring_vel.png` (8× met raster en genummerde FAIL-zones, 8× Taillow en Swablu; 3× en 1× op licht en donker: r4, het reparatievoorstel, Taillow, Swablu, en op 1× ook Wingull, Natu, Pidgey, Zigzagoon, Spheal, Whismur, Skitty en Plusle).
Coördinaten: (x, y), 0-geteld, zoals in `raster.txt`. Indexen: `1` bijna-zwart, `2` donker violet (selout), `3`–`7` lijf licht→donker omgekeerd (3 donker, 7 wit), `A` grijsviolet, `B` kapbasis, `E` kapschaduw, `C`/`D` geel/oranje.

## Eerste indruk (zelf, vóór de notities)
Op 1× en 3× staat hij tussen Taillow, Swablu en Pidgey zonder op te vallen: rustige vlakken, 1-px lijn, lichtkant in gekleurde selout, schaduwkant bijna-zwart, weinig ruis. Dit is dicht bij Gen 3. Wat op 8× nog "zelfgemaakt" leest: de lichte vleugelrand en de donkere rugrand lopen als twee strepen van gelijke breedte mee met de omtrek, een paar omlijningspixels hebben de verkeerde tint (selout aan de onderkant, zwart midden op de kruin), een dubbele lijn waar lijf en staart samenkomen, en de verre poot is een dambordje.

## Metingen (eigen scripts, tegen 10 Gen 3-sprites: Taillow, Swablu, Wingull, Natu, Pidgey, Zigzagoon, Spheal, Whismur, Skitty, Plusle)
| meting | r4 | Gen 3-referenties |
|---|---|---|
| px / kleuren | 735 / 15 + transparant | 431–1127 / 10–15 |
| randpixels in de donkerste lijnkleur | 0,56 | 0,46–0,62 |
| contrast selout ↔ vulling (luminantie) | 128 | 53–89, Wingull (wit lijf) 167 |
| lichte kleur naast transparant, niet donkerder dan binnen | 3: `D` (11–13,18) | 0–6 |
| andere niet-`1`/`2`-randen | `D` (14,14) (13,15) (14,16) (14,17); `A` aan de poten | – |
| 2×2-klonten donker | 7: oog (4), poot (32,41)(32,42), **lijf/staart (36,39)** | Taillow 180, Natu 8 |
| ellebogen (dubbele pixel in een hoek, buitenlijn) | 4: snavelpunt (9,10)(9,11), hiel (28,43), staartaanzet (38,41) | 0–24 |
| losse pixels (geen 8-buur van dezelfde kleur) | 14 | 23–54 |
| 1-px stroken die ≥ 3 rijen parallel lopen | **13 px aan één stuk**: vleugelrand `3|4|B` (31,26)→(37,38); verder 2 korte (4 en 3 px) | langste keten 5; totaal 0–18 px |
| schaduwband `E` langs de rugomtrek | **exact 2 px breed op y 25–34 (10 rijen)** | Taillow: wisselend 0–4 |
| selout `2` aan de schaduw-/onderkant | 8: (21,39) (23,40) (24,40) (35,40) (39,41) + pootjes `A` | 0–15 |

Opmerking bij de notities: "open randen 0" klopt met de uitzondering voor `D`; die uitzondering neem ik grotendeels over (zie F1). De les van de maker zelf ("een band van gelijke breedte maakt een cilinder") geldt nog voor de rugschaduw `E` (F6).

## Tabel
| # | richtlijn | oordeel | waar / waarom |
|---|---|---|---|
| – | formaat, 16 kleuren, index 0 transparant | PASS | 64×64, 15 + 0. Tip: `7` (252,250,255) en `F` (255,255,255) zijn op het oog gelijk; één slot vrij te maken als ooit nodig |
| – | leest op 1× tussen echte Gen 3-sprites | PASS | licht en donker, naast 10 referenties |
| – | omlijning 1 px (geen klonten) | FAIL → F3 | dubbele lijn (36–37, 39–40); oog en pootjes zijn bewuste donkere delen |
| F1 | omlijning gesloten | FAIL | snavelbasis (14,14): oranje steekt boven de lijn uit in het gat tussen bovensnavel en voorhoofd; losse lijnstomp (15,15) |
| – | gaap in `D` als pseudo-omlijning | PASS | dun deel (2 px), `D` donkerder dan `C`, zoals de r2-keuring voorstelde; §8 pseudo-omlijning |
| F2 | zwart alleen aan de schaduwkant, selout aan de lichtkant | FAIL | onderrand flikkert `2 2 2 1 2 2 1` (19,38)→(25,41); selout aan de onderkant (35,40) en (39,41); kruin: zwart begint al midden bovenop (25,9)(26,9) |
| – | selout-contrast | PASS | 128, binnen de reeks (wit lijf, vgl. Wingull 167, Taillow-buik zwart naast wit) |
| – | losse pixels | PASS | 14, minder dan elke referentie; allemaal bewust (lidhoekjes, kin, keelglans, poot) |
| – | jaggies (ellebogen) | PASS | 4, allemaal op echte hoeken (snavelpunt, hiel, staartaanzet) |
| F7 | curven zonder besluiteloosheid | FAIL | onderbuik links: verticale stappen 3-3-1-1-1 (x 16: y 31–33, x 17: y 34–36, dan 1-1-1): abrupt van 3 naar 1 |
| – | kruin, achterhoofd, rug | PASS | kruin 4-2-2-2-1-1 en 4-2-1-1-1-1-2-4; rug 1-1-1-1-1-2-2-3-3-4: geleidelijk |
| – | rechte stukken ≥ 4 px waar rond | PASS (silhouet) | onderkant y 41 (10 px) en achterhoofd x 33 (4 px) horen bij het bevroren silhouet; Taillow heeft dezelfde vlakke zit-onderkant |
| F5 | geen banding (lichte vleugelrand) | FAIL | `4`-rand van 1 px loopt 13 rijen strak naast de `3`-lijn: (31,26)→(37,38). Langste keten bij de referenties: 5 |
| F6 | geen banding (schaduw langs de omtrek) | FAIL | `E` precies 2 px breed langs de rug, y 25–34; leest als een rand, niet als schaduw die de vorm volgt |
| – | buik: geen pillow shading | PASS | hooglicht linksboven, `5` als boog die naar onder breder wordt (1→4 px) |
| – | oog | PASS | donker boven, `E`-iris onder, glans 1×2, afgeronde hoekjes |
| F4 | details leesbaar, geen harken/dambord | FAIL | verre poot (31–34, 42–43) `A1 / A1A1`: dambord |
| – | nabije poot, staart, keelglans | PASS | nabije poot leest als poot met tenen; staartveren als korte diagonalen; keelvlek is ontwerp |
| – | licht linksboven | PASS | kap, buik en vleugel consequent |

## FAILs met reparatie (29 px, voorstel op het vel getoond)
1. **Snavelbasis (2 px).** (14,14) `D` → `1` (sluit de lijn bovensnavel → voorhoofd); (15,15) `2` → `C` (weg met de lijnstomp, de geel/lila grens doet het werk).
2. **Lijntint (6 px).** (23,40) en (24,40) `2` → `1` (onderrand wordt `2 2 2 1 1 1…`, één overgang); (35,40) en (39,41) `2` → `1` (onderkant = schaduwkant); (25,9) en (26,9) `1` → `2` (kruin in selout tot de afloop rechts, zoals Taillow).
3. **Dubbele lijn lijf/staart (2 px).** (36,39) en (37,39) `2` → `3`; de lijn (36–37,40) blijft.
4. **Verre poot (2 px).** (31,43) `A` → `1`, (32,43) `1` → `A`: wordt `1AA1`, een kleinere versie van de nabije poot `1AAA1` (geen kopie).
5. **Vleugelrand (8 px).** `4` → `B` op (32,31) (33,32) (33,33) (34,34) (35,35) (35,36) (36,37) (37,38): de lichte rand alleen aan de schouder (y 25–30), waar het licht valt; lager zit de lijn direct tegen de vleugel.
6. **Rugschaduw (7 px).** `B` → `E` op (37,29) (38,30) (38,31) (38,32) (39,33) (3 px breed waar het lijf het breedst is); `E` → `B` op (36,25) en (37,26) (1 px bij de schouder). Sikkel in plaats van band.
7. **Onderbuik links (2 px, raakt de omtrek met 1 px).** (17,36) `2` → transparant, (18,36) `6` → `2`: stappen 3-2-2-1-1. De maker verplaatste in r4 al 3 omtrekpixels om dezelfde reden; dit is er één van dat soort.

Na reparatie (gemeten op het voorstel): lichte kleur naast transparant alleen nog de bewuste `D`-gaap (11–13,18), langste parallelle strook 5 px (gelijk aan de referenties), geen selout meer aan de onderkant behalve het overgangspixel (21,39), alpha-diff 1 px.

## Oordeel: **TERUG**
Dichtbij: zeven kleine reparaties, samen 29 px, geen herbouw. De rest (vlakken, oog, buik, curven van kop en rug, selout-schema, ruis) haalt het Gen 3-niveau van Taillow en Swablu.
