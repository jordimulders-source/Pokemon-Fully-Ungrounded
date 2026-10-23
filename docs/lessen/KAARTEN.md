# Lessen: Kaarten, tilesets en events

Lees vóór je een kaart, route, grot, stad of tileset bouwt. Opgesplitst uit CLAUDE.md (23 okt); nieuwe lessen hier toevoegen.

- **Bronsheets (Essentials/RMXP):** objecten beginnen vaak een (halve) rij hoger of een kolom anders dan je denkt (sneeuwpophoofd, boomtop, luifel, lantaarn). Zoom per object op pixelniveau in (`grid.py`-achtig) vóór het knippen, en controleer de render op afgekapte koppen/daken. Rode X-vakjes zijn markeringen: leeg laten.
- **Tile-limiet:** Essentials-art ontdubbelt slecht (een gebouw ≈ 50–60 tiles). Een eigen primary + secondary geeft 2×512 tiles en 13 paletten (zie Ashfrost). Onderlaag = grond (gedeeld uit de primary), bovenlaag = object.
- **Kliffen:** afgeschuinde hoeken bij kuilen/terrassen geven rommelige losse klifstukjes; gebruik rechte rechthoeken. Trappen midden in een rechte wand (laat het script dat controleren) en laat het pad tot op elke trap doorlopen (controleer de render op gaten). `cliff_front_b` in de sneeuwset heeft een grotopening; voor hoge wanden gestapelde `cliff_b`-rijen.
- **Deuren:** de deur-tile in de kaart moet precies de tile met deurgedrag uit de tileset zijn (groen huis: (2,3), niet (1,3)); anders loop je over de deur zonder warp.
- **Kaartgrootte wijzigen:** ook `layouts.json` (breedte/hoogte), warps, coord-triggers, heal location, inkomende warps (bijv. Route 136) en NPC-posities bijwerken.
- **Decor uit General** kan op sneeuw als je de graskleuren (palet 1/2, index 12–14) transparant maakt (`_general_metatile(..., nograss=True)`).
- **Coord-triggers** (`coord_events`) vergrendelen de besturing: ook een script dat alleen een geluid speelt moet eindigen met `releaseall`, anders sta je vast.
- **Sootopolis:** het eiland voor de gym is x 27–34, y 32–36; daaromheen is water (collision 0 zegt niets over water, kijk naar het metatile-gedrag 0x10).
- **Onderwater-ingang:** een zwemgat (metatiles 0x265–0x267 / 0x26D–0x26F, `MB_WATER_DOOR`) met een gewone warp naar een bovenwaterkaart werkt; je komt surfend uit als het doel water is. Duidelijker dan een onzichtbaar bovenkomplekje. `render_map.py` wil `<kaart> <uit.png> <y0> <y1>`.
- **Nieuwe kaart:** ook de `scripts.inc` in `data/event_scripts.s` opnemen, anders linkerfout op `*_MapScripts`.
- **Warp-elevation** moet gelijk zijn aan die van de tegel (0 = elke); vanilla-grotplateaus zijn soms elevation 4 (Altering Cave).
- **Kaart op zijn kop** (omgekeerde Sky Pillar, `reverse_pillar.py`): rijen per metatile wisselen + v-flip (bit 11) per tile, `map.bin`-rijen omdraaien, en het gedrag aanpassen (trapdeur 0x60 → zuidpijl, zuidpijl → noordpijl).
- **Object toevoegen aan een kaart met `"object_events": []`:** tekstueel vóór `"warp_events"` invoegen belandt in `connections`; controleer met `json.load`.
- **Zwarte leegte op een kaart:** metatile 0 is niet zwart (layer NORMAL tekent grasbasis op BG3); gebruik Facility-metatile 0x201. Kleine kaarten tonen de border: rondom aanvullen. `build/emerald/data/maps.o` volgt `map.bin`/`border.bin` niet: na een wijziging verwijderen.
- **Max. 128 kaarten per kaartgroep** (`struct WarpData` gebruikt `s8 mapNum`; kaart 128+ laat het spel vastlopen in `CB2_LoadMap2`). `gMapGroup_Dungeons` zit vol (128): nieuwe kaarten in `gMapGroup_Grounded` (achteraan `group_order`).
- **Max. 16 objecten tegelijk op een kaart** (speler incl.); objecten achteraan de lijst verschijnen dan niet (Stadium-arena in doubles).
- **Meteor Falls-wanden** zijn ringen rond de vloer: noord 231/231/23e, west 212/22a/234, oost 210/228/23c, zuid 286, hoeken 213/214 (`Map.rock_tile` in `meteor_falls_ext.py`). In testscripts `additem` i.p.v. `giveitem` (pop-ups blokkeren de debugtest).
- **Sneeuwkliffen:** `cliff_front_b` in de route-set `snow` heeft een grotopening (zwarte gaten); `snowlib` gebruikt `cliff_b`. Decor pas vanaf rij 2 (randbomen overschrijven rij 0–1); terrassen tot onder de bosrand laten doorlopen. `route135.py` maakt de huidige Route 135 niet meer na: niet opnieuw draaien zonder vergelijken.
- **Kaart met twee toestanden** (verzegelde tempel): twee layouts uit één script, kiezen met `setmaplayoutindex` in `ON_TRANSITION`. Vrije flags altijd met `grep FLAG_UNUSED_0x include/constants/flags.h` controleren (de lijsten hieronder kunnen verouderd zijn).
- **Kaarten met `setmaplayoutindex`** (Route 130 Mirage, 131 Sky Pillar, 132 eb/vloed, 111): wijzigingen ook in de andere layout zetten; Route 131 laadt altijd `Route131_SkyPillar`.
- **Verschijnende objecten zonder vaste flag:** `FLAG_TEMP_x` als objectflag, in `ON_TRANSITION` zetten/wissen (Dave in Petalburg/Sootopolis, de zeemijnen).
- **Randen in een vanilla-tileset:** een autotiler die per cel de tegel uit dezelfde 3x3-omgeving in een bestaande kaart kiest (`sootopolis_craters.py`) geeft nette randen zonder handwerk; klifbanden even dik als in het voorbeeld. Stadium-omroepregels max. 3 regels per vak. `testrom.py` draait `make_intro_state.py` met `python3`: los herhalen met `python3.11`.
- **Grotopening in een buitenkaart:** Cave-tegel 0x23c (zuidpijl-warp) op de vloer met 258/259/25a in de wand eronder, niet op zand. Verborgen gat in bomen: de Toadstool-tegels 0x35e–0x361 (Rustboro-set). Emulatortest na een warp: wacht op het mapnummer (`gSaveBlock1Ptr`+5).
- **Kusthoeken in Sootopolis-stijl:** geen eigen hoeken verzinnen; neem exact de tegelcombinaties uit SootopolisCity over (Jordi keurde losse klifblokjes, waterrandjes in de klif en plantjes-tegels 2de/2df af).
- **FRLG-kaart 1-op-1 overnemen** (`spacetime_cave.py`): metatile-raster + botsings-/hoogtebits van FRLG houden, per FRLG-metatile een eigen secondary-tegel ("reskin" naar Emerald-texturen), gedrag op naam vertalen (FRLG-enum → Emerald), daarna laagtype/gedrag patchen. `render_map.py` leidt de tilesetmap af van het symbool (`gTileset_FooBar` → `foo_bar`). Scheuren/teleporttegels 2x2: alleen de bovenste rij als warp.
- **Kaartgroepen:** Spacetime-locaties in `gMapGroup_Spacetime` (sinds v0.9.173); een nieuwe groep = achteraan `group_order` en als laatste sleutel in `map_groups.json`.
- **Sfeereffecten per pixel** (ruïnes, `ruin_beasts.py`): teken een canvas van de hele kaart en knip het in metatiles (`emit()` ontdubbelt); geditherde maskers met laagfrequente ruis geven grillige randen zonder halve tegels. Floats clippen vóór `uint8`, seeds met `zlib.crc32` (niet `hash()`), geen scipy in de container.
- **Bos in General/Petalburg:** grote bomen (0x1D4–0x1E7, kruin 0x1CE/0x1CF) op een raster van 2×2-cellen plannen; een open cel boven een boom krijgt de kruin in zijn onderste rij (geen events daar). Hoenn-boompjes 0x0E/0x0F/0x16/0x17 zijn 1 breed. Emulatortests: teksten met B sluiten (extra A opent ze opnieuw en blokkeert het volgende debugscript).
- **Sombere kaart:** `WEATHER_FOG_*` over een donker eigen palet wordt melkwit; gebruik `WEATHER_SHADE`. Bij `setmaplayoutindex` in `ON_TRANSITION` ook de objectflags daar zetten. Trainers in gangen van 1 breed blokkeren de route voorgoed: zet ze in zijnissen.
- **Cave-tileset is vol** (511/512 tiles sinds v0.9.179): nieuwe grotdecor in een eigen (getinte) secondary. Vrij palet in een tileset: geen metatile gebruikt `pal<<12` (tel `metatiles.bin >> 12`). Decor op water: metatile met laag COVERED (ondergrond onder, object midden). Quest-teller zonder var: vondst-flags tellen met `call_if_set` + `addvar VAR_TEMP_x`.
- **Grote legendary-sprites** vallen over de speler als je ze van de noordkant aanspreekt: zet ze zo dat je ze van opzij of onderen aanspreekt. Bootreis zonder animatie: `fadescreen FADE_TO_BLACK`, `playse SE_M_SURF`, `delay 40`, `warpsilent`.
- **Eigen tilesetanimatie** (draaikolken, `swords_isle.py`): frame 0 op vaste tegelplekken in `tiles.png` (uitsluiten van ontdubbelen), elk frame als 128×8-png, `AppendTilesetAnimToBuffer` naar `NUM_TILES_IN_PRIMARY + plek` in `tileset_anims.c`; gespiegelde tegels draaien de andere kant op. Schuim langs een kust: losse kammetjes, niet per vak (wordt een hek). Metatiles toevoegen aan een gegenereerde secondary: eerst terug naar het basisaantal, dan ontdubbelen.
- **Geanimeerd vuur op de kaart:** `graphics/battle_anims/sprites/fire.png` (8 frames 32×32) werkt als tileset-vuur; vlammen op een boomkruin met een grillige onderrand (recht = "vlammenhoed"). Na wijzigingen in tileset-/animatieplaatjes `touch src/tilesets.c src/tileset_anims.c`.
- **Meer met zwemgrot** (`lakes.py`): General-vijver met `pond_tile()` (vooraf 3x3-opening op de watervorm), Route 120-heuvel met `MB_WATER_DOOR` + een Scorched Slab-kopie op `gTileset_Cave`. Sneeuwset heeft geen bordtegel: sign op een sneeuwpop. Kristallen 0x3A5–0x3A7 alleen op 0x211-vloer.
- **Debug Zone warp** (Utilities): naar elke kaart; na nieuwe kaarten `python3 tools/grounded/debug_zone_warps.py`. Acties met een parameter in `debug.c` moeten in `DebugTask_HandleMenuInput_General` een eigen `else if` krijgen, anders krijgen ze geen `actionParams`.
- **Water op elevation 0 is beloopbaar** (Nothing Island, v1.0): water hoort op elevation 1; met 0 loop je er zonder surfen op. Controle: `waterelev.py`-aanpak (water met botsing 0 en elevation 0 naast beloopbaar land). **Halve bomen** controleer je per kaart met een script (links-/rechterhelft 1d4/1d5, 1dc/1dd, 1e4/1e5 moeten paren vormen), niet alleen op het oog: Jordi vond in Lavender drie plekken na elkaar.
- **Bereikbaarheid in grotten:** reken met objecten (rotsen) én gescheurde vloer (`MB_CRACKED_FLOOR*`, Mach Bike) als blokkade, anders zie je omwegen en fiets-routes over het hoofd (Granite Cave, 13 okt).


## Werkwijzen

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
- Teams en levels: zie "Trainer parties". Teksten: **meteen een placeholder in de toon van dit project** (serieuzer verhaal, droge humor waar het past; zie Toon) (Jordi, 5 okt: "dat mag je voortaan doen"): droog, absurd, donker, self-aware, popcultuur, soms de vierde wand doorbrekend. Lees eerst wat bestaande teksten van Jordi en de humor-entries in de changelog (v0.6.x). Kort houden. Geldt ook voor teksten die subagents schrijven: geef ze deze opdracht mee. Jordi herschrijft wat hij wil via de Dialoogstudio.

### Testen
- `python3 tools/grounded/maptools/testrom.py <scratchmap> "regels script 1" ["regels script 2" ...]` bouwt een test-ROM met tijdelijke debug-scripts (bijv. `warp MAP_X, x, y; waitstate`) en zet `debug.inc` terug. Daarna in Python: `Emu(rom)`, `load(e, intro)`, `debug_script(e, 1)` (`emu.py`). Bouw daarna opnieuw voor een schone ROM.
- **Testgevechten:** altijd met een **Mewtwo lv 100** (Arceus zit sinds v0.0.7 niet meer in de ROM) met Dark Pulse, Psychic, Thunderbolt en Ice Beam (`givemon SPECIES_MEWTWO, 100, move1=MOVE_DARK_PULSE, move2=MOVE_PSYCHIC, move3=MOVE_THUNDERBOLT, move4=MOVE_ICE_BEAM`), tenzij een gevecht een ander soort Pokémon vereist. Zet in het testscript ook **alle badges** aan (`setflag FLAG_BADGE01_GET` t/m `FLAG_BADGE08_GET`), anders luistert Arceus niet.
- Valkuilen: savestates zijn ongeldig na een rebuild; `data/scripts/debug.inc` nooit committen; grote JSON-bestanden (`wild_encounters.json`, `layouts.json`, `map_groups.json`) tekstueel bewerken, niet via `json.dump`; trainer-AI in `trainers.party` met bestaande namen (bijv. `Check Bad Move / Try To Faint`); nieuwe kaarten achteraan hun groep in `map_groups.json` (nieuwe eigen kaarten in `gMapGroup_Grounded`).

### Afronden van een stuk werk
`make -j4` slaagt → changelogsectie → **Stand van zaken** bijwerken (kort) → commit en push. Bij een kaart: één render van de hele kaart naar Jordi (plus emulatorbeelden als er iets te zien valt). Geen ROM tenzij gevraagd.

