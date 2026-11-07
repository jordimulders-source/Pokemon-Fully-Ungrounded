# Keuring Sapa Inca (kandidaat, 6/7 nov)

Gekeurd: `kandidaat/sapa_inca.png` (= ronde 9 v3). Onafhankelijke keurder; niets aan de sprite gewijzigd.
Vellen: `keuring/vel.png` (1×, 4×, 8× op licht en donker; naast Honchkrow, Noctowl, Staraptor, Braviary, Empoleon, Decidueye op 1×; op 4× naast die zes plus Pidgeot, Talonflame, Corviknight, Xatu, Swellow en Blaziken). Uitsneden: `keuring/uitsnede_kop.png` (x8–39, y14–33, 20×), `uitsnede_lijf.png` (x8–41, y26–63, 16×), `uitsnede_vleugel.png` (x32–57, y14–35, 16×).

Werkwijze: eerst blind gekeurd (vel, 8×-uitsneden, rasterdump, scripts), daarna SPEC.md en ronde 4/9-NOTITIES gelezen. Waar een FAIL een bewuste of bevroren keuze van Jordi raakt, staat dat erbij. Coördinaten zijn (x,y) in de 64×64.

## Metingen
| | Sapa Inca | Referenties (fase 3 / vogels) |
|---|---|---|
| Oppervlak | 1637 px | Xatu 1033, Noctowl 1204, Swellow 1432, Staraptor 1446, Corviknight 1526, Blaziken 1579, Decidueye 1668, Honchkrow 1715, Empoleon 1825, Talonflame 1898, Pidgeot 1996, Braviary 2012 |
| Box | 46×62 | Decidueye 45×64, Corviknight 47×60, Staraptor 48×58 |
| Soliditeit | 0,80 | 0,65–0,80 |
| Symmetrie | 0,74 | < 0,80 |
| Zeer donker (K+d) | 0,24 (K 0,11) | refs 0,15–0,37 |
| Palet | 15 kleuren + transparant (index 0) | ≤ 16 |
| Samenhang | 1 component, geen zwevende pixels | |

## Oordeel per punt
| # | Punt | Oordeel | Reden |
|---|---|---|---|
| 1 | Formaat en palet | PASS | 64×64, index 0 transparant, 16 slots. Grijze snavel kost 2 slots voor 12 px, maar binnen de grens. |
| 2 | Oppervlak en box (fase 3) | PASS | 1637 px, net onder de 1700 uit de checklist, maar gelijk aan Decidueye/Corviknight/Blaziken; hoogte 62 vult het vak. |
| 3 | Silhouet en massa | PASS | Op 1× leest het als een rechtopstaande vogel met een enorme waaier, staf links en opgeheven vleugel rechts. Peervormig lijf vergelijkbaar met Empoleon/Noctowl; lucht tussen staf en lijf, onder de vleugel en tussen de poten. |
| 4 | Dominant kenmerk (kroon) | PASS | De waaier is het grootste vlak en breekt de omtrek, zoals bij Noctowl/Empoleon. |
| 5 | 3/4 en perspectief | PASS | Kop draait meer naar de kijker dan het lijf; snavel links van het kopmidden; verre waaierhelft (links) korter dan de nabije (18 vs 21 px); verre vleugel (links) donker, nabije poot (rechts) lager en dikker. |
| 6 | Pose met gewicht, niet stijf | PASS | Contrapposto, opgeheven nabije vleugel, staf in de verre vleugel; geen T-pose. |
| 7 | Alles geteld en verbonden | PASS | 2 vleugels, 2 poten, 2 ogen, snavel; alles vast aan het lijf. |
| 8 | Omlijning per kleurgroep, zwart alleen aan de schaduwkant | FAIL | Kroon goed (paars links, zwart rechts). Maar: zwart aan de lichtkant van de stafkop tegen de kroon (13,22)–(11,27) (E2: overlap in omlijningsbasis, niet zwart); lijf links heeft geen omlijning maar de hooglichttint (zie 11). |
| 9 | Licht van linksboven | PASS | Kroon licht links/rood rechts, buik geel linksboven, vleugel licht aan de bovenkant. |
| 10 | Volume en shading volgen de vorm | FAIL | Lichte streep B langs de rechterrand van de buik (x30–32, y34–52) zit aan de schaduwkant en leest als naad, niet als volume; de staf is in het midden belicht (sYs, x14–16) in plaats van links-van-het-midden. |
| 11 | Open randen (script) | FAIL | Hooglicht-bruin B direct naast transparant: (22,27), (21,28)–(21,31), (37,29), (38,29), (40,28)–(42,28), (50,19), (52,18). Basisbruin b naast transparant: (20,32), (19,33), (18,34), (13,39), (13,40), (12,41), (12,42), (35,30), (36,29), (39,28). Verder schaduwtinten aan de rand: kroonkwastje r (10,23)–(10,27), gezicht r (22,23)–(22,25), (32,23); poten G (24,54)–(24,59), (22,60), (23,60); stafvaan s onderaan (14,47), (15,47) aan de onderkant (schaduwkant hoort zwart). Ronde 9 meldt "0 open randen": de eigen controle telt deze tinten blijkbaar als omlijning. |
| 12 | Losse pixels / vlekjes | FAIL | Paarse kwastjespuntjes van de kroon rechts komen als losse vlekjes uit: (43,23)–(43,24) tussen kroon en vleugel en (46,31)–(47,31) onder de vleugel; op 1× twee paarse stippen zonder vorm. (Volgens SPEC "rechter kwastje valt achter de vleugel": bedoeling klopt, uitvoering leest als ruis.) |
| 13 | Geen ruis | FAIL | Schaakbordje b/d in de verre vleugelpunt om de staf (x13–19, y42–45), losse d-stippen in de borst (25,30), (27,31), (24,32) en B-stippen (24,34), (28,34); op 1× oogt de hand gevlekt. |
| 14 | Ogen geïntegreerd, Pokémon-stijl | FAIL | Nabije oog (29–31,24): lid d, iris Y, pupil K, glans C: de opbouw klopt, maar het is 1 rij hoog en de glans zit aan de buitenkant/schaduwkant. Verre oog (24,24) is 1 px geel zonder lid. Op 1× twee gouden puntjes. (Jordi: "mogen klein, maar wel duidelijk pokemon stijl"; dat laatste haalt het op 1× nog niet.) |
| 15 | Kroon leesbaar op 1× | PASS | Waaier met paarse rand, gouden boog en randvlekken leest direct. |
| 16 | Gezicht leesbaar op 1× | FAIL | De haaksnavel (cCc, x24–27, y22–26) is op 1× een lichtgrijs stipje recht naar beneden; het leest als witte vlek/monocle onder een rode band, niet als snavel. Geen enkele referentie heeft een gezicht dat zo weinig zegt. Gouden vlekje (32–33, 25–27) is op 1× onduidelijk (oorschijf?). (Jordi vond het gezicht(sidee) mooi en bevroor het; dit gaat dus om leesbaarheid, niet om het idee.) |
| 17 | Staf als staf | PASS | Gouden speerpunt + vaan + schacht, rechtop, leest op 1× als scepter. |
| 18 | Opgeheven vleugel | PASS | Leest als opgeheven vleugel/arm met penscheidingen. Stompe, rechte punt (x54, y18–22) zie 22. |
| 19 | Buik | PASS | Gouden ovaal met volume, licht linksboven. |
| 20 | Poten | PASS | Twee poten, nabije lager en dikker, tenen; dun maar zoals Staraptor/Swellow. Klauwen ontbreken (zie smaak). |
| 21 | Kopverhouding (fase 3: 20–30%) | FAIL | Kop zonder kroon 11×9 px = 15% van de hoogte; daardoor lukken ogen en snavel niet (14, 16). Bekend en door Jordi genoemd ("gezicht nog net iets te klein"); zit in het silhouet. |
| 22 | Curven, geen rechte stukken waar het rond is | FAIL | Linkerkant van de kop recht (x22, y23–27, 5 px: doos-kop), rechterflank recht (x38, y36–41, 6 px), vleugelpunt plat afgesneden (x54, y18–22, 5 px), onderrand van de vleugelwortel recht (x35–40, y33). De rechte onderkant van de kroon (y22) reken ik niet mee: zie smaak. |

**Totaal: 13 PASS, 9 FAIL.**

### Wat ik als eerste zou repareren (technisch)
1. Kop een paar px groter (silhouetkeuze, al open in de SPEC), zodat snavel en ogen 2 rijen krijgen; snavel schuin naar linksonder met een donkere haak, zodat hij op 1× een snavel is.
2. Lijf links en de vleugelwortel een omlijning geven (d of b-donker) i.p.v. B naast transparant.
3. Paarse kwastjespuntjes (43,23–24) en (46–47,31) weg of groot genoeg om als kwastje te lezen.
4. Schaakbord in de hand en losse d/B-stippen in de borst gladstrijken.
5. B-streep rechts van de buik vervangen door b/d (schaduwkant).

## Voor Jordi (smaak)
- **Onderkant van de kroon is één rechte horizontale rand** (y22, x17–46): dat is trouw aan de echte koningstiran (paraplu/paddenstoel, foto 2), maar op 1× oogt hij als een parasol of hoed boven de kop in plaats van een kuif die uit de kop groeit. Mag zo blijven; een lichte boog of één pixel verspringen bij de kop maakt hem organischer.
- **Staf als staart:** op 1× leest hij als staf; de staart-hint (vaan, bocht onderin naar het lijf, rood puntje tussen de poten (28,54–55)) is subtiel tot onzichtbaar. Prima als bedoeling ("een hint"), maar wie het niet weet, ziet geen staart.
- **Gezichtsidee** (oranjerood caracaramasker met bleke snavel) is mooi gekozen en past bij het type; het probleem zit in de maat (zie 16, 21).
- **Kleurbalans:** veel oranjerood bovenin, donker chocoladebruin lijf; samen met de gouden buik, staf en poten oogt hij top-zwaar maar wel koninklijk. Paars (Psychic) komt alleen in de kroonrand terug.
- **Hand om de staf** leest als vuist/klomp; past bij "koning met scepter", maar is de minst vogelachtige plek.
- **Poten zonder klauwen**: de bergcaracara heeft zwarte klauwen en Staraptor/Braviary/Talonflame tonen ze duidelijk; nu zijn de voeten kleine gouden klompjes. Smaak/kleine toevoeging.
- **Vleugelpunt plat afgesneden**: Empoleon-flipper is gekozen; een iets rondere of spitse punt (open vraag in de SPEC) zou meer "vleugel" zeggen.
