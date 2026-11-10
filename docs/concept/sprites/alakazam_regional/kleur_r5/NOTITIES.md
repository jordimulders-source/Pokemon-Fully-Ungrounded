# Charlatan-Alakazam: kleur r5 (verse maker, snor grijs)

Vanaf nul op de onderlaag (niet vanaf r4). Stap: `python3 meet5.py` (meting per spritepixel, `meet5.npz`), `python3 onderlaag.py` (model → `onderlaag.txt`), basis = onderlaag met zwart `k`→`m` vanaf rij 29 (`basis0.txt`), dan `python3 apply.py basis0.txt raster.txt kop lijf hand schoon` en `python3 vel.py`. Controle: `controle.py`, `lijnkaart.py`, `box1x.py`, `q.py` (model per spritepixel in 4 kwadranten, 128-raster) en `zij.py` (sprite | model op 12–22×). Geometrie: `../silhouet/geo.py` (ongewijzigd).

Jordi: snor **grijs zoals het model** ("nee houd hem grijs"); één versie.

## Gedaan
1. **Onderlaag:** per spritepixel `fo` = fractie modelpixels met L<20 (omlijning, drempel 0,3) en de mediaan van de overige pixels; materiaal en tint per helderheid. Silhouetrand altijd omlijning. Het model is een 128-raster (lijnen zijn een halve spritepixel); waar een lijn tussen twee pixels valt is gekozen met `q.py` (kwadranten).
2. **Kop (kop.py), per rij gemeten met q.py:**
   - Linkeroor: buitenlijn onder/links zwart (o), bovenrand selout d (model: donkergrijs), lichte band a langs de bovenrand zoals het model (rij 3 x19–20 → rij 6 x24–26), daaronder b, onderste band c.
   - Rechteroor: linkerrand d (model 'DD'), binnen c/b, rechterrand d tot rij 13, vanaf rij 14 zwart (model: zwart vanaf (41,14)).
   - Wenkbrauwrichel d: (31,14), (32–34,13), (35,14), (36,15) (model 'DD' op exact die plekken).
   - Open oog: lid (32,15), (33,15), (34,16), (35,16) o; wit (33,16), (32–33,17), (35,17), (33–34,18) (model wit rij 16b–18a, x32,5–36); pupil (34,16–17) (model '#' op (34,16a) en (34,17a)); hoek (36,17) o.
   - Halfdicht oog: (40,17), (41,17) o (lid), (40,18) w (model wit op (40,17b–18a)), (41,18) o.
   - Snor (grijs, gevulde streng met omlijning): linkerkrul als spiraal: buitenlijn (30–31,18), (29,19), (28,20–21), (29,22), (29–30,23); binnenlijn (31,19), (30,20–21), (31,22); vulling b (30,19), (29,20), (29,21), (30,22), (31–33,23). Band: bovenlijn (31–34,22) → (35–37,21) d, vulling (35–37,22) b, onderlijn (30–36,24) en (34–37,23); onder de snuit vulling c (38–41,25) tussen (38–41,24) en (38–42,26) (model: 'CC CC DD BC' tussen twee lijnen). Rechts de streng (43–44,22) c + (45,22) d tussen (42–44,21) en (43–45,23); rechterkrul: buitenlijn (45–46,17), (47,18), (48,19–20), (47,21), binnenhaak (44,18–19), (46,18–19), vulling (47,19–20) b en (46,20–21) d (randpixel, dus selout).
   - Kin: (37–40,27) c tussen (38–42,26) en (36–40,28).
3. **Strikje:** x29–35, rij 25–28: t linksboven per lus, r midden, s naar rechtsonder en in het midden (32,25–27) als knik (geen knoop); onderaan (32,28) wit zoals het model ('AA').
4. **Linkerplaat:** zwart materiaal n met glans p (16–18,19–20), m in de onderste rijen; eigen omlijning: rechts op x24 (rij 22–26; model '#' op x23,5–24), onder (14–17,26), (18–20,27), (19–23,28). Bovenarm eronder n/m met zwarte omlijning, (17,29) k.
5. **Rechterplaat:** (37–38,29), (38,30–31) n, (39,30–32) m, (40,33) m, omlijnd (36,29–30), (37,30–31), (38,32), (40,30–32), (39–41,33).
6. **Romp en wit front:** zwart m met k-schaduw onder de kop (24–28,22), langs de arm (19–20,29–32) en (22,34–37); lijn arm/romp x21 rij 33–38. Wit front volgt het model: links x27 (rij 26–28), x26 (29–36), x25 a (37–43); rechts x34 (29–31) → x33 → x32 (34–39) → x31 (40) → x30 (41–42) → x28 (43); a als schaduw rechtsonder (31,39–40), (30,40–41), (32,33–35) en onder het strikje (29–31,29).
7. **Handen:** links drie vingers als stroken b op x11, x13, x15 (rij 39–43) met binnenlijnen d op x12 (39–41) en x14 (39–43), buitenlijn x10 tegen de kaart; pols c (16–19,40–43). Rechts de duim x50–51 (rij 28–31) langs de kaart en drie horizontale vingers b: (52–54,31), (52–55,33), (51–52,35), gescheiden door d-lijnen (52–55,32) en (52–54,34); onderarm c/b/c op x49–51.
8. **Kaarten:** wit, selout d op de belichte randen (links/boven), o rechts/onder; schoppen o: rechts (55,24), (54–56,25–26), (55,27); links (8,38), (7–9,39).
9. **Benen:** dijen grijs (links b/c, rechts c/d want verre been), knieën zwart met n-glans linksboven en k rechtsonder, eigen omlijning (rij 45/51 links, 46/48 rechts); schenen a-randlicht links, b, c rechts. Voeten: links twee tenen met klauw a (16,61–62) en (25,61–62), inkeping (18–21,60); rechts tenen met scheidingslijn (40,57) d en klauwen (42,57), (41,58), bovenrand selout d (38–42,55).
10. **Palet** (13 kleuren + transparant): o (16,14,22); zwart k m n p; grijs/wit w a b c d (c en d violet getint: alleen de schaduwen violet, SPEC); rood t r s.

## Afwijking van de onderlaag per zone (pixels anders dan `basis0.txt`)
| zone | px | anders | waarvan lijn↔vlak | waarom |
|---|---|---|---|---|
| oren + schedel (y0–15) | 208 | 58 | 33 | selout d op de randen i.p.v. o of licht, a/b/c-banden als nette trappen, wenkbrauwrichel en ooglid gezet |
| gezicht + snor | 238 | 80 | 26 | oog, snorspiraal en strengen op de halve-pixellijnen van het model (q.py), ruis in de snuit weg |
| linkerplaat + bovenarm | 203 | 101 | 9 | vooral hertinting (onderlaag gaf grijs, SPEC zwart) en plaatrand naar x24 |
| romp + wit + strik | 229 | 56 | 11 | strikje opnieuw getint, witgrens en schaduw a, rompschaduw |
| rechterplaat + arm | 87 | 36 | 4 | plaat als eigen omlijnd stuk (SPEC), armschaduw |
| rechterhand + kaart | 109 | 54 | 27 | duim en drie vingers als stroken (Jordi: "pixel blurs"), kaartrand selout |
| linkerhand + kaart | 131 | 62 | 27 | idem; drie verticale vingers |
| benen + voeten | 242 | 103 | 21 | knieën/schenen/voeten opnieuw belijnd en getint (Jordi: "slordig lijnen werk") |

## Controle
- Alpha-diff met `../silhouet/silhouet.png`: 0 erbij, 0 eraf.
- Open randen 0, losse o 0 (8-buren).
- Clusters < 3 px (8-buren): 6, alle in dunne delen: vulling rechterkrul (47,19–20), snorstreng (43–44,22), teenlijn (40,57), klauwen (42,57)/(41,58) en (25,61–62), selout (24,59).
- Lijnkaart (`lijnkaart_r5.png`, drempel 0,3): 45 rood, 91 blauw. Blauw is vrijwel overal de verplichte buitenlijn op de silhouetrand (model heeft daar een halve pixel lijn) en de schoppen/vingerlijnen die het model als 'k' (20–60) i.p.v. <20 tekent. Rood zit op halve-pixellijnen (plaatonderkant rij 26/27, kopsom rij 20/21) en in de linkerhand (zie zwakke punten).
- 1× naast het BOX-verkleinde model: `box1x_r5.png`; leest als het model (kop, snorkrullen, strik, kaarten, knieën).

## Zwakke punten
- **Linkerhand:** het model is daar een vlek van diagonale lijnen; ik heb drie verticale vingers getekend (Jordi wilde duidelijke vingers). Daardoor 12 rode lijnpixels: de vingerlijnen staan op x12/x14 i.p.v. diagonaal (12,39)→(14,42).
- **Rechterplaat:** in het model een donkergrijs stuk zonder duidelijke plaatvorm; als plaat gelezen volgens SPEC, klein en diagonaal.
- **Oog:** wit (33–34,18) loopt een halve pixel lager dan het model om het oog groot genoeg te laten lezen.
- **Bovenarmen** zijn zwart (SPEC), in het model grijs; links leest de bovenarm daardoor minder los van de plaat.
- **Licht:** schenen en dijen links licht (Gen 3), het model heeft daar de lichte kant rechts.
