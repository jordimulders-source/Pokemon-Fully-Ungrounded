# The Spire – rekenwerk (gegenereerd)

Gemaakt met `tools/grounded/spire/spire_pool.py`; opnieuw draaien na wijzigingen in soorten of moves.

## Model

- **Rating** van een vorm op lv 50 (IV 31, EV 84):
  `aanval^0,55 × bulk^0,45` (aanval iets zwaarder: vijanden hebben ×HP en passief spelen wordt afgestraft). Aanval = hoogste van Atk/SpA × 1,5 (STAB); bulk = HP × harmonisch gemiddelde van Def en SpD;
  snelheid = 1 tot 1,25 (logistisch t.o.v. een base-75-tegenstander); ability-factor voor o.a. Huge Power ×1,6, Truant ×0,5.
  **100 = mediaan van alle volledig geëvolueerde kandidaten** (1750 ruw).
- **Vorm per act**: act 1 = eerste vorm (baby's tellen niet), na elke baas één evolutie. Vertakkingen: de speler kiest; in de rating telt de sterkste tak.
- **Runwaarde V** = gewogen gemiddelde van (rating / mediaan van die act) over de drie acts, 30/30/40% (act 3 zwaarder: daar zitten de zwaarste bazen). 100 = precies gemiddeld in elke act.
- **Toelating**: in elke act minstens 75% van de mediaan van die act (act 1: 45, act 2: 71, act 3: 76).
  Soorten zonder evolutie alleen als ze minstens zo sterk zijn als een gemiddelde act-2-vorm (rating ≥ 95): dan is het een echte afweging (nu sterk, nooit beter).
  En de startkit moet compleet zijn (STAB-aanval, statusmove, grounded move).
- **Tiers** op V: C < 98 ≤ B < 105 ≤ A < 118 ≤ S (30/30/25/15%). Draft: C/B gewoon, A uncommon, S rare.

## Startkit

- **STAB-aanval 40–50** per type van de eerste vorm; fysiek of speciaal naar de hoogste aanvalsstat over de drie acts.
  Voorkeur: level-up van de eerste vorm > level-up van de lijn > eimove > TM > algemene typemove (bijv. Flame Charge voor een fysieke vuursoort).
- **Statusmove**: de basismove uit de eigen leerset met de hoogste verwachtingswaarde in het gevechtsmodel
  (60% gewone gevechten van 3 beurten, 25% elites van 5, 15% bazen van 11; een statusmove kost een halve beurt aan schade
  en levert over de resterende beurten minder binnenkomende of meer uitgaande schade op).
  Uitkomst in het kort: **Growl** (−1 Atk op beide) wint van Sand Attack/Double Team (één doel −25%%) zolang de helft van de vijanden fysiek is;
  **Tail Whip/Leer** wint bij een fysieke aanvaller; alle statusmoves zijn netto negatief in gewone gevechten van 3 beurten en verdienen zich terug bij elites en bazen. Precies zoals Defend in Slay.
- **Grounded move**: uit de eigen level-up/eimoves, iets wat de soort typeert (zeldzaam onder alle soorten, eigen type, vroeg geleerd), maximaal sterkte 3 (dus geen Spore, Sleep Powder, Swords Dance).
  Vast: Bulbasaur Leech Seed, Pikachu Thunder Wave, Jigglypuff Sing, Oddish Moonlight.

### Pikachu: Thunder Wave, Double Team of Growl?

Verwachtingswaarde (in beurten vijandelijke schade, + = winst) voor Pikachu als statusmove:

- Growl: +0.12
- Cosmic Power: +0.12
- Tickle: +0.03
- Tail Whip: -0.09
- Sweet Kiss: -0.16
- Charge: -0.19
- Thunder Wave (verlamd: 25% beurt kwijt + trager): ≈ -0.04 (plus snelheid); daarom de grounded move.

Conclusie: **Growl** als statusmove, **Thunder Wave** als grounded move. Double Team wint niets van Growl en ontwijken is anti-fun (en tegen 2 vijanden raakt maar de helft van de aanvallen jou).

## Verboden moves

- **wisselen of vluchten (je kunt in de Spire niet wisselen):** Teleport, Roar, Whirlwind, U-turn, Volt Switch, Flip Turn, Parting Shot, Baton Pass, Shed Tail, Chilly Reception, Dragon Tail, Circle Throw, Healing Wish, Lunar Dance, Memento, Revival Blessing
- **doet niets (of alleen buiten gevechten):** Splash, Celebrate, Hold Hands, Happy Hour, Sweet Scent, Camouflage, Conversion, Conversion 2, Sketch, Recycle, Bestow, Embargo, Telekinesis, Lucky Chant, Mud Sport, Water Sport, Snatch, Grudge, Imprison, Nightmare, Attract, Captivate, Defog, Court Change, Ion Deluge, Fairy Lock, Mean Look, Block, Spider Web, Foresight, Odor Sleuth, Miracle Eye, Lock-On, Mind Reader, Spotlight, Magnet Rise, Mimic, Spikes, Toxic Spikes, Stealth Rock, Sticky Web, Gravity, Magic Room, Play Nice
- **vaste of procentuele schade (negeert de HP-vermenigvuldiger):** Psywave, Sonic Boom, Dragon Rage, Seismic Toss, Night Shade, Super Fang, Nature's Madness, Ruination, Endeavor, Pain Split, Final Gambit, Guillotine, Horn Drill, Fissure, Sheer Cold, Guardian of Alola, Bide
- **KO ongeacht HP (breekt bazen met xHP):** Perish Song, Destiny Bond
- **jezelf opofferen (zonder wissel blijft je partner alleen; Jordi: nutteloos):** Explosion, Self-Destruct, Misty Explosion
- **items stelen of ruilen (items zijn je relics):** Trick, Switcheroo, Covet, Thief, Knock Off, Incinerate, Corrosive Gas
- **objectief slechter dan een andere move (Jordi):** Bubble, Pound, Scratch, Constrict, Powder Snow

## Later beginnen

Is de eerste vorm in act 1 of 2 te zwak, dan begint de lijn een stap later (zelfde drempels):
- Beautifly in plaats van Silcoon (alleen via events)
- Beedrill in plaats van Kakuna (alleen via events)
- Butterfree in plaats van Metapod (alleen via events)
- Diggersby in plaats van Bunnelby (alleen via events)
- Dolliv in plaats van Smoliv
- Dottler in plaats van Blipbug
- Flaaffy in plaats van Mareep
- Frosmoth in plaats van Snom
- Gyarados in plaats van Magikarp (alleen via events)
- Kirlia in plaats van Ralts
- Kricketune in plaats van Kricketot (alleen via events)
- Lokix in plaats van Nymble
- Lombre in plaats van Lotad
- Loudred in plaats van Whismur
- Milotic in plaats van Feebas (alleen via events)
- Naclstack in plaats van Nacli
- Nidorina in plaats van Nidoran♀
- Nidorino in plaats van Nidoran♂
- Nuzleaf in plaats van Seedot
- Palpitoad in plaats van Tympole
- Pawmo in plaats van Pawmi
- Pidgeotto in plaats van Pidgey
- Skiploom in plaats van Hoppip
- Steenee in plaats van Bounsweet
- Sunflora in plaats van Sunkern (alleen via events)
- Swadloon in plaats van Sewaddle
- Tinkatuff in plaats van Tinkatink
- Tranquill in plaats van Pidove
- Vespiquen in plaats van Combee (alleen via events)
- Vigoroth in plaats van Slakoth
- Weepinbell in plaats van Bellsprout
- Whirlipede in plaats van Venipede

## Objectief slechtere moves (automatisch)

Zelfde type, categorie, doelwit en prioriteit; de andere is minstens even sterk en accuraat en heeft alle bijeffecten ook. Niet als startmove of beloning (tegenstanders mogen ze wel).

Apple Acid (→ Energy Ball), Aqua Tail (→ Crabhammer), Bind (→ Wrap), Chip Away (→ Stomp), Cross Chop (→ Superpower), Cross Poison (→ Poison Jab), Dragon Pulse (→ Core Enforcer), Drill Run (→ High Horsepower), Frost Breath (→ Aurora Beam), Headbutt (→ Stomp), Hyper Fang (→ Stomp), Mega Punch (→ Stomp), Night Slash (→ Crunch), Razor Shell (→ Liquidation), Sky Uppercut (→ Sacred Sword), Slash (→ Stomp), Spacial Rend (→ Core Enforcer), Storm Throw (→ Low Sweep), Wicked Blow (→ Crunch)

## Items (relics): getallen

**Life Orb** (×1,3 schade voor de drager): het team neemt minder schade omdat gevechten korter duren.

| gevecht | beurten | HP-verlies | bespaard (team) | break-even terugslag per aanval |
|---|---|---|---|---|
| normaal | 3 | 15% | 3.9% | 1.3% |
| elite | 5 | 25% | 6.5% | 1.3% |
| baas | 11 | 65% | 17.0% | 1.5% |

Gewogen break-even: **1.3%** van de max HP per aanval. Gekozen: **2%** (de normale 10% is met ×4 HP veel te zwaar). Netto kost Life Orb dus iets HP, maar wint tempo: sneller KO's, minder buffs en woede-opbouw van de vijand. Bij 1% is hij altijd winst (geen afweging).

**Leftovers**: normaal 1/16 per beurt; met ×4 HP is dat 6,25% van de balk per beurt, ofwel ±19% per gewoon gevecht: meer dan je in een gevecht verliest (±15%). In de Spire **1/32** (±9% per gewoon gevecht, ±34% per baas): nog steeds extreem sterk, dus rare.

**Focus Sash**: overleeft één keer een KO-klap, op elke HP (niet alleen vol); daarna weg. Waarde ≈ één klap (±10% HP) plus het redden van een run.

## Overige getallen (en waarom)

- **Levels:** alles in de Spire is lv 100 (Jordi). Level is dus nooit een knop; sterkte komt uit soort, moves, items, totem-boosts en HP-vermenigvuldiger.
- **Heal na een gevecht 8%, rustplek (Chansey) 30%, nieuwe act 40%** (v0.8.107, zie *Vergelijking met Slay the Spire* onderaan; eerder 10/40/40). Slay: Burning Blood 6 van 80 HP (7,5%), rust 30%, nieuwe act 75% van het tekort (A5+). Een gewoon gevecht kost ±12% (zie Ontmoetingen), een elite ±24-30%, een baas ±55-65%: gewone gevechten kosten netto een paar procent, elites echt HP, en rusten (30% ≈ één elite) concurreert met upgraden. Met de oude 20% na elk gevecht was een gewoon gevecht altijd gratis.
- **Upgrade (Porygon2, "+"):** aanval +30% kracht; statusmove één stage extra en mist nooit; altijd max PP. Rekensom: de hoofdaanval wordt ±60% van de beurten gebruikt, dus ±18% meer schade, gevechten ±15% korter, ±15% minder schade incasseren: ±1,6% HP per gewoon gevecht, 3,6% per elite, 8% per baas. Over de ±15 gevechten die na de eerste rustplek nog komen is dat ±40% HP: meer dan rusten (30%) als je gezond bent. Vroeg in de run en met genoeg HP is upgraden dus beter, laag of vlak voor de baas rusten: een echte keuze (zoals Smith/Rest in Slay).
- **Geld:** start 75¥, gevecht 15-25¥, elite 35-45¥, baas 80¥ (Amulet Coin +50%): ±235¥ per act. Winkel: move 45/70/120¥ (common/uncommon/rare), vasthouditem 50/85/140¥, relic 150¥, Move Relearner 50¥ + 25¥ per eerder gebruik (zoals card removal in Slay: 75 + 25n). Eén winkelbezoek koopt dus 1-3 dingen (Slay: start 99, relic 150-300 op ±250 per act).
- **Vasthouditems:** één per Pokémon, zoals in de echte games; gebruikt (Focus Sash, bes) = weg voor de rest van de run. Spire-afwijkingen: Life Orb 2% terugslag, Focus Sash op elke HP, Leftovers 1/32 (zie boven). Nutteloos en dus niet in de pool: Red Card, Eject Button/Pack, Shed Shell, Smoke Ball, Exp. Share, Lucky Egg, Everstone, evolutie-items (Up-Grade, ...), Destiny Knot, Float Stone, Iron Ball, Lagging Tail, Sticky Barb, Ring Target, Full Incense, Macho Brace, Power-items, Cleanse Tag.
- **Draft-zeldzaamheid:** C 35%, B 35%, A 22%, S 8% (zoals kaartzeldzaamheid in Slay: de sterkste opties zijn zeldzaam).
- **Beloningskaarten:** kaart 1 past bij het type van je eerste Pokémon, kaart 2 bij je tweede, kaart 3 is vrij (zoals klassekaarten in Slay). Zeldzaamheid 60/30/10%.

## Rentals

### Tier S (51)

| soort | acts | V | startmoves |
|---|---|---|---|
| Scyther | Scyther → Kleavor | 141 (112/119/119) | Pounce, Wing Attack, Leer, Agility |
| Duraludon | Duraludon → Archaludon | 137 (104/119/119) | Mirror Shot, Twister, Leer, Iron Defense |
| Meditite | Meditite → Medicham | 131 (77/129/129) | Vacuum Wave, Confusion, Work Up, Detect |
| Aerodactyl | Aerodactyl | 129 (106/106/106) | Accelerock, Wing Attack, Supersonic, Scary Face |
| Sneasel | Sneasel → Sneasler | 128 (91/115/115) | Rock Smash, Poison Fang, Leer, Taunt |
| Flamigo | Flamigo | 128 (105/105/105) | Peck, Mach Punch, Focus Energy, Detect |
| Lunatone | Lunatone | 128 (105/105/105) | Ancient Power, Confusion, Cosmic Power, Lunar Blessing |
| Electabuzz | Electabuzz → Electivire | 127 (95/111/111) | Thunder Fang, Leer, Thunder Wave |
| Dondozo | Dondozo | 127 (104/104/104) | Aqua Jet, Tickle, Soak |
| Druddigon | Druddigon | 126 (104/104/104) | Breaking Swipe, Leer, Scary Face |
| Relicanth | Relicanth | 126 (104/104/104) | Aqua Jet, Rock Throw, Harden, Whirlpool |
| Magmar | Magmar → Magmortar | 126 (95/109/109) | Ember, Smokescreen, Sunny Day |
| Farfetch'd | Farfetch'd | 126 (103/103/103) | Mach Punch, Peck, Leer, Feather Dance |
| Cryogonal | Cryogonal | 126 (103/103/103) | Icy Wind, Acid Armor, Haze |
| Bouffalant | Bouffalant | 126 (103/103/103) | Tackle, Leer, Focus Energy |
| Sableye | Sableye | 126 (103/103/103) | Rock Throw, Shadow Sneak, Leer, Confuse Ray |
| Sneasel | Sneasel → Weavile | 125 (91/111/111) | Bite, Ice Shard, Leer, Taunt |
| Togetic | Togetic → Togekiss | 125 (79/119/119) | Fairy Wind, Gust, Growl, Sweet Kiss |
| Miltank | Miltank | 125 (102/102/102) | Tackle, Growl, Heal Bell |
| Bruxish | Bruxish | 125 (102/102/102) | Aqua Jet, Heart Stamp, Screech, Disable |
| Lucario | Lucario | 125 (102/102/102) | Vacuum Wave, Mirror Shot, Work Up, Detect |
| Chimecho | Chimecho | 124 (102/102/102) | Confusion, Mirror Shot, Growl, Heal Bell |
| Yanma | Yanma → Yanmega | 124 (81/116/116) | Struggle Bug, Gust, Supersonic, Pollen Haze |
| Throh | Throh | 124 (102/102/102) | Rock Smash, Leer, Wide Guard |
| Dhelmise | Dhelmise | 124 (101/101/101) | Shadow Sneak, Vine Whip, Growth, Mega Drain |
| Larvesta | Larvesta → Volcarona | 124 (71/123/123) | Struggle Bug, Ember, Harden, String Shot |
| Qwilfish | Qwilfish → Overqwil | 123 (91/109/109) | Bite, Poison Sting, Harden, Toxic |
| Bombirdier | Bombirdier | 123 (101/101/101) | Peck, Bite, Leer, Hone Claws |
| Misdreavus | Misdreavus → Mismagius | 122 (91/107/107) | Ominous Wind, Growl, Confuse Ray |
| Durant | Durant | 122 (100/100/100) | Pounce, Metal Claw, Sand Attack, Iron Defense |
| Rufflet | Rufflet → Braviary | 122 (75/118/118) | Quick Attack, Peck, Leer, Tailwind |
| Spinda | Spinda | 122 (100/100/100) | Tackle, Rock Smash, Fake Tears, Teeter Dance |
| Hitmontop | Hitmontop | 122 (100/100/100) | Mach Punch, Focus Energy, Quick Guard |
| Glimmet | Glimmet → Glimmora | 121 (74/118/118) | Ancient Power, Acid Spray, Harden, Mortal Spin |
| Roselia | Roselia → Roserade | 121 (81/112/112) | Mega Drain, Acid, Growth, Stun Spore |
| Illumise | Illumise | 121 (99/99/99) | Struggle Bug, Thunder Shock, Growth, String Shot |
| Gligar | Gligar → Gliscor | 121 (87/107/107) | Sand Tomb, Wing Attack, Sand Attack, Agility |
| Lapras | Lapras | 121 (99/99/99) | Aqua Jet, Ice Shard, Tickle, Life Dew |
| Stantler | Stantler → Wyrdeer | 120 (94/102/102) | Tackle, Leer, Hypnosis |
| Hitmonlee | Hitmonlee | 120 (99/99/99) | Mach Punch, Focus Energy, Wide Guard |
| Komala | Komala | 120 (99/99/99) | Rapid Spin, Defense Curl, Yawn |
| Tyrunt | Tyrunt → Tyrantrum | 120 (78/113/113) | Accelerock, Breaking Swipe, Tail Whip, Charm |
| Hawlucha | Hawlucha | 120 (99/99/99) | Rock Smash, Wing Attack, Feather Dance, Detect |
| Hitmonchan | Hitmonchan | 120 (98/98/98) | Mach Punch, Focus Energy, Quick Guard |
| Porygon | Porygon → Porygon2 → Porygon-Z | 119 (76/99/124) | Thunder Shock, Defense Curl, Magic Coat |
| Sandshrew | Sandshrew → Sandslash | 119 (70/118/118) | Bulldoze, Sand Attack, Rototiller |
| Wailmer | Wailmer → Wailord | 119 (78/111/111) | Aqua Jet, Tickle, Soak |
| Growlithe | Growlithe → Arcanine | 119 (67/119/119) | Flame Charge, Rock Throw, Leer, Howl |
| Anorith | Anorith → Armaldo | 119 (80/109/109) | Accelerock, Pounce, Sand Attack, Rock Polish |
| Mr. Mime | Mr. Mime → Mr. Rime | 118 (91/102/102) | Icy Wind, Confusion, Tickle, Reflect |
| Sandshrew | Sandshrew → Sandslash | 118 (68/118/118) | Ice Shard, Metal Claw, Defense Curl, Snowscape |

### Tier A (85)

| soort | acts | V | startmoves |
|---|---|---|---|
| Cufant | Cufant → Copperajah | 118 (74/113/113) | Bullet Punch, Growl, Iron Defense |
| Drilbur | Drilbur → Excadrill | 118 (69/117/117) | Sand Tomb, Iron Defense, Mud-Slap |
| Frosmoth | Frosmoth | 118 (97/97/97) | Icy Wind, Struggle Bug, Feather Dance, Snowscape |
| Darumaka | Darumaka → Darmanitan | 118 (70/115/115) | Ice Shard, Work Up, Taunt |
| Rotom | Rotom | 117 (96/96/96) | Thunder Shock, Infernal Parade, Charge, Thunder Wave |
| Comfey | Comfey | 117 (96/96/96) | Draining Kiss, Growth, Floral Healing |
| Cyclizar | Cyclizar | 117 (96/96/96) | Breaking Swipe, Quick Attack, Growl, Rapid Spin |
| Maschiff | Maschiff → Mabosstiff | 117 (71/114/114) | Bite, Leer, Hone Claws |
| Lokix | Lokix | 117 (96/96/96) | Pounce, Bite, Leer, Struggle Bug |
| Voltorb | Voltorb → Electrode | 117 (71/113/113) | Thunder Shock, Charge, Magnetic Flux |
| Girafarig | Girafarig → Farigiraf | 117 (89/101/101) | Swift, Confusion, Growl, Agility |
| Growlithe | Growlithe → Arcanine | 116 (66/117/117) | Flame Charge, Leer, Howl |
| Jynx | Jynx | 116 (95/95/95) | Icy Wind, Confusion, Sweet Kiss, Transmutation |
| Mudbray | Mudbray → Mudsdale | 116 (79/106/106) | Bulldoze, Iron Defense, Mud-Slap |
| Togedemaru | Togedemaru | 115 (95/95/95) | Spark, Bullet Punch, Tickle, Charge |
| Teddiursa | Teddiursa → Ursaring → Ursaluna | 115 (66/104/124) | Quick Attack, Leer, Scary Face |
| Goldeen | Goldeen → Seaking | 115 (73/110/110) | Aqua Jet, Tail Whip, Aqua Ring |
| Doduo | Doduo → Dodrio | 115 (70/112/112) | Bulldoze, Peck, Growl, Mud-Slap |
| Cetoddle | Cetoddle → Cetitan | 114 (67/113/113) | Ice Shard, Growl, Rest |
| Frigibax | Frigibax → Arctibax → Baxcalibur | 114 (65/87/136) | Breaking Swipe, Ice Shard, Leer, Snowscape |
| Cranidos | Cranidos → Rampardos | 114 (76/105/105) | Accelerock, Leer, Focus Energy |
| Grimer | Grimer → Muk | 113 (71/109/109) | Poison Fang, Harden, Venom Drench |
| Grimer | Grimer → Muk | 113 (71/109/109) | Poison Fang, Bite, Harden, Poison Gas |
| Hippopotas | Hippopotas → Hippowdon | 113 (70/109/109) | Sand Tomb, Sand Attack, Yawn |
| Litleo | Litleo → Pyroar | 113 (72/107/107) | Ember, Swift, Work Up, Leer |
| Eevee | Eevee → Espeon | 113 (64/113/113) | Swift, Growl, Helping Hand |
| Ekans | Ekans → Arbok | 113 (66/111/111) | Poison Sting, Leer, Jaw Lock |
| Staryu | Staryu → Starmie | 112 (67/110/110) | Water Gun, Harden, Thunder Wave |
| Ponyta | Ponyta → Rapidash | 112 (81/100/100) | Flame Charge, Tail Whip, Fire Spin |
| Ponyta | Ponyta → Rapidash | 112 (81/100/100) | Heart Stamp, Tail Whip, Agility |
| Pawniard | Pawniard → Bisharp → Kingambit | 112 (68/102/115) | Bite, Metal Claw, Leer, Torment |
| Rhyhorn | Rhyhorn → Rhydon → Rhyperior | 112 (71/100/111) | Rock Throw, Tail Whip, Rototiller |
| Makuhita | Makuhita → Hariyama | 112 (62/113/113) | Rock Smash, Sand Attack, Swallow |
| Farfetch'd | Farfetch'd → Sirfetch'd | 111 (74/104/104) | Rock Smash, Leer, Detect |
| Aipom | Aipom → Ambipom | 111 (73/104/104) | Quick Attack, Tail Whip, Tickle |
| Nuzleaf | Nuzleaf → Shiftry | 111 (69/106/106) | Mega Drain, Disarming Voice, Growth, Grass Whistle |
| Timburr | Timburr → Gurdurr → Conkeldurr | 111 (71/91/116) | Mach Punch, Leer, Focus Energy |
| Poochyena | Poochyena → Mightyena | 111 (60/112/112) | Bite, Howl, Hone Claws |
| Axew | Axew → Fraxure → Haxorus | 110 (66/88/123) | Breaking Swipe, Leer, Taunt |
| Pancham | Pancham → Pangoro | 110 (71/104/104) | Rock Smash, Leer, Taunt |
| Gible | Gible → Gabite → Garchomp | 110 (60/85/133) | Breaking Swipe, Sand Tomb, Sand Attack, Bulldoze |
| Mankey | Mankey → Primeape → Annihilape | 110 (63/96/121) | Rock Smash, Leer, Counter |
| Tangela | Tangela → Tangrowth | 110 (82/96/96) | Mega Drain, Growth, Stun Spore |
| Varoom | Varoom → Revavroom | 109 (61/110/110) | Bullet Punch, Poison Fang, Screech, Poison Gas |
| Tranquill | Tranquill → Unfezant | 109 (69/104/104) | Quick Attack, Peck, Leer, Swagger |
| Stufful | Stufful → Bewear | 109 (67/106/106) | Tackle, Mach Punch, Leer, Endure |
| Swadloon | Swadloon → Leavanny | 109 (69/104/104) | Pounce, Vine Whip, Screech, String Shot |
| Cacnea | Cacnea → Cacturne | 109 (73/102/102) | Vine Whip, Leer, Ingrain |
| Bagon | Bagon → Shelgon → Salamence | 109 (59/80/135) | Breaking Swipe, Leer, Roost |
| Pawmo | Pawmo → Pawmot | 109 (70/103/103) | Spark, Mach Punch, Growl, Charge |
| Tentacool | Tentacool → Tentacruel | 109 (61/109/109) | Water Gun, Acid, Tickle, Barrier |
| Loudred | Loudred → Exploud | 108 (71/102/102) | Mirror Shot, Thunder Shock, Growl, Nuzzle |
| Dolliv | Dolliv → Arboliva | 108 (69/103/103) | Mega Drain, Swift, Growth, Grassy Terrain |
| Crabrawler | Crabrawler → Crabominable | 108 (69/103/103) | Rock Smash, Leer, Protect |
| Flaaffy | Flaaffy → Ampharos | 108 (71/101/101) | Thunder Shock, Growl, Magnetic Flux |
| Murkrow | Murkrow → Honchkrow | 108 (76/97/97) | Feint Attack, Peck, Screech, Taunt |
| Phanpy | Phanpy → Donphan | 108 (65/105/105) | Bulldoze, Growl, Endure |
| Pikachu | Pikachu → Raichu | 107 (70/101/101) | Thunder Shock, Growl, Thunder Wave |
| Nidorino | Nidorino → Nidoking | 107 (69/101/101) | Poison Sting, Leer, Acid Rain |
| Kirlia | Kirlia → Gardevoir | 107 (55/111/111) | Confusion, Disarming Voice, Growl, Hypnosis |
| Deino | Deino → Zweilous → Hydreigon | 107 (59/80/131) | Bite, Breaking Swipe, Work Up, Focus Energy |
| Karrablast | Karrablast → Escavalier | 107 (63/105/105) | Pounce, Leer, Iron Defense |
| Corphish | Corphish → Crawdaunt | 107 (69/101/101) | Aqua Jet, Leer, Clamp |
| Zigzagoon | Zigzagoon → Linoone → Obstagoon | 107 (56/102/115) | Bite, Tackle, Leer, Hone Claws |
| Naclstack | Naclstack → Garganacl | 106 (67/101/101) | Salt Cure, Harden, Rock Polish |
| Surskit | Surskit → Masquerain | 106 (54/111/111) | Struggle Bug, Chilling Water, Agility, Infestation |
| Magnemite | Magnemite → Magneton → Magnezone | 106 (67/95/108) | Thunder Shock, Mirror Shot, Supersonic, Magnetic Flux |
| Scraggy | Scraggy → Scrafty | 106 (72/98/98) | Feint Attack, Power-Up Punch, Leer, Torment |
| Gastly | Gastly → Haunter → Gengar | 106 (69/91/107) | Infernal Parade, Clear Smog, Scary Face, Curse |
| Charcadet | Charcadet → Ceruledge | 106 (48/114/114) | Flame Charge, Leer, Will-O-Wisp |
| Palpitoad | Palpitoad → Seismitoad | 106 (70/99/99) | Aqua Jet, Sand Tomb, Growl, Aqua Ring |
| Electrike | Electrike → Manectric | 106 (63/104/104) | Charge Beam, Leer, Thunder Wave |
| Natu | Natu → Xatu | 106 (61/105/105) | Confusion, Gust, Cosmic Power, Tailwind |
| Binacle | Binacle → Barbaracle | 106 (60/106/106) | Accelerock, Aqua Jet, Tickle, Rock Polish |
| Shuppet | Shuppet → Banette | 106 (64/103/103) | Shadow Sneak, Screech, Confuse Ray |
| Corsola | Corsola → Cursola | 106 (75/95/95) | Infernal Parade, Harden, Curse |
| Amaura | Amaura → Aurorus | 106 (67/101/101) | Ancient Power, Icy Wind, Growl, Snow Storm |
| Tinkatuff | Tinkatuff → Tinkaton | 106 (71/98/98) | Fairy Wind, Metal Claw, Sweet Kiss, Draining Kiss |
| Larvitar | Larvitar → Pupitar → Tyranitar | 105 (61/77/126) | Rock Throw, Sand Tomb, Leer, Sandstorm |
| Abra | Abra → Kadabra → Alakazam | 105 (69/88/108) | Confusion, Flash, Barrier |
| Kabuto | Kabuto → Kabutops | 105 (65/102/102) | Accelerock, Aqua Jet, Leer, Mud Shot |
| Zigzagoon | Zigzagoon → Linoone | 105 (56/107/107) | Tackle, Tail Whip, Trailblaze |
| Sandile | Sandile → Krokorok → Krookodile | 105 (64/77/122) | Sand Tomb, Bite, Leer, Hone Claws |
| Vigoroth | Vigoroth → Slaking | 105 (100/76/76) | Quick Attack, Tickle, Encore |
| Nosepass | Nosepass → Probopass | 105 (66/100/100) | Ancient Power, Charge Beam, Harden, Magnetic Flux |

### Tier B (101)

| soort | acts | V | startmoves |
|---|---|---|---|
| Omanyte | Omanyte → Omastar | 105 (70/97/97) | Ancient Power, Water Gun, Sand Attack, Leer |
| Exeggcute | Exeggcute → Exeggutor | 105 (62/103/103) | Mega Drain, Confusion, Growth, Reflect |
| Nidorina | Nidorina → Nidoqueen | 105 (67/99/99) | Poison Sting, Tail Whip, Acid Rain |
| Munna | Munna → Musharna | 105 (63/102/102) | Confusion, Defense Curl, Magic Coat |
| Chinchou | Chinchou → Lanturn | 105 (64/101/101) | Water Gun, Thunder Shock, Supersonic, Parabolic Charge |
| Lileep | Lileep → Cradily | 105 (73/95/95) | Ancient Power, Mega Drain, Growth, Ingrain |
| Golett | Golett → Golurk | 104 (63/101/101) | Sand Tomb, Shadow Sneak, Defense Curl, Curse |
| Whirlipede | Whirlipede → Scolipede | 104 (64/101/101) | Pounce, Poison Sting, Defense Curl, Venom Drench |
| Lickitung | Lickitung → Lickilicky | 104 (72/95/95) | Quick Attack, Supersonic, Disable |
| Grookey | Grookey → Thwackey → Rillaboom | 104 (60/85/117) | Branch Poke, Growth, Grassy Terrain |
| Torchic | Torchic → Combusken → Blaziken | 104 (58/80/124) | Flame Charge, Peck, Growl, Roost |
| Skiddo | Skiddo → Gogoat | 104 (64/101/101) | Vine Whip, Tail Whip, Synthesis |
| Steenee | Steenee → Tsareena | 104 (52/109/109) | Vine Whip, Aromatic Mist, Grass Whistle |
| Slowpoke | Slowpoke → Slowking | 104 (65/99/99) | Confusion, Growl, Toxic |
| Petilil | Petilil → Lilligant | 104 (59/104/104) | Vine Whip, Growth, Stun Spore |
| Vullaby | Vullaby → Mandibuzz | 104 (68/97/97) | Bite, Pluck, Leer, Tailwind |
| Machop | Machop → Machoke → Machamp | 104 (67/86/108) | Mach Punch, Leer, Quick Guard |
| Duskull | Duskull → Dusclops → Dusknoir | 104 (63/84/114) | Shadow Sneak, Leer, Confuse Ray |
| Psyduck | Psyduck → Golduck | 104 (60/103/103) | Water Gun, Confusion, Cosmic Power, Amnesia |
| Jigglypuff | Jigglypuff → Wigglytuff | 104 (66/98/98) | Swift, Disarming Voice, Sweet Kiss, Sing |
| Baltoy | Baltoy → Claydol | 103 (63/101/101) | Mud Shot, Confusion, Cosmic Power, Power Split |
| Zorua | Zorua → Zoroark | 103 (63/100/100) | Swift, Infernal Parade, Leer, Curse |
| Dottler | Dottler → Orbeetle | 103 (62/101/101) | Struggle Bug, Confusion, Supersonic, Magic Coat |
| Krabby | Krabby → Kingler | 103 (65/99/99) | Aqua Jet, Leer, Protect |
| Elgyem | Elgyem → Beheeyem | 103 (68/97/97) | Confusion, Growl, Power Split |
| Cubchoo | Cubchoo → Beartic | 103 (58/104/104) | Ice Shard, Growl, Snowscape |
| Vulpix | Vulpix → Ninetales | 103 (57/104/104) | Ember, Tail Whip, Will-O-Wisp |
| Salandit | Salandit → Salazzle | 103 (64/99/99) | Acid, Ember, Sand Attack, Poison Gas |
| Dratini | Dratini → Dragonair → Dragonite | 103 (57/80/124) | Breaking Swipe, Leer, Roost |
| Scorbunny | Scorbunny → Raboot → Cinderace | 103 (62/86/112) | Flame Charge, Growl, Agility |
| Lombre | Lombre → Ludicolo | 103 (70/95/95) | Aqua Jet, Vine Whip, Tickle, Life Dew |
| Skorupi | Skorupi → Drapion | 103 (60/101/101) | Poison Sting, Pounce, Leer, Hone Claws |
| Swablu | Swablu → Altaria | 103 (57/104/104) | Quick Attack, Peck, Growl, Sing |
| Slugma | Slugma → Magcargo | 103 (61/101/101) | Ember, Smokescreen, Yawn |
| Trapinch | Trapinch → Vibrava → Flygon | 103 (66/77/114) | Pounce, Sand Tomb, Sand Attack, Bulldoze |
| Aron | Aron → Lairon → Aggron | 103 (66/85/106) | Metal Claw, Harden, Autotomize |
| Houndour | Houndour → Houndoom | 102 (62/100/100) | Shadow Siphon, Ember, Leer, Beat Up |
| Sizzlipede | Sizzlipede → Centiskorch | 102 (58/102/102) | Flame Charge, Pounce, Smokescreen, Lunge |
| Numel | Numel → Camerupt | 102 (66/97/97) | Ember, Mud Shot, Growth, Bulldoze |
| Silicobra | Silicobra → Sandaconda | 102 (60/101/101) | Sand Tomb, Sand Attack, Bulldoze |
| Zorua | Zorua → Zoroark | 102 (61/100/100) | Shadow Siphon, Leer, Hone Claws |
| Snubbull | Snubbull → Granbull | 102 (66/96/96) | Disarming Voice, Tail Whip, Charm |
| Stunky | Stunky → Skuntank | 102 (64/97/97) | Poison Fang, Bite, Leer, Poison Gas |
| Paras | Paras → Parasect | 102 (66/96/96) | Pounce, Vine Whip, Growth, Fungal Control |
| Shroomish | Shroomish → Breloom | 102 (56/103/103) | Vine Whip, Growth, Stun Spore |
| Clamperl | Clamperl → Huntail | 101 (64/97/97) | Aqua Jet, Supersonic, Clamp |
| Drifloon | Drifloon → Drifblim | 101 (65/96/96) | Infernal Parade, Gust, Focus Energy, Tailwind |
| Beldum | Beldum → Metang → Metagross | 101 (58/78/120) | Bullet Punch, Heart Stamp, Iron Defense, Transmutation |
| Sobble | Sobble → Drizzile → Inteleon | 101 (62/87/108) | Water Gun, Growl, Soak |
| Weepinbell | Weepinbell → Victreebel | 101 (71/92/92) | Vine Whip, Poison Fang, Tickle, Stun Spore |
| Buizel | Buizel → Floatzel | 101 (62/98/98) | Aqua Jet, Growl, Soak |
| Slowpoke | Slowpoke → Slowbro | 101 (65/95/95) | Water Gun, Confusion, Growl, Amnesia |
| Noibat | Noibat → Noivern | 101 (47/108/108) | Gust, Twister, Supersonic, Tailwind |
| Spoink | Spoink → Grumpig | 101 (71/91/91) | Confusion, Swift, Cosmic Power, Psychic Terrain |
| Greavard | Greavard → Houndstone | 101 (59/99/99) | Shadow Sneak, Tail Whip, Rest |
| Venonat | Venonat → Venomoth | 101 (58/100/100) | Struggle Bug, Acid, Supersonic, Poison Powder |
| Bergmite | Bergmite → Avalugg | 101 (62/98/98) | Ice Shard, Harden, Icy Wind |
| Solosis | Solosis → Duosion → Reuniclus | 101 (67/82/103) | Confusion, Charm, Reflect |
| Pidgeotto | Pidgeotto → Pidgeot | 101 (66/95/95) | Quick Attack, Wing Attack, Sand Attack, Tailwind |
| Oddish | Oddish → Gloom → Vileplume | 101 (66/79/107) | Mega Drain, Acid, Growth, Moonlight |
| Vulpix | Vulpix → Ninetales | 100 (55/102/102) | Icy Wind, Tail Whip, Mist |
| Barboach | Barboach → Whiscash | 100 (59/99/99) | Aqua Jet, Bulldoze, Tickle, Mud-Slap |
| Tirtouga | Tirtouga → Carracosta | 100 (68/92/92) | Aqua Jet, Rock Throw, Withdraw, Wide Guard |
| Minccino | Minccino → Cinccino | 100 (59/99/99) | Quick Attack, Tail Whip, Sing |
| Helioptile | Helioptile → Heliolisk | 100 (57/101/101) | Thunder Shock, Swift, Tail Whip, Parabolic Charge |
| Ledyba | Ledyba → Ledian | 100 (52/103/103) | Pounce, Tackle, Supersonic, Safeguard |
| Buneary | Buneary → Lopunny | 100 (68/93/93) | Quick Attack, Cosmic Power, After You |
| Geodude | Geodude → Graveler → Golem | 100 (66/81/104) | Rock Throw, Sand Tomb, Cosmic Power, Rock Polish |
| Snorunt | Snorunt → Froslass | 100 (57/100/100) | Icy Wind, Leer, Confuse Ray |
| Toedscool | Toedscool → Toedscruel | 100 (58/99/99) | Mud Shot, Mega Drain, Growth, Stun Spore |
| Marill | Marill → Azumarill | 100 (57/100/100) | Water Gun, Disarming Voice, Tickle, Aqua Ring |
| Ferroseed | Ferroseed → Ferrothorn | 100 (62/96/96) | Vine Whip, Metal Claw, Harden, Ingrain |
| Litwick | Litwick → Lampent → Chandelure | 100 (60/76/115) | Infernal Parade, Ember, Acid Armor, Will-O-Wisp |
| Roggenrola | Roggenrola → Boldore → Gigalith | 100 (60/80/111) | Accelerock, Sand Attack, Sandstorm |
| Fennekin | Fennekin → Braixen → Delphox | 100 (58/81/113) | Ember, Tail Whip, Light Screen |
| Seel | Seel → Dewgong | 99 (58/98/98) | Water Gun, Growl, Aqua Ring |
| Clobbopus | Clobbopus → Grapploct | 99 (61/96/96) | Rock Smash, Leer, Octolock |
| Jangmo-o | Jangmo-o → Hakamo-o → Kommo-o | 99 (56/77/118) | Breaking Swipe, Leer, Protect |
| Trubbish | Trubbish → Garbodor | 99 (60/96/96) | Poison Fang, Sand Attack, Poison Gas |
| Dreepy | Dreepy → Drakloak → Dragapult | 99 (53/81/117) | Breaking Swipe, Shadow Sneak, Agility, Infestation |
| Spritzee | Spritzee → Aromatisse | 99 (67/91/91) | Fairy Wind, Sweet Kiss, Misty Terrain |
| Swinub | Swinub → Piloswine → Mamoswine | 99 (49/89/115) | Ice Shard, Sand Tomb, Amnesia, Mist |
| Arrokuda | Arrokuda → Barraskewda | 99 (55/100/100) | Aqua Jet, Focus Energy, Agility |
| Wimpod | Wimpod → Golisopod | 99 (45/106/106) | Pounce, Aqua Jet, Sand Attack, Struggle Bug |
| Gulpin | Gulpin → Swalot | 98 (62/94/94) | Acid Spray, Amnesia, Poison Gas |
| Blitzle | Blitzle → Zebstrika | 98 (56/98/98) | Spark, Tail Whip, Thunder Wave |
| Carvanha | Carvanha → Sharpedo | 98 (59/96/96) | Aqua Jet, Bite, Leer, Focus Energy |
| Quaxly | Quaxly → Quaxwell → Quaquaval | 98 (59/78/110) | Aqua Jet, Work Up, Counter |
| Drowzee | Drowzee → Hypno | 98 (58/97/97) | Confusion, Barrier, Hypnosis |
| Tadbulb | Tadbulb → Bellibolt | 98 (55/99/99) | Thunder Shock, Charge, Electric Terrain |
| Turtwig | Turtwig → Grotle → Torterra | 98 (63/80/103) | Vine Whip, Tickle, Synthesis |
| Fuecoco | Fuecoco → Crocalor → Skeledirge | 98 (60/81/106) | Ember, Leer, Will-O-Wisp |
| Voltorb | Voltorb → Electrode | 98 (65/91/91) | Thunder Shock, Mega Drain, Charge, Stun Spore |
| Clefairy | Clefairy → Clefable | 98 (62/93/93) | Disarming Voice, Growl, Moonlight |
| Flittle | Flittle → Espathra | 98 (50/102/102) | Confusion, Growl, Agility |
| Lillipup | Lillipup → Herdier → Stoutland | 98 (56/78/114) | Tackle, Leer, Helping Hand |
| Phantump | Phantump → Trevenant | 98 (60/95/95) | Shadow Sneak, Branch Poke, Growth, Leech Seed |
| Frillish | Frillish → Jellicent | 98 (64/92/92) | Water Gun, Infernal Parade, Acid Armor, Rain Dance |
| Sandygast | Sandygast → Palossand | 98 (64/92/92) | Infernal Parade, Mud Shot, Sand Attack, Sand Tomb |
| Fidough | Fidough → Dachsbun | 98 (60/95/95) | Disarming Voice, Tail Whip, Charm |
| Croagunk | Croagunk → Toxicroak | 98 (54/98/98) | Poison Sting, Rock Smash, Meditate, Acid Rain |

### Tier C (101)

| soort | acts | V | startmoves |
|---|---|---|---|
| Popplio | Popplio → Brionne → Primarina | 98 (61/79/106) | Water Gun, Growl, Misty Terrain |
| Panpour | Panpour → Simipour | 97 (57/96/96) | Aqua Jet, Leer, Taunt |
| Pansage | Pansage → Simisage | 97 (57/96/96) | Vine Whip, Leer, Leech Seed |
| Pansear | Pansear → Simisear | 97 (57/96/96) | Flame Charge, Leer, Yawn |
| Sprigatito | Sprigatito → Floragato → Meowscarada | 97 (59/81/106) | Leafage, Tail Whip, Worry Seed |
| Remoraid | Remoraid → Octillery | 97 (54/98/98) | Water Gun, Supersonic, Soak |
| Zubat | Zubat → Golbat → Crobat | 97 (48/91/111) | Poison Fang, Wing Attack, Supersonic, Venom Drench |
| Charmander | Charmander → Charmeleon → Charizard | 97 (57/79/110) | Ember, Growl, Fire Spin |
| Cyndaquil | Cyndaquil → Quilava → Typhlosion | 97 (57/79/110) | Ember, Smokescreen, Leer |
| Dwebble | Dwebble → Crustle | 97 (61/93/93) | Pounce, Accelerock, Sand Attack, Rock Polish |
| Meowth | Meowth → Persian | 97 (59/95/95) | Shadow Siphon, Growl, Taunt |
| Yamper | Yamper → Boltund | 97 (53/99/99) | Spark, Tail Whip, Nuzzle |
| Totodile | Totodile → Croconaw → Feraligatr | 97 (61/76/107) | Aqua Jet, Leer, Scary Face |
| Meowth | Meowth → Perrserker | 97 (60/93/93) | Metal Claw, Growl, Iron Defense |
| Archen | Archen → Archeops | 97 (63/92/92) | Rock Throw, Pluck, Leer, Tailwind |
| Wattrel | Wattrel → Kilowattrel | 97 (54/98/98) | Thunder Shock, Gust, Growl, Roost |
| Joltik | Joltik → Galvantula | 97 (59/94/94) | Struggle Bug, Charge Beam, Screech, Electroweb |
| Litten | Litten → Torracat → Incineroar | 97 (59/80/105) | Flame Charge, Growl, Scary Face |
| Shroodle | Shroodle → Grafaiai | 97 (57/95/95) | Poison Fang, Quick Attack, Leer, Substitute |
| Skitty | Skitty → Delcatty | 97 (57/95/95) | Quick Attack, Tickle, Heal Bell |
| Goomy | Goomy → Sliggoo → Goodra | 97 (54/81/110) | Twister, Acid Armor, Protect |
| Horsea | Horsea → Seadra → Kingdra | 97 (56/86/104) | Water Gun, Smokescreen, Whirlpool |
| Treecko | Treecko → Grovyle → Sceptile | 97 (59/79/104) | Leafage, Leer, Mega Drain |
| Bramblin | Bramblin → Brambleghast | 96 (53/98/98) | Vine Whip, Shadow Sneak, Defense Curl, Curse |
| Swirlix | Swirlix → Slurpuff | 96 (63/90/90) | Fairy Wind, Fake Tears, Draining Kiss |
| Rellor | Rellor → Rabsca | 96 (54/97/97) | Struggle Bug, Cosmic Power, Speed Swap |
| Skwovet | Skwovet → Greedent | 96 (56/95/95) | Tackle, Tail Whip, Stuff Cheeks |
| Wooloo | Wooloo → Dubwool | 96 (50/100/100) | Tackle, Growl, Guard Split |
| Tepig | Tepig → Pignite → Emboar | 96 (59/80/103) | Flame Charge, Tail Whip, Endure |
| Mudkip | Mudkip → Marshtomp → Swampert | 96 (60/80/102) | Aqua Jet, Growl, Life Dew |
| Yamask | Yamask → Cofagrigus | 96 (59/93/93) | Infernal Parade, Fake Tears, Curse |
| Yamask | Yamask → Runerigus | 96 (59/93/93) | Sand Tomb, Shadow Sneak, Scary Face, Curse |
| Taillow | Taillow → Swellow | 96 (59/93/93) | Peck, Growl, Roost |
| Grubbin | Grubbin → Charjabug → Vikavolt | 96 (56/77/109) | Struggle Bug, Charge, String Shot |
| Klink | Klink → Klang → Klinklang | 96 (57/80/105) | Bullet Punch, Charge, Gear Up |
| Bulbasaur | Bulbasaur → Ivysaur → Venusaur | 96 (60/76/104) | Mega Drain, Acid, Growth, Leech Seed |
| Snover | Snover → Abomasnow | 95 (61/91/91) | Leafage, Ice Shard, Leer, Mist |
| Skrelp | Skrelp → Dragalge | 95 (60/91/91) | Acid, Water Gun, Smokescreen, Acid Rain |
| Froakie | Froakie → Frogadier → Greninja | 95 (58/80/102) | Water Gun, Growl, Role Play |
| Starly | Starly → Staravia → Staraptor | 95 (49/75/117) | Quick Attack, Wing Attack, Growl, Agility |
| Chespin | Chespin → Quilladin → Chesnaught | 95 (60/75/103) | Vine Whip, Growl, Leech Seed |
| Oshawott | Oshawott → Dewott → Samurott | 95 (58/76/104) | Water Gun, Tail Whip, Soak |
| Shelmet | Shelmet → Accelgor | 94 (55/93/93) | Struggle Bug, Acid Armor, Yawn |
| Spheal | Spheal → Sealeo → Walrein | 94 (58/77/102) | Icy Wind, Water Gun, Growl, Snow Storm |
| Koffing | Koffing → Weezing | 94 (61/89/89) | Poison Fang, Smokescreen, Poison Gas |
| Geodude | Geodude → Graveler → Golem | 94 (62/76/99) | Rock Throw, Spark, Defense Curl, Rock Polish |
| Piplup | Piplup → Prinplup → Empoleon | 94 (59/75/102) | Water Gun, Growl, Whirlpool |
| Rowlet | Rowlet → Dartrix → Decidueye | 94 (59/77/100) | Leafage, Peck, Growl, Synthesis |
| Chansey | Chansey → Blissey | 94 (62/88/88) | Swift, Tail Whip, Sing |
| Honedge | Honedge → Doublade | 94 (65/86/86) | Bullet Punch, Shadow Sneak, Iron Defense, Autotomize |
| Vanillite | Vanillite → Vanillish → Vanilluxe | 94 (58/73/105) | Icy Wind, Harden, Snow Storm |
| Glameow | Glameow → Purugly | 94 (60/89/89) | Quick Attack, Tail Whip, Fake Out |
| Onix | Onix → Steelix | 93 (61/88/88) | Rock Throw, Sand Tomb, Harden, Autotomize |
| Cottonee | Cottonee → Whimsicott | 93 (53/94/94) | Mega Drain, Fairy Wind, Growth, Stun Spore |
| Bronzor | Bronzor → Bronzong | 93 (53/93/93) | Bullet Punch, Heart Stamp, Iron Defense, Hypnosis |
| Chimchar | Chimchar → Monferno → Infernape | 93 (56/76/104) | Flame Charge, Leer, Fire Spin |
| Pikipek | Pikipek → Trumbeak → Toucannon | 93 (57/76/101) | Quick Attack, Peck, Growl, Roost |
| Shinx | Shinx → Luxio → Luxray | 93 (55/72/107) | Spark, Leer, Electric Terrain |
| Ducklett | Ducklett → Swanna | 93 (55/91/91) | Aqua Jet, Wing Attack, Feather Dance, Aqua Ring |
| Capsakid | Capsakid → Scovillain | 92 (55/90/90) | Leafage, Leer, Spicy Extract |
| Wingull | Wingull → Pelipper | 92 (54/91/91) | Water Gun, Gust, Growl, Tailwind |
| Finneon | Finneon → Lumineon | 92 (59/87/87) | Aqua Jet, Tickle, Rain Dance |
| Applin | Applin → Appletun | 92 (49/94/94) | Mega Drain, Twister, Growth, Leech Seed |
| Shellder | Shellder → Cloyster | 92 (56/89/89) | Aqua Jet, Leer, Whirlpool |
| Yungoos | Yungoos → Gumshoos | 92 (55/89/89) | Tackle, Leer, Yawn |
| Snivy | Snivy → Servine → Serperior | 92 (55/76/100) | Vine Whip, Leer, Leech Seed |
| Skiploom | Skiploom → Jumpluff | 91 (62/84/84) | Vine Whip, Peck, Tail Whip, Stun Spore |
| Squirtle | Squirtle → Wartortle → Blastoise | 91 (57/72/100) | Water Gun, Tail Whip, Rain Dance |
| Foongus | Foongus → Amoonguss | 91 (58/87/87) | Vine Whip, Poison Fang, Growth, Stun Spore |
| Spearow | Spearow → Fearow | 91 (53/90/90) | Quick Attack, Peck, Leer, Roost |
| Pineco | Pineco → Forretress | 91 (59/85/85) | Pounce, Iron Defense, Curse |
| Chikorita | Chikorita → Bayleef → Meganium | 91 (57/72/99) | Mega Drain, Growl, Synthesis |
| Gothita | Gothita → Gothorita → Gothitelle | 90 (57/75/96) | Confusion, Tickle, Hypnosis |
| Hatenna | Hatenna → Hattrem → Hatterene | 90 (54/74/100) | Confusion, Aromatic Mist, Heal Pulse |
| Meowth | Meowth → Persian | 90 (57/86/86) | Pay Day, Tail Whip, Fake Out |
| Nickit | Nickit → Thievul | 90 (48/92/92) | Shadow Siphon, Tail Whip, Hone Claws |
| Fomantis | Fomantis → Lurantis | 89 (48/91/91) | Leafage, Growth, Ingrain |
| Impidimp | Impidimp → Morgrem → Grimmsnarl | 89 (51/72/101) | Bite, Disarming Voice, Confide, Flatter |
| Nincada | Nincada → Ninjask | 89 (52/88/88) | Pounce, Sand Tomb, Sand Attack, Leech Life |
| Morelull | Morelull → Shiinotic | 89 (60/82/82) | Mega Drain, Disarming Voice, Growth, Moonlight |
| Rattata | Rattata → Raticate | 88 (53/86/86) | Quick Attack, Tail Whip, Laser Focus |
| Diglett | Diglett → Dugtrio | 88 (51/87/87) | Bulldoze, Metal Claw, Growl, Mud-Slap |
| Hoothoot | Hoothoot → Noctowl | 88 (48/89/89) | Swift, Gust, Growl, Roost |
| Woobat | Woobat → Swoobat | 88 (59/81/81) | Confusion, Gust, Supersonic, Amnesia |
| Fletchling | Fletchling → Fletchinder → Talonflame | 88 (52/75/94) | Quick Attack, Peck, Growl, Tailwind |
| Gossifleur | Gossifleur → Eldegoss | 87 (50/86/86) | Mega Drain, Growth, Synthesis |
| Shieldon | Shieldon → Bastiodon | 86 (58/80/80) | Accelerock, Bullet Punch, Screech, Iron Defense |
| Cubone | Cubone → Marowak | 86 (58/80/80) | Sand Tomb, Tail Whip, Mud-Slap |
| Diglett | Diglett → Dugtrio | 86 (51/85/85) | Bulldoze, Growl, Mud-Slap |
| Purrloin | Purrloin → Liepard | 86 (51/84/84) | Feint Attack, Growl, Hone Claws |
| Rookidee | Rookidee → Corvisquire → Corviknight | 86 (47/72/98) | Peck, Leer, Iron Defense |
| Rattata | Rattata → Raticate | 85 (52/83/83) | Bite, Quick Attack, Tail Whip, Focus Energy |
| Patrat | Patrat → Watchog | 85 (51/83/83) | Tackle, Leer, Rototiller |
| Wooper | Wooper → Clodsire | 85 (47/86/86) | Poison Tail, Sand Tomb, Tail Whip, Toxic |
| Wiglett | Wiglett → Wugtrio | 85 (48/85/85) | Aqua Jet, Sand Attack, Wrap |
| Sentret | Sentret → Furret | 84 (46/85/85) | Quick Attack, Defense Curl, Follow Me |
| Bidoof | Bidoof → Bibarel | 83 (50/82/82) | Tackle, Growl, Yawn |
| Rolycoly | Rolycoly → Carkol → Coalossal | 83 (46/73/93) | Accelerock, Smokescreen, Tar Shot |
| Wooper | Wooper → Quagsire | 83 (47/83/83) | Aqua Jet, Sand Tomb, Tail Whip, Rain Dance |
| Spinarak | Spinarak → Ariados | 82 (52/78/78) | Pounce, Poison Sting, String Shot, Toxic Thread |
| Tarountula | Tarountula → Spidops | 78 (45/78/78) | Pounce, String Shot, Struggle Bug |

### Alleen via events (te sterk voor de draft)

Eenstaps-soorten met een rating boven 106 (5% boven de mediaan van act 3). In act 1 zouden ze bijna 2× zo sterk zijn als een eerste vorm en daarmee act 1 breken; via een event kosten ze iets (HP, geld of een move).

- Gholdengo (129): Mirror Shot, Infernal Parade, Metal Sound, Confuse Ray
- Gyarados (128): Aqua Jet, Peck, Scary Face, Whirlpool
- Heracross (121): Pounce, Rock Smash, Leer, Pollen Haze
- Milotic (116): Chilling Water, Tickle, Aqua Ring
- Tauros (115): Mach Punch, Tail Whip, Scary Face
- Kricketune (113): Pounce, Growl, Infestation
- Volbeat (113): Ember, Thunder Shock, Flash, Fire Spin
- Solrock (111): Accelerock, Heart Stamp, Harden, Morning Sun
- Zangoose (111): Quick Attack, Leer, Hone Claws
- Tauros (110): Tackle, Tail Whip, Scary Face
- Passimian (110): Rock Smash, Leer, Focus Energy
- Snorlax (110): Tackle, Defense Curl, Metronome
- Pinsir (109): Pounce, Bulldoze, Focus Energy, Pollen Haze
- Sawk (108): Rock Smash, Leer, Quick Guard
- Sigilyph (108): Confusion, Gust, Cosmic Power, Hypnosis
- Kangaskhan (108): Quick Attack, Tail Whip, Focus Energy
- Absol (107): Bite, Disarming Voice, Leer, Snarl
- Seviper (107): Poison Tail, Bullet Punch, Screech, Gastro Acid
- Vespiquen (84): Pounce, Peck, Defend Order, Roost
- Sunflora (83): Mega Drain, Growth, Ingrain
- Beedrill (80): Pounce, Poison Sting, Harden, String Shot
- Beautifly (80): Struggle Bug, Gust, Harden, Tailwind
- Butterfree (80): Struggle Bug, Gust, Supersonic, Rage Powder
- Diggersby (79): Quick Attack, Bulldoze, Leer, Laser Focus

## Afgevallen

- Alomomola: geen evolutie en zwakker dan een gemiddelde act-2-vorm (91 < 95)
- Arctovish: geen evolutie en zwakker dan een gemiddelde act-2-vorm (94 < 95); geen basis-statusmove
- Arctozolt: geen evolutie en zwakker dan een gemiddelde act-2-vorm (94 < 95); geen grounded move
- Audino: geen evolutie en zwakker dan een gemiddelde act-2-vorm (79 < 95)
- Bellsprout: act 2 te zwak (WEEPINBELL 71 < 71)
- Blipbug: act 1 te zwak (BLIPBUG 35 < 45); act 2 te zwak (DOTTLER 62 < 71)
- Bounsweet: act 1 te zwak (BOUNSWEET 41 < 45); act 2 te zwak (STEENEE 52 < 71)
- Bunnelby: act 1 te zwak (BUNNELBY 44 < 45)
- Carbink: geen evolutie en zwakker dan een gemiddelde act-2-vorm (78 < 95)
- Carnivine: geen evolutie en zwakker dan een gemiddelde act-2-vorm (88 < 95)
- Cascoon: act 1 te zwak (CASCOON 44 < 45); act 3 te zwak (DUSTOX 72 < 76)
- Caterpie: act 1 te zwak (CATERPIE 39 < 45); act 2 te zwak (METAPOD 40 < 71)
- Chatot: geen evolutie en zwakker dan een gemiddelde act-2-vorm (83 < 95)
- Cherubi: act 2 te zwak (CHERUBI 56 < 71); act 3 te zwak (CHERUBI 56 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (56 < 95)
- Chewtle: geen basis-statusmove
- Clauncher: geen basis-statusmove
- Combee: act 1 te zwak (COMBEE 44 < 45)
- Corsola: geen evolutie en zwakker dan een gemiddelde act-2-vorm (82 < 95)
- Cramorant: geen evolutie en zwakker dan een gemiddelde act-2-vorm (89 < 95)
- Cutiefly: geen basis-statusmove
- Darumaka: act 2 te zwak (DARUMAKA 70 < 71); act 3 te zwak (DARUMAKA 70 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (70 < 95)
- Dedenne: geen evolutie en zwakker dan een gemiddelde act-2-vorm (87 < 95)
- Delibird: act 2 te zwak (DELIBIRD 62 < 71); act 3 te zwak (DELIBIRD 62 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (62 < 95); geen basis-statusmove
- Dewpider: geen basis-statusmove
- Ditto: act 2 te zwak (DITTO 52 < 71); act 3 te zwak (DITTO 52 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (52 < 95); geen basis-statusmove
- Dracovish: geen basis-statusmove
- Dracozolt: geen grounded move
- Drampa: geen basis-statusmove
- Dunsparce: geen evolutie en zwakker dan een gemiddelde act-2-vorm (76 < 95)
- Dustox: act 3 te zwak (DUSTOX 72 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (72 < 95)
- Emolga: geen evolutie en zwakker dan een gemiddelde act-2-vorm (80 < 95)
- Espurr: act 2 te zwak (ESPURR 67 < 71); act 3 te zwak (ESPURR 67 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (67 < 95)
- Falinks: geen evolutie en zwakker dan een gemiddelde act-2-vorm (92 < 95)
- Feebas: act 1 te zwak (FEEBAS 36 < 45)
- Finizen: act 2 te zwak (FINIZEN 57 < 71); act 3 te zwak (FINIZEN 57 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (57 < 95)
- Heatmor: geen evolutie en zwakker dan een gemiddelde act-2-vorm (91 < 95)
- Hoppip: act 2 te zwak (SKIPLOOM 62 < 71)
- Inkay: geen basis-statusmove
- Kakuna: act 1 te zwak (KAKUNA 39 < 45)
- Kecleon: geen evolutie en zwakker dan een gemiddelde act-2-vorm (92 < 95)
- Klawf: geen evolutie en zwakker dan een gemiddelde act-2-vorm (94 < 95)
- Klefki: geen evolutie en zwakker dan een gemiddelde act-2-vorm (90 < 95)
- Kricketot: act 1 te zwak (KRICKETOT 39 < 45)
- Lechonk: act 2 te zwak (LECHONK 50 < 71); act 3 te zwak (LECHONK 50 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (50 < 95)
- Lotad: act 2 te zwak (LOMBRE 70 < 71)
- Luvdisc: geen evolutie en zwakker dan een gemiddelde act-2-vorm (80 < 95)
- Magikarp: act 1 te zwak (MAGIKARP 36 < 45)
- Mantine: geen evolutie en zwakker dan een gemiddelde act-2-vorm (94 < 95)
- Maractus: geen evolutie en zwakker dan een gemiddelde act-2-vorm (87 < 95)
- Mareanie: geen basis-statusmove
- Mareep: act 2 te zwak (FLAAFFY 71 < 71)
- Mawile: geen evolutie en zwakker dan een gemiddelde act-2-vorm (92 < 95)
- Metapod: act 1 te zwak (METAPOD 40 < 45)
- Mienfoo: geen basis-statusmove
- Milcery: act 2 te zwak (MILCERY 52 < 71); act 3 te zwak (MILCERY 52 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (52 < 95)
- Minun: geen evolutie en zwakker dan een gemiddelde act-2-vorm (92 < 95)
- Mr. Mime: geen evolutie en zwakker dan een gemiddelde act-2-vorm (94 < 95)
- Nacli: act 2 te zwak (NACLSTACK 67 < 71)
- Nidoran♀: act 2 te zwak (NIDORINA 67 < 71)
- Nidoran♂: act 2 te zwak (NIDORINO 69 < 71)
- Nymble: act 1 te zwak (NYMBLE 44 < 45)
- Oranguru: geen evolutie en zwakker dan een gemiddelde act-2-vorm (95 < 95); geen basis-statusmove
- Orthworm: geen evolutie en zwakker dan een gemiddelde act-2-vorm (86 < 95)
- Pachirisu: act 3 te zwak (PACHIRISU 73 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (73 < 95)
- Pawmi: act 2 te zwak (PAWMO 70 < 71)
- Pidgey: act 2 te zwak (PIDGEOTTO 66 < 71)
- Pidove: act 2 te zwak (TRANQUILL 69 < 71)
- Pincurchin: geen evolutie en zwakker dan een gemiddelde act-2-vorm (82 < 95)
- Plusle: geen evolutie en zwakker dan een gemiddelde act-2-vorm (94 < 95)
- Poliwag: geen basis-statusmove
- Pyukumuku: geen evolutie en zwakker dan een gemiddelde act-2-vorm (78 < 95)
- Qwilfish: geen evolutie en zwakker dan een gemiddelde act-2-vorm (91 < 95)
- Ralts: act 1 te zwak (RALTS 42 < 45); act 2 te zwak (KIRLIA 55 < 71)
- Rockruff: act 2 te zwak (ROCKRUFF 57 < 71); act 3 te zwak (ROCKRUFF 57 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (57 < 95)
- Seedot: act 2 te zwak (NUZLEAF 69 < 71)
- Sewaddle: act 2 te zwak (SWADLOON 69 < 71)
- Shuckle: act 2 te zwak (SHUCKLE 55 < 71); act 3 te zwak (SHUCKLE 55 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (55 < 95)
- Silcoon: act 1 te zwak (SILCOON 44 < 45)
- Skarmory: geen evolutie en zwakker dan een gemiddelde act-2-vorm (93 < 95)
- Slakoth: act 1 te zwak (SLAKOTH 38 < 45)
- Smeargle: act 2 te zwak (SMEARGLE 46 < 71); act 3 te zwak (SMEARGLE 46 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (46 < 95); geen basis-statusmove; geen grounded move
- Smoliv: act 2 te zwak (DOLLIV 69 < 71)
- Snom: act 1 te zwak (SNOM 43 < 45)
- Spiritomb: geen evolutie en zwakker dan een gemiddelde act-2-vorm (85 < 95)
- Stonjourner: geen evolutie en zwakker dan een gemiddelde act-2-vorm (94 < 95); geen basis-statusmove
- Stunfisk: geen evolutie en zwakker dan een gemiddelde act-2-vorm (90 < 95)
- Stunfisk: geen evolutie en zwakker dan een gemiddelde act-2-vorm (90 < 95)
- Sudowoodo: geen evolutie en zwakker dan een gemiddelde act-2-vorm (86 < 95)
- Sunkern: act 1 te zwak (SUNKERN 37 < 45)
- Tandemaus: act 2 te zwak (TANDEMAUS 58 < 71); act 3 te zwak (TANDEMAUS 58 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (58 < 95)
- Tinkatink: act 2 te zwak (TINKATUFF 71 < 71)
- Torkoal: geen evolutie en zwakker dan een gemiddelde act-2-vorm (87 < 95)
- Tropius: geen evolutie en zwakker dan een gemiddelde act-2-vorm (90 < 95)
- Turtonator: geen evolutie en zwakker dan een gemiddelde act-2-vorm (87 < 95)
- Tympole: act 2 te zwak (PALPITOAD 70 < 71)
- Tynamo: geen basis-statusmove
- Veluza: geen evolutie en zwakker dan een gemiddelde act-2-vorm (94 < 95); geen grounded move
- Venipede: act 2 te zwak (WHIRLIPEDE 64 < 71)
- Weedle: act 1 te zwak (WEEDLE 39 < 45); act 2 te zwak (KAKUNA 39 < 71)
- Whismur: act 2 te zwak (LOUDRED 71 < 71)
- Wobbuffet: act 2 te zwak (WOBBUFFET 70 < 71); act 3 te zwak (WOBBUFFET 70 < 76); geen evolutie en zwakker dan een gemiddelde act-2-vorm (70 < 95)
- Wurmple: act 2 te zwak (SILCOON 44 < 71)

## Beloningsmoves

**Common (129):** Acid Armor, Acrobatics, Aerial Ace, After You, Agility, Air Cutter, Air Slash, Amnesia, Ancient Power, Aqua Ring, Assurance, Aurora Beam, Avalanche, Barrier, Bite, Breaking Swipe, Brick Break, Brine, Brutal Swing, Bubble Beam, Bug Bite, Bulldoze, Charge Beam, Charm, Chilling Water, Clear Smog, Confuse Ray, Confusion, Cut, Detect, Dragon Breath, Dragon Rush, Draining Kiss, Dynamic Punch, Endure, Facade, Fake Tears, Feint Attack, Fire Fang, Fire Punch, Flame Burst, Flame Charge, Flame Wheel, Focus Energy, Force Palm, Freeze-Dry, Growl, Harden, Helping Hand, Hex, Hone Claws, Horn Attack, Howl, Hurricane, Ice Fang, Ice Punch, Icicle Crash, Icy Wind, Ingrain, Iron Defense, Iron Tail, Lager Lagoon, Laser Beam, Laser Focus, Leer, Low Sweep, Magical Leaf, Metal Claw, Metal Sound, Mist, Mud Bomb, Mud Shot, Mystical Fire, Ominous Wind, Payback, Pluck, Poison Fang, Poison Powder, Poison Tail, Protect, Psybeam, Psycho Cut, Punishment, Quick Guard, Rain Dance, Rapid Spin, Razor Leaf, Retaliate, Revenge, Rock Climb, Rock Polish, Rock Throw, Rock Tomb, Safeguard, Sandstorm, Scary Face, Secret Power, Shadow Claw, Shadow Punch, Shadow Siphon, Shock Wave, Signal Beam, Silver Wind, Skitter Smack, Sludge, Smack Down, Smelling Salts, Snarl, Snowscape, Spark, Steel Wing, Stockpile, Stomping Tantrum, Struggle Bug, Sunny Day, Supersonic, Swift, Thunder, Thunder Fang, Thunder Punch, Venoshock, Vintage Spill, Vise Grip, Wake-Up Slap, Water Pulse, Weather Ball, Wing Attack, Work Up, Zen Headbutt

**Uncommon (121):** Acupressure, Aromatherapy, Aura Sphere, Baneful Bunker, Blizzard, Body Press, Body Slam, Bug Buzz, Bulk Up, Calm Mind, Coaching, Coil, Cosmic Power, Crabhammer, Crunch, Crush Claw, Curse, Dark Pulse, Decorate, Disable, Discharge, Dragon Claw, Drain Punch, Drill Peck, Earth Power, Electric Terrain, Encore, Energy Ball, Extrasensory, Fell Stinger, Fiery Dance, Fire Blast, Flamethrower, Flash Cannon, Flatter, Follow Me, Foul Play, Giga Drain, Grassy Terrain, Grass Whistle, Guard Split, Gunk Shot, Hammer Arm, Haze, Heal Bell, Heal Pulse, High Horsepower, Horn Leech, Hydro Pump, Hypnosis, Ice Beam, Inferno, Iron Head, Jaw Lock, King's Shield, Lava Plume, Leaf Blade, Leech Life, Leech Seed, Life Dew, Light Screen, Liquidation, Lunge, Mega Kick, Meteor Mash, Misty Terrain, Moonblast, Moonlight, Morning Sun, Muddy Water, Noble Roar, Play Rough, Poison Jab, Power Gem, Power Split, Psychic, Psychic Fangs, Psychic Terrain, Psyshock, Rage Powder, Reflect, Rock Slide, Roost, Sacred Sword, Scald, Seed Bomb, Shadow Ball, Sing, Slam, Sludge Bomb, Soak, Spiky Shield, Stomp, Stone Edge, Strength, Stun Spore, Submission, Substitute, Sucker Punch, Swagger, Synthesis, Tailwind, Take Down, Tar Shot, Taunt, Throat Chop, Thunderbolt, Thunder Wave, Tickle, Topsy-Turvy, Toxic, Tri Attack, Vital Throw, Waterfall, Wide Guard, Wild Charge, Will-O-Wisp, Wish, X-Scissor, Yawn, Zap Cannon

**Rare (64):** Acid Rain, Aurora Veil, Belly Drum, Boomburst, Brave Bird, Clangorous Soul, Close Combat, Cotton Guard, Dazzling Gleam, Double-Edge, Dragon Cheer, Dragon Dance, Earthquake, Eruption, Extreme Speed, Fillet Away, First Impression, Flare Blitz, Fungal Control, Glare, Head Smash, Heal Order, Heat Wave, High Jump Kick, Hyper Voice, Implosion, Jungle Healing, Leaf Storm, Lovely Kiss, Lunar Blessing, Machine Learning, Megahorn, Milk Drink, Nasty Plot, No Retreat, Outrage, Overheat, Petal Blizzard, Petal Dance, Pollen Haze, Power Whip, Quiver Dance, Recover, Seltzer Surge, Shell Smash, Shift Gear, Shore Up, Slack Off, Sleep Powder, Sludge Wave, Soft-Boiled, Spore, Strength Sap, Superpower, Surf, Swords Dance, Thrash, Tidy Up, Transmutation, Trick Room, Victory Dance, Water Spout, Wave Crash, Wood Hammer

## Ontmoetingen (gegenereerd door encounters.py)

Geschat HP-verlies van een gemiddeld team in die act (zelfde schadeformule; speler ×4 HP, 2 aanvallen per beurt op de gevaarlijkste vijand eerst; vijanden vallen in 80% van de beurten aan). Gimmicks (patronen, totem, abilities) zitten er niet in: die maken een gevecht makkelijker als je ze doorziet en zwaarder als je ze negeert. Doel per gevecht: zwak 3–12%, gewoon 6–18%, elite 15–35%, baas 40–75%.

**Kalibratie** (automatisch): per act en soort gevecht een levelverschuiving en HP-factor zodat de mediaan precies op het doel valt (in act 1/2/3: zwak 8/8/10%, gewoon 12/14/16%, elite 24/27/30%, baas 55/60/65% bij ±9 beurten; zoals Slay: gewone gevechten kosten weinig, elites en bazen veel, en elke act doet meer pijn). Level hooguit ±6 (een Grubbin op lv 66 klopt niet). Zo blijft de verhouding tussen de gevechten in een groep (de puzzel) staan, en ligt het gemiddelde vast.

| act | soort | level | HP-factor | mediaan beurten | mediaan HP-verlies |
|---|---|---|---|---|---|
| 1 | boss:Gigantamax Pikachu | +0 | ×1.8 | 12.5 | 52% |
| 1 | boss:Totem Marowak | +0 | ×0.8 | 8.5 | 56% |
| 1 | boss:Totem Wishiwashi | +0 | ×1.0 | 9.5 | 56% |
| 1 | boss:Venusaur & Blastoise | +0 | ×0.8 | 12.5 | 41% |
| 1 | elite | +0 | ×0.7 | 4.5 | 26% |
| 1 | normal | +0 | ×1.0 | 3.5 | 12% |
| 1 | weak | +0 | ×0.6 | 2.5 | 8% |
| 2 | boss:Darkrai | +0 | ×1.3 | 9.5 | 58% |
| 2 | boss:Dialga & Palkia | +0 | ×0.8 | 7.5 | 65% |
| 2 | boss:Mega Metagross | +0 | ×1.4 | 12.5 | 56% |
| 2 | boss:Mewtwo & Mew | +0 | ×1.4 | 11.5 | 66% |
| 2 | elite | +0 | ×1.0 | 5.0 | 27% |
| 2 | normal | +0 | ×1.7 | 3.5 | 13% |
| 2 | weak | +0 | ×1.5 | 2.5 | 7% |
| 3 | boss:Eternamax Eternatus | +0 | ×0.5 | 10.5 | 67% |
| 3 | boss:Mega Mewtwo Y | +0 | ×1.2 | 9.5 | 66% |
| 3 | boss:Mega Rayquaza | +0 | ×0.9 | 7.5 | 68% |
| 3 | boss:Terapagos | +0 | ×1.4 | 11.5 | 65% |
| 3 | boss:Ultra Necrozma | +0 | ×1.1 | 8.5 | 73% |
| 3 | elite | +0 | ×1.2 | 5.5 | 28% |
| 3 | normal | +0 | ×1.6 | 3.5 | 16% |
| 3 | weak | +0 | ×1.0 | 2.5 | 11% |

| act | biome | soort | ontmoeting | beurten | HP-verlies | |
|---|---|---|---|---|---|---|
| 1 | Overgrown Grove | weak | Fuzzy Crawlers (Grubbin + Cutiefly) | 1.5 | 8% |  |
| 1 | Overgrown Grove | weak | Snapping Berries (Cherubi + Bounsweet) | 2.5 | 6% |  |
| 1 | Overgrown Grove | weak | Leaf Slimes (Gulpin + Shroomish) | 2.5 | 10% |  |
| 1 | Overgrown Grove | normal | Vine Shambler (Tangela + Sewaddle) | 4.5 | 18% |  |
| 1 | Overgrown Grove | normal | Fogmog (Foongus + Paras) | 3.5 | 10% |  |
| 1 | Overgrown Grove | normal | Overgrown Statue (Sudowoodo + Bonsly) | 4.5 | 11% |  |
| 1 | Overgrown Grove | normal | Slithering Strangler (Ekans + Seedot) | 2.5 | 9% |  |
| 1 | Overgrown Grove | normal | Mawler (Teddiursa + Skwovet) | 3.5 | 17% |  |
| 1 | Overgrown Grove | normal | Jungle Ambush (Bellsprout + Hoppip) | 22.5 | 25% | te zwaar |
| 1 | Overgrown Grove | normal | Moonlight Recital (Clefairy + Clefairy) | 3.5 | 11% |  |
| 1 | Overgrown Grove | elite | Gremlin Nob (Primeape + Mankey) | 4.5 | 34% |  |
| 1 | Overgrown Grove | elite | Byrdonis (Trumbeak + Pikipek) | 3.5 | 42% | te zwaar |
| 1 | Overgrown Grove | elite | Bygone Effigy (Snorlax + Munchlax) | 8.5 | 25% |  |
| 1 | Overgrown Grove | elite | Phrog Parasite (Pyukumuku + Croagunk) | 6.5 | 13% | te makkelijk |
| 1 | Sunken Docks | weak | Corpse Slugs (Shellos + Shellos) | 3.5 | 17% | te zwaar |
| 1 | Sunken Docks | weak | Toadpoles (Tympole + Poliwag) | 1.5 | 6% |  |
| 1 | Sunken Docks | weak | Seapunks (Tentacool + Clauncher) | 2.5 | 11% |  |
| 1 | Sunken Docks | weak | Just Two Magikarp (Magikarp + Magikarp) | 1.5 | 3% | te makkelijk |
| 1 | Sunken Docks | normal | Secret Santa (Delibird + Wingull) | 2.5 | 8% |  |
| 1 | Sunken Docks | normal | Gremlin Mercs (Purrloin + Impidimp) | 2.5 | 9% |  |
| 1 | Sunken Docks | normal | Living Fog (Koffing + Stunky) | 3.5 | 13% |  |
| 1 | Sunken Docks | normal | Haunted Ship (Dhelmise + Frillish) | 4.5 | 27% | te zwaar |
| 1 | Sunken Docks | normal | Sewer Clam (Shellder + Clamperl) | 23.5 | 62% | te zwaar |
| 1 | Sunken Docks | normal | Two-Tailed Rats (Tandemaus + Rattata) | 2.5 | 22% | te zwaar |
| 1 | Sunken Docks | normal | Cultists (Wooper + Lotad) | 2.5 | 7% |  |
| 1 | Sunken Docks | elite | Terror Eel (Eelektross + Tynamo) | 4.5 | 37% | te zwaar |
| 1 | Sunken Docks | elite | Skulking Colony (Corsola + Mareanie) | 6.5 | 26% |  |
| 1 | Sunken Docks | elite | Phantasmal Gardeners (Frillish + Dreepy) | 3.5 | 8% | te makkelijk |
| 2 | The Hive | weak | Bowlbugs (Shuckle + Dwebble) | 4.5 | 5% |  |
| 2 | The Hive | weak | Exoskeletons (Nincada + Nincada) | 2.5 | 4% |  |
| 2 | The Hive | weak | Tunneler (Drilbur + Sandile) | 2.5 | 10% |  |
| 2 | The Hive | normal | Hunter Killer (Yanmega + Combee) | 3.5 | 20% | te zwaar |
| 2 | The Hive | normal | Louse Progenitor (Forretress + Venonat) | 4.5 | 12% |  |
| 2 | The Hive | normal | Mytes (Ariados + Galvantula) | 3.5 | 17% |  |
| 2 | The Hive | normal | Ovicopter (Vespiquen + Combee) | 3.5 | 8% |  |
| 2 | The Hive | normal | Spiny Toad (Ferrothorn + Cacnea) | 5.5 | 23% | te zwaar |
| 2 | The Hive | normal | Sandpit Worms (Trapinch + Silicobra) | 2.5 | 14% |  |
| 2 | The Hive | elite | Decimillipede (Scolipede + Whirlipede) | 4.5 | 18% |  |
| 2 | The Hive | elite | Entomancer (Ribombee + Volbeat) | 3.5 | 33% |  |
| 2 | The Hive | elite | The Insatiable (Sandaconda + Gligar) | 5.5 | 34% |  |
| 2 | Frostbite Hollow | weak | Snow Hares (Snorunt + Cubchoo) | 2.5 | 7% |  |
| 2 | Frostbite Hollow | weak | Living Icicles (Bergmite + Snom) | 2.5 | 6% |  |
| 2 | Frostbite Hollow | weak | Seal Pups (Spheal + Seel) | 2.5 | 8% |  |
| 2 | Frostbite Hollow | normal | Frost Byrds (Delibird + Swablu) | 3.5 | 13% |  |
| 2 | Frostbite Hollow | normal | Glass Sentries (Cryogonal + Snover) | 4.5 | 11% |  |
| 2 | Frostbite Hollow | normal | Beartic Brute (Beartic + Cubchoo) | 3.5 | 25% | te zwaar |
| 2 | Frostbite Hollow | normal | The Lost and the Forgotten (Froslass + Glalie) | 5.5 | 16% |  |
| 2 | Frostbite Hollow | normal | Avalanche (Piloswine + Swinub) | 3.5 | 13% |  |
| 2 | Frostbite Hollow | normal | Rock, Paper, Wobbuffet (Wobbuffet + Wynaut) | 7.5 | 7% |  |
| 2 | Frostbite Hollow | normal | Ice Dancers (Spinda + Jynx) | 3.5 | 5% | te makkelijk |
| 2 | Frostbite Hollow | elite | Lagavulin Matriarch (Avalugg + Bergmite) | 6.5 | 13% | te makkelijk |
| 2 | Frostbite Hollow | elite | Frozen Knight (Glalie + Snover) | 5.5 | 21% |  |
| 2 | Frostbite Hollow | elite | Kaiser Crab (Crabominable + Kingler) | 4.5 | 54% | te zwaar |
| 3 | Gilded Court | weak | Turret Operator (Bastiodon + Octillery) | 2.5 | 11% |  |
| 3 | Gilded Court | weak | Scrolls of Biting (Bronzor + Sigilyph) | 2.5 | 10% |  |
| 3 | Gilded Court | weak | Devoted Sculptor (Smeargle + Mr. Mime) | 1.5 | 10% |  |
| 3 | Gilded Court | normal | Axebots (Bisharp + Doublade) | 3.5 | 22% | te zwaar |
| 3 | Gilded Court | normal | Fabricator (Magnezone + Klinklang) | 3.5 | 31% | te zwaar |
| 3 | Gilded Court | normal | Owl Magistrate (Noctowl + Xatu) | 3.5 | 12% |  |
| 3 | Gilded Court | normal | Frog Knight (Sirfetch'd + Toxicroak) | 3.5 | 21% | te zwaar |
| 3 | Gilded Court | normal | Globe Head (Rotom + Chimecho) | 3.5 | 15% |  |
| 3 | Gilded Court | normal | Slimed Berserker (Goodra + Muk) | 5.5 | 25% | te zwaar |
| 3 | Gilded Court | normal | The Sloth (Slaking + Vigoroth) | 4.5 | 17% |  |
| 3 | Gilded Court | elite | Knights Trio (Aegislash + Escavalier) | 6.5 | 28% |  |
| 3 | Gilded Court | elite | Mecha Knight (Metagross + Bronzong) | 5.5 | 25% |  |
| 3 | Gilded Court | elite | Soul Nexus (Chandelure + Lampent) | 4.5 | 58% | te zwaar |
| 3 | The Abyss | weak | Darklings (Golbat + Sableye) | 2.5 | 13% | te zwaar |
| 3 | The Abyss | weak | Writhing Mass (Ditto + Muk) | 2.5 | 11% |  |
| 3 | The Abyss | weak | Exploders (Electrode + Spiritomb) | 2.5 | 13% | te zwaar |
| 3 | The Abyss | normal | Transient (Shedinja + Dusknoir) | 3.5 | 18% | te zwaar |
| 3 | The Abyss | normal | Nemesis (Gengar + Banette) | 2.5 | 13% |  |
| 3 | The Abyss | normal | Reptomancer (Salazzle + Salandit) | 2.5 | 7% |  |
| 3 | The Abyss | normal | Giant Head (Golurk + Golett) | 2.5 | 7% |  |
| 3 | The Abyss | normal | Spire Growth (Tangrowth + Trevenant) | 3.5 | 28% | te zwaar |
| 3 | The Abyss | normal | The Maw (Swalot + Gulpin) | 3.5 | 12% |  |
| 3 | The Abyss | normal | Nightmare (Hypno + Mismagius) | 3.5 | 16% |  |
| 3 | The Abyss | normal | The Costume (Mimikyu + Banette) | 3.5 | 12% |  |
| 3 | The Abyss | elite | Time Eater (Bronzong + Conkeldurr) | 5.5 | 22% |  |
| 3 | The Abyss | elite | Awakened One (Honchkrow + Murkrow) | 3.5 | 30% |  |
| 3 | The Abyss | elite | Donu and Deca (Solrock + Lunatone) | 6.5 | 28% |  |
| 1 | Boss | boss | Venusaur & Blastoise (Blastoise + Venusaur) | 12.5 | 41% |  |
| 1 | Boss | boss | Totem Wishiwashi (Wishiwashi + Araquanid) | 9.5 | 56% |  |
| 1 | Boss | boss | Totem Marowak (Marowak + Salazzle) | 8.5 | 56% |  |
| 1 | Boss | boss | Gigantamax Pikachu (Pikachu + Plusle) | 12.5 | 52% |  |
| 2 | Boss | boss | Mega Metagross (Metagross + Beldum) | 12.5 | 56% |  |
| 2 | Boss | boss | Darkrai (Darkrai + Misdreavus) | 9.5 | 58% |  |
| 2 | Boss | boss | Mewtwo & Mew (Mewtwo + Mew) | 11.5 | 66% |  |
| 2 | Boss | boss | Dialga & Palkia (Dialga + Palkia) | 7.5 | 65% |  |
| 3 | Boss | boss | Mega Mewtwo Y (Mewtwo + Mew) | 9.5 | 66% |  |
| 3 | Boss | boss | Ultra Necrozma (Necrozma + Lunatone) | 8.5 | 73% |  |
| 3 | Boss | boss | Eternamax Eternatus (Eternatus) | 10.5 | 67% |  |
| 3 | Boss | boss | Mega Rayquaza (Rayquaza + Altaria) | 7.5 | 68% |  |
| 3 | Boss | boss | Terapagos (Terapagos + Carbink) | 11.5 | 65% |  |

## Vergelijking met Slay the Spire (v0.8.107)

Gegenereerd door `tools/grounded/spire/runsim.py` (Monte Carlo over de echte kaartgenerator, ontmoetingen, events, geld en prijzen uit de C-code; 3000 runs per niveau). Referentie: Slay the Spire 1, A0 (Ironclad/Silent).

**Bot:** padplanner zoals een Slay-speler (elites als je gezond bent, rust vóór de baas, winkel met geld); kiest per event de optie met de hoogste verwachtingswaarde. HP-verlies per gevecht = ontmoetingsmodel (hierboven) × niveau × teamfactor (lognormaal, sd 0,25 per act: types tegen biome/baas) × relics/upgrades/items, met spreiding per gevecht (CV 0,45 gewoon, 0,5 elite, 0,3 baas; `balance.py` meet 0,6 inclusief teamverschil). Niveaus: **goed** ×0,8 (DEFEND, gimmicks doorzien), **gemiddeld** ×1,0, **slordig** ×1,5.

**Waarde-eenheden (¥)**, uit de winkelprijzen: 1% HP = 1.4¥ (Super Potion 35¥ voor 25%), relic 150¥, upgrade 56¥ (±40% HP over de rest van de run), willekeurige move = halve prijs, vasthouditem 70% van de prijs, 1 procentpunt max HP = 3× 1% HP (buffer bij elke baas).

### Kamers per act (gekozen pad)

| kamer | Slay (15 + baas) | Spire act 1 | act 2 | act 3 | Spire ×15/7 |
|---|---|---|---|---|---|
| gevecht | 5-7 | 3.1 | 3.2 | 3.2 | 6.8 |
| elite | 1-3 | 1.0 | 1.1 | 1.2 | 2.4 |
| event | 3-5 | 1.2 | 0.9 | 0.9 | 2.1 |
| winkel | 1-2 | 0.3 | 0.4 | 0.4 | 0.8 |
| rust | 2-4 | 1.3 | 1.2 | 1.2 | 2.7 |

Kaart: gevecht ±45%, event 22%, elite 8% (A0) / 13% (A1+), rust 12%, winkel 5%; verdieping 1 gevecht, 9 schatkist, 15 rust; geen elite/rust vóór verdieping 6. Spire: 7 verdiepingen + baas; verdieping 1 gevecht, 7 rust; elites vanaf verdieping 3, rust vanaf 4; kansen gevecht/event/elite/winkel/rust = 45/25/15/7/8%.

### HP per kamer (gemiddeld niveau, % van de team-HP)

| | Slay | act 1 | act 2 | act 3 |
|---|---|---|---|---|
| verlies gevecht | 5-15% | 12% (p10 3%, p90 24%) | 9% (p10 3%, p90 18%) | 10% (p10 4%, p90 19%) |
| verlies elite | 20-35% | 25% (p10 6%, p90 50%) | 24% (p10 8%, p90 49%) | 22% (p10 8%, p90 42%) |
| verlies baas | 30-50% | 47% (p10 25%, p90 72%) | 48% (p10 25%, p90 77%) | 45% (p10 24%, p90 69%) |
| aankomst bij de baas | ±70-90% | 93% (p10 75%, p90 100%) | 97% (p10 90%, p90 100%) | 98% (p10 93%, p90 100%) |
| na de baas | ±40-70% | 60% (p10 31%, p90 85%) | 67% (p10 37%, p90 90%) | 72% (p10 48%, p90 93%) |
| heal: na gevecht (effectief, per act) | Ironclad 6 HP (7,5%), Silent 0 per gevecht | 42% | 56% | 69% |
| heal: rust (effectief, per act) | 30% per rustplek | 20% | 16% | 12% |
| heal: event (effectief, per act) | wisselend | 2% | 2% | 1% |
| heal: winkel (effectief, per act) | potions | 2% | 2% | 1% |
| heal: act-overgang (effectief, per act) | 100% (A0-4), 75% van het tekort (A5+) | 28% | 26% | 0% |
| schade uit events (per act) | ±5-15% | 4% | 3% | 3% |
| rustplek: heal / upgrade | ±60/40 (act 1) | 61/38 | 47/52 | 33/66 |

### Geld en winkel (gemiddeld niveau)

| | Slay | act 1 | act 2 | act 3 |
|---|---|---|---|---|
| geld uit gevecht | ±90 | 62¥ | 73¥ | 84¥ |
| geld uit elite | ±60 | 43¥ | 53¥ | 66¥ |
| geld uit baas | ±100 | 75¥ | 90¥ | 107¥ |
| geld uit event | ±30 | 16¥ | 14¥ | 14¥ |
| totaal per act | ±250 (+99 start) | 196¥ | 230¥ | 271¥ |
| uitgegeven per act | ±200-300 | 39¥ | 101¥ | 97¥ |
| aankopen per winkelbezoek | 2-3 | 1.4 | 2.8 | 2.8 |
| relic-prijs / geld per act | 0,6-1,2 | 0.77 | 0.65 | 0.55 |
| goedkoopste move / geld per act | ±0,2 | 0.23 | 0.20 | 0.17 |

Prijzen Slay: kaart 45-55 / 68-82 / 135-165, relic 143-315, verwijderen 75+25n, potion 48-105. Spire: move 45/70/120¥, item 50/85/140¥, relic 150¥, Super Potion 35¥ (25%), Move Relearner 50+25n¥; startgeld 75¥.

### Winkans per act en run

| niveau | act 1 gehaald | act 2 | act 3 | hele run | Slay |
|---|---|---|---|---|---|
| goed | 94% | 97% | 98% | **89%** | ±70-90% (ervaren, A0) |
| gemiddeld | 89% | 92% | 95% | **78%** | 40-60% (redelijke speler, A0) |
| slordig | 66% | 69% | 75% | **34%** | <15% |

**Gevoeligheid** (winkans van de hele run tegen de HP-verliesfactor van de speler; 1,0 = het ontmoetingsmodel): ×0.65 → 95%, ×0.80 → 89%, ×1.00 → 78%, ×1.25 → 56%, ×1.50 → 34%, ×2.00 → 9%. De curve is steil, zoals in Slay: hoeveel spelkwaliteit scheelt, bepalen de gimmicks van de ontmoetingen (puzzels), niet de economie.

**Waar runs eindigen** (gemiddeld niveau; Slay: act-1-elites en de act-1/2-baas zijn de grote killers, act 2 ook gewone gevechten):

act 1 baas 25%, act 2 baas 21%, act 1 gevecht 13%, act 1 elite 11%, act 2 elite 9%, act 3 baas 9%, act 3 elite 6%, act 2 gevecht 3%, act 3 gevecht 2%

### Events (verwachtingswaarde van de beste optie voor de bot, ¥)

Slay: een event is gemiddeld ±50-100 goud waard, met gemene uitzonderingen. Doel hier (events.py): ±60-120¥; >180 = te gul, <15 = zinloos.

Gemiddeld **45¥** per event (55 events). Hoogste: clefairy 236, dojo 163, jirachi 134, ace 127, chest 116, lunch 116. Laagste: persian 0, pelipper 0, magikarp 0, rotom -0, zubat -7, dugtrio -16.

### Voor en na

| | vóór | na |
|---|---|---|
| gevecht per act | 3.14 | 3.20 |
| elite per act | 1.23 | 1.13 |
| event per act | 0.67 | 1.00 |
| winkel per act | 0.60 | 0.35 |
| rust per act | 1.31 | 1.25 |
| geld per act | 237¥ | 232¥ |
| aankomst baas act 1 | 96% | 93% |
| verlies gevecht act 1/2/3 | 13% / 7% / 10% | 12% / 9% / 10% |
| verlies elite act 1/2/3 | 20% / 21% / 18% | 25% / 24% / 22% |
| verlies baas act 1/2/3 | 47% / 42% / 37% | 47% / 48% / 45% |
| aankopen per winkel act 1 | 0.5 | 1.4 |
| rust: heal act 1 | 48% | 61% |
| relic-pool leeg (runs) | 46% | 28% |
| winkans goed | 95% | 89% |
| act 1 gehaald (goed) | 97% | 94% |
| winkans gemiddeld | 86% | 78% |
| act 1 gehaald (gemiddeld) | 91% | 89% |
| winkans slordig | 51% | 34% |
| act 1 gehaald (slordig) | 71% | 66% |
| event-EV (gemiddeld) | 43¥ | 45¥ |

### Aanpassingen (v0.8.107) en waarom

- `SPIRE_HEAL_AFTER` 10 → **8%** (`include/spire.h`): Slay's Burning Blood is 6 van 80 HP (7,5%), Silent heeft niets. Met 10% was een gewoon act-1-gevecht (±12%) bijna gratis en kwam de bot met 96% bij de baas; nu kost een gang netto een paar procent en blijft HP de grondstof over de hele act.
- `SPIRE_REST_HEAL` 40 → **30%**: zoals Slay. Rust/elite-verhouding was 40/24 = 1,7 (Slay 30/±27 ≈ 1,1); nu ±1,2: één rustplek betaalt één elite. Upgraden (±40% HP waard over de run) wint nu als je gezond bent: de echte Smith/Rest-keuze. Status gaat weg vanaf 30% (de drempel volgt de constante).
- `SPIRE_ACT_HEAL` **40%** (nieuw; was `SPIRE_REST_HEAL`): de act-overgang los van de rustplek, zelfde 40%. Slay A0 heelt alles, A5+ 75% van het tekort (±30-40% na een baas): bewust de strengere variant.
- `SPIRE_START_GOLD` 0 → **75¥** (`NewRun`): Slay begint met 99 goud (±40% van een act). Zonder startgeld kocht de bot in een act-1-winkel gemiddeld 0,5 dingen; nu ±1,4, en een eerste winkel is een echte keuze (relic sparen of nu een move).
- Relic in de winkel 120 → **150¥** (`src/spire_shop.c`): relic-prijs gedeeld door het geld van een act was 0,5 (Slay 0,6-1,2, gewone relic 150 op ±250). Relics zijn het sterkste in de winkel en de pool is klein: vóór liep hij in bijna de helft van de runs leeg.
- Kaart (`Spire_GenerateMap`): gevecht/event/elite/winkel/rust **45/25/15/7/8%** (was 45/20/15/10/10); te vroeg voor een elite = gevecht, te vroeg voor een winkel = event. Vóór had verdieping 2 25% winkels (de elite-kans viel door naar de winkel) terwijl je daar nog geen geld hebt; events per act 0,7 → 1,0 (Slay ×7/15: ±1,5-2), winkels ±0,35 per act (Slay 1-2 per 15 kamers).
- Ontmoetingen (`encounters.py`): kalibratie op **HP-verlies per act** (zwak 8/8/10%, gewoon 12/14/16%, elite 24/27/30%, baas 55/60/65%), eerder alleen op duur (alle acts gelijk). Daardoor waren act-2-gangen goedkoper dan act 1 (11% en 5% tegen 12% en 8%) en act-3-elites lichter dan act-1-elites; in Slay doet elke act meer pijn en de speler groeit (relics, upgrades, items). HP-factoren in `src/data/spire_encounters.h` opnieuw berekend; act-1-gangen gelijk, act-1-elites ×0,6 → ×0,7 (terug op het oude doel van 24%).
- Event *Mimikyu's Birthday*, *Bring a gift* 40 → **75¥** (`events.py`): een relic voor 40¥ was een kwart van de winkelprijs (EV +100¥, het op twee na gulste event); nu de halve prijs.

### Conclusies

- Per kamer zit de Spire in de Slay-banden: gang ±11%, elite ±24%, baas ±46% van de team-HP (gemiddeld niveau, alle acts).
- Kamerverdeling per act (×15/7 om met Slay te vergelijken): 6.8 gevechten, 2.4 elites, 2.1 events, 0.8 winkels, 2.7 rustplekken. Elites en rust kloppen; events en winkels zijn wat dun door de korte acts.
- HP-economie: aankomst bij de act-1-baas 93% (Slay ±70-90%); rustplekken heal/upgrade 61/38, 47/52, 33/66 per act (Slay: vroeg vaak rusten, later smeden).
- Doodsoorzaken: baas 55%, elite 26%, gang 19%. In Slay zijn act-1-elites een grotere killer; hier weegt de bot het risico mee (elites alleen als je gezond bent).
- Events zijn gemiddeld 45¥ waard (Slay ±50-100): iets minder dan een gevecht (±20¥ + een move). De dure ruil-events (betaal X voor Y tegen winkelprijs) zijn bewust neutraal; de type-opties maken ze voor het juiste team goed.

### Voor Jordi (beslissen of testen)

- **Gif, Leech Seed, weer en %-heals schalen niet mee met ×HP.** Gif doet 1/8 van de (×4) max HP = 12,5% van de balk per beurt, terwijl een klap ±10% doet. Toxic doodt elke baas (×4,5 HP) in ±6 beurten ongeacht zijn HP-vermenigvuldiger; Recover/Roost/Wish helen de helft van de balk. Het event *Toxic Spikes* kost daardoor ±20% HP per gevecht per vergiftigde Pokémon (tot de volgende rustplek). Voorstel: in de Spire schade/heal in % van de max HP delen door de HP-vermenigvuldiger (engine, `battle_util.c`), of bewust zo laten (Pokémon-kennis) maar dan Toxic/Leech Seed als rare.
- **Vastloper:** in een event waarvan elke optie geld of een type vraagt (nu *The Vending Machine*/Rotom: 20¥, 30¥ of Electric) kun je niet verder als je te weinig geld hebt en geen Electric-type. Voorstel: B = weglopen als alles op slot zit (`spire_event.c`), of een Leave-optie.
- **Relic-pool (8) is te klein** voor een Slay-ritme (±2-3 elites + baas + winkel per act = 7-10 relics per run): ook na de prijsverhoging loopt hij in ±30% van de runs leeg en dan geven elites/bazen niets meer. Slay heeft 100+ relics; 20-25 zou hier genoeg zijn.
- **Winkans:** volgens het model is de Spire nog steeds iets milder dan Slay A0 (gemiddeld niveau ±75-80% gewonnen, Slay 40-60%); bijna alle runs eindigen bij een baas. De economie (HP, geld, rust) is nu Slay-achtig; wat overblijft is hoeveel slordig spel kost (gevoeligheid hierboven). Dat hangt aan de gimmicks van de ontmoetingen en is pas na testen te meten: houd in een paar runs bij hoeveel HP elk gevecht kost, dan kan `runsim.py` de factor ijken.
- **Act-escalatie in de praktijk:** in het model wordt de speler per act ±15-35% sterker door relics/upgrades/items (schatting), waardoor gangen en elites in act 2/3 in de praktijk even duur blijven als in act 1 (Slay: ±1,5× zo duur in act 3). Na testen eventueel act 3 nog zwaarder (gewoon 18-20%).
- **Lengte:** 7 verdiepingen + baas tegen 15 + baas in Slay: per act ±3 gevechten, 1,1 elite, 1 event (Slay ±6, 2-3, 3-5). Kort en snappy, maar de run heeft daardoor ±10 beloningen minder; 9 verdiepingen zou dichter bij Slay zitten (ontwerpkeuze, niet aangepast).
- Uitschieters in de ontmoetingen (al gemarkeerd *te zwaar*), zoals Sewer Clam (62% HP) en Jungle Ambush (22 beurten), maken de gang-doden in act 1: eerst die bijstellen.
