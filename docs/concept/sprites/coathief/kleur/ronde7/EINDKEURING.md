# Coathief kleur ronde 7: verse eindkeuring

Keurder: verse agent (25 okt). Eerst zelf geoordeeld en pas daarna `ronde2/KEURING.md`, `ronde3/EVOLUTIEKEURING.md` en `ronde7/NOTITIES.md` gelezen. Bij twijfel geldt FAIL.

- **Vel:** `eindkeuring_vel.png`, gemaakt met `bron/eindkeuring_vel.py`. Het toont:
  - de sprite op 8×, 3× en 1×, op licht en op donker;
  - de olinguito;
  - 13 echte Gen 3-sprites: Linoone, Zigzagoon, Mightyena, Poochyena, Zangoose, Sandslash, Raticate, Furret, Persian, Houndoom, Absol, Sneasel en Ninetales, op 3× en op 1× (licht en donker);
  - onderaan een uitsnede op 8× waarin de FAIL-zones gemarkeerd zijn.
- **Indexnamen in dit rapport:**

  | Index | Kleur |
  |---|---|
  | 1 | zwart |
  | 2 | bijna-zwart |
  | 3 | maskerbasis |
  | 4 | maskerlicht |
  | 5 | maskerhooglicht |
  | 6 | bruin, schaduw/omlijningsbasis |
  | 7 | bruin, basis |
  | 8 | bruin, licht |
  | 9 | bruin, hooglicht |
  | A | crème, schaduw |
  | B | crème |
  | C | glans |
  | D | iris, donker |
  | E | iris, licht |
  | F | crème-selout |

## Scriptcontroles

| Controle | Uitkomst |
|---|---|
| Formaat | 64×64, mode P, `transparency` 0, palet van 16 kleuren. **PASS** |
| Kleuren | 15 kleuren plus de transparante index 0. Alle 16 indexen worden gebruikt. **PASS** |
| Alpha tegen `silhouet/ronde8.txt` | Diff 0, 1323 px, box 56×62 (x 4–59, y 1–62). **PASS** |
| Eilanden | 1 component, zowel bij 4- als bij 8-buren. **PASS** |
| Losse pixels | Geen zwevende pixels. Er zijn 127 enkelvoudige kleurpixels, vrijwel allemaal contourlijnen (snuitrug, schouder- en dijlijn, ringranden, klauwen); de vlakken zijn rustig. **PASS** |
| Zwarte klonten (2×2 in index 1) | Alleen in de neus (4–6, 44–47); die is bewust zwart. **PASS** |
| Donkerte | Index 1+2: 0,22 (Dark-type, donkere muts). **PASS** |
| Soliditeit | 0,60, lager door de rechtopstaande staart. Het silhouet is bevroren, zie "Voor Jordi". |
| **Open randen** (geen 1/2 naast transparant) | De selout 6 op de rug (y 29–35) en F op de staart en de oortoppen zit aan de lichtkant en is correct. De crème van de klauwen telt als dun deel van 1–2 px, dus als pseudo-omlijning (§8). **Fout:** 6 aan de onderkant (schaduwkant) op (32,47), (33,47), (43,51) en (44,51). **Twijfel:** glans C op de buitenrand van een klauw op (25,59) en (25,61). Zie eis 9. |

## Harde eisen (SPRITE_NORM)

| # | Eis | Oordeel | Reden |
|---|---|---|---|
| 1 | Leest op 1× als een echte Pokémon | PASS | Naast Linoone, Raticate, Mightyena en Houndoom leest hij direct als neusbeer: lange zwarte snuit, geringde staart rechtop met een haak, en een warm lijf. Hij is iets donkerder dan de R/S-gemiddelde (zie "Voor Jordi"). |
| 2 | 3/4 links-voor, kop meer gedraaid dan het lijf; lange snuit, één oog | PASS | Eén oog, neus vooraan, het verre oor is zichtbaar en het lijf staat op 42°. |
| 3 | 4 poten, eigen kolom, geen stokpoten, gewrichten, diagonale gang | PASS | Nabije voorpoot opgetild en verre voorpoot staand (de overlap is bewust, Jordi). Verre achterpoot hoger (onderkant y 57 tegen y 60), lucht op x 32–35 en x 43–44. Diagonaal: de nabije voorpoot en de verre achterpoot zwaaien samen. De staande onderpoot is 5 px en de enkel 4 px, wat aan de grens zit maar bij een pols klopt. Hakken aan beide achterpoten. |
| 4 | Geen Escher | PASS | De nabije poot ligt over de verre en de nabije dij over de verre achterpoot. |
| 5 | Lijf op skelet, curven, niets symmetrisch | PASS | Lijf en kop zijn rond geschaduwd. Er zit een kleine onrust in de rugcontour (segmenten 2-1-3-4-2-2-6, y 29–35), maar die komt uit het silhouet; zie "Voor Jordi". |
| 6 | Kopverhouding | PASS | Kop y 31–49 = 31% (fase 2: 30–35%). |
| 7 | Ogen geïntegreerd | PASS | Zwart bovenlid (18–20, 39), iris D boven en E onder, glans C linksboven op (18,40). Klein, zoals Jordi wil, en geen platte rode stip. De bovenste vlek raakt het lid en zweeft dus niet. |
| 8 | Kenmerken op 1× leesbaar | PASS | Staartringen, muts, vlekken, zwarte neus en de klauwen aan beide voorpoten zijn leesbaar. Over de vorm van de hangende klauwen: zie de valkuil "klauwen". |
| 9 | Omlijning, licht linksboven, geen open randen | **FAIL** | (a) Onderkant van de buik (32,47) en (33,47), tussen de nabije voor- en achterpoot: index 6 naast transparant, terwijl links (31,48) en rechts (34,48) zwart zijn. Daardoor zit er een gat in de zwarte boog aan de schaduwkant. (b) Onderkant van de nabije dij (43,51) en (44,51): hetzelfde, tussen (42,51)=1 en (45,52)=2. (c) Glans C op de buitenrand van de klauwen van de staande voet: (25,59) aan de bovenrand en (25,61) aan de onderrand, op de grond. Een bijna-witte pixel aan de schaduw- of grondkant is fout licht en geeft een puntje op een donkere achtergrond. |
| 10 | Geen Chernobyl | PASS | Gezicht compleet: neus, mond (k-lijn y 46) en kaak. Geen losse delen. De crème zit alleen in klauwen, vlekken, oren en ringen. |

## SPRITING §0

| # | Punt | Oordeel | Reden |
|---|---|---|---|
| 1 | Lijf en blik diagonaal | PASS | Zie eis 2. |
| 2 | Alles geteld en verbonden | PASS | 4 poten, 2 oren, 1 oog, staart en 2 klauwen per voorpoot. Alles hangt aan elkaar (1 component). |
| 3 | Geen rechte lijnen waar het dier rond is | PASS | De kaakonderkant (y 48–49, 8 en 9 px) en de rugcontour komen uit het bevroren silhouet; zie "Voor Jordi". |
| 4 | Ogen geïntegreerd, één oog bij een snuit | PASS | Zie eis 7. |
| 5 | Silhouet op 1× leest als de soort | PASS | Coati. |
| 6 | Formaat | PASS | 1323 px valt binnen fase 2 (1100–1550). De groei is ×1,13 tegen de olinguito; Jordi besloot dat dit mag (precedent Zigzagoon → Linoone). |
| 7 | Pose niet stijf | PASS | Loopt, één voorpoot opgetild, de staande poot buigt licht naar achter. |

## FAKEMON_CHECKLIST (kort)

- **PASS:** A1, A2 (staart), A3, A5, B1, B2, B4, B5, B6, B7, C1–C7, D2, D3 (n.v.t.) en E2.
- **A4 (soliditeit):** 0,60, onder 0,65. Dat komt door de lange staart. Er is genoeg lucht tussen de poten, dus het is geen leesbaarheidsprobleem. Silhouet bevroren: melding voor Jordi, geen FAIL.
- **D1:** het oppervlak klopt. De box (56×62) is groter dan de richtlijn ±47–53, door de staart.
- **D5:** ×1,13. Besluit van Jordi.
- **E1 (verre kant donkerder):** zwak maar aanwezig. De verre poten hebben hooglicht 4, de nabije 5.
- **E3:** 0,22.

## Valkuilen (WERKWIJZE stap 3)

| Valkuil | Oordeel | Reden |
|---|---|---|
| Kop als helm | PASS | De naad muts–hals kartelt bij y 39–41 en loopt daarna schuin (x 27 → 23). Alleen y 36–38 staat recht op x 28 (3 px), wat net onder de grens ligt. |
| Ruis | PASS | Rustige vlakken en contourlijnen. |
| Plat (2D) | PASS | Schouder- en heuplicht, buikschaduw, en een licht- en schaduwkant op de staartringen. De snuitrug heeft hooglicht 5. |
| Mini-oog op een donkere kop | PASS | Lid, glans en lichte iris tegenover de glans. De vlekken zijn groter dan het oog, maar de glans is het helderste punt. |
| Verre ledematen | PASS | Schaduwtint (zwak verschil) en een eigen kolom, hoger. |
| **Klauwen als gebogen haakjes, niet als rechte stokjes** | **FAIL (twijfel)** | De twee hangende klauwen van de opgetilde poot hebben een **rechte buitenrand**: klauw A links x 19, 18, 18, 17, 17, 16, 16 (y 54–60, segmenten 1-2-2-2, regelmatig dus recht), klauw B links x 21, 21, 21, 20, 20, 20 (3-3). Op 3× en 8× lezen ze als taps toelopende spijkers of twijgjes, niet als haken. Alleen de binnenrand van klauw A buigt (3-1-1-1-1). De maker noemt ze "gladde haken"; dat zie ik niet. |
| Open randen en losse pixels | **FAIL** | Zie eis 9. Geen losse pixels. |

## Reparaties (klein, per zone)

**R1. Gat in de schaduwrand onder de buik** (zone x 31–34, y 47–48; 2 px)
- (32,47) en (33,47): 6 → 1.
- Zo loopt de zwarte boog van (31,48) naar (34,48) door. De alpha verandert niet.

**R2. Gat onder de nabije dij** (zone x 42–45, y 51–52; 2 px)
- (43,51) en (44,51): 6 → 1.
- De boog (42,51)–(45,52) sluit. De alpha verandert niet.

**R3. Glans op de buitenrand van de klauwen van de staande voet** (zone x 24–28, y 59–61; 2 px)
- (25,61): C → B. De grondkant van de onderste klauw mag niet het lichtste punt zijn.
- (25,59): C → B. Wil de maker een glans houden, dan alleen op een pixel die niet aan transparant grenst; in een klauw van 2 rijen bestaat die niet, dus hier geen glans.
- De alpha verandert niet.

**R4. Haak in de hangende klauwen** (zone x 15–22, y 57–60; ±4 px)
- Dit **raakt silhouet ronde 8**, dus Jordi beslist eerst (WERKWIJZE stap 4.3).
- Klauw A:
  - de punt buigt 1 px terug naar de poot: (16,60) wordt transparant, (17,60) wordt F;
  - (16,59) B → F, zodat de punt donker afloopt.
- Klauw B:
  - (20,60) wordt transparant, zodat de punt op (21,59) F eindigt en naar rechts haakt;
  - (20,59) B blijft.
- Er blijft lucht naar de bovenste klauw van de staande voet op (22,60).
- Netto −1 px in het silhouet.
- **Kleuralternatief zonder silhouetwijziging**, als Jordi het silhouet wil houden: (16,59) B → F en (20,59) B → A. De punten donkeren dan eerder af, zodat het lichte deel korter en meer gebogen leest. Dat is minder sterk dan de silhouetversie.

**Bewijs na de reparatie:**
- alpha-diff 0 tegen ronde8, of tegen een ronde 9 als R4 met silhouet wordt gekozen;
- diff buiten de zones R1–R4 = 0;
- het open-randscript geeft voor 6/3/4/7/8/9 aan de schaduwkant 0 treffers.

## Voor Jordi (smaakkeuzes, niet als FAIL geteld)

1. **Silhouet ronde 8 is nieuw** (maker, ronde 7):
   - aan de staande poot: −2 px en +4 px;
   - aan de klauwen: −2 px.
   - Kijk of de staande poot nu "iets minder recht, klein beetje naar achter" is zoals je vroeg. Ik vind van wel: de voorrand loopt 27 → 28 → 29 en de achterrand 31 → 32.
2. **Klauwen hangend** (R4): wil je een echte haak (1 px silhouet) of alleen een kleuroplossing?
3. **Vlekken tegen het oog:** de crème vlekken boven en onder het oog zijn groter en lichter dan het oog. Dat staat al als bewaarde A/B-test in de SPEC ("bovenste vlek een tint terug").
4. **Algemene helderheid:** naast Linoone, Furret en Persian oogt hij donkerder dan R/S, naast Mightyena en Houndoom passend. Iets meer bruin licht (8/9) op schouder en flank zou meer R/S zijn.
5. **Naad muts–hals:** y 36–38 staat 3 px recht op x 28. Eén vachtplukje (bijv. (28,37) 6 → 3 of (27,36) 3 → 6) maakt het nog zachter. Puur smaak.
6. **Kaakonderkant** (y 48–49) is een lange, bijna rechte donkere lijn (silhouet); de rugcontour (y 29–35) heeft een kleine bult bij x 32–35. Beide zijn bevroren; alleen gemeld.
7. **Soliditeit en box** (0,60; 56×62) door de lange staart. Hoort bij het besluit "staart met patroon, mag krullen".
8. **Verre poten** zijn maar een fractie donkerder dan de nabije (hooglicht 4 tegen 5). Voor meer diepte kunnen de verre poten één tint omlaag.

## Na het lezen van de eerdere keuringen

- Wat ronde 2 en 3 als FAIL hadden, is opgelost:
  - de mondlijn is er;
  - de helm-naad kartelt;
  - het oog heeft een donkere en een lichte iris en een glans;
  - de selout F zit op staart en oren;
  - er staat geen glans meer op de buitenrand van de hangende klauwen.
- **Nieuw** in deze keuring:
  - de twee gaten van index 6 aan de schaduwkant van buik en dij (R1, R2). De maker meldt "open randen 0", maar zijn script telt 6 blijkbaar als omlijning; aan de schaduwkant hoort zwart;
  - de glans op de buitenrand van de nieuwe klauwen van de staande voet (R3);
  - de rechte buitenranden van de hangende klauwen (R4).

## Eindoordeel: **BIJNA**

Hij leest als een coati en als een echte Pokémon, en de opbouw (muts, oog, staart, poten) staat. Wat nog nodig is:
- R1–R3: 6 pixels kleur, zonder alphawijziging;
- R4: een kleine klauwhaak. Daarvoor beslist Jordi eerst of het silhouet 1 px mag veranderen.

Na R1–R3, en R4 in welke vorm Jordi ook kiest, is hij klaar voor `af/`.
