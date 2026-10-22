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
- **Muziek:** de nummers zijn nog niet opgeruimd. Het gaat om:
  - de YI-rips (663–667), MKSC (668, 669, 671, 672 en Sunset Wilds 620), WL4 (688–695), Area Zero (681, 682), Broken Pier (619), Yoshi Castle (618) en de Poké Tower-remix (687);
  - ze in `songs.h` als vrij markeren en in `song_table.inc` naar `mus_dummy` zetten;
  - opruimen in `battle_music_options.c`, in `pokemon.c` (`GetRegionalWildBattleMusic`: Area Zero, Poké Tower, YI, Lakeside Park) en in `battle_setup.c` (paradoxen en Terapagos gebruiken `MUS_GROUNDED_VS_AREA_ZERO`, die moet `MUS_GROUNDED_VS_LEGENDARY` worden);
  - de samples (`sound/direct_sound_samples/rip/{mksc,wl4}` en de YI/Area Zero-samples), de voicegroups en `direct_sound_data.inc` opruimen, en daarna `songtable_check.py` draaien.
  - Let op: WL4 Monsoon Jungle/Toy Block Tower/Arabian Night en MKSC Lakeside Park spelen nog op Hoenn-kaarten (Fortree Jungle, Mangrove Mire, Game Corner, Mirage Tower en wilde gevechten in de jungle). Die laten staan tot de Hoenn-kaarten weg zijn.
- Bouwscripts in `tools/grounded/maptools/` opruimen (spacetime_cave, yoshis_island, ultra_space, ultra_worlds_a/b, glimwood, chargestone, coronet, hall_of_origin, lakes, national_park(_tiles)), en ook `graphics/grounded/yoshis_island` en `bronnen/muziek/yoshis_island_gsf`.
- De overige punten uit TODO-stap 3 (intro's/films, Battle Frontier/Tents/Trick House) zijn niet aangeraakt.

## Stap 4 (expansion 1.14.4 → 1.17.1)
Niet begonnen. Remote `upstream` bestaat al in de repo.
