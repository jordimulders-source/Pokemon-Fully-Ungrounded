# Keuring kleur ronde 8 (verse keurder, 3 nov)

Te keuren: `ronde8.png` (+ `.txt`/`.pal`, `vel_ronde8.png`), naast `ronde7.png`, de render `silhouet_v2/onderlaag_s1a_256.png` en het bevroren silhouet `silhouet_v2/direct_s1a.txt`. Vergeleken op 1x/2x/8x/16x, licht en donker, met 13 echte sprites (Zigzagoon, Linoone, Mightyena, Raticate, Teddiursa, Ursaring, Zangoose, Sneasel, Furret, Sentret, Absol, Weavile, Gumshoos) en met de lijn (`referenties/fase1_olinguito.png`, `fase2_coathief.png`). Ik heb eerst zelf geoordeeld en pas daarna `NOTITIES_ronde8.md` en de oude keuringen gelezen.

Coördinaten (x, y), 0-geteld; paletindex als hexteken (1 zwart, 2 masker, 3 lichtgrijs, 4–7 grijsbruin donker→licht, 8 oker, 9/a crème, b/c/d buidel, e/f oog).

**Uitslag: FAIL (5 van 10 FAIL).** Ronde 8 is duidelijk beter dan ronde 7: de rechte 4-lijn onder de kaak is weg, de schouder is bol, de neus is een echte neus, de staartpunt krult en het "zwevende" vlak op de dij is weg. Bevroren zones zijn niet geraakt (diff ten opzichte van ronde 7: 134 px lijf/kop, 47 px staart, 0 in klauwen en buidel). Wat nog faalt is klein pixelwerk: het oog, het verre oor, een paar losse pixels en één vlek achter de kop. Het oog is ook door de maker zelf als zwak punt genoemd ("op 1x een rood puntje"). Volgens de norm is dat een automatische FAIL.

| # | Punt | Uitslag |
|---|---|---|
| 1 | Alpha-diff, open randen, ruis | **FAIL** (alpha-diff 0 en open randen 0 zijn PASS; 2 losse pixels) |
| 2 | Staartpunt | **FAIL** (2 px slordig; de haak op 1x vraagt een silhouetwijziging: voor Jordi) |
| 3 | Ogen + pixelwerk eromheen | **FAIL** |
| 4 | Oren | **FAIL** (verre oor) |
| 5 | Lijf links tussen arm en hoofd | **PASS** (de rechte rand zit in het silhouet: voor Jordi) |
| 6 | Neus | **PASS** (kleine verfijning mag) |
| 7 | Shading overal | **FAIL** (vlek achter de kop, oorkern) |
| 8 | Leesbaarheid 1x | **PASS** |
| 9 | Past in de lijn | **PASS** |
| 10 | Afgekeurde dingen komen niet terug | **PASS** |

## 1. Alpha-diff, open randen, ruis: FAIL
- Alpha-diff met `direct_s1a.txt`: **0**. Open randen (een randpixel die niet 1/2/4/b/c/e is): **0**. 1682 px.
- Ruis: (33,29) is een losse 4 midden in de donkere onderarm (2). Die leest als stip en volgt geen vorm. (56,28) is zwart naast de zwarte rand (57,28), dus een rand van 2 px dik (klont).

## 2. Staartpunt: FAIL
- Beter dan ronde 7: de lichte dop is weg. De lichte kant loopt nu als één boog (5/4) langs de hangende punt, er zit een binnenlijn van (53,22) naar (51,27), en een crème ring in de bocht. Op 2x en 8x leest het als een omkrullende donkere punt.
- Slordig: (56,26) 8 is een los oker pixeltje. Daardoor springt de onderrand van de crème ring heen en weer (x 52–53 op y 26, x 54–55 op y 25, x 56 weer op y 26), en dat is besluiteloos. (56,28) is de dubbele zwarte rand uit punt 1.
- Op 1x leest de punt vooral als een donkere kop met een lichte vlek. Dat zegt de maker ook. De bocht is in het silhouet dicht; zie Voor Jordi.

## 3. Ogen: FAIL
- Het nabije oog (20–22, 11–12) is nog steeds een balkje van 3x2: e-a-e boven, f-f-f onder, zonder pupil. Het is in wezen het oog van ronde 7; alleen de glans is verschoven. Het zwarte lid (20–23,10) valt weg tegen het masker (2). Daaronder ligt een grijze streep 4 (20–22,13), precies even breed als het oog. Op 16x is dat een wallenbalk, op 1x een rood streepje met een witte stip.
- Echte sprites met een maskerband (Zigzagoon, Linoone) en Sneasel/Raticate hebben een rond oog met een donkere pupil, de glans erboven en lichtere iris eronder. De lijn (olinguito, Coathief) heeft rode irissen zonder pupil, maar die zijn kleiner (fase 1 en 2). Voor een eindvorm mag het oog een stap ronder en rijker.
- Het verre oog (13,11–12) is bevroren. (13,13) 4 is in ronde 8 toegevoegd en geeft hetzelfde grijze streepje.
- Wel goed: de wenkbrauwboog (19–26, 7–9) en de 2 maskerlobben met een brug.

## 4. Oren: FAIL
- Verre oor (rechts, x 24–30, y 1–6): de crème rand zit ook aan de schaduwkant, in 9 (28,3), (28,4), (28,5), (29,5). Hij loopt verder door langs de kopzijde (29,6), dus het oor sluit onderaan niet. De donkere binnenkant (26–28, 5–6) loopt over in de kopschaduw (26–29,7). Op 8x en 16x vloeien oor en kop in elkaar. Dit is het "niet netjes" van Jordi.
- Nabij oor (x 12–22, y 0–4): leest als oor. Wel zit er een donkere kern 4 (16,3)–(17,3) midden in de binnenkant 5. Dat is een kussentje (pillow). Een holte die van linksboven belicht wordt, is donker onder de bovenrand en lichter naar rechtsonder.

## 5. Lijf links tussen arm en hoofd: PASS
- De horizontale 4-lijn onder de kaak (ronde 7, y 20) is weg. Onder de kaak zit nu een slagschaduw 5 (15–17,20)/(16–17,21), dan een bolle schouder 7 met een kleine kern 3 (17–18,23)/(17,24), via 6 naar de verre arm. Kop en lijf sluiten op 1x aan, en de kleur volgt de vorm.
- Rest: de linkerrand x 15, y 21–27 blijft een rechte lijn van 7 px. Dat zit in het bevroren silhouet (voor Jordi). Kan nog beter: de onderkant van de kaak (16–18,19) is 7, dus belicht, terwijl een onderkant van het licht af staat (reparatie 8, optioneel).

## 6. Neus: PASS
- Ronde 7 had een 4-streep. Nu is het een donkere neus 2 (11–13,16)/(10–13,17) met een glanspixel (12,16) en crème snuit eromheen. Op 2x leest hij als neus, zoals bij Zigzagoon.
- Verfijning (optioneel): de onderrij is 4 px lang (met de 1 op (10,17)), dus de neus ligt nog iets als een trapezium. Met (13,17) 2→4 wordt de rechteronderhoek rond. De glans 6 is dof; 7 maakt hem lichter.

## 7. Shading: FAIL
- Over het geheel nu Gen 3-achtig: licht linksboven (kruin 3, schouder 3/7, dij-sikkel 7), schaduw rechts en de vorm volgend. Geen pillow op lijf, kop of dijen. De ringstaart heeft per ring een lichte linkerkant.
- Vlek: (30,16), (31,16), (30,17), (31,17), (28,18), (29,18) vormen een los 6-vlak in de schaduw 5 achter de kop, op de nek of schouder onder de kaak. Ze volgen geen vorm, en volgens SPRITING §5 hoort de slagschaduw van de kop daar volledig in de schaduwkleur. Dit vlak zat al in ronde 7 en is een van de "willekeurige vlekken".
- De oorkern 4 (punt 4) en (33,29) (punt 1).
- Niet als FAIL gerekend, wel gezien: de buidelplooi als stippellijn (buidel bevroren), de 1-px lichte streep 4-3-6-5-4 op x 30–34, y 21–27 (rand bovenarm/buidel), en de 44444-bovenrand (29–33, 26–27) van de donkere onderarm, die recht en blokkig is.

## 8. Leesbaarheid 1x: PASS
Op 1x leest hij direct als wasbeerachtige Pokémon die sluipend op 2 poten staat, met masker, witte snuit en wenkbrauw, ringstaart, buidel en crème klauwen. Hij is doffer dan de echte sprites (een warm grijs palet, bevroren), maar hij valt niet weg, op licht noch donker.

## 9. Lijn: PASS
Rood oog met glans in een donker masker, crème klauwen, ringstaart en een warm bruingrijs palet: dat sluit aan op olinguito en Coathief. De grootte is 1682 px, 1,28x Coathief.

## 10. Afgekeurde dingen: PASS
Geen helmmasker (2 lobben met brug), geen traan, geen trapjesmasker, geen grijs blok onder de kop, geen klauwen uit de buik, geen jetpack. Het masker loopt over de neusrug.

## Reparaties (8; alleen kleur, silhouet en bevroren zones blijven gelijk)
1. **Nabij oog rond, met pupil** (4 px): (21,12) f→1 (pupil onder de glans (21,11)), (21,13) 4→f (ronde onderkant), (20,13) 4→2, (22,13) 4→2 (de grijze wallenbalk weg). Resultaat: een oog van 3x3, e-a-e / f-1-f / 2-f-2, met iris donker boven en licht onder, pupil en glans.
2. **Verre oog onderlid** (1 px): (13,13) 4→2, zodat het gelijk is aan reparatie 1. Het verre oog zelf (13,11–12) blijft.
3. **Verre oor: schaduwrand en sluiten** (6 px): (28,3), (28,4), (28,5), (29,5) 9→3; (28,6) 5→4 (de schedellijn (24,5)–(27,6) loopt door onder het oor); (29,6) 9→5.
4. **Nabij oor als holte** (3 px): (16,2), (17,2) 5→4; (17,3) 4→5.
5. **Staartpunt** (2 px): (56,26) 8→2; (56,28) 1→2.
6. **Onderarm** (1 px): (33,29) 4→2.
7. **Slagschaduw achter de kop** (6 px): (30,16), (31,16), (30,17), (31,17), (28,18), (29,18) 6→5.
8. *(optioneel)* **Kaak en neus**: (16,19), (17,19), (18,19) 7→6, zodat de onderkant van de kaak in de slagschaduw doorloopt; (12,16) 6→7 (lichtere neusglans); (13,17) 2→4 (ronde neushoek).

Na de reparaties opnieuw controleren: alpha-diff 0, open randen 0, en 0 px in de bevroren zones (K/k/Z en het verre oog (13,11–12)).

## Voor Jordi (alleen met een silhouetwijziging of een ontwerpkeuze)
- **Staarthaak op 1x:** de bocht is in het bevroren silhouet dicht. Met kleur leest hij op 2x en groter als haak, maar op 1x als een donkere kop met een lichte vlek. Een echte haak vraagt 1–2 px lucht tussen punt en schacht (rond x 51–52, y 24–27).
- **Rechte randen:** de linkerborst x 15, y 21–27 (7 px) en de kopzijde x 12, y 3–7 (5 px) zijn recht in het silhouet. De kleur verzacht ze, maar haalt ze niet weg.
- **Pupil (reparatie 1):** olinguito en Coathief hebben geen pupil. Mag de eindvorm er wel een, zodat het oog "Pokémon-achtiger" wordt (Zigzagoon/Linoone), of liever zonder pupil en alleen ronder (dan (21,12) f houden)?
- **Mond:** er is geen mondlijn (SPRITING §12: "gezicht compleet"). Een mondje van 1–2 px onder de neus, of zo laten zoals nu (gesloten snuit)?
- **Buikband y 35–37** (bevroren "borst zoals nu", ronde 3): op 1x leest hij als een rechte crème balk of riem onder de klauwen.
- **Donkere onderarm (x 28–34, y 26–33)** naast de nabije hand: op 1x een ronde klodder met een rechte bovenkant. Dat is de vorm uit de render; alleen kleur helpt hier beperkt.
