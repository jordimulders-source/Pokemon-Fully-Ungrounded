# Kolibrie pre-evo – kleur r5 (maker)

Jordi over het oog (letterlijk, laatste woord): "houd het starly oog maar" · "dan maar geen kleur". (Eerder: "doe maar combusken, maar de snavel op de combusken sprite is niet goed, dus, houd daar rekening mee" en "alhoewel, die kijkt idd wat boos"; beide vervangen door het Starly-oog.)
Opdracht verder: vleugel meer contrast met het lijf zodat hij als eigen plaat leest (zoals Taillow/Starly), rand netjes en zacht, geen harde strepen; rest van r4 gelijk.

Bron: `bouw.py` neemt `kleur_r4/raster.txt` en past twee dingen toe → `raster.txt` + `kolibrie_pre.png`; `palet.py` → `normal.pal`; `controle.py`; `vel.py` → `vel.png` (r5 op 1×/2×/4× licht en donker, naast r4, Taillow, Starly, toonkaart).

## Controle (`python3 controle.py`)
- alpha-diff met `kleur_r4/silhouet_r4.txt`: **0**.
- Snavelzone (x≤20, y13–22) t.o.v. r4: **0 px** afwijkend (snavel, mondhoek, gaap ongewijzigd).
- 138 px gewijzigd t.o.v. r4, **allemaal binnen oogvak (x21–25, y16–21) of vleugelvak (x31–41, y27–42)**; daarbuiten 0.
- Oog x21–25 y17–21 = `maker/kleur_r10/raster.txt` x21–25 y14–18 pixel voor pixel (zwart, witte glans, onderglans `5`, rand `2`): waar.
- Open randen: 0. Losse pixels: alleen bedoelde (kapselout-diagonaal, onderglans oog (23,20), nekplooi (29,25), veerstreepjes (35,36)(36,37), (38,41)(39,42)).
- 16 kleuren.

## Wat er veranderde
1. **Oog**: Latias-oog eruit, Starly-oog terug op x21–25 y17–21 (zoals r1–r3). Gezichtspixels waar het Latias-oog groter was terug naar huidkleur: (23–25,16) `5`, (21,17) `5`, (25,17) `4`, (21,21) `4`, (25,21) `3`.
2. **Palet**: smaragd eruit. `8` = **vleugel basis (90,78,164)**, `A` = **vleugel schaduw (62,54,130)**; `B`/`E` blijven voor de kap. Vleugel is daardoor ±50 luma donkerder dan de flank `4` (was ±40 voor `B`).
3. **Vleugel**: dezelfde vormen als r4 (dekverenvlak, twee tongen, lichte veerstreepjes, donkere onder-/voorrand `2`), nu in `8`/`A`, met een **zachte rand `E`** (1 px) langs boven- en voorkant: (35–38,27), (33–34,28), (32,29–30), (31,31–33), (32,34–35). De bovenrand is rond gemaakt: (33–34,27) zijn nu lila `4`. Geen zwarte lijnen erbij.

## Eerlijke zwakke punten
1. De zachte rand `E` (luma ±73) ligt dicht bij de vleugelbasis `8` (±87); op 1× leest de vleugel vooral door het donkerdere vlak, de rand zelf zie je pas op 4×.
2. De vleugel is nu een vrij egaal donker vlak; de lichte veerstreepjes (`8` op `A`) zijn subtiel, dus de veerrijen lezen op 1× nauwelijks.
3. Uit r4 blijven: flank `4` als smalle baan tussen buik en vleugel, druk stuk nek/schouder, kleine pootjes, laag contrast van kop en buik vergeleken met Taillow.
4. Het Starly-oog is 3×5 en smal (zwart met witte middenkolom); dat is bewust teruggezet, geen iris.

## Lessen
- Bouw een reparatieronde als patch op het vorige raster (vakken met coördinaten) in plaats van alle rijen opnieuw; dan bewijst één diff dat alles buiten de vakken gelijk bleef.
- Bij het overnemen van een oog uit een ouder raster alleen de oogpixels kopiëren, niet de gezichtspixels in de hoeken van het vak (hier gaf `5` op (21,21) een los pixel).
