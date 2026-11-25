# Gaucho-Lotad, frontsprite ronde 2 (maker, 25 nov)

Basis: r1 (zelfde methode en scripts; zie `../r1/NOTITIE.md`). Alleen de vier benoemde reparaties; niets hertekend.

## Bestanden
- `lotad_gaucho.png`: hoofdversie, figuur **43×41** (1148 px), **14 kleuren incl. transparant**.
- `lotad_gaucho_klein.png`: figuur **40×38** (982 px), 13 kleuren incl. transparant (snavel-midden valt weg bij het schrappen).
- `r1_r2_model.png`: r1 | r2 | model op 8×, dezelfde schaal.
- `vel.png`: zelfde indeling als r1 (r2 | klein | kaal | model op 8×; kop 12× naast model en Lotad; 1× op 4 achtergronden; naast Lotad op 8×).
- Nieuw script: `lijnkaart.py`. Gewijzigd: `tonen.py` (kraag), `bouw.py` (R2a/R3/R4), `gemeen.py` (oogtint), `kijk.py`/`vel.py` (elk png met zijn eigen palet).

## Reparaties
1. **Ogen** (Jordi: "houd er rekening mee dat het lotad oog lichtblauwe pixels heeft omdat het op een blauw lijf is gebouwd, dus die maak jij een tint van het bruin van het lichaam, zoals de originele lotad het doet"). In Lotad is het lichtblauw (148,180,222) zijn lichte lijfblauw (82,139,205), ±36 % naar wit geschoven (per kanaal 0,38/0,35/0,34). Dezelfde verhouding op ons lichte lijf, terra licht (213,137,101), geeft de **oogrand (228,180,156)**. Vorm, plek, wit en de zwarte stip zijn ongewijzigd: Lotad 1-op-1.
2. **Kraag.**
   - (b) **Cumulatief oppervlak**, zoals `r8/kleur_r1.py`: het percentiel van de modelhelderheid binnen de kraag wordt de r1-kraagkleur op hetzelfde oppervlaktepercentiel. r1-aandelen: donker 31,9 % (87,66,43 + 104,82,55 → 88,68,46), midden 18,3 %, licht 45,6 %, hooglicht 4,1 %. Gemeten op het model: 32,7 / 16,7 / 46,6 / 4,0 %.
   - (a) **Scheidingslijnen uit een lijnkaart van het model** (`lijnkaart.py`): een kraagpixel die ≥ 22 donkerder is dan de mediaan van zijn 5×5-kraagomgeving telt als lijn, alleen dunne strepen van ≥ 3 modelpixels. Elke lijnpixel gaat naar zijn eigen spritepixel als 1 px in de donkere kraagtint, alleen op kraagvlak en niet op de rand. Dat raakt maar **13 px**: de meeste modellijnen vielen al op een lijn- of donkere pixel. De zwarte tanden onderaan zijn de modellijnen uit de reductie.
3. **Onder de snavel (27 px):** in fase OY=1 vallen mondlijn (modelrijen 70–71), kop (72–73) en kinlijn (74–75) over elkaars 2×2-blokken. In de zone sprite-rij 34–37 / kolom 42–58 (reductiecoördinaten) komen de blokken nu uit fase OY=0. Dan is rij 35 = mondlijn, 36 = kop en 37 = kinlijn, elk 1 px. Elke pixel blijft een 2×2-modelblok.
4. **Hoedrand links (15 px):** in de zone (sprite x 10–24, y 29–34) is elke binnenlijnpixel vervangen door de gemeten modellijnen (natief zwart of hoed-lijntoon, u 76–104, v 36–47), elk naar zijn eigen spritepixel. Lijnpixels zonder modellijn krijgen de meest voorkomende hoedtoon van hun buren.
   - **Eén eigen ingreep:** de hoekpixel x15,y32 weg, waar lijn B (randlijn vanaf de linkerpunt) en lijn A (vanaf de kroon) samenkomen en B 2 px dik lag.
   - Resultaat: B is een doorlopende trap 2-2-10 (y31 x11–12, y32 x13–14, y33 x15–24); A loopt 4-4-1 van de kroon naar het knooppunt.
- **Donkere schaduwband onder de hoedrand:** blijft (model).

## Verschil met de kale reductie (hoofdversie)
- r2-reparaties: R3 27, R4 15, R2a 13 px.
- Opschoning zoals r1: buitenlijn 38, binnenlijnen 89 (alleen hertint), ontkorrelen 38, losse tintpixel 1, ogen 11.
- Pixels die niet uit het model of uit Lotad komen: de oograndtint (berekend, zie 1), terra-midden (188,113,78; berekend zoals in r1) en de ene weggehaalde hoekpixel in de hoedrand.

## Zwakke punten (eerlijk)
1. **Kraag leest nu als één bruine massa.** Met de oppervlaktekoppeling krijgt het donkerbruin een derde van de kraag. De hele schaduwkant rechts wordt dan één vlak (88,68,46). De middentint (17 % in het model) overleeft de 2×-reductie en het ontkorrelen nauwelijks (18 px). De lichte bladpunten vooraan zijn één vlak (161,132,92) met maar enkele donkere strepen. De punten lezen minder dan in het model, en eerlijk gezegd ook minder dan in r1. Het is minder geel, maar ook doffer. Mogelijke vervolgstap (voorstel, niet gedaan): de middentint als eigen band laten staan, met ontkorrelen uit voor de kraag.
2. **Lijnkaart (R2a)** zet maar 13 px. De diagonale streken op de voorste bladen uit het model zijn op 43 px grotendeels niet terug te zien.
3. **Hoedrand:** lijn A (kroon → links) en lijn B (rand) vormen samen een "<"-knooppunt, zoals in het model. Op 8× blijven het twee lijnen die elkaar raken, geen enkele boog.
4. Kleine variant: het schrappen haalt de snavel-middentint weg, dus de snavel is daar effen licht met een lijn.
5. Nog steeds geen keurder of DC-eindkeuring gedaan.
