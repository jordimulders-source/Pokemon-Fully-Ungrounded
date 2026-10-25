# Coathief ronde 8b: laatste keuring (verse keurder)

Keurder: verse agent (25 okt). Ik heb eerst helemaal zelf geoordeeld (scripts, vel, alle richtlijnen) en pas daarna `ronde7/EINDKEURING.md`, `ronde2/KEURING.md` en `ronde3/EVOLUTIEKEURING.md` gelezen. Twijfel = FAIL. Aan de sprite is niets veranderd; de reparaties hieronder zijn alleen in een kopie in de scratchpad geproefd.

- **Gekeurd:** `coathief.png` (ronde 8b), silhouet `../../silhouet/ronde10.txt`.
- **Vel:** `laatste_keuring_vel.png`, met:
  - de sprite op 8× en 3×, op licht en donker;
  - de sprite op 1× en 3×, op licht en donker, naast de olinguito en 12 echte Gen 3-sprites: Linoone, Zigzagoon, Furret, Mightyena, Poochyena, Sneasel, Houndour, Absol, Zangoose, Sandslash, Umbreon en Sentret (`anim_front_gba.png`, de eerste 64 rijen);
  - onderaan de vier klauwen op 12× (licht, donker en wit) plus 1× en 3×. In de bovenste rij staat ronde 8b zoals hij is, in de onderste rij de voorgestelde reparatie (magenta kaders).
- **Vorm:** de vorm is door Jordi goedgekeurd en bevroren. Waar een richtlijn naar de letter niet gehaald wordt door die bevroren vorm, staat **BEVROREN**. Dat telt niet als FAIL en ik stel er geen reparatie voor; zulke punten staan wel onder "Voor Jordi".

**Indexen:**

| Index | Kleur |
|---|---|
| 1 | zwart |
| 2 | bijna-zwart |
| 3 | muts, basis |
| 4 | muts, licht |
| 5 | muts, hooglicht |
| 6 | bruin, omlijningsbasis/schaduw |
| 7 | bruin, basis |
| 8 | bruin, licht |
| 9 | bruin, hooglicht |
| a | crème, schaduw (164,134,96) |
| b | crème, basis |
| c | glans |
| d | iris, donker |
| e | iris, licht |
| f | crème-selout (124,100,72) |

## Scripts

| Controle | Uitkomst | Oordeel |
|---|---|---|
| Formaat | 64×64, mode P, `transparency` 0, 16 paletkleuren, index 0 transparant (152,208,160); alle 16 indexen gebruikt | PASS |
| Alpha-diff tegen `silhouet/ronde10.txt` | 0. Beide hebben 1315 px. Box 56×62 (x 4–59, y 1–62). | PASS |
| Eilanden | 1 component bij 4-buren en bij 8-buren; 1 transparant gebied (geen ingesloten gaten) | PASS |
| Losse pixels | Geen zwevende pixels. 112 enkelvoudige kleurpixels: contourlijnen, ringranden, oog, vlekken en klauwen; de vlakken zijn rustig. 5 uitsteeksels (≤ 1 opake 4-buur): (15,33) punt van het verre oor, (35,56) teen van de verre achtervoet, (18,59) en (21,59) klauwpunten K1 en K2, (22,62) klauwpunt K3. Dat zijn allemaal bedoelde punten. | PASS |
| Open randen: pixels naast transparant die niet 1 of 2 zijn | 66 stuks, waarvan 39 keer f en 22 keer 6. De f zit aan de lichtkant van de staart en op de bovenrand van de klauwen, als selout. De 6 zit op de belichte bovenrand van rug en schouder (y 29–35) als omlijningsbasis. Geen 6 aan de schaduwkant: de vier gaten uit ronde 7 (32/33,47 en 43/44,51) zijn dicht. **Fout:** b op (18,56), (18,57), (18,58) en (21,58), en a op (28,61). | **FAIL** (5 px) |
| Rechte contourstukken ≥ 5 px | Kaakonderkant y 48 (8 px) en y 49 (9 px). Staart links x 54 (y 8–18, 11 px) en rechts x 59 (y 8–21, 14 px). Staande poot rechts x 31 (y 48–60, 13 px; door Jordi zo gevraagd: "mag iets rechter"). Verder 5–6 px op de staartkrul, de rug en de achtervoet. | BEVROREN |
| Helderheid (luma) | Gemiddeld 80 en donker-aandeel (< 50) 0,23. Ter vergelijking: Linoone 161, Furret 151, Zigzagoon 135, Mightyena 78, Houndour 85, Umbreon 89, olinguito 71. | PASS |
| Oppervlak en kop | 1315 px (fase 2: 1100–1550); ×1,12 de olinguito. Kop y 31–49 = 31% van de hoogte. | PASS |
| Soliditeit en symmetrie | Soliditeit 0,60, door de rechtopstaande staart. Symmetrie 0,73. | BEVROREN / PASS |

## Klauwcheck (vier klauwen)

- **K1:** opgetilde poot, voorste klauw (x 18–19, y 56–59).
- **K2:** opgetilde poot, achterste klauw (x 21–22, y 56–59).
- **K3:** staande voet, voorste klauw (x 22–24, y 59–62).
- **K4:** staande voet, achterste klauw (x 26–28, y 59–62).

| Vraag | K1 | K2 | K3 | K4 |
|---|---|---|---|---|
| Leest op 1× en 3× als klauw, op licht en donker | Op donker wel: een hangende haak. **Op licht niet:** de linkerkant is crème b direct naast de achtergrond, waardoor de klauw er op een lichte en een witte achtergrond in oplost. Het blijft een vage lichte veeg zonder rand. → **FAIL** | Op donker wel. Op licht vervaagt de linkerrand van (21,58) in de lucht tussen de klauwen. → **FAIL** (na de reparatie PASS) | Ja, als een lichte nagel die naar voren op de grond ligt, met de punt op (22,62) naar voren. Op 1× een lichte stip aan de voet, zoals bij Linoone. Het is geen echte haak (zie "Voor Jordi"). → PASS | Ja, als een korte, ronde nagel met glans. Het is eerder een nagel dan een haak (zie "Voor Jordi"). → PASS |
| Vast aan de poot | Ja, via de knokkelrij y 55–56 (f b c b b a / b b b b a). | Ja, dezelfde knokkelrij. | Ja, de f-rij (24–26,59) sluit aan op de voet. | Ja, onder (27–28,59) van de voet. |
| Opbouw: crème kern, glans binnenin, donkere rand aan de schaduwkant en op de punt | Kern b, met de glans in de hand op (20,55), helemaal binnenin. Schaduwkant (19,58) en (20,57) f, punt (18,59) f. De lichtkant mist een selout. → FAIL (valt onder de open randen) | Kern b. Schaduwkant (22,57–58) f, punt (21,59) f. → PASS (na de reparatie van de lichtkant) | Kern b (24,60–61) met f rondom. Geen eigen glans, wat in een kern van 1 px ook niet kan. → PASS | Kern b/c, met de glans (27,60) binnenin: hij grenst aan de voet en niet aan transparant. Schaduwkant a (28,60–61), maar **(28,61) a ligt naast transparant aan de onderkant**: de schaduwkant is open. → **FAIL** |
| Lucht tussen de klauwen | (20,58–59) is transparant: 2 rijen lucht, met f op (20,57) als scheiding bovenaan. → PASS | idem | Tussen K3 en K4 staat een f-scheiding op (25,59–61) en alleen onderaan lucht op (25,62). Op 3× lezen het toch twee nagels. → PASS | idem |
| Curves zonder trapjes of hoeken | Recht omlaag vanaf de knokkel en dan een punt; geen trapjes. → PASS | idem → PASS | → PASS | → PASS |
| Geen open randen | **FAIL:** (18,56), (18,57) en (18,58) zijn b naast transparant. | **FAIL:** (21,58) is b naast transparant. | PASS | **FAIL:** (28,61) is a naast transparant, aan de onderkant (schaduwkant). |

**Conclusie klauwen:** K1, K2 en K4 halen het niet, alleen door 5 randpixels; dat is met kleur te repareren. Na de reparatie lezen K1 en K2 ook op licht en wit als twee aparte haken, met een tan selout zoals de klauwen van Sandslash (vel, onderste rij). De olinguito sluit zijn klauwen aan de lichtkant zelfs met zwart af, dus een tan selout is de lichtere variant van dezelfde regel. Kleiner of anders van vorm worden ze niet.

## Richtlijnen

### SPRITE_NORM, harde eisen
| # | Eis | Oordeel | Reden |
|---|---|---|---|
| 1 | Leest op 1× als echte Pokémon | PASS | Naast Linoone, Mightyena, Houndour en Poochyena leest hij op 1× direct als neusbeer: zwarte wigkop met lange snuit, warm lijf, geringde staart rechtop met een haak. |
| 2 | 3/4 links-voor, kop meer gedraaid; lange snuit → één oog | PASS | Eén oog, de zwarte neus is de meest linkse punt, het verre oor is zichtbaar en het lijf staat schuin (B1). |
| 3 | Alle ledematen, eigen kolom, ≥ 5–6 px, gewrichten, diagonaal | PASS | 4 poten. De nabije voorpoot is opgetild, de verre voorpoot staat. De verre achterpoot staat hoger (voet y 57 tegen y 60). Er is lucht tussen de poten en beide achterpoten hebben een hak. Diagonale gang. |
| 4 | Geen Escher | PASS | De opgetilde poot ligt over de staande en de nabije dij over de verre achterpoot. |
| 5 | Skelet, curven, geen rechte lijnen ≥ 4 px, niet symmetrisch | PASS / BEVROREN | De shading volgt de ronding. De rechte staartkolom, de kaak en de staande poot horen bij de bevroren vorm (zie de scripts). Symmetrie 0,73. |
| 6 | Kop | PASS | 31% (fase 2: 30–35%). |
| 7 | Ogen geïntegreerd | PASS | Zwart bovenlid (18–20,39), iris d boven en e onder, glans c linksboven (18,40), lichte iris tegenover de glans. Klein en geen platte stip: op 3× een Pokémon-oog zoals bij Mightyena en Poochyena. |
| 8 | Kenmerken op 1× leesbaar | PASS | Bivakmuts, de twee coati-vlekken, de zwarte neus, de staartringen en lichte klauwen aan beide voorpoten. |
| 9 | Omlijning per groep, zwart aan de schaduwkant, licht linksboven, geen open randen | **FAIL** | De rest klopt: 6 als selout op de rug, f op de staart, zwart rechts en onder, licht linksboven. Maar er zijn 5 open randpixels aan de klauwen (zie de klauwcheck). |
| 10 | Geen Chernobyl | PASS | Gezicht compleet, geen crème uit het niets, geen losse delen. |

### SPRITE_OPDRACHT §2 (Jordi's vaste feedback)
| Punt | Oordeel | Reden |
|---|---|---|
| Lijf en blik 3/4 links-voor | PASS | Zie eis 2. |
| Snuitdier: één oog, snuit is één vorm | PASS | De snuit wijst schuin naar links-onder, met de neus aan het eind. |
| Alles telt en is verbonden; poten niet aan elkaar vast | PASS | 1 component. De poten zijn gescheiden door lucht of omlijning. |
| Diagonaal lopen, geen telgang | PASS | De nabije voorpoot is geheven; de verre achterpoot is hoger en naar voren. |
| Pose niet stijf, één houding | PASS | Lopend, met het gewicht op de staande voor- en de achterpoten. |
| Lijf over een echt skelet, geleidelijke overgangen | PASS | Bevroren silhouet uit het poppetje en de onderlaag. |
| Formaat tegen dezelfde fase, kop niet te groot | PASS | 1315 px en 31%. De groei ×1,12 is een besluit van Jordi. |
| Kenmerken op 1× | PASS | Zie eis 8. |
| Geen rechte lijnen, geen overdreven rechte staart | BEVROREN | De staart staat 11–14 rijen recht omhoog (coati, `foto4`). Op 1× leest hij goed. Zie "Voor Jordi". |
| Ogen geïntegreerd | PASS | Zie eis 7. |
| Omlijning per kleurgroep, geen open randen | **FAIL** | Zie eis 9. |
| Kleuren tegen hetzelfde type (Dark mag donker) | PASS | Luma 80, tussen Mightyena (78) en Houndour/Umbreon (85–89). Ruim donkerder dan Linoone (161) en Furret (151), zoals Jordi wil. |
| Verzonnen kleurvlakken alleen als ze werken | PASS | Bivakmuts en vlekken lezen als coati (keuze C). |
| Referentie herkenbaar | PASS | *Nasua nasua*. |
| Goedgekeurd blijft letterlijk staan | PASS | Alpha-diff 0 tegen ronde10. |

### SPRITING §0–§8
| § | Punt | Oordeel | Reden |
|---|---|---|---|
| §0.1 | Lijf en blik diagonaal | PASS | Zie eis 2. |
| §0.2 | Geteld en verbonden | PASS | 4 poten, 2 oren, 1 oog, de staart en 2 klauwen per voorpoot. |
| §0.3 | Geen rechte lijnen | BEVROREN | Zie de scripts. |
| §0.4 | Ogen | PASS | Zie eis 7. |
| §0.5 | Silhouet leest als de soort | PASS | Coati. |
| §0.6 | Formaat | PASS | Fase 2. |
| §0.7 | Pose niet stijf | PASS | |
| §1–2 | Handwerk, per onderdeel | PASS | Overgetrokken cel voor cel; geen filters of verlopen te zien. |
| §3 | Curven | BEVROREN | De rugcontour heeft segmenten 1-3-4-2-2-6 (y 29–35), wat niet gelijkmatig oploopt. Dat zit in het silhouet en op 1× zie je het niet. De klauwcurves zijn schoon. |
| §4 | Palet: 3 tinten + omlijning per groep, één tint per groep | PASS | Muts 1-2-3-4-5, vacht 6-7-8-9, crème f-a-b-c, iris d-e. Er is niet overgeshaded. |
| §5 | Licht linksboven, evenaar, slagschaduw | PASS | Hooglicht 8/9 op rug en schouder, 4/5 op de snuitrug en de schedel. Buik en dij in 6, de staartringen rechts donker. |
| §6 | Glans en ogen | PASS | Glans en reflectie in het oog, glans op de neus (5,45). |
| §7 | Textuur | PASS | Rustig, geen spikkels. |
| §8 | Omlijning: zwart alleen aan de schaduwkant, selout aan de lichtkant, 1 px, geen AA buiten | **FAIL** | Alleen de klauwen: daar ligt basis b aan de lichtkant zonder selout, zie eis 9. Over pseudo-omlijning (§8, dunne delen): ronde 7 rekende de klauwen daaronder. Op de lichte en witte achtergrond van het vel lossen K1 en K2 echter op, en ronde 2 keurde precies dit al af ("op een witte achtergrond lopen de lichte ringen en klauwen links in de achtergrond over"). Bij twijfel geldt FAIL. |

### SPRITE_WERKWIJZE stap 3: valkuilen
| Valkuil | Oordeel | Reden |
|---|---|---|
| Kop als helm | PASS | De bivakmuts is een ontwerpkeuze. De naad muts–hals loopt schuin en kartelt met 6-plukjes. |
| Ruis | PASS | Grote rustige vlakken. |
| Plat (2D) | PASS | Kop en lijf rond geschaduwd, staartringen met een licht- en schaduwkant, poten met een lichtkant (4/5). |
| Mini-oog op een donkere kop | PASS | Lid, glans en lichte iris tegenover de glans. |
| Verre ledematen in de schaduwtint | PASS (zwak) | De verre poten zijn maar iets donkerder dan de nabije. Ze lezen wel apart door hun hoogte en kolom. |
| Klauwen als gebogen haakjes | PASS na reparatie | K1 en K2 zijn hangende haken. K3 en K4 zijn liggende nagels (vorm, zie "Voor Jordi"). |
| Open randen en losse pixels (script) | **FAIL** | 5 px, zie de klauwcheck. Geen losse pixels. |

### FAKEMON_CHECKLIST
| # | Oordeel | Reden |
|---|---|---|
| A1 | PASS | Coati. |
| A2 | PASS | De geringde staart met haak breekt de omtrek. |
| A3 | PASS | Kop linksonder en de staart als tegenwicht rechtsboven. |
| A4 | BEVROREN | Soliditeit 0,60 (< 0,65) door de staart; er is genoeg lucht tussen de poten. |
| A5 | PASS | 0,73. |
| A6 (R) | BEVROREN | De staart is een zuil (x 54/59, 11 rijen evenwijdig). Coati's houden de staart rechtop. |
| B1–B7 | PASS | Eén oog, neus vooraan, de snuit als één vorm, het verre oor kleiner, de kop vóór de borst. Gezicht compleet: neus, mondlijn (8–10,46) → (11,46) → (12,47), die naar achteren daalt en dus geen lachmondje is. |
| C1–C9 | PASS | Zie eis 3. C6 en E1 zijn zwak: de verre poten zijn nauwelijks donkerder. |
| D1 | PASS | 1315 px. De box van 56×62 is groter dan ±47–53, door de staart. |
| D2 | PASS | 31%. |
| D5 (R) | Besluit van Jordi | ×1,12 ("formaat blijft"). |
| E1 (R) | Zwak | Zie hierboven. |
| E2 | PASS | Naden in 6 en 2 tussen de nabije en de verre delen. |
| E3 | PASS | 0,23 (Dark). |

### SPEC (besluiten en Jordi's woorden)
| Besluit | Oordeel | Reden |
|---|---|---|
| Warm roodbruin lijf, donkerder dan Linoone en Furret, niet lichter maken | PASS | Vacht 6/7/8/9 warm roodbruin. Totaal-luma 80 tegen 161 en 151. |
| Zwarte bivakmuts-kop met coati-vlekken boven en onder het oog | PASS | Vlek boven (19–21,36–38) sluit aan op het lid, vlek onder (20–22,43–45). Alleen een lichte ring rond het oog, verder zwart. |
| Zwarte neus | PASS | (4–7,44–47) met een glans op (5,45). |
| Zwarte oren | PASS | Beide oren 2/3/4/5 met een 1-rand rechts, rond en niet afgeknipt. |
| Klein Pokémon-oog, geen rode stip | PASS | Zie eis 7. |
| Geen lachmondje | PASS | De mondlijn daalt naar achteren. |
| Staart met ringpatroon | PASS | Afwisselend crème en zwart, met een licht- en schaduwkant per ring, tot in de krul. |
| Klauwen aan beide voorpoten, niet aan de achterpoten | PASS | 2 aan de opgetilde poot en 2 aan de staande voet. De achtervoeten zijn grijs, zonder crème. |
| Geen tas of voorwerp | PASS | |
| Driekwart naar je toe lopen, één voorpoot opgetild | PASS | Bevroren pose. |

## Reparaties (alleen kleur, alpha-diff 0, 5 px)

| Pixel | Oud → nieuw | Reden |
|---|---|---|
| (18,56) | b → a | De lichtkant van de knokkel ligt naast transparant. a wordt de selout, zoals de klauwen van Sandslash. |
| (18,57) | b → a | De lichtkant van K1: de klauw lost niet meer op in een lichte achtergrond, en de crème kern blijft (19,57). |
| (18,58) | b → a | idem; de punt (18,59) f blijft donker. |
| (21,58) | b → a | De lichtkant van K2, aan de lucht tussen de klauwen. Zo lezen K1 en K2 op licht als twee aparte haken. |
| (28,61) | a → f | De schaduwkant en onderrand van K4 lagen open. De omlijning loopt nu door met (26–27,62) f en (29,61) 1. |

**Bewijs** (proef in de scratchpad):
- 5 px gewijzigd, alpha-diff 0;
- naast transparant liggen daarna alleen nog 1, 2, 6 (lichtkant), f, en a op de vier lichtkantpixels hierboven;
- op 1×, 3× en 12× op licht, donker en wit lezen K1 en K2 als twee lichte haken met een rand (vel, onderste rij).

## Voor Jordi

Geen van deze punten is een opdracht aan een maker.

1. **K3 en K4 (staande voet) lezen als twee liggende nagels, niet als haken.** Dat volgt de onderlaag ("grote crème klauwen ook aan de staande voet, naar voren op de grond"). Op 1× is het een lichte stip aan de voet, zoals bij Linoone. Een echte haak kan alleen met een silhouetwijziging, dus alleen als je dat wilt.
2. **Lengte van de klauwen tegen de olinguito:** de hangende klauwen zijn 4–5 rijen lang, die van de olinguito ±6. De evolutiekeuring vroeg dat het USP per fase groeit. De vorm is nu door jou goedgekeurd, dus dit is alleen ter info.
3. **Rechte staartkolom:** de staart staat 11–14 rijen recht omhoog met evenwijdige randen. Dat klopt met de rechtopgehouden coati-staart (`foto4`) en leest op 1× goed, maar volgens de letter van de richtlijn is het een zuil. Alleen melden.
4. **Verre poten** zijn nauwelijks donkerder dan de nabije (ook gemeld in ronde 7). Eén tint omlaag op de verre achterpoot geeft meer diepte. Dat zou wel de helderheid raken, en jij wilde hem al donker.
5. **Bewaarde A/B-tests uit de SPEC** blijven open: bovenste vlek een tint terug, frons, bijna-witte klauwen, familiebrug in oudroze.

## Na het lezen van de eerdere keuringen

- De punten uit ronde 7 zijn opgelost:
  - R1 en R2, de 6 aan de schaduwkant van buik en dij, zijn nu 1;
  - R3, de glans op de buitenrand van de staande klauwen: de glans zit nu binnenin op (27,60);
  - R4, de rechte spijkerklauwen, is door Jordi's overtrek vervangen door kortere hangende haken.
- De punten uit ronde 2 zijn opgelost: oog, mond, helm-naad en de selout op staart en oren.
- **Verschil met ronde 7:** die keurder rekende de crème klauwrand als pseudo-omlijning. Ik niet, om twee redenen:
  - op licht en wit lossen K1 en K2 zichtbaar op;
  - ronde 2 keurde precies dit al af, en de goedgekeurde olinguito sluit zijn klauwen aan de lichtkant wel af.
- **Nieuw:** (28,61) a aan de onderkant van K4. K4 is pas in ronde 8 zo getekend.

## Eindoordeel: **BIJNA**

Hij leest als een coati en als een echte Dark-Pokémon, donkerder dan Linoone en Furret. Alle besluiten uit de SPEC zijn gehaald. Wat nog nodig is: alleen de 5 kleurpixels hierboven, zonder alphawijziging. Daarna is hij AF en kan hij naar `af/`.
