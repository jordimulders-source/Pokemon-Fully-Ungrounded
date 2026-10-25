# Coathief kleur ronde 2: onafhankelijke keuring

Keurder: verse agent (25 okt). Eerst zelf geoordeeld, daarna pas `NOTITIES.md` van ronde 1 en 2 gelezen. Twijfel = FAIL. Er is niets aan de sprite veranderd.

- Gekeurd: `coathief.png` (ronde 2).
- Vel: `keuring_vel.png`. Daarop staat de sprite op 8×, 3×, 2× en 1×, op licht en donker, naast:
  - de olinguito (fase 1) en ronde 1;
  - 14 echte sprites: Linoone, Zigzagoon, Furret, Sentret, Mightyena, Poochyena, Houndour, Houndoom, Sneasel, Liepard, Raichu, Ursaring, Teddiursa en Sandslash (eerste frame).

## Metingen (scripts)
| Meting | Uitkomst |
|---|---|
| Alpha tegen `silhouet/ronde1.txt` en `ronde1_1x.png` | **0 verschil** (1297 px) |
| Kleuren | 14 + transparant (index 15 `3a1e10` is ongebruikt); mode P, transparency=0 |
| Bbox | 56 × 62 (x 4–59, y 1–62) |
| Losse pixels (zonder 4-buur) | 0 |
| Losse delen (4-samenhangend) | 2: het lijf, plus een **eiland van 2 px op (21–22, 62)** dat alleen schuin vastzit. Dat eiland zit in het bevroren silhouet. |
| Randkleuren naast transparant | k 139, m 66, d 26, **n 32**, **c 3**, **w 4**, **z 1** |
| Zeer donker aandeel (luma < 45) | 0,24 (olinguito 0,20; voor Dark is dat ok) |
| Gemiddelde luma: kop (z/y/m) | 51 |
| Oog (6 px) | gemiddeld 99. **Iris-donker r = luma 51, gelijk aan de kop**; iris-licht i = 101; glans 238 |
| Vlekken (elk 7 px) | gemiddeld **196**: twee keer zo helder als het oog |
| Onderpoten (gemiddelde luma) | nabije voorpoot 55, nabije achterpoot 48, verre voorpoot 42, verre achterpoot 41 |
| Naad kop–hals (eerste bruine x per rij, y 35–47) | 26, 26, 27, 27, 27, 27, 26, 26, 26, 25, 24, 25, 23. Er loopt een doorlopende m-kolom op x 25–26 van y 35 tot 47. |

Over het palet: d (`5e3216`, luma 60) is de selout van de vacht. Hij wordt ook binnenin als schaduw gebruikt, net als index 3 bij de goedgekeurde olinguito (luma 55). Dat volgt de huisstijl, dus d aan de rugrand reken ik niet als open rand. Bij n (luma 139) ligt dat anders: hij staat als "omlijning" naast transparant op lichte delen, en dat is geen omlijning.

## Harde eisen SPRITE_NORM
| # | Eis | Oordeel | Reden |
|---|---|---|---|
| 1 | Leest op 1× als echte Pokémon | PASS | Naast Linoone, Mightyena en Houndour leest hij op 1× als een coati: oranje lijf, zwarte wigkop, geringde staart rechtop en lichte klauwen. Hij is donkerder dan de meeste refs, maar vergelijkbaar met Houndour en Mightyena. |
| 2 | 3/4 links-voor, één oog, neus vooraan | PASS | Lange snuit, één oog, zwarte neus als meest linkse punt. Het silhouet is bevroren. |
| 3 | Ledematen tellen, verre in schaduwtint | PASS | 4 poten in eigen kolommen. De verre poten zijn donkerder (luma 41–42 tegen 48–55), gescheiden met k aan de schaduwkant van de nabije poot. Diagonale gang. |
| 4 | Geen Escher | PASS | De nabije voorpoot ligt over en vóór de verre. De nabije dij heeft een d-selout tegen de verre achterpoot. |
| 5 | Lijf, curven | PASS | De schouder- en dijcontouren in d zijn gebogen en de rug heeft een lichtband. De rechte naad hoort bij de helm-kop (zie de valkuilen). |
| 6 | Kop | PASS | Kophoogte ±27% (17 van 62 rijen), passend voor fase 2. Bevroren. |
| 7 | Ogen geïntegreerd | **FAIL** | De bouw klopt: zwart lid, glans linksboven, iris donker boven en licht onder. Maar r (luma 51) = de kop (51), dus de bovenste helft van de iris verdwijnt. Op 1× blijft er een witte pixel met 2 oranjerode pixels over: dat is precies de "rode stip". De twee vlekken (luma 196) trekken meer aandacht dan het oog. |
| 8 | Kenmerken op 1× leesbaar | PASS | Muts, vlekken, staartringen en de twee klauwen van de opgetilde poot lezen op 1×. Over de klauwen aan de andere poten: zie "voor Jordi". |
| 9 | Omlijning, geen open randen | **FAIL** | Lichte tinten staan als buitenrand naast transparant. **n** (luma 139) zit op 32 px: de linkerkant van de lichte staartringen, de staartkrul en de oortoppen. **c en w** zitten op 7 px: de buitenkant van de klauwen (de glans aan de buitenrand is anti-aliasing aan de buitenkant). **z** op (24, 61) is basis naast transparant. Op een witte achtergrond lopen de lichte ringen en klauwen links in de achtergrond over. De olinguito heeft alleen randen met een luma ≤ 56. |
| 10 | Geen Chernobyl | PASS | Geen crème uit het niets; alle lichte vlakken zijn coati-kenmerken. Geen zwevende delen in kleur (het 2-px-eiland is een silhouetzaak). |

## SPRITING §0
| # | Punt | Oordeel | Reden |
|---|---|---|---|
| 1 | Lijf en blik diagonaal | PASS | Bevroren B1 (lijf 42°, kop 52°). |
| 2 | Ledematen, oren en ogen geteld en verbonden | PASS | 4 poten, 2 oren (het verre 1 px, het nabije 3 px), 1 oog. Het 2-px-eiland op (21–22, 62) is silhouet: zie "voor Jordi". |
| 3 | Geen rechte lijnen | **FAIL** | De naad tussen kop en hals is een vrijwel verticale m-lijn van 13 rijen (x 25–27). De omtrek zelf (kaakonderkant) is silhouet: zie "voor Jordi". |
| 4 | Ogen geïntegreerd | **FAIL** | Zie eis 7. |
| 5 | Silhouet leest op 1× als de soort | PASS | Coati. |
| 6 | Formaat | PASS | 1297 px, binnen fase 2 (1100–1550) en 1,1× de olinguito. De box van 56 × 62 komt door de staart: zie "voor Jordi". |
| 7 | Pose niet stijf | PASS | Opgetilde voorpoot, verre achterpoot hoger, gewicht op twee poten. |

## FAKEMON_CHECKLIST (kleurrelevant)
| # | Oordeel | Reden |
|---|---|---|
| B7 Gezicht compleet | **FAIL** | **Er is geen mond.** Poochyena, Mightyena, Houndour, Houndoom en Linoone hebben allemaal een mondlijn onder de snuit. Hier is de kaak een egale z-wig, en het gezicht oogt onaf. |
| E1 Verre kant donkerder | PASS | 41–42 tegen 48–55. Het verschil met de nabije achterpoot is klein, maar wel zichtbaar. |
| E2 Overlap met omlijningsbasis | PASS | De nabije dij heeft een d-selout tegen de verre achterpoot. De k ertussen is de schaduwrand van de verre poot. |
| E3 Donkerte | PASS | 0,24, Dark. |

## Valkuilen WERKWIJZE stap 3
| Valkuil | Oordeel | Reden |
|---|---|---|
| Helm-kop | **FAIL** | De muts eindigt in een rechte m-kolom (x 25–26, y 35–47), met de bruine hals er direct tegenaan. Op 8× en 3× lijkt het een losse helm die op het lijf is gezet. De maker schrijft in ronde 1 zelf: "geen 2 px donkere kolom … anders wordt het een helm". Die kolom staat er wel. |
| Ruis | PASS | 109 enkelvoudige kleurpixels (olinguito 93), op de juiste plekken (randen, contourlijnen). De grote vlakken zijn rustig. |
| Plat 2D | PASS | De kop heeft een y/Y-licht linksboven en m onder de kaak. Het lijf heeft een rug-licht, schouder- en dijbollen en een buikschaduw. De staartringen hebben een licht- en een schaduwkant. Het mag ruimer: zie "voor Jordi" (hooglicht). |
| Mini-oog op donkere kop | **FAIL** | Zie eis 7. De glans is er en de lichte iris zit tegenover de glans, maar de donkere iris is onzichtbaar en de vlekken overstralen het oog. |
| Verre ledematen | PASS | Schaduwtint, eigen kolom. |
| Klauwen als stokjes | PASS | Twee gebogen haken (w/c/n), elk 2–3 px, met een punt. De rand is wel fout: zie eis 9. |
| Open randen | **FAIL** | Zie eis 9. |

## Reparaties (klein, per zone)
1. **Oog** (zone x 18–23, y 36–45, ±2 px plus 1 paletwaarde):
   - Maak index 13 (r) lichter, zodat de donkere iris boven de kop uitkomt: van `6a1c14` naar ±`8c2418` (luma ±65 of meer, nog altijd duidelijk donkerder dan i). Dat is 0 px, want r komt alleen in het oog voor.
   - Zet de w-glans in beide vlekken terug naar c: (20, 36) en (21, 43). Dan is het oog het helderste punt van de kop.
2. **Mond** (zone x 8–14, y 45–47, ≤ 6 px):
   - een k-lijn van ±4 px vanaf achter de neus naar achteren: (8–11, 46);
   - een mondhoek van 1 px in m op (12, 45) of (12, 47), naar keuze grijns of grimas.
   - De kaak eronder blijft 1 rij z plus de k-omlijning.
3. **Naad kop–hals** (zone x 22–28, y 34–47, ±12–16 px):
   - Haal de m-kolom weg: binnen de muts z of y, aan de halskant d.
   - Laat de grens als vachtkartel lopen: om de 2–3 rijen een d-plukje 1 px de muts in, en een z-plukje 1 px de hals in.
   - Zet de uitbolling van de schedel achter het oor (y 35–40) 1 px verder naar rechts.
   - Geen nieuwe donkere lijn.
4. **Open randen** (±40 px, plus eventueel 1 paletwaarde):
   - **Staart en oren:** maak van de ongebruikte index 15 een selout voor crème van ±luma 95–105 (bv. `7c6448`). Zet daarmee de n-randpixels om: (49–50, 1), (48, 2), (47, 3), (46, 4–6), (53, 6–7), (54, 11–14), (53, 19–22), (51, 26), (50, 27), (49, 28), en de oortoppen (17, 33) en (21–23, 33). De n binnenin blijft.
   - **Klauwen** (x 16–21, y 56–60): geen w of c op de buitenrand. (17, 56), (16, 57), (20, 57) en (19, 58) worden c → n, en (16, 58), (16, 59) en (20, 59) worden c → n of x. Houd per klauw één w-glans binnenin, bv. (17, 57) en (20, 58).
   - **(24, 61):** z wordt m.
   - Bewijs: alpha-diff 0 en een diff buiten de zones van 0.

Ik reken op ±75 px in totaal. Alles daarbuiten blijft bevroren: het lijf, de staartringen binnenin, de poten en de neus.

## Voor Jordi (smaak en silhouet; geen opdracht aan de maker)
- **Lijfkleur:** warm oranje-roodbruin (*Nasua nasua*, conform de SPEC). Dat is warmer en verzadigder dan de doffe bruine olinguito. Het is te temperen met alleen paletwaarden (b/l/h). Is de lijn zo herkenbaar genoeg?
- **Klauwen aan de andere poten:** alleen de opgetilde voorpoot heeft zichtbare klauwen.
  - De verre voorpoot heeft nu **donkere tenen** in plaats van klauwtjes, omdat crème haakjes binnen het silhouet als kruimels lazen (zie `uitsnede_klauwen.png`).
  - De achtervoeten zijn klauwloos.
  - De SPEC zegt "2 lange lichte klauwen per poot". De olinguito had ook alleen klauwen aan de voorpoot.
  - Wil Jordi klauwen aan meer poten, dan moet het silhouet daar 1–2 px groter (y 60–62, x 20–26, en de nabije achtervoet x 45–48).
- **Eiland van 2 px op (21–22, 62)**, onder de verre voorvoet. Het zit alleen schuin vast (silhouet). Bij een silhouetreparatie verbinden of weghalen.
- **Kaakonderkant:** twee rechte k-stukken van 8–9 px (y 48, x 5–12 en y 49, x 13–21) in het silhouet. Op 1× leest de kop daardoor als een wig of liniaal. Een knik of een lichte bolling onder de kaak zou helpen.
- **Pose "confrontatie, naar je toe":** op 1× leest hij eerder als "snuffelend naar links lopen" dan als "op je af komen". De kop wijst opzij-omlaag. Dat is het bevroren silhouet; alleen melden.
- **Box van 56 × 62** is groter dan de richtlijn voor fase 2 (±47–53) door de rechtopstaande staart. Het oppervlak klopt wel.
- **Hooglicht:** de romp heeft weinig h (18 px) en veel d (169 px). Naast Linoone en Furret oogt hij somber, naast Houndour en Mightyena passend. Iets meer l/h op de schouder zou "R/S-lichter" ogen. Dat is een smaakkeuze.
- **Vlekken:** de vorm volgt keuze C ("echte coati-vlek"). Ze staan boven-achter en onder-achter het oog, niet er recht boven en onder.

## Eindoordeel: **BIJNA**
De vorm, het palet en het volume staan, en hij leest als een coati. Er zijn vier kleine reparaties in benoemde zones:
1. het oog boven de vlekken laten uitkomen;
2. een mond;
3. de helm-naad;
4. de lichte open randen van de staart, oren en klauwen.

Geen herbouw nodig.
