# Project Grounded – werkafspraken voor Claude

Pokémon Emerald-romhack op basis van pokeemerald-expansion. De eigenaar (Jordi) communiceert in het Nederlands; antwoord en schrijf de changelog in het Nederlands.

## Zuinig met tokens
- **Geen ROM opleveren** (zippen/versturen) tenzij Jordi erom vraagt. `make -j4` om te controleren dat het bouwt mag altijd; filter de uitvoer met `make -j8 2>&1 | grep -i error` (`grep "rror:"` mist linkerfouten zoals een onbekend geluid of symbool).
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
- **Battle Stadium-pool (Jordi):** elk nieuw iconisch personage (trainer, NPC-gevecht, grap-trainer met een eigen naam; bijv. Colress, Zinnia, Mimi, Keccles) komt ook in de toernooipool van het Battle Stadium, met zijn sterkste team.
- **Elemental monkeys** (Pansage/Pansear/Panpour-lijnen) zijn bewust weggelaten.
- **National Dex** is vanaf het begin beschikbaar.
- Merk je een nieuw designprincipe op, stel het eerst aan Jordi voor en voeg het pas na bevestiging toe aan dit bestand.

## Speelervaring
- Filosofie à la Shin Megami Tensei / Slay the Spire: gevechten mogen pittig zijn, maar de speler krijgt veel tools en mogelijkheden om ze op te lossen.
- Move-aanpassingen gebeuren per move; er is geen algemene regel (zoals "altijd 100% bijeffect").

## Quality of life
- **De game respecteert de tijd van de speler.** Pokémon is een JRPG vol herhaling; schrap die herhaling zodat speed-up-knoppen niet nodig zijn. Animaties (aanvallen, schermtransities) zijn tof en blijven; wachttijden, overbodige teksten, ja/nee-vragen en minigames gaan eruit.
- Al gedaan: korte intro, geen tutorial, instant heal bij de verpleegster, vissen zonder minigame (Old Rod blijft bewust slecht), tekstsnelheid standaard Fast, B zet de cursor op Run, korter flitsen vóór transities, Itemfinder als ORAS-dowsing, sneller fietsen/surfen, geen vluchtende Safari-/rondzwervende Pokémon, Wailmer Pail toont rijpe bessen, Repel "Use another?", EV/IV in het summary-scherm, kaartnaam-popup niet herhalen, itembeschrijving bij eerste keer oppakken, Fly vanuit de Town Map/PokéNav-kaart na de 6e badge, geen bijnaamvraag na het vangen, bessen planten in één handeling (direct de tas, meteen water), Move Deleter bij de Move Relearner, gevechtsmenu onthoudt de laatste move per teamlid, gymgidsen noemen het ace-level (ook van de volgende gym), SELECT in het partymenu healt het team met items uit de tas, Six-Pack (60 HP voor het hele team), tweede registratieknop L (bijv. fiets op L, hengel op SELECT), nature en ability in de pc, L in wilde gevechten opent het summary-scherm van al gevangen soorten, items die je al eens vond: alleen een pop-up met de naam, Rare Candy/vitamines meerdere tegelijk (aantal kiezen in de tas), tas sorteren met START (zat al in expansion), HM-acties met badge + HM in de tas (geen Pokémon nodig die de move kent), direct bij aanspreken zonder animatie (Cut/Rock Smash zonder vraag; Strength, Surf, Waterfall en Dive met ja/nee), donkere grotten automatisch verlicht met melding, Match Call zet rematch-klare trainers bovenaan.
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
- **Spore-partikels** (`create_spore_particle_sprite`) volgen altijd `gBattleAnimTarget`, ook met `ANIM_ATTACKER`; voor beide kanten het doel wisselen (`AnimTask_PollenHazeSetSide`).
- **Animaties in gevechten:** argumenten van `createvisualtask` worden niet gewist; voeg je een argument toe aan een taak, zet het dan expliciet in álle aanroepen. Weer aan het eind van de beurt (`gBattleAnimGeneral_*`) los van de move-animatie inkorten.
- **Gevechtsanimaties versnellen:** algemeen via `sFastBattleAnim` in `src/battle_anim.c` (halveert `delay` voor status/algemene animaties); per animatie alleen nog als iets na het halveren te lang blijft.
- **Emulatortests:** de intro-savestate heeft een kapotte party (Lv0); doe `givemon` vóór een testgevecht. Zonder `setflag FLAG_SYS_POKEMON_GET` ontbreekt POKéMON in het startmenu. B in een wild gevecht zet de cursor op Run (wacht op berichten i.p.v. B te drukken). Tas: pockets wisselen met RIGHT (hold 8, ~60 frames), Key Items = 4× RIGHT. HP/status testen: direct in `gPlayerParty` schrijven (100 bytes per Pokémon; status +80, hp +86).
- **Meldingen in menu's** (partymenu, tas): de tekst moet eindigen op `{PAUSE_UNTIL_PRESS}`, anders verdwijnt hij meteen. In het partymenu eerst `PartyMenuRemoveWindow(&sPartyMenuInternal->windowId[1])`.
- **Save-offsets voor emulatortests:** de `/*0x...*/`-commentaren in `include/global.h` kloppen niet meer (expansion); laat de compiler `offsetof` berekenen (cpp + preproc + cc1, zie Makefile-flags) of lees een symbool uit `pokeemerald.map`. Bijv. `trainerRematches` = SaveBlock1 + 0x92A.
- **Bool-functies in scripts:** `goto_if_eq VAR_RESULT, TRUE` vergelijkt met precies 1; functies als `GetSetItemObtained` geven een ruwe bit terug (bijv. 0x20). Normaliseer met `!= 0` in een special.
- **Summary-scherm vanuit een gevecht:** nooit een pointer naar `gEnemyParty` meegeven (wordt gezien als link-tegenstander → leest `gLinkPlayers` → geheugen kapot, tekst weg, zwart scherm); geef een kopie mee. Een apart scherm openen vanuit het actiemenu: via de engine-route van het debugmenu (`B_ACTION_DEBUG` → `PlayerHandleBattleDebug`), en `DeactivateAllTextPrinters()` vóór het nieuwe scherm.
- **Tekstregels dicht op elkaar** (bijv. pc-infovak): `AddTextPrinterParameterized` tekent een achtergrond per regel en wist zo de onderkant van de regel erboven. Gebruik `AddTextPrinterParameterized3` met `{TEXT_COLOR_TRANSPARENT, …}` na één `FillWindowPixelBuffer`.
- **Gevechts-UI:** informatie in één omkaderd vak tonen (bijv. het level-up-vak `B_WIN_LEVEL_UP_BOX` via `HandleBattleWindow(18, 7, 29, 19, WINDOW_BG1)`), niet verspreid over de vakken van het actiemenu (Jordi: cognitief onduidelijk, tekst viel weg). Altijd ingezoomd controleren op afgekapte tekst. Fly testen: START → A (debug) → A (Utilities) → A (Fly to map). Fly-flags worden pas gezet bij het binnenlopen van de kaart.
- **Wilde gevechten/transities testen:** debug Utilities > "Wild battle (map)" of in `testrom.py` het script `special Debug_StartMapWildBattle; waitstate` na een warp. Een soort forceren in een emulatortest: schrijf `gDebugForcedWildSpecies` (adres uit `pokeemerald.map`) met `e.core.memory.u16[adres] = soort`. Transitie vanaf frame 0 vastleggen: de laatste A van het debugscript met `after=0`.
- **Mugshot + eigen transitie aan elkaar plakken** (Colress): draai `sMugshot_Funcs` tot de witte fade (state 7), zet dan VBlank/HBlank/DMA/BLDCNT/vensters terug, maak de mugshot-trainerfoto's onzichtbaar (anders liggen ze als silhouet over je sprites) en blijf in dezelfde taakfunctie (`IsBattleTransitionDone` zoekt op de taakfunctie). In `emu.py` heten de knoppen `DOWN`/`UP` (hoofdletters).
- **Coord-triggers** (`coord_events`) vergrendelen de besturing: ook een script dat alleen een geluid speelt moet eindigen met `releaseall`, anders sta je vast.
- **Spelerpositie in emulatortests:** lees `gSaveBlock1Ptr` uit `pokeemerald.map` en dan `pos` (s16 x, y op offset 0); loop met een goto(x,y)-lus in plaats van een vaste toetsenreeks (scripts slikken soms een stap in).
- **Emulator-screenshots hebben een dag/nacht-tint** (`OW_ENABLE_DNS`, echte klok): roze/oranje of blauw is de tijd van de dag, geen paletbug.
- **Gehoorzaamheid in emulatortests:** de intro-savestate heeft geen badges, dus een `givemon` boven lv 10 is ongehoorzaam (doet een andere move, gaat slapen). Altijd testen met lv ≤ 10 óf eerst alle badges zetten (`setflag FLAG_BADGE01_GET` … `FLAG_BADGE08_GET`).
- **Wilde gevechten via debugscript** starten pas na de eerste knopdruk: na `debug_script` eerst A, dan ~400 frames wachten tot het actiemenu er is.
- **ROM opleveren:** 32 MB is te groot voor SendUserFile; zip hem (≈16 MB). Bouw eerst opnieuw na `testrom.py`.
- **Dubbel tegen twee trainers vanuit een script:** `trainerbattle_two_trainers A, verliestekstA, B, verliestekstB`; het script loopt daarna gewoon door. Zelf vooraf `goto_if_defeated` en `specialvar VAR_RESULT, GetMonsStateToDoubles` (special toegevoegd) controleren.
- **Multi battles hangen bij te veel sprites:** vier ballen tegelijk + partikels kunnen alle 64 sprites opmaken (`gBattlerSpriteIds` = 64, controller blijft in `Intro_TryShinyAnimShowHealthbox`). Debuggen: `arm-none-eabi-nm -n pokeemerald.elf` geeft ook statische symbolen; lees `gBattlerControllerFuncs` en tel `gSprites[i].inUse`. Sinds v0.8.66 houden bal-partikels 8 sprites vrij.
- **Sootopolis:** het eiland voor de gym is x 27–34, y 32–36; daaromheen is water (collision 0 zegt niets over water, kijk naar het metatile-gedrag 0x10).
- **Pokémon-sprites aanpassen:** zoek per frame eerst het echte hoofd (ogen/mond; bij Muk's backsprite is de bult rechtsboven de hand). Meet hoofdbreedte niet automatisch als een arm eraan vastzit. Toevoegingen moeten in het silhouet opgaan: dezelfde breedte als het hoofd, geen omlijning tegen het lijf, en alleen de kleurindices die het lijf al gebruikt. Jordi wil het ingezoomd zien vóór het in de game gaat.
- **Nieuwe vorm (zoals Alolan):** constante achter `SPECIES_FALINKS_MEGA` + `SPECIES_EGG` ophogen, graphics-blok in `src/data/graphics/pokemon.h`, `sPicTable_*` in `object_event_pic_tables_followers.h`, overworld-regel in `spritesheet_rules.mk`, `formSpeciesIdTable`, level-up learnset in `gen_9.h`; in `trainers.party` heet hij `Grimer_Hoenn`.
- **Onderwater-ingang:** een zwemgat (metatiles 0x265–0x267 / 0x26D–0x26F, `MB_WATER_DOOR`) met een gewone warp naar een bovenwaterkaart werkt; je komt surfend uit als het doel water is. Duidelijker dan een onzichtbaar bovenkomplekje. `render_map.py` wil `<kaart> <uit.png> <y0> <y1>`.
- **Nieuwe kaart:** ook de `scripts.inc` in `data/event_scripts.s` opnemen, anders linkerfout op `*_MapScripts`.
- **Gevechten in emulatortests aansturen:** wacht niet op vaste frames maar lees `gBattlerControllerFuncs[0/2]` (adres via `arm-none-eabi-nm pokeemerald.elf`) tot het `HandleInputChooseAction` van de speler is. Spread-moves (Muddy Water) vragen een extra A (`HandleInputShowTargets`). `gBattleOutcome` 1 = gewonnen.
- **AI-keuze vóór de speler:** `ComputeBattlerDecisions` draait bij `STATE_TURN_START_RECORD` voor alle battlers, dus `gAiBattleData->chosenMoveIndex/chosenTarget` en `gAiLogicData->simulatedDmg` zijn al gevuld als het actiemenu verschijnt (zo werken de Spire-intenties). `moveDamage` is `s16`.
- **Nieuwe gevechtsactie:** constante (vrij nummer na 21), tabel `sTurnActionsFuncsTable`, beide `case`s in `HandleTurnActionSelectionState` (WAIT_ACTION_CHOSEN en CASE_CHOSEN) en de drie lijsten in `SetActionsAndBattlersTurnOrder` (dan gaat hij vóór moves, zoals items/wissels).
- **Eigen scherm bouwen** (zoals `spire_reward.c`): sjabloon `src/dexnav.c`; type-icoontjes = `gSpriteSheet_MoveTypes` + `gMoveTypes_Pal` op OBJ-palet 13–15 + `gTypesInfo[type].palette`; Pokémon-icoontjes = `LoadMonIconPalettes` + `CreateMonIcon`. `COMPOUND_STRING` in een `switch`-toewijzing geeft een dangling-pointer-fout: gebruik `static const u8[]`. Sprites liggen over de tekst: geen cursor-hand bij tekstregels, gebruik daar het rode ▶.
- **Kaders tekenen zonder de inhoud te wissen:** `DrawStdFrameWithCustomTileAndPalette` vult het venster ook opnieuw; voor een rand die van kleur wisselt (selectie) alleen de tilemap zetten (`DrawFrameOnly` in `spire_cards.c`).
- **Nieuwe save-data:** `SaveBlock2` had ±1100 bytes vrij (v0.8.103); `struct Pokemon` is in `global.h` pas na SaveBlock2 bekend, dus reserveer een `u32`-blok en cast (zie `SPIRE_SAVE`). Grootte checken: `arm-none-eabi-nm -S pokeemerald.elf | grep gSaveblock`.
- **Emulatortests van menu-flows:** lees `gMain.callback2` (gMain+4) om te zien welk scherm actief is en lees de schermstatus uit een statische struct (`sCards` in `pokeemerald.elf`); reageer daarop i.p.v. vaste toetsreeksen.
- **Spire-rekenscripts:** `tools/grounded/spire/spire_pool.py` en `encounters.py` genereren `src/data/spire_pool.h`, `spire_encounters.h` en `SPIRE_BALANS.md`; na een wijziging in soorten/moves of ontmoetingen opnieuw draaien. Leerbaarheid controleren met `tools/learnset_helpers/build/all_learnables.json` (alle games), niet alleen de TM's van deze rom. `SPECIES_X`-aliassen (Shellos, Wishiwashi, Minior) staan als `#define` in `species.h`.
- **Vormen die uit staan** (`include/config/species_enabled.h`: Mega, Gmax, Ultra Burst, Tera, Primal) verschijnen als "??????????" met een ?-sprite. Mega/Gmax/Ultra/Tera staan sinds v0.8.104 aan (Spire-bazen).
- **Eigen schermen (BG):** tegel 0 van elke BG moet leeg zijn; deel nooit een charblock tussen een tekst-BG en een groot venster van een andere BG (de lege tegel 0 werd routegrafiek: hele scherm vol patroon). Gevechtsachtergronden (`gBattleEnvironmentInfo`) werken goed als decor (kamp), maar niet verdonkerd achter een kaart (gedithered lucht wordt arcering).
- **`CreateMonPicSprite` met een paletteTag:** het palet wordt geladen onder de tag = soort, dus geef `paletteTag = species` mee; met een eigen tag krijgt de sprite een verkeerd palet. Item-iconen (`AddItemIconSprite`) met een vaste tag per plek: bij het wisselen altijd `FreeSpriteTilesByTag`/`FreeSpritePaletteByTag`, anders erft de volgende kaart het oude icoon.
- **`COMPOUND_STRING` teruggeven uit een functie** geeft `-Werror=return-local-addr`; gebruik `static const u8 x[] = _("...")`. Tekens als ▲▼ staan niet in de charmap: `{UP_ARROW}`/`{DOWN_ARROW}`.
- **Spire testen:** `special Spire_DebugOpen` met `VAR_0x8004` (0 kamp, 1 winkel, 2 event, 3 kaart, 4 elite, 5 baas, 6 relic-beloning met VAR_0x8005 0 elite / 1 baas) in een `testrom.py`-script; zonder run maakt hij er een.
- **Nieuwe graphics:** een overworld-sprite heeft een eigen regel in `spritesheet_rules.mk` nodig (`-mwidth 2 -mheight 4` voor 16×32), anders staan de tegels door elkaar. Make bouwt een `.c` niet opnieuw als alleen een INCBIN-bestand verandert: `touch` het `.c`-bestand (bijv. `src/event_object_movement.c`). FRLG-graphics komen uit `pret/pokefirered` (raw.githubusercontent.com); trainerfoto's heten daar `*_front_pic.png`, NPC-overworlds hebben 3 frames (dupliceer naar 9) en een eigen palet past vaak beter dan NPC_1–4 (eigen `OBJ_EVENT_PAL_TAG_*` + `PALSLOT_NPC_SPECIAL`, zie Brock).

- **Battle Stadium-gevechten:** `gStadiumBattle` schakelt geld/white-out (battle_scripts_1.s via `jumpifbyte`), EXP en het singles/doubles-type van de trainer uit; het team van een tegenstander komt uit `Stadium_BuildTrainerParty` (masker uit pool.py). Party-bestanden gaan door de C-preprocessor: markeringen als `/* */`, nooit `#`.
- **Tekst in C-strings:** de charmap kent geen `"`; gebruik “ ”. Kleuren in een string: `{COLOR GREEN}{SHADOW LIGHT_GREEN}` = paletindex 6/7 (namen in charmap.txt), dus leg een eigen tekstpalet op die indexen (zie `spire_event.c`).
- **Spire-events:** alleen `tools/grounded/spire/events.py` bewerken en opnieuw draaien; het script controleert breedtes. Contactvel van alle events: `gSpecialVar_0x8005` in het geheugen zetten vóór `debug_script` (script: `setvar VAR_0x8004, 2; special Spire_DebugOpen`).
- **Subagents in worktrees:** laat ze eerst `git reset --hard <werkbranch>` doen (worktrees starten soms op een oude commit) en CHANGELOG/CLAUDE.md níet aanraken; zelf samenvoegen, gegenereerde bestanden (stadium_pool.h, battle_partners-blok) na een conflict opnieuw genereren i.p.v. met de hand mergen.
- **Healthboxes:** bij het eerste tekenen is `gBattleMons` nog leeg; lees HP uit de `struct Pokemon` die `UpdateHealthboxAttribute` meekrijgt.
- **Pixel-art 1,5x vergroten** (bron te breed voor 2x in 64×64): Scale3x en dan halveren (`scale3x` in `guest_trainer_pics.py`); losse rijen/kolommen 1x of 2x geeft scheve lijnen.
- **Trainers in `trainers.party` achteraan toevoegen** (laatste blok heeft geen `===` erna) en objecten achteraan `object_events` in map.json (vooraan verschuiven de nummers van NPC's zonder local_id).
- **Kleine trainerfoto's** (bracket): niet verkleinen (`SetOamMatrix` geeft lelijke pixels) maar een 32×32-uitsnede van het hoofd uit de gedecomprimeerde foto (`AddPortrait` in `stadium_screens.c`). DS-sprites hoger dan 64 px: onderkant geditherd laten wegvallen (`fade_bottom`).
- **Overworld-GFX-ID's boven 255** (Kanto-sprites 248–259+): het Stadium en scripts kunnen het aan, maar `src/vs_seeker.c` gebruikt nog `u8 graphicsId`; zulke sprites niet als gewone rematch-trainer op een kaart zetten.
- **Fades en wachttijden:** paletfades wisselen BG en sprites af (`objPaletteToggle`), dus elke stap kost 2 frames + 4 frames afronden; een warp wacht ook op het uitfaden van de oude muziek (`GetMapMusicFadeoutSpeed`). Eigen transities: eindbeeld max ±2 frames vasthouden, fade ±8 frames (v0.8.119).
- **Warp-elevation** moet gelijk zijn aan die van de tegel (0 = elke); vanilla-grotplateaus zijn soms elevation 4 (Altering Cave).
- **Kaart op zijn kop** (omgekeerde Sky Pillar, `reverse_pillar.py`): rijen per metatile wisselen + v-flip (bit 11) per tile, `map.bin`-rijen omdraaien, en het gedrag aanpassen (trapdeur 0x60 → zuidpijl, zuidpijl → noordpijl).
- **Transities die elke frame de BG0-tilemap opnieuw tekenen:** elk vak in één keer de eindwaarde geven, niet eerst wissen (tearing).
- **Agent-branches samenvoegen:** conflicten achteraan enums/tabellen/map_groups zijn "beide houden"; let op een `}` of komma die op de grens wegvalt. Vlecht git twee nieuwe functieblokken door elkaar (battle_transition.c), bouw het bestand dan op uit onze versie + hun blok.
- **Subagents en de scratchpad:** die wordt gedeeld; laat elke agent een eigen submap gebruiken (een `test.gba` van een ander proces gaf een Bus error).
- **Object toevoegen aan een kaart met `"object_events": []`:** tekstueel vóór `"warp_events"` invoegen belandt in `connections`; controleer met `json.load`.
- **Zwarte leegte op een kaart:** metatile 0 is niet zwart (layer NORMAL tekent grasbasis op BG3); gebruik Facility-metatile 0x201. Kleine kaarten tonen de border: rondom aanvullen. `build/emerald/data/maps.o` volgt `map.bin`/`border.bin` niet: na een wijziging verwijderen.
- **Winkelhouders/cameo's:** Kecleon is van Keccles (eigen rol); niet als winkelier of losse NPC gebruiken.

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
- **Testgevechten:** altijd met een **Arceus lv 100** met Dark Pulse, Psychic, Thunderbolt en Ice Beam (`givemon SPECIES_ARCEUS, 100, move1=MOVE_DARK_PULSE, move2=MOVE_PSYCHIC, move3=MOVE_THUNDERBOLT, move4=MOVE_ICE_BEAM`), tenzij een gevecht een ander soort Pokémon vereist. Zet in het testscript ook **alle badges** aan (`setflag FLAG_BADGE01_GET` t/m `FLAG_BADGE08_GET`), anders luistert Arceus niet.
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
- Branch: `claude/amazing-wozniak-2iz078` (voortzetting van `claude/dreamy-brown-o55b7w`, PR 7; PR 6 gemerged; nieuwe PR naar `master` per ronde). Is die gemerged, begin dan een nieuwe branch vanaf `master`.
- Commit en push na elk afgerond stuk, met een changelogsectie.
- Tilesets: sneeuw (`snow`, routes; nieuwe metatiles **alleen achteraan**, daarna `make data/tilesets/secondary/snow/tiles.4bpp`; ~445/512 tiles), `snow_town_base` (primary) + `snow_town` (secondary) voor Ashfrost: eigen nummering, 362 + 465 van 2×512 tiles; opnieuw genereren mag (alleen Ashfrost gebruikt ze), daarna `ashfrost.py` opnieuw draaien, Cave (kristallen 0x3A5–0x3A7, `-num_tiles 441` in `graphics_file_rules.mk`).

## Stand van zaken
- **v0.8.113–0.8.114:** ochtendfeedback Stadium verwerkt (bracketportretten, Gen 4-fade, compagnons via puntendrempels, korte arena, Wario flexend, Lyle i.p.v. Thomas, Ditto op Route 115). v0.8.115: Kanto-overworlds, Aurora Ticket weg. v0.8.116: Pokémon-revisie (buffs, verborgen abilities naar slot 2). Vragen 1–21 van `VRAGEN_OCHTEND.md` beantwoord (antwoorden bovenaan dat bestand); 22–26 nog doorlopen. Spire v0.8.118: 50 relics (`relics.py`), %-moves zeldzaam; balans na testruns (zie changelog).
- **Nacht 4-5 okt (v0.8.107–0.8.112):** Battle Stadium speelbaar en getest (lobby op OutsideEast, arena-opkomst, singles 32 / doubles 16 duo's, level 50, bracket op papier, 94 deelnemers incl. gasten/Ditto/meme-trainers, 111 compagnons incl. 17 collecties; `tools/grounded/stadium/pool.py`, `STADIUM_DESIGN.md`), Deoxys-ruimte-event (`meteor_space.py`), QA-ronde (`QA_RAPPORT.md`), Pokémon-balansrapport (`POKEMON_BALANS.md`), Spire-balans tegen Slay (`runsim.py`). **Eerst `VRAGEN_OCHTEND.md` met Jordi doorlopen.**
- **The Spire v0.8.106:** draft 10→2, Mart-winkel (Banette), HP% i.p.v. level, slanke toren, 55 datagedreven events (`events.py` → `spire_event.c`). Volgende: Jordi speelt; open: codex, golven, baas-intro, receptioniste, echte teksten.
- **The Spire v0.8.104:** branch `claude/amazing-wozniak-2iz078` (nog geen PR naar `master`). Toren in de Battle Frontier (West, noordkant) + lobby, rentals/startkits/bans/biomes/ontmoetingen/bazen uit de rekenscripts (`SPIRE_BALANS.md`), Snorlax-kamp, winkel met schappen en Move Relearner, 16 events. Alles lv 100. Volgende: Jordi speelt en geeft feedback; open: codex, golven, baas-intro, ja/nee bij de receptioniste, echte teksten. Kernprincipes staan bovenaan `SPIRE_DESIGN.md`.
- **v0.8.94–0.8.96:** graphics in `graphics/grounded/`; Colress, Zinnia, Zangoose/Seviper-transities, debug "Force encounter…"/"off" en "Wild battle (map)"; Regi-stippenpuzzel in alle Regi-grotten (`src/regi_dots.c`, `regi_caves.py`), Regieleki (luik in de Cycling Road-pijler, Route 110), Regidrago (eiland Route 130), Regigigas-tempel onder de iglo van Ashfrost (`regigigas_temple.py`, tileset `snow_temple`). Branch `claude/dreamy-brown-o55b7w`; nog geen PR. v0.8.97: tickets voor 200 BP in de Battle Frontier, Eon Ticket (rood/blauw) via de rivaal in Lilycove. Deoxys-ruimte-event in de backlog. v0.8.98: Heatran-hol (post-game, Fiery Path linksboven, `heatran_lair.py`), Burglar-trainerfoto als voorstel (`burglar_sprite.py`, nog niet in de game). **The Spire** (roguelike-faciliteit): ontwerp in `SPIRE_DESIGN.md`; v0.8.100 = rekenscript (`tools/grounded/spire/balance.py`) + prototypegevecht (debug Utilities > Spire prototype; `src/spire.c`: ×HP, DEFEND als actie `B_ACTION_SPIRE_DEFEND`, blok in `Cmd_adjustdamage`, intenties uit `gAiBattleData->chosenMoveIndex`, met KO/KO?). v0.8.101: losse Pokémon (wild dubbelgevecht, `IsWildMonSmart` = TRUE in de Spire). v0.8.103: **beta** speelbaar (debug Utilities > The Spire): `spire_run.c` (run in `SaveBlock2.spireData`, kaartgeneratie, kamers, relics, acts), `spire_map.c` (act-kaart), `spire_cards.c` (alle kaartenschermen). Open: ingang in de wereld (vraag Jordi), balans na testen. Burglar en Safari-biomen: Jordi denkt nog na.
- **Volgende sessie:** `BACKLOG_PLAN.md` heeft per backlog-onderdeel een voorstel en genummerde vragen voor Jordi; eerst zijn antwoorden verwerken, dan bouwen. Er is nog geen PR naar `master` voor v0.8.79–0.8.92.
- **Transities v0.8.82–0.8.88:** route-transities per gebied en unieke transities per soort/trainer/plek, allemaal via `GetGroundedRouteTransition` + de soort-switch in `GetWildBattleTransition` (`src/battle_setup.c`) en `RouteTransition_Run` (`src/battle_transition.c`). Graphics: `tools/grounded/route_transitions.py`; testen: `tools/grounded/maptools/transtest.py`. Nieuwe transitie = tiles in het script, een `RouteTransition`-struct met update() en een regel in de keuzefunctie.
- **Raikou/Entei v0.8.80:** Raikou in het kapotte datacenter onder New Mauville (schakelaar in de oostkamer), Entei achter een verborgen ingang op Mt. Chimney (vanaf badge 5). Eigen transities `B_TRANSITION_RAIKOU`/`B_TRANSITION_ENTEI`; nieuwe transities kosten maar een paar KB (ROM ±23 van 32 MB).
- **Birch v0.8.79–0.8.81:** vast strontteam (Rabsca, Clodsire, Palossand, Mudsdale, ace Hoenn-Muk) + per gevecht één Pokémon in het thema. Mossdeep (meteoriet = Birth Island-steen, Macarena-lore) en Underwater Route 124. Alle Birch-trainers staan in `battle_setup.c` (transitie) en `pokemon.c` (muziek); een nieuwe Birch daar ook toevoegen.
- **Hoenn-Grimer/Muk v0.8.67:** nieuwe vormen (Poison/Ground), Birch in Verdanturf (`TRAINER_BIRCH_VERDANTURF`, ace Hoenn-Grimer), Birch 2 doorontwikkeld met Hisui-Avalugg en Hoenn-Muk. De speler krijgt alleen één Hoenn-Grimer van Birch (Verdanturf); verder nergens te vangen.
- **Transities/Sootopolis v0.8.62–0.8.66:** Regidrago/Regieleki/Deoxys/Birch-transities (Birch alleen prut, geen drol), Keccles-scène na Rayquaza met multi battle (Archie + Maxie, weerneutraal), Mt. Pyre-berouwscène overgeslagen.
- **Events v0.8.58–0.8.61:** Mimi (Mimikyu-trainer, Route 119), Heatran-cutscene (Route 111), Rotom in de kelder van `MauvilleCity_House2_B1F`, eerste Gabby & Ty-gevecht dubbel met Brad (`TRAINER_LOCAL_CELEBRITY`). ROM v0.8.61 opgeleverd. Volgende ronde staat in `TODO.md` ("Volgende ronde").
- **Moves/weer v0.8.45–0.8.53:** Fungal Control, Transmutation, Implosion (zwart gat), Laser Beam (TM55), Machine Learning (TM54), Shadow Siphon (TM56), Acid Rain (TM57, weer `B_WEATHER_ACID_RAIN`, ability Air Pollution), Pollen Haze (TM58, `B_WEATHER_POLLEN_HAZE`, ability Pollen Season, Bug Maniac Timothy op Route 119). Prof. Oak in Slateport. Suicune-noorderlichttransitie (`B_TRANSITION_AURORA`).
- **Af:** QoL-reeks v0.8.18–0.8.34, Lager Lagoon (TM52, Coldstep) en Vintage Spill (TM53, Wallace), Scald (TM03, Route 120), snellere animaties tussen beurten (v0.8.13–0.8.14), Keccles 3-tekst, Fly naar Ashfrost, Coldstep Cave, Keccles 1–3, Seltzer Surge (TM51), muziekcredits, Route 135, Route 136 met Crystal Cavity (kristalgrot, duikstuk, Suicune lv 50 met beasts-thema), weer: Route 135 sneeuwstorm/as (`WEATHER_ASHFROST_STORM_CYCLE`), Route 136 sneeuw/as (`WEATHER_ASHFROST_CYCLE`; hoe dichter bij Ashfrost, hoe milder); Hail heet Snow Storm (schade + Ice-Def), lichte sneeuw = Snowscape, Town Map met Route 135/136 en Ashfrost.
- Nog van Jordi: definitieve teksten van Route 135/136 en Ashfrost (nu placeholders).
- Emulator: `pip install mgba` + `apt-get install libmgba0.10` (verse container).
- **Ashfrost Village** (v0.8.3–0.8.9): af en goedgekeurd door Jordi, incl. tamme encounters in gras en meer. Bouwscript `ashfrost.py` (48×40, vier lagen, Regi-heiligdom op laag 1), eigen primary `snow_town_base` + secondary `snow_town` (beide via `snow_tileset.py --town`; namen in `snow_town/metatile_names.json`).
