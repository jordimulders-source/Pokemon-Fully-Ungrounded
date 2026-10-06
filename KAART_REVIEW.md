# Kaartreview: zee en regio (6 okt 2026)

Methode: script over alle 613 `map.json` (grootte uit layouts.json, trainers = `trainer_type`, items = item-ballen + `hidden_item`, NPC = overige objecten, warps, encounters uit wild_encounters.json) + Town Map-raster (28x15). Let op: items zijn alleen zichtbare ballen en verborgen items; geschenken/beloningen via NPC's tellen niet mee. Tel-dichtheid = (trainers + NPC/2 + items) per 100 tiles.

## Kort antwoord
Exploreren is op de **zee zelf nog niet echt leuk**: Route 105-134 zijn 3200-6400 tiles open water met 3-9 zwemmers/vissers, 0-3 items en bijna geen NPC's of eigen plekken. Wat dat compenseert zijn de **zijkaarten** (nieuw in v0.9.110-116): daar is het erg goed. Het probleem is de verhouding: 1 bezienswaardigheid per ~4 routes, en de zeeroutes hebben allemaal hetzelfde sjabloon (Swimmers + Triathletes, 5 water- + 10 viskansen). Wél sterk: elke zeeroute heeft een eigen, thematische encountertabel (geen dubbelen), dus vissen/surfen levert variatie op.

## (a) Zee: wat er is en oordeel
| Gebied | Grootte | Inhoud (trainers / NPC / items / verborgen) | Bijzonder | Oordeel |
|---|---|---|---|---|
| Route 105 | 40x80 | 7 / 0 / 1 / 2 | Regirock-poort, Nothing Island vlakbij | mager |
| Route 106 | 80x20 | 4 / 0 / 1 / 3 | Granite Cave | mager-OK |
| Route 107 | 60x20 | 7 / 0 / 0 / 0 | alleen trainers | **leeg** |
| Route 108 | 60x20 | 6 / 0 / 1 / 1 | Abandoned Ship | mager |
| Route 109 | 40x63 | 14 / 9 / 2 / 6 | Paradiso Resort, Seashore House | leuk |
| Route 122 | 40x40 | 0 / 0 / 0 / 0 | alleen 1 warp (Mt. Pyre) | **leeg** |
| Route 124 | 80x80 | 9 / 1 / 3 / 0 | reuzen-Wailord, Whirl Island via onderwater | OK |
| Route 125 | 80x40 | 9 / 0 / 1 / 0 | Shoal Cave | mager |
| Route 126 | 80x80 | 8 / 0 / 1 / 0 | Sootopolis-duik, 6400 tiles | **leeg** |
| Route 127 | 80x80 | 8 / 0 / 3 / 0 | grot (Wellspring), 6400 tiles | mager |
| Route 128 | 120x40 | 7 / 4 / 0 / 3 | Zeetempel-duik, reuzen-Wailord | OK |
| Route 129 | 80x40 | 5 / 5 / 0 / 0 | Juans eiland | OK |
| Route 130 | 80x40 | 3 / 1 / 0 / 0 | Mirage Island (Wynaut) | mager |
| Route 131 | 60x40 | 8 / 0 / 0 / 0 | Shipwreck Shoals, Steam Island vlakbij | mager (route zelf) |
| Route 132 | 80x40 | 8 / 1 / 2 / 2 | eb en vloed | leuk |
| Route 133 | 80x40 | 7 / 0 / 3 / 0 | Drijvende markt | mager (route zelf) |
| Route 134 | 80x40 | 9 / 0 / 2 / 0 | Sealed Chamber, Manaphy/Volcanion-vis | mager |
| Nothing Island + Plasma Frigate | 44x40 | 3 / 1 / 0 / 0 (+ schip) | Genesect-quest | leuk |
| Shipwreck Shoals (+ spookschip) | 42x58 | 0 / 1 / 1 / 1 (+ schip 's nachts) | eigen tileset | leuk |
| Drijvende markt | 36x26 | 10 NPC | dagelijkse winkel | leuk |
| Steam Island (+ vulkaan) | 40x34 | 5 NPC, 0 trainers/items | hete bron, Volcanion | OK (geen item) |
| Paradiso Resort (4 kaarten) | 40x46 + 3 | 13+9+13+4 NPC | 5 post-game gevechten | leuk |
| Whirl Island (+ grot) | 40x40 | 0 NPC, 0 items | Lugia | **leeg** buiten de Lugia-grot |
| Zeetempel (hal + heiligdom) | 21x23 x2 | 1 NPC, 1 item | Manaphy, puzzel | OK |
| Juans eiland, Dewford-steiger | (in kaart) | NPC's | Juan, visserstoernooi | leuk |
| Onderwater 124/126/127 | 6400 elk | 7/8/4 verborgen items | 124 en 126 hebben encounters | OK |
| Onderwater 105/125/129/128 | 3200-4800 | 0-2 verborgen, **geen encounters** | | **leeg** |
| Eilanden Southern/Birth/Faraway | 900-1560 | 2 NPC, 0 items | alleen event-legendary | OK, maar kaal |

## (b) Top 10 lege of saaie plekken (hele regio)
1. **Route 126 + 127** (2x 6400 tiles, 16 trainers, 4 items, 0 verborgen): de grootste kaarten van het spel met een Swimmer/Triathlete-sjabloon.
2. **Route 122** (1600 tiles): 0 trainers/NPC/items; een verbindingsroute naar Mt. Pyre zonder reden om te blijven.
3. **Route 107, 131, 133** (1200-3200 tiles): 0 NPC's, 0-3 items, 0-1 verborgen; alleen trainers.
4. **Whirl Island buiten de Lugia-grot** (40x40): lagune met niets erop; Lugia-grot zelf is goed.
5. **Onderwater 105/125/129** en **128** (3200-4800 tiles, géén wilde encounters, 0-2 verborgen items): duiken levert niets op behalve routes naar andere dingen. Underwater 124/126 hebben tenminste 5 slots en 7-8 items.
6. **Ever Grande City** (3200 tiles): 0 NPC's/items buiten de League-poort; stadsbuurt zonder leven (post-game 'siege' mogelijk).
7. **Mt. Pyre Exterior, Navel Rock Fork, Desert Underpass** (1900-3200 tiles): 0-1 NPC, 0-2 items; grote kaarten zonder verhaal. Desert Underpass is 3197 tiles met 1 NPC.
8. **Southern Island / Birth Island / Faraway Island** (900-1500 tiles): elk 2 NPC's en niets te vinden tot de legendary.
9. **Safari Zone-deelkaarten, Meteor Falls Starfall Grotto, Fiery Path Heatran-hol** (1600-2000 tiles): 0-2 items, geen trainers (bewust voor safari).
10. **De regio als geheel**: op de Town Map zijn 252 van 420 vakken leeg (MAPSEC_NONE in het raster, vóór de extra mapsecs die een vak delen) (zie d); de zee zelf (Route 126-134) leent zich het best voor meer 'eilandjes'.

## (c) Ideeën per plek (stijl: droog-absurd, immersief)
1. **Route 126/127**: *drijvend afval-eilandje* ("The Great Pacifidlog Garbage Patch": boeien, een tv, een toegangsbewijs; gevonden items + een Trubbish-nest, 's avonds een zeehond die Pokéradio hoort; klein) + 4-6 verborgen items in zandbanken/rotsen (klein). Een **zeemijn-veld** met Voltorb/Electrode (zeldzaam, ontploffen: klein-middel).
2. **Route 122**: een **tolbrug-hut** met een ferryman (Pelipper-post) die tol vraagt: gratis passeren als je een aantal Water-types hebt, anders een grappig gevecht (klein) of het **Ghost Pier**, een kleine steiger die 's nachts naar Mt. Pyre loopt met een bruiloft van spoken (middel).
3. **Route 107/131/133**: elk een **bijzondere NPC op een eilandje** (klein): bv. een eenzame sushichef op een vlot (verkoopt voedsel/bessen), een bergingsduiker die vraagt om Heart Scales (cadeautje), een meteoroloog met een Castform-waarnemingspost.
4. **Whirl Island**: een **vuurtorenwachtershut** op het strand van de lagune (verhaal voor Lugia; tekst: de wachter heeft 1 jaar niet gesproken, zijn Slowpoke wel) + vijf items rond de lagune (klein-middel).
5. **Onderwater 105/125/129**: geef ze **5 water-encounters** per kaart (zeewier met unieke soorten uit de zee-tabellen, bv. 125 diepzee-Chinchou, 129 Dratini-vijver) en 3-4 verborgen items; plus een **zeemansgraf** (anker, schat). Klein per kaart, bijna alleen data.
6. **Ever Grande City**: inwoners en een **Victory-promenade** (fans, een hotdog-kar, Spoken-fotografen); post-game: rematch-NPC's van de Elite Four in de straat (middel).
7. **Mt. Pyre Exterior / Desert Underpass / Navel Rock Fork**: NPC's die verhalen vertellen en 3-4 verborgen items; Desert Underpass: een **fossielenopgraving** met 2 archeologen en een Armaldo-grap (middel).
8. **Southern/Birth/Faraway Island**: bij elk **een bezoeker die al sinds jaren weg is** (een verlaten kamp met brieven en 2-3 items; klein), zodat de reis ook zonder legendary iets oplevert.
9. **Safari Zone-deelkaarten / Starfall Grotto / Heatran-hol**: sterrenstof/stuk-meteoriet verborgen items, 1 bijzondere NPC (middel-klein).
10. **Route 130**: kaal (3 trainers). Een **Wynaut-kleuterschool** ('Wynaut Daycare, we are not responsible'; klein-middel) op de ring rond Mirage Island, plus een tweede eilandje met een Pokémon-fotograaf (klein).
Algemeen: **trainer-sjabloon doorbreken** (nu Swimmer/Triathlete overal): per route 1-2 afwijkende klassen (Sailor, Diver, Pokémon Ranger, Expert) of een grap-NPC; en **meer verborgen items** op de zee (ze zijn bijna overal 0-1).

## (d) Lege vakken op de Town Map (28x15)
Bezet: bijna alle routes + nieuwe gebieden (Nothing 0,10; Whirl 21,3; Steam 20,9; Floating Market 13,9; Sea Temple 24,10; Paradiso 9,14; Shipwreck 18-19,12; Southern Island 12,14; Battle Frontier 22,12; Mirage 17,10 delend met Pacifidlog).
Grote lege blokken, geschikt voor nieuwe eilanden:
- **Zuid-midden/zuid-oost, rij 11-14, x 13-27** (op Southern Island 12,14, Shipwreck 18-19,12 en BF 22,12 na): het **grote lege stuk onder Pacifidlog**, ongeveer 50 vakken. Beste plek voor 3-4 nieuwe eilanden.
- **Midden-zee, rij 7-9, x 9-19** (ook rij 4-5 x 17-19): ~30 vakken tussen Route 118/123 en 126/127. Geschikt voor 1-2 eilanden (bv. Tapu, Sootopolis-eilanden).
- **Oost-rand x 26-27** (rij 0-14) en **noordoost x 14-27, rij 0-2**: ~45 vakken, ver weg; geschikt voor een Dragon Island of een mist-eiland.
- **West-zee, rij 11-13, x 1-3 en 5-7**: ~15 vakken, tussen Route 105 en Dewford (Nothing Island zit er al 0,10).
- **Noordwest, rij 0-2, x 0 en x 2-5** en land-gaten (Rustboro-Fallarbor): binnenland; minder geschikt.
- Let op: Nothing Island (0,10) deelt zijn vak met Island Cave, Mirage (17,10) met Pacifidlog.

## (e) ZEE_PLAN.md: wat is nog niet gedaan
Gedaan: reuzen-Wailord, eb en vloed, Juans eiland, Plasma Frigate, Shipwreck Shoals, drijvende markt, stoomeiland, Paradiso Resort, zeetempel, Whirl Island, visserstoernooi.
**Nog niet** (uit "Ideeën van Jordi"):
1. **Sootopolis-eilanden** (idee 1): rond Sootopolis (rij 6-8, x 19-22 zijn Route 126/Sootopolis; lege vakken ligt in rij 7-9, x 9-19 en rij 4-5, x 17-19). Plaats: tussen Route 126 en 127, of ten westen van Route 126 (nu leeg open water).
2. **Tapu-eiland** (idee 2): vier Tapu's post-game; eigen eiland, bv. rij 11-13 x 24-27 (zuidoost, ver van het hart) of rij 7-9 x 12-16; Tapu-soorten zijn in het spel (gen_7_families.h) maar geen script/trainer gebruikt ze.
3. **Diepzeetrog** (idee 4): deels (Zeetempel in de trog onder 128); een echte "Mariana"-trog met eigen items/encounters ontbreekt. Plek: tussen Route 126 en 127 onder water (Underwater 126/127 zijn 6400 tiles met alleen verborgen items; 127 zonder encounters).
4. **Dragon Island** (idee 6): nog niet gedaan. Past in het zuidoosten (rij 11-14, x 24-27) of in de oost-rand. Thema sluit aan op de dragon-encounters van Route 129-131.
5. **Het grote lege stuk onder Pacifidlog** (idee 8): alleen Shipwreck en Southern Island staan er; de rest (rij 11-14, x 13-27) is leeg. Past voor Tapu, Dragon Island en 1-2 kleine eilandjes (een vuurtoren: staat al in het plan als "ja, maar eerst schets", **nog niet gemaakt**, Route 133/134 of rij 11, x 14-16).
6. Draaikolkeiland: Lugia gedaan; **Wishmaker-eiland** voor Jirachi niet (Jirachi blijft in Fallarbor, bewust besloten).
7. Strandresort/Juans eiland/visserstoernooi: gedaan; "Vragen" in het plan (hoofd- vs. troostprijs, echte vissen) staan nog open.
Open uit eerdere vragen: `GYM_INTRO_IDEEEN.md`, `CONTESTS_VOORSTEL.md`, vuurtorenschets.

## Aanbevolen volgorde (klein naar groot)
1. Data-werk zonder kaart: onderwater-encounters (105/125/129), extra verborgen items op 107/122/126/127/131/133, afwisselende trainerklassen (klein, 1 sessie).
2. Whirl-lagune-hut, Route 122 pier, kleine eilandje-NPC's (klein-middel).
3. Vuurtoren + Tapu-eiland + Dragon Island + Sootopolis-eilanden (groot elk; vuurtoren eerst schetsen).
