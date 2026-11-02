# Kleur ronde 2 (maker-agent, 2 nov)

Basis `ronde1.txt` + reparaties uit `KEURING_ronde1.md` punt 1–10, als expliciete pixellijsten per zone in `rijen_ronde2.py` → `ronde2.txt`, `ronde2.png`, `ronde2.pal`, `vel_ronde2.png`. Alpha-diff met `direct_s1a.txt` = 0; geen randpixel buiten 1/2/4/b/c (open randen dicht).

**Palet:** 3 (72,63,58) ging op in 4 (niet te onderscheiden). Index 3 = nieuw hooglicht-grijs (176,168,156). Crème selout = c (120,103,84, gelijk aan de buidelbasis).

| Zone | px | wat |
|---|---|---|
| oren/kop selout | 16 | zwart op de lichtkant van oren en kop → 4 |
| kop hooglicht | 5 | 3 op de schedel linksboven |
| masker | 13 | twee lobben met een smalle brug (16–17,10) over de neusrug, wenkbrauwboog (18,9), lobonderkant rond (19,14 a; 23–25 → grijs), streepje (16,12–13) weg |
| ogen | 11 | oogkas 4 onder/naast het nabije oog, bovenlid 4 breed, iris donker boven / licht onder (3 breed), glans; verre oog 1 px naar binnen (13,11–12) |
| romp | 20 | hooglichtboog 3 op schouder/borst, gebogen 6/5-grens (y 23–25), bovenarm-/kernschaduwlijn 4 (x 33, y 22–28 → x 35–37, y 28–32) |
| naad | 26 | dubbele naad (4 + b) → alleen b met 5 ernaast; onderkant buidel loopt via 5/b over in de rug |
| buidel | 31 | zakmond: gebogen spleet 1 (35,18)→(39,20), lichte lip d erboven, b eronder; plooi b (38,25)→(42,29) met lichte rug d |
| nabije klauw | 32 | klauwen tegen elkaar (24,30–31 → 9), inkeping alleen bij de punt (24,32–33); crème strook links → grijs 7/6/5; 2 punten |
| nabije onderarm | 30 | buis: bovenrand 5, midden 4, onder 2, rand 1; bovenarmlijn x 33 |
| verre klauw | 58 | crème selout c aan de lichtkant (rand dicht), schaduw 8 onderaan/rechts, hooglicht 9 boven; losse pixels (11,34), (17,30) weg |
| nabije dij | 23 | hooglicht 7 linksboven, schaduwhalvemaan 5 onderaan; (28,45) 1 → 4 |
| staart | 36 | lichte vierkant in de haak → 2, lichte rand 8 langs de bovenkant van de haak, schaduwlijn 1 onder de punt, ringranden 1 px lager aan de zijkant, open randen → 4 |

Niet gedaan (voor Jordi, volgens de opdracht): grijstemperatuur, crème handen, verre oog weglaten, buidelkleur, lichtere borst.

## Eigen zwakke punten (eerlijk)
- **Nabije klauw:** op 1x nog steeds vooral een witte vlek. De inkeping is alleen op 2x+ te zien.
- **Nabije onderarm:** leest beter als buis, maar op 1x is het nog een donkere vorm naast de klauw. De bovenarm is maar één lijn.
- **Zakmond:** de spleet is klein en leest op 1x niet als opening. De plooi leest als een lijn, niet als een vouw.
- **Oogkas:** de 4 onder het nabije oog kan als een wal onder het oog lezen.
- **Staartringen:** alleen de randpixels zijn gebogen; de ringen blijven in het midden recht. De haakkop is nu egaal donker, waardoor de haak op 1x nog als knots kan lezen.
- **Lijfschaduw:** het hooglicht is klein en de schaduw blijft in banen; nog doffer dan Coathief.
- **Losse pixels:** de resterende meldingen zijn bewuste details (glans, iris, hooglichtrand, nagels); niet elke pixel is op 1x getoetst.

## Lessen
- Een spleet met een donkere rij eronder én een omlijning ernaast werd drie diagonale strepen ("riem"); een zakmond is één donkere lijn met een lichte lip.
