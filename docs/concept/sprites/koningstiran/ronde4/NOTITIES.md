# Sapa Inca – ronde 4 (kleine bewerking op ronde 3)

Basis: `ronde3/sapa_inca.png` met de 2 staartpixels van de coördinator op (28,54) t en (28,55) r; die staan er nog. `sapa_inca.txt` begint met dat volledige raster, en de wijzigingen staan onderaan in het blok "ronde 4". Verder: `bouw.py`, `controle4.py` (diff per zone t.o.v. ronde 3), `vel.py` → `vel.png` (gezicht op 10× en linkerkant op 6× naast ronde 3), `kijk.py`. Draaien vanuit de repo-root.

Jordi: "de vleugel om de staf heen mag iets minder recht, iets meer als de vleugelvorm die we hanteren. De staf mag nog iets meer op een staart lijken. Linkerpoot sluit niet lekker aan op het lichaam tov de rechter, gezicht is nog net iets te klein." Daarna: "gaat vooral om de ogen die moeten pokemon stijl zijn, mogen klein hoor, maar wel duidelijk pokemon stijl" en "hij heeft daar wel iets te lieve ogen".

## Ogenstudie (Gen 3-front, 8–12×)
| Soort | Grootte | Opbouw |
|---|---|---|
| Honchkrow | 3×2 | zwart bovenlid, rode iris van 2 px, witte glans van 1 px ernaast, in een wit gezichtsvlak |
| Murkrow | 3×2 | rode iris met witte glans, zwart eromheen, geen oogwit |
| Corviknight | 2×2 | rode iris + roze glans van 1 px, schuin donker lid in de kopkleur |
| Staraptor | 3×2 | zwarte wenkbrauw/lid die schuin naar de snavel zakt, wit + rood oog eronder (strenge, trotse blik) |
| Swellow | 3×2 | donkerrood lid (kopkleur), glans + zwarte pupil, smal |
| Talonflame | 4×2 | zwart masker als vlak bovenlid, gele iris hoog onder het lid, zwarte pupil, witte glans van 1 px ernaast (trots) |
| Braviary | 3×2 | wit gezicht, donkere iris onder een schuin lid |
Conclusie: trots = een vlakke, donkere bovenrand die naar de snavel zakt, een gekleurde iris hoog onder het lid, een pupil met glans van 1 px en geen ronde iris met witte vlek (= lief). Het lid heeft de kleur van de kop en er is geen brilring.

## Wat er veranderde
1. **Vleugel om de staf:** de rechte kolom en de vuist zijn weg. Nu loopt een schuine bovenarm van de schouder naar een knik in de pols links (x12, y41–43), met een bolle achterrand terug naar de punt rechtsonder. Twee schuine penscheidingen (K) lopen naar de punt, die licht gekarteld om de staf vouwt. Het is dezelfde vleugeltaal en dezelfde tinten (m-rand, d-vulling, K-pennen) als in ronde 2/3 en de rechtervleugel.
2. **Staf meer staart:** van boven naar onder taps (5 px bij de zon, 4, dan 3 bij de hand). Gouden schacht (y) met de roestbruine vaan (t) aan beide kanten bovenin. De zonneschijf blijft het waaierende uiteinde, en onderaan blijft de roestbruine veer die achter het donkere lijf verdwijnt (ongewijzigd).
3. **Linkerpoot:** opgebouwd zoals de rechterpoot. Een vouwrij (a) onder de buik laat de dij uit het lijf komen; de dij is 4 px breed met een rechte linkeromtrek, en de onderrand sluit met K. De scheen is nu 3 px breed en staat onder het midden van de dij (was 2 px aan de linkerrand); de voet is ongewijzigd.
4. **Ogen (gezichtsmaat van ronde 3, niet vergroot):** donker bovenlid (d) in koptint, dat naar de snavel toe overgaat in rood (r). Daaronder een gouden iris (y) aan de snavelkant, een zwarte pupil en een glans van 1 px (w) aan de buitenkant van het nabije oog; het verre oog is iris + pupil zonder glans. De rode rij tussen kroon en oog blijft. Vergroten bleek voor deze ogen niet nodig.

## Diff t.o.v. ronde 3 (`controle4.py`)
| Zone | Gewijzigd |
|---|---|
| kroon | **0 px** |
| gezicht | 7 px (alleen de ogen) |
| opgeheven rechtervleugel | **0 px** |
| buik | **0 px** |
| rechterpoot + de 2 staartpixels | **0 px** |
| linkerpoot | 16 px |
| staf + zon | 15 px |
| linkervleugel + opvulling | 49 px |
| rest | 0 px |
- Alpha t.o.v. ronde 3: +20 / −6 px (verbreding van de staf, pols links, scheen); totaal 1627 px.
- Grensrandjes: geen; de buik en de rechterpoot zijn bewezen 0 px.
- Staf-eind: (18,49)–(19,50) roestbruin, rechts ervan K en dan het donkere lijf (d); de buik ligt 3–5 px verder.
- 15 kleuren + transparant; aandeel zwart 0,13; **0 open randen** (de dunne linkerscheen heeft nu een a-omlijning).

## Zelf gekeken (1×, 4×, 6× en 10× naast ronde 3)
- De vleugel leest als gesloten vleugel om de staf (pols, pennen), niet meer als vuist. De linkerpoot staat net zo in het lijf als de rechter.
- De ogen ogen kleiner en strenger dan in ronde 3: vlak donker lid, goud oog, niet rond en niet boos.

## Eerlijk: wat nog niet klopt
- **Ogen zijn klein** (iris + pupil 2–3 px); op 1× lees je vooral twee gouden puntjes onder een donkere streep. Trotser dan ronde 3, maar het verre oog zonder glans kan op 10× wat dof ogen.
- **Staf als staart:** de vaan aan beide kanten maakt hem bovenin roestbruin met een gouden middenstreep; op 1× leest hij eerder als een gouden staf met bruine randen dan als staartveer. Het onderste veerdeel is nog maar 5 px.
- **Vleugel:** de bovenarm overlapt de staf vanaf rij 37, waardoor die tussen rij 37 en 49 onzichtbaar is. Daardoor lijkt de hand de staf vrij hoog vast te houden.
- Het staartpuntje (2 px van de coördinator) is op 1× bijna onzichtbaar; dat is bewust ("hele lichte hint").

## Lessen
- Trotse ogen in 2–3 px: een donker lid in koptint, vlak en zakkend naar de snavel, met de iris direct eronder; een ronde gekleurde iris met witte glans in het midden leest lief.
- Bij een overlappend deel altijd per zone diffen: twee keer overschreef een nieuwe vleugelrij net één randpixel van de bevroren buik (x20 y40, x23 y48).
- Een 45°-trap van 5 px als vleugelrand leest recht; één sprong van 2 px in de reeks (17,16,14,13,13) maakt hem bol.
