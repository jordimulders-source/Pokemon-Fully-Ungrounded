# Kaartgereedschap (Project Grounded)

Hulpscripts waarmee Claude kaarten bouwt, rendert en test. Draai alles vanuit de root van de repo.

| Bestand | Wat |
|---|---|
| `render_map.py <MapNaam> <uit.png> <y0> <y1>` | Rendert een kaart (met rasternummers en rode vakjes voor events) naar PNG. |
| `gridrender.py` | `render(grid, prim, sec)`: rendert een raster metatile-id's (voor prototypes). |
| `snowlib.py` | Bouwstenen voor sneeuwkaarten: `M` (kaart), `terrace` (klifterrassen, `face=` hoogte), `fall` (waterval zoals Ever Grande), `water` (meer met oevers), `autopath`, `blob`/`smooth` (organische vormen), `hforest` (besneeuwde Hoenn-randbomen). |
| `route135.py [voorbeeld.png]` | Bouwt `data/layouts/Route135/map.bin` opnieuw (vaste seed, dus identiek). |
| `route136.py`, `grotto136.py` | Bouwen Route 136 en de kristalgrot opnieuw. |
| `ashfrost.py [voorbeeld.png]` | Bouwt Ashfrost Village (primary `snow_town_base` + secondary `snow_town`, via `use_tileset('snow_town')` in `snowlib`). `SOFT=1` meldt objecten die niet passen in plaats van te stoppen. |
| `meteor_space.py [voorbeeld.png]` | Bouwt de Deoxys-meteoriet in de ruimte: eigen tileset `meteor_space` (donkere Meteor Falls-grond, randen per pixel getekend, sterren, aarde, kristallen), layout en map.json (44x64), gevechtsachtergrond `cave/space.pal`. Vaste seed, controleert de bereikbaarheid. |
| `reverse_pillar.py [rendermap]` | Bouwt de omgekeerde Sky Pillar (Giratina): tileset `sky_pillar_reverse` (Sky Pillar-metatiles op hun kop, Distortion World-kleuren), B1F/B2F/B3F als gespiegelde 1F/2F/5F, registreert layouts/maps/tileset en controleert de bereikbaarheid. |
| `fortree_jungle.py [voorbeeld.png]` | Bouwt Fortree Jungle (40x68, General + `fortree_jungle`, regen): paden, open plekken, lang gras, poelen en reuzenpalmen met autotiling (kruin/stam, oevers), openingen in de zuidrand van Fortree + connection, registratie; controleert de bereikbaarheid. Tropische laag (jungle-groene bomen met lianen, mangroves, stammen, bananen/heliconia, hibiscus, varens) via `jungle_tileset.py`. Vrijgehouden: open plek Zarude (zuidwest), masker-altaar Ogerpon (zuidoost). |
| `jungle_tileset.py [voorbeeld.png]` | Tileset `fortree_jungle`: kopie van Fortree, nieuwe tiles/metatiles alleen achteraan (connection met Fortree blijft naadloos); paletten 6 (jungleplanten, hout, Ekat99-mangrove), 7 (bloemen) en 12 (jungle-groene bomen + lianen). Los gedraaid: vergroot voorbeeld van alle tekeningen. |
| `rocket_hideout.py [rendermap]` | Bouwt de Rocket-hideout onder Fortree Jungle (1F opslag, B1F teleportdoolhof, B2F kantoor van Petrel) uit stukken van de Aqua Hideout, met tilesets `rocket_general`/`rocket_facility` (alleen eigen paletten, BASE-bestand). Koppelt de teleportvlakken, plaatst grunts/items en controleert de bereikbaarheid over de warps heen. |
| `liberty_garden.py` | Bouwt Liberty Garden (Victini-eiland, post-game): Southern Island-buitenkant met de grot dicht en een tuin met fontein, lantaarns en bloemen (Rustboro-tiles); layout, map.json, map_groups en event_scripts. Controleert de bereikbaarheid. |
| `darkrai_nightmare.py [voorbeeld.png]` | Bouwt Darkrai's nachtmerrie (`MtPyre_Nightmare`): uitsnede van de top van Mt. Pyre in zwarte leegte, eigen donkerpaarse paletten (`nightmare_general`/`nightmare_facility` lenen tiles van General/Facility; `BASE`-bestand voor `render_map.py`). |
| `icepuzzle_search.py <seed> <iteraties>` | Zoekt een ijsglijpuzzel die oplosbaar blijft voor elke combinatie van opgepakte items (gebruikt voor Coldstep ijskamer 2). |
| `emu.py` | Headless mGBA: `Emu(rom)`, `press()`, `debug_script(e, k)`. |
| `testrom.py <map> "script 1" [...]` | Test-ROM met tijdelijke debug-scripts (regels met `;`), zet `debug.inc` daarna terug en maakt een savestate na de intro. |
| `make_intro_state.py <rom> <uit.bin>` | Savestate na de intro (opnieuw maken na elke rebuild). |

## Testen in de emulator
1. Zet tijdelijk een `warp MAP_X, 255, x, y` + `waitstate` in `Debug_EventScript_Script_N` in `data/scripts/debug.inc` (maak eerst een backup).
2. `make -j4`, kopieer de ROM, zet `debug.inc` meteen terug (**nooit committen**).
3. Maak een savestate met `make_intro_state.py`, laad hem, `debug_script(e, N)`, maak screenshots met `e.img.to_pil()`.

## Sneeuwtileset
- Gegenereerd door `tools/grounded/snow_tileset.py` uit `graphics/grounded/snow_src/` (CinnaYva). Namen staan in `data/tilesets/secondary/snow/metatile_names.json`.
- `python3 tools/grounded/snow_tileset.py --town` maakt voor Ashfrost een eigen primary `snow_town_base` (grond, kliffen, water, bomen, decor) en secondary `snow_town` (gebouwen): 2×512 tiles, 13 paletten. Daarna `make data/tilesets/primary/snow_town_base/tiles.4bpp data/tilesets/secondary/snow_town/tiles.4bpp`.
- **Nieuwe metatiles altijd achteraan toevoegen**, anders verschuiven alle nummers en raken bestaande kaarten kapot.
- Na het genereren: `make data/tilesets/secondary/snow/tiles.4bpp` vóór het renderen.
- Tile-budget: max. 512 tiles per tileset; `snow` ~445. Een primary + secondary samen geeft 1024 (zie Ashfrost).
