# Lama fase 2: silhouet ronde 5 (verse maker, 3 nov)

Bron: `direct.txt` (poppetje ronde 5, pose F "pas", 1178 px, box 40×62) + `onderlaag_256.png`. Met de hand gezet als spans per rij in `spans_ronde5.py` (elke rij staat er letterlijk in, per zone; geen morfologie of automatische vormen) → `ronde5.txt` / `ronde5_1x.png`.
Vel: `vel_ronde5.png` (`vel.py`): ronde 5 | direct | alpaca fase 1 | Flaaffy | Mareep | Girafarig | Ponyta op 4× en 1× (licht en groen) + ronde 5 als omtrek over het poppetje.
Controles: `controle.py` → `controle_uitvoer.txt`; korrels: `korrel.py` (overgenomen uit ronde 3) → `korrel_uitvoer.txt`.

**Resultaat:** 1408 px (1,38× fase 1 = 1019; SPEC 1100–1550), box 45×62 (y1–62), kop (incl. oren, y1–20) 20/62 = **32 %** van de hoogte (SPEC 30–35 %), 14 % van het oppervlak. Eén component, 0 losse px, 0 gaten, 0 px buiten de zones.

## Pose (FAKEMON_CHECKLIST §0)
- Pose: F "pas" van het poppetje (Jordi koos F), lijf horizontaal bijna zijaanzicht (foto 8), kop driekwart naar de kijker.
- Telgang (kameelachtige, uitzondering SPRITE_OPDRACHT §2): **nabije voorpoot én nabije achterpoot naar voren, verre voorpoot en verre achterpoot iets naar achteren**. Zo staan alle vier de poten op de grond, elk schuin in een eigen kolom (open A-vormen voor en achter, zoals Girafarig/Ponyta), in plaats van de "tafelpoten" van de bron.
- Skelet-sprites: Girafarig en Ponyta (poten, hak), Flaaffy en Mareep (wolomtrek).

## Zones (t.o.v. direct.txt)
| Zone | +px / −px | Max. afstand tot de bron | Wat |
|---|---|---|---|
| 1 kop (y0–20) | +36 / −2 | 1,4 px | Banaanoren zoals het poppetje: beide licht naar links hellend door de 3/4-draai, nabij oor bijna recht met smallere top, ver oor met de top naar binnen; breedst halverwege (kwast binnen de oorbreedte); 2 kolommen lucht ertussen (x19–21) tot de kruin. Ronde kruin en rond achterhoofd (x26 op y13–15), korte kop, stompe ronde snuit naar links-voor (x11, y15–17), ronde kin; geen sik. De onderlip is op 64 px geen silhouetvorm (een 1-px lipje = korrel) → komt in de kleur (mondlijn). |
| 2 hals (y21–27, x≤28) | +16 / −1 | 2,0 | **Kaarsrecht en verticaal** (achterrand x27 y22–26, voorrand x15–16); voor één zachte verbreding naar de halsbasis, achter een zachte nek-inham onder het achterhoofd (y17–18). |
| 5 halsband (y28–31, x≤24) | +1 / −1 | 1,0 | Ring steekt 1 px voor de hals uit (x14, y28–30), daaronder 2 rijen inham (y31–32): de band leest als ring. Pompons hangen binnen de borst (komen in de kleur). |
| 3 lijf + staart + aguayo (y21–43) | +67 / −20 | 5,0 (staart/romp achter, +2–3 px t.o.v. het poppetje) | Rug recht (lamarug, SPEC). **Aguayo = platte doek**, 1 rij boven de rug (y26 x30–38), geen bult/koffer. Staart als ronde pluim (y23–26) met een zachte inham (y28–29) naar de romp. Wol: borst één grote boog (x12, y36–38), achterwerk twee bogen (romp y30–37, wolbroek y40–45). Onderkant: één hangende buikboog (franje) y44 x32–37. |
| 4 poten (y44–62) | +229 / −95 | 6,1 (nabije achterpoot staat ±3–5 px naar voren t.o.v. het poppetje, voor lucht en telgang) | Zie pose. Alle poten ≥ 5 px breed, schuin, met zachte taper. Voorpoten: wolmouw bovenaan, ronde rode MMA-handschoen als bol (nabij 8×7 op de grond y62, ver 8×7 twee rijen hoger y60). Achterpoten: wolbroek (y44–45), nabije met hak naar achteren (y49–51, x47) en voet naar voren; verre schuin naar achteren met kleine voet (y59, hoger). |

## Korrels (`korrel.py`)
| | uitsteeksel-px | inkeping-px | tanden |
|---|---|---|---|
| direct (bron) | 6 | 6 | 11 |
| **ronde 5** | **0** | **0** | **0** |

Regel aangehouden: elke boog ≥ 2 rijen op zijn verste punt, elke inham ≥ 2 rijen hoog, lucht tussen poten altijd ≥ 2 kolommen (1 kolom lucht telt als inkeping-korrel).

## Controles
- **Lucht tussen de poten per rij** (zie `controle_uitvoer.txt`): vanaf y45/y46 tot de grond overal 2–11 kolommen tussen alle vier poten; vier aparte segmenten op y46–y59.
- **Voethoogtes:** nabije voor y62 (laagst), nabije achter y61, verre voor y60, verre achter y59 (4 hoogtes).
- **Rechte runs ≥ 4 px:** verticaal 31 (12×4, 9×5, 8×6, 1×7: binnenrand nabij oor); ter vergelijking Ponyta 12, Girafarig 10, Umbreon 16, maxima 6–12. Langste: oorbinnenranden (6–7, dunne oren), poten 6 (schuine benen in trappen van 4–6, zoals Ponyta). Horizontaal: aguayo-bovenkant 9 (platte doek, bewust), rug 6 (lamarug recht, SPEC), buikboog 6, hoefzool 6 (grondcontact).
- **Formaat:** 1408 px, groter dan fase 1 (1019) en tussen Ponyta (1291) en Girafarig (1517).

## SPRITE_OPDRACHT §0 / §2, punt voor punt
1. 3/4 naar links-voor: lijf bijna zijaanzicht volgens foto 8/Jordi, kop driekwart (beide oren zichtbaar, snuit links-voor). ok
2. Alles geteld en verbonden: 2 oren, kop, hals, staart, 4 poten, 2 handschoenen; 1 component. ok
3. Geen rechte lijnen waar het dier rond is: wol in bogen, poten schuin; resterende rechte stukken zijn rug/doek/zool (zie boven). ok
4. Ogen: n.v.t. (silhouet; oogvarianten in de kleurronde).
5. Leest op 1× als lama (vel, licht en groen): lange rechte hals, banaanoren, rechte rug met pluimstaart, lange poten. ok
6. Formaat vergeleken: zie boven. ok
7. Pose niet stijf: pas in telgang, poten niet evenwijdig, vier voethoogtes. ok
- Telgang: bewust (kameelachtige). ok
- Geen Escher: elke poot onder zijn eigen schouder/heup, nabije poten vóór de verre. ok
- Geen stokpoten: alle ≥ 5 px. ok
- Geen poten omhoog/opgetild, geen geknikte "gebroken" poot (AFGEKEURD). ok
- Geen korrel, niet golviger dan de schapen: 0 korrels; per onderdeel ≤ 2 bogen. ok
- Accessoires zoals het poppetje: halsband-ring, aguayo-doek, ronde handschoenen. ok
- Met de hand (spans per rij). ok

## Eerlijk: wat het silhouet (nog) niet kan dragen
- **Onderlip, pompons, oorkwasten en MMA-vorm (open vingers, nagels)** zitten binnen de omtrek; die moeten in de kleurronde leesbaar worden. In het silhouet zou elk daarvan een 1-px korrel zijn.
- **Lijf is in de kern een liggende rechthoek met ronde hoeken**: dat is de lama van foto 8 en het poppetje (rechte rug, SPEC). De zachte buik- en wolbogen breken de doos, maar de vorm blijft rustig, zoals gevraagd.
- **Nabije achterpoot staat 3–5 px vóór de poot van het poppetje** (anders geen eigen kolom met 2 px lucht en geen telgang-pas). Dit is de grootste afwijking van de bron.

## Lessen
- Toppen van beide oren naar elkaar toe ("( )") leest op 1× als lier/hoorns, net als in ronde 3; volg de 3/4-helling van het poppetje (beide oren licht dezelfde kant op, alleen het verre oor met de top naar binnen).
- 1 kolom lucht tussen poten telt als inkeping-korrel; plan altijd 2 kolommen, en begin het kruis met een leeg 2×2-blok.
- De bron had alle poten in 2 klonten (voor/achter); de telgang-pas (nabije poten vóór, verre achter) geeft vier eigen kolommen zonder poten op te tillen.
- Een lange rij "wolbogen" langs één rand (keel, halsband, borst) leest op 4× als golf; houd de hals glad en laat alleen halsband + één borstboog over.
- Een aguayo van 2 rijen hoog leest als bult (kameel); 1 rij platte doek is genoeg, de rest doet de kleur.
- Kalibreer "rechte runs" met echte sprites (Ponyta/Girafarig hebben 10–12 runs ≥ 4, maxima 6–7) in plaats van naar 0 te streven.

---

# Ronde 5b (zelfde maker, 3 nov): ronde wolmassa en Girafarig/Ponyta-poten

Claude-check op ronde 5: (1) de romp is een liggende doos, (2) de poten zijn paaltjes (5 px over de hele lengte). Akkoord en bevroren: kop, oren, hals, halsband, aguayo en de telgang-pas.
Bestanden: `spans_ronde5b.py` → `ronde5b.txt` / `ronde5b_1x.png`; vel `vel_ronde5b.png` (`vel5b.py`: ronde 5 | 5b | Girafarig | Ponyta | Mareep op 4× en 1× + 5b over het poppetje); `controle_uitvoer_5b.txt`, `korrel_uitvoer_5b.txt`.

**Resultaat:** 1361 px (1,34× fase 1; ronde 5: 1408), box 43×62, kop 32 % van de hoogte, 1 component, 0 losse px, 0 gaten.

## Bevriezing (pixeldiff, script in `spans_ronde5b.py`)
Rijen y0–30 worden letterlijk uit `ronde5.txt` gekopieerd. **Diff y0–30, x ≤ 31: 0 px.** Ook y0–30 over de hele breedte (staart, achterkant van de aguayo): 0 px.

## Zones (t.o.v. ronde 5)
| Zone | +px / −px | Wat |
|---|---|---|
| romp y31–45 | +13 / −20 | Borst als één bolle boog onder de halsband (x15 → x12 op y36–39 → x16), daarna een vloeiende overgang in de nabije voorpoot. Buiklijn licht bol: laagste punt x35–37 (y45). Hij krult op naar de poten, met een oksel achter de voorpoten (x31–32 leeg vanaf y43) en een lies vóór de achterpoot (x38–39 leeg op y45). Achterwerk als ronde boog (x53 op y32–35) die onder de bil naar de dij inspringt (x50 op y41–45). Er is geen rechte onderrand meer (y41–44 was 13–16 px recht). |
| poten y46–62 | +29 / −71 | Elke poot loopt breed uit de wol (5–6 px) en wordt naar beneden smaller: onderbeen 4 px. Nabije voorpoot: schuin naar voren met een zachte knie (y48, 6 px). Verre voorpoot: licht naar achteren met een knie op y50. Nabije achterpoot: hak naar achteren (x46, y49–50), onderbeen schuin naar voren tot de voet. Verre achterpoot: dij schuin naar achteren, hak x53 (y50–51), onderbeen licht naar voren. Handschoenen en voeten zijn ongewijzigd rond, de vier voethoogtes (y62, 61, 60, 59) blijven en de telgang ook. |

## Korrels en controles
- `korrel.py ronde5b.txt`: **0 uitsteeksel-px, 0 inkeping-px, 0 tanden.**
- Lucht tussen de poten: vanaf y46 vier aparte segmenten met 2–11 kolommen lucht (`controle_uitvoer_5b.txt`).
- Rechte verticale runs ≥ 4: 28 (ronde 5: 31), waarvan maar 3 van 6–7 px: twee oorbinnenranden (bevroren) en de achterrand van de verre voorpoot bij de aanzet (x29, y44–49). De langste stukken in de poten zijn nu 4–5 px; de rechte kolommen van x41 (7) en x49 (8) uit de eerste 5b-poging zijn weg. Horizontaal blijven aguayo (9, bevroren) en rug (6, SPEC) recht.

## Eerlijk: wat nog niet leest
- **Bovenkant romp:** de rug is recht (SPEC) en de hoek bij de staartaanzet ligt in de bevroren/ongewijzigde rijen y23–30. Daar zit de staartpluim, die de hoek rond maakt. Naast Mareep blijft de lama daardoor een langwerpige massa. Dat hoort bij een lama, maar hij is minder bol dan een schaap.
- **Onderbeen 4 px** (op verzoek, Girafarig/Ponyta). De SPRITE_NORM noemt ≥ 5–6 px. In de kleurronde moet de omlijning dan binnen die 4 px passen, met 2 px vacht.
- Onderlip, pompons, oorkwasten en MMA-details zitten nog steeds alleen in de kleur.

## Lessen (5b)
- Een poot "uit de wol" laten lopen gaat het best door de buiklijn naast de poot 1–2 rijen hoger te leggen (oksel/lies als leeg 2×2-blok) in plaats van de poot breder te maken.
- Een hak leest al met 1 px naar achteren over 2 rijen, als het onderbeen eronder 1 px per 2–3 rijen terugloopt. Een in-uit-in van 1 rij geeft meteen een tand.
- Bevriezen door rijen letterlijk uit de goedgekeurde tekst te kopiëren (`S[:31] = R5[:31]`) maakt de pixeldiff triviaal.

---

# Ronde 5c (zelfde maker, 3 nov): reparaties R1–R6 uit KEURING_5b.md

Precies de zes reparaties uit `KEURING_5b.md` / `keuring_5b_vel.png`. Ze staan met de hand als losse pixelwijzigingen in `spans_ronde5c.py`, toegepast op `ronde5b.txt`, met als uitvoer `ronde5c.txt` / `ronde5c_1x.png`. Vel: `vel_ronde5c.png` (`vel5c.py`: 5b | 5c | Mareep | Girafarig | Ponyta op 4× en 1× + 5c over het poppetje). Controles: `controle_uitvoer_5c.txt`, `korrel_uitvoer_5c.txt`.

**Resultaat:** 1388 px (1,36× fase 1), box 43×62, kop 32 %. `korrel.py`: **0 / 0 / 0**. 1 component, 0 losse px, 0 gaten.

## Kosten per reparatie (budget ±53: +40 / −13)
| Reparatie | Werkelijk |
|---|---|
| R1 rug oplopend schoft → kruis (y24–26) | +25 / −0 |
| R2 deuk onder de staart weg (y28–29 x52) | +2 / −0 |
| R3 buik als één boog (y43 x31–32 erbij, y45 x35–37 eraf) | +2 / −3 |
| R4 nabije onderbenen 5 px (voor y51/53/54, achter y53–56) | +7 / −0 |
| R5 achtervoeten hoeven (nabij x38–43, ver x47–51) | +0 / −6 |
| R6 handschoenen op de grond (nabije zool 6, verre 7 breed met platte zool) | +4 / −4 |
| **Totaal** | **+40 / −13** (precies het budget) |

## Bevriezingsdiff (t.o.v. ronde5b.txt)
- Kop, oren, hals en halsband (x ≤ 27, y0–30): **0 px**.
- x ≤ 31, y0–30: **2 px**, namelijk y26 x28–29. Dat is de inkeping bij de schoft die R1 volgens de keuring moet vullen ("y26: x28–29 … erbij"). Hij ligt tussen de halsachterrand (x27) en de rug, niet in de hals zelf. Als Claude x28–31 strikt bevroren wil, blijft er een dip van 2 px bij de schoft.
- Buiten de zones van R1–R6: **0 px**.

## Toets op 1× (vel)
- **R1:** de bovenrand loopt in drie lange treden op (y26 x28–33, y25 x34–41, y24 x42–51). Op 1× leest dat als een licht oplopende rug naar een hoog kruis, **zonder bult of kameel**: er is geen top in het midden, het hoogste punt is het kruis. De doos is weg omdat boven- en onderlijn niet meer evenwijdig lopen.
- **R5/R6:** alleen de voorpoten staan op (rode) handschoenen. De achterpoten eindigen in smalle hoeven, zoals op het poppetje. De handschoenen staan plat op de grond; de verre is kleiner dan de nabije.
- **R3/R4:** de buik loopt in één boog van voor- naar achterpoot. De nabije poten zijn 5 px en de hak van de nabije achterpoot leest lager (y53–56).

## Eerlijk: wat nog niet leest
- **Staartpluim:** na R1 is de staart alleen nog een koepel van 1 rij (y23 x48–50) op het kruis. Op 1× zie je een hoog achterwerk, maar geen staart als eigen vorm. Een opstaande pluim kost 2–3 rijen boven y23 en is een nieuw kenmerk. Dat staat bij de keurder als smaakvraag voor Jordi.
- De rug is oplopend, niet vlak zoals foto 8: dat is de smaakkeuze van de keurder (advies: oplopend), Jordi beslist.
- Formaat 1,36× fase 1 (D5 1,5–1,7×), door de slanke lama binnen 62 px hoogte.
- Onderlip, pompons, oorkwasten, aguayo en MMA-vorm zitten alleen in de kleur.

## Lessen (5c)
- `korrel.py` vangt geen golf van stukken die elk ≥ 2 px breed zijn (plateau + dip + koepel + deuk). Kijk ook naar de bovenrand als reeks treden: een lijn die alleen oploopt of alleen daalt, is glad.
- Een reparatielijst als (y, x0, x1, ±) in een script maakt de kosten per reparatie en de diff buiten de zones meteen bewijsbaar.

---

# Ronde 5d (zelfde maker, 3 nov): 5c met de staartpluim terug

Jordi (letterlijk): "5b ok want c eheft opeens geen staart meer" en "als c nu gewoon een staart zou hebben, zou die het beste zijn".
De staart staat met de hand als spans in `spans_ronde5d.py`, toegepast op `ronde5c.txt`, met als uitvoer `ronde5d.txt` / `ronde5d_1x.png`. Vel: `vel_ronde5d.png` (`vel5d.py`: 5b | 5c | 5d op 4× en 1× + 5d over het poppetje). Controles: `controle_uitvoer_5d.txt`, `korrel_uitvoer_5d.txt`.

**Resultaat:** 1415 px (1,39× fase 1), box 43×62, kop 32 %. `korrel.py`: **0 / 0 / 0**. 1 component, 0 losse px, 0 gaten.

## Staartzone en diff
- **Zone y19–24, x47–53: +27 / −0 px.** Per rij: y19 x49–51, y20 x48–52, y21–23 x47–53, y24 x47–52 (staartvoet op het kruis).
- Diff buiten de staartzone t.o.v. `ronde5c.txt`: **0 px**. Kop/oren/hals/halsband (x ≤ 27, y0–30): **0 px**.

## Vorm
- Een ronde koepel van 5 rijen die boven het kruis opstaat (top y19, 5 rijen boven de rug op y24) en licht naar achteren helt (breedst x47–53 op y21–23, 1 px voorbij de staartaanzet). Het is net als in 5b een eigen vorm, nu op de hoge achterkant van 5c.
- **Aansluiting:** de oplopende rug van 5c (y26 → y25 → y24, x28–46) loopt ongewijzigd door tot de staartvoet (x47). De staart rijst daar in één keer op: geen dip in de rug en geen bult ervoor. De holle hoek tussen rug en staart (x46, y23) is 2×2 leeg, dus geen korrel.
- Op 1× (vel, licht en groen) leest de staart als opstaande pluim, net als in 5b. Tegelijk blijven de oplopende rug, de buikboog, de hoeven en de handschoenen van 5c staan.

## Eerlijk
- Onder de staart loopt de achterrand op x52 recht van y24 tot y31 (8 rijen), daarna volgt de rompboog (x53). Een inham daar was in 5b de "deuk" die de keurder als golf afkeurde (R2). Deze rechte rand heb ik daarom bewust laten staan.
- Onderlip, pompons, oorkwasten, aguayo en MMA-vorm zitten alleen in de kleur. Formaat 1,39× fase 1 (D5 vraagt 1,5–1,7×).

## Les (5d)
- Bij een oplopende rug moet de staart een eigen vorm boven het kruis zijn (minstens 4–5 rijen hoog). Een koepel van 1 rij gaat op in het kruis en leest niet meer als staart. Na een reparatie aan de bovenlijn altijd nakijken of de kenmerken die daar uitsteken (staart, oren) nog op 1× lezen.

---

# Ronde 5e (zelfde maker, 3 nov): kop driekwart

Jordi (letterlijk): "ik twijfel of de pose van het hoofd nu nog goed genoeg is, verder lijkt het wel oke ondanks dat het anders is dan het model". Claude's diagnose: in 5d staan de oren kaarsrecht en evenwijdig midden op een symmetrische kop, wat leest als frontaal of als een konijn.
Alleen de kopzone (y0–21) is opnieuw met de hand gezet in `spans_ronde5e.py`, toegepast op `ronde5d.txt`, met als uitvoer `ronde5e.txt` / `ronde5e_1x.png`. Vel: `vel_ronde5e.png` (`vel5e.py`): alleen 5e op 4× en 1×, 5e over het poppetje, de kop 8× naast de poppetjeskop (+ omtrek erover) en de 1×-toets naast Girafarig, Ponyta, Rapidash en Stantler. Controles: `controle_uitvoer_5e.txt`, `korrel_uitvoer_5e.txt`.

**Resultaat:** 1422 px, box 43×62, kop 32 % van de hoogte (16 % van het oppervlak). `korrel.py`: **0 / 0 / 0**. 1 component, 0 losse px, 0 gaten.

## Kopzone en diff
- **Kopzone y0–21: +46 / −39 px.** Vanaf y22 (hals, halsband, lijf, staart, poten): **0 px diff** met `ronde5d.txt`.
- Max. afstand tot de bron (`direct.txt`): nabij oor 2,0 px, ver oor 3,2 px, schedel + snuit 3,2 px (de 3,2 zit in het achterhoofd, dat bewust langer is; de snuit is gelijk aan 5d).

## Wat er veranderde
- **Oren:** banaanoren die vanaf de bovenkant/achterkant van de schedel naar achteren/rechts hellen, in een smalle V met 2–4 kolommen lucht ertussen.
  - Het nabije oor loopt van de voet x17–19 (y9) naar de top x20–21 (y1).
  - Het verre oor begint lager (top y2) en schuiner, van de voet x22–25 (y9) naar de top x26–27.
  - Beide oren zijn breedst halverwege (kwast binnen de oorbreedte) en buigen niet naar elkaar toe, dus geen lier.
  - Een eerste poging met het verre oor tot x28 (top y3) week 4 px af van het poppetje en gaf een te wijde V. Die heb ik teruggezet naar de helling van het poppetje.
- **Schedel:** 1–2 px langer naar achteren (x28 op y13–16). Het achterhoofd loopt via een zachte nek (x26, y18–20) door in de achterrand van de hals (x27). De kop is daardoor niet meer symmetrisch rond de oren.
- **Snuit:** ongewijzigd, stomp naar links-voor (x11, y15–17), ronde kin, geen sik. De onderlip komt in de kleur.

## Toets op 1× (vel)
- Naast Girafarig, Ponyta, Rapidash en Stantler leest de kop nu driekwart: de oren staan schuin achter op de kop, de snuit wijst naar links en de schedel loopt door in de hals. Je ziet geen konijnenoren meer midden boven op de kop.
- De 8×-kop naast de poppetjeskop heeft dezelfde opbouw: oren in een V boven/achter, snuit links, achterhoofd naar de hals.

## Eerlijk
- Het voorhoofd is nog steeds een rechte trap van 45° (y10 x16 → y15 x11), zoals in het poppetje en eerder door de keurder geaccepteerd.
- De kop is 1–2 px langer naar achteren dan het poppetje, zoals gevraagd.
- Onderlip, oorkwasten, oog en neusgaten zitten alleen in de kleur.

## Les (5e)
- Driekwart lees je op 1× vooral aan de oren: als ze evenwijdig en recht boven het midden van de kop staan, oogt de kop frontaal (konijn). Laat ze in een V naar achteren hellen, met het verre oor lager en schuiner, en verleng het achterhoofd tot in de hals. Een te wijde V wijkt van het poppetje af en wordt een gewei.

---

# Ronde 5f (zelfde maker, 3 nov): kop overgetrokken van het goedgekeurde poppetje

Jordi (letterlijk, over 5e): "ja en de kop is dus niet goed want die is anders". De opdracht was overtrekken, niet zelf ontwerpen. Daarom heb ik de kop van 5e (mijn eigen V-oren en verlengde schedel) volledig losgelaten.
- **Werkwijze:** `kop_dekking.py` rendert het poppetje opnieuw met dezelfde pose en camera als `bron.py` (fase2_r4('F_pas', head_yaw=55), yaw 8, pitch 8, fill 0.99; alfa intern op 768 = 12× per 64-pixel). Het drukt per 64-pixel van de kopzone de dekking in tienden af en bewaart de alfa in `kop_alpha.npy`.
- **Spans:** in `spans_ronde5f.py` heb ik elke rij met de hand gezet op de 0,5-grens van die dekking. Uitvoer: `ronde5f.txt` / `ronde5f_1x.png`.
- **Vel:** `vel_ronde5f.png` (`vel5f.py`), met alleen 5f op 4× en 1×, 5f over het poppetje, en de kop 8× naast de poppetjeskop met de 5f-omtrek erover.

**Resultaat:** 1363 px (1,34× fase 1), box 42×62, kop 32 % van de hoogte (12 % van het oppervlak: de kleine lamakop van het poppetje). `korrel.py`: **0 / 0 / 0**. 1 component, 0 losse px, 0 gaten.

## Diff
- Kopzone y0–21: +19 / −78 px t.o.v. 5e. Vanaf y22: **0 px diff** met `ronde5e.txt`.

## Afstand tot de omtrek van het poppetje (op 64, 0,5-grens van de dekking)
| Onderdeel | Rijen | Afwijkende px | Max. afstand | Reden |
|---|---|---|---|---|
| Oor nabij | y1–9 | 3 (y1 x18 weg, y9 x19 erbij, 1 grens-px) | 1,0 | Een top van 1 px op y1 is een korrel, dus de top begint op y2 (2 breed). |
| Oor ver | y1–9 | 4 (y2 x21 erbij, y6 x22 erbij, y9 x21 weg, 1 grens-px) | 1,0 | Een top van 1 px en een tand in de binnenrand zijn korrels; met y9 x21 weg blijven er 2 kolommen lucht tussen de oorvoeten. |
| Kruin / voorhoofd | y10–13 | 0 | 0,0 | |
| Snuit (bult naar voren-onder) | y14–18 | 0 | 0,0 | |
| Kaak / onderlip + aansluiting hals | y19–21 | 1 (y21 x26 erbij) | 1,0 | Aansluiting op de bevroren hals (y22 x16–27). |

Geen enkele afwijking is groter dan 1 px. Oorhoek, oorlengte en oorbreedte (de kwast valt binnen de oorbreedte) volgen het poppetje, net als de ronde kruin, de snuitbult, de kaak met onderlip (y19 x14–15) en de nek.

## Eerlijk
- De hals vanaf y22 is bevroren uit ronde 5 en is aan de achterkant 1–2 px breder dan de hals van het poppetje (x27 tegenover x25–26). Onder de kop staat daardoor een trapje van 1 px achter (y20 x24 → y21 x26 → y22 x27). Dat valt buiten de kopzone; om het weg te halen moet de hals vrijgegeven worden.
- De kop is kleiner dan in 5b–5e (165 px tegenover ±220). Dat is de maat van het poppetje.

## Les (5f)
- "Overtrekken" betekent: render het poppetje opnieuw en zet de spans op de dekkingsgrens, met alleen afwijkingen van ≤ 1 px voor korrels of lucht. Elk eigen "verbeteren" van de pose (de V-oren in 5e) is een nieuwe interpretatie die Jordi afkeurt.
