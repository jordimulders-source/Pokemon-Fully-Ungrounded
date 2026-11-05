# Kolibrie pre-evo – kleur r8 (maker)

Jordi over r7 (letterlijk): "de snavel hoeft niet afgekeurd te worden. De pootjes zijn niet ideaal en er blijft een gekke hoek links in die buik zitten. De schaduw in de vleugel vind ik ook niet lekker rond, is meer een lijn. En ja je mag wat pixels in het silhouet veranderen, maar ik hoef het silhouet niet te zien, alleen de sprite".

Bron: `bouw.py` = `kleur_r7/raster.txt` + met de hand geschreven rijstukken per zone → `raster.txt` + `kolibrie_pre.png`. `palet.py`/`normal.pal`: alleen `F` (vrij sinds r7) is nu poot donkerst (112,62,28). `controle.py`, `clusters.py`, `vel.py` → `vel.png` (alleen sprites: r8 op 4× en 1× op licht en donker naast r7, Taillow, Starly).

## Controle (`python3 controle.py`)
- alpha-diff met r7: 26 px, **alle binnen de zones**:
  - buik links +5/−1: (18,27) (19,28) (20,28) (19,29) (19,30) erbij, (19,35) weg;
  - pootjes +15: (25–26,44) (33–35,44) (25–27,45) (32–34,45) (26,46) (28,46) (31,46) (33,46);
  - rug −2: (36,24) (39,26); kop linksboven −1: (19,14); vleugelpunt −2: (41,42) (40,43).
- 54 px gewijzigd (kleur of alpha), geen enkele buiten de zones. **Snavel en oog: 0 px.**
- Open randen: 0. Rand rechts/onder overal zwart `1`; geen wisselende 1/2 erbij.
- Clusters < 3 px: 4, alle al goedgekeurd in r7: oogglans (23,19), onderglans (23,20), tapse vleugelrand (32,30) en (32,34).
- 619 px (was 605).

## Wat er veranderde
1. **Pootjes** naar Taillow/Starly. De nabije poot (x25–30) heeft een enkel `D`/`9` en twee tenen naar voren: (26,44–45) en (28,44–45) in `D`, met licht `C` op de voorste teen en donker `9` ertussen. Elke teen heeft een zwarte punt eronder (rij 46). De verre poot (x30–35) is donkerder (enkel `9`/`F`, tenen `9` met `F` ertussen) en staat er direct achter. Alles is omlijnd.
2. **Buik links**: de kin-inham (21,28) en de knik zijn weg. De linkerrand loopt nu als één boog: 16,16,17,17,18,18,19 (×7),20,20,21,22,22,23,24,25. De plooitint `5` op de keel is weg, zodat keel en buik één wit vlak zijn.
3. **Vleugelschaduw als sikkel**: `A` begint per rij op x40,40,39,39,38,38,37,36 (rij 29–36) en is 1 px breed bovenaan en 5 px onderaan. Daaronder is alles `A`. De tongetjes in de dekveren zijn weg, dus het licht `8` is één rond vlak. De rand blijft zoals goedgekeurd (`2`/`3` taps voor, zwart achter).
4. **Trapjes**: rug rechterrand nu 33,35,37,38,39,40 ((36,24) en (39,26) weg; (36,25) wordt zwart, (35–37,26) wordt schaduw `3`). Kop linksboven nu 4-2-2-1 ((19,14) weg, (19,15) wordt `2`). Vleugelpunt zonder haakse hoek ((41,42) en (40,43) weg, (40,42) wordt zwart).

## Eerlijke zwakke punten
1. De linker buikrand heeft nu een rechte verticale run van 7 px (x19, rij 28–34). Er is geen knik meer, maar op 4× leest dat stuk vlak. Een lichte bolling (x18 op rij 31–33) zou het ronder maken, maar geeft weer een kleine holte bij de hals.
2. De pootjes zijn groter dan in r7 (5–6 px breed, 3 rijen) en lezen op 4× als tenen. Op 1× zijn het nog twee oranje vlekjes met zwart. De verre poot staat naast de nabije en nauwelijks erachter, want er is geen ruimte om hem te laten overlappen.
3. De vleugelsikkel is rond, maar gebruikt maar twee tinten (`8`/`A`). Op 1× leest hij als licht vlak met donkere onderkant.
4. Blijft: de snavel leest op 1× als twee sprietjes (Jordi: niet afkeuren) en de sprite is zachter dan Taillow/Starly (mild lila).

## Lessen
- Silhouetwijzigingen per zone in het controlescript tellen (+/−) en ook kleurwijzigingen buiten de zones verbieden. Dan bewijst één run dat snavel en oog onaangeroerd zijn.
- Een sikkel in een vleugel lees je aan het beginpunt van de schaduwtint per rij. Laat dat versnellen (40,40,39,39,38,38,37,36) in plaats van een vaste stap. Een vaste stap leest als lijn.
