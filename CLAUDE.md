# Project Grounded – werkafspraken voor Claude

Pokémon Emerald-romhack op basis van pokeemerald-expansion. De eigenaar (Jordi) communiceert in het Nederlands; antwoord en schrijf de changelog in het Nederlands.

## Zuinig met tokens
- **Geen ROM opleveren** (zippen/versturen) tenzij Jordi erom vraagt. `make -j4` om te controleren dat het bouwt mag altijd; filter de uitvoer (`make -j8 2>&1 | grep "rror:"`).
- Emulatortests en screenshots alleen voor wat echt nieuw of riskant is (warps, scripts, nieuwe mechanics); niet voor elke kleine kaartwijziging. Eén render van de hele kaart aan het eind is genoeg; stuur die zonder ze zelf eerst vaak te bekijken.
- Gebruik de bestaande tools (`tools/grounded/maptools/`, o.a. `testrom.py`, `render_map.py`) in plaats van ze opnieuw te schrijven. Lees grote bestanden gericht (grep, offset/limit), niet in zijn geheel.
- Korte statusberichten; geen samenvattingen van wat al in de changelog staat.
- **Stand van zaken** hieronder kort houden: alleen wat een volgende sessie moet weten. Details horen in `CHANGELOG.md`.

## Vaste regels
- **Changelog:** zet elke wijziging onderaan in `CHANGELOG.md`, als een nieuwe `### [v.x.y.z] - ...`-sectie. Dit is Jordi's eigen logboek; het mag "vervuild" zijn (codeblokken, learnsets). Niet opschonen of herstructureren.
- **Debugmenu blijft aan** (`DEBUG_OVERWORLD_MENU` en `DEBUG_BATTLE_MENU` in `include/config/debug.h`).
- **Mail en Magikarp-levels** niet aanpassen.
- **Grap-trainers blijven een grap:** extreem lage levels op sterke Pokémon zijn bewust (bijv. Ivan's Gyarados lv 3, Lyle's Scizor/Yanmega lv 6). Ze moeten schrikken, niet onverslaanbaar zijn.
- **Humor:** dialogen zijn bewust absurd en donker-humoristisch. Niet "netjes maken"; wel tekstregels afbreken zodat ze passen (`\n`, `\l`, `\p`).
- **Intro kort houden:** geen truck-intro, geen tv-scène. Mom houdt haar humoristische standaardtekst; healen, PokéNav-registratie en post-game-dialoog werken wel.
- **Elemental monkeys** (Pansage/Pansear/Panpour-lijnen) zijn bewust weggelaten.
- **National Dex** is vanaf het begin beschikbaar.
- Merk je een nieuw designprincipe op, stel het eerst aan Jordi voor en voeg het pas na bevestiging toe aan dit bestand.

## Speelervaring
- Filosofie à la Shin Megami Tensei / Slay the Spire: gevechten mogen pittig zijn, maar de speler krijgt veel tools en mogelijkheden om ze op te lossen.
- Move-aanpassingen gebeuren per move; er is geen algemene regel (zoals "altijd 100% bijeffect").

## Quality of life
- **De game respecteert de tijd van de speler.** Pokémon is een JRPG vol herhaling; schrap die herhaling zodat speed-up-knoppen niet nodig zijn. Animaties (aanvallen, schermtransities) zijn tof en blijven; wachttijden, overbodige teksten, ja/nee-vragen en minigames gaan eruit.
- Al gedaan: korte intro, geen tutorial, instant heal bij de verpleegster, vissen zonder minigame (Old Rod blijft bewust slecht), tekstsnelheid standaard Fast, B zet de cursor op Run, korter flitsen vóór transities, Itemfinder als ORAS-dowsing, sneller fietsen/surfen, geen vluchtende Safari-/rondzwervende Pokémon, Wailmer Pail toont rijpe bessen, Repel "Use another?", EV/IV in het summary-scherm, kaartnaam-popup niet herhalen, itembeschrijving bij eerste keer oppakken, Fly vanuit de Town Map/PokéNav-kaart na de 6e badge.
- Bewust níet: Exp. Share als Key Item, pc in het menu, type-effectiviteit altijd tonen, zwakke encounters ontlopen (zwakkere routes afzoeken kan een bewuste keuze zijn), uitleg van de laatst-gebruikte-bal-knop, een echte levelcap.
- Gedaan (events): Wally-gevecht in Meteor Falls en tag battle met Wally tegen Maxie + Tabitha op Mt. Chimney, Prof. Birch op het strand van Route 109, gevechtsmuziek kiezen in het optiemenu. Belangrijke gevechten (rivalen, gymleiders, Archie, Maxie, Wally, Birch) krijgen de mugshot-slide (`Mugshot:` in `trainers.party`). Legendary beasts (Raikou/Entei/Suicune) krijgen hun eigen thema (`MUS_C_VS_LEGEND_BEAST`) via `BattleSetup_StartLegendaryBattle`.

## Werkwijzen (herhaalde taken)

### Een route bouwen
Blauwdruk: **Route 135 en 136** (`tools/grounded/maptools/route135.py`, `route136.py`). Bouw elke kaart met een script (vaste seed), nooit met de hand.
- Grootte: gemiddeld of net onder gemiddeld (2400–3200 tiles, bijv. 60×40).
- Hoogteverschillen met `terrace(..., face=...)`; trappen = stenen Hoenn-trap (General 175 links / 207 rechts, 2 breed, per rij in de klifwand), zoals Route 119.
- Randen: vaste Hoenn-randbomen (`hforest`, op sneeuw `htree_*`), ook in `border.bin`. Geen losse overlappende bomen; bomen sluiten aan op bestaande bomen.
- Hoog gras niet direct tegen randbomen; geen halve sprites of onafgemaakte randen (controleer de render op afgekapte daken, kliffen en oevers).
- Watervallen breed in een massieve rotswand (`fall()`).
- Houd events en doorgangen vrij van decor (EVENTS/KEEP-sets) en laat het script de **bereikbaarheid** controleren (deuren, items, trainers, uitgangen).
- Wilde Pokémon: zie "Wilde encounters". Trainers: zie "Trainer parties".
- Verbonden kaarten (connections) moeten dezelfde secondary tileset hebben; anders een warp (zoals Route 136 ↔ Ashfrost).

### Een grot of binnenkaart bouwen
Blauwdruk: **Coldstep Cave** (randen af, geen onafgemaakte sprites) en `Route136_Grotto` (`grotto136.py`). Hergebruik vanilla layouts waar het kan (kopie in een eigen layoutmap, dan aanpassen). Duiken: `setdivewarp` in de map-scripts (zie `Underwater_Route136`).

### Een stad bouwen
- Gebouwen en stadsgrond komen uit de stads-tileset `snow_town` (`python3 tools/grounded/snow_tileset.py --town`; bouwscript `ashfrost.py`). Controleer in de bronsheet waar een gebouw echt begint (sommige daken beginnen halverwege een rij).
- Pokémon Center: `*_PokemonCenter_1F/2F` op de standaard layouts, heal location in `src/data/heal_locations.json`, `setrespawn` in de 1F. Mart en huizen op de vanilla layouts.
- Nieuwe mapsec: `region_map_sections.json`, beide popup-tabellen in `src/map_name_popup.c`, en op de Town Map (zie Stand van zaken).

### Nieuwe NPC's en trainers
- Teams en levels: zie "Trainer parties". Teksten: **meteen een humoristische placeholder** in de stijl van de game (droog, self-aware, soms de vierde wand doorbrekend). Jordi herschrijft wat hij wil via de Dialoogstudio.
- Script-aanpassingen daarna exporteren voor de Dialoogstudio (zie "Dialogen").

### Testen
- `python3 tools/grounded/maptools/testrom.py <scratchmap> "regels script 1" ["regels script 2" ...]` bouwt een test-ROM met tijdelijke debug-scripts (bijv. `warp MAP_X, x, y; waitstate`) en zet `debug.inc` terug. Daarna in Python: `Emu(rom)`, `load(e, intro)`, `debug_script(e, 1)` (`emu.py`). Bouw daarna opnieuw voor een schone ROM.
- Valkuilen: savestates zijn ongeldig na een rebuild; `data/scripts/debug.inc` nooit committen; grote JSON-bestanden (`wild_encounters.json`, `layouts.json`, `map_groups.json`) tekstueel bewerken, niet via `json.dump`; trainer-AI in `trainers.party` met bestaande namen (bijv. `Check Bad Move / Try To Faint`); nieuwe kaarten achteraan hun groep in `map_groups.json`.

### Afronden van een stuk werk
`make -j4` slaagt → changelogsectie → **Stand van zaken** bijwerken (kort) → commit en push. Bij een kaart: één render van de hele kaart naar Jordi (plus emulatorbeelden als er iets te zien valt). Geen ROM tenzij gevraagd.

## Wilde encounters (`src/data/wild_encounters.json`)
- Land heeft precies **12 slots** met kansen 20/20/10/10/10/10/5/5/4/4/1/1. Meer of minder entries = bug (extra entries komen nooit voor).
- **Design-filosofie:** elke tabel heeft **12 unieke soorten**, geen soort in twee slots. De 1%-slots zijn dus echte zeldzaamheden.
- In oudere tabellen die nog dubbele soorten hebben: vervang bij voorkeur zo'n dubbel slot, zodat er geen soort verdwijnt.
- Elke entry heeft `min_level` én `max_level` (ontbrekende `max_level` gaf eerder lv 100-encounters).
- Schuif je slots door, behoud dan de zeldzaamheidsvolgorde (wie het zeldzaamst was, blijft dat).
- Houd rekening met evolutielevels (bijv. Deino evolueert op 32, Zweilous op 53).

## Pokémon-revisies
- Types, stats, abilities en learnsets van veel soorten zijn aangepast; dat staat per soort in `CHANGELOG.md` ("Pokémon Revisie: ..."). De code in `src/data/pokemon/species_info/` moet overeenkomen met de changelog. Controleer dat bij twijfel (Swellow had Wind Rider in de changelog maar niet in de code).
- Level-up learnsets staan in `src/data/pokemon/level_up_learnsets/gen_9.h` (actief via `P_LVL_UP_LEARNSETS` = GEN_LATEST). Wijzigingen in `gen_1.h` t/m `gen_8.h` hebben geen effect.
- Een `Ability:` in `src/data/trainers.party` moet in de abilitylijst van die soort staan.

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
- Eigen tests staan in `test/battle/grounded/`.

## Bouwen en testen
- Bouwen: `make -j4` (moet zonder fouten slagen vóór elke push).
- `make check` (CI-job `build`) faalt ook op `master`, met honderd-en-zoveel tests die de bewust gewijzigde mechanics en soorten niet meer verwachten. Nieuwe failures ten opzichte van master zijn wel een probleem; meld de bekende failures niet aan Jordi.
- Werk op een branch en open een PR naar `master`.

## Dialogen (Dialoogstudio)
- Jordi schrijft dialogen in de Dialoogstudio: https://claude.ai/artifact/LP3qyGyvhaj6p5GS32Gjxz (bewerkingen staan in de database van die pagina: collectie `edits`, per tekstlabel `{text, note, status, map}`; wensen per kaart in `verzoeken`).
- "Verwerk de dialogen": lees `edits` met status `klaar` (ArtifactData), schrijf `{label: text}` naar een JSON-bestand en draai `python3 tools/dialogen/import.py <bestand>`. Dat breekt de tekst automatisch af (zelfde regels als het voorbeeld in de editor). Bouw, controleer, commit, zet de verwerkte documenten op status `verwerkt` en voer de notities/wensen uit.
- **Niet vóór de beta:** dialogen in het Trick House (`Route110_TrickHouse*`), de Battle Frontier (`BattleFrontier_*`) en de Battle Tents (`*_BattleTent*`) blijven bewust vanilla tot na de beta. Niet aanpassen, tenzij Jordi erom vraagt. De Dialoogstudio verbergt deze gebieden standaard.
- Na wijzigingen in de scripts: `python3 tools/dialogen/export.py <dialogen.json>` en publiceer dat bestand opnieuw bij de pagina, zodat de editor de actuele game-tekst toont.

## Sessies en overdracht
- **Takenlijst:** `TODO.md` (openstaande taken op volgorde, goedgekeurde QoL, backlog). Afgeronde taken daar weghalen en in de changelog zetten.
- Elke sessie begint vers; dit bestand is het geheugen. Werk **Stand van zaken** bij aan het eind van elk afgerond stuk werk (in dezelfde commit).
- Branch: `claude/hopeful-brahmagupta-hsth8c` (PR 5 naar `master`). Is die PR gemerged, begin dan een nieuwe branch vanaf `master`.
- Commit en push na elk afgerond stuk, met een changelogsectie.
- Tilesets: sneeuw (`snow`, routes; nieuwe metatiles **alleen achteraan**, daarna `make data/tilesets/secondary/snow/tiles.4bpp`; ~445/512 tiles), `snow_town` (Ashfrost; eigen nummering, 481/512 tiles), Cave (kristallen 0x3A5–0x3A7, `-num_tiles 441` in `graphics_file_rules.mk`).

## Stand van zaken
- **Af:** Coldstep Cave, Keccles 1–3, Seltzer Surge (TM51), muziekcredits, Route 135, Route 136 met Crystal Cavity (kristalgrot, duikstuk, Suicune lv 50 met beasts-thema), weer sneeuw/as (`WEATHER_ASHFROST_CYCLE`), Town Map met Route 135/136 en Ashfrost.
- Nog van Jordi: definitieve teksten van Route 135/136 en Ashfrost (nu placeholders).
- **Ashfrost Town – herontwerp bezig** (feedback Jordi): in een kloof zoals Sootopolis, meer een paar lagen dieper, Pokémon Center centraal, Mart minder centraal, meer schwung/design. Het roze huis is in `snow_town` gerepareerd (4×4, dak vanaf rij 103) en de groene winkel is eruit; daardoor zijn de metatile-nummers van `snow_town` verschoven en is **`data/layouts/AshfrostTown/map.bin` nog niet opnieuw gebouwd** (de stad ziet er in de game nu kapot uit). Het nieuwe bouwscript `ashfrost.py` (44×34: rotswand rondom, dorpsring, twee lagen omlaag naar het meer) staat klaar maar faalt nog op de plaatsing van het Pokémon Center (deur valt op de trap/klif). Na het bouwen: layout 40×30 → 44×34 in `layouts.json`, objecten, warps en de coord-triggers in `AshfrostTown/map.json` (onderrand y 33) en de warp-bestemming in `Route136_EventScript_ToAshfrost` aanpassen.
