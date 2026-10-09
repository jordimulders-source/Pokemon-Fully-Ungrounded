"""Project Grounded: zeevulling 4 (onderwater + diepzeetrog + de dunste zeeroutes).

Onderwater:
- Elke onderwaterkaart heeft nu wilde Pokemon: nieuwe tabellen voor Sootopolis (kratermond), Whirl Island, Marine
  Cave (buiten), Route 134, de Sealed Chamber-trog (buitenkant), Scorched Slab, Seafloor Cavern (ingang) en
  Route 136. Op de kleine 'grotmond'-kaarten zijn de diepe tegels (MB_DEEP_WATER) al encountertegels; de twee lange
  troggen (Sealed Chamber, Route 136) krijgen zeewier.
- Extra zeewier op onderwater 125/127/128/129.
- Duikers op de zeebodem (Swimmer-trainers) op onderwater 105, 125, 126, 128 en in de trog; duiker-NPC's op 124/129.
- Verborgen items op elke onderwaterkaart (ook een paar grotere vondsten) en een verhaalbord op 126.
Diepzeetrog:
- Underwater_Route127_Trench: nieuwe kaart (kopie van de Sealed Chamber-trog, 14 rijen dieper), via een zwemgat in de
  kop van de centrale trog van onderwater 127 (24,12). Eigen diepzee-tabel, items, een diepzeeduiker en een geheim.
  Sinds 9 okt bouwt trog127.py het onderste deel (zigzaggebied, tweede zwemgat naar onderwater 128) en verplaatst hij de
  trogitems: draai trog127.py (en daarna coral_cathedral.py) na dit script.
Bovenwater:
- Verborgen items op Route 126/127/128/130/132/133/134; oceanograaf (127), Parasol Lady op een eilandje (128),
  zwemmende Tuber + fotograaf (130), Ruin Maniac (134).

Werkt als zee_vulling_3.py (gekopieerde hulpjes; markeringen ZV4, eigen _orig.json, trainers 1187-1199,
flags FLAG_GROUNDED(330)-(429)). Idempotent.
Gebruik (vanuit de repo-root): python3 tools/grounded/maptools/zee_vulling_4.py
"""
import json, os, random, re, struct, sys
from collections import deque

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
random.seed(1094)
BLOCK = 1 << 10

BEH = {}
for l in open('include/constants/metatile_behaviors.h'):
    m = re.match(r'\s*(MB_\w+)', l)
    if m and m.group(1) not in BEH:
        BEH[m.group(1)] = len(BEH)
MB = {v: k for k, v in BEH.items()}


def attrs(path):
    a = open(path, 'rb').read()
    return [struct.unpack_from('<H', a, i * 2)[0] for i in range(len(a) // 2)]


def tsname(sym):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', sym.replace('gTileset_', '')).lower()


GEN = attrs('data/tilesets/primary/general/metatile_attributes.bin')
LAYOUTS = {l['id']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'id' in l}
SECS = {}
SURF = {'MB_OCEAN_WATER', 'MB_DEEP_WATER', 'MB_POND_WATER', 'MB_SEAWEED', 'MB_NO_SURFACING', 'MB_SEAWEED_NO_SURFACING',
        'MB_WESTWARD_CURRENT', 'MB_EASTWARD_CURRENT', 'MB_NORTHWARD_CURRENT', 'MB_SOUTHWARD_CURRENT', 'MB_INTERIOR_DEEP_WATER'}
CURRENT = {'MB_WESTWARD_CURRENT': (-1, 0), 'MB_EASTWARD_CURRENT': (1, 0), 'MB_NORTHWARD_CURRENT': (0, -1),
           'MB_SOUTHWARD_CURRENT': (0, 1)}

ORIG_PATH = 'tools/grounded/maptools/zee_vulling_4_orig.json'
ORIG = json.load(open(ORIG_PATH)) if os.path.exists(ORIG_PATH) else {}


class Map:
    def __init__(self, name):
        self.name = name
        self.json = json.load(open('data/maps/%s/map.json' % name))
        L = LAYOUTS[self.json['layout']]
        self.layout = L['name']
        self.w, self.h = L['width'], L['height']
        self.path = L['blockdata_filepath']
        sec = tsname(L['secondary_tileset'])
        if sec not in SECS:
            SECS[sec] = attrs('data/tilesets/secondary/%s/metatile_attributes.bin' % sec)
        self.sec = SECS[sec]
        self.underwater = self.json.get('map_type') == 'MAP_TYPE_UNDERWATER'
        b = open(self.path, 'rb').read()
        assert len(b) == self.w * self.h * 2, name
        self.v = [[struct.unpack_from('<H', b, (y * self.w + x) * 2)[0] for x in range(self.w)] for y in range(self.h)]
        for k, c in ORIG.get(self.layout, {}).items():  # alles wat dit script ooit overschreef terugzetten
            x, y = map(int, k.split(','))
            self.v[y][x] = c

    def beh(self, c):
        mt = c & 0x3FF
        a = GEN[mt] if mt < 0x200 else self.sec[mt - 0x200]
        return MB.get(a & 0xFF, a & 0xFF)

    def cell(self, mt, blocked=False):
        return mt | ((1 if self.beh(mt) in SURF else 3) << 12) | (BLOCK if blocked else 0)

    def elev(self, x, y):
        return (self.v[y][x] >> 12) & 0xF

    def put(self, x, y, c):
        ORIG.setdefault(self.layout, {}).setdefault('%d,%d' % (x, y), self.v[y][x])
        self.v[y][x] = c

    def save(self):
        open(self.path, 'wb').write(b''.join(struct.pack('<H', c) for r in self.v for c in r))
        json.dump(ORIG, open(ORIG_PATH, 'w'), indent=0, sort_keys=True)  # meteen, zodat een afgebroken run herstelbaar blijft


# --- General-autotile (zelfde tiles als zee_vulling_3.py) ---
RING = {'TL': 0x1AD, 'T': 0x1AE, 'TR': 0x1AF, 'L': 0x1B5, 'R': 0x1B7, 'BL': 0x1BD, 'B': 0x1BE, 'BR': 0x1BF,
        'NW': 0x19B, 'NE': 0x19C, 'SW': 0x1A3, 'SE': 0x1A4, 'C': 0x19E}
SAND = {'C': 0x124, 'TL': 0x195, 'T': 0x196, 'TR': 0x197, 'L': 0x19D, 'R': 0x19F, 'BL': 0x1A5, 'B': 0x1A6,
        'BR': 0x1A7, 'NW': 0x185, 'NE': 0x186, 'SW': 0x18D, 'SE': 0x18E}
ROCK_SAND = [0x0A3, 0x0A4, 0x0AB, 0x0AC]


def shape(S, x, y):
    has = lambda dx, dy: (x + dx, y + dy) in S
    n, s, w, e = has(0, -1), has(0, 1), has(-1, 0), has(1, 0)
    if not n and not w: return 'TL'
    if not n and not e: return 'TR'
    if not s and not w: return 'BL'
    if not s and not e: return 'BR'
    if not n: return 'T'
    if not s: return 'B'
    if not w: return 'L'
    if not e: return 'R'
    if not has(-1, -1): return 'NW'
    if not has(1, -1): return 'NE'
    if not has(-1, 1): return 'SW'
    if not has(1, 1): return 'SE'
    return 'C'


def rect(x0, y0, x1, y1):
    return {(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)}


NEED = {'TL': 'e s se', 'TR': 'w s sw', 'BL': 'n e ne', 'BR': 'n w nw', 'T': 'w e s sw se', 'B': 'w e n nw ne',
        'L': 'n s e ne se', 'R': 'n s w nw sw', 'C': 'n s w e nw ne sw se'}
for _k, _d in (('NW', 'nw'), ('NE', 'ne'), ('SW', 'sw'), ('SE', 'se')):
    NEED[_k] = ' '.join(d for d in NEED['C'].split() if d != _d)
DIRS = {'n': (0, -1), 's': (0, 1), 'w': (-1, 0), 'e': (1, 0), 'nw': (-1, -1), 'ne': (1, -1), 'sw': (-1, 1), 'se': (1, 1)}


def tileable(S):
    for (x, y) in S:
        if not all((x + DIRS[d][0], y + DIRS[d][1]) in S for d in NEED[shape(S, x, y)].split()):
            return False
    return True


def dilate4(S):
    return S | {(x + dx, y + dy) for (x, y) in S for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))}


SEA_KEEP = {}


def keep_events(M):
    """Eilandjes mogen niet groeien over bestaande objecten/verborgen items (+- 2 tegels)."""
    keep = set()
    for e in M.json['object_events'] + M.json['bg_events'] + M.json['warp_events']:
        if 'ZV4' in e.get('flag', '') or 'ZV4' in e.get('script', ''):
            continue
        keep |= rect(e['x'] - 2, e['y'] - 2, e['x'] + 2, e['y'] + 2)
    SEA_KEEP[M.name] = keep


def organic(M, sand):
    """Rechthoekig zand -> organische vorm (zoals zee_vulling_3.py)."""
    rng = random.Random('zv4:%s:%d,%d' % (M.name, min(sand)[0], min(sand)[1]))
    xs, ys = [p[0] for p in sand], [p[1] for p in sand]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)

    def sea(x, y):
        if not (1 <= x < M.w - 1 and 1 <= y < M.h - 1):
            return False
        c = M.v[y][x]
        return M.beh(c) == 'MB_OCEAN_WATER' and not c & BLOCK

    S = set(sand)
    base = dilate4(dilate4(sand))
    want = max(5, x1 - x0 + y1 - y0)
    for _ in range(want * 20):
        if want <= 0:
            break
        side = rng.choice('nswe')
        bw, bh = rng.randint(3, 5), rng.randint(2, 3)
        if side in 'ns':
            bx = rng.randint(x0 - 1, max(x0 - 1, x1 - bw + 2))
            by = y0 - rng.randint(1, 2) if side == 'n' else y1 + rng.randint(1, 2) - bh + 1
        else:
            bh, bw = bw, bh
            by = rng.randint(y0 - 1, max(y0 - 1, y1 - bh + 2))
            bx = x0 - rng.randint(1, 2) if side == 'w' else x1 + rng.randint(1, 2) - bw + 1
        blob = rect(bx, by, bx + bw - 1, by + bh - 1)
        T = S | blob
        if not (S & blob) and not any((x + dx, y + dy) in S for (x, y) in blob for dx, dy in DIRS.values()):
            continue
        A = dilate4(T)
        if not tileable(T) or not tileable(A):
            continue
        if not all(sea(x, y) for p in dilate4(A) - base for x, y in [p]) or dilate4(A) & SEA_KEEP.get(M.name, set()):
            continue
        S = T
        want -= 1
    return dilate4(S), S


def islet(M, sand, rocks=()):
    area, sand = organic(M, sand)
    xs, ys = [p[0] for p in area], [p[1] for p in area]
    for cx, cy, dx, dy in ((min(xs), min(ys), 1, 1), (max(xs), min(ys), -1, 1), (min(xs), max(ys), 1, -1),
                           (max(xs), max(ys), -1, -1)):
        if (cx + dx, cy + dy) not in sand:
            area = area - {(cx, cy)}
    for (x, y) in area:
        c = M.v[y][x]
        assert M.beh(c) == 'MB_OCEAN_WATER' and not c & BLOCK, '%s: eiland op (%d,%d) overlapt %x %s' % (
            M.name, x, y, c & 0x3FF, M.beh(c))
    for (x, y) in area:
        M.put(x, y, M.cell(SAND[shape(sand, x, y)]) if (x, y) in sand else M.cell(RING[shape(area, x, y)]))
    for (px, py) in rocks:
        for i in range(4):
            cx, cy = px + i % 2, py + i // 2
            assert (M.v[cy][cx] & 0x3FF) == SAND['C'], '2x2-rots (%d,%d) niet op vol zand' % (px, py)
            M.put(cx, cy, M.cell(ROCK_SAND[i], True))


FAIL = []


def reach(M, start, targets, solid):
    """Surfen/zwemmen + lopen (alles zonder botsing), met glijden over stroomtegels."""
    w, h = M.w, M.h

    def free(x, y):
        return 0 <= x < w and 0 <= y < h and not M.v[y][x] & 0xC00 and (x, y) not in solid

    def slide(x, y):
        seen = set()
        while True:
            d = CURRENT.get(M.beh(M.v[y][x]))
            if not d or (x, y) in seen: return x, y
            seen.add((x, y))
            if not free(x + d[0], y + d[1]): return x, y
            x, y = x + d[0], y + d[1]

    assert free(*start), (M.name, 'start', start)
    s = slide(*start)
    seen, q = {s}, deque([s])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if free(x + dx, y + dy):
                p = slide(x + dx, y + dy)
                if p not in seen:
                    seen.add(p); q.append(p)
    return seen


# =====================================================================================================
# flags: FLAG_GROUNDED(330)-(429) (eigen blok in flags.h)
FLAGS_H = 'include/constants/flags.h'
FLAGS = {}         # naam -> (n, omschrijving)
FLAG_FIRST, FLAG_LAST = 330, 429
FBEGIN, FEND = '// zee_vulling_4 { (tools/grounded/maptools/zee_vulling_4.py; FLAG_GROUNDED 330-429)', '// } zee_vulling_4'


def flag(name, desc):
    if name in FLAGS:
        return name
    n = FLAG_FIRST + len(FLAGS)
    assert n <= FLAG_LAST, 'flags op'
    FLAGS[name] = (n, desc)
    return name


def write_flags():
    s = open(FLAGS_H).read()
    if FBEGIN in s:
        s = s[:s.index(FBEGIN)] + s[s.index(FEND) + len(FEND) + 1:]
    for name in FLAGS:
        assert not re.search(r'#define %s\b' % re.escape(name), s), 'vlag %s bestaat al' % name
    for n in range(FLAG_FIRST, FLAG_LAST + 1):
        assert 'FLAG_GROUNDED(%d)' % n not in s, 'FLAG_GROUNDED(%d) al in gebruik' % n
    block = FBEGIN + '\n' + ''.join('#define %-48s FLAG_GROUNDED(%d) // Project Grounded (zeevulling 4): %s\n'
                                    % (name, n, desc) for name, (n, desc) in FLAGS.items()) + FEND + '\n'
    anchor = '// Special Flags (Stored in EWRAM'
    assert anchor in s
    s = s.replace(anchor, block + '\n' + anchor, 1) if not s[:s.index(anchor)].endswith('\n\n') else \
        s.replace(anchor, block + '\n' + anchor, 1)
    s = re.sub(r'\n\n\n+(%s)' % re.escape(FBEGIN), r'\n\n\1', s)
    # verdeelregel bijwerken
    s = re.sub(r'(// Verdeling \(houd bij!\):[^\n]*?)(, 330-429 zeevulling 4 \(zee_vulling_4\.py\))?(, \d+\+ vrij\.|\.)\n',
               lambda m: m.group(1) + ', 330-429 zeevulling 4 (zee_vulling_4.py)' + m.group(3) + '\n', s, count=1)
    open(FLAGS_H, 'w').write(s)


# =====================================================================================================
# trainers (opponents.h + trainers.party), id's 1187-1199
TRAINERS = []
TBEGIN, TEND = '/* --- zee_vulling_4 (gegenereerd door tools/grounded/maptools/zee_vulling_4.py) --- */', '/* --- einde zee_vulling_4 --- */'
FIRST_ID, LAST_ID = 1187, 1199


def trainer(const, desc, header, mons):
    tid = FIRST_ID + len(TRAINERS)
    assert tid <= LAST_ID
    TRAINERS.append((const, tid, desc, '=== %s ===\n%s\n\n%s' % (const, header.strip(), mons.strip())))
    return const


def write_trainers():
    op = open('include/constants/opponents.h').read()
    op = re.sub(r'\n// zee_vulling_4 \{\n.*?// \}\n', '\n', op, flags=re.S)
    for c, i, d, _ in TRAINERS:
        assert not re.search(r'#define %s\b' % c, op), c
        assert not re.search(r'#define TRAINER_\w+\s+%d\b' % i, op), i
    block = '// zee_vulling_4 {\n' + ''.join('#define %-35s %d // Project Grounded (zeevulling 4): %s\n' % (c, i, d)
                                             for c, i, d, _ in TRAINERS) + '// }\n'
    last = max([TRAINERS[-1][1]] + [int(n) for n in re.findall(r'#define TRAINER_\w+\s+(\d+)', op)]) + 1
    op = re.sub(r'\n(#define TRAINERS_COUNT\s+)(\d+)', lambda m: '\n' + block + '\n' + m.group(1) + str(last), op)
    op = re.sub(r'\n{3,}(// zee_vulling_4 \{)', r'\n\n\1', op)
    op = re.sub(r'// \}\n{2,}#define TRAINERS_COUNT', '// }\n\n#define TRAINERS_COUNT', op)
    open('include/constants/opponents.h', 'w').write(op)
    p = open('src/data/trainers.party').read()
    if TBEGIN in p:
        p = p[:p.index(TBEGIN)].rstrip('\n') + p[p.index(TEND) + len(TEND):]
    p = p.rstrip('\n') + '\n\n' + TBEGIN + '\n\n' + '\n\n'.join(t[3] for t in TRAINERS) + '\n\n' + TEND + '\n'
    open('src/data/trainers.party', 'w').write(p)


def team(level, ivs, *mons):
    """mons: 'Soort' of ('Soort', lvl-delta[, [moves][, item]])"""
    out = []
    for m in mons:
        m = (m,) if isinstance(m, str) else tuple(m)
        sp, d, moves, item = (m + (0, [], None)[len(m) - 1:])[:4]
        s = sp + (' @ ' + item if item else '') + '\nLevel: %d\nIVs: %d HP / %d Atk / %d Def / %d SpA / %d SpD / %d Spe' % (
            (level + d,) + (ivs,) * 6)
        for mv in moves: s += '\n- ' + mv
        out.append(s)
    return '\n\n'.join(out)


def hdr(name, cls, pic, gender, music, ai='Check Bad Move / Try To Faint'):
    return 'Name: %s\nClass: %s\nPic: %s\nGender: %s\nMusic: %s\nDouble Battle: No\nAI: %s' % (
        name, cls, pic, gender, music, ai)


SMART = 'Check Bad Move / Try To Faint / Check Viability'

# =====================================================================================================
# wild_encounters.json (tekstueel)
WILD = 'src/data/wild_encounters.json'
WTEXT = [open(WILD).read()]


def _block(label):
    s = WTEXT[0]
    i = s.index('"base_label": "%s"' % label)
    start = s.rindex('{', 0, i)
    depth, j = 0, start
    while True:
        if s[j] == '{': depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0: break
        j += 1
    return start, j + 1, i


WATER_TABLES = {}


def add_water_table(label, mapconst, after_label, mons):
    """Water-tabel (5 slots: 60/30/5/4/1) achter een bestaande; idempotent (bestaand blok wordt vervangen)."""
    assert len(mons) == 5 and len({m[0] for m in mons}) == 5, label
    for sp, lo, hi in mons:
        assert lo <= hi
        assert re.search(r'#define SPECIES_%s\b' % sp, SPECIES_H), sp
    WATER_TABLES[label] = mons
    lm = ',\n'.join('              { "min_level": %d, "max_level": %d, "species": "SPECIES_%s" }' % (lo, hi, sp)
                    for sp, lo, hi in mons)
    blk = ('{\n          "map": "%s",\n          "base_label": "%s",\n          "water_mons": {\n'
           '            "encounter_rate": 4,\n            "mons": [\n%s\n            ]\n          }\n        }'
           % (mapconst, label, lm))
    s = WTEXT[0]
    if '"base_label": "%s"' % label in s:
        a, b, _ = _block(label)
        WTEXT[0] = s[:a] + blk + s[b:]
    else:
        a, b, _ = _block(after_label)
        WTEXT[0] = s[:b] + ',\n        ' + blk + s[b:]


SPECIES_H = open('include/constants/species.h').read()

# =====================================================================================================
# map.json-hulpjes
MARK = '@ --- zee_vulling_4 (gegenereerd door tools/grounded/maptools/zee_vulling_4.py) ---'
MARK_END = '@ --- einde zee_vulling_4 ---'
TEXTS = []


def obj(gfx, x, y, script, move='MOVEMENT_TYPE_FACE_DOWN', trainer=False, sight=0, flag='0', item=None):
    return {'graphics_id': gfx, 'x': x, 'y': y, 'elevation': 3, 'movement_type': move,
            'movement_range_x': 0, 'movement_range_y': 0,
            'trainer_type': 'TRAINER_TYPE_NORMAL' if trainer else 'TRAINER_TYPE_NONE',
            'trainer_sight_or_berry_tree_id': item or str(sight), 'script': script, 'flag': flag}


def ball(M, x, y, item, tag):
    name = flag('FLAG_ITEM_ZV4_%s_%s' % (tag, item[5:]), 'item (%s)' % M.name)
    return obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', 'MOVEMENT_TYPE_LOOK_AROUND',
               flag=name, item=item)


def hidden(M, x, y, item, tag):
    name = flag('FLAG_HIDDEN_ITEM_ZV4_%s_%s' % (tag, item[5:]), 'verborgen item (%s)' % M.name)
    return {'type': 'hidden_item', 'x': x, 'y': y, 'elevation': M.elev(x, y), 'item': item, 'flag': name}


def sign(x, y, script, elev=3):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': elev, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
            'script': script}


def apply_events(M, objs, bgs, script_text):
    path = 'data/maps/%s/map.json' % M.name
    m = json.load(open(path))
    for o in objs:
        c = M.v[o['y']][o['x']]
        if M.underwater:
            o['elevation'] = M.elev(o['x'], o['y']) or 3
        elif M.beh(c) in SURF:
            o['elevation'] = 1
    inc_path = 'data/maps/%s/scripts.inc' % M.name
    inc = open(inc_path).read()
    old_scripts = re.findall(r'^(\w+)::', inc.split(MARK)[1], re.M) if MARK in inc else []
    mine = set(old_scripts) | {o['script'] for o in objs if o['script'] != 'Common_EventScript_FindItem'}
    m['object_events'] = [o for o in m['object_events'] if o['script'] not in mine and 'ZV4' not in o['flag']]
    m['bg_events'] = [b for b in m['bg_events'] if b.get('script') not in mine and 'ZV4' not in b.get('flag', '')]
    m['object_events'] += objs
    m['bg_events'] += bgs
    os_ = m['object_events']
    for o in os_:
        near = [p for p in os_ if abs(p['x'] - o['x']) <= 12 and abs(p['y'] - o['y']) <= 9]
        assert len(near) <= 15, '%s: te veel objecten rond (%d,%d)' % (M.name, o['x'], o['y'])
    taken = {}
    for e in m['object_events'] + m['bg_events'] + m['warp_events']:
        k = (e['x'], e['y'])
        assert k not in taken or e.get('type') == 'sign' and taken[k] == 'sign', (M.name, 'dubbel event op', k)
        taken[k] = e.get('type', 'obj')
    for o in objs:
        assert not M.v[o['y']][o['x']] & BLOCK, (M.name, o['script'], o['x'], o['y'])
    for b in bgs:
        if b['type'] == 'hidden_item':
            assert not M.v[b['y']][b['x']] & BLOCK, (M.name, b['item'], b['x'], b['y'])
    open(path, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    if MARK in inc:
        inc = inc[:inc.index(MARK)].rstrip('\n') + '\n' + inc[inc.index(MARK_END) + len(MARK_END):].lstrip('\n')
    if script_text.strip():
        inc = inc.rstrip('\n') + '\n\n' + MARK + '\n' + script_text.strip('\n') + '\n' + MARK_END + '\n'
    open(inc_path, 'w').write(inc)


def check_text(label, s, width=36):
    """Elke regel (tussen \\n, \\l, \\p) moet in het tekstvak passen (ruwe telling, {PLAYER} = 7)."""
    s2 = s.replace('{PLAYER}', 'XXXXXXX').replace('POKeMON', 'POKEMON')
    s2 = re.sub(r'\{[^}]*\}', '', s2)
    for part in re.split(r'\\[nlp]', s2):
        if len(part) > width:
            print('%s: regel te lang (%d): %s' % (label, len(part), part)); FAIL.append(label)
    if '"' in s:
        print('%s: " in tekst' % label); FAIL.append(label)


def text(label, s):
    check_text(label, s)
    return '%s:\n\t.string "%s$"\n\n' % (label, s)


def talk(label, body):
    return '%s::\n%s\n\n' % (label, body.strip('\n'))


def npc(P, name, lines):
    t = P.replace('EventScript', 'Text') + name
    return talk(P + name, '\tmsgbox %s, MSGBOX_NPC\n\tend' % t) + text(t, lines)


def signpost(P, name, lines):
    t = P.replace('EventScript', 'Text') + name
    return talk(P + name, '\tmsgbox %s, MSGBOX_SIGN\n\tend' % t) + text(t, lines)


def single(P, name, tr, intro, defeat, post):
    t = P.replace('EventScript', 'Text') + name
    return (talk(P + name, '\ttrainerbattle_single %s, %s_Intro, %s_Defeat\n\tmsgbox %s_Post, MSGBOX_AUTOCLOSE\n\tend'
                 % (tr, t, t, t)) + text(t + '_Intro', intro) + text(t + '_Defeat', defeat) + text(t + '_Post', post))


def solid_of(objs):
    return {(o['x'], o['y']) for o in objs if o['graphics_id'] != 'OBJ_EVENT_GFX_ITEM_BALL'}


def finish(M, objs, bgs, scr, start, extra=()):
    old = {(o['x'], o['y']) for o in M.json['object_events'] if 'ZV4' not in o['flag']
           and o['graphics_id'] != 'OBJ_EVENT_GFX_ITEM_BALL' and o['script'] not in {p['script'] for p in objs}}
    S = solid_of(objs) | old
    targets = [(b['x'], b['y']) for b in bgs if b['type'] == 'hidden_item'] + list(extra)
    targets += [(o['x'], o['y']) for o in objs if o['graphics_id'] == 'OBJ_EVENT_GFX_ITEM_BALL']
    seen = set()
    for st in (start if isinstance(start, list) else [start]):  # onder water: elke kom is apart te bereiken (duiken)
        seen |= reach(M, st, targets, S)
    miss = [t for t in targets if t not in seen]
    if miss:
        print('%s: niet bereikbaar: %s' % (M.name, miss)); FAIL.append(M.name)
    for o in objs:  # personen/borden: een buurtegel moet bereikbaar zijn
        if (o['x'], o['y']) in S and not any((o['x'] + dx, o['y'] + dy) in seen
                                             for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            print('%s: %s niet aan te spreken' % (M.name, o['script'])); FAIL.append(M.name)
    for b in bgs:
        if b['type'] == 'sign' and not any((b['x'] + dx, b['y'] + dy) in seen
                                           for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            print('%s: bord %s niet te lezen' % (M.name, b['script'])); FAIL.append(M.name)
    M.save()
    apply_events(M, objs, bgs, scr)
    return seen


# --- zeewier: bodem -> zeewier (zelfde paren als zee_vulling_1/3) + de donkere trogbodem (zoals de zeetempel)
SEAWEED = {0x2A9: 0x281, 0x216: 0x201, 0x25B: 0x281, 0x256: 0x281, 0x2D3: 0x281}


def seaweed(M, patches, keep=()):
    rng = random.Random('zv4-zeewier:%s' % M.name)
    keep = set(keep)
    n = 0
    for (cx, cy, r) in patches:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r - 1, cx + r + 2):
                if not (0 <= x < M.w and 0 <= y < M.h) or (x, y) in keep: continue
                d = ((x - cx) / (r + 1.0)) ** 2 + ((y - cy) / (r + 0.5)) ** 2
                if d <= 1.0 and rng.random() < 0.85 and (M.v[y][x] & 0x3FF) in SEAWEED and not M.v[y][x] & BLOCK:
                    M.put(x, y, (M.v[y][x] & ~0x3FF) | SEAWEED[M.v[y][x] & 0x3FF]); n += 1
    print('%s: %d zeewiertegels erbij' % (M.name, n))
    return n


def put_hole(M, x, ytop):
    """Zwemgat (Underwater-tileset): bovenrij 265-267 (massief), onderrij 26d/26e/26f (alleen het midden open)."""
    for i, (top, bot) in enumerate(((0x265, 0x26d), (0x266, 0x26e), (0x267, 0x26f))):
        M.put(x - 1 + i, ytop, (M.v[ytop][x - 1 + i] & 0xF000) | top | BLOCK)
        M.put(x - 1 + i, ytop + 1, (M.v[ytop + 1][x - 1 + i] & 0xF000) | bot | (0 if bot == 0x26e else BLOCK))


def warp_to(name, x, y, dest, dest_id='0'):
    """Zet (of vervang) een warp naar `dest` op (x,y); geeft de index terug."""
    p = 'data/maps/%s/map.json' % name
    m = json.load(open(p))
    idx = None
    for i, w in enumerate(m['warp_events']):
        if w['dest_map'] == dest:
            w.update({'x': x, 'y': y, 'elevation': 0, 'dest_warp_id': dest_id}); idx = i
    if idx is None:
        m['warp_events'].append({'x': x, 'y': y, 'elevation': 0, 'dest_map': dest, 'dest_warp_id': dest_id})
        idx = len(m['warp_events']) - 1
    open(p, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    return idx


def hook_after(mapname, label, line):
    """Eén regel direct na een label in scripts.inc (buiten ons blok); idempotent."""
    p = 'data/maps/%s/scripts.inc' % mapname
    s = open(p).read()
    if line in s:
        return
    assert label + '\n' in s, (mapname, label)
    s = s.replace(label + '\n', label + '\n' + line + '\n', 1)
    open(p, 'w').write(s)


# =====================================================================================================
# NIEUWE KAART: de diepzeetrog onder Route 127
TRENCH, TRENCH_CONST = 'Underwater_Route127_Trench', 'UNDERWATER_ROUTE127_TRENCH'
EXTRA_ROWS = 14          # de schacht van de Sealed Chamber-trog wordt 14 rijen langer
UW127_HOLE = (24, 12)    # bovenrij van het zwemgat in onderwater 127 (warp op (24,13))
R127_SURFACE = (24, 14)  # bovenkomen in de trog = terug naar het diepe water boven de trogkop


def register_layout(name, const, W, H):
    lj = open('data/layouts/layouts.json').read()
    entry = '''    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_Underwater",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (const, name, W, H, name, name)
    if '"LAYOUT_%s"' % const in lj:
        i = lj.index('"id": "LAYOUT_%s"' % const); s = lj.rindex('    {', 0, i); e = lj.index('    }', i) + 5
        lj = lj[:s] + entry + lj[e:]
    else:
        i = lj.rindex('    }\n  ]')
        lj = lj[:i + 5] + ',\n' + entry + lj[i + 5:]
    open('data/layouts/layouts.json', 'w').write(lj)
    json.loads(lj)
    LAYOUTS['LAYOUT_' + const] = {'id': 'LAYOUT_' + const, 'name': name + '_Layout', 'width': W, 'height': H,
                                  'primary_tileset': 'gTileset_General', 'secondary_tileset': 'gTileset_Underwater',
                                  'blockdata_filepath': 'data/layouts/%s/map.bin' % name}


def register_map(name):
    g = open('data/maps/map_groups.json').read()
    if '"%s"' % name not in g:
        i = g.index('"gMapGroup_Grounded": ['); j = g.index(']', i)
        g = g[:i] + g[i:j].rstrip() + ',\n    "%s"\n  ' % name + g[j:]
        open('data/maps/map_groups.json', 'w').write(g)
        assert len(json.loads(g)['gMapGroup_Grounded']) <= 128
    es = open('data/event_scripts.s').read()
    inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
    if inc not in es:
        anchor = '\t.include "data/maps/Underwater_SeaTemple/scripts.inc"\n'
        assert anchor in es
        es = es.replace(anchor, anchor + inc, 1)
        open('data/event_scripts.s', 'w').write(es)


def build_trench():
    W, H0 = 22, 48
    b = open('data/layouts/Underwater_SealedChamber/map.bin', 'rb').read()
    g = [list(struct.unpack_from('<%dH' % W, b, y * W * 2)) for y in range(H0)]
    assert g[11] == g[12], 'rij 11/12 van de Sealed Chamber-trog verwacht gelijk'
    g = g[:13] + [list(g[12]) for _ in range(EXTRA_ROWS)] + g[13:]
    H = len(g)
    # braille (0x270) wordt gewone wand
    for y in range(H):
        for x in range(W):
            if g[y][x] & 0x3FF == 0x270:
                g[y][x] = (g[y][x] & ~0x3FF) | 0x21E
    os.makedirs('data/layouts/' + TRENCH, exist_ok=True)
    open('data/layouts/%s/map.bin' % TRENCH, 'wb').write(b''.join(struct.pack('<H', c) for r in g for c in r))
    open('data/layouts/%s/border.bin' % TRENCH, 'wb').write(open('data/layouts/Underwater_SealedChamber/border.bin', 'rb').read())
    register_layout(TRENCH, TRENCH_CONST, W, H)
    base = json.load(open('data/maps/Underwater_SealedChamber/map.json'))
    m = {k: base[k] for k in base}
    p = 'data/maps/%s/map.json' % TRENCH
    old = json.load(open(p)) if os.path.exists(p) else {}
    m.update({'id': 'MAP_' + TRENCH_CONST, 'name': TRENCH, 'layout': 'LAYOUT_' + TRENCH_CONST, 'connections': None,
              'region_map_section': 'MAPSEC_ROUTE_127', 'show_map_name': False,
              'object_events': old.get('object_events', []), 'coord_events': [], 'bg_events': old.get('bg_events', []),
              'warp_events': [{'x': 7, 'y': 1, 'elevation': 0, 'dest_map': 'MAP_UNDERWATER_ROUTE127', 'dest_warp_id': '0'}]})
    os.makedirs('data/maps/' + TRENCH, exist_ok=True)
    open(p, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    sp = 'data/maps/%s/scripts.inc' % TRENCH
    keep = ''
    if os.path.exists(sp):
        s = open(sp).read()
        if MARK in s:
            keep = '\n' + s[s.index(MARK):]
    open(sp, 'w').write('''@ Project Grounded: de diepzeetrog onder Route 127 (zwemgat in de kop van de centrale trog van onderwater 127,
@ %d,%d). Kopie van Underwater_SealedChamber, %d rijen dieper. Bovenkomen = terug naar het diepe water van Route 127.
@ Kaart: tools/grounded/maptools/zee_vulling_4.py
%s_MapScripts::
	map_script MAP_SCRIPT_ON_DIVE_WARP, %s_OnDive
	.byte 0

%s_OnDive:
	setdivewarp MAP_ROUTE127, %d, %d
	end
''' % (UW127_HOLE[0], UW127_HOLE[1] + 1, EXTRA_ROWS, TRENCH, TRENCH, TRENCH, R127_SURFACE[0], R127_SURFACE[1]) + keep)
    register_map(TRENCH)
    # warps over en weer (het zwemgat zelf: zie ONDERWATER 127)
    x, y = UW127_HOLE
    wi = warp_to('Underwater_Route127', x, y + 1, 'MAP_' + TRENCH_CONST, '0')
    warp_to(TRENCH, 7, 1, 'MAP_UNDERWATER_ROUTE127', str(wi))
    R = Map('Route127')
    assert R.beh(R.v[R127_SURFACE[1]][R127_SURFACE[0]]) == 'MB_DEEP_WATER', 'bovenkomen niet op diep water'


# =====================================================================================================
P_ALL = []
build_trench()

# -----------------------------------------------------------------------------------------------------
# WILDE POKEMON ONDER WATER (5 slots: 60/30/5/4/1). Eerst weinig voorkomende families (ONDERVERTEGENWOORDIGD.md).
add_water_table('gUnderwater_SootopolisCity', 'MAP_UNDERWATER_SOOTOPOLIS_CITY', 'gUnderwater_Route124',
                [('TYNAMO', 38, 41), ('GASTRODON_WEST', 39, 42), ('EELEKTRIK', 40, 43), ('FEEBAS', 30, 35),
                 ('EELEKTROSS', 43, 45)])
add_water_table('gUnderwater_WhirlIsland', 'MAP_UNDERWATER_WHIRL_ISLAND', 'gUnderwater_SootopolisCity',
                [('KINGLER', 42, 45), ('DEWGONG', 42, 45), ('CRAMORANT', 43, 46), ('OCTILLERY', 43, 46),
                 ('TATSUGIRI_DROOPY', 44, 46)])
add_water_table('gUnderwater_MarineCave', 'MAP_UNDERWATER_MARINE_CAVE', 'gUnderwater_WhirlIsland',
                [('JELLICENT', 45, 48), ('SHARPEDO', 45, 48), ('KABUTOPS', 46, 49), ('OMASTAR', 46, 49),
                 ('WAILORD', 48, 50)])
add_water_table('gUnderwater_Route134', 'MAP_UNDERWATER_ROUTE134', 'gUnderwater_MarineCave',
                [('CORSOLA', 42, 45), ('BARBARACLE', 42, 45), ('CARRACOSTA', 43, 46), ('STARMIE', 43, 46),
                 ('VAPOREON', 45, 47)])
add_water_table('gUnderwater_SealedChamber', 'MAP_UNDERWATER_SEALED_CHAMBER', 'gUnderwater_Route134',
                [('WAILMER', 36, 39), ('TENTACRUEL', 42, 45), ('RELICANTH', 43, 46), ('MANTYKE', 40, 44),
                 ('UNOWN', 40, 45)])
add_water_table('gUnderwater_ScorchedSlab', 'MAP_UNDERWATER_SCORCHED_SLAB', 'gUnderwater_SealedChamber',
                [('ARAQUANID', 38, 41), ('BASCULIN_RED_STRIPED', 38, 41), ('POLIWHIRL', 38, 41), ('GOLDUCK', 40, 43),
                 ('LUDICOLO', 42, 44)])
add_water_table('gUnderwater_SeafloorCavern', 'MAP_UNDERWATER_SEAFLOOR_CAVERN', 'gUnderwater_ScorchedSlab',
                [('WUGTRIO', 40, 43), ('QWILFISH_HISUI', 40, 43), ('TOXAPEX', 41, 44), ('CORSOLA_GALAR', 41, 44),
                 ('OVERQWIL', 43, 45)])
add_water_table('gUnderwater_Route136', 'MAP_UNDERWATER_ROUTE136', 'gUnderwater_SeafloorCavern',
                [('SEALEO', 38, 41), ('EISCUE', 38, 41), ('BASCULEGION_M', 40, 43), ('WALREIN', 42, 44),
                 ('EMPOLEON', 40, 42)])
add_water_table('g' + TRENCH, 'MAP_' + TRENCH_CONST, 'gUnderwater_Route136',
                [('LANTURN', 43, 46), ('PYUKUMUKU', 42, 45), ('MALAMAR', 44, 47), ('RELICANTH', 44, 47),
                 ('DHELMISE', 45, 48)])

# -----------------------------------------------------------------------------------------------------
# DE TROG (lv ~46)
M = Map(TRENCH)
P = TRENCH + '_EventScript_ZV4'
DY = EXTRA_ROWS
nweed = seaweed(M, [(6, 42 + DY, 3), (17, 42 + DY, 3), (12, 46 + DY, 3), (10, 37 + DY, 2), (5, 18, 2), (5, 28, 2)],
                keep={(7, 2), (12, 44 + DY)})
assert nweed >= 30
ABYSSA = trainer('TRAINER_DIVER_ABYSSA', 'diepzeetrog onder Route 127, wil de bodem aanraken',
                 hdr('ABYSSA', 'Swimmer F', 'Swimmer F', 'Female', 'Swimmer', ai=SMART),
                 team(46, 18, ('Toxapex', 0, ['Baneful Bunker', 'Scald', 'Toxic', 'Recover']),
                      ('Dhelmise', 0, ['Anchor Shot', 'Power Whip', 'Shadow Claw', 'Rapid Spin']),
                      ('Lanturn', 0, ['Discharge', 'Scald', 'Ice Beam', 'Thunder Wave']),
                      ('Kingdra', 1, ['Dragon Pulse', 'Surf', 'Flash Cannon', 'Agility'])))
objs = [obj('OBJ_EVENT_GFX_SWIMMER_F', 7, 22, P + 'Abyssa', move='MOVEMENT_TYPE_FACE_UP', trainer=True, sight=4),
        ball(M, 6, 46 + DY, 'ITEM_DEEP_SEA_SCALE', 'TRENCH'),
        ball(M, 18, 41 + DY, 'ITEM_DEEP_SEA_TOOTH', 'TRENCH')]
bgs = [sign(12, 43 + DY, P + 'Bottom'), hidden(M, 16, 46 + DY, 'ITEM_RELIC_CROWN', 'TRENCH'),
       hidden(M, 8, 9, 'ITEM_DIVE_BALL', 'TRENCH')]
scr = single(P, 'Abyssa', ABYSSA,
             "I'm going to touch the bottom of\\n"
             "the deepest trench in HOENN.\\p"
             "Then I'm going to come back up and\\n"
             "tell people. That's the hard part.",
             "Fine. You can touch it first.\\n"
             "It's just sand. I knew it.",
             "Down there, the pressure is like\\n"
             "forty WAILORD sitting on you.\\p"
             "I've had worse family reunions.")
scr += signpost(P, 'Bottom',
                "A plaque, bolted to the rock:\\p"
                "'DEEPEST POINT IN HOENN.\\p"
                "DEPTH: MORE THAN OUR TECHNOLOGY\\n"
                "COULD RELIABLY MEASURE.'\\p"
                "Underneath, smaller:\\n"
                "'The research team turned back\\l"
                "here. The LANTURN did not.'")
start = (7, 3)
finish(M, objs, bgs, scr, start)

# -----------------------------------------------------------------------------------------------------
# KLEINE GROTMONDEN: alleen een tabel (hierboven) + soms een verborgen item op de diepe tegels
for name, (x, y), item, tag, start in [
        ('Underwater_SootopolisCity', (6, 7), 'ITEM_PRISM_SCALE', 'SOOTO', (9, 7)),
        ('Underwater_WhirlIsland', (13, 7), 'ITEM_SHOAL_SHELL', 'WHIRL', (9, 7)),
        ('Underwater_MarineCave', (8, 7), 'ITEM_SPLASH_PLATE', 'MARINE', (9, 7)),
        ('Underwater_Route134', (6, 7), 'ITEM_RELIC_SILVER', 'R134', (8, 7)),
        ('Underwater_SeafloorCavern', (4, 6), 'ITEM_NET_BALL', 'SEAFLOOR', (6, 6))]:
    M = Map(name)
    finish(M, [], [hidden(M, x, y, item, tag)], '', start)

# -----------------------------------------------------------------------------------------------------
# SEALED CHAMBER (buitenkant): zeewier in de kom, een verborgen relikwie
M = Map('Underwater_SealedChamber')
seaweed(M, [(6, 41, 2), (18, 40, 1), (8, 46, 1), (16, 46, 1), (7, 22, 1)], keep={(7, 2), (12, 44)})
finish(M, [], [hidden(M, 17, 45, 'ITEM_RELIC_STATUE', 'SEALED')], '', (7, 3))

# ROUTE 136 (onder water, Suicune-grot): zeewier + verborgen item
M = Map('Underwater_Route136')
seaweed(M, [(6, 41, 2), (18, 40, 1), (8, 46, 1), (16, 46, 1), (7, 14, 1)], keep={(7, 2), (12, 44)})
finish(M, [], [hidden(M, 6, 45, 'ITEM_NEVER_MELT_ICE', 'UW136')], '', (7, 3))

# -----------------------------------------------------------------------------------------------------
# ONDERWATER 105 (lv ~42): vrijduikster Nerissa + parelsnoer
M = Map('Underwater_Route105')
P = 'Underwater_Route105_EventScript_ZV4'
NERISSA = trainer('TRAINER_DIVER_NERISSA', 'onderwater Route 105, vrijduikster op een record',
                  hdr('NERISSA', 'Swimmer F', 'Swimmer F', 'Female', 'Swimmer'),
                  team(42, 14, 'Bruxish', 'Jellicent', ('Clawitzer', 1)))
objs = [obj('OBJ_EVENT_GFX_SWIMMER_F', 13, 26, P + 'Nerissa', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=4)]
bgs = [hidden(M, 8, 32, 'ITEM_PEARL_STRING', 'UW105')]
scr = single(P, 'Nerissa', NERISSA,
             "Shh! I'm going for the record.\\n"
             "Eleven minutes on one breath.\\p"
             "I'm at minute ten. Talking costs\\n"
             "air. Battling costs air.\\l"
             "Let's do it anyway.",
             "...!\\n"
             "(She gives a thumbs up. Or down.)",
             "New plan: the record is for\\n"
             "MOST BATTLES ON ONE BREATH.\\l"
             "I'm currently the world champion.")
finish(M, objs, bgs, scr, (9, 29))

# ONDERWATER 124: een duiker die naar Whirl Island zoekt + verborgen item (Route 124 zelf is van een andere agent)
M = Map('Underwater_Route124')
P = 'Underwater_Route124_EventScript_ZV4'
objs = [obj('OBJ_EVENT_GFX_SWIMMER_M', 20, 34, P + 'Diver', move='MOVEMENT_TYPE_FACE_LEFT')]
bgs = [hidden(M, 10, 3, 'ITEM_STAR_PIECE', 'UW124')]
scr = npc(P, 'Diver',
          "(A diver writes on a slate:)\\p"
          "'THE HOLE UP NORTH GOES TO AN\\n"
          "ISLAND. OR TO A WHIRLPOOL.\\p"
          "I'VE BEEN SPINNING FOR 3 DAYS.\\n"
          "IT'S A WHIRLPOOL.'")
finish(M, objs, bgs, scr, [(13, 33), (11, 4)])

# ONDERWATER 125 (lv ~42): extra zeewier, duiker Gill, verborgen item
M = Map('Underwater_Route125')
seaweed(M, [(9, 17, 1), (56, 29, 1), (47, 31, 1)])
P = 'Underwater_Route125_EventScript_ZV4'
GILL = trainer('TRAINER_DIVER_GILL', 'onderwater Route 125, zoekt zijn zoon (een Clauncher van 34)',
               hdr('GILL', 'Swimmer M', 'Swimmer M', 'Male', 'Swimmer'),
               team(42, 14, 'Kingler', 'Grapploct', ('Barraskewda', 1)))
objs = [obj('OBJ_EVENT_GFX_SWIMMER_M', 59, 29, P + 'Gill', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=4)]
bgs = [hidden(M, 59, 32, 'ITEM_BIG_PEARL', 'UW125')]
scr = single(P, 'Gill', GILL,
             "Have you seen my son? He's a\\n"
             "CLAUNCHER. Small. One big claw.\\p"
             "He's 34. He said he needed space.\\n"
             "The ocean is mostly space.",
             "You fight like his mother.\\n"
             "Also a CLAUNCHER.",
             "If you see him, tell him his room\\n"
             "is still a rock. Same rock.\\l"
             "I didn't touch it.")
finish(M, objs, bgs, scr, (52, 30))

# ONDERWATER 126 (lv ~43): duikster Odessa, een gedenksteen van Sootopolis, Big Nugget
M = Map('Underwater_Route126')
P = 'Underwater_Route126_EventScript_ZV4'
ODESSA = trainer('TRAINER_DIVER_ODESSA', 'onderwater Route 126, gidst duiktoeristen rond Sootopolis',
                 hdr('ODESSA', 'Swimmer F', 'Swimmer F', 'Female', 'Swimmer'),
                 team(43, 15, 'Gastrodon', 'Araquanid', ('Golisopod', 1)))
objs = [obj('OBJ_EVENT_GFX_SWIMMER_F', 24, 16, P + 'Odessa', move='MOVEMENT_TYPE_FACE_DOWN', trainer=True, sight=3)]
bgs = [sign(33, 9, P + 'Stone'), hidden(M, 22, 60, 'ITEM_BIG_NUGGET', 'UW126'),
       hidden(M, 21, 14, 'ITEM_HEART_SCALE', 'UW126')]
scr = single(P, 'Odessa', ODESSA,
             "Welcome to the SOOTOPOLIS DIVE\\n"
             "TOUR! On your left: rock.\\p"
             "On your right: also rock.\\n"
             "Tips are appreciated. Battles too.",
             "Tour's over. Please exit through\\n"
             "the gift shop. There is no gift\\n"
             "shop.",
             "The rocks here are older than the\\n"
             "city. The city is older than me.\\p"
             "I'm older than the rocks feel.\\n"
             "It's the job.")
scr += signpost(P, 'Stone',
                "A carved stone, half buried:\\p"
                "'HERE LIES THE FIRST SOOTOPOLIS\\n"
                "SUBMARINE. IT WORKED PERFECTLY.\\p"
                "IT JUST NEVER CAME BACK UP.'")
finish(M, objs, bgs, scr, (30, 10))

# ONDERWATER 127: zeewier erbij + verborgen item (de trog zit in build_trench)
M = Map('Underwater_Route127')
x, y = UW127_HOLE
assert all(M.v[y][x + d] & BLOCK for d in (-1, 0, 1)) and not M.v[y + 1][x] & BLOCK and not M.v[y + 2][x] & BLOCK
put_hole(M, x, y)
seaweed(M, [(67, 57, 2), (62, 37, 1), (72, 49, 1), (57, 12, 1), (27, 52, 1)], keep={(24, 13), (24, 14), (72, 45), (72, 46)})
finish(M, [], [hidden(M, 31, 70, 'ITEM_PP_MAX', 'UW127')], '', (31, 60), extra=[(24, 14)])

# ONDERWATER 128 (lv ~43): duiker Brine, zeewier, verborgen item
M = Map('Underwater_Route128')
seaweed(M, [(52, 17, 1), (62, 12, 1), (74, 22, 2), (42, 32, 1)], keep={(76, 19), (76, 20), (38, 26), (38, 27)})
P = 'Underwater_Route128_EventScript_ZV4'
BRINE = trainer('TRAINER_DIVER_BRINE', 'onderwater Route 128, bewaakt de ingang naar de zeebodemgrot',
                hdr('BRINE', 'Swimmer M', 'Swimmer M', 'Male', 'Swimmer'),
                team(43, 15, 'Overqwil', 'Cramorant', ('Dracovish', 1)))
objs = [obj('OBJ_EVENT_GFX_SWIMMER_M', 55, 14, P + 'Brine', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=4)]
bgs = [hidden(M, 36, 36, 'ITEM_MAX_REVIVE', 'UW128')]
scr = single(P, 'Brine', BRINE,
             "A submarine came through here once.\\n"
             "Team AQUA. Very loud. No manners.\\p"
             "Ever since, I check everyone.\\n"
             "Arms up. Fins out.",
             "You're clean. Suspiciously clean.\\n"
             "Nobody's that clean underwater.",
             "The sub left a smell down there.\\n"
             "The smell is still here.\\l"
             "It has a name now. Gary.")
finish(M, objs, bgs, scr, (50, 14))

# ONDERWATER 129: een duiker met een verhaal + zeewier + verborgen item
M = Map('Underwater_Route129')
seaweed(M, [(40, 22, 1), (25, 6, 1), (16, 16, 1)])
P = 'Underwater_Route129_EventScript_ZV4'
objs = [obj('OBJ_EVENT_GFX_SWIMMER_M', 17, 14, P + 'Diver', move='MOVEMENT_TYPE_FACE_DOWN')]
bgs = [hidden(M, 44, 22, 'ITEM_BOTTLE_CAP', 'UW129')]
scr = npc(P, 'Diver',
          "I followed the captain's map. X\\n"
          "marks the spot. I dug for a week.\\p"
          "Found a note. The note said: 'THREE\\n"
          "STEPS EAST'. I took three steps.\\p"
          "Somebody had already been there.\\n"
          "Story of my life. Also of my wife.")
finish(M, objs, bgs, scr, [(16, 17), (43, 21)])

# =====================================================================================================
# BOVENWATER
# ROUTE 126: twee verborgen items op de zandbank en in het ondiepe water
M = Map('Route126')
finish(M, [], [hidden(M, 43, 5, 'ITEM_STARDUST', 'R126'), hidden(M, 41, 6, 'ITEM_DIVE_BALL', 'R126')], '', (70, 50))

# ROUTE 127: oceanograaf die de trog meet + verborgen item
M = Map('Route127')
P = 'Route127_EventScript_ZV4'
objs = [obj('OBJ_EVENT_GFX_SCIENTIST_1', 65, 68, P + 'Oceanographer', move='MOVEMENT_TYPE_FACE_LEFT')]
bgs = [hidden(M, 68, 37, 'ITEM_DEEP_SEA_TOOTH', 'R127')]
scr = npc(P, 'Oceanographer',
          "I measure the depth of the trench\\n"
          "west of here. With a rope.\\p"
          "The rope ran out. I tied on a\\n"
          "second rope. That ran out too.\\p"
          "Official result: two ropes deep.\\n"
          "If you DIVE at the head of the\\l"
          "trench, look for a hole. Bring\\l"
          "rope.")
finish(M, objs, bgs, scr, [(40, 40), (66, 42)], extra=[(64, 68)])

# ROUTE 128: Parasol Lady op een eilandje + verborgen item
M = Map('Route128')
keep_events(M)
islet(M, rect(6, 28, 10, 29))
P = 'Route128_EventScript_ZV4'
SOLENNE = trainer('TRAINER_PARASOL_LADY_SOLENNE', 'Route 128, zonnebaadt op een zandbank die er gisteren niet was',
                  hdr('SOLENNE', 'Parasol Lady', 'Parasol Lady', 'Female', 'Female', ai=SMART),
                  team(41, 15, ('Torkoal', 0, ['Lava Plume', 'Earth Power', 'Yawn', 'Rapid Spin']),
                       ('Leafeon', 0, ['Leaf Blade', 'X-Scissor', 'Swords Dance', 'Synthesis']),
                       ('Cherrim', 0, ['Solar Beam', 'Weather Ball', 'Growth', 'Leech Seed']),
                       ('Ninetales', 1, ['Flamethrower', 'Solar Beam', 'Extrasensory', 'Will-O-Wisp'])))
objs = [obj('OBJ_EVENT_GFX_WOMAN_5', 8, 28, P + 'Solenne', move='MOVEMENT_TYPE_FACE_DOWN', trainer=True, sight=3)]
bgs = [hidden(M, 24, 4, 'ITEM_HEAT_ROCK', 'R128')]
scr = single(P, 'Solenne', SOLENNE,
             "I came for the sun. My parasol\\n"
             "came for the shade.\\p"
             "We're in a very complicated\\n"
             "relationship.",
             "Fine, I'll get a tan. On one side.\\n"
             "The parasol side stays pale.",
             "This sandbank wasn't here\\n"
             "yesterday. Tomorrow it won't be\\l"
             "either. I have to keep moving my\\l"
             "towel.")
finish(M, objs, bgs, scr, [(0, 30), (40, 30)], extra=[(8, 29)])

# ROUTE 130: een zwemmende Tuber ver uit de kust, een fotograaf bij de grot, verborgen item.
# LET OP: Route 130 kiest in ON_TRANSITION een layout (Mirage Island). Bobby staat op water dat in beide layouts
# gelijk is; de grot-eilandjes bestaan alleen zonder Mirage Island, dus de fotograaf is weg als het eiland er is
# (FLAG_TEMP_5, gezet in Route130_EventScript_SetMirageIslandLayout).
M = Map('Route130')
L2 = [l for l in LAYOUTS.values() if l['name'] == 'Route130_MirageIsland_Layout'][0]
_b = open(L2['blockdata_filepath'], 'rb').read()
MIRAGE = [[struct.unpack_from('<H', _b, (y * M.w + x) * 2)[0] for x in range(M.w)] for y in range(M.h)]
assert M.v[23][66] == MIRAGE[23][66] and M.beh(M.v[23][66]) == 'MB_OCEAN_WATER', 'Bobby niet op gedeeld water'
P = 'Route130_EventScript_ZV4'
BOBBY = trainer('TRAINER_TUBER_BOBBY', 'Route 130, dreef op zijn band weg uit Slateport',
                hdr('BOBBY', 'Tuber M', 'Tuber M', 'Male', 'Girl'),
                team(40, 12, 'Azumarill', 'Golduck', ('Floatzel', 1)))
objs = [obj('OBJ_EVENT_GFX_TUBER_M_SWIMMING', 66, 23, P + 'Bobby', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=4),
        obj('OBJ_EVENT_GFX_CAMERAMAN', 17, 26, P + 'Photographer', move='MOVEMENT_TYPE_FACE_RIGHT', flag='FLAG_TEMP_5')]
bgs = [hidden(M, 19, 27, 'ITEM_STAR_PIECE', 'R130')]
scr = single(P, 'Bobby', BOBBY,
             "Mom said stay where she can see me.\\n"
             "That was in SLATEPORT.\\p"
             "She has very good eyes.\\n"
             "Probably.",
             "Can you tell my mom I'm fine?\\n"
             "And that the tube is fine too?",
             "I've been floating for two weeks.\\n"
             "WAILMER bring me snacks.\\l"
             "I'm never going home.")
scr += npc(P, 'Photographer',
           "I'm waiting for MIRAGE ISLAND to\\n"
           "appear. Then I take the photo.\\p"
           "I've been here four years.\\n"
           "I have 30,000 photos of water.\\p"
           "Once I went to get a sandwich.\\n"
           "I hear it was beautiful.")
finish(M, objs, bgs, scr, (40, 22), extra=[(18, 26)])
hook_after('Route130', 'Route130_EventScript_SetMirageIslandLayout::', '\tsetflag FLAG_TEMP_5 @ zee_vulling_4: fotograaf mist het eiland')

# ROUTE 132: twee verborgen items (op zand/ondiepte; bestaan bij eb en vloed, alleen events)
M = Map('Route132')
finish(M, [], [hidden(M, 46, 28, 'ITEM_SHOAL_SALT', 'R132'), hidden(M, 13, 16, 'ITEM_HEART_SCALE', 'R132')], '', (40, 20))

# ROUTE 133: twee verborgen items
M = Map('Route133')
finish(M, [], [hidden(M, 6, 20, 'ITEM_PEARL', 'R133'), hidden(M, 42, 26, 'ITEM_RARE_CANDY', 'R133')], '', (79, 20))

# ROUTE 134: Ruin Maniac op de lange zandbank (de Sealed Chamber ligt ten zuiden) + verborgen item
M = Map('Route134')
P = 'Route134_EventScript_ZV4'
DORIAN = trainer('TRAINER_RUIN_MANIAC_DORIAN', 'Route 134, wil de Sealed Chamber openen met een schep',
                 hdr('DORIAN', 'Ruin Maniac', 'Ruin Maniac', 'Male', 'Hiker'),
                 team(41, 15, 'Claydol', 'Relicanth', 'Golurk', ('Bronzong', 1)))
objs = [obj('OBJ_EVENT_GFX_HIKER', 54, 16, P + 'Dorian', move='MOVEMENT_TYPE_FACE_DOWN', trainer=True, sight=2)]
bgs = [hidden(M, 9, 13, 'ITEM_RELIC_COPPER', 'R134')]
scr = single(P, 'Dorian', DORIAN,
             "Somewhere under this sea is a\\n"
             "SEALED CHAMBER. With BRAILLE.\\p"
             "I can't read braille.\\n"
             "I brought a shovel. Same thing.",
             "My shovel isn't waterproof.\\n"
             "Neither am I.",
             "The chamber is south of here,\\n"
             "deep down. They say you need a\\l"
             "WAILORD and a RELICANTH to open it.\\p"
             "I have a RELICANTH. My WAILORD\\n"
             "is in a different chamber.\\l"
             "It's called 'the PC'.")
finish(M, objs, bgs, scr, (40, 20), extra=[(54, 17)])

# =====================================================================================================
assert not FAIL, FAIL
open(WILD, 'w').write(WTEXT[0])
json.loads(WTEXT[0])
write_flags()
write_trainers()
json.dump(ORIG, open(ORIG_PATH, 'w'), indent=0, sort_keys=True)
print('ok: %d trainers (%d-%d), %d flags (FLAG_GROUNDED %d-%d), %d nieuwe watertabellen' % (
    len(TRAINERS), FIRST_ID, FIRST_ID + len(TRAINERS) - 1, len(FLAGS), FLAG_FIRST, FLAG_FIRST + len(FLAGS) - 1,
    len(WATER_TABLES)))
