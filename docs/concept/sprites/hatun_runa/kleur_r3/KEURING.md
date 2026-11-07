# Hatun runa r3 – onafhankelijke keuring (7 nov)

Verse keurder, eerst blind geoordeeld (NOTITIES.md pas daarna gelezen). Getoetst: alleen (1) trouw aan `referenties/model_gekozen.png` en (2) Gen 3-techniek (SPRITE_KERN). Vel: `keuring_vel.png` (sprite | verkleind model op 8×, kop op 16× naast de modelbron, 1× en 2×).
Meetmethode: modelblok per spritepixel volgens `silhouet/sil.py` (schaal 16,875, top 19, left 8, bbox x108/y104), mediaan of gemiddelde helderheid per blok; dichtstbijzijnde paletindex. Kleurindexen hieronder = de tekens in `raster.txt` (1 = omlijning, 2–5 = bruin donker→licht, 6–8 = goud donker→licht, 9 = wit, A = crème, B/C = grijs, D = rood, E = grijsbruin, F = masker).

## Hoofdvraag
Op 1× en 2× leest hij als de vogel uit het model: zelfde pose, silhouet identiek (alpha-diff 0, 971 px), kleurvlakken op dezelfde plekken (kruin met goudvlek, witte streep, masker, open bek, witte keel, gele buik, drie bruine vleugel-/staartvormen). **Het oog leest op 1× als een donkere stip in het wit/zwart, niet duidelijk als Pokémon-oog**: de glans die het model heeft ontbreekt.

## Eindoordeel: **NIET GOED** (dichtbij; 3 benoemde reparaties nodig, 2 optioneel)

## Per onderdeel
| Onderdeel | Oordeel | Reden |
|---|---|---|
| Kruin + gouden vlekje | PASS | Zwart y43–45 en goud (17–18,44) op de gemeten modelplek (model goud x17,0–19,3, y44). |
| Witte wenkbrauwstreep | PASS (kleine afwijking) | Vorm en plek kloppen; achterkant 1 px te lang: model (25,45) = (70,58,48) en (25,46) = (50,48,47) donker, sprite crème A. Zie reparatie 4. |
| Zwart masker | PASS | Snavelbasis → onder oog → achter oog tot de nek, zoals model. |
| **Oog** | **FAIL** | Pupil (18–19,47–48), witte sikkel (20,47–48), grijsbruin eronder (18–19,49): plek en opbouw kloppen. Maar het model heeft een duidelijke witte glans in de pupil (gemeten: witte pixels > 235 op x17,8–18,9, y47,4–48,2; centroïde (18,6, 48,0)) en SPEC zegt "oog met lichte iris/glans zoals in het model". Zonder glans is het op 1× een zwarte stip die half in het masker opgaat. De glans versmelt niet met wit: (18,48) raakt geen witte pixel (wit staat op (20,47–48) en diagonaal (17,47)). |
| Snavel + open bek | PASS | Bovensnavelpunt (9,50), onderkaakpunt (13,55), rood (15–16,51), (15,52) en bruinrood (14,51), (14,53) gemeten gelijk aan model. Optioneel: zie reparatie 5. |
| Witte keel | PASS | Wit x18–24, y50–53, grens naar geel als model. |
| **Nabije vleugel** | **FAIL (techniek + 1 px verschoven)** | Lijf van de vleugel, voorrand, slagpennen en gemiddelde toon kloppen (model 110 / sprite 107). Maar op de goud/bruin-grens x34–35, y35–38 staat een **dambord** (6/4 om en om, 4 rijen: (34,36), (35,35), (34,38), (35,37) bruin tussen goud). Het model heeft daar twee korte schuine streepjes met twee gouden rijen ertussen: (35,34)+(34,35) en (35,38)+(34,39). |
| **Verre vleugel (boven, veren)** | **FAIL (toon)** | Eén toon te licht: modelmediaan 78 (≈ index 3), sprite 104 (index 4) in x8–24, y29–36. Het model heeft basis 3 met lichte randjes 4/5 en donkere scheidingen 1; de sprite heeft basis 4 met veel 5. De verre vleugel staat achter en hoort donkerder te zijn dan de nabije (die klopt wel). Onderste deel (y37–43) klopt (model 69 / sprite 66). |
| Lijf / gele buik | PASS | Toon (185/192) en verdeling licht linksboven → schaduw rechtsonder als model. |
| Staart | PASS | Vorm, tonen (90/88) en donkere basis kloppen. Textuur iets drukker dan het model (buurverschil 28 vs 19), niet storend op 1×. |
| Pootjes | PASS | Twee pootjes x30–33 en x36–40, y57–61, zoals model, omlijnd. |

### Gen 3-techniek
| Eis | Oordeel | Opmerking |
|---|---|---|
| ≤ 3 tinten per groep + omlijning | PASS (grensgeval) | Bruin heeft 4 tinten (2–5), maar 2 is de donkerbruine rug/verre-vleugelbasis die het model als eigen materiaal heeft en tegelijk binnen-/selout-lijn; goud 3, wit 2, grijs 2. |
| Geen tintvlakjes < 3 px | FAIL (alleen het dambord) | De overige 1–2 px clusters zijn 1 px veerlijnen (lijnen, geen vlakjes) en het goudvlekje. |
| Geen banding / pillow shading | PASS | |
| Licht linksboven | PASS | |
| 1 px buitenlijn, selout | PASS | Gekleurde selout (3) op de lichte voorrand van de nabije vleugel; zwart aan de schaduwkant. Bovenrand verre vleugel wisselt 3/1, maar dat volgt de veerpunten (zwart in de inkepingen), geen om-en-om-rand. |
| Open randen / losse pixels | PASS | |
| Oog als Pokémon-oog | FAIL | Zie oog. Vergeleken met Taillow/Swellow (`anim_front_gba.png`): hun oog leest door hoog contrast pupil/licht; hier staat de pupil (32,22,22) tegen het masker (50,50,56), dus alleen een glans maakt het een oog. |

## Top-5 reparaties (prioriteit)
1. **Oog: glans.** (18,48): 1 → **9** (wit). De rest van het oog blijft (pupil (18,47), (19,47), (19,48) = 1; sikkel (20,47–48) = 9; (18–19,49) = E).
2. **Nabije vleugel: dambord weg, streepjes op de modelplek.** (34,36): 4 → 6; (34,38): 4 → 6; (35,35): 4 → 6; (35,37): 4 → 6; dan (35,34): 6 → **3** (model 107,68,42); (34,35): 6 → **4** (model 172,120,54); (35,38): 6 → **3** (model 123,76,45); (34,39): 6 → **4** (model 148,90,45). (36,38) = 4 en (35,36) = 6 blijven. Resultaat: x34 goud y33–34 en y36–38, x35 goud y35–37, twee schuine streepjes met twee gouden rijen ertussen.
3. **Verre vleugel één toon donkerder (x9–24, y30–36).** Basis 4 → 3, licht 5 → 4 behalve de smalle lichte veerranden bovenaan, scheidingen blijven 1/2. Gemeten doel (dichtstbijzijnde paletindex per pixel, links sprite nu, rechts model):
   ```
   x:    890123456789012345      890123456789012345
   y30  33135531..........      35514331..........
   y31  15425444131.......      34543532315.......
   y32  .11425442541.1....      .44533333354.3....
   y33  ...14254425421....      ...44343131423....
   y34  ...144254424421...      ...543333333313...
   y35  ....134234423421..      ....243131324232..
   y36  .....14322222221.1      .....24222223233.5
   ```
   Niet pixel voor pixel overnemen (dan wordt het ruis); doel is de gemiddelde toon ≈ 3 met lichte randjes op de veerbovenkanten, zoals de rechterkolom laat zien. Geen nieuwe 1 px-vlekjes.
4. **Achterkant witte streep.** (25,45): A → **2**; (25,46): A → **F** (model donker, stuk 50–70). Daarmee eindigt de streep op x24 zoals in het model en is hij aan de achterkant omlijnd.
5. **(Optioneel) bovensnavel.** Model: bovensnavel grijs op y48–49 met donkere onderlijn op y50; sprite schuift een halve pixel lager. (14,48), (15,48): 1 → **B**; (13,50), (14,50), (15,50): B → **1**. Alleen doen als het op 1× de open bek niet verzwakt.

## Ter info voor Jordi
- Gemeten in het model: een donker hapje in de onderrand van de witte streep op (21,46) (mediaan 65,61,58) en (22,46) half. Ronde 3 heeft "de bobbel in de wenkbrauw" op aanwijzing van Claude bewust weggehaald; ik zet het niet in de reparaties, maar het model heeft hem wel (1 px).
- Kop is vrij klein en de staart opgezet: dat is het model, geen fout.
- Bruin met 4 tinten (rug donkerbruin als apart materiaal) is een grensgeval van de 3-tintenregel; samenvoegen zou de rug/verre-vleugelbasis van het model laten verdwijnen.
- Makersnotitie zegt "geen losse glanspixel (Taillow-opbouw)": het model heeft hem wel, en SPEC vraagt hem. Daarom FAIL op het oog.
