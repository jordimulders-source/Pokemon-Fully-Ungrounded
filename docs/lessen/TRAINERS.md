# Lessen: Trainers, flags, levels en balans

Lees vóór werk aan trainers, flags/vars, levelcurve of balans. Opgesplitst uit CLAUDE.md (23 okt); nieuwe lessen hier toevoegen.

- **Trainers in `trainers.party` achteraan toevoegen** (laatste blok heeft geen `===` erna) en objecten achteraan `object_events` in map.json (vooraan verschuiven de nummers van NPC's zonder local_id).
- **Gymleider-rematches (v0.9.79):** na de Hall of Fame altijd klaar, 1× per dag per leider (`FLAG_DAILY_REMATCH_*` 0x935–0x93C), bellen via Match Call zet de leider klaar (`src/gym_leader_rematch.c`).
- **Gymleider 8 is Wallace, kampioen is Steven** (niet Juan/Wallace zoals in vanilla Emerald). Trainerconstanten heten naar het personage in de game (v0.9.84); zie `TRAINER_NAMEN.md` vóór je met trainers/flags werkt, en houd die lijst bij bij elke hernoeming. Tekstlabels (`*_Text_*`) niet hernoemen (Dialoogstudio-sleutels).
- **Winkelhouders/cameo's:** Kecleon is van Keccles (eigen rol); niet als winkelier of losse NPC gebruiken.
- **TM's zijn herbruikbaar:** nooit een TM die al ergens ligt of te koop is nog eens als beloning leggen (Jordi). Alle TM01–TM59 liggen al; nieuwe TM's komen later (richting 100). Tot dan: een ander item als beloning.
- **Trainer-id's:** max 1199 (`MAX_TRAINERS_COUNT` 1200 niet ophogen: de trainerflags en dus alle systeemflags schuiven mee). Vrij (9 okt, 50 stuks): 1017–1019, 1026–1029, 1049, 1055–1059, 1068–1069, 1080–1099, 1107–1109, 1124–1129, 1180–1185; tel opnieuw met een regex over `opponents.h` en geef agents een eigen bereik. Namen kunnen al in vanilla bestaan (`TRAINER_GERALD`): eerst grep'en.
- **Extra flags (v0.9.151, vergroot in v0.9.187):** `FLAG_GROUNDED(n)` (n 0–2047 sinds v0.9.190; daarboven valt een flag stil buiten het blok en corrumpeert hij de save: bij nieuwe bereiken eerst `NUM_GROUNDED_FLAGS` controleren) staat in een eigen blok achteraan SaveBlock1; de verdeling per onderdeel staat in `flags.h` bij `GROUNDED_FLAGS_START`. Geef elke agent een eigen bereik. Verborgen items kunnen er ook mee (flag − 0x1F4 past in u16).
- **Flags zijn bijna op** (8 okt): parallelle agents pakten dezelfde R/S-restanten (0x409, 0x465–0x467, 0x46D). Geef elke agent vooraf een eigen flagbereik, of laat ze alleen nieuwe dagelijkse flags gebruiken voor herhaalbare items. Dubbele flagwaarden opsporen: alle `#define FLAG_*` in flags.h op waarde groeperen.
- **Generatorblokken** in `flags.h`/`opponents.h` hebben elk een eigen `// }` nodig, anders overschrijft het ene script de blokken van het andere. Nieuwe items die nog nergens liggen: centrale lijst `tools/grounded/maptools/nieuwe_items.py` (controleert dubbelen/TM's). Emulatortests in grotten: `givemon` lv 100 + `setvar VAR_REPEL_STEP_COUNT, 900`.
- **Levelcurve (Jordi 12 okt):** met regulier spelen zit je 2–3 levels ónder de ace van gymleiders én bossgevechten (rivalen, Wally, Archie/Maxie, Zinnia), nooit erboven (de speler heeft al het voordeel van een menselijk brein); inhaal-EXP is alleen een vangnet. Het begin (routes tot Roxanne) blijft op de oude levels; de curve stijgt geleidelijk met de EXP die je pakt (grotere teams, nieuwe trainers/gebieden). Ophogen alleen waar nieuwe content/grotere teams de speler echt laten voorlopen; altijd ook vanuit de speler kijken (eerste trainer, eerste wilde Pokémon), niet alleen het gemiddelde.
- **Levelcurve (v0.9.192):** trainer-EXP 50% + inhaal-EXP naar de volgende mijlpaal (`src/caps.c`); gehoorzaamheidsgrens = ace van de volgende gym. Na nieuwe trainers/gymteams: `python3 tools/grounded/levelcurve.py --postgame --profile` en de gymgids-teksten (`*_Text_GymGuide*`) bijwerken. Nieuwe post-game-content: lv 83–100 (Spacetime ±91–93, superbosses 100).
- **Generator opnieuw draaien na de levelcurve:** sinds v0.9.195 houdt `check_levels.protect()` (bovenin elk bouwscript, ook in nieuwe) levels en evoluties vast; daarna `python3 tools/grounded/check_levels.py`. Scripts als heatran_lair, safari_zones, zee_vulling_2/3 herschrijven hele `map.json`'s: `git diff` op map.json controleren.
- **Trainer-id's op (9 okt):** vrijgemaakt door ongebruikte vanilla-constanten te hernoemen (CINDY_2, DUDLEY, KAYLEE, … voor de constructen; MAY_PLACEHOLDER → SickBlik); nog over: 851–853 (RED, LEAF, BRENDAN_PLACEHOLDER), eerst met grep controleren.
- **Optionele zijroutes naast een stad** (Route 111-zuid boven Mauville, 16 okt: lv 34 vóór Wattson): bij elke levelklacht ook de routes die je vanaf diezelfde stad al kunt bereiken nalopen (trainers per kaart-y + wild), niet alleen de genoemde trainer. Jordi verwacht dat zulke sprongen zonder vragen worden rechtgezet.
- **Balanstool (`tools/grounded/balance/calc.py`, `underpowered.py`):** speler-levels staan in `LEVEL_AT_STAGE` (balancedata.py) = gym-ace − 2; na een nieuwe levelcurve bijwerken, anders verliezen laat-beschikbare Pokémon alles (Electivire 0 winsten op lv 56 tegen Wallace 73). Evoluties met een plaatsvoorwaarde (Mt. Pyre, New Mauville) ziet hij als vroeg beschikbaar.
- **Wilde levels (Jordi 13 okt):** landtabel gemiddeld ±4 onder het trainerlevel van die kaart (Jordi rouleert: actieve ace ±5 onder de trainers, beste Pokémon ±2); niet-geëvolueerde vormen mogen in het wild boven hun evolutielevel. `wild_encounters.json` heeft twee notaties (mons over meerdere regels én `{ "min_level": …, "species": … }` op één regel): tekstuele bewerkingen op beide controleren.
- **Gym- en bossteams niet zelf aanpassen na een verloren gevecht** (Jordi 13 okt, Brawly's Spinda: "nee je vervangt niks"): eerst analyseren en voorstellen, pas na akkoord wijzigen. Jordi verliest bewust om te testen.


## Wilde encounters (`src/data/wild_encounters.json`)
- Land heeft precies **12 slots** met kansen 20/20/10/10/10/10/5/5/4/4/1/1. Meer of minder entries = bug (extra entries komen nooit voor).
- **Design-filosofie:** elke tabel heeft **12 unieke soorten**, geen soort in twee slots. De 1%-slots zijn dus echte zeldzaamheden.
- In oudere tabellen die nog dubbele soorten hebben: vervang bij voorkeur zo'n dubbel slot, zodat er geen soort verdwijnt.
- Elke entry heeft `min_level` én `max_level` (ontbrekende `max_level` gaf eerder lv 100-encounters).
- Schuif je slots door, behoud dan de zeldzaamheidsvolgorde (wie het zeldzaamst was, blijft dat).
- Houd rekening met evolutielevels (bijv. Deino evolueert op 32, Zweilous op 53).
- **Uitzondering: steden met gras** (Ashfrost, à la Icirrus): mogen afwijken van de 12-unieke-soorten-regel. Alleen tamme, ongevaarlijke soorten die niet schuw zijn voor mensen, op lage levels (jonge Pokémon).


## Pokémon-revisies
- Types, stats, abilities en learnsets van veel soorten zijn aangepast; dat staat per soort in `CHANGELOG.md` ("Pokémon Revisie: ..."). De code in `src/data/pokemon/species_info/` moet overeenkomen met de changelog. Controleer dat bij twijfel (Swellow had Wind Rider in de changelog maar niet in de code).
- Level-up learnsets staan in `src/data/pokemon/level_up_learnsets/gen_9.h` (actief via `P_LVL_UP_LEARNSETS` = GEN_LATEST). Wijzigingen in `gen_1.h` t/m `gen_8.h` hebben geen effect.
- Een `Ability:` in `src/data/trainers.party` moet in de abilitylijst van die soort staan.
- **Verborgen abilities zijn niet verkrijgbaar** (Jordi; geen Ability Patch, DexNav uit). Een sterke ability die de speler moet kunnen krijgen hoort in slot 1 of 2 (hele evolutielijn meenemen); het verborgen slot is alleen voor trainers. Eerst de revisie in de changelog lezen: slot 1/2 die Jordi bewust koos (Sharpedo Strong Jaw, Hariyama Purifying Salt) niet vervangen.


## Trainer parties (`src/data/trainers.party`)
- **Taakverdeling:** Jordi doet de echte humor (grap-teams, definitieve dialogen); Claude doet het serieuze werk en schrijft humoristische placeholders. Laat Jordi's grappen staan.
- **Elk gevecht moet engaging zijn**, serieus óf als grap. De speler mag niet op de automatische piloot raken zoals in de echte games. Placeholders moeten ook al vermakelijk zijn; na de beta wordt alles echt uniek gemaakt.
- **Levels:** gelijk aan Jordi's eigen trainers op dezelfde route (meestal 5–6 boven vanilla). Binnen een team vlakke levels, de ace eventueel 1–2 hoger.
- **Evoluties:** een Pokémon op een level waarop hij al geëvolueerd had kunnen zijn, is geëvolueerd. Gebruik de evolutielevels van dit project (`src/data/pokemon/species_info/`), die wijken soms af van de officiële games. Uitzondering: een bewuste grap van Jordi.
- **Variatie:** soorten die al vaak voorkomen (bijv. Wingull, Marill, Tentacool, Machop, Meditite, Makuhita) vervangen door soorten die nog weinig of niet voorkomen.
- **Thema:** grounded per trainerklasse, maar het mag out of the box (bijv. een Tuber met een niet-water-Pokémon).
- Teams die Jordi al niet-Emerald Pokémon heeft gegeven, laten staan, tenzij de levels echt te laag zijn.
- **Rematches:** team van de eerste versie behouden; per rematchronde +1 Pokémon (max 6) en evoluties passend bij het level. Level = vanilla-rematchlevel + dezelfde marge als de eerste versie (4–8); gymleiders +12. Door Jordi zelf ontworpen rematches (Calvin, Gabby & Ty, Miguel, Isaiah_2, Amy & Liv_2, Kira & Dan_2–5) blijven staan.


## Moves (`src/data/moves_info.h`)
- Stat-drops op de tegenstander: gebruik losse effecten per stat (`MOVE_EFFECT_DEF_MINUS_1`, `MOVE_EFFECT_SP_DEF_MINUS_1`, ...). Gecombineerde effecten zoals `MOVE_EFFECT_DEF_SPDEF_DOWN` (Close Combat) en `MOVE_EFFECT_ATK_DEF_DOWN` (Superpower) werken altijd op de gebruiker.
- `additionalEffects` worden alleen uitgevoerd bij aanvallende moves (en bij `onChargeTurnOnly` op de laadbeurt van two-turn moves), niet bij statusmoves zoals Flash.
- **Beschrijving van een nieuwe TM/move-item** (`.description` in `src/data/items.h`): het tasvak is smal, dus 3 regels van max. ±17 tekens (zoals U-turn: "Attacks, then / swaps places with / a party Pokémon.").
- Eigen tests staan in `test/battle/grounded/`.

