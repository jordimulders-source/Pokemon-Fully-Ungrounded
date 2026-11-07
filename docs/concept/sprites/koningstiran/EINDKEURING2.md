# Eindkeuring 2 Sapa Inca (ronde 14)

Gekeurd: `ronde14/sapa_inca.png`. Ik ben een verse, onafhankelijke eindkeurder en heb niets aan de sprite gewijzigd. Eerst heb ik zelf geoordeeld, met een rasterdump, uitsneden op 12×, 1× op licht en donker en scripts. Pas daarna heb ik `SPEC.md`, `ronde14/NOTITIES.md` en `EINDKEURING.md` gelezen.

Maatstaf: netheid per onderdeel, en twijfel = FAIL (Jordi: "de poten plus ertussenin is slordig", "evenals het linkeroog", "boven de rechter vleugel zitten opeens een paar paarse pixels"). Coördinaten zijn (x,y) in de 64×64.

Tinten-afkortingen:
- K zwart, d donkerbruin (52,38,36), m middenbruin, l lichtbruin (136,104,86);
- r rood, o oranje, p paars, v lavendel;
- a donkergoud, b goud, c lichtgoud, f roest;
- s snavelgrijs, e snavelwit.

## Vellen (`eindkeuring2/`)
- `onderdelen_12x.png`: elk onderdeel op 12× met raster. De blauwe kaders zijn FAIL-plekken; de nummers zijn die van de tabel hieronder. Onderaan staat de hele sprite op 1× en 2×, op licht en op donker.
- `voorbeeld_top5.png`: alleen ter illustratie. Het is ronde 14 naast ronde 14 + de top 5 (14 px), om te laten zien dat de reparaties werken. Het is géén nieuwe sprite.
- `full12.png`: tussenstand (al aanwezig).

## Scripts
- **Open randen:** 0. Aan transparant grenzen alleen K, d en de kroonomlijning p. In totaal 15 kleuren + transparant; 1624 px.
- **Losse pixels, per kleurgroep:** alleen (29,24), de glans van het nabije oog. Die is bewust.
- **Losse pixels, per exacte tint** (34 stuks, waarvan de meeste bewust: vlekken, glans, iris). Deze zijn wél slordig:
  - (34,19): oranje o alleen in het rood;
  - (15,34) en (15,38): lichtgoud c-stippen in de schacht;
  - (16,47), (17,47), (18,47): c, b en a naast elkaar onder de hand;
  - (28,54): f, de staartaanzet (bevroren).
- **Kleuren buiten hun onderdeel:**
  - paars staat op de omlijningsplek (48,19), als staafje (46–48,19) direct boven de vleugelpunt;
  - het paarse kwastje (9–10,28–30) hangt los onder een rand die van (10,23) tot (10,27) d is in plaats van p.
- **Jaggies:**
  - kroon rechtsboven, rij-eindes 34,37,38,40,41,42,44 (segmenten 3-1-2-1-1-2);
  - de vleugelpunt is een hoek: 4 horizontaal (51–54,18) op 5 verticaal (54,18–22);
  - de flank is recht: x38 over y37–41 en x39 over y42–45.
- **Banding:** de flank is opgelost; de lijfbasis is nog maar 1 px (x32) en loopt uit. De diagonale strepen in de vleugel (4-4-3-3-2-3-2 per rij) zijn bedoeld als penscheiding.

## Oordeel per onderdeel
| # | Onderdeel | Oordeel | Plek en reden |
|---|---|---|---|
| A | Kroon: omtrek en patroon | **FAIL** | De gouden boog (7 vlekken, (15,14)→(41,14)) en de 9 L-vormige randkwastjes zijn netjes en symmetrisch. Wel fout: **1** paars staafje (46–48,19) met (48,19) op de plek van de zwarte omlijning, precies boven de vleugelpunt (Jordi's klacht; ronde 14 haalde (46,20) en (45,21) weg, maar deze rij bleef staan). **2** Los oranje (34,19) in het rode midden. **3** Jaggies rechtsboven (38–44,3–7); de kroonomtrek is bevroren. |
| B | Kroon: linkerlap en kwastje | **FAIL** | **4**: de paarse rand stopt bij (9,22), de lap loopt verder met een d-rand (10,23–27) en daaronder staat ineens weer paars (9–10,28–30). Op 1× leest dat als een los paars haakje links onder de kroon. |
| C | Gezicht: verre (linker) oog | **FAIL** | **5**: het lid (23–24,23), de pupil (23,24) en de iris (24,24) zijn goed. De "reflectie" a op (23,25) leest als een bruine veeg tussen het oranje (22,25) en de snavel (24,25). Een reflectie zonder glans aan de schaduwkant heeft geen lichtlogica. De iris c raakt de snavel s (25,24). |
| D | Gezicht: nabije oog + oorschijf | **FAIL** | **6**: het oog zelf is in orde (lid (30–31,23), glans e (29,24), pupil (30,24), iris c (31,24), warme reflectie a (30,25)). Maar de iris c (31,24) raakt diagonaal de oorschijf c (32,25), en die loopt door met b (32,26) en a (32,27). Op 12× en 1× is dat één gele streep van oog naar oor. |
| E | Gezicht: snavel | PASS | Een bleke rug schuin naar de punt: (26–27,22) → (26,24) → (25,25) → punt s (24,26), met een donkere mondlijn (27,25) en (25,26). Leest op 12× als haaksnavel. Op 1× is hij een grijswit druppeltje (zie smaak: kopmaat). |
| F | Opgeheven rechtervleugel | **FAIL** | De vorm, de buitenomlijning (segmenten 5-3-1-1-1-1 → 2-2-3) en de pennen zijn netjes. Wel fout: **7** spikkels op de onderarm: rij 31 (37–41) is d-m-d-m-d, (42,29) is een losse l tussen m, (46,29) een m tussen d. Leest als ruis, niet als veren. **8** Dubbele zwarte omlijning (44–45,24) + (45,23) aan de binnenrand. De hoek van de vleugelpunt (51–54,18) is smaak (Jordi: "merk je bijna niet"). |
| G | Linkervleugel met hand | **FAIL** | De vuist is schoon: één diagonale vingerscheiding (17,43)–(19,45) en een lichte knokkelrij (14–16,42). Wel fout: **9** een zwarte klont onder de hand: (14,46), (14,47) en (15,47) zijn K en (15,46) is d. Dat is in feite 2×2 donker; het stond al als FAIL 16 in de vorige keuring. |
| H | Staf: punt | PASS | Spits: zwarte top (15,16), 1 px c met d links en K rechts (rij 17–20), dan uitlopend naar de ruit. Steekt af tegen de kroon. |
| I | Staf: ruit, kraag, schacht | PASS (klein punt) | De ruit (13–17,21–25), de roestkraag (12–17,26–28) en de schacht b\|f met licht links zijn consistent. **11** (klein): losse c-stippen (15,34) en (15,38) in de schacht, en de zwarte rechterrand van de schacht breekt bij (17,36) (m tussen K erboven en d eronder). |
| J | Staf: overgang naar het lijf | **FAIL** | De gebogen zwarte scheiding (19,47) → (19,48) → (17–18,49) werkt (Jordi's krabbel is opgelost). Wel fout: **10** het stompje onder de hand is c-b-a op 3 losse pixels naast elkaar (16–18,47), met f f eronder. Dat is een andere opbouw dan de schacht erboven (b\|f, 2 px) en leest als een goudklompje, niet als dezelfde staf. |
| K | Lijf | PASS | Licht linksboven (l op de schouder (22–25,28–33)), schaduw rechts. De banding uit de vorige keuring is weg. De rechte flank is smaak/bevroren. |
| L | Buik | PASS | Ovaal, c linksboven, b, en a als schaduw rechts. De a-rand links (x20) is interne omlijning, geen kussenschaduw. |
| M | Poten | **FAIL** (twijfel) | Beide poten hebben dezelfde opbouw (d links, kleur, K rechts), met een zoomrij op y56 en voeten met een gesloten zwarte onderrand. Wel twijfel: **12** de buik a (26–27,52) loopt zonder scheiding over in de linkerdij (25–28,53), terwijl de rechterdij met een d-rij (30–33,52) van het lijf gescheiden is. Daardoor loopt de buik links door in de poot. Dit raakt de bevroren buik en poten, dus het is een vraag voor Jordi. |
| N | Ruimte tussen de poten | PASS | Schoon: (27–29,56–61) is helemaal transparant; alleen de bewuste staartaanzet f (28,54) en K (28,55) staan er. |
| O | Leest op 1× | PASS (met smaakpunt) | Kroon, staf, vleugel, buik en poten lezen allemaal. Het gezicht is op 1× klein (zie smaak). |

**Totaal: 7 PASS, 8 FAIL.** Alle FAIL-punten zijn netheidspunten van 1 tot 5 px; geen enkele vraagt om een nieuwe vorm.

## Controle van de FAIL-punten uit `EINDKEURING.md` (ronde 12)
| Vorige FAIL | Nu (ronde 14) |
|---|---|
| 6 leest op 1× als vogel | Beter (gezicht 2 rijen, haaksnavel), maar de kop blijft klein; dat is een silhouetkeuze. |
| 10 kopverhouding | Niet veranderd (silhouet, smaak). |
| 11 ogen | Grotendeels opgelost: lid, glans op de lichtkant en reflectie bij het nabije oog, lid bij het verre oog. Nieuw rest: veeg (23,25) en de koppeling iris-oorschijf (punten 5 en 6). |
| 12 snavel | Opgelost op 12× (schuine rug); op 1× klein. |
| 16 klont en drup | Drup opgelost. **De klont onder de hand (14–15,46–47) is niet opgelost** (punt 9). |
| 17 jaggies en zigzag onderrand | Zigzag onderrand opgelost ((45,22) is nu K). Jaggies rechtsboven niet: bevroren kroonomtrek. |
| 18 hoeken en rechte stukken | Niet veranderd (vleugelpunt en flank; Jordi vond het niet nodig). |
| 21 banding flank | Opgelost (1 px lijfbasis die uitloopt). |
| 22 hooglicht romp | Ongeveer gelijk; voldoende voor een donkere soort. |
| 24 ruis | Hand opgelost (één vingerscheiding); stray (17,19) en los rood (45,22) zijn weg. Nieuwe ruis op de onderarm van de rechtervleugel (punt 7). |
| 27 stafpunt zichtbaar | Opgelost. |

Jordi's drie klachten over ronde 13:
- Poten en de ruimte ertussen: opgelost. Wel blijft twijfel 12 over.
- Linkeroog: grotendeels opgelost; punt 5 rest.
- Paarse pixels boven de rechtervleugel: **niet helemaal opgelost.** Er staan nog drie paarse pixels op (46–48,19), waarvan (48,19) in de omlijning.

## Eindoordeel: **nog niet af**
Het is dichtbij. De top 5 hieronder (14 px) maakt van elke FAIL behalve 4 (keuze) en 12 (bevroren) een PASS; zie `voorbeeld_top5.png`.

## Top 5 reparaties (klein, precies; geen bevroren keuze geraakt)
1. **Paars boven de vleugel:** (48,19) p → K. De paarse rand eindigt dan, net als erboven, op x46–47 bij de gouden randvlek.
2. **Ogen schoon:**
   - (23,25) a → o, zodat er geen bruine veeg meer onder het verre oog zit;
   - (32,25) c → m, zodat de iris (31,24) los staat van de oorschijf; die wordt dan b/a op (32,26–27).
3. **Staf onder de hand en klont:**
   - (16,47) c → b en (18,47) a → f, zodat het stompje dezelfde b\|f-opbouw krijgt als de schacht;
   - (14,47) K → transparant, zodat de klont weg is en de onderrand van de hand diagonaal (14,46) → (15,47) loopt.
4. **Rechtervleugel opschonen:**
   - (38,31) en (40,31) m → d, en (42,29) l → m: dan zijn de spikkels op de onderarm weg en loopt de tint geleidelijk;
   - (45,24) K → l: de dubbele binnenomlijning is weg.
5. **Losse pixels:**
   - (34,19) o → r;
   - (15,34) en (15,38) c → b;
   - (17,36) m → d, zodat de rand rechts van de schacht doorloopt.

## Smaakpunten (voor Jordi, geen FAIL voor de techniek)
- **Kroonlap links (punt 4).** Er zijn twee nette oplossingen:
  - de rand doortrekken: (10,23–27) d → p, dan hoort het kwastje bij de rand, maar is er meer paars;
  - het kwastje weghalen of donker maken: (9–10,28–30) → d/K, dan is er geen los paars meer.

  Ik zou de tweede kiezen, gezien Jordi's afkeer van losse paarse pixels. Het blijft wel een kroonkeuze.
- **Buik loopt in de linkerdij (punt 12):** dat lost (26–27,52) a → d op, maar het raakt de bevroren buik.
- **Kop/gezicht klein op 1×:** dat is een silhouetkeuze ("ja, zolang de verhoudingen goed blijven").
- **Kroon rechtsboven 1 px gladstrijken** (rij-eindes 37,39,41,42,43,44): raakt de bevroren kroonomtrek.
- **Vleugelpunt-hoek en rechte flank:** volgens Jordi merk je ze bijna niet.
- **Staartaanzet (28,54):** één roestpixel. Dat is bevroren ("hele lichte hint"), maar op 1× leest het als vuiltje.
- **Opgeheven vleugel zonder slagpenpunten:** op 1× een gladde bruine knots/flipper (de Empoleon-flipper is bevroren). Naast Staraptor en Braviary is dat de minst vogelachtige vorm.
- **Goud overal** (buik, poten, staf, kroonvlekken): samenhangend, maar poten en buik lopen daardoor in elkaar over.
