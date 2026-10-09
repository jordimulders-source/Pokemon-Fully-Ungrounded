"""Project Grounded: vijf Ultra Space-werelden, elk met een eigen getekende tileset (Jordi, 9 okt: "je kan veel beter").

Vervangt de oude kaarten van ultra_space.py (zelfde kaartnamen, zelfde plek in het portaal; ultra_space.py slaat ze
over via EXTERNAL_B en leest de aankomstplek uit het warpblok van de hub, dat dit script bijwerkt):
- UltraSpace_Guzzlord     Lilycove, maar door Guzzlord kapotgegeten: warenhuis met een hap eruit, Contest Hall als
                          krater (Guzzlord in het midden), museum ingestort, haven met gebroken pier, as en puin.
- UltraSpace_Stakataka    een echt doolhof van Stakataka-stenen met ogen in de muren (knipperen via een tileset-
                          animatie; losse ogen (OBJ_EVENT_GFX_ULTRA_EYE) draaien mee naar de speler), de muur van
                          Stakataka in het hart.
- UltraSpace_Blacephalon  circus: tent, piste, tribunes, ringen, ballonnen (animatie), clowns met teksten,
                          Blacephalon als ster van de show.
- UltraSpace_Necrozma     prismagrot: kristallen in alle kleuren, lichtstralen, regenboogbreking, spiegelvloer,
                          glinsteringen (animatie), Necrozma op een zwart altaar dat het licht opslokt.
- UltraSpace_Poipole      buitenaardse wereld (space horror): meteorieten, uitbarstingen, gasgeisers, bliksem en
                          zwaartekrachtscheuren (animaties + src/ultra_worlds.c), de aliens met Poipole.
Elke wereld: eigen primary + secondary (ultra_worlds_b_art.emit_pair), wilde Pokémon (12 unieke soorten),
de UB als object (FLAG_ULTRA_*, zelfde scripts als in ultra_space.py), terug via het wormgat.

Gebruik: python3 tools/grounded/maptools/ultra_worlds_b.py [--scripts] [--only Key,Key] [--preview DIR]
  --scripts  schrijft de scripts.inc's opnieuw (anders alleen als ze nog niet bestaan; Jordi bewerkt teksten in de
             Dialoogstudio)."""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
_sys.path.append(_os.path.dirname(_os.path.abspath(__file__)))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import importlib.util, json, math, os, random, re, struct, sys, zlib  # noqa: E401,E402
from collections import deque  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
import ultra_worlds_b_art as A  # noqa: E402
import nieuwe_items as ni  # noqa: E402

REPO = A.REPO
os.chdir(REPO)
FORCE_SCRIPTS = '--scripts' in sys.argv
ONLY = sys.argv[sys.argv.index('--only') + 1].split(',') if '--only' in sys.argv else None
PREVIEW = sys.argv[sys.argv.index('--preview') + 1] if '--preview' in sys.argv else None
_spec = importlib.util.spec_from_file_location('dialogen_import', 'tools/dialogen/import.py')
dimp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dimp)
MAPSEC = 'MAPSEC_ALTERING_CAVE'
WORM = 'OBJ_EVENT_GFX_ULTRA_WORMHOLE'
EYE = 'OBJ_EVENT_GFX_ULTRA_EYE'
EKAT = 'graphics/grounded/tilesets/ekat/'


def mon(sp):
    return 'OBJ_EVENT_GFX_SPECIES(%s)' % sp


def obj(lid, gfx, x, y, script, flag='0', move='MOVEMENT_TYPE_FACE_DOWN', sight='0', rx=0, ry=0, elev=3):
    o = {'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move,
         'movement_range_x': rx, 'movement_range_y': ry, 'trainer_type': 'TRAINER_TYPE_NONE',
         'trainer_sight_or_berry_tree_id': sight, 'script': script, 'flag': flag}
    if lid:
        o = dict(local_id=lid, **o)
    return o


def map_const(name):
    return 'MAP_' + re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name).upper()


def layout_const(name):
    return 'LAYOUT_' + re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', name).upper()


# ====================================================================== bereikbaarheid
def reachable(coll, start, blocked=()):
    H, W = coll.shape
    seen = {start}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and not coll[n[1], n[0]] and n not in blocked:
                seen.add(n)
                q.append(n)
    return seen


def dist_map(coll, start, blocked=()):
    H, W = coll.shape
    d = {start: 0}
    q = deque([start])
    while q:
        c = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + dx, c[1] + dy)
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in d and not coll[n[1], n[0]] and n not in blocked:
                d[n] = d[c] + 1
                q.append(n)
    return d


def next_to(r, x, y):
    return any((x + dx, y + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


def check_spec(spec):
    """bereikbaarheid van UB, wormgat, NPC's, items + max. 15 objecten in elk beeld"""
    w = spec['world']
    key = w.key
    objs = spec['objects']
    blocked = {(o['x'], o['y']) for o in objs}
    arrive = spec['arrive']
    assert not w.coll[arrive[1], arrive[0]], (key, 'aankomst op een muur')
    assert arrive not in blocked, (key, 'aankomst op een object')
    r = reachable(w.coll, arrive, blocked)
    for o in objs:
        if o.get('decor'):
            continue
        assert next_to(r, o['x'], o['y']) or (o['x'], o['y']) in r, (key, 'onbereikbaar object', o['graphics_id'], o['x'], o['y'])
    for b in spec['bgs']:
        assert (b['x'], b['y']) in r or next_to(r, b['x'], b['y']), (key, 'onbereikbaar bg-event', b)
    for c in spec.get('coords', []):
        assert (c['x'], c['y']) in r, (key, 'onbereikbare coord-trigger', c)
    # max. 15 objecten tegelijk (speler = 16e): spawnvenster x-9..x+10, y-7..y+9 rond elke bereikbare plek
    worst = 0
    pts = [(o['x'], o['y']) for o in objs]
    for (px, py) in r:
        n = sum(1 for (x, y) in pts if px - 9 <= x <= px + 10 and py - 7 <= y <= py + 9)
        worst = max(worst, n)
    assert worst <= 15, (key, 'te veel objecten in beeld', worst)
    assert len(objs) <= 64
    return r, worst


# ====================================================================== registratie in de bron
BLOCK_START = '// ultra_worlds_b {'
BLOCK_END = '// } ultra_worlds_b'


def put_block(path, lines, header):
    s = open(path).read()
    blk = '%s %s\n%s\n%s' % (BLOCK_START, header, '\n'.join(lines), BLOCK_END)
    if BLOCK_START in s:
        i = s.index(BLOCK_START)
        j = s.index(BLOCK_END, i) + len(BLOCK_END)
        s = s[:i] + blk + s[j:]
    else:
        s = s.rstrip('\n') + '\n\n' + blk + '\n'
    open(path, 'w').write(s)


def ts_sym(key, prim):
    return 'UltraB%s%s' % (key, 'Base' if prim else '')


def ts_path(key, prim):
    return 'data/tilesets/%s/ultra_b_%s%s' % ('primary' if prim else 'secondary', key.lower(), '_base' if prim else '')


def register_tilesets(results):
    gfx, mts, hdr = [], [], []
    anim_c, anim_h = [], []
    for key, info in results:
        for prim in (True, False):
            sym = ts_sym(key, prim)
            d = ts_path(key, prim)
            gfx.append('const u32 gTilesetTiles_%s[] = INCBIN_U32("%s/tiles.4bpp.fastSmol");' % (sym, d))
            gfx.append('const u16 gTilesetPalettes_%s[][16] =\n{' % sym)
            gfx += ['    INCBIN_U16("%s/palettes/%02d.gbapal"),' % (d, i) for i in range(16)]
            gfx.append('};\n')
            mts.append('const u16 gMetatiles_%s[] = INCBIN_U16("%s/metatiles.bin");' % (sym, d))
            mts.append('const u16 gMetatileAttributes_%s[] = INCBIN_U16("%s/metatile_attributes.bin");' % (sym, d))
            cb = 'InitTilesetAnim_%s' % sym if (not prim and info['anims']) else 'NULL'
            hdr.append('const struct Tileset gTileset_%s =\n{\n    .isCompressed = TRUE,\n    .isSecondary = %s,\n'
                       '    .tiles = gTilesetTiles_%s,\n    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n'
                       '    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = %s,\n};\n'
                       % (sym, 'FALSE' if prim else 'TRUE', sym, sym, sym, sym, cb))
        if info['anims']:
            sym = ts_sym(key, False)
            d = ts_path(key, False)
            body = []
            for a in info['anims']:
                nm = '%s_%s' % (sym, a['name'].capitalize())
                for f in range(a['nframes']):
                    anim_c.append('static const u16 sTilesetAnims_%s_Frame%d[] = INCBIN_U16("%s/anim/%s/%d.4bpp");' % (nm, f, d, a['name'], f))
                anim_c.append('static const u16 *const sTilesetAnims_%s[] = {\n%s};' % (
                    nm, ''.join('    sTilesetAnims_%s_Frame%d,\n' % (nm, f) for f in range(a['nframes']))))
                anim_c.append('static const u8 sTilesetAnimSeq_%s[] = {%s};' % (nm, ', '.join(str(v) for v in a['seq'])))
                body.append('    if (timer %% %d == %d)\n        AppendTilesetAnimToBuffer(sTilesetAnims_%s[sTilesetAnimSeq_%s[(timer / %d) %% ARRAY_COUNT(sTilesetAnimSeq_%s)]],\n'
                            '                                  (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(NUM_TILES_IN_PRIMARY + %d)), %d * TILE_SIZE_4BPP);'
                            % (a['period'], a.get('phase', len(body) % a['period']), nm, nm, a['period'], nm, a['slot'], a['ntiles']))
            anim_c.append('static void TilesetAnim_%s(u16 timer)\n{\n%s\n}\n' % (sym, '\n'.join(body)))
            anim_c.append('void InitTilesetAnim_%s(void)\n{\n    sSecondaryTilesetAnimCounter = 0;\n'
                          '    sSecondaryTilesetAnimCounterMax = sPrimaryTilesetAnimCounterMax;\n'
                          '    sSecondaryTilesetAnimCallback = TilesetAnim_%s;\n}\n' % (sym, sym))
            anim_h.append('void InitTilesetAnim_%s(void);' % sym)
    put_block('src/data/tilesets/graphics.h', gfx, '(tools/grounded/maptools/ultra_worlds_b.py: Ultra Space-werelden, eigen tilesets)')
    put_block('src/data/tilesets/metatiles.h', mts, '(tools/grounded/maptools/ultra_worlds_b.py)')
    put_block('src/data/tilesets/headers.h', hdr, '(tools/grounded/maptools/ultra_worlds_b.py)')
    put_block('src/tileset_anims.c', anim_c, '(tools/grounded/maptools/ultra_worlds_b.py: animaties van de Ultra Space-werelden)')
    # header: declaraties binnen de include-guard
    p = 'include/tileset_anims.h'
    s = open(p).read()
    blk = '%s\n%s\n%s' % (BLOCK_START, '\n'.join(anim_h), BLOCK_END)
    if BLOCK_START in s:
        i = s.index(BLOCK_START)
        j = s.index(BLOCK_END, i) + len(BLOCK_END)
        s = s[:i] + blk + s[j:]
    else:
        i = s.rindex('#endif')
        s = s[:i] + blk + '\n\n' + s[i:]
    open(p, 'w').write(s)


def save_layout(name, grid, border, key):
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', t) for r in grid for t in r))
    open('data/layouts/%s/border.bin' % name, 'wb').write(struct.pack('<4H', *border))
    lj = open('data/layouts/layouts.json').read()
    const = layout_const(name)
    entry = '''    {
      "id": "%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_%s",
      "secondary_tileset": "gTileset_%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (const, name, len(grid[0]), len(grid), ts_sym(key, True), ts_sym(key, False), name, name)
    m = re.search(r'    \{\n      "id": "%s",.*?\n    \}' % const, lj, re.S)
    if m:
        lj = lj[:m.start()] + entry + lj[m.end():]
    else:
        i = lj.rindex('    }\n  ]')
        lj = lj[:i + 5] + ',\n' + entry + lj[i + 5:]
    json.loads(lj)
    open('data/layouts/layouts.json', 'w').write(lj)
    return const


def write_map_json(spec, lconst):
    name = 'UltraSpace_' + spec['world'].key
    objs = [{k: v for k, v in o.items() if k != 'decor'} for o in spec['objects']]
    d = {'id': map_const(name), 'name': name, 'layout': lconst, 'music': spec['music'],
         'region_map_section': MAPSEC, 'requires_flash': False, 'weather': spec.get('weather', 'WEATHER_NONE'),
         'map_type': 'MAP_TYPE_UNDERGROUND', 'allow_cycling': False, 'allow_escaping': False,
         'allow_running': True, 'show_map_name': False, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL',
         'connections': None, 'object_events': objs, 'warp_events': [], 'coord_events': spec.get('coords', []),
         'bg_events': spec['bgs']}
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')


def update_hub(key, arrive):
    p = 'data/maps/UltraSpace_Hub/scripts.inc'
    s = open(p).read()
    s2 = re.sub(r'(UltraSpace_Hub_EventScript_To%s::\n\twarp MAP_ULTRA_SPACE_\w+, )\d+, \d+' % key,
                r'\g<1>%d, %d' % arrive, s)
    assert 'UltraSpace_Hub_EventScript_To%s::' % key in s
    open(p, 'w').write(s2)


# ---------------------------------------------------------------- wilde Pokémon
def write_encounters(key, mons, rate):
    """mons: 12 x (soort, min, max) in slotvolgorde (20/20/10/10/10/10/5/5/4/4/1/1)"""
    assert len(mons) == 12 and len({m[0] for m in mons}) == 12, key
    p = 'src/data/wild_encounters.json'
    s = open(p).read()
    mc = map_const('UltraSpace_' + key)
    body = ',\n'.join('            {\n              "min_level": %d,\n              "max_level": %d,\n              "species": "SPECIES_%s"\n            }'
                      % (lo, hi, sp) for sp, lo, hi in mons)
    entry = ('        {\n          "map": "%s",\n          "base_label": "gUltraSpace%s",\n          "land_mons": {\n'
             '            "encounter_rate": %d,\n            "mons": [\n%s\n            ]\n          }\n        }'
             % (mc, key, rate, body.replace('\n            ', '\n              ').replace('              {', '              {', 1)))
    # netjes inspringen zoals de rest: per mon-object 14 spaties
    lines = []
    for sp, lo, hi in mons:
        lines.append('              {\n                "min_level": %d,\n                "max_level": %d,\n                "species": "SPECIES_%s"\n              }' % (lo, hi, sp))
    entry = ('        {\n          "map": "%s",\n          "base_label": "gUltraSpace%s",\n          "land_mons": {\n'
             '            "encounter_rate": %d,\n            "mons": [\n%s\n            ]\n          }\n        }'
             % (mc, key, rate, ',\n'.join(lines)))
    m = re.search(r'        \{\n          "map": "%s",.*?\n        \}(?=,?\n)' % mc, s, re.S)
    if m:
        s = s[:m.start()] + entry + s[m.end():]
    else:
        # achteraan de eerste groep (gWildMonHeaders): vóór de afsluiting van "encounters"
        i = s.index('"encounters": [')
        j = s.index('\n      ]', i)
        s = s[:j] + ',\n' + entry + s[j:]
    json.loads(s)
    open(p, 'w').write(s)


# ---------------------------------------------------------------- scripts
def text_block(label, txt):
    plain = txt.replace('\\p', '\n\n').replace('\\l', ' ')
    plain = '\n\n'.join(re.sub(r'\s*\n\s*', ' ', b).strip() for b in plain.split('\n\n'))
    return ['%s:' % label] + ['\t.string "%s"' % l for l in dimp.to_strings(plain)] + ['']


def ub_script(name, species, level):
    sp = 'SPECIES_' + species
    flag = 'FLAG_ULTRA_' + species
    return ['%s_EventScript_UB::' % name, '\tlock', '\tfaceplayer',
            '\tplaymoncry %s, CRY_MODE_ENCOUNTER' % sp,
            '\tmsgbox %s_Text_UB, MSGBOX_DEFAULT' % name, '\twaitmoncry', '\tclosemessage',
            '\tsetwildbattle %s, %d' % (sp, level), '\tspecial BattleSetup_StartLegendaryBattle',
            '\twaitstate', '\tspecialvar VAR_RESULT, GetBattleOutcome',
            '\tgoto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, %s_EventScript_UBCaught' % name,
            '\tgoto_if_eq VAR_RESULT, B_OUTCOME_WON, %s_EventScript_UBBack' % name,
            '\trelease', '\tend', '',
            '%s_EventScript_UBBack::' % name, '\tmsgbox %s_Text_UBBack, MSGBOX_DEFAULT' % name,
            '\trelease', '\tend', '',
            '%s_EventScript_UBCaught::' % name, '\tsetflag %s' % flag, '\tgoto UltraSpace_EventScript_CaughtFade', '']


def write_scripts(spec):
    name = 'UltraSpace_' + spec['world'].key
    path = 'data/maps/%s/scripts.inc' % name
    if os.path.exists(path) and not FORCE_SCRIPTS:
        return
    out = ['%s_MapScripts::' % name, '\tmap_script MAP_SCRIPT_ON_RESUME, %s_OnResume' % name]
    if spec.get('on_transition'):
        out.append('\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransition' % name)
    out += ['\t.byte 0', '', '%s_OnResume:' % name, '\tsetstepcallback STEP_CB_ULTRA_WORLDS', '\tend', '']
    if spec.get('on_transition'):
        out += ['%s_OnTransition:' % name] + ['\t' + l for l in spec['on_transition']] + ['\tend', '']
    if spec.get('ub_script', True):
        out += ub_script(name, spec['species'], spec['level'])
    out += spec.get('extra_scripts', [])
    for lbl, kind in spec.get('npc_scripts', []):
        out += ['%s_EventScript_%s::' % (name, lbl), '\tmsgbox %s_Text_%s, %s' % (name, lbl, kind), '\tend', '']
    out += ['@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)']
    for lbl, txt in spec['texts']:
        out += text_block('%s_Text_%s' % (name, lbl), txt)
    open(path, 'w').write('\n'.join(out) + '\n')


# ====================================================================== kleur-hulpjes
def C(*c):
    return np.array(c, float)


def shade(c, f):
    return np.clip(np.asarray(c, float) * f, 0, 255)


def mix(a, b, t):
    return np.asarray(a, float) * (1 - t) + np.asarray(b, float) * t


def rgba(h, w, fill=None):
    a = np.zeros((h, w, 4))
    if fill is not None:
        a[..., :3] = fill
        a[..., 3] = 255
    return a


def hsv(h, s, v):
    import colorsys
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
    return C(r * 255, g * 255, b * 255)


WORLDS = {}


def world(fn):
    WORLDS[fn.__name__.replace('world_', '').capitalize()] = fn
    return fn


# ====================================================================== STAKATAKA: doolhof met ogen
ST_FLOOR = [C(20, 22, 30), C(27, 30, 40), C(36, 40, 52), C(14, 15, 21)]
ST_CAP = [C(84, 88, 104), C(104, 109, 126), C(128, 134, 152), C(160, 166, 184), C(58, 61, 74)]
ST_BRICK = [C(46, 49, 60), C(58, 62, 76), C(70, 75, 90), C(92, 98, 116), C(120, 126, 144)]
ST_MORTAR = C(20, 21, 28)
ST_CYAN = [C(16, 72, 104), C(32, 152, 200), C(120, 224, 248), C(208, 248, 255)]
ST_SCLERA = C(216, 214, 196)


def st_floor_cell(x, y, kind=0):
    """vloertegel (16x16): donkere leistenen platen van 32x32, zacht reliëf; kind 1 = hartvloer (gepolijst)"""
    img = rgba(16, 16, ST_FLOOR[1])
    px, py = x % 2, y % 2
    h = zlib.crc32(b'st%d,%d' % (x // 2, y // 2)) % 9
    base = ST_FLOOR[1] if h < 6 else (ST_FLOOR[0] if h < 8 else mix(ST_FLOOR[1], ST_FLOOR[2], 0.4))
    if kind == 1:
        base = C(24, 30, 42)
    img[..., :3] = base
    if px == 0:
        img[:, 0, :3] = ST_FLOOR[3]
        img[:, 1, :3] = mix(base, ST_FLOOR[2], 0.5)
    if py == 0:
        img[0, :, :3] = ST_FLOOR[3]
        img[1, :, :3] = mix(base, ST_FLOOR[2], 0.5)
    if kind == 0:
        rs = random.Random(h * 13 + px * 2 + py)
        for _ in range(2):
            sx, sy = rs.randrange(3, 14), rs.randrange(3, 14)
            img[sy, sx, :3] = mix(base, ST_FLOOR[2], 0.7)
            img[sy, sx + 1, :3] = ST_FLOOR[3]
    return img


def st_rune(img, kind):
    """ingegraveerde, zwak cyaan gloeiende rune midden op de tegel"""
    pts = {0: [(5, 8), (6, 7), (7, 6), (8, 6), (9, 7), (10, 8), (9, 9), (8, 10), (7, 10), (6, 9), (7, 8), (8, 8)],
           1: [(4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (11, 4), (10, 5), (5, 10), (4, 11)],
           2: [(8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (5, 6), (6, 6), (10, 6), (11, 6), (6, 11), (10, 11)]}[kind]
    for (x, y) in pts:
        img[y, x, :3] = ST_CYAN[0] if kind else ST_CYAN[1]
    return img


def st_rubble(img, seed):
    """een paar losse stenen op de vloer"""
    rs = random.Random(seed)
    for _ in range(rs.randint(2, 4)):
        bx, by = rs.randrange(1, 11), rs.randrange(3, 12)
        bw, bh = rs.choice(((5, 3), (4, 3), (3, 2), (6, 3)))
        img[by + 1:by + bh + 1, bx + 1:bx + bw + 1, :3] = ST_FLOOR[3]                 # schaduw
        img[by:by + bh, bx:bx + bw, :3] = ST_BRICK[2]
        img[by, bx:bx + bw, :3] = ST_BRICK[4]
        img[by + bh - 1, bx:bx + bw, :3] = ST_BRICK[0]
    return img


def st_brick_row(img, y0, h, off, seedbase):
    """een rij stenen (hoogte h incl. voeg); 'off' = verspringing"""
    W = img.shape[1]
    h = min(h, img.shape[0] - y0)
    x = -off
    i = 0
    while x < W:
        bw = 8 if (i + seedbase) % 3 else 6
        x0, x1 = max(x, 0), min(x + bw - 1, W)
        tone = ST_BRICK[1 + ((i * 7 + seedbase) % 5 == 0)] if (i + seedbase) % 4 else ST_BRICK[0]
        img[y0:y0 + h - 1, x0:x1, :3] = tone
        img[y0, x0:x1, :3] = ST_BRICK[3]
        if h > 3:
            img[y0 + h - 2, x0:x1, :3] = mix(tone, ST_MORTAR, 0.4)
        if x1 < W:
            img[y0:y0 + h - 1, x1, :3] = ST_MORTAR
        x += bw
        i += 1
    img[y0 + h - 1, :, :3] = ST_MORTAR


def st_eye(img, cx, cy, state, look=0, r=4):
    """oog in een steen: state 0 open, 1 half, 2 dicht; look -1 links, 0 midden, 1 rechts"""
    dark = C(10, 10, 16)
    if state == 2:
        img[cy, cx - r:cx + r + 1, :3] = dark
        img[cy + 1, cx - r + 1:cx + r, :3] = mix(ST_BRICK[0], dark, 0.5)
        return img
    hh = 2 if state == 0 else 1
    for dy in range(-hh, hh + 1):
        wd = r - (1 if abs(dy) == 2 else 0)
        img[cy + dy, cx - wd:cx + wd + 1, :3] = ST_SCLERA
        img[cy + dy, cx - wd, :3] = mix(ST_SCLERA, dark, 0.5)
        img[cy + dy, cx + wd, :3] = mix(ST_SCLERA, dark, 0.5)
    img[cy - hh - 1, cx - r + 1:cx + r, :3] = dark                                   # bovenooglid
    img[cy + hh + 1, cx - r + 2:cx + r - 1, :3] = mix(ST_BRICK[0], dark, 0.6)       # onderooglid
    px = cx + look * (r - 2)
    for dy in range(-hh, hh + 1):
        for dx in (-1, 0, 1):
            img[cy + dy, px + dx, :3] = ST_CYAN[1] if abs(dx) == 1 or abs(dy) == 2 else ST_CYAN[2]
    img[cy, px, :3] = dark
    if state == 0:
        img[cy - 1, px, :3] = dark
        img[cy - 1, px - 1, :3] = ST_CYAN[3]
    return img


def st_wall_cell(x, y, south_floor, north_floor, west_floor, east_floor):
    """muurvak: bovenvlak = lichte afdekstenen; met een voorkant (2 rijen stenen) als het vak eronder vloer is"""
    img = rgba(16, 16, ST_CAP[1])
    vx, vy = x % 4, y % 2
    # afdekstenen 8x8 (verspringend), lichte linkerboven-rand, donkere voeg
    for by in (0, 8):
        off = 4 if ((y * 2 + by // 8) % 2) else 0
        for bx in (-off, 8 - off, 16 - off):
            x0, x1 = max(bx, 0), min(bx + 8, 16)
            if x0 >= x1:
                continue
            t = ST_CAP[1] if zlib.crc32(b'cap%d,%d,%d' % (vx, vy, bx + by)) % 3 else ST_CAP[0]
            img[by:by + 8, x0:x1, :3] = t
            img[by, x0:x1, :3] = mix(t, ST_CAP[2], 0.6)
            img[by + 7, x0:x1, :3] = mix(t, ST_CAP[4], 0.7)
            if bx >= 0:
                img[by:by + 8, x0, :3] = mix(t, ST_CAP[2], 0.4)
            if bx + 8 <= 16:
                img[by:by + 8, min(bx + 7, 15), :3] = ST_CAP[4]
    if north_floor:
        img[0, :, :3] = ST_CAP[3]
    if west_floor:
        img[:, 0, :3] = C(14, 14, 20)
        img[:, 1, :3] = ST_CAP[2]
    if east_floor:
        img[:, 15, :3] = C(14, 14, 20)
    if south_floor:
        top = 5
        img[top - 1, :, :3] = ST_CAP[3]
        img[top:16, :, :3] = ST_BRICK[1]
        st_brick_row(img, top, 6, (x % 2) * 4, vx * 7 + vy)
        st_brick_row(img, top + 6, 5, (x % 2) * 4 + 4, vx * 5 + vy * 3 + 1)
        img[15, :, :3] = C(10, 10, 14)
        if west_floor:
            img[top:, 0, :3] = C(14, 14, 20)
        if east_floor:
            img[top:, 15, :3] = C(14, 14, 20)
    return img


def maze(W, H, rnd, carve, loops=25):
    """perfect doolhof (recursive backtracker) op oneven coördinaten + een paar extra lussen; carve: open gebieden"""
    wall = np.ones((H, W), bool)
    cells = [(x, y) for y in range(1, H - 1, 2) for x in range(1, W - 1, 2)]
    start = cells[rnd.randrange(len(cells))]
    stack = [start]
    seen = {start}
    wall[start[1], start[0]] = False
    while stack:
        x, y = stack[-1]
        nb = [(x + dx, y + dy, dx, dy) for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2))
              if 0 < x + dx < W - 1 and 0 < y + dy < H - 1 and (x + dx, y + dy) not in seen]
        if not nb:
            stack.pop()
            continue
        nx, ny, dx, dy = rnd.choice(nb)
        wall[y + dy // 2, x + dx // 2] = False
        wall[ny, nx] = False
        seen.add((nx, ny))
        stack.append((nx, ny))
    cand = [(x, y) for y in range(1, H - 1) for x in range(1, W - 1) if wall[y, x] and (
        (not wall[y, x - 1] and not wall[y, x + 1] and wall[y - 1, x] and wall[y + 1, x]) or
        (not wall[y - 1, x] and not wall[y + 1, x] and wall[y, x - 1] and wall[y, x + 1]))]
    rnd.shuffle(cand)
    for (x, y) in cand[:len(cand) // loops]:
        wall[y, x] = False
    for (x0, y0, x1, y1) in carve:
        wall[y0:y1 + 1, x0:x1 + 1] = False
    return wall


@world
def world_stakataka():
    W, H = 41, 33
    w = A.World('Stakataka', W, H, seed=848)
    HEART = (14, 9, 26, 17)          # hart (open)
    PLAZA = (17, 27, 23, 31)         # aankomst
    SW = (16, 8, 24, 11)             # de Stakataka-muur: noordkant van het hart (4 rijen: bovenkant + 3 rijen stenen)
    ROOMS = [(5, 5, 7, 7), (33, 5, 35, 7), (5, 23, 7, 25), (33, 23, 35, 25)]   # pleintjes met een oog in de vloer
    arrive = (20, 30)
    ret = (20, 29)
    ub = (20, 12)
    x0, y0, x1, y1 = HEART

    def layout(seed):
        rnd = random.Random(seed)
        wall = maze(W, H, rnd, [HEART, PLAZA] + ROOMS)
        for x in range(x0 - 1, x1 + 2):
            wall[y0 - 1, x] = True
            wall[y1 + 1, x] = True
        for y in range(y0 - 1, y1 + 2):
            wall[y, x0 - 1] = True
            wall[y, x1 + 1] = True
        wall[13, x0 - 1] = wall[13, x0 - 2] = False      # poortjes west en oost
        wall[13, x1 + 1] = wall[13, x1 + 2] = False
        px0, py0, px1, py1 = PLAZA
        for x in range(px0 - 1, px1 + 2):
            wall[py0 - 1, x] = True
        for y in range(py0 - 1, py1 + 1):
            wall[y, px0 - 1] = True
            wall[y, px1 + 1] = True
        wall[py0 - 1, 17] = wall[py0 - 2, 17] = False
        wall[py0 - 1, 23] = wall[py0 - 2, 23] = False
        wall[0, :] = wall[-1, :] = True
        wall[:, 0] = wall[:, -1] = True
        for y in range(SW[1], SW[3] + 1):
            for x in range(SW[0], SW[2] + 1):
                wall[y, x] = True
        dm = dist_map(wall, arrive, {ret})
        return wall, dm.get((x0, 13), 0), dm.get((x1, 13), 0)
    best = None
    for seed in range(848, 948):
        wall, a, b = layout(seed)
        if a and b and min(a, b) >= 90 and (best is None or min(a, b) > best[1]):
            best = (seed, min(a, b))
            if min(a, b) >= 120:
                break
    wall, a, b = layout(best[0])
    print('Stakataka: doolhof seed %d, weg naar het hart %d/%d stappen' % (best[0], a, b))
    w.coll[:] = wall
    heart = lambda x, y: x0 <= x <= x1 and y0 <= y <= y1  # noqa: E731
    # ---------------------------------------------------------------- tekenen
    blink_cells = []
    for y in range(H):
        for x in range(W):
            if wall[y, x]:
                s = y + 1 < H and not wall[y + 1, x]
                n = y > 0 and not wall[y - 1, x]
                ww = x > 0 and not wall[y, x - 1]
                e = x + 1 < W and not wall[y, x + 1]
                w.put(st_wall_cell(x, y, s, n, ww, e), x, y)
                if s and not (SW[0] <= x <= SW[2] and SW[1] <= y <= SW[3]) and zlib.crc32(b'eye%d,%d' % (x, y)) % 4 == 0:
                    blink_cells.append((x, y))
            else:
                img = st_floor_cell(x, y, 1 if heart(x, y) else 0)
                if y > 0 and wall[y - 1, x]:                      # schaduw van de muur erboven
                    img[0:3, :, :3] = mix(img[0:3, :, :3], C(4, 4, 8), 0.6)
                    img[3:5, ::2, :3] = mix(img[3:5, ::2, :3], C(4, 4, 8), 0.4)
                if x > 0 and wall[y, x - 1]:
                    img[:, 0:2, :3] = mix(img[:, 0:2, :3], C(4, 4, 8), 0.4)
                hsh = zlib.crc32(b'rune%d,%d' % (x, y))
                if not heart(x, y):
                    if hsh % 19 == 0:
                        st_rune(img, hsh // 19 % 3)
                    elif hsh % 17 == 0:
                        st_rubble(img, hsh % 5)
                    w.beh[y, x] = 0x08                            # MB_CAVE: wilde Pokémon in de gangen
                w.put(img, x, y)
    for y in range(PLAZA[1], PLAZA[3] + 1):
        for x in range(PLAZA[0], PLAZA[2] + 1):
            w.beh[y, x] = 0
    # hart: inleg van cyaan ringen in de gepolijste vloer, licht van de muur in banden
    cx, cy = 20 * 16 + 8, 14 * 16 + 8
    d = np.hypot((w.xx - cx) / 1.0, (w.yy - cy) * 1.7)
    hm = np.zeros(w.bot.shape[:2], bool)
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not wall[y, x]:
                hm[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = True
    for r, col in ((40, ST_CYAN[1]), (41, ST_CYAN[0]), (72, ST_CYAN[0]), (100, ST_CYAN[0])):
        ring = hm & (np.abs(d - r) < 0.75)
        w.bot[ring] = col
    # vier 'oogstralen' in de vloer
    for k in range(8):
        a = k * math.pi / 4
        for t in range(44, 70):
            px_, py_ = int(cx + math.cos(a) * t), int(cy + math.sin(a) * t / 1.7)
            if hm[py_, px_]:
                w.bot[py_, px_] = ST_CYAN[0] if t % 4 else ST_CYAN[1]
    # oog in het midden van de hartvloer
    eye_floor(w, cx, cy, 13)
    # licht van de muur: twee rijen onder de muur iets cyaan
    for (yy0, yy1, t) in ((12 * 16, 12 * 16 + 6, 0.35), (12 * 16 + 6, 12 * 16 + 12, 0.18)):
        sl = (slice(yy0, yy1), slice(SW[0] * 16 - 8, (SW[2] + 1) * 16 + 8))
        m = hm[sl]
        w.bot[sl][m] = mix(w.bot[sl][m], ST_CYAN[0], t)
    # pleintjes: een oog in de vloer, geen wilde Pokémon
    for (rx0, ry0, rx1, ry1) in ROOMS:
        eye_floor(w, (rx0 + rx1 + 1) * 8, (ry0 + ry1 + 1) * 8, 9)
        for y in range(ry0, ry1 + 1):
            for x in range(rx0, rx1 + 1):
                w.beh[y, x] = 0
    st_wall_of_stakataka(w, SW)
    # ---------------------------------------------------------------- animatie: knipperende ogen in de muren
    base_cells = {c: w.cellpix(*c).copy() for c in blink_cells}

    def eye_fn(f, x, y):
        img = np.concatenate([base_cells[(x, y)].copy(), np.full((16, 16, 1), 255.0)], 2)
        state, look = [(0, 0), (0, -1), (0, 1), (1, 0), (2, 0)][f]
        ex = 5 + (zlib.crc32(b'ex%d,%d' % (x, y)) % 3) * 3
        st_eye(img, ex, 10, state, look)
        return img
    seqs = [[0] * 10 + [1, 1, 0, 0, 2, 2, 0] + [0] * 6 + [3, 4, 3],
            [0] * 4 + [3, 4, 3] + [0] * 12 + [2, 2, 2, 0, 1, 1] + [0] * 3,
            [0] * 7 + [1, 1, 1, 0] + [0] * 9 + [3, 4, 4, 3, 0, 2, 2]]
    rnd2 = random.Random(5)
    rnd2.shuffle(blink_cells)
    for gi in range(3):
        g = blink_cells[gi::3]
        byvar = {}
        for c in g:
            k = (base_cells[c].astype(np.uint8).tobytes(), zlib.crc32(b'ex%d,%d' % c) % 3)
            byvar.setdefault(k, []).append(c)
        reps = sorted(byvar.values(), key=len, reverse=True)[:9]
        cells = [v[0] for v in reps]
        a = w.anim('eyes%d' % gi, eye_fn, cells, seqs[gi], 8)
        for v in byvar.values():
            for c in v:
                w.put(eye_fn(0, *c), *c)
                if v in reps:
                    w.anim_cell[c] = (a, reps.index(v))
    # ---------------------------------------------------------------- objecten
    objs = [obj('LOCALID_ULTRA_STAKATAKA_RETURN', WORM, ret[0], ret[1], 'UltraSpace_EventScript_ReturnToHub'),
            obj('LOCALID_ULTRA_STAKATAKA_UB', mon('STAKATAKA'), ub[0], ub[1], 'UltraSpace_Stakataka_EventScript_UB',
                'FLAG_ULTRA_STAKATAKA')]
    # twee 'stenen' naast de UB zijn ook Stakataka (verdwijnen als je hem vangt)
    for x in (17, 23):
        objs.append(obj(None, mon('STAKATAKA'), x, 12, 'UltraSpace_Stakataka_EventScript_Wall', 'FLAG_ULTRA_STAKATAKA'))
    cands = [(x, y) for y in range(1, H - 1) for x in range(1, W - 1) if wall[y, x] and not wall[y + 1, x]
             and not (SW[0] - 1 <= x <= SW[2] + 1 and SW[1] - 1 <= y <= SW[3] + 1) and (x, y) not in base_cells]
    rnd3 = random.Random(77)
    rnd3.shuffle(cands)
    eyes = []
    for c in cands:
        if any(abs(c[0] - e[0]) + abs(c[1] - e[1]) < 6 for e in eyes):
            continue
        pts = [(o['x'], o['y']) for o in objs] + eyes + [c]
        ok = all(sum(1 for (x, y) in pts if px - 9 <= x <= px + 10 and py - 7 <= y <= py + 9) <= 13
                 for (px, py) in [(c[0] + dx, c[1] + dy) for dx in range(-10, 11) for dy in range(-9, 10)])
        if ok:
            eyes.append(c)
        if len(eyes) >= 36:
            break
    for e in eyes:
        objs.append(dict(obj(None, EYE, e[0], e[1], 'UltraSpace_Stakataka_EventScript_Eye'), decor=True))
    # verborgen Steel Memory: het verste doodlopende eind
    dm = dist_map(wall, arrive, {ret})
    deadends = [c for c in dm if sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (c[0] + dx, c[1] + dy) in dm) == 1]
    hid = max(deadends, key=lambda c: dm[c])
    bgs = []
    for fl, it, q, h in ni.items('UltraSpace_Stakataka'):
        bgs.append({'type': 'hidden_item', 'x': hid[0], 'y': hid[1], 'elevation': 3, 'item': it, 'flag': fl})
    texts = [('UB', 'The wall is looking at you.\\pOne brick in particular is looking at you\nreally hard.'),
             ('UBBack', 'The bricks reshuffle. The wall is still\nlooking at you. Harder now.'),
             ('Wall', 'The wall looks at you. You look at the\nwall. Nobody blinks. Bricks can\'t blink.'),
             ('Eye', 'An eye in the wall. It follows you.\\pYou move left. It moves left. You\nmove right. It sighs.')]
    return dict(world=w, objects=objs, bgs=bgs, arrive=arrive, ret=ret, ub=ub, species='STAKATAKA', level=90,
                music='MUS_SEALED_CHAMBER', weather='WEATHER_NONE', texts=texts,
                npc_scripts=[('Wall', 'MSGBOX_NPC'), ('Eye', 'MSGBOX_SIGN')],
                encounters=[('CLAYDOL', 86, 88), ('BRONZONG', 86, 88), ('PROBOPASS', 87, 89), ('GIGALITH', 87, 89),
                            ('GOLURK', 86, 88), ('CARBINK', 85, 87), ('KLINKLANG', 87, 89), ('SIGILYPH', 86, 88),
                            ('SABLEYE', 85, 87), ('DUSKNOIR', 88, 90), ('AEGISLASH', 90, 91), ('NOSEPASS', 66, 68)],
                rate=6)


def eye_floor(w, cx, cy, r):
    """groot oog ingelegd in de vloer (cyaan iris, donkere pupil), om (cx, cy) in pixels"""
    for yy in range(int(cy - r), int(cy + r + 1)):
        for xx in range(int(cx - r * 1.6), int(cx + r * 1.6 + 1)):
            dx, dy = (xx - cx) / (r * 1.6), (yy - cy) / (r * 0.75)
            e = dx * dx + dy * dy
            if e > 1.0:
                continue
            if e > 0.78:
                w.bot[yy, xx] = ST_CYAN[1]
                continue
            d = math.hypot(xx - cx, yy - cy)
            if d < r * 0.25:
                w.bot[yy, xx] = C(6, 8, 12)
            elif d < r * 0.55:
                w.bot[yy, xx] = ST_CYAN[1] if (xx + yy) % 2 else ST_CYAN[0]
            elif d < r * 0.62:
                w.bot[yy, xx] = ST_CYAN[2]
            else:
                w.bot[yy, xx] = C(40, 46, 56)
    w.bot[int(cy - r * 0.3), int(cx - r * 0.2)] = ST_CYAN[3]


def st_wall_of_stakataka(w, SW):
    """de muur van Stakataka: grote stenen met cyaan ogen; bovenste rij = afdekking, dan drie rijen stenen"""
    x0, y0, x1, y1 = SW
    pw, ph = (x1 - x0 + 1) * 16, (y1 - y0 + 1) * 16
    img = rgba(ph, pw, ST_BRICK[0])
    # afdekking (16 px): lichte stenen, net als de muren
    for bx in range(0, pw, 16):
        img[0:12, bx:bx + 16, :3] = ST_CAP[1]
        img[0, bx:bx + 16, :3] = ST_CAP[3]
        img[0:12, bx, :3] = ST_CAP[2]
        img[11, bx:bx + 16, :3] = ST_CAP[4]
    img[12:16, :, :3] = ST_CAP[3]
    img[15, :, :3] = ST_CAP[0]
    rs = random.Random(9)
    rows = [(16, 11), (27, 11), (38, 12), (50, 12)]
    for r, (ry, rh) in enumerate(rows):
        x = -(r % 2) * 12
        while x < pw:
            bw = rs.choice((20, 22, 24, 26))
            xa, xb = max(x, 0), min(x + bw - 2, pw)
            tone = ST_BRICK[1 + rs.randrange(2)]
            img[ry:ry + rh - 1, xa:xb, :3] = tone
            img[ry, xa:xb, :3] = ST_BRICK[4]
            img[ry + 1, xa:xb, :3] = ST_BRICK[3]
            img[ry + rh - 2, xa:xb, :3] = mix(tone, ST_MORTAR, 0.5)
            if xa > 0:
                img[ry:ry + rh - 1, xa, :3] = ST_BRICK[3]
            img[ry:ry + rh - 1, max(xb - 1, 0), :3] = ST_BRICK[0]
            if xb - xa > 12 and rs.random() < 0.85:
                st_eye(img, (xa + xb) // 2, ry + rh // 2 - 1, rs.choice((0, 0, 0, 1)), rs.choice((-1, 0, 0, 1)), r=4)
            x += bw
    img[-2:, :, :3] = C(8, 8, 12)
    img[:, 0, :3] = C(10, 10, 14)
    img[:, -1, :3] = C(10, 10, 14)
    w.put(img, x0, y0)


# ====================================================================== gedeeld: grotvormen
def blob_mask(W, H, shapes, seed, wobble=1.2, smooth=2):
    """vloermasker uit ellipsen (cx, cy, rx, ry) en gangen ('c', x0, y0, x1, y1, breedte), met ruis op de rand"""
    rs = np.random.RandomState(seed)
    nz = A.value_noise(H, W, 3, seed) * wobble
    yy, xx = np.mgrid[0:H, 0:W]
    m = np.zeros((H, W), bool)
    for s in shapes:
        if s[0] == 'c':
            _, xa, ya, xb, yb, wd = s
            n = int(max(abs(xb - xa), abs(yb - ya)) * 2) + 1
            for i in range(n + 1):
                t = i / n
                px, py = xa + (xb - xa) * t, ya + (yb - ya) * t
                m |= np.hypot(xx - px, yy - py) <= wd / 2.0 + nz * 0.3
        else:
            cx, cy, rx, ry = s
            m |= ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0 + nz * 0.35
    for _ in range(smooth):
        n = sum(np.roll(np.roll(m, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1))
        m = np.where(n >= 6, True, np.where(n <= 3, False, m))
    m[0, :] = m[-1, :] = False
    m[:, 0] = m[:, -1] = False
    m[1, :] = False
    rs.rand()
    return m


def periodic_voronoi(size, n, seed):
    """facetten (tegelbaar): geeft (index per pixel, randmasker)"""
    rs = np.random.RandomState(seed)
    pts = rs.uniform(0, size, (n, 2))
    yy, xx = np.mgrid[0:size, 0:size]
    best = np.full((size, size), 1e9)
    second = np.full((size, size), 1e9)
    idx = np.zeros((size, size), int)
    for i, (px, py) in enumerate(pts):
        for ox in (-size, 0, size):
            for oy in (-size, 0, size):
                d = np.hypot(xx - px - ox, yy - py - oy)
                closer = d < best
                second = np.where(closer, best, np.minimum(second, d))
                idx = np.where(closer, i, idx)
                best = np.where(closer, d, best)
    return idx, (second - best) < 1.2


# ====================================================================== NECROZMA: prismagrot
NZ_ROCK = [C(10, 6, 20), C(20, 14, 38), C(34, 24, 60), C(52, 40, 88), C(84, 70, 130), C(140, 128, 190)]
NZ_FLOOR = [C(12, 10, 24), C(18, 15, 34), C(26, 22, 48), C(40, 36, 70)]
HUES = [0.0, 0.08, 0.15, 0.33, 0.5, 0.6, 0.75, 0.88]       # rood, oranje, geel, groen, cyaan, blauw, violet, roze


def crystal_cols(h, sat=1.0):
    if h == 'black':   # leeggezogen kristal (bij Necrozma): zwart glas met een prismarand
        return [C(4, 2, 8), C(22, 16, 36), C(40, 32, 64), C(84, 72, 128), C(200, 180, 255)]
    if h is None:      # wit/helder
        return [C(56, 60, 88), C(120, 128, 168), C(184, 192, 224), C(232, 236, 252), C(255, 255, 255)]
    return [hsv(h, 0.85 * sat, 0.30), hsv(h, 0.75 * sat, 0.55), hsv(h, 0.60 * sat, 0.82), hsv(h, 0.32 * sat, 1.0), hsv(h, 0.08, 1.0)]


def draw_prism(img, bx, by, hgt, wid, lean, cols):
    """één kristal (zeshoekige zuil met punt) vanaf de voet (bx, by) omhoog; cols: donker..licht"""
    Hh, Ww = img.shape[:2]
    tip = max(3, wid // 1)
    for t in range(hgt + 1):
        y = by - t
        cx = bx + lean * t / max(hgt, 1)
        if t > hgt - tip:
            half = wid / 2.0 * (hgt - t) / tip
        else:
            half = wid / 2.0
        xl, xr = cx - half, cx + half
        for x in range(int(math.floor(xl)), int(math.ceil(xr)) + 1):
            if not (0 <= x < Ww and 0 <= y < Hh):
                continue
            if x < xl - 0.5 or x > xr + 0.5:
                continue
            u = (x - xl) / max(xr - xl, 0.01)
            if x <= xl + 0.5 or x >= xr - 0.5:
                c = cols[0]
            elif u < 0.38:
                c = cols[3]
            elif u < 0.5:
                c = cols[4] if t > 1 else cols[3]
            elif u < 0.78:
                c = cols[2]
            else:
                c = cols[1]
            img[y, x, :3] = c
            img[y, x, 3] = 255
    # voet: donkere rand
    for x in range(int(bx - wid / 2), int(bx + wid / 2) + 1):
        if 0 <= x < Ww and 0 <= by < Hh and img[by, x, 3] > 0:
            img[by, x, :3] = cols[0]


def crystal_cluster(cw, ch, hue, seed, white=False):
    """cluster van 3-6 kristallen in een vak van cw x ch cellen; voet in de onderste cel"""
    rs = random.Random(seed)
    img = np.zeros((ch * 16, cw * 16, 4))
    cols = crystal_cols(None if white else hue)
    n = rs.randint(3, 3 + cw * 2)
    base_y = ch * 16 - 3
    items = []
    for i in range(n):
        bx = rs.uniform(4, cw * 16 - 4)
        hgt = rs.uniform(ch * 16 * 0.35, ch * 16 * 0.92)
        wid = rs.choice((5, 6, 7, 8)) if cw > 1 else rs.choice((4, 5, 6))
        lean = rs.uniform(-0.6, 0.6) * hgt * 0.45
        if abs(bx - cw * 8) > cw * 5:
            lean += (bx - cw * 8) * 0.3
        items.append((hgt, bx, wid, lean))
    items.sort(key=lambda t: -t[0])          # hoge achteraan, lage vooraan
    for hgt, bx, wid, lean in items:
        hgt = min(hgt, base_y - 2)
        draw_prism(img, bx, base_y - rs.randint(0, 2), int(hgt), wid, lean, cols)
    return img


def reflect(w, img, x, y, strength=0.35):
    """spiegeling van een kristal in de glazen vloer, onder de voet (img: RGBA, linksboven = vak (x, y))"""
    h = img.shape[0]
    flip = img[::-1].copy()
    y0 = (y * 16) + h - 2
    for dy in range(min(h // 2, 14)):
        yy = y0 + dy
        if yy >= w.bot.shape[0]:
            break
        row = flip[dy]
        a = (row[:, 3] > 0) & (A.B4[yy % 4, (np.arange(row.shape[0]) + x * 16) % 4] < strength * (1 - dy / 14.0) * 2)
        xs = np.arange(row.shape[0]) + x * 16
        ok = a & (xs < w.bot.shape[1])
        w.bot[yy, xs[ok]] = mix(w.bot[yy, xs[ok]], row[ok, :3], 0.55)


@world
def world_necrozma():
    W, H = 42, 32
    w = A.World('Necrozma', W, H, seed=411)
    shapes = [(21, 6.5, 12, 5),             # altaarzaal (noord)
              (7.5, 15, 6, 6.8), (34.5, 15, 6, 6.8),     # galerijen west (koel) / oost (warm)
              (21, 20.5, 13, 4.6),          # prismahal
              (21, 27, 7, 3),               # ingang
              ('c', 7, 12, 13, 6, 3), ('c', 35, 12, 29, 6, 3),
              ('c', 10, 19, 13, 20, 3), ('c', 32, 19, 29, 20, 3),
              ('c', 21, 24, 21, 27, 4)]
    floor = blob_mask(W, H, shapes, 411, wobble=1.1)
    for x in range(12, 31):                 # kristalwand: geen rechte weg van de hal naar het altaar
        for y in range(11, 16):
            floor[y, x] = False
    arrive, ret, ub = (21, 28), (21, 27), (21, 6)
    for (x, y) in (arrive, ret, ub, (21, 29), (20, 28), (22, 28)):
        floor[y, x] = True
    wall = ~floor
    zone = lambda x, y: 'altar' if y <= 10 else ('west' if x <= 13 else ('east' if x >= 29 else 'hall'))  # noqa: E731
    ZONE_HUES = {'west': [0.5, 0.55, 0.6, 0.66, 0.75], 'east': [0.0, 0.04, 0.08, 0.12, 0.15],
                 'hall': HUES, 'altar': ['black', 'black', None]}
    # ---------------------------------------------------------------- wanden: obsidiaan met facetten
    vid, vedge = periodic_voronoi(64, 20, 7)
    fl = np.random.RandomState(3).uniform(0, 1, 20)
    stripes = np.array([0.55 + 0.45 * math.sin(i * 1.7) * math.cos(i * 0.6) for i in range(32)])
    for y in range(H):
        for x in range(W):
            if not wall[y, x]:
                continue
            img = rgba(16, 16, NZ_ROCK[1])
            sub = vid[(y * 16) % 64:(y * 16) % 64 + 16, (x * 16) % 64:(x * 16) % 64 + 16]
            ed = vedge[(y * 16) % 64:(y * 16) % 64 + 16, (x * 16) % 64:(x * 16) % 64 + 16]
            img[..., :3] = A.ramp(fl[sub] * 0.38 + 0.05, NZ_ROCK[:5])
            img[ed, :3] = NZ_ROCK[2]
            s = y + 1 < H and not wall[y + 1, x]
            n = y > 0 and not wall[y - 1, x]
            wv = x > 0 and not wall[y, x - 1]
            e = x + 1 < W and not wall[y, x + 1]
            if s:
                for xx in range(16):
                    v = stripes[(x * 16 + xx) % 32]
                    img[3:15, xx, :3] = A.ramp(np.full(12, v * 0.62) * np.linspace(1.0, 0.5, 12), NZ_ROCK[1:6])
                hz = ZONE_HUES[zone(x, y)]
                hue = hz[(x // 2) % len(hz)]
                gl = hsv(hue if isinstance(hue, float) else 0.75, 0.5 if isinstance(hue, float) else 0.15, 0.95)
                gx = [3, 9, 6, 12][x % 4]
                img[5:10, gx, :3] = gl
                img[6:9, gx + 1, :3] = mix(gl, NZ_ROCK[2], 0.5)
                img[2, :, :3] = NZ_ROCK[5]
                img[3, :, :3] = NZ_ROCK[4]
                img[15, :, :3] = C(4, 2, 10)
                img[14, :, :3] = NZ_ROCK[0]
            if n:
                img[0, :, :3] = NZ_ROCK[4]
                img[1, :, :3] = NZ_ROCK[0]
            if wv:
                img[:, 0, :3] = NZ_ROCK[0]
                img[:, 1, :3] = NZ_ROCK[3]
            if e:
                img[:, 15, :3] = NZ_ROCK[0]
                img[:, 14, :3] = NZ_ROCK[2]
            w.put(img, x, y)
            w.coll[y, x] = True
    # ---------------------------------------------------------------- vloer: spiegelglas
    for y in range(H):
        for x in range(W):
            if wall[y, x]:
                continue
            base = NZ_FLOOR[1] if zone(x, y) != 'altar' else C(10, 8, 18)
            img = rgba(16, 16, base)
            for yy in range(16):
                for xx in range(16):
                    d = (x * 16 + xx + (y * 16 + yy) * 2) % 64
                    if d < 2:
                        img[yy, xx, :3] = mix(base, NZ_FLOOR[3], 0.5)
                    elif d == 2:
                        img[yy, xx, :3] = NZ_FLOOR[3]
            if y > 0 and wall[y - 1, x]:
                img[0:3, :, :3] = mix(img[0:3, :, :3], C(0, 0, 0), 0.6)
            w.put(img, x, y)
            w.beh[y, x] = 0x08
    floorpix = np.zeros(w.bot.shape[:2], bool)
    for y in range(H):
        for x in range(W):
            if not wall[y, x]:
                floorpix[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = True
    # ---------------------------------------------------------------- licht: banden evenwijdig aan de glansstrepen
    # (s = X + 2Y is constant langs een streep; banden in s herhalen per (2, -1) vakken, dus weinig nieuwe tiles)
    S = w.xx + 2 * w.yy
    T = 2 * w.xx - w.yy

    def band(cx, cy, s_half, length, col, strength, amount=0.35, spot=True):
        """lichtband van (cx, cy) (pixels, onderste eind) schuin omhoog naar rechts, over de vloer"""
        s0, t0 = cx + 2 * cy, 2 * cx - cy
        f = np.clip((s_half - np.abs(S - s0)) / 3.0, 0, 1)
        f = f * np.clip((T - t0) / 24.0 + 1, 0, 1) * np.clip((t0 + length - T) / 60.0, 0, 1)
        if spot:
            f = np.maximum(f, np.clip(1 - np.hypot(w.xx - cx, (w.yy - cy) * 1.9) / (s_half * 0.75), 0, 1) * 1.0)
        w.apply(f * strength, lambda c: mix(c, col, amount), where=floorpix)
    band(4 * 16, 16 * 16, 22, 300, C(190, 225, 255), 0.95)
    band(33 * 16, 16 * 16, 20, 300, C(255, 226, 180), 0.9)
    band(15 * 16, 6 * 16, 16, 260, C(255, 255, 255), 0.6, amount=0.22)
    PR = (25, 17)                          # het grote prisma (3x4 vakken, linksboven)
    ox, oy = PR[0] * 16 + 10, (PR[1] + 3) * 16 + 4          # uittreepunt linksonder
    band(ox + 30, oy - 14, 12, 220, C(255, 255, 255), 1.0, amount=0.4, spot=False)  # witte straal van rechtsboven
    # ---------------------------------------------------------------- het grote prisma + regenboog
    pimg = crystal_cluster(3, 4, None, 21, white=True)
    draw_prism(pimg, 24, 61, 58, 14, 2, crystal_cols(None))
    s0 = ox + 2 * oy
    t0 = 2 * ox - oy
    for k in range(7):
        col = hsv(k / 7.0 * 0.8, 0.85, 1.0)
        lo, hi = s0 - 21 + k * 6, s0 - 21 + k * 6 + 6
        f = ((S >= lo) & (S < hi)).astype(float)
        f = f * (T <= t0) * np.clip((T - (t0 - 520)) / 220.0, 0, 1)
        w.apply(f, lambda c, col=col: mix(c, col, 0.42), where=floorpix)
    reflect(w, pimg, PR[0], PR[1], 0.6)
    w.put(pimg[:32], PR[0], PR[1], 'top')
    w.put(pimg[32:], PR[0], PR[1] + 2)
    for y in range(PR[1] + 2, PR[1] + 4):
        for x in range(PR[0], PR[0] + 3):
            w.coll[y, x] = True
    # ---------------------------------------------------------------- altaar: zwart glas dat het licht opslokt
    acx, acy = ub[0] * 16 + 8, ub[1] * 16 + 10
    da = np.hypot(w.xx - acx, (w.yy - acy) * 1.45)
    ang2 = np.arctan2((w.yy - acy) * 1.45, w.xx - acx)
    altar = (da < 52) & floorpix
    w.bot[altar] = C(8, 6, 14)
    spiral = altar & ((((ang2 * 3 + da / 6.0) % (2 * math.pi)) < 0.8))
    w.bot[spiral] = C(30, 16, 52)
    for r, col in ((52, NZ_ROCK[4]), (51, NZ_ROCK[1]), (36, C(70, 40, 120)), (20, C(120, 70, 200))):
        w.bot[floorpix & (np.abs(da - r) < 0.7)] = col
    w.bot[(da < 8) & floorpix] = C(0, 0, 0)
    pylons = []
    for k in range(6):
        a = math.pi * 2 * k / 6.0 + math.pi / 6
        px_, py_ = acx + math.cos(a) * 84, acy + math.sin(a) * 84 / 1.45
        cx_, cy_ = int(px_ // 16), int(py_ // 16)
        if not (1 <= cx_ < W - 1 and 1 <= cy_ < H) or wall[cy_, cx_]:
            continue
        hue = [0.0, 0.15, 0.33, 0.5, 0.66, 0.8][k]
        pylons.append((cx_, cy_, hue))
        for t in np.linspace(0.12, 0.92, 160):
            bx_, by_ = px_ + (acx - px_) * t, py_ + (acy - py_) * t
            if floorpix[int(by_), int(bx_)]:
                col = mix(hsv(hue, 0.55, 1.0), C(0, 0, 0), min(1.0, t * 1.1))
                for o in (0, 1):
                    w.bot[int(by_) + o, int(bx_)] = col if o == 0 else mix(col, C(0, 0, 0), 0.5)
    # ---------------------------------------------------------------- kristallen
    rsd = random.Random(99)
    taken = set()
    sparkle = []
    keep_free = {arrive, ret, ub, (21, 29), (20, 28), (22, 28)}
    keep_free |= {(x, y) for x in range(17, 26) for y in range(2, 10)}
    keep_free |= {(x, y) for x in range(18, 25) for y in range(22, 30)}
    keep_free |= {(x, y) for x in range(PR[0] - 1, PR[0] + 4) for y in range(PR[1] - 1, PR[1] + 5)}

    def place(img, x, y, cw, ch, on_wall_rows, block_cells):
        """img (cw x ch vakken); de onderste rij staat op vloervak-rij y; bovenste rijen op de muur = onderlaag"""
        for r in range(ch):
            yy = y - (ch - 1) + r
            for c in range(cw):
                cell = img[r * 16:(r + 1) * 16, c * 16:(c + 1) * 16]
                if r == ch - 1 or wall[yy, x + c] or r < on_wall_rows:
                    A.paste(w.bot, cell, (x + c) * 16, yy * 16)
                else:
                    w.put(cell, x + c, yy, 'top')
        reflect(w, img, x, y - (ch - 1), 0.55)
        for c in block_cells:
            w.coll[c[1], c[0]] = True
        sparkle.append((x + (cw - 1) // 2, y - 1))

    for (cx_, cy_, hue) in pylons:
        place(crystal_cluster(1, 2, hue, 7), cx_, cy_, 1, 2, 0, [(cx_, cy_)])
        taken |= {(cx_ + dx, cy_ + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    # kristalwand tussen hal en altaar: hoge clusters op de muur, voeten op de eerste vloerrij van de hal
    for x in range(12, 30, 2):
        ys = [y for y in range(14, 22) if not wall[y, x] and not wall[y, x + 1] and wall[y - 1, x] and wall[y - 1, x + 1]]
        if not ys or any((x + c, ys[0]) in keep_free for c in (0, 1)):
            continue
        y = ys[0]
        img = crystal_cluster(2, 4, HUES[(x // 2) % 8], (x // 2) % 3, white=(x in (20, 22)))
        place(img, x, y, 2, 4, 3, [(x, y), (x + 1, y)])
        taken |= {(x + dx, y + dy) for dx in (0, 1) for dy in (-1, 0, 1)}
    # geodes: kristallen die uit de rotsmassa steken (alleen tekening, in de onderlaag)
    rg = random.Random(5)
    interior = [(x, y) for y in range(2, H - 3) for x in range(1, W - 2)
                if all(wall[y + dy, x + dx] for dx in (-1, 0, 1, 2) for dy in (-1, 0, 1, 2))]
    rg.shuffle(interior)
    geodes = []
    for (x, y) in interior:
        if any(abs(x - gx) + abs(y - gy) < 5 for gx, gy in geodes):
            continue
        geodes.append((x, y))
        z = zone(x, min(y, H - 1))
        hz = ZONE_HUES[z] if z != 'altar' else ['black', 0.8]
        hue = hz[len(geodes) % len(hz)]
        img = crystal_cluster(2, 2, hue, len(geodes) % 3)          # drie vormen, per zone een paar kleuren
        cav = np.zeros((32, 32, 4))
        yy, xx = np.mgrid[0:32, 0:32]
        hole = ((xx - 16) / 14.0) ** 2 + ((yy - 21) / 10.0) ** 2 < 1
        rim = (((xx - 16) / 15.5) ** 2 + ((yy - 21) / 11.5) ** 2 < 1) & ~hole
        outer = ~hole & ~rim
        cav[..., :3] = NZ_ROCK[1]
        cav[..., 3] = 255
        cav[outer, :3] = A.ramp(np.full(outer.sum(), 0.25), NZ_ROCK[:5])
        cav[hole, :3] = C(6, 4, 12)
        cav[rim, :3] = NZ_ROCK[3]
        A.paste(cav, img, 0, -2)
        w.bot[y * 16:y * 16 + 32, x * 16:x * 16 + 32] = cav[..., :3]
        if len(geodes) >= 14:
            break
    # grote formaties tegen de wanden van de galerijen en de hal
    cand = [(x, y) for y in range(3, H - 2) for x in range(1, W - 3) if all(not wall[y, x + c] and wall[y - 1, x + c] for c in range(2))]
    rsd.shuffle(cand)
    rcount = len(reachable(w.coll, arrive, {ret}))
    for (x, y) in cand:
        cells = [(x, y), (x + 1, y)]
        if any(c in taken or c in keep_free for c in cells):
            continue
        z = zone(x, y)
        for c in cells:
            w.coll[c[1], c[0]] = True
        r = reachable(w.coll, arrive, {ret})
        if len(r) != rcount - 2 or not next_to(r, *ub):
            for c in cells:
                w.coll[c[1], c[0]] = False
            continue
        rcount -= 2
        ch = rsd.choice((3, 3, 4))
        hz = ZONE_HUES[z]
        hue = rsd.choice(hz)
        img = crystal_cluster(2, ch, hue, (x * 31 + y) % 4, white=False)
        place(img, x, y, 2, ch, ch - 1, [])
        taken |= {(x + dx, y + dy) for dx in (-1, 0, 1, 2) for dy in (-1, 0, 1)}
    # middelgrote, vrijstaande kristallen in groepjes van 2-3
    cand = [(x, y) for y in range(3, H - 2) for x in range(1, W - 1) if not wall[y, x] and not wall[y - 1, x]]
    rsd.shuffle(cand)
    groups = 0
    for (x, y) in cand:
        if groups >= 14:
            break
        grp = [(x, y)] + [(x + dx, y + dy) for dx, dy in rsd.sample([(2, 0), (-2, 0), (1, 1), (-1, 1), (2, 1)], 2)]
        ok_cells = []
        for c in grp:
            if c in taken or c in keep_free or (c[0], c[1] - 1) in keep_free:
                continue
            if not (1 <= c[0] < W - 1 and 2 <= c[1] < H - 1) or wall[c[1], c[0]] or wall[c[1] - 1, c[0]] or w.coll[c[1], c[0]]:
                continue
            w.coll[c[1], c[0]] = True
            r = reachable(w.coll, arrive, {ret})
            if len(r) != rcount - 1 or not next_to(r, *ub):
                w.coll[c[1], c[0]] = False
                continue
            rcount -= 1
            ok_cells.append(c)
        if not ok_cells:
            continue
        groups += 1
        hz = ZONE_HUES[zone(x, y)]
        hue = rsd.choice(hz)
        for c in ok_cells:
            place(crystal_cluster(1, 2, hue, (c[0] * 13 + c[1] * 7) % 4, white=False), c[0], c[1], 1, 2, 0, [])
            taken |= {(c[0] + dx, c[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    # scherven op de vloer (begaanbaar): kleine kristalletjes, dichter bij de wanden
    for y in range(2, H - 1):
        for x in range(1, W - 1):
            if wall[y, x] or w.coll[y, x] or (x, y) in keep_free or (x, y) in taken:
                continue
            nearwall = any(wall[y + dy, x + dx] for dx in (-1, 0, 1) for dy in (-1, 0, 1))
            hsh = zlib.crc32(b'shard%d,%d' % (x, y))
            if hsh % (4 if nearwall else 11):
                continue
            hz = ZONE_HUES[zone(x, y)]
            hue = hz[hsh // 7 % len(hz)]
            cols = crystal_cols(hue)
            img = np.zeros((16, 16, 4))
            rs2 = random.Random(hsh % 6)
            for _ in range(rs2.randint(1, 3)):
                draw_prism(img, rs2.randint(3, 12), rs2.randint(11, 14), rs2.randint(4, 8), rs2.choice((2, 3, 3)), rs2.uniform(-2, 2), cols)
            A.paste(w.bot, img, x * 16, y * 16)
    # ---------------------------------------------------------------- glinsteringen (animatie)
    spark_pts = {}
    for c in sparkle:
        if not (0 <= c[1] < H):
            continue
        for lay in ('top', 'bot'):
            src = w.cellpix(*c, layer='top') if lay == 'top' else np.concatenate([w.cellpix(*c), np.full((16, 16, 1), 255.0)], 2)
            if lay == 'top' and not (src[..., 3] > 127).any():
                continue
            bright = np.argwhere((src[..., 3] > 127) & (src[..., :3].sum(2) > 560))
            if len(bright):
                yx = bright[len(bright) // 3]
                spark_pts[c] = (lay, int(yx[1]), int(yx[0]))
                break

    def spark_fn(f, x, y):
        lay, sx, sy = spark_pts[(x, y)]
        img = w.cellpix(x, y, 'top').copy() if lay == 'top' else np.concatenate([w.cellpix(x, y).copy(), np.full((16, 16, 1), 255.0)], 2)
        size = [0, 1, 2, 3, 2, 1][f]
        if size:
            img[sy, sx] = [255, 255, 255, 255]
            for d in range(1, size + 1):
                for (dx, dy) in ((d, 0), (-d, 0), (0, d), (0, -d)):
                    if 0 <= sx + dx < 16 and 0 <= sy + dy < 16:
                        img[sy + dy, sx + dx] = [255, 255, 255, 255] if d < size else [190, 210, 255, 255]
            if size == 3:
                for (dx, dy) in ((1, 1), (-1, -1), (1, -1), (-1, 1)):
                    if 0 <= sx + dx < 16 and 0 <= sy + dy < 16:
                        img[sy + dy, sx + dx] = [220, 230, 255, 255]
        return img
    seqs = [[0, 1, 2, 3, 2, 1] + [0] * 14, [0] * 9 + [1, 2, 3, 2, 1] + [0] * 6, [0] * 4 + [1, 2, 3, 3, 2, 1] + [0] * 10]
    gi = 0
    for lay in ('top', 'bot'):
        cells = [c for c, v in spark_pts.items() if v[0] == lay][:21]
        for k in range(3):
            sub = cells[k::3]
            if sub:
                w.anim('spark%d' % gi, spark_fn, sub, seqs[k], 6, layer=lay)
                gi += 1
    # ---------------------------------------------------------------- objecten, items
    objs = [obj('LOCALID_ULTRA_NECROZMA_RETURN', WORM, ret[0], ret[1], 'UltraSpace_EventScript_ReturnToHub'),
            obj('LOCALID_ULTRA_NECROZMA_UB', mon('NECROZMA'), ub[0], ub[1], 'UltraSpace_Necrozma_EventScript_UB',
                'FLAG_ULTRA_NECROZMA')]
    r = reachable(w.coll, arrive, {ret, ub})
    spots = []
    for tx in (3, 39):
        c = min((c for c in r if abs(c[0] - tx) <= 5 and 10 <= c[1] <= 21), key=lambda c: abs(c[0] - tx) * 2 + abs(c[1] - 16))
        spots.append(c)
    for (fl_, it, q, h), (x, y) in zip(ni.items('UltraSpace_Necrozma'), spots):
        objs.append(obj(None, 'OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', fl_, 'MOVEMENT_TYPE_LOOK_AROUND', it, rx=q))
    npcs = [('MINIOR', 'Minior', 'MOVEMENT_TYPE_FACE_UP'), ('CARBINK', 'Carbink', 'MOVEMENT_TYPE_WANDER_AROUND'),
            ('CRYOGONAL', 'Cryogonal', 'MOVEMENT_TYPE_WANDER_AROUND')]
    targets = [(17, 21), (33, 18), (8, 17)]
    for (sp, lbl, mv), (tx, ty) in zip(npcs, targets):
        c = min((c for c in r if c not in [(o['x'], o['y']) for o in objs]), key=lambda c: abs(c[0] - tx) + abs(c[1] - ty))
        objs.append(obj(None, mon(sp), c[0], c[1], 'UltraSpace_Necrozma_EventScript_' + lbl, '0', mv,
                        rx=1 if 'WANDER' in mv else 0, ry=1 if 'WANDER' in mv else 0))
    for y in range(H):
        for x in range(W):
            if (abs(x - ub[0]) <= 5 and y <= 10) or (17 <= x <= 25 and y >= 23):
                w.beh[y, x] = 0
    texts = [('UB', 'A POKéMON made of hungry darkness,\nsucking the light out of the prisms.\\pIt wants your light. You only have a\nflashlight app and a bad attitude.'),
             ('UBBack', 'NECROZMA folds back into the dark.\nThe prisms dim. They\'re waiting for you.'),
             ('Minior', 'A MINIOR is staring into the rainbow like\na moth. A very rocky, very doomed moth.'),
             ('Carbink', 'CARBINK is admiring its reflection in the\nfloor. The floor is admiring it back.'),
             ('Cryogonal', 'CRYOGONAL spins slowly, refracting your\nface into seven slightly worse faces.')]
    return dict(world=w, objects=objs, bgs=[], arrive=arrive, ret=ret, ub=ub, species='NECROZMA', level=95,
                music='MUS_RG_SEVII_DUNGEON', weather='WEATHER_NONE', texts=texts,
                npc_scripts=[('Minior', 'MSGBOX_NPC'), ('Carbink', 'MSGBOX_NPC'), ('Cryogonal', 'MSGBOX_NPC')],
                encounters=[('CRYOGONAL', 86, 88), ('ESPEON', 86, 88), ('GLIMMORA', 87, 89), ('PORYGON_Z', 86, 88),
                            ('METAGROSS', 88, 90), ('AURORUS', 86, 88), ('GARDEVOIR', 86, 88), ('UMBREON', 86, 88),
                            ('ORBEETLE', 85, 87), ('MAGNEZONE', 87, 89), ('BAXCALIBUR', 90, 91), ('MINIOR', 84, 86)],
                rate=5)


# ====================================================================== bouwen
def build(key):
    spec = WORLDS[key]()
    w = spec['world']
    name = 'UltraSpace_' + key
    r, worst = check_spec(spec)
    if PREVIEW:
        w.preview(os.path.join(PREVIEW, name + '_canvas.png'))
    grid, info = A.emit_pair(w, ts_path(key, True), ts_path(key, False))
    out = [[grid[y][x] | ((1 if w.coll[y, x] else 0) << 10) | (int(w.elev[y, x]) << 12) for x in range(w.W)] for y in range(w.H)]
    # border: het vak dat de spec noemt (standaard: linksboven)
    bx, by = spec.get('border_cell', (0, 0))
    bt = grid[by][bx] | (1 << 10) | (3 << 12)
    lconst = save_layout(name, out, [bt] * 4, key)
    write_map_json(spec, lconst)
    write_scripts(spec)
    write_encounters(key, spec['encounters'], spec['rate'])
    update_hub(key, spec['arrive'])
    print('%s: %dx%d, %d objecten (max %d in beeld), %d tiles, %d metatiles' % (
        name, w.W, w.H, len(spec['objects']), worst, info['tiles'], info['metatiles']))
    return info


def main():
    keys = [k for k in WORLDS if ONLY is None or k in ONLY]
    results = {}
    cache = 'tools/grounded/maptools/ultra_worlds_b_anims.json'
    old = json.load(open(cache)) if os.path.exists(cache) else {}
    for k in keys:
        info = build(k)
        old[k] = info['anims']
    json.dump(old, open(cache, 'w'), indent=1)
    register_tilesets([(k, {'anims': old.get(k, [])}) for k in WORLDS if k in old])


if __name__ == '__main__':
    main()
