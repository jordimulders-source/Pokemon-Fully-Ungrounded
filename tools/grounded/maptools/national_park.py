"""Project Grounded: National Park + Ilex Forest (Spacetime Cave, post-game): Calyrex, Celebi en Eternatus.

  NationalPark          50x60, General + Rustboro. Park in de vorm van een Poke Ball: bovenste helft hoog gras,
                        onderste helft donker gazon (eigen metatile achteraan Rustboro), de horizontale band en de
                        knop van stenen tegels met de fontein in het midden, een ring van tegels eromheen (de
                        trapvorm komt van het raster), bloemen en lantaarns langs de rand, Hoenn-bomen rondom.
                        Oostkant: het poortgebouwtje (Rustboro-huisje), onderaan een gang met hekjes naar een
                        pleintje (bankjes, bloembak, bord) en het bospad naar Ilex Forest (zuidpijl-warp).
  NationalPark_Ruined   Tweede layout van dezelfde kaart (zelfde indeling + smeulende plekken): park_burnt_general /
                        park_burnt_rustboro (alleen eigen paletten: as, verkoold hout, gloeiende sintels), as-regen,
                        andere muziek. Gekozen in ON_TRANSITION (FLAG_NATIONAL_PARK_REVEALED tot ..._RESTORED).
  NationalPark_Gate     Poorthuis (layout van de Seaside Cycling Road-poort): links de uitgang naar het park,
                        rechts de zijuitgang terug naar de Spacetime Cave (warp 2/3; de scheur in de hub komt hier aan).
  IlexForest            40x48, ilex_general / ilex_petalburg (General/Petalburg met donkere, mistige paletten) +
                        WEATHER_SHADE: kronkelpaden, dwaalpaden, vijver linksboven, het schrijn (stenen Celebi-beeld)
                        in het midden met bloemen en hekjes. Bovenaan de noordpijl-warp terug naar het park.

Quest (SPACETIME_PLAN): vier trainers -> Calyrex bij de fontein toont de echte, brandende dimensie -> twee
multi battles met Calyrex (PARTNER_CALYREX) tegen schimmen -> Ilex: Celebi bij het schrijn vangen (verslagen:
Calyrex zet de tijd terug) -> Calyrex + Celebi herstellen het park -> ETERNATUS (lv 75) met omniboost
(src/battle_main.c: +1 op alle stats bij elke inzet) -> Calyrex vertrekt, FLAG_NATIONAL_PARK_DONE.
Flags FLAG_GROUNDED 700-759 (blok 'national_park' in flags.h), trainers 1090-1097, partner PARTNER_CALYREX.
Idempotent; controleert de bereikbaarheid. Gebruik: python3 tools/grounded/maptools/national_park.py [rendermap]"""
import json, math, os, re, struct, subprocess, sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beacon_dragon as bd          # zet de werkmap op de repo-root
from PIL import Image

Scr, text = bd.Scr, bd.text
warp, obj, tr, ball, sign, hidden = bd.warp, bd.obj, bd.tr, bd.ball, bd.sign, bd.hidden
GROUP = 'gMapGroup_Spacetime'


def val(mt, coll=0, elev=3):
    return mt | (coll << 10) | (elev << 12)


def const(name):
    return re.sub(r'(?<=[a-z])(?=[A-Z])', '_', name).upper()


# ====================================================================== tilesets
RUST = 'data/tilesets/secondary/rustboro'
PET = 'data/tilesets/secondary/petalburg'
RUST_VANILLA, PET_VANILLA = 0x363 - 0x200, 0x290 - 0x200      # aantal metatiles voor dit script
DARK_LAWN, PAVE_SOUTH_WARP = 0x363, 0x364                     # achteraan Rustboro
GRASS_NORTH_WARP = 0x290                                      # achteraan Petalburg
DARK_TILES = (503, 504)                                       # vrije tiles achteraan Rustboro
MB_NORTH_ARROW, MB_SOUTH_ARROW = 0x64, 0x65


def append_metatiles(ts, vanilla, new):
    mts = bytearray(open(ts + '/metatiles.bin', 'rb').read())
    att = bytearray(open(ts + '/metatile_attributes.bin', 'rb').read())
    assert len(mts) // 16 in (vanilla, vanilla + len(new)), (ts, len(mts) // 16)
    mts, att = mts[:vanilla * 16], att[:vanilla * 2]
    for ent, a in new:
        mts += struct.pack('<8H', *ent)
        att += struct.pack('<H', a)
    open(ts + '/metatiles.bin', 'wb').write(mts)
    open(ts + '/metatile_attributes.bin', 'wb').write(att)


def tilesets():
    # donker gazon: de grastiles van General (tile 2/3, palet 2) een tint donkerder (index 12->13, 13->14, 14->15)
    gen = Image.open('data/tilesets/primary/general/tiles.png')
    rust = Image.open(RUST + '/tiles.png')
    gp, rp = gen.load(), rust.load()
    remap = {12: 13, 13: 14, 14: 15}
    for src, dst in zip((2, 3), DARK_TILES):
        sx, sy = (src % (gen.width // 8)) * 8, (src // (gen.width // 8)) * 8
        dx, dy = (dst % (rust.width // 8)) * 8, (dst // (rust.width // 8)) * 8
        for y in range(8):
            for x in range(8):
                c = gp[sx + x, sy + y] & 15
                rp[dx + x, dy + y] = remap.get(c, c)
    rust.save(RUST + '/tiles.png')
    a, b = 0x200 + DARK_TILES[0], 0x200 + DARK_TILES[1]
    rm = open(RUST + '/metatiles.bin', 'rb').read()
    pave = struct.unpack_from('<8H', rm, (0x2BB - 0x200) * 16)
    append_metatiles(RUST, RUST_VANILLA, [
        ((0x2000 | a, 0x2000 | b, 0x2000 | b, 0x2000 | a, 0, 0, 0, 0), 0x0000),     # 0x363 donker gazon
        (pave, MB_SOUTH_ARROW),                                                     # 0x364 tegels + zuidpijl-warp
    ])
    gm = open('data/tilesets/primary/general/metatiles.bin', 'rb').read()
    grass = struct.unpack_from('<8H', gm, 1 * 16)
    append_metatiles(PET, PET_VANILLA, [(grass, MB_NORTH_ARROW)])                # 0x290 gras + noordpijl-warp


def lum(c):
    return 0.30 * c[0] + 0.59 * c[1] + 0.11 * c[2]


def burnt(c):
    """Park in brand: groen -> as en verkoold hout, rood/geel -> gloeiende sintels, de rest grauw en warm."""
    r, g, b = c
    L = lum(c)
    if g > r + 12 and g >= b - 10:                      # gras, bladeren
        out = (L * 0.42 + 34, L * 0.36 + 26, L * 0.32 + 24)
    elif r > g + 30 and r > b + 30:                     # bloemen, daken
        out = (min(248, r + 30), g * 0.45 + 20, b * 0.2)
    elif b > r + 30 and b > g:                          # water: troebel
        out = (L * 0.45 + 30, L * 0.42 + 26, L * 0.45 + 30)
    else:
        out = (L * 0.70 + 20, L * 0.62 + 14, L * 0.55 + 10)
    return tuple(max(0, min(248, int(v) // 8 * 8)) for v in out)


def ilex(c):
    """Ilex Forest: donker, koel blauwgroen, een beetje mistig (minder contrast), bloemen houden wat kleur."""
    r, g, b = c
    L = lum(c)
    if r > g + 70 and r > b + 40:                        # bloemen: gedempt roze
        out = (r * 0.62 + 18, g * 0.45 + 18, b * 0.6 + 30)
    else:
        out = (r * 0.30 + L * 0.18 + 14, g * 0.46 + L * 0.12 + 18, b * 0.46 + L * 0.16 + 34)
    return tuple(max(0, min(248, int(v) // 8 * 8)) for v in out)


PAL_SETS = [  # (map, BASE, transform, symbol, primary?)
    ('primary/park_burnt_general', 'general', burnt, 'ParkBurntGeneral', True),
    ('secondary/park_burnt_rustboro', 'rustboro', burnt, 'ParkBurntRustboro', False),
    ('primary/ilex_general', 'general', ilex, 'IlexGeneral', True),
    ('secondary/ilex_petalburg', 'petalburg', ilex, 'IlexPetalburg', False),
]
BASES = {'general': ('General', 'InitTilesetAnim_General'), 'rustboro': ('Rustboro', 'InitTilesetAnim_Rustboro'),
         'petalburg': ('Petalburg', 'InitTilesetAnim_Petalburg')}


def palettes():
    gh = open('src/data/tilesets/graphics.h').read()
    hh = open('src/data/tilesets/headers.h').read()
    for path, base, fn, sym, prim in PAL_SETS:
        dst = 'data/tilesets/' + path
        src = 'data/tilesets/%s/%s' % ('primary' if prim else 'secondary', base)
        os.makedirs(dst + '/palettes', exist_ok=True)
        open(dst + '/BASE', 'w').write(base + '\n')
        for i in range(16):
            lines = open('%s/palettes/%02d.pal' % (src, i)).read().split('\n')
            cols = [tuple(map(int, l.split())) for l in lines[3:19]]
            cols = [cols[0]] + [fn(c) for c in cols[1:]]
            with open('%s/palettes/%02d.pal' % (dst, i), 'w', newline='\r\n') as fp:
                fp.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in cols))
        if 'gTilesetPalettes_%s[]' % sym not in gh:
            blk = '\n// Project Grounded: National Park / Ilex Forest (tools/grounded/maptools/national_park.py)\n' \
                  'const u16 gTilesetPalettes_%s[][16] =\n{\n' % sym + \
                  ''.join('    INCBIN_U16("%s/palettes/%02d.gbapal"),\n' % (dst, i) for i in range(16)) + '};\n'
            gh = gh.rstrip('\n') + '\n' + blk
        B, cb = BASES[base]
        if 'gTileset_%s =' % sym not in hh:
            hh = hh.rstrip('\n') + '\n\n// Project Grounded: National Park / Ilex Forest, tiles en metatiles van %s met eigen ' \
                 'paletten (tools/grounded/maptools/national_park.py)\nconst struct Tileset gTileset_%s =\n{\n' \
                 '    .isCompressed = TRUE,\n    .isSecondary = %s,\n    .tiles = gTilesetTiles_%s,\n' \
                 '    .palettes = gTilesetPalettes_%s,\n    .metatiles = gMetatiles_%s,\n' \
                 '    .metatileAttributes = gMetatileAttributes_%s,\n    .callback = %s,\n};\n' % (
                     B, sym, 'FALSE' if prim else 'TRUE', B, sym, B, B, cb)
    open('src/data/tilesets/graphics.h', 'w').write(gh)
    open('src/data/tilesets/headers.h', 'w').write(hh)


# ====================================================================== bomen (Hoenn-bos op een raster van 2x2-cellen)
def forest(M, cell, CW, CH, bottom_open=()):
    """Zet 2x2-bomen op elke 'T'-cel; een open cel boven een boom krijgt de kruin in zijn onderste rij."""
    for cy in range(CH):
        for cx in range(CW):
            if cell(cx, cy) != 'T':
                continue
            x, y = cx * 2, cy * 2
            Lf, R = cell(cx - 1, cy) == 'T', cell(cx + 1, cy) == 'T'
            B = cell(cx, cy + 1) == 'T' and (cx, cy) not in bottom_open
            M[y][x] = val(0x1D4 if Lf else 0x1D6, 1, 0); M[y][x + 1] = val(0x1D5 if R else 0x1D7, 1, 0)
            if B:
                M[y + 1][x] = val(0x1DC, 1, 0); M[y + 1][x + 1] = val(0x1DD, 1, 0)
            else:
                M[y + 1][x] = val(0x1E4 if Lf else 0x1E6, 1, 0); M[y + 1][x + 1] = val(0x1E5 if R else 0x1E7, 1, 0)
            if cy > 0 and cell(cx, cy - 1) != 'T':
                M[y - 1][x] = val(0x1CE, 0, 3); M[y - 1][x + 1] = val(0x1CF, 0, 3)


BORDER = [val(0x1D4, 1, 0), val(0x1D5, 1, 0), val(0x1DC, 1, 0), val(0x1DD, 1, 0)]


def save_layout(name, W, H, M, prim, sec, layout_dir=None):
    d = layout_dir or name
    os.makedirs('data/layouts/' + d, exist_ok=True)
    if layout_dir is None:
        open('data/layouts/%s/map.bin' % d, 'wb').write(struct.pack('<%dH' % (W * H), *[v for r in M for v in r]))
        open('data/layouts/%s/border.bin' % d, 'wb').write(struct.pack('<4H', *BORDER))
    lj = open('data/layouts/layouts.json').read()
    c = const(name)
    entry = '''    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "%s",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (c, name, W, H, prim, sec, d, d)
    if '"LAYOUT_%s"' % c in lj:
        i = lj.index('"id": "LAYOUT_%s"' % c); s = lj.rindex('    {', 0, i); e = lj.index('    }', i) + 5
        lj = lj[:s] + entry + lj[e:]
    else:
        i = lj.rindex('    }\n  ]')
        lj = lj[:i + 5] + ',\n' + entry + lj[i + 5:]
    json.loads(lj)
    open('data/layouts/layouts.json', 'w').write(lj)
    return 'LAYOUT_' + c


def register_map(name):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        i = g.index('"%s": [' % GROUP); j = g.index('\n  ]', i)
        g = g[:j] + ',\n    "%s"' % name + g[j:]
    d = json.loads(g)
    assert len(d[GROUP]) <= 128
    open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/SpacetimeCave/scripts.inc"\n'
        assert anchor in es
        es = es.replace(anchor, anchor + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


def write_map(name, layout, objs, warps, bgs, coords=(), **kw):
    m = {'id': 'MAP_' + const(name), 'name': name, 'layout': layout, 'music': 'MUS_RG_CELADON',
         'region_map_section': 'MAPSEC_NATIONAL_PARK', 'requires_flash': False, 'weather': 'WEATHER_NONE',
         'map_type': 'MAP_TYPE_ROUTE', 'allow_cycling': True, 'allow_escaping': False, 'allow_running': True,
         'show_map_name': True, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
         'object_events': objs, 'warp_events': warps, 'coord_events': list(coords), 'bg_events': bgs}
    m.update(kw)
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    register_map(name)


def lid(o, name):
    o['local_id'] = name
    return o


# ====================================================================== National Park
PW, PH = 50, 60
CX, CY = 22, 22                     # midden van de fontein
GATE_HOUSE = (42, 17)               # linksboven van het huisje (5x5), deur op (44, 21)
GATE_DOOR = (44, 21)
TUNNEL = (22, 23)                   # x van het bospad naar Ilex (onderaan)
LAMP_TOP, LAMP_POST = 0x212, 0x21A
PAVE, GRASS, TALL, FLOWER, SIGN_MT = 0x2BB, 0x001, 0x00D, 0x004, 0x003
FOUNTAIN = [[0x338, 0x339, 0x33A], [0x340, 0x341, 0x342], [0x348, 0x349, 0x34A]]
BENCH = (0x346, 0x347)
PLANTER = 0x307                     # Rustboro: struik in een plantenbak
FENCE_H = (0x148, 0x149, 0x14A)     # General: hekje met paaltjes (links, midden, rechts)
FENCE_L, FENCE_R = 0x142, 0x140     # paaltjes aan de linker-/rechterkant van een pad


def d0(x, y):
    return math.hypot(x - CX, y - CY)


def park_cell(cx, cy):
    if not (0 <= cx < PW // 2 and 0 <= cy < PH // 2):
        return 'T'
    x, y = cx * 2 + 0.5, cy * 2 + 0.5
    if cx == 0 or cx == PW // 2 - 1 or cy == 0:
        return 'T'
    if d0(x, y) < 18.3:                         # bal + minstens een rij gazon/bloemen voor de bomen
        return '.'
    if 17 <= cx <= 23 and 8 <= cy <= 11:        # pad naar en plek voor het poorthuisje
        return '.'
    if 10 <= cx <= 12 and 19 <= cy <= 21:       # gang naar het plein
        return '.'
    if 6 <= cx <= 16 and 22 <= cy <= 26:        # plein
        return '.'
    if cx == 11 and cy >= 27:                   # bospad naar Ilex
        return '.'
    return 'T'


def build_park():
    W, H = PW, PH
    M = [[val(GRASS) for _ in range(W)] for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if park_cell(x // 2, y // 2) == 'T':
                continue
            d = d0(x, y)
            if d < 13.5:
                if abs(x - CX) <= 1 and abs(y - CY) <= 1:
                    M[y][x] = val(FOUNTAIN[y - CY + 1][x - CX + 1], 1)
                elif abs(y - CY) <= 1 or d < 3.7:
                    M[y][x] = val(PAVE)
                elif y < CY:
                    M[y][x] = val(TALL)
                else:
                    M[y][x] = val(DARK_LAWN)
            elif d < 15.5:
                M[y][x] = val(PAVE)
            elif d < 16.5 and d0(x, y) and park_cell(x // 2, y // 2) == '.':
                M[y][x] = val(FLOWER)
    # pad van de ring naar het poorthuisje (rij 22-23) en het huisje zelf (Rustboro-huis, x 28-32, y 24-28)
    for x in range(36, 47):
        M[22][x] = val(PAVE)
    for y in range(16, 22):
        for x in range(40, 48):
            M[y][x] = val(GRASS)
    rw = 40
    rb = open('data/layouts/RustboroCity/map.bin', 'rb').read()
    for j in range(5):
        for i in range(5):
            M[GATE_HOUSE[1] + j][GATE_HOUSE[0] + i] = struct.unpack_from('<H', rb, ((24 + j) * rw + 28 + i) * 2)[0]
    assert M[GATE_DOOR[1]][GATE_DOOR[0]] & 0x3FF == 0x21F
    # gang (x 20-25, y 38-45): tegelpad 22-23 tussen hekjes, bloemen erbuiten
    for y in range(38, 46):
        if park_cell(10, y // 2) != '.':
            continue
        for x in range(20, 26):
            if d0(x, y) < 16.5:
                continue
            M[y][x] = val(PAVE) if x in (22, 23) else val(FLOWER) if x in (20, 25) else \
                val(FENCE_L if x == 21 else FENCE_R, 1)
    # plein (x 12-33, y 44-53): tegels met een gazonrand, hekjes bovenaan, bankjes, bloembak, bord
    for y in range(44, 54):
        for x in range(12, 34):
            if x in (22, 23) and y < 46:
                continue
            M[y][x] = val(PAVE) if 14 <= x <= 31 and 46 <= y <= 51 else val(GRASS)
    for x0, x1 in ((12, 21), (24, 33)):
        for x in range(x0, x1 + 1):
            M[44][x] = val(FENCE_H[0] if x == x0 else FENCE_H[2] if x == x1 else FENCE_H[1], 1)
    for x in (13, 32):
        for y in (45, 52):
            M[y][x] = val(FLOWER)
    for bx, by in ((16, 47), (28, 47), (16, 50), (28, 50)):
        M[by][bx] = val(BENCH[0], 1); M[by][bx + 1] = val(BENCH[1], 1)
    for x in (20, 25):
        M[49][x] = val(PLANTER, 1)
    for x in (19, 21, 24, 26):
        M[49][x] = val(FLOWER)
    # bospad naar Ilex: tegels, de onderste rij is de zuidpijl-warp
    for y in range(54, H):
        for x in TUNNEL:
            M[y][x] = val(PAVE_SOUTH_WARP if y == H - 1 else PAVE)
    # lantaarns: op de buitenste helft van de ring (8 richtingen) en langs het plein
    lamps = []
    for deg in (35, 145, 215, 325):
        a = math.radians(deg)
        best = None
        for y in range(H):
            for x in range(W):
                if 14.5 <= d0(x, y) < 15.5 and 14.5 <= d0(x, y - 1) < 15.5 and M[y][x] & 0x3FF == PAVE \
                        and M[y - 1][x] & 0x3FF == PAVE:
                    e = abs(math.atan2(y - CY, x - CX) - math.atan2(math.sin(a), math.cos(a)))
                    e = min(e, 2 * math.pi - e)
                    if best is None or e < best[0]:
                        best = (e, x, y)
        lamps.append(best[1:])
    lamps += [(14, 47), (31, 47), (14, 51), (31, 51)]
    for lx, ly in lamps:
        M[ly - 1][lx] = val(LAMP_TOP)
        M[ly][lx] = val(LAMP_POST, 1)
    forest(M, park_cell, PW // 2, PH // 2)
    return M


# ====================================================================== Ilex Forest
IPLAN = [
    "TTTTTTTTTT.TTTTTTTTT",
    "TTTTTTTT...TTTTTTTTT",
    "TT.....T.TTTTT...TTT",
    "TT.www...TTTT..L.TTT",
    "TT.www.TTTT...LL.TTT",
    "TT.....TTT..TTTT..TT",
    "TTTT.TTTT..TTTTTT.TT",
    "TTTT.TTT..TTTT....TT",
    "TT...TTT.TTTT..TTTTT",
    "TT.LLTT...TTT.TTTTTT",
    "TT.LLT..ffff.T..TTTT",
    "TTT..T.fSSSSf.T.L.TT",
    "TTTT...fSSSSf..LL.TT",
    "TTTTTT.ffffff.TT..TT",
    "TTT....TT..TTTTTT.TT",
    "TT..TTTTT.TTT.....TT",
    "TT.LLTTT...T..LLTTTT",
    "TT.LL.TTTT....LLT.TT",
    "TTT...TTTTTTT.TT..TT",
    "TTTTT.TT...TT....TTT",
    "TT....TT.L.TTTTT.TTT",
    "TT.TTTTT.L.TTT...TTT",
    "TT.......TTTTT.TTTTT",
    "TTTTTTTTTTTTTTTTTTTT",
]
ICW, ICH = len(IPLAN[0]), len(IPLAN)
assert all(len(r) == ICW for r in IPLAN)
IW, IH = ICW * 2, ICH * 2
ILEX_ENTRY = (20, 21)               # noordpijl-warps in rij 0
SHRINE = (20, 24)                   # sokkel van het Celebi-beeld
CELEBI = (21, 25)                    # verschijnt naast de speler, die voor het schrijn staat


def ilex_cell(cx, cy):
    if not (0 <= cx < ICW and 0 <= cy < ICH):
        return 'T'
    return IPLAN[cy][cx]


def build_ilex():
    W, H = IW, IH
    M = [[val(GRASS) for _ in range(W)] for _ in range(H)]
    kind = lambda x, y: ilex_cell(x // 2, y // 2)
    for y in range(H):
        for x in range(W):
            k = kind(x, y)
            if k == 'L':
                M[y][x] = val(TALL)
            elif k == 'f':
                M[y][x] = val(FLOWER)
            elif k == 'w':
                up, lf, rt = kind(x, y - 1) != 'w', kind(x - 1, y) != 'w', kind(x + 1, y) != 'w'
                ul, ur = kind(x - 1, y - 1) != 'w', kind(x + 1, y - 1) != 'w'
                assert kind(x, y + 1) != 'T', 'vijver tegen bomen'
                mt = (0xB0 if lf else 0xB2 if rt else 0xB1) if up else 0xB8 if lf else 0xBA if rt else \
                    0xC0 if ul else 0xC2 if ur else 0xA1
                M[y][x] = val(mt, 0, 1)
            elif kind(x, y - 1) == 'w':
                M[y][x] = val(0x002)
    # hekjes aan de bovenkant van het schrijnplein (bloemenrij 20), pad naar het schrijn open (x 20-21 boven)
    for x in range(16, 26):
        if x in (20, 21):
            continue
        M[20][x] = val(FENCE_H[0] if x in (16, 22) else FENCE_H[2] if x in (19, 25) else FENCE_H[1], 1)
    for x in ILEX_ENTRY:
        M[0][x] = val(GRASS_NORTH_WARP)
    forest(M, ilex_cell, ICW, ICH)
    return M


# ====================================================================== bereikbaarheid
def reach(M, W, H, start, blocked_extra=()):
    seen = {start}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p in seen or not (0 <= p[0] < W and 0 <= p[1] < H) or p in blocked_extra:
                continue
            v = M[p[1]][p[0]]
            if v & 0xC00 or (v >> 12) not in (0, 3):
                continue
            seen.add(p)
            q.append(p)
    return seen


def adj(r, p):
    return any((p[0] + dx, p[1] + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


# ====================================================================== flags (FLAG_GROUNDED 700-759)
FLAGS = [
    (700, 'FLAG_NATIONAL_PARK_REVEALED', 'National Park: Calyrex heeft de illusie opgeheven (brandend park)'),
    (701, 'FLAG_NATIONAL_PARK_CELEBI_DONE', 'Ilex Forest: Celebi gevangen'),
    (702, 'FLAG_NATIONAL_PARK_RESTORED', 'National Park: Celebi heeft het park hersteld (Eternatus verschijnt)'),
    (703, 'FLAG_NATIONAL_PARK_DONE', 'Spacetime-sidequest klaar: Eternatus gevangen/verslagen, Calyrex vertrokken'),
    (704, 'FLAG_NATIONAL_PARK_SCENE_PENDING', 'National Park: tekst na de schermwissel nog tonen (eenmalig)'),
    (705, 'FLAG_ITEM_NATIONAL_PARK_SILVER_POWDER', 'National Park: Silver Powder'),
    (706, 'FLAG_ITEM_NATIONAL_PARK_SUN_STONE', 'National Park: Sun Stone'),
    (707, 'FLAG_HIDDEN_ITEM_NATIONAL_PARK_BIG_NUGGET', 'National Park: verborgen Big Nugget'),
    (708, 'FLAG_ITEM_ILEX_FOREST_REVIVAL_HERB', 'Ilex Forest: Revival Herb'),
    (709, 'FLAG_ITEM_ILEX_FOREST_BOTTLE_CAP', 'Ilex Forest: Bottle Cap'),
    (710, 'FLAG_HIDDEN_ITEM_ILEX_FOREST_RARE_CANDY', 'Ilex Forest: verborgen Rare Candy'),
    (711, 'FLAG_ITEM_ILEX_FOREST_MIRACLE_SEED', 'Ilex Forest: Miracle Seed (dwaalpad)'),
]


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// national_park { (tools/grounded/maptools/national_park.py; FLAG_GROUNDED 700-759, %d-759 nog vrij)\n' % (
        max(n for n, *_ in FLAGS) + 1)
    for n, name, why in FLAGS:
        assert 700 <= n <= 759
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// national_park {' in s:
        i = s.index('// national_park {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// mega_forest {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


# ====================================================================== mapsecs
MAPSECS = [('MAPSEC_NATIONAL_PARK', 'NATIONAL PARK', 'MAPPOPUP_THEME_WOOD', 'National Park (Spacetime Cave)'),
           ('MAPSEC_ILEX_FOREST', 'ILEX FOREST', 'MAPPOPUP_THEME_WOOD', 'Ilex Forest (Spacetime Cave)')]


def mapsecs():
    p = 'src/data/region_map/region_map_sections.json'
    s = open(p).read()
    for mid, nm, theme, why in MAPSECS:
        if '"%s"' % mid not in s:
            i = s.rindex('    }\n  ]')
            s = s[:i + 5] + ',\n    {\n      "id": "%s",\n      "name": "%s"\n    }' % (mid, nm) + s[i + 5:]
    json.loads(s)
    open(p, 'w').write(s)
    p = 'src/map_name_popup.c'
    s = open(p).read()
    a = '    [MAPSEC_SPACETIME_CAVE - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_STONE, // Project Grounded: Spacetime Cave\n'
    b = '    [MAPSEC_SPACETIME_CAVE - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: Spacetime Cave\n'
    assert a in s and b in s
    for mid, nm, theme, why in reversed(MAPSECS):
        if '[%s - KANTO' % mid in s:
            continue
        s = s.replace(a, a + '    [%s - KANTO_MAPSEC_COUNT] = %s, // Project Grounded: %s\n' % (mid, theme, why), 1)
        s = s.replace(b, b + '    [%s - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT, // Project Grounded: %s\n' % (mid, why), 1)
    open(p, 'w').write(s)


# ====================================================================== wilde Pokemon
WILD = {
    'NATIONAL_PARK': dict(land=(20, [
        ('BUTTERFREE', 60, 64), ('BEEDRILL', 60, 64), ('KRICKETUNE', 61, 65), ('LEDIAN', 61, 65), ('VENOMOTH', 61, 65),
        ('SUNFLORA', 61, 65), ('PARASECT', 62, 66), ('VIVILLON', 62, 66), ('RIBOMBEE', 63, 66), ('PINSIR', 63, 67),
        ('SCYTHER', 64, 68), ('HERACROSS', 64, 68)])),
    'ILEX_FOREST': dict(land=(15, [
        ('NOCTOWL', 60, 64), ('ARIADOS', 60, 64), ('AMOONGUSS', 61, 65), ('SHIINOTIC', 61, 65), ('BRELOOM', 61, 65),
        ('VILEPLUME', 61, 65), ('FORRETRESS', 62, 66), ('TREVENANT', 62, 66), ('MISMAGIUS', 63, 67), ('ZOROARK', 63, 67),
        ('FARFETCHD', 64, 68), ('SUDOWOODO', 64, 68)])),
}


# ====================================================================== trainers
IV = bd.IV
AI, AI_BOSS = bd.AI, bd.AI_BOSS
mon = bd.mon
# (sleutel, id, naam, klasse, pic, geslacht, muziek, ai, team, waarom)
TRAINERS = [
    ('NP_BUG_CATCHER_DOUGLAS', 1090, 'DOUGLAS', 'Bug Catcher', 'Bug Catcher', 'Male', 'Male', AI, [
        mon('Vespiquen', 67, ['Attack Order', 'Defend Order', 'Heal Order', 'Air Slash']),
        mon('Lokix', 67, ['First Impression', 'Sucker Punch', 'Leech Life', 'Axe Kick']),
        mon('Escavalier', 67, ['Megahorn', 'Iron Head', 'Drill Run', 'Swords Dance']),
        mon('Frosmoth', 68, ['Quiver Dance', 'Bug Buzz', 'Ice Beam', 'Giga Drain'])], 'National Park, insectenwedstrijd'),
    ('NP_PICNICKER_SIENNA', 1091, 'SIENNA', 'Picnicker', 'Picnicker', 'Female', 'Girl', AI, [
        mon('Arboliva', 67, ['Hyper Voice', 'Energy Ball', 'Earth Power', 'Leech Seed']),
        mon('Dachsbun', 67, ['Body Press', 'Play Rough', 'Wish', 'Protect']),
        mon('Sawsbuck', 67, ['Horn Leech', 'Double-Edge', 'Jump Kick', 'Swords Dance']),
        mon('Lurantis', 68, ['Solar Blade', 'Leaf Blade', 'X-Scissor', 'Sunny Day'])], 'National Park, picknick'),
    ('NP_GENTLEMAN_WALDORF', 1092, 'WALDORF', 'Gentleman', 'Gentleman', 'Male', 'Rich', AI, [
        mon('Furfrou', 68, ['Return', 'Sucker Punch', 'U-turn', 'Cotton Guard']),
        mon('Mr. Rime', 68, ['Freeze-Dry', 'Psychic', 'Rapid Spin', 'Focus Blast']),
        mon('Stoutland', 68, ['Return', 'Crunch', 'Play Rough', 'Wild Charge']),
        mon('Kleavor', 69, ['Stone Axe', 'X-Scissor', 'Close Combat', 'Swords Dance'])], 'National Park, wandelt met zijn wandelstok'),
    ('NP_AROMA_LADY_PETUNIA', 1093, 'PETUNIA', 'Aroma Lady', 'Aroma Lady', 'Female', 'Female', AI, [
        mon('Florges', 68, ['Moonblast', 'Psychic', 'Synthesis', 'Calm Mind']),
        mon('Comfey', 68, ['Draining Kiss', 'Giga Drain', 'Floral Healing', 'Calm Mind']),
        mon('Roserade', 68, ['Sludge Bomb', 'Leaf Storm', 'Shadow Ball', 'Toxic Spikes']),
        mon('Meganium', 69, ['Petal Blizzard', 'Earthquake', 'Body Slam', 'Synthesis'])], 'National Park, ruikt aan alles'),
    # schimmen in het brandende park (multi battles met Calyrex): klasse SHADOW
    ('NP_SHADOW_ASH', 1094, 'ASH', 'Shadow Triad', 'Shadow Triad', 'Male', 'Suspicious', AI, [
        mon('Houndoom', 70, ['Fire Blast', 'Dark Pulse', 'Sludge Bomb', 'Nasty Plot']),
        mon('Golurk', 70, ['Poltergeist', 'High Horsepower', 'Ice Punch', 'Rock Slide'])], 'brandend park, schim'),
    ('NP_SHADOW_CINDER', 1095, 'CINDER', 'Shadow Triad', 'Shadow Triad', 'Male', 'Suspicious', AI, [
        mon('Ceruledge', 70, ['Bitter Blade', 'Shadow Sneak', 'Poltergeist', 'Swords Dance']),
        mon('Weezing-Galar', 70, ['Strange Steam', 'Sludge Bomb', 'Will-O-Wisp', 'Fire Blast'])], 'brandend park, schim'),
    ('NP_SHADOW_EMBER', 1096, 'EMBER', 'Shadow Triad', 'Shadow Triad', 'Male', 'Suspicious', AI, [
        mon('Chandelure', 71, ['Shadow Ball', 'Flamethrower', 'Energy Ball', 'Will-O-Wisp']),
        mon('Drapion', 71, ['Knock Off', 'Poison Jab', 'Earthquake', 'Swords Dance'])], 'brandend park, schim'),
    ('NP_SHADOW_SOOT', 1097, 'SOOT', 'Shadow Triad', 'Shadow Triad', 'Male', 'Suspicious', AI, [
        mon('Dusknoir', 71, ['Shadow Punch', 'Earthquake', 'Ice Punch', 'Trick Room']),
        mon('Salazzle', 71, ['Sludge Wave', 'Flamethrower', 'Dragon Pulse', 'Nasty Plot'])], 'brandend park, schim'),
]


def trainers():
    p = 'include/constants/opponents.h'
    s = open(p).read()
    blk = '// national_park { (tools/grounded/maptools/national_park.py; id 1090-1097)\n'
    for key, n, *_, why in TRAINERS:
        blk += '#define TRAINER_%-28s%d // Project Grounded: %s\n' % (key, n, why)
    blk += '// }'
    if '// national_park {' in s:
        i = s.index('// national_park {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    for key, n, *_ in TRAINERS:
        hits = re.findall(r'^#define TRAINER_\w+\s+%d\b' % n, s, re.M)
        assert len(hits) == 1, ('trainer-id dubbel', n, hits)
        assert n < 1200
    open(p, 'w').write(s)
    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- national_park (tools/grounded/maptools/national_park.py) --- */\n\n'
    for key, n, nm, cls, pic, gender, music, ai, team, why in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: ' + cls, 'Pic: ' + pic, 'Gender: ' + gender, 'Music: ' + music,
               'Double Battle: No', ai]
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (key, '\n'.join(hdr), '\n\n'.join(team))
    blk = blk.rstrip('\n') + '\n\n/* --- einde national_park --- */'
    s = bd.replace_block(s, '/* --- national_park', '/* --- einde national_park --- */', blk)
    open(p, 'w').write(s)


PARTNER = '''=== PARTNER_CALYREX ===
Name: CALYREX
Class: Rival
Pic: Ruin Maniac
Gender: Male
Music: Male
Back Pic: Calyrex
AI: Check Bad Move / Try To Faint / Check Viability

Calyrex @ Leftovers
Level: 72
Ability: Unnerve
Nature: Modest
IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe
EVs: 252 HP / 252 SpA / 4 SpD
- Psychic
- Giga Drain
- Life Dew
- Helping Hand

'''


def partner():
    p = 'src/data/battle_partners.party'
    s = open(p).read()
    if '=== PARTNER_CALYREX ===' not in s:
        anchor = '/* --- Battle Stadium (gegenereerd door tools/grounded/stadium/pool.py) --- */'
        s = s.replace(anchor, PARTNER + anchor, 1)
        open(p, 'w').write(s)
    p = 'include/constants/battle_partner.h'
    s = open(p).read()
    if 'PARTNER_CALYREX' not in s:
        a = '#define PARTNER_KECCLES 3 // Project Grounded: Keccles in Sootopolis\n'
        assert a in s
        top, rest = s.split(a)
        rest = re.sub(r'(#define PARTNER_\w+ )(\d+)', lambda m: m.group(1) + str(int(m.group(2)) + 1), rest)
        s = top + a + '#define PARTNER_CALYREX 4 // Project Grounded: Calyrex in het brandende National Park\n' + rest
        open(p, 'w').write(s)


# ====================================================================== scripts en teksten
def park_scripts(T):
    S = Scr('NationalPark', '@ Project Grounded: NationalPark (tools/grounded/maptools/national_park.py)\n'
            '@ Illusie (layout NationalPark) -> brandend park (NationalPark_Ruined) -> hersteld (NationalPark).\n'
            'NationalPark_MapScripts::\n'
            '\tmap_script MAP_SCRIPT_ON_TRANSITION, NationalPark_OnTransition\n'
            '\tmap_script MAP_SCRIPT_ON_FRAME_TABLE, NationalPark_OnFrame\n\t.byte 0\n')
    P, X = S.P, S.T
    tr_keys = [t[0] for t in TRAINERS[:4]]
    S.raw(f'''NationalPark_OnTransition:
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	setflag FLAG_TEMP_3
	setflag FLAG_TEMP_4
	setflag FLAG_TEMP_5
	setflag FLAG_TEMP_6
	call_if_set FLAG_NATIONAL_PARK_SCENE_PENDING, {P}SetScene
	goto_if_set FLAG_NATIONAL_PARK_DONE, {P}StateDone
	goto_if_set FLAG_NATIONAL_PARK_RESTORED, {P}StateRestored
	goto_if_set FLAG_NATIONAL_PARK_REVEALED, {P}StateRuined
	clearflag FLAG_TEMP_1
''' + ''.join(f'\tgoto_if_not_defeated TRAINER_{k}, {P}StateEnd\n' for k in tr_keys) + f'''	clearflag FLAG_TEMP_3
	end

{P}SetScene:
	setvar VAR_TEMP_1, 1
	return

{P}StateDone:
	clearflag FLAG_TEMP_1
	end

{P}StateRestored:
	clearflag FLAG_TEMP_1
	clearflag FLAG_TEMP_3
	clearflag FLAG_TEMP_4
	end

{P}StateRuined:
	setmaplayoutindex LAYOUT_NATIONAL_PARK_RUINED
	setweather WEATHER_VOLCANIC_ASH
	savebgm MUS_RG_POKE_MANSION
	clearflag FLAG_TEMP_3
	goto_if_defeated TRAINER_NP_SHADOW_ASH, {P}StateRuinedB
	clearflag FLAG_TEMP_2
{P}StateRuinedB:
	goto_if_defeated TRAINER_NP_SHADOW_EMBER, {P}StateEnd
	clearflag FLAG_TEMP_5
{P}StateEnd:
	end

NationalPark_OnFrame:
	map_script_2 VAR_TEMP_1, 1, {P}Scene
	.2byte 0

{P}Scene:
	lockall
	setvar VAR_TEMP_1, 0
	clearflag FLAG_NATIONAL_PARK_SCENE_PENDING
	goto_if_set FLAG_NATIONAL_PARK_RESTORED, {P}SceneRestored
	delay 30
	playmoncry SPECIES_CALYREX, CRY_MODE_NORMAL
	msgbox {X}RevealAfter, MSGBOX_DEFAULT
	waitmoncry
	releaseall
	end

{P}SceneRestored:
	delay 30
	msgbox {X}RestoredAfter, MSGBOX_DEFAULT
	closemessage
	playse SE_THUNDER
	delay 20
	playmoncry SPECIES_ETERNATUS, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox {X}EternatusArrives, MSGBOX_DEFAULT
	releaseall
	end

{P}CheckCalyrex::
''' + ''.join(f'\tgoto_if_not_defeated TRAINER_{k}, {P}CheckCalyrexEnd\n' for k in tr_keys) + f'''	msgbox {X}CalyrexAppears, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_TEMP_3
	addobject LOCALID_NATIONAL_PARK_CALYREX
	playmoncry SPECIES_CALYREX, CRY_MODE_NORMAL
	waitmoncry
{P}CheckCalyrexEnd::
	release
	end
''', [('RevealAfter', "CALYREX: Behold. This is your park in this dimension. Eternatus got here first. "
                      "It did not bring a picnic basket. The shades that feed on the smoke will come for us. "
                      "Fight beside me. I am a king. I am also, technically, a cabbage."),
          ('RestoredAfter', "The ash blows away. The grass remembers it is green. A Butterfree lands on your head "
                            "as if nothing happened. Denial is a powerful thing."),
          ('EternatusArrives', "CALYREX: It followed the green. Of course it did. Celebi's power is still in "
                               "your team: every POKéMON you send out will rise above itself. Go. I will hold your sandwiches."),
          ('CalyrexAppears', "Something by the fountain clears its throat. Regally.")])

    for key, n, nm, *_ in TRAINERS[:4]:
        lines = {
            'NP_BUG_CATCHER_DOUGLAS': ("This park has a bug-catching contest every day. I win every day. Nobody else enters. "
                                       "Is that suspicious? Don't answer that.",
                                       "My bugs! My contest record!", "The grass feels... painted. Like a screensaver."),
            'NP_PICNICKER_SIENNA': ("I've been eating the same sandwich since I got here. It never runs out. "
                                    "Best day of my life! Probably! Has it been a day?", "My sandwich is crying.",
                                    "If you see a crowned guy on a stag, tell him the sandwich is a little suspicious."),
            'NP_GENTLEMAN_WALDORF': ("Good afternoon. It's always afternoon here. I find that very civilised.",
                                     "Most uncivilised. Well played.", "Have you noticed the sun never moves? Lovely. Terrifying."),
            'NP_AROMA_LADY_PETUNIA': ("Smell that? Fresh grass, flowers... and a faint hint of something burning. "
                                      "Probably a barbecue. In every direction.", "Even my Florges smells smoke now.",
                                      "The fountain hums. Fountains don't hum. I'm going to pretend it's jazz."),
        }[key]
        S.raw(f'''{P}{nm.title()}::
	trainerbattle_single TRAINER_{key}, {X}{nm.title()}Intro, {X}{nm.title()}Defeat, {P}CheckCalyrex
	msgbox {X}{nm.title()}Post, MSGBOX_AUTOCLOSE
	end
''', [(nm.title() + 'Intro', lines[0]), (nm.title() + 'Defeat', lines[1]), (nm.title() + 'Post', lines[2])])

    # Calyrex: illusie opheffen / schimmen / naar Ilex / herstel / Eternatus
    S.raw(f'''{P}Calyrex::
	lock
	faceplayer
	goto_if_set FLAG_NATIONAL_PARK_RESTORED, {P}CalyrexEternatus
	goto_if_set FLAG_NATIONAL_PARK_CELEBI_DONE, {P}CalyrexRestore
	goto_if_set FLAG_NATIONAL_PARK_REVEALED, {P}CalyrexRuins
	playmoncry SPECIES_CALYREX, CRY_MODE_ENCOUNTER
	msgbox {X}CalyrexIntro, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	playse SE_M_PSYBEAM
	fadescreenspeed FADE_TO_WHITE, 6
	setflag FLAG_NATIONAL_PARK_REVEALED
	setflag FLAG_NATIONAL_PARK_SCENE_PENDING
	warpsilent MAP_NATIONAL_PARK, {CX}, {CY + 5}
	waitstate
	release
	end

{P}CalyrexRuins:
	goto_if_not_defeated TRAINER_NP_SHADOW_ASH, {P}CalyrexShades
	goto_if_not_defeated TRAINER_NP_SHADOW_EMBER, {P}CalyrexShades
	msgbox {X}CalyrexIlex, MSGBOX_DEFAULT
	release
	end

{P}CalyrexShades:
	msgbox {X}CalyrexShades, MSGBOX_DEFAULT
	release
	end

{P}CalyrexRestore:
	msgbox {X}CalyrexRestore, MSGBOX_DEFAULT
	closemessage
	setobjectxyperm LOCALID_NATIONAL_PARK_CELEBI, {CX - 1}, {CY + 2}
	clearflag FLAG_TEMP_6
	addobject LOCALID_NATIONAL_PARK_CELEBI
	playmoncry SPECIES_CELEBI, CRY_MODE_NORMAL
	waitmoncry
	applymovement LOCALID_NATIONAL_PARK_CELEBI, {P}CelebiCircle
	waitmovement 0
	msgbox {X}CelebiRestores, MSGBOX_DEFAULT
	closemessage
	playse SE_M_HEAL_BELL
	fadescreenspeed FADE_TO_WHITE, 8
	removeobject LOCALID_NATIONAL_PARK_CELEBI
	setflag FLAG_NATIONAL_PARK_RESTORED
	setflag FLAG_NATIONAL_PARK_SCENE_PENDING
	warpsilent MAP_NATIONAL_PARK, {CX}, {CY + 5}
	waitstate
	release
	end

{P}CalyrexEternatus:
	msgbox {X}CalyrexEternatus, MSGBOX_DEFAULT
	release
	end

{P}CelebiCircle:
	walk_fast_left
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_left
	walk_fast_left
	walk_fast_left
	face_down
	step_end

{P}Eternatus::
	lock
	playmoncry SPECIES_ETERNATUS, CRY_MODE_ENCOUNTER
	msgbox {X}EternatusBattle, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_ETERNATUS, 75
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}EternatusStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}EternatusStays
	removeobject LOCALID_NATIONAL_PARK_ETERNATUS
	setflag FLAG_NATIONAL_PARK_DONE
	msgbox {X}CalyrexFarewell, MSGBOX_DEFAULT
	closemessage
	playse SE_M_TELEPORT
	fadescreenspeed FADE_TO_WHITE, 4
	removeobject LOCALID_NATIONAL_PARK_CALYREX
	fadescreenspeed FADE_FROM_WHITE, 4
	msgbox {X}ParkDone, MSGBOX_DEFAULT
{P}EternatusStays:
	release
	end
''', [('CalyrexIntro', "I am CALYREX, King of Bountiful Harvests, traveller of dimensions, and the reason "
                       "this park looks so nice. Sorry. It is an illusion. I channelled it so you would not "
                       "panic. You beat everyone in it, so now you may panic. Look."),
          ('CalyrexShades', "CALYREX: The shades want what is left of this park. One stands by the band of "
                            "the ball, the other blocks the path south. Talk to them. I will be right "
                            "behind you. Slightly to the left."),
          ('CalyrexIlex', "CALYREX: The shades are gone. Now go south, through the woods, to ILEX FOREST. "
                          "At the shrine you will find CELEBI. It cannot beat Eternatus. Nobody here can. "
                          "But it can lend you the strength to try. Bring it back. Gently. In a ball."),
          ('CalyrexRestore', "CALYREX: You caught CELEBI. Now, little one: show this park what it used to be."),
          ('CelebiRestores', "CELEBI circles the fountain and hums a very old song. The fire listens."),
          ('CalyrexEternatus', "CALYREX: Eternatus waits north of the fountain. Your team carries CELEBI's "
                               "power: each one rises above itself the moment it enters battle."),
          ('EternatusBattle', "ETERNATUS looms over the tall grass. It smells like a burnt-out sun. "
                              "Your POKéMON glow green: CELEBI's power is with them."),
          ('CalyrexFarewell', "CALYREX: The park is safe, in this dimension and the next. My horses are "
                              "waiting somewhere cold; they have been sulking without me. Farewell, "
                              "trainer. Do not eat the sandwich."),
          ('ParkDone', "CALYREX has left. The park is quiet. A Ledian waves at you. You wave back. "
                       "Nobody saw. Good.")])

    # schimmen: twee multi battles met Calyrex
    for a, b, tag in (('ASH', 'CINDER', 'A'), ('EMBER', 'SOOT', 'B')):
        S.raw(f'''{P}Shades{tag}::
	lock
	faceplayer
	msgbox {X}Shades{tag}, MSGBOX_DEFAULT
	closemessage
{P}Shades{tag}Choose::
	special SavePlayerParty
	fadescreen FADE_TO_BLACK
	special ChooseHalfPartyForBattle
	waitstate
	goto_if_ne VAR_RESULT, 0, {P}Shades{tag}Battle
	special LoadPlayerParty
	goto {P}Shades{tag}Choose

{P}Shades{tag}Battle::
	multi_2_vs_2 TRAINER_NP_SHADOW_{a}, {X}{a.title()}Defeat, TRAINER_NP_SHADOW_{b}, {X}{b.title()}Defeat, PARTNER_CALYREX
	switch VAR_RESULT
	case 1, {P}Shades{tag}Won
	fadescreen FADE_TO_BLACK
	special SetCB2WhiteOut
	waitstate

{P}Shades{tag}Won::
	msgbox {X}Shades{tag}Won, MSGBOX_DEFAULT
	closemessage
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_NATIONAL_PARK_SHADOW_{a}
	removeobject LOCALID_NATIONAL_PARK_SHADOW_{b}
	setflag FLAG_TEMP_{2 if tag == 'A' else 5}
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end
''', [('Shades' + tag, {'A': "Two shapes made of smoke turn towards you. They have no faces, but somehow "
                                  "they look smug. CALYREX: Together, then.",
                             'B': "The shades block the path south. One of them is wearing a picnic hat. "
                                  "That is the worst thing you have seen today."}[tag]),
              (a.title() + 'Defeat', "...hsss..."),
              (b.title() + 'Defeat', "...the smoke... remembers..."),
              ('Shades' + tag + 'Won', "The shades dissolve into ash. CALYREX nods, as if he did most of the work.")])

    S.npc('SignPlaza', "NATIONAL PARK\nThe shady path south leads to ILEX FOREST.\nPlease do not feed the Beedrill.", 'MSGBOX_SIGN')
    S.npc('SignGate', "NATIONAL PARK\nGate to the SPACETIME CAVE. Opening hours: always, and also never.", 'MSGBOX_SIGN')
    S.write()


def gate_scripts():
    S = Scr('NationalPark_Gate', '@ Project Grounded: NationalPark_Gate (tools/grounded/maptools/national_park.py)\n'
            'NationalPark_Gate_MapScripts::\n\t.byte 0\n')
    S.npc('Guard', "Welcome to the NATIONAL PARK! Admission is free. Leaving is also free, if you can find "
                   "the exit. Most people can. Most.")
    S.write()


def ilex_scripts():
    S = Scr('IlexForest', '@ Project Grounded: IlexForest (tools/grounded/maptools/national_park.py)\n'
            'IlexForest_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, IlexForest_OnTransition\n\t.byte 0\n')
    P, X = S.P, S.T
    S.raw(f'''IlexForest_OnTransition:
	setflag FLAG_TEMP_1
	end

{P}Shrine::
	lock
	goto_if_set FLAG_NATIONAL_PARK_CELEBI_DONE, {P}ShrineDone
	goto_if_unset FLAG_NATIONAL_PARK_REVEALED, {P}ShrineQuiet
	goto_if_not_defeated TRAINER_NP_SHADOW_ASH, {P}ShrineQuiet
	goto_if_not_defeated TRAINER_NP_SHADOW_EMBER, {P}ShrineQuiet
	msgbox {X}ShrineCall, MSGBOX_DEFAULT
	closemessage
	playse SE_M_HEAL_BELL
	clearflag FLAG_TEMP_1
	addobject LOCALID_ILEX_FOREST_CELEBI
	delay 20
	goto {P}CelebiBattle

{P}Celebi::
	lock
{P}CelebiBattle::
	playmoncry SPECIES_CELEBI, CRY_MODE_ENCOUNTER
	msgbox {X}Celebi, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	setwildbattle SPECIES_CELEBI, 70
	special BattleSetup_StartLegendaryBattle
	waitstate
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}CelebiCaught
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}CelebiReset
	release
	end

{P}CelebiReset::
	playse SE_M_TELEPORT
	fadescreenspeed FADE_TO_WHITE, 4
	fadescreenspeed FADE_FROM_WHITE, 4
	msgbox {X}CelebiReset, MSGBOX_DEFAULT
	release
	end

{P}CelebiCaught::
	removeobject LOCALID_ILEX_FOREST_CELEBI
	setflag FLAG_NATIONAL_PARK_CELEBI_DONE
	msgbox {X}CelebiCaught, MSGBOX_DEFAULT
	release
	end

{P}ShrineQuiet::
	msgbox {X}ShrineQuiet, MSGBOX_DEFAULT
	release
	end

{P}ShrineDone::
	msgbox {X}ShrineDone, MSGBOX_DEFAULT
	release
	end
''', [('ShrineCall', "A small stone CELEBI on a mossy pedestal. CALYREX said to call it. You feel silly. "
                     "You call it anyway. The forest goes quiet. Then: a chime."),
          ('Celebi', "CELEBI looks at you as if it has seen this moment before. Several times. "
                     "It did not like how most of them ended."),
          ('CelebiReset', "The world folds back on itself. Somewhere far away, CALYREX sighs and rewinds "
                          "time by a few minutes. CELEBI is still here. Try again. Gently. With a ball."),
          ('CelebiCaught', "CELEBI is yours. The forest exhales. Go back to the NATIONAL PARK: CALYREX is waiting."),
          ('ShrineQuiet', "A small stone CELEBI on a mossy pedestal. Someone left a sandwich as an offering. "
                          "It looks suspiciously familiar."),
          ('ShrineDone', "The shrine is empty now. The sandwich is gone too. Nobody saw who took it.")])
    S.npc('Sign', "ILEX FOREST\nThe forest is said to be protected by a time-travelling spirit.\n"
                  "Please do not walk in circles. It is rude.", 'MSGBOX_SIGN')
    S.write()


# ====================================================================== kaarten
PARK_TRAINERS = [  # (sleutel, gfx, x, y, richting, zicht, scriptnaam)
    ('NP_BUG_CATCHER_DOUGLAS', 'OBJ_EVENT_GFX_BUG_CATCHER', 16, 13, 'RIGHT', 4, 'Douglas'),
    ('NP_PICNICKER_SIENNA', 'OBJ_EVENT_GFX_PICNICKER', 13, 30, 'RIGHT', 4, 'Sienna'),
    ('NP_GENTLEMAN_WALDORF', 'OBJ_EVENT_GFX_GENTLEMAN', 34, 31, 'LEFT', 4, 'Waldorf'),
    ('NP_AROMA_LADY_PETUNIA', 'OBJ_EVENT_GFX_WOMAN_3', 29, 13, 'LEFT', 4, 'Petunia'),
]
CALYREX = (CX, CY + 4)
ETERNATUS = (CX, CY - 5)
SHADOWS = [('ASH', 9, 21, 'A'), ('CINDER', 9, 23, 'A'), ('EMBER', 22, 41, 'B'), ('SOOT', 23, 41, 'B')]
PARK_ITEMS = [(15, 51, 'ITEM_SILVER_POWDER', 'FLAG_ITEM_NATIONAL_PARK_SILVER_POWDER'),
              (47, 20, 'ITEM_SUN_STONE', 'FLAG_ITEM_NATIONAL_PARK_SUN_STONE')]
PARK_HIDDEN = [(8, 31, 'ITEM_BIG_NUGGET', 'FLAG_HIDDEN_ITEM_NATIONAL_PARK_BIG_NUGGET')]
SIGN_PLAZA = (24, 52)
SIGN_GATE = (41, 21)

ILEX_ITEMS = [(5, 41, 'ITEM_REVIVAL_HERB', 'FLAG_ITEM_ILEX_FOREST_REVIVAL_HERB'),
              (33, 5, 'ITEM_BOTTLE_CAP', 'FLAG_ITEM_ILEX_FOREST_BOTTLE_CAP'),
              (35, 35, 'ITEM_MIRACLE_SEED', 'FLAG_ITEM_ILEX_FOREST_MIRACLE_SEED')]
ILEX_HIDDEN = [(7, 18, 'ITEM_RARE_CANDY', 'FLAG_HIDDEN_ITEM_ILEX_FOREST_RARE_CANDY')]
# items die nergens anders liggen (nieuwe_items.py; Jordi 9 okt)
import nieuwe_items as _ni
NEW_ITEM_POS = {'ITEM_SPORT_BALL': (11, 8), 'ITEM_INSECT_PLATE': (13, 49), 'ITEM_POWER_BELT': (47, 23),
                'ITEM_FRIEND_BALL': (17, 38), 'ITEM_LOVE_BALL': (4, 31), 'ITEM_DESTINY_KNOT': (28, 4),
                'ITEM_ROSE_INCENSE': (4, 44)}
NEW_QTY = {}
for _mp, _balls, _hid in (('NationalPark', 'PARK_ITEMS', 'PARK_HIDDEN'), ('IlexForest', 'ILEX_ITEMS', 'ILEX_HIDDEN')):
    for _fl, _it, _q, _h in _ni.items(_mp):
        _x, _y = NEW_ITEM_POS[_it]
        globals()[_hid if _h else _balls] = globals().get(_hid if _h else _balls, []) + [(_x, _y, _it, _fl)]
        NEW_QTY[_it] = _q
ILEX_SIGN = (18, 2)


def maps():
    M = build_park()
    lay = save_layout('NationalPark', PW, PH, M, 'gTileset_General', 'gTileset_Rustboro')
    P = 'NationalPark_EventScript_'
    objs = []
    for key, gfx, x, y, face, sight, nm in PARK_TRAINERS:
        o = tr(gfx, x, y, P + nm, face, sight)
        o['flag'] = 'FLAG_TEMP_1'
        objs.append(o)
    objs.append(lid(obj('OBJ_EVENT_GFX_SPECIES(CALYREX)', CALYREX[0], CALYREX[1], P + 'Calyrex', 'FLAG_TEMP_3',
                        'MOVEMENT_TYPE_FACE_DOWN'), 'LOCALID_NATIONAL_PARK_CALYREX'))
    objs.append(lid(obj('OBJ_EVENT_GFX_SPECIES(ETERNATUS)', ETERNATUS[0], ETERNATUS[1], P + 'Eternatus', 'FLAG_TEMP_4',
                        'MOVEMENT_TYPE_FACE_DOWN'), 'LOCALID_NATIONAL_PARK_ETERNATUS'))
    objs.append(lid(obj('OBJ_EVENT_GFX_SPECIES(CELEBI)', CX, CY + 3, '0x0', 'FLAG_TEMP_6',
                        'MOVEMENT_TYPE_FACE_DOWN'), 'LOCALID_NATIONAL_PARK_CELEBI'))
    for nm, x, y, tag in SHADOWS:
        objs.append(lid(obj('OBJ_EVENT_GFX_SHADOW_TRIAD', x, y, P + 'Shades' + tag, 'FLAG_TEMP_%d' % (2 if tag == 'A' else 5),
                            'MOVEMENT_TYPE_FACE_RIGHT' if tag == 'A' else 'MOVEMENT_TYPE_FACE_UP'),
                        'LOCALID_NATIONAL_PARK_SHADOW_' + nm))
    for x, y, it, fl in PARK_ITEMS:
        objs.append(ball(x, y, it, fl))
        objs[-1]['movement_range_x'] = NEW_QTY.get(it, 1) if NEW_QTY.get(it, 1) > 1 else 0
    warps = [warp(GATE_DOOR[0], GATE_DOOR[1], 'NATIONAL_PARK_GATE', 0),
             warp(TUNNEL[0], PH - 1, 'ILEX_FOREST', 0), warp(TUNNEL[1], PH - 1, 'ILEX_FOREST', 1)]
    bgs = [sign(SIGN_PLAZA[0], SIGN_PLAZA[1], P + 'SignPlaza'), sign(SIGN_GATE[0], SIGN_GATE[1], P + 'SignGate')] + \
          [hidden(x, y, it, fl) for x, y, it, fl in PARK_HIDDEN]
    for x, y in (SIGN_PLAZA, SIGN_GATE):
        M[y][x] = val(SIGN_MT, 1)
    save_layout('NationalPark', PW, PH, M, 'gTileset_General', 'gTileset_Rustboro')
    # brandend park: zelfde kaart, maar met smeulende plekken (bloemen in het sintelpalet, ze flakkeren mee met de
    # bloemenanimatie van General) in het verbrande gras
    import random
    rng = random.Random(898)        # nationaal dexnummer van Calyrex
    R = [row[:] for row in M]
    for y in range(PH):
        for x in range(PW):
            if R[y][x] & 0x3FF in (TALL, DARK_LAWN, GRASS) and rng.random() < 0.07:
                R[y][x] = val(FLOWER)
    save_layout('NationalPark_Ruined', PW, PH, R, 'gTileset_ParkBurntGeneral', 'gTileset_ParkBurntRustboro')
    write_map('NationalPark', lay, objs, warps, bgs)

    # poorthuis: layout van de Seaside Cycling Road-poort
    write_map('NationalPark_Gate', 'LAYOUT_ROUTE110_SEASIDE_CYCLING_ROAD_ENTRANCE',
              [obj('OBJ_EVENT_GFX_MAN_1', 7, 2, 'NationalPark_Gate_EventScript_Guard')],
              [warp(1, 5, 'NATIONAL_PARK', 0), warp(2, 5, 'NATIONAL_PARK', 0),
               warp(12, 5, 'SPACETIME_CAVE', 5), warp(13, 5, 'SPACETIME_CAVE', 6)], [],
              **bd.indoor(show_map_name=False, music='MUS_RG_CELADON', region_map_section='MAPSEC_NATIONAL_PARK'))

    I = build_ilex()
    for x, y in (ILEX_SIGN,):
        I[y][x] = val(SIGN_MT, 1)
    ilay = save_layout('IlexForest', IW, IH, I, 'gTileset_IlexGeneral', 'gTileset_IlexPetalburg')
    P = 'IlexForest_EventScript_'
    iobjs = [lid(obj('OBJ_EVENT_GFX_STATUE_CELEBI', SHRINE[0], SHRINE[1], P + 'Shrine', move='MOVEMENT_TYPE_NONE'),
                 'LOCALID_ILEX_FOREST_SHRINE'),
             lid(obj('OBJ_EVENT_GFX_SPECIES(CELEBI)', CELEBI[0], CELEBI[1], P + 'Celebi', 'FLAG_TEMP_1',
                     'MOVEMENT_TYPE_FACE_DOWN'), 'LOCALID_ILEX_FOREST_CELEBI')]
    for x, y, it, fl in ILEX_ITEMS:
        iobjs.append(ball(x, y, it, fl))
        iobjs[-1]['movement_range_x'] = NEW_QTY.get(it, 1) if NEW_QTY.get(it, 1) > 1 else 0
    write_map('IlexForest', ilay, iobjs, [warp(ILEX_ENTRY[0], 0, 'NATIONAL_PARK', 1), warp(ILEX_ENTRY[1], 0, 'NATIONAL_PARK', 2)],
              [sign(ILEX_SIGN[0], ILEX_SIGN[1], P + 'Sign')] + [hidden(x, y, it, fl) for x, y, it, fl in ILEX_HIDDEN],
              music='MUS_RG_VIRIDIAN_FOREST', region_map_section='MAPSEC_ILEX_FOREST', weather='WEATHER_SHADE',
              allow_cycling=False)
    return M, I


def check(M, I):
    # park: vanaf de deur van het poorthuisje alles bereikbaar
    shades_b = {(x, y) for _, x, y, t in SHADOWS if t == 'B'}
    objs = {(x, y) for _, _, x, y, *_ in PARK_TRAINERS} | {CALYREX, ETERNATUS} | {(x, y) for _, x, y, _ in SHADOWS} | \
           {(x, y) for x, y, *_ in PARK_ITEMS}
    start = (GATE_DOOR[0], GATE_DOOR[1] + 1)
    r = reach(M, PW, PH, start, objs - shades_b)
    canopy = {(x, y) for y in range(PH) for x in range(PW) if M[y][x] & 0x3FF in (0x1CE, 0x1CF)}
    probs = []
    for p in objs | {SIGN_PLAZA, SIGN_GATE}:
        if not adj(r, p):
            probs.append(('park: onbereikbaar', p))
        if p in canopy:
            probs.append(('park: event op een boomkruin', p))
    for x, y in [(CX - 1, CY + 2), (CX - 2, CY + 2)] + [(CX - 2, CY + 1 - i) for i in range(4)] + \
            [(CX - 2 + i, CY - 2) for i in range(5)] + [(CX + 2, CY - 1 + i) for i in range(4)] + \
            [(CX + 1 - i, CY + 2) for i in range(3)]:
        if M[y][x] & 0x3FF != PAVE:
            probs.append(('park: Celebi-rondje niet over tegels', (x, y)))
    for x, y, *_ in PARK_HIDDEN:
        if (x, y) not in r:
            probs.append(('park: verborgen item onbereikbaar', (x, y)))
    for x in TUNNEL:
        if (x, PH - 1) not in r:
            probs.append(('park: bospad onbereikbaar', x))
    # schimmen B blokkeren de gang: zonder hen kom je niet bij het plein
    rb = reach(M, PW, PH, start, objs)
    if (TUNNEL[0], PH - 1) in rb:
        probs.append(('park: schimmen blokkeren de gang niet', None))
    # Ilex: vanaf de ingang
    iobjs = {SHRINE, CELEBI} | {(x, y) for x, y, *_ in ILEX_ITEMS}
    ri = reach(I, IW, IH, (ILEX_ENTRY[0], 0), iobjs)
    for p in iobjs | {ILEX_SIGN}:
        if not adj(ri, p):
            probs.append(('ilex: onbereikbaar', p))
    for x, y, *_ in ILEX_HIDDEN:
        if (x, y) not in ri:
            probs.append(('ilex: verborgen item onbereikbaar', (x, y)))
    for p in probs:
        print('PROBLEEM', p)
    assert not probs
    print('park %d, ilex %d tegels bereikbaar' % (len(r), len(ri)))


def main():
    tilesets()
    palettes()
    flags()
    mapsecs()
    bd.WILD = WILD
    bd.wild()
    trainers()
    partner()
    for mp in ('NationalPark', 'NationalPark_Gate', 'IlexForest'):
        os.makedirs('data/maps/' + mp, exist_ok=True)
    park_scripts(None)
    gate_scripts()
    ilex_scripts()
    M, I = maps()
    check(M, I)
    if len(sys.argv) > 1:
        for mp, h in (('NationalPark', PH), ('IlexForest', IH)):
            subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), mp,
                            os.path.join(sys.argv[1], mp + '.png'), '0', str(h)], check=True)


if __name__ == '__main__':
    main()
