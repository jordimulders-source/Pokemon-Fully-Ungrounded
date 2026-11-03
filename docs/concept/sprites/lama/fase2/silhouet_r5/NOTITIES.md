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
