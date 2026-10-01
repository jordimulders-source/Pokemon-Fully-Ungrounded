# Kaartgereedschap (Project Grounded)

Hulpscripts waarmee Claude kaarten bouwt, rendert en test. Draai alles vanuit de root van de repo.

| Bestand | Wat |
|---|---|
| `render_map.py <MapNaam> <uit.png> <y0> <y1>` | Rendert een kaart (met rasternummers en rode vakjes voor events) naar PNG. |
| `gridrender.py` | `render(grid, prim, sec)`: rendert een raster metatile-id's (voor prototypes). |
| `snowlib.py` | Bouwstenen voor sneeuwkaarten: `M` (kaart), `terrace` (klifterrassen, `face=` hoogte), `fall` (waterval zoals Ever Grande), `water` (meer met oevers), `autopath`, `blob`/`smooth` (organische vormen), `hforest` (besneeuwde Hoenn-randbomen). |
| `route135.py [voorbeeld.png]` | Bouwt `data/layouts/Route135/map.bin` opnieuw (vaste seed, dus identiek). |
| `route136.py`, `grotto136.py` | Bouwen Route 136 en de kristalgrot opnieuw. |
| `ashfrost.py [voorbeeld.png]` | Bouwt Ashfrost Town (tileset `snow_town`, via `use_tileset('snow_town')` in `snowlib`). |
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
- `python3 tools/grounded/snow_tileset.py --town` maakt de stads-tileset `snow_town` (basis + gebouwen) voor Ashfrost; die heeft eigen metatile-nummers.
- **Nieuwe metatiles altijd achteraan toevoegen**, anders verschuiven alle nummers en raken bestaande kaarten kapot.
- Na het genereren: `make data/tilesets/secondary/snow/tiles.4bpp` vóór het renderen.
- Tile-budget: max. 512 tiles; nu ~431 in gebruik. Voor Ashfrost (Pokémon Center, Mart, huizen staan al in de bronsheet, rijen 104–134) is waarschijnlijk een eigen stads-tileset nodig.
