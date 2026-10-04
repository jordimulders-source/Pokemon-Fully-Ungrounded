"""Project Grounded: optionele kamers in Victory Road (vette loot en events).

Bouwt vier nieuwe kaarten (General + Cave, zelfde stijl als Victory Road) en past de ingangen in
VictoryRoad_1F/B1F/B2F aan. Deterministisch en idempotent.

  WaitingRoom  (1F, grotopening (7,12) dicht met een Rock Smash-rots) Ace Trainer-gauntlet: drie
               Cooltrainers in de rij voor de Elite Four, gevonden voorwerpen aan het eind.
  Vault        (B1F, grotopening (6,16) in de gang linksonder)      Strength-blokpuzzel (door dit
               script opgelost en gecontroleerd), drie voorwerpen + een verstopt voorwerp.
  Hermit       (B2F, gat (20,1) op een eilandje in het bovenmeer; Surf)  REGINALD, de "vijfde" van de
               Elite Four (sterk team), geeft TM Flamethrower.
  SharkDen     (B1F, gat in de vloer (35,22) in een nis; je valt erin)   vaste Garchomp lv 58 op een
               schat; ladder terug naar B1F (36,22).

Controleert de bereikbaarheid (HM-poorten), de oplosbaarheid van de puzzel en dat je nooit vast
komt te zitten (de ingang blijft in elke puzzelstand bereikbaar).
Gebruik: python3 tools/grounded/maptools/victory_road_ext.py [voorbeeldmap]"""
import json, os, struct, sys
from collections import deque

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
os.chdir(REPO)

COL = 0x400
def T(mt, col=False, elev=0):
    return mt | (COL if col else 0) | (elev << 12)
F = T(0x201, elev=3)          # vloer (Granite/Victory Road-binnenvloer)
R = T(0x211, col=True)        # massieve rots
ROCKS = (0x202, 0x203)

# ---------------------------------------------------------------- bouwstenen
def blank(W, H):
    return [[R] * W for _ in range(H)]

def room(g, x0, y0, x1, y1):
    """Rechthoekige kamer: vloer x0..x1, y0..y1; twee rijen bovenwand, zijwanden, onderrand."""
    g[y0 - 2][x0 - 1] = T(0x21b, True); g[y0 - 2][x1 + 1] = T(0x21c, True)
    g[y0 - 1][x0 - 1] = T(0x212, True); g[y0 - 1][x1 + 1] = T(0x210, True)
    for x in range(x0, x1 + 1):
        g[y0 - 2][x] = T(0x219, True); g[y0 - 1][x] = T(0x219, True)
        g[y1 + 1][x] = T(0x221, True)
    for y in range(y0, y1 + 1):
        g[y][x0 - 1] = T(0x212, True); g[y][x1 + 1] = T(0x210, True)
        for x in range(x0, x1 + 1):
            g[y][x] = F
    g[y1 + 1][x0 - 1] = T(0x224, True); g[y1 + 1][x1 + 1] = T(0x224, True)

def door(g, x, ydoor, elev=3):
    """Grotopening: 20b/20c/20d boven, 213/214/215 op de deurrij (214 = deur, warp)."""
    g[ydoor - 1][x - 1:x + 2] = [T(0x20b, True), T(0x20c, True), T(0x20d, True)]
    g[ydoor][x - 1:x + 2] = [T(0x213, True), T(0x214, elev=elev), T(0x215, True)]

def ladder_up(g, x, y):
    """Ladder omhoog: 20f in de wand, 216 op de vloer (warp)."""
    g[y - 1][x] = T(0x20f, True); g[y][x] = T(0x216, elev=3)

def rock(g, x, y):
    g[y][x] = T(ROCKS[(x + y) % 2], True)

def carpet(g, x0, y0, x1, y1):
    """Zandvlek (Altering Cave): 298/299/29a, 2a0/2a1/2a2, 2a8/2a9/2aa."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            r = 0 if y == y0 else 2 if y == y1 else 1
            c = 0 if x == x0 else 2 if x == x1 else 1
            g[y][x] = T([[0x298, 0x299, 0x29a], [0x2a0, 0x2a1, 0x2a2], [0x2a8, 0x2a9, 0x2aa]][r][c], elev=3)

def walkable(t):
    return not t & 0xc00

# ---------------------------------------------------------------- bestanden
L = {l['id']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'id' in l}
def load_vr(name):
    l = L['LAYOUT_' + name]
    W, H = l['width'], l['height']
    v = list(struct.unpack('<%dH' % (W * H), open(l['blockdata_filepath'], 'rb').read()))
    return [v[y * W:(y + 1) * W] for y in range(H)], l['blockdata_filepath']

def save_grid(g, path):
    open(path, 'wb').write(struct.pack('<%dH' % (len(g) * len(g[0])), *[t for r in g for t in r]))

def obj(gfx, x, y, script, flag='0', ttype='TRAINER_TYPE_NONE', sight='0', move='MOVEMENT_TYPE_FACE_DOWN', local_id=None, elev=3):
    o = {}
    if local_id: o['local_id'] = local_id
    o.update({'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move,
              'movement_range_x': 0, 'movement_range_y': 0, 'trainer_type': ttype,
              'trainer_sight_or_berry_tree_id': sight, 'script': script, 'flag': flag})
    return o
def item(x, y, it, flag):
    return obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', flag, sight=it, move='MOVEMENT_TYPE_LOOK_AROUND')
def boulder(x, y, flag, elev=3):
    return obj('OBJ_EVENT_GFX_PUSHABLE_BOULDER', x, y, 'EventScript_StrengthBoulder', flag, move='MOVEMENT_TYPE_LOOK_AROUND', elev=elev)
def sign(x, y, script):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY', 'script': script}

# ---------------------------------------------------------------- 1. Wachtkamer (Ace Trainer-gauntlet)
def waiting_room():
    W, H = 13, 26
    g = blank(W, H)
    room(g, 2, 3, 10, 23)
    door(g, 6, 2)
    # rijen rotsen = de wachtrij; één opening, afwisselend rechts/links
    for y, gap in ((8, 10), (13, 2), (18, 10)):
        for x in range(2, 11):
            if x != gap: rock(g, x, y)
    # wat decor in de "wachtzaal" bovenin en bij de gevonden voorwerpen
    rock(g, 2, 3); rock(g, 10, 3); rock(g, 2, 23); rock(g, 10, 23)
    carpet(g, 4, 21, 8, 23)
    objs = [
        obj('OBJ_EVENT_GFX_MAN_3', 2, 9, 'VictoryRoad_WaitingRoom_EventScript_Brent', ttype='TRAINER_TYPE_NORMAL', sight='8', move='MOVEMENT_TYPE_FACE_RIGHT'),
        obj('OBJ_EVENT_GFX_WOMAN_5', 10, 14, 'VictoryRoad_WaitingRoom_EventScript_Nadia', ttype='TRAINER_TYPE_NORMAL', sight='8', move='MOVEMENT_TYPE_FACE_LEFT'),
        obj('OBJ_EVENT_GFX_MAN_3', 2, 19, 'VictoryRoad_WaitingRoom_EventScript_Oskar', ttype='TRAINER_TYPE_NORMAL', sight='8', move='MOVEMENT_TYPE_FACE_RIGHT'),
        item(5, 22, 'ITEM_CHOICE_SCARF', 'FLAG_ITEM_VICTORY_ROAD_WAITING_ROOM_CHOICE_SCARF'),
        item(7, 22, 'ITEM_CHOICE_SPECS', 'FLAG_ITEM_VICTORY_ROAD_WAITING_ROOM_CHOICE_SPECS'),
    ]
    # kaartjesautomaat = de rots rechtsboven; "gevonden voorwerpen" = de rots linksonder
    bgs = [sign(10, 3, 'VictoryRoad_WaitingRoom_EventScript_TicketSign'),
           sign(2, 23, 'VictoryRoad_WaitingRoom_EventScript_LostAndFound')]
    return g, W, H, objs, bgs, (6, 2)

# ---------------------------------------------------------------- 2. Schatkelder (Strength-puzzel)
VW, VH = 11, 9           # binnenmaat van de puzzel
def solve(rocks, items, boulders, start, door_cell, cap=40000):
    """BFS op duwen (Sokoban-toestand: blokken + gebied van de speler). Geeft per voorwerp het
    minimale aantal duwen om ernaast te staan (None = onbereikbaar) en of je jezelf kunt
    opsluiten (ingang onbereikbaar) terug. Voorwerpen tellen als obstakel. De blokken staan bij
    elk bezoek weer op hun plek, dus elk voorwerp mag in een eigen poging."""
    free = lambda c: 0 <= c[0] < VW and 0 <= c[1] < VH and c not in rocks and c not in items
    adj = [[(it[0] + dx, it[1] + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))] for it in items]
    def region(p, bs):
        seen = {p}; st = [p]
        while st:
            x, y = st.pop()
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n not in seen and free(n) and n not in bs:
                    seen.add(n); st.append(n)
        return seen
    b0 = frozenset(boulders)
    q = deque([(start, b0, 0)]); seen = {(min(region(start, b0)), b0)}
    best = [None] * len(items); trap = False
    while q:
        p, bs, d = q.popleft()
        reg = region(p, bs)
        if door_cell not in reg:
            # een blok vóór de ingang is geen val als je hem opzij kunt duwen
            dx0, dy0 = door_cell
            ok = door_cell in bs and any((dx0 - dx, dy0 - dy) in reg and free((dx0 + dx, dy0 + dy)) and (dx0 + dx, dy0 + dy) not in bs
                                         for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if not ok: trap = True
        for i, a in enumerate(adj):
            if best[i] is None and any(c in reg for c in a): best[i] = d
        for b in bs:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                pc = (b[0] - dx, b[1] - dy); tc = (b[0] + dx, b[1] + dy)
                if pc in reg and free(tc) and tc not in bs:
                    nb = (bs - {b}) | {tc}
                    k = (min(region(b, nb)), nb)
                    if k not in seen:
                        seen.add(k); q.append((b, nb, d + 1))
                        if len(seen) > cap: return best, True
    return best, trap

# @ aankomst, B blok, # rots, 1-3 voorwerpen, h verstopt voorwerp. Bedoelde oplossing: het blok in
# de linkeringang 2x omlaag (parkeert in het nisje), via de linkervleugel naar het middenblok en dat
# naar rechts het nisje in duwen; wie het middenblok van bovenaf omlaag duwt, zet de schat klem
# (opnieuw binnenkomen zet alles terug). De rechtervleugel (2x duwen) heeft het verstopte voorwerp.
VAULT = [
    '.....@.....',
    '...........',
    '##B##.###B#',
    '#...#.##...',
    '#...#.##...',
    '#.#..B.#.#.',
    '#.###.##.#.',
    '#.###.##.#.',
    '#1##2.3#.#h',
]
VAULT_ITEMS = {'1': 'BIG_NUGGET', '2': 'ABILITY_CAPSULE', '3': 'PP_MAX'}

def vault():
    rocks, boulders, items, hidden = set(), [], {}, None
    for y, row in enumerate(VAULT):
        for x, c in enumerate(row):
            if c == '#': rocks.add((x, y))
            elif c == 'B': boulders.append((x, y))
            elif c in VAULT_ITEMS: items[c] = (x, y)
            elif c == 'h': hidden = (x, y)
            elif c == '@': start = (x, y)
    targets = [items[k] for k in sorted(items)]
    best, trap = solve(rocks, targets + [hidden], boulders, start, start, cap=200000)
    assert None not in best and not trap and min(best) > 0, 'kluispuzzel klopt niet: %s %s' % (best, trap)
    print('kluis: duwen per voorwerp (1,2,3,verstopt) =', best)
    ox, oy = 2, 3            # puzzel-oorsprong in de kaart
    W, H = VW + 4, VH + 6
    g = blank(W, H)
    room(g, ox, oy, ox + VW - 1, oy + VH - 1)
    door(g, ox + start[0], oy - 1)
    for x, y in rocks: rock(g, ox + x, oy + y)
    objs = [item(ox + x, oy + y, 'ITEM_' + VAULT_ITEMS[k], 'FLAG_ITEM_VICTORY_ROAD_VAULT_' + VAULT_ITEMS[k]) for k, (x, y) in sorted(items.items())]
    objs += [boulder(ox + x, oy + y, 'FLAG_TEMP_%X' % (0x11 + i)) for i, (x, y) in enumerate(boulders)]
    bgs = [sign(ox + start[0] - 1, oy - 1, 'VictoryRoad_Vault_EventScript_Sign'),  # inscriptie links van de opening
           {'type': 'hidden_item', 'x': ox + hidden[0], 'y': oy + hidden[1], 'elevation': 3, 'item': 'ITEM_MAX_ELIXIR',
            'flag': 'FLAG_HIDDEN_ITEM_VICTORY_ROAD_VAULT_MAX_ELIXIR'}]
    return g, W, H, objs, bgs, (ox + start[0], oy - 1)

# ---------------------------------------------------------------- 3. Kluizenaar (ex-Elite Four-kandidaat)
def hermit():
    W, H = 17, 14
    g = blank(W, H)
    room(g, 2, 3, 14, 11)
    ladder_up(g, 4, 3)
    carpet(g, 7, 5, 11, 8)
    for x, y in ((2, 11), (3, 11), (14, 11), (14, 10), (14, 3), (13, 3), (2, 7)):
        rock(g, x, y)
    objs = [
        obj('OBJ_EVENT_GFX_EXPERT_M', 9, 6, 'VictoryRoad_Hermit_EventScript_Reginald', local_id='LOCALID_VR_HERMIT_REGINALD'),
        item(13, 10, 'ITEM_EXPERT_BELT', 'FLAG_ITEM_VICTORY_ROAD_HERMIT_EXPERT_BELT'),
    ]
    bgs = [sign(13, 3, 'VictoryRoad_Hermit_EventScript_Application')]
    return g, W, H, objs, bgs, (4, 3)

# ---------------------------------------------------------------- 4. Haaienbak (Garchomp + schat)
HOLE = (35, 22)          # gat in VictoryRoad_B1F; je landt op dezelfde coördinaten
def shark_den():
    W, H = 42, 27
    g = blank(W, H)
    room(g, 28, 15, 39, 24)
    ladder_up(g, 30, 15)
    carpet(g, 31, 18, 36, 20)
    for x, y in ((28, 24), (29, 24), (39, 24), (39, 23), (39, 15), (38, 15), (28, 19), (37, 17)):
        rock(g, x, y)
    assert walkable(g[HOLE[1]][HOLE[0]])
    objs = [
        obj('OBJ_EVENT_GFX_SPECIES(GARCHOMP)', 33, 19, 'VictoryRoad_SharkDen_EventScript_Garchomp', 'FLAG_HIDE_VICTORY_ROAD_GARCHOMP',
            local_id='LOCALID_VR_SHARK_DEN_GARCHOMP'),
        item(31, 18, 'ITEM_LIFE_ORB', 'FLAG_ITEM_VICTORY_ROAD_SHARK_DEN_LIFE_ORB'),
        item(36, 18, 'ITEM_EVIOLITE', 'FLAG_ITEM_VICTORY_ROAD_SHARK_DEN_EVIOLITE'),
        item(34, 20, 'ITEM_DRAGON_FANG', 'FLAG_ITEM_VICTORY_ROAD_SHARK_DEN_DRAGON_FANG'),
    ]
    bgs = [sign(28, 19, 'VictoryRoad_SharkDen_EventScript_Backpacks')]
    return g, W, H, objs, bgs, (30, 15)

# ---------------------------------------------------------------- bereikbaarheid in een kamer
def reach_room(g, start, objs, extra_block=()):
    W, H = len(g[0]), len(g)
    block = {(o['x'], o['y']) for o in objs} | set(extra_block)
    seen = {start}; st = [start]
    while st:
        x, y = st.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen and walkable(g[n[1]][n[0]]) and n not in block:
                seen.add(n); st.append(n)
    return seen

def check_room(name, g, start, objs, skip_boulders=False):
    blocking = [o for o in objs if not (skip_boulders and o['graphics_id'] == 'OBJ_EVENT_GFX_PUSHABLE_BOULDER')]
    reg = reach_room(g, start, blocking)
    for o in objs:
        if skip_boulders and o['graphics_id'] in ('OBJ_EVENT_GFX_PUSHABLE_BOULDER', 'OBJ_EVENT_GFX_ITEM_BALL'): continue
        ok = any((o['x'] + dx, o['y'] + dy) in reg for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        assert ok, '%s: %s op (%d,%d) onbereikbaar' % (name, o['script'], o['x'], o['y'])
    return reg

# ---------------------------------------------------------------- registratie
NEW = [('VictoryRoad_WaitingRoom', 'VICTORY_ROAD_WAITING_ROOM', False),
       ('VictoryRoad_Vault', 'VICTORY_ROAD_VAULT', False),
       ('VictoryRoad_Hermit', 'VICTORY_ROAD_HERMIT', False),
       ('VictoryRoad_SharkDen', 'VICTORY_ROAD_SHARK_DEN', True)]

def register_layout(name, const, W, H):
    lj = open('data/layouts/layouts.json').read()
    entry = '''
    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_Cave",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    },''' % (const, name, W, H, name, name)
    if '"LAYOUT_%s"' % const in lj:
        i = lj.index('"id": "LAYOUT_%s"' % const); s = lj.rindex('{', 0, i); e = lj.index('},', i) + 2
        lj = lj[:s - 5] + entry + lj[e:]
    else:
        i = lj.index('"id": "LAYOUT_VICTORY_ROAD_B2F"'); j = lj.index('},', i) + 2
        lj = lj[:j] + entry + lj[j:]
    open('data/layouts/layouts.json', 'w').write(lj)

def write_map(name, const, dark, objs, warps, bgs):
    base = json.load(open('data/maps/VictoryRoad_B1F/map.json'))
    m = {k: base[k] for k in base}
    m.update({'id': 'MAP_' + const, 'name': name, 'layout': 'LAYOUT_' + const, 'requires_flash': dark,
              'show_map_name': False, 'connections': None, 'object_events': objs, 'warp_events': warps,
              'coord_events': [], 'bg_events': bgs})
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')

def register_map(name):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        i = g.index('"gMapGroup_Grounded": ['); j = g.index(']', i)
        body = g[i:j].rstrip()
        g = g[:i] + body + ',\n    "%s"\n  ' % name + g[j:]
        open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/ShoalCave_LowTideEntranceRoom/scripts.inc"\n'   # direct na Victory Road
        es = es.replace(anchor, inc + anchor, 1)
        open('data/event_scripts.s', 'w').write(es)

def set_warp(m, x, y, elev, dest, dest_id):
    """Voegt een warp toe (of werkt hem bij) en geeft de index terug."""
    for i, w in enumerate(m['warp_events']):
        if w['x'] == x and w['y'] == y:
            w.update({'elevation': elev, 'dest_map': dest, 'dest_warp_id': str(dest_id)}); return i
    m['warp_events'].append({'x': x, 'y': y, 'elevation': elev, 'dest_map': dest, 'dest_warp_id': str(dest_id)})
    return len(m['warp_events']) - 1

def set_obj(m, o):
    for e in m['object_events']:
        if e['x'] == o['x'] and e['y'] == o['y']:
            e.clear(); e.update(o); return
    m['object_events'].append(o)

# ---------------------------------------------------------------- Victory Road zelf
def vr_reach(g, starts, surf=False, passable=()):
    """Bereikbaarheid op een VR-kaart met hoogteregels (0/15 = elke hoogte, water = hoogte 1)."""
    W, H = len(g[0]), len(g)
    def el(t): return t >> 12
    def ok(a, b):
        ea, eb = el(a), el(b)
        if ea in (0, 15) or eb in (0, 15) or ea == eb: return True
        return surf and {ea, eb} == {1, 3}
    seen = set(starts); st = list(starts)
    while st:
        x, y = st.pop()
        for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= n[0] < W and 0 <= n[1] < H and n not in seen:
                t = g[n[1]][n[0]]
                if (walkable(t) or n in passable) and ok(g[y][x], t) and (surf or el(t) != 1):
                    seen.add(n); st.append(n)
    return seen

def main():
    rooms = {'VictoryRoad_WaitingRoom': waiting_room(), 'VictoryRoad_Vault': vault(),
             'VictoryRoad_Hermit': hermit(), 'VictoryRoad_SharkDen': shark_den()}

    # --- Victory Road-kaarten aanpassen
    m1 = json.load(open('data/maps/VictoryRoad_1F/map.json'))
    mb1 = json.load(open('data/maps/VictoryRoad_B1F/map.json'))
    mb2 = json.load(open('data/maps/VictoryRoad_B2F/map.json'))
    g1, p1 = load_vr('VICTORY_ROAD_1F'); gb1, pb1 = load_vr('VICTORY_ROAD_B1F'); gb2, pb2 = load_vr('VICTORY_ROAD_B2F')

    # 1F: grotopening in de noordwand linksboven, dichtgezet met een Rock Smash-rots OP de opening
    # (niet ervoor: bij terugkomst loop je automatisch een stap uit de opening, dwars door objecten heen).
    # Vaste flag, dus eenmaal kapot blijft hij weg.
    door(g1, 7, 12, elev=4)
    w1 = set_warp(m1, 7, 12, 4, 'MAP_VICTORY_ROAD_WAITING_ROOM', 0)
    set_obj(m1, obj('OBJ_EVENT_GFX_BREAKABLE_ROCK', 7, 12, 'EventScript_RockSmash', 'FLAG_VICTORY_ROAD_WAITING_ROOM_ROCK', move='MOVEMENT_TYPE_LOOK_AROUND', elev=4))
    # B1F: grotopening in de noordwand van de gang linksonder (de Strength-puzzel zit binnen)
    door(gb1, 6, 16)
    wb1 = set_warp(mb1, 6, 16, 3, 'MAP_VICTORY_ROAD_VAULT', 0)
    # B1F: gat in de vloer in de nis rechts; aankomstpunt (gewone vloer) ernaast voor de ladder terug
    gb1[HOLE[1]][HOLE[0]] = T(0x206, elev=3)
    wb1b = set_warp(mb1, 36, 22, 3, 'MAP_VICTORY_ROAD_SHARK_DEN', 0)
    # B2F: eilandje in het bovenmeer (kopie van het ladder-eiland (17-21, 12-14)) met een gat omlaag
    src = [row[17:22] for row in gb2[12:15]]
    for dy in range(3):
        for dx in range(5):
            gb2[1 + dy][18 + dx] = src[dy][dx]
    gb2[1][20] = T(0x205, elev=3)
    wb2 = set_warp(mb2, 20, 1, 3, 'MAP_VICTORY_ROAD_HERMIT', 0)

    # --- bereikbaarheid in Victory Road (met HM's; rotsen/blokken als passeerbaar)
    r = vr_reach(g1, [(9, 14)])
    assert (7, 13) in r and (7, 12) in r, '1F: opening Wachtkamer onbereikbaar'
    r = vr_reach(gb1, [(17, 16)])          # gebied van de ladders (17,16)/(20,21)/(5,26)
    assert (6, 17) in r and (6, 16) in r, 'B1F: opening Kluis onbereikbaar'
    r = vr_reach(gb1, [(42, 25)])          # gebied van de ladders (42,25)/(30,25)/(8,3)
    assert HOLE in r and (36, 22) in r, 'B1F: gat Haaienbak onbereikbaar'
    r = vr_reach(gb2, [(3, 8)], surf=True)
    assert (20, 1) in r, 'B2F: eiland onbereikbaar'
    assert (20, 1) not in vr_reach(gb2, [(3, 8)], surf=False), 'B2F: eiland hoort Surf te vereisen'

    save_grid(g1, p1); save_grid(gb1, pb1); save_grid(gb2, pb2)
    for m, n in ((m1, 'VictoryRoad_1F'), (mb1, 'VictoryRoad_B1F'), (mb2, 'VictoryRoad_B2F')):
        open('data/maps/%s/map.json' % n, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')

    back = {'VictoryRoad_WaitingRoom': ('MAP_VICTORY_ROAD_1F', w1), 'VictoryRoad_Vault': ('MAP_VICTORY_ROAD_B1F', wb1),
            'VictoryRoad_Hermit': ('MAP_VICTORY_ROAD_B2F', wb2), 'VictoryRoad_SharkDen': ('MAP_VICTORY_ROAD_B1F', wb1b)}
    for name, const, dark in NEW:
        g, W, H, objs, bgs, warp = rooms[name]
        # bereikbaarheid vanaf de aankomst
        start = (warp[0], warp[1] + 1) if name in ('VictoryRoad_WaitingRoom', 'VictoryRoad_Vault') else (warp[0], warp[1] + 1)
        check_room(name, g, start, objs, skip_boulders=(name == 'VictoryRoad_Vault'))
        if name == 'VictoryRoad_SharkDen':
            assert HOLE in reach_room(g, start, objs), 'Haaienbak: landingsplek niet verbonden met de ladder'
        os.makedirs('data/layouts/' + name, exist_ok=True)
        save_grid(g, 'data/layouts/%s/map.bin' % name)
        save_grid([[R, R], [R, R]], 'data/layouts/%s/border.bin' % name)
        register_layout(name, const, W, H)
        dest, did = back[name]
        write_map(name, const, dark, objs, [{'x': warp[0], 'y': warp[1], 'elevation': 3, 'dest_map': dest, 'dest_warp_id': str(did)}], bgs)
        register_map(name)
    if len(sys.argv) > 1:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from gridrender import render
        from PIL import Image
        ims = [render(rooms[n][0]) for n, _, _ in NEW]
        out = Image.new('RGB', (sum(i.width for i in ims) + 16 * len(ims), max(i.height for i in ims)), 'black')
        x = 0
        for i in ims: out.paste(i, (x, 0)); x += i.width + 16
        out.save(sys.argv[1])
    print('klaar; warps 1F %d, B1F %d/%d, B2F %d' % (w1, wb1, wb1b, wb2))

if __name__ == '__main__':
    main()
