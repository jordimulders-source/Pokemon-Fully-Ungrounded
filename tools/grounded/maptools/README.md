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
| `fortree_jungle.py [voorbeeld.png]` | Bouwt Fortree Jungle (40x68, General + Fortree, regen): paden, open plekken, lang gras, poelen en reuzenpalmen met autotiling (kruin/stam, oevers), openingen in de zuidrand van Fortree + connection, registratie; controleert de bereikbaarheid. Vrijgehouden: open plek Zarude (zuidwest), masker-altaar Ogerpon (zuidoost). |
| `safari_zones.py [rendermap]` | Bouwt de drie nieuwe Safari-zones: Fairy Forest (44x40, pastel, glinsterbloemen), Thunder Plains (48x40, savanne met acacia's, onweer) en Haunted Camp (44x40, donker, mist, oud rusthuis). Maakt de openingen + warps + afzettingen (Safari-medewerker, weg met `FLAG_SAFARI_ZONES_OPEN`) in SafariZone_Southwest/Northwest/Northeast, registreert alles en controleert de bereikbaarheid. Roept `safari_tilesets.py` aan. |
| `safari_tilesets.py` | Tilesets van de Safari-zones: primary `safari_<zone>_general` (General met eigen paletten, `BASE`) en secondary `safari_<zone>` (kopie van Fortree/Fallarbor/Lilycove met eigen paletten en metatiles achteraan: pijlwarps, droog hoog gras, glinsterbloemen). Zet ook een westpijl-grastegel achteraan Lilycove. |
| `rocket_hideout.py [rendermap]` | Bouwt de Rocket-hideout onder Fortree Jungle (1F opslag, B1F teleportdoolhof, B2F kantoor van Petrel) uit stukken van de Aqua Hideout, met tilesets `rocket_general`/`rocket_facility` (alleen eigen paletten, BASE-bestand). Koppelt de teleportvlakken, plaatst grunts/items en controleert de bereikbaarheid over de warps heen. |
| `liberty_garden.py` | Bouwt Liberty Garden (Victini-eiland, post-game): Southern Island-buitenkant met de grot dicht en een tuin met fontein, lantaarns en bloemen (Rustboro-tiles); layout, map.json, map_groups en event_scripts. Controleert de bereikbaarheid. |
| `darkrai_nightmare.py [voorbeeld.png]` | Bouwt Darkrai's nachtmerrie (`MtPyre_Nightmare`): uitsnede van de top van Mt. Pyre in zwarte leegte, eigen donkerpaarse paletten (`nightmare_general`/`nightmare_facility` lenen tiles van General/Facility; `BASE`-bestand voor `render_map.py`). |
| `icepuzzle_search.py <seed> <iteraties>` | Zoekt een ijsglijpuzzel die oplosbaar blijft voor elke combinatie van opgepakte items (gebruikt voor Coldstep ijskamer 2). |
| `victory_road_ext.py [voorbeeld.png]` | Bouwt de vier optionele Victory Road-kamers (Wachtkamer/gauntlet, Kluis/Strength-puzzel, Kluizenaar/Reginald, Haaienbak/Garchomp) en hun ingangen in 1F/B1F/B2F; controleert bereikbaarheid (HM-poorten) en lost de blokpuzzel op (geen val, niets gratis). |
| `chimney_ext.py [voorbeeld.png]` | Bouwt de lavabuis onder Jagged Pass (`JaggedPass_LavaTube`, 40x30: twee grotopeningen in Jagged Pass, waarvan één achter een Rock Smash-rots, magmapoelen, Strength-nis) en de top van Mt. Chimney (`MtChimney_Summit`, 36x40: terrassen, kratermeer) + de trap in Mt. Chimney. Muren automatisch (grot = kuil met 30x-randen, buiten = terrassen met 27x-randen, lava met 347/346/289 en oever 3a3/3a4); controleert bereikbaarheid, trappen en randvormen. |
| `ogerpon_quest.py [rendermap]` | Ogerpon-quest: de drie schuilplaatsen van de Loyal Three (`GraniteCave_CornerstoneRoom` = kopie kamer van Steven, `FieryPath_EmberHollow` = lavagrot met de autotiler van `chimney_ext.py`, `Route127_WellspringGrotto` = kopie ingang Seafloor Cavern) + warps in Granite Cave B2F, Fiery Path en Underwater Route 127. De openingen zelf zet het ON_LOAD-script pas na `FLAG_OGERPON_QUEST_STARTED`. Controleert de bereikbaarheid. |
| `../lavaridge_decor.py [voorbeeld.png]` | Decor achteraan de Lavaridge-tileset (tiles 450+, metatiles 0x3B9+, eigen palet 12): zwavelkristallen, gloeiende scheuren, as-hoopjes, keien, gestolde lava, stronk, dode boom; elk op grotgrind (308) en berggrond (271). Schrijft `lavaridge/decor.json`, dat `chimney_ext.py` gebruikt. Vanilla-nummers blijven gelijk. |
| `tides_juan.py [voorbeeld.png]` | Eb en vloed op Route 132 (layout `Route132_LowTide`: wad met slik = `MB_DEEP_SAND`-kopieën achteraan Pacifidlog, rotsen, strandjutter, verborgen items; het map-script kiest de layout bij binnenkomst via `Grounded_UpdateTide`, even uur = eb) en Juans eiland op Route 129 (strand, palmen, lagune). Idempotent, controleert de bereikbaarheid. |
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
