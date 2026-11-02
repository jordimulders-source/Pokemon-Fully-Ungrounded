# Lama fase 2: silhouet ronde 1 (maker-agent, 2 nov)

Bron: `direct.txt` (onderlaag direct verkleind, 1092 px, box 42×60). Reparatie met de hand in vijf benoemde zones;
elke zone staat als getypt tekstraster in `repareer.py` en vervangt alleen zijn eigen rechthoek. Vel: `vel_ronde1.png` (`vel.py`).

**Resultaat:** `ronde1.txt` / `ronde1_1x.png`: **1177 px, box 43×60** (x 11–53, y 3–62; voeten op rij 61–62), kop (oortop r3 t/m kin r23) 21/60 = **35%**. Groter dan fase 1 (1019), slank zoals de bron.

## Per zone (diff t.o.v. `direct.txt`, uit `repareer.py`)
| Zone | Rechthoek | + / − | Wat |
|---|---|---|---|
| A voorpoten | x18–36, y41–62 | +79 / −40 | Het blok van rij 50–58 gesplitst. **Nabije voorpoot opgetild:** dij schuin naar voren, knie vooruit (r46–47, x20), pols smaller (r49–50), MMA-handschoen als ronde bal r50–56 (x19–27, 9 breed), vrij van de grond (onderkant r56, 6 rijen boven de grond). **Verre dragende voorpoot:** eigen kolom x30–34 (5 px), handschoen op de grond r57–62. Lucht: 2 kolommen (x28–29) van r44 tot r56; de V begint als 1 px op r43 (aanzet aan de borst). Handschoen-ballen raken elkaar niet (ook niet diagonaal). |
| B achterpoten | x39–54, y41–62 | +69 / −29 | Eén kolom van 8–10 px werd twee poten van 5 px. **Nabij** (rechts, lager): dij x47–52, **hak** naar achteren r49–51 (x53), onderbeen 1 px naar voren eronder, voet r60–61 x46–51 (= voet van de bron). **Ver** (links, hoger): x41–45, knik onder de hak (r53) 1 px naar voren, voet met tenen naar voren r58–59 (1 rij hoger dan de bron: perspectief). Inkeping vanaf r45, 2 kolommen lucht vanaf r47. Ruimte onder de buik (x35–40) blijft leeg. |
| C oren | x11–22, y2–8 | +2 / −3 | Het nabije oor was een knop op een steeltje (4 breed bovenaan, 2 breed op r7: las als voelspriet/hoorntje). Nu een blad: punt r3, breedst r5–6 (kwast), 3 breed bij de aanzet. Verre oor: punt 2 breed. V ertussen 3–4 px breed, sluit pas op r8. |
| D snuit | x10–19, y13–23 | +6 / −2 | Bobbel van het verre oog (r14–15, x11) weg: lange snuit = één oog. Neus steekt 1 px naar voren-onder (r19–21, x11), ronde kin r22–23 (x12–15) die 3–5 px over de keel hangt; keelinkeping x16–17 → kop leest als eigen onderdeel boven de hals. |
| E wol | x52, y31–33 | +3 / 0 | Eén wolbobbel op het achterwerk, breekt de rechte rand van r28–36. Rug (aguayo) en halsband niet aangeraakt. |

**Buiten de zones gewijzigd: 0 px** (eis ±1; `python3 repareer.py` print het bewijs).

Controle 1-px-spleten/diagonale aanrakingen (script): alleen de toppen van de V's (oor-V r8, voorpoot-V r43, achterpoot-V r45–46), daarna minstens 2 px lucht. Geen losse pixels, geen diagonale aanrakingen.

## Eigen keuring (overlay op de onderlaag, 4× en 1× naast Mightyena/Girafarig/Rapidash/Stantler/Absol)
- **Pose:** gelijk aan de bron: lijf 3/4 naar links-voor, kop rechtop met de snuit naar de kijker, staart omhoog, opgetilde nabije voorpoot. Kop, hals, romp, staart: 0 px gewijzigd buiten de zones.
- **Massa:** +85 px (+8%), allemaal in de poten (poten ≥ 5 px i.p.v. 3–4). In de overlay: de opgetilde voorpoot ligt 1–2 px vóór de bron (knie naar voren, handschoen 2 px naar links) om lucht te maken naar de dragende poot; de verre achterpoot onderaan 1–2 px naar voren; nabije achtervoet valt op de bronvoet.
- **1×:** vier poten in vier kolommen, de handschoen als bal vóór de borst, twee oren, kop met snuit boven een lange hals. Leest als een slanke langnek-viervoeter naast Girafarig/Stantler; slanker en rustiger dan de referenties, wat past bij "slungelige tiener".
- **Telgang/diagonaal:** kameelachtige, uitzondering mag; de stand is staand met één poot opgetild, dus niet van belang.

## Vragen voor Claude (geen zwakke punten van het silhouet, maar afwijkingen tussen opdracht en bron)
- **Oren:** de opdracht zegt "plat naar achteren", maar de bron (onderlaag/poppetje) heeft de oren rechtop, licht naar achteren. Ik heb de bron gevolgd (massa heilig) en alleen de vorm leesbaar gemaakt. Moeten ze echt plat, dan is dat een poppetje-/bronwijziging, geen silhouetreparatie.
- **Kop laag en naar voren:** in de bron staat de kop hoog op een bijna rechte hals (snuit naar beneden/naar de kijker). Niet verplaatst; dat zou de bron veranderen.

## Lessen
- Een tekstraster per zone in het reparatiescript (rechthoek vervangen) maakt de diff per zone en "0 buiten de zones" vanzelf bewijsbaar.
- Twee poten uit één verkleind blok halen kost breedte (5 + 2 lucht + 5 = 12 px): neem die ruimte uit de lege buikruimte (verre poot iets naar voren), niet door poten dunner te maken.
- Een knop-op-steeltje-oor (smal bij r7, breed erboven) leest op 1× als voelspriet; een blad (breedst in het midden, smal bij punt) leest als oor.
- Kijk in de overlay welke bronpoot dichtbij is (lager op het scherm = dichtbij); de voet van de nabije poot op de bronvoet laten vallen houdt de stand eerlijk.


# Ronde 1b (2 nov): achterpoten en omtrek van het lijf

Claude: A (voorpoten), C (oren) en D (snuit) akkoord en **bevroren**; oren en kop volgen de bron (Jordi keurde het plaatje van het poppetje, niet de beschrijving "plat"/"laag"). Terug: B (achterpoten, "paaltjes"; Jordi bij de alpaca: "alpaca's achterpoten zijn iets te recht") en nieuw E2 (omtrek rug/achterwerk/borst/buik: bijna een rechthoek). Ronde 1b = `ronde1.txt` + `ZONES_1B` in `repareer.py` (`python3 repareer.py ronde1b`); vel: `vel.py ronde1b ronde1` (ronde 1 op 4× ernaast).

**Resultaat:** `ronde1b.txt` / `ronde1b_1x.png`: **1188 px, box 44×60** (x 11–54, y 3–62), kop 35% (onveranderd).

## Diff (t.o.v. ronde1, uit `repareer.py ronde1b`)
| Zone | Rechthoek | + / − | Wat |
|---|---|---|---|
| B achterpoten | x37–54, y41–62 | +28 / −30 | Geen paaltjes meer. De dij zit in de wolmassa: de buiklijn loopt schuin (voorrand 38 → 39 → 40 op r41–44) over in het been, geen rechte kolom vanaf de buik. **Nabij:** voorrand 47 → 48 → 49 (dij schuin naar achteren), holte boven de hak (achterrand 49 op r42–43), **hak steekt naar achteren** (x54, r50–51), onderbeen schuin naar voren (voorrand 49 → 48 → 47 → 46 → 45) tot de voet x45–50 r60–61 (= voet van de bron). **Ver:** dezelfde "<" kleiner en hoger: hak x46 r50–51, onderbeen naar voren, voet x39–44 r57–58 (3 rijen hoger dan de nabije). Overal 5–6 px dik, ≥ 2 px lucht (vanaf r45 direct 2), ruimte onder de buik x35–39 leeg. |
| E2 rug+staart | x32–54, y20–24 | +11 / −5 | **Staart als pluim:** bol bovenaan (r21–23, 4 breed), punt naar achteren, smalle aanzet (x50–51, r24), los van de rug door een inkeping ervoor. Wolpluk op de schoft (x36–37) en bolling van de aguayo (x44–45); rij 25 (rugrand onder de aguayo) ongewijzigd. |
| E2 achterwerk | x50–54, y25–40 | +6 / 0 | Twee wolplukken van 2 rijen (r27–28, r32–33) met dalen ertussen (r29–30, r34–37), daarna de rand van de bron (50) naar de dij. Geen enkele-pixelpieken (een eerste poging met 1-rij-pieken las op 4× als zaagtand; weggehaald). |
| E2 borst | x19–23, y26–40 | +2 / −1 | Wolpluk onder de halsband (r35–36, x20) met een dal erboven (r33–34). |
| Buik | (in B) | | Buiklijn rond: van de dragende voorpoot via r40 schuin omlaag naar de dij (r41–44). |

- **Bevroren A, C, D: 0 px verschil met ronde1. Buiten de zones: 0 px t.o.v. ronde1 en t.o.v. direct.**
- **Massa van de bron:** lijf (r20–40) 549 → 565 px = **+2,9%** (binnen ±3%; plukken gecompenseerd met dalen). Totaal +11 t.o.v. ronde1.
- Script-check: geen losse pixels, geen enkele-pixeluitsteeksels, geen diagonale aanrakingen; 1-px-spleten alleen in de top van de oor-V (r8) en de voorpoot-V (r43, bevroren). Rechte randruns in het lijf ≤ 4 rijen (de 4 zijn de achterrand van de dij net boven de holte).

## Eigen keuring ronde 1b (4× en 1×/3× naast Girafarig en Stantler)
- Achterpoten lezen nu als lama-achterpoten: dij uit de wol, hak naar achteren, onderbeen schuin naar voren; de verre poot is duidelijk de kleinere/hogere. Geen twee identieke paaltjes meer.
- Omtrek: achterwerk en borst wollig met rustige plukken, staart leest als pluim; de rug blijft vrij recht (lama: "rug recht", aguayo erop) met twee kleine plukken.
- Pose en massa liggen in de overlay op de bron; de nabije achtervoet valt op de bronvoet.
- Ik zie op dit moment geen zwak punt in de zones die ik mocht raken. De hals blijft een rechte, dikke kolom (zoals de bron, buiten mijn zones).

## Lessen (ronde 1b)
- Wolplukken in een silhouet: 2 rijen breed met een dal ernaast; enkele-rijpieken van 1 px lezen op 4× als zaagtand/ruis.
- Plukken toevoegen zonder massa te winnen: elk uitsteeksel compenseren met een dal ernaast (lijf bleef binnen +3%).
- Een achterpoot die geen paaltje is: voorrand schuin terug (dij), achterrand met een holte boven een hak die 1–2 px uitsteekt, onderbeen schuin naar voren; de verre poot dezelfde "<" kleiner en hoger. Zo blijft er ruimte voor 2 px lucht zonder de poten dunner te maken.
