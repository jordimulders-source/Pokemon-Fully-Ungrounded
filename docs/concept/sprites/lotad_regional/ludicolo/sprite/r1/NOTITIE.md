# Gaucho-Ludicolo, frontsprite ronde 1 (maker, 25 nov)

Model: `../../r6/gemini_r6.png` (onaangeroerd). Pipeline van de gaucho-Lombre (`../../../lombre/sprite/r1/`) hergebruikt.

## Bestanden
- `ludicolo_gaucho_0.png`: kale opgeschoonde reductie, zonder ponchowijziging.
- `ludicolo_gaucho_A.png`, `_B.png`, `_C.png`: ponchovarianten (alleen lijnenwerk in de poncho).
- Alle vier: 64×64, P, index 0 transparant, **14 kleuren incl. transparant**, figuur **51×62** (x6–56, y1–62; hoedrand bijna tot de rand, voeten op rij 62), 1955 px. Silhouet-diff tussen alle varianten en met de kale reductie: **0**.
- `vel.png`: model | 0 | A | B | C op 4×; ponchouitsnede 8×; 1× en 2× op licht en donker naast de gaucho-Lotad en gaucho-Lombre.
- Scripts in volgorde: `pitch.py` → `natief.py` → `kmeans.py 18` → `quant.py` → `kaal_vlak.py` (gebruikte reductie) → `bouw.py` (variant 0) → `ponchomasker.py` + `varianten.py` (A/B/C) → `controle.py`, `vel.py`. Hulp: `toon.py` (sprite naast model), `raster.py` (uitsnede met raster). `kaal.py`/`kaal.png` = de schrapmethode van de Lombre, alleen ter vergelijking (niet gebruikt, zie onder).

## Werkwijze
1. **Natief raster:** pitch **10,24 px** (= 1024/100) in x en y, fase 9,25, zelfde als de Lombre; spreiding binnen een cel 0,88 (raster klopt). Figuur natief 75×91.
2. **Kleuren:** k-means (18) op de figuurpixels; elke cluster naar één paletindex (`quant.py`). De donkere olijfclusters (50,35,23) en (72,63,42) komen in het rode lijf ook voor als donkerbruine lijnpixels: buiten het gezicht, waar rood in een 5×5-venster ≥ 3× zoveel is als olijf, → zwart resp. rode lijn (57 natieve px).
3. **Verkleinen 0,68× (75×91 → 51×62):** eerst geprobeerd met schrappen (`kaal.py`, 24 kolommen, 29 rijen): bij 1/3 schrappen breken 1-px-lijnen (mond, bladlijnen, ogen) te veel. Gebruikt: **vlakstemming** (`kaal_vlak.py`): per spritepixel de modelkleur met de grootste oppervlakte in zijn cel, met voorrang voor lijnen (zwart/rode lijn/olijflijn) als die ≥ 30 % van de cel bedekken. Elke pixel is een modelkleur; geen RGB-middeling, niets getekend.
4. **Variant 0 (`bouw.py`, 130 px t.o.v. de kale reductie):**
   - gezicht naar het model (7 px): linkeroog iris aan beide kanten van de pupil (model L K L): (22,25)→rood donker, (22,26)→rood licht; rechteroog pupil los van de hoedrandlijn (28,24)→rood diep, pupil 2 hoog (28,27)→rood midden, iris links (27,26)→rood mdonker; mond 1 px dik zonder dubbele stukken: (20,31) en (19,32) → geel licht.
   - buitenlijn (92 px): rand rechts/onder aan de achtergrond zwart; rand alleen links/boven selout in de lijntint van het materiaal (rood 2, olijf 8), zoals Lotad/Lombre.
   - losse tintpixels (31 px, niet in het gezicht) → meest voorkomende buurtint uit dezelfde kleurgroep.

## Palet (index: kleur, herkomst)
0 transparant · 1 zwart (20,16,18) = Lotad/Lombre · rood: 2 lijn (108,44,30) = Lombre (model 111–126), 3 diep (136,60,42) model 138, 4 donker (160,74,50) = Lombre (model 149–158), 5 middendonker (186,94,64) model 178–188, 6 midden (204,114,80) = Lombre (model 202–214), 7 licht (230,154,112) = Lombre (model 206,138,102) · olijf: 8 lijn (66,56,30) = Lombre (model 50,35,23), 9 diep (86,76,44) model 72,63,42, 10 donker (110,98,58) = Lombre (model 88,83,53), 11 midden (156,142,86) = Lombre (model 137,128,79) · 12 geel donker (193,143,41) en 13 geel licht (240,200,73) = model · 14 en 15 vrij.
Rood heeft 5 vlaktinten (model heeft ze allemaal, op het lijf, de hoed en de benen verdeeld).

## Ponchogebied (`ponchomasker.py`, 513 px)
Rode/zwarte pixels van het lijf onder hoedrand en gezicht (vanaf rij 28; gezicht x15–35 t/m rij 34 eruit), zonder armen, linkervoet (onder de diagonaal (17,50)–(22,55)), rechterbeen (rechts van (32,47)–(24,55)), staart, en zonder lijnen die tegen arm/achtergrond liggen. De varianten raken alleen bladlijnen (zwart/rode lijn) **binnen** dit gebied aan, in rij 37–55, x ≤ 37; de schaduwkant onder de hoedrand, de halslijn onder de snavel en de rechter schouderrand naar de arm blijven het model. Zones: boven rij ≤ 41 (poncho), overgang 42–45, onder ≥ 46 (bladpunten). Geen pixels verschoven, alleen omgekleurd.

## Varianten (t.o.v. variant 0; silhouet-diff 0, alle wijzigingen binnen het ponchomasker)
- **A (38 px omgekleurd, 0 verschoven):** bovenaan verdwijnen de bladlijnen in het ponchovlak (tint = meest voorkomende vlaktint eromheen, de modelschaduw licht links → donker rechts blijft); in de overgang worden ze rode lijn; onderaan blijven de zwarte bladlijnen en punten van het model.
- **B (38 px omgekleurd, 0 verschoven):** als A, maar bovenaan worden de bladlijnen plooien (één tint donkerder dan het vlak) in plaats van te verdwijnen.
- **C (44 px omgekleurd, 0 verschoven):** als A, en ook onderaan worden de zwarte bladlijnen binnen de poncho rode lijn; zwart blijft alleen op de rand van de punten (tegen been, voet, arm, achtergrond), zodat de poncho als één stuk met een bladvormige zoom leest.

## Controle (`controle.py`)
Geen lichte kleur op de buitenrand. Losse pixels: 43 (0) / 42 (A–C), vrijwel allemaal diagonale lijnstukjes en gezichtspixels (oog, snavelrand: modeldetail, bewust niet aangeraakt); één 1-px rood midden op (16,46) in de poncho (model). Zwart 18,6 % (0), 17,5 % (A/B), 17,2 % (C).

## Twijfels / zwakke punten
1. **Varianten verschillen subtiel** (38–44 px): de meeste bladlijnen liggen in het onderste deel en op de rand van het ponchogebied (tegen been/voet), en die bleven model. Wil Jordi meer poncho, dan is de volgende stap pixels schuiven (bijv. de zwarte linkerbladlijn x14–20, rij 40–53), nog niet gedaan.
2. **A en B zijn op 1× bijna gelijk.**
3. **Geel = model** (240,200,73), feller dan de Lotad-snavel (232,204,124) en de Lombre-mond; niet bijna gelijk, dus niet overgenomen. Moet de snavel de Lotad-tint krijgen (zoals bij Lombre), dan is dat een paletwissel van index 12/13.
4. **Ogen** zijn op 1× klein (pupil 1×2 met rode iris en olijfmasker, zoals het model); leesbaar op 2×, op 1× zwak.
5. Rood heeft 5 vlaktinten (meer dan de ≤ 3-regel per kleurgroep), allemaal uit het model; een eindkeuring kan ze per onderdeel terugbrengen.
6. Nog geen keurder en geen DC-eindkeuring (schaduw, belijning, kleurtinten).
