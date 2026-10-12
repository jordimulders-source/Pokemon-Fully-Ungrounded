"""Project Grounded: hulpjes om objecten/teksten op bestaande landkaarten te zetten (gebruikt door land_vulling.py).

- Kaart(naam): laadt map.json + layout + gedrag per tegel (primary/secondary uit headers.h/metatiles.h).
- walk(): bereikbare tegels vanaf een start (botsing, hoogte (elevation), water alleen met surf=True).
- explore: `python3 tools/grounded/maptools/landlib.py <Kaart> <x> <y>` print de bereikbare tegels als ASCII
  (. = bereikbaar, cijfer = hoogte van een onbereikbare vrije tegel, # = muur, ~ = water, W/O/i/h/b = events).
- apply_events(): zet eigen objecten/bg-events achteraan map.json (idempotent via script-/flagnamen) en
  een gemarkeerd blok in scripts.inc.
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

BEH = {}
for _l in open('include/constants/metatile_behaviors.h'):
    _m = re.match(r'\s*(MB_\w+)', _l)
    if _m and _m.group(1) not in BEH:
        BEH[_m.group(1)] = len(BEH)
MB = {v: k for k, v in BEH.items()}
_HDR = open('src/data/tilesets/headers.h').read()
_MT = open('src/data/tilesets/metatiles.h').read()
_LAYOUTS = {l['id']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'id' in l}


def _attrs(sym):
    body = re.search(r'const struct Tileset ' + sym + r' =(?:\s*//[^\n]*)?\s*\{(.*?)\};', _HDR, re.S).group(1)
    a = re.search(r'\.metatileAttributes = (\w+)', body).group(1)
    p = re.search(a + r'\[\] = INCBIN_U16\("([^"]+)"', _MT).group(1)
    b = open(p, 'rb').read()
    return [struct.unpack_from('<H', b, i * 2)[0] for i in range(len(b) // 2)]


WATER = {'MB_OCEAN_WATER', 'MB_DEEP_WATER', 'MB_POND_WATER', 'MB_SEAWEED', 'MB_NO_SURFACING', 'MB_SEAWEED_NO_SURFACING',
         'MB_WESTWARD_CURRENT', 'MB_EASTWARD_CURRENT', 'MB_NORTHWARD_CURRENT', 'MB_SOUTHWARD_CURRENT', 'MB_WATERFALL',
         'MB_INTERIOR_DEEP_WATER', 'MB_SOOTOPOLIS_DEEP_WATER'}
NOPLACE = WATER | {'MB_SHALLOW_WATER'}  # geen objecten/items in (ondiep) water
LEDGE = {'MB_JUMP_EAST', 'MB_JUMP_WEST', 'MB_JUMP_NORTH', 'MB_JUMP_SOUTH', 'MB_JUMP_NORTHEAST', 'MB_JUMP_NORTHWEST',
         'MB_JUMP_SOUTHEAST', 'MB_JUMP_SOUTHWEST'}


class Kaart:
    def __init__(self, name):
        self.name = name
        self.path = 'data/maps/%s/map.json' % name
        self.d = json.load(open(self.path))
        L = _LAYOUTS[self.d['layout']]
        self.w, self.h = L['width'], L['height']
        self.v = struct.unpack('<%dH' % (self.w * self.h), open(L['blockdata_filepath'], 'rb').read())
        self.P, self.S = _attrs(L['primary_tileset']), _attrs(L['secondary_tileset'])

    def c(self, x, y):
        return self.v[y * self.w + x]

    def beh(self, x, y):
        mt = self.c(x, y) & 0x3FF
        a = self.P[mt] if mt < 0x200 else self.S[mt - 0x200]
        return MB.get(a & 0xFF, hex(a & 0xFF))

    def elev(self, x, y):
        return self.c(x, y) >> 12

    def blocked(self, x, y):
        return bool(self.c(x, y) & 0xC00)

    def event_tiles(self):
        t = set()
        for wp in self.d['warp_events']:
            t.add((wp['x'], wp['y']))
        for ce in self.d.get('coord_events') or []:
            t.add((ce['x'], ce['y']))
        return t

    def walk(self, start, solid=(), surf=False):
        """Bereikbare tegels (lopen; met surf ook water). solid = extra geblokkeerde tegels (objecten)."""
        solid = set(solid)
        seen = {start: self.elev(*start)}
        q = deque([start])
        while q:
            x, y = q.popleft()
            ze = seen[(x, y)]
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                p = (x + dx, y + dy)
                if p in seen or not (0 <= p[0] < self.w and 0 <= p[1] < self.h): continue
                if self.blocked(*p) or p in solid: continue
                b = self.beh(*p)
                if b in LEDGE: continue
                if b in WATER and not surf: continue
                e = self.elev(*p)
                if not (e in (0, 15) or ze in (0, 15) or e == ze): continue
                seen[p] = ze if e == 15 else e
                q.append(p)
        return seen

    def ascii(self, start, y0=0, y1=9999, surf=False):
        r = self.walk(start, surf=surf)
        ev = {}
        for o in self.d['object_events']:
            ev[(o['x'], o['y'])] = 'i' if 'ITEM_BALL' in o['graphics_id'] else 'O'
        for b in self.d['bg_events']:
            ev[(b['x'], b['y'])] = 'h' if b['type'] == 'hidden_item' else 'b'
        for wp in self.d['warp_events']:
            ev[(wp['x'], wp['y'])] = 'W'
        out = ['    ' + ''.join(str(x // 10 % 10) for x in range(self.w)),
               '    ' + ''.join(str(x % 10) for x in range(self.w))]
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            row = ''
            for x in range(self.w):
                if (x, y) in ev: ch = ev[(x, y)]
                elif (x, y) in r: ch = '~' if self.beh(x, y) in WATER else ('g' if 'GRASS' in self.beh(x, y) and 'SHORT' not in self.beh(x, y) else '.')
                elif self.blocked(x, y): ch = '#'
                elif self.beh(x, y) in WATER: ch = '='
                else: ch = '%x' % self.elev(x, y)
                row += ch
            out.append('%3d ' % y + row)
        return '\n'.join(out)


# ---------------------------------------------------------------------------------------------------------
def obj(gfx, x, y, script, elev=3, move='MOVEMENT_TYPE_FACE_DOWN', trainer=False, sight=0, flag='0', item=None, rx=0, ry=0):
    return {'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move,
            'movement_range_x': rx, 'movement_range_y': ry,
            'trainer_type': 'TRAINER_TYPE_NORMAL' if trainer else 'TRAINER_TYPE_NONE',
            'trainer_sight_or_berry_tree_id': item or str(sight), 'script': script, 'flag': flag}


def hidden(x, y, item, flag, elev=3):
    return {'type': 'hidden_item', 'x': x, 'y': y, 'elevation': elev, 'item': item, 'flag': flag}


def sign(x, y, script, elev=3):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': elev, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_ANY',
            'script': script}


def ball(x, y, item, flag, elev=3):
    return obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', elev, 'MOVEMENT_TYPE_LOOK_AROUND',
               flag=flag, item=item)


def text(label, s):
    return '%s:\n\t.string "%s$"\n\n' % (label, s)


def talk(label, body):
    return '%s::\n%s\n\n' % (label, body.strip('\n'))


def trainer_single(label, trainer, intro, defeat, post):
    t = label.replace('EventScript', 'Text')
    return ('%s::\n\ttrainerbattle_single %s, %s_Intro, %s_Defeat\n\tmsgbox %s_Post, MSGBOX_AUTOCLOSE\n\tend\n\n'
            % (label, trainer, t, t, t)
            + text(t + '_Intro', intro) + text(t + '_Defeat', defeat) + text(t + '_Post', post))


def check_text(label, s, width=35):
    """Elke regel (tussen \\n, \\l, \\p) moet in het tekstvak passen (ruwe telling, {PLAYER} = 7)."""
    s2 = s.replace('{PLAYER}', 'XXXXXXX').replace('POKéMON', 'POKEMON')
    s2 = re.sub(r'\{[^}]*\}', '', s2)
    for part in re.split(r'\\[nlp]', s2):
        assert len(part) <= width, '%s: regel te lang (%d): %s' % (label, len(part), part)


def apply_events(k, objs, bgs, script_text, mark):
    """Eigen objecten/bg-events achteraan (bestaande nummers blijven gelijk); blok in scripts.inc tussen markeringen."""
    m = json.load(open(k.path))
    mine_scripts = {o['script'] for o in objs if o['script'] != 'Common_EventScript_FindItem'}
    mine_flags = {o['flag'] for o in objs if o['flag'] != '0'} | {b.get('flag') for b in bgs if 'flag' in b}
    mine_bg_scripts = {b.get('script') for b in bgs if 'script' in b}
    m['object_events'] = [o for o in m['object_events'] if o['script'] not in mine_scripts and o['flag'] not in mine_flags]
    m['bg_events'] = [b for b in m['bg_events'] if b.get('flag') not in mine_flags and b.get('script') not in mine_bg_scripts]
    m['object_events'] += objs
    m['bg_events'] += bgs
    os_ = m['object_events']
    for o in os_:  # max. 16 objecten tegelijk (beeld + spawnmarge ~ 24x18 tiles), speler telt mee
        near = [p for p in os_ if abs(p['x'] - o['x']) <= 12 and abs(p['y'] - o['y']) <= 9]
        assert len(near) <= 15, '%s: te veel objecten rond (%d,%d)' % (k.name, o['x'], o['y'])
    open(k.path, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    inc_path = 'data/maps/%s/scripts.inc' % k.name
    inc = open(inc_path).read()
    a, b = '@ --- %s (gegenereerd door tools/grounded/maptools/land_vulling.py) ---' % mark, '@ --- einde %s ---' % mark
    if a in inc:
        inc = inc[:inc.index(a)].rstrip('\n') + '\n' + inc[inc.index(b) + len(b):].lstrip('\n')
    if script_text.strip():
        inc = inc.rstrip('\n') + '\n\n' + a + '\n' + script_text.strip('\n') + '\n' + b + '\n'
    open(inc_path, 'w').write(inc)


if __name__ == '__main__':
    k = Kaart(sys.argv[1])
    x, y = int(sys.argv[2]), int(sys.argv[3])
    y0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    y1 = int(sys.argv[5]) if len(sys.argv) > 5 else 9999
    print(k.ascii((x, y), y0, y1, surf='surf' in sys.argv))
