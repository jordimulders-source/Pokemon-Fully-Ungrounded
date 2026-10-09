"""Project Grounded: Swords of Justice (Cobalion, Terrakion, Virizion) + Keldeo. Deterministisch en idempotent.

Zonder quest, zoals in Gen 5; alles post-game (FLAG_SYS_GAME_CLEAR), lv 70.
  GraniteCave_SwordChamber   Cobalion. Opening in de noordwand van een nis in Granite Cave B2F (11,10), dicht
                             met een Rock Smash-rots OP de opening (vaste flag). Layout SWORD_CHAMBER = kopie van
                             Stevens kamer (15x14), gedeeld met de Victory Road-kamer; steen met zwaardkerf (10,8).
  VictoryRoad_SwordChamber   Terrakion. Zelfde opening in Victory Road B2F (8,23), gang linksonder bij de ladder.
  Mangrove Mire              Virizion in de doodlopende open plek aan het einde van het oostelijke zijpad (49,14);
                             een boomstam met een zwaardsnede (50,13). Geen eigen kaart: de plek is al verborgen.
  UnchartedIsle (MAPSEC "???") Keldeo. Na de drie zwaarden belt Mr. Briney (PokeNav); praat met hem (huis Route 104,
                             Dewford of Route 109), fade, en je staat op een pas ontstane zandbank binnen een ring van
                             draaikolken (General-tiles: ondiepte-autotile zoals Whirl Island). Briney brengt je terug.
In beide kamers verschijnt het zwaard pas na de Hall of Fame (FLAG_TEMP_1 in ON_TRANSITION), in het moeras ook.
Flags: FLAG_GROUNDED 800-839. scripts.inc's staan met de hand in data/maps (en data/maps/UnchartedIsle).
Gebruik: python3 tools/grounded/maptools/swords_keldeo.py [rendermap]"""
import json, os, random, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ogerpon_quest as oq          # zet ook de werkmap op de repo-root
import victory_road_ext as vre
import sea_temple_lugia as stl

SOLID = 0xc00
rng = random.Random(647)            # Keldeo
SAND_MS = {(1, 1, 1, 1): 0x124, (0, 0, 0, 1): 0x195, (0, 0, 1, 1): 0x196, (0, 0, 1, 0): 0x197, (0, 1, 0, 1): 0x19d,
           (1, 0, 1, 0): 0x19f, (0, 1, 0, 0): 0x1a5, (1, 1, 0, 0): 0x1a6, (1, 0, 0, 0): 0x1a7,
           (0, 1, 1, 1): 0x185, (1, 0, 1, 1): 0x186, (1, 1, 0, 1): 0x18d, (1, 1, 1, 0): 0x18e}   # zoals shipwreck_shoals
ATTR = open('data/tilesets/primary/general/metatile_attributes.bin', 'rb').read()
def beh(m):
    return struct.unpack_from('<H', ATTR, (m & 0x3ff) * 2)[0] & 0xff

# ====================================================================== flags
FLAGS = [
    (800, 'FLAG_DEFEATED_COBALION', 'Cobalion gevangen/verslagen (Granite Cave)'),
    (801, 'FLAG_DEFEATED_TERRAKION', 'Terrakion gevangen/verslagen (Victory Road)'),
    (802, 'FLAG_DEFEATED_VIRIZION', 'Virizion gevangen/verslagen (Mangrove Mire)'),
    (803, 'FLAG_BRINEY_KELDEO_CALL', 'Mr. Briney heeft gebeld over het eiland (na de drie zwaarden)'),
    (804, 'FLAG_DEFEATED_KELDEO', 'Keldeo gevangen/verslagen (UnchartedIsle)'),
    (805, 'FLAG_GRANITE_SWORD_CHAMBER_ROCK', 'Rock Smash-rots voor de zwaardkamer in Granite Cave B2F'),
    (806, 'FLAG_VICTORY_ROAD_SWORD_CHAMBER_ROCK', 'Rock Smash-rots voor de zwaardkamer in Victory Road B2F'),
    (807, 'FLAG_KELDEO_TRIP_FROM_DEWFORD', 'Keldeo-bootreis vertrokken uit Dewford (terugweg)'),
    (808, 'FLAG_KELDEO_TRIP_FROM_ROUTE109', 'Keldeo-bootreis vertrokken van Route 109 (terugweg)'),
    (809, 'FLAG_RECEIVED_MELTAN', 'Meltan gekregen (Sterns scheepswerf, Slateport)'),
]


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// swords_keldeo { (tools/grounded/maptools/swords_keldeo.py; FLAG_GROUNDED 800-839, 810-839 nog vrij)\n'
    for n, name, why in FLAGS:
        assert 800 <= n <= 839
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// swords_keldeo {' in s:
        i = s.index('// swords_keldeo {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = '// mega_forest {'
        i = s.index(anchor)
        s = s[:i] + blk + '\n' + s[i:]
    open(p, 'w').write(s)


# ====================================================================== zwaardkamers
CH_W, CH_H = 15, 14
CH_DOOR = (7, 3)                    # deur in de noordwand (zoals bij Steven)
CH_MON = (9, 7)                     # het zwaard, van opzij aan te spreken (grote sprite valt anders over je heen)
CH_STONE = (10, 8)                  # rotsblok 0x203 = steen met zwaardkerf


def chamber_layout():
    g = oq.read_layout('data/layouts/GraniteCave_StevensRoom/map.bin', CH_W, CH_H)
    assert g[CH_STONE[1]][CH_STONE[0]] & 0x3ff == 0x203
    r = oq.reach(g, [(CH_DOOR[0], CH_DOOR[1] + 1)])
    assert (CH_MON[0] - 1, CH_MON[1]) in r and (CH_STONE[0] - 1, CH_STONE[1]) in r
    oq.save(g, 'SwordChamber', 'data/layouts/GraniteCave_StevensRoom/border.bin')
    oq.register_layout('SwordChamber', 'SWORD_CHAMBER', CH_W, CH_H, 'gTileset_Cave')


def chamber_map(name, const, base, species, back_map, back_warp, music=None):
    lid = 'LOCALID_%s_%s' % (const, species)
    o = oq.obj('OBJ_EVENT_GFX_SPECIES(%s)' % species, CH_MON[0], CH_MON[1], '%s_EventScript_%s' % (name, species.title()),
               'FLAG_TEMP_1', lid, move='MOVEMENT_TYPE_FACE_LEFT')
    kw = {'requires_flash': False}
    if music:
        kw['music'] = music
    oq.write_map(name, const, base, 'SWORD_CHAMBER', [o],
                 [{'x': CH_DOOR[0], 'y': CH_DOOR[1], 'elevation': 3, 'dest_map': back_map, 'dest_warp_id': str(back_warp)}], **kw)
    oq.edit_map(name, lambda m: m.__setitem__('bg_events', [
        {'type': 'sign', 'x': CH_STONE[0], 'y': CH_STONE[1], 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
         'script': 'SwordsOfJustice_EventScript_NotchedStone'}]))
    oq.register_map(name)


def opening(mapname, x, y, dest, rockflag, start):
    """Grotopening (x,y) in een dubbele noordwand met een Rock Smash-rots erop; geeft de warp-index terug."""
    m = json.load(open('data/maps/%s/map.json' % mapname))
    L = [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id') == m['layout']][0]
    W, H = L['width'], L['height']
    g = oq.read_layout(L['blockdata_filepath'], W, H)
    done = g[y][x] & 0x3ff == 0x214
    if not done:
        assert all(g[yy][xx] & 0x3ff == 0x219 for xx in (x - 1, x, x + 1) for yy in (y - 1, y)), (mapname, 'geen wand')
        vre.door(g, x, y, elev=3)
    rocks = {(o['x'], o['y']) for o in m['object_events'] if o['graphics_id'] == 'OBJ_EVENT_GFX_BREAKABLE_ROCK'}
    r = vre.vr_reach(g, [start], passable=rocks | {(x, y)})
    assert (x, y + 1) in r and (x, y) in r, (mapname, 'opening onbereikbaar')
    oq.cx.save_grid(g, L['blockdata_filepath'])
    wi = vre.set_warp(m, x, y, 3, dest, 0)
    vre.set_obj(m, vre.obj('OBJ_EVENT_GFX_BREAKABLE_ROCK', x, y, 'EventScript_RockSmash', rockflag,
                           move='MOVEMENT_TYPE_LOOK_AROUND', elev=3))
    open('data/maps/%s/map.json' % mapname, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    return wi


# ====================================================================== Mangrove Mire
VIRIZION = (49, 14)
CUT_TREE = (50, 13)


def mire():
    def fn(m):
        m['object_events'] = [o for o in m['object_events'] if o.get('local_id') != 'LOCALID_MANGROVE_MIRE_VIRIZION']
        m['object_events'].append(oq.obj('OBJ_EVENT_GFX_SPECIES(VIRIZION)', VIRIZION[0], VIRIZION[1],
                                         'MangroveMire_EventScript_Virizion', 'FLAG_TEMP_1', 'LOCALID_MANGROVE_MIRE_VIRIZION',
                                         move='MOVEMENT_TYPE_FACE_DOWN'))
        m['bg_events'] = [b for b in m['bg_events'] if b.get('script') != 'MangroveMire_EventScript_CutTree']
        m['bg_events'].append({'type': 'sign', 'x': CUT_TREE[0], 'y': CUT_TREE[1], 'elevation': 0,
                               'player_facing_dir': 'BG_EVENT_PLAYER_FACING_NORTH', 'script': 'MangroveMire_EventScript_CutTree'})
    oq.edit_map('MangroveMire', fn)
    g = oq.read_layout('data/layouts/MangroveMire/map.bin', 56, 44)
    r = oq.reach(g, [(54, 29)])
    assert (VIRIZION[0], VIRIZION[1] + 1) in r and (CUT_TREE[0], CUT_TREE[1] + 1) in r, 'Virizion-plek onbereikbaar'
    assert g[CUT_TREE[1]][CUT_TREE[0]] & SOLID


# ====================================================================== UnchartedIsle (Keldeo)
IW, IH = 28, 22
KELDEO = (14, 9)
ARRIVE = (14, 14)                   # hier zet Briney je af (op de ondiepte, boot eronder)
BRINEY = (15, 14)
BOAT = (14, 16)


def isle():
    W, H = IW, IH
    M = [[0x170] * W for _ in range(H)]
    # zandbank: ondiepte (V) met een zandplaat (S) erin, beide op een hoekpuntenraster (ellips + wat ruis)
    def blob(rx, ry, noise, inside=None):
        G = [[0] * (W + 1) for _ in range(H + 1)]
        for y in range(1, H):
            for x in range(1, W):
                d = ((x - 14.0) / rx) ** 2 + ((y - 10.5) / ry) ** 2
                if d < 1.0 + rng.uniform(-noise, noise) and (inside is None or all(
                        inside[y + b][x + a] for a in (-1, 0, 1) for b in (-1, 0, 1))):
                    G[y][x] = 1
        changed = True
        while changed:
            changed = False
            for y in range(1, H):              # losse uitsteeksels weg
                for x in range(1, W):
                    if G[y][x] and G[y - 1][x] + G[y + 1][x] + G[y][x - 1] + G[y][x + 1] < 2:
                        G[y][x] = 0; changed = True
            for y in range(H):                 # geen diagonale paren
                for x in range(W):
                    q = (G[y][x], G[y][x + 1], G[y + 1][x], G[y + 1][x + 1])
                    if q in ((1, 0, 0, 1), (0, 1, 1, 0)):
                        if inside is None:
                            G[y][x] = G[y][x + 1] = G[y + 1][x] = G[y + 1][x + 1] = 1
                        else:
                            G[y][x] = G[y][x + 1] = G[y + 1][x] = G[y + 1][x + 1] = 0
                        changed = True
        return G
    V = blob(8.4, 5.6, 0.08)
    S = blob(5.6, 3.4, 0.08, inside=V)
    for y in range(H):
        for x in range(W):
            q = (V[y][x], V[y][x + 1], V[y + 1][x], V[y + 1][x + 1])
            M[y][x] = stl.SHOAL_MS[q]
            s4 = (S[y][x], S[y][x + 1], S[y + 1][x], S[y + 1][x + 1])
            if any(s4):
                assert q == (1, 1, 1, 1), ('zand tegen de rand', x, y)
                M[y][x] = SAND_MS[s4]
    shoal = {(x, y) for y in range(H) for x in range(W) if M[y][x] != 0x170}

    def free2(x, y, gap=1):
        for yy in range(y - gap, y + 2 + gap):
            for xx in range(x - gap, x + 2 + gap):
                if not (0 <= xx < W and 0 <= yy < H) or (xx, yy) in shoal:
                    return False
        return True

    def stamp(x, y, piece):
        for i, mt in enumerate(piece):
            M[y + i // 2][x + i % 2] = mt | SOLID

    keep = {(BOAT[0] + dx, BOAT[1] + dy) for dx in (-1, 0, 1, 2) for dy in (-1, 0, 1, 2)}
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            if x in (0, W - 2) or y in (0, H - 2):
                stamp(x, y, stl.ROCK if rng.random() < 0.15 else stl.WHIRL)
    for y in range(2, H - 2, 2):
        for x in range(2, W - 2, 2):
            if (x in (2, W - 4) or y in (2, H - 4)) and rng.random() < 0.5 and free2(x, y, 0) \
                    and not any((x + a, y + b) in keep for a in (0, 1) for b in (0, 1)):
                stamp(x, y, stl.ROCK if rng.random() < 0.3 else stl.WHIRL)
    placed, tries = 0, 0
    while placed < 3 and tries < 400:
        tries += 1
        x, y = rng.randrange(4, W - 6, 2), rng.randrange(4, H - 6, 2)
        if free2(x, y) and not any((x + a, y + b) in keep for a in range(-1, 3) for b in range(-1, 3)):
            stamp(x, y, stl.WHIRL if placed != 1 else stl.ROCK); placed += 1
    # hoogtes: open water 1, ondiepte en zand 3 (zoals shipwreck_shoals)
    for y in range(H):
        for x in range(W):
            if not M[y][x] & SOLID:
                M[y][x] |= (1 << 12) if beh(M[y][x]) == 0x15 else (3 << 12)
    # controles: Keldeo op het zand, aankomst/Briney op de bank, boot op open water, alles te voet verbonden
    mt = lambda p: M[p[1]][p[0]] & 0x3ff
    if os.environ.get('ISLE_DEBUG'):
        for y, row in enumerate(M):
            print('%2d ' % y + ''.join({0x170: '~', 0x19e: 's', 0x124: 'S'}.get(t & 0x3ff, '#' if t & SOLID else (
                'e' if beh(t) == 0x15 else 'd')) for t in row))
    assert mt(KELDEO) == 0x124 and mt((KELDEO[0], KELDEO[1] + 1)) == 0x124, 'Keldeo niet op het zand'
    for p in (ARRIVE, BRINEY):
        assert mt(p) in (0x19e, 0x124), ('niet op de zandbank', p)
    assert beh(M[BOAT[1]][BOAT[0]]) == 0x15 and not M[BOAT[1]][BOAT[0]] & SOLID, 'boot niet op open water'
    foot = {(x, y) for y in range(H) for x in range(W) if not M[y][x] & SOLID and beh(M[y][x]) != 0x15}
    sea = {(x, y) for y in range(H) for x in range(W)} - foot
    r = oq.reach(M, [ARRIVE], blocked=sea | {KELDEO, BRINEY})
    assert (KELDEO[0], KELDEO[1] + 1) in r and (BRINEY[0] - 1, BRINEY[1]) in r
    assert len(r) == len(foot) - 2, 'losse stukjes zandbank'
    stl.save(M, 'UnchartedIsle', stl.WHIRL)
    oq.register_layout('UnchartedIsle', 'UNCHARTED_ISLE', W, H, 'gTileset_Mossdeep')
    objs = [
        oq.obj('OBJ_EVENT_GFX_SPECIES(KELDEO)', KELDEO[0], KELDEO[1], 'UnchartedIsle_EventScript_Keldeo',
               'FLAG_DEFEATED_KELDEO', 'LOCALID_UNCHARTED_ISLE_KELDEO', elev=3),
        oq.obj('OBJ_EVENT_GFX_EXPERT_M', BRINEY[0], BRINEY[1], 'UnchartedIsle_EventScript_Briney', '0',
               'LOCALID_UNCHARTED_ISLE_BRINEY', elev=3, move='MOVEMENT_TYPE_FACE_LEFT'),
        oq.obj('OBJ_EVENT_GFX_MR_BRINEYS_BOAT', BOAT[0], BOAT[1], '0x0', '0', 'LOCALID_UNCHARTED_ISLE_BOAT', elev=1,
               move='MOVEMENT_TYPE_FACE_UP'),
    ]
    oq.write_map('UnchartedIsle', 'UNCHARTED_ISLE', 'WhirlIsland', 'UNCHARTED_ISLE', objs, [],
                 region_map_section='MAPSEC_UNCHARTED_ISLE', show_map_name=True, music='MUS_SEALED_CHAMBER',
                 weather='WEATHER_NONE', map_type='MAP_TYPE_OCEAN_ROUTE', allow_cycling=False, allow_escaping=False)
    oq.register_map('UnchartedIsle')
    return M


# ====================================================================== Meltan (gift, Sterns scheepswerf)
def meltan():
    def fn(m):
        m['object_events'] = [o for o in m['object_events']
                              if o.get('local_id') not in ('LOCALID_SHIPYARD_RIVET', 'LOCALID_SHIPYARD_MELTAN')]
        m['object_events'] += [
            oq.obj('OBJ_EVENT_GFX_HIKER', 17, 10, 'SlateportCity_SternsShipyard_1F_EventScript_Rivet', '0',
                   'LOCALID_SHIPYARD_RIVET', move='MOVEMENT_TYPE_FACE_LEFT'),
            oq.obj('OBJ_EVENT_GFX_SPECIES(MELTAN)', 16, 10, 'SlateportCity_SternsShipyard_1F_EventScript_Meltan',
                   'FLAG_RECEIVED_MELTAN', 'LOCALID_SHIPYARD_MELTAN', move='MOVEMENT_TYPE_FACE_RIGHT'),
        ]
    oq.edit_map('SlateportCity_SternsShipyard_1F', fn)


# ====================================================================== mapsec "???"
def mapsec():
    p = 'src/data/region_map/region_map_sections.json'
    s = open(p).read()
    if 'MAPSEC_UNCHARTED_ISLE' not in s:
        i = s.rindex('}', 0, s.rindex(']'))
        s = s[:i + 1] + ',\n    {\n      "id": "MAPSEC_UNCHARTED_ISLE",\n      "name": "???"\n    }' + s[i + 1:]
        json.loads(s)
        open(p, 'w').write(s)
    p = 'src/map_name_popup.c'
    s = open(p).read()
    if 'MAPSEC_UNCHARTED_ISLE' not in s:
        for theme, anchor in (('MAPPOPUP_THEME_STONE', '[MAPSEC_SPACETIME_CAVE - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_STONE,'),
                              ('MAPPOPUP_THEME_BW_DEFAULT', '[MAPSEC_SPACETIME_CAVE - KANTO_MAPSEC_COUNT] = MAPPOPUP_THEME_BW_DEFAULT,')):
            i = s.index(anchor); j = s.index('\n', i)
            s = s[:j + 1] + '    [MAPSEC_UNCHARTED_ISLE - KANTO_MAPSEC_COUNT] = %s, // Project Grounded: Keldeo-eiland (\"???\")\n' % theme + s[j + 1:]
        open(p, 'w').write(s)
    p = 'src/region_map.c'
    s = open(p).read()
    if 'MAPSEC_UNCHARTED_ISLE' not in s:
        anchor = '    {MAPSEC_OUTER_SPACE,'
        i = s.index(anchor)
        s = s[:i] + '    {MAPSEC_UNCHARTED_ISLE,              MAPSEC_ROUTE_105}, // Project Grounded: Keldeo-eiland, "ergens op zee"\n' + s[i:]
        open(p, 'w').write(s)


def main():
    flags()
    chamber_layout()
    wg = opening('GraniteCave_B2F', 11, 10, 'MAP_GRANITE_CAVE_SWORD_CHAMBER', 'FLAG_GRANITE_SWORD_CHAMBER_ROCK', (29, 14))
    wv = opening('VictoryRoad_B2F', 8, 23, 'MAP_VICTORY_ROAD_SWORD_CHAMBER', 'FLAG_VICTORY_ROAD_SWORD_CHAMBER_ROCK', (5, 26))
    chamber_map('GraniteCave_SwordChamber', 'GRANITE_CAVE_SWORD_CHAMBER', 'GraniteCave_StevensRoom', 'COBALION',
                'MAP_GRANITE_CAVE_B2F', wg)
    chamber_map('VictoryRoad_SwordChamber', 'VICTORY_ROAD_SWORD_CHAMBER', 'VictoryRoad_B2F', 'TERRAKION',
                'MAP_VICTORY_ROAD_B2F', wv)
    mire()
    isle()
    mapsec()
    meltan()
    if len(sys.argv) > 1:
        for n, y1 in (('GraniteCave_SwordChamber', 14), ('GraniteCave_B2F', 26), ('VictoryRoad_B2F', 31),
                      ('MangroveMire', 44), ('UnchartedIsle', 22)):
            subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), n,
                            os.path.join(sys.argv[1], n + '.png'), '0', str(y1)], check=True)
    print('klaar; warps Granite B2F %d, Victory Road B2F %d' % (wg, wv))


if __name__ == '__main__':
    main()
