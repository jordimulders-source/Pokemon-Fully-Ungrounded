"""Project Grounded: zeevulling 3 (de gaten na zeevulling 1 en 2).

- Onderwater 127: zeewier + wilde Pokémon, het anker van de S.S. TIDAL; onderwater 128: een gezonken
  postzak; onderwater 129: een piratenkist (X marks the spot); extra verborgen items op onderwater 125/129.
- Verborgen items op Route 107, 122, 125, 126, 129, 131, 133 en Whirl Island (vijf rond de lagune).
- Nieuwe trainers met een andere klasse: Hex Maniac Vesper (122), Sailor Marty (126), Ranger Coral (129),
  Sailor Rusty (131).
- Eilandje-NPC's: afhaalbalie bij SUSHI 107, bergingsduiker die Heart Scales ruilt (131), meteoroloog met een
  Castform-waarnemingspost (133).
- Garbage Patch (126): de tv, het toegangsbewijs, een boei en 's nachts een Seel die Pokéradio luistert.
- Route 127: zeemijnenveld (Voltorb/Electrode en één Hisui-Voltorb; komen terug als je de kaart verlaat).

Werkt als zee_vulling_2.py (gekopieerde hulpjes; eigen markeringen ZV3, eigen _orig.json, trainers vanaf 1170).
Gebruik (vanuit de repo-root): python3 tools/grounded/maptools/zee_vulling_3.py
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
random.seed(1093)
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


ORIG_PATH = 'tools/grounded/maptools/zee_vulling_3_orig.json'
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
# LET OP (merge 8 okt): 14 flags uit deze pool botsten met landvulling en zijn in flags.h met de hand verplaatst
# (0x276, 0x2D9, 0x468, 0x470, 0x472, 0x479, 0x49C-0x4A0, dagelijks 0x940-0x942). Pas de pool aan vóór je dit opnieuw draait.
FLAGS_H = 'include/constants/flags.h'
FLAGS = {}         # naam -> (oude FLAG_UNUSED-naam, omschrijving)
# Flags zijn schaars: alleen de laatste vrije systeemflags (0x8E3, 0x8E5-0x8ED) en vijf R/S-overblijfselen die
# nergens gebruikt worden (0x409, 0x465-0x467, 0x46D). Eén pool voor alles.
SYS_FREE = ['FLAG_UNUSED_0x8E3'] + ['FLAG_UNUSED_0x%03X' % n for n in range(0x8E5, 0x8EE)] + [
    'FLAG_ITEM_ROUTE_123_RARE_CANDY', 'FLAG_ITEM_OLD_MAGMA_HIDEOUT_B1F_MASTER_BALL',
    'FLAG_ITEM_OLD_MAGMA_HIDEOUT_B1F_MAX_ELIXIR', 'FLAG_ITEM_OLD_MAGMA_HIDEOUT_B2F_NEST_BALL',
    'FLAG_ITEM_MOSSDEEP_STEVENS_HOUSE_HM08']
REG_FREE = SYS_FREE


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
        s = s[:m.start()] + '#define %-44s%s // Project Grounded (zeevulling 3): %s' % (name, m.group(2), desc) + s[m.end():]
    open(FLAGS_H, 'w').write(s)


# =====================================================================================================
# trainers (opponents.h + trainers.party)
TRAINERS = []   # (constante, id, omschrijving, party-tekst)
TBEGIN, TEND = '/* --- zee_vulling_3 (gegenereerd door tools/grounded/maptools/zee_vulling_3.py) --- */', '/* --- einde zee_vulling_3 --- */'
FIRST_ID = 1170


def trainer(const, desc, header, mons):
    tid = FIRST_ID + len(TRAINERS)
    TRAINERS.append((const, tid, desc, '=== %s ===\n%s\n\n%s' % (const, header.strip(), mons.strip())))
    return const


def write_trainers():
    op = open('include/constants/opponents.h').read()
    op = re.sub(r'\n// zee_vulling_3 \{\n.*?// \}\n', '\n', op, flags=re.S)
    block = '// zee_vulling_3 {\n' + ''.join('#define %-35s %d // Project Grounded (zeevulling 3): %s\n' % (c, i, d)
                                             for c, i, d, _ in TRAINERS) + '// }\n'
    last = max([TRAINERS[-1][1]] + [int(n) for n in re.findall(r'#define TRAINER_\w+\s+(\d+)', op)]) + 1  # ook trainers van andere scripts
    op = re.sub(r'\n(#define TRAINERS_COUNT\s+)(\d+)', lambda m: '\n' + block + '\n' + m.group(1) + str(max(last, FIRST_ID + len(TRAINERS))), op)
    op = re.sub(r'\n{3,}(// zee_vulling_3 \{)', r'\n\n\1', op)
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
MARK = '@ --- zee_vulling_3 (gegenereerd door tools/grounded/maptools/zee_vulling_3.py) ---'
MARK_END = '@ --- einde zee_vulling_3 ---'


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
    name = flag('FLAG_HIDDEN_ITEM_ZV3_%s_%s' % (tag, item[5:]), 'verborgen item (%s)' % M.name, hidden=True)
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
                          and 'ZV3' not in o['flag']]
    m['bg_events'] = [b for b in m['bg_events'] if b.get('flag') not in flags_ and b.get('script') not in mine
                      and 'ZV3' not in b.get('flag', '')]
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
    if MARK in inc:
        inc = inc[:inc.index(MARK)].rstrip('\n') + '\n' + inc[inc.index(MARK_END) + len(MARK_END):].lstrip('\n')
    if script_text.strip():
        inc = inc.rstrip('\n') + '\n\n' + MARK + '\n' + script_text.strip('\n') + '\n' + MARK_END + '\n'
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
# extra hulpjes (zeevulling 3)
def sign(x, y, script, elev=3):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': elev, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
            'script': script}


def keep_events(M):
    """Eilandjes mogen niet groeien over bestaande objecten/verborgen items (± 2 tegels)."""
    keep = set(SEA_KEEP.get(M.name, set()))
    for e in M.json['object_events'] + M.json['bg_events']:
        if 'ZV3' in e.get('flag', '') or 'ZV3' in e.get('script', ''):
            continue
        keep |= rect(e['x'] - 2, e['y'] - 2, e['x'] + 2, e['y'] + 2)
    SEA_KEEP[M.name] = keep


SEAWEED = {0x2A9: 0x281, 0x216: 0x201, 0x25B: 0x281, 0x256: 0x281}  # bodem -> zeewier (zie zee_vulling_1.py)


def seaweed(M, patches):
    rng = random.Random('zeewier:%s' % M.name)
    orig = ORIG.setdefault(M.layout, {})
    n = 0
    for (cx, cy, r) in patches:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r - 1, cx + r + 2):
                if not (0 <= x < M.w and 0 <= y < M.h): continue
                d = ((x - cx) / (r + 1.0)) ** 2 + ((y - cy) / (r + 0.5)) ** 2
                if d <= 1.0 and rng.random() < 0.85 and (M.v[y][x] & 0x3FF) in SEAWEED:
                    orig.setdefault('%d,%d' % (x, y), M.v[y][x])
                    M.v[y][x] = (M.v[y][x] & ~0x3FF) | SEAWEED[M.v[y][x] & 0x3FF]; n += 1
    print('%s: %d zeewiertegels' % (M.name, n))
    assert n >= 12, M.name


def add_water_table(label, mapconst, after_label, mons):
    """Nieuwe water-tabel (5 slots) achter een bestaande; idempotent (bestaand blok wordt vervangen)."""
    assert len(mons) == 5 and len({m[0] for m in mons}) == 5
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


def hook(mapname, label, line):
    """Eén regel (call) direct na een label in scripts.inc buiten ons blok; idempotent."""
    p = 'data/maps/%s/scripts.inc' % mapname
    s = open(p).read()
    if line in s:
        return
    s = s.replace('%s:\n' % label, '%s:\n%s\n' % (label, line), 1)
    assert line in s, (mapname, label)
    open(p, 'w').write(s)


def wild(P, name, species, level, text_label):
    return talk(P + name, '''
	lock
	faceplayer
	playmoncry SPECIES_%s, CRY_MODE_ENCOUNTER
	msgbox %s, MSGBOX_DEFAULT
	waitmoncry
	setwildbattle SPECIES_%s, %d
	dowildbattle
	removeobject VAR_LAST_TALKED
	release
	end''' % (species, text_label, species, level))



def sync_layout(M, dst_name):
    """Kaarten die in hun map-script een andere layout kiezen (Route 131 gebruikt in het spel altijd
    Route131_SkyPillar_Layout): alle cellen die zeevulling 2 en 3 in de gewone layout veranderden, ook in de
    andere layout zetten (alleen waar die nog het oorspronkelijke zee-vak heeft)."""
    L = [l for l in LAYOUTS.values() if l['name'] == dst_name][0]
    path = L['blockdata_filepath']
    b = open(path, 'rb').read()
    v = [[struct.unpack_from('<H', b, (y * M.w + x) * 2)[0] for x in range(M.w)] for y in range(M.h)]
    mine = ORIG.setdefault(dst_name, {})
    for k, c in mine.items():  # eerst terugzetten (idempotent)
        x, y = map(int, k.split(','))
        v[y][x] = c
    zv2 = json.load(open('tools/grounded/maptools/zee_vulling_2_orig.json')).get(M.layout, {})
    cells = dict(zv2)
    cells.update(ORIG.get(M.layout, {}))
    for k, c in cells.items():
        x, y = map(int, k.split(','))
        assert v[y][x] == c, '%s: (%d,%d) wijkt af (%x != %x)' % (dst_name, x, y, v[y][x], c)
        mine.setdefault(k, v[y][x])
        v[y][x] = M.v[y][x]
    open(path, 'wb').write(b''.join(struct.pack('<H', c) for r in v for c in r))


# =====================================================================================================
# ROUTE 107 (Dewford, lv ~30): afhaalbalie bij SUSHI 107 + verborgen item op het strand
M = Map('Route107')
P = 'Route107_EventScript_ZV3'
objs = [obj('OBJ_EVENT_GFX_MOVING_BOX', 27, 9, P + 'Takeaway')]
bgs = [hidden(M, 2, 12, 'ITEM_SOFT_SAND', 'R107')]
scr = talk(P + 'Takeaway', '''
	lock
	msgbox Route107_Text_ZV3Takeaway, MSGBOX_DEFAULT
	pokemart Route107_Pokemart_ZV3Takeaway
	msgbox Route107_Text_ZV3TakeawayBye, MSGBOX_DEFAULT
	release
	end

	.align 2
Route107_Pokemart_ZV3Takeaway:
	.2byte ITEM_ORAN_BERRY
	.2byte ITEM_SITRUS_BERRY
	.2byte ITEM_BERRY_JUICE
	.2byte ITEM_RAGE_CANDY_BAR
	.2byte ITEM_LAVA_COOKIE
	.2byte ITEM_OLD_GATEAU
	.2byte ITEM_CASTELIACONE
	.2byte ITEM_BIG_MALASADA
	pokemartlistend''')
scr += text('Route107_Text_ZV3Takeaway',
            "A crate with a hand-painted sign:\\n"
            "'SUSHI 107 - TAKEAWAY'.\\p"
            "The menu says 'RICE'.\\n"
            "The small print sells everything\\l"
            "except rice.")
scr += text('Route107_Text_ZV3TakeawayBye',
            "A note on the crate: 'NO REFUNDS.\\n"
            "NO FISH. NO QUESTIONS. -CHEF'")
finish(M, objs, bgs, scr, (0, 8), extra=[(27, 10)])

# =====================================================================================================
# ROUTE 122 (Mt. Pyre, lv ~36): Hex Maniac Vesper (bruidsmeisje van een spokenbruiloft) + verborgen item
M = Map('Route122')
P = 'Route122_EventScript_ZV3'
VESPER = trainer('TRAINER_HEX_MANIAC_VESPER', 'Route 122, bruidsmeisje van een spokenbruiloft',
                 hdr('VESPER', 'Hex Maniac', 'Hex Maniac', 'Female', 'Suspicious'),
                 team(36, 14, 'Brambleghast', 'Trevenant', 'Polteageist', ('Basculegion', 1)))
objs = [obj('OBJ_EVENT_GFX_HEX_MANIAC', 24, 31, P + 'Vesper', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=2)]
bgs = [hidden(M, 24, 30, 'ITEM_CLEANSE_TAG', 'R122')]
scr = single(P, 'Vesper', VESPER,
             "I'm the maid of honor at a wedding\\n"
             "tonight. Both of them are dead.\\p"
             "The groom has been dead for 200\\n"
             "years. The bride is 'only' 80.\\l"
             "People are talking.",
             "I'll still catch the bouquet.\\n"
             "It goes straight through my hands.",
             "The ceremony is on the shore at\\n"
             "midnight. Dress code: transparent.\\p"
             "The ferryman refuses to do the\\n"
             "catering. Again.")
finish(M, objs, bgs, scr, (20, 0))

# =====================================================================================================
# ROUTE 125 (Shoal Cave, lv ~39): drie verborgen items op de zandplaten
M = Map('Route125')
bgs = [hidden(M, 10, 22, 'ITEM_SNOWBALL', 'R125'), hidden(M, 45, 18, 'ITEM_BIG_PEARL', 'R125'),
       hidden(M, 26, 29, 'ITEM_ULTRA_BALL', 'R125')]
finish(M, [], bgs, '', (40, 10))

# =====================================================================================================
# ROUTE 126 (Mossdeep, lv ~40): Garbage Patch aanvullen (tv, toegangsbewijs, Seel 's nachts) + Sailor Marty
M = Map('Route126')
P = 'Route126_EventScript_ZV3'
MARTY = trainer('TRAINER_SAILOR_MARTY', 'Route 126, zijn schip is nu deel van de Garbage Patch',
                hdr('MARTY', 'Sailor', 'Sailor', 'Male', 'Male'),
                team(40, 12, 'Crabominable', 'Bibarel', ('Ursaring', 1)))
objs = [obj('OBJ_EVENT_GFX_SAILOR', 73, 38, P + 'Marty', move='MOVEMENT_TYPE_FACE_DOWN', trainer=True, sight=3),
        obj('OBJ_EVENT_GFX_MOVING_BOX', 76, 38, P + 'TV'),
        obj('OBJ_EVENT_GFX_SPECIES(SEEL)', 77, 38, P + 'Seel', move='MOVEMENT_TYPE_FACE_LEFT', flag='FLAG_TEMP_11')]
bgs = [sign(75, 38, P + 'Ticket'), hidden(M, 73, 41, 'ITEM_ELIXIR', 'R126')]
scr = talk(P + 'Night', '''
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, TRUE, %sNight_End
	setflag FLAG_TEMP_11
%sNight_End:
	return''' % (P, P))
scr += single(P, 'Marty', MARTY,
              "See that pile of junk? That was my\\n"
              "ship. Well, a third of it.\\p"
              "The other two thirds are a sock\\n"
              "and that TV. The ocean doesn't\\l"
              "do refunds.",
              "Sunk twice in one week.\\n"
              "That has to be a record.",
              "Every morning I salute my ship.\\n"
              "Every morning a WINGULL sits on it.\\l"
              "We have an understanding.")
scr += talk(P + 'TV', '''
	lock
	specialvar VAR_RESULT, IsNightTime
	goto_if_eq VAR_RESULT, TRUE, %sTV_Night
	msgbox Route126_Text_ZV3TV, MSGBOX_DEFAULT
	release
	end
%sTV_Night:
	msgbox Route126_Text_ZV3TVNight, MSGBOX_DEFAULT
	release
	end''' % (P, P))
scr += text('Route126_Text_ZV3TV',
            "A TV washed up in a crate. It has\\n"
            "no cable and no power.\\p"
            "It's showing the weather anyway.\\n"
            "Forecast for this sandbank:\\l"
            "'GARBAGE, WITH SPELLS OF GARBAGE.'")
scr += text('Route126_Text_ZV3TVNight',
            "At night the TV picks up\\n"
            "POKeNAV RADIO.\\p"
            "'...and that was the shipping\\n"
            "forecast. Route 126: moderate,\\l"
            "occasionally a sock.'")
scr += mon(P, 'Seel', 'SEEL',
           "SEEL: Arf.\\p"
           "A SEEL is listening to the radio\\n"
           "with its eyes closed.\\p"
           "It shushes you. This is the\\n"
           "shipping forecast. It's important.")
scr += signpost(P, 'Ticket', "A soggy ticket in the sand:\\p"
                "'GREAT PACIFIDLOG GARBAGE PATCH.\\n"
                "ADMIT ONE. NO RE-ENTRY.\\l"
                "NO EXIT EITHER, REALLY.'")
finish(M, objs, bgs, scr, (70, 50), extra=[(75, 37), (74, 38)])
hook('Route126', 'Route126_OnTransition', '\tcall Route126_EventScript_ZV3Night')

# =====================================================================================================
# ROUTE 127 (lv ~39): zeemijnenveld (Voltorb/Electrode, één antieke Hisui-Voltorb). Tijdelijke flags: na het
# verlaten van de kaart liggen de mijnen er weer ("de stroming brengt ze terug").
M = Map('Route127')
P = 'Route127_EventScript_ZV3'
MINES = [(61, 45, 'VOLTORB', 40), (65, 46, 'ELECTRODE', 42), (69, 45, 'VOLTORB', 40), (63, 48, 'ELECTRODE', 42),
         (67, 48, 'VOLTORB_HISUI', 40), (71, 47, 'ELECTRODE', 42)]
objs, scr = [], ''
for i, (x, y, sp, lv) in enumerate(MINES):
    gfx = 'OBJ_EVENT_GFX_SPECIES(%s)' % sp
    objs.append(obj(gfx, x, y, P + 'Mine%d' % i, move='MOVEMENT_TYPE_FACE_DOWN', flag='FLAG_TEMP_%X' % (0x11 + i)))
    scr += wild(P, 'Mine%d' % i, sp, lv, 'Route127_Text_ZV3MineAntique' if 'HISUI' in sp else 'Route127_Text_ZV3Mine')
bgs = [sign(59, 46, P + 'Warning')]
scr += text('Route127_Text_ZV3Mine',
            "Something round is bobbing in the\\n"
            "water. It's ticking.\\p"
            "It's a SEA MINE!\\n"
            "...No. It's a POKeMON pretending.\\l"
            "It's very committed to the bit.")
scr += text('Route127_Text_ZV3MineAntique',
            "This mine is made of wood and has\\n"
            "a fuse. An antique.\\p"
            "It looks at you like you are\\n"
            "the newfangled one.")
scr += signpost(P, 'Warning', "DANGER: MINEFIELD.\\n"
                "DO NOT TOUCH, PET OR CATCH.\\p"
                "Someone has scratched underneath:\\n"
                "'they respawn btw'")
finish(M, objs, bgs, scr, (64, 47), extra=[(60, 46)])

# =====================================================================================================
# ROUTE 129 (lv ~40): eilandje met Pokémon Ranger Coral (ondervertegenwoordigd: Grass/Bug/Electric)
M = Map('Route129')
keep_events(M)
islet(M, None, rect(23, 34, 28, 36))
P = 'Route129_EventScript_ZV3'
CORAL = trainer('TRAINER_RANGER_CORAL', 'Route 129, telt Wailord die er niet zijn',
                hdr('CORAL', 'Pkmn Ranger', 'Pokemon Ranger F', 'Female', 'Cool', ai=SMART),
                team(40, 15, ('Lurantis', 0, ['Solar Blade', 'Leaf Blade', 'X-Scissor', 'Sunny Day']),
                     ('Leavanny', 0, ['Leaf Blade', 'X-Scissor', 'Swords Dance', 'Poison Jab']),
                     ('Togedemaru', 0, ['Zing Zap', 'Iron Head', 'U-turn', 'Spiky Shield']),
                     ('Bellibolt', 1, ['Parabolic Charge', 'Muddy Water', 'Slack Off', 'Toxic'])))
objs = [obj('OBJ_EVENT_GFX_PICNICKER', 25, 35, P + 'Coral', move='MOVEMENT_TYPE_FACE_UP', trainer=True, sight=3)]
bgs = [hidden(M, 27, 36, 'ITEM_BIG_ROOT', 'R129')]
scr = single(P, 'Coral', CORAL,
             "Shh. I'm doing the yearly WAILORD\\n"
             "census.\\p"
             "So far: zero. Same as last year.\\n"
             "The tour boats say 'hundreds'.\\l"
             "Somebody is lying to tourists.",
             "Census update: one trainer,\\n"
             "very rude, zero WAILORD.",
             "If you see a WAILORD, don't tell\\n"
             "the tour guys. They'd only\\l"
             "sell tickets to it.")
finish(M, objs, bgs, scr, (40, 35))

# =====================================================================================================
# ROUTE 131 (lv ~40): bergingsduiker die Heart Scales ruilt (herhaalbaar) + Sailor Rusty
M = Map('Route131')
keep_events(M)
islet(M, None, rect(44, 23, 49, 25))
P = 'Route131_EventScript_ZV3'
RUSTY = trainer('TRAINER_SAILOR_RUSTY', 'Route 131, schipper van de bergingsduiker',
                hdr('RUSTY', 'Sailor', 'Sailor', 'Male', 'Male'),
                team(40, 12, 'Hitmonlee', 'Pawmot', 'Dachsbun', ('Kangaskhan', 1)))
objs = [obj('OBJ_EVENT_GFX_MAN_4', 45, 24, P + 'Diver', move='MOVEMENT_TYPE_FACE_RIGHT'),
        obj('OBJ_EVENT_GFX_SAILOR', 48, 23, P + 'Rusty', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=3)]
bgs = [hidden(M, 49, 25, 'ITEM_PP_UP', 'R131')]
D = P + 'Diver'
scr = talk(D, '''
	lock
	faceplayer
	msgbox Route131_Text_ZV3Diver, MSGBOX_DEFAULT
	checkitem ITEM_HEART_SCALE, 2
	goto_if_eq VAR_RESULT, FALSE, {D}_NoScales
	msgbox Route131_Text_ZV3DiverAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, {D}_No
	removeitem ITEM_HEART_SCALE, 2
	msgbox Route131_Text_ZV3DiverDeal, MSGBOX_DEFAULT
	random 10
	goto_if_lt VAR_RESULT, 4, {D}_Star
	goto_if_lt VAR_RESULT, 7, {D}_Pearl
	goto_if_lt VAR_RESULT, 9, {D}_Nugget
	giveitem ITEM_COMET_SHARD
	goto {D}_Given
{D}_Star:
	giveitem ITEM_STAR_PIECE
	goto {D}_Given
{D}_Pearl:
	giveitem ITEM_BIG_PEARL
	goto {D}_Given
{D}_Nugget:
	giveitem ITEM_NUGGET
{D}_Given:
	goto_if_eq VAR_RESULT, FALSE, {D}_Full
	msgbox Route131_Text_ZV3DiverDone, MSGBOX_DEFAULT
	release
	end
{D}_Full:
	additem ITEM_HEART_SCALE, 2
	msgbox Route131_Text_ZV3DiverFull, MSGBOX_DEFAULT
	release
	end
{D}_NoScales:
	msgbox Route131_Text_ZV3DiverNoScales, MSGBOX_DEFAULT
	release
	end
{D}_No:
	msgbox Route131_Text_ZV3DiverNo, MSGBOX_DEFAULT
	release
	end'''.replace('{D}', D))
scr += text('Route131_Text_ZV3Diver',
            "I'm a salvage diver. I dive for\\n"
            "treasure in the wrecks down there.\\p"
            "Mostly I find HEART SCALES.\\n"
            "Then I lose them. I'm a collector\\l"
            "with no pockets.")
scr += text('Route131_Text_ZV3DiverAsk',
            "Tell you what: give me two\\n"
            "HEART SCALES and I'll give you\\l"
            "something from my last dive.\\p"
            "I don't know what it is either.\\n"
            "Deal?")
scr += text('Route131_Text_ZV3DiverDeal',
            "Pleasure doing business.\\n"
            "Let me see what's in the bag...")
scr += text('Route131_Text_ZV3DiverDone',
            "Huh. Better than last time.\\n"
            "Last time it was a hand.")
scr += text('Route131_Text_ZV3DiverFull',
            "Your bag is full? Then keep your\\n"
            "scales. I'm a diver, not a monster.")
scr += text('Route131_Text_ZV3DiverNoScales',
            "You don't have two HEART SCALES?\\n"
            "Go look. The sea is full of them.\\l"
            "That's where mine went.")
scr += text('Route131_Text_ZV3DiverNo',
            "Your loss. Literally. I'll just\\n"
            "drop them back in the sea.")
scr += single(P, 'Rusty', RUSTY,
              "I'm the captain of our salvage\\n"
              "operation. The boat sank.\\p"
              "Now I captain this sandbank.\\n"
              "It also sinks. Twice a day.",
              "Abandon sandbank!\\n"
              "...Never mind. Tide's out.",
              "My diver gives away everything he\\n"
              "finds. I only keep the paperwork.\\l"
              "The paperwork is also wet.")
finish(M, objs, bgs, scr, (59, 24), extra=[(46, 24)])
sync_layout(M, 'Route131_SkyPillar_Layout')

# =====================================================================================================
# ROUTE 133 (lv ~39): meteoroloog met een Castform-waarnemingspost
M = Map('Route133')
keep_events(M)
islet(M, None, rect(47, 33, 52, 34))
P = 'Route133_EventScript_ZV3'
F_ICY = flag('FLAG_RECEIVED_ROUTE_133_ICY_ROCK', 'Route 133, meteoroloog (Icy Rock)')
objs = [obj('OBJ_EVENT_GFX_SCIENTIST_1', 48, 33, P + 'Meteorologist', move='MOVEMENT_TYPE_FACE_DOWN'),
        obj('OBJ_EVENT_GFX_SPECIES(CASTFORM)', 49, 33, P + 'Castform', move='MOVEMENT_TYPE_FACE_DOWN')]
bgs = [sign(51, 33, P + 'Post'), hidden(M, 52, 34, 'ITEM_UTILITY_UMBRELLA', 'R133')]
M2 = P + 'Meteorologist'
scr = talk(M2, '''
	lock
	faceplayer
	goto_if_set {F}, {M}_After
	msgbox Route133_Text_ZV3Meteo, MSGBOX_DEFAULT
	giveitem ITEM_ICY_ROCK
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag {F}
	release
	end
{M}_After:
	random 4
	goto_if_eq VAR_RESULT, 0, {M}_F0
	goto_if_eq VAR_RESULT, 1, {M}_F1
	goto_if_eq VAR_RESULT, 2, {M}_F2
	msgbox Route133_Text_ZV3Forecast3, MSGBOX_DEFAULT
	release
	end
{M}_F0:
	msgbox Route133_Text_ZV3Forecast0, MSGBOX_DEFAULT
	release
	end
{M}_F1:
	msgbox Route133_Text_ZV3Forecast1, MSGBOX_DEFAULT
	release
	end
{M}_F2:
	msgbox Route133_Text_ZV3Forecast2, MSGBOX_DEFAULT
	release
	end'''.replace('{M}', M2).replace('{F}', F_ICY))
scr += text('Route133_Text_ZV3Meteo',
            "Welcome to the CASTFORM WEATHER\\n"
            "OBSERVATION POST. Staff: me.\\l"
            "Equipment: CASTFORM.\\p"
            "When it's sunny, CASTFORM looks\\n"
            "sunny. When it rains, it looks\\l"
            "rainy. Science.\\p"
            "My grant ran out, so the ice\\n"
            "cooler goes. Take this rock.\\l"
            "It's the cold part.")
scr += text('Route133_Text_ZV3Forecast0',
            "Today's forecast: CASTFORM looks\\n"
            "normal. So: weather. Probably.")
scr += text('Route133_Text_ZV3Forecast1',
            "CASTFORM sneezed. That's either\\n"
            "rain or allergies. I'm writing\\l"
            "'rain'. Nobody checks.")
scr += text('Route133_Text_ZV3Forecast2',
            "Forecast: 90% chance of KYOGRE.\\n"
            "Just kidding. 40%.")
scr += text('Route133_Text_ZV3Forecast3',
            "I've predicted the weather here\\n"
            "for six years. I've been right\\l"
            "once. It was a guess.")
scr += mon(P, 'Castform', 'CASTFORM',
           "CASTFORM: Pyuu!\\p"
           "It's wearing a tiny label:\\n"
           "'PROPERTY OF THE WEATHER INSTITUTE.\\l"
           "IF FOUND, IT'S PROBABLY RAINING.'")
scr += signpost(P, 'Post', "CASTFORM WEATHER OBSERVATION POST\\p"
                "Today: see CASTFORM.\\n"
                "Tomorrow: see CASTFORM tomorrow.")
finish(M, objs, bgs, scr, (79, 20), extra=[(50, 33), (49, 34)])

# =====================================================================================================
# WHIRL ISLAND (lv ~45): nog twee verborgen items, zodat er vijf rond de lagune liggen
M = Map('WhirlIsland')
bgs = [hidden(M, 16, 30, 'ITEM_SEA_INCENSE', 'WHIRL'), hidden(M, 31, 21, 'ITEM_MAX_ELIXIR', 'WHIRL')]
finish(M, [], bgs, '', (19, 33))

# =====================================================================================================
# ONDERWATER
# 125: nog een verborgen item
M = Map('Underwater_Route125')
finish(M, [], [hidden(M, 9, 20, 'ITEM_WAVE_INCENSE', 'UW125')], '', (9, 19))

# 127: de trog krijgt zeewier + wilde Pokémon, en het anker van een schip dat nooit aankwam
M = Map('Underwater_Route127')
seaweed(M, [(58, 9, 2), (62, 33, 2), (71, 51, 2), (30, 55, 2), (73, 16, 1), (16, 55, 1), (32, 64, 1)])
P = 'Underwater_Route127_EventScript_ZV3'
scr = signpost(P, 'Anchor', "A huge anchor is stuck in the rock.\\n"
               "Engraved on it: 'S.S. TIDAL II'.\\p"
               "The S.S. TIDAL I is still sailing.\\n"
               "Nobody ever talks about the II.")
finish(M, [], [sign(34, 52, P + 'Anchor')], scr, (33, 52))
add_water_table('gUnderwater_Route127', 'MAP_UNDERWATER_ROUTE127', 'gUnderwater_Route129',
                [('QWILFISH', 38, 42), ('TATSUGIRI_STRETCHY', 38, 42), ('HUNTAIL', 40, 44), ('CURSOLA', 40, 44),
                 ('DHELMISE', 42, 46)])

# 128: een gezonken postzak
M = Map('Underwater_Route128')
P = 'Underwater_Route128_EventScript_ZV3'
scr = signpost(P, 'Mailbag', "A mailbag, sealed tight. One letter\\n"
               "has floated out:\\p"
               "'Dear Mom, the cruise is lovely.\\n"
               "The captain says KYOGRE is a myth.\\l"
               "More soon!'\\p"
               "There was no more soon.")
finish(M, [], [sign(35, 26, P + 'Mailbag')], scr, (35, 27))

# 129: piratenkist (X marks the spot) + de echte schat een paar tegels verderop
M = Map('Underwater_Route129')
P = 'Underwater_Route129_EventScript_ZV3'
scr = signpost(P, 'Chest', "A rotten chest with an X on the lid.\\n"
               "Inside, a note:\\p"
               "'THE REAL TREASURE WAS THE FRIENDS\\n"
               "WE DROWNED ALONG THE WAY.\\l"
               "-CAPT. REDBEARD'\\p"
               "P.S. 'Three steps east. Don't tell\\n"
               "the friends.'")
finish(M, [], [sign(16, 19, P + 'Chest'), hidden(M, 19, 18, 'ITEM_COMET_SHARD', 'UW129')], scr, (15, 18))

# =====================================================================================================
# Vergeten gewone lijnen: een tweede wilde plek voor Meowth, Buneary en Skwovet (slot van een soort met veel plekken)
for label, slot, old, new, lo, hi in [
        ('gRoute102', 5, 'SURSKIT', 'SKWOVET', 6, 6),
        ('gRoute113', 6, 'SALANDIT', 'MEOWTH', 16, 17),
        ('gRoute117', 11, 'COMFEY', 'BUNEARY', 15, 15)]:
    swap_land(label, slot, old, new, lo, hi)

assert not FAIL, FAIL
open(WILD, 'w').write(WTEXT[0])
json.loads(WTEXT[0])
write_flags()
write_trainers()
json.dump(ORIG, open(ORIG_PATH, 'w'), indent=0, sort_keys=True)
print('ok: %d trainers (%d-%d), %d flags' % (len(TRAINERS), FIRST_ID, FIRST_ID + len(TRAINERS) - 1, len(FLAGS)))
