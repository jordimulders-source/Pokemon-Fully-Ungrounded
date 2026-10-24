# Olinguito finale: eindkeuring (24 okt)

Keurder = de spriter zelf, zo streng mogelijk, alsof hij moet afkeuren. Maatstaf: `FAKEMON_CHECKLIST.md` (A–E), `SPRITING.md` §0–§8, `SPRITE_OPDRACHT.md` §2–3, `olinguito/AFGEKEURD.md`, `ronde23/OORDEEL_VORMSTUDIE.md`, plus de Chernobyl-lijst uit de opdracht.

**Bewijs:** `bron/check_uitvoer.txt` (metingen), `bron/keuring/` (uitsneden 14× per onderdeel, beide frames 7×, vel met 15 echte fase-1-sprites op 1× en 3×), `compare.png` (finale f1/f2, ronde 23, Poochyena, Zigzagoon, Cyndaquil, Growlithe, Nickit, Purrloin op 3× en 1×).

## Metingen
| | Ronde 23 | Finale f1 | Maatstaf |
|---|---|---|---|
| Oppervlak | 1045 | **936** | fase 1: 700–950 (D1) |
| Box | 48×36 | 50×33 | fase 1 ±36–42; ≤ 48 breed (D4, R) |
| Kopaandeel (kopvak neuspunt–achterhoofd, oortop–kin) | 44 % (31×20) | **39 %** (26×19) | snuitdieren 3/4 met één oog: 25–41 %, mediaan 34 %; OORDEEL-doel 38–39 % |
| Kophoogte / totale hoogte | 56 % | 58 % | Poochyena 55, Vulpix 57, Growlithe 61, mediaan van 13 refs 62 (D2) |
| Soliditeit | 0,76 | 0,71 | 0,65–0,80 (A4) |
| Symmetrie | 0,57 | 0,50 | < 0,80 (A5) |
| Donkere pixels | 0,52 | 0,53 | E3: hoger mag bij Dark; Mightyena 0,58, Houndour 0,46, Zorua 0,41 |
| Open randen / losse delen / rechte omtrekstukken ≥ 5 / regelmatige trappen ≥ 5 | 0 / 1 deel / 4 / – | **0 / 1 deel / 0 / 0** (beide frames) | 0 |
| Gezicht (neus, snuit, masker, oog, boogje, grijns, verre oor) | – | **diff 0** | bevroren |
| Nabije oor | – | **diff 0** (als geheel 2 px naar links) | bevroren vorm |
| PNG | | P-modus, 64×128, 2 frames, transparency 0, palet = `ronde23/normal.pal` | |

## A. Silhouet en kenmerk
| # | Oordeel | Toelichting |
|---|---|---|
| A1 H silhouet leest als de soort | **pass** | Op 1× in de rij met 15 echte sprites: laag gemaskerd wasbeerdier met lange haakstaart en witte klauwen (olinguito/coati). |
| A2 H dominant kenmerk breekt de omtrek | **pass** | J-staart rechts (stijgt nu boven de rug uit en hangt in een haak); klauwen als tweede kenmerk vooraan, beide op 1× als vorm te lezen. |
| A3 H diagonale compositie | **pass** | Kop linksboven, massa naar rechtsonder, staartwortel als tegenwicht rechtsboven (in ronde 23 lag die onder de ruglijn). |
| A4 H negatieve ruimte | **pass** | 0,71; lucht onder de buik (boog), tussen dij en staart, binnen de J, tussen de klauwen. |
| A5 H niet symmetrisch | **pass** | 0,50. |
| A6 R geen bouwblokken | **pass** | Geen rechte rand ≥ 5; rug in stukken van 4 (schouder, zadel, staartwortel). |

## B. 3/4-constructie en gezicht
| # | Oordeel | Toelichting |
|---|---|---|
| B1 H kop meer naar de kijker dan het lijf | **pass** | Ongewijzigd uit ronde 23 (kop 3/4 met één oog, lijf bijna profiel). |
| B2 H snuitlengte → één oog | **pass** | Lange snuit, één oog, neus is het meest linkse punt. |
| B3 H twee ogen = perspectief | n.v.t. | Eén oog. |
| B4 H snuit één vorm | **pass** | Ongewijzigd. |
| B5 R oren volgen de draai | **pass** | Verre oor (links) kleiner, nabije oor groter op de achterhoek van de schedel (zoals Poochyena). |
| B6 H kop overlapt het lijf | **pass** | Kop vóór de borst; nek alleen als ondiepe nekkuil; kop/nek-lijn met wangbolling (kop blijft een apart onderdeel, Jordi's Linoone-nuance). |
| B7 H gezicht compleet | **pass** | Oog, neus, mond/grijns met tandje. |

## C. Pose en ledematen
| # | Oordeel | Toelichting |
|---|---|---|
| C1 H alles geteld | **pass** | 4 poten (verre achterpoot nieuw), 2 oren, 1 oog, 2 klauwen per voorpoot, 1 staart. |
| C2 H 4 kolommen, 3–4 voethoogtes | **pass** (met Jordi's spec) | Voeten op y51/52 (nabije voor, opgetild), y52–54 (verre voor op zijn klauwen), y53 (verre achter), y54 (nabije achter); overal lucht of omlijning ertussen. De letterlijke C2-regel "nabije voorpoot het meest links" wijkt af omdat Jordi de Galar-Linoone-configuratie voorschreef (verre voorpoot vooraan onder de kin). |
| C3 H elk ledemaat onder zijn schouder/heup | **pass** | Verre voorpoot onder de kin, nabije onder de schouder, nabije achter onder de dij, verre achter rechts erachter onder het kruis. Geen verre poot vóór de nabije op dezelfde plek. |
| C4 H gewrichten | **pass** | Nabije achterpoot: knie voor, hak naar achteren, middenvoet weer naar voren. Nabije voorpoot: elleboog achter, onderarm in een boog naar de pols. |
| C5 H ledematen groeien uit de romp | **pass** | Dij als bolling, voorpoten uit borst/schouder, geen T-aansluiting. |
| C6 H nabij ≠ ver | **pass** | Verre poten donkerder (schaduwtint), kleiner zichtbaar, andere hoek; verre klauwen grijs, nabije wit. |
| C7 H één houding met gewicht | **pass** | Sluipende stap: drie poten dragen, nabije voorpoot opgetild met hangende klauwen. **Diagonaal:** verre voor + nabije achter vooruit, nabije voor + verre achter achteruit; geen telgang. |
| C8 R staart sluit aan en buigt | **pass** | Begint boven op het kruis, boog omhoog, hangt, haak terug. |
| C9 R pose past bij het karakter | **pass** | P3 sluipend/laag (Dark, kruimeldief): kop vooruit, klauwen voorop. |

## D. Verhoudingen en formaat
| # | Oordeel | Toelichting |
|---|---|---|
| D1 H oppervlak fase 1 | **pass** | 936 px (frame 2 971: ademhalingsframe). |
| D2 H kop per fase | **pass** | 58 % van de hoogte; binnen de echte snuitdieren (55–69 %). Het OORDEEL-punt "kop te lang" opgelost: schedel 26 i.p.v. 31 px, kopaandeel 39 % i.p.v. 44 %. |
| D3 H compacte romp | **pass** | Romp ±14 px lang en ±12 hoog achter de kop; poten kort en stomp (twee kenmerkloze rijen uit de poten geknipt). |
| D4 R breedte ≤ 48 | **afwijking met reden** | 50 px door de lange haakstaart. Lage lange fase-1-soorten liggen ook daarboven: Nickit 51, Zigzagoon 56, Yungoos 61. Smaller kan alleen door de staart tegen de dij te drukken (lus dicht) of de staart in te korten. |
| D5 R groei binnen de lijn | n.v.t. | Nog geen fase 2. |

## E. Omlijning, shading en kleur
| # | Oordeel | Toelichting |
|---|---|---|
| E1 R verre kant donkerder | **pass** | Verre poten in 3 met omlijning 2/1. |
| E2 R overlap met omlijning | **pass** | Klauw A over de verre voorpoot met grijze lichtzijde-omlijning; nabije achterpoot over de verre met omlijning; dij/staart gescheiden door lucht. |
| E3 R donkerte | **pass** | 0,53, binnen de Dark-band (Mightyena 0,58); palet is goedgekeurd. |

## SPRITING.md §0 en §1–§8
| Punt | Oordeel |
|---|---|
| §0.1 lijf en blik diagonaal | pass (ongewijzigd uit ronde 23) |
| §0.2 alles geteld en verbonden | pass (1 verbonden deel, 4 poten) |
| §0.3 geen rechte lijnen | pass (geen omtrekstuk ≥ 5, geen regelmatige trap ≥ 5; onderarm en kop/nek-lijn rechtgetrokken stukken vervangen door bogen) |
| §0.4 ogen geïntegreerd | pass (oog ongewijzigd: donker bovenlid, iris, glans) |
| §0.5 silhouet op 1× | pass |
| §0.6 formaat | pass (936) |
| §0.7 pose niet stijf | pass |
| §1 met de hand | pass: elke pixel staat in `bron/kop.txt`, `achterlijf.txt`, `klauwen.txt`, `naden_f*.txt` of is een knip/plak van ronde 23 (gezicht, oor, staart); geen vormfuncties |
| §3 curven | pass: klauwen hebben punten (toegestaan bij klauwen), verder geen spijkertjes |
| §5 licht linksboven | pass: hooglicht op schouder, dij, staartwortel; schaduw onder |
| §8 omlijning per kleurgroep | pass: vacht 2/1, klauwen 9 (licht) / 1 (schaduw), 1 px breed, geen open randen |

## SPRITE_OPDRACHT §2 (Jordi's vaste feedback)
| Punt | Oordeel |
|---|---|
| Lijf en blik 3/4 | pass |
| Eén oog, snuit één vorm | pass |
| Alles verbonden, geen geamputeerde verre kant, geen poten aan elkaar | pass (verre achterpoot toegevoegd; alle poten met omlijning of lucht gescheiden) |
| Diagonaal, nooit telgang | pass (zie C7; het OORDEEL-voorstel "verre achterpoot tussen de poten" bewust niet gevolgd omdat dat telgang gaf) |
| Pose niet stijf, geen Escher | pass |
| Over een echte sprite als skelet | pass (ronde 23 op Galar-Linoone; achterpoot op Nickit/Mightyena gecontroleerd) |
| Formaat fase 1, kop niet te groot | pass (936 px, kop 39 %) |
| Kenmerken op 1× | pass (staart, klauwen, masker, oog) |
| Geen rechte lijnen, ogen niet opgeplakt, omlijning, licht linksboven | pass |
| Kleur zoals Dark-soorten | pass (palet ongewijzigd) |
| Goedgekeurd blijft letterlijk staan | pass voor gezicht, verre oor (diff 0), nabije oor (diff 0, verschoven), J-staart (zelfde pixels; zie zwakke punten). Klauwen bewust opnieuw (opdracht: geen klodders) met behoud van 2 Sandslash-klauwen per voorpoot. |
| Met de hand, geen automatische vormen | pass |

## AFGEKEURD.md
| Afgekeurd | Hier |
|---|---|
| r17 neus/grijns/kaak verschoven | niet aangeraakt (diff 0) |
| r18 alleen het neusje | n.v.t. |
| r19 kop herschaald, oren veranderd, beige vlak, masker kleiner | geen herschaling: alleen kenmerkloze vachtstroken weggeknipt (één schedelrij, twee schedelkolommen achter het masker); oren en masker pixel-identiek; geen nieuw crème/beige |
| r12 babystarter-herschaling | nee |
| 21/21b verre voorpoot naar achteren, telgang | verre voorpoot blijft vooraan (Linoone); diagonale gang |
| 22 dunne rechte poot | alle poten ≥ 6 px (verre achterpoot is maar deels zichtbaar, ±4–5 px, achter de nabije) en met knik |
| herbouw: klauwen als dunne streepjes/vlekjes | haken met een witte kern van 2–4 px en eigen omlijning, 5–7 rijen lang |
| Linoone-nuance: kop apart onderdeel | ja, eigen omtrek en kop/nek-lijn |

## Chernobyl-checks
| Check | Oordeel |
|---|---|
| Misvormd gezicht | pass (gezicht pixel-identiek aan ronde 23) |
| Escher-poten | pass |
| Telgang | pass |
| Losse of zwevende delen | pass (1 component; frame 2 ook; voeten in beide frames op dezelfde grond) |
| Dunne/rechte stokpoten | pass |
| Klauwen als streepjes of klodders | pass (in ronde 23 waren het klodders: nu haken) |
| Beige vlakken uit het niets | pass |
| Zwevende wenkbrauw | pass (boogje ligt op de maskerrand, ongewijzigd) |
| Opgeplakte ogen | pass |
| Te grote kop | pass (39 %, was 44 %) |
| Symmetrie | pass (0,50) |
| Rechte lijnen | pass |

## Per onderdeel op 14× (vast aan het lijf? rechte lijn? dikte? diagonaal? bevroren diff? AFGEKEURD?)
| Onderdeel | Oordeel |
|---|---|
| Kop | pass: achterhoofd als boog (32-33-33-34-34-33-33), oor op de achterhoek, wangbolling naar de nek |
| Oog | pass: diff 0 |
| Masker + boogje | pass: diff 0 |
| Oren | pass: verre diff 0; nabije diff 0 (2 px naar links), steekt 1 px over de schedelachterkant zoals een oor op de achterhoek |
| Snuit, neus | pass: diff 0 |
| Mond/grijns | pass: diff 0 |
| Verre voorpoot | pass: vast in de borst, 7–8 px, gebogen voorrand, voet met klauwen C/D |
| Nabije voorpoot | pass: vast in de schouder, 8–9 px, elleboog achter, onderarm in een boog, pols met klauwen A/B |
| Nabije achterpoot | pass: dij als bolling met hooglicht, knie–hak–voet, 7–8 px, voet met teenscheiding |
| Verre achterpoot | pass: vast onder het kruis (bovenkant achter de staartkrul en de nabije poot), lichte voorrand, voet 1 hoger met teenscheiding |
| Klauw A (nabij voor) | pass: wortel 4 wit, haak naar links-onder, punt omlaag, ligt over de verre poot met omlijning |
| Klauw B (nabij achter) | pass: wortel 3, korter, apart van A (lucht vanaf rij 50) |
| Klauw C (ver voor) | pass: grijs, wortel 3, punt op de grond |
| Klauw D (ver achter) | pass: grijs, kleiner, onder de voet, apart van C |
| Staart | pass: zelfde pixels als ronde 23; wortel boven de rug, hangt, haak met lichte punt; 2 px lucht tot de dij |
| Romp | pass: schouder–zadel–staartwortel, buikboog, compact |
| Frame 2 | pass: kop, romp, staartwortel 1 px hoger, poten en hangende staart 1 rij langer, voeten op dezelfde plek; gezicht diff 0 |

## Naast echte fase-1-sprites (1× en 3×)
Vel `bron/keuring/vel_15_echte_*.png`: Poochyena, Zigzagoon, Growlithe, Eevee, Vulpix, Skitty, Meowth, Sentret, Shinx, Purrloin, Nickit, Cyndaquil, Totodile, Charmander, Chimchar. De olinguito heeft hetzelfde visuele gewicht als Poochyena/Nickit/Zigzagoon, valt niet op als groter of donkerder dan Mightyena-achtige Dark-soorten, en heeft net als de echte één leesbaar kenmerk (staart) plus een tweede (klauwen). Vraag "zou een fan zonder uitleg denken dat dit een officiële Dark-starter fase 1 is?": **ja**, als laag sluipend Dark-dier in de stijl van de Gen 4–9-sprites in de expansion; minder knuffelig-frontaal dan Cyndaquil/Totodile, maar in de lijn van Litten/Sprigatito (sluw, halfdichte blik), wat bij een kruimeldief past.

## Wat Jordi als volgende zou kunnen zien
Per onderdeel gezocht naar wat nog in geen lijst stond; wat ik vond en hoe het is opgelost:
1. **Kop "korter" maar niet kleiner**: na alleen het achterhoofd te verplaatsen was het kopaandeel nog 42 % (de pootknip maakte het lijf kleiner). Opgelost met twee kenmerkloze schedelkolommen + oor mee naar links → 39 %.
2. **Achterkant van de kop werd een rechte verticale rand** (na stap 1) → weer een boogje.
3. **Kop/nek-lijn als rechte zwarte streep van 6 px** → wangbolling.
4. **Onderarm nabije voorpoot recht (7 px)**: in ronde 23 al zo, viel nog nergens op → boog naar de elleboog.
5. **Verre achterpoot op de OORDEEL-plek gaf telgang** (verre voor én verre achter vooruit) → rechts achter de nabije gezet.
6. **Eerste schedelknip haalde de onderste rij van het verre oor weg** ("oren veranderd") → andere rij geknipt; oren nu diff 0.
7. **J-krul raakte de dij** (staart las als gesloten lus) → staart 2 px naar rechts, dij-achterkant 1–2 px kleiner: 2 px lucht.
8. **Klauwen eerst te dun en lang (hark/vork)** → dikker aan de wortel, korter, punt omlaag.
9. **Open randen aan de onderkant van de klauwhaken** (pixel `a` naast transparant) → `11` waar de haak versmalt.
10. **Rechte voetzool verre achterpoot (5 px)** en **rechte buikrand** → teenscheiding en buikboog.
11. **Frame 2 brak de J-krul op de naad** → frame 2 uit dezelfde tekening.
Na deze reparaties kan ik per onderdeel (kop, oog, masker, oren, snuit, mond, vier poten, vier klauwen, staart, romp, frame 2) geen volgend afkeurpunt meer vinden dat binnen de opdracht op te lossen is.

## Eerlijk: het zwakst
- **Staart:** zelfde pixels, maar de hangende strook is 2 rijen korter (frame 2: 1) en de hele staart hangt 3 px hoger dan in ronde 23 (nodig voor de verre achterpoot). Jordi kan zeggen dat de J "anders hangt".
- **Verre achterpoot:** zoals gevraagd licht in beeld (±20 px, onder de staartkrul); op 1× leest hij eerder als donkere diepte dan als duidelijke vierde poot.
- **Kop:** 2 kolommen korter en 1 rij lager. De kenmerken zijn pixel-identiek, maar het nabije oor staat 2 px dichter bij het verre oor en de schedel is iets platter dan in ronde 23.
- **D4:** 50 px breed (R-richtlijn ≤ 48), door de staart.
