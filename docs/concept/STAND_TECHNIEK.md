# Stand techniek (skelet, TODO-stap 3 en 4)

Bijgewerkt op 22 okt door de techniek-agent, die stopte vanwege de gebruikslimiet.

## Af (commit `a7c68b05ea`, branch `worktree-agent-aaf7ea91cb0733434`, basis `fu/main` d8febc522b)
Stap 3, deel 1: Spacetime, Yoshi's Island en Ultra Space zijn eruit. Het bouwt (`make -j4` zonder fouten).
- Kaartgroepen `gMapGroup_Spacetime` en `gMapGroup_UltraSpace` weg: 66 kaarten, 63 layouts, 65 tilesets (+ tileset-animaties), wilde encounters, heal location Lavender en debug-warps.
- Warps en haken weg op Route 125 (Spacetime-grotopening), Sky Pillar Top (trap van licht naar Hall of Origin) en Altering Cave (Ultra-wormgat).
- Weg: Azure Flute (item 863, script, hints, `src/azure_flute.c`), Gen 1-GHOST (`src/gen1_ghost.c`), `src/ultra_worlds.c`, portaal-specials, National Park-omniboost en het Area Zero-Tera-alarm.
- 71 trainers (Area Zero, Cerulean Cave, Chargestone, Coronet, Glimwood, Hall of Origin, National Park, Pokémon Tower, Yoshi's Island, Shy Guy op Route 111), trainerklassen Zero Lab/Shy Squad/Construct, 18 trainerfoto's (hernummerd), partners Yoshi en Calyrex (hernummerd), 33 overworld-sprites en de battle-transities Wario/Boo/Shy Guy.
- ROM-ruimte: vóór 814 KB vrij (`__rom_end` 0x09F34724), na 1,94 MB vrij (0x09E0EAEC).

## Bewust laten staan
- Keccles (alles) en Cozmo's Cosmog-lijn (evolutieregel in `ultra_space.c`).
- De mapsecs van de verwijderde gebieden (`region_map_sections.json` en de popup-tabellen). Magnezone/Vikavolt evolueren via `MAPSEC_CHARGESTONE_CAVE`; dat moet in de nieuwe regio een nieuwe plek krijgen.
- Flags in `flags.h` (ongebruikt, kosten niets), de trainerfoto's van Giovanni/Agatha, de klassen Boss/Commander/Guest Star. (De legendary-intro's zijn later alsnog weggehaald, zie hieronder.)
- Route 125: de rotstegel van de grotopening blijft staan (alleen de warp en `setmetatile` zijn weg).

## Nog te doen (stap 3)
- **Muziek: afgerond (muziek-agent, 22 okt).** Alle Ungrounded-muziek is weg, behalve Battle! Keccles (nu song 610):
  - weg: songs 610–725 (eigen composities, covers, legendary-/personage-/gymthema's, gym-/trainerklasse-/wild-/nachtremixes, Ashfrost, YI/MKSC/WL4-rips, Boo, Area Zero, Poké Tower), 103 MIDI's, 14 rip-`.s`-bestanden, `sound/songs/grounded_src/`, 143 voicegroup-bestanden, 8 eigen keysplits, 490 samples (`grounded/` behalve `kc_*`, heel `rip/`), `gym2_saw.pcm`, en de generatoren in `tools/grounded/` (`*_theme.py`/`*_samples.py` behalve Keccles en `gm_samples.py`);
  - code: `battle_music_options.c` (alleen vanilla-keuzes + Keccles), `GetBattleBGM` in `pokemon.c` (vanilla-logica + Keccles, Juan/Brock/Oak/Rocket-FRLG-muziek), `battle_setup.c` (legendaries → `MUS_RG_VS_LEGEND`, Mew/Jirachi → `MUS_VS_MEW`, Mewtwo → `MUS_RG_VS_MEWTWO`, beasts → `MUS_C_VS_LEGEND_BEAST`, Rayquaza → `MUS_VS_RAYQUAZA`, Regigigas → `MUS_VS_REGI`), nachtmuziek in `overworld.c` weg;
  - kaarten: Ashfrost → `MUS_FALLARBOR`, Coldstep Cave → `MUS_CAVE_OF_ORIGIN`, Fortree Jungle/Mangrove Mire → `MUS_ROUTE119`, Game Corner → `MUS_GAME_CORNER`, Mirage Tower → `MUS_MT_CHIMNEY` (vanilla).
  - ROM-ruimte: vóór 1,94 MB vrij (`__rom_end` 0x09E0EAEC), na 7,48 MB vrij (0x09885C38), dus 5,53 MB erbij.
  - Blijft: HQ-mixer, 16 BGM-sporen, mixer 21 kHz, de algemene muziektools. `bronnen/muziek/` (bronbestanden, niet in de ROM) is niet aangeraakt.
- ~~Bouwscripts opruimen~~ (gedaan met de intro's, zie hieronder). `graphics/grounded/yoshis_island` blijft (Jordi: assets blijven).
- **Intro's en films: afgerond (intro-agent, 22 okt).**
  - Weg: alle legendary-intro's (per soort, beasts, Rayquaza-film, muurschilderingen, Tapu's, Deoxys, Regidrago/
    Regieleki/Regigigas, Mew, Zygarde, Volcanion, legend_intros*), de per-soort wilde intro's (Pikachu, Magikarp ook
    bij Magikarp-trainers, Psyduck, Koffing, Zangoose, Seviper, Zarude), de gym-/rivaal-/personage-intro's en films
    (Steven, Wally, Colress, SickBlik, Maxie/Archie, mugshot-koppelingen), de route-transities per gebied, hun
    generatorscripts (37 stuks in `tools/grounded/`, o.a. `legend_intros*.py`, `gym_intro_lib.py`, `*_transition.py`)
    en 335 graphics-bestanden in `graphics/battle_transitions/` die alleen daarbij hoorden.
  - Legendaries vallen terug op vanilla: `BattleSetup_StartLegendaryBattle` kent alleen nog Groudon/Kyogre/Rayquaza
    (hun vanilla-transities), Deoxys, Mew/Jirachi, Mewtwo en de beasts (vanilla-muziek); de rest Blur +
    `MUS_RG_VS_LEGEND`. Regi's: vanilla Regirock/Regice/Registeel, overige Grid Squares.
  - Blijft: klasse-intro's (`src/data/class_intros*.h`, hulpjes in `intro_lib.h`), Keccles (film + `film.py`,
    `film_art.py`, `film_delta.py`, `keccles_transition.py`), zee-/onderwatertransitie (`route_transitions.py`), de
    vanilla-transities, en `graphics/grounded/yoshis_island/{boo,shyguy}_intro` (bronsprites).
  - Ook weg: bouwscripts van Spacetime/Yoshi's Island/Ultra Space/Glimwood/Chargestone/Coronet/Hall of Origin/
    meren/National Park in `tools/grounded/maptools/` en `bronnen/muziek/yoshis_island_gsf`. `area_zero.py` importeerde
    `chargestone.py` en werkt niet meer (gaat mee met de Hoenn-opruiming).
  - ROM-ruimte: vóór 7,42 MB vrij (`__rom_end` 0x098946F4), na 9,36 MB vrij (0x096A41C8), dus 1,94 MB erbij.
- **Hoenn-wereld eruit, stap 1–6: afgerond (Hoenn-agent, 22 okt).** Details en wat er over is: `docs/concept/PLAN_HOENN_ERUIT.md`
  (sectie "Stand").
  - Over: één kaartgroep `gMapGroup_FullyUngrounded` met StartTown (Oldale-kopie), Pokémon Center 1F/2F, Mart,
    zeven stock-kaarten (zes interieurs) en de TestMap (Route 102 + huizen, wild, water, Keccles, PC). Nieuw spel
    start in StartTown; respawn bij het Pokémon Center.
  - Weg: alle 648 Hoenn-/Ungrounded-kaarten (ook Frontier, Tents, Trick House, Trainer Hill, Safari, alle oude
    groepen), 542 layoutmappen, 22 heal locations, de wilde tabellen, 1036 trainerteams (Keccles blijft, plus wat
    algemene scripts nog bevechten). Rematchtabel, Match Call-trainers en gymleider-rematches zijn plaatshouders.
    Tilesets en graphics staan er nog.
  - Overgangslaag: `include/constants/map_compat.h` + `data/scripts/map_compat_stubs.inc` (`map_compat.py`) houden de
    oude code compileerbaar; ze krimpen bij stap 7 (C-code per systeem) en 8 (Frontier/contest, eerst Jordi).
  - ROM-ruimte: vóór 9,36 MB vrij (`__rom_end` 0x096A41C8), na 11,47 MB vrij (0x09488034), dus 2,11 MB erbij.
  - Oude saves/savestates zijn ongeldig: nieuw spel.

- **Pokémon buiten de dex eruit: afgerond (dex-agent, 23 okt).** Lijst, schakelaars en twijfelgevallen: `docs/concept/DEX_IN_ROM.md`.
  - In de ROM: de 213 lijnen van categorie A/B + Hitmontop, Mew, Mewtwo, Zarude (440 dexnummers, 582 soortconstanten
    incl. vormen). Eruit: 326 families (212 uit categorie C, 114 legendary/mythical/UB/paradox), Mega/Gmax/Ultra/Tera/Primal,
    en 51 losse vormen binnen behouden families (regionaal, totem, partner, Tyrogue/Hitmonlee/Hitmonchan, gewone Meowth/Grimer).
  - Schakelaars in `include/config/species_enabled.h`: families op `FALSE`, legendaries in één blok onderaan, `FU_*` voor
    losse vormen. `pokemon.o` wordt met `-fdata-sections` gebouwd, zodat ongebruikte sprites wegvallen.
  - Starters (`starter_choose.c`), Keccles/trainers en het TestMap-wild gebruiken nu alleen behouden soorten.
    Debugtests: Mewtwo lv 100 i.p.v. Arceus.
  - ROM-ruimte: vóór 11,47 MB vrij (`__rom_end` 0x09488034), na 18,55 MB vrij (0x08D71FE4), dus 7,09 MB erbij
    (kreten −4,68 MB, `pokemon.o` −2,41 MB).

## Stap 4 (expansion 1.14.4 → 1.17.1)
Niet begonnen. Remote `upstream` bestaat al in de repo.
