# Project Grounded – werkafspraken voor Claude

Pokémon Emerald-romhack op basis van pokeemerald-expansion. De eigenaar (Jordi) communiceert in het Nederlands; antwoord en schrijf de changelog in het Nederlands.

## Zuinig met tokens
- **Geen ROM opleveren** (zippen/versturen) tenzij Jordi erom vraagt. `make -j4` om te controleren dat het bouwt mag altijd; filter de uitvoer (`make -j8 2>&1 | grep "rror:"`).
- Emulatortests en screenshots alleen voor wat echt nieuw of riskant is (warps, scripts, nieuwe mechanics); niet voor elke kleine kaartwijziging. Eén render van de hele kaart aan het eind is genoeg; stuur die zonder ze zelf eerst vaak te bekijken.
- Gebruik de bestaande tools (`tools/grounded/maptools/`, o.a. `testrom.py`, `render_map.py`) in plaats van ze opnieuw te schrijven. Lees grote bestanden gericht (grep, offset/limit), niet in zijn geheel.
- Korte statusberichten; geen samenvattingen van wat al in de changelog staat.
- **Stand van zaken** hieronder kort houden: alleen wat een volgende sessie moet weten. Details horen in `CHANGELOG.md`.

## Vaste regels
- **Changelog:** zet elke wijziging onderaan in `CHANGELOG.md`, als een nieuwe `### [v.x.y.z] - ...`-sectie. Versies: 0.8.x tot de laatste fase vóór de beta; 0.9 = die laatste fase; 1.0 = de beta. Dit is Jordi's eigen logboek; het mag "vervuild" zijn (codeblokken, learnsets). Niet opschonen of herstructureren.
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
- Al gedaan: korte intro, geen tutorial, instant heal bij de verpleegster, vissen zonder minigame (Old Rod blijft bewust slecht), tekstsnelheid standaard Fast, B zet de cursor op Run, korter flitsen vóór transities, Itemfinder als ORAS-dowsing, sneller fietsen/surfen, geen vluchtende Safari-/rondzwervende Pokémon, Wailmer Pail toont rijpe bessen, Repel "Use another?", EV/IV in het summary-scherm, kaartnaam-popup niet herhalen, itembeschrijving bij eerste keer oppakken, Fly vanuit de Town Map/PokéNav-kaart na de 6e badge, geen bijnaamvraag na het vangen, bessen planten in één handeling (direct de tas, meteen water), Move Deleter bij de Move Relearner, gevechtsmenu onthoudt de laatste move per teamlid, gymgidsen noemen het ace-level (ook van de volgende gym), SELECT in het partymenu healt het team met items uit de tas, Six-Pack (60 HP voor het hele team), tweede registratieknop L (bijv. fiets op L, hengel op SELECT), nature en ability in de pc, L in wilde gevechten toont ability/item/moves van al gevangen soorten.
- Bewust níet: Exp. Share als Key Item, pc in het menu, type-effectiviteit altijd tonen, zwakke encounters ontlopen (zwakkere routes afzoeken kan een bewuste keuze zijn), uitleg van de laatst-gebruikte-bal-knop, een echte levelcap.
- Gedaan (events): Wally-gevecht in Meteor Falls en tag battle met Wally tegen Maxie + Tabitha op Mt. Chimney, Prof. Birch op het strand van Route 109, gevechtsmuziek kiezen in het optiemenu. Belangrijke gevechten (rivalen, gymleiders, Archie, Maxie, Wally, Birch) krijgen de mugshot-slide (`Mugshot:` in `trainers.party`). Legendary beasts (Raikou/Entei/Suicune) krijgen hun eigen thema (`MUS_C_VS_LEGEND_BEAST`) via `BattleSetup_StartLegendaryBattle`.

## Zelflerend werken
- Leer van elke sessie en word steeds beter in het meebouwen aan deze rom. Voeg **zelf, zonder het te vragen**, aan het eind van een stuk werk nieuwe lessen toe onder "Lessen" hieronder: fouten die je maakte, feedback van Jordi, valkuilen in de code/tools en testtrucs die werkten. Kort, één regel per les; verouderde lessen bijwerken of schrappen.
- Alleen **designprincipes** (smaak, spelregels, humor) eerst aan Jordi voorleggen (zie Vaste regels). Technische en werkwijze-lessen mag je direct opschrijven.

## Lessen
- **Bronsheets (Essentials/RMXP):** objecten beginnen vaak een (halve) rij hoger of een kolom anders dan je denkt (sneeuwpophoofd, boomtop, luifel, lantaarn). Zoom per object op pixelniveau in (`grid.py`-achtig) vóór het knippen, en controleer de render op afgekapte koppen/daken. Rode X-vakjes zijn markeringen: leeg laten.
- **Tile-limiet:** Essentials-art ontdubbelt slecht (een gebouw ≈ 50–60 tiles). Een eigen primary + secondary geeft 2×512 tiles en 13 paletten (zie Ashfrost). Onderlaag = grond (gedeeld uit de primary), bovenlaag = object.
- **Kliffen:** afgeschuinde hoeken bij kuilen/terrassen geven rommelige losse klifstukjes; gebruik rechte rechthoeken. Trappen midden in een rechte wand (laat het script dat controleren) en laat het pad tot op elke trap doorlopen (controleer de render op gaten). `cliff_front_b` in de sneeuwset heeft een grotopening; voor hoge wanden gestapelde `cliff_b`-rijen.
- **Deuren:** de deur-tile in de kaart moet precies de tile met deurgedrag uit de tileset zijn (groen huis: (2,3), niet (1,3)); anders loop je over de deur zonder warp.
- **Kaartgrootte wijzigen:** ook `layouts.json` (breedte/hoogte), warps, coord-triggers, heal location, inkomende warps (bijv. Route 136) en NPC-posities bijwerken.
- **Decor uit General** kan op sneeuw als je de graskleuren (palet 1/2, index 12–14) transparant maakt (`_general_metatile(..., nograss=True)`).
- **Immersie telt voor Jordi:** alleen dingen die in de wereld kloppen (geen Reshiram-beeld als Reshiram niet in de game zit; dieren die echt in koud zoet water leven; bloemen alleen waar het plausibel is). Bij twijfel kort uitleggen of voorleggen.
- **Animaties in gevechten:** argumenten van `createvisualtask` worden niet gewist; voeg je een argument toe aan een taak, zet het dan expliciet in álle aanroepen. Weer aan het eind van de beurt (`gBattleAnimGeneral_*`) los van de move-animatie inkorten.
- **Gevechtsanimaties versnellen:** algemeen via `sFastBattleAnim` in `src/battle_anim.c` (halveert `delay` voor status/algemene animaties); per animatie alleen nog als iets na het halveren te lang blijft.
- **Emulatortests:** de intro-savestate heeft een kapotte party (Lv0); doe `givemon` vóór een testgevecht. Zonder `setflag FLAG_SYS_POKEMON_GET` ontbreekt POKéMON in het startmenu. B in een wild gevecht zet de cursor op Run (wacht op berichten i.p.v. B te drukken). Tas: pockets wisselen met RIGHT (hold 8, ~60 frames), Key Items = 4× RIGHT. HP/status testen: direct in `gPlayerParty` schrijven (100 bytes per Pokémon; status +80, hp +86).
- **Meldingen in menu's** (partymenu, tas): de tekst moet eindigen op `{PAUSE_UNTIL_PRESS}`, anders verdwijnt hij meteen. In het partymenu eerst `PartyMenuRemoveWindow(&sPartyMenuInternal->windowId[1])`.
- **Gevechts-UI:** informatie in één omkaderd vak tonen (bijv. het level-up-vak `B_WIN_LEVEL_UP_BOX` via `HandleBattleWindow(18, 7, 29, 19, WINDOW_BG1)`), niet verspreid over de vakken van het actiemenu (Jordi: cognitief onduidelijk, tekst viel weg). Altijd ingezoomd controleren op afgekapte tekst. Fly testen: START → A (debug) → A (Utilities) → A (Fly to map). Fly-flags worden pas gezet bij het binnenlopen van de kaart.

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
- **Uitzondering: steden met gras** (Ashfrost, à la Icirrus): mogen afwijken van de 12-unieke-soorten-regel. Alleen tamme, ongevaarlijke soorten die niet schuw zijn voor mensen, op lage levels (jonge Pokémon).

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
- De Dialoogstudio **niet** automatisch bijwerken na scriptwijzigingen (bespaart tokens). Alleen op verzoek van Jordi: `python3 tools/dialogen/export.py <dialogen.json>` en dat bestand opnieuw publiceren bij de pagina.

## Sessies en overdracht
- **Takenlijst:** `TODO.md` (openstaande taken op volgorde, goedgekeurde QoL, backlog). Afgeronde taken daar weghalen en in de changelog zetten.
- Elke sessie begint vers; dit bestand is het geheugen. Werk **Stand van zaken** bij aan het eind van elk afgerond stuk werk (in dezelfde commit).
- Branch: `claude/epic-lamport-voso15` (nog geen PR naar `master`). Is die gemerged, begin dan een nieuwe branch vanaf `master`.
- Commit en push na elk afgerond stuk, met een changelogsectie.
- Tilesets: sneeuw (`snow`, routes; nieuwe metatiles **alleen achteraan**, daarna `make data/tilesets/secondary/snow/tiles.4bpp`; ~445/512 tiles), `snow_town_base` (primary) + `snow_town` (secondary) voor Ashfrost: eigen nummering, 362 + 465 van 2×512 tiles; opnieuw genereren mag (alleen Ashfrost gebruikt ze), daarna `ashfrost.py` opnieuw draaien, Cave (kristallen 0x3A5–0x3A7, `-num_tiles 441` in `graphics_file_rules.mk`).

## Stand van zaken
- **Af:** QoL-reeks v0.8.18–0.8.27, Lager Lagoon (TM52, Coldstep) en Vintage Spill (TM53, Wallace), Scald (TM03, Route 120), snellere animaties tussen beurten (v0.8.13–0.8.14), Keccles 3-tekst, Fly naar Ashfrost, Coldstep Cave, Keccles 1–3, Seltzer Surge (TM51), muziekcredits, Route 135, Route 136 met Crystal Cavity (kristalgrot, duikstuk, Suicune lv 50 met beasts-thema), weer sneeuw/as (`WEATHER_ASHFROST_CYCLE`), Town Map met Route 135/136 en Ashfrost.
- Nog van Jordi: definitieve teksten van Route 135/136 en Ashfrost (nu placeholders).
- Emulator: `pip install mgba` + `apt-get install libmgba0.10` (verse container).
- **Ashfrost Village** (v0.8.3–0.8.9): af en goedgekeurd door Jordi, incl. tamme encounters in gras en meer. Bouwscript `ashfrost.py` (48×40, vier lagen, Regi-heiligdom op laag 1), eigen primary `snow_town_base` + secondary `snow_town` (beide via `snow_tileset.py --town`; namen in `snow_town/metatile_names.json`).
