# Keuring kolibrie ronde 2 (24 okt, onafhankelijke keurder)

**Gekeurd:** `kolibrie.png` (64×64, P-modus, 16 kleuren waarvan 15 gebruikt, index 0 transparant, 1035 px, box 62×60).
**Vergeleken met** (eerste frame van `anim_front.png` met `normal.pal`, op 1×, 3× en 5×, op lichte en donkere achtergrond): Venomoth, Ho-Oh, Fearow, Articuno, Talonflame, Ninjask, Murkrow, Honchkrow, Swellow, Crobat, Mismagius, Drifblim, Yanma en Beautifly (14). Vel: `keuring_vergelijking.png` (bovenaan 3× naast Venomoth, Yanma, Swellow, Articuno, Crobat en Drifblim; daaronder alle 14 op 1×, licht en donker).

## Totaaloordeel: NIET GOED

Op 1× leest hij **niet overduidelijk als kolibrie**. Naast Yanma en Venomoth leest hij als een paarse **mug of langpootmug**: een naaldsnuit, twee smalle rechte vleugels, drie kleurblokken achter elkaar (zwarte kop, blauwgroen "borststuk", fel paars "achterlijf") en drie dunne geknikte poten met witte voetjes eronder. De slierten zijn de grootste oorzaak. Daarnaast zijn er drie automatische fails:
- de maker noemt zelf een zwak punt (de kop verdwijnt op een donkere achtergrond);
- de slierten hebben veel rechte stukken en scherpe knikken;
- de omlijning van de slierten zit aan de verkeerde kant.

---

## 1. Silhouet (bevroren: `silhouet_v6_groot_1x.png`)
Pixeldiff (eigen script): sprite 1035 px, silhouet 986 px, **56 erbij en 7 eraf**. Elke afwijking ligt op maximaal 1 px van de omtrek (Chebyshev-afstand, gemeten in beide richtingen). Dat klopt met NOTITIES.md.

| punt | oordeel | toelichting |
|---|---|---|
| ±1 px-regel | **PASS** | Geen enkele pixel ligt verder dan 1 px van het silhouet. Alles is gemeld. |
| slierten 41 px breder | **PASS, met kanttekening** | De verbreding valt binnen ±1 px en hoort bij de opdracht (punt 3), maar het is geen omlijning of anti-kartel: elke sliert wordt ±50% dikker, van 2 naar 3 px. De **lijnvorm** blijft gelijk (zelfde banen, zelfde knikken). Het silhouet verandert dus niet, de leesbaarheid wel: als 3 px-band met een zwarte rand lezen ze nog sterker als **poten** dan in het slanke silhouet. De oorzaak is de kleuring, niet de breedte (zie reparatie 1). |
| kuif, voorhoofd, buikgat, racket B | **PASS** | Kleine verschuivingen binnen 1 px, met reden. Let op: met het dichten van het buikgat (29–31,39) is de buik een rechte lijn van 20 px geworden (zie A6). |

## 2. Harde eisen `SPRITE_NORM.md`
| # | eis | oordeel | wat er mis is (waar) | reparatie |
|---|---|---|---|---|
| 1 | Leest op 1× als echte Pokémon van dit bouwtype | **FAIL** | Naast de 14 referenties leest hij op 1× als insect (Yanma-familie): drie kleursegmenten (kop / blauwgroen / paars) als kop-borststuk-achterlijf, en drie slierten met bleke ovaaltjes als geknikte poten met voetjes. Naast Swellow, de vogel met staartslierten, valt op dat Swellow brede, taps toelopende staartveren heeft, geen lijnen. | Reparaties 1, 2, 3 en 5. |
| 2 | 3/4 links-voor | **PASS** | Vogel met snavel in profiel, één oog (B2). Het lijf staat open naar de kijker via de V van de vleugels; de verre vleugel is smaller en donkerder, zoals bij Swellow en Fearow. | – |
| 3 | Delen vast, geen gat vleugel–lijf | **PASS** | Beide vleugelwortels sluiten aan; de slierten zitten aan de staartbasis. | – |
| 4 | Geen Escher, overlap consequent | **FAIL** | Sliert 2 loopt in rij 48–51 (x 53–55, `171`) **direct tegen racket A aan** (x 56–59), zonder lucht of scheidingslijn. De knik van sliert 2 en het vlammetje van sliert 1 smelten zo samen tot één "knie met voet". Ook het einde van sliert 2 (53–54,53) loopt zonder overgang in racket B over. | Minstens 1 kolom lucht tussen sliert 2 en racket A (rij 48–51), of sliert 2 daar 1 px naar links (binnen ±1 px). Laat racket B duidelijk uit het einde van sliert 2 groeien: een smaller steeltje en dan pas de verdikking. |
| 5 | Geleidelijke curven, geen rechte lijnen ≥ 4 px waar het dier rond is, geen doos | **FAIL** | (a) **Buik:** rij 39, x 22–41, is een rechte zwarte lijn van **20 px** (de onderkant van het lijf als liniaal). (b) **Sliert 3:** x 45–47 loopt in rij 45–51 7 rijen kaarsrecht verticaal. (c) **Sliert 1:** x 60–62 loopt in rij 41–45 5 rijen recht verticaal en knikt dan scherp. (d) **Sliert 2:** x 54–56 loopt in rij 44–47 4 rijen recht. (e) Rij 36, x 48–53: 6 px zwart, recht horizontaal. Articuno's staart (de referentie die Jordi aanwees) heeft geen enkel recht stuk: de helling verandert geleidelijk. | Buik binnen ±1 px als holle boog: rij 40 bij x 25–33 1 px laten uitbollen, en de lijn bij x 38–42 1 rij hoger laten oplopen naar de staartbasis. Slierten: hellingen 1-1-2-2-3 / 3-2-2-1-1 in plaats van recht–knik–recht (Articuno, Swellow). |
| 6 | Kop ±20–30% bij eindvorm, geen te lange schedel | **PASS** | Kop rij 20–33 is 14/60, ofwel 23%. Plat bovenhoofd zoals Jordi vroeg. | – |
| 7 | Ogen geïntegreerd | **PASS (polijsten)** | 2×3 px: zwart, glans wit (11,26), reflectie violet (11,27). Klein, zoals gevraagd, en het leest op 1× als oog. Maar glans en reflectie staan in dezelfde kolom onder elkaar, wat op 3× leest als "wit puntje met paarse traan". De reflectie hoort tegenover de glans. | Glans naar (11,25), reflectie naar (12,27); (11,26) en (12,25) zwart. |
| 8 | Kenmerken leesbaar op 1×, geen klodders of harken | **FAIL** | (a) De **vlammetjes** lezen op 1× als bleke druppels of voetjes, niet als vlam (ovaal, met de donkerste tint `6` onderaan, dus "hangend"). (b) De **staartfranje** (x 43–58, rij 33–36) leest niet: een egale paarse steel waar de slierten uit komen. Er zijn geen veren te zien, dus geen kolibriestaart. (c) De **pennen** in de nabije vleugel (rij 14–21, x 33–48: `33cc33`, `333c333cc33`) vormen een ruitjes- of gaaspatroon. Dat leest als libellenvleugel. | Zie reparaties 2, 3 en 4. |
| 9 | Omlijning per kleurgroep, zwart alleen aan de schaduwkant, licht linksboven, geen open randen | **FAIL** | (a) **Slierten:** het patroon `1 7 5` (zwart links, omlijningsbasis rechts) zet het zwart aan de kant die naar het licht (linksboven) gekeerd is. Bij sliert 1 en 3 zit de lichtkant dus zwart en de schaduwkant licht: omgekeerd. (b) Open randen: basistint `7` naast transparant op (42,36), (43,56), (42,57); schaduwtint `6` naast transparant op (21,38); bleek `e`/`d` op de vleugelrand op (49,12), (55,11) en op het vlammetje op (56,51), (50,54). | (a) Draai het per sliert om: lichtkant (links/boven) `5`, schaduwkant (rechts/onder) `1`, en waar de sliert onder iets anders doorloopt alleen `1`. (b) De genoemde pixels vervangen door de omlijningstint van hun groep (`5`/`1` voor violet, `c` voor bleek). |
| 10 | Geen Chernobyl | **PASS** | Geen misvormd gezicht of losse delen. Het blauwgroen "uit het niets" grenst eraan, zie §5. | – |

## 3. `FAKEMON_CHECKLIST.md` (wat voor een vliegende vogel geldt)
| # | oordeel | toelichting |
|---|---|---|
| A1 silhouet leest als de soort | **FAIL** | Het silhouet alleen (v6) leest als kolibrie. De gekleurde sprite leest op 1× als mug: de kleuring zet de segmentatie en de poten neer (eis 1). |
| A2 dominant kenmerk breekt de omtrek | PASS | Snavel en slierten. |
| A3 diagonale compositie | PASS | Kop linksonder-midden, vleugels als tegenwicht rechtsboven, slierten rechtsonder. |
| A4 negatieve ruimte | PASS | |
| A5 niet symmetrisch | PASS | |
| A6 geen bouwblokken | **FAIL** | Buik van 20 px recht (rij 39); de romp plus de franje (x 16–58, rij 28–39) is één horizontale worst met evenwijdige boven- en onderrand van ±8 px dik (zuil). |
| B1 kop meer naar de kijker | PASS | Profielkop met één oog, zoals Swellow en Fearow. |
| B2 / B7 één oog, gezicht compleet | PASS | |
| C1 alles geteld | PASS | Twee vleugels, kuif, drie slierten. Geen pootjes, wat klopt voor een zwevende kolibrie. Voeg ze ook niet toe: de slierten lezen al als poten. |
| C7 één houding | PASS | Drinkende zweefpose. |
| C8 staart sluit aan en buigt | **FAIL** | De slierten komen uit een rechte zwarte balk (rij 36) en buigen in hoeken, niet in bogen. |
| D1 oppervlak per fase | **FAIL** | Eindvorm: 1035 px. Fearow 1978, Articuno 1953, Talonflame 1898, Honchkrow 1715, Swellow 1432, Crobat 1096. Alleen Crobat zit in de buurt, maar Crobat heeft grote dichte vleugelvlakken. Hier zit de massa in lijnen. Op 1× oogt hij als een fase 1 (naast Murkrow 937 en Yanma 966). **Valt niet binnen het bevroren silhouet op te lossen**: dit is een vraag voor Jordi (zie §8). |
| D2 kop per fase | PASS | 23%. |
| E1 verre kant donkerder | PASS | De verre vleugelwortel is `2`, de nabije `3`, met het hooglicht `4` op de voorrand. |
| E2 overlap met omlijning | **FAIL** | Sliert 2 en racket A raken elkaar zonder scheiding (eis 4). |
| E3 donker-aandeel | **FAIL (via zelfgenoemd zwak punt)** | De tinten `1`, `2` en `5` samen zijn ±0,30, met `3` erbij ±0,49 (de band is 0,10–0,25). Bij fluweelzwart is dat toegestaan, maar de maker meldt zelf dat de kop en de vleugelwortels **op een donkere achtergrond verdwijnen**. Dat is bevestigd: op het donkere vel valt de kop weg, de snavel is onzichtbaar en alleen het oog blijft over. Murkrow en Honchkrow (ook bijna zwart) lezen daar wel, door koel blauwe hooglichten (64,96,152 / 112,136,184) op de lichtkant. |

## 4. `SPRITING.md` §0 en §1–§8
| punt | oordeel | toelichting |
|---|---|---|
| §0.1 diagonaal 3/4 | PASS | |
| §0.2 geteld en verbonden | PASS | |
| §0.3 geen rechte lijnen | **FAIL** | Zie eis 5. |
| §0.4 ogen | PASS (polijsten) | Zie eis 7. |
| §0.5 silhouet op 1× leest als de soort | **FAIL** | Zie A1. |
| §0.6 formaat | **FAIL** | Zie D1. |
| §0.7 pose niet stijf | PASS | |
| §1 met de hand | PASS | Een tekstraster in `teken.py`. |
| §3 curven: geen knik in een curve, geen besluiteloosheid | **FAIL** | De slierten wisselen recht verticaal (5–7 rijen) af met abrupte 1:1-diagonalen: "spijkertjes" op de knikken (onder meer (60–62,45→47), (45–47,51→52)). |
| §4 palet: 3 tinten + omlijning per groep, niet overshaden | PASS (krap) | Vier groepen: fluweel 1–4, violet 5–8, blauwgroen 9–b, bleek c–f. Netjes opgebouwd. |
| §4 "kleuren liefst van een bestaande sprite, niet te fel" | **FAIL** | Het lijfviolet (142,54,214) heeft een verzadiging van 0,75 en het schaduwviolet (106,30,166) 0,82. Dat is feller dan Crobat (131,74,205, 0,64) en veel feller dan de Ghost-paarsen van Mismagius en Drifblim (128,80,168 / 152,112,216, ±0,5). Naast de gedempte fluweelkop en het blauwgroen ontstaat daardoor een **neon-achterlijf** dat zich als los blok losmaakt. |
| §5 licht linksboven | **FAIL** | Kop, schouder en lijf kloppen (hooglicht `4` links op de kop, `b` linksboven op de schouder, slagschaduw `6` onder de vleugel, `1` aan de buik). De slierten staan andersom (eis 9a). Het vleugelhooglicht `4` staat alleen op de wortel. |
| §5 shading met vorm, geen kussen | PASS (krap) | Slagschaduw onder de vleugel, licht op de flank, schaduw aan de buik: dat volgt de vorm. Wel liggen de hooglichten `8` als losse vlekjes midden op het lijf ((23–24,29–31), (28–29,32–33)) en die lezen op 3× als stippen. Polijsten: samenvoegen tot één smalle band langs de bovenflank. |
| §6 glans | PASS | Eén glanspixel in het oog en één kern per vlammetje. |
| §7 texturen: glad | PASS | Veren glad, geen schubben. Goed. |
| §8 omlijning 1 px, zwart alleen aan de schaduwkant, geen AA buiten | **FAIL** | Zie eis 9. Verder overal 1 px en geen buiten-AA. De kuif gebruikt pseudo-omlijning (1–2 px dik), wat is toegestaan. |

## 5. `FAKEMON_DESIGN.md`
| principe | oordeel | toelichting |
|---|---|---|
| Simpel: geen detail dat niet op 1× leest | **FAIL** | Het gaaspatroon in de vleugel, de vlekjes `8` op het lijf, het violette kruinvlekje (9–13,21–22) en de bleke kuifpuntjes lezen op 1× als ruis of stipjes. |
| Beperkt palet (2–3 hoofdkleuren) | **FAIL (twijfel)** | Fluweel, violet, blauwgroen en bleek Ghost-licht zijn vier groepen, en drie daarvan lezen als **afzonderlijke blokken** achter elkaar. Het blauwgroen (x 15–26, rij 23–30) heeft rondom een eigen donkere rand (`9`) en ligt als een ovaal **badge of kraag** tussen kop en lijf. Het hoort dus niet bij de vorm. Bij de echte fluweelpaarse kroonkolibrie is het een glans op de rug, geen apart vlak. |
| Geen hybride, één geheel | **FAIL** | Door de segmentering (zwart / blauwgroen / neonpaars) en de "poten" voelt hij als kolibriekop op een insectenlijf. |
| Type verwerkt (Ghost: mystiek, positief) | **FAIL (twijfel)** | Het is niet eng, dat is goed. Maar de Ghost-sfeer komt op 1× nauwelijks over: alleen de bleke vleugelpunten en drie witte stipjes. Zonder briefing ziet een kijker een paarse Bug/Flying. Mismagius en Drifblim zetten Ghost neer met gedempt paars en zachte, wapperende vormen. Hier is het neonpaars en hoekige lijnen. |

## 6. `SPEC.md` per onderdeel (Jordi's woorden)
| onderdeel | oordeel | toelichting |
|---|---|---|
| pose, lijf, kop, vleugelaanzet (bevroren) | PASS | Volgt het silhouet. Met "dat lichaam mag ook iets gladder" is de rechte buiklijn wel in strijd (eis 5). |
| vleugels: vorm (bevroren) | PASS | Volgt het silhouet. |
| vleugels: doorzichtig, "venomoth doet het vleugel effect goed", "vanaf het midden tot de buitenkant geleidelijk aan doorzichtiger" | **FAIL** | Het verloop fluweel → lila → bleek → bijna wit is er wel, maar het leest als **donkere vleugel met lichte punt** (kleurverloop), niet als doorschijnend. Bij Venomoth (en Yanma) zit het effect in een bleke vulling met **doorlopende dunne aders tot aan de rand** en een gesloten, iets donkerdere buitenrand. Hier is het binnenste ±40% egaal fluweel, zijn de aders een gaaspatroon en houden ze op vóór de bleke zone. Op donker gloeien de punten wit op, het tegendeel van doorzichtig. Dezelfde valkuil staat al als les in FAKEMON_DESIGN.md: "vervagen naar een egale achtergrond leest als kleurverloop". |
| staart: "articuno achtige dynamiek" | **FAIL** | Articuno heeft één brede, golvende band met geleidelijke helling. Hier zijn het drie dunne geknikte draden (eis 5, C8). |
| racketpunten: bleke zielvlammetjes | **FAIL** | Ze lezen als druppels, parels of voetjes: ovaal met de donkere kant onderaan. Een vlam heeft een punt naar boven of naar achteren en een brede, ronde onderkant. |
| kuif: jeguaka, drie veren schuin naar achteren, "de kroon maken we nog wat langer" | **FAIL (twijfel)** | De vorm is bevroren en Jordi is akkoord. Maar op 3× komen de drie veren samen in één steel (rij 17–19, x 12–15: `575751`, `1551`, `121`) en de derde veer ligt horizontaal (`5775`, rij 16). Dat leest als takje, klauwtje of drietand, niet als drie losse veren. Op 1× is het een paars sprietje. |
| kop: Ho-Oh/Fearow-stijl, "het oog mag veel kleiner" | PASS | Klein oog, platte kruin. Alleen op een donkere achtergrond FAIL (E3). |
| palet: velvet purple, "mystiek ... positieve link met de dood/afterlife" | **FAIL** | Zie §4 (neonviolet) en §5 (blauwgroen als badge, Ghost-sfeer zwak). |

## 7. Bijzondere aandachtspunten in het kort
- **Overduidelijk kolibrie op 1×?** Nee: mug of langpootmug (Yanma ernaast maakt het pijnlijk duidelijk).
- **Ghost-sfeer?** Niet eng, maar ook nauwelijks mystiek.
- **Vleugels doorschijnend à la Venomoth?** Nee: het is een kleurverloop en het gaaspatroon leest als insectenvleugel.
- **Omlijning en selout?** Kop en lijf zijn goed. De slierten zijn omgekeerd, plus 9 open randpixels.
- **Shading?** Volgt de vorm (geen kussen), met losse hooglichtvlekjes.
- **Oog?** Goed. Klein polijstpunt (glans en reflectie diagonaal).
- **Kleurvlakken?** Het blauwgroen is een los blok en het violet te fel. Samen geven ze segmentatie.
- **Slierten en vlammetjes?** De hoofdfout: poten met voetjes.
- **Kuif als drie veertjes?** Op 3× eerder een takje.
- **Grootte?** Te klein voor een eindvorm (1035 px tegen 1430–2490).
- **Te druk of te veel kleuren?** 15 kleuren is binnen de grens en niet druk. Wel te veel losse accenten (gaas, vlekjes, kruinvlek, kuifpuntjes).

## 8. Geprioriteerde reparatielijst
Alles binnen ±1 px van het silhouet, tenzij anders gemeld.
1. **Slierten herkleuren tot staartveren, niet poten** (eis 1, 5, 8, 9; C8). Laat de zwarte binnenrand weg als doorlopende lijn. Per sliert: lichtkant (links/boven) `5`, kern `7` met hier en daar `8`, schaduwkant `1` alleen aan de onderkant van een bocht. Zo leest het als glanzend lint (Swellow, Articuno). Strijk binnen ±1 px de rechte stukken glad tot geleidelijke bogen: sliert 3 rij 45–51, sliert 1 rij 41–47, sliert 2 rij 44–47, en de zwarte balk in rij 36 (x 48–53). Laat ze naar het eind iets **dunner** worden (3 → 2 px vóór het vlammetje), zodat ze niet als poten met voeten eindigen.
2. **Sliert 2 los van racket A en racket B** (eis 4, E2): 1 kolom lucht in rij 48–51 tussen x 55 en 56; racket B via een steeltje uit sliert 2.
3. **Vlammetjes als vlam, niet als druppel** (SPEC, Ghost): de punt naar achteren of omhoog (1 px breed, `d`/`e`), de brede ronde kant aan de sliert, de omlijning `c` rondom gesloten, en de donkerste tint niet onderaan. Eén vorm voor alle drie, in verschillende grootte (niet gekopieerd).
4. **Vleugels doorschijnend à la Venomoth/Yanma** (SPEC): fluweel alleen op de wortel (±⅓, waar hij aan het lijf zit); de middelste ⅓ `c` en de buitenste ⅓ `d`/`e`. Teken 2–3 **doorlopende** pennen (`3` op de wortel, `c` in de bleke zone) evenwijdig aan de vleugelas tot aan de rand, in plaats van het gaas in rij 14–21. Houd de buitenrand gesloten in `c` (repareer (49,12) en (55,11)).
5. **Segmentatie weg: één vogel met donkere kap** (eis 1, ontwerp):
   - (a) Lijfviolet dempen naar Crobat-niveau: ±(132,74,200) basis, ±(98,44,150) schaduw, ±(176,128,232) hooglicht.
   - (b) Blauwgroen als **glans op de rug** in plaats van een omrande badge: haal de rand `9` weg waar het grenst aan de kop en de vleugelwortel; laat het als smalle, iets onregelmatige band (2–4 rijen) over de schouder naar de vleugelwortel lopen en daar overgaan in fluweel.
   - (c) Laat het fluweel van de kop via de nek in schaduwtinten overlopen in het violet van de borst (kraag), in plaats van een harde kleurgrens bij x 15–17.
6. **Kop leesbaar op een donkere achtergrond** (zelfgenoemd zwak punt, E3): een koel randlicht (bijv. 112,104,160, of `4` lichter maken) als 1 px-rand op de lichtkant van kruin, achterhoofd en snavelrug, en op de voorrand van beide vleugelwortels, zoals Murkrow en Honchkrow het met blauw doen.
7. **Buik rond** (eis 5, A6): de rechte lijn van 20 px in rij 39 binnen ±1 px als boog; franje x 43–58 voorzien van 2–3 veerpunten met donkere inkepingen (binnen het silhouet), zodat er een staart leest.
8. **Kuif:** binnen ±1 px de gezamenlijke steel splitsen (een donkere inkeping tussen veer 1 en 2 bij rij 17–18), zodat er drie veren uit de kruin komen. Maak de bleke punten 2 px en volg de veerrichting (schuin naar achteren).
9. **Open randen** sluiten: (42,36), (43,56), (42,57), (21,38), (56,51), (50,54).
10. **Polijsten:** de hooglichtvlekjes `8` op het lijf samenvoegen tot één band langs de bovenflank; de glans van het oog naar (11,25) en de reflectie naar (12,27).

### Voor de coördinator en Jordi (niet binnen het bevroren silhouet op te lossen)
- **Formaat:** 1035 px is klein voor een eindvorm (Swellow 1432, Fearow 1978). Mogelijkheden: accepteren als slanke zweefvogel (Crobat 1096) of het silhouet ±15% opschalen. Dat beslist Jordi.
- **Slierten:** ook in het silhouet zelf (v6, effen kleur) lezen ze al half als poten. Lost reparatie 1 dat niet op, dan moeten de slierten breder en lintvormiger worden zoals bij Articuno, en dat is een silhouetwijziging voor Jordi.
