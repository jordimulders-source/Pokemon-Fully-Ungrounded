#!/usr/bin/env python3
"""Statische controle van de hele game (zonder emulator).

Gebruik (vanuit de root van de repo):
    python3 tools/grounded/audit.py              # overzicht per categorie
    python3 tools/grounded/audit.py -v           # ook alle meldingen
    python3 tools/grounded/audit.py --md AUDIT.md  # open lijst als Markdown
    python3 tools/grounded/audit.py --only warps,items

Categorieën: warps, kaarten, scripts, flags, trainers, wild, items.
Ernst:  FOUT  = vrijwel zeker een bug
        MELD  = verdacht / ontwerpkeuze, even naar kijken
        VANILLA = zelfde bevinding op een kaart/tekst die sinds vanilla niet veranderd is (niet in AUDIT.md)
Trainerdata komt uit het gegenereerde src/data/trainers.h (eerst `make`); zonder dat bestand wordt
trainers.party zelf gelezen.

Een bevinding bewust negeren: zet de sleutel (laatste kolom in -v / AUDIT.md) in IGNORE hieronder.
"""
import argparse, collections, glob, importlib.util, json, os, re, statistics, struct, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(ROOT)
BASE = 'd79b0c5f31^'   # pokeemerald-expansion vlak vóór de eerste Grounded-commit (vanilla-referentie)

# Bewuste uitzonderingen (sleutel -> reden). Sleutels staan achteraan elke regel in -v / AUDIT.md.
IGNORE = {
    # v0.9.295 (1.0-audit): bewust. Levels: routedelen/kamers die je later bereikt of grap-trainers; Steven, Mimi en de
    # taakstraf-gevechten hebben een eigen transitie (battle_setup.c); Artisan Cave is (zoals vanilla) een Smeargle-grot.
    'lvlfit:TRAINER_ZINNIA_DELTA': 'bewust (1.0-audit)',
    'lvlfit:TRAINER_ANDREW': 'bewust (1.0-audit)',
    'lvlfit:TRAINER_RHETT': 'bewust (1.0-audit)',
    'lvlfit:TRAINER_PETE': 'bewust (1.0-audit)',
    'lvlfit:TRAINER_ISABELLE': 'bewust (1.0-audit)',
    'lvlfit:TRAINER_NED': 'bewust (1.0-audit)',
    'lvlfit:TRAINER_EDWARD': 'bewust (1.0-audit)',
    'lvlfit:TRAINER_JACLYN': 'bewust (1.0-audit)',
    'lvlfit:TRAINER_NOLAN': 'bewust (1.0-audit)',
    'lvlfit:TRAINER_AARON': 'bewust (1.0-audit)',
    'lvlfit:TRAINER_COLTON': 'bewust (1.0-audit)',
    'mugshot:TRAINER_STEVEN': 'bewust (1.0-audit)',
    'mugshot:TRAINER_MIMI': 'bewust (1.0-audit)',
    'mugshot:TRAINER_ARCHIE_SERVICE_1': 'bewust (1.0-audit)',
    'mugshot:TRAINER_ARCHIE_SERVICE_2': 'bewust (1.0-audit)',
    'mugshot:TRAINER_ARCHIE_SERVICE_3': 'bewust (1.0-audit)',
    'mugshot:TRAINER_ARCHIE_SERVICE_4': 'bewust (1.0-audit)',
    'mugshot:TRAINER_MAXIE_SERVICE_1': 'bewust (1.0-audit)',
    'mugshot:TRAINER_MAXIE_SERVICE_2': 'bewust (1.0-audit)',
    'mugshot:TRAINER_MAXIE_SERVICE_3': 'bewust (1.0-audit)',
    'mugshot:TRAINER_MAXIE_SERVICE_4': 'bewust (1.0-audit)',
    'wild:gArtisanCave_B1F:land_mons:dup': 'bewust (1.0-audit)',
    'wild:gArtisanCave_1F:land_mons:dup': 'bewust (1.0-audit)',

    'reachobj:YoshisIsland_Jungle:2': 'bereikbaar via de Poochy-rit (script verplaatst de speler)',
    'reachobj:YoshisIsland_Jungle:4': 'bereikbaar via de Poochy-rit (script verplaatst de speler)',
}

# Handmatige controles (renders/emulator) die niet automatisch te herhalen zijn; komen onderaan AUDIT.md.
MANUAL = [
    'Renders van de 91 kaarten die sinds 6 okt zijn toegevoegd bekeken (contactvellen): geen afgekapte objecten, '
    'zwarte leegtes of open randen gevonden. De witte hoek rechtsboven in de Battle Casino komt uit de vanilla '
    'Game Corner-layout.',
    'Emulator (python3.11, debugscript-warp + sWarpDestination): alle warp-bestemmingen van Spacetime Cave (hub + '
    'portalen), Yoshi\'s Island (9 kaarten), Area Zero (6), Hall of Origin (3), Crown Tundra, Battle Casino en '
    'Abandoned Ship geladen: 91 warps zonder crash of zwart beeld, de speler staat op de juiste kaart en plek '
    '(afwijkingen alleen door aankomstscènes die de speler laten lopen). Wilde gevechten gestart op Crown Tundra, '
    'Yoshi\'s Island (Hills, Jungle, Flowers, Cave) en Area Zero (Depths, Crystal, Past, Future): alle goed. '
    'Abandoned Ship \'s nachts niet getest (de emulator volgt de klok van de host).',
    'Coord-triggers zonder releaseall: in deze engine geeft `end` de besturing gewoon terug (ScriptContext_RunScript '
    'ontgrendelt bij het einde); alleen lock/lockall zonder release laat je vastzitten. De check meldt daarom alleen dat.',
]

CATS = ('warps', 'kaarten', 'scripts', 'flags', 'trainers', 'wild', 'items')
findings = []          # (cat, ernst, sleutel, tekst)
stats = collections.defaultdict(collections.Counter)


def add(cat, sev, key, msg):
    if key in IGNORE:
        stats[cat]['genegeerd'] += 1
        return
    findings.append((cat, sev, key, msg))


def read(p):
    try:
        return open(p, encoding='utf-8', errors='replace').read()
    except OSError:
        return ''


def git(*a):
    try:
        return subprocess.run(('git',) + a, capture_output=True, text=True, errors='replace').stdout
    except OSError:
        return ''


_CHANGED = None


def changed_since_base(path):
    """True als het bestand sinds vanilla veranderd (of nieuw) is."""
    global _CHANGED
    if _CHANGED is None:
        out = git('diff', '--name-only', BASE, '--', 'data', 'src', 'include')
        _CHANGED = set(out.split()) if out else None
        untracked = git('ls-files', '--others', '--exclude-standard', 'data', 'src', 'include')
        if _CHANGED is not None:
            _CHANGED |= set(untracked.split())
    if _CHANGED is None:
        return True
    return path in _CHANGED


_BASECACHE = {}


def base_file(path):
    if path not in _BASECACHE:
        _BASECACHE[path] = git('show', '%s:%s' % (BASE, path))
    return _BASECACHE[path]


# ------------------------------------------------------------------ #defines uitrekenen
def load_defines(text):
    d = {}
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    for l in text.split('\n'):
        m = re.match(r'\s*#define\s+(\w+)(\([^)]*\))?\s+(.*)', l)
        if m and not m.group(2):
            d[m.group(1)] = re.sub(r'//.*', '', m.group(3)).strip()
    return d


def evaluator(defs):
    cache = {}

    def ev(name, depth=0):
        if name in cache:
            return cache[name]
        if name not in defs or depth > 40:
            return None
        e = defs[name]
        e = re.sub(r'FLAG_GROUNDED\(([^()]*)\)', r'(GROUNDED_FLAGS_START + (\1))', e)
        e = re.sub(r'TRAINER_FLAGS_START\s*\+\s*', 'TRAINER_FLAGS_START + ', e)
        ok = True

        def rep(m):
            nonlocal ok
            t = m.group(0)
            if re.fullmatch(r'0[xX][0-9a-fA-F]+|\d+', t):
                return t
            v = ev(t, depth + 1)
            if v is None:
                ok = False
                return '0'
            return str(v)
        e2 = re.sub(r'\b[A-Za-z_]\w*\b|\b0[xX][0-9a-fA-F]+\b', rep, e)
        e2 = e2.replace('/', '//').replace('u)', ')')
        v = None
        if ok:
            try:
                v = int(eval(e2, {'__builtins__': {}}))
            except Exception:
                v = None
        cache[name] = v
        return v
    return ev


_EXTRA_DEFS = load_defines(read('include/constants/opponents.h') + '\n' + read('include/constants/global.h'))
FLAG_DEFS = load_defines(read('include/constants/flags.h'))
FLAG = evaluator(dict(_EXTRA_DEFS, **FLAG_DEFS))
VAR_DEFS = load_defines(read('include/constants/vars.h'))
VAR = evaluator(dict(_EXTRA_DEFS, **VAR_DEFS))


def flagval(s):
    s = str(s).strip()
    if s in ('0', '', 'FALSE'):
        return None
    m = re.fullmatch(r'TRAINER_FLAGS_START\s*\+\s*(\w+)', s)
    if m:
        return ('T', m.group(1))
    if re.fullmatch(r'0[xX][0-9a-fA-F]+|\d+', s):
        return int(s, 0)
    v = FLAG(s)
    return v if v is not None else ('?', s)


# ------------------------------------------------------------------ kaarten en layouts
MAPGROUPS = json.load(open('data/maps/map_groups.json'))
MAPS = {}          # naam -> dict (map.json)
MAP_GROUP = {}     # naam -> groep
ID2NAME = {}
for g in MAPGROUPS['group_order']:
    for n in MAPGROUPS[g]:
        MAP_GROUP[n] = g
        p = 'data/maps/%s/map.json' % n
        if os.path.exists(p):
            MAPS[n] = json.load(open(p))
            ID2NAME[MAPS[n]['id']] = n
LAYOUTS = {l['id']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'id' in l}

BEH = {}
for _l in open('include/constants/metatile_behaviors.h'):
    _m = re.match(r'\s*(MB_\w+)', _l)
    if _m and _m.group(1) not in BEH:
        BEH[_m.group(1)] = len(BEH)
MB = {v: k for k, v in BEH.items()}
_HDR = read('src/data/tilesets/headers.h')
_MT = read('src/data/tilesets/metatiles.h')
_ATTR = {}


def tileset_attrs(sym):
    if sym not in _ATTR:
        try:
            body = re.search(r'const struct Tileset ' + sym + r' =(?:\s*//[^\n]*)?\s*\{(.*?)\};', _HDR, re.S).group(1)
            a = re.search(r'\.metatileAttributes = (\w+)', body).group(1)
            p = re.search(a + r'\[\] = INCBIN_U16\("([^"]+)"', _MT).group(1)
            b = open(p, 'rb').read()
            _ATTR[sym] = [struct.unpack_from('<H', b, i * 2)[0] for i in range(len(b) // 2)]
        except Exception:
            _ATTR[sym] = None
    return _ATTR[sym]


class Grid:
    def __init__(self, layout_id):
        L = LAYOUTS[layout_id]
        self.w, self.h = L['width'], L['height']
        self.path = L.get('blockdata_filepath')
        raw = open(self.path, 'rb').read()
        n = min(len(raw) // 2, self.w * self.h)
        self.v = list(struct.unpack('<%dH' % n, raw[:n * 2])) + [0] * (self.w * self.h - n)
        self.sizeok = len(raw) == self.w * self.h * 2
        self.P, self.S = tileset_attrs(L['primary_tileset']), tileset_attrs(L['secondary_tileset'])

    def inside(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def c(self, x, y):
        return self.v[y * self.w + x]

    def beh(self, x, y):
        mt = self.c(x, y) & 0x3FF
        t = self.P if mt < 0x200 else self.S
        i = mt if mt < 0x200 else mt - 0x200
        if not t or i >= len(t):
            return None
        return MB.get(t[i] & 0xFF, hex(t[i] & 0xFF))

    def elev(self, x, y):
        return self.c(x, y) >> 12

    def blocked(self, x, y):
        return bool(self.c(x, y) & 0xC00)


_GRIDS = {}


def grid(name):
    lid = MAPS[name]['layout']
    if lid not in _GRIDS:
        try:
            _GRIDS[lid] = Grid(lid)
        except Exception:
            _GRIDS[lid] = None
    return _GRIDS[lid]


METATILE_IDS = {k: v for k, v in ((k, evaluator(load_defines(read('include/constants/metatile_labels.h')))(k))
                                  for k in load_defines(read('include/constants/metatile_labels.h'))) if v is not None}


def map_script_text(name):
    return read('data/maps/%s/scripts.inc' % name)


def tile_variants(name, x, y):
    """(gedrag, elevation) van een tegel in alle toestanden: map.bin, setmetatile in de kaartscripts en
    andere layouts via setmaplayoutindex."""
    g = grid(name)
    out = []
    if g and g.inside(x, y):
        out.append((g.beh(x, y), g.elev(x, y)))
    st = map_script_text(name)
    for m in re.finditer(r'setmetatile\s+(\d+)\s*,\s*(\d+)\s*,\s*(\w+)', st):
        if int(m.group(1)) == x and int(m.group(2)) == y and g:
            mt = METATILE_IDS.get(m.group(3))
            if mt is None and re.fullmatch(r'0x[0-9a-fA-F]+|\d+', m.group(3)):
                mt = int(m.group(3), 0)
            if mt is not None:
                t, i = (g.P, mt) if mt < 0x200 else (g.S, mt - 0x200)
                if t and i < len(t):
                    out.append((MB.get(t[i] & 0xFF), g.elev(x, y)))
    for lid in set(re.findall(r'setmaplayoutindex\s+(\w+)', st)):
        if lid in LAYOUTS:
            if lid not in _GRIDS:
                try:
                    _GRIDS[lid] = Grid(lid)
                except Exception:
                    _GRIDS[lid] = None
            g2 = _GRIDS[lid]
            if g2 and g2.inside(x, y):
                out.append((g2.beh(x, y), g2.elev(x, y)))
    return out


def part_vanilla(name, key):
    """True als map.json[key] én de blockdata van deze kaart gelijk zijn aan vanilla."""
    t = base_file('data/maps/%s/map.json' % name)
    if not t:
        return False
    try:
        b = json.loads(t)
    except ValueError:
        return False
    if b.get(key) != MAPS[name].get(key) or b.get('layout') != MAPS[name].get('layout'):
        return False
    L = LAYOUTS.get(MAPS[name]['layout'], {})
    return not changed_since_base(L.get('blockdata_filepath', ''))


def map_changed(name):
    """Kaart (map.json, scripts.inc of layout) veranderd sinds vanilla?"""
    paths = ['data/maps/%s/map.json' % name, 'data/maps/%s/scripts.inc' % name]
    L = LAYOUTS.get(MAPS[name]['layout'], {})
    if L.get('blockdata_filepath'):
        paths.append(L['blockdata_filepath'])
    return any(changed_since_base(p) for p in paths)


def sev_for(name, sev='FOUT'):
    return sev if map_changed(name) else 'VANILLA'


# ------------------------------------------------------------------ scripts inlezen
SCRIPT_FILES = sorted(set(glob.glob('data/maps/*/scripts.inc') + glob.glob('data/scripts/**/*.inc', recursive=True)
                          + glob.glob('data/text/*.inc') + glob.glob('data/*.s') + glob.glob('data/**/*.inc', recursive=True)))
LABELS = {}        # label -> (bestand, regelindex)
FILELINES = {}
for f in SCRIPT_FILES:
    ls = read(f).split('\n')
    FILELINES[f] = ls
    for i, l in enumerate(ls):
        m = re.match(r'^([A-Za-z_]\w*)::?\s*(@.*)?$', l)
        if m:
            LABELS.setdefault(m.group(1), (f, i))
        m = re.match(r'^\s*\.set\s+(\w+)\s*,', l)
        if m:
            LABELS.setdefault(m.group(1), (f, i))

_CSYMS = None


def c_symbols():
    global _CSYMS
    if _CSYMS is None:
        s = set()
        for f in glob.glob('src/**/*.c', recursive=True) + glob.glob('src/**/*.h', recursive=True) + glob.glob('include/**/*.h', recursive=True):
            s.update(re.findall(r'\b[A-Za-z_]\w*\b', read(f)))
        _CSYMS = s
    return _CSYMS


def label_exists(lb):
    return lb in LABELS or lb in c_symbols()


def body(label):
    """Regels van een label tot het volgende label."""
    if label not in LABELS:
        return []
    f, i = LABELS[label]
    out = []
    for l in FILELINES[f][i + 1:]:
        if re.match(r'^[A-Za-z_]\w*::?\s*(@.*)?$', l):
            break
        out.append(l.split('@')[0].strip() if not l.strip().startswith('.string') else l.strip())
    return out


def label_vanilla(label):
    """De regels van dit label zijn gelijk aan vanilla."""
    if label not in LABELS:
        return False
    f, i = LABELS[label]
    if not changed_since_base(f):
        return True
    bl = base_file(f).split('\n')
    try:
        j = next(k for k, l in enumerate(bl) if re.match(r'^%s::?\s*(@.*)?$' % re.escape(label), l))
    except StopIteration:
        return False
    out = []
    for l in bl[j + 1:]:
        if re.match(r'^[A-Za-z_]\w*::?\s*(@.*)?$', l):
            break
        out.append(l.split('@')[0].strip() if not l.strip().startswith('.string') else l.strip())
    return out == body(label)


def cmd_args(line):
    m = re.match(r'^(\w+)\s*(.*)$', line)
    if not m:
        return None, []
    return m.group(1), [a.strip() for a in m.group(2).split(',')] if m.group(2) else []


LABELISH = re.compile(r'\b([A-Z][A-Za-z0-9]*_[A-Za-z0-9_]*[a-z][A-Za-z0-9_]*)\b')


def reachable(label, seen=None):
    seen = set() if seen is None else seen
    stack = [label]
    while stack:
        lb = stack.pop()
        if lb in seen or lb not in LABELS:
            continue
        seen.add(lb)
        for l in body(lb):
            c, args = cmd_args(l)
            if c and (c in ('goto', 'call') or c.startswith('goto_if') or c.startswith('call_if') or c.startswith('trainerbattle')
                      or c in ('switch', 'case', 'goto_if_unset', 'call_if_unset')):
                for a in args:
                    if re.fullmatch(r'[A-Z][A-Za-z0-9]*_\w+', a) and a in LABELS:
                        stack.append(a)
    return seen


# ------------------------------------------------------------------ 1. warps
WARP_BEH_FUNCS = ('IsWarpDoor', 'IsLadder', 'IsEscalator', 'IsNonAnimDoor', 'IsLavaridgeB1FWarp', 'IsLavaridge1FWarp',
                  'IsAquaHideoutWarp', 'IsMtPyreHole', 'IsMossdeepGymWarp', 'IsUnionRoomWarp', 'IsEastArrowWarp',
                  'IsWestArrowWarp', 'IsNorthArrowWarp', 'IsSouthArrowWarp', 'IsDeepSouthWarp', 'IsBattlePyramidWarp',
                  'IsDirectionalStairWarp', 'IsDirectionalUpRightStairWarp', 'IsDirectionalUpLeftStairWarp',
                  'IsDirectionalDownRightStairWarp', 'IsDirectionalDownLeftStairWarp', 'IsDoor', 'IsCrackedFloorHole')


def warp_behaviors():
    src = read('src/metatile_behavior.c')
    out = set()
    for fn in WARP_BEH_FUNCS:
        m = re.search(r'MetatileBehavior_' + fn + r'\([^)]*\)\s*\{(.*?)\n\}', src, re.S)
        if m:
            out |= set(re.findall(r'MB_\w+', m.group(1)))
    return out


WARP_CMDS = ('warp', 'warpsilent', 'warpdoor', 'warphole', 'warpteleport', 'warpspinenter', 'warpwhitefade',
             'warpmossdeepgym', 'warpsootopolislegend', 'setwarp', 'setdynamicwarp', 'setdivewarp', 'setescapewarp',
             'setholewarp', 'warpfollowmon')


HOLES = {'MB_MT_PYRE_HOLE', 'MB_CRACKED_FLOOR_HOLE', 'MB_CRACKED_FLOOR'}


def has_route(n, dn, WB):
    """Kan de speler van kaart n terug naar kaart dn? Via een warp-tegel (ook na setmetatile), een
    script op deze kaart dat naar dn warpt (of een gat/duik instelt), of een duik-/bovenkomverbinding."""
    d = MAPS[n]
    did = MAPS[dn]['id']
    for w in d.get('warp_events') or []:
        if w['dest_map'] == did and any(b in WB for b, _ in tile_variants(n, w['x'], w['y'])):
            return True
    if re.search(r'\b%s\b' % did, map_script_text(n)):
        return True
    for c in d.get('connections') or []:
        if c.get('map') == did:
            return True
    return False


def base_tile(name, x, y):
    L = LAYOUTS[MAPS[name]['layout']]
    p = L['blockdata_filepath']
    key = 'bin:' + p
    if key not in _BASECACHE:
        try:
            _BASECACHE[key] = subprocess.run(('git', 'show', '%s:%s' % (BASE, p)), capture_output=True).stdout
        except OSError:
            _BASECACHE[key] = b''
    raw = _BASECACHE[key]
    o = (y * L['width'] + x) * 2
    return struct.unpack_from('<H', raw, o)[0] if o + 2 <= len(raw) else None


def warp_vanilla(name, i):
    """Deze warp (index en inhoud) en zijn tegel zijn gelijk aan vanilla."""
    t = base_file('data/maps/%s/map.json' % name)
    if not t:
        return False
    try:
        bw = json.loads(t).get('warp_events') or []
    except ValueError:
        return False
    w = MAPS[name]['warp_events'][i]
    g = grid(name)
    return (i < len(bw) and bw[i] == w and g is not None and g.inside(w['x'], w['y'])
            and base_tile(name, w['x'], w['y']) == g.c(w['x'], w['y']))


def event_vanilla(name, kind, e):
    """Dit event (zelfde inhoud, op welke index ook) en zijn tegel bestonden al zo in vanilla."""
    t = base_file('data/maps/%s/map.json' % name)
    if not t:
        return False
    try:
        be = json.loads(t).get(kind) or []
    except ValueError:
        return False
    if e not in be:
        return False
    g = grid(name)
    if g is None or not g.inside(e['x'], e['y']):
        return True
    return base_tile(name, e['x'], e['y']) == g.c(e['x'], e['y'])


def same_positions(name):
    """Objecten staan op dezelfde plekken (en met dezelfde flags) als in vanilla."""
    t = base_file('data/maps/%s/map.json' % name)
    if not t:
        return False
    key = lambda o: (o['x'], o['y'], str(o.get('flag', '0')) in ('0', ''))
    try:
        return sorted(map(key, json.loads(t).get('object_events') or [])) == sorted(map(key, MAPS[name].get('object_events') or []))
    except ValueError:
        return False


def neighbour_elevs(g, x, y):
    out = set()
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if g.inside(x + dx, y + dy) and not g.blocked(x + dx, y + dy):
            out.add(g.elev(x + dx, y + dy))
    return out


def wsev(n, sev='FOUT'):
    return 'VANILLA' if part_vanilla(n, 'warp_events') else sev


def check_warps():
    WB = warp_behaviors()
    arrivals = collections.defaultdict(set)     # kaartnaam -> set(warp-index) waar iets naartoe warpt
    targets = collections.defaultdict(set)      # kaart -> kaarten waar zijn warps naartoe gaan
    for n, d in MAPS.items():
        for wp in d.get('warp_events') or []:
            dm, di = wp['dest_map'], str(wp['dest_warp_id'])
            if dm in ID2NAME and re.fullmatch(r'\d+', di):
                arrivals[ID2NAME[dm]].add(int(di))
            if dm in ID2NAME:
                targets[n].add(ID2NAME[dm])
    script_targets = collections.defaultdict(set)   # door scripts/C bereikte kaarten
    for f, ls in FILELINES.items():
        for l in ls:
            c, args = cmd_args(l.strip())
            if c in WARP_CMDS and args and args[0] in ID2NAME:
                script_targets[ID2NAME[args[0]]].add(f)
                if len(args) == 2 and re.fullmatch(r'\d+', args[1]):
                    arrivals[ID2NAME[args[0]]].add(int(args[1]))
    for f in glob.glob('src/**/*.c', recursive=True):
        t = read(f)
        for m in re.finditer(r'MAP_GROUP\((\w+)\),\s*MAP_NUM\(\1\)\s*,\s*(-?\w+)', t):
            if m.group(1) in ID2NAME:
                script_targets[ID2NAME[m.group(1)]].add(f)
                if re.fullmatch(r'\d+', m.group(2)):
                    arrivals[ID2NAME[m.group(1)]].add(int(m.group(2)))
    n_warps = 0
    for n, d in sorted(MAPS.items()):
        g = grid(n)
        warps = d.get('warp_events') or []
        for i, wp in enumerate(warps):
            n_warps += 1
            key = 'warp:%s:%d' % (n, i)
            dm, di = wp['dest_map'], str(wp['dest_warp_id'])
            x, y = wp['x'], wp['y']
            where = '%s warp %d (%d,%d)' % (n, i, x, y)
            if dm == 'MAP_DYNAMIC' or di in ('WARP_ID_DYNAMIC', '0x7F', '127', 'WARP_ID_SECRET_BASE', '0x7E', '126'):
                stats['warps']['dynamisch'] += 1
            elif dm not in ID2NAME:
                add('warps', wsev(n), key + ':map', '%s: doelkaart %s bestaat niet' % (where, dm))
            elif not re.fullmatch(r'\d+', di):
                add('warps', wsev(n), key + ':id', '%s: warp-index %r is geen getal' % (where, di))
            else:
                dn = ID2NAME[dm]
                dw = MAPS[dn].get('warp_events') or []
                if int(di) >= len(dw):
                    add('warps', wsev(n), key + ':idx', '%s -> %s: warp %s bestaat niet (kaart heeft %d warps)'
                        % (where, dn, di, len(dw)))
                else:
                    dg = grid(dn)
                    t = dw[int(di)]
                    if dg and not dg.inside(t['x'], t['y']):
                        add('warps', wsev(dn), key + ':destout', '%s -> %s warp %s ligt buiten de kaart' % (where, dn, di))
            if not g:
                continue
            if not g.inside(x, y):
                add('warps', wsev(n), key + ':out', '%s ligt buiten de kaart (%dx%d)' % (where, g.w, g.h))
                continue
            van = 'VANILLA' if warp_vanilla(n, i) else None
            variants = tile_variants(n, x, y)
            trig = [(b, e) for b, e in variants if b in WB]
            b = g.beh(x, y)
            we = int(wp.get('elevation', 0))
            # elevation telt alleen op tegels die zelf warpen (een aankomstpunt mag elke hoogte hebben)
            if trig and we != 0:
                es = {e for _, e in trig}
                if not (es & {we, 0, 15}):
                    add('warps', van or 'FOUT', key + ':elev', '%s: elevation %d, tegel heeft %s (warp werkt niet; zet 0 of %s)'
                        % (where, we, '/'.join(map(str, sorted(es))), '/'.join(map(str, sorted(es)))))
                elif es <= {0, 15} and we not in neighbour_elevs(g, x, y):
                    add('warps', van or 'MELD', key + ':elev0', '%s: elevation %d op een tegel met elevation %s (werkt alleen als je met die hoogte aankomt)'
                        % (where, we, '/'.join(map(str, sorted(es)))))
            if not trig:
                if i in arrivals[n]:
                    stats['warps']['alleen aankomstpunt'] += 1
                    # aankomstpunt zonder warpgedrag, terwijl het een tweerichtingspaar lijkt: kom je hier nog terug?
                    dn = ID2NAME.get(dm)
                    if dn and dn != n:
                        cps = [w2 for w2 in MAPS[dn].get('warp_events') or []
                               if w2['dest_map'] == d['id'] and str(w2['dest_warp_id']) == str(i)]
                        cpb = {bb for w2 in cps for bb, _ in tile_variants(dn, w2['x'], w2['y'])}
                        if cps and not cpb & HOLES and not has_route(n, dn, WB):
                            v2 = van if all(warp_vanilla(dn, j) for j, w2 in enumerate(MAPS[dn]['warp_events']) if w2 in cps) else None
                            add('warps', v2 or 'FOUT', key + ':nobeh',
                                '%s: aankomstpunt zonder warpgedrag (%s); %s warpt hierheen, maar van hier is er geen warp-tegel, '
                                'script of duik-verbinding terug naar %s (deur-/grottegel vergeten?)' % (where, b, dn, dn))
                else:
                    pad = g.blocked(x, y) or any(abs(w2['x'] - x) + abs(w2['y'] - y) == 1 and w2['dest_map'] == dm
                                                 for w2 in warps)
                    add('warps', van or ('INFO' if pad else 'MELD'), key + ':dead', '%s: tegel zonder warpgedrag (%s) en niets warpt hierheen (dode warp)' % (where, b))
        # heen-en-terug
        for dn in sorted(targets[n]):
            if dn == n:
                continue
            if n not in targets[dn] and n not in [ID2NAME.get(w['dest_map']) for w in MAPS[dn].get('warp_events') or []]:
                if script_targets.get(n) and any(dn in f for f in script_targets[n]):
                    continue
                add('warps', wsev(n, 'MELD'), 'warpback:%s:%s' % (n, dn),
                    '%s warpt naar %s, maar daar wijst geen warp terug (eenrichting/gat/script?)' % (n, dn))
    stats['warps']['warps'] = n_warps


# ------------------------------------------------------------------ 2. kaarten
GIANT = set(re.findall(r'OBJ_EVENT_GFX_\w+', re.search(r'GiantObjectViewMargin\([^)]*\)\s*\{(.*?)\n\}',
                                                         read('src/event_object_movement.c'), re.S).group(1))) \
    if re.search(r'GiantObjectViewMargin\([^)]*\)\s*\{', read('src/event_object_movement.c')) else set()
WALL_OK_GFX = re.compile(r'ITEM_BALL|BERRY_TREE|CUTTABLE_TREE|BREAKABLE_ROCK|BOULDER|STATUE|DOLL|CUSHION|BIG_|INVISIBLE|'
                         r'TRUCK|SS_TIDAL|BOAT|SUBMARINE|_SHADOW|MOVING_BOX|LIGHT|ROPE|DEOXYS_TRIANGLE|BIRTH_ISLAND|'
                         r'MYSTERY_EVENT|CABLE_CAR|CHALLENGE|ANTENNA|FOSSIL|REGI|SPECIES|MEGA_STONE|SIGN|VAR_|ULTRA_EYE')


WATER_B = {'MB_OCEAN_WATER', 'MB_DEEP_WATER', 'MB_POND_WATER', 'MB_SEAWEED', 'MB_NO_SURFACING', 'MB_SEAWEED_NO_SURFACING',
           'MB_WESTWARD_CURRENT', 'MB_EASTWARD_CURRENT', 'MB_NORTHWARD_CURRENT', 'MB_SOUTHWARD_CURRENT', 'MB_WATERFALL',
           'MB_INTERIOR_DEEP_WATER', 'MB_SOOTOPOLIS_DEEP_WATER', 'MB_WATER_DOOR', 'MB_WATER_SOUTH_ARROW_WARP'}
JUMP = {'MB_JUMP_EAST': (1, 0), 'MB_JUMP_WEST': (-1, 0), 'MB_JUMP_NORTH': (0, -1), 'MB_JUMP_SOUTH': (0, 1)}
# objecten die geen blijvende muur zijn: items (oppakken), veldobstakels (HM's), onzichtbare/dynamische
NONWALL_GFX = re.compile(r'ITEM_BALL|CUTTABLE_TREE|BREAKABLE_ROCK|BOULDER|INVISIBLE|BERRY_TREE|VAR_\d|MOVING_BOX')


class Reach:
    """Bereikbaarheid op één kaart: lopen + surfen, richels in één richting, objecten zonder flag als muur.
    Optimistisch: tegels die een kaartscript met setmetatile vrijmaakt tellen als vrij."""

    def __init__(self, name):
        self.n = name
        self.d = MAPS[name]
        self.g = g = grid(name)
        self.free_by_script = set()
        for m in re.finditer(r'setmetatile\s+(\d+)\s*,\s*(\d+)\s*,\s*\w+\s*,\s*(FALSE|0)\b', map_script_text(name)):
            self.free_by_script.add((int(m.group(1)), int(m.group(2))))
        self.walls = set()
        st = map_script_text(name)
        moved = set(re.findall(r'(?:setobjectxyperm|setobjectxy|removeobject|applymovement)\s+(LOCALID_\w+)', st))
        for o in self.d.get('object_events') or []:
            if o.get('local_id') in moved:
                continue        # gaat via een script opzij (bewakers, verdwijnende NPC's)
            if str(o.get('flag', '0')) in ('0', '') and not NONWALL_GFX.search(o['graphics_id']) \
                    and o['graphics_id'] not in GIANT and 'WANDER' not in o['movement_type'] \
                    and 'WALK_' not in o['movement_type']:
                self.walls.add((o['x'], o['y']))

    def passable(self, x, y):
        g = self.g
        return g.inside(x, y) and (not g.blocked(x, y) or (x, y) in self.free_by_script)

    def water(self, x, y):
        return self.g.beh(x, y) in WATER_B

    def run(self, starts):
        g = self.g
        seen = set()
        q = collections.deque()
        for s in starts:
            if g.inside(*s) and s not in seen:
                seen.add(s)
                q.append(s)
        while q:
            x, y = q.popleft()
            e0 = g.elev(x, y)
            w0 = self.water(x, y)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p = (x + dx, y + dy)
                if not self.g.inside(*p) or p in seen:
                    continue
                b = g.beh(*p)
                if b in JUMP:
                    if JUMP[b] == (dx, dy):
                        p2 = (p[0] + dx, p[1] + dy)
                        if self.passable(*p2) and p2 not in self.walls and p2 not in seen:
                            seen.add(p2)
                            q.append(p2)
                    continue
                if not self.passable(*p) or p in self.walls:
                    continue
                e = g.elev(*p)
                w = self.water(*p)
                if w != w0:
                    pass            # op/af het water (surfen): hoogte maakt niet uit
                elif not (e in (0, 15) or e0 in (0, 15) or e == e0):
                    continue
                seen.add(p)
                q.append(p)
        return seen

    def entries(self):
        g = self.g
        st = []
        for w in self.d.get('warp_events') or []:
            st.append((w['x'], w['y']))
        for c in self.d.get('connections') or []:
            dr = c.get('direction')
            if dr == 'up':
                st += [(x, 0) for x in range(g.w)]
            elif dr == 'down':
                st += [(x, g.h - 1) for x in range(g.w)]
            elif dr == 'left':
                st += [(0, y) for y in range(g.h)]
            elif dr == 'right':
                st += [(g.w - 1, y) for y in range(g.h)]
        if any(c.get('direction') in ('dive', 'emerge') for c in self.d.get('connections') or []):
            # bovenkomen na duiken kan op elk diep water
            st += [(x, y) for y in range(g.h) for x in range(g.w) if g.beh(x, y) == 'MB_DEEP_WATER']
        return [s for s in st if g.inside(*s) and (self.passable(*s) or s in [(w['x'], w['y']) for w in self.d.get('warp_events') or []])]


def near(seen, x, y, also_self=True):
    if also_self and (x, y) in seen:
        return True
    return any((x + dx, y + dy) in seen for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


def counter_near(g, seen, x, y):
    """Aanspreken over een toonbank: twee tegels verderop bereikbaar."""
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if g.inside(x + dx, y + dy) and g.beh(x + dx, y + dy) == 'MB_COUNTER' and (x + 2 * dx, y + 2 * dy) in seen:
            return True
    return False


def check_reach():
    nmaps = 0
    for n, d in sorted(MAPS.items()):
        g = grid(n)
        if not g or not g.sizeok or 'setmaplayoutindex' in map_script_text(n) or d.get('map_type') == 'MAP_TYPE_UNDERWATER':
            continue
        if n.startswith(('BattleFrontier', 'BattlePyramid', 'TrainerHill', 'Route110_TrickHouse', 'SecretBase', 'Unused', 'InsideOfTruck')) \
                or 'Unused' in n or 'Prototype' in n:
            continue
        R = Reach(n)
        st = R.entries()
        if not st:
            continue
        nmaps += 1
        seen = R.run(st)
        L = LAYOUTS.get(d['layout'], {})
        van_obj = same_positions(n) and part_vanilla(n, 'bg_events') and part_vanilla(n, 'warp_events') \
            and not changed_since_base(L.get('blockdata_filepath', ''))
        sev = 'VANILLA' if van_obj else 'MELD'
        # warps
        for i, w in enumerate(d.get('warp_events') or []):
            x, y = w['x'], w['y']
            if not g.inside(x, y):
                continue
            if not near(seen - {(x, y)}, x, y, also_self=False):
                add('kaarten', sev, 'reachwarp:%s:%d' % (n, i),
                    '%s: warp %d (%d,%d) heeft geen bereikbare buurtegel (aankomst vast, of warp onbereikbaar)' % (n, i, x, y))
        for i, o in enumerate(d.get('object_events') or []):
            x, y = o['x'], o['y']
            if not g.inside(x, y) or o['script'] in ('0x0', 'NULL', '0'):
                continue
            if 'BERRY_TREE' in o['graphics_id'] or o['graphics_id'] in GIANT:
                continue
            if o.get('local_id') and re.search(r'(setobjectxy(perm)?|addobject)\s+%s\b' % o['local_id'], map_script_text(n)):
                continue    # wordt door een script ergens anders neergezet
            if not near(seen, x, y, also_self=False) and not counter_near(g, seen, x, y):
                what = 'item' if 'ITEM_BALL' in o['graphics_id'] else ('trainer' if o.get('trainer_type') != 'TRAINER_TYPE_NONE' else 'object')
                add('kaarten', sev, 'reachobj:%s:%d' % (n, i), '%s: %s %d (%s, %s) op (%d,%d) is niet bereikbaar'
                    % (n, what, i, o['graphics_id'].replace('OBJ_EVENT_GFX_', ''), o['script'] if what != 'item' else o['trainer_sight_or_berry_tree_id'], x, y))
        for i, b in enumerate(d.get('bg_events') or []):
            x, y = b['x'], b['y']
            if not g.inside(x, y) or b['type'] == 'secret_base':
                continue
            ok = (x, y) in seen if b['type'] == 'hidden_item' and R.passable(x, y) else near(seen, x, y)
            if not ok and b['type'] == 'sign':
                # meerdelig bord (bed, terminal): goed als een ander deel met hetzelfde script leesbaar is
                ok = any(b2 is not b and b2.get('script') == b.get('script') and abs(b2['x'] - x) + abs(b2['y'] - y) == 1
                         and near(seen, b2['x'], b2['y']) for b2 in d.get('bg_events') or [])
            if not ok and not counter_near(g, seen, x, y):
                add('kaarten', sev, 'reachbg:%s:%d' % (n, i), '%s: %s %d op (%d,%d) is niet bereikbaar (%s)'
                    % (n, b['type'], i, x, y, b.get('item') or b.get('script')))
        # wandelende NPC's: looproute geblokkeerd door een ander object
        objpos = {(o['x'], o['y']): k for k, o in enumerate(d.get('object_events') or [])}
        for i, o in enumerate(d.get('object_events') or []):
            rx, ry = int(o.get('movement_range_x', 0) or 0), int(o.get('movement_range_y', 0) or 0)
            mt = o['movement_type']
            if not (rx or ry) or not re.search(r'WANDER|WALK_(UP_AND_DOWN|LEFT_AND_RIGHT|SEQUENCE)|COPY', mt):
                continue
            others = [(k, o2) for k, o2 in enumerate(d.get('object_events') or [])
                      if k != i and str(o2.get('flag', '0')) in ('0', '')]
            for k, o2 in others:
                if abs(o2['x'] - o['x']) <= rx and abs(o2['y'] - o['y']) <= ry and \
                        (('UP_AND_DOWN' in mt and o2['x'] == o['x']) or ('LEFT_AND_RIGHT' in mt and o2['y'] == o['y'])
                         or 'WANDER' in mt and (o2['x'] == o['x'] or o2['y'] == o['y'])):
                    # alleen het dichtstbijzijnde object aan die kant telt (verder weg kwam hij toch al niet)
                    dx, dy = o2['x'] - o['x'], o2['y'] - o['y']
                    if any(o3 is not o2 and (o3['x'] - o['x']) * dx >= 0 and (o3['y'] - o['y']) * dy >= 0
                           and (o3['x'] == o['x'] if dx == 0 else o3['y'] == o['y'])
                           and 0 < abs(o3['x'] - o['x']) + abs(o3['y'] - o['y']) < abs(dx) + abs(dy) for _, o3 in others):
                        continue
                    s2 = 'VANILLA' if event_vanilla(n, 'object_events', o) and event_vanilla(n, 'object_events', o2) else 'MELD'
                    add('kaarten', s2, 'walkroute:%s:%d:%d' % (n, i, k), '%s: looproute van object %d (%s, %s, bereik %d/%d) loopt over object %d (%s) op (%d,%d)'
                        % (n, i, o['graphics_id'].replace('OBJ_EVENT_GFX_', ''), mt.replace('MOVEMENT_TYPE_', ''), rx, ry, k,
                           o2['graphics_id'].replace('OBJ_EVENT_GFX_', ''), o2['x'], o2['y']))
    stats['kaarten']['bereikbaarheid'] = nmaps


_TSINFO = {}
_GFXH = read('src/data/tilesets/graphics.h') + read('src/data/tilesets/metatiles.h') + read('src/graphics.c')


def tileset_info(sym):
    """(aantal metatiles, aantal tiles, metatile-data) van een tileset, of None."""
    if sym in _TSINFO:
        return _TSINFO[sym]
    try:
        body = re.search(r'const struct Tileset ' + sym + r' =(?:\s*//[^\n]*)?\s*\{(.*?)\};', _HDR, re.S).group(1)
        tiles = re.search(r'\.tiles = (\w+)', body).group(1)
        mts = re.search(r'\.metatiles = (\w+)', body).group(1)
        tp = re.search(tiles + r'\[\] = INC\w+\("([^"]+)"', _GFXH).group(1)
        tp = re.sub(r'\.(smol|fastSmol|lz)$', '', tp)
        if not tp.endswith('.4bpp'):
            tp = os.path.splitext(tp)[0] + '.4bpp'
        mp = re.search(mts + r'\[\] = INCBIN_U16\("([^"]+)"', _GFXH).group(1)
        mb = open(mp, 'rb').read()
        nt = os.path.getsize(tp) // 32 if os.path.exists(tp) else None
        _TSINFO[sym] = (len(mb) // 16, nt, struct.unpack('<%dH' % (len(mb) // 2), mb))
    except Exception:
        _TSINFO[sym] = None
    return _TSINFO[sym]


def check_graphics():
    """Grafische fouten die je zonder kijken vindt: metatile-nummers buiten de tileset, tegels die naar niet-bestaande
    tiles wijzen of paletten 13-15 gebruiken (die zijn in de overworld niet van de tileset), en lege metatiles."""
    done = set()
    nmaps = 0
    for n, d in sorted(MAPS.items()):
        L = LAYOUTS.get(d['layout'])
        if not L or L['id'] in done:
            continue
        done.add(L['id'])
        g = grid(n)
        if not g:
            continue
        P, S = tileset_info(L['primary_tileset']), tileset_info(L['secondary_tileset'])
        if not P or not S:
            continue
        nmaps += 1
        van = not changed_since_base(L.get('blockdata_filepath', ''))
        used = collections.Counter(v & 0x3FF for v in g.v)
        bad_mt, bad_tile, bad_pal, empty = [], [], [], []
        for mt, cnt in sorted(used.items()):
            if mt < 0x200:
                info, idx = P, mt
            else:
                info, idx = S, mt - 0x200
            if idx >= info[0]:
                bad_mt.append(mt)
                continue
            words = info[2][idx * 8: idx * 8 + 8]
            for wv in words:
                t, pal = wv & 0x3FF, wv >> 12
                ntot = 512 + (S[1] or 512)
                if t >= ntot or (t < 512 and P[1] and t >= P[1]):
                    bad_tile.append(mt)
                    break
                if pal >= 13:
                    bad_pal.append(mt)
                    break
            if mt != 0 and all((wv & 0x3FF) == 0 for wv in words):
                empty.append(mt)
        sev = 'VANILLA' if van else 'FOUT'
        if bad_mt:
            add('kaarten', sev, 'gfxmt:%s' % L['id'], '%s (%s): metatiles buiten de tileset: %s' % (n, L['id'], ', '.join('0x%X' % m for m in bad_mt[:8])))
        if bad_tile:
            add('kaarten', sev, 'gfxtile:%s' % L['id'], '%s (%s): metatiles die naar niet-bestaande tiles wijzen (vuilnis): %s'
                % (n, L['id'], ', '.join('0x%X' % m for m in bad_tile[:8])))
        if bad_pal:
            add('kaarten', 'VANILLA' if van else 'MELD', 'gfxpal:%s' % L['id'], '%s (%s): metatiles met palet 13-15 (niet van de tileset): %s'
                % (n, L['id'], ', '.join('0x%X' % m for m in bad_pal[:8])))
        if empty:
            add('kaarten', 'VANILLA' if van else 'MELD', 'gfxempty:%s' % L['id'], '%s (%s): lege metatiles (alleen tile 0, %d tegels): %s'
                % (n, L['id'], sum(used[m] for m in empty), ', '.join('0x%X' % m for m in empty[:8])))
    stats['kaarten']['tegelcontrole'] = nmaps


def check_maps():
    check_reach()
    check_graphics()
    for g in MAPGROUPS['group_order']:
        n = len(MAPGROUPS[g])
        if n > 128:
            add('kaarten', 'FOUT', 'group:%s' % g, '%s heeft %d kaarten (max 128)' % (g, n))
        elif n >= 120:
            add('kaarten', 'MELD', 'groupfull:%s' % g, '%s: %d/128 kaarten' % (g, n))
    dirs = {os.path.basename(os.path.dirname(p)) for p in glob.glob('data/maps/*/map.json')}
    for dname in sorted(dirs - set(MAP_GROUP)):
        add('kaarten', 'MELD', 'orphan:%s' % dname, 'data/maps/%s staat niet in map_groups.json' % dname)
    stats['kaarten']['kaarten'] = len(MAPS)
    for n, d in sorted(MAPS.items()):
        if d['layout'] not in LAYOUTS:
            if d['layout'] != 'LAYOUT_NONE' and not d['layout'].startswith('0'):
                add('kaarten', 'FOUT', 'layout:%s' % n, '%s: layout %s bestaat niet' % (n, d['layout']))
            continue
        g = grid(n)
        if not g:
            continue
        if not g.sizeok:
            add('kaarten', sev_for(n), 'binsize:%s' % n, '%s: map.bin past niet bij %dx%d uit layouts.json' % (n, g.w, g.h))
        objs = d.get('object_events') or []
        if len(objs) > 64:
            add('kaarten', 'FOUT', 'objmax:%s' % n, '%s: %d objecten (max 64 templates)' % (n, len(objs)))
        # tegelijk zichtbaar: venster van 20x17 rond de speler (TrySpawnObjectEvents)
        if len(objs) > 15:
            best = bestu = 0
            spot = None
            for py in range(g.h):
                for px in range(g.w):
                    inwin = [o for o in objs if px - 9 <= o['x'] <= px + 10 and py - 7 <= o['y'] <= py + 9]
                    cnt = len(inwin)
                    cu = len([o for o in inwin if str(o.get('flag', '0')) in ('0', '')])
                    if cnt > best:
                        best, spot = cnt, (px, py)
                    bestu = max(bestu, cu)
            if bestu > 15:
                add('kaarten', ('VANILLA' if same_positions(n) else 'FOUT'), 'objview:%s' % n,
                    '%s: tot %d objecten zonder flag tegelijk in beeld (max 15 + speler)' % (n, bestu))
            elif best > 15:
                add('kaarten', ('VANILLA' if same_positions(n) else 'MELD'), 'objview:%s' % n,
                    '%s: %d objecten in totaal, tot %d tegelijk in beeld rond %s (incl. objecten met flag; controleer dat ze niet allemaal tegelijk zichtbaar zijn)'
                    % (n, len(objs), best, spot))
        for kind in ('object_events', 'bg_events', 'coord_events', 'warp_events'):
            for i, e in enumerate(d.get(kind) or []):
                if not g.inside(e['x'], e['y']):
                    if kind == 'warp_events':
                        continue   # al bij warps
                    add('kaarten', ('VANILLA' if event_vanilla(n, kind, e) else 'FOUT'), 'out:%s:%s:%d' % (n, kind, i),
                        '%s: %s %d (%d,%d) ligt buiten de kaart (%dx%d)' % (n, kind[:-7], i, e['x'], e['y'], g.w, g.h))
        for i, o in enumerate(objs):
            if not g.inside(o['x'], o['y']):
                continue
            gfx = o['graphics_id']
            if g.blocked(o['x'], o['y']) and gfx not in GIANT and not WALL_OK_GFX.search(gfx) \
                    and 'INVISIBLE' not in o.get('movement_type', ''):
                b = g.beh(o['x'], o['y'])
                add('kaarten', ('VANILLA' if event_vanilla(n, 'object_events', o) else 'MELD'), 'wall:%s:%d' % (n, i),
                    '%s: object %d (%s, %s) staat op een muur/geblokkeerde tegel (%d,%d) [%s]'
                    % (n, i, gfx.replace('OBJ_EVENT_GFX_', ''), o['script'], o['x'], o['y'], b))


# ------------------------------------------------------------------ 3. scripts
def load_text_width():
    spec = importlib.util.spec_from_file_location('dialogen_import', 'tools/dialogen/import.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.text_width


TEXT_LIMIT = 216   # 27 tegels breed tekstvak (de Dialoogstudio breekt al op 208 af)
SKIP_TEXT = re.compile(r'TrickHouse|BattleFrontier|BattleTent|match_call|braille|^data/text/(tv|record_mix|trainers)\.inc|'
                       r'secret_base|contest|BattleDome|BattlePike|BattlePyramid|BattleArena|BattleFactory|BattlePalace|'
                       r'TrainerHill|mauville_man|pokemon_news|apprentice|questionnaire|union_room|cable_club')


UNLOCKING_MSGBOX = ('MSGBOX_NPC', 'MSGBOX_SIGN', 'MSGBOX_AUTOCLOSE')


def _label_order():
    """bestand -> lijst van (regelindex, label) om door te vallen naar het volgende label."""
    out = collections.defaultdict(list)
    for lb, (f, i) in LABELS.items():
        out[f].append((i, lb))
    for f in out:
        out[f].sort()
    return out


_ORDER = None


def next_label(lb):
    global _ORDER
    if _ORDER is None:
        _ORDER = _label_order()
    f, i = LABELS[lb]
    lst = _ORDER[f]
    for j, (k, l2) in enumerate(lst):
        if l2 == lb:
            return lst[j + 1][1] if j + 1 < len(lst) else None
    return None


def lock_paths(start, limit=4000):
    """Loop alle paden van een script af; geeft de labels terug waar het script eindigt terwijl de speler
    nog vastzit (lock/lockall zonder release)."""
    bad = set()
    seen = set()
    stack = [(start, 0, False, ())]
    steps = 0
    while stack and steps < limit:
        lb, idx, locked, calls = stack.pop()
        if (lb, idx, locked, calls) in seen or lb not in LABELS:
            continue
        seen.add((lb, idx, locked, calls))
        steps += 1
        lines = body(lb)
        j = idx
        done = False
        prev = None
        while j < len(lines):
            c, args = cmd_args(lines[j])
            j += 1
            if c:
                prev, cur = (lines[j - 2] if j >= 2 else ''), c
            if not c or c.startswith('.'):
                if c in ('.byte', '.2byte', '.4byte', '.string'):
                    done = True   # data, geen script
                    break
                continue
            if c in ('lock', 'lockall'):
                locked = True
            elif c in ('release', 'releaseall') or c.startswith('warp') or (c == 'special' and args and 'Warp' in args[0]) or c.startswith('trainerbattle') \
                    or (c == 'msgbox' and len(args) > 1 and args[1] in UNLOCKING_MSGBOX):
                locked = False
                if c.startswith('trainerbattle') and len(args) >= 4 and args[-1] in LABELS:
                    stack.append((args[-1], 0, False, calls))
                if c.startswith('warp'):
                    done = True
                    break
            elif c == 'goto' and args:
                stack.append((args[0], 0, locked, calls))
                done = True
                break
            elif (c.startswith('goto_if') or c == 'case') and args and args[-1] in LABELS:
                stack.append((args[-1], 0, locked, calls))
            elif (c == 'call' or c.startswith('call_if')) and args and args[-1] in LABELS and len(calls) < 6:
                # subroutine: eerst erin, daarna verder na de call (de lock-status na de call nemen we
                # ruim: beide mogelijkheden)
                stack.append((args[-1], 0, locked, calls + ((lb, j),)))
                if c != 'call':
                    continue
                done = True
                break
            elif c == 'return':
                if calls:
                    rlb, rj = calls[-1]
                    stack.append((rlb, rj, locked, calls[:-1]))
                elif locked:
                    bad.add(lb)
                done = True
                break
            elif c in ('end', 'releaseall_end', 'goto_if_unset_end'):
                # 'end' direct na een rij goto_if/case is meestal onbereikbaar (JA/NEE, switch)
                pc = cmd_args(prev or '')[0] or ''
                if locked and not (pc.startswith('goto_if') or pc == 'case'):
                    bad.add(lb)
                done = True
                break
        if not done:
            nl = next_label(lb)
            if nl:
                stack.append((nl, 0, locked, calls))
    return bad


def check_softlocks():
    seen = set()
    n_checked = 0
    for n, d in sorted(MAPS.items()):
        for kind in ('object_events', 'bg_events', 'coord_events'):
            for e in d.get(kind) or []:
                s = e.get('script')
                if not s or s in seen or s not in LABELS:
                    continue
                seen.add(s)
                n_checked += 1
                bad = lock_paths(s)
                for b in sorted(bad):
                    van = label_vanilla(s) and label_vanilla(b)
                    add('scripts', 'VANILLA' if van else 'MELD', 'lock:%s:%s' % (s, b),
                        '%s: script %s kan eindigen in %s terwijl de speler nog vastzit (lock zonder release op dat pad)' % (n, s, b))
    stats['scripts']['lock-paden'] = n_checked


OBJ_CMDS = ('applymovement', 'waitmovement', 'removeobject', 'addobject', 'showobjectat', 'hideobjectat', 'setobjectxy',
            'setobjectxyperm', 'turnobject', 'setobjectmovementtype', 'copyobjectxytoperm', 'faceplayer_obj')


def check_localids():
    glob_ids = set(re.findall(r'#define\s+(LOCALID_\w+)', read('include/constants/event_objects.h')))
    for f in glob.glob('include/constants/*.h'):
        if 'map_event_ids' not in f:
            glob_ids |= set(re.findall(r'#define\s+(LOCALID_\w+)', read(f)))
    owner = collections.defaultdict(set)
    for n, d in MAPS.items():
        for o in d.get('object_events') or []:
            if o.get('local_id'):
                owner[o['local_id']].add(n)
    for n, d in sorted(MAPS.items()):
        p = 'data/maps/%s/scripts.inc' % n
        if not os.path.exists(p):
            continue
        objs = d.get('object_events') or []
        mine = {o.get('local_id') for o in objs}
        # .set LOCALID_X, N: object N moet nog hetzelfde object zijn als in vanilla
        bt = base_file('data/maps/%s/map.json' % n)
        try:
            bobjs = json.loads(bt).get('object_events') or [] if bt else None
        except ValueError:
            bobjs = None
        for m in re.finditer(r'^\.set\s+(LOCALID_\w+)\s*,\s*(\d+)', read(p), re.M):
            k = int(m.group(2))
            if k > len(objs):
                add('scripts', 'FOUT', 'setid:%s:%s' % (n, m.group(1)), '%s: .set %s, %d maar de kaart heeft %d objecten' % (p, m.group(1), k, len(objs)))
            elif bobjs and k <= len(bobjs) and (bobjs[k - 1]['graphics_id'], bobjs[k - 1]['script']) != (objs[k - 1]['graphics_id'], objs[k - 1]['script']):
                add('scripts', 'FOUT', 'setid:%s:%s' % (n, m.group(1)), '%s: .set %s, %d wijst nu naar %s (%s) i.p.v. %s; geef het object een local_id'
                    % (p, m.group(1), k, objs[k - 1]['graphics_id'], objs[k - 1]['script'], bobjs[k - 1]['graphics_id']))
        for j, l in enumerate(FILELINES.get(p, [])):
            c, args = cmd_args(l.split('@')[0].strip())
            if c not in OBJ_CMDS or not args:
                continue
            a = args[0]
            if a.startswith('LOCALID_') and a not in mine and a not in glob_ids:
                if not owner.get(a):
                    add('scripts', 'FOUT', 'localid:%s:%s' % (n, a), '%s:%d: %s %s bestaat op geen enkele kaart' % (p, j + 1, c, a))
                elif not re.search(r'\bwarp\w*\s+MAP_', read(p)) and not label_vanilla(next((lb for lb, (ff, ii) in LABELS.items() if ff == p and ii < j), '') or ''):
                    add('scripts', 'MELD', 'localid:%s:%s' % (n, a), '%s:%d: %s %s hoort bij %s, niet bij deze kaart'
                        % (p, j + 1, c, a, ', '.join(sorted(owner[a]))))
            elif re.fullmatch(r'\d+', a) and 0 < int(a) < 200 and int(a) > len(objs):
                add('scripts', 'FOUT', 'localid:%s:%s' % (n, a), '%s:%d: %s %s, maar de kaart heeft maar %d objecten' % (p, j + 1, c, a, len(objs)))


def check_scripts():
    # scripts.inc in event_scripts.s
    ev = read('data/event_scripts.s')
    for n in MAPS:
        p = 'data/maps/%s/scripts.inc' % n
        if os.path.exists(p) and ('maps/%s/scripts.inc' % n) not in ev:
            add('scripts', 'FOUT', 'notinc:%s' % n, '%s niet opgenomen in data/event_scripts.s' % p)
    # map.json-scripts
    nscr = 0
    for n, d in sorted(MAPS.items()):
        for kind in ('object_events', 'bg_events', 'coord_events'):
            for i, e in enumerate(d.get(kind) or []):
                s = e.get('script')
                if not s or s in ('0x0', '0', 'NULL'):
                    continue
                nscr += 1
                if not label_exists(s):
                    add('scripts', 'FOUT', 'nolabel:%s:%s:%d' % (n, kind, i), '%s: %s %d gebruikt script %s, dat niet bestaat' % (n, kind[:-7], i, s))
    stats['scripts']['map-scripts'] = nscr
    # labels in scriptcommando's
    nref = 0
    for f, ls in FILELINES.items():
        if not (f.startswith('data/maps/') or f.startswith('data/scripts/')):
            continue
        for j, l in enumerate(ls):
            s = l.split('@')[0].strip()
            if not s or s.startswith('.string') or s.endswith(':') or s.startswith('#') or s.startswith('.'):
                continue
            c, args = cmd_args(s)
            for a in args:
                for lb in LABELISH.findall(a):
                    nref += 1
                    if not label_exists(lb):
                        add('scripts', 'FOUT', 'ref:%s:%s' % (f, lb), '%s:%d: label %s bestaat niet' % (f, j + 1, lb))
    stats['scripts']['labelverwijzingen'] = nref
    # coord-events moeten de besturing teruggeven
    release = re.compile(r'^(releaseall|release|warp\w*|trainerbattle\w*|special\s+\w*(Warp|Battle)\w*|waitstate|goto\s+Common_EventScript_\w*|end_?trainer\w*)\b')
    seen_scripts = set()
    for n, d in sorted(MAPS.items()):
        for i, e in enumerate(d.get('coord_events') or []):
            s = e.get('script')
            if e.get('type') != 'trigger' or not s or s in ('0x0', '0') or s in seen_scripts or s not in LABELS:
                continue
            seen_scripts.add(s)
            labs = reachable(s)
            ok = locks = effect = False
            for lb in labs:
                for l in body(lb):
                    if release.match(l):
                        ok = True
                    if re.match(r'^(lock|lockall)\b', l):
                        locks = True
                    if re.match(r'^(playse|playfanfare|msgbox|message|applymovement|delay|waitse|waitmovement|special|fadescreen\w*|setmetatile)\b', l):
                        effect = True
            if ok or not (locks or effect):
                continue
            van = all(label_vanilla(lb) for lb in labs)
            if locks:
                add('scripts', 'VANILLA' if van else 'FOUT', 'coordrel:%s' % s,
                    '%s: coord-event-script %s doet lock/lockall maar nooit releaseall/warp (speler staat vast)' % (n, s))
            else:
                add('scripts', 'VANILLA' if van else 'MELD', 'coordrel:%s' % s,
                    '%s: coord-event-script %s eindigt zonder releaseall (Lessen: coord-triggers vergrendelen de besturing)' % (n, s))
    stats['scripts']['coord-scripts'] = len(seen_scripts)
    check_softlocks()
    check_localids()
    # tekstbreedte
    tw = load_text_width()
    ntxt = 0
    for f, ls in FILELINES.items():
        if not (f.startswith('data/maps/') or f.startswith('data/scripts/') or f.startswith('data/text/')):
            continue
        if SKIP_TEXT.search(f):
            continue
        cur_label, buf, start = None, '', 0
        base = None
        for j, l in enumerate(ls + ['']):
            m = re.match(r'^\s*\.string\s+"(.*)"\s*$', l)
            if m:
                if not buf:
                    start = j
                buf += m.group(1)
                continue
            if buf:
                if not SKIP_TEXT.search(cur_label or ''):
                    ntxt += 1
                    for part in re.split(r'\\[nlp]|\$', buf):
                        part2 = part.replace('\\"', '"')
                        part2 = re.sub(r'\{(PAUSE|PLAY_SE|PLAY_BGM|FONT_\w+|COLOR|SHADOW|HIGHLIGHT|CLEAR\w*|PAUSE_UNTIL_PRESS|PAUSE_MUSIC|RESUME_MUSIC|WAIT_SE|SPEED_\w*|SKIP|FIXED_\w*)[^}]*\}', '', part2)
                        w = tw(part2)
                        if w > TEXT_LIMIT and '{FONT_' not in buf:
                            if base is None:
                                base = base_file(f) if not changed_since_base(f) or True else ''
                            sev = 'VANILLA' if part.strip() and part in base else 'FOUT'
                            add('scripts', sev, 'width:%s:%s' % (cur_label, part[:20]),
                                '%s:%d (%s): regel %d px breed (max %d): "%s"' % (f, start + 1, cur_label, w, TEXT_LIMIT, part))
                buf = ''
            m = re.match(r'^([A-Za-z_]\w*)::?', l)
            if m:
                cur_label = m.group(1)
    stats['scripts']['teksten'] = ntxt


# ------------------------------------------------------------------ 4. flags en vars
RANGE_NAME = re.compile(r'(_START|_END|_COUNT|^NUM_|_FIRST|_LAST|_MAX|UNUSED|SPECIAL_FLAGS|TEMP_FLAGS|_BASE$)')


def dup_groups(defs, ev, prefix, base_text):
    base_defs = load_defines(base_text) if base_text else {}
    base_ev = evaluator(dict(load_defines(base_file('include/constants/opponents.h')), **base_defs))
    groups = collections.defaultdict(list)
    for name in defs:
        if not name.startswith(prefix) or RANGE_NAME.search(name):
            continue
        e = defs[name]
        if re.fullmatch(r'[A-Za-z_]\w*', e) and e in defs and not RANGE_NAME.search(e) and e.startswith(prefix):
            continue    # bewuste alias: #define FLAG_A FLAG_B
        v = ev(name)
        if v is None:
            continue
        groups[v].append(name)
    out = []
    for v, names in sorted(groups.items()):
        if len(names) < 2:
            continue
        if all(base_ev(nm) == v for nm in names):
            continue    # zelfde dubbel als in vanilla
        out.append((v, names))
    return out


def used_names(prefix):
    """Alle namen met dit voorvoegsel die buiten de constants-headers voorkomen (bestand -> set)."""
    use = collections.defaultdict(set)
    files = SCRIPT_FILES + glob.glob('data/maps/*/map.json') + glob.glob('src/**/*.c', recursive=True) + \
        glob.glob('src/**/*.h', recursive=True) + glob.glob('src/data/*.json')
    rx = re.compile(r'\b' + prefix + r'\w+')
    for f in files:
        for nm in set(rx.findall(read(f))):
            use[nm].add(f)
    return use


def _CHANGED_LINES_FILES(name):
    """Bestanden waarin `name` nieuw voorkomt t.o.v. vanilla (of die nieuw zijn)."""
    out = set()
    for f in SCRIPT_FILES + glob.glob('data/maps/*/map.json') + glob.glob('src/**/*.c', recursive=True):
        if name in read(f) and changed_since_base(f) and name not in base_file(f):
            out.add(f)
    return out


def check_flags():
    blocks = []
    for name in ('include/constants/flags.h', 'include/constants/opponents.h', 'include/constants/vars.h'):
        cur = None
        for i, l in enumerate(read(name).split('\n'), 1):
            if re.match(r'// \w+ \{', l):
                if cur:
                    add('flags', 'FOUT', 'block:%s:%s' % (name, cur), '%s:%d: generatorblok "%s" niet gesloten met "// }"' % (name, i, cur))
                cur = l.split()[1]
            elif l.startswith('// }'):
                cur = None
        if cur:
            add('flags', 'FOUT', 'block:%s:%s' % (name, cur), '%s: generatorblok "%s" niet gesloten aan het eind' % (name, cur))
    num = FLAG('NUM_GROUNDED_FLAGS')
    start = FLAG('GROUNDED_FLAGS_START')
    ng = 0
    for nm, e in FLAG_DEFS.items():
        m = re.search(r'FLAG_GROUNDED\((\d+)\)', e)
        if m:
            ng += 1
            if int(m.group(1)) >= num:
                add('flags', 'FOUT', 'grounded:%s' % nm, '%s = FLAG_GROUNDED(%s) valt buiten NUM_GROUNDED_FLAGS (%d)' % (nm, m.group(1), num))
    stats['flags']['FLAG_GROUNDED'] = ng
    # dubbele waarden
    for v, names in dup_groups(FLAG_DEFS, FLAG, 'FLAG_', base_file('include/constants/flags.h')):
        add('flags', 'FOUT', 'dupflag:%s' % '/'.join(sorted(names)), 'flagwaarde 0x%X dubbel: %s' % (v, ', '.join(names)))
    for v, names in dup_groups(VAR_DEFS, VAR, 'VAR_', base_file('include/constants/vars.h')):
        add('flags', 'FOUT', 'dupvar:%s' % '/'.join(sorted(names)), 'varwaarde 0x%X dubbel: %s' % (v, ', '.join(names)))
    # UNUSED-flags/vars die toch gebruikt worden (door meerdere systemen?)
    for prefix, defs in (('FLAG_UNUSED', FLAG_DEFS), ('VAR_UNUSED', VAR_DEFS)):
        use = used_names(prefix)
        for nm, files in sorted(use.items()):
            sys_ = {re.sub(r'^data/maps/([A-Za-z]+?)(_|City|Town|\d|/).*', r'\1', f) for f in files}
            if len(files) > 0:
                sev = 'MELD' if any(f in _CHANGED_LINES_FILES(nm) for f in files) else 'VANILLA'
                add('flags', sev, 'unusedused:%s' % nm, '%s heet "unused" maar wordt gebruikt in %s' % (nm, ', '.join(sorted(files)[:4])))
    # vars die door meerdere onafhankelijke systemen gebruikt worden (alleen nieuwe/hergebruikte vars)
    stats['flags']['flags'] = len([n for n in FLAG_DEFS if n.startswith('FLAG_')])
    stats['flags']['vars'] = len([n for n in VAR_DEFS if n.startswith('VAR_')])


# ------------------------------------------------------------------ 5. trainers
def species_const(s):
    out, us = [], False
    s = s.replace('’', '').replace("'", '').replace('%', '')
    for ch in s:
        if ch.isascii() and ch.isalnum():
            if us:
                out.append('_')
            us = False
            out.append(ch.upper())
        elif ch == '♂':
            out.append('_M'); us = False
        elif ch == '♀':
            out.append('_F'); us = False
        elif ch == 'é':
            if us:
                out.append('_')
            us = False
            out.append('E')
        else:
            us = True
    return 'SPECIES_' + ''.join(out)


def plain_const(prefix, s):
    s = s.strip()
    if s.startswith(prefix + '_'):
        return s
    return prefix + '_' + ''.join(c.upper() if (c.isascii() and c.isalnum()) else ('' if c == "'" else '_') for c in s)


def parse_party():
    t = re.sub(r'/\*.*?\*/', '', read('src/data/trainers.party'), flags=re.S)
    trainers = {}
    for blk in re.split(r'^(?====\s*TRAINER_)', t, flags=re.M):
        m = re.match(r'===\s*(\w+)\s*===', blk)
        if not m:
            continue
        mons = []
        for chunk in re.split(r'\n\s*\n', blk)[1:]:
            ls = [l.strip() for l in chunk.strip().split('\n') if l.strip()]
            if not ls or ':' in ls[0] and not re.search(r'\(.*\)|@', ls[0]) and re.match(r'^[A-Z][\w ]*:', ls[0]):
                continue
            head = ls[0].split('@')[0].strip()
            head = re.sub(r'\((M|F)\)\s*$', '', head).strip()
            mm = re.search(r'\(([^()]*)\)\s*$', head)
            sp = mm.group(1) if mm else head
            mon = {'species': species_const(sp), 'raw': ls[0]}
            for l in ls[1:]:
                k = re.match(r'(Level|Ability):\s*(.*)', l)
                if k and k.group(1) == 'Level':
                    mon['lvl'] = k.group(2).strip()
                elif k:
                    mon['ability'] = plain_const('ABILITY', k.group(2))
            mons.append(mon)
        trainers[m.group(1)] = mons
    return trainers


def species_abilities():
    defs = {}
    for f in glob.glob('src/data/pokemon/species_info/*.h') + ['src/data/pokemon/species_info.h']:
        t = read(f)
        for m in re.finditer(r'#define\s+(\w+_ABILITIES)\s+\{([^}]*)\}', t):
            defs.setdefault(m.group(1), set()).update(re.findall(r'ABILITY_\w+', m.group(2)))   # #if/#else: alle varianten
    ab = collections.defaultdict(set)
    unknown = set()
    for f in glob.glob('src/data/pokemon/species_info/*.h'):
        cur = None
        for l in read(f).split('\n'):
            m = re.match(r'\s*\[(SPECIES_\w+)\]\s*=', l)
            if m:
                cur = m.group(1)
                if not l.rstrip().endswith('=') and '{' not in l:
                    unknown.add(cur)
                continue
            if cur and '.abilities' in l:
                mm = re.search(r'\.abilities\s*=\s*(\{[^}]*\}|\w+)', l)
                if mm:
                    v = mm.group(1)
                    if v.startswith('{'):
                        s = set(re.findall(r'ABILITY_\w+', v))
                        if not s:
                            unknown.add(cur)
                        ab[cur] |= s
                    elif v in defs:
                        ab[cur] |= defs[v]
                    else:
                        unknown.add(cur)
    return ab, unknown


def level_evolutions():
    """pre -> [(level, post)] en post -> (level, pre) voor EVO_LEVEL-evoluties (alleen gewone level-evoluties)."""
    up, down = collections.defaultdict(list), {}
    for f in glob.glob('src/data/pokemon/species_info/*.h'):
        cur = None
        for l in read(f).split('\n'):
            m = re.match(r'\s*\[(SPECIES_\w+)\]\s*=', l)
            if m:
                cur = m.group(1)
            if cur and '.evolutions' in l:
                for lv, post in re.findall(r'\{EVO_LEVEL,\s*(\d+),\s*(SPECIES_\w+)\s*\}', l):
                    up[cur].append((int(lv), post))
                    down.setdefault(post, (int(lv), cur))
    return up, down


def trainer_maps():
    """trainer -> set(kaart) uit trainerbattle-commando's in data/maps/*/scripts.inc"""
    out = collections.defaultdict(set)
    for f, ls in FILELINES.items():
        if not f.startswith('data/maps/'):
            continue
        n = f.split('/')[2]
        for l in ls:
            c, args = cmd_args(l.split('@')[0].strip())
            if c and c.startswith('trainerbattle'):
                for a in args:
                    if re.fullmatch(r'TRAINER_\w+', a) and not a.startswith(('TRAINER_BATTLE_', 'TRAINER_TYPE_')):
                        out[a].add(n)
    return out


BOSS = re.compile(r'Leader|Elite|Champion|Rival|Boss|Admin|Magma Leader|Aqua Leader|Legend|Stadium|Dave', re.I)


def check_trainer_fit(trainers):
    """Gevechten die niet op hun plek voelen: level ver van de andere trainers op die kaart, en evoluties
    die niet bij het level passen (meldingen; grap-trainers van Jordi staan in IGNORE of worden zo gemeld)."""
    up, down = level_evolutions()
    tmaps = trainer_maps()
    party_text = read('src/data/trainers.party')
    cls = dict(re.findall(r'===\s*(TRAINER_\w+)\s*===\s*\n(?:[^\n]*\n)*?Class:\s*([^\n]*)', party_text))
    permap = collections.defaultdict(list)
    for tr, ms in trainers.items():
        lv = [int(m['lvl']) for m in ms if re.fullmatch(r'\d+', m.get('lvl') or '')]
        if not lv or re.search(r'_\d$', tr):
            continue
        for n in tmaps.get(tr, ()):
            permap[n].append((tr, max(lv)))
    nchk = 0
    for n, lst in sorted(permap.items()):
        if len(lst) < 3:
            continue
        med = statistics.median(v for _, v in lst)
        for tr, v in lst:
            nchk += 1
            if BOSS.search(cls.get(tr, '')):
                continue
            if v > med + 12 or v < med - 15:
                add('trainers', 'MELD', 'lvlfit:%s' % tr, '%s op %s: ace lv %d, de andere trainers op die kaart rond lv %d'
                    % (tr, n, v, med))
    stats['trainers']['level-vergelijking'] = nchk
    # mugshot bij belangrijke gevechten (CLAUDE.md: rivalen, gymleiders, Archie, Maxie, Wally, Birch)
    nmug = 0
    for blk in re.split(r'^(?====\s*TRAINER_)', party_text, flags=re.M):
        m = re.match(r'===\s*(TRAINER_\w+)\s*===', blk)
        if not m or m.group(1).startswith('TRAINER_STADIUM_') or m.group(1) not in tmaps:
            continue
        head = blk.split('\n\n')[0]
        c = re.search(r'^Class:\s*(.*)$', head, re.M)
        c = c.group(1).strip() if c else ''
        if c in ('Leader', 'Rival', 'Champion', 'Aqua Leader', 'Magma Leader', 'Professor') or 'WALLY' in m.group(1):
            nmug += 1
            if not re.search(r'^Mugshot:', head, re.M):
                add('trainers', 'MELD', 'mugshot:%s' % m.group(1), '%s (%s, %s) heeft geen Mugshot:'
                    % (m.group(1), c, ', '.join(sorted(tmaps[m.group(1)]))))
    stats['trainers']['belangrijke gevechten'] = nmug
    nevo = 0
    for tr, ms in sorted(trainers.items()):
        for i, m in enumerate(ms):
            sp, lv = m['species'], m.get('lvl')
            if not lv or not re.fullmatch(r'\d+', lv) or tr.startswith('TRAINER_STADIUM_') or 'Eviolite' in m['raw']:
                continue    # Stadium: alles lv 50; Eviolite: bewust niet geëvolueerd
            lv = int(lv)
            if sp in up:
                need = min(l for l, _ in up[sp])
                if lv >= need + 3:
                    nevo += 1
                    add('trainers', 'INFO', 'evo:%s:%d' % (tr, i), '%s: %s op lv %d is nog niet geëvolueerd (evolueert op %d)'
                        % (tr, sp.replace('SPECIES_', ''), lv, need))
            if sp in down and lv < down[sp][0] - 2:
                nevo += 1
                add('trainers', 'INFO', 'evo:%s:%d' % (tr, i), '%s: %s op lv %d, maar %s evolueert pas op %d'
                    % (tr, sp.replace('SPECIES_', ''), lv, down[sp][1].replace('SPECIES_', ''), down[sp][0]))
    stats['trainers']['evolutie-meldingen'] = nevo


def check_trainers():
    trainers = parse_party()
    check_trainer_fit(trainers)
    species_h = read('include/constants/species.h')
    species = set(re.findall(r'#define\s+(SPECIES_\w+)', species_h))
    ab, unknown_ab = species_abilities()
    nmons = 0
    for tr, mons in trainers.items():
        for i, mon in enumerate(mons):
            nmons += 1
            sp = mon['species']
            if sp not in species:
                add('trainers', 'FOUT', 'species:%s:%d' % (tr, i), '%s: soort %s (%s) bestaat niet' % (tr, sp, mon['raw']))
            lv = mon.get('lvl')
            if lv is None or not re.fullmatch(r'\d+', lv) or not 1 <= int(lv) <= 100:
                if lv is None or re.fullmatch(r'\d+', lv or ''):
                    add('trainers', 'FOUT', 'lvl:%s:%d' % (tr, i), '%s: %s heeft level %s' % (tr, sp, lv))
            a = mon.get('ability')
            if a and sp in ab and sp not in unknown_ab and a not in ab[sp]:
                add('trainers', 'FOUT', 'ability:%s:%d' % (tr, i),
                    '%s: %s heeft %s, maar die soort kan alleen %s' % (tr, sp, a, ', '.join(sorted(ab[sp] - {'ABILITY_NONE'}))))
    stats['trainers']['partijen'] = len(trainers)
    stats['trainers']['pokemon'] = nmons
    # trainerconstanten
    opp = load_defines(read('include/constants/opponents.h'))
    oev = evaluator(opp)
    ids = {n: oev(n) for n in opp if n.startswith('TRAINER_') and n not in ('TRAINER_NONE',) and not RANGE_NAME.search(n)
           and not n.startswith('TRAINER_PARTNER')}
    maxid = oev('MAX_TRAINERS_COUNT') or 1200
    # gebruikt in scripts / C (niet: opponents.h, trainers.party, gegenereerde trainers.h)
    use = collections.defaultdict(set)
    files = SCRIPT_FILES + glob.glob('data/maps/*/map.json') + [f for f in glob.glob('src/**/*.c', recursive=True) + glob.glob('src/**/*.h', recursive=True)
                                                                  if not f.endswith('src/data/trainers.h')]
    for f in files:
        for nm in set(re.findall(r'\bTRAINER_\w+', read(f))):
            use[nm].add(f)
    battle_refs = set()
    for f, ls in FILELINES.items():
        for l in ls:
            c, args = cmd_args(l.strip())
            if c and (c.startswith('trainerbattle') or c in ('settrainerflag', 'cleartrainerflag', 'checktrainerflag', 'goto_if_defeated', 'goto_if_not_defeated', 'call_if_defeated', 'call_if_not_defeated')):
                for a in args:
                    if re.fullmatch(r'TRAINER_\w+', a):
                        battle_refs.add(a)
    for tname in sorted(battle_refs):
        if tname in ids and tname not in trainers:
            add('trainers', 'FOUT', 'noparty:%s' % tname, '%s wordt in een script gebruikt maar heeft geen partij in trainers.party' % tname)
        elif tname not in ids and tname not in opp and not tname.startswith(('TRAINER_BATTLE_', 'TRAINER_TYPE_')):
            add('trainers', 'FOUT', 'noconst:%s' % tname, '%s wordt in een script gebruikt maar bestaat niet in opponents.h' % tname)
    for tname in sorted(trainers):
        if tname not in opp:
            add('trainers', 'FOUT', 'partyconst:%s' % tname, 'trainers.party heeft %s, maar die constante bestaat niet' % tname)
    used_ids = {v for n, v in ids.items() if v is not None and use.get(n)}
    defined = {v for v in ids.values() if v is not None}
    unused = sorted(n for n, v in ids.items() if v is not None and not use.get(n))
    free = [i for i in range(1, maxid) if i not in defined]
    stats['trainers']['trainer-id\'s'] = len(defined)
    stats['trainers']['vrije id\'s'] = len(free)
    stats['trainers']['ongebruikte constanten'] = len(unused)
    dup = collections.defaultdict(list)
    for n, v in ids.items():
        if v is not None:
            dup[v].append(n)
    for v, ns in dup.items():
        if len(ns) > 1:
            add('trainers', 'FOUT', 'dupid:%d' % v, 'trainer-id %d dubbel: %s' % (v, ', '.join(ns)))
    # alleen gebruikt op ongebruikte kaarten (Unused/Prototype) en nergens anders
    dead_maps = re.compile(r'data/maps/[^/]*(Unused|Prototype)[^/]*/')
    onlydead = sorted(n for n, v in ids.items() if v is not None and use.get(n)
                      and all(dead_maps.search(f) for f in use[n]))
    stats['trainers']['alleen op ongebruikte kaarten'] = len(onlydead)
    for n in onlydead:
        add('trainers', 'INFO', 'deadmaptrainer:%s' % n, '%s (id %d) staat alleen op ongebruikte kaarten (%s): kan vrij'
            % (n, ids[n], ', '.join(sorted(f.split('/')[2] for f in use[n]))))
    for n in unused:
        add('trainers', 'INFO', 'unusedtrainer:%s' % n, '%s (id %d) wordt nergens gebruikt (kan vrij)%s'
            % (n, ids[n], '' if n in trainers else ', geen partij'))
    global FREE_IDS
    FREE_IDS = free


FREE_IDS = []


# ------------------------------------------------------------------ 6. wilde encounters
def check_wild():
    cur = json.load(open('src/data/wild_encounters.json'))
    try:
        base = json.loads(base_file('src/data/wild_encounters.json'))
    except Exception:
        base = {'wild_encounter_groups': []}
    btabs = {}
    for g in base['wild_encounter_groups']:
        for e in g['encounters']:
            btabs[e.get('base_label')] = e
    ntab = 0
    for g in cur['wild_encounter_groups']:
        slots = {f['type']: len(f['encounter_rates']) for f in g.get('fields', [])}
        if not slots:
            slots = {'land_mons': 12, 'water_mons': 5, 'rock_smash_mons': 5, 'fishing_mons': 10}
        for e in g['encounters']:
            lbl = e.get('base_label')
            for k, v in e.items():
                if not isinstance(v, dict) or 'mons' not in v:
                    continue
                ntab += 1
                mons = v['mons']
                vanilla = btabs.get(lbl, {}).get(k) == v
                sev = 'VANILLA' if vanilla else 'FOUT'
                key = 'wild:%s:%s' % (lbl, k)
                if k in slots and len(mons) != slots[k]:
                    add('wild', sev, key + ':n', '%s %s: %d slots (moet %d zijn)' % (lbl, k, len(mons), slots[k]))
                elif k not in slots:
                    add('wild', 'MELD', key + ':field', '%s: veld %s is niet gedefinieerd in fields' % (lbl, k))
                for i, m in enumerate(mons):
                    if 'min_level' not in m or 'max_level' not in m:
                        add('wild', sev, key + ':lv%d' % i, '%s %s slot %d (%s): min_level of max_level ontbreekt' % (lbl, k, i, m.get('species')))
                    elif m['min_level'] > m['max_level']:
                        add('wild', sev, key + ':lv%d' % i, '%s %s slot %d (%s): min_level %d > max_level %d' % (lbl, k, i, m['species'], m['min_level'], m['max_level']))
                    elif not (1 <= m['min_level'] <= 100 and 1 <= m['max_level'] <= 100):
                        add('wild', sev, key + ':lv%d' % i, '%s %s slot %d (%s): level buiten 1-100' % (lbl, k, i, m['species']))
                town = MAPS.get(ID2NAME.get(e.get('map'), ''), {}).get('map_type') in ('MAP_TYPE_CITY', 'MAP_TYPE_TOWN')  # steden met gras: uitzondering
                if k == 'land_mons' and not vanilla and not town:
                    c = collections.Counter(m['species'] for m in mons)
                    d = sorted(s for s, n in c.items() if n > 1)
                    if d:
                        hi = max(m.get('max_level', 0) for m in mons)
                        post = hi >= 70
                        add('wild', 'MELD' if post else 'INFO', key + ':dup',
                            '%s land (lv tot %d%s): dubbele soorten %s' % (lbl, hi, ', post-game' if post else '', ', '.join(s.replace('SPECIES_', '') for s in d)))
    stats['wild']['tabellen'] = ntab
    # wilde levels die niet bij de trainers op dezelfde kaart passen
    trainers = parse_party()
    tm = trainer_maps()
    permap = collections.defaultdict(list)
    for tr, ms in trainers.items():
        lv = [int(m['lvl']) for m in ms if re.fullmatch(r'\d+', m.get('lvl') or '')]
        if lv and not re.search(r'_\d$', tr):
            for n in tm.get(tr, ()):
                permap[n].append(max(lv))
    for g in cur['wild_encounter_groups']:
        for e in g['encounters']:
            n = ID2NAME.get(e.get('map'))
            if not n or len(permap.get(n, [])) < 3:
                continue
            lm = e.get('land_mons')
            if not lm or btabs.get(e.get('base_label'), {}).get('land_mons') == lm:
                continue
            wl = statistics.median(m.get('max_level', 0) for m in lm['mons'])
            tl = statistics.median(permap[n])
            if wl > tl + 12 or wl < tl - 20:
                add('wild', 'MELD', 'wildlvl:%s' % e['base_label'], '%s: wilde Pokémon rond lv %d, trainers op die kaart rond lv %d'
                    % (e['base_label'], wl, tl))


# ------------------------------------------------------------------ 7. items
def check_items():
    flags = collections.defaultdict(list)
    nballs = nhidden = 0
    tm_src = collections.defaultdict(set)
    tm_new = set()      # (tm, bron) die niet uit vanilla komen
    for n, d in sorted(MAPS.items()):
        for i, o in enumerate(d.get('object_events') or []):
            it = o.get('trainer_sight_or_berry_tree_id', '')
            if o['script'] == 'Common_EventScript_FindItem':
                nballs += 1
                fv = flagval(o.get('flag'))
                if fv is None:
                    add('items', sev_for(n), 'noflag:%s:%d' % (n, i), '%s: item-ball %d (%s) heeft geen flag (komt steeds terug)' % (n, i, it))
                else:
                    flags[fv].append('%s item %s (%d,%d)' % (n, it.replace('ITEM_', ''), o['x'], o['y']))
                if it.startswith('ITEM_TM'):
                    tm_src[it].add('ligt: %s' % n)
                    if not event_vanilla(n, 'object_events', o):
                        tm_new.add((it, 'ligt: %s' % n))
            elif str(o.get('flag', '0')) not in ('0', ''):
                fv = flagval(o['flag'])
                if fv is not None:
                    flags[fv].append('%s object %d (%s)' % (n, i, o['graphics_id'].replace('OBJ_EVENT_GFX_', '')))
        for i, b in enumerate(d.get('bg_events') or []):
            if b.get('type') == 'hidden_item':
                nhidden += 1
                fv = flagval(b.get('flag'))
                if fv is None:
                    add('items', sev_for(n), 'noflag:%s:bg%d' % (n, i), '%s: verborgen item %d (%s) heeft geen flag' % (n, i, b.get('item')))
                else:
                    flags[fv].append('%s verborgen %s (%d,%d)' % (n, str(b.get('item')).replace('ITEM_', ''), b['x'], b['y']))
                if str(b.get('item', '')).startswith('ITEM_TM'):
                    tm_src[b['item']].add('verborgen: %s' % n)
                    if not event_vanilla(n, 'bg_events', b):
                        tm_new.add((b['item'], 'verborgen: %s' % n))
    stats['items']['item-balls'] = nballs
    stats['items']['verborgen items'] = nhidden
    for fv, where in flags.items():
        items = [w for w in where if ' item ' in w or ' verborgen ' in w]
        if not items or len(where) < 2:
            continue
        # objecten op dezelfde kaart met dezelfde flag (bijv. twee varianten van één NPC) zijn geen item-probleem
        maps_ = {w.split(' ')[0] for w in where}
        name = fv if not isinstance(fv, int) else '0x%X' % fv
        names = [nm for nm, e in FLAG_DEFS.items() if isinstance(fv, int) and FLAG(nm) == fv and not RANGE_NAME.search(nm)][:3]
        sev = 'FOUT' if any(map_changed(m) for m in maps_ if m in MAPS) else 'VANILLA'
        add('items', sev, 'dupflag:%s' % name, 'flag %s (%s) gedeeld door: %s' % (name, ', '.join(names), '; '.join(where)))
    # TM's: rewards, winkels, C-code
    for f, ls in FILELINES.items():
        inmart = False
        basetext = base_file(f) if changed_since_base(f) else None
        for l in ls:
            s = l.split('@')[0].strip()
            if re.match(r'^(pokemart|pokemartdecoration)\b', s) or re.match(r'^\w+_Pokemart\w*::?$', s):
                inmart = True
            if s.startswith('pokemartlistend') or s == 'end' or s == 'return':
                inmart = False
            for tm in re.findall(r'\bITEM_TM_\w+', s):
                c = s.split()[0]
                src = None
                if c == '.2byte' and inmart:
                    src = 'winkel: %s' % (f.split('/')[-2] if f.startswith('data/maps/') else f)
                elif c in ('giveitem', 'finditem', 'additem', 'giveitem_msg', 'setvar') or c.startswith('giveitem'):
                    src = 'script: %s' % (f.split('/')[-2] if f.startswith('data/maps/') else f)
                if src:
                    tm_src[tm].add(src)
                    if basetext is not None and l.strip() not in basetext:
                        tm_new.add((tm, src))
    for f in glob.glob('src/**/*.c', recursive=True) + glob.glob('src/data/**/*.h', recursive=True):
        if f.endswith(('items.h', 'tmhm.h')) or 'learnset' in f or 'pokemon/' in f or 'trainers' in f:
            continue
        code = re.sub(r'/\*.*?\*/|//[^\n]*', '', read(f), flags=re.S)
        for tm in set(re.findall(r'\bITEM_TM_\w+', code)):
            tm_src[tm].add('C: %s' % f)
            if changed_since_base(f) and tm not in re.sub(r'/\*.*?\*/|//[^\n]*', '', base_file(f), flags=re.S):
                tm_new.add((tm, 'C: %s' % f))
    ntm = 0
    for tm, srcs in sorted(tm_src.items()):
        ntm += 1
        places = {s.split(': ', 1)[1] for s in srcs}
        if len(srcs) > 1:
            # dezelfde TM binnen één kaart (bijv. script-beloning + additem) telt één keer
            if len(places) == 1:
                continue
            new = [x for x in sorted(srcs) if (tm, x) in tm_new]
            add('items', 'MELD' if new else 'VANILLA', 'tm:%s' % tm, '%s komt op meer plekken voor: %s' % (
                tm, '; '.join(x + (' (nieuw)' if (tm, x) in tm_new else '') for x in sorted(srcs))))
    stats['items']["TM's"] = ntm


# ------------------------------------------------------------------ hoofdprogramma
CHECKS = {'warps': check_warps, 'kaarten': check_maps, 'scripts': check_scripts, 'flags': check_flags,
          'trainers': check_trainers, 'wild': check_wild, 'items': check_items}
TITLES = {'warps': 'Warps', 'kaarten': 'Kaarten en objecten', 'scripts': 'Scripts en teksten', 'flags': 'Flags en vars',
          'trainers': 'Trainers', 'wild': 'Wilde encounters', 'items': 'Items en TM\'s'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', '--verbose', action='store_true')
    ap.add_argument('--md')
    ap.add_argument('--only')
    ap.add_argument('--vanilla', action='store_true', help='ook VANILLA-bevindingen tonen')
    a = ap.parse_args()
    cats = a.only.split(',') if a.only else CATS
    for c in cats:
        CHECKS[c]()
    print('Audit Project Grounded')
    for c in cats:
        cnt = collections.Counter(f[1] for f in findings if f[0] == c)
        st = ', '.join('%s %d' % kv for kv in stats[c].items())
        print('  %-9s FOUT %3d  MELD %3d  INFO %3d  (vanilla %d)   [%s]' % (c, cnt['FOUT'], cnt['MELD'], cnt['INFO'], cnt['VANILLA'], st))
        if a.verbose:
            for f in findings:
                if f[0] == c and (f[1] != 'VANILLA' or a.vanilla):
                    print('     %-5s %s   [%s]' % (f[1], f[3], f[2]))
    if a.md:
        out = ['# Audit Project Grounded', '',
               'Gegenereerd met `python3 tools/grounded/audit.py --md AUDIT.md` (statisch, zonder emulator). '
               'FOUT = vrijwel zeker een bug, MELD = even naar kijken / ontwerpkeuze, INFO = ter informatie. '
               'Bevindingen op kaarten/teksten die sinds vanilla niet veranderd zijn, staan er niet in. '
               'Bewust negeren: de sleutel tussen [ ] in `IGNORE` in het script zetten.', '']
        out.append('| Categorie | FOUT | MELD | INFO | tellingen |')
        out.append('|---|---|---|---|---|')
        for c in cats:
            cnt = collections.Counter(f[1] for f in findings if f[0] == c)
            out.append('| %s | %d | %d | %d | %s |' % (TITLES[c], cnt['FOUT'], cnt['MELD'], cnt['INFO'],
                                                    ', '.join('%s %d' % kv for kv in stats[c].items())))
        for c in cats:
            fs = [f for f in findings if f[0] == c and f[1] != 'VANILLA']
            out += ['', '## ' + TITLES[c], '']
            if not fs:
                out.append('Niets open.')
            for sev in ('FOUT', 'MELD', 'INFO'):
                sub = [f for f in fs if f[1] == sev]
                if not sub:
                    continue
                if sev == 'INFO' and len(sub) > 60:
                    out.append('- **INFO** (%d stuks, eerste 60):' % len(sub))
                    sub = sub[:60]
                for f in sub:
                    out.append('- **%s** %s `[%s]`' % (sev, f[3], f[2]))
            if c == 'trainers' and FREE_IDS:
                out += ['', 'Vrije trainer-id\'s (%d): %s' % (len(FREE_IDS), compress(FREE_IDS))]
        if not a.only:
            out += ['', '## Handmatige controle', ''] + ['- ' + m for m in MANUAL]
        open(a.md, 'w').write('\n'.join(out) + '\n')
        print('-> %s' % a.md)
    return 1 if any(f[1] == 'FOUT' for f in findings) else 0


def compress(ids):
    out, s = [], None
    for i, v in enumerate(ids):
        if s is None:
            s = v
        if i + 1 == len(ids) or ids[i + 1] != v + 1:
            out.append(str(s) if s == v else '%d-%d' % (s, v))
            s = None
    return ', '.join(out)


if __name__ == '__main__':
    sys.exit(main())
