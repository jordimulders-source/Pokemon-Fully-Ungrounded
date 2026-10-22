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
- Flags in `flags.h` (ongebruikt, kosten niets), de trainerfoto's van Giovanni/Agatha, de klassen Boss/Commander/Guest Star en de legendary-intro's (die zijn generiek en gaan op soort).
- Route 125: de rotstegel van de grotopening blijft staan (alleen de warp en `setmetatile` zijn weg).

## Nog te doen (stap 3)
- **Muziek: afgerond (muziek-agent, 22 okt).** Alle Ungrounded-muziek is weg, behalve Battle! Keccles (nu song 610):
  - weg: songs 610–725 (eigen composities, covers, legendary-/personage-/gymthema's, gym-/trainerklasse-/wild-/nachtremixes, Ashfrost, YI/MKSC/WL4-rips, Boo, Area Zero, Poké Tower), 103 MIDI's, 14 rip-`.s`-bestanden, `sound/songs/grounded_src/`, 143 voicegroup-bestanden, 8 eigen keysplits, 490 samples (`grounded/` behalve `kc_*`, heel `rip/`), `gym2_saw.pcm`, en de generatoren in `tools/grounded/` (`*_theme.py`/`*_samples.py` behalve Keccles en `gm_samples.py`);
  - code: `battle_music_options.c` (alleen vanilla-keuzes + Keccles), `GetBattleBGM` in `pokemon.c` (vanilla-logica + Keccles, Juan/Brock/Oak/Rocket-FRLG-muziek), `battle_setup.c` (legendaries → `MUS_RG_VS_LEGEND`, Mew/Jirachi → `MUS_VS_MEW`, Mewtwo → `MUS_RG_VS_MEWTWO`, beasts → `MUS_C_VS_LEGEND_BEAST`, Rayquaza → `MUS_VS_RAYQUAZA`, Regigigas → `MUS_VS_REGI`), nachtmuziek in `overworld.c` weg;
  - kaarten: Ashfrost → `MUS_FALLARBOR`, Coldstep Cave → `MUS_CAVE_OF_ORIGIN`, Fortree Jungle/Mangrove Mire → `MUS_ROUTE119`, Game Corner → `MUS_GAME_CORNER`, Mirage Tower → `MUS_MT_CHIMNEY` (vanilla).
  - ROM-ruimte: vóór 1,94 MB vrij (`__rom_end` 0x09E0EAEC), na 7,48 MB vrij (0x09885C38), dus 5,53 MB erbij.
  - Blijft: HQ-mixer, 16 BGM-sporen, mixer 21 kHz, de algemene muziektools. `bronnen/muziek/` (bronbestanden, niet in de ROM) is niet aangeraakt.
- Bouwscripts in `tools/grounded/maptools/` opruimen (spacetime_cave, yoshis_island, ultra_space, ultra_worlds_a/b, glimwood, chargestone, coronet, hall_of_origin, lakes, national_park(_tiles)), en ook `graphics/grounded/yoshis_island` en `bronnen/muziek/yoshis_island_gsf`.
- De overige punten uit TODO-stap 3 (intro's/films, Battle Frontier/Tents/Trick House) zijn niet aangeraakt.

## Stap 4 (expansion 1.14.4 → 1.17.1)
Niet begonnen. Remote `upstream` bestaat al in de repo.
