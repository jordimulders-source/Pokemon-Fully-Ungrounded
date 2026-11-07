# Hitmontop-evolutie: 3D-poppetje ronde 1 (5 nov)

Script: `pop3d_hitmontop_evo.py`. Het gebruikt de renderer van de lama (`lama/ontwerp/pop3d_lama.py`: render/shade/view) en
`olinguito_v2/silhouet_kolibriemethode/pop3d.py` (Model, chain, rotaties) en zet alleen een eigen kleurenschema. Draaien vanuit de repo-root, duurt ±6 s.

## Bron en opbouw
- **Pose = de foto, gespiegeld** (kop links). Alle punten staan in pixels van de gespiegelde foto (+ diepte) en worden met `W()` omgezet.
  Bij yaw 70 kijk je zoals de foto. Vel: `vel_pop_ronde1.png`, met de rode omtrek van A70 óver de foto (de pose valt erop; afwijkingen zijn de bewuste Pokémon-aanpassingen hieronder).
- Ledematen en romp zijn **doorlopende getaperde buizen** (catmull-rom door de foto-houding), geen losse bollen (les 159).
- **Kleuren uit Hitmontop's normal.pal**: huid 222,189,131, handen/hoorn 255,222,156, haar 131,90,41, wenkbrauw 180,139,90, broek 98,156,222 (zoom 74,115,197), voeten 139,189,238, klauwen 205,205,205, koordjes 197,74,49.

## Wat aangepast is t.o.v. de foto (SPEC)
- Kop ±2,3× de fotokop (Pokémon-verhouding; op 64 px ±14 px breed met haar), gekanteld zoals op de foto, gezicht naar de kijker; Hitmontop-ogen (groot, zwart, glans linksboven, zwaar lid).
- Haar: locs naar achteren gebonden (voorhoofd vrij) + rode haarband met een bundel van 4 dikke dreads die door de zwaartekracht omlaag hangen (Eddy Gordo).
- Kleine hoorn (lichte huidkleur) midden op de kruin, steekt net boven de locs uit.
- Broek: lang en aansluitend (dunner dan de wijde foto-broek), met een donkerblauwe zoom; daaronder een stukje bruine enkel (zoals de bruine Hitmontop-benen) en een blauwe voet met drie grijze klauwen, kleiner t.o.v. het been dan bij Hitmontop. Nabije voet geflexed (tenen omlaag), verre voet gestrekt, zoals de foto.
- Handen: rondjes; de steunhand is een bal op de grondlijn.
- Koordjes: cordão om de taille met knoop en twee hangende einden; prajiad om beide bovenarmen met hangende einden.
- Ledematen en romp 1,15× de foto-dikte (massa, leesbaar op 64 px).

## Standen
A70 = zoals de foto; B55 = 15° meer naar links; C40 = 30° meer naar links (yaw in de pop3d-conventie; 25° wordt bijna zijaanzicht, dan klapt de V-split dicht). Verschil tussen de standen is klein, omdat de split in het beeldvlak ligt; mijn voorkeur: **B55** (kop en borst iets naar links-voor, split blijft wijd).
64 px: `pop_70_64.png`, `pop_55_64.png`, `pop_40_64.png` (ruwe verkleining, figuur ±58 px hoog). 8×-vel: `vel_pop_ronde1_8x.png` (B55 naast de gespiegelde foto en Hitmontop).

## Zwakke punten (eerlijk)
1. **Lijf leest dun/slungelig** naast Hitmontop: op 1× is het vooral een blauwe V met een kop; Hitmontop is compacter en ronder. Mogelijk romp en heup nog voller, of benen iets korter dan de foto.
2. **Haar**: de locs lezen op 8× als krullen, maar de dreadbundel leest eerder als een paardenstaart; op 64 px is het een bruine vlek links van de kop. Eddy Gordo-gevoel is er nog maar half. Optie voor Jordi: bundel korter en dikker, of als opgebonden knot.
3. **Familie-gelijkenis** zit nu in ogen, kleuren, ronde handen en blauwe klauwvoeten; de brede "hoed"-vorm van de Hitmontop-kop is weg (SPEC vraagt een menselijkere kop met afro). Of hij direct als evolutie leest, moet Jordi beoordelen.
4. **Schouder vrije arm** geeft een bult bovenop de romp (zit ook in de foto), en de vrije arm valt op 64 px samen met het lijf (alleen de hand leest).
5. **Koordjes** rood: kleur staat open in de SPEC; de cordão-ring om de taille is nauwelijks te zien, alleen knoop + einden lezen. Prajiad op de steunarm leest als een rood bandje met een sliertje.
6. Hoorn steekt als puntje linksboven uit; "veel kleiner" is gehaald, maar hij kan als een feesthoedje lezen.
7. Geen gezichtsuitdrukking/mond (staat open in de SPEC).

Niet gedaan (bewust): geen silhouet, geen sprite; niet gecommit. `silhouet_r1/` is niet aangemaakt.

# Ronde 2 (5 nov): `ronde2.py` (importeert `pop3d_hitmontop_evo.py`)
Pose en standen bevroren (B55 hoofdstand, A70 ernaast). Vellen: `vel_pop_ronde2.png` (ronde 1 B55 ernaast, uitsneden, Hitmontop-kop als bron, 64 px, 1×/2× naast Hitmontop), `vel_pop_ronde2_8x.png`, `vel_pop_ronde2_dreads.png` (drie dreadvarianten). Los: `pop2_55.png`, `pop2_55_64.png`, `pop2_70_64.png`.

## Gedaan
1. **Kop = Hitmontop-kop**: lichte koepel (gezicht) op een brede, donkerder bruine platte rand met puntige zijkanten, naar de kijker gekanteld (lens zoals in de sprite); kop 1,15× groter dan ronde 1 (met rand ±1,5× zo breed). Kop hangt zoals bij Hitmontop omgekeerd: koepel boven, rand eronder, **kleine stompe hoorn** midden onder de rand (= kruin, wijst naar de grond). Schuine zwarte ogen met glans, dalende wenkbrauwen (boze Hitmontop-blik), kleine mond.
2. **Haar**: 5 dikke dreads (±3 px op 64) onder de rand vandaan, door de zwaartekracht omlaag, licht uitwaaierend, ongelijke lengtes; om en om eigen lijn. Geen paardenstaart/pony meer.
3. **Lijf**: romp + broek als één doorlopende volle buis (geen schouderballen), ledematen voller (armen ±4 px, dij ±8 px op 64), V-split even lang.
4. **Familiedetails**: blauwe voeten groter dan ronde 1 met drie **witte** klauwen; lichte ronde handen; **wit-grijze polsmanchetten** zoals bij Hitmontop; donkerblauwe zoom aan de broek.
5. **Cordão** dikker (ring r 28, knoop r 40, einden r 26→20), armkoordjes blijven.

## Eigen oordeel en zwakke punten (eerlijk)
- **Hoofdvraag half gehaald.** Het gezicht leest nu duidelijk als Hitmontop (ogen, wenkbrauwen, rand met punten). Maar **de dreads lezen als spinnen- of octopuspoten**. Ik heb drie opzetten geprobeerd: vanaf de voorrand (tentakels), kort onder de rand (uier/tepels) en halflang. Met dreads die van een omgekeerde kop omlaag hangen ontstaat steeds hetzelfde beeld. Volgens de regel "na 2 missers stoppen" heb ik niet verder gepatcht. **Dit is een ontwerpvraag voor Jordi/coördinator.** Opties:
  (a) dreads niet onder de kop maar **op de koepel**, naar achteren gebonden (het haar zit dan bovenop het gezicht). Bij een omgekeerde kop kan dat niet logisch omlaag hangen.
  (b) dreads als **dikke bundel vanaf één punt** (bij de hoorn), samengebonden met een koordje, één massa die omlaag valt. Dat leest minder als poten.
  (c) kop **rechtop** (koepel onder, rand boven; de kop draait dan zoals op de foto) met locs óp de rand als kroon. Dan wijkt de kop af van de Hitmontop-oriëntatie.
  (d) haar als een **afro-kroon van bollen rond de rand** (geen strengen). Dat is het minst Eddy Gordo.
  Varianten D1–D3 staan op `vel_pop_ronde2_dreads.png`.
- **Rand** is aan de rechterkant grotendeels verborgen achter de romp; alleen de linkerpunt leest. In de sprite is de rand juist het grote kenmerk.
- **Romp** heeft nog een borstbult (de romp wordt naar de schouders dikker, zoals de foto) en leest nog wat menselijk. Hij is nog geen "één vorm" zoals in de fanart.
- **Cordão-ring** om de taille valt grotendeels achter de vrije arm. Alleen de knoop en de einden lezen; dikker hielp maar een beetje.
- Een dread valt in D1 deels over de steunarm (bij B55 net vrij, bij A70 raakt hij).
- Op 1× is hij nog smaller en lichter dan Hitmontop. Leesbaar zijn: blauwe V, kop met rand, hand op de grond.
