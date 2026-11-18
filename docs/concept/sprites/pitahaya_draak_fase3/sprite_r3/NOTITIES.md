# Pitahaya-draak fase 3, sprite r3 (verse maker): benoemde reparaties op r2

Basis = `../sprite_r2/pitahaya3_r2.png` (en `_zonder_tong.png`); `maak_r3.py` past per stap rij-teksten of een regel toe en schrijft
elke gewijzigde pixel met stapnaam naar `pitahaya3_r3_afwijkingen.txt` (zonder tong: `pitahaya3_r3_zonder_tong_afwijkingen.txt`).

```
python3 maak_r3.py ../sprite_r2/pitahaya3_r2.png pitahaya3_r3.png
python3 maak_r3.py ../sprite_r2/pitahaya3_r2_zonder_tong.png pitahaya3_r3_zonder_tong.png --zonder-tong
python3 ../sprite_r2/controle.py pitahaya3_r3.png ; python3 vel.py
```
Meetgereedschap nieuw (alle op het r2-raster, `box.py` = venster per spritepixel):
- `lumroze.py` / `lumgroen.py`: gem. helderheid roze/groen modelpixels + zwartfractie per spritepixel;
- `klas.py`: dominante modelklasse per pixel (zwart, wit, licht/midden/donkerroze, groen, geel; achtergrond via floodfill);
- `masker.py`: silhouet sprite tegen model; `klein.py`: model als 64×64-vlakgemiddelde naast sprites (1×-vergelijking);
- `volume.py` + `lijf.py`: volume-toonkaart van het lijf (zie 2); `tekstraster.py`: sprite <-> tekstraster.

## Maat, palet
- 61×50 px, 1799 px (zonder tong 1782); silhouet = r2 op 2 px na (stekelpunten (31,15) en (37,16) weg). 16 kleuren incl. transparant (zonder tong 13), palet ongewijzigd (teju).
- Zwart binnen 3,1 %, buitenrand 48 % zwart; dambord 0; losse pixels alleen tanden, pitjes, tongpunten, klauwpunten voorhand en 1 rib (43,56) uit r2.
- Afwijking per zone (zones overlappen deels): kop 51 px t.o.v. r2 (177 t.o.v. kale reductie); rug/stekels 82 (208); nabije hand 36 (34); rest lijf/staart 160 (556). Totaal 329 px t.o.v. r2.

## Per reparatie
1. **Kop** (51 px). Metingen `lumroze.py`/`klas.py`:
   - Kroonhooglicht van ±19 px lichtroze naar 6 px (alleen model ≥ 145: (9-10,17), (7-9,18), (7,19)), rest middenroze.
   - Snuitrug licht van de punt (2,25) tot (6,23) (model 126-149: het lichtste roze van de snuit). Getest in 4 varianten op 1×/2×/4× naast het verkleinde model (`klein.py`); deze las het best als uitstekende snuit.
   - Snuitbovenrand zwart: (3,22), (3,23), (2,24), (1,25) (model: dunne zwarte omlijning; (3,22) 30 % zwart). Kaaklijn (2-5,27)+(7,26-27)+(8-12,25) stond al zwart.
   - Vouw voorhoofd/snuit op rij 22: (4-6,22) middenschaduw r, (7,22) donkerroze (model 30 % donkerroze, 101), die bij de ooghoek (8,23) d uitkomt. Snuitonderkant (5-6,26) en (7,24-25) r (model 98-103).
   - Oog nu wit|pupil|wit als het teju-oog: wit (10,22) en (10,23), pupil (9,23) zwart (model: blauwgrijze pupil aan de voorkant van het oog), wenkbrauw (9,22)+(10-11,21) zwart, (11,22) donkerroze (model 70 % donkerroze). In r2 stond op de pupilplek wit.
   - Neusgat (5,25) donkerroze bleef (model 20 % zwart).
2. **Lijf** (239 px). Losse hooglichtvlekken vervangen door een toonkaart: `volume.py` berekent op het natieve model (groen masker, zwarte modellijnen en roze/achtergrond als rand) de afstand tot de rand → bolle hoogte → normaal → n·l met licht linksboven-voor, plus 0,5 × de gladde modelhelderheid (zodat bovenarm, dij en staartrug, die in het model lichter zijn, lichter blijven). Gekwantiseerd op 35/47/18 % (G/h/H), clusters < 3 px naar de buurmeerderheid. Alleen vulpixels van de grote lijfmassa; verre arm blijft schaduw (r2), lijnen/ribben (#, g), roze en bracteeën ongewijzigd. Resultaat: licht op de linksboven-kant van nek, bovenarm, dij en staartrug, sikkelschaduw rechtsonder en onder de rugrand.
   - Ribben: niet verplaatst. De r2-ribben (g) komen uit het skelet van de lange donkergroene modellijnen (`lijnen.py`, ≥ 25 px) en liggen op de modelribben (gecontroleerd op `grp2`-kaart: de lange donkergroene modellijnen zijn de ribben; massa-omtrekken heeft het model alleen als zwart).
3. **Rugstekels** (18 px): de 6 punten staan op de modelplekken (punten S1 (32,15.9) S2 (38.8,16.3) S3 (44.3,20.2) S4 (48.3,25) S5 (50.8,31.7) S6 (52.5,35), rasteruitsneden op 30×). In het model is elke stekel een doorn met lichtgroene bovenkant en zwart/donkere onderrand en punt; r2 had ze helemaal donkergroen, waardoor ze als donkere rand op het roze lazen. Nu: punt + onderrand g, bovenkant/kern h; elke punt 1 px scherp ((31,15) en (37,16) weg, model achtergrond). Hoogte boven het roze 2 px, zoals in het model (de modelstekels liggen schuin, ±30°, niet rechtop zoals bij de teju).
4. **Nabije hand** (36 px, x 28-36, y 43-48): model `lumgroen.py`: handrug licht (rij 43: 109-128), vingers op x 31 en x 34, klauwpunten op (31,48) en (34,48). Handrug nu als één vlak (licht linksboven), daaronder 2 klauwen die versmallen h H → H → H, met zwart ertussen; in plaats van r2's gestreepte rij 47.
5. **Tand onder de snuit** (3,28): **beide modellen hebben hem** (model.png én model_zonder_tong.png, uitsnede x 80-240, y 370-520 op 3×: grijze tand op model x 97-113, y 413-430 in beide). Dus in beide versies laten staan, volgens het eigen model (de r2-notitie "zonder tong 0 % wit" klopte niet: daar telde de grijze tand niet als wit).
   - Met tong: (9,29) vruchtvlees i.p.v. tong (model W9). Zonder tong: onderste hoektand (6,30) wit (model W7), zodat de hoektand 2 px hoog is zoals in het model.

## Twee versies
Met en zonder tong verschillen 28 px, alle binnen x 1-9, y 26-37; buiten de bekzone (x 0-12, y 26-38) diff 0 (gecontroleerd).

## Zwakke punten (eerlijk)
- **Kop op 1×/2×:** leest nu als kop met lichte snuit en open bek, maar de snuit oogt korter dan in het model: het modelsilhouet steekt maar ±2 px voorbij het voorhoofd uit (masker.py: silhouet gelijk aan het model) en de lengte komt in het model uit de dunne lijnen. Verder rekken zou het silhouet veranderen.
- **Bovenlip** (8-12,25) is een 5 px zwarte balk; het model heeft hier een dunne lijn op de rijgrens 25/26. Laten staan omdat hij vruchtvlees en snuit scheidt.
- **Lijf:** het lichte vlak op nek/schouder onder de rugrand (x 25-32, y 24-26) is groot; staartrug-hooglicht is een lange lichte rij (y 58, x 33-45) onder de donkergroene bovenrand.
- **Rugstekels** zijn 2-tonig maar klein (2 px boven het roze, model-hoogte).
- **Nabije hand:** 2 klauwen; het model toont 3-4 smalle vingers, die op 64 px niet los passen.
