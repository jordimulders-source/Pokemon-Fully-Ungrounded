# Eindkeuring Sapa Inca (ronde 12, 6 nov)

Gekeurd: `ronde12/sapa_inca.png` (= ronde 10 + goudstaf; diff met ronde 10: 18 px, alleen staftinten). Onafhankelijke eindkeurder; niets aan de sprite gewijzigd. Eerst zelf geoordeeld (vellen, rasterdump, scripts), daarna pas `SPEC.md` en `KEURING.md` gelezen. Opdracht van Jordi: "kritisch kijken en vergelijken met dragonflycave en andere pokemon sprites": twijfel = FAIL. Coördinaten zijn (x,y) in de 64×64.

## Vellen (`eindkeuring/`)
- `zoom8x.png`: 8× op licht en donker. `sapa_4x_licht.png`, `sapa_4x_donker.png`: 4×.
- `vel_1x_licht.png`, `vel_1x_donker.png`, `vel_3x_licht.png`, `vel_3x_donker.png`: naast 16 echte sprites (Honchkrow, Noctowl, Staraptor, Braviary, Empoleon, Decidueye, Corviknight, Kilowattrel, Talonflame, Armarouge, Delphox, Kingambit, Pyroar, Hawlucha, Blaziken, Pidgeot; bovenste 64×64-frame).
- `uitsnede_gezicht_16x.png` (x16–39, y16–31), `uitsnede_vleugel_r_16x.png` (x32–57, y16–35), `uitsnede_buik_poten_16x.png` (x10–41, y32–62), `uitsnede_staf_16x.png` (x6–21, y16–49).
- `markeringen_10x.png`: de FAIL-plekken genummerd (1 gezicht, 2 kroononderrand/drup, 3 klont, 4 banding, 5 stafpunt, 6 jaggies, 7 vleugelpunt, 8 arcering, 9 flank, 10 romp zonder hooglicht).

## Metingen
| | Sapa Inca | Referenties |
|---|---|---|
| Oppervlak | 1629 px | Noctowl 1204, Staraptor 1446, Corviknight 1526, Blaziken 1579, Decidueye 1668, Kingambit 1674, Honchkrow 1715, Empoleon 1825, Delphox 1868, Talonflame 1898, Pidgeot 1996, Braviary 2012 |
| Box | 46×62 | Decidueye 45×64, Corviknight 47×60, Staraptor 48×58 |
| Soliditeit / symmetrie | 0,79 / 0,70 | Empoleon 0,69/0,58, Noctowl 0,69/0,57, Decidueye 0,81/0,74 |
| Zeer donker (luma < 60) | 0,283 (zwart alleen 0,116) | 0,15–0,58 (Talonflame 0,283, Honchkrow 0,266) |
| Kleuren | 15 + transparant | ≤ 16 |
| Randpixels naast transparant | alleen zwart (148), omlijningsbruin (62), kroonpaars (36) | |
| 2×2-klonten zwart | 1: (14–15, 46–47) | |
| Hooglichttint lijf (136,104,86) | 42 px, waarvan op de romp ±8 | |

## Oordeel per regel
| # | Regel (bron) | Oordeel | Reden en plek |
|---|---|---|---|
| 1 | Formaat, index 0 transparant, ≤ 16 kleuren (NORM) | PASS | 64×64, 16 slots incl. transparant. |
| 2 | Oppervlak en box fase 3 (CHECKLIST D1) | PASS | 1629 px, 46×62; gelijk aan Decidueye/Kingambit/Corviknight. |
| 3 | Soliditeit, symmetrie, negatieve ruimte (A4, A5) | PASS | 0,79 / 0,70; lucht tussen staf en lijf, onder de vleugel, tussen de poten (84 px ingesloten). |
| 4 | Aandeel zeer donker (E3) | PASS | 0,283, binnen de band van de referenties; donker lijf is soortkleur. |
| 5 | Dominant kenmerk breekt de omtrek (A2) | PASS | De waaier is het grootste vlak, zoals bij Pyroar/Kingambit/Noctowl. |
| 6 | Leest op 1× als (roof)vogel naast echte sprites (NORM 1, A1) | **FAIL** | Op 1× (`vel_1x_*`) leest het als een oranje waaier op een bruin ei met een stok. Elke referentievogel (Staraptor, Honchkrow, Noctowl, Braviary, Talonflame, Corviknight) toont kop + snavel als herkenbare vorm; hier verdwijnen ze tussen kroon en lijf (x21–33, y22–27). Zelfs Noctowl, met de snavel binnen de omtrek, heeft een groot gezicht met twee ogen. |
| 7 | 3/4 naar links-voor, kop meer naar de kijker (NORM 2, B1) | PASS | Snavel links van het kopmidden, verre waaierhelft korter, lijf schuiner dan de kop. |
| 8 | Pose met gewicht, geen T-pose (C7, §0.7) | PASS | Contrapposto, staf links, opgeheven vleugel rechts. |
| 9 | Alles geteld en verbonden (C1) | PASS | 2 vleugels, 2 poten, 2 ogen, snavel; één component. |
| 10 | Kopverhouding fase 3 (D2, NORM 6) | **FAIL** | Zichtbare kop onder de kroon ±13×6 px (rij 22–27) = ±10% van de hoogte (eis 20–30%). Bekend en door Jordi toegestaan om te vergroten ("ja, zolang de verhoudingen goed blijven"); ronde 11 mislukte en werd teruggedraaid. Oorzaak van 11 en 12. |
| 11 | Ogen geïntegreerd, Pokémon-stijl (NORM 7, SPRITING §6) | **FAIL** | Nabije oog (29–31,24): lid ok (rij 23), maar 1 rij hoog en de glans E staat op (31,24), aan de schaduw-/buitenkant. Verre oog = 1 px geel (24,24) naast zwart (23,24), geen lid. Op 1×: twee gouden puntjes. Ongewijzigd sinds KEURING punt 14. |
| 12 | Snavel/gezicht op 1× leesbaar (NORM 8, B7) | **FAIL** | Bleke haaksnavel (25–27,22–25 → punt 23,26) is op 1× een grijswitte druppel recht omlaag; geen donkere haak, leest als monocle onder een rode band. Ongewijzigd sinds KEURING punt 16. |
| 13 | Geen open randen (NORM 9, SPRITING §12) | PASS | Script: aan transparant grenzen alleen zwart, omlijningsbruin (52,38,36) en kroonpaars (116,90,172) als omlijningsbasis van de kroon. KEURING punt 11 is echt opgelost. |
| 14 | Selout: zwart aan de schaduwkant, omlijningsbasis aan de lichtkant (DFC "Outline shading", §8) | PASS | Kroon paars links/boven en zwart rechts/onder; lijf en staf links omlijningsbruin, rechts zwart. Bruin gebruikt zijn schaduwtint als omlijningsbasis (mag). |
| 15 | Geen anti-aliasing aan de buitenkant (DFC, §8) | PASS | Geen lichte pixels buiten de omlijning; leest op donker zonder puntjes (`vel_3x_donker`). |
| 16 | Omlijning 1 px, geen klonten (DFC, §8) | **FAIL** | 2×2 zwart onder de hand (14–15,46–47) met een rechte zwarte balk van 5 px (14–18,46). Onder de kroon een zwarte "drup" 2 rijen dik: (40–42,23) + (42,24). |
| 17 | Curven zonder jaggies/besluiteloosheid (DFC "Curves") | **FAIL** | Kroon rechtsboven: segmenten 3-1-2-1-1-2 (rij 2→7, rij-eind x37,38,40,41,42,44), zichtbare knobbels bij (38–40,3–4) en (43–44,6–7); linkerkant van de kroon loopt wel netjes af (3-2-2-1-1-1…). Kroononderrand zigzagt bij (43–46,22–23): zwart op rij 23, dan rij 22, los rood (45,22), weer rij 23. |
| 18 | Geen hoeken/rechte stukken waar het rond is (DFC "no corners in curves", NORM 5) | **FAIL** | Vleugelpunt: horizontaal 4 px (51–54,18) direct op verticaal 5 px (x54, y18–22) = hoek zonder neutraal segment. Rechterflank recht: x38 y37–41 (5 px) + x39 y42–45. (Jordi over de vleugelpunt: "merk je bijna niet"; technisch blijft het een hoek.) KEURING punt 22: linkerkant kop is opgelost. |
| 19 | Eén lichtbron linksboven (DFC "Shading", §5) | PASS | Kroonstralen licht links, staf licht links (B) en schaduw rechts (F), buik hooglicht linksboven, vleugel licht aan de bovenrand. KEURING punt 10 (staf middenbelicht, B-streep rechts in de buik) is opgelost. |
| 20 | Geen pillow shading (DFC) | PASS | Buik: hooglicht linksboven, schaduw rechtsonder; de A-rand links (x20, y40–50) is de interne omlijning van de goudgroep tegen het donkere lijf, geen kussenrand. |
| 21 | Geen banding (DFC "evenaar", geen evenwijdige randen) | **FAIL** | Rechterflank (x29–37, y36–50): buikschaduw AA, dan lijfbasis 33, dan schaduw 2222, dan zwart: vier banden van gelijke breedte evenwijdig aan de omtrek over 15 rijen. De 2 px lijfbasis (x31–32) heeft geen lichtlogica (rand van de schaduwkant). Opgeheven vleugel (x43–52, y19–30): 1-44-33-2-3-2-1 over 9 rijen evenwijdig; bedoeld als penscheiding, leest op 1× als gestreepte knots. |
| 22 | Genoeg hooglicht, volume (DFC Scyther-revamp: "R/S gebruikt veel hooglicht", §5) | **FAIL** | Hooglichtbruin op de romp alleen (21–24,28–34); de rechterhelft van de romp is vrijwel helemaal de schaduwtint = omlijningsbasis (lum 41). De romp oogt vlak en zwaar naast Staraptor, Noctowl, Honchkrow, die een duidelijke lichtzone op borst/schouder hebben. |
| 23 | 3 tinten per kleurgroep + omlijningstint, vaste verhouding (DFC, §4) | PASS | Kroon 5/6/7 + paars 8/9, goud A/B/C (+F roest), bruin 2/3/4 + zwart, snavel D/E. Goud gedeeld door buik, staf, poten en kroonvlekken: zuinig en samenhangend. |
| 24 | Geen ruis of losse pixels (NORM 8, KEURING 12/13) | **FAIL** | Hand (12–20, y41–45): diagonale 3/2-arcering (rij 43 `3233233`, rij 45 `3323323`), op 1× gevlekt. Zwarte pixel (17,19) in de kroon rechts van de stafpunt; vormt met (15,19) een "oogje" (zwart-oranje-zwart) in de kroon. Los rood (45,22). Borststippen uit de vorige keuring zijn weg. |
| 25 | Geen dithering waar het niet hoort (DFC "Textures") | PASS | Geen dithering. |
| 26 | Kroon leesbaar op 1× (A2) | PASS | Paarse rand, gouden boog en randvlekken lezen direct; het sterkste deel van de sprite. |
| 27 | Staf leest als staf met puntige kop (SPEC: "3 en puntig") | **FAIL** | Schacht en ruit (12–17,22–27) lezen, maar de punt (14–15,18–21) ligt in de kroon: goud B (luma 176) tegen kroonlicht 7 (luma 180), aan de linkerkant zonder omlijning ((13,18)–(13,21) = kroontint). Op 1× eindigt de staf bij de ruit; de gekozen punt is niet te zien. |
| 28 | Opgeheven vleugel leest als vleugel (Empoleon-flipper, bevroren) | PASS | Massieve flipper met pols; leest als gebiedend geheven vleugel. (Punt en strepen: zie 18 en 21.) |
| 29 | Buik (bevroren) | PASS | Rond, volume, licht linksboven. |
| 30 | Poten (bevroren) | PASS | Dun zoals Staraptor/Noctowl, nabije lager, verre voet in schaduw. |
| 31 | Kleurgebruik past bij type en soort | PASS | Fire in kroon en goud, Psychic in het paars; caracaragezicht. Balans: zie smaak. |

**Totaal: 20 PASS, 11 FAIL.**

## Controle van de FAIL-punten uit `KEURING.md`
| Vorige FAIL | Nu |
|---|---|
| 8 zwart aan de lichtkant (stafkop, lijf links) | Opgelost. |
| 10 B-streep rechts in de buik, staf middenbelicht | Opgelost; maar de nieuwe rechterflank heeft banding (21). |
| 11 open randen | Opgelost (script: 0). |
| 12 paarse kwastjespuntjes | Opgelost, maar op die plek zit nu een zwarte drup onder de kroon (16) en een zigzag in de onderrand (17). |
| 13 ruis in hand en borst | Borst opgelost; hand nog gearceerd (24). |
| 14 ogen | Niet opgelost. |
| 16 gezicht op 1× | Niet opgelost. |
| 21 kopverhouding | Niet opgelost (ronde 11 teruggedraaid). |
| 22 rechte stukken | Kop links opgelost; flank en vleugelpunt niet. |

## Eindoordeel: **nog niet af**
De kroon, de pose en de techniek van de omlijning (selout, geen open randen) zijn op het niveau van de referenties. Maar naast elke echte vogelsprite valt het gezicht weg (6, 10–12), en de shading van de romp (21, 22) en een handvol opschoonpunten (16, 17, 24, 27) halen de Dragonfly Cave-norm niet.

## Top 5 reparaties (op volgorde van impact; geen goedgekeurde vorm of keuze verandert)
1. **Ogen Pokémon-stijl binnen de huidige kopmaat.** Nabije oog: glans E van (31,24) naar de lichtkant (29,24), pupil zwart (30,24), iris C (31,24), en een tweede rij met gekleurde reflectie onder de pupil op (30,25) (nu rood 5). Verre oog: lid 2 op (24,23) (nu rood 5), zodat het geen los goudpuntje meer is. Snavel: donkere haakpunt op (23,26) (D → 2) en (24,26) 2 → D, lichte E alleen op de rug linksboven, zodat hij als haaksnavel naar linksonder leest. Gezichtsmaat en -idee blijven.
2. **Banding rechterflank weg (x31–32, y36–50).** De 2 px lijfbasis tussen buikschaduw en lijfschaduw vervangen door schaduw 2, of laten versmallen tot 1 px die naar onder uitloopt, zodat buik → lijfschaduw zonder evenwijdige strook overgaat. Omtrek en buikvorm blijven.
3. **Hooglicht op de romp.** Lijfhooglicht 4 uitbreiden van (21–24,28–34) naar een kleine schouderzone linksboven (±x21–27, y28–33, alleen tinten 3 → 4), zodat de romp volume krijgt zoals bij Staraptor/Noctowl. Geen palet- of omtrekwijziging (les ronde 11: niet het hele palet omgooien).
4. **Stafpunt zichtbaar maken.** Links van de punt omlijning in A of omlijningsbruin 2 op (13,18)–(13,21), de zwarte stray (17,19) terug naar kroontint 7, en de punt zelf C/A in plaats van B, zodat hij tegen de kroon afsteekt (nu luma 176 tegen 180).
5. **Opschonen: klont, drup, zigzag, arcering.** (15,46) en (15,47) zwart → omlijningsbruin 2 / roest F (geen 2×2 meer); drup (42,24) weg en (40–42,23) in één lijn met de rest van de kroononderrand; los rood (45,22) → zwart; in de hand (12–20, y43–45) de diagonale 2-streepjes terug tot één doorlopende scheiding per veer.

Kleiner, buiten de top 5: kroon rechtsboven 1 px gladstrijken (rij-eindes 37,39,41,42,43,44 in plaats van 37,38,40,41,42,44; raakt de bevroren kroonomtrek, dus alleen met toestemming van Jordi); vleugelpunt (54,18) 1 px afronden (Jordi vond dat niet nodig).

## Voor Jordi (smaak)
- **Kop/gezicht klein** (bevroren idee, maat open: Jordi zei "ja, zolang de verhoudingen goed blijven"). Reparatie 1 verbetert de leesbaarheid binnen de huidige maat; naast de referenties blijft dit het zwakste punt. Een kop van 1–2 px hoger (kroon iets omhoog) is de echte oplossing, maar dat is een silhouetkeuze.
- **Kroononderrand recht** (y22): trouw aan de echte paraplu-kuif, oogt op 1× als hoed. Jordi: "merk je amper".
- **Vleugelpunt plat** (Empoleon-flipper, bevroren). Jordi: "merk je bijna niet".
- **Staart-als-staf**: de staart-hint is bewust heel subtiel ("het feit dat de staf afkrult is al een hint"); wie het niet weet ziet een staf, geen staart.
- **Hand om de staf** leest als vuist; past bij een koning, minst vogelachtige plek.
- **Verre voet donker/zwart, nabije goud** (poten bevroren): klopt met "verre kant donkerder", leest op 1× als een zwart klompje.
- **Kleurbalans**: veel oranjerood boven, donker chocoladebruin lijf, paars alleen in de kroonrand: top-zwaar maar koninklijk.
- **Kroonpatroon v3** (bevroren): regelmatige 2×2-goudvlekken lezen als gestempeld patroon; past bij Inca-textiel.
- **Geen klauwen** (Jordi: "nee hoeft niet") en **geen lichte selout aan de lichtkant** (ronde 11 met nieuw palet afgekeurd).
