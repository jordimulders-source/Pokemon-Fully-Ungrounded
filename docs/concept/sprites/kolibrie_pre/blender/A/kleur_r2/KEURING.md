# Keuring kolibrie pre-evo – kleur r2 (onafhankelijke keurder, 5 nov)

Gekeurd: `kolibrie_pre.png` (64×64, 603 px, 15 kleuren + transparant, box x12–45 / y13–45 = 34×33).
Vel: `keuring_vel.png` (4× en 1× naast Taillow, Natu, Pidove, Rookidee, Chikorita, op licht en donker; onderaan 8× met de FAIL-zones genummerd).
Coördinaten zijn (x,y) in de 64×64-sprite. Paletletters zoals in `raster.txt` (1 = bijna-zwart, 2 = donker lila, 3–7 = lila ramp, B/E = vleugel/kap, A/F = grijs, 8/9 = roze, C/D = geel).

## 1. Blinde eerste indruk (vóór NOTITIES/normen gelezen)
- **4×:** een klein lila vogeltje dat schuin naar links zit, kop omhoog, vleugel ingeklapt op de flank, lichte bolle borst. Het lijf heeft goed volume en het licht valt duidelijk van linksboven. De kop leest als vogelkop. Het open bekje leest **niet** als bek maar als twee dunne sprietjes/snorharen met een oranje-roze stipje ertussen; het oog leest als een zwart kadertje met een witte streep (een "0"), niet als een kraaloog. Pootjes: grijze ruis onder de buik.
- **1×:** "een lavendelkleurig vogeltje"; verder niets. Bek, pootjes en bedelgebaar vallen weg. Naast Taillow/Natu/Rookidee is het de zwakste lezer: alles in één lila waas, geen accent (alle referenties hebben een contrastkleur in poten/bek). Het leest als een nette Gen 3-achtige sprite van een generiek vogeltje, niet als fanart; maar het "bedelende nestjong" komt op 1× niet over.

## 2. Vergelijking met echte sprites
Bekeken: taillow, starly, fletchling, pidgey, swablu, wingull, natu, zigzagoon, pichu, chikorita, pidove, rookidee, hoothoot, togepi, spearow (bovenste 64×64, 1× en 4×, licht en donker).
- **Formaat:** 603 px, 34×33. Klopt met de SPEC-richtlijn (±450–650 px); vergelijkbaar met Natu (30×28) en Rookidee (34×33). Onderkant op y45, refs meestal y47–52 (positie regelt de data; geen punt).
- **Omlijning:** refs zetten een duidelijke donkere omtrek rondom; hier is de lichtkant (`2`, x19–21 y22–37) op donkere achtergrond bijna weg. Selout is toegestaan, dus PASS, maar het draagt bij aan de vage 1×-lezing.
- **Accenten:** Taillow (gele poten, rode keel), Natu (gele bek, rode poten), Pidove (roze poten), Rookidee (geel lijf, grijze poten): poten en bek lezen op 1× altijd, met een eigen kleur en dikte ≥ 2 px. Hier zijn bek en poten grijs (A/F) en 1 px dun.
- **Oog:** Starly (repo) heeft zwarte ring + **oranje iris** + witte glans; Taillow donker oog met 1 witte glanspixel. Hier: zwarte ring met een witte/lichte middenkolom, geen iris.

## 3. Richtlijnen (twijfel = FAIL)
| # | punt | oordeel | waar | reparatie |
|---|---|---|---|---|
| 1 | Outline/selout per kleurgroep | PASS | lichtkant `2`/`3`, schaduwkant `1` | – |
| 2 | Zwart alleen aan de schaduwkant | PASS | `1` rechts/onder; links-onder (x22–25, y38–42) is onderkant, mag | – |
| 3 | Binnenlijnen alleen waar vorm over vorm valt | **FAIL** | kop-over-rug: losse donkere `2`-pixels (27,25), (28,26), (29,26), (27,27) tussen `3`'s; leest als vlek/streep, geen lijn (maker noemt dit zelf zwak) | maak er één taps lijntje van 2–3 px in `3`/`2` dat de kinrand volgt (bijv. (29,26)(28,26)(27,27)), of haal `2` weg en laat het een kleurgrens 3/4 zijn |
| 4 | Banding | **FAIL** | kap/achterkop: `E`-strook 2 px breed parallel aan de omtrek, x29–30 y19–23 (`BEE1`, `33EE1`); NOTITIES zegt E-strook weg, maar dat gold alleen y16–18 | E alleen op (30,22),(30,23),(31,23); y19–21 x29–30 naar `B`, zodat de schaduw naar onder breder wordt i.p.v. de rand te volgen |
| 5 | Banding/pillow vleugel | **FAIL** | 1-px lichte `4`-strook binnen de voorrand: (33,29),(33,30),(32,31),(32,32) + (34–36,28) = een lichte binnenrand parallel aan de donkere `E`-lijn; leest als "dubbele lijn" en voedt Jordi's "belijning van de vleugel te hard" | `4` alleen als vlekje van 3–4 px linksboven op de vleugel (34–35,28–29), de rest `B` |
| 6 | Pillow shading lijf/kop | PASS | borst/buik ok (licht linksboven, 7→6→5→4→3→2); kop licht pillow (kern `5` midden, `4` aan de lichtrand x18–19 y15–17) maar binnen marge | – |
| 7 | Jaggies/curven | **FAIL** (klein) | rechterrug: runs x41 y29–32 (4) gevolgd door 2-2-2-3-2 (y33–41): besluiteloos; linksonder runs 1-1-2-1-1 bij x22 y38–39 | rug: (41,32)→ verplaats outline naar (42,32) (runs 3-3-2-2...); linksonder (22,39)→(23,39) indien de vorm het toelaat. Max 4 px |
| 8 | Anti-aliasing | PASS | geen lichte pixels aan de buitenkant | – |
| 9 | Open randen | **FAIL** | (28,44) `F` teen tegen transparant; (15,18) en (16,19) roze `9` van de gaap tegen transparant (bekje, bevroren – zie §4) | teen: (28,44)→`A` of omlijn met (28,45)=`1` |
| 10 | Losse pixels/spijkertjes | **FAIL** | (45,42) `1` hangt als spijker onder de staartpunt; (30,45) `1` enkel pixel onder de pootjes | (45,42) weg; (30,45) weg of onderdeel van een teen maken (zie 14) |
| 11 | Contrast/leesbaarheid 1× | **FAIL** | alles één lila waas; bek, poten, bedelgebaar weg op 1× | opgelost via 14 (pootkleur) + §4 (bek/gaap, als Jordi akkoord is) |
| 12 | Volume (bol lijf/kop) | PASS | lijf leest als bolletje, licht linksboven klopt | – |
| 13 | Vleugel | PASS (vorm) | ingeklapte plaat, rand taps; afwerking zie 5 | – |
| 14 | Pootjes | **FAIL** | x26–33 y43–45: grijze ruis `F/A/1` op 1 rij, geen tenen; maker noemt ze zelf "twee lichte stipjes"; refs: poten altijd met eigen accentkleur | 2 pootjes van elk 2–3 px breed met 2 teentjes, in een warme accenttint (bijv. de `D`-oranje of een roze/lichtgrijs-warm van de kleurfamilie), verre poot een tint donkerder; tussen de pootjes 1 kolom lucht; binnen y43–45, geen silhouetgroei > 4 px |
| 15 | Staart | **FAIL** (klein) | stompje `4/3` x41–43 y35–40 leest op 4× als lichte naad tussen vleugel en omtrek, niet als staart; spijker (45,42) | staartlob donkerder (3/2, achter het lijf = schaduw, Dragonfly Cave §5), alleen top (41,35) `4`; punt netjes afsluiten zonder (45,42) |
| 16 | Palet (≤16, rustig) | PASS | 15 + transparant; tinten rustig; `7` puur wit op de borst (22–24,29–31) is fel maar werkt als hooglicht | – |
| 17 | Oog | bevroren (§4) | (22–24, 17–21) | – |
| 18 | Snavel | bevroren (§4) | (12–18, 15–21) | – |
| 19 | 3/4 links-voor, één oog | PASS | lijf schuin, kop meer naar kijker, één oog (Jordi: "A, met maar 1 oog") | – |
| 20 | Silhouet vs `silhouet_r2.txt` | PASS | alpha-diff 0 (t.o.v. `silhouet_open.txt`: alleen de 13 px buikboog, zoals gemeld) | – |

**FAILs: 9** (3, 4, 5, 7, 9, 10, 11, 14, 15), waarvan 11 grotendeels volgt uit 14 en §4.

## 4. Voor Jordi (smaak / bevroren onderdelen)
- **Oog (bevroren als "Starly-oog"):** op 4× en 8× leest het als zwart kadertje met witte streep (ring x22/x24, wit `7` in de middenkolom (23,18–19), plus een extra `2`-rand aan beide kanten x21/x25 y18–20). De echte Starly heeft een oranje iris; hier is de iris wit geworden, wat op de norm "iris donker boven/licht onder, glans" faalt (SPRITE_NORM #7). Voorstel (alleen met Jordi's akkoord): middenkolom donker (`1`/`A`), 1 glanspixel `7` op (23,18), `2` op x21/x25 naar `3`. Dat maakt het een kraaloog zoals Taillow.
- **Snavel (Jordi: "snavel is prima"):** op 1× lezen de twee 1-px kaken (12,15)–(17,17) en (13,20)–(16,20) als sprietjes; de gaap (roze 9/8, geel C/D) is een stipje van 2×3 px en heeft een open rand (15,18),(16,19). Het bedelgebaar, de kern van het concept, valt daardoor op 1× weg. SPEC zelf eist "snavel op 1× ≥ 2 px". Vraag aan Jordi of de bovenkaak 2 px dik en de gaap 1 px groter/geler mag; anders laten.
- **Vleugel zonder veertextuur:** rustige plaat; voor een donsjong verdedigbaar, Taillow heeft wel lichte veerrijen.
- **Kleurtint:** de ramp (4 = 152,136,200; B = 102,90,172) oogt eerder periwinkle/blauwviolet dan "mild lila"; een iets warmere (roodere) verschuiving zou dichter bij lila zitten.
- **Geen accentkleur:** elke referentievogel heeft een contrastkleur (poten/bek/keel). De gele mondhoeken zijn de logische accentdrager (bedeljong); grotere gaap + warme pootjes geven het sprite 1×-leesbaarheid zonder nieuw kleurvlak.

## 5. Eindoordeel: **TERUG**
Klein en benoemd (bevroren oog/snavel niet aanraken tenzij Jordi het zegt):
1. Pootjes x26–33 y43–45: 2 leesbare pootjes met teentjes in een warme accenttint, verre poot donkerder; (28,44) dicht, (30,45) weg.
2. Kap-banding x29–30 y19–23: `E` alleen onderaan (30–31, 22–23), rest `B`.
3. Vleugel: lichte `4`-binnenrand (33,29)–(32,32) en (34–36,28) vervangen door één vlekje linksboven.
4. Kop-over-rug (27–29, 25–27): één taps lijntje of alleen kleurgrens.
5. Staart: spijker (45,42) weg, staartlob in schaduw (3/2), alleen top lichter.
6. Rugcurve x41 y29–32: runs gelijkmatig maken (≤ 4 px).

Na reparatie opnieuw keuren op 1× naast Taillow/Natu/Rookidee; het oog- en snavelvoorstel (§4) eerst aan Jordi voorleggen.

*Na het eigen oordeel gelezen: NOTITIES.md. De maker noemt zelf de kop-over-schouderlijn en de pootjes als zwak (= fail volgens SPRITE_NORM), en meldt "banding kop opgelost", wat alleen voor y16–18 klopt.*
