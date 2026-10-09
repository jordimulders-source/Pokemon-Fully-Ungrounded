"""Project Grounded: zeevulling 2 (Route 105, 108, 122, 124, 128-131, 133, 134, Whirl Island + losse verborgen items
in de rivieren/zeeën van Route 110/115/118/119/120) en de vergeten gewone lijnen in het wild.

Werkt als zee_vulling_1.py: kleine eilandjes (General-autotile: ondiepe rand + zand, eventueel hoog gras) met NPC's,
trainers, items en verborgen items; eigen objecten/bg-events/scriptblokken worden steeds vervangen (idempotent).
Daarnaast beheert dit script zijn eigen stukken in:
  - include/constants/flags.h (vervangt FLAG_UNUSED_0x...-regels; zie FLAGS/HIDDEN_FLAGS),
  - include/constants/opponents.h + src/data/trainers.party (blok tussen markeringen; TRAINERS_COUNT),
  - src/data/wild_encounters.json (land-tabellen op de eilandjes, en slotvervangingen op landroutes; tekstueel).
Bereikbaarheid: surfen + lopen, met de zeestroming van Route 131-134 (glijden zoals calm_currents.py).
Grap-trainers met lage levels horen alleen vroeg in de game (Jordi): de benoemde trainers hier hebben een echt team.

Gebruik (vanuit de repo-root): python3 tools/grounded/maptools/zee_vulling_2.py
Daarna: python3 tools/grounded/stadium/pool.py en python3 tools/grounded/stadium/announcer.py (Stadium-pool).
"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, os, random, re, struct, sys
from collections import deque

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
random.seed(1082)
BLOCK = 1 << 10
OCEAN = 0x170

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

    def save(self):
        open(self.path, 'wb').write(b''.join(struct.pack('<H', c) for r in self.v for c in r))
        json.dump(ORIG, open(ORIG_PATH, 'w'), indent=0, sort_keys=True)


ORIG_PATH = 'tools/grounded/maptools/zee_vulling_2_orig.json'
ORIG = json.load(open(ORIG_PATH)) if os.path.exists(ORIG_PATH) else {}

# --- General-autotile (zelfde tiles als zee_vulling_1.py / tides_juan.py) ---
RING = {'TL': 0x1AD, 'T': 0x1AE, 'TR': 0x1AF, 'L': 0x1B5, 'R': 0x1B7, 'BL': 0x1BD, 'B': 0x1BE, 'BR': 0x1BF,
        'NW': 0x19B, 'NE': 0x19C, 'SW': 0x1A3, 'SE': 0x1A4, 'C': 0x19E}
SAND = {'C': 0x124, 'TL': 0x195, 'T': 0x196, 'TR': 0x197, 'L': 0x19D, 'R': 0x19F, 'BL': 0x1A5, 'B': 0x1A6,
        'BR': 0x1A7, 'NW': 0x185, 'NE': 0x186, 'SW': 0x18D, 'SE': 0x18E}
ROCK_SAND = [0x0A3, 0x0A4, 0x0AB, 0x0AC]
TALL_GRASS = 0x00D


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
    """Elke cel moet met de autotile-stukken te tekenen zijn (geen 1-brede uitsteeksels of dubbele binnenhoeken)."""
    for (x, y) in S:
        if not all((x + DIRS[d][0], y + DIRS[d][1]) in S for d in NEED[shape(S, x, y)].split()):
            return False
    return True


def dilate4(S):
    return S | {(x + dx, y + dy) for (x, y) in S for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))}


SEA_KEEP = {'Route122': rect(5, 33, 6, 35), 'Route124': rect(38, 30, 41, 32), 'Route129': rect(58, 30, 61, 32)}  # bootjes blijven op zee


def organic(M, sand):
    """Rechthoekig zand -> organische vorm: willekeurige bulten (vaste seed per eiland) die alleen op open zee
    vallen. Het oorspronkelijke zand blijft (events staan daarop)."""
    rng = random.Random('%s:%d,%d' % (M.name, min(sand)[0], min(sand)[1]))
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


def islet(M, area, sand, rocks=(), grass=()):
    area, sand = organic(M, sand)
    orig = ORIG.setdefault(M.layout, {})
    xs, ys = [p[0] for p in area], [p[1] for p in area]
    for cx, cy, dx, dy in ((min(xs), min(ys), 1, 1), (max(xs), min(ys), -1, 1), (min(xs), max(ys), 1, -1),
                           (max(xs), max(ys), -1, -1)):
        if (cx + dx, cy + dy) not in sand:
            area = area - {(cx, cy)}
    for (x, y) in area:
        c = M.v[y][x]
        assert M.beh(c) == 'MB_OCEAN_WATER' and not c & BLOCK, '%s: eiland op (%d,%d) overlapt %x %s' % (
            M.name, x, y, c & 0x3FF, M.beh(c))
        orig.setdefault('%d,%d' % (x, y), c)
    for (x, y) in area:
        M.v[y][x] = M.cell(SAND[shape(sand, x, y)]) if (x, y) in sand else M.cell(RING[shape(area, x, y)])
    for (px, py) in rocks:
        for i in range(4):
            cx, cy = px + i % 2, py + i // 2
            assert (M.v[cy][cx] & 0x3FF) == SAND['C'], '2x2-rots (%d,%d) niet op vol zand' % (px, py)
            M.v[cy][cx] = M.cell(ROCK_SAND[i], True)
    if grass:  # gras ook organisch: hoeken eraf, bulten erbij (alleen op vol zand)
        rng = random.Random('gras:%s:%d,%d' % (M.name, min(grass)[0], min(grass)[1]))
        G = set(grass)
        gx, gy = [p[0] for p in G], [p[1] for p in G]
        for cx, cy, dx, dy in ((min(gx), min(gy), 1, 1), (max(gx), min(gy), -1, 1), (min(gx), max(gy), 1, -1),
                               (max(gx), max(gy), -1, -1)):
            if rng.random() < 0.6:
                G.discard((cx, cy))
        goal = len(grass) * 3 // 2
        for _ in range(len(grass) * 30):
            if len(G) >= goal:
                break
            x, y = rng.choice(sorted(G))
            dx, dy = rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
            if (M.v[y + dy][x + dx] & 0x3FF) == SAND['C']:
                G.add((x + dx, y + dy))
        grass = G
    for (x, y) in grass:
        assert (M.v[y][x] & 0x3FF) == SAND['C'], '%s: gras (%d,%d) niet op vol zand' % (M.name, x, y)
        M.v[y][x] = M.cell(TALL_GRASS)


FAIL = []


def reach(M, start, targets, solid):
    """Surfen + lopen (alles zonder botsing), met glijden over stroomtegels. Doel = tegel waar je moet kunnen staan."""
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
    miss = [t for t in targets if t not in seen]
    if miss:
        print('%s: niet bereikbaar: %s' % (M.name, miss)); FAIL.append(M.name)
    return seen


# =====================================================================================================
# flags.h: eigen flags op vrije plekken (hoge eind)
FLAGS_H = 'include/constants/flags.h'
FLAGS = {}         # naam -> (oude FLAG_UNUSED-naam, omschrijving)
REG_FREE = ['FLAG_UNUSED_0x4FF', 'FLAG_UNUSED_0x4FA', 'FLAG_UNUSED_0x4F9', 'FLAG_UNUSED_0x4EF', 'FLAG_UNUSED_0x4EE',
            'FLAG_UNUSED_0x4ED', 'FLAG_UNUSED_0x4E8', 'FLAG_UNUSED_0x4BF', 'FLAG_UNUSED_0x4BE']
SYS_FREE = ['FLAG_UNUSED_0x%03X' % n for n in range(0x90C, 0x8E4, -1)]


def flag(name, desc, hidden=False):
    pool = SYS_FREE if hidden else REG_FREE
    FLAGS[name] = (pool.pop(0), desc)
    return name


def write_flags():
    s = open(FLAGS_H).read()
    saved = ORIG.setdefault('__flags__', {})
    for name, line in saved.items():  # eerst alles van een vorige run terugzetten
        s = re.sub(r'#define %s\b.*' % re.escape(name), lambda m: line, s)
    saved.clear()
    for name, (unused, desc) in FLAGS.items():
        assert not re.search(r'#define %s\b' % re.escape(name), s), 'vlag %s bestaat al' % name
        m = re.search(r'#define %s(\s+)(\S+(?: \+ 0x\w+\))?)\s*// Unused Flag.*' % unused, s)
        assert m, 'vlag %s niet meer vrij' % unused
        saved[name] = m.group(0)
        s = s[:m.start()] + '#define %-44s%s // Project Grounded (zeevulling 2): %s' % (name, m.group(2), desc) + s[m.end():]
    open(FLAGS_H, 'w').write(s)


# =====================================================================================================
# trainers (opponents.h + trainers.party)
TRAINERS = []   # (constante, id, omschrijving, party-tekst)
TBEGIN, TEND = '/* --- zee_vulling_2 (gegenereerd door tools/grounded/maptools/zee_vulling_2.py) --- */', '/* --- einde zee_vulling_2 --- */'
FIRST_ID = 1110


def trainer(const, desc, header, mons):
    tid = FIRST_ID + len(TRAINERS)
    TRAINERS.append((const, tid, desc, '=== %s ===\n%s\n\n%s' % (const, header.strip(), mons.strip())))
    return const


def write_trainers():
    op = open('include/constants/opponents.h').read()
    pat = r'// zee_vulling_2 \{\n.*?// \}\n'
    block = '// zee_vulling_2 {\n' + ''.join('#define %-35s %d // Project Grounded (zeevulling 2): %s\n' % (c, i, d)
                                             for c, i, d, _ in TRAINERS) + '// }\n'
    rest = re.sub(pat, '', op, flags=re.S)
    last = max([TRAINERS[-1][1]] + [int(n) for n in re.findall(r'#define TRAINER_\w+\s+(\d+)', rest)]) + 1  # ook trainers van andere scripts
    if re.search(pat, op, re.S):  # op zijn plek vervangen
        op = re.sub(pat, lambda m: block, op, count=1, flags=re.S)
    else:
        op = re.sub(r'\n(#define TRAINERS_COUNT)', lambda m: '\n' + block + '\n' + m.group(1), op)
    op = re.sub(r'(#define TRAINERS_COUNT\s+)(\d+)', lambda m: m.group(1) + str(max(last, 1107, int(m.group(2)))), op)
    open('include/constants/opponents.h', 'w').write(op)
    p = open('src/data/trainers.party').read()
    new = TBEGIN + '\n\n' + '\n\n'.join(t[3] for t in TRAINERS) + '\n\n' + TEND
    if TBEGIN in p:  # op zijn plek vervangen (geen blokken naar achteren schuiven)
        p = p[:p.index(TBEGIN)] + new + p[p.index(TEND) + len(TEND):]
    else:
        p = p.rstrip('\n') + '\n\n' + new + '\n'
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


def hdr(name, cls, pic, gender, music, double=False, ai='Check Bad Move / Try To Faint'):
    return 'Name: %s\nClass: %s\nPic: %s\nGender: %s\nMusic: %s\nDouble Battle: %s\nAI: %s' % (
        name, cls, pic, gender, music, 'Yes' if double else 'No', ai)


SMART = 'Check Bad Move / Try To Faint / Check Viability'

# =====================================================================================================
# wild_encounters.json (tekstueel)
WILD = 'src/data/wild_encounters.json'
WTEXT = [open(WILD).read()]
RATES = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]


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


def set_land(label, mons, rate=20):
    """Hele land-tabel (12 unieke soorten) zetten op een kaart die al een encountertabel heeft."""
    assert len(mons) == 12 and len({m[0] for m in mons}) == 12, label
    s = WTEXT[0]
    start, end, i = _block(label)
    blk = s[start:end]
    ind = re.search(r'\n(\s*)"base_label"', blk).group(1)
    lm = ',\n'.join('%s    { "min_level": %d, "max_level": %d, "species": "SPECIES_%s" }' % (ind, a, b, sp) for sp, a, b in mons)
    new = ('"land_mons": {\n%s  "encounter_rate": %d,\n%s  "mons": [\n%s\n%s  ]\n%s},' % (ind, rate, ind, lm, ind, ind)).replace(
        '\n%s    {' % ind, '\n%s      {' % ind)
    if '"land_mons"' in blk:
        a = blk.index('"land_mons"')
        b = blk.index('},', blk.index(']', a)) + 2
        blk = blk[:a] + new + blk[b:]
    else:
        a = blk.index('\n', blk.index('"base_label"')) + 1
        blk = blk[:a] + ind + new + '\n' + blk[a:]
    WTEXT[0] = s[:start] + blk + s[end:]


def swap_land(label, slot, old, new, lo, hi):
    """Eén slot van een bestaande land-tabel vervangen (zeldzaamheid blijft zo gelijk)."""
    s = WTEXT[0]
    start, end, i = _block(label)
    blk = s[start:end]
    a = blk.index('"land_mons"')
    lines = re.findall(r'\{\s*"min_level": \d+,\s*"max_level": \d+,\s*"species": "SPECIES_\w+"\s*\}', blk[a:blk.index(']', a)])
    assert len(lines) == 12, (label, len(lines))
    cur = re.search(r'SPECIES_(\w+)', lines[slot]).group(1)
    assert cur in (old, new), (label, slot, cur, old)
    sp = [re.search(r'SPECIES_(\w+)', l).group(1) for k, l in enumerate(lines) if k != slot]
    assert new not in sp, (label, new, 'staat al in de tabel')
    rep = re.sub(r'"min_level": \d+', '"min_level": %d' % lo, lines[slot])
    rep = re.sub(r'"max_level": \d+', '"max_level": %d' % hi, rep)
    rep = re.sub(r'SPECIES_\w+', 'SPECIES_' + new, rep)
    pos = blk.index(lines[slot], a)
    blk = blk[:pos] + rep + blk[pos + len(lines[slot]):]
    WTEXT[0] = s[:start] + blk + s[end:]


# =====================================================================================================
# map.json-hulpjes
MARK = '@ --- zee_vulling_2 (gegenereerd door tools/grounded/maptools/zee_vulling_2.py) ---'
MARK_END = '@ --- einde zee_vulling_2 ---'


def obj(gfx, x, y, script, elev=3, move='MOVEMENT_TYPE_FACE_DOWN', trainer=False, sight=0, flag='0', item=None):
    return {'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move,
            'movement_range_x': 0, 'movement_range_y': 0,
            'trainer_type': 'TRAINER_TYPE_NORMAL' if trainer else 'TRAINER_TYPE_NONE',
            'trainer_sight_or_berry_tree_id': item or str(sight), 'script': script, 'flag': flag}


def ball(x, y, item, flagname, desc):
    flag(flagname, desc)
    return obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', 3, 'MOVEMENT_TYPE_LOOK_AROUND',
               flag=flagname, item=item)


def hidden(M, x, y, item, tag):
    name = flag('FLAG_HIDDEN_ITEM_ZV2_%s_%s' % (tag, item[5:]), 'verborgen item (%s)' % M.name, hidden=True)
    return {'type': 'hidden_item', 'x': x, 'y': y, 'elevation': M.elev(x, y), 'item': item, 'flag': name}


def apply_events(M, objs, bgs, script_text):
    path = 'data/maps/%s/map.json' % M.name
    m = json.load(open(path))
    # objecten op het water: elevation 1; op het land: 3
    for o in objs:
        if M.beh(M.v[o['y']][o['x']]) in SURF: o['elevation'] = 1
    old_scripts = re.findall(r'^(\w+)::', open('data/maps/%s/scripts.inc' % M.name).read().split(MARK)[1], re.M) \
        if MARK in open('data/maps/%s/scripts.inc' % M.name).read() else []
    mine = set(old_scripts) | {o['script'] for o in objs if o['script'] != 'Common_EventScript_FindItem'}
    flags_ = {o['flag'] for o in objs if o['flag'] != '0'} | {b['flag'] for b in bgs if 'flag' in b}
    m['object_events'] = [o for o in m['object_events'] if o['script'] not in mine and o['flag'] not in flags_
                          and 'ZV2' not in o['flag']]
    m['bg_events'] = [b for b in m['bg_events'] if b.get('flag') not in flags_ and b.get('script') not in mine
                      and 'ZV2' not in b.get('flag', '')]
    m['object_events'] += objs
    m['bg_events'] += bgs
    os_ = m['object_events']
    for o in os_:
        near = [p for p in os_ if abs(p['x'] - o['x']) <= 12 and abs(p['y'] - o['y']) <= 9]
        assert len(near) <= 15, '%s: te veel objecten rond (%d,%d)' % (M.name, o['x'], o['y'])
    for o in objs:  # objecten niet op een muur, verborgen items niet op een muur
        assert not M.v[o['y']][o['x']] & BLOCK, (M.name, o['script'], o['x'], o['y'])
    for b in bgs:
        if b['type'] == 'hidden_item':
            assert not M.v[b['y']][b['x']] & BLOCK, (M.name, b['item'], b['x'], b['y'])
    open(path, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    inc_path = 'data/maps/%s/scripts.inc' % M.name
    inc = open(inc_path).read()
    new = (MARK + '\n' + script_text.strip('\n') + '\n' + MARK_END) if script_text.strip() else ''
    if MARK in inc and new:  # op zijn plek vervangen
        inc = inc[:inc.index(MARK)] + new + inc[inc.index(MARK_END) + len(MARK_END):]
    elif MARK in inc:
        inc = inc[:inc.index(MARK)].rstrip('\n') + '\n' + inc[inc.index(MARK_END) + len(MARK_END):].lstrip('\n')
    elif new:
        inc = inc.rstrip('\n') + '\n\n' + new + '\n'
    open(inc_path, 'w').write(inc)


def text(label, s):
    return '%s:\n\t.string "%s$"\n\n' % (label, s)


def talk(label, body):
    return '%s::\n%s\n\n' % (label, body.strip('\n'))


def npc(P, name, lines):
    t = P.replace('EventScript', 'Text') + name
    return talk(P + name, '\tmsgbox %s, MSGBOX_NPC\n\tend' % t) + text(t, lines)


def signpost(P, name, lines):
    t = P.replace('EventScript', 'Text') + name
    return talk(P + name, '\tmsgbox %s, MSGBOX_SIGN\n\tend' % t) + text(t, lines)


def gift(P, name, flagname, item, first, after):
    t = P.replace('EventScript', 'Text') + name
    return talk(P + name, '''
	lock
	faceplayer
	goto_if_set %s, %s_After
	msgbox %s, MSGBOX_DEFAULT
	giveitem %s
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag %s
	release
	end
%s_After:
	msgbox %sAfter, MSGBOX_DEFAULT
	release
	end''' % (flagname, P + name, t, item, flagname, P + name, t)) + text(t, first) + text(t + 'After', after)


def mon(P, name, species, lines):
    t = P.replace('EventScript', 'Text') + name
    return talk(P + name, '''
	lock
	faceplayer
	playmoncry SPECIES_%s, CRY_MODE_NORMAL
	msgbox %s, MSGBOX_DEFAULT
	waitmoncry
	release
	end''' % (species, t)) + text(t, lines)


def single(P, name, tr, intro, defeat, post):
    t = P.replace('EventScript', 'Text') + name
    return (talk(P + name, '\ttrainerbattle_single %s, %s_Intro, %s_Defeat\n\tmsgbox %s_Post, MSGBOX_AUTOCLOSE\n\tend'
                 % (tr, t, t, t)) + text(t + '_Intro', intro) + text(t + '_Defeat', defeat) + text(t + '_Post', post))


def double(P, name, tr, intro, defeat, notenough, post):
    t = P.replace('EventScript', 'Text') + name
    return (talk(P + name, '\ttrainerbattle_double %s, %s_Intro, %s_Defeat, %s_NotEnough\n\tmsgbox %s_Post, MSGBOX_AUTOCLOSE\n\tend'
                 % (tr, t, t, t, t)) + text(t + '_Intro', intro) + text(t + '_Defeat', defeat)
            + text(t + '_NotEnough', notenough) + text(t + '_Post', post))


def solid_of(objs):
    return {(o['x'], o['y']) for o in objs if o['graphics_id'] != 'OBJ_EVENT_GFX_ITEM_BALL'}


def finish(M, objs, bgs, scr, start, extra=()):
    S = solid_of(objs)
    targets = [(b['x'], b['y']) for b in bgs if b['type'] == 'hidden_item'] + list(extra)
    targets += [(o['x'], o['y']) for o in objs if o['graphics_id'] == 'OBJ_EVENT_GFX_ITEM_BALL']
    seen = reach(M, start, targets, S)
    for o in objs:  # personen/borden: een buurtegel moet bereikbaar zijn
        if (o['x'], o['y']) in S and not any((o['x'] + dx, o['y'] + dy) in seen
                                             for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            print('%s: %s niet aan te spreken' % (M.name, o['script'])); FAIL.append(M.name)
    M.save()
    apply_events(M, objs, bgs, scr)


# =====================================================================================================
# ROUTE 105 (Dewford, lv ~32): eilandje van een schipbreukeling die niet gered wil worden
M = Map('Route105')
islet(M, rect(19, 24, 27, 31), rect(20, 25, 26, 30), grass=rect(23, 27, 25, 29))
P = 'Route105_EventScript_ZV2'
F_SASH = 'FLAG_RECEIVED_ROUTE_105_FOCUS_SASH'
flag(F_SASH, 'Route 105, schipbreukeling (Focus Sash)')
KENTA = trainer('TRAINER_BLACK_BELT_KENTA', 'Route 105, eilandje van de schipbreukeling',
                hdr('KENTA', 'Black Belt', 'Black Belt', 'Male', 'Intense'),
                team(32, 12, 'Pangoro', 'Hawlucha', ('Passimian', 1)))
objs = [obj('OBJ_EVENT_GFX_HIKER', 21, 26, P + 'Castaway', move='MOVEMENT_TYPE_FACE_RIGHT'),
        obj('OBJ_EVENT_GFX_SPECIES(VOLTORB)', 22, 26, P + 'Wilson', move='MOVEMENT_TYPE_FACE_LEFT'),
        obj('OBJ_EVENT_GFX_BLACK_BELT', 26, 27, P + 'Kenta', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=3)]
bgs = [hidden(M, 20, 30, 'ITEM_BIG_PEARL', 'R105'), hidden(M, 26, 25, 'ITEM_STAR_PIECE', 'R105'),
       hidden(M, 23, 40, 'ITEM_HEART_SCALE', 'R105')]
scr = gift(P, 'Castaway', F_SASH, 'ITEM_FOCUS_SASH',
           "Rescue? No thanks.\\p"
           "I've lived on this sandbank for\\n"
           "three years. DEWFORD is right\\l"
           "there. I can see the gym.\\p"
           "I could swim back any time.\\n"
           "I choose not to. Taxes, you know.\\p"
           "Here, take this. I don't need it.\\n"
           "I can't focus on anything except\\l"
           "the horizon.",
           "WILSON and I are doing great.\\n"
           "He's a very good listener.\\l"
           "Sometimes he explodes. We all do.")
scr += mon(P, 'Wilson', 'VOLTORB',
           "A VOLTORB with a face painted on it.\\p"
           "...No, wait. That's just its face.\\n"
           "It looks at you like it's waiting\\l"
           "for an apology.")
scr += single(P, 'Kenta', KENTA,
              "Every morning I punch the tide\\n"
              "a thousand times.\\p"
              "The tide has never lost.\\n"
              "Neither have I. We're both stubborn.",
              "The tide is laughing at me.\\n"
              "I can hear it. Shhhh. Shhhh.",
              "The castaway says I'm his only\\n"
              "friend. Then he talks to the\\l"
              "VOLTORB for six hours.")
finish(M, objs, bgs, scr, (15, 0))
set_land('gRoute105', [('GUMSHOOS', 30, 32), ('RATICATE', 30, 32), ('SQUAWKABILLY', 30, 33), ('OINKOLOGNE', 30, 32),
                       ('FURFROU', 31, 33), ('LYCANROC', 31, 33), ('PANCHAM', 30, 31), ('ZANGOOSE', 31, 33),
                       ('SKITTY', 30, 32), ('MAUSHOLD', 31, 33), ('CAPSAKID', 31, 33), ('APPLIN', 31, 33)])

# =====================================================================================================
# ROUTE 108 (Slateport, lv ~31): bergingsvlot bij de Abandoned Ship (verzekeringsexpert + Sis & Bro)
M = Map('Route108')
islet(M, rect(17, 8, 24, 11), rect(18, 9, 23, 10))
P = 'Route108_EventScript_ZV2'
JOLEO = trainer('TRAINER_SIS_AND_BRO_JO_AND_LEO', 'Route 108, bergingsvlot (dubbel)',
                hdr('JO & LEO', 'Sis And Bro', 'Sis And Bro', 'Female', 'Twins', double=True),
                team(32, 15, 'Bellibolt', 'Kilowattrel', 'Maushold', 'Gumshoos'))
objs = [obj('OBJ_EVENT_GFX_GENTLEMAN', 19, 9, P + 'Adjuster', move='MOVEMENT_TYPE_FACE_RIGHT'),
        obj('OBJ_EVENT_GFX_TWIN', 22, 9, P + 'JoLeo', move='MOVEMENT_TYPE_FACE_DOWN', trainer=True, sight=2),
        obj('OBJ_EVENT_GFX_SCHOOL_KID_M', 23, 9, P + 'JoLeo', move='MOVEMENT_TYPE_FACE_DOWN', trainer=True, sight=2)]
bgs = [hidden(M, 18, 10, 'ITEM_PEARL', 'R108'), hidden(M, 23, 10, 'ITEM_NUGGET', 'R108'),
       hidden(M, 33, 9, 'ITEM_METAL_COAT', 'R108')]
scr = npc(P, 'Adjuster',
          "I'm from the insurance company.\\n"
          "Claim number 4471: that ship.\\p"
          "Cause of loss, it says here:\\n"
          "'KYOGRE.'\\p"
          "That's an act of god. Not covered.\\n"
          "Neither is 'GHOSTS'. Neither is\\l"
          "'we forgot where we parked it'.")
scr += double(P, 'JoLeo', JOLEO,
              "JO: Dad left us the salvage\\n"
              "business!\\p"
              "LEO: The business is one rope.\\n"
              "And this sandbank.",
              "JO: We lost the rope.\\n"
              "LEO: We ARE the rope now.",
              "JO: Two of us, two of yours.\\n"
              "LEO: Family rules. Bring a friend.",
              "LEO: Everything on that ship is\\n"
              "ours by salvage law.\\p"
              "JO: The ghosts disagree.\\n"
              "They have a lawyer. He's also dead.")
finish(M, objs, bgs, scr, (0, 8))

# =====================================================================================================
# ROUTE 122 (Mt. Pyre, lv ~35): veerman zonder veer, begrafenisondernemer, rouwzwemster
M = Map('Route122')
islet(M, rect(7, 32, 15, 35), rect(8, 33, 14, 34))
P = 'Route122_EventScript_ZV2'
MORT = trainer('TRAINER_MORTIMER', 'Route 122, begrafenisondernemer (Battle Stadium)',
               hdr('MORTIMER', 'Gentleman', 'Gentleman', 'Male', 'Suspicious', ai=SMART),
               team(36, 20, ('Houndstone', 0, ['Last Respects', 'Play Rough', 'Dig', 'Crunch']),
                    ('Cofagrigus', 0, ['Shadow Ball', 'Will-O-Wisp', 'Protect', 'Hex']),
                    ('Dudunsparce', 0, ['Hyper Drill', 'Coil', 'Roost', 'Glare']),
                    ('Annihilape', 1, ['Rage Fist', 'Drain Punch', 'Bulk Up', 'Close Combat'])))
CORA = trainer('TRAINER_SWIMMER_CORA', 'Route 122, zwemt baantjes rond Mt. Pyre',
               hdr('CORA', 'Swimmer F', 'Swimmer F', 'Female', 'Swimmer'),
               team(35, 12, 'Floatzel', 'Bibarel', ('Bruxish', 1)))
objs = [obj('OBJ_EVENT_GFX_OLD_MAN', 9, 33, P + 'Ferryman', move='MOVEMENT_TYPE_FACE_LEFT'),
        obj('OBJ_EVENT_GFX_MR_BRINEYS_BOAT', 6, 34, P + 'Boat', move='MOVEMENT_TYPE_FACE_RIGHT'),
        obj('OBJ_EVENT_GFX_GENTLEMAN', 13, 33, P + 'Mortimer', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=3),
        obj('OBJ_EVENT_GFX_SWIMMER_F', 29, 34, P + 'Cora', move='MOVEMENT_TYPE_LOOK_AROUND', trainer=True, sight=4)]
bgs = [hidden(M, 14, 34, 'ITEM_SPELL_TAG', 'R122'), hidden(M, 35, 20, 'ITEM_RARE_BONE', 'R122')]
scr = npc(P, 'Ferryman',
          "The fee to cross is one coin.\\p"
          "You have no coin? Then swim.\\n"
          "Everyone swims. That's the joke.\\p"
          "I used to row the dead to the\\n"
          "mountain. Now they take the\\l"
          "LILYCOVE bus. Times change.")
scr += signpost(P, 'Boat', "A small boat. Painted on the side:\\n"
                "'ONE WAY ONLY'.\\p"
                "It's been crossed out and replaced\\n"
                "with 'RETURN TRIPS NEGOTIABLE'.")
scr += single(P, 'Mortimer', MORT,
              "Ah, a customer. How... lively.\\p"
              "I'm an undertaker. Business is\\n"
              "dead. That's not a joke, it's\\l"
              "a quarterly report.",
              "Splendid. I'll put you down for\\n"
              "the premium package. Later. Much\\l"
              "later. I'm patient.",
              "Every POKeMON on MT. PYRE has a\\n"
              "grave. Except the GHOSTS.\\p"
              "They refuse. Something about\\n"
              "'commitment issues'.")
scr += single(P, 'Cora', CORA,
              "I swim laps around MT. PYRE.\\n"
              "Grandpa is up there.\\p"
              "Every lap I wave. Once, something\\n"
              "waved back. It wasn't Grandpa.",
              "Okay, okay. You win.\\n"
              "Grandpa would've cheered for you.\\l"
              "He always picked the wrong side.",
              "Lap 4,012. Still haven't seen\\n"
              "what waved back. Maybe tomorrow.")
finish(M, objs, bgs, scr, (20, 0))

# =====================================================================================================
# ROUTE 124 (Mossdeep, lv ~39): weerstation-eilandje (Castform), en kapitein Abe die de reuzen-Wailord zoekt
M = Map('Route124')
islet(M, rect(20, 22, 28, 27), rect(21, 23, 27, 26), grass=rect(23, 24, 26, 25))
islet(M, rect(33, 29, 38, 34), rect(34, 30, 37, 33))
P = 'Route124_EventScript_ZV2'
F_ROCK = 'FLAG_RECEIVED_ROUTE_124_SMOOTH_ROCK'
flag(F_ROCK, 'Route 124, weerman (Smooth Rock)')
ELLIOT = trainer('TRAINER_BUG_MANIAC_ELLIOT', 'Route 124, weerstation (insecten)',
                 hdr('ELLIOT', 'Bug Maniac', 'Bug Maniac', 'Male', 'Suspicious'),
                 team(39, 12, 'Volbeat', 'Illumise', 'Galvantula', ('Vikavolt', 1)))
ABE = trainer('TRAINER_CAPTAIN_ABE', 'Route 124, kapitein op walvisjacht (Battle Stadium)',
              hdr('ABE', 'Sailor', 'Sailor', 'Male', 'Male', ai=SMART),
              team(40, 20, ('Grapploct', 0, ['Octolock', 'Drain Punch', 'Liquidation', 'Bulk Up']),
                   ('Dhelmise', 0, ['Anchor Shot', 'Power Whip', 'Shadow Claw', 'Rapid Spin']),
                   ('Eelektross', 0, ['Wild Charge', 'Crunch', 'Thunder Punch', 'Acid Spray']),
                   ('Barraskewda', 0, ['Liquidation', 'Psychic Fangs', 'Aqua Jet', 'Drill Run']),
                   ('Sharpedo', 1, ['Crunch', 'Waterfall', 'Ice Fang', 'Aqua Jet'])))
objs = [obj('OBJ_EVENT_GFX_SCIENTIST_1', 22, 24, P + 'Weatherman', move='MOVEMENT_TYPE_FACE_RIGHT'),
        obj('OBJ_EVENT_GFX_SPECIES(CASTFORM)', 21, 25, P + 'Castform', move='MOVEMENT_TYPE_FACE_RIGHT'),
        obj('OBJ_EVENT_GFX_BUG_CATCHER', 27, 23, P + 'Elliot', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=3),
        obj('OBJ_EVENT_GFX_SAILOR', 36, 31, P + 'Abe', move='MOVEMENT_TYPE_FACE_RIGHT', trainer=True, sight=2),
        obj('OBJ_EVENT_GFX_MR_BRINEYS_BOAT', 39, 31, P + 'AbeBoat', move='MOVEMENT_TYPE_FACE_LEFT')]
bgs = [hidden(M, 27, 26, 'ITEM_PP_UP', 'R124'), hidden(M, 34, 33, 'ITEM_BIG_PEARL', 'R124'),
       hidden(M, 12, 28, 'ITEM_HEART_SCALE', 'R124')]
scr = gift(P, 'Weatherman', F_ROCK, 'ITEM_SMOOTH_ROCK',
           "Welcome to HOENN WEATHER STATION\\n"
           "number 2. Number 1 blew away.\\p"
           "My equipment: one CASTFORM.\\n"
           "If it's round, nice weather.\\l"
           "If it's on fire, also nice weather.\\p"
           "If it's gone, run.\\p"
           "Here, a souvenir. It's a rock.\\n"
           "Very smooth. Science!",
           "Today's forecast: weather.\\n"
           "I'm right 100% of the time.")
scr += mon(P, 'Castform', 'CASTFORM',
           "The CASTFORM is round.\\n"
           "The forecast is good.\\p"
           "It looks very proud of this.")
scr += single(P, 'Elliot', ELLIOT,
              "Shh! The VOLBEAT and ILLUMISE\\n"
              "dance here at night.\\p"
              "I've been watching them for a\\n"
              "week. I think they're watching\\l"
              "me back. Battle!",
              "My bugs are fine. They're just\\n"
              "lying down. Dramatically.",
              "The weatherman says there's a\\n"
              "storm coming. He says that every\\l"
              "day. One day he'll be right.")
scr += single(P, 'Abe', ABE,
              "Call me ABE. Somewhere in these\\n"
              "waters swims a WAILORD the size\\l"
              "of a town. White as a cloud.\\p"
              "It took my boat. My hat. My\\n"
              "sandwich. Today I take it back!",
              "Argh! You fight like that WAILORD.\\n"
              "Heavy. Wet. Unbothered.",
              "Some days the giant WAILORD is\\n"
              "here, some days it isn't.\\p"
              "When it is, it's asleep. I've\\n"
              "never had the heart to wake it.")
scr += signpost(P, 'AbeBoat', "ABE's boat. Named the 'SEQUEL'.\\p"
                "The first boat is inside a WAILORD.")
finish(M, objs, bgs, scr, (0, 23))
set_land('gRoute124', [('CASTFORM', 38, 40), ('ORICORIO', 38, 40), ('VOLBEAT', 38, 41), ('ILLUMISE', 38, 41),
                       ('SPINDA', 38, 40), ('PIDGEOT', 39, 41), ('FARFETCHD', 38, 40), ('SQUAWKABILLY', 38, 41),
                       ('DUNSPARCE', 38, 40), ('TROPIUS', 39, 41), ('AMPHAROS', 40, 42), ('LUXRAY', 40, 42)])

# =====================================================================================================
# ROUTE 128 (lv ~41): Dereks dojo, een gezakte League-kandidaat met verwilderde trainingspartners
M = Map('Route128')
islet(M, rect(100, 3, 110, 9), rect(101, 4, 109, 8), grass=rect(105, 5, 108, 7))
P = 'Route128_EventScript_ZV2'
DEREK = trainer('TRAINER_EXPERT_DEREK', 'Route 128, eigen dojo-eilandje (Battle Stadium)',
                hdr('DEREK', 'Expert', 'Expert M', 'Male', 'Intense', ai=SMART),
                team(42, 22, ('Bewear', 0, ['Hammer Arm', 'Double-Edge', 'Bulk Up', 'Shadow Claw']),
                     ('Falinks', 0, ['No Retreat', 'Megahorn', 'Close Combat', 'First Impression']),
                     ('Lucario', 0, ['Aura Sphere', 'Flash Cannon', 'Dark Pulse', 'Vacuum Wave']),
                     ('Mienshao', 0, ['High Jump Kick', 'U-turn', 'Fake Out', 'Poison Jab']),
                     ('Conkeldurr', 1, ['Mach Punch', 'Drain Punch', 'Knock Off', 'Rock Slide'])))
JUNO = trainer('TRAINER_BATTLE_GIRL_JUNO', 'Route 128, Dereks enige leerling',
               hdr('JUNO', 'Battle Girl', 'Battle Girl', 'Female', 'Intense'),
               team(41, 12, 'Hawlucha', 'Lopunny', ('Breloom', 1)))
objs = [obj('OBJ_EVENT_GFX_EXPERT_M', 103, 6, P + 'Derek', move='MOVEMENT_TYPE_FACE_DOWN', trainer=True, sight=2),
        obj('OBJ_EVENT_GFX_EXPERT_F', 102, 8, P + 'Juno', move='MOVEMENT_TYPE_FACE_RIGHT', trainer=True, sight=3),
        ball(109, 8, 'ITEM_BLACK_BELT', 'FLAG_ITEM_ROUTE_128_BLACK_BELT', 'Route 128, Dereks dojo')]
bgs = [hidden(M, 101, 4, 'ITEM_PROTEIN', 'R128'), hidden(M, 109, 4, 'ITEM_HP_UP', 'R128'),
       hidden(M, 112, 15, 'ITEM_STAR_PIECE', 'R128')]
scr = single(P, 'Derek', DEREK,
             "I'm DEREK. I challenged the\\n"
             "POKeMON LEAGUE 47 times.\\p"
             "I lost to SIDNEY 47 times.\\n"
             "He sends me a birthday card now.\\p"
             "So I built a dojo. On a sandbank.\\n"
             "Next to EVER GRANDE. To stare.",
             "48 losses. Same as SIDNEY.\\n"
             "Well. Similar.",
             "My old training partners ran into\\n"
             "the grass. They went wild.\\p"
             "Literally. Catch them if you want.\\n"
             "They never listened to me anyway.")
scr += single(P, 'Juno', JUNO,
              "I'm DEREK's only student!\\p"
              "He's a great teacher. He knows\\n"
              "exactly how to lose. So I know\\l"
              "exactly what NOT to do!",
              "Oh no. I did what he does.",
              "Membership fee is zero. Monthly.\\n"
              "DEREK says it's 'exclusive'.")
finish(M, objs, bgs, scr, (110, 0))  # vanaf Route 127 (het westdeel is een afgesloten bekken)
set_land('gRoute128', [('THROH', 40, 42), ('SAWK', 40, 42), ('PANGORO', 40, 43), ('FALINKS', 40, 42),
                       ('HAWLUCHA', 41, 43), ('PASSIMIAN', 41, 43), ('MACHOKE', 40, 42), ('BEWEAR', 41, 43),
                       ('PRIMEAPE', 40, 42), ('HITMONCHAN', 41, 43), ('MIENSHAO', 42, 44), ('GURDURR', 42, 44)])

# =====================================================================================================
# ROUTE 129 (lv ~40): Wailord-safari zonder Wailord (gids + huwelijksreis-koppel)
M = Map('Route129')
islet(M, rect(60, 29, 70, 34), rect(61, 30, 69, 33))
P = 'Route129_EventScript_ZV2'
TOMTINA = trainer('TRAINER_YOUNG_COUPLE_TOM_AND_TINA', 'Route 129, op huwelijksreis (dubbel)',
                  hdr('TOM & TINA', 'Young Couple', 'Young Couple', 'Male', 'Girl', double=True),
                  team(41, 15, 'Delcatty', 'Furfrou', 'Ampharos', 'Leavanny'))
objs = [obj('OBJ_EVENT_GFX_WOMAN_5', 62, 31, P + 'Guide', move='MOVEMENT_TYPE_FACE_LEFT'),
        obj('OBJ_EVENT_GFX_MR_BRINEYS_BOAT', 59, 31, P + 'TourBoat', move='MOVEMENT_TYPE_FACE_RIGHT'),
        obj('OBJ_EVENT_GFX_MAN_3', 66, 31, P + 'Couple', move='MOVEMENT_TYPE_FACE_DOWN', trainer=True, sight=2),
        obj('OBJ_EVENT_GFX_WOMAN_2', 67, 31, P + 'Couple', move='MOVEMENT_TYPE_FACE_DOWN', trainer=True, sight=2)]
bgs = [hidden(M, 69, 33, 'ITEM_PEARL_STRING', 'R129'), hidden(M, 64, 33, 'ITEM_ULTRA_BALL', 'R129')]
scr = npc(P, 'Guide',
          "Welcome to WAILORD WATCHING TOURS!\\n"
          "Today is day 41 without a WAILORD.\\p"
          "We do see water. Lots of it.\\n"
          "Very authentic.\\p"
          "Refunds are available in the form\\n"
          "of more water.")
scr += signpost(P, 'TourBoat', "A tour boat. A sign on it reads:\\n"
                "'WAILORD GUARANTEED'.\\p"
                "Underneath, in very small letters:\\n"
                "'guarantee not guaranteed'.")
scr += double(P, 'Couple', TOMTINA,
              "TOM: We're on our honeymoon!\\n"
              "TINA: We booked the WAILORD tour!\\p"
              "TOM: There's no WAILORD.\\n"
              "TINA: There's YOU though!",
              "TINA: Still the best honeymoon.\\n"
              "TOM: It's our only honeymoon.",
              "TOM: It's a couples thing.\\n"
              "TINA: Come back with a plus-one!",
              "TINA: Someone said a giant WAILORD\\n"
              "naps on these routes sometimes.\\p"
              "TOM: We'll stay until we see it.\\n"
              "TINA: We've been here since June.")
finish(M, objs, bgs, scr, (0, 35))

# =====================================================================================================
# ROUTE 130 (lv ~40): Wynaut-kinderopvang ("we are not responsible")
M = Map('Route130')
islet(M, rect(30, 1, 40, 5), rect(31, 2, 39, 4))
P = 'Route130_EventScript_ZV2'
HONEY = trainer('TRAINER_BREEDER_HONEY', 'Route 130, Wynaut-kinderopvang',
                hdr('HONEY', 'Pkmn Breeder', 'Pokemon Breeder F', 'Female', 'Female'),
                team(40, 12, 'Audino', 'Wobbuffet', 'Indeedee', ('Blissey', 1)))
# FLAG_TEMP_6: de crèche staat niet op de Mirage-layout (setflag in Route130 ON_TRANSITION)
objs = [obj('OBJ_EVENT_GFX_WOMAN_4', 33, 3, P + 'Teacher', move='MOVEMENT_TYPE_LOOK_AROUND', flag='FLAG_TEMP_6'),
        obj('OBJ_EVENT_GFX_SPECIES(WYNAUT)', 35, 3, P + 'WynautA', move='MOVEMENT_TYPE_LOOK_AROUND', flag='FLAG_TEMP_6'),
        obj('OBJ_EVENT_GFX_SPECIES(WYNAUT)', 36, 2, P + 'WynautB', move='MOVEMENT_TYPE_FACE_DOWN', flag='FLAG_TEMP_6'),
        obj('OBJ_EVENT_GFX_SPECIES(WYNAUT)', 32, 4, P + 'WynautC', move='MOVEMENT_TYPE_FACE_UP', flag='FLAG_TEMP_6'),
        obj('OBJ_EVENT_GFX_POKEFAN_F', 38, 3, P + 'Honey', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=3, flag='FLAG_TEMP_6'),
        ball(39, 4, 'ITEM_EVERSTONE', 'FLAG_ITEM_ROUTE_130_EVERSTONE', 'Route 130, Wynaut-kinderopvang')]
bgs = [hidden(M, 31, 4, 'ITEM_LUCKY_PUNCH', 'R130'), hidden(M, 50, 3, 'ITEM_STARDUST', 'R130')]
scr = npc(P, 'Teacher',
          "Welcome to WYNAUT DAYCARE!\\n"
          "Motto: 'Why not?'\\p"
          "Small print: we are not\\n"
          "responsible.\\p"
          "Not for lost WYNAUT, not for found\\n"
          "WYNAUT, not for WYNAUT that are\\l"
          "now somehow a WOBBUFFET.")
scr += mon(P, 'WynautA', 'WYNAUT', "WYNAUT: Wy? Wy? Wynaut!\\p"
           "It has asked 'why' 300 times today.\\n"
           "Nobody has an answer.")
scr += mon(P, 'WynautB', 'WYNAUT', "WYNAUT: Wynaaaut.\\p"
           "It's taking a nap standing up.\\n"
           "Its tail is still awake.")
scr += mon(P, 'WynautC', 'WYNAUT', "WYNAUT: Wy!\\p"
           "It's guarding a sandcastle.\\n"
           "The sandcastle is just sand.")
scr += single(P, 'Honey', HONEY,
              "Shift change! I'm the night\\n"
              "supervisor. It is noon.\\p"
              "Battle me, sweetie. Nap time\\n"
              "starts when I win.",
              "No nap for anyone, then.\\n"
              "The WYNAUT will riot.",
              "Parents pick them up from MIRAGE\\n"
              "ISLAND. When it's there.\\p"
              "When it isn't... more WYNAUT.")
finish(M, objs, bgs, scr, (79, 3))

# =====================================================================================================
# ROUTE 131 (lv ~40): "nurse's cousin" die je team gratis heelt, en een verdwaalde Hiker
M = Map('Route131')
islet(M, rect(15, 23, 23, 27), rect(16, 24, 22, 26))
P = 'Route131_EventScript_ZV2'
BERNARD = trainer('TRAINER_HIKER_BERNARD', 'Route 131, verdwaalde bergbeklimmer',
                  hdr('BERNARD', 'Hiker', 'Hiker', 'Male', 'Hiker'),
                  team(41, 12, 'Throh', 'Sawk', 'Lycanroc', ('Coalossal', 1)))
objs = [obj('OBJ_EVENT_GFX_NURSE', 18, 25, P + 'Cousin', move='MOVEMENT_TYPE_FACE_DOWN'),
        obj('OBJ_EVENT_GFX_HIKER', 21, 24, P + 'Bernard', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=3)]
bgs = [hidden(M, 22, 26, 'ITEM_HYPER_POTION', 'R131'), hidden(M, 40, 26, 'ITEM_BIG_PEARL', 'R131')]
scr = talk(P + 'Cousin', '''
	lock
	faceplayer
	msgbox Route131_Text_ZV2Cousin, MSGBOX_DEFAULT
	fadescreen FADE_TO_BLACK
	playfanfare MUS_HEAL
	waitfanfare
	special HealPlayerParty
	fadescreen FADE_FROM_BLACK
	msgbox Route131_Text_ZV2CousinDone, MSGBOX_DEFAULT
	release
	end''')
scr += text('Route131_Text_ZV2Cousin',
            "I'm not a NURSE. I'm a nurse's\\n"
            "cousin. Very different.\\p"
            "No license, no POKeMON CENTER,\\n"
            "no machine. Just vibes.\\p"
            "Hold still.")
scr += text('Route131_Text_ZV2CousinDone',
            "There. All better.\\n"
            "Don't ask what I did.\\l"
            "Legally I can't tell you.")
scr += single(P, 'Bernard', BERNARD,
              "I followed the tallest mountain\\n"
              "I could see.\\p"
              "It was SKY PILLAR. It's a tower.\\n"
              "I don't do towers. I do rocks.",
              "Rocks: 0. Towers: 1. You: 1.\\n"
              "I hate this scoreboard.",
              "The nurse lady fixed my knee.\\n"
              "It's my other knee now. Somehow.")
finish(M, objs, bgs, scr, (59, 24))

# =====================================================================================================
# ROUTE 133 (lv ~39): influencer op een zandbank (vaargeul x 28-31 vrijhouden)
M = Map('Route133')
islet(M, rect(3, 20, 12, 23), rect(4, 21, 11, 22))
P = 'Route133_EventScript_ZV2'
BRAYDEN = trainer('TRAINER_BRAYDEN', 'Route 133, influencer op een zandbank (Battle Stadium)',
                  hdr('BRAYDEN', 'Rich Boy', 'Rich Boy', 'Male', 'Rich', ai=SMART),
                  team(40, 20, ('Furfrou', 0, ['Double-Edge', 'Thunder Wave', 'U-turn', 'Bite']),
                       ('Toxtricity', 0, ['Overdrive', 'Sludge Bomb', 'Boomburst', 'Volt Switch']),
                       ('Oricorio', 0, ['Revelation Dance', 'Hurricane', 'Quiver Dance', 'Teeter Dance']),
                       ('Hawlucha', 0, ['Flying Press', 'Swords Dance', 'Acrobatics', 'Brick Break']),
                       ('Lopunny', 1, ['Fake Out', 'High Jump Kick', 'Bounce', 'Ice Punch'])))
objs = [obj('OBJ_EVENT_GFX_RICH_BOY', 6, 21, P + 'Brayden', move='MOVEMENT_TYPE_FACE_DOWN', trainer=True, sight=2),
        obj('OBJ_EVENT_GFX_CAMERAMAN', 8, 22, P + 'Cameraman', move='MOVEMENT_TYPE_FACE_LEFT'),
        ball(11, 22, 'ITEM_CHOICE_SPECS', 'FLAG_ITEM_ROUTE_133_CHOICE_SPECS', 'Route 133, zandbank van de influencer')]
bgs = [hidden(M, 4, 22, 'ITEM_NUGGET', 'R133'), hidden(M, 40, 21, 'ITEM_PEARL', 'R133')]
scr = single(P, 'Brayden', BRAYDEN,
             "Hey guys, BRAYDEN here! We're\\n"
             "LIVE from a literal sandbank!\\p"
             "Today's challenge: battle a random\\n"
             "kid! Smash that LIKE button!\\p"
             "The LIKE button is my POKeMON's\\n"
             "face. Smash it. Respectfully.",
             "...Cut that. CUT THAT.\\n"
             "We're doing a 'lessons learned'\\l"
             "video now.",
             "My sponsor sent me those glasses.\\n"
             "I threw them over there.\\p"
             "They only let you pick one move.\\n"
             "My brand is about OPTIONS.")
scr += npc(P, 'Cameraman',
           "I'm not his cameraman. I'm his\\n"
           "dad. He pays me in exposure.\\p"
           "We've been on this sandbank for\\n"
           "four hours. The view count is 3.\\l"
           "Two of them are me.")
finish(M, objs, bgs, scr, (79, 20))
for x in range(28, 32):  # vaargeul naar de drijvende markt: niets van ons in x 28-31
    assert all(not (o['x'] == x) for o in objs), x

# =====================================================================================================
# ROUTE 134 (lv ~40): architect die een vuurtoren wil bouwen, en een ninja in het zand
M = Map('Route134')
islet(M, rect(3, 8, 12, 13), rect(4, 9, 11, 12))
P = 'Route134_EventScript_ZV2'
KAGE = trainer('TRAINER_NINJA_BOY_KAGE', 'Route 134, ninja op een zandbank',
               hdr('KAGE', 'Ninja Boy', 'Ninja Boy', 'Male', 'Suspicious'),
               team(40, 12, 'Ninjask', 'Accelgor', ('Lokix', 1)))
objs = [obj('OBJ_EVENT_GFX_MAN_2', 6, 10, P + 'Architect', move='MOVEMENT_TYPE_LOOK_AROUND'),
        obj('OBJ_EVENT_GFX_NINJA_BOY', 10, 11, P + 'Kage', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=3),
        ball(11, 12, 'ITEM_LIGHT_CLAY', 'FLAG_ITEM_ROUTE_134_LIGHT_CLAY', 'Route 134, bouwplaats vuurtoren')]
bgs = [hidden(M, 5, 12, 'ITEM_STAR_PIECE', 'R134'), hidden(M, 20, 21, 'ITEM_ZINC', 'R134')]
scr = npc(P, 'Architect',
          "This is where the lighthouse goes.\\n"
          "Big. White. Stripes. A light.\\p"
          "Problem: nobody in HOENN knows what\\n"
          "a lighthouse looks like.\\p"
          "I asked around. Someone drew me a\\n"
          "very tall PEEKO. I'm considering it.\\p"
          "...Wait. There's one south of ROUTE 133\\n"
          "already? And the lamp is a LANTURN?\\p"
          "Cheater.")
scr += single(P, 'Kage', KAGE,
              "...!\\p"
              "You saw me?! I was hiding! In the\\n"
              "sand! In full black clothing!",
              "My disguise needs work.\\n"
              "Maybe a beige ninja.",
              "The architect thinks I'm a\\n"
              "lighthouse. I'm not correcting him.")
finish(M, objs, bgs, scr, (79, 8))

# =====================================================================================================
# WHIRL ISLAND (lagune, lv ~45): vuurtorenwachter zonder vuurtoren + zijn Slowpoke, Bird Keeper wacht op Lugia
M = Map('WhirlIsland')
islet(M, rect(26, 4, 35, 7), rect(27, 5, 34, 6))
P = 'WhirlIsland_EventScript_ZV2'
F_KROCK = 'FLAG_RECEIVED_WHIRL_ISLAND_KINGS_ROCK'
flag(F_KROCK, 'Whirl Island, zwijgende wachter (King\'s Rock)')
SKYE = trainer('TRAINER_BIRD_KEEPER_SKYE', 'Whirl Island, wacht op een grote vogel',
               hdr('SKYE', 'Bird Keeper', 'Bird Keeper', 'Male', 'Cool'),
               team(45, 15, 'Pidgeot', 'Staraptor', 'Squawkabilly', ('Braviary', 1)))
objs = [obj('OBJ_EVENT_GFX_OLD_MAN', 29, 5, P + 'Keeper', move='MOVEMENT_TYPE_FACE_DOWN'),
        obj('OBJ_EVENT_GFX_SPECIES(SLOWPOKE)', 30, 5, P + 'Slowpoke', move='MOVEMENT_TYPE_FACE_DOWN'),
        obj('OBJ_EVENT_GFX_MAN_5', 33, 6, P + 'Skye', move='MOVEMENT_TYPE_LOOK_AROUND', trainer=True, sight=3),
        ball(24, 31, 'ITEM_SHARP_BEAK', 'FLAG_ITEM_WHIRL_ISLAND_SHARP_BEAK', 'Whirl Island, strand van de lagune')]
bgs = [hidden(M, 13, 28, 'ITEM_PP_MAX', 'WHIRL'), hidden(M, 34, 5, 'ITEM_BIG_NUGGET', 'WHIRL')]
scr = gift(P, 'Keeper', F_KROCK, 'ITEM_KINGS_ROCK',
           "...\\p"
           "(The old man hasn't spoken in a\\n"
           "year. He points at his SLOWPOKE.)\\p"
           "SLOWPOKE: ...Yawn.\\p"
           "(Apparently that means 'take this'.\\n"
           "He hands you a crown-shaped rock.)",
           "...\\p"
           "(He points at the sea. Then at the\\n"
           "sky. Then at his SLOWPOKE. Then he\\l"
           "goes back to staring.)")
scr += mon(P, 'Slowpoke', 'SLOWPOKE',
           "SLOWPOKE: ......................\\p"
           "...Pokaaa?\\p"
           "It answered a question you asked\\n"
           "four minutes ago.")
scr += single(P, 'Skye', SKYE,
              "Something huge sleeps below this\\n"
              "island. A bird! A BIG bird!\\p"
              "I've waited three summers. My\\n"
              "birds are bored. Entertain them!",
              "My birds are entertained.\\n"
              "I am not.",
              "The old man knows something.\\n"
              "He won't say. His SLOWPOKE says\\l"
              "'yawn'. I've decoded nothing.")
finish(M, objs, bgs, scr, (19, 33))

# =====================================================================================================
# Losse verborgen items in het water van de volle landroutes (alleen extra vondsten; geen nieuwe objecten)
for mapname, x, y, item, tag in [('Route110', 20, 27, 'ITEM_PEARL', 'R110'), ('Route115', 5, 27, 'ITEM_BIG_PEARL', 'R115'),
                                 ('Route118', 22, 10, 'ITEM_HEART_SCALE', 'R118'),
                                 ('Route119', 18, 35, 'ITEM_MYSTIC_WATER', 'R119'),
                                 ('Route120', 27, 70, 'ITEM_PEARL_STRING', 'R120')]:
    M = Map(mapname)
    assert M.beh(M.v[y][x]) in SURF and not M.v[y][x] & BLOCK, (mapname, x, y, M.beh(M.v[y][x]))
    apply_events(M, [], [hidden(M, x, y, item, tag)], '')

# =====================================================================================================
# Vergeten gewone lijnen in het wild (task 2): slot vervangen, zeldzaamheid blijft gelijk
for label, slot, old, new, lo, hi in [
        ('gRoute101', 0, 'POOCHYENA', 'RATTATA', 2, 3),
        ('gRoute103', 7, 'ZIGZAGOON', 'MEOWTH', 4, 4),
        ('gRoute104', 0, 'WINGULL', 'CATERPIE', 7, 8),
        ('gRoute104', 3, 'MARILL', 'RATTATA', 8, 8),
        ('gPetalburgWoods', 0, 'POOCHYENA', 'CATERPIE', 9, 9),
        ('gPetalburgWoods', 8, 'TAILLOW', 'SKWOVET', 9, 10),
        ('gRoute110', 1, 'MAGNEMITE', 'GLAMEOW', 12, 14),
        ('gRoute116', 5, 'COTTONEE', 'BUNEARY', 10, 11),
        ('gRoute118', 1, 'FURRET', 'RATICATE', 24, 26),
        ('gRoute119', 4, 'TROPIUS', 'KOMALA', 27, 29),
        ('gRoute120', 7, 'KECLEON', 'GREEDENT', 31, 33),
        ('gRoute121', 5, 'LINOONE', 'GLAMEOW', 29, 31),
        ('gFortreeJungle', 2, 'VENOMOTH', 'KOMALA', 32, 34)]:
    swap_land(label, slot, old, new, lo, hi)

assert not FAIL, FAIL
open(WILD, 'w').write(WTEXT[0])
json.loads(WTEXT[0])
write_flags()
write_trainers()
json.dump(ORIG, open(ORIG_PATH, 'w'), indent=0, sort_keys=True)
print('ok: %d trainers (%d-%d), %d flags' % (len(TRAINERS), FIRST_ID, FIRST_ID + len(TRAINERS) - 1, len(FLAGS)))
