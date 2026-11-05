# Kolibrie pre-evo – kleur r6 (maker)

Jordi over r5 (letterlijk): "ja het blijft een beetje een slordige sprite, ik twijfel ook over de grootte van het oog".

Bron: `bouw.py` = `kleur_r5/raster.txt` + met de hand herschreven rijen in `rijen_r6.txt` → `raster_basis.txt`, daarna drie oogmaten → `raster_{S,M,L}.txt`, `kolibrie_pre_{S,M,L}.png`; `kolibrie_pre.png`/`raster.txt` = M. `palet.py` → `normal.pal`. `clusters.py` (tintclusters < 3 px), `controle.py`, `vel.py` → `vel.png` (r6 naast r5, Taillow, Starly, toonkaart) en `oog_maten.png` (S/M/L op 4× en 1×, licht en donker, naast Starly en Taillow).

## Controle (`python3 controle.py`), voor S, M en L
- alpha-diff met `kleur_r4/silhouet_r4.txt`: **0**.
- Snavelzone (x≤20, y13–22) t.o.v. r4: **0 px** afwijkend.
- Open randen: 0.
- Tinten per kleurgroep (luma): kop/lijf lila `5/4/3` = 184/146/103; buik `7/6/5` = 255/224/184; vleugel `8/A` = 96/63; kap `B/E` = 103/67; omlijning `2/1` = 59/18. Hooguit 3 tinten per groep + omlijning.

## Tintclusters < 3 px (`clusters.py`)
**Vóór (r5): 17.** E (26,14), E (27,15), E (28,16) [kapselout]; 7 (23,18)(23,19) en 5 (23,20) [oog]; 3 (30,24)(31,24) en 3 (29,25) [nek]; E (33,28)(34,28), E (32,29)(32,30), E (32,34)(32,35) [vleugelrand]; 8 (35,36), A (35,37), 8 (36,37)(36,38) [veerstreepje]; A (37,41), 8 (38,41), A (38,42), 8 (39,42) [vleugelpunt].
**Na (r6): M 2, S 2, L 1, alleen de bewuste glans/onderglans in het oog** (M: 7 (23,18)(23,19), 5 (23,20); S: 7 (23,19), 5 (23,20); L: 5 (24,20)).
Oplossingen per cluster:
- Kapselout: (26,14) → `2` (omlijning bovenop, anders open rand), (27,15)/(28,16) → `B`; de kapschaduw `E` begint nu op rij 17 en is één samenhangende sikkel tot rij 22.
- Nek: plooilijn `2` en losse `3`'s weg. Alleen één tapse schaduw `3` onder de kop (5, 4, 3, 2, 1 px breed op rij 23–27) met een kleurgrens naar de schouder `4`; het schouderlicht `5` en de dubbele randpixel zijn weg.
- Vleugelrand: zachte rand `E` (losse stukjes) vervangen door een doorlopende rand in omlijningskleur `2` langs boven- en voorkant (lijnen tellen niet als tintvlak), achterrand zwart.
- Veerstreepje en punt: losse `8`/`A` opgenomen in de vlakken. De dekveren `8` hebben nu twee tongen die aan het vlak vastzitten: (33–34,34–35)+(34,36) en (36,34–35), met de inkeping (35,34–35) in `A`. Onderste deel van de vleugel één rustig `A`-vlak.
- L: (27,19) `4` werd los door de bredere oogrand → `3` (samen met de schaduw eronder).
- Grens flank `4`/schaduw `3` onderaan rechtgetrokken tot een gelijkmatige diagonaal (x32, 31, 30, 29, 28 op rij 36–40) in plaats van de sprong 30→27.

## Contrast
Taillow gemeten: helderheidsstappen ±35 (blauw 107→72→43→zwart 16, rood 123→87, wit 255→191). Onze stappen nu: lila 38/43 (was 36/48), buik 31/40, vleugel 33 (was 26), kap 36 (was 30), daarna omlijning `2` 59 en zwart 18. Lila is iets donkerder/koeler gezet (`2`, `3`, `4`), buik `6` iets donkerder, vleugel donkerder dan het lijf (±50 luma onder de flank), zodat hij als eigen plaat leest.

## Oogmaten (zelfde opbouw als het Starly-oog: zwart, witte glanskolom, onderglans `5`, rand `2`; geen iris)
- **S** (5×4, x21–25 y18–21): één glansrij minder dan M.
- **M** (5×5, x21–25 y17–21): het Starly-oog uit `maker/kleur_r10`, ongewijzigd (zoals r5).
- **L** (6×6, x21–26 y16–21): rond (hoeken in `2`), glans 3 px linksboven, onderglans 1 px rechtsonder.
De rest van de sprite is in alle drie gelijk.

## Eerlijke zwakke punten
1. Het contrast is meetbaar zoals Taillow, maar de sprite blijft lichter dan Taillow, omdat het lila zelf licht is (mild lila is de familie). Op 1× leest hij nog altijd zachter dan Taillow/Starly.
2. De vleugelrand is nu een doorlopende lijn in `2`. Dat is netjes, maar een echte lijn. De veerrij zie je alleen nog als twee tongen; op 1× leest de vleugel als één donkere plaat zonder veren.
3. L leest op 4× als groot glimmend oog; op 1× is het verschil tussen M en L duidelijk, tussen S en M klein.
4. Blijft uit r4: kleine pootjes (2×2 en 2×1), smalle flankbaan tussen buik en vleugel.

## Lessen
- Een clusterscript (4-samenhangend, zelfde index, < 3 px) vindt precies de "slordige" pixels; los ze op door ze bij het grotere buurvlak te voegen of een rand als doorlopende lijn in omlijningskleur te zetten.
- Een zachte rand in een vlaktint die alleen diagonaal doorloopt telt als losse pixels; gebruik daarvoor de omlijningskleur (lijn) of een 4-samenhangend vlak.
- Helderheidsstappen van Taillow (±35 luma per tint) zijn een bruikbare maat voor "niet flets".
