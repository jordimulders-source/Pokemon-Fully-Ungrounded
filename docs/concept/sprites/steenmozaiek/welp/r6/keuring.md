# Keuring welp r6 (onafhankelijke keurder, 15 nov)

**Oordeel: FAIL** (dichtbij; vorm en pose kloppen, maar kleur, neus, tong, oog en korrels zijn nog niet op het niveau dat Jordi wil zien).

Werkwijze: blind beoordeeld vóór het lezen van iets anders in de map (er waren geen eerdere rapporten). Vergelijkingen: sprite 8× naast het model, uitgelijnd op de bbox (model x 97–942 / y 194–942 → sprite x 7–57 / y 18–63); gezicht op 20×; 1× (3×) naast Growlithe, Vulpix, Skitty en de afgemaakte `af/steenjaguar.png`. Kleurmeting: per sprite-tint de gemiddelde modelkleur op dezelfde pixels.

## Hoofdvraag
Pose, massa en silhouet zijn trouw (voeten, staart, opgeheven poot en kop liggen op de modelplek, x/y-meting klopt binnen ±1 px). De facetten (gehakte steen) zijn er en het 3D-idee is niet weg. Maar naast het model is hij duidelijk **te licht en te perzikkleurig**: het model is koel chocoladebruin, de sprite is zalm/zandbruin, en naast de volwassen vorm valt hij flets weg. Het gezicht is minder mooi dan het model (holle neus, platte tong, oog zonder onderrand). Met ±30 losse korrels leest hij op 8× rommelig. Zo zou ik hem Jordi nog niet sturen.

## Eis 1: trouw aan het model (per onderdeel)
| Onderdeel | Oordeel |
|---|---|
| Oren | OK (ver oor x11–16, nabij oor x25–31 met lichte rand en donkere binnenkant, zoals het model) |
| Voorhoofdsband | OK in vorm en plek (haarspeldgolf, lila 3 tinten). MAG: het rechtereinde stopt bij x21; in het model loopt de bocht nog ±2 px verder richting het nabije oor |
| Oog (nabij) | AFWIJKING: in het model rond en rondom omlijnd; in de sprite geen onderrand (zie MOET 3) |
| Ver oog | toegestaan (deels weg); de W op (11,27) mag blijven |
| Snuit | OK in vorm |
| Neus | AFWIJKING: in het model een volle donkere neus op de snuitpunt, in de sprite een hol doosje (MOET 2) |
| Mond | OK (open, donker binnen, lip x10–17 y35). MAG: lijn y35 is 8 px kaarsrecht, in het model licht gebogen |
| Tanden | OK (W op (12,36), (15,36) boven, (16,38) onder) |
| Tong | AFWIJKING: in het model twee rozen met middengroef en ronde punt naar de poot, in de sprite een egaal blok (MOET 4) |
| Opgeheven poot | Vorm en tenen OK (3 tenen, lijnen x9/x11); kleur te licht (MOET 1) |
| Borst / nekplooi | OK (donkere lijn kin→schouder zoals het model) |
| Romp / facetten | Facetverdeling OK; toon te licht/warm (MOET 1); korrels langs de rug (MOET 5) |
| Dij | OK in vorm en plek |
| Voeten | OK in plek (voorvoet x22–35, achtervoet x37–48, gemeten tegen het model); bovenkanten te licht (MOET 1) |
| Staart met ring | OK in vorm; ring (C/Q op x52–53, y53–55) aanwezig; staart te licht |
| Spiraalplekken | Plekken kloppen (schouder, dij, rugband); ontwerp later. Netheid: zie MOET 6 |

## Eis 2: Gen 3-techniek
- Tinten: bruin d/S/M/L/H (4 + lijn, toegestaan), lila P/Q/R (3), crème C (1), tong T (1), oog W/g/G. Aantallen OK.
- Contrast: stappen 86→125→166→203 (±40), op zich Gen 3-achtig, maar de hele ladder staat ±20–40 te hoog en te verzadigd t.o.v. het model.
- Buitenlijn: dicht, op 2 open randen na (tong). Op de lichte linkerkant van de kop wisselen d en K elkaar af ((10,25)d,(10,27)K,(10,29)d,(9,31)d,(8,32)K,(9,33)d,(9,34)K): MAG.
- Korrels: ±30 losse vulpixels (1–2 px) buiten lijnen en spiralen, zie MOET 5.
- Geen pillow shading, geen echte banding behalve het M/S-streepje langs de rug.

## MOET-reparaties
1. **Bruine ladder naar de modelkleur (alleen palet, silhouet diff 0).** Meting op dezelfde pixels: waar de sprite M (166,110,93) heeft is het model gemiddeld (134,94,86); waar de sprite L (206,152,129) heeft is het model (155,111,100); S-zones model (103,68,64). Het model is dus donkerder en koeler (rood−blauw ±48 i.p.v. 73). Verschuif S/M/L/H naar die tint, met Gen 3-stappen van ±30–35, bv. S ≈ (98,64,60), M ≈ (136,96,88), L ≈ (170,128,114), H ≈ (204,166,148) als hooglicht. d en K blijven. Vooral L (155 px: voorhoofd x16–27 y21–25, snuit x11–17 y29–31, poot x8–15 y41–45, voeten y57–60, staart x53–55 y50–53) mag niet meer als perzik oplichten.
2. **Neus (x8–13, y31–34):** nu een hol doosje (K-rij (10–13,31), (8,32)K, SSS op (9–11,32), K op (12,32), (11,33), (9,34), (11,34)). Maak het zoals het model: een volle donkere neus op de snuitpunt, (8–12,31–32) gevuld met K/d (eventueel 1 px glans), en haal de losse K-pixels (11,33), (9,34), (11,34) weg (M/S van de snuit, buitenrand blijft omlijnd).
3. **Oog (x16–20, y26–29):** onderrand ontbreekt; de crème rij (17–19,29) loopt direct over in de wang ((16,29)M, (17–19,30) L). Sluit het oog rondom zoals het model (donkere onderrand op y30 onder x17–19, of de CCC-rij wordt rand), zodat het een rond oog is en geen spleet met een lichte vlek eronder. Pupil (18,27–28) en glans (17,27) houden.
4. **Tong (x11–14, y36–40):** één egale tint, en twee lichte pixels op de buitenrand zonder lijn: (12,37) en (11,39). Geef hem zoals het model een tweede, donkerdere roze (rechterkant/onderrand + middengroef op x13) en een gesloten rand (selout in donkerroze op (12,37) en (11,39)), ronde punt op y40 richting de poot.
5. **Korrels weg** (1–2 px vulpixels die geen lijn of spiraal zijn):
   - rug, tussen lila band en buitenlijn: (35,33)M, (36,34)S, (37,35)M, (38,36)S wisselen elkaar af: één tint (S), of laat de lila tot de lijn lopen zoals op y37–39;
   - kop: (15,26)M, (16,29)M, (11,29)L, (13,30)L, (14,30–31)M, (10,33–34)M;
   - lijf: (18,38)S, (28,38)M, (32–33,38)M, (34,39)M, (35,40–41)S, (35,43)L;
   - achterkant/staartaanzet: (47,46)S, (46,47)S, (47,48)S en de prut op x45–51, y52–56 ((45,53)M, (46,53)P, (47,53)M, (46,54)M, (47,54)Q, (46,55)Q, (49,53–54)S, (48,55–56)S, (51,54)S): opschonen tot doorlopende vlakken naar het model (lila band van de dij, dan bruin, dan de staart).
6. **Spiralen netjes (alleen techniek, niet het ontwerp):** losse C/P-pixels (25,40)C, (30,41)P, (27,46)P, (28,47)P, (41,48)P, (40,49)P, (39,50)P, (44,51)C, (45,52)C laten de lijnen breken; maak elke spiraallijn een doorlopende 1 px-lijn zonder gaten of losse stippen.

## MAG-punten
- Voorhoofdsband rechts ±2 px verder doortrekken (x22–23, y21–22) zoals de bocht in het model.
- Lipijn (10–17,35) een lichte buiging geven.
- Iris in het model is grijsbeige, niet het crème van de spiralen; de iris uit g/G maken scheidt oog en patroon.
- Linkerrand van de kop: één lijntype (d op de lichte kant), niet d/K om en om.
- Teenpixels (23,61), (25–26,61), (29,61), (38,59–60), (43–44,60) consequent maken (elke teen ≥ 2 px).
