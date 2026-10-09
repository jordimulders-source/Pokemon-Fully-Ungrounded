"""Project Grounded: vier extra dungeons (TODO deel 1, punten 1-2). Deterministisch en idempotent.

  GraniteCave_CrystalGrotto   Kristalgrot onder Granite Cave B2F (Carbink, Steven-lore, Diancie-hommage).
                              Layout: kopie van SeafloorCavern_Room3 (zuidelijke uitgangen dicht) met blauwe/rode
                              kristallen (metatiles 0x3A5-0x3A7, zoals Crystal Cavity). Ingang: ladder in B2F (25,16).
  Cave of Origin dieper       De drie ongebruikte R/S-kamers (CaveOfOrigin_UnusedRubySapphireMap1-3, vanilla layouts)
                              als keten onder B1F: B1F (13,4) -> Map1 -> Map2 -> Map3 (doodlopend, ladder weg).
                              De ladder in B1F verschijnt pas na de Hall of Fame (ON_LOAD, FLAG_SYS_GAME_CLEAR).
                              Primal-lore op borden, een onderzoeker, items; geen legendary.
  ShoalCave_LowTideFrozenDepths
                              IJzige onderlaag van Shoal Cave (bij eb). Layout: kopie van ColdstepCave_IceRoom2
                              (ijsglijpuzzel; tweede ladder wordt vloer). Ingang: ladder in de Ice Room (17,28).
  Route128_BubbleGrotto       Luchtbel-grot (Route 128): kopie van MarineCave_Entrance (uitgang boven dicht).
                              Ingang: zwemgat in Underwater_Route128 (27,19); terug = duiken in de poel.
                              Kluizenaar met Relicanth-lore. Alleen water/vissen (de vloer is zand, geen landgras).

Flags: FLAG_GROUNDED 470-499 (dit script). Geen trainers. Teksten zijn placeholders (Jordi herschrijft ze).
Gebruik: python3 tools/grounded/maptools/dungeon_extra.py [rendermap]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, os, random, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beacon_dragon as bd          # zet ook de werkmap op de repo-root

sms, cx, oq = bd.sms, bd.cx, bd.oq
Scr, ball, sign, hidden, warp, obj = bd.Scr, bd.ball, bd.sign, bd.hidden, bd.warp, bd.obj
reach, next_to = cx.reach, cx.next_to

# ====================================================================== flags
FLAGS = [
    (470, 'FLAG_ITEM_GRANITE_CRYSTAL_STAR_PIECE', 'Granite Cave kristalgrot: Star Piece'),
    (471, 'FLAG_ITEM_GRANITE_CRYSTAL_HARD_STONE', 'Granite Cave kristalgrot: Hard Stone'),
    (472, 'FLAG_HIDDEN_ITEM_GRANITE_CRYSTAL_SHINY_STONE', 'Granite Cave kristalgrot: verborgen Shiny Stone'),
    (473, 'FLAG_ITEM_ORIGIN_DEEP1_DAMP_ROCK', 'Cave of Origin diep 1: Damp Rock'),
    (474, 'FLAG_ITEM_ORIGIN_DEEP2_HEAT_ROCK', 'Cave of Origin diep 2: Heat Rock'),
    (475, 'FLAG_ITEM_ORIGIN_DEEP3_PP_MAX', 'Cave of Origin diep 3: PP Max'),
    (476, 'FLAG_HIDDEN_ITEM_ORIGIN_DEEP3_BIG_NUGGET', 'Cave of Origin diep 3: verborgen Big Nugget'),
    (477, 'FLAG_ITEM_SHOAL_FROZEN_ICE_STONE', 'Shoal Cave ijzige onderlaag: Ice Stone'),
    (478, 'FLAG_ITEM_SHOAL_FROZEN_ICY_ROCK', 'Shoal Cave ijzige onderlaag: Icy Rock'),
    (479, 'FLAG_ITEM_SHOAL_FROZEN_ABILITY_CAPSULE', 'Shoal Cave ijzige onderlaag: Ability Capsule'),
    (480, 'FLAG_HIDDEN_ITEM_SHOAL_FROZEN_PEARL_STRING', 'Shoal Cave ijzige onderlaag: verborgen Pearl String'),
    (481, 'FLAG_ITEM_BUBBLE_GROTTO_DEEP_SEA_TOOTH', 'luchtbel-grot Route 128: Deep Sea Tooth'),
    (482, 'FLAG_ITEM_BUBBLE_GROTTO_RARE_BONE', 'luchtbel-grot Route 128: Rare Bone'),
    (483, 'FLAG_HIDDEN_ITEM_BUBBLE_GROTTO_STAR_PIECE', 'luchtbel-grot Route 128: verborgen Star Piece'),
]
F = {name: name for _, name, _ in FLAGS}


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// dungeon_extra { (tools/grounded/maptools/dungeon_extra.py; FLAG_GROUNDED 470-499)\n'
    for n, name, why in FLAGS:
        assert 470 <= n <= 499
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// dungeon_extra {' in s:
        i = s.index('// dungeon_extra {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('\n', s.index('// Verdeling (houd bij!)')) + 1
        anchor = s.index('\n', anchor) + 1          # na de 3 commentaarregels
        anchor = s.index('\n', anchor) + 1
        s = s[:anchor] + blk + '\n' + s[anchor:]
    s = s.replace('430-469 Tao-eiland (tao_island.py), 470+ vrij.',
                  '430-469 Tao-eiland (tao_island.py), 470-499 extra dungeons (dungeon_extra.py), 500+ vrij.')
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


# ====================================================================== hulpjes
def read(path, W, H):
    return oq.read_layout(path, W, H)


def save(g, path):
    cx.save_grid(g, path)


def layout_grid(mapname):
    L = bd.layout_of(mapname)
    return read(L['blockdata_filepath'], L['width'], L['height']), L


def edit_map(name, fn):
    return oq.edit_map(name, fn)


def check(g, start, objs, bgs, tag, passable=()):
    blocked = {(o['x'], o['y']) for o in objs}
    walk = reach(g, [start], blocked=blocked, passable=passable)
    for o in objs:
        assert next_to((o['x'], o['y']), walk), (tag, 'object onbereikbaar', o['x'], o['y'], o['script'])
    for b in bgs:
        if b['type'] == 'hidden_item':
            assert (b['x'], b['y']) in walk, (tag, 'verborgen item onbereikbaar', b)
        else:
            assert next_to((b['x'], b['y']), walk) and not cx.walkable(g[b['y']][b['x']]), (tag, 'bord', b)
    return walk


def scripts_block(mapname, block):
    """Voegt een gemarkeerd blok toe aan (of vervangt het in) de scripts.inc van een bestaande kaart."""
    p = 'data/maps/%s/scripts.inc' % mapname
    s = open(p).read()
    start, end = '@ --- dungeon_extra (', '@ --- einde dungeon_extra ---'
    new = '@ --- dungeon_extra (gegenereerd door tools/grounded/maptools/dungeon_extra.py) ---\n' + \
          block.rstrip('\n') + '\n' + end
    s = bd.replace_block(s, start, end, new)
    open(p, 'w').write(s.rstrip('\n') + '\n')


def add_map_script(mapname, kind, label):
    p = 'data/maps/%s/scripts.inc' % mapname
    s = open(p).read()
    line = '\tmap_script %s, %s\n' % (kind, label)
    if line not in s:
        hdr = '%s_MapScripts::\n' % mapname
        i = s.index(hdr) + len(hdr)
        s = s[:i] + line + s[i:]
        open(p, 'w').write(s)


def texts(prefix, items):
    return ''.join(bd.text(prefix + k, v) for k, v in items)


# ====================================================================== 1. Granite Cave: kristalgrot
GC_LADDER = (25, 16)                 # in B2F, vloer 0x201 tegen de noordwand
CRYSTAL_BLUE, CRYSTAL_RED = 0x3a5, (0x3a6, 0x3a7)


def granite():
    name, const = 'GraniteCave_CrystalGrotto', 'GRANITE_CAVE_CRYSTAL_GROTTO'
    g, W, H, prim, sec = bd.copy_layout('SeafloorCavern_Room3', name)
    FLOOR = g[11][6]
    assert (FLOOR & 0x3ff) == 0x201
    wall_edge = g[14][11]
    for (x, y) in ((9, 13), (4, 15)):                    # zuidelijke uitgangen dicht
        assert (g[y][x] & 0x3ff) in (0x207, 0x201)
        g[y][x] = FLOOR
        for dx in (-1, 0, 1):
            g[y + 1][x + dx] = wall_edge
    entry = (8, 1)
    start = (8, 2)
    S = Scr(name, '''@ Project Grounded: kristalgrot onder Granite Cave B2F (Carbink, Steven-lore). Layout: kopie van
@ SeafloorCavern_Room3 met kristallen. Kaart en scripts: tools/grounded/maptools/dungeon_extra.py.
GraniteCave_CrystalGrotto_MapScripts::
	.byte 0
''')
    P = S.P
    S.npc('Collector',
          "Shh. The CARBINK think I'm a rock.\n\n"
          "I've been a rock for three days. My knees are basically gravel now.\n\n"
          "They say a pink princess made of diamond sleeps down here. The CARBINK say that. "
          "They're liars. Beautiful, sparkly liars.")
    S.npc('Scratches',
          "Scratched into the wall:\n“S. STONE WAS HERE. TOOK NOTHING.”\n\n"
          "Below it, smaller:\n“TOOK ONE.”\n\nBelow that, smaller still:\n“OK, SEVEN.”", 'MSGBOX_SIGN')
    objs = [obj('OBJ_EVENT_GFX_HIKER', 12, 11, P + 'Collector', move='MOVEMENT_TYPE_FACE_LEFT'),
            ball(12, 5, 'ITEM_STAR_PIECE', F['FLAG_ITEM_GRANITE_CRYSTAL_STAR_PIECE']),
            ball(3, 15, 'ITEM_HARD_STONE', F['FLAG_ITEM_GRANITE_CRYSTAL_HARD_STONE'])]
    bgs = [sign(8, 8, P + 'Scratches'),
           hidden(6, 7, 'ITEM_SHINY_STONE', F['FLAG_HIDDEN_ITEM_GRANITE_CRYSTAL_SHINY_STONE'])]
    # kristallen op vloer langs wanden (zoals grotto136.py), niets mag onbereikbaar worden
    keep = {start, (6, 13), (6, 14), (7, 11)} | {(o['x'] + dx, o['y'] + dy) for o in objs + bgs
                                                  for dx in (-1, 0, 1) for dy in (-1, 0, 1)}
    rnd = random.Random(4700)
    cand = [(x, y) for y in range(2, H - 1) for x in range(1, W - 1)
            if g[y][x] == FLOOR and (x, y) not in keep and
            sum(g[y + dy][x + dx] != FLOOR for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))) >= 1]
    rnd.shuffle(cand)
    base = len(reach(g, [start]))
    placed = []
    for (x, y) in cand:
        if len(placed) >= 12:
            break
        if any(abs(x - a) + abs(y - b) < 3 for a, b in placed):
            continue
        old = g[y][x]
        g[y][x] = (CRYSTAL_BLUE if (x + y) % 3 else rnd.choice(CRYSTAL_RED)) | 0x400 | (3 << 12)
        n = len(reach(g, [start]))
        if n < base - 1:
            g[y][x] = old
            continue
        base = n
        placed.append((x, y))
    check(g, start, objs, bgs, name)
    save(g, 'data/layouts/%s/map.bin' % name)
    bd.register_layout(name, const, W, H, prim, sec)

    # B2F: ladder omlaag (vast in de layout), warp ernaartoe
    b2, L2 = layout_grid('GraniteCave_B2F')
    x, y = GC_LADDER
    assert (b2[y][x] & 0x3ff) in (0x201, 0x23d) and (b2[y - 1][x] & 0xc00), 'B2F-ladder niet tegen een noordwand'
    b2[y][x] = 0x23d | (3 << 12)
    save(b2, L2['blockdata_filepath'])
    gi = edit_map('GraniteCave_B2F', lambda m: oq.warp_to(m, x, y, 'MAP_' + const))
    sms.write_map(name, const, objs, [warp(entry[0], entry[1], 'GRANITE_CAVE_B2F', gi)], [], bgs,
                  music='MUS_PETALBURG_WOODS', weather='WEATHER_NONE', map_type='MAP_TYPE_UNDERGROUND',
                  region_map_section='MAPSEC_GRANITE_CAVE', show_map_name=False, allow_cycling=False,
                  allow_escaping=True)
    oq.register_map(name)
    S.write()
    return name


# ====================================================================== 2. Cave of Origin dieper
B1F_LADDER = (13, 4)
ORIGIN = ['CaveOfOrigin_UnusedRubySapphireMap1', 'CaveOfOrigin_UnusedRubySapphireMap2',
          'CaveOfOrigin_UnusedRubySapphireMap3']


def origin():
    # B1F: warp 1 naar Map1 (warp 0); de ladder verschijnt na de Hall of Fame
    b1, L1 = layout_grid('CaveOfOrigin_B1F')
    x, y = B1F_LADDER
    assert (b1[y][x] & 0x3ff) == 0x31b and (b1[y - 1][x] & 0xc00), 'B1F-ladderplek'
    bi = edit_map('CaveOfOrigin_B1F', lambda m: oq.warp_to(m, x, y, 'MAP_CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP1'))
    assert bi == 1
    add_map_script('CaveOfOrigin_B1F', 'MAP_SCRIPT_ON_LOAD', 'CaveOfOrigin_B1F_OnLoad')
    scripts_block('CaveOfOrigin_B1F', '''@ Na de Hall of Fame: ladder (%d,%d) omlaag naar de oude R/S-kamers (Cave of Origin dieper).
CaveOfOrigin_B1F_OnLoad:
	goto_if_unset FLAG_SYS_GAME_CLEAR, CaveOfOrigin_B1F_EventScript_NoDeepLadder
	setmetatile %d, %d, 0x33D, FALSE
CaveOfOrigin_B1F_EventScript_NoDeepLadder:
	end
''' % (x, y, x, y))

    def chain(m1):
        def f(m):
            for w in m['warp_events']:
                if m1 == 0 and w['dest_map'] == 'MAP_CAVE_OF_ORIGIN_1F':
                    w.update({'dest_map': 'MAP_CAVE_OF_ORIGIN_B1F', 'dest_warp_id': '1'})
            if m1 == 2:
                m['warp_events'] = [w for w in m['warp_events'] if w['dest_map'] != 'MAP_CAVE_OF_ORIGIN_B1F']
            m['requires_flash'] = False
        return f

    texts_by_map = {
        0: [('Mural', "An ancient mural. A huge whale and a huge... other whale? No, that one has legs.\n\n"
                      "They are fighting over a small island. The island looks like it would rather not be involved."),
            ('Glyphs', "Old glyphs:\n“WHEN THE SEA ROSE, WE BUILT BOATS.\nWHEN THE LAND ROSE, WE BUILT "
                       "SMALLER BOATS.”\n\n“WE WERE NOT VERY GOOD AT THIS.”")],
        1: [('Helmet', "A MAGMA helmet, half melted, next to an AQUA bandana, half dissolved.\n\n"
                       "Someone has arranged them in a little heart shape. That's worse, somehow.")],
        2: [('Orbs', "Two empty hollows in the rock, shaped like orbs. One red, one blue.\n\n"
                     "A note: “BORROWED. WILL RETURN. -A.”\nUnderneath: “NO YOU WON'T. -M.”"),
            ('Primal', "Carved deep into the stone:\n“THE PRIMAL FORM IS THE TRUE FORM.”\n\n"
                       "Someone added, in marker:\n“THE TRUE FORM HAS VERY BAD MANNERS.”"),
            ('Researcher', "I'm writing my thesis on PRIMAL REVERSION. Twelve years now.\n\n"
                           "Chapter one: it is very hot. Chapter two: it is very wet. Chapter three is mostly "
                           "me crying.\n\nMy supervisor says the legendaries left. I'm staying until they come "
                           "back and sign my consent form.")],
    }
    layout = {
        0: dict(start=(13, 6), objs=[ball(9, 5, 'ITEM_DAMP_ROCK', F['FLAG_ITEM_ORIGIN_DEEP1_DAMP_ROCK'])],
                signs=[(11, 4, 'Mural'), (10, 18, 'Glyphs')], hidden=[]),
        1: dict(start=(5, 10), objs=[ball(15, 6, 'ITEM_HEAT_ROCK', F['FLAG_ITEM_ORIGIN_DEEP2_HEAT_ROCK'])],
                signs=[(10, 4, 'Helmet')], hidden=[]),
        2: dict(start=(7, 14), objs=[ball(5, 12, 'ITEM_PP_MAX', F['FLAG_ITEM_ORIGIN_DEEP3_PP_MAX'])],
                signs=[(9, 4, 'Orbs'), (11, 16, 'Primal')],
                hidden=[(13, 6, 'ITEM_BIG_NUGGET', F['FLAG_HIDDEN_ITEM_ORIGIN_DEEP3_BIG_NUGGET'])]),
    }
    # Map3: de oude ladder naar B1F (12,6) wordt vloer
    g3, L3 = layout_grid(ORIGIN[2])
    if (g3[6][12] & 0x3ff) == 0x33d:
        g3[6][12] = g3[6][11]
        save(g3, L3['blockdata_filepath'])
    for i, mname in enumerate(ORIGIN):
        edit_map(mname, chain(i))
        g, L = layout_grid(mname)
        lay = layout[i]
        P = mname + '_EventScript_'
        T = mname + '_Text_'
        code = ''
        objs = list(lay['objs'])
        for k, _ in texts_by_map[i]:
            kind = 'MSGBOX_NPC' if k == 'Researcher' else 'MSGBOX_SIGN'
            code += '%s%s::\n\tmsgbox %s%s, %s\n\tend\n\n' % (P, 'DX' + k, T, 'DX' + k, kind)
        if i == 2:
            objs.append(obj('OBJ_EVENT_GFX_SCIENTIST_1', 13, 8, P + 'DXResearcher', move='MOVEMENT_TYPE_FACE_UP'))
        bgs = [sign(sx, sy, P + 'DX' + k) for sx, sy, k in lay['signs']] + \
              [hidden(hx, hy, it, fl) for hx, hy, it, fl in lay['hidden']]
        check(g, lay['start'], objs, bgs, mname)

        def setev(m, objs=objs, bgs=bgs):
            m['object_events'] = objs
            m['bg_events'] = bgs
        edit_map(mname, setev)
        scripts_block(mname, '@ Cave of Origin dieper: Primal-lore (placeholders).\n' + code +
                      texts(T, [('DX' + k, v) for k, v in texts_by_map[i]]))
    return ORIGIN


# ====================================================================== 3. Shoal Cave: ijzige onderlaag
ICE = 0x38d
ICE_LADDER = (17, 28)                # in ShoalCave_LowTideIceRoom


def walk_ok(t, z):
    e = t >> 12
    if t & 0xc00:
        return False, z
    if e == 0 or z == 0 or e == z:
        return True, (e if e else z)
    return False, z


def ice_reach(g, start, blocked=()):
    """Standplaatsen met ijsglijden (MB_ICE 0x38d): over ijs glij je door tot een obstakel of gewone vloer."""
    W, H = len(g[0]), len(g)
    z0 = g[start[1]][start[0]] >> 12
    seen = {(start, z0)}
    st = [(start, z0)]
    while st:
        (x, y), z = st.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in blocked:
                continue
            ok, nz = walk_ok(g[ny][nx], z)
            if not ok:
                continue
            while (g[ny][nx] & 0x3ff) == ICE:
                mx, my = nx + dx, ny + dy
                if not (0 <= mx < W and 0 <= my < H) or (mx, my) in blocked:
                    break
                ok2, mz = walk_ok(g[my][mx], nz)
                if not ok2:
                    break
                nx, ny, nz = mx, my, mz
            if ((nx, ny), nz) not in seen:
                seen.add(((nx, ny), nz))
                st.append(((nx, ny), nz))
    return {p for p, _ in seen}


def ice_check(g, start, objs, bgs, tag):
    stand = ice_reach(g, start, {(o['x'], o['y']) for o in objs})
    for o in objs:
        assert next_to((o['x'], o['y']), stand), (tag, 'object onbereikbaar', o['x'], o['y'])
    for b in bgs:
        if b['type'] == 'hidden_item':
            assert (b['x'], b['y']) in stand, (tag, 'verborgen item onbereikbaar', b)
        else:
            assert next_to((b['x'], b['y']), stand), (tag, 'bord', b)
    return stand


def shoal():
    name, const = 'ShoalCave_LowTideFrozenDepths', 'SHOAL_CAVE_LOW_TIDE_FROZEN_DEPTHS'
    g, W, H, prim, sec = bd.copy_layout('ColdstepCave_IceRoom2', name)
    LADDER = 0x38b
    arrive = (3, 11)
    assert (g[11][3] & 0x3ff) == LADDER
    if (g[3][15] & 0x3ff) == LADDER:                    # tweede ladder (naar Route 135 in Coldstep) wordt vloer
        g[3][15] = g[3][14]
    S = Scr(name, '''@ Project Grounded: de ijzige onderlaag van Shoal Cave (bij eb). Layout: kopie van ColdstepCave_IceRoom2.
@ Kaart en scripts: tools/grounded/maptools/dungeon_extra.py.
ShoalCave_LowTideFrozenDepths_MapScripts::
	.byte 0
''')
    P = S.P
    S.npc('Hole', "A big CETODDLE-shaped hole in the ice wall.\n\n"
                  "The CETODDLE that made it is nowhere to be seen. The hole looks very proud of itself.",
          'MSGBOX_SIGN')
    S.npc('Tally', "Tally marks scratched into the ice. Hundreds of them.\n\n"
                   "At the very end:\n“DAY 412. THE TIDE CAME BACK. I DID NOT.”", 'MSGBOX_SIGN')
    objs = [ball(13, 3, 'ITEM_ABILITY_CAPSULE', F['FLAG_ITEM_SHOAL_FROZEN_ABILITY_CAPSULE']),
            ball(3, 7, 'ITEM_ICY_ROCK', F['FLAG_ITEM_SHOAL_FROZEN_ICY_ROCK']),
            ball(5, 13, 'ITEM_ICE_STONE', F['FLAG_ITEM_SHOAL_FROZEN_ICE_STONE'])]
    bgs = [sign(16, 2, P + 'Hole'), sign(1, 11, P + 'Tally'),
           hidden(15, 3, 'ITEM_PEARL_STRING', F['FLAG_HIDDEN_ITEM_SHOAL_FROZEN_PEARL_STRING'])]
    ice_check(g, arrive, objs, bgs, name)
    save(g, 'data/layouts/%s/map.bin' % name)
    bd.register_layout(name, const, W, H, prim, sec)

    # Ice Room: ladder omlaag
    ir, LI = layout_grid('ShoalCave_LowTideIceRoom')
    x, y = ICE_LADDER
    assert (ir[y][x] & 0x3ff) in (0x385, 0x37f)
    ir[y][x] = 0x37f | (3 << 12)
    m_ir = json.load(open('data/maps/ShoalCave_LowTideIceRoom/map.json'))
    assert (x, y) in ice_reach(ir, (17, 10), {(o['x'], o['y']) for o in m_ir['object_events']}), 'ijsladder onbereikbaar'
    save(ir, LI['blockdata_filepath'])
    ii = edit_map('ShoalCave_LowTideIceRoom', lambda m: oq.warp_to(m, x, y, 'MAP_' + const))
    sms.write_map(name, const, objs, [warp(arrive[0], arrive[1], 'SHOAL_CAVE_LOW_TIDE_ICE_ROOM', ii)], [], bgs,
                  music='MUS_MT_PYRE', weather='WEATHER_NONE', map_type='MAP_TYPE_UNDERGROUND',
                  region_map_section='MAPSEC_SHOAL_CAVE', show_map_name=False, allow_cycling=False,
                  allow_escaping=True)
    oq.register_map(name)
    S.write()
    return name


# ====================================================================== 4. Route 128: luchtbel-grot
UW_HOLE = (27, 19)                   # zwemgat in Underwater_Route128 (middenonder); bovenrij op y-1
UW_HOLE_SRC = (38, 26)               # bestaand zwemgat (naar de Seafloor Cavern) als bron voor de tegels


def bubble():
    name, const = 'Route128_BubbleGrotto', 'ROUTE128_BUBBLE_GROTTO'
    g, W, H, prim, sec = bd.copy_layout('MarineCave_Entrance', name)
    WALL = 0x2f9 | 0x400
    for xx in (13, 14, 15):                             # uitgang boven (naar Marine Cave End) dicht
        g[0][xx] = WALL
        g[1][xx] = WALL
    arrive = (9, 18)
    assert (g[18][9] & 0x3ff) == 0x294, 'aankomst niet in diep water'
    S = Scr(name, '''@ Project Grounded: luchtbel-grot onder Route 128 (kopie van MarineCave_Entrance). Ingang: zwemgat in
@ Underwater_Route128 (27,19); terug = duiken in de poel. Kaart en scripts: tools/grounded/maptools/dungeon_extra.py.
Route128_BubbleGrotto_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, Route128_BubbleGrotto_OnResume
	.byte 0

Route128_BubbleGrotto_OnResume:
	setdivewarp MAP_UNDERWATER_ROUTE128, %d, %d
	setescapewarp MAP_UNDERWATER_ROUTE128, %d, %d
	end
''' % (UW_HOLE[0], UW_HOLE[1] + 1, UW_HOLE[0], UW_HOLE[1] + 1))
    P = S.P
    S.npc('Hermit', "Air! Real air! Well, recycled air. Mostly mine.\n\n"
                    "I came down here to study RELICANTH. It hasn't changed in a hundred million years.\n\n"
                    "Neither have I, since 1987. We get along great.\n\n"
                    "Don't tell the surface about this place. They'll want to put a gift shop in it.")
    S.npc('Bubble', "A pocket of trapped air wobbles against the ceiling.\n\n"
                    "It has been there for centuries. It is the oldest bubble in HOENN. It looks very tired.",
          'MSGBOX_SIGN')
    objs = [obj('OBJ_EVENT_GFX_OLD_MAN', 17, 11, P + 'Hermit', move='MOVEMENT_TYPE_FACE_LEFT'),
            ball(14, 3, 'ITEM_DEEP_SEA_TOOTH', F['FLAG_ITEM_BUBBLE_GROTTO_DEEP_SEA_TOOTH']),
            ball(3, 11, 'ITEM_RARE_BONE', F['FLAG_ITEM_BUBBLE_GROTTO_RARE_BONE'])]
    bgs = [sign(12, 2, P + 'Bubble'),
           hidden(3, 12, 'ITEM_STAR_PIECE', F['FLAG_HIDDEN_ITEM_BUBBLE_GROTTO_STAR_PIECE'])]
    check(g, arrive, objs, bgs, name)
    save(g, 'data/layouts/%s/map.bin' % name)
    bd.register_layout(name, const, W, H, prim, sec)

    # Underwater_Route128: zwemgat (tegels gekopieerd van het bestaande gat), warp erop
    uw, LU = layout_grid('Underwater_Route128')
    sx, sy = UW_HOLE_SRC
    x, y = UW_HOLE
    src = [[uw[sy - 1 + r][sx - 1 + c] for c in range(3)] for r in range(2)]
    assert [[t & 0x3ff for t in row] for row in src] == [[0x265, 0x266, 0x267], [0x26d, 0x26e, 0x26f]], src
    assert cx.walkable(uw[y + 1][x]), 'onder het zwemgat ligt geen zeebodem'
    for r in range(2):
        for c in range(3):
            uw[y - 1 + r][x - 1 + c] = src[r][c]
    save(uw, LU['blockdata_filepath'])
    ui = edit_map('Underwater_Route128', lambda m: oq.warp_to(m, x, y, 'MAP_' + const))
    sms.write_map(name, const, objs, [warp(arrive[0], arrive[1], 'UNDERWATER_ROUTE128', ui)], [], bgs,
                  music='MUS_SEALED_CHAMBER', weather='WEATHER_NONE', map_type='MAP_TYPE_UNDERGROUND',
                  region_map_section='MAPSEC_ROUTE_128', show_map_name=False, allow_cycling=False,
                  allow_escaping=False)
    oq.register_map(name)
    S.write()
    return name


# ====================================================================== wilde Pokemon
def lv(spec, a, b):
    return [(s, a, b) for s in spec]


ORIGIN_SPECIES = ['GASTRODON', 'HIPPOWDON', 'CLODSIRE', 'MUDSDALE', 'SEISMITOAD', 'DONPHAN', 'KROOKODILE',
                  'HEATMOR', 'COPPERAJAH', 'SANDACONDA', 'RHYPERIOR', 'VOLCARONA']
WILD = {
    'GRANITE_CAVE_CRYSTAL_GROTTO': dict(
        land=(10, [('CARBINK', 15, 17), ('ROGGENROLA', 14, 16), ('NACLI', 14, 16), ('CHINGLING', 14, 16),
                   ('SPOINK', 14, 16), ('MINIOR', 15, 17), ('FERROSEED', 15, 17), ('KLINK', 15, 17),
                   ('CUFANT', 16, 18), ('MAWILE', 16, 18), ('PAWNIARD', 17, 19), ('SABLEYE', 18, 19)])),
    'CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP1': dict(land=(8, lv(ORIGIN_SPECIES, 52, 55))),
    'CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP2': dict(land=(8, lv(ORIGIN_SPECIES, 53, 56))),
    'CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP3': dict(land=(8, lv(ORIGIN_SPECIES, 54, 58))),
    'SHOAL_CAVE_LOW_TIDE_FROZEN_DEPTHS': dict(
        land=(10, [('CETODDLE', 36, 38), ('BERGMITE', 34, 36), ('AVALUGG_HISUI', 38, 41), ('ABOMASNOW', 36, 39),
                   ('AMAURA', 36, 38), ('EISCUE', 37, 39), ('SNOM', 35, 37), ('CRABOMINABLE', 38, 40),
                   ('CETITAN', 40, 42), ('ARCTOZOLT', 40, 42), ('MAMOSWINE', 42, 43), ('AURORUS', 42, 43)])),
    'ROUTE128_BUBBLE_GROTTO': dict(
        water=(4, [('OMASTAR', 38, 41), ('KABUTOPS', 38, 41), ('CARRACOSTA', 39, 42), ('BARBARACLE', 40, 42),
                   ('RELICANTH', 42, 44)]),
        fishing=(25, [('CLAMPERL', 20, 24), ('BINACLE', 20, 24), ('CLAUNCHER', 26, 30), ('SKRELP', 26, 30),
                      ('MANTYKE', 26, 30), ('HUNTAIL', 36, 40), ('GOREBYSS', 36, 40), ('CLAWITZER', 38, 42),
                      ('BRUXISH', 40, 43), ('DHELMISE', 42, 44)])),
}


# ====================================================================== main
if __name__ == '__main__':
    flags()
    names = [granite()] + origin() + [shoal(), bubble()]
    bd.WILD = WILD
    bd.wild()
    if len(sys.argv) > 1:
        for n in names + ['GraniteCave_B2F', 'CaveOfOrigin_B1F', 'ShoalCave_LowTideIceRoom', 'Underwater_Route128']:
            L = bd.layout_of(n)
            subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), n,
                            os.path.join(sys.argv[1], n + '.png'), '0', str(L['height'])], check=True)
    print('klaar:', ', '.join(names))
    print('let op: draai daarna tools/grounded/maptools/legends2.py opnieuw (legendaries op deze kaarten)')
