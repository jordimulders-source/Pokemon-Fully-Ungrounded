# Keuring Coathief r6 (bruine lijf), verse keurder, 19 nov

**Oordeel: BIJNA** (duidelijk beter dan r5; één zone moet nog).

## Hoofdvraag (blind, 8× en 1×, naast Mightyena/Linoone/Furret/Zigzagoon `anim_front_gba` frame 1)
- **r6 heeft nu volume, r5 niet.** r5 was één middenvlak met een lichte rugstrook en donkere randen ("effen 2 kleuren" klopt). In r6 lezen op 1× twee massa's: een ronde schouder links en een dij rechts, gescheiden door een schaduwvouw die doorloopt in de buikschaduw; onderbuik en rechterkant liggen rustig in schaduw (sikkel). Dat zit dicht bij Mightyena/Linoone (veel hooglichttint, grote rustige vlakken).
- **Schouder:** leest als bolling. Alleen het hooglicht loopt tot tegen de linkerrand (x29, y38–39) en trekt daardoor iets schuin naar linksonder.
- **Dij: het hooglicht leest als een schuine streep, niet als bolling.** E loopt als 2 px brede baan van (44,33) naar (41,38)–(42,39), en daaronder loopt een 7-strook verder door tot y42 (x40–41). Samen een lange diagonale streep langs de voorkant van de dij in plaats van een vlek op de top van de bol.
- Niet rommelig/vlekkerig: geen losse tintvlakjes in het lijf.

## Regels (gemeten)
- Tinten lijf: 5/6/7/E = helderheid 57 / 95 / 136 / 176 → stappen 38, 41, 40. OK.
- Tintvlakjes < 3 px in het lijf: geen (de enige kleine 5-clusters, (35–36,31) en (30–31,33), zijn selout van de buitenrand).
- Pillow shading: nee. Licht linksboven: ja. Banding: lichte neiging bij de rechter schaduwband (x47–49, y39–47, gelijk breed langs de rand), acceptabel.
- Bevriezing: r5→r6 verschilt in 137 px, allemaal bruin→bruin; diff 0 buiten het lijf.

## MOET (pixels, index E = hooglicht)
**Romp/dij (hooglicht ovaal maken, staart weg):**
- (42,36) → E
- (42,37) → 7, (43,37) → 7
- (41,38) → 7, (42,38) → 7
- (42,39) → 7
- (40,41) → 6, (41,41) → 6, (40,42) → 6
Resultaat E-dij: y33 x43–44, y34 x42–44, y35 x42–45, y36 x42–44 (ovaal op de top van de dij, 7 als rand eromheen en wegvallend naar 6 onder y40).

**Schouder (hooglicht van de rand af):**
- (29,38) → 7, (29,39) → 7

## MAG
- (37,34) (losse 6 in de 7-rugstrook, begin van de vouw) → 7, zodat de rug bovenaan één doorlopend licht vlak is en de vouw pas bij y35 begint.
- Rechter schaduwband iets taps: bovenaan smaller (bijv. (46,39) → 6) zodat hij als sikkel onder de dij uitwaaiert i.p.v. even breed langs de rand.
