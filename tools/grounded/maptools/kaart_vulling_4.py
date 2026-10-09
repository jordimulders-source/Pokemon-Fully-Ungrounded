"""Project Grounded: kaartvulling 4 ("eerst de basale map klaar met vulling", 8 okt).

Vult de leegste kaarten uit de kaartaudit:
- Wilde Pokémon in grotten/dungeons die nog niets hadden (behalve legendary-holen), Mt. Chimney (aspatches),
  de zijkamers van Victory Road, de hideouts (water), het Abandoned Ship en het Ghost Ship.
- Items en verborgen items in lege grotten en kamers.
- Extra inhoud: Granite Cave (spelonkgids + trainer), Shoal Cave (getijdenwachter, een zwemmer die er alleen bij
  vloed is, een gevecht in de ijsgrot, een item dat alleen bij eb droog ligt), Seafloor Cavern en Cave of Origin
  (sporen van Team Aqua/Magma, trainers), en NPC's/trainers/items op Shipwreck Shoals, de Safari-zones,
  Nothing Island en Route 124.

Idempotent: eigen objecten/bg-events (herkend aan script- en flagnamen met KV4), de gemarkeerde blokken in
scripts.inc, flags.h, opponents.h en trainers.party, de eigen encountertabellen en de map.bin-cellen (oude waarden
in kaart_vulling_4_orig.json) worden eerst teruggezet en dan opnieuw geschreven.
Controleert bereikbaarheid (lopen en surfen vanaf alle warps; objecten zijn muren), tekstbreedte, soortnamen en
de 12-unieke-soorten-regel.
Flags: FLAG_GROUNDED(200)-(329). Trainer-id's: 1150-1169.
Gebruik (vanuit de repo-root): python3 tools/grounded/maptools/kaart_vulling_4.py
Verkennen: python3 tools/grounded/maptools/kaart_vulling_4.py --probe <Kaart> [--nosurf]
"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
# Levels: de levelcurve (v0.9.192) is leidend. check_levels zet bij het afsluiten de levels van
# bestaande trainers/wilde slots/setwildbattles terug naar de stand vóór dit script; alleen nieuwe
# entries krijgen de levels hieronder. Bewust een level wijzigen: GROUNDED_SCRIPT_LEVELS=1.
import check_levels  # noqa: E402
check_levels.protect()
import json, os, re, struct, sys
from collections import deque

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from landlib import Kaart, WATER, LEDGE, NOPLACE, check_text, _LAYOUTS  # noqa: E402

TAG = 'KV4'
MARK = '@ --- kaart_vulling_4 (gegenereerd door tools/grounded/maptools/kaart_vulling_4.py) ---'
MARK_END = '@ --- einde kaart_vulling_4 ---'
ORIG_PATH = 'tools/grounded/maptools/kaart_vulling_4_orig.json'
ORIG = json.load(open(ORIG_PATH)) if os.path.exists(ORIG_PATH) else {}
FAIL = []
TEXTS = []
REPORT = []   # (kaart, wat)


def note(mapname, s):
    REPORT.append((mapname, s))


# =====================================================================================================
# kaarten: laden met teruggezette map.bin-cellen, bereikbaarheid
def load(name):
    k = Kaart(name)
    L = _LAYOUTS[k.d['layout']]
    v = list(k.v)
    for key, c in ORIG.get(L['name'], {}).items():  # alles wat dit script ooit overschreef terugzetten
        x, y = map(int, key.split(','))
        v[y * k.w + x] = c
    k.v = v
    k.layout = L
    return k


def set_cell(k, x, y, mt):
    orig = ORIG.setdefault(k.layout['name'], {})
    i = y * k.w + x
    orig.setdefault('%d,%d' % (x, y), k.v[i])
    k.v[i] = (k.v[i] & ~0x3FF) | mt


def save_bin(k):
    open(k.layout['blockdata_filepath'], 'wb').write(struct.pack('<%dH' % len(k.v), *k.v))
    json.dump(ORIG, open(ORIG_PATH, 'w'), indent=0, sort_keys=True)  # meteen, zodat een afgebroken run niets kwijtraakt


def starts(k):
    out = []
    for w in k.d['warp_events']:
        p = (w['x'], w['y'])
        if not k.blocked(*p):
            out.append(p)
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            q = (p[0] + dx, p[1] + dy)
            if 0 <= q[0] < k.w and 0 <= q[1] < k.h and not k.blocked(*q):
                out.append(q)
    if k.d.get('connections'):  # verbonden kaarten: elke vrije randtegel aan een verbonden kant is een ingang
        sides = {c['direction'] for c in k.d['connections']}
        for x in range(k.w):
            for y in range(k.h):
                edge = ((y == 0 and 'up' in sides) or (y == k.h - 1 and 'down' in sides)
                        or (x == 0 and 'left' in sides) or (x == k.w - 1 and 'right' in sides))
                if edge and not k.blocked(x, y) and k.beh(x, y) not in LEDGE:
                    out.append((x, y))
    return out


def reach(k, solid=(), surf=True, extra_starts=()):
    """Lopen + surfen vanaf alle warps. Hoogte: gelijk, 0/15, of de overgang land<->water."""
    solid = set(solid)
    seen = {}
    q = deque()
    for s in list(starts(k)) + list(extra_starts):
        if s not in seen and s not in solid:
            seen[s] = k.elev(*s); q.append(s)
    while q:
        x, y = q.popleft()
        ze = seen[(x, y)]
        zw = k.beh(x, y) in WATER
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p in seen or not (0 <= p[0] < k.w and 0 <= p[1] < k.h): continue
            if k.blocked(*p) or p in solid: continue
            b = k.beh(*p)
            if b in LEDGE: continue
            pw = b in WATER
            if pw and not surf: continue
            e = k.elev(*p)
            if not (e in (0, 15) or ze in (0, 15) or e == ze or pw != zw): continue
            seen[p] = ze if e == 15 else e
            q.append(p)
    return seen


def probe(name, surf=True, layout=None):
    k = load(name)
    if layout:
        L = _LAYOUTS[layout]
        k.v = list(struct.unpack('<%dH' % (k.w * k.h), open(L['blockdata_filepath'], 'rb').read()))
    r = reach(k, surf=surf)
    ev = {}
    for o in k.d['object_events']:
        ev[(o['x'], o['y'])] = 'i' if 'ITEM_BALL' in o['graphics_id'] else 'O'
    for b in k.d['bg_events']:
        ev[(b['x'], b['y'])] = 'h' if b['type'] == 'hidden_item' else 'b'
    for w in k.d['warp_events']:
        ev[(w['x'], w['y'])] = 'W'
    print('==', name, k.w, k.h)
    for o in k.d['object_events']:
        print('  obj %2d,%2d %-22s %s' % (o['x'], o['y'], o['graphics_id'][14:], o['script'][-40:]))
    print('    ' + ''.join(str(x // 10 % 10) for x in range(k.w)))
    print('    ' + ''.join(str(x % 10) for x in range(k.w)))
    for y in range(k.h):
        row = ''
        for x in range(k.w):
            b = k.beh(x, y)
            if (x, y) in ev: ch = ev[(x, y)]
            elif (x, y) in r: ch = '~' if b in WATER else ('g' if b in ('MB_TALL_GRASS', 'MB_LONG_GRASS', 'MB_ASHGRASS') else ('s' if b == 'MB_SAND' else '.'))
            elif k.blocked(x, y): ch = '#'
            elif b in WATER: ch = '='
            else: ch = '%x' % k.elev(x, y)
            row += ch
        print('%3d ' % y + row)


if __name__ == '__main__' and len(sys.argv) > 2 and sys.argv[1] == '--probe':
    lay = [a[9:] for a in sys.argv if a.startswith('--layout=')]
    probe(sys.argv[2], surf='--nosurf' not in sys.argv, layout=lay[0] if lay else None)
    sys.exit(0)


# =====================================================================================================
# geldige namen
SPECIES = set(re.findall(r'#define SPECIES_(\w+)', open('include/constants/species.h').read()))
ITEMS = set(re.findall(r'#define (ITEM_\w+)', open('include/constants/items.h').read()))
GFX = set(re.findall(r'#define (OBJ_EVENT_GFX_\w+)', open('include/constants/event_objects.h').read()))
EVO = {}  # soort -> laagste level waarop hij in dit project per level evolueert
for _f in os.listdir('src/data/pokemon/species_info'):
    _s = open('src/data/pokemon/species_info/' + _f).read()
    for _m in re.finditer(r'\n    \[SPECIES_(\w+)\]\s*=(.*?)(?=\n    \[SPECIES_|\Z)', _s, re.S):
        _lv = [int(x) for x in re.findall(r'\{EVO_LEVEL\w*, (\d+), SPECIES_', _m.group(2)) if int(x) > 0]
        if _lv:
            EVO[_m.group(1)] = min(_lv)
EVO_OK = {('BAGON', 'gMeteorFalls_DraconidShrine')}  # bewust: "hier komen alleen Bagon" (lv 27-29, evolueert op 30)

# =====================================================================================================
# flags (FLAG_GROUNDED 200-329)
FLAGS_H = 'include/constants/flags.h'
FLAG_FIRST, FLAG_LAST = 200, 329
FLAGS = []  # (naam, omschrijving)


def flag(name, desc):
    assert name not in [f[0] for f in FLAGS], name
    FLAGS.append((name, desc))
    assert FLAG_FIRST + len(FLAGS) - 1 <= FLAG_LAST, 'flags op'
    return name


def write_flags():
    s = open(FLAGS_H).read()
    mm = re.search(r'// kaart_vulling_4 \{.*?\n// \}\n', s, flags=re.S)
    at = mm.start() if mm else None  # bestaand blok op zijn plek vervangen
    s = re.sub(r'// kaart_vulling_4 \{.*?\n// \}\n', '', s, flags=re.S)
    for name, _ in FLAGS:
        assert not re.search(r'#define %s\b' % name, s), 'vlag %s bestaat al' % name
    used = {int(n) for n in re.findall(r'#define \w+\s+FLAG_GROUNDED\((\d+)\)', s)}
    block = '// kaart_vulling_4 { (tools/grounded/maptools/kaart_vulling_4.py; FLAG_GROUNDED %d-%d)\n' % (FLAG_FIRST, FLAG_LAST)
    for i, (name, desc) in enumerate(FLAGS):
        assert FLAG_FIRST + i not in used, 'FLAG_GROUNDED(%d) is al in gebruik' % (FLAG_FIRST + i)
        block += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded (kaartvulling 4): %s\n' % (name, FLAG_FIRST + i, desc)
    block += '// }\n'
    anchor = '\n// Special Flags'
    if at is not None:
        s = s[:at] + block + s[at:]
    else:
        s = s.replace(anchor, '\n' + block + anchor, 1)
    s = s.replace('100-149 vuurtoren/Dragon Island, 150+ vrij.',
                  '100-149 vuurtoren/Dragon Island, 200-329 kaartvulling 4 (kaart_vulling_4.py), 150-199 en 330+ vrij.')
    s = re.sub(r'\n{3,}// kaart_vulling_4 \{', '\n\n// kaart_vulling_4 {', s)
    open(FLAGS_H, 'w').write(s)


# =====================================================================================================
# trainers (1150-1169)
TRAINERS = []
TBEGIN, TEND = '/* --- kaart_vulling_4 (gegenereerd door tools/grounded/maptools/kaart_vulling_4.py) --- */', '/* --- einde kaart_vulling_4 --- */'
FIRST_ID, LAST_ID = 1150, 1169


def team(level, ivs, *mons):
    out = []
    for m in mons:
        m = (m,) if isinstance(m, str) else tuple(m)
        sp, d = m[0], (m[1] if len(m) > 1 else 0)
        moves = m[2] if len(m) > 2 else []
        item = m[3] if len(m) > 3 else None
        s = sp + (' @ ' + item if item else '') + '\nLevel: %d\nIVs: %d HP / %d Atk / %d Def / %d SpA / %d SpD / %d Spe' % (
            (level + d,) + (ivs,) * 6)
        for mv in moves:
            s += '\n- ' + mv
        out.append(s)
    return '\n\n'.join(out)


def new_trainer(const, desc, name, cls, pic, gender, music, mons_text, double=False):
    tid = FIRST_ID + len(TRAINERS)
    assert tid <= LAST_ID
    hdr = 'Name: %s\nClass: %s\nPic: %s\nGender: %s\nMusic: %s\nDouble Battle: %s\nAI: Check Bad Move / Try To Faint' % (
        name, cls, pic, gender, music, 'Yes' if double else 'No')
    TRAINERS.append((const, tid, desc, '=== %s ===\n%s\n\n%s' % (const, hdr, mons_text.strip())))
    return const


def write_trainers():
    op = open('include/constants/opponents.h').read()
    mm = re.search(r'\n// kaart_vulling_4 \{\n.*?// \}\n', op, flags=re.S)
    KV4_AT = mm.start() + 1 if mm else None
    op = re.sub(r'\n// kaart_vulling_4 \{\n.*?// \}\n', '\n', op, flags=re.S)
    for c, i, _, _ in TRAINERS:
        assert not re.search(r'#define %s\b' % c, op), c
        assert not re.search(r'#define TRAINER_\w+\s+%d\b' % i, op), 'trainer-id %d al in gebruik' % i
    block = '// kaart_vulling_4 {\n' + ''.join('#define %-35s %d // Project Grounded (kaartvulling 4): %s\n' % (c, i, d)
                                              for c, i, d, _ in TRAINERS) + '// }\n'
    m = re.search(r'\n(#define TRAINERS_COUNT\s+)(\d+)', op)
    assert int(m.group(2)) > LAST_ID
    if KV4_AT is not None:  # op zijn plek vervangen
        op = op[:KV4_AT] + block + op[KV4_AT:]
    else:
        op = op[:m.start()] + '\n' + block + op[m.start():]
        op = re.sub(r'\n{3,}(// kaart_vulling_4 \{)', r'\n\n\1', op)
        op = re.sub(r'(// kaart_vulling_4 \{.*?// \}\n)\n*(#define TRAINERS_COUNT)', r'\1\n\2', op, flags=re.S)
    open('include/constants/opponents.h', 'w').write(op)
    p = open('src/data/trainers.party').read()
    new = TBEGIN + '\n\n' + '\n\n'.join(t[3] for t in TRAINERS) + '\n\n' + TEND
    if TBEGIN in p:  # op zijn plek vervangen (geen blokken naar achteren schuiven)
        p = p[:p.index(TBEGIN)] + new + p[p.index(TEND) + len(TEND):]
    else:
        p = p.rstrip('\n') + '\n\n' + new + '\n'
    open('src/data/trainers.party', 'w').write(p)


# =====================================================================================================
# wild_encounters.json (tekstueel)
WILD = 'src/data/wild_encounters.json'
WTEXT = [open(WILD).read()]
LAND_N, WATER_N, FISH_N = 12, 5, 10
ROD = [(0, 2), (2, 5), (5, 10)]  # old/good/super rod-slots
TABLES = []


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
    return start, j + 1


def _mons(lst, ind):
    return ',\n'.join('%s{ "min_level": %d, "max_level": %d, "species": "SPECIES_%s" }' % (ind, a, b, sp) for sp, a, b in lst)


def check_mons(label, lst, n, groups=None):
    assert len(lst) == n, (label, len(lst))
    for g0, g1 in (groups or [(0, n)]):
        sp = [m[0] for m in lst[g0:g1]]
        assert len(set(sp)) == len(sp), '%s: dubbele soort %s' % (label, sp)
    for sp, a, b in lst:
        assert sp in SPECIES, '%s: onbekende soort %s' % (label, sp)
        assert a <= b, (label, sp)
        if sp in EVO and b >= EVO[sp] and (sp, label) not in EVO_OK:
            print('%s: %s lv %d-%d had al geevolueerd kunnen zijn (lv %d)' % (label, sp, a, b, EVO[sp])); FAIL.append(label)


def table(mapname, land=None, water=None, fish=None, land_rate=10, water_rate=4, fish_rate=10, why=''):
    """Nieuwe encountertabel (of de vorige versie van dit script vervangen)."""
    k = json.load(open('data/maps/%s/map.json' % mapname))
    mapconst = k['id']
    label = 'g' + mapname
    parts = []
    ind = '              '
    if land:
        check_mons(label, land, LAND_N)
        parts.append('"land_mons": {\n            "encounter_rate": %d,\n            "mons": [\n%s\n            ]\n          }' % (land_rate, _mons(land, ind)))
    if water:
        check_mons(label, water, WATER_N)
        parts.append('"water_mons": {\n            "encounter_rate": %d,\n            "mons": [\n%s\n            ]\n          }' % (water_rate, _mons(water, ind)))
    if fish:
        check_mons(label, fish, FISH_N, ROD)
        parts.append('"fishing_mons": {\n            "encounter_rate": %d,\n            "mons": [\n%s\n            ]\n          }' % (fish_rate, _mons(fish, ind)))
    blk = '{\n          "map": "%s",\n          "base_label": "%s",\n          %s\n        }' % (mapconst, label, ',\n          '.join(parts))
    s = WTEXT[0]
    if '"base_label": "%s"' % label in s:
        a, b = _block(label)
        assert ('"map": "%s"' % mapconst) in s[a:b]
        WTEXT[0] = s[:a] + blk + s[b:]
    else:
        assert ('"map": "%s"' % mapconst) not in s, '%s heeft al een andere tabel' % mapname
        a, b = _block('gSkyPillar_1F')
        WTEXT[0] = s[:b] + ',\n        ' + blk + s[b:]
    TABLES.append(mapname)
    kinds = [n for n, t in (('land', land), ('surf', water), ('vissen', fish)) if t]
    note(mapname, 'encounters (%s): %s' % ('/'.join(kinds), why))


# =====================================================================================================
# events
def T(label, s):
    TEXTS.append((label, s))
    return '%s:\n\t.string "%s$"\n\n' % (label, s)


def talk(label, body):
    return '%s::\n%s\n\n' % (label, body.strip('\n'))


class Ev:
    """Verzamelt objecten, bg-events en scripts voor één kaart."""

    def __init__(self, mapname, surf=True, shallow=False):
        self.k = load(mapname)
        self.noplace = WATER if shallow else NOPLACE  # shallow: zandbanken (Shipwreck Shoals) mogen
        self.name = mapname
        self.P = '%s_EventScript_%s' % (mapname, TAG)
        self.Q = '%s_Text_%s' % (mapname, TAG)
        self.objs, self.bgs, self.scr, self.surf = [], [], '', surf
        self.items = []
        self.people = []

    def _o(self, gfx, x, y, script, move='MOVEMENT_TYPE_FACE_DOWN', trainer=False, sight=0, fl='0', item=None, water=False):
        assert gfx in GFX, gfx
        o = {'graphics_id': gfx, 'x': x, 'y': y, 'elevation': 3, 'movement_type': move,
             'movement_range_x': 0, 'movement_range_y': 0,
             'trainer_type': 'TRAINER_TYPE_NORMAL' if trainer else 'TRAINER_TYPE_NONE',
             'trainer_sight_or_berry_tree_id': item or str(sight), 'script': script, 'flag': fl}
        if water:
            o['_water'] = True
        self.objs.append(o)
        return o

    def ball(self, x, y, item, desc=''):
        assert item in ITEMS, item
        f = flag('FLAG_ITEM_%s_%s_%s' % (TAG, self.name.upper(), item[5:]), '%s: %s %s' % (self.name, item[5:], desc))
        self._o('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', 'MOVEMENT_TYPE_LOOK_AROUND', fl=f, item=item)
        self.items.append(item[5:].replace('_', ' ').title())

    def hidden(self, x, y, item, desc=''):
        assert item in ITEMS, item
        f = flag('FLAG_HIDDEN_ITEM_%s_%s_%s' % (TAG, self.name.upper(), item[5:]), '%s: verborgen %s %s' % (self.name, item[5:], desc))
        self.bgs.append({'type': 'hidden_item', 'x': x, 'y': y, 'elevation': 3, 'item': item, 'flag': f})
        self.items.append(item[5:].replace('_', ' ').title() + ' (verborgen)')

    def sign(self, x, y, name, s):
        self.bgs.append({'type': 'sign', 'x': x, 'y': y, 'elevation': 3, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
                         'script': self.P + name})
        self.scr += talk(self.P + name, '\tmsgbox %s, MSGBOX_SIGN\n\tend' % (self.Q + name)) + T(self.Q + name, s)

    def npc(self, gfx, x, y, name, s, move='MOVEMENT_TYPE_FACE_DOWN', who=None, fl='0'):
        self._o(gfx, x, y, self.P + name, move, fl=fl)
        self.scr += talk(self.P + name, '\tmsgbox %s, MSGBOX_NPC\n\tend' % (self.Q + name)) + T(self.Q + name, s)
        self.people.append(who or name)

    def npc_script(self, gfx, x, y, name, body, texts, move='MOVEMENT_TYPE_FACE_DOWN', who=None, fl='0', water=False):
        """Eigen script; in body staan %(P)s (scriptlabel) en %(Q)s (tekstlabel)."""
        self._o(gfx, x, y, self.P + name, move, fl=fl, water=water)
        self.scr += talk(self.P + name, body % {'P': self.P + name, 'Q': self.Q + name})
        for suf, s in texts.items():
            self.scr += T(self.Q + name + suf, s)
        if who != '':
            self.people.append(who or name)

    def gift(self, gfx, x, y, name, item, s, after, move='MOVEMENT_TYPE_FACE_DOWN', who=None):
        assert item in ITEMS, item
        f = flag('FLAG_%s_%s_GIFT_%s' % (TAG, self.name.upper(), name.upper()), '%s: cadeau van %s (%s)' % (self.name, name, item[5:]))
        self.npc_script(gfx, x, y, name, '''
	lock
	faceplayer
	goto_if_set %s, %%(P)s_After
	msgbox %%(Q)s, MSGBOX_DEFAULT
	giveitem %s
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag %s
	release
	end
%%(P)s_After:
	msgbox %%(Q)s_After, MSGBOX_DEFAULT
	release
	end''' % (f, item, f), {'': s, '_After': after}, move, who=who)
        self.items.append(item[5:].replace('_', ' ').title() + ' (cadeau)')

    def trainer(self, gfx, x, y, name, tconst, sight, intro, defeat, post, move='MOVEMENT_TYPE_FACE_DOWN', who=None, fl='0', water=False):
        t = self.Q + name
        self._o(gfx, x, y, self.P + name, move, trainer=True, sight=sight, fl=fl, water=water)
        self.scr += (talk(self.P + name, '\ttrainerbattle_single %s, %s_Intro, %s_Defeat\n\tmsgbox %s_Post, MSGBOX_AUTOCLOSE\n\tend'
                          % (tconst, t, t, t)) + T(t + '_Intro', intro) + T(t + '_Defeat', defeat) + T(t + '_Post', post))
        self.people.append(who or name)

    def finish(self, need=()):
        k = self.k
        ev = k.event_tiles()
        others = [o for o in k.d['object_events'] if TAG not in o['script'] and TAG not in o['flag']]
        other_bg = [b for b in k.d['bg_events'] if TAG not in b.get('script', '') and TAG not in b.get('flag', '')]
        old_solid = {(o['x'], o['y']) for o in others if 'ITEM_BALL' not in o['graphics_id']}
        old_all = {(o['x'], o['y']) for o in others} | {(b['x'], b['y']) for b in other_bg}
        solid = set()
        for o in self.objs:
            p = (o['x'], o['y'])
            assert 0 <= p[0] < k.w and 0 <= p[1] < k.h, (self.name, p)
            assert not k.blocked(*p), '%s: object op een muur %s (%s)' % (self.name, p, o['script'])
            assert p not in ev, '%s: object op een warp/coord-event %s' % (self.name, p)
            assert o.get('_water') or k.beh(*p) not in self.noplace, '%s: object in het water %s (%s)' % (self.name, p, o['script'])
            assert p not in old_all and p not in solid, '%s: botst met een bestaand event %s' % (self.name, p)
            o['elevation'] = o.get('_elev', 1 if k.beh(*p) in WATER else k.elev(*p))
            if o['script'] != 'Common_EventScript_FindItem':
                solid.add(p)
        for b in self.bgs:
            p = (b['x'], b['y'])
            assert p not in solid and p not in ev and p not in old_all, '%s: bg-event %s' % (self.name, p)
            assert b['type'] == 'sign' or not k.blocked(*p), '%s: verborgen item op een muur %s' % (self.name, p)
            assert b['type'] == 'sign' or k.beh(*p) not in self.noplace, '%s: item in het water %s' % (self.name, p)
            b['elevation'] = k.elev(*p)
        r = reach(k, solid=solid | old_solid, surf=self.surf)
        adj = lambda x, y, R: any((x + dx, y + dy) in R for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        for o in self.objs:
            x, y = o['x'], o['y']
            if o['script'] == 'Common_EventScript_FindItem':
                ok = (x, y) in r or adj(x, y, r)
            else:
                ok = adj(x, y, r)
            if not ok:
                print('%s: object (%d,%d) %s niet bereikbaar' % (self.name, x, y, o['script'])); FAIL.append(self.name)
        for b in self.bgs:
            x, y = b['x'], b['y']
            ok = (x, y) in r if b['type'] == 'hidden_item' else adj(x, y, r)
            if not ok:
                print('%s: bg-event (%d,%d) niet bereikbaar' % (self.name, x, y)); FAIL.append(self.name)
        # wat zonder onze objecten bereikbaar was (warps, bestaande events), moet bereikbaar blijven
        r0 = reach(k, solid=old_solid, surf=self.surf)
        pts = list(need) + [(w['x'], w['y']) for w in k.d['warp_events']] + list(old_all)
        for p in pts:
            if (p in r0 or adj(p[0], p[1], r0)) and not (p in r or adj(p[0], p[1], r)):
                print('%s: %s niet meer bereikbaar door de nieuwe objecten' % (self.name, p)); FAIL.append(self.name)
        self._apply()
        if self.items:
            note(self.name, 'items: ' + ', '.join(self.items))
        if self.people:
            note(self.name, 'NPC/trainer: ' + ', '.join(self.people))

    def _apply(self):
        k = self.k
        m = json.load(open(k.path))
        m['object_events'] = [o for o in m['object_events'] if TAG not in o['script'] and TAG not in o['flag']]
        m['bg_events'] = [b for b in m['bg_events'] if TAG not in b.get('script', '') and TAG not in b.get('flag', '')]
        m['object_events'] += [{kk: vv for kk, vv in o.items() if not kk.startswith('_')} for o in self.objs]
        m['bg_events'] += self.bgs
        os_ = m['object_events']
        for o in os_:
            near = [p for p in os_ if abs(p['x'] - o['x']) <= 12 and abs(p['y'] - o['y']) <= 9]
            if len(near) > 15 and TAG in o['script'] + o['flag']:
                print('%s: te veel objecten rond (%d,%d)' % (self.name, o['x'], o['y'])); FAIL.append(self.name)
        open(k.path, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
        inc_path = 'data/maps/%s/scripts.inc' % self.name
        inc = open(inc_path).read()
        new = (MARK + '\n' + self.scr.strip('\n') + '\n' + MARK_END) if self.scr.strip() else ''
        if MARK in inc and new:  # op zijn plek vervangen
            inc = inc[:inc.index(MARK)] + new + inc[inc.index(MARK_END) + len(MARK_END):]
        elif MARK in inc:
            inc = inc[:inc.index(MARK)].rstrip('\n') + '\n' + inc[inc.index(MARK_END) + len(MARK_END):].lstrip('\n')
        elif new:
            inc = inc.rstrip('\n') + '\n\n' + new + '\n'
        open(inc_path, 'w').write(inc)


def hook(mapname, label, line):
    """Eén regel direct na een label in scripts.inc (buiten ons blok); idempotent."""
    p = 'data/maps/%s/scripts.inc' % mapname
    s = open(p).read()
    if '%s:\n%s\n' % (label, line) in s:
        return
    assert ('%s:\n' % label) in s, (mapname, label)
    s = s.replace('%s:\n' % label, '%s:\n%s\n' % (label, line), 1)
    open(p, 'w').write(s)


# =====================================================================================================
# =====================================================================================================
# 1. WILDE POKEMON
# =====================================================================================================
# Grotten/dungeons die nog geen wilde Pokémon hadden. Bewust leeg gelaten: legendary-holen (Regi-grotten, Terra/
# Marine Cave, Sealed Chamber, Sea Temple, Entei-/Raikou-/Heatran-hol, Crystal Cavity = Route136_Grotto, de
# Ogerpon-holen (Ember Hollow, Cornerstone Room, Wellspring Grotto), Steam Island, Whirl Island, Navel Rock-top/
# -bodem, omgekeerde Sky Pillar B3F, Darkrai/Genesect), Sky Pillar 2F/4F (geen encountertegels: barstvloer-
# puzzel, zoals vanilla), kapiteinshutten, schepen van Team Plasma, de Kubfu-torens en kaarten zonder
# encountertegels of met onbereikbaar water (Aqua Hideout B1F, Rocket Hideout).

table('SeafloorCavern_Room9',
      land=[('CRAWDAUNT', 44, 46), ('BARBARACLE', 44, 46), ('CRUSTLE', 45, 47), ('GRAPPLOCT', 45, 47),
            ('KINGLER', 45, 47), ('DRAPION', 45, 47), ('KABUTOPS', 46, 48), ('OMASTAR', 46, 48),
            ('PROBOPASS', 47, 49), ('SKUNTANK', 47, 49), ('GOLISOPOD', 50, 50), ('CLAWITZER', 50, 50)],
      water=[('TENTACRUEL', 40, 45), ('SHARPEDO', 40, 45), ('HUNTAIL', 42, 46), ('GOREBYSS', 42, 46), ('WAILORD', 45, 50)],
      land_rate=4, why='diepzeegrot: kreeften, fossielen, gif/duister (Fighting/Dark/Steel ondervertegenwoordigd)')

table('CaveOfOrigin_B1F',
      land=[('AUDINO', 48, 50), ('LICKILICKY', 48, 50), ('GRANBULL', 49, 51), ('KOMALA', 49, 51),
            ('WIGGLYTUFF', 50, 52), ('SLURPUFF', 50, 52), ('TOGEKISS', 51, 53), ('KLEFKI', 51, 53),
            ('BLISSEY', 52, 54), ('SYLVEON', 52, 54), ('GRIMMSNARL', 55, 55), ('TINKATON', 55, 55)],
      land_rate=4, why='"oorsprong van het leven": Normal/Fairy zoals 1F; Komala (had geen plek), Klefki/Snubbull/Swirlix-lijn (1 plek)')

table('SkyPillar_Entrance',
      land=[('BOLDORE', 34, 36), ('GRAVELER', 34, 36), ('PROBOPASS', 35, 37), ('SANDSLASH', 35, 37),
            ('GLIGAR', 35, 37), ('SKARMORY', 35, 37), ('SABLEYE', 36, 38), ('LAIRON', 35, 36),
            ('HIPPOWDON', 37, 39), ('CRUSTLE', 37, 39), ('DURANT', 38, 38), ('DRUDDIGON', 38, 38)],
      why='rotsige voorhal onder de toren; Durant (1 plek) als 1%')

table('VictoryRoad_SharkDen',
      land=[('GABITE', 42, 44), ('KROOKODILE', 42, 44), ('HIPPOWDON', 43, 45), ('DUGTRIO', 43, 45),
            ('SANDACONDA', 43, 45), ('FLYGON', 43, 45), ('PUPITAR', 44, 46), ('GLISCOR', 44, 46),
            ('COPPERAJAH', 45, 47), ('EXCADRILL', 45, 47), ('GARCHOMP', 48, 48), ('HAXORUS', 48, 48)],
      why='het hol van de Garchomp: grondhaaien en zandgravers')

table('VictoryRoad_Hermit',
      land=[('RATICATE', 42, 44), ('RATICATE_ALOLA', 42, 44), ('WATCHOG', 42, 44), ('FURRET', 43, 45),
            ('LINOONE', 43, 45), ('GREEDENT', 43, 45), ('BIBAREL', 44, 46), ('DIGGERSBY', 44, 46),
            ('GUMSHOOS', 45, 47), ('MAUSHOLD', 45, 47), ('PERSIAN', 47, 47), ('DUDUNSPARCE', 48, 48)],
      why='Reginalds huisgenoten: knaagdieren (Rattata/Alola-Rattata hadden geen wilde plek; Normal ondervertegenwoordigd)')

table('VictoryRoad_Vault',
      land=[('GOLEM', 43, 45), ('COALOSSAL', 43, 45), ('GARGANACL', 43, 45), ('SUDOWOODO', 44, 46),
            ('CARBINK', 44, 46), ('PROBOPASS', 44, 46), ('KLAWF', 45, 47), ('STONJOURNER', 45, 47),
            ('CRUSTLE', 46, 48), ('GIMMIGHOUL', 46, 48), ('GOLEM_ALOLA', 48, 48), ('GHOLDENGO', 50, 50)],
      why='de kluis van Hiker Gordon: stenen en een schatkist-Gimmighoul (Gholdengo 1%)')

table('VictoryRoad_WaitingRoom',
      land=[('DUSCLOPS', 43, 45), ('KOMALA', 43, 45), ('SLOWBRO', 44, 46), ('HOUNDSTONE', 44, 46),
            ('POLTEAGEIST', 44, 46), ('SLAKING', 44, 46), ('COFAGRIGUS', 45, 47), ('SNORLAX', 45, 47),
            ('TREVENANT', 46, 48), ('BRONZONG', 46, 48), ('SPIRITOMB', 48, 48), ('DUSKNOIR', 48, 48)],
      why='31 jaar wachten: slapers, trage soorten en de geesten van wie het niet haalde')

table('AquaHideout_1F',
      water=[('TENTACRUEL', 32, 36), ('SHARPEDO', 32, 36), ('ARAQUANID', 33, 37), ('LANTURN', 35, 38), ('BRUXISH', 38, 38)],
      fish=[('TENTACOOL', 20, 25), ('CARVANHA', 20, 25),
            ('CHINCHOU', 22, 26), ('QWILFISH', 24, 28), ('REMORAID', 22, 24),
            ('SHARPEDO', 30, 35), ('TENTACRUEL', 30, 35), ('LANTURN', 32, 36), ('OCTILLERY', 32, 36), ('BRUXISH', 36, 38)],
      why='het binnenwater bij de ingang: Team Aqua houdt Sharpedo en kwallen')

table('AquaHideout_B2F',
      water=[('SHARPEDO', 34, 38), ('TENTACRUEL', 34, 38), ('MANTYKE', 34, 38), ('SKRELP', 34, 35), ('MANTINE', 38, 38)],
      fish=[('CHINCHOU', 20, 25), ('REMORAID', 20, 24),
            ('QWILFISH', 22, 26), ('CARVANHA', 22, 26), ('SKRELP', 24, 28),
            ('SHARPEDO', 30, 35), ('OCTILLERY', 32, 36), ('DRAGALGE', 34, 38), ('BARRASKEWDA', 32, 36), ('OVERQWIL', 36, 38)],
      why='de onderzeeërhaven')

_ship1 = [('RATICATE', 26, 28), ('RATICATE_ALOLA', 26, 28), ('HAUNTER', 26, 28), ('SHUPPET', 26, 28),
          ('MAGNEMITE', 27, 29), ('KLANG', 27, 29), ('GRIMER', 27, 29), ('SINISTEA', 27, 29),
          ('PHANTUMP', 27, 29), ('DRIFBLIM', 28, 30), ('MEOWTH', 27, 27), ('MIMIKYU', 30, 30)]
_ship2 = [('RATICATE', 26, 28), ('GRIMER', 26, 28), ('JELLICENT', 28, 30), ('HAUNTER', 26, 28),
          ('SHUPPET', 26, 28), ('DUSKULL', 26, 27), ('TRUBBISH', 26, 27), ('KLANG', 27, 29),
          ('MAREANIE', 28, 30), ('MAGNEMITE', 27, 29), ('SABLEYE', 30, 30), ('CORSOLA_GALAR', 30, 30)]
for _m in ('AbandonedShip_Corridors_1F', 'AbandonedShip_Rooms_1F', 'AbandonedShip_Rooms2_1F'):
    table(_m, land=_ship1, why='scheepsratten (Rattata-lijnen hadden geen plek), spoken, roest; de scheepskat Meowth als 1%')
for _m in ('AbandonedShip_Corridors_B1F', 'AbandonedShip_Room_B1F', 'AbandonedShip_Rooms2_B1F', 'AbandonedShip_HiddenFloorRooms'):
    table(_m, land=_ship2, why='benedendeks: ratten, slib, spoken en Galar-Corsola')

table('GhostShip_Corridors',
      land=[('GENGAR', 48, 50), ('DUSCLOPS', 48, 50), ('BANETTE', 48, 50), ('JELLICENT', 49, 51),
            ('POLTEAGEIST', 49, 51), ('DRIFBLIM', 49, 51), ('COFAGRIGUS', 50, 52), ('MISMAGIUS', 50, 52),
            ('GOLURK', 50, 52), ('DHELMISE', 50, 52), ('MAROWAK_ALOLA', 52, 52), ('SPIRITOMB', 52, 52)],
      why='spookschip: de bemanning die nooit is afgemonsterd')
table('GhostShip_Cabins',
      land=[('DUSCLOPS', 48, 50), ('BANETTE', 48, 50), ('GENGAR', 48, 50), ('POLTEAGEIST', 49, 51),
            ('MISMAGIUS', 49, 51), ('DRIFBLIM', 49, 51), ('COFAGRIGUS', 50, 52), ('TREVENANT', 50, 52),
            ('JELLICENT', 50, 52), ('CHANDELURE', 50, 52), ('MIMIKYU', 52, 52), ('DUSKNOIR', 52, 52)],
      why='spookschip: hutten')

table('MeteorFalls_DraconidShrine',
      land=[('BAGON', 27, 29), ('SHELGON', 32, 34), ('DRAGONAIR', 33, 35), ('FRAXURE', 34, 36),
            ('ZWEILOUS', 35, 37), ('GOOMY', 35, 37), ('HAKAMO_O', 36, 38), ('NOIBAT', 35, 37),
            ('ALTARIA', 36, 38), ('DRUDDIGON', 37, 39), ('DRAKLOAK', 38, 38), ('DRAMPA', 40, 40)],
      why='Selene: "hier komen alleen Bagon en belastinginners". Geen heiligdom zonder wild: het is een woonkamer')

table('ScorchedSlab',
      land=[('SOLROCK', 30, 32), ('CAMERUPT', 30, 32), ('KROKOROK', 30, 32), ('HELIOPTILE', 30, 32),
            ('VIBRAVA', 31, 33), ('SALANDIT', 31, 32), ('SANDSLASH', 31, 33), ('GROWLITHE', 32, 34),
            ('PYROAR', 32, 34), ('CAPSAKID', 32, 34), ('TORKOAL', 34, 34), ('TURTONATOR', 35, 35)],
      water=[('WHISCASH', 30, 33), ('DREDNAW', 30, 33), ('SEAKING', 33, 35), ('ARAQUANID', 34, 36), ('BASCULIN_RED_STRIPED', 36, 36)],
      land_rate=4, why='voorhof van de zonnetempel: zon, zand en vuur; Capsakid (1 plek)')

table('MtChimney',
      land=[('NUMEL', 20, 22), ('SLUGMA', 20, 22), ('TORKOAL', 21, 23), ('VULPIX', 21, 23),
            ('PONYTA', 21, 23), ('LITWICK', 21, 23), ('CARKOL', 22, 24), ('SALANDIT', 22, 24),
            ('HOUNDOUR', 22, 23), ('LITLEO', 23, 25), ('MAGBY', 24, 24), ('LARVESTA', 23, 23)],
      land_rate=20, why='nieuwe asgraspatches op de kraterrand (3 stuks)')

table('MtChimney_Summit',
      land=[('NUMEL', 24, 26), ('SLUGMA', 24, 26), ('TORKOAL', 25, 27), ('SKARMORY', 25, 27),
            ('FEAROW', 25, 27), ('FLETCHINDER', 25, 27), ('HEATMOR', 26, 28), ('SIZZLIPEDE', 26, 27),
            ('CHARCADET', 26, 28), ('GROWLITHE_HISUI', 27, 29), ('MAGMAR', 30, 30), ('TURTONATOR', 29, 29)],
      land_rate=20, why='asgras en kraterbodem op de top (had al asgras, maar geen tabel)')

table('NavelRock_Fork',
      land=[('CROBAT', 55, 57), ('NOCTOWL', 55, 57), ('XATU', 55, 57), ('SIGILYPH', 56, 58),
            ('SKARMORY', 56, 58), ('BRONZONG', 56, 58), ('ALTARIA', 57, 59), ('CLAYDOL', 57, 59),
            ('PIDGEOT', 58, 60), ('HONCHKROW', 58, 60), ('AERODACTYL', 60, 60), ('ARCHEOPS', 60, 60)],
      land_rate=4, why='heilige berg: vogels en oude wachters')
table('NavelRock_Entrance',
      land=[('GOLEM', 54, 56), ('STEELIX', 54, 56), ('CRUSTLE', 55, 57), ('GIGALITH', 55, 57),
            ('EXCADRILL', 55, 57), ('GLISCOR', 55, 57), ('SANDSLASH_ALOLA', 56, 58), ('LYCANROC', 56, 58),
            ('DUGTRIO', 57, 59), ('CARBINK', 57, 59), ('TYRANITAR', 60, 60), ('DRUDDIGON', 60, 60)],
      land_rate=4, why='rotsige ingang van de berg')

# =====================================================================================================
# 2. MT. CHIMNEY: drie asgraspatches (Lavaridge-asgras 0x207 op kraterbodem 0x271)
ASH_FLOOR, ASH_GRASS = 0x271, 0x207
k = load('MtChimney')
keep = k.event_tiles() | {(o['x'], o['y']) for o in k.d['object_events']} | {(b['x'], b['y']) for b in k.d['bg_events']}
n_ash = 0
for (x0, y0, x1, y1) in [(24, 30, 29, 33), (25, 13, 30, 16), (8, 7, 10, 9)]:
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if (k.v[y * k.w + x] & 0x3FF) == ASH_FLOOR and not k.blocked(x, y) and \
                    not any((x + dx, y + dy) in keep for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                set_cell(k, x, y, ASH_GRASS); n_ash += 1
assert n_ash >= 25, n_ash
save_bin(k)
note('MtChimney', '%d asgrastegels in 3 patches' % n_ash)


# =====================================================================================================
# 3. TRAINERS
T_DOUG = new_trainer('TRAINER_KV4_HIKER_DOUG', 'Granite Cave B1F, tekent al 12 jaar een kaart van de grot',
                     'DOUG', 'Hiker', 'Hiker', 'Male', 'Hiker',
                     team(14, 8, 'Roggenrola', 'Nosepass', ('Drilbur', 1)))
T_OLGA = new_trainer('TRAINER_KV4_EXPERT_OLGA', 'Shoal Cave, ijsgrot (alleen bij eb bereikbaar)',
                     'OLGA', 'Expert', 'Expert F', 'Female', 'Intense',
                     team(39, 18, 'Cetitan', 'Frosmoth', 'Beartic', ('Arctozolt', 1)))
T_MAREN = new_trainer('TRAINER_KV4_SWIMMER_MAREN', 'Shoal Cave, binnengrot (alleen bij vloed)',
                      'MAREN', 'Swimmer F', 'Swimmer F', 'Female', 'Swimmer',
                      team(38, 14, 'Floatzel', 'Dewgong', ('Lanturn', 1)))
T_AQUA = new_trainer('TRAINER_KV4_AQUA_GRUNT_SEAFLOOR', 'Seafloor Cavern Room 2, achtergelaten grunt',
                     'GRUNT', 'Team Aqua', 'Aqua Grunt M', 'Male', 'Aqua',
                     team(42, 16, 'Crawdaunt', 'Toxapex', ('Sharpedo', 1)))
T_MAGMA = new_trainer('TRAINER_KV4_MAGMA_GRUNT_ORIGIN', 'Cave of Origin 1F, kwam kijken naar het einde van de wereld',
                      'GRUNT', 'Team Magma', 'Magma Grunt F', 'Female', 'Magma',
                      team(48, 18, 'Camerupt', 'Magcargo', 'Houndoom', ('Torkoal', 1)))
T_BARNABY = new_trainer('TRAINER_KV4_SAILOR_BARNABY', 'Shipwreck Shoals, deserteur van het spookschip',
                        'BARNABY', 'Sailor', 'Sailor', 'Male', 'Suspicious',
                        team(51, 20, 'Golisopod', 'Cursola', 'Dhelmise', ('Basculegion', 1)))
T_COD = new_trainer('TRAINER_KV4_SWIMMER_COD', 'Shipwreck Shoals, zwemt rondjes om de wrakken',
                    'COD', 'Swimmer M', 'Swimmer M', 'Male', 'Swimmer',
                    team(51, 20, 'Huntail', 'Relicanth', ('Barraskewda', 1)))
T_NADIA = new_trainer('TRAINER_KV4_TRIATHLETE_NADIA', 'Route 124, eilandje: traint voor een triatlon zonder fiets',
                      'NADIA', 'Triathlete', 'Swimming Triathlete F', 'Female', 'Girl',
                      team(40, 16, 'Floatzel', 'Pelipper', ('Lanturn', 1)))
T_WADE = new_trainer('TRAINER_KV4_SWIMMER_WADE', 'Route 124, oostelijke open zee',
                     'WADE', 'Swimmer M', 'Swimmer M', 'Male', 'Swimmer',
                     team(40, 16, 'Wailord', 'Clawitzer', ('Kingler', 1)))


# =====================================================================================================
# 4. GRANITE CAVE: een spelonkgids met een eindeloze kaart, een Hiker en items
E = Ev('GraniteCave_B1F', surf=False)
E.gift('OBJ_EVENT_GFX_MANIAC', 28, 16, 'Spelunker', 'ITEM_HARD_STONE',
       "I've been mapping this cave for\\n"
       "twelve years. Look. My map.\\p"
       "…Yes, it's a drawing of a man in\\n"
       "a suit. He walked past in year two.\\l"
       "I got distracted.\\p"
       "He was looking for stones. Here.\\n"
       "Have one. I have a lot of stones.",
       "Year thirteen. I'm adding a hat.\\n"
       "He didn't have a hat. Artistic\\l"
       "freedom.", 'MOVEMENT_TYPE_FACE_LEFT', who='spelonkgids (geeft Hard Stone)')
E.trainer('OBJ_EVENT_GFX_HIKER', 14, 12, 'Doug', T_DOUG, 2,
          "Oi! You're standing in my\\n"
          "favourite dark spot!",
          "Fine. I'll find a darker one.",
          "There's a guy down the hall drawing\\n"
          "a map. Twelve years. He still asks\\l"
          "me where the exit is.", who='Hiker Doug (trainer)')
E.ball(1, 1, 'ITEM_FIST_PLATE')
E.hidden(25, 22, 'ITEM_REVIVE')
E.sign(13, 11, 'Graffiti',
       "Scratched into the rock:\\p"
       "“STEVEN WAS HERE.”\\n"
       "“NO HE WASN'T. -STEVEN”")
E.finish()

E = Ev('GraniteCave_1F', surf=False)
E.hidden(12, 12, 'ITEM_ESCAPE_ROPE', '(doodlopend gangetje)')
E.finish()


# =====================================================================================================
# 5. SHOAL CAVE: eb en vloed doen ertoe
F_HIDE_SWIMMER = flag('FLAG_KV4_HIDE_SHOAL_SWIMMER', 'Shoal Cave: zwemmer alleen bij vloed')
F_HIDE_SANDBAR = flag('FLAG_KV4_HIDE_SHOAL_SANDBAR', 'Shoal Cave: Splash Plate op de zandbank alleen bij eb')
F_SANDBAR = flag('FLAG_KV4_SHOAL_SANDBAR_TAKEN', 'Shoal Cave: Splash Plate van de zandbank gepakt')

E = Ev('ShoalCave_LowTideEntranceRoom')
E.npc_script('OBJ_EVENT_GFX_OLD_MAN', 24, 24, 'TideWatcher', '''
	lock
	faceplayer
	goto_if_set FLAG_SYS_SHOAL_TIDE, %(P)s_High
	msgbox %(Q)s_Low, MSGBOX_DEFAULT
	release
	end
%(P)s_High:
	msgbox %(Q)s_High, MSGBOX_DEFAULT
	release
	end''', {
    '_Low': "Low tide. The sea has gone out for\\n"
            "cigarettes. It always comes back.\\p"
            "Now's your chance. There is a\\n"
            "sandbar in the inner cave that only\\l"
            "shows when the water's away.\\p"
            "Something shiny on it. I'd get it,\\n"
            "but my knees have a tide too.",
    '_High': "High tide. The cave is soup again.\\p"
             "Some girl swims laps in the inner\\n"
             "cave when the water's up. Says she\\l"
             "trains for the moon.\\p"
             "The moon pulls the tide, she says.\\n"
             "She wants to pull back. Harder."},
    'MOVEMENT_TYPE_FACE_DOWN', who='getijdenwachter (andere tekst bij eb/vloed, hint naar zandbank en zwemmer)')
E.finish()

E = Ev('ShoalCave_LowTideInnerRoom')
# zandbank: alleen bij eb droog (bij vloed water) -> eigen pak-script met een aparte verbergvlag
E.npc_script('OBJ_EVENT_GFX_ITEM_BALL', 11, 15, 'Sandbar', '''
	lock
	giveitem ITEM_SPLASH_PLATE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag %s
	setflag %s
	removeobject VAR_LAST_TALKED
	release
	end''' % (F_SANDBAR, F_HIDE_SANDBAR), {}, 'MOVEMENT_TYPE_LOOK_AROUND', who='', fl=F_HIDE_SANDBAR)
E.items.append('Splash Plate (alleen bij eb, op de zandbank)')
# zwemmer: alleen bij vloed (staat dan op het water)
E.trainer('OBJ_EVENT_GFX_SWIMMER_F', 20, 8, 'Maren', T_MAREN, 3,
          "The moon pulls the sea. I pull it\\n"
          "back. Every lap is a protest!",
          "The moon wins again.\\n"
          "It always has better PR.",
          "At low tide I just lie on the sand\\n"
          "and wait. Like a beached grudge.",
          'MOVEMENT_TYPE_FACE_LEFT', who='Swimmer Maren (trainer, alleen bij vloed)', fl=F_HIDE_SWIMMER, water=True)
E.objs[-1]['_elev'] = 1
E.hidden(3, 30, 'ITEM_PEARL_STRING')
E.scr += talk(E.P + 'Tide', '''
	setflag %s
	setflag %s
	goto_if_set FLAG_SYS_SHOAL_TIDE, %sTide_High
	goto_if_set %s, %sTide_End
	clearflag %s
	return
%sTide_High:
	clearflag %s
%sTide_End:
	return''' % (F_HIDE_SWIMMER, F_HIDE_SANDBAR, E.P, F_SANDBAR, E.P, F_HIDE_SANDBAR, E.P, F_HIDE_SWIMMER, E.P))
E.finish()
hook('ShoalCave_LowTideInnerRoom', 'ShoalCave_LowTideInnerRoom_OnTransition', '\tcall ShoalCave_LowTideInnerRoom_EventScript_KV4Tide')
# controle: zandbank is bij vloed water, de zwemmer ligt bij vloed in bereikbaar water
_hi = load('ShoalCave_LowTideInnerRoom')
_hi.v = list(struct.unpack('<%dH' % (_hi.w * _hi.h), open(_LAYOUTS['LAYOUT_SHOAL_CAVE_HIGH_TIDE_INNER_ROOM']['blockdata_filepath'], 'rb').read()))
assert _hi.beh(11, 15) in WATER and _hi.beh(20, 8) in WATER
_r = reach(_hi)
assert any((20 + dx, 8 + dy) in _r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))), 'zwemmer bij vloed onbereikbaar'
assert (3, 30) in _r, 'Pearl String bij vloed onbereikbaar'

E = Ev('ShoalCave_LowTideIceRoom', surf=False)
E.trainer('OBJ_EVENT_GFX_EXPERT_F', 6, 24, 'Olga', T_OLGA, 3,
          "You came in at low tide? Brave.\\n"
          "The sea locks this room twice\\l"
          "a day.\\p"
          "I've been locked in since Tuesday.\\n"
          "I'm fine. My POKéMON are fine.\\l"
          "We are all VERY fine.",
          "Warm. You're warm. I'd forgotten\\n"
          "what that was like.",
          "When the water comes back, I'll\\n"
          "be here. Practising my glare.\\l"
          "It's the only thing that's warm.",
          'MOVEMENT_TYPE_FACE_RIGHT', who='Expert Olga (trainer, ijsgrot; alleen bij eb bereikbaar)')
E.hidden(2, 2, 'ITEM_ICICLE_PLATE')
E.finish()


# =====================================================================================================
# 6. SEAFLOOR CAVERN: sporen van Team Aqua
E = Ev('SeafloorCavern_Room2')
E.trainer('OBJ_EVENT_GFX_AQUA_MEMBER_M', 3, 9, 'Grunt', T_AQUA, 2,
          "Is it over? Did we win? Nobody\\n"
          "told me anything. I'm guarding a\\l"
          "rock. It's a very important rock.",
          "Ow. So that's a yes to\\n"
          "“did we lose”,\\l"
          "wasn't it?",
          "The BOSS said “stay here until I\\n"
          "come back”. That was three weeks\\l"
          "ago. I named the rock. It's Gary.",
          'MOVEMENT_TYPE_FACE_RIGHT', who='Aqua Grunt (trainer, vergeten op wacht)')
E.finish()

E = Ev('SeafloorCavern_Room5')
E.hidden(17, 11, 'ITEM_DEEP_SEA_SCALE')
E.finish()

E = Ev('SeafloorCavern_Room6')
E.hidden(2, 4, 'ITEM_DIVE_BALL')
E.finish()

E = Ev('SeafloorCavern_Room7')
E.sign(3, 19, 'DiveLog',
       "A soggy notebook. TEAM AQUA\\n"
       "DIVING LOG.\\p"
       "Day 1: Found the cave. Spooky.\\n"
       "Day 2: Found a bigger cave.\\p"
       "Day 3: Boss says we can wake up a\\n"
       "sea god. I asked if we SHOULD.\\l"
       "I am now on boulder duty.")
E.ball(8, 22, 'ITEM_DREAD_PLATE')
E.hidden(2, 23, 'ITEM_BIG_PEARL')
E.finish()

E = Ev('SeafloorCavern_Room9')
E.hidden(2, 2, 'ITEM_MAX_ELIXIR')
E.hidden(5, 31, 'ITEM_DAMP_ROCK')
E.finish()


# =====================================================================================================
# 7. CAVE OF ORIGIN: verslaggeefster, Magma-grunt en items
E = Ev('CaveOfOrigin_Entrance', surf=False)
E.npc('OBJ_EVENT_GFX_REPORTER_F', 7, 12, 'Reporter',
      "This is GABBY's backup, live from\\n"
      "the end of the world!\\p"
      "Our sources say the sky and the sea\\n"
      "are fighting. Our other sources say\\l"
      "that's every Tuesday in HOENN.\\p"
      "Back to you in the studio. Hello?\\n"
      "Is there still a studio?",
      'MOVEMENT_TYPE_FACE_RIGHT', who='reserve-verslaggeefster')
E.finish()

E = Ev('CaveOfOrigin_1F', surf=False)
E.trainer('OBJ_EVENT_GFX_MAGMA_MEMBER_F', 17, 15, 'Grunt', T_MAGMA, 4,
          "I quit TEAM MAGMA this morning.\\n"
          "I'm still in the uniform. It's\\l"
          "the only clean thing I own.",
          "Even unemployed, I lose.",
          "I came to watch the apocalypse up\\n"
          "close. You know. For closure.\\p"
          "It's mostly just humid.",
          'MOVEMENT_TYPE_FACE_LEFT', who='ex-Magma Grunt (trainer)')
E.ball(6, 6, 'ITEM_PP_UP')
E.finish()

E = Ev('CaveOfOrigin_B1F', surf=False)
E.hidden(4, 5, 'ITEM_COMET_SHARD')
E.hidden(14, 12, 'ITEM_BOTTLE_CAP')
E.finish()


# =====================================================================================================
# 8. LEGE GROTTEN EN KAMERS: (verborgen) items
E = Ev('AbandonedShip_Deck', surf=False)
E.ball(9, 6, 'ITEM_LUXURY_BALL')
E.hidden(8, 11, 'ITEM_HEART_SCALE')
E.finish()

E = Ev('MagmaHideout_2F_3R', surf=False)
E.hidden(9, 11, 'ITEM_HEAT_ROCK')
E.hidden(23, 13, 'ITEM_FULL_RESTORE')
E.finish()

E = Ev('MeteorFalls_B1F_1R')
E.hidden(3, 6, 'ITEM_MOON_STONE')
E.ball(16, 17, 'ITEM_DRAGON_SCALE')
E.hidden(17, 34, 'ITEM_STAR_PIECE')
E.finish()

E = Ev('MeteorFalls_StevensCave', surf=False)
E.hidden(3, 17, 'ITEM_IRON_PLATE')
E.ball(25, 8, 'ITEM_MAX_REVIVE')
E.hidden(23, 15, 'ITEM_METAL_COAT')
E.finish()

E = Ev('Route136_Grotto')
E.hidden(10, 2, 'ITEM_NEVER_MELT_ICE')
E.ball(4, 25, 'ITEM_ICE_STONE')
E.finish()

E = Ev('NavelRock_Entrance', surf=False)
E.hidden(3, 3, 'ITEM_PP_MAX')
E.ball(8, 13, 'ITEM_ULTRA_BALL')
E.finish()


# =====================================================================================================
# 9. BUITENKAARTEN
E = Ev('ShipwreckShoals', shallow=True)
E.npc('OBJ_EVENT_GFX_SAILOR', 8, 40, 'Salvager',
      "I salvage wrecks. Mostly I salvage\\n"
      "the same wreck. Over and over.\\p"
      "Every night it sinks again. Every\\n"
      "morning it's back. The ghosts call\\l"
      "it a “routine”.\\p"
      "I call it job security.",
      'MOVEMENT_TYPE_FACE_RIGHT', who='bergingsduiker')
E.trainer('OBJ_EVENT_GFX_SAILOR', 32, 14, 'Barnaby', T_BARNABY, 3,
          "I deserted the ghost ship! Don't\\n"
          "tell the captain. Or the union.",
          "Defeated. Still technically alive.\\n"
          "That's more than the crew can say.",
          "I'm three hundred years behind on\\n"
          "union dues. With interest, I owe\\l"
          "them roughly one soul.",
          'MOVEMENT_TYPE_FACE_LEFT', who='Sailor Barnaby (trainer)')
E.trainer('OBJ_EVENT_GFX_SWIMMER_M', 14, 30, 'Cod', T_COD, 4,
          "I swim laps around the wrecks.\\n"
          "They can't chase me. Probably.",
          "Okay. You can chase me.",
          "One of the wrecks winked at me\\n"
          "yesterday. I'm not saying it\\l"
          "was a portal. I'm thinking it.",
          'MOVEMENT_TYPE_FACE_RIGHT', who='Swimmer Cod (trainer)', water=True)
E.hidden(29, 18, 'ITEM_RELIC_GOLD')
E.ball(4, 12, 'ITEM_SPELL_TAG')
E.hidden(37, 47, 'ITEM_PEARL_STRING')
E.finish()

E = Ev('SafariZone_North', surf=False)
E.npc('OBJ_EVENT_GFX_POKEFAN_M', 12, 16, 'RockFan',
      "I come here to watch people smash\\n"
      "rocks. Every rock is different.\\p"
      "Inside every rock is a smaller\\n"
      "rock. Or a POKéMON. Or nothing.\\p"
      "Like a gift. From a rock.\\n"
      "Who hates you a little.",
      'MOVEMENT_TYPE_FACE_RIGHT', who='steenliefhebber')
E.hidden(38, 1, 'ITEM_SOFT_SAND')
E.hidden(5, 38, 'ITEM_HP_UP')
E.ball(33, 24, 'ITEM_SMOOTH_ROCK')
E.finish()

E = Ev('SafariZone_Northwest', surf=False)
E.npc('OBJ_EVENT_GFX_WOMAN_3', 14, 24, 'Birdwatcher',
      "I've been watching birds for six\\n"
      "hours. None of them were birds.\\p"
      "One was a TAUROS. One was a man\\n"
      "named Keith. Keith was very still.\\p"
      "I'm counting him anyway.",
      'MOVEMENT_TYPE_FACE_UP', who='vogelaarster')
E.hidden(36, 15, 'ITEM_ZINC')
E.hidden(2, 31, 'ITEM_BIG_MUSHROOM')
E.finish()

E = Ev('SafariZone_Southwest', surf=False)
E.npc('OBJ_EVENT_GFX_SCIENTIST_1', 20, 25, 'Starter',
      "I'm studying why starter POKéMON\\n"
      "live together in the wild here.\\p"
      "Theory: they were all abandoned by\\n"
      "children who picked the other one.\\p"
      "This is a support group.\\n"
      "Please don't pick one in front of\\l"
      "the others. They talk.",
      'MOVEMENT_TYPE_FACE_DOWN', who='starteronderzoeker')
E.hidden(39, 20, 'ITEM_CARBOS')
E.hidden(38, 6, 'ITEM_MIRACLE_SEED')
E.finish()

E = Ev('NothingIsland')
E.npc('OBJ_EVENT_GFX_MAN_2', 16, 13, 'Tourist',
      "I booked a trip to NOTHING ISLAND.\\n"
      "Brochure promised nothing.\\p"
      "Then a giant pirate ship showed up\\n"
      "with men in robes. That's not\\l"
      "nothing. That's SOMETHING.\\p"
      "I'm leaving a one-star review.",
      'MOVEMENT_TYPE_FACE_DOWN', who='teleurgestelde toerist')
E.hidden(18, 27, 'ITEM_NUGGET')
E.hidden(7, 25, 'ITEM_RELIC_SILVER')
E.finish()

E = Ev('Route124')
E.npc('OBJ_EVENT_GFX_FISHERMAN', 58, 39, 'Beachcomber',
      "Everything washes up here sooner\\n"
      "or later. Bottles. Shoes. A whole\\l"
      "WAILORD once. Took a week to roll\\l"
      "it back.\\p"
      "Stand still long enough and you'll\\n"
      "wash up here too. Most people do.",
      'MOVEMENT_TYPE_FACE_DOWN', who='strandjutter')
E.trainer('OBJ_EVENT_GFX_RUNNING_TRIATHLETE_F', 62, 41, 'Nadia', T_NADIA, 3,
          "A triathlon is swim, bike, run.\\n"
          "My bike sank. So now it's swim,\\l"
          "swim, run. Mostly swim.",
          "A podium finish! For you.",
          "I'm thinking of making it a\\n"
          "biathlon. Then a regular athlon.\\l"
          "Then just a nap.",
          'MOVEMENT_TYPE_FACE_LEFT', who='Triathlete Nadia (trainer, eiland)')
E.trainer('OBJ_EVENT_GFX_SWIMMER_M', 66, 60, 'Wade', T_WADE, 4,
          "I'm swimming to MOSSDEEP. It's\\n"
          "been four days. Is it this way?",
          "You beat me AND I'm lost.\\n"
          "Busy day.",
          "If you see MOSSDEEP, tell it I'm\\n"
          "on my way. Slowly. In circles.",
          'MOVEMENT_TYPE_FACE_LEFT', who='Swimmer Wade (trainer, open zee)', water=True)
E.hidden(60, 43, 'ITEM_SHINY_STONE')
E.ball(19, 72, 'ITEM_NET_BALL')
E.finish()


# =====================================================================================================
for label, s in TEXTS:
    try:
        check_text(label, s)
    except AssertionError as e:
        print(e); FAIL.append('tekst')
assert not FAIL, FAIL
open(WILD, 'w').write(WTEXT[0])
json.loads(WTEXT[0])
write_flags()
write_trainers()
json.dump(ORIG, open(ORIG_PATH, 'w'), indent=0, sort_keys=True)
print('ok: %d tabellen, %d trainers (%d-%d), %d flags (FLAG_GROUNDED %d-%d)' % (
    len(TABLES), len(TRAINERS), FIRST_ID, FIRST_ID + len(TRAINERS) - 1, len(FLAGS), FLAG_FIRST, FLAG_FIRST + len(FLAGS) - 1))
if '--report' in sys.argv:
    for mp, s in REPORT:
        print('%-34s %s' % (mp, s))
