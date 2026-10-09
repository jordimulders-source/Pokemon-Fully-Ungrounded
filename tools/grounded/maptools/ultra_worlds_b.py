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


# ====================================================================== GUZZLORD: Lilycove, kapotgegeten
def gz_grade(rgb):
    """kleurcorrectie voor heel Lilycove: gras wordt as, water wordt donker oliewater, daken verbleekt en vuil.
    Eén vaste kleur -> kleur-functie, dus de tegelstructuur blijft gelijk (geen extra tiles)."""
    import colorsys
    flat = rgb.reshape(-1, 3)
    uniq, inv = np.unique(np.clip(flat, 0, 255).astype(int), axis=0, return_inverse=True)
    res = np.zeros((len(uniq), 3))
    for i, (r, g, b) in enumerate(uniq):
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        if 0.17 < h < 0.47 and s > 0.18:            # gras, bladeren -> grijze as / verkoold
            h, s, v = 0.08, s * 0.22, v * 0.58
        elif 0.5 < h < 0.7 and s > 0.25 and v > 0.5 and b > 150 and g > 120:   # water (licht blauw)
            h, s, v = 0.47, s * 0.45, v * 0.34
        elif 0.5 < h < 0.75:                        # blauwe daken/muren
            s, v = s * 0.55, v * 0.66
        elif h < 0.1 or h > 0.9:                    # rode daken
            s, v = s * 0.7, v * 0.66
        else:                                       # zand, steen, hout
            s, v = s * 0.55, v * 0.7
        rr, gg, bb = colorsys.hsv_to_rgb(h, s, v)
        res[i] = np.array([rr, gg, bb]) * 255 * 0.9 + np.array([48, 18, 26]) * 0.1
    return res[inv.reshape(-1)].reshape(rgb.shape)


GZ_SOOT = C(16, 12, 16)
GZ_EMBER = [C(64, 10, 6), C(150, 40, 16), C(232, 112, 32), C(248, 208, 96)]
GZ_MATS = {
    'grey': [C(22, 20, 24), C(52, 50, 56), C(82, 80, 86), C(116, 112, 116), C(150, 146, 148)],
    'blue': [C(22, 22, 32), C(46, 50, 70), C(70, 76, 102), C(98, 104, 132), C(132, 138, 160)],
    'red': [C(30, 16, 16), C(72, 34, 30), C(110, 52, 42), C(146, 80, 62), C(176, 112, 90)],
    'wood': [C(28, 20, 16), C(62, 44, 30), C(92, 66, 42), C(124, 92, 60), C(150, 120, 84)],
}


def rubble_texture(seed, mats):
    """naadloos herhalend puin (32x32): brokken van de materialen in mats, met schaduw"""
    rs = random.Random(seed)
    img = np.zeros((32, 32, 3))
    img[:] = GZ_MATS['grey'][0]
    for _ in range(70):
        m = GZ_MATS[rs.choice(mats)]
        bw, bh = rs.choice(((4, 3), (5, 3), (6, 4), (3, 3), (7, 3), (4, 4), (5, 2)))
        x0, y0 = rs.randrange(32), rs.randrange(32)
        for yy in range(bh + 1):
            for xx in range(bw + 1):
                px, py = (x0 + xx) % 32, (y0 + yy) % 32
                if yy == bh or xx == bw:
                    img[py, px] = m[0]
                elif yy == 0 or xx == 0:
                    img[py, px] = m[4] if (xx + yy) % 3 else m[3]
                else:
                    img[py, px] = m[2] if (xx * 3 + yy) % 7 else m[1]
    return img


def jag(side, i):
    """rafelige rand: hoeveel pixels de rand van een puinvak inspringt op positie i (vast patroon per kant)"""
    return [2, 3, 4, 3, 2, 1, 2, 4, 5, 4, 3, 2, 1, 2, 3, 2][(i + side * 5) % 16]


def place_rubble(w, cells, tex, block=True, emb=False):
    """puinvlak over de vakken: textuur (32x32 herhalend), rafelige randen waar het geen puin meer is"""
    cs = set(cells)
    for (x, y) in cells:
        cell = rgba(16, 16)
        cell[..., :3] = tex[(y % 2) * 16:(y % 2) * 16 + 16, (x % 2) * 16:(x % 2) * 16 + 16]
        cell[..., 3] = 255
        for side, (dx, dy) in enumerate(((0, -1), (1, 0), (0, 1), (-1, 0))):
            if (x + dx, y + dy) in cs:
                continue
            for i in range(16):
                d = jag(side, i)
                for k in range(d):
                    if side == 0:
                        cell[k, i, 3] = 0
                    elif side == 1:
                        cell[i, 15 - k, 3] = 0
                    elif side == 2:
                        cell[15 - k, i, 3] = 0
                    else:
                        cell[i, k, 3] = 0
                # schaduw net buiten de rand (onder en rechts)
                if side in (1, 2):
                    if side == 2 and d < 16:
                        cell[15 - d + 1 if d > 0 else 15, i, :3] = mix(cell[15 - d + 1 if d > 0 else 15, i, :3], GZ_SOOT, 0.3)
        # ondergrond onder de rafels: verdonkerd (stof)
        under = w.bot[y * 16:y * 16 + 16, x * 16:x * 16 + 16]
        under[:] = mix(under, C(30, 24, 26), 0.45)
        A.paste(w.bot, cell, x * 16, y * 16)
        w.top[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = 0
        w.layer[y, x] = A.COVERED
        if block:
            w.coll[y, x] = True


def heap(w, cx, cy, rx, ry, tex, seed, block=True, nz=None):
    """puinberg (pixels): grillige rand, herhalende puintextuur binnenin, lichte bovenrand, donkere voet en
    slagschaduw rechtsonder. Vakken waarvan het midden in de berg ligt worden geblokkeerd."""
    if nz is None:
        nz = A.value_noise(w.bot.shape[0], w.bot.shape[1], 5, seed)
    d = np.hypot((w.xx - cx) / rx, (w.yy - cy) / ry) - nz * 0.22
    m = d < 1
    shadow = (np.hypot((w.xx - cx - 4) / rx, (w.yy - cy - 4) / ry) - nz * 0.22 < 1.04) & ~m
    w.bot[shadow] = mix(w.bot[shadow], C(10, 8, 10), 0.5)
    texall = np.tile(tex, (w.H // 2 + 1, w.W // 2 + 1, 1))[:w.H * 16, :w.W * 16]
    w.bot[m] = texall[m]
    up = m & ~np.roll(m, 2, 0)                                 # bovenrand (2 px)
    w.bot[up] = mix(w.bot[up], C(190, 178, 166), 0.45)
    low = m & ~np.roll(m, -3, 0)                               # voet (3 px)
    w.bot[low] = mix(w.bot[low], C(8, 6, 8), 0.5)
    edge = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1))
    w.bot[edge] = C(14, 10, 12)
    w.top[m] = 0
    cells = []
    for y in range(int((cy - ry) // 16), int((cy + ry) // 16) + 1):
        for x in range(int((cx - rx) // 16), int((cx + rx) // 16) + 1):
            if 0 <= x < w.W and 0 <= y < w.H and m[y * 16 + 8, x * 16 + 8]:
                cells.append((x, y))
                w.layer[y, x] = A.COVERED
                if block:
                    w.coll[y, x] = True
    return m, cells


CRACK_PATHS = {}


def crack_piece(mask, variant, hot):
    """scheurtegel: vanuit het midden naar de randen in mask (bits N=1, E=2, S=4, W=8); rafelig, 2 varianten"""
    key = (mask, variant, hot)
    if key in CRACK_PATHS:
        return CRACK_PATHS[key]
    img = np.zeros((16, 16, 4))
    rs = random.Random(mask * 7 + variant * 101)
    mid = (8 + rs.choice((-1, 0, 1)), 8 + rs.choice((-1, 0, 1)))
    ends = {1: (8, 0), 2: (15, 8), 4: (8, 15), 8: (0, 8)}
    for bit, (ex, ey) in ends.items():
        if not mask & bit:
            continue
        x, y = mid
        pts = []
        steps = 9
        for k in range(steps + 1):
            t = k / steps
            px = mid[0] + (ex - mid[0]) * t + (rs.choice((-1, 0, 1)) if 0 < k < steps else 0)
            py = mid[1] + (ey - mid[1]) * t + (rs.choice((-1, 0, 1)) if 0 < k < steps else 0)
            pts.append((int(round(px)), int(round(py))))
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            n = max(abs(bx - ax), abs(by - ay), 1)
            for i in range(n + 1):
                qx, qy = ax + (bx - ax) * i // n, ay + (by - ay) * i // n
                if 0 <= qx < 16 and 0 <= qy < 16:
                    img[qy, qx] = list(GZ_EMBER[2] if hot else C(8, 6, 8)) + [255]
                    for (ox, oy) in ((1, 0), (0, 1)):
                        if 0 <= qx + ox < 16 and 0 <= qy + oy < 16 and img[qy + oy, qx + ox, 3] == 0:
                            img[qy + oy, qx + ox] = list(GZ_EMBER[0] if hot else C(26, 20, 22)) + [255]
    if hot:
        img[mid[1], mid[0]] = list(GZ_EMBER[3]) + [255]
    CRACK_PATHS[key] = img
    return img


def fire_frames16():
    """8 frames vuur (16x16) uit de Gen 3-vuuranimatie (graphics/battle_anims/sprites/fire.png), verkleind"""
    im = Image.open('graphics/battle_anims/sprites/fire.png')
    pal = im.getpalette()[:48]
    px = np.array(im)
    out = []
    for f in range(8):
        fr = px[f * 32:(f + 1) * 32]
        o = np.zeros((16, 16, 4))
        for y in range(16):
            for x in range(16):
                v = sorted(c for c in fr[y * 2:y * 2 + 2, x * 2:x * 2 + 2].reshape(-1) if c)
                if len(v) >= 2:
                    c = v[len(v) // 2]
                    if c == 1:
                        c = 2
                    o[y, x] = [pal[c * 3], pal[c * 3 + 1], pal[c * 3 + 2], 255]
        out.append(o)
    return out


@world
def world_guzzlord():
    X0, Y0, W, H = 7, 0, 44, 35
    w = A.World('Guzzlord', W, H, seed=446)
    bot, top, coll, beh, lay = A.render_vanilla('LilycoveCity', X0, Y0, W, H)
    w.bot[:] = gz_grade(bot)
    w.top[..., :3] = gz_grade(top[..., :3])
    w.top[..., 3] = top[..., 3]
    w.coll[:] = coll
    w.layer[:] = lay
    water = (beh == 0x15) | (beh == 0x10) | (beh == 0x11) | (beh == 0x12) | (beh == 0x17)
    for y in range(H):
        for x in range(W):
            w.beh[y, x] = beh[y, x] if 0x38 <= beh[y, x] <= 0x3F else 0      # richels houden
            if 0x60 <= beh[y, x] <= 0x6F:
                w.coll[y, x] = True                     # deuren dicht (geen warps)
            if water[y, x]:
                w.coll[y, x] = True                     # het water is giftig: niet surfen
    # bomen -> dode, verkoolde bomen (Ekat, Haunted Woods); grond eronder wordt as
    comp = bot.copy()
    A.over_rgb(comp, top)
    green = (comp[..., 1] > comp[..., 0] + 8) & (comp[..., 1] > comp[..., 2] + 8)
    gfrac = green.reshape(H, 16, W, 16).mean((1, 3))
    treecell = (gfrac > 0.45) & (coll | (top[..., 3].reshape(H, 16, W, 16).mean((1, 3)) > 60))
    grass = [(x, y) for y in range(H) for x in range(W) if gfrac[y, x] > 0.97 and not coll[y, x]]
    gx_, gy_ = grass[len(grass) // 2]
    ground = w.bot[gy_ * 16:gy_ * 16 + 16, gx_ * 16:gx_ * 16 + 16].copy()
    dead = A.load_png(EKAT + 'haunted_woods_deadtrees.png')[:, 0:16].copy()
    dmask = dead[..., 3] > 0
    gm = (dead[..., 1] > dead[..., 0] + 10) & dmask                       # grasrand onder de boom -> as
    dead[gm, :3] = mix(dead[gm, :3], C(70, 62, 58), 0.8)
    dead[dmask & ~gm, :3] = mix(dead[dmask & ~gm, :3], C(30, 22, 24), 0.45)   # verkoold
    used = set()
    for y in range(H - 1):
        for x in range(W - 1):
            blk = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
            if all(treecell[c[1], c[0]] for c in blk) and not any(c in used for c in blk):
                used |= set(blk)
                for (cx_, cy_) in blk:
                    w.bot[cy_ * 16:cy_ * 16 + 16, cx_ * 16:cx_ * 16 + 16] = ground
                    w.top[cy_ * 16:cy_ * 16 + 16, cx_ * 16:cx_ * 16 + 16] = 0
                    w.layer[cy_, cx_] = A.COVERED
                A.paste(w.bot, dead[16:], x * 16 + 8, (y + 1) * 16)
                A.paste(w.top, dead[:16], x * 16 + 8, y * 16)
                w.layer[y, x] = w.layer[y, x + 1] = A.SPLIT
                w.coll[y, x] = w.coll[y, x + 1] = False
                w.coll[y + 1, x] = w.coll[y + 1, x + 1] = True
    rect = lambda x0, y0, x1, y1: [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1)]  # noqa: E731
    TEX = {'grey': rubble_texture(1, ['grey', 'grey', 'red']), 'blue': rubble_texture(2, ['blue', 'grey', 'wood']),
           'red': rubble_texture(3, ['red', 'grey', 'wood']), 'mixed': rubble_texture(4, ['grey', 'blue', 'red', 'wood'])}

    def soot(cells, f=0.45):
        """gebouw zwartgeblakerd: vaste verdonkering per gebouw (geen ruis: geen extra tiles)"""
        for (x, y) in cells:
            sl = (slice(y * 16, y * 16 + 16), slice(x * 16, x * 16 + 16))
            w.bot[sl] = mix(w.bot[sl], GZ_SOOT, f)
            t = w.top[sl]
            m = t[..., 3] > 0
            t[m, :3] = mix(t[m, :3], GZ_SOOT, f)

    def hole(cx, cy, rx, ry, seed):
        """ingestort dak: zwart gat met lichte breukrand en een paar balken"""
        rs = random.Random(seed)
        d = np.hypot((w.xx - cx) / rx, (w.yy - cy) / ry)
        th = np.arctan2(w.yy - cy, w.xx - cx)
        d = d - 0.12 * np.sin(th * 5 + seed)
        inside = d < 1
        rim = (d >= 1) & (d < 1.16)
        for arr in (w.bot, w.top):
            if arr is w.top:
                m = inside & (arr[..., 3] > 0)
                arr[m] = 0
                m = rim & (arr[..., 3] > 0)
                arr[m, :3] = C(150, 134, 116)
            else:
                arr[inside] = C(10, 8, 10)
                arr[rim] = C(150, 134, 116)
        for k in range(3):                                   # verkoolde balken over het gat
            a = rs.uniform(-0.5, 0.5)
            y0 = cy + rs.uniform(-ry * 0.5, ry * 0.5)
            for t in np.linspace(-rx * 1.05, rx * 1.05, int(rx * 2.2)):
                px, py = int(cx + t), int(y0 + t * a)
                if 0 <= py < w.bot.shape[0] - 1 and inside[py, px]:
                    w.bot[py, px] = C(60, 44, 34)
                    w.bot[py + 1, px] = C(24, 18, 16)

    # ---------------------------------------------------------------- de krater (hier stond de Contest Hall)
    KC = (16.5, 21.5)                                       # midden in vakken
    cx, cy = KC[0] * 16, KC[1] * 16
    nzc = A.value_noise(H * 16, W * 16, 9, 77)
    dd = np.hypot(w.xx - cx, (w.yy - cy) * 1.25) - nzc * 7
    R = 84
    ctex = np.zeros((32, 32, 3))                              # kraterbodem: gebarsten aarde (herhalend)
    ctex[:] = C(40, 30, 28)
    rs = random.Random(12)
    for _ in range(30):
        x0, y0 = rs.randrange(32), rs.randrange(32)
        for k in range(rs.randint(3, 7)):
            ctex[(y0 + (k // 3)) % 32, (x0 + k) % 32] = C(22, 16, 16)
        ctex[y0 % 32, x0 % 32] = C(62, 48, 42)
    ctex_all = np.tile(ctex, (H // 2 + 1, W // 2 + 1, 1))[:H * 16, :W * 16]
    inner = dd < R
    w.bot[inner] = ctex_all[inner]
    w.top[inner] = 0

    core = np.hypot(w.xx - cx, (w.yy - cy - 4) * 1.4) < 14
    w.bot[core] = mix(w.bot[core], GZ_EMBER[1], 0.45)
    # rand: een ring van puin (de resten van de Contest Hall), met drie bressen
    ringm = (dd >= R) & (dd < R + 15)
    texall = np.tile(TEX['mixed'], (H // 2 + 1, W // 2 + 1, 1))[:H * 16, :W * 16]
    gaps = []
    for gx, gy in ((16.5, 14.2), (9.2, 23.0), (23.6, 24.2)):
        gaps.append(np.hypot(w.xx - gx * 16, w.yy - gy * 16) < 15)
    gapm = gaps[0] | gaps[1] | gaps[2]
    rm = ringm & ~gapm
    w.bot[rm] = texall[rm]
    up = rm & ~np.roll(rm, 2, 0)
    w.bot[up] = mix(w.bot[up], C(190, 178, 166), 0.4)
    low = rm & ~np.roll(rm, -3, 0)
    w.bot[low] = mix(w.bot[low], C(8, 6, 8), 0.5)
    w.top[ringm] = 0
    w.bot[ringm & gapm] = mix(w.bot[ringm & gapm], C(54, 44, 42), 0.6)
    crater_cells, rim_cells = [], []
    for y in range(H):
        for x in range(W):
            v = dd[y * 16 + 8, x * 16 + 8]
            if v < R + 15:
                w.layer[y, x] = A.COVERED
                w.coll[y, x] = False
                if v < R:
                    crater_cells.append((x, y))
                elif not gapm[y * 16 + 8, x * 16 + 8]:
                    rim_cells.append((x, y))
                    w.coll[y, x] = True
    # ---------------------------------------------------------------- warenhuis: een hap eruit
    bx, by, br = 24.6 * 16, 1.6 * 16, 60
    th = np.arctan2(w.yy - by, w.xx - bx)
    bd = np.hypot(w.xx - bx, (w.yy - by) * 1.05) - 6 * np.abs(np.sin(th * 6))      # tandvormige rand
    store = np.zeros(w.bot.shape[:2], bool)
    store[0:7 * 16, 16 * 16:25 * 16] = True
    star = np.zeros((32, 32, 3))
    star[:] = C(6, 4, 10)
    rsv = random.Random(3)
    for _ in range(8):
        sx, sy = rsv.randrange(32), rsv.randrange(32)
        star[sy, sx] = rsv.choice([C(120, 100, 150), C(200, 190, 220), C(90, 60, 110)])
    voidimg = np.tile(star, (H // 2 + 1, W // 2 + 1, 1))[:H * 16, :W * 16]
    region = (bd < br) & (w.yy < 8 * 16) & (w.xx > 15 * 16) & (w.xx < 30 * 16)
    w.bot[region] = voidimg[region]
    w.top[region] = 0
    cut = (bd >= br) & (bd < br + 4) & store
    w.bot[cut] = C(176, 160, 146)                                          # doorgebeten beton
    w.bot[(bd >= br + 1) & (bd < br + 2) & store] = C(120, 108, 100)
    w.bot[(bd >= br + 4) & (bd < br + 5) & store] = C(30, 26, 28)
    rebar = cut & (((w.xx + w.yy) % 7) == 0)
    w.bot[rebar] = C(90, 50, 40)
    for fy in (1, 3, 5):                                    # afgebeten verdiepingsvloeren steken uit
        m = region & (np.abs(w.yy - fy * 16 - 3) < 1.5) & (bd > br - 18) & (w.xx < 25 * 16)
        w.bot[m] = C(120, 110, 104)
        w.bot[np.roll(m, 2, 0) & region] = C(30, 26, 28)
    for (x, y) in rect(14, 0, 30, 8):
        if region[y * 16 + 8, x * 16 + 8]:
            w.coll[y, x] = True
            w.layer[y, x] = A.COVERED
    soot(rect(16, 0, 24, 6), 0.5)
    # ---------------------------------------------------------------- museum, huizen, PC, motel, haven
    hole(4.3 * 16, 2.0 * 16, 30, 15, 31)
    soot(rect(0, 0, 9, 7), 0.5)
    heap(w, 36.0 * 16, 5.0 * 16, 42, 34, TEX['blue'], 41)                                       # huis helemaal plat
    soot(rect(28, 2, 31, 6), 0.5)
    heap(w, 5.0 * 16, 21.0 * 16, 40, 34, TEX['blue'], 43)                                       # huis weg
    heap(w, 6.0 * 16, 11.6 * 16, 36, 22, TEX['blue'], 44)                                       # dak eraf
    soot(rect(4, 13, 7, 14), 0.5)
    soot(rect(30, 10, 34, 14), 0.5)
    hole(17.9 * 16, 12.1 * 16, 19, 13, 46)                                                     # Pokémon Center
    soot(rect(16, 11, 19, 14), 0.5)
    soot(rect(29, 20, 34, 24), 0.5)                                                           # motel: verkoold
    hole(30.6 * 16, 21.2 * 16, 24, 11, 47)
    heap(w, 34.4 * 16, 21.0 * 16, 22, 20, TEX['red'], 49)
    hole(5.8 * 16, 28.4 * 16, 24, 16, 48)                                                      # haven
    soot(rect(2, 27, 8, 32), 0.5)
    # puinbergen op straat (los, blokkerend)
    for (hx, hy, rx_, ry_, t, sd) in ((37.0, 24.0, 20, 16, 'red', 53), (21.4, 7.6, 28, 16, 'blue', 56)):
        heap(w, hx * 16, hy * 16, rx_, ry_, TEX[t], sd)
    # ---------------------------------------------------------------- gebroken pier in de haven
    for x in range(9, 17):
        if x in (12, 13):
            continue
        img = rgba(16, 16, C(88, 64, 44))
        for py in (2, 13):
            img[py, :, :3] = C(48, 34, 26)
        img[0, :, :3] = img[15, :, :3] = C(30, 22, 18)
        for px in range(0, 16, 4):
            img[3:13, px, :3] = C(64, 46, 32)
        if x == 11:
            for py in range(16):
                img[py, 9 + (py * 7) % 4:, 3] = 0               # afgebroken planken
        if x == 14:
            for py in range(16):
                img[py, :5 - (py * 5) % 3, 3] = 0
        img[..., :3] = gz_grade(img[..., :3])
        A.paste(w.bot, img, x * 16, 31 * 16)
        w.coll[31, x] = x >= 12
    for (px, py) in ((12 * 16 + 3, 31 * 16 + 5), (13 * 16 + 6, 31 * 16 + 10), (12 * 16 + 9, 32 * 16 + 2)):
        w.bot[py:py + 2, px:px + 7] = C(70, 52, 38)
        w.bot[py + 2, px:px + 7] = C(16, 20, 22)
    # ---------------------------------------------------------------- scheuren: gloeiend vanuit de krater, donker elders
    walkable = lambda c: 0 <= c[0] < W and 0 <= c[1] < H and not w.coll[c[1], c[0]] and not water[c[1], c[0]]  # noqa: E731
    groundm = np.zeros(w.bot.shape[:2], bool)
    for y in range(H):
        for x in range(W):
            if walkable((x, y)) and (x, y) not in crater_cells:
                groundm[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = True
    rs = random.Random(21)
    for k, a_ in enumerate((-1.75, -0.4, 1.0, 2.2, 2.9)):
        L = rs.uniform(50, 95)
        pts = w.crack(rs, cx + math.cos(a_) * (R + 18), cy + math.sin(a_) * (R + 18) / 1.25, a_, L, seg=(4, 8), wob=0.5, branch=0.18)
        w.paint_crack(pts, core=C(60, 12, 8), rim=lambda c: mix(c, C(0, 0, 0), 0.45), hot=GZ_EMBER[2], hot_at=0.55,
                      thick=0.45, mask=groundm)
    for (x, y) in ((33, 9), (8, 15), (30, 28)):
        pts = w.crack(rs, x * 16 + 8, y * 16 + 8, rs.uniform(0, 6.28), rs.uniform(30, 60), seg=(3, 6), branch=0.25)
        w.paint_crack(pts, core=C(10, 8, 10), rim=lambda c: mix(c, C(0, 0, 0), 0.35), mask=groundm)
    # ---------------------------------------------------------------- brandvlekken + losse rommel (begaanbaar)
    scorch = []
    for v in range(2):
        img = np.zeros((32, 32, 4))
        rsx = random.Random(v + 5)
        yy, xx = np.mgrid[0:32, 0:32]
        r = np.hypot(xx - 15.5, (yy - 15.5) * 1.3)
        th = np.arctan2(yy - 15.5, xx - 15.5)
        rr = 13 + 2.5 * np.sin(th * 5 + v) + 1.5 * np.sin(th * 11)
        core = r < rr - 4
        ring = (r < rr) & ~core & (((xx + yy) % 2) == 0)
        img[core] = list(C(14, 10, 12)) + [255]
        img[ring] = list(C(30, 22, 22)) + [255]
        for _ in range(7):                                  # stralen
            a = rsx.uniform(0, 6.28)
            for t in range(9, 16):
                px, py = int(15.5 + math.cos(a) * t), int(15.5 + math.sin(a) * t / 1.3)
                if 0 <= px < 32 and 0 <= py < 32:
                    img[py, px] = list(C(22, 16, 18)) + [255]
        scorch.append(img)
    debris_sheet = A.load_png(EKAT + 'dreamyard_debris.png')   # Ekat, Dreamyard (zie CREDITS.md)
    debris_sheet[..., :3] = gz_grade(debris_sheet[..., :3])
    debris = [debris_sheet[0:16, 0:16], debris_sheet[0:16, 16:32], debris_sheet[0:16, 32:48], debris_sheet[0:16, 48:64],
              debris_sheet[16:32, 48:64]]
    occupied = set(crater_cells) | set(rim_cells)
    for (x, y) in [(36, 9), (26, 16), (8, 26), (31, 31), (39, 20), (27, 12)]:
        if walkable((x, y)) and walkable((x + 1, y + 1)):
            A.paste(w.bot, scorch[(x + y) % 2], x * 16, y * 16)
            occupied |= {(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)}
    rs = random.Random(33)
    for k in range(60):
        x, y = rs.randrange(1, W - 1), rs.randrange(1, H - 1)
        if not walkable((x, y)) or (x, y) in occupied:
            continue
        A.paste(w.bot, debris[rs.randrange(len(debris))], x * 16, y * 16)
        occupied.add((x, y))
    # ---------------------------------------------------------------- de leegte vreet de linkerrand op
    void_cells = set()
    for y in range(H):
        depth = 1.3 + 1.3 * math.sin(y * 0.55) + 0.8 * math.sin(y * 1.7 + 1)
        if y < 8:
            depth += (8 - y) * 0.2
        for x in range(W):
            if x < depth:
                void_cells.add((x, y))
    for (x, y) in void_cells:
        sl = (slice(y * 16, y * 16 + 16), slice(x * 16, x * 16 + 16))
        w.bot[sl] = voidimg[sl]
        w.top[sl] = 0
        w.layer[y, x] = A.COVERED
        w.coll[y, x] = True
    for (x, y) in void_cells:
        if (x + 1, y) not in void_cells and x + 1 < W:          # afgebrokkelde rand: aardlagen
            for py in range(16):
                d = 2 + (py * 5 + y * 3) % 3
                for px in range(d):
                    w.bot[y * 16 + py, x * 16 + 15 - px] = [C(70, 52, 42), C(46, 34, 30), C(30, 22, 22)][(py // 3) % 3]
        if (x, y - 1) not in void_cells and y > 0:
            for px in range(16):
                for py in range(2 + (px * 3 + x) % 4):
                    w.bot[y * 16 + py, x * 16 + px] = [C(70, 52, 42), C(46, 34, 30), C(30, 22, 22)][py % 3]
    for (fx, fy) in ((0, 13), (1, 21), (0, 28), (0, 5)):        # zwevende brokken
        if (fx, fy) in void_cells:
            chunk = np.zeros((16, 16, 4))
            chunk[4:10, 3:13] = list(C(70, 64, 60)) + [255]
            chunk[4, 4:12] = list(C(110, 100, 92)) + [255]
            chunk[10:13, 5:11] = list(C(46, 34, 30)) + [255]
            chunk[13, 7:9] = list(C(30, 22, 22)) + [255]
            A.paste(w.bot, chunk, fx * 16, fy * 16)
    # ---------------------------------------------------------------- vuur (animatie) op puin en in daken
    fires = fire_frames16()
    fire_cells = [(35, 3), (5, 19), (31, 21), (6, 11), (26, 7), (22, 2), (13, 8)]
    fire_cells = [c for c in fire_cells if w.coll[c[1], c[0]]]
    base = {c: np.concatenate([w.cellpix(*c).copy(), np.full((16, 16, 1), 255.0)], 2) for c in fire_cells}

    def fire_fn(f, x, y):
        img = base[(x, y)].copy()
        A.paste(img, fires[(f + (x * 3 + y)) % 8], 0, -1)
        return img
    groups = [fire_cells[i::2] for i in range(2)]
    for gi, g in enumerate(groups):
        if g:
            w.anim('fire%d' % gi, fire_fn, g, list(range(8)), 8)
            for c in g:
                w.put(fire_fn(0, *c), *c)
    # ---------------------------------------------------------------- plekken, objecten
    arrive, ret = (38, 28), (38, 27)
    ub = (16, 21)
    for c in (arrive, ret):
        w.coll[c[1], c[0]] = False
    for y in range(H):
        for x in range(W):
            if w.coll[y, x] or water[y, x]:
                continue
            g = bot[y * 16 + 8, x * 16 + 8]
            if (g[1] > g[0] + 10 and g[1] > g[2]) or (x, y) in crater_cells:    # oude grasvelden en de krater
                w.beh[y, x] = 0x08
            if abs(x - ub[0]) <= 1 and abs(y - ub[1]) <= 1:
                w.beh[y, x] = 0
    objs = [obj('LOCALID_ULTRA_GUZZLORD_RETURN', WORM, ret[0], ret[1], 'UltraSpace_EventScript_ReturnToHub'),
            obj('LOCALID_ULTRA_GUZZLORD_UB', mon('GUZZLORD'), ub[0], ub[1], 'UltraSpace_Guzzlord_EventScript_UB',
                'FLAG_ULTRA_GUZZLORD')]
    r = reachable(w.coll, arrive, {ret, ub})
    assert next_to(r, *ub), 'Guzzlord onbereikbaar'

    def near(tx, ty):
        taken_ = {(o['x'], o['y']) for o in objs} | {arrive}
        return min((c for c in r if c not in taken_), key=lambda c: abs(c[0] - tx) + abs(c[1] - ty))
    for sp, lbl, (tx, ty), mv in (('TRUBBISH', 'Trubbish', (21, 8), 'MOVEMENT_TYPE_WANDER_AROUND'),
                                  ('GARBODOR', 'Garbodor', (35, 8), 'MOVEMENT_TYPE_FACE_DOWN'),
                                  ('MURKROW', 'Murkrow', (9, 16), 'MOVEMENT_TYPE_LOOK_AROUND'),
                                  ('MUNCHLAX', 'Munchlax', (20, 25), 'MOVEMENT_TYPE_FACE_LEFT')):
        c = near(tx, ty)
        objs.append(obj(None, mon(sp), c[0], c[1], 'UltraSpace_Guzzlord_EventScript_' + lbl, '0', mv,
                        rx=1 if 'WANDER' in mv else 0, ry=1 if 'WANDER' in mv else 0))
    c = near(27, 3)                                            # in de hap uit het warenhuis... ernaast
    for fl_, it, q, h in ni.items('UltraSpace_Guzzlord'):
        objs.append(obj(None, 'OBJ_EVENT_GFX_ITEM_BALL', c[0], c[1], 'Common_EventScript_FindItem', fl_,
                        'MOVEMENT_TYPE_LOOK_AROUND', it, rx=q))
    c = near(26, 9)
    signs = [{'type': 'sign', 'x': c[0], 'y': c[1], 'elevation': 3, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
              'script': 'UltraSpace_Guzzlord_EventScript_Sign'}]
    texts = [('UB', 'GUZZLORD is eating the horizon.\\pIt has been eating it for a while. The\nhorizon is getting nervous.'),
             ('UBBack', 'GUZZLORD burps and keeps eating.\nYou were a snack. Barely.'),
             ('Trubbish', 'TRUBBISH is going through the ruins of\nthe DEPARTMENT STORE.\\pIt found a coupon. It expired the day the\nworld ended.'),
             ('Garbodor', 'GARBODOR is sitting where a house used to\nbe. It has never felt more at home.'),
             ('Murkrow', 'MURKROW is perched on what is left of a\nstreetlight, waiting for the sequel.'),
             ('Munchlax', 'MUNCHLAX is staring at GUZZLORD with\nprofessional admiration.'),
             ('Sign', 'LILYCOVE CITY\nWhere the land ends and the sea begins.\\pSomeone has crossed it out and written:\n“WHERE THE LAND ENDS.”')]
    return dict(world=w, objects=objs, bgs=signs, arrive=arrive, ret=ret, ub=ub, species='GUZZLORD', level=90,
                music='MUS_ABANDONED_SHIP', weather='WEATHER_VOLCANIC_ASH', texts=texts,
                npc_scripts=[('Trubbish', 'MSGBOX_NPC'), ('Garbodor', 'MSGBOX_NPC'), ('Murkrow', 'MSGBOX_NPC'),
                             ('Munchlax', 'MSGBOX_NPC'), ('Sign', 'MSGBOX_SIGN')],
                border_cell=(0, 12),
                encounters=[('GARBODOR', 86, 88), ('HONCHKROW', 86, 88), ('SWALOT', 86, 88), ('MUK', 86, 88),
                            ('MANDIBUZZ', 87, 89), ('KROOKODILE', 87, 89), ('HOUNDOOM', 87, 89), ('WEEZING', 86, 88),
                            ('DUSKNOIR', 88, 90), ('BISHARP', 86, 88), ('SNORLAX', 90, 91), ('HYDREIGON', 91, 92)],
                rate=8)


# ====================================================================== BLACEPHALON: circus
BL = {
    'red': [C(70, 10, 24), C(128, 20, 36), C(184, 36, 48), C(224, 72, 72)],
    'cream': [C(132, 112, 96), C(184, 168, 140), C(224, 212, 184), C(248, 240, 216)],
    'gold': [C(96, 64, 16), C(168, 120, 32), C(232, 184, 56), C(252, 236, 140)],
    'saw': [C(120, 88, 52), C(168, 128, 80), C(200, 160, 100), C(224, 192, 132)],
    'board': [C(46, 28, 22), C(72, 44, 30), C(96, 62, 40), C(122, 82, 54)],
    'bench': [C(60, 36, 24), C(98, 64, 38), C(140, 96, 56), C(176, 130, 80)],
    'night': [C(8, 6, 18), C(16, 12, 30)],
    'blue': [C(20, 30, 80), C(40, 64, 150), C(80, 120, 210), C(150, 190, 248)],
    'purple': [C(40, 16, 60), C(84, 36, 120), C(132, 72, 180), C(196, 140, 232)],
}


def bl_stripes(img, x_px0, dark_top=0):
    """rood-witte tentbanen (8 px breed) met plooischaduw"""
    Hh, Ww = img.shape[:2]
    for xx in range(Ww):
        gx = x_px0 + xx
        band = (gx // 8) % 2
        pos = gx % 8
        ramp_ = BL['red'] if band == 0 else BL['cream']
        shade_ = 2 if pos in (2, 3, 4) else (3 if pos == 5 else (1 if pos in (0, 7) else 2))
        img[:, xx, :3] = ramp_[shade_]
    if dark_top:
        img[:dark_top, :, :3] = mix(img[:dark_top, :, :3], C(10, 4, 10), 0.55)
    return img


def bl_floorboards(x, y):
    img = rgba(16, 16, BL['board'][2])
    for yy in range(16):
        gy = y * 16 + yy
        if gy % 5 == 0:
            img[yy, :, :3] = BL['board'][0]
        elif gy % 5 == 1:
            img[yy, :, :3] = BL['board'][3]
    # naden van de planken (versprongen per rij, herhalend per 2 vakken)
    for yy in range(16):
        row = (y * 16 + yy) // 5
        sx = (row * 11) % 32
        gx0 = x * 16
        for k in (sx, sx + 32):
            if gx0 <= k < gx0 + 16 and (y * 16 + yy) % 5:
                img[yy, k - gx0, :3] = BL['board'][1]
    return img


def bl_sawdust(x, y):
    img = rgba(16, 16, BL['saw'][2])
    rs = random.Random((x % 2) * 7 + (y % 2) * 13)
    for _ in range(26):
        img[rs.randrange(16), rs.randrange(16), :3] = rs.choice((BL['saw'][1], BL['saw'][3], BL['saw'][1]))
    return img


def bl_crowd(img, y0, x_px0, seed, facing='s'):
    """rij publiek: hoofden + schouders, kleurige haren/pruiken, herhalend per 32 px"""
    HEADS = [(C(240, 196, 160), C(250, 120, 40)), (C(220, 170, 130), C(60, 40, 30)), (C(250, 220, 200), C(240, 60, 140)),
             (C(200, 150, 110), C(250, 220, 90)), (C(236, 200, 170), C(80, 180, 240)), (C(250, 250, 250), C(220, 40, 40))]
    SHIRTS = [C(70, 90, 170), C(170, 60, 70), C(80, 140, 80), C(200, 160, 60), C(120, 70, 150), C(60, 60, 70)]
    Ww = img.shape[1]
    for xx0 in range(-8, Ww + 8, 8):
        gx = x_px0 + xx0
        k = ((gx // 8) * 5 + seed) % 6
        skin, hair = HEADS[k]
        shirt = SHIRTS[(k * 2 + seed) % 6]
        cx = xx0 + 4
        for yy in range(y0, min(y0 + 11, img.shape[0])):
            for xx in range(cx - 3, cx + 4):
                if not (0 <= xx < Ww):
                    continue
                dy = yy - y0
                if dy < 6:                                         # hoofd
                    if (xx - cx) ** 2 + (dy - 3) ** 2 <= 9:
                        c = hair if dy < 3 or abs(xx - cx) == 3 else skin
                        if dy == 3 and xx in (cx - 1, cx + 1) and facing == 's':
                            c = C(20, 16, 20)                       # oogjes
                        img[yy, xx, :3] = c
                        img[yy, xx, 3] = 255
                elif abs(xx - cx) <= 3:                            # schouders
                    img[yy, xx, :3] = shirt if dy < 10 else mix(shirt, C(0, 0, 0), 0.4)
                    img[yy, xx, 3] = 255


def bl_bench_row(x, y, crowd=True, seed=0):
    """tribunerij (kijkt naar het zuiden): zitplank boven, donkere optrede, publiek"""
    img = rgba(16, 16, BL['bench'][0])
    img[8:12, :, :3] = BL['bench'][2]
    img[8, :, :3] = BL['bench'][3]
    img[11, :, :3] = BL['bench'][1]
    img[12:16, :, :3] = BL['bench'][0]
    img[0:8, :, :3] = mix(BL['bench'][0], C(0, 0, 0), 0.3)
    for xx in range(0, 16, 8):
        img[12:16, xx, :3] = C(20, 12, 10)
    if crowd:
        bl_crowd(img, 1, x * 16, seed + y)
    return img


def bl_bench_side(x, y, face, crowd=True, seed=0):
    """zijtribune (kijkt naar oost of west): verticale zitplank, publiek van opzij (alleen hoofden)"""
    img = rgba(16, 16, BL['bench'][0])
    px = 3 if face == 'e' else 9
    img[:, px:px + 4, :3] = BL['bench'][2]
    img[:, px + (0 if face == 'e' else 3), :3] = BL['bench'][3]
    if crowd:
        sub = rgba(16, 16)
        sub[...] = 0
        for k, yy in enumerate((1, 9)):
            g = ((y * 2 + k) * 5 + x + seed) % 6
            hair = [C(250, 120, 40), C(60, 40, 30), C(240, 60, 140), C(250, 220, 90), C(80, 180, 240), C(220, 40, 40)][g]
            hx = 8 if face == 'e' else 7
            for dy in range(6):
                for dx in range(-3, 4):
                    if dx * dx + (dy - 3) ** 2 <= 9:
                        c = hair if (dx < 0 if face == 'e' else dx > 0) or dy < 2 else C(236, 200, 170)
                        img[yy + dy, hx + dx, :3] = c
    return img


def bl_balloon_frames(cols, n=4):
    """trosje ballonnen (16x32) dat zachtjes op en neer deint (n frames)"""
    out = []
    for f in range(n):
        img = np.zeros((32, 16, 4))
        off = [0, 1, 1, 0][f % 4]
        for k, (bx, by, col) in enumerate(((4, 5, cols[0]), (11, 4, cols[1]), (7, 9, cols[2]))):
            by += off if k != 1 else (1 - off)
            for yy in range(-4, 5):
                for xx in range(-3, 4):
                    if (xx / 3.3) ** 2 + (yy / 4.3) ** 2 <= 1 and 0 <= by + yy < 32 and 0 <= bx + xx < 16:
                        c = col[2]
                        if xx > 0 and yy > 0:
                            c = col[1]
                        if (xx, yy) in ((-1, -2), (-2, -2), (-1, -3)):
                            c = C(255, 255, 255)
                        img[by + yy, bx + xx] = list(c) + [255]
            # touwtje naar beneden
            for yy in range(by + 5, 29):
                xx = int(round(bx + (8 - bx) * (yy - by - 5) / max(29 - by - 5, 1)))
                img[yy, xx] = [60, 50, 50, 255]
        img[28:31, 6:10] = list(C(90, 60, 40)) + [255]                    # gewichtje
        out.append(img)
    return out


@world
def world_blacephalon():
    W, H = 40, 32
    w = A.World('Blacephalon', W, H, seed=449)
    RC = (20.0, 17.0)               # midden van de piste (vakken)
    RX, RY = 7.2 * 16, 6.0 * 16
    rcx, rcy = (RC[0]) * 16, (RC[1]) * 16 + 8
    # ---------------------------------------------------------------- vloer, piste
    for y in range(H):
        for x in range(W):
            w.put(bl_floorboards(x, y), x, y)
    dr = np.hypot((w.xx - rcx) / RX, (w.yy - rcy) / RY)
    inside = dr < 1
    saw = np.zeros((32, 32, 4))
    for (sx, sy) in ((0, 0), (1, 0), (0, 1), (1, 1)):
        saw[sy * 16:sy * 16 + 16, sx * 16:sx * 16 + 16] = bl_sawdust(sx, sy)
    sawall = np.tile(saw[..., :3], (H // 2 + 1, W // 2 + 1, 1))[:H * 16, :W * 16]
    w.bot[inside] = sawall[inside]
    # pisterand: rood-witte vakken met gouden bies, schaduw naar buiten
    ang = np.arctan2((w.yy - rcy) / RY, (w.xx - rcx) / RX)
    curb = (dr >= 1) & (dr < 1.0 + 7.0 / RY)
    seg = ((ang + math.pi) / (2 * math.pi) * 28).astype(int) % 2
    w.bot[curb & (seg == 0)] = BL['red'][2]
    w.bot[curb & (seg == 1)] = BL['cream'][2]
    w.bot[curb & (dr < 1.0 + 1.6 / RY)] = BL['gold'][2]
    w.bot[curb & (dr >= 1.0 + 5.6 / RY)] = mix(w.bot[curb & (dr >= 1.0 + 5.6 / RY)], C(0, 0, 0), 0.45)
    outer_sh = (dr >= 1.0 + 7.0 / RY) & (dr < 1.0 + 9.0 / RY)
    w.bot[outer_sh] = mix(w.bot[outer_sh], C(0, 0, 0), 0.35)
    # spotlichten op het zaagsel
    for (lx, ly, lr) in ((rcx, rcy - 4, 30), (rcx - 64, rcy + 30, 18), (rcx + 66, rcy - 34, 18)):
        sp = np.hypot((w.xx - lx), (w.yy - ly) * 1.3) < lr
        w.bot[sp & inside] = mix(w.bot[sp & inside], C(255, 250, 220), 0.32)
        ring = (np.abs(np.hypot((w.xx - lx), (w.yy - ly) * 1.3) - lr) < 0.8) & inside
        w.bot[ring] = mix(w.bot[ring], C(255, 250, 220), 0.2)
    # podium in het midden: trommel met een ster
    pd = np.hypot((w.xx - rcx) / 30.0, (w.yy - rcy) / 20.0)
    pod = pd < 1
    w.bot[pod] = BL['purple'][2]
    w.bot[(pd >= 0.84) & pod] = BL['gold'][2]
    w.bot[(pd >= 0.92) & pod] = BL['gold'][1]
    side = (pd >= 1) & (pd < 1.0 + 6.0 / 20) & (w.yy > rcy)
    w.bot[side] = BL['red'][1]
    w.bot[side & (((w.xx // 4) % 2) == 0)] = BL['red'][2]
    w.bot[side & (w.yy > rcy + 24)] = C(20, 8, 16)
    # ster (gevuld, vijf punten)
    sx_, sy_ = w.xx - rcx, (w.yy - rcy) * 1.45
    sang = np.arctan2(sy_, sx_) + math.pi / 2
    sr = np.hypot(sx_, sy_)
    k5 = (sang % (2 * math.pi / 5)) / (2 * math.pi / 5)
    lim = 9 + 11 * np.abs(1 - 2 * k5) ** 1.6
    starm = (sr < lim) & pod
    w.bot[starm] = BL['gold'][2]
    w.bot[starm & (sx_ < 0)] = BL['gold'][3]
    w.bot[(sr < lim + 1) & ~starm & pod] = BL['gold'][0]
    # ---------------------------------------------------------------- tribunes
    TOP = (4, 8)                    # rijen 4-8 (kijken naar het zuiden), x 8-31
    for y in range(TOP[0], TOP[1] + 1):
        for x in range(8, 32):
            crowd = not (19 <= x <= 20)
            img = bl_bench_row(x, y, crowd, seed=3)
            if 19 <= x <= 20:                            # middenpad met trapjes
                img[:, :, :3] = BL['board'][1]
                img[::4, :, :3] = BL['board'][3]
            w.put(img, x, y)
            w.coll[y, x] = True
    for y in range(9, 27):
        for x in range(2, 8):
            if 16 <= y <= 17:
                continue
            w.put(bl_bench_side(x, y, 'e', seed=1), x, y)
            w.coll[y, x] = True
        for x in range(32, 38):
            if 16 <= y <= 17:
                continue
            w.put(bl_bench_side(x, y, 'w', seed=4), x, y)
            w.coll[y, x] = True
    for y in (8,):
        for x in list(range(2, 8)) + list(range(32, 38)):
            img = bl_bench_row(x, y, True, seed=7)
            w.put(img, x, y)
            w.coll[y, x] = True
    # ---------------------------------------------------------------- tentwanden
    for y in range(0, 4):
        for x in range(W):
            img = bl_stripes(rgba(16, 16, C(0, 0, 0)), x * 16)
            if y == 0:
                img[..., :3] = mix(img[..., :3], C(8, 4, 12), 0.55)
            elif y == 1:
                img[..., :3] = mix(img[..., :3], C(8, 4, 12), 0.3)
            w.put(img, x, y)
            w.coll[y, x] = True
    # valance met lampjes op rij 3 (animatie: looplicht)
    val_cells = [(x, 3) for x in range(W)]
    val_base = {}
    for (x, y) in val_cells:
        img = w.cellpix(x, y).copy()
        img = np.concatenate([img, np.full((16, 16, 1), 255.0)], 2)
        for xx in range(16):
            gx = x * 16 + xx
            sc = 9 + int(round(3 * math.sin(math.pi * ((gx % 16) / 16.0))))
            img[sc:16, xx, :3] = mix(img[sc:16, xx, :3], BL['red'][0], 0.0)
            img[sc - 2:sc, xx, :3] = BL['gold'][2]
            img[sc:, xx, :3] = C(30, 8, 20)
            img[sc, xx, :3] = BL['gold'][1]
        val_base[(x, y)] = img

    def bulbs_fn(f, x, y):
        img = val_base[(x, y)].copy()
        for k, bx in enumerate((3, 11)):
            on = ((x * 2 + k) % 3) == f
            c0 = BL['gold'][3] if on else BL['gold'][0]
            img[5:8, bx:bx + 3, :3] = c0
            img[6, bx + 1, :3] = C(255, 255, 255) if on else BL['gold'][1]
        return img
    for c in val_cells:
        w.put(bulbs_fn(0, *c), *c)
    w.anim('bulbs', bulbs_fn, [(0, 3), (1, 3), (2, 3)], [0, 1, 2], 10)
    for (x, y) in val_cells:
        w.anim_cell[(x, y)] = (w.anims[-1], x % 3)
    for y in range(4, H):
        for x in (0, 1, 38, 39):
            img = bl_stripes(rgba(16, 16, C(0, 0, 0)), x * 16)
            img[..., :3] = mix(img[..., :3], C(8, 4, 12), 0.5 if x in (0, 39) else 0.25)
            w.put(img, x, y)
            w.coll[y, x] = True
    for y in (30, 31):
        for x in range(W):
            if 18 <= x <= 21 and y == 30:
                continue
            img = rgba(16, 16, C(20, 8, 16))
            img[0:4 if y == 30 else 0, :, :3] = BL['red'][1]
            img[0, :, :3] = BL['gold'][2]
            w.put(img, x, y)
            w.coll[y, x] = True
    # ingang: gordijnen links en rechts van de opening
    for (x, flip) in ((17, False), (22, True)):
        img = rgba(32, 16, BL['red'][1])
        for xx in range(16):
            v = (xx * 3) % 8
            img[:, xx, :3] = BL['red'][3] if v < 2 else (BL['red'][2] if v < 5 else BL['red'][1])
        img[14:18, :, :3] = BL['gold'][2]                       # koord
        img[15, :, :3] = BL['gold'][3]
        if flip:
            img = img[:, ::-1]
        w.put(img[:16], x, 29, 'top')
        w.put(img[16:], x, 30)
        w.coll[30, x] = True
    for x in range(18, 22):
        img = rgba(16, 16, C(10, 6, 14))
        img[0:2, :, :3] = BL['board'][1]
        w.put(img, x, 30)
        w.put(img, x, 31)
        w.coll[31, x] = True
    w.coll[30, 18] = w.coll[30, 21] = True
    # ---------------------------------------------------------------- rekwisieten
    def prop(img, x, y, block_rows=1, top_rows=None):
        """plaatje (veelvoud van 16) met de onderste block_rows geblokkeerd; de rijen erboven boven de speler"""
        ch, cw = img.shape[0] // 16, img.shape[1] // 16
        tr = ch - block_rows if top_rows is None else top_rows
        for r in range(ch):
            part = img[r * 16:(r + 1) * 16]
            if r < tr:
                w.put(part, x, y + r, 'top')
            else:
                w.put(part, x, y + r)
                for c in range(cw):
                    if (part[:, c * 16:(c + 1) * 16, 3] > 0).any():
                        w.coll[y + r, x + c] = True

    # kanon (Blacephalon-thema: knallen) linksonder, gericht op de piste
    can = np.zeros((32, 48, 4))
    for t in range(36):                                            # loop: schuin omhoog naar de piste
        rad = 6 - t * 0.06
        for k in range(-7, 8):
            if abs(k) > rad:
                continue
            px, py = 10 + t, 22 - t * 0.5 + k
            r_ = (k + rad) / (2 * rad)
            col = A.ramp(np.array([0.15 + 0.8 * (1 - abs(r_ - 0.35) * 1.6)]), [C(30, 30, 50), C(70, 70, 110), C(150, 150, 200), C(230, 230, 250)])[0]
            if t % 9 in (0, 1):
                col = BL['gold'][2] if abs(k) < rad - 1 else BL['gold'][1]
            if 0 <= int(py) < 32 and 0 <= int(px) < 48:
                can[int(py), int(px)] = list(col) + [255]
    for yy in range(14, 32):                                       # wiel met spaken
        for xx in range(2, 24):
            d = math.hypot(xx - 12, yy - 24)
            if d <= 7.5:
                ring = d > 5.5
                spoke = abs((xx - 12) - (yy - 24)) < 1 or abs((xx - 12) + (yy - 24)) < 1 or xx == 12 or yy == 24
                col = BL['red'][1] if ring else (BL['gold'][2] if spoke or d < 2 else None)
                if col is not None:
                    can[yy, xx] = list(col) + [255]
    can[0:4, 42:47] = list(C(40, 36, 50)) + [255]                   # mond van de loop
    prop(can, 9, 24, 1)
    # kaartjeshuisje rechtsonder
    tb = np.zeros((48, 48, 4))
    tb[16:48, 2:46] = list(BL['red'][2]) + [255]
    for xx in range(2, 46):
        tb[16:48, xx, :3] = BL['red'][2] if (xx // 6) % 2 else BL['cream'][2]
    tb[22:34, 10:38] = list(C(30, 20, 30)) + [255]                    # loket
    tb[22, 10:38] = list(BL['gold'][2]) + [255]
    for yy in range(0, 16):                                         # puntdak
        half = int(22 * yy / 15)
        tb[yy, 24 - half:24 + half] = list(BL['red'][1] if (yy % 4) < 2 else BL['red'][3]) + [255]
    tb[0:2, 23:25] = list(BL['gold'][3]) + [255]
    tb[44:48, 2:46] = list(C(20, 10, 14)) + [255]
    prop(tb, 32, 26, 2)
    # popcornkar linksonder
    pc = np.zeros((32, 32, 4))
    pc[12:28, 4:28] = list(BL['red'][2]) + [255]
    pc[12:28, 4:28:4] = list(BL['cream'][3]) + [255]
    pc[2:12, 6:26] = list(C(200, 220, 255)) + [255]                   # glazen kast
    rsp = random.Random(4)
    for _ in range(50):
        pc[rsp.randrange(5, 12), rsp.randrange(7, 25)] = list(C(255, 248, 200)) + [255]
    pc[0:2, 5:27] = list(BL['red'][1]) + [255]
    for yy in range(27, 32):
        for xx in (8, 23):
            if (yy - 29) ** 2 <= 4:
                pc[yy, xx - 2:xx + 3] = list(C(30, 30, 30)) + [255]
    prop(pc, 4, 27, 1)
    # trapezepalen met touw en trapeze over de piste (boven de speler)
    for (px_, py_) in ((11, 16), (29, 16)):
        img = rgba(16, 16)
        img[...] = 0
        for yy in range(16):
            for xx in range(16):
                d = math.hypot(xx - 7.5, yy - 9)
                if d < 4:
                    img[yy, xx] = list(BL['cream'][2] if d < 2.5 else BL['cream'][0]) + [255]
                elif d < 6 and yy > 9:
                    img[yy, xx] = [20, 12, 12, 255]
        w.put(img, px_, py_)
        w.coll[py_, px_] = True
    for t in np.linspace(0, 1, 300):                          # touw (doorhangend)
        px = 11 * 16 + 8 + (18 * 16) * t
        py = 16 * 16 + 6 + math.sin(t * math.pi) * 22
        w.top[int(py), int(px)] = list(C(220, 200, 160)) + [255]
    for (lx, ly) in ((rcx - 40, 16 * 16 + 24), (rcx + 40, 16 * 16 + 24)):
        for t in np.linspace(0, 1, 40):                        # trapeze-stang
            w.top[int(ly + t * 10), int(lx - 10 + 20 * t)] = list(BL['gold'][2]) + [255]
    for y in range(15, 19):
        for x in range(11, 30):
            if (w.top[y * 16:y * 16 + 16, x * 16:x * 16 + 16, 3] > 0).any():
                w.layer[y, x] = A.SPLIT
    # hoepels op de grond en een brandende hoepel in de piste
    for (hx, hy, col) in ((10.5, 11.5, 'blue'), (29.5, 23.5, 'gold'), (13.4, 26.5, 'purple')):
        d = np.hypot(w.xx - hx * 16, (w.yy - hy * 16) * 1.6)
        ring = (np.abs(d - 9) < 1.6)
        w.bot[ring] = BL[col][2]
        w.bot[ring & (w.yy < hy * 16)] = BL[col][3]
    fires = fire_frames16()
    hoop_cells = [(14, 13), (15, 13)]
    base = {}
    for (x, y) in hoop_cells:
        base[(x, y)] = np.concatenate([w.cellpix(x, y).copy(), np.full((16, 16, 1), 255.0)], 2)
    hoop = np.zeros((16, 32, 4))
    for yy in range(16):
        for xx in range(32):
            d = math.hypot((xx - 15.5) / 1.0, (yy - 8) * 2.0)
            if abs(d - 12) < 1.6:
                hoop[yy, xx] = list(C(60, 50, 50)) + [255]

    def hoop_fn(f, x, y):
        img = base[(x, y)].copy()
        k = 0 if x == hoop_cells[0][0] else 1
        A.paste(img, hoop[:, k * 16:(k + 1) * 16], 0, 0)
        A.paste(img, fires[(f + k * 3) % 8], 0, -3)
        return img
    for c in hoop_cells:
        w.put(hoop_fn(0, *c), *c)
        w.coll[c[1], c[0]] = True
    w.anim('hoop', hoop_fn, hoop_cells, list(range(8)), 8)
    # ballonnen (animatie, boven de speler)
    BCOLS = [(BL['red'], BL['gold'], BL['blue']), (BL['purple'], BL['red'], BL['gold']), (BL['blue'], BL['purple'], BL['red'])]
    bal_cells = [(24, 27), (15, 27), (8, 10), (31, 10)]
    bal_frames = [bl_balloon_frames(BCOLS[i % 3]) for i in range(len(bal_cells))]
    for i, (x, y) in enumerate(bal_cells):
        w.put(bal_frames[i][0][16:], x, y)
        w.coll[y, x] = True
    top_base = {}

    def bal_fn(f, x, y):
        i = [c for c in bal_cells].index((x, y + 1))
        return bal_frames[i][f][:16].copy()
    tops = [(x, y - 1) for (x, y) in bal_cells]
    for i, (x, y) in enumerate(tops):
        w.put(bal_frames[i][0][:16], x, y, 'top')
    w.anim('balloons', bal_fn, tops, [0, 1, 2, 3], 16, layer='top')
    # spandoek boven de ingang van de piste (op de tribune)
    ban = np.zeros((16, 96, 4))
    ban[2:14, 4:92] = list(BL['purple'][1]) + [255]
    ban[2, 4:92] = list(BL['gold'][2]) + [255]
    ban[13, 4:92] = list(BL['gold'][1]) + [255]
    for k in range(9):                                   # sterretjes op het doek
        sx = 10 + k * 10
        for (dx, dy) in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            ban[8 + dy, sx + dx] = list(BL['gold'][3]) + [255]
    A.paste(w.bot, ban, 17 * 16, 9 * 16)
    # confetti op de vloer (herhalend patroon, niet in de piste)
    conf = np.zeros((32, 32, 4))
    rsc = random.Random(8)
    for _ in range(14):
        cc = rsc.choice([BL['red'][3], BL['gold'][3], BL['blue'][3], BL['purple'][3], C(120, 220, 120)])
        x0, y0 = rsc.randrange(32), rsc.randrange(32)
        conf[y0, x0] = list(cc) + [255]
        conf[y0, (x0 + 1) % 32] = list(cc) + [255]
    confall = np.tile(conf, (H // 2 + 1, W // 2 + 1, 1))[:H * 16, :W * 16]
    fl = np.zeros(w.bot.shape[:2], bool)
    for y in range(9, 30):
        for x in range(8, 32):
            if not w.coll[y, x]:
                fl[y * 16:y * 16 + 16, x * 16:x * 16 + 16] = True
    m = fl & (confall[..., 3] > 0) & (dr >= 1.0 + 9.0 / RY)
    w.bot[m] = confall[m][:, :3]
    # spotlichtbundels vanuit de bovenhoeken naar de piste (licht op vloer en tribunes)
    for (sx0, sy0) in ((3 * 16, 4 * 16), (37 * 16, 4 * 16)):
        vx, vy = rcx - sx0, rcy - sy0
        L = math.hypot(vx, vy)
        ux, uy = vx / L, vy / L
        al = (w.xx - sx0) * ux + (w.yy - sy0) * uy
        pp = np.abs((w.xx - sx0) * (-uy) + (w.yy - sy0) * ux)
        cone = (al > 0) & (al < L) & (pp < 4 + al * 0.16)
        w.apply(cone.astype(float) * 0.9, lambda c: mix(c, C(255, 250, 210), 0.18))
        lamp = np.hypot(w.xx - sx0, w.yy - sy0 - 4) < 6
        w.bot[lamp] = C(60, 60, 70)
        w.bot[np.hypot(w.xx - sx0 - ux * 3, w.yy - sy0 - 4 - uy * 3) < 3] = C(255, 250, 220)
    # vlaggetjeslijnen boven de speler
    PCOL = [BL['red'][2], BL['gold'][2], BL['blue'][2], BL['purple'][2], BL['cream'][3]]
    for (xa, ya, xb, yb, sag) in ((2 * 16, 10 * 16, 38 * 16, 10 * 16, 30), (2 * 16, 27 * 16, 38 * 16, 27 * 16, 26)):
        n = int(abs(xb - xa))
        prev = None
        for i in range(n):
            t = i / n
            px = xa + (xb - xa) * t
            py = ya + (yb - ya) * t + math.sin(t * math.pi) * sag
            w.top[int(py), int(px)] = list(C(40, 30, 30)) + [255]
            if i % 12 == 0:                                         # driehoekje
                col = PCOL[(i // 12) % 5]
                for dy in range(7):
                    for dx in range(-3 + dy // 2, 4 - (dy + 1) // 2):
                        yy, xx = int(py) + 1 + dy, int(px) + dx
                        if 0 <= yy < w.top.shape[0] and 0 <= xx < w.top.shape[1]:
                            w.top[yy, xx] = list(col if dx < 1 else mix(col, C(0, 0, 0), 0.25)) + [255]
    for y in range(H):
        for x in range(W):
            if (w.top[y * 16:y * 16 + 16, x * 16:x * 16 + 16, 3] > 0).any():
                w.layer[y, x] = A.SPLIT
    # ---------------------------------------------------------------- buiten de tent: nacht
    for y in range(H):
        for x in range(W):
            if w.coll[y, x] and (y == 0 or x in (0, 39) or y == 31):
                pass
    # ---------------------------------------------------------------- objecten
    arrive, ret = (20, 28), (20, 29)
    ub = (20, 17)
    for c in (arrive, ret):
        w.coll[c[1], c[0]] = False
    objs = [obj('LOCALID_ULTRA_BLACEPHALON_RETURN', WORM, ret[0], ret[1], 'UltraSpace_EventScript_ReturnToHub'),
            obj('LOCALID_ULTRA_BLACEPHALON_UB', mon('BLACEPHALON'), ub[0], ub[1], 'UltraSpace_Blacephalon_EventScript_UB',
                'FLAG_ULTRA_BLACEPHALON', 'MOVEMENT_TYPE_FACE_DOWN')]
    clowns = [('MR_MIME', 'MrMime', (16, 21), 'MOVEMENT_TYPE_WANDER_AROUND'),
              ('HYPNO', 'Hypno', (20, 10), 'MOVEMENT_TYPE_FACE_DOWN'),
              ('SPOINK', 'Spoink', (24, 21), 'MOVEMENT_TYPE_JOG_IN_PLACE_DOWN'),
              ('MIME_JR', 'MimeJr', (25, 14), 'MOVEMENT_TYPE_WANDER_AROUND'),
              ('GRIMMSNARL', 'Grimmsnarl', (9, 20), 'MOVEMENT_TYPE_FACE_RIGHT'),
              ('SPINDA', 'Spinda', (30, 18), 'MOVEMENT_TYPE_WANDER_AROUND')]
    r = reachable(w.coll, arrive, {ret, ub})
    for sp, lbl, (tx, ty), mv in clowns:
        taken = {(o['x'], o['y']) for o in objs} | {arrive}
        c = min((c for c in r if c not in taken), key=lambda c: abs(c[0] - tx) + abs(c[1] - ty))
        wander = 'WANDER' in mv
        objs.append(obj(None, mon(sp), c[0], c[1], 'UltraSpace_Blacephalon_EventScript_' + lbl, '0', mv,
                        rx=1 if wander else 0, ry=1 if wander else 0))
    taken = {(o['x'], o['y']) for o in objs} | {arrive}
    c = min((c for c in r if c not in taken), key=lambda c: abs(c[0] - 13) + abs(c[1] - 24))
    objs.append(obj(None, 'OBJ_EVENT_GFX_SHY_GUY_RED', c[0], c[1], 'UltraSpace_Blacephalon_EventScript_ShyGuy', '0',
                    'MOVEMENT_TYPE_WALK_SLOWLY_IN_PLACE_DOWN' if False else 'MOVEMENT_TYPE_FACE_UP'))
    bgs = [{'type': 'sign', 'x': 33, 'y': 28, 'elevation': 3, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
            'script': 'UltraSpace_Blacephalon_EventScript_Tickets'},
           {'type': 'sign', 'x': 5, 'y': 28, 'elevation': 3, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
            'script': 'UltraSpace_Blacephalon_EventScript_Popcorn'},
           {'type': 'sign', 'x': 10, 'y': 25, 'elevation': 3, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
            'script': 'UltraSpace_Blacephalon_EventScript_Cannon'}]
    # wilde Pokémon achter de schermen: op de planken langs de tribunes, niet in de piste of bij de ingang
    for y in range(9, 30):
        for x in range(8, 32):
            if not w.coll[y, x] and dr[y * 16 + 8, x * 16 + 8] > 1.12 and y < 26:
                w.beh[y, x] = 0x08
    texts = [('UB', 'BLACEPHALON juggles its own head.\\pIt drops it, on purpose, and it explodes.\nThe crowd goes wild. Your eyebrows go home.'),
             ('UBBack', 'BLACEPHALON grows a new head and takes\na bow. The crowd demands an encore.'),
             ('MrMime', 'MR. MIME is trapped in an invisible box.\\pHe built the box himself. He is very proud\nof the box.'),
             ('Hypno', 'HYPNO: LADIES AND GENTLEMEN, POKéMON OF\nALL AGES… look into the pendulum…\\pYou WILL buy popcorn. You WILL laugh at\nthe clowns. You WILL NOT ask for a refund.'),
             ('Spoink', 'SPOINK has been bouncing since the show\nstarted. The show started in 1998.'),
             ('MimeJr', 'MIME JR. is miming that it is having fun.\nConvincingly. Mostly.'),
             ('Grimmsnarl', 'GRIMMSNARL is the strongman. It is lifting\na barbell made of two smaller GRIMMSNARL.'),
             ('Spinda', 'SPINDA is doing the tightrope act.\nThere is no rope. That is the act.'),
             ('ShyGuy', 'The clown refuses to take off his mask.\\pNobody has ever seen him without it.\nIncluding him.'),
             ('Tickets', 'ADMISSION: ONE (1) HEAD.\\pBLACEPHALON BRINGS ITS OWN.'),
             ('Popcorn', 'The popcorn is free. The popcorn is\nalso slightly on fire. Those are related.'),
             ('Cannon', 'THE HUMAN CANNONBALL\n(position available)\\pPrevious applicant: BLACEPHALON\'s head.')]
    return dict(world=w, objects=objs, bgs=bgs, arrive=arrive, ret=ret, ub=ub, species='BLACEPHALON', level=90,
                music='MUS_GAME_CORNER', weather='WEATHER_NONE', texts=texts,
                npc_scripts=[(lbl, 'MSGBOX_NPC') for _, lbl, _, _ in clowns] + [('ShyGuy', 'MSGBOX_NPC'),
                                                                               ('Tickets', 'MSGBOX_SIGN'), ('Popcorn', 'MSGBOX_SIGN'),
                                                                               ('Cannon', 'MSGBOX_SIGN')],
                border_cell=(0, 0),
                encounters=[('MR_MIME', 86, 88), ('HYPNO', 86, 88), ('GRUMPIG', 86, 88), ('MAGMORTAR', 87, 89),
                            ('GRIMMSNARL', 87, 89), ('CHANDELURE', 87, 89), ('HATTERENE', 87, 89), ('WOBBUFFET', 86, 88),
                            ('SPINDA', 84, 86), ('DELPHOX', 87, 89), ('MIMIKYU', 88, 90), ('ZOROARK', 89, 90)],
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
