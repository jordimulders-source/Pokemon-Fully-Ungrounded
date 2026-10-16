# Testrun Jordi – bevindingen

Jordi speelt de 1.0 (ROM altijd `Pokemon_Ungrounded_1.0_testfix8.gba`, save blijft werken). Per bevinding: wat hij zag, wat we deden, status.
Status: ✅ opgelost · 👍 goed zo (geen actie) · ⏳ open · 💡 idee/later. Details van oplossingen staan in `CHANGELOG.md` onder [v1.0.0], "Testrun Jordi".

## Ronde 1 (12 okt): begin t/m Roxanne

### Speelgevoel en balans
| Wat | Bevinding | Status |
|---|---|---|
| Levelcurve begin | Mudkip te snel lv 8–9 (dubbele EXP door inhaal-EXP + hogere trainers). Inhaal-EXP is nu alleen vangnet (pas 9+ onder de volgende gym-ace); routes vóór Roxanne terug op de oude levels, daarna geleidelijk. | ✅ |
| Levelsprongen | Na Petalburg sprongen van 8–9 naar 12. Hele game per trainer gladgestreken (looprichting). | ✅ |
| Route 116 | Liep van 12 naar 15 door elkaar; nu 12 → 13 → 14 in looprichting. | ✅ |
| Johnson (6× Metronome) | Lv 15 te sterk (Lucario/Electabuzz), 2× verloren; nu lv 12. Kon in een dubbelgevecht belanden: van plek geruild met Joey (nu 3 Poochyena). | ✅ |
| Keccles 1 | Te hoog (19–21, vóór Roxanne te bevechten); nu 15, Salandit 17. | ✅ |
| Team vlak vóór Roxanne | Lv 13–16 met 6 Pokémon (veel gerouleerd, een paar white-outs); Mudkip nog niet geëvolueerd → geen inflatie meer. | 👍 |
| **Roxanne** | Gewonnen in 1 poging, "perfect". Elke starter heeft een counter (Sableye ↔ Torchic, Shuckle ↔ Treecko, Lileep ↔ Mudkip). Lileep's Recover-stall voelde logisch. Minccino's Sing maakte het verschil tegen Sableye en Nosepass; Super Fang tegen Shuckle. | 👍 |
| Roxanne's ace | Nosepass is de ace, niet Shuckle: levels omgedraaid (Nosepass 19, Shuckle 18). | ✅ |
| Sterke vroege wilde Pokémon | Emolga (Mini Forest, 10%, 428 BST) en Minccino (Technician) zijn sterk. Voorstel: laten staan (zijgebied = marge); evt. Emolga naar een 1%-slot. | 💡 |
| Shellos (Billy) | Harden + Recover was eindeloos rekken; Recover → Mud Shot. Recover mag, maar niet om vroege gevechten te rekken. | ✅ |
| AI-debuffspam | Keccles' Charmander deed 3× Smokescreen vóór Dragon Breath. Nu: een stat-verlaging scoort alleen zolang die stat nog niet verlaagd is. Uitzondering: eerste rivaalgevecht (Route 103), daar maakt de spam het winbaar. | ✅ |
| Pokémon zonder aanval | Ivan's Pyukumuku (Baton Pass gaf Leech Seed door) kon niets: + Counter. Alle trainer-Pokémon zonder aanval kregen er een (behalve grappen). | ✅ |
| Bullet Seed | Raakte maar 2×. Kansen zijn standaard Gen 5+ (35% 2×, 35% 3×, 15% 4×, 15% 5×); de power is wel verhoogd (30 per hit i.p.v. 25, gemiddeld ±93 i.p.v. ±77). Jordi: viel mee, niet te sterk. | 👍 |
| Self-Destruct mist | Alola-Geodude's Self-Destruct "raakte niet": miss door 1 Mud-Slap (accuracy −1). Geen bug. | 👍 |
| Leech Seed na wissel | Bleef hangen: Pyukumuku gebruikte Baton Pass (geeft het door, zoals in de echte games). Geen bug. | 👍 |

### Bugs
| Wat | Status |
|---|---|
| Ingang Toadstool Hollow niet te vinden (zag eruit als een boom); nu een zichtbaar pad. Ook de Wo-Chien-ingang. | ✅ |
| Speler/rivaal onzichtbaar na de rivaal-intro (May) | ✅ |
| Verkeerde pc-melding na het vangen ("sent to PC" terwijl er plek was) | ✅ |
| Dave (Route 104) stond 1 tegel te laag in zee | ✅ |
| SickBlik dubbel rond Petalburg Woods; tweede verwijderd | ✅ |
| SickBlik/Dave/Colress misten soms hun intro/thema | ✅ |
| Save corrupt na nieuwe ROM (savestate) → hersteld als .sav | ✅ |
| Relearn-knop zwart in "welke move vergeten?" na evolutie | ✅ |
| Briney's boot voer over een eiland in Route 105; nu eromheen | ✅ |
| Fish Judge (Dewford) alleen met Surf bereikbaar; nu op het zand onder de steiger (13,11) | ✅ |
| Madame Silk had een Cooltrainer-sprite; nu de Bard-sprite (Mauville) | ✅ |
| SickBlik (strand Route 104) blijft niet staan na het gevecht maar gaat de wereld verkennen | ✅ |

### Wensen en teksten (verwerkt)
TV-teksten Mom/Dad, pc's van May/Brendan, Galar-Zigzagoon, Birch achtervolgd door Jigglypuff, hoog-gras-tekst, tijdschriften, Spinda-DJ, winkelplanken, muziekman Oldale verplaatst, VS-intro Route 103, wilde muziek (Hoenn, Kanto vanaf badge 4), tekstvakken afbreken op zinnen, Wally-Ralts-gevecht in Petalburg, Fisherman-intro (Wailord-finale) en Magikarp-intro, L INFO-melding in wilde gevechten, items verplaatsen in MOVE POKéMON, itemmelding onderin. Allemaal ✅.

### Open / later
- ⏳ Jordi heeft nog een lijstje met mogelijke aanpassingen.
- 💡 Simulatie: bij Brawly komt een hoofdpadspeler ±0,7 boven de ace uit; nalopen als Jordi daar is.
- 💡 Emolga eventueel naar een 1%-slot.

## Ronde 2 (13 okt): Dewford en Granite Cave
| Wat | Bevinding | Status |
|---|---|---|
| Granite Cave wild | 1F stond nog op lv 6–13; nu 14–17 (1F), 15–18 (B1F), 16–21 (B2F), 15–20 (Steven). | ✅ |
| Sirfetch'd op lv 18 | SIR LEEK (ruil) houdt een Leek vast: 50% crit per treffer, dus 3 crits in één gevecht gaat snel. Vroeg, maar niet game-breaking (Jordi): zo laten. | 👍 |
| Pollen Season verborgen | Butterfree had Pollen Season als verborgen ability (niet te krijgen). Bij alle 8 soorten nu in slot 1/2; verder geen nieuwe abilities alleen in het verborgen slot. | ✅ |
| Romero (Dewford Gym) Detect-spam | Gymtrainers hadden een bijna willekeurige AI; nu slimmere AI, Combusken een echte moveset. | ✅ |
| AI van gymtrainers | Alle gymtrainers (gym 1–8, 39 in totaal) hebben nu de slimmere AI. | ✅ |
| Team vóór Brawly | Lv 17–19 (Butterfree, Shroodle, Cutiefly, Emolga, Tinkatink, Sirfetch'd), 3 van 6 gewisseld na Roxanne, zonder grinden en zonder Slateport. Brawly ace 23: 4–6 eronder. Uitslag: zie Brawly hieronder. | 👍 |
| Black Belt Cristian heet nu Chael | | ✅ |
| Volgorde Granite Cave / Flash | Hoofdpad naar Steven was donker (Flash pas na Brawly). Nu: B1F en B2F licht; Cornerstone- en zwaardkamer donker tot Flash (en achter Rock Smash); Crystal Grotto vroeg, maar verstopt. Vóór Brawly kun je naar Slateport voor extra EXP. | ✅ |
| Crystal Grotto te makkelijk te vinden; bedoeld als vroege optionele grot: ladder nu in een hoekje van B1F (15,21, door Jordi aangewezen; geen rots, donker tot Flash) | | ✅ |
| Briney voer richting Slateport over eilanden/NPC's in Route 107/108; nu eromheen | | ✅ |
| Strand Slateport (Route 109) | Trainers te voet lv 22–24, hoger dan Brawly maar makkelijker; met de Gen 5-EXP (hoger level = meer EXP) juist een goede EXP-plek vóór Brawly (Jordi): zo laten. | 👍 |
| Spit or Swallow (strand Slateport) | Gaf met een vol team geen keuzemenu; nu wel (Pokémon naar de pc) en een vrouw i.p.v. een man. | ✅ |
| Burglar SIMON (Slateport) | Eerste inbrekersevent getriggerd in Slateport: werkt zoals bedoeld, "erg leuk" (Jordi). | 👍 |
| Burglar SIMON levels | Teams per badge liepen vanaf badge 3 tot 24 levels achter; nu net onder de volgende gym-ace (26–28 … 70–72). Hone Claws tegen Tinkatink: logische keuze, AI blijft. | ✅ |
| Simon verdween zomaar na zijn vlucht; nu een snelle fade naar zwart | | ✅ |
| Team na Slateport | Lv 17–21 (Emolga 21, Butterfree/Sirfetch'd 20, Cutiefly/Sableye 19, Tinkatink 17): kern 2–3 onder Brawly's ace 23 = doel; gemiddeld −3,7 door rouleren. EXP niet aanpassen; bij problemen eerst naar Brawly's team kijken. | 👍 |
| **Brawly** | Gewonnen, nipt. Sableye (Prankster Will-O-Wisp) en Sirfetch'd nuttig, Cutiefly/Tinkatink kansloos. Spinda (Normal/Fighting, Pure Power, Silk Scarf) is de grote drempel; counters vóór Brawly: Phantump (Will-O-Wisp + Leech Seed/Hex), Shuppet/Sableye (Prankster Will-O-Wisp), Mawile (Intimidate, in- en uitwisselen). Genoeg counters (Jordi): zo laten. | 👍 |
| Cornerstone-kamer (Okidogi) bereikbaar zonder Rock Smash (pad om de vanilla-rotsen heen); nu een rots op de ingang | | ✅ |
| Crystal Grotto: nutteloze richel bij de ingang weggehaald | | ✅ |
| Leftovers en andere healing-items: de animatie duurde te lang (elke beurt). Nu alleen een korte flits met een ring | | ✅ |
| Pollen Haze-balans | Besproken: buffs nodig (Bug was het zwakste type). Ribombee te weinig bulk; Scizor en Volcarona hebben geen Pollen Season (move of partner nodig) en een eigen weersetter of windmove lost de haze op. Zo laten, in het late spel in de gaten houden. | 👍 |
| Wilde levels | Route 110 (Gulpin lv 14) en de hele middengame lagen ver onder de trainers; 43 tabellen verhoogd tot ±2 onder het trainerlevel, evoluties waar nodig. | ✅ |
| May Route 110 (ace 29) | Jordi getest met Sandslash 25, Vivillon/Butterfree/Paras 23: eerst achter, daarna snel omgebogen met Stone Axe en First Impression. Levels fair, niets veranderd. | ✅ |
| Simon (inbreker, 2 badges: lv 26–28) | Jordi verloor 2× met Carkol in het team, won daarna met Sir Leek: lag aan het eigen team, niets veranderd. | ✅ |
| West-Route 118 trainers 31–32 (Colress 26–27) | Rose/Dalton 28, Deandre/Wade 29 (levelcurve rekende Route 118 tot Winona). | ✅ |
| Tas vol in Mauville | Items-pocket 30 → 120, oude save blijft werken. | ✅ |
| Straight Line 140 met priority te sterk | Opnieuw achter elkaar: x1,5 zonder priority. | ✅ |
| Wigglytuff met Boomburst vóór gym 1 | Boomburst 50, Hyper Voice 36, Double-Edge 44; Moon Stone van Petalburg Woods naar Capt. Stern (Slateport), Petalburg Woods geeft een Scope Lens. | ✅ |
| Birch op Route 110: nieuwe dialoog van Jordi | | ✅ |
| EXP-bomgevechten | Miguel (Route 103-oost, 4× Blissey) werkt perfect als compensatie na veel vangen. Idee (Jordi, hardop): meer van zulke gevechten na grote vangmomenten, bijv. Route 113/114 (±37), Route 119 (±47), Route 121/123 (±55), Route 128/129 (±66); eerst testen met de nieuwe wilde levels. Nog maar 3 vrije trainer-id's (851–853). | 💡 |
| Rhett (Route 103) volledig lv 20, onbedoeld | Nu 26–27 zoals de buren. Andere uitschieters nagelopen; Nolan (Route 114, Whiscash 50), Juan en Aaron (lv 74) blijven bewust (Jordi). | ✅ |

## Ronde 3 (15 okt): kladblok t/m Mauville
| Wat | Bevinding | Status |
|---|---|---|
| Wally KO't Ralts in de tutorial | Zigzagoon had Hustle (slot 1); nu Pickup en één Tackle | ✅ |
| Wally-Ralts-gevecht meteen na de vangst | Nu terug in de Petalburg Gym | ✅ |
| Lady Cindy te hoog | Lv 10 | ✅ |
| SickBlik (strand) | Porygon blijft een test; Toedscool lv 10 | ✅ |
| Tatsugiri (Bubble Beam) bij de eerste Aqua-grunt | Fijne test, lv 11 prima | 👍 |
| TM-naam bij krijgen | "TM09 Bullet Seed" | ✅ |
| Pretty Petal, moeder naast de school, Rusturf, Roxanne/Tommy, May 2, Janice, Anna & Meg, rivaal Route 110, Cyclizar | Nieuwe teksten (placeholders in huisstijl; Jordi levert later eigen dialogen) | ✅ |
| Scott "als Roxanne" | Nu cosplay als PROF. BIRCH | ✅ |
| Focus Sash-trainer (Karen) spoilt de Sash | FEAR-woordgrap | ✅ |
| Hiker Gerrit | GARRETT | ✅ |
| Keccles over te slaan | Teksten vertakken naar wat je oversloeg | ✅ |
| Wonderful-profielman nutteloos | Databroker, eenmalig een Nugget | ✅ |
| Petalburg huis rechtsonder + meer giveaways | Zes steden + Rusturf Tunnel | ✅ |
| Rusturf Tunnel nutteloos / X Sp. Atk | Lepelgraver, 2 verborgen items; X Sp. Atk → Revive | ✅ |
| Meer X-items vervangen | 5 van 6 | ✅ |
| Route 104 boven Petalburg Woods | Eigen encountertabel | ✅ |
| Marts groeien mee | Per badge | ✅ |
| Move Tutors onbeperkt | | ✅ |
| Briney Petalburg → Slateport | | ✅ |
| Josh (Gligar Knock Off) | Gligar zonder Knock Off | ✅ |
| Colress te zwak, Ground-zwakte | 29–30, geëvolueerd, Air Balloon/Levitate/Ice Beam | ✅ |
| Hypno Dream Eater zonder slaper | AI-fix | ✅ |
| Tinkatink 2× Covet | Engine-bug bij meerdere levels tegelijk | ✅ |
| PokéFan-intro: item als 3e Pokémon | Pikachu-knuffel | ✅ |
| Fisherman Andrew | Magikarp-transitie | ✅ |
| Bessen plukken sneller | | ✅ |
| Melding na move/take van items | Pc: melding bij oppakken; partymenu had hem al | ✅ |
| Burglar SIMON post-game tijdverspilling | Alleen met ≥ 3 Pokémon van lv 90+ in het team | ✅ |
| Simon: bewoners Fallarbor/Lilycove | Cozmo zelf; de Kecleon met spraakverwarring | ✅ |
| Simon twee keer op rij in dezelfde stad | Kan niet meer | ✅ |
| Coin Case niet te krijgen (geen Harbor Mail meer) | Mauville House2 geeft hem direct | ✅ |
| NPC over de vervloekte tv (Rotom-kelder) ontbrak | Man des huizes in Mauville House2 | ✅ |
| Rotom-tv vóór 3 badges | Telesell-reclames met subliminale badge-boodschap | ✅ |
| Route 111-zuid lv 34 boven Mauville | 29–31, Dave ongewijzigd | ✅ |
| Mail bestaat nog | Overal weg en vervangen | ✅ |
| Audit: Hydrapple/Wyrdeer, Ice Stone Ashfrost, luik Route 110, Zygarde Cube | Opgelost | ✅ |
| Oostkant Fortree vóór Winona te hoog (Route 123, Mt. Pyre, Lilycove-rivaal, Safari) | Trainers 52–55 (rivaal 57), wild omlaag | ✅ |
| Route 135/136 richting Ashfrost | Iets hoger dan Route 119 (49–52) | ✅ |
| Kangaskhan lv 62–67 op Route 115 | 55–57 | ✅ |
| Eindmelding Fungal Control sprak over Encore | Eigen tekst | ✅ |
| Fungal Control kon Uproar niet overschrijven | Wist nu Uproar/rampage/Rollout/Bide | ✅ |
| Illumise als (laatste) Wattson-Pokémon zwak | Rotom-Wash | ✅ |
| Fungal Control werkt niet op Grass | Geen poedermove meer; Overcoat/Safety Goggles blokkeren | ✅ |
| Straight Line te sterk? | 60 / 100 | ✅ |
