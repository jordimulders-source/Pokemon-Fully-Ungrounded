"""Project Grounded: de omgekeerde Sky Pillar (Giratina, post-game).
Na Rayquaza scheurt de vloer van Sky Pillar 1F open (gat op GAT); wie erin springt valt in een gespiegelde toren
die steeds dieper gaat. Drie verdiepingen, gebouwd uit de vanilla Sky Pillar-layouts, verticaal gespiegeld:
- tileset sky_pillar_reverse: de Pacifidlog-tiles (Sky Pillar), alle metatiles op hun kop (rijen gewisseld en
  v-flip per tile) en de Sky Pillar-kleuren omgekeerd naar een paars/groene Distortion World. Gedrag: trapdeur ->
  zuidpijl (de trap ligt nu onderin), ingangsmat (zuidpijl) -> noordpijl.
- B1F = 1F gespiegeld (de ingangsmat bovenin leidt terug naar buiten), B2F = 2F gespiegeld zonder scheuren
  (op deze verdieping zijn boven en onder omgedraaid, zie field_control_avatar.c), B3F = 5F gespiegeld met
  alleen de linkertrap; Giratina zweeft voor de put.
Idempotent. Gebruik: python3 tools/grounded/maptools/reverse_pillar.py [render-map]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, os, shutil, struct, sys, colorsys

TS = 'data/tilesets/secondary/sky_pillar_reverse'
SRC = 'data/tilesets/secondary/pacifidlog'
MB_NON_ANIMATED_DOOR, MB_NORTH_ARROW_WARP, MB_SOUTH_ARROW_WARP = 0x60, 0x64, 0x65
W = H = 14

# ---------------------------------------------------------------- tileset
os.makedirs(TS + '/palettes', exist_ok=True)
shutil.copy(SRC + '/tiles.png', TS + '/tiles.png')
mts = open(SRC + '/metatiles.bin', 'rb').read()
attrs = open(SRC + '/metatile_attributes.bin', 'rb').read()
n = len(mts) // 16
out_m, out_a = b'', b''
for i in range(n):
    e = list(struct.unpack_from('<8H', mts, i * 16))
    f = []
    for layer in range(2):
        tl, tr, bl, br = e[layer * 4:layer * 4 + 4]
        f += [t ^ 0x800 for t in (bl, br, tl, tr)]          # rijen wisselen + v-flip
    f = [(t & 0x0FFF) | (7 << 12) if t >> 12 == 0 else t for t in f]   # General-palet 0 -> slot 7 (ROCK_SLOT)
    out_m += struct.pack('<8H', *f)
    a = struct.unpack_from('<H', attrs, i * 2)[0]
    beh = a & 0xFF
    if beh == MB_NON_ANIMATED_DOOR:
        beh = MB_SOUTH_ARROW_WARP
    elif beh == MB_SOUTH_ARROW_WARP:
        beh = MB_NORTH_ARROW_WARP
    out_a += struct.pack('<H', (a & 0xFF00) | beh)
open(TS + '/metatiles.bin', 'wb').write(out_m)
open(TS + '/metatile_attributes.bin', 'wb').write(out_a)


def read_pal(p):
    return [tuple(map(int, l.split())) for l in open(p).read().split('\n')[3:19]]


def distort(c, idx):
    """Distortion World: alles donkerder; blauwgrijs -> grauw paars (de put wordt een zwarte leegte), bruin ->
    vaal groen, goud -> Giratina-rood."""
    if idx == 0:
        return c
    r, g, b = [v / 255 for v in c]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if s < 0.08 or 0.45 < h < 0.80:              # grijs/blauw: vloer, put, stenen
        nh, ns, nl = 0.78, 0.18 + s * 0.25, 0.03 + l ** 1.6 * 0.62
    elif s > 0.35 and l > 0.45:                  # goud
        nh, ns, nl = 0.99, 0.75, 0.25 + (l - 0.45) * 0.8
    else:                                        # bruin: muren
        nh, ns, nl = 0.45, 0.22, 0.05 + l * 0.30
    r, g, b = colorsys.hls_to_rgb(nh, max(0.0, min(1.0, nl)), min(1.0, ns))
    return tuple(int(v * 255) // 8 * 8 for v in (r, g, b))


ROCK_SLOT = 7          # General-palet 0 (stenen) als omgekeerde kopie in een vrij secondary-slot
for i in range(16):
    pal = read_pal('%s/palettes/%02d.pal' % (SRC, i))
    if i == 6:
        pal = [distort(c, k) for k, c in enumerate(pal)]
    if i == ROCK_SLOT:
        pal = [distort(c, k) for k, c in enumerate(read_pal('data/tilesets/primary/general/palettes/00.pal'))]
    with open('%s/palettes/%02d.pal' % (TS, i), 'w', newline='\r\n') as fp:
        fp.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in pal))

# ---------------------------------------------------------------- layouts
CRACKED, FLOOR2F = 0x236, 0x234
WALL_TOP, WALL = 0x227, 0x22F


def load(name):
    b = open('data/layouts/%s/map.bin' % name, 'rb').read()
    return [list(struct.unpack_from('<%dH' % W, b, y * W * 2)) for y in range(H)]


def setid(v, idnum):
    return (v & ~0x3FF) | idnum


b1 = load('SkyPillar_1F')
b2 = load('SkyPillar_2F')
for row in b2:
    for x, v in enumerate(row):
        if v & 0x3FF == CRACKED:
            row[x] = setid(v, FLOOR2F)
b3 = load('SkyPillar_5F')
# rechtertrap van 5F (kolom 9-11, rij 0-1) dichtmetselen
for x in (9, 10, 11):
    b3[0][x] = WALL_TOP | (1 << 10)
    b3[1][x] = WALL | (1 << 10)

LAYOUTS = {'B1F': b1[::-1], 'B2F': b2[::-1], 'B3F': b3[::-1]}
NAMES = {k: 'SkyPillar_Reverse' + k for k in LAYOUTS}
CONSTS = {k: 'SKY_PILLAR_REVERSE_' + k for k in LAYOUTS}
lj = open('data/layouts/layouts.json').read()
for k, grid in LAYOUTS.items():
    name, const = NAMES[k], CONSTS[k]
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<%dH' % W, *r) for r in grid))
    shutil.copy('data/layouts/SkyPillar_1F/border.bin', 'data/layouts/%s/border.bin' % name)
    if '"LAYOUT_%s"' % const not in lj:
        i = lj.index('"id": "LAYOUT_SKY_PILLAR_TOP_CLEAN"'); j = lj.index('},', i) + 2
        lj = lj[:j] + '''
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_SkyPillarReverse",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    },''' % (const, name, W, H, name, name) + lj[j:]
open('data/layouts/layouts.json', 'w').write(lj)

# ---------------------------------------------------------------- maps
GIRATINA = (7, 10)


def warp(x, y, dest, wid):
    return {'x': x, 'y': y, 'elevation': 3, 'dest_map': 'MAP_' + dest, 'dest_warp_id': str(wid)}


WARPS = {
    'B1F': [warp(6, 0, 'SKY_PILLAR_OUTSIDE', 1), warp(7, 0, 'SKY_PILLAR_OUTSIDE', 1),
            warp(10, 12, CONSTS['B2F'], 0)],
    'B2F': [warp(10, 12, CONSTS['B1F'], 2), warp(3, 12, CONSTS['B3F'], 0)],
    'B3F': [warp(3, 12, CONSTS['B2F'], 1)],
}
for k in LAYOUTS:
    name = NAMES[k]
    m = {
        'id': 'MAP_' + CONSTS[k], 'name': name, 'layout': 'LAYOUT_' + CONSTS[k], 'music': 'MUS_MT_PYRE',
        'region_map_section': 'MAPSEC_SKY_PILLAR', 'requires_flash': False, 'weather': 'WEATHER_NONE',
        'map_type': 'MAP_TYPE_UNDERGROUND', 'allow_cycling': False, 'allow_escaping': True, 'allow_running': True,
        'show_map_name': False, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
        'object_events': [], 'warp_events': WARPS[k], 'coord_events': [], 'bg_events': [],
    }
    if k == 'B3F':
        m['object_events'] = [{
            'local_id': 'LOCALID_SKY_PILLAR_REVERSE_GIRATINA', 'graphics_id': 'OBJ_EVENT_GFX_SPECIES(GIRATINA_ORIGIN)',
            'x': GIRATINA[0], 'y': GIRATINA[1], 'elevation': 3, 'movement_type': 'MOVEMENT_TYPE_FACE_DOWN',
            'movement_range_x': 0, 'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE',
            'trainer_sight_or_berry_tree_id': '0', 'script': name + '_EventScript_Giratina',
            'flag': 'FLAG_HIDE_SKY_PILLAR_GIRATINA'}]
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')

# ---------------------------------------------------------------- bereikbaarheid
LANDING = (11, 11)     # waar je op B1F neerkomt (zelfde x,y als het gat op 1F)


def reach(grid, start):
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and not (grid[ny][nx] >> 10) & 3:
                seen.add((nx, ny)); todo.append((nx, ny))
    return seen


for k, start in (('B1F', LANDING), ('B2F', (10, 12)), ('B3F', (3, 12))):
    grid = LAYOUTS[k]
    r = reach(grid, start)
    need = [(w['x'], w['y']) for w in WARPS[k]] + ([(GIRATINA[0], GIRATINA[1] + 1)] if k == 'B3F' else [])
    missing = [c for c in need if c not in r]
    assert not missing, (k, 'onbereikbaar', missing)
print('bereikbaarheid ok')

gj = open('data/maps/map_groups.json').read()
es = open('data/event_scripts.s').read()
for k in LAYOUTS:
    name = NAMES[k]
    if '"%s"' % name not in gj:
        gj = gj.replace('    "MeteorSpace"\n', '    "MeteorSpace",\n    "%s"\n' % name, 1) if k == 'B1F' else \
             gj.replace('    "%s"\n' % NAMES[prev], '    "%s",\n    "%s"\n' % (NAMES[prev], name), 1)
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/MeteorSpace/scripts.inc"\n' if k == 'B1F' else \
                 '\t.include "data/maps/%s/scripts.inc"\n' % NAMES[prev]
        es = es.replace(anchor, anchor + inc, 1)
    prev = k
open('data/maps/map_groups.json', 'w').write(gj)
open('data/event_scripts.s', 'w').write(es)

# ---------------------------------------------------------------- tileset registreren
hdr = open('src/data/tilesets/headers.h').read()
if 'gTileset_SkyPillarReverse' not in hdr:
    hdr += '''
const struct Tileset gTileset_SkyPillarReverse = // Project Grounded: omgekeerde Sky Pillar (Giratina), via reverse_pillar.py
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_SkyPillarReverse,
    .palettes = gTilesetPalettes_SkyPillarReverse,
    .metatiles = gMetatiles_SkyPillarReverse,
    .metatileAttributes = gMetatileAttributes_SkyPillarReverse,
    .callback = NULL,
};
'''
    open('src/data/tilesets/headers.h', 'w').write(hdr)
gfx = open('src/data/tilesets/graphics.h').read()
if 'gTilesetTiles_SkyPillarReverse' not in gfx:
    gfx += '\nconst u32 gTilesetTiles_SkyPillarReverse[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");\n\n' % TS
    gfx += 'const u16 gTilesetPalettes_SkyPillarReverse[][16] =\n{\n'
    gfx += ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (TS, i) for i in range(16)) + '};\n'
    open('src/data/tilesets/graphics.h', 'w').write(gfx)
mh = open('src/data/tilesets/metatiles.h').read()
if 'gMetatiles_SkyPillarReverse' not in mh:
    mh += '\nconst u16 gMetatiles_SkyPillarReverse[] = INCBIN_U16("%s/metatiles.bin");\n' % TS
    mh += 'const u16 gMetatileAttributes_SkyPillarReverse[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % TS
    open('src/data/tilesets/metatiles.h', 'w').write(mh)
mk = open('graphics_file_rules.mk').read()
if 'secondary/sky_pillar_reverse/' not in mk:
    a = '$(TILESETGFXDIR)/secondary/pacifidlog/tiles.4bpp: %.4bpp: %.png\n\t$(GFX) $< $@ -num_tiles 504 -Wnum_tiles\n'
    mk = mk.replace(a, a + '\n$(TILESETGFXDIR)/secondary/sky_pillar_reverse/tiles.4bpp: %.4bpp: %.png\n\t$(GFX) $< $@ -num_tiles 504 -Wnum_tiles\n', 1)
    open('graphics_file_rules.mk', 'w').write(mk)
if len(sys.argv) > 1:
    import subprocess
    subprocess.run(['make', '-s', TS + '/tiles.4bpp'], check=True)
    for k in LAYOUTS:
        subprocess.run([sys.executable, 'tools/grounded/maptools/render_map.py', NAMES[k], '%s/%s.png' % (sys.argv[1], NAMES[k]), '0', '14'], check=True)
print('klaar')
