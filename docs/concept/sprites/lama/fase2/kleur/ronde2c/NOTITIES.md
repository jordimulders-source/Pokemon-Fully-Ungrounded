# Lama fase 2: kleur ronde 2c (nieuwe maker-agent, 2 nov)

Uitgangspunt `../ronde2b/lama.png` + `normal.pal`. Opdracht: de FAIL-punten uit `../ronde2b/KEURING.md` (R1–R5 en de spikkels).

Bevroren (pixeldiff 0, zie onder):
- het silhouet ronde 2 en het palet;
- de kop (behalve de snuit), het oog, de oren, de wolhals uit 2b en de halsband;
- de handschoenvormen en de achterpoten.

Jordi (letterlijk):
- "de poten zijn nog net wat te hoekig he, plus 1 is een rechte lijn, plus ik vind het kleurgebruik nog niet helemaal pokemon like, vooral de vacht. Plus het is ook net niet genoeg een lama meer sinds de vertaling naar sprite"
- "ja hij moest wat meer fluffy zijn vooral"

## Bestanden
- `lama.png` (P, 64×64, transparency 0, 16 kleuren), `normal.pal` (byte voor byte gelijk aan 2b), `raster_grid.txt` (het volledige raster).
- `vel.png`:
  - rij 1: 2c op 4× (licht en donker), met 2b op 4× ernaast;
  - daaronder op 3× (licht en donker) en op 1× (licht en donker): 2c, 2b, de alpaca, Flaaffy, Stantler en Ponyta.
- `bron/`:
  - **met de hand getypte overlays** (`rij x0 pixels`) op het 2b-raster: `romp.txt`, `poot.txt`, `aguayo.txt`, `snuit.txt`, `nagels.txt`;
  - `bouw.py` (raster + overlays → png; controleert dubbele pixels en pixels buiten het silhouet), `controle.py`, `diff_2b.py` (diff per zone), `vel.py`, `zoom.py` en `kijk.py`.
- **Geen tintwissel-scripts:** elke pixel in de overlays is getypt.

Bouwen: `python3 bron/bouw.py && python3 bron/controle.py && python3 bron/diff_2b.py && python3 bron/vel.py`

## Controles
```
mode P transparency 0 | pixels 1278 | alpha-diff 0 (silhouet/ronde2.txt)
kleuren gebruikt: 16 | palet = 2b | open randen: 0
diff t.o.v. 2b: R1 85 | R2 10 | R3 12 | R4 6 | R5 2 | spikkels 2 | BUITEN de zones: 0 | totaal 117
```
Zones in `diff_2b.py`:
- R1: x18–53, y30–40
- R2: x30–36, y41–56
- R3: x34–53, y23–29
- R4: x10–17, y19–23
- R5 en de spikkels: alleen de genoemde pixels

**Het budget is overschreden: 117 px tegen ±80, waarvan R1 85 px tegen ±45.** De banden (y32–34), de stempelschulpen (y35–37) en de liniaal (y38) lopen elk over ±28 px breed. Ze vervangen raakt vanzelf elke pixel in die rijen. Met 45 px blijft een van de drie banden staan. Volgens de norm wint een pixelgrens niet van de vorm, dus ik meld het hier in plaats van te bezuinigen.

Vachtverdeling (heel de sprite): s 32% | b 23% | l 21% | d 20% | h 3%. In 2b was het s 44% van de romp.

Losse pixels in de zones zijn allemaal bewust:
- (39,34) h: wolpunt op klont C;
- (40,37) d: diepste punt van de rand van C;
- (35,39), (40,39), (44,39) d: de tussenruimtes van de franje.

## Per punt
**R1 romp (85 px, `romp.txt`).** Eén bol volume met het recept van de hals.
- **Licht:** een ronde lichtvlek linksboven op de schouder en de rug (x21–34, y30–35, h op (28,32) en (23,35)). Die loopt naar rechts af in b. Onder de aguayo ligt de slagschaduw s op (38–40,32).
- **Kernschaduw:** volgt de ronde buik. Ze ligt links hoog (y37 onder de schouder), in het midden het laagst (y38) en loopt rechts weer op onder het achterwerk (y37).
- **Vier klonten**, verspringend en van verschillende grootte. Elk heeft een lichte bovenkant en een s-rand rechtsonder die de ronding volgt:
  - **A**, groot: de schouder. De rand is een boog van (26,36) via (27–30,37) naar (35,33).
  - **B**, klein en laag: x33–36, y36–38, met een lichte kap op (33–35,36).
  - **C**, middelgroot, midden op de flank: x36–43, y34–37. De kap is l/h op y34–35, de rand loopt via (38,36), (39–40,37) en (41–42,36) naar (43,35).
  - **D**, middelgroot: het achterwerk, x45–50 y31–37, met de rand rond (46–48,37).
- **Franje:** drie schuine tongen in b, op (30–31,38) met (30,39), op (38–39,38) met (38,39) en op (43–44,38) met (43,39). Daartussen liggen d-gaten op y39 als teruggekaatst licht onderaan.
- **Weg:** de lichtband y32–34, de drie schulpen op x34, x40 en x46, en de s-lijn op y38. De spikkels (23,35), (28,32) en (32,33) zijn opgenomen in klont A.

**R2 verre voorpoot (10 px, `poot.txt`).**
- Een lichte b-strook aan de lichtkant volgt de S: x32 voor y45–47, x32 voor y52–53.
- De knie is een bolletje b op (33,48), (33–34,49) en (34,50). De losse (33,50) is erin opgenomen.
- De s op (33,50) en (32,51) onder de knie laat hem loskomen. De kern blijft s, de rechterrand k.

**R3 aguayo (12 px, `aguayo.txt`).**
- Het grijze blok op (45–47,27–29) is weg. De gele en de blauwe streep lopen door tot x45 en buigen op x46 in m (schaduw) weg, met een k-rand op (47,28). Zo leest de doek als lap die over de rug wegvalt, niet als slot.
- Het nopje (44–45,24) is nu m m, een kwastje.
- (37,24) en (51,24) gingen van k naar d.

**R4 snuit (6 px, `snuit.txt`).**
- Het neusgat staat nu op (12,20), los van de rand. (11,20) en (12,21) zijn s.
- De splitlip is een d-naad op x13 (y21–22) met een lichte onderlip in s op (14–15,22). De zigzag van k en d is weg.

**R5 nagels (2 px, `nagels.txt`).**
- De pixel tussen de twee nagels is donker gemaakt: (22,55) en (29,61) van r naar m. Elke nagel is nu een losse lichte stip in een donkere rand.
- **Een nagel van 2 px kan niet binnen het bevroren silhouet.** De pixel onder elke nagel ((21,56), (23,56), (28,62), (30,62)) is een randpixel naast transparant. Het advies uit de keuring (s daar) geeft open randen. Ik heb het silhouet niet veranderd.

**Spikkels (2 px).**
- (43,51): b naar s.
- (48,56): s naar b, zodat de lichte strook van de nabije achterpoot doorloopt.

## Eigen keuring
Bekeken op 12×, 8×, 4×, 3× en 1×, op licht en donker, naast 2b, de alpaca, Flaaffy, Mareep, Altaria, Stantler en Ponyta.
- **Romp:** geen banden, stempels of liniaal meer. Op 3× en 4× leest de romp als één rond wollig lijf met licht op de schouder en een klont midden op de flank. Het licht ligt zoals bij Stantler en Mareep: één vlek linksboven, schaduw onderaan.
- **Verre voorpoot:** leest als ronde poot met knie, niet meer als paal.
- **Aguayo:** gestreepte doek zonder slot of handvat.
- **Snuit:** neusgat en splitlip lezen op 3×.

Wat eerlijk nog niet (helemaal) leest:
- **Klonten op 1×:** op 1× zie je vooral het volume (licht boven, schaduw onder) en geen banden. De losse klonten B en C zijn op 1× subtiel; zichtbaar worden ze pas vanaf 3×. Meer "fluffy" op 1× moet uit de omtrek komen (bevroren silhouet). Binnen de kleur heb ik C en B in een tweede pas al versterkt (grotere lichte kap, één d in de diepste rand). Nog meer contrast maakte de buik spikkelig (eerste versie, teruggedraaid).
- **Nagels:** 1 px, op 1× nauwelijks. Dit is een silhouetkeuze voor Jordi (zie "Voor Jordi" in de keuring van 2b).
- **Splitlip op 1×:** een naad van 2 px op een snuit van 7 px. Op 1× lees je hem als een donker puntje onder de neus, op 3× als splitlip.
- **Kwastje op (44–45,24):** blijft een uitsteeksel van 2 px in het silhouet. In m leest het als kwastje, maar de vorm komt uit het bevroren silhouet.

## Lessen
- Een budget per zone moet passen bij de fout. Een band over de volle breedte wegwerken kost minstens één pixel per kolom per band (hier 3 × ±28). Schat het budget dus vooraf op breedte × aantal rijen.
- De kernschaduw en de rand van een klont in dezelfde tint smelten samen. Laat de buik onder een klont iets lichter beginnen (b), of geef de klont één d op het diepste punt. Gebruik niet meer d dan dat, anders wordt de buik spikkelig.
- Franje met een bevroren omtrek: schuine tongen in b met d-gaten op de onderste rij. Drie tongen is genoeg; meer wordt ruis.
- Bij randpixels naast transparant kan een nagel of tong nooit in een vul-/schaduwtint eindigen (open rand). Controleer elk keurdersadvies dus eerst tegen de controle op open randen.
