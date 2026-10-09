# Levelcurve (9 okt, v0.9.18x)

Vraag van Jordi: door alle nieuwe trainers en grotere teams loopt een reguliere speler te ver voor. Simuleren, trainerlevels bijstellen, de gehoorzaamheid bekijken en voor-/tegenargumenten geven.

## Methode
Script: `python3 tools/grounded/levelcurve.py` (parsers in `levelcurve_data.py`).
- **Route:** het Emerald-verhaal in 10 hoofdstukken (tot en met elke gym, E4, kampioen) over de kaarten van het hoofdpad. Alle trainers op die kaarten (uit `scripts.inc`, zonder rematches, één rivaalvariant) worden verslagen. Een trainer die nog te hoog is (watertrainers op vroege routes) schuift door naar het eerste hoofdstuk waarin zijn mediaanlevel ≤ ace van de gymleider + 3. Post-game (mediaan boven de kampioen, Archie/Maxie-service, Wally VR_2, Zinnia Delta), Trick House en zijgebieden tellen niet mee.
- **Wild:** 6 wilde gevechten per kaart met wilde Pokémon (gewogen naar de slotkansen, gemiddeld level), inclusief vangen (Gen 6: vangen geeft EXP).
- **EXP zoals de engine:** Gen 5 geschaald (`((2L+10)/(L+Lp+10))^2.5`), Gen 5-split (vechters delen de helft, Exp. Share-houders de andere helft), trainerbonus, geen Lucky Egg/geruilde Pokémon. Twee Exp. Shares (Birch vóór gym 1, Mr. Stone na de brief).
- **Team:** groeit naar 6 (starter Medium Slow; vangsten op Route 102, Petalburg Woods, Granite Cave, Route 110, Route 111 met Medium Fast/Medium Slow/Slow), elk op het gemiddelde wilde level van die kaart. Strategie *evenwichtig*: de zwakste vecht, de twee volgende zwakste houden de Exp. Shares.
- Tot de kampioen verslaat de speler zo **±2100 trainer-Pokémon**. Rare Candies (22 in de wereld) zijn niet meegerekend.

## Resultaat
Grafieken: `levelcurve_verschil.png` en `levelcurve_levels.png` (scratchpad). Verschil = teamgemiddelde − level van de ace van de tegenstander, net vóór het gevecht.

| Mijlpaal | Ace vóór | Team vóór | Verschil vóór | Alleen EXP 50% | Ace na | Team na | Verschil na | Routetrainers na¹ |
|---|---|---|---|---|---|---|---|---|
| Roxanne | 16 | 22.7 | +6.7 | +1.9 | 18 | 19.0 | +1.0 | +2.6 |
| Brawly | 22 | 26.4 | +4.4 | +0.2 | 22 | 22.9 | +0.9 | +2.5 |
| Wattson | 25 | 34.5 | +9.5 | +3.0 | 28 | 29.3 | +1.3 | +3.1 |
| Flannery | 29 | 42.3 | +13.3 | +5.0 | 35 | 37.2 | +2.2 | +2.5 |
| Norman | 35 | 45.2 | +10.2 | +1.1 | 37 | 38.7 | +1.7 | −1.6 |
| Winona | 43 | 52.6 | +9.6 | −0.9 | 44 | 45.2 | +1.2 | +3.4 |
| Tate & Liza | 49 | 62.0 | +13.0 | +0.9 | 53 | 54.2 | +1.2 | +2.9 |
| Wallace | 56 | 69.7 | +13.7 | +0.5 | 61 | 61.9 | +0.9 | +2.8 |
| Drake (E4) | 66 | 73.5 | +7.5 | −6.6 | 66 | 64.9 | −1.1 | +1.8 |
| Steven | 70 | 73.7 | +3.7 | −10.5 | 70 | 65.0 | −5.0 | — |

¹ mediaan van (teamgemiddelde − ace) over de gewone trainers van dat hoofdstuk. Vóór de aanpassing was dat +8 tot +25 (Wallace-hoofdstuk: routes rond lv 40 tegen een team van 60+).

**Vóór:** de speler liep 7–14 levels voor op de gymleiders en 10–25 op de routetrainers. Story-gevechten (Lilycove-rivaal, Matt) lagen 16–20 levels onder het team.

**Waarom niet alleen levels omhoog:** met Gen 5-geschaalde EXP geeft een sterkere tegenstander ook meer EXP; de speler loopt dan gewoon mee. Een oplosser die alleen trainerlevels verhoogt, kwam uit op Roxanne 32, Flannery 60 en de E4 op 99–100: het gat zit in de hoeveelheid trainers, niet in hun level.

## Wat is aangepast
1. **Trainer-EXP 150% → 50%** (`B_TRAINER_EXP_PERCENT` in `include/config/battle.h`, gebruikt in `src/battle_script_commands.c`). Wilde gevechten blijven 100%: wie wil grinden, kan dat nog (en geschaalde EXP remt dat vanzelf af). Eén getal, makkelijk bij te stellen.
2. **Trainerlevels, schaalregel per hoofdstuk** (`solve()` in het script, alleen omhoog):
   - gewone trainers +r tot de mediaan van (team − ace) ≤ +3;
   - gymleider/E4/kampioen +d tot team − ace ≤ +1,5; gymtrainers krijgen +d (of +r als dat hoger is, maar max. ace − 2);
   - story-gevechten (rivaal, Wally, Birch, Dave, Maxie/Archie, Matt) +d tot team − ace ≤ +2,5.

   | Hoofdstuk | Routes +r | Sleutelgevechten |
   |---|---|---|
   | Roxanne | +2 | Roxanne +2, rivaal 103 +1 |
   | Brawly | +2 | — |
   | Wattson | +3 | Wattson +3, rivaal 110 +1 |
   | Flannery | +5 | Flannery +6, Wally (Meteor Falls) +2, Birch +1 |
   | Norman | +2 | Norman +2, Dave +2 |
   | Winona | +6 | Winona +1, rivaal 119 +3 |
   | Tate & Liza | +11 | T&L +4, Matt +10, rivaal Lilycove +6, Maxie (hideout) +4 |
   | Wallace | +15 | Wallace +5, Archie +5, Maxie (Space Center) +1 |
   | Victory Road/E4 | +10 | Wally VR +4, Sidney +1; Phoebe, Glacia, Drake, Steven ongewijzigd |
   - Meegeschoven: alle rivaalvarianten (May/Brendan × starter), rematches `_2`–`_5` van gewone trainers met dezelfde +r (gymleider-rematches niet), en zijgebieden met hun regio: Toadstool Hollow +2, Dojo/Towers op Route 112 +5, Fortree Jungle, Mangrove Mire, Rocket Hideout en Scorched Slab +6.
   - **Niet** verschoven: grap-teams (Ivan, Lyle en elk team met ≥ 10 levels spreiding: Andrew, Edward, Roger, Ronald enz.), bewust lage teams (> 8 onder de rest van het hoofdstuk, zoals Keccles op Route 115), Magikarp, Trick House, post-game, en de zijgebieden rond lv 41–54 (Tao, Beacon Isle, Ghost Ship, Hermit Crater, Meteor Falls-tunnels, onderwater): die passen nu vanzelf beter bij de lagere spelercurve.
   - **Evoluties:** een Pokémon die door de verschuiving over zijn evolutielevel (dit project) gaat, is geëvolueerd (165×). Niet bij sleutelgevechten, Stadium-pool-personages, Jordi's eigen teams (Calvin, Gabby & Ty, Miguel, Isaiah, Amy & Liv, Kira & Dan, Wally, Birch, Keccles, Zinnia, Colress, Mustard, SickBlik …), bijnamen, Eviolite-houders of als de ability niet past. Stadium-pool en omroeper ongewijzigd (`pool.py`/`announcer.py` geven geen diff).
3. **Gymgidsen** noemen de nieuwe ace-levels: Roxanne 18, Brawly 22, Wattson 28, Flannery 35, Norman 37, Winona 44, Tate & Liza 53, Wallace 61.

**Na:** elke gym ligt het team 1–2 levels boven de ace, routetrainers ±3 onder het team. De E4 en Steven zijn ongewijzigd (66/70), dus de post-game (lv 65–80) past nog. Bij Steven loopt het gemiddelde team 5 levels achter (ace-team 2–3): zo laat ik het, het is de eindbaas; wie wil, grindt op Victory Road.

**Gevoeligheid:** zonder wilde gevechten 1–2 levels lager, met 12 per kaart 1–2 hoger; zonder Exp. Share vrijwel gelijk. Wie alles met één Pokémon doet, heeft die 6–19 levels boven de ace (de rest blijft achter): dat is een keuze van de speler, geen fout van de curve.

## Gehoorzaamheid
Sinds `B_OBEDIENCE_MECHANICS` GEN_8 kijken eigen Pokémon naar hun **vanglevel**, niet naar hun huidige level. Doortrainen geeft dus nooit ongehoorzaamheid; alleen vangen boven de grens, geruilde Pokémon en gifts boven de grens.
- Grens per badge 10/20/30/…/80, na badge 8 geen grens. Getoetst tegen de wilde levels per hoofdstuk: alleen **Route 116 vóór gym 1** zat erboven (lv 11–13 tegen een grens van 10). **Aangepast: zonder badges 15** (`GetPlayerObedienceLevel`, `src/battle_util.c`). De rest past: gifts (Lileep/Anorith 20, Grimer 22, Kubfu 22, Castform 25) vallen binnen de grens van dat moment. Getest in de emulator (Arceus met vanglevel 15, geen badges, Dark Pulse + 3× Splash, 8 wilde gevechten): grens 10 → 4/8 keer gehoorzaam, grens 15 → 8/8.
- Bewust boven de grens (zo laten): Route 115 (lv 30–50, al bereikbaar met 1 badge) en hengels in het water van vroege routes. Daar is de gehoorzaamheid precies de rem.

### Eruit of erin laten?
**Voor eruit halen**
- Normaal spelen botst er na deze aanpassing toch al bijna nooit op (vanglevel-regel): de regel raakt alleen wie bewust iets sterks vangt, en is dan vooral irritant ("loafing around" is willekeur, geen keuze).
- Ruilen bestaat nauwelijks; het oorspronkelijke doel (geruilde lv 60 meenemen naar gym 2) speelt hier niet.
- SMT/Slay the Spire-filosofie: de speler krijgt tools. Een sterke vangst op Route 115 is zo'n tool die hij zelf verdiend heeft (zoeken, kans, ballen).
- Minder uitleg, minder tekst, minder frustratie; past bij "de game respecteert de tijd van de speler".

**Voor erin laten**
- Het is de enige rem op Route 115 (Blissey/Kangaskhan lv 35–50 met 1 badge) en op hoge hengelvangsten: zonder regel walst één vangst over drie gyms en is de nieuwe curve voor niets.
- Rare Candies en vitamines (meerdere tegelijk) raken de regel niet (vanglevel), dus die tools blijven werken.
- Het uitdagingsgevoel komt uit het team dat je *opbouwt*; badges krijgen een tastbare beloning ("nu luistert hij").
- De vanglevel-regel maakt hem al mild, en er is een waarschuwing bij een level-up boven de grens.

**Advies:** erin laten, met de mildere grens zonder badges (15). Alternatief als hij toch stoort: geen willekeur meer, maar een harde, voorspelbare regel (bijv. een Pokémon boven de grens luistert gewoon, maar krijgt minder EXP), dan blijft de rem zonder de frustratie. Dat is een designkeuze voor Jordi.

## Opnieuw draaien
Na grote wijzigingen in trainers of routes: `python3 tools/grounded/levelcurve.py` (tabel per mijlpaal). `solve()` geeft dan de nieuwe verschuivingen; met de huidige data komen die uit op 0–2 levels.
