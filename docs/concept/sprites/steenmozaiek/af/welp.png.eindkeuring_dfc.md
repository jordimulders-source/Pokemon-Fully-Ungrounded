# Eindkeuring welp c10_1 (Dragonfly Cave + Gen 3)

Gekeurd: `welp_c10_1.png` (greige, normaal) en `welp_c10_1_grijs.png` (zelfde pixels, ander palet; bewezen identiek). Alleen uitvoering; ontwerp (pose, silhouet, voluten, koplijnen, halve cirkel naast het oog, kleuren) is bevroren en niet gekeurd.
Vergeleken op 1× (wit en gras), 2× en 4×/8× naast Growlithe, Regirock, Golem, Claydol en Skitty (`anim_front_gba.png`).

## Eindoordeel: **PASS** (5 MOET-pixels, allemaal rand of losse pixel; geen vormwerk)
Blind op 1× leest hij meteen als een zittende katachtige welp van steen die zijn poot likt; de tong is het eerste wat je ziet, de voluten op schouder en dij lezen als gegraveerde spiralen. Naast Regirock en Golem past hij qua contrast en steenkarakter; hij oogt niet als fanwerk. Omlijning is overal 1 px en gesloten, met een gekleurde selout (index 2) aan de lichtkant en zwart (1) aan de schaduwkant, 56% zwart (Gen 3: 45–68%). Licht komt van linksboven (kop links licht 5, rechts 3; dij bovenop 14, rechterrand 2). Wat overblijft zijn twee open randpixels, één plek waar zwart en selout om en om lopen, en twee losse lichte pixels aan een schaduwkant.

## Meting
| Meting | Resultaat |
|---|---|
| Formaat / modus | 64×64, palet (P), index 0 = transparant (255,0,255) |
| Kleuren | 14 in gebruik + transparant (6/7/8 lila-restjes: 6 alleen als pupil, 7/8 ongebruikt) |
| Steen (luma) | 1 (26) · 2 (77) · 3 (116) · 4 (152) · 5 (187) · 14 (216) → stappen 51/39/36/35/29 (Taillow-orde) |
| Tong / tanden / oog | 15 (123) 12 (166) 13 (195) · 10 (249) 9 (208) 11 (204) · pupil 6 (95) |
| Grijs-palet | 27/77/118/153/188/218: zelfde stappen, kleurgroepen gelijk |
| Box | x7–56, y18–62 (50×45), horizontaal midden 31,5, onderkant y62: gecentreerd en onderaan |
| Buitenrand | 169 px: 95× index 1, 72× index 2, **2× een vlakkleur (open rand)** |
| Lichtkant (transparant boven/links) | 71× 2, 33× 1 (de 1-en zitten op de rugdiagonaal en onderkant poot: terecht) |
| Schaduwkant | 62× 1, 1× 2 (18,39), 1× 3 (open rand, zie MOET 2) |
| Om en om 1/2 op de rand | 1 plek: (8,33)=1 · (9,34)=2 · (10,35)=1 · (10,36)=2 |
| Echt losse pixels (geen 8-buur gelijk) | 38; vrijwel alle zijn graveerwerk (lichte rand naast een groef, spiraalkernen (27,52) (33,52) (29,53)), oogdetails en tanden: toegestaan. Afwijkend: zie MOET 4–5 en MAG 1 |
| Oppervlak | 1244 px (zie ter info) |

## Per eis
| Eis | Oordeel |
|---|---|
| Buitenlijn 1 px, gesloten | PASS na MOET 1–2 |
| Selout aan lichtkant, geen zwart/kleur om en om | PASS na MOET 3 |
| Binnenlijnen (groeven, oor, mond, poot/lijf-overlap) | PASS: 1 px, in 2, taps; overlap poot/lijf in 1 (37,49–50) |
| Tinten per kleurgroep | PASS: 3/4/5 + glans 14 + groef 2 |
| Contrast / stappen | PASS (29–51 per stap) |
| Licht linksboven, consequent | PASS na MOET 4–5 |
| Geen pillow shading / banding | PASS: de diagonale 5-2-5-band op de opgeheven voorarm (15–18, 47–49) is een gegraveerde band, geen banding |
| Korrels / losse pixels | PASS na MOET 4–5 (rest = graveerwerk) |
| Jaggies | PASS: rug 1:1-diagonaal schoon, spiralen hoekig (Chavín, ontwerp) |
| Leesbaarheid 1× | PASS (wit en gras) |
| ≤16 kleuren, index 0 transparant, 64×64, onderaan gecentreerd | PASS |

## MOET (index op `welp_c10_1.png`; geldt identiek voor `_grijs`)
1. **(16,20) 4 → 2.** Open rand: vlaktint direct tegen de lucht in de inkeping tussen het nabije oor en de kruin ((16,19) is transparant). Met 2 loopt de selout door van (15,19) naar (17,19).
2. **(22,49) 3 → 1.** Open rand aan de schaduwkant (rechts) van de opgeheven voorarm, tegen de lucht bij (23,49). Sluit aan op 1 bij (23,48) en (22,50).
3. **(9,34) 2 → 1.** Snuitvoorkant loopt nu zwart-selout-zwart-selout: (8,33)=1, (9,34)=2, (10,35)=1, (10,36)=2. Met 1 is de onderkant van neus/bovenlip één zwart stuk tot de mondlijn; daaronder blijft de onderkaak selout 2 (één overgang, bij de mond, zoals Gen 3).
4. **(14,46) 5 → 3.** Losse lichtste-tint-pixel tussen groeven (2) aan de onderkant van de opgeheven poot (schaduwkant); ligt niet op een gegraveerde band. Sluit aan op 3 bij (15,46) en (14,47).
5. **(21,50) 5 → 3.** Losse lichte pixel op de rechteronderhoek van de voorarm, tussen zwart (22,50)/(21,51) en groef (20,50): schaduwhoek. Sluit aan op 3 bij (21,49).

Gecontroleerd in een kladversie (niet in de repo): na deze 5 pixels geen nieuwe open randen, geen nieuwe losse pixels; het beeld verandert op 1× vrijwel niet, op 8× is de rand dicht en de poot-onderkant rustig.

## MAG
1. **(20,37) 1 → 2.** Los zwart puntje in de mondhoek, alleen aan 2/3 grenzend; met 2 vormt het één tapse mondhoeklijn met (21,37), (19,38), (20,38). Op 1× leest het nu als een gaatje.
2. **Pupil nabije oog (20,27) index 6** is een lila restkleur (113,86,97); in het grijze palet staat hij er ook nog in. Kan naar 2 of 1 als dat beter bij de steen past (paletkeuze, geen fout).
3. **Binnenoor ver oor (26–27, 21–22) index 1:** pure zwart in het oor leest op 1× als gat; 2 zou zachter zijn. Alleen als het model dat toelaat (model: donkerder bruin, geen zwart).
4. Tong is omlijnd met greige 2 (10,37–40); een donkerroze (15) zou Gen 3-achtiger zijn langs het lichte roze. Klein.

## Ter info voor Jordi (ontwerp, niet nodig voor PASS)
- **Formaat:** 1244 px voor een fase 1 (norm 700–950, box ±36–42; hier 50×45), en de volwassen steenjaguar is 1552 px: de welp is maar 1,25× zo klein (bij Gen 3 groeit een 2-fasenlijn ±1,5–2×). Silhouet is bevroren; alleen melden.
- De gegraveerde voluten geven veel 1–2-pixelstukjes (groef + lichte rand). Dat is het bedoelde Chavín-reliëf en leest op 1× goed; wie "rustiger" wil, moet de voluten groter of minder maken: ontwerpkeuze.
- Palet heeft nog 2 ongebruikte slots (7, 8) en een bijna-ongebruikte (6, 1 px): ruimte voor een latere kleurvariant.
