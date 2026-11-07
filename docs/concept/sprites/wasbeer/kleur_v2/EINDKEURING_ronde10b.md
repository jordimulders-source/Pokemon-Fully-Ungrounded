# Eindkeuring ronde 10b (verse keurder, 3 nov): eindversie

Te keuren: `ronde10b.png` (met pupil, Jordi's keuze: "10b met pupil, laat de eindkeurder deze keuren, voor de allerlaatste afwerking"), met `ronde10b.txt`, `ronde10.pal` en `vel_ronde10.png`. Vergeleken op 1x/2x/12x/16x/18x, licht en donker, met 13 echte sprites (frame 1 + normal.pal: Zigzagoon, Linoone, Mightyena, Raticate, Teddiursa, Ursaring, Zangoose, Sneasel, Weavile, Furret, Sentret, Absol, Gumshoos) en met de lijn (fase1_olinguito, fase2_coathief). Ook naast 9b gelegd. Eerst zelf geoordeeld, daarna `NOTITIES_ronde10.md` en `KEURING_ronde8.md` gelezen. Mijn keuring van ronde 9 (`EINDKEURING_ronde9.md`) is hierin verwerkt.

Coördinaten (x, y), 0-geteld; paletindex als hexteken (1 zwart, 2 masker, 3 lichtgrijs, 4–7 grijsbruin donker→licht, 8 oker, 9/a crème, b/c/d buidel, e/f oog).

**Uitslag: bijna klaar.** 2 van 10 punten FAIL, op te lossen met 8 pixels kleur, zonder silhouetwijziging. Daarna is hij klaar als eindversie, zonder nieuwe ontwerpronde. De drie punten van Jordi voor ronde 10 zijn alle drie goed opgelost: neus, staarthaak en de lijn op de klauw.

| # | Punt | Uitslag |
|---|---|---|
| 1 | Alpha, open randen, losse pixels | **PASS** |
| 2 | Staartpunt | **PASS** |
| 3 | Ogen + omgeving | **PASS** (pupil = Jordi's keuze) |
| 4 | Oren | **FAIL** (1 px, verre oor) |
| 5 | Lijf links tussen arm en kop | **PASS** (rechte silhouetrand: voor Jordi) |
| 6 | Neus | **PASS** |
| 7 | Shading en omlijning overal | **FAIL** (dubbele zwarte lijn poot/staart) |
| 8 | Leesbaarheid 1x | **PASS** |
| 9 | Past in de lijn | **PASS** |
| 10 | Geen afgekeurde dingen terug | **PASS** |

## 1. Alpha, open randen, losse pixels: PASS
- Alpha-diff met `direct_s1a.txt`: 23 px, allemaal in de vrijgegeven zones.
  - Neus: (10,16), (9,17) en (10,18) erbij.
  - Staart: (57,20–21), (48,21–22) en x 58 op y 22–28 erbij; (52,24–26), (51–52,27–28) en (49–50,29) weg.
  - Daarbuiten: 0. De png komt overeen met de txt. 1687 px.
- Open randen: **0**. De randpixels zijn allemaal 1/2/4/b/c; de `c` is de bruine selout aan de lichtkant van de klauw en de buidel.
- Losse pixels (geen 8-buur in dezelfde kleur, zwart niet meegeteld): **27 = 16 per 1000 px**. Ter vergelijking: Mightyena 19, Zigzagoon 28, Raticate 32, Teddiursa 61, Linoone 63, Sneasel 71. Ze zijn functioneel: glans, oog, selout. Er zijn geen willekeurige vlekken meer.

## 2. Staartpunt: PASS
- De haak heeft nu echt lucht: een spleet van 1 px (x 52, y 24–26), die linksonder breder wordt en open uitkomt (49–52, 27–29).
- De hangende punt (x 49–50) heeft een lichte kant 5 links en 4 rechts, met een eigen zwarte rand langs de spleet. De koepel heeft een lichte boog linksboven. De ring in de bocht heeft glans (55,24) linksboven en oker 8 rechtsonder.
- Op 2x leest hij als vraagteken-haak; op 1x net. Veel beter dan 9b, waar de haak dicht was. Dit is de "vertaling uit het 3D-model" die Jordi vroeg.

## 3. Ogen: PASS
- Nabij oog: lid 1111 / e-a-e / f-1-f / 2-f-2. Donker boven, licht onder, glans en pupil. Op 2x en 1x leest het als een levendig, ietwat fel Pokémon-oog. Dat past bij Dark.
- In ronde 9 rekende ik de gecentreerde glans en de 3 px brede pupil als FAIL. De pupil is nu Jordi's keuze, en met pupil leest de gecentreerde glans als glans boven de pupil. Geen FAIL meer.
- Optioneel, alleen als Jordi het wil (het raakt het oog dat hij koos): glans naar linksboven, (20,11) e→a en (21,11) a→e, zoals Zigzagoon en Linoone.
- Rond het oog is het netjes: wenkbrauwboog, twee maskerlobben met een brug, een gladde maskerrand rechts (x 24→22, y 11–15). Het verre oog is bevroren en in orde.

## 4. Oren: FAIL (1 px)
- **Verre oor:** de schedellijn onder het oor, (23–25,5) → (26–28,6), stopt 1 px voor de buitenrand (30,6). (29,6) is 5, dus de oorrand (29,5) loopt zonder lijn door in de kopzijde (29,7). Dat is het "niet netjes" van Jordi, en het staat nog steeds open sinds ronde 8.
- Reparatie: (29,6) 5→4.
- **Nabij oor:** netjes (rand a/9, holte 4/5, selout). Dat het oor in één rechte lijn doorloopt in de kopzijde (x 12, y 3–7), zit in het silhouet.

## 5. Lijf links tussen arm en kop: PASS
- Onder de kin ligt een slagschaduw 5, daaronder een bolle borst 7 met een kern 3 en via 6 de verre schouder. De kleur sluit aan.
- De rechte rand x 15, y 21–27 (7 px) zit in het bevroren silhouet.
- Klein (optioneel): de lichte rij (13–15,19) tussen kin en schaduw.

## 6. Neus: PASS
- Een ronde knop: de rand loopt x 11→10→9→10→11 over y 15–19. De neus is donker 2, met de glans 7 linksboven (11,16) ingesloten door de omlijning, en een zachte 4 rechtsonder naar de crème kin, (13,17) en (12,18).
- Op 2x leest hij als echte neusknop, zoals bij Zigzagoon en Linoone. Het streepje van Jordi is weg. In ronde 9 rekende ik de glans die tegen de crème zat als FAIL; dat is hiermee opgelost.

## 7. Shading en omlijning: FAIL
- Shading zelf is PASS. Het licht komt overal van linksboven (kruin, borst, dijsikkel, buidel, staartringen), de schaduw volgt de vorm en er is geen pillow of banding.
- De nieuwe lijn boven de nabije hand (22,25) 5 + (23–28,25) 4 geeft de hand de "belijning" die Jordi vroeg en sluit aan op de onderarm. Het is wel een rechte rij van 6 px. Optioneel: (23,25) 4→5, zodat de lijn aan de lichte kant zachter begint.
- **FAIL: dubbele zwarte lijn tussen de nabije poot en de staart.** Op x 41–43, y 41–47 staan de zwarte rand van de poot en die van de staart naast elkaar: 2x2-klonten op (42,41), (42,42), (41,44)–(41,47). SPRITING §8 zegt: "Omlijning altijd 1 pixel breed, geen klonten zwart". Op 12x is het een dikke zwarte naad; op 1x een zwart gat tussen poot en staart. De staart ligt achter de poot, dus de poot houdt zijn zwarte rand en de staartkant krijgt staartkleur (reparatie 2–8). Dit zat er al vanaf het begin in; eerdere keuringen noemden het niet.

## 8. Leesbaarheid 1x: PASS
Op licht en donker leest hij als sluipende wasbeer-Pokémon. Masker, witte snuit en wenkbrauw, rood oog met pupil, neusknop, buidel, crème klauwen en ringstaart met haak zijn allemaal leesbaar.

## 9. Lijn: PASS
Rood oog in een donker masker, crème klauwen, ringstaart, warm palet. Hij oogt als logische eindvorm na olinguito en Coathief (1,28x Coathief).

## 10. Afgekeurde dingen: PASS
Geen helmmasker, geen traan, geen trapjes, geen grijs blok, geen klauwen uit de buik, geen jetpack, pose niet horizontaal. Bevroren delen (buidel, klauwvorm, crème handen, verre oog, borst/buik, palet) zijn niet geraakt, op de door Jordi gevraagde lijn boven de hand na.

## Reparaties voor de allerlaatste afwerking (8 px, alleen kleur)
1. (29,6) 5→4: de verre oorvoet sluit op de buitenrand.
2. (43,41) 1→9: de staartrand naast de poot wordt crème ring (sluit aan op (44,41) 9).
3. (43,42) 1→9: idem.
4. (43,43) 1→9: idem.
5. (42,44) 1→2: de staartrand wordt de donkere ring (sluit aan op (43,44) 2).
6. (42,45) 1→2: idem.
7. (42,46) 1→2: idem.
8. (42,47) 1→2: idem.

Optioneel, buiten het budget, alleen als er tijd is: (23,25) 4→5 (zachter begin van de klauwlijn), (14,19) en (15,19) 7→5 (kinschaduw). Alleen met Jordi's akkoord: glans linksboven, (20,11) e→a en (21,11) a→e.

Na de reparaties controleren:
- alpha-diff 0 ten opzichte van ronde10b;
- bevroren zones gelijk;
- geen 2x2-zwartklonten meer op x 41–43;
- de pootrand blijft 1: (42,41–43) en (41,44–47).

## Voor Jordi (alleen met een silhouetwijziging of een ontwerpkeuze)
- **Rechte randen in het silhouet:** borst x 15, y 21–27 en kopzijde/nabij oor x 12, y 3–7.
- **Nabije hand en onderarm** (bevroren, vorm uit de render): op 1x leest de hand als een crème blokje op de borst. De donkere onderarm (x 28–34, y 26–33) leest als klodder.
- **Mond:** er is geen mondlijn; zo laten of 1–2 px.

## Wat ik anders zie dan de vorige keuringen en notities
- De dubbele zwarte naad poot/staart (x 41–43, y 39–47) noemde geen enkele eerdere keuring.
- De verre oorvoet: de reparatie uit `KEURING_ronde8` R3 zette (29,6) op 5 in plaats van 4, dus hij staat nog steeds open.
- De maker noemt de neusglans "subtiel, leest op 1x zonder glans". Dat vind ik juist goed: een neus hoort op 1x een donkere knop te zijn.
