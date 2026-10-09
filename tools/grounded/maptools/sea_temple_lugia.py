"""Project Grounded: de zeetempel in de trog van Route 128 (Manaphy/Phione) en Whirl Island (Lugia).

Bouwt (idempotent, vaste seed) layouts + map.json's en registreert alles; de scripts.inc's staan met de hand in
data/maps/<kaart>/scripts.inc.

Zeetempel (Dive, dus vanaf badge 7):
  Underwater_Route128   zwemgat in de noordwand van de oostelijke kom (76,19), warp naar
  Underwater_SeaTemple  kopie van Underwater_SealedChamber: een lange donkere trog naar beneden, met zeewier
                        (wilde Pokemon) in de hele onderste kom; bovenkomen op het plateau (12,44) = tempel, elders =
                        Route 128 (ON_DIVE_WARP, zoals de Sealed Chamber).
  SeaTemple_Hall        kopie van SealedChamber_OuterRoom (poel om in boven te komen, tien gebeeldhouwde
                        stenen = de puzzel: maan, eb, vloed; de deur in de noordwand gaat dan open).
  SeaTemple_Sanctum     kopie van SealedChamber_InnerRoom: Manaphy (lv 50), daarna een ei (Phione) + de Silver Wing.
Whirl Island (Lugia, Dive):
  Underwater_Route124   zwemgat in de noordwand van de westelijke kom (13,25), warp naar
  Underwater_WhirlIsland  kopie van Underwater_SootopolisCity (onderzeese grot); bovenkomen = de lagune.
  WhirlIsland           40x40: de Shoal Cave-berg van Route 125 (alleen General-tiles) met eigen ondiepte
                        (autotile op een hoekpuntenraster), een lagune en een ring van draaikolken en rotsen
                        (border = draaikolken). Diep water in de lagune = terug duiken.
  WhirlIsland_Cave      kopie van MarineCave_End: Lugia (lv 60) in het meer, alleen met de Silver Wing in de tas.

Gebruik: python3 tools/grounded/maptools/sea_temple_lugia.py [rendermap]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, os, random, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ogerpon_quest as oq     # hulpjes (read_layout, register_layout, register_map, ...); zet de werkmap op de repo

rng = random.Random(249)       # Lugia
SOLID = 0xc00

def grid_copy(src, W, H, name, border_from=None):
    g = oq.read_layout('data/layouts/%s/map.bin' % src, W, H)
    return g

def save(g, name, border):
    os.makedirs('data/layouts/' + name, exist_ok=True)
    oq.cx.save_grid(g, 'data/layouts/%s/map.bin' % name)
    if isinstance(border, str):
        border = open(border, 'rb').read()
    else:
        border = struct.pack('<4H', *border)
    open('data/layouts/%s/border.bin' % name, 'wb').write(border)

def put_hole(g, x, ytop):
    """Zwemgat (Underwater-tileset): bovenrij 265-267 (massief), onderrij 26d/26e/26f (alleen het midden open)."""
    for i, (top, bot) in enumerate(((0x265, 0x26d), (0x266, 0x26e), (0x267, 0x26f))):
        g[ytop][x - 1 + i] = top | SOLID
        g[ytop + 1][x - 1 + i] = bot | (0 if bot == 0x26e else SOLID)

def sign(x, y, script):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
            'script': script}

def base_map(name, const, base, layout_const, objs, warps, bgs=(), **kw):
    oq.write_map(name, const, base, layout_const, objs, warps, **kw)
    p = 'data/maps/%s/map.json' % name
    m = json.load(open(p))
    m['bg_events'] = list(bgs)
    open(p, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')

# =============================================================== Zeetempel
R128_HOLE = (76, 18)           # bovenrij van het zwemgat in Underwater_Route128 (warp op (76,19))
EMERGE_TEMPLE = (12, 44)       # plateau in Underwater_SeaTemple

def sea_temple():
    # --- Underwater_Route128: zwemgat
    W, H = 120, 40
    g = oq.read_layout('data/layouts/Underwater_Route128/map.bin', W, H)
    x, y = R128_HOLE
    assert all(g[y][x + d] & SOLID for d in (-1, 0, 1)) and not g[y + 1][x] & SOLID, 'gat niet in een noordwand'
    put_hole(g, x, y)
    oq.cx.save_grid(g, 'data/layouts/Underwater_Route128/map.bin')
    wi = oq.edit_map('Underwater_Route128', lambda m: oq.warp_to(m, x, y + 1, 'MAP_UNDERWATER_SEA_TEMPLE'))

    # --- Underwater_SeaTemple: kopie van de Sealed Chamber-trog, zeewier in de onderste kom
    W, H = 22, 48
    g = oq.read_layout('data/layouts/Underwater_SealedChamber/map.bin', W, H)
    weed = 0
    for yy in range(36, 47):
        for xx in range(W):
            if g[yy][xx] & 0x3ff == 0x2d3 and (xx, yy) != EMERGE_TEMPLE:
                g[yy][xx] = (g[yy][xx] & ~0x3ff) | 0x281; weed += 1
    save(g, 'Underwater_SeaTemple', 'data/layouts/Underwater_SealedChamber/border.bin')
    oq.register_layout('Underwater_SeaTemple', 'UNDERWATER_SEA_TEMPLE', W, H, 'gTileset_Underwater')
    base_map('Underwater_SeaTemple', 'UNDERWATER_SEA_TEMPLE', 'Underwater_SealedChamber', 'UNDERWATER_SEA_TEMPLE', [],
             [{'x': 7, 'y': 1, 'elevation': 0, 'dest_map': 'MAP_UNDERWATER_ROUTE128', 'dest_warp_id': str(wi)}],
             [sign(12, 43, 'Underwater_SeaTemple_EventScript_Carving')],
             region_map_section='MAPSEC_SEA_TEMPLE', show_map_name=True)
    oq.register_map('Underwater_SeaTemple')

    # --- SeaTemple_Hall: kopie van SealedChamber_OuterRoom (deur dicht via ON_LOAD tot de puzzel klaar is)
    W, H = 21, 23
    g = oq.read_layout('data/layouts/SealedChamber_OuterRoom/map.bin', W, H)
    save(g, 'SeaTemple_Hall', 'data/layouts/SealedChamber_OuterRoom/border.bin')
    oq.register_layout('SeaTemple_Hall', 'SEA_TEMPLE_HALL', W, H, 'gTileset_Cave')
    stones = {  # steen (midden-x, y) -> script; elke steen is drie tiles breed
        (5, 6): 'Moon', (5, 9): 'Sun', (5, 12): 'LowTide', (5, 15): 'Magikarp',
        (11, 6): 'Wailord', (11, 9): 'HighTide', (11, 12): 'Storm', (11, 15): 'Ranger',
        (16, 6): 'Riddle', (16, 9): 'Notice'}
    bgs = []
    for (sx, sy), nm in stones.items():
        for dx in ((-1, 0, 1) if sx != 16 else (0,)):
            bgs.append(sign(sx + dx, sy, 'SeaTemple_Hall_EventScript_Stone' + nm))
    for dx in (9, 10, 11):
        bgs.append(sign(dx, 2, 'SeaTemple_Hall_EventScript_Door'))
    base_map('SeaTemple_Hall', 'SEA_TEMPLE_HALL', 'SealedChamber_OuterRoom', 'SEA_TEMPLE_HALL', [],
             [{'x': 10, 'y': 2, 'elevation': 0, 'dest_map': 'MAP_SEA_TEMPLE_SANCTUM', 'dest_warp_id': '0'}], bgs,
             region_map_section='MAPSEC_SEA_TEMPLE', show_map_name=True)
    oq.register_map('SeaTemple_Hall')

    # --- SeaTemple_Sanctum: kopie van SealedChamber_InnerRoom
    W, H = 21, 23
    g = oq.read_layout('data/layouts/SealedChamber_InnerRoom/map.bin', W, H)
    save(g, 'SeaTemple_Sanctum', 'data/layouts/SealedChamber_InnerRoom/border.bin')
    oq.register_layout('SeaTemple_Sanctum', 'SEA_TEMPLE_SANCTUM', W, H, 'gTileset_Cave')
    objs = [oq.obj('OBJ_EVENT_GFX_SPECIES(MANAPHY)', 10, 8, 'SeaTemple_Sanctum_EventScript_Manaphy',
                   'FLAG_CAUGHT_SEA_TEMPLE_MANAPHY', 'LOCALID_SEA_TEMPLE_MANAPHY'),
            oq.obj('OBJ_EVENT_GFX_ITEM_BALL', 10, 6, 'SeaTemple_Sanctum_EventScript_Egg',
                   'FLAG_TEMP_1', 'LOCALID_SEA_TEMPLE_EGG')]
    bgs = [sign(x, 4, 'SeaTemple_Sanctum_EventScript_BackWall') for x in (9, 10, 11)]
    for (x, y), nm in {(6, 8): '1', (14, 8): '2', (4, 13): '3', (16, 13): '4', (6, 18): '5', (14, 18): '6'}.items():
        bgs.append(sign(x, y, 'SeaTemple_Sanctum_EventScript_Mural' + nm))
    base_map('SeaTemple_Sanctum', 'SEA_TEMPLE_SANCTUM', 'SealedChamber_InnerRoom', 'SEA_TEMPLE_SANCTUM', objs,
             [{'x': 10, 'y': 19, 'elevation': 0, 'dest_map': 'MAP_SEA_TEMPLE_HALL', 'dest_warp_id': '0'}], bgs,
             region_map_section='MAPSEC_SEA_TEMPLE', show_map_name=False)
    oq.register_map('SeaTemple_Sanctum')

    # bereikbaarheid
    hall = oq.read_layout('data/layouts/SeaTemple_Hall/map.bin', 21, 23)
    r = oq.reach(hall, [(10, 18)])
    assert (10, 3) in r, 'tempeldeur onbereikbaar'
    for (sx, sy) in stones:
        assert any(n in r for n in ((sx, sy + 1), (sx - 1, sy + 1), (sx + 1, sy + 1), (sx, sy - 1))), ('steen', sx, sy)
    san = oq.read_layout('data/layouts/SeaTemple_Sanctum/map.bin', 21, 23)
    r = oq.reach(san, [(10, 19)])
    assert (10, 9) in r and (10, 7) in r, 'Manaphy/ei onbereikbaar'
    uw = oq.read_layout('data/layouts/Underwater_SeaTemple/map.bin', 22, 48)
    assert EMERGE_TEMPLE in oq.reach(uw, [(7, 2)]), 'plateau onbereikbaar'
    print('zeetempel: %d zeewiertiles' % weed)

# =============================================================== Whirl Island
R124_HOLE = (13, 24)
WI_W, WI_H = 40, 40
OX, OY = 8, 8                  # waar de Shoal Cave-berg (Route 125, x15-38, y0-23) komt
SRC_X0, SRC_Y0, SRC_W, SRC_H = 15, 0, 24, 24
WHIRL = (0x150, 0x151, 0x158, 0x159)
ROCK = (0x175, 0x176, 0x17d, 0x17e)
DEEP = 0x14e
SHOAL_MS = {(1, 1, 1, 1): 0x19e, (0, 1, 1, 1): 0x19b, (1, 0, 1, 1): 0x19c, (1, 1, 1, 0): 0x1a4, (1, 1, 0, 1): 0x1a3,
            (0, 0, 1, 1): 0x1ae, (1, 1, 0, 0): 0x1be, (0, 1, 0, 1): 0x1b5, (1, 0, 1, 0): 0x1b7,
            (0, 0, 0, 1): 0x1ad, (0, 0, 1, 0): 0x1af, (0, 1, 0, 0): 0x1bd, (1, 0, 0, 0): 0x1bf, (0, 0, 0, 0): 0x170}
MERGED_WHIRL = {0x163, 0x16b, 0x162, 0x16a, 0x168, 0x169}    # draaikolk half in een bergrand
EMERGE_LAGOON = (20, 33)       # hier kom je boven (diep water, ook terug duiken)
CAVE_DOOR = (22 - SRC_X0 + OX, 19 - SRC_Y0 + OY)

def whirl_island():
    src = oq.read_layout('data/layouts/Route125/map.bin', 80, 40)
    W, H = WI_W, WI_H
    M = [[0x170] * W for _ in range(H)]
    mountain = set()
    for sy in range(SRC_H):
        for sx in range(SRC_W):
            t = src[SRC_Y0 + sy][SRC_X0 + sx]
            m = t & 0x3ff
            if (t & SOLID and m not in WHIRL and m not in MERGED_WHIRL and m not in ROCK) or m == 0xa7:
                if m in (0x33b, 0x33c, 0x33d, 0x17d, 0x17e, 0x175, 0x176):
                    continue
                x, y = OX + sx, OY + sy
                M[y][x] = t
                mountain.add((x, y))
    # de westrand van het stuk (x15) hoort niet bij de berg; alleen aaneengesloten berg rond de grotdeur houden
    keep, st = {CAVE_DOOR}, [CAVE_DOOR]
    while st:
        x, y = st.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)):
            if n in mountain and n not in keep:
                keep.add(n); st.append(n)
    for c in mountain - keep:
        M[c[1]][c[0]] = 0x170
    mountain = keep
    # ondiepte: hoekpunten rond de berg (1 tile rand, onderaan bij de deur 3)
    V = [[0] * (W + 1) for _ in range(H + 1)]
    TOPW = {0x202, 0x173, 0x203}     # bovenrand van de berg met open zee erboven (geen ondiepte erboven)
    for (x, y) in mountain:
        for dy in (range(1, 3) if M[y][x] & 0x3ff in TOPW else range(-1, 3)):
            for dx in range(-1, 3):
                V[y + dy][x + dx] = 1
    dx0, dy0 = CAVE_DOOR
    for y in range(dy0, dy0 + 5):
        for x in range(dx0 - 3, dx0 + 5):
            V[y][x] = 1
    prot = {(vx, vy) for (x, y) in mountain if M[y][x] & 0x3ff not in TOPW
            for vx in (x, x + 1) for vy in (y, y + 1)}
    for (x, y) in mountain:            # boven een bovenrand: open zee (de tile heeft zelf al een waterrand)
        if M[y][x] & 0x3ff in TOPW:
            for vx in (x, x + 1):
                if (vx, y) not in prot:
                    V[y][vx] = 0
    # geen diagonale hoekpunten
    changed = True
    while changed:
        changed = False
        for y in range(H):
            for x in range(W):
                q = (V[y][x], V[y][x + 1], V[y + 1][x], V[y + 1][x + 1])
                if q in ((1, 0, 0, 1), (0, 1, 1, 0)):
                    V[y][x] = V[y][x + 1] = V[y + 1][x] = V[y + 1][x + 1] = 1; changed = True
    for y in range(H):
        for x in range(W):
            if (x, y) in mountain:
                q = (V[y][x], V[y][x + 1], V[y + 1][x], V[y + 1][x + 1])
                assert q == (1, 1, 1, 1) or (M[y][x] & 0x3ff in TOPW and q[2:] == (1, 1)), ('berg op de rand', x, y)
                continue
            M[y][x] = SHOAL_MS[(V[y][x], V[y][x + 1], V[y + 1][x], V[y + 1][x + 1])]
    shoal = {(x, y) for y in range(H) for x in range(W) if M[y][x] != 0x170 and (x, y) not in mountain}

    def free2(x, y, gap=1):
        for yy in range(y - gap, y + 2 + gap):
            for xx in range(x - gap, x + 2 + gap):
                if not (0 <= xx < W and 0 <= yy < H) or (xx, yy) in mountain or (xx, yy) in shoal:
                    return False
        return True

    def stamp(x, y, piece):
        for i, mt in enumerate(piece):
            M[y + i // 2][x + i % 2] = mt | SOLID

    # ring van draaikolken (rand van de kaart, even coordinaten zoals de border), hier en daar een rots
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            if x in (0, W - 2) or y in (0, H - 2):
                stamp(x, y, ROCK if rng.random() < 0.18 else WHIRL)
    # tweede, rafelige ring
    for y in range(2, H - 2, 2):
        for x in range(2, W - 2, 2):
            edge = x in (2, W - 4) or y in (2, H - 4)
            if edge and rng.random() < 0.55 and free2(x, y, 0):
                stamp(x, y, ROCK if rng.random() < 0.3 else WHIRL)
    # diep water in de lagune: bovenkomen en terug duiken
    ex, ey = EMERGE_LAGOON
    for yy in (ey, ey + 1):
        for xx in (ex - 1, ex, ex + 1):
            assert M[yy][xx] == 0x170, ('diep water niet op zee', xx, yy)
            M[yy][xx] = DEEP
    # een paar losse draaikolken in de lagune (niet op het pad van de duikplek naar de ondiepte)
    path_keep = {(x, y) for y in range(ey - 6, ey + 3) for x in range(ex - 3, ex + 4)}
    tries = 0; placed = 0
    while placed < 6 and tries < 400:
        tries += 1
        x, y = rng.randrange(4, W - 6, 2), rng.randrange(4, H - 6, 2)
        if free2(x, y) and not any((x + a, y + b) in path_keep for a in range(-1, 3) for b in range(-1, 3)):
            stamp(x, y, WHIRL if placed % 2 == 0 else ROCK); placed += 1

    # bereikbaarheid: van de duikplek over water/ondiepte naar de grotdeur
    r = oq.reach(M, [EMERGE_LAGOON])
    assert CAVE_DOOR in r, 'grotdeur onbereikbaar vanaf de lagune'
    assert not any(M[y][x] & 0x3ff == 0x170 and (x, y) in r for x in (0, 1, W - 1, W - 2) for y in range(H)), 'ring lek'
    save(M, 'WhirlIsland', WHIRL)
    oq.register_layout('WhirlIsland', 'WHIRL_ISLAND', W, H, 'gTileset_Mossdeep')

    # --- Underwater_Route124: zwemgat
    UW, UH = 80, 80
    g = oq.read_layout('data/layouts/Underwater_Route124/map.bin', UW, UH)
    x, y = R124_HOLE
    assert all(g[y][x + d] & SOLID for d in (-1, 0, 1)) and not g[y + 1][x] & SOLID, 'gat niet in een noordwand'
    put_hole(g, x, y)
    oq.cx.save_grid(g, 'data/layouts/Underwater_Route124/map.bin')
    wi = oq.edit_map('Underwater_Route124', lambda m: (m.__setitem__('warp_events', m.get('warp_events') or []),
                                                       oq.warp_to(m, x, y + 1, 'MAP_UNDERWATER_WHIRL_ISLAND'))[1])

    # --- Underwater_WhirlIsland: kopie van de onderzeese grot van Sootopolis
    g = oq.read_layout('data/layouts/Underwater_SootopolisCity/map.bin', 20, 10)
    save(g, 'Underwater_WhirlIsland', 'data/layouts/Underwater_SootopolisCity/border.bin')
    oq.register_layout('Underwater_WhirlIsland', 'UNDERWATER_WHIRL_ISLAND', 20, 10, 'gTileset_Underwater')
    base_map('Underwater_WhirlIsland', 'UNDERWATER_WHIRL_ISLAND', 'Underwater_SootopolisCity', 'UNDERWATER_WHIRL_ISLAND', [],
             [{'x': 9, 'y': 8, 'elevation': 0, 'dest_map': 'MAP_UNDERWATER_ROUTE124', 'dest_warp_id': str(wi)},
              {'x': 10, 'y': 8, 'elevation': 0, 'dest_map': 'MAP_UNDERWATER_ROUTE124', 'dest_warp_id': str(wi)}],
             region_map_section='MAPSEC_WHIRL_ISLAND', show_map_name=True)
    oq.register_map('Underwater_WhirlIsland')

    # --- WhirlIsland (boven)
    base_map('WhirlIsland', 'WHIRL_ISLAND', 'Route125', 'WHIRL_ISLAND', [],
             [{'x': CAVE_DOOR[0], 'y': CAVE_DOOR[1], 'elevation': 0, 'dest_map': 'MAP_WHIRL_ISLAND_CAVE', 'dest_warp_id': '0'}],
             [sign(CAVE_DOOR[0] + 2, CAVE_DOOR[1] + 2, 'WhirlIsland_EventScript_Bottle')],
             region_map_section='MAPSEC_WHIRL_ISLAND', show_map_name=True, music='MUS_ROUTE119',
             weather='WEATHER_RAIN', map_type='MAP_TYPE_OCEAN_ROUTE', allow_cycling=False)
    oq.register_map('WhirlIsland')

    # --- WhirlIsland_Cave: kopie van MarineCave_End, Lugia op de plek van Kyogre
    g = oq.read_layout('data/layouts/MarineCave_End/map.bin', 27, 30)
    g[25][9] = (g[25][9] & 0x0fff) | (3 << 12)   # Lugia's tile op hoogte 3 (oever), anders is hij niet aan te spreken
    save(g, 'WhirlIsland_Cave', 'data/layouts/MarineCave_End/border.bin')
    oq.register_layout('WhirlIsland_Cave', 'WHIRL_ISLAND_CAVE', 27, 30, 'gTileset_Cave')
    # het meer is massief (zoals bij Kyogre); Lugia ligt aan de rand, aan te spreken vanaf de oever (9,26)
    lugia = oq.obj('OBJ_EVENT_GFX_SPECIES(LUGIA)', 9, 25, 'WhirlIsland_Cave_EventScript_Lugia', 'FLAG_TEMP_1',
                   'LOCALID_WHIRL_ISLAND_LUGIA', elev=3, move='MOVEMENT_TYPE_FACE_DOWN')
    assert (9, 26) in oq.reach(g, [(20, 4)]), 'oever bij Lugia onbereikbaar'
    base_map('WhirlIsland_Cave', 'WHIRL_ISLAND_CAVE', 'MarineCave_End', 'WHIRL_ISLAND_CAVE', [lugia],
             [{'x': 20, 'y': 4, 'elevation': 0, 'dest_map': 'MAP_WHIRL_ISLAND', 'dest_warp_id': '0'}],
             [sign(9, 25, 'WhirlIsland_Cave_EventScript_Lake')],
             region_map_section='MAPSEC_WHIRL_ISLAND', show_map_name=False, music='MUS_CAVE_OF_ORIGIN',
             weather='WEATHER_NONE')
    oq.register_map('WhirlIsland_Cave')
    print('Whirl Island: grotdeur', CAVE_DOOR, 'duikplek', EMERGE_LAGOON)


if __name__ == '__main__':
    sea_temple()
    whirl_island()
    if len(sys.argv) > 1:
        out = sys.argv[1]
        for mp in ('Underwater_SeaTemple', 'SeaTemple_Hall', 'SeaTemple_Sanctum', 'Underwater_WhirlIsland',
                   'WhirlIsland', 'WhirlIsland_Cave', 'Underwater_Route128', 'Underwater_Route124'):
            os.system('python3 tools/grounded/maptools/render_map.py %s %s/%s.png 0 120' % (mp, out, mp))


# zee_vulling_2.py zet later eilandjes op Whirl Island; meteen erna draaien, anders verdwijnen ze.
import subprocess as _sp  # noqa: E402
_sp.check_call([sys.executable, 'tools/grounded/maptools/zee_vulling_2.py'])
