# Olinguito finale: onafhankelijke keuring (24 okt)

Gekeurd: `finale/anim_front.png` (frame 1 en 2). Eigen oordeel eerst gevormd; de KEURING.md van de maker pas daarna gelezen. Coördinatoraanvullingen verwerkt: Jordi "ik zie nu al dat er een been mist" en de nieuwe regel "wat de maker zelf zwak noemt is automatisch fail".

Coördinaten: x/y in het 64×64-frame 1 (frame 2: kop/romp/staartwortel 1 px hoger, poten 1 rij langer; dezelfde fouten).
Vellen in `keuring_onafh/`: `vergelijking.png` (1× en 3× tussen 16 echte fase-1-sprites), `vs_ronde23_linoone.png`, `foutzones.png` (genummerde zones), `1x_2x_3x.png`, `f1_8x.png`, `f2_8x.png`, uitsneden met raster `kop.png`, `voorpoten.png`, `achterpoten_staart.png`, `romp.png`.

## Metingen
| Meting | Olinguito | Norm / echte |
|---|---|---|
| Oppervlak | 936 (f2: 971) | fase 1: 700–950 |
| Box | 50×33 | ±40×40; Poochyena 40×40, Shinx 43×32, Growlithe 42×41 |
| Kophoogte / totale hoogte | 20/33 = **61 %** (oortop y22 t/m kin y41) | fase 1 40–55 %, sjabloon ±45–50 % |
| Soliditeit | 0,71 | 0,65–0,80 |
| Symmetrie | 0,50 | < 0,80 |
| Donkere pixels (shape.py, luma < 55) | **0,53** | Poochyena 0,20, Purrloin 0,29, Nickit 0,32, Litten 0,45 (hoogste Dark-referentie) |
| Ingesloten gaten | 36 px (lus x45–53, y39–45) + 2 losse gaatjes (24,44) en (13,52) | echte: meestal 0 |
| Open randen (vachtkleur naast transparant) | **13 px**, alle in de klauwen (index 9 grijs): (24,45) (13,48) (14,48) (12,49) (25,49) (11,50) (25,50) (10,51) (24,51) (10,52) (14,52) (13,53) (13,54) | 0 |
| Gezicht y29–40 vs ronde 23 | pixeldiff 0 (rij 41 anders: kinknip) | bevroren |

Poten op pixelniveau: verre voorpoot x15–22 (tint 3) met klauwen x10–17 tot y54; nabije voorpoot x27–33 (tint 4/5) y41–48, klauwen x22–29 tot y52; nabije achterpoot x37–45 tot y53; **verre achterpoot = strook `4331` x45–48, y48–52, 3 px vacht**, direct tegen de nabije achterpoot (geen lucht) en van boven vastgegroeid aan de onderkant van de staarthaak (y46–47), niet aan de heup.

## Tabel
| # | Punt | Oordeel | Meting / bewijs |
|---|---|---|---|
| §0 | Pose-sjabloon (P3 laag sluipend, Dark) | pass | pose leest als sluiper |
| A1 | Silhouet leest als de soort | pass | 1×: lage marter/neusbeer |
| A2 | Dominant kenmerk breekt de omtrek | **fail** | J-staart breekt de omtrek, maar de haak sluit zich op de achterpoot: op 1× een **O-lus**, geen hangende J |
| A3 | Diagonale compositie | pass | kop linksboven, staart rechts |
| A4 | Negatieve ruimte | **fail** | soliditeit 0,71 ok, maar geen lucht tussen nabije en verre achterpoot, lus dicht, tussen de voorpoten alleen een gaatje van 1 px (24,44) |
| A5 | Niet symmetrisch | pass | 0,50 |
| A6 | Geen bouwblokken | **fail** | verre voorpoot x16–21 y41–48 is een blok van 6×8 met evenwijdige randen (zuil > 6 px) |
| B1 | Kop draait meer dan lijf | pass | |
| B2 | Lange snuit → één oog, neus links | pass | neus x9 |
| B3 | Twee ogen perspectief | n.v.t. | één oog |
| B4 | Snuit één vorm | pass | bevroren, ronde 23 |
| B5 | Oren volgen de draai | pass | verre oor hoger |
| B6 | Kop overlapt lijf | pass | |
| B7 | Gezicht compleet | pass | |
| C1 | Alles geteld | **fail** | 4e poot staat technisch in de pixels maar leest op 1× niet (Jordi: "er mist een been") |
| C2 | 4 kolommen, 3–4 voethoogtes, lucht | **fail** | verre voorpoot is de **laagste** (y54) en verre achterpoot plakt aan de nabije (0 kolommen lucht); op 1× 3 voetkolommen |
| C3 | Elk ledemaat onder eigen schouder/heup | **fail** | verre achterpoot hangt aan de staarthaak (y46–47), heupzone x45–50 y39–45 is leeg (gat) |
| C4 | Gewrichten | **fail** | verre voorpoot en verre achterpoot rechte stokken zonder knik |
| C5 | Ledematen groeien uit de romp | **fail** | verre achterpoot groeit uit de staart |
| C6 | Nabij ≠ ver | **fail** | verre voorpoot langer (13 rijen) en lager dan de nabije (8 rijen + klauw) |
| C7 | Eén houding met gewicht | pass | |
| C8 | Staart sluit aan en buigt | **fail** | aansluiting ok, maar haak raakt poot (lus dicht); maker: hangende strook 2 rijen korter en 3 px hoger dan goedgekeurd |
| C9 | Pose past bij karakter | pass | |
| D1 | Oppervlak 700–950 | pass | 936 (f2 971: **fail** voor frame 2, > 950) |
| D2 | Kop 40–55 % van de hoogte | **fail** | 61 % |
| D3 | Compacte romp | pass | |
| D4 | Breedte ≤ 48 | **fail** | 50 (maker noemt het zelf zwak) |
| E1 | Verre kant donkerder | **fail** | verre oor heeft de lichtste binnenkant (tint 8) en is groter dan het nabije (bevroren deel; zie Moet nog 10) |
| E2 | Overlap met omlijning | pass | |
| E3 | Omlijningsdonkerte | **fail** | 0,53, boven elke Dark-referentie (Litten 0,45); op 1× een donkere vlek waarin alleen het oog leest |
| §2 | Lijf en blik 3/4 links-voor | pass | |
| §2 | Eén oog, snuit één vorm | pass | |
| §2 | Alles verbonden, geen poten aan elkaar | **fail** | verre achterpoot vast aan nabije achterpoot én staart |
| §2 | Diagonaal lopen, geen telgang | pass | verre voor + nabije achter vóór, nabije voor + verre achter achter |
| §2 | Pose niet stijf, geen Escher | pass | |
| §2 | Lijf natuurlijk, geen doos | **fail** | verre voorpoot blok (A6) |
| §2 | Formaat fase 1, kop niet te groot | **fail** | kop 61 % (Jordi's "kop te groot" niet opgelost) |
| §2 | Kenmerken lezen op 1× | **fail** | klauwen lezen op 1× als grijze krassen/vorkjes; 4e poot leest niet |
| §2 | Geen rechte lijnen | **fail** | elke klauw is een rechte 45°-streep; achterhoofd x33–34 y28–34 vrijwel verticaal (33-33-34-34-33-33-33) |
| §2 | Ogen geïntegreerd | pass | |
| §2 | Omlijning, geen open randen | **fail** | 13 open randpixels in de klauwen (maker meldt ze als gerepareerd: niet waar) + 2 losse gaatjes |
| §2 | Kleuren passend bij Dark | pass | palet zelf ok; probleem is de waardeverdeling (E3) |
| §2 | Goedgekeurd blijft letterlijk staan | **fail** | schedel platter, nabije oor 2 px dichter bij het verre oor, J-staart korter/hoger dan ronde 23 (maker noemt alle drie zelf zwak) |
| §2 | Met de hand | pass | |
| AFG | r17/r18/r19: neus, grijns, masker, beige vlak | pass | gezicht diff 0 met ronde 23, geen nieuwe crème |
| AFG | "achterpoot helemaal rechts bevalt steeds minder" | **fail** | verre achterpoot staat weer helemaal rechts, onder de staart |
| AFG | 21/21b telgang, verre voorpoot onder de kin (Linoone) | pass | |
| AFG | 22: dunne rechte poot | **fail** | verre achterpoot 3 px brede rechte strook |
| AFG | herbouw: klauwen als streepjes/vlekjes | **fail** | twee rechte streepjes per poot, geen Sandslash-haak |
| CH | Misvormd gezicht / opgeplakt oog / zwevende wenkbrauw / beige vlak | pass | bevroren gezicht |
| CH | Escher-poten / telgang | pass | |
| CH | Losse/zwevende delen | **fail** | verre achterpoot hangt aan de staart |
| CH | Dunne of rechte stokpoten | **fail** | verre achterpoot, verre voorpoot |
| CH | Klauwen als streepjes/klodders/harken | **fail** | harkjes |
| CH | Te grote kop | **fail** | 61 % |
| CH | Rechte lijnen | **fail** | klauwen, achterhoofd |
| CH | Symmetrie | pass | |
| CH | Poten niet aan het lijf | **fail** | verre achterpoot |
| CH | Verre ledematen ontbreken | **fail** | 4e poot leest niet |
| 5 | Officiële Dark-starter? | **fail** | zie eindvraag |

## Eindvraag
`vergelijking.png`: tussen Poochyena, Zigzagoon, Growlithe, Eevee, Vulpix, Skitty, Meowth, Sentret, Shinx, Purrloin, Nickit, Cyndaquil, Totodile, Charmander, Chimchar en Litten valt hij op 1× op als **de enige zonder leesbare poten en gezicht**. Iedere echte toont vier (of twee) duidelijke voeten met lucht ertussen, een licht gezicht met contrast en een kop van hooguit ±55 % van de hoogte. De olinguito is een donkerbruine lage vlek, met als enige lichte delen het oog, een crème streep en grijze krassen onder de kin; de staart leest als een ring. Op 3× is het een nette fan-sprite van een marter, maar geen starter: de starters (ook de Dark-achtige Litten en de sluwe Nickit/Purrloin) hebben een open, leesbare kop en heldere voeten. **Nee**, een fan zou zonder uitleg niet denken dat dit een officiële Dark-starter fase 1 is; eerder een fanmade routepokémon.

## Moet nog (op ernst)
1. **Vierde poot leest niet (Jordi: "er mist een been")** – zone x45–51, y39–53. Haal de strook `4331` (x45–48, y48–52) weg. Teken de verre achterpoot opnieuw als eigen poot onder de verre heup: dij x45–50 y40–46 in tint 3 (68,44,38) met één lichtpixel tint 4 linksboven, omlijning 2 waar hij achter de nabije dij ligt (E2); onderbeen x47–50 y47–51 met hak naar achteren (x50–51, y47–48); voet x46–51 y51–52 met teenscheiding, onderkant **1 rij hoger** dan de nabije achterpoot (y53). Vachtbreedte minstens 4 px, geen rechte strook. **Minstens 1 kolom lucht (x45–46) van y48 tot de grond** tussen nabije en verre achterpoot, zoals bij Poochyena/Growlithe/Shinx, waar alle vier de voeten als losse stompjes op de grond staan.
2. **Staart: lus dicht, korter/hoger dan goedgekeurd** – zone x45–58, y38–53. Laat de haak niet terugkrullen naar x46 (haakpunt `122/2552/25541`, x47–51 y43–45, eruit). Verleng de hangende strook rechts (x54–57) weer met 2 rijen (zoals ronde 23) tot ±y50, en laat de haak onderaan open naar linksboven krullen (x51–56, y49–53), met minstens 1 kolom lucht tussen haakpunt en de nieuwe verre voet. Resultaat: een open J die hangt, geen O.
3. **Klauwen zijn harkjes en hebben open randen** – zones x10–17 y48–54 (ver) en x22–30 y45–52 (nabij). Per poot 2 Sandslash-klauwen: elke klauw 3 px breed aan de wortel, 4–5 px lang, **gebogen** (wortel bijna horizontaal, punt omlaag/naar binnen), lichaam wit/C met A als schaduw aan de onderkant, omlijning 1 aan de schaduwkant en onderkant, 9 alleen op de lichte bovenrand die tegen de poot ligt. Klauwen beginnen aan een zichtbare pootrand (knokkelrij in tint 3/4), niet midden in het lijf (de nabije klauwen beginnen nu op y45, boven de pootonderkant). Nul vachtkleur/9 naast transparant. Toets op 1× naast Sandslash/Sneasel: "klauwen", geen "vork".
4. **Verre voorpoot langer en lager dan de nabije, en een blok** – zone x15–23 y40–54. Verre voorpoot 1–2 rijen hoger eindigen dan de nabije (klauwen onderkant y52 i.p.v. y54) en de nabije voorpoot (x27–33) 2 rijen verlengen zodat zijn klauwen op y54 eindigen (nabij = laagst). Geef de verre voorpoot een knik (pols iets naar voren, x16–17 y47–49) en laat de rechterrand x22 schuin weglopen zodat de 6×8-zuil verdwijnt. Minstens 1 kolom lucht tussen de twee voorpoten onder y46 (nu alleen gaatje (24,44)).
5. **Kop 61 % van de hoogte (kop te groot)** – niet oplossen door de kop te knippen of te schalen (dat maakte de schedel plat, zie 6). Maak de rest groter: alle vier poten 2–3 rijen langer (box ±50×36, kop ±55 %), wat punten 1 en 4 meteen lucht geeft. Oppervlak komt dan ±990–1010: boven 950, maar AFGEKEURD.md zegt "vorm gaat vóór pixelgrenzen". Vraag Jordi expliciet of dat mag.
6. **Schedel platter en oren dichter bij elkaar dan goedgekeurd** – zone x14–36 y21–28. Zet de bovenkant van de kop van ronde 23 terug (pixeldiff 0, knippen/plakken): schedelboog tussen de oren op y22–23, nabije oor terug op zijn ronde-23-afstand (oorafstand 9 px i.p.v. 7).
7. **Achterhoofd recht** – x33–34 y28–34: met punt 6 komt de ronde-23-boog terug; anders als boog 32-33-34-34-34-33-32.
8. **Donker: aandeel 0,53** – vooral de tint-1/2-massa in romp, achterpoten en staart. Verlicht de bovenkant van rug, dij en staart met tint 5/6 (licht linksboven), houd 1 alleen aan de schaduwkant en tussen overlappende delen; doel ≤ 0,45 (Litten). Gezicht niet aanraken.
9. **Twee losse gaatjes** (24,44) en (13,52): dichten met omlijning of openen tot echte lucht (vervalt grotendeels met punten 3 en 4).
10. **Breedte 50 > 48 en frame 2 971 px > 950** – volgt uit 1, 2 en 5; laat Jordi kiezen (zie 5). Verre oor heeft de lichtste binnenkant (E1): bevroren deel, alleen met toestemming van Jordi 2–3 px tint 8 → 6.

## Wat de maker ten onrechte goedkeurde
- "Open randen aan de klauwhaken gedicht": er staan er nog 13.
- "Eindvraag: ja": op 1× tussen de echte valt hij juist af door de onleesbare poten en het donkere geheel.
- De vier punten onder "Eerlijk: het zwakst" zijn volgens de nieuwe regel allemaal fails (punten 1, 2, 6, 10).

## Eindoordeel
**AFGEKEURD.** 33 fails in de tabel (veel overlappend), waarvan 8 zwaar: vierde poot leest niet en hangt aan de staart, staart sluit tot een O, klauwen zijn harkjes met open randen, verre voorpoot langer/lager dan de nabije, kop 61 %, schedel/oren/staart wijken af van het goedgekeurde ronde 23.
