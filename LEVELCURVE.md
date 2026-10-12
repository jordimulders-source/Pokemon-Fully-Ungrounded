# Levelcurve (9 okt)

> **12 okt:** inhaal-EXP milder (Jordi: inflatie aan het begin): +25% per level achterstand, max. ×3 (was +100%, max. ×10). Hoofdpad nu +1,5 tot +3 boven elke gymleider, Steven −0,7. Zie de changelog ([v1.0.0], testrun).
> **12 okt (2):** het hoofdstuk vóór Roxanne staat weer op de levels van vóór deze revisie (Roxanne ace 18, Route 102 trainers 6–8, wild 6–8): het begin hoeft niet te stijgen (weinig nieuwe content), de curve loopt pas daarna geleidelijk op. Hoofdpad: Roxanne +2,1, Brawly +1,3, Wattson +1,9.
> **12 okt (3), geldend:** regulier spelen = een paar levels ónder de gymleider (Jordi). Inhaal-EXP alleen als vangnet (onder ace − 9); gymleiders en bossgevechten opgehoogd tot ace ≈ team + 2,5. Hoofdpad: gyms −1,8 tot −3,0, E4 −3,6, Steven −6,5; met alle zijcontent nergens boven de ace. Details in de changelog.

Vraag van Jordi: door alle nieuwe trainers en grotere teams loopt een reguliere speler ver voor. Daarna (feedback): **de E4 rond lv 80, Steven ace 84, de sterkste superbosses op 100; grinden is een no-go; extra content is het alternatief voor grinden; variatie in teams moet worden aangemoedigd.** Ronde 3: grap-teams, wilde Pokémon en legendaries schalen mee; advies over evolutielevels.

## Ontwerp in één alinea
Het **hoofdpad alleen** brengt je zonder grinden net boven elk doel (ace van de volgende gymleider/E4/Steven). **Extra content** (zijgebieden, optionele trainers) geeft marge, of houdt een grotere rotatie van Pokémon op niveau. Twee knoppen:
- **Trainer-EXP 50%** (er zijn ±2100 trainer-Pokémon tot de kampioen).
- **Inhaal-EXP:** een Pokémon onder het ace-level van de volgende mijlpaal krijgt +100% EXP per level achterstand (max. ×10). Erboven verandert er niets, dus geen levelcap. Na de Hall of Fame is het doel 100, zodat je lage Pokémon in de post-game snel optilt.

Hetzelfde doel is ook de **gehoorzaamheidsgrens**. Wilde Pokémon, statics en legendaries volgen dezelfde curve.

## Methode
Script: `python3 tools/grounded/levelcurve.py [--profile hoofdpad|compleet6|completionist] [--postgame]` (parsers in `levelcurve_data.py`).
- **Route:** het Emerald-verhaal in hoofdstukken (tot en met elke gym, E4, kampioen; met `--postgame` daarna alle post-game-trainers oplopend en de superbosses). Alle trainers op de kaarten (`scripts.inc`, geen rematches, één rivaalvariant). Trainers die nog te hoog zijn (water op vroege routes) schuiven door tot hun mediaan ≤ ace + 3.
- **Wild:** 6 wilde gevechten per kaart (gewogen naar de slotkansen), inclusief vangen.
- **EXP zoals de engine:** Gen 5 geschaald, Gen 5-verdeling met twee Exp. Shares (Birch vóór gym 1, Mr. Stone), `B_TRAINER_EXP_PERCENT`, inhaal-EXP (`src/caps.c`).
- **Profielen:**
  - *Hoofdpad*: alleen het verhaal, vast team van 6, EXP evenwichtig verdeeld.
  - *Alle content, 6*: plus alle zijgebieden vóór de E4 (Toadstool Hollow, Dojo/Towers, Fortree Jungle, Mangrove Mire, Rocket Hideout, Scorched Slab, Route 135/136, Beacon Isle, Ghost Ship, Shipwreck Shoals, Hermit Crater, Koraalkathedraal, Whirl Island, onderwater, Meteor Falls-tunnels, VR-kluizenaar).
  - *Alle content, rotatie van 12*: hetzelfde met 12 Pokémon. Gemeten: het gemiddelde van de sterkste 6.

## Resultaat
Grafieken (scratchpad): `levelcurve_levels.png` en `levelcurve_verschil.png`. Getal tussen haakjes = team (sterkste 6) − ace.

| Mijlpaal | Ace vóór | Team vóór | Ace na | Hoofdpad (6) | Alle content (6) | Alle content (12 rotatie) |
|---|---|---|---|---|---|---|
| Roxanne | 16 | 22.7 | 23 | 25.5 (+2.5) | 25.5 (+2.5) | 25.5 (+2.5) |
| Brawly | 22 | 26.4 | 26 | 28.6 (+2.6) | 28.8 (+2.8) | 28.8 (+2.8) |
| Wattson | 25 | 34.5 | 34 | 37.3 (+3.3) | 37.4 (+3.4) | 36.6 (+2.6) |
| Flannery | 29 | 42.3 | 45 | 49.2 (+4.2) | 49.4 (+4.4) | 48.2 (+3.2) |
| Norman | 35 | 45.2 | 47 | 50.1 (+3.1) | 50.3 (+3.3) | 49.0 (+2.0) |
| Winona | 43 | 52.6 | 55 | 58.4 (+3.4) | 60.4 (+5.4) | 58.0 (+3.0) |
| Tate & Liza | 49 | 62.0 | 66 | 70.8 (+4.8) | 70.9 (+4.9) | 68.1 (+2.1) |
| Wallace | 56 | 69.7 | 76 | 80.4 (+4.4) | 82.0 (+6.0) | 78.7 (+2.7) |
| E4 (Drake) | 66 | 73.5 | 81 | 85.1 (+4.1) | 85.9 (+4.9) | 84.0 (+3.0) |
| Steven | 70 | 73.7 | 84 | 85.1 (+1.1) | 86.0 (+2.0) | 84.1 (+0.1) |
| Superbosses | — | — | 100 | 100 (0) | 100 (0) | 100 (0) |

- **Vóór:** het team liep 7–14 levels voor op de gymleiders en 10–25 op de routetrainers.
- **Na:** het hoofdpad zit bij elke mijlpaal 1–5 boven de ace, ook bij Steven en de superbosses; nergens grinden. Alle content met 6 Pokémon geeft meer marge. Een rotatie van 12 blijft op de curve.
- **Zonder inhaal-EXP** zakt de rotatie van 12 weg (−4 bij Flannery, −14 bij Steven, −25 bij de superbosses): de inhaal-EXP maakt teamvariatie mogelijk.
- **Waarom niet alleen levels omhoog:** met geschaalde EXP geeft een sterkere tegenstander ook meer EXP, dus de speler loopt mee. Een oplosser die alleen levels verhoogde, kwam uit op Roxanne 32 en de E4 op 99–100.

## Wat is aangepast
1. **EXP** (`include/config/battle.h`): `B_TRAINER_EXP_PERCENT 50` (was vast 150%), `B_GROUNDED_CATCHUP_EXP` met `B_CATCHUP_EXP_STEP 100` / `B_CATCHUP_EXP_MAX 900` (`src/caps.c`).
   - Het doel (`GetGroundedCatchUpTarget`) leest de ace uit het team van de volgende gymleider; na badge 8 is dat Steven, na de Hall of Fame 100.
   - Wilde EXP blijft 100%.
   - Emulatortests:
     - Lv 5 zonder badges: na twee wilde gevechten lv 6 (±×10 EXP).
     - **Post-game** (alle badges + `FLAG_IS_CHAMPION`): een Arceus lv 20 ging na één wilde Zigzagoon lv 20 naar lv 21. Zonder inhaal-EXP blijft hij volgens de berekening lv 20.
2. **Trainerlevels** (schaalregel per hoofdstuk; `solve()` in het script):
   - Gewone trainers +r tot de mediaan van (team − ace) ≤ +3.
   - Gymleiders tot team − ace ≤ +1,5. Gymtrainers schuiven mee met hun leider, maar blijven max. ace − 2.
   - Story-gevechten tot ≤ +2,5 (Zinnia op Sky Pillar −3).
   - E4 en Steven op Jordi's ankers.

   Totaal:

   | Hoofdstuk | Routes | Ace na |
   |---|---|---|
   | Roxanne | +6 | 23 |
   | Brawly | +6 | 26 |
   | Wattson | +8 | 34 |
   | Flannery | +12 | 45 |
   | Norman | +6 | 47 |
   | Winona | +17 | 55 |
   | Tate & Liza | +24 | 66 |
   | Wallace | +29 | 76 |
   | Victory Road / E4 | +28 | Sidney 78, Phoebe 79, Glacia 80, Drake 81 |
   | Steven | | 84 (team 81–84) |

   - Meegeschoven: rivaalvarianten, rematches `_2`–`_5` van gewone trainers, zijgebieden per regio of via de levelafbeelding.
   - Evoluties: 340 Pokémon geëvolueerd waar het nieuwe level dat vraagt. Niet bij sleutelgevechten, Stadium-personages, Jordi's eigen teams, bijnamen, Eviolite of als de ability niet past. Stadium-pool/omroeper: geen diff.
3. **Grap- en bewust lage teams schalen procentueel** met hun hoofdstuk (oud level × nieuw/oud van de routes daar: ×1,4–1,7). Zo blijven ze extreem laag ten opzichte van de rest. Magikarp blijft zoals hij was.
   - Ivan: Gyarados 3 → **4**, Pyukumuku/Arrokuda 12 → 18 (Magikarp 20 blijft).
   - Lyle: Scizor/Yanmega 6 → **9**, Scyther/Pinsir 10 → 15.
   - Edward: Abra's 15–60 → 21–84. Jaclyn: 16/24/37 → 22/34/52. Keccles (Route 115): 13–14 → 19–21.
   - Rose, Wade, Dalton, Deandre (Route 118 west): 20–21 → 31–32.
   - Chris (Magikarp + echt team): het echte team naar het hoofdstuk (39 → 51).
   - Laat in de game: Roger (Gyarados 35 → 60), Ronald (25–35 → 43–60), Andrew (Tentacool 10 → 17); de Magikarps blijven.
4. **Post-game** (samengedrukt in 83–100 op de ace: nieuw = 83 + (oud − 40)/3):
   - Tao-eiland 85–87, SS Tidal 84–87.
   - Pokémon Tower, Cerulean Cave, Chargestone Cave, National Park, Plasma Frigate, Nothing Island, Mega Forest, Tapu Isle, Glimwood Tangle/Ballonlea: 91–93.
   - Burglar (na de Hall of Fame) 92, Liberty Garden en Mirage Bazaar 94, Paradiso 95–96, Giovanni/Colress/Zinnia Delta 95.
   - **Precies 100:** Steven (Meteor Falls), Cynthia, Ghetsis, Archie/Maxie-taakstraf 4, alle gymleider-rematches `_5`, Wally VR_5. De andere rematches: `_2` 86, `_3` 90, `_4` 95.
   - **Dave, SickBlik, Mitch:** hebben nu geen post-game-gevecht. Dave praat na de Hall of Fame alleen op een ligstoel; SickBlik en Mitch vechten in Victory Road vóór de E4. Komt er een post-game-gevecht voor hen (Mitch na zijn thema), dan op **lv 100**.
5. **Wilde Pokémon** (`src/data/wild_encounters.json`: land, water, vissen, rock smash, onderwater):
   - Per hoofdstuk één afbeelding door twee punten: de mediaan van de routetrainers (oud → nieuw) en de ace van de mijlpaal (oud → nieuw); boven de ace dezelfde verschuiving als de ace.
   - Verhoudingen en zeldzaamheidsvolgorde in een tabel blijven gelijk (monotoon).
   - Kaarten buiten het hoofdpad via hun regio (Safari = Tate & Liza, Seafloor/Cave of Origin/Sky Pillar/onderwater = Wallace, Meteor Falls/Victory Road = E4 enz.).
   - Post-game-kaarten via de post-game-afbeelding. Magikarp blijft; Route 101 blijft zoals hij was (de starter is lv 5).

   | Kaart | Vóór | Na |
   |---|---|---|
   | Route 101 | 2–5 | 2–5 |
   | Route 116 | 10–13 | 15–19 |
   | Granite Cave 1F | 7–12 | 10–17 |
   | Route 110 | 12–15 | 17–21 |
   | Route 111 | 19–23 | 28–34 |
   | Route 115 | 30–50 | 46–66 |
   | Route 119 | 25–35 | 38–51 |
   | Route 120 | 28–38 | 43–52 |
   | Safari Zone North | 27–35 | 45–58 |
   | Mt. Pyre 6F | 33–42 | 55–63 |
   | Route 128 (surf) | 35–50 | 60–73 |
   | Cave of Origin B1F | 48–55 | 72–76 |
   | Victory Road B1F | 42–50 | 65–77 |
   | Cerulean Cave B1F | 65–70 | 91–93 |
   | Glimwood Tangle | 60–68 | 90–92 |

   **Evolutielevels in wilde tabellen:** ±650 slots hebben nu een soort die al 5+ levels over zijn evolutielevel is. Voor een deel was dat al zo, of het is een bewuste vangplek.
   - Wild lv 85–93 in de post-game: Cleffa en Elgyem in Meteor Space, Krabby/Poliwag/Goldeen (hengel) en Machoke in Cerulean Cave, Haunter in Pokémon Tower en Sky Pillar Reverse.
   - Fossielen lv 81–84 in de Desert Underpass.
   - Budew/Togepi/Solosis lv 69–71 in Cave of Origin.
   - Wynaut/Togepi/Bounsweet lv 60–70 op Route 130.
   - Sprigatito/Fuecoco lv 60 in de Safari.

   Advies: baby's en eerste stadia laat in de game vervangen door hun evolutie (of laten als bewuste "zeldzame basisvorm"-plek). Volledige lijst in `applied3.json` (scratchpad).
6. **Statics en legendaries** (`setwildbattle` in `data/maps/*/scripts.inc`, `forces.inc`, `kecleon.inc`):
   - Vóór de E4 dezelfde afbeelding als de wilde Pokémon van hun hoofdstuk.
   - Post-game (en alles vanaf lv 60) via de post-game-afbeelding: 60 → 90, 65 → 91, 70 → 93, 75 → 95.

   | Legendary / static | Plek | Vóór | Na |
   |---|---|---|---|
   | Volcarona | Mt. Chimney-top / Scorched Slab | 40 / 42 | 56 / 54 |
   | Entei, Raikou, Suicune | Mt. Chimney, New Mauville, Route 136 (badge 5) | 50 | 62 |
   | Regirock, Regice, Registeel | Braille-grotten (na Dive) | 40 | 69 |
   | Regidrago, Regieleki | Braille-grotten | 50 | 73 |
   | Manaphy | Sea Temple (badge 7) | 50 | 73 |
   | Spiritomb | Abandoned Ship | 45 | 57 |
   | Garchomp | Victory Road Shark Den | 58 | 81 |
   | Salamence / Minior | Meteor Falls Star Core | 55 / 48 | 80 / 74 |
   | Bagon, Deino, Carbink, Mienfoo, Minior, Lapras | Meteor Falls-krater | 20–22 | 30–33 |
   | Lapras, Bergmite, Eiscue | Route 135 | 33–36 | 50–51 |
   | Rotom | Mauville | 28 | 40 |
   | Kecleon, Voltorb/Electrode | Route 120 / 127, New Mauville, Aqua Hideout | 25–42 | 38–70 |
   | Lugia, Cresselia | Whirl Island / Fullmoon Island | 60 | 90 |
   | Munkidori, Okidogi, Fezandipiti | | 65 | 91 |
   | Rayquaza | Sky Pillar | 70 / 75 | 93 / 95 |
   | Kyogre, Groudon, Regigigas, Heatran, Volcanion, Jirachi, Darkrai, Shaymin, Celebi, Victini, Keldeo, Swords of Justice, Ruin-beesten, Tapu's, Forces, Zacian/Zamazenta, Xerneas/Yveltal, Reshiram/Zekrom/Kyurem, Zeraora, Genesect, Hoopa, Giratina, Ogerpon, Zarude | post-game | 70 | 93 |
   | Mewtwo, Eternatus | Cerulean Cave, National Park | 75 | 95 |
   | Sudowoodo | Battle Frontier | 40 | 83 |
   | Lavender-geesten | Lavender Town | 66–67 | 92 |

   `grounded_debug.inc` (debugmenu) is niet aangepast.
7. **Gymgidsen** noemen de nieuwe ace-levels (23/26/34/45/47/55/66/76).
8. **Gehoorzaamheid:** de grens is nu het ace-level van de volgende gymleider; zie hieronder.

The Spire staat los: rentals op vaste levels.

## Gehoorzaamheid (blijft erin, op vanglevel)
Sinds `B_OBEDIENCE_MECHANICS` GEN_8 kijken eigen Pokémon naar hun **vanglevel**. Doortrainen, inhaal-EXP en Rare Candies raken de regel niet; alleen vangen boven de grens, geruilde Pokémon en gifts.

**Nieuwe grens:** dezelfde als het doel van de inhaal-EXP, dus het ace-level van de volgende gymleider (`GetPlayerObedienceLevel` roept `GetGroundedCatchUpTarget` aan).

| Badges | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| Grens | 23 | 26 | 34 | 45 | 47 | 55 | 66 | 76 | geen |

De grens schuift zo vanzelf mee met de curve en de wilde levels.
- Emulatortests zonder badges: vanglevel 23 → 8/8 keer gehoorzaam; vanglevel 30 → 1/8.
- Let op: de intro-savestate van `testrom.py` had badges. Zet ze in een test eerst uit met `clearflag`.

**De Abra van Jordi's maat:** Abra komt alleen voor op Route 116 (toen lv 11–12), al vóór gym 1 bereikbaar. Zonder badges was de grens 10, dus die Abra was ongehoorzaam tot de eerste badge. Abra kent alleen Teleport, dus dat valt niet op. Pas als Kadabra (lv 16, vaak nog vóór Roxanne) echt aanvalt, zie je hem 'loafing around'. Nu: Route 116 is lv 15–19 en de grens zonder badges is 23, dus dit kan niet meer.

**Controle van alle wilde tabellen tegen de grens** (land met het aantal badges van dat hoofdstuk; Old Rod vanaf 1 badge, Good Rod/surfen vanaf 5, Super Rod vanaf 6):
- Overal binnen de grens, behalve:
  - **Route 115** (lv 46–66, al met 0–1 badges bereikbaar): bewust, daar is de gehoorzaamheid de rem.
  - Magmar op de Mt. Chimney-top (46 tegen 45).
  - Drie Super Rod-vangsten op Route 122–124 (67 tegen 66).
- Gifts (Lileep/Anorith 20, Grimer 22, Kubfu 22, Castform 25) vallen binnen de grens.

## Evolutielevels (advies; ingevoerd, zie onder de tabel)
De nieuwe curve ligt hoger dan in vanilla Emerald (team ±37 bij Wattson, ±49 bij Flannery, ±58 bij Winona, ±71 bij Tate & Liza). Daardoor komen evoluties in verhaaltermen al eerder dan in vanilla, ook op officiële levels. Jordi's verlagingen komen daar bovenop.

Hieronder sterke eindvormen (BST ≥ 500) die in dit project eerder evolueren dan officieel (bron: `species_info` van pokeemerald-expansion master). "Nu" = wanneer een speler op het hoofdpad dat level haalt.

| Evolutie | Project | Officieel | Nu (project) | Nu (officieel) | Vanilla-Emerald-curve (officieel) | Advies |
|---|---|---|---|---|---|---|
| Zweilous → Hydreigon | 53 | 64 | vóór Winona | vóór Tate & Liza | na de kampioen | 64 terug |
| Drakloak → Dragapult | 50 | 60 | vóór Norman | vóór Tate & Liza | na de kampioen | 60 terug |
| Dragonair → Dragonite, Pupitar → Tyranitar | 51 | 55 | vóór Winona | vóór Winona | vóór de kampioen | 55 (officieel) |
| Duraludon → Archaludon | 50 | item | vóór Norman | — | — | ±60 of item |
| Bisharp → Kingambit | 49 | leider-item | vóór Flannery | — | — | ±55 |
| Gimmighoul → Gholdengo | 45 | munten | vóór Flannery | — | — | ±55 |
| Larvesta → Volcarona | 40 | 59 | vóór Flannery | vóór Tate & Liza | na de kampioen | 59 terug (of ±55) |
| Fraxure → Haxorus | 43 | 48 | vóór Flannery | vóór Flannery | vóór de E4 | 48 |
| Vibrava → Flygon, Noibat → Noivern | 38 | 45 / 48 | vóór Flannery | vóór Flannery | vóór Wallace/E4 | 45 / 48 |
| Mienfoo → Mienshao | 30 | 50 | vóór Wattson | vóór Norman | vóór de E4 | 45–50 |
| Vullaby → Mandibuzz | 34 | 54 | vóór Wattson | vóór Winona | vóór de kampioen | 50–54 |
| Klang → Klinklang | 36 | 49 | vóór Wattson | vóór Flannery | vóór de E4 | 45–49 |
| Vanillish → Vanilluxe | 34 | 47 | vóór Wattson | vóór Flannery | vóór Wallace | 45–47 |
| Wailmer → Wailord, Lileep/Anorith → Cradily/Armaldo, Skorupi → Drapion, Ponyta → Rapidash | 30–32 | 40 | vóór Wattson | vóór Flannery | vóór Tate & Liza | 40 (fossielen krijg je op lv 20, nu evolueren ze vóór gym 3) |
| Archen → Archeops | 30 | 37 | vóór Wattson | vóór Wattson | vóór Tate & Liza | 37 |
| Grimer → Muk (alle vormen) | 30 | 38 | vóór Wattson | vóór Flannery | vóór Tate & Liza | 38 |
| Snorunt → Glalie | 32 | 42 | vóór Wattson | vóór Flannery | vóór Tate & Liza | 42 |
| Skiddo → Gogoat, Tentacool → Tentacruel, Hippopotas → Hippowdon, Cubchoo → Beartic | 26–28 | 30–37 | vóór Brawly | vóór Wattson | Flannery–T&L | officieel (30–37) |
| Machoke, Graveler, Gurdurr, Boldore → (ruil-evo's) | 37 | ruil | vóór Wattson | — | — | prima (ruilen bestaat nauwelijks), eventueel 40–45 |
| Golbat → Crobat, Chansey → Blissey, Riolu → Lucario, Munchlax → Snorlax, Roselia → Roserade | 30–36 | vriendschap/steen | vóór Wattson | — | — | prima als QoL; Blissey en Snorlax eventueel 40+ |

**Kort advies:**
- De pseudo-legendaries (Hydreigon, Dragapult) en Volcarona terug naar officieel. Die zijn nu al vóór Winona fully evolved, terwijl ze in vanilla post-game zijn.
- Mienshao, Mandibuzz, Klinklang en Vanilluxe (−13 tot −20 levels) terug naar ±officieel.
- Voor de rest is officieel genoeg. De hogere curve maakt fully evolved teams halverwege de game toch al normaal, en de trainers zijn daarop gebouwd.

### Ingevoerd (Jordi: "Eens wat betreft evolutielevels")
| Evolutie | Was | Nu |
|---|---|---|
| Zweilous → Hydreigon | 53 | 64 |
| Drakloak → Dragapult | 50 | 60 |
| Dragonair → Dragonite, Pupitar → Tyranitar | 51 | 55 |
| Duraludon → Archaludon | 50 | 60 |
| Bisharp → Kingambit | 49 | 55 |
| Gimmighoul (beide vormen) → Gholdengo | 45 | 55 |
| Larvesta → Volcarona | 40 | 59 |
| Fraxure → Haxorus | 43 | 48 |
| Vibrava → Flygon | 38 | 40 (Jordi's eigen revisie, zie onder) |
| Noibat → Noivern | 38 | 48 |
| Mienfoo → Mienshao | 30 | 48 |
| Vullaby → Mandibuzz | 34 | 52 |
| Klang → Klinklang | 36 | 47 |
| Vanillish → Vanilluxe | 34 | 46 |
| Wailmer → Wailord, Skorupi → Drapion, Ponyta (ook Galar) → Rapidash | 30–32 | 40 |
| Archen → Archeops | 30 | 37 |
| Skiddo → Gogoat / Hippopotas → Hippowdon / Cubchoo → Beartic | 26 / 28 / 28 | 32 / 34 / 37 (officieel) |

**Bewust blijven staan** (Jordi koos het level zelf in zijn "Pokémon Revisie" in de changelog):
- Grimer → Muk op 30 (v0.2.2 "Evolueert nu op level 30 naar Muk"; Alola- en Hoenn-Muk volgen dat).
- Lileep → Cradily en Anorith → Armaldo op 30 (v0.2.2 "evolved op lvl 30").
- Snorunt → Glalie op 32 (v0.2.2 Snorunt-lijn).
- Tentacool → Tentacruel op 27 (v0.2.1 Tentacool-revisie).
- Flygon: Jordi schreef 40 (v0.2.2 Trapinch-lijn), de code stond op 38; nu 40 in plaats van het advies 45.
- Ruil-evo's (Machoke, Graveler, Gurdurr, Boldore) en vriendschap/steen ongewijzigd.

**Gevolgen:**
- Trainers: 34 Pokémon onder hun nieuwe evolutielevel terug naar de voorvorm (o.a. Jeffrey/Kent/Cole: Larvesta, Nicolas: Drakloak, Abigail/Benjamin/Amy & Liv: Klang, Diana: Noibat/Vullaby, Shelby/Cora/Dojo: Mienfoo, Yasu/Keigo/Connor: Bisharp, Magma Hideout-grunt: Zweilous, Charles: Wailmer, Abigail: Skiddo, Sophie: Cubchoo). De Battle Stadium-teams (vast lv 50, `TRAINER_STADIUM_*` en `PARTNER_STADIUM_*`) zijn niet aangepast: dat is een lv 50-format waarin eindvormen normaal zijn.
- Wild: Wailord in de Route 103-hengeltabel (lv 32–37) is Wailmer; de Mienshao in de Rock Smash-tabel van Granite Cave B2F (lv 26–29, 1%) is Throh geworden (Mienfoo stond er al).

## Post-game wilde levels per evolutiefase
Jordi: "Post game wilde pokemon hoeven niet zo extreem hoog, misschien op hele sterke pokemon na cappen. Bijv dat een Budew of Togepi op lagere levels zitten dan evolved forms."

Toegepast op elk wild slot met `min_level` ≥ 80 (Spacetime, meren, Coronet, Yoshi's Island, Area Zero, Tao-eiland, Cerulean Cave e.d.; niet Victory Road/Ever Grande, niet de Magikarp van Route 103). Soorten, slots en kansen zijn gelijk gebleven; `setwildbattle` is niet aangeraakt.

| Fase | Levels | Binnen de band |
|---|---|---|
| Baby (Cleffa, Togepi, Budew, ...) | 55–60 | naar BST |
| Basisvorm die nog evolueert (Goldeen, fossielen, Larvesta, Duraludon) | 60–70 | naar BST; onder het eigen evolutielevel als dat ≥ 55 is (Larvesta 58, Duraludon 58–59) |
| Middenfase (Haunter, Gabite, Dragonair, Zweilous) | 70–80 | naar BST; onder het eigen evolutielevel als dat ≥ 60 is (Zweilous 62–63) |
| Eindvorm of losse soort | 80–90 | naar BST (400 → ±81, 560 → 90); stond hij al lager, dan blijft het oude level |
| Sterk (BST ≥ 580, legendary, paradox, pseudo-eindvormen, Slaking, Wailord) | ongewijzigd (85–94) | |

- 564 slots aangepast (463 eindvormen, 66 middenfases, 34 basisvormen, 1 baby; 72 sterke slots ongewijzigd). Babies volgen de baby-band, ook als de basisvorm een baby als voorvorm heeft (Clefairy, Chansey, Magmar tellen als basisvorm).
- EXP per wild gevecht (team lv 90): gemiddeld ±87% van vroeger; het minst in de Desert Underpass (59%, alleen fossielen), Meteor Space en Steam Island (60%), het meest in Area Zero/Steven's Cave (95–98%). `levelcurve.py --postgame` rekent in de post-game alleen trainers en verandert dus niet door deze wilde levels.

## Opnieuw draaien
Na nieuwe trainers of routes: `python3 tools/grounded/levelcurve.py --postgame` (tabel per mijlpaal; met `--profile completionist` de rotatie). `solve()` geeft de nieuwe verschuivingen.
