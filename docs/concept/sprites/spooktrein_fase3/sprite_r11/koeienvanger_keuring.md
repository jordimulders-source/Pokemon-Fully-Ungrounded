# Keuring + voorstel koeienvanger (verse keurder, 16 nov)

Zone x0–25, y42–61. Vel: `koeienvanger_vel.png` (16×: voorstel | r11 | model; hele sprite 2×: voorstel | model | r11; 1×). Voorstel: `voorstel.png` (+ `voorstel_8x.png`, `voorstel_16x.png`), gemaakt met `koeienvanger_voorstel.py` (128 px anders dan r11, groen 0 px, alles binnen de zone; asserts in het script).

## 1. Het model (natief.png 99×99, nx 9–41 / ny 64–83; sprite ≈ (nx−9)·0,744, (ny−73)·0,744+52,5)
- Onder de roestband met de zigzag van de grijns hangen **drie grote platen + een lichte rand**, geen rij gelijke spijlen:
  1. **links een lichte wig**: bleke (roze-grijze) voorrand van 2–3 natieve px, donkerroest als buitenrand, met roeststrepen en één donkere spleet ertussen; loopt door tot de punt;
  2. **grote grijze plaat** die schuin naar **de punt linksonder** loopt (laagste punt van het hele ding, ny 83 = sprite y59, x4–7), lichte linkerrand, zwarte spleet rechts;
  3. **smalle middentand** tussen twee groene kieren: lichte linkerkant, roest onderaan, punt omlaag;
  4. **brede rechterplaat**: grijs met roestvlekken en één zwarte groef, onderrand bijna vlak (stijgt 1 px naar rechts), donkere rechterrand.
- **Bovenkanten zijn schuin**: de band hangt in V's tussen de platen; elke plaat heeft een lichte schuine bovenrand.
- **Spleten waaieren naar de punt**: links leunen ze naar rechts (omlaag), rechts naar links. Licht linksboven; roest vooral in de linkerwig, onder in de middentand en midden op de rechterplaat.

## 2. Oordeel vorige rondes
- **r9**: drie afgeronde blokken met kussenschaduw = vaten/pillen, geen kaak; helling en punt ontbreken. Niet het model.
- **r10**: rustig, maar rechte kistjes met verticale latjes; geen schuine bovenkanten, geen V, rechterplaat een vlak doosje. Leest op 1× als een krat.
- **r11**: tonen kloppen het best met het model, maar het is per pixel overgenomen ruis: losse zwarte stippen, roestspikkels van 1 px, geen grote vormen. Leest op 1× als puin, niet als drie platen. Onrustig voor Gen 3.
- Hoofdvraag "leest het op 1× als dezelfde schuine puntige kaak?": r9 nee, r10 half (punt links wel, schuin niet), r11 half (silhouet goed, binnenkant onleesbaar).

## 3. Voorstel (wat het script tekent)
- Silhouet van r11 blijft (dat klopt met het model); alleen de binnenkant in rijen 47–58, x0–23.
- Lichte wig x2–3 (index 7) met donkerroest-selout (9) aan de lichtkant links, groef (12), roestblad x5–6 (8/9).
- Linkerplaat x6–10, schuine lichte bovenrand (7) van (6,47) naar (10,49), vlak 11, schaduwkolom 12, zwarte spleet x11; versmalt naar de punt x4–7 onderaan (lichte rand blijft links).
- Middentand x12–15 → x12–13: lichte kolom, roest onderaan (8/9), zwarte spleet die naar links leunt (x16→x15→x14).
- Rechterplaat x16–22: schuine lichte bovenrand (rij 49 x17–18, rij 48 x19–20), vlak 11, roestvlek 2×3 (x17–18, y51–53), groef 12 die naar links leunt (x20→x19), schaduwkolom x22, zwarte onderrand y55.
- Zwart alleen in spleten en aan de schaduwkant (onder/rechts); tinten 7/11/12 + 1, roest 8/9; geen clusters < 3 px buiten de smalle tand.

## Open / niet gedaan
- Rechterplaat volgens het model 1 px lager (y56) kan niet zonder het bevroren groen op y56 x15–18 te raken; onderrand blijft vlak op y55.
- Groef en roest in de rechterplaat zijn bewust vereenvoudigd ("wat simpeler", Jordi); het model heeft daar meer kleine vlekken.
