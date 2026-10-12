"""Project Grounded: het nachtelijke benedendek van het Abandoned Ship (Route 108), TODO 13 (Jordi 9 okt).

's Nachts (echte klok, IsNightTime = TIME_NIGHT) ligt in de gang van B1F (AbandonedShip_Corridors_B1F) een trap naar
beneden op (11,6): het ON_LOAD-script zet daar de trap-metatile uit de 1F-gang (0x20A, oostpijl-warp) met de wand
0x20B ernaast. Overdag is het gewone vloer + een dichtgetimmerd gat (0x2AC): de warp ligt er wel, maar warps werken
alleen op een tegel met warpgedrag, dus overdag gebeurt er niets. Het bordje op (12,6) vertelt overdag dat het luik
dicht zit.

Benedendek (gMapGroup_Grounded), kopieen van vanilla layouts (InsideShip-tileset), WEATHER_SHADE:
- AbandonedShip_NightDeck (13x11): kopie van HiddenFloorCorridors; linksboven de trap omhoog uit B1F (0x2A6, zoals
  B1F <-> 1F), alle zes deuren open (0x233 -> 0x22B, 0x234 -> 0x21A). Het ondergelopen hoekje linksonder is surfbaar
  (water-encounters).
- AbandonedShip_NightCabins (44x15): kopie van HiddenFloorRooms (zes hutten), met spoken, een logboek, en de items.
Wilde Pokemon (Ghost/Water, 12 unieke soorten): op de plek in het verhaal (Route 108 en het schip zelf, lv 40-53),
dus lv 44-50 (Norman-Winona). Geen trainers.
Items: nieuwe_items.py (FLAG_GROUNDED 1400-1402). Flags: FLAG_GROUNDED 1400-1439, blok 'abandoned_ship_night'.
Idempotent; controleert de bereikbaarheid van deuren, warps, items, NPC's en het water.
Gebruik: python3 tools/grounded/maptools/abandoned_ship_night.py [render.png]   (render: na make)"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
import check_levels  # noqa: E402
check_levels.protect()
import importlib.util, json, os, random, re, struct, sys  # noqa: E401,E402
from collections import deque  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
os.chdir(REPO)
sys.path.insert(0, HERE)
import nieuwe_items as ni  # noqa: E402

SEED = 1400
rng = random.Random(SEED)   # (geen toeval nodig; vaste seed voor latere uitbreidingen)
GROUP = 'gMapGroup_Grounded'
DECK, CABINS = 'AbandonedShip_NightDeck', 'AbandonedShip_NightCabins'
DECK_C, CABINS_C = 'ABANDONED_SHIP_NIGHT_DECK', 'ABANDONED_SHIP_NIGHT_CABINS'
B1F = 'AbandonedShip_Corridors_B1F'
HATCH = (11, 6)                  # trap naar beneden in de B1F-gang ('s nachts)
HATCH_WALL = (12, 6)
STAIRS = (0, 2)                  # trap omhoog in het benedendek (aankomst)
MUSIC = 'MUS_MT_PYRE'

_spec = importlib.util.spec_from_file_location('dialogen_import', 'tools/dialogen/import.py')
dimp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dimp)

# ====================================================================== flags (FLAG_GROUNDED 1400-1439)
FLAGS = [
    (1410, 'FLAG_HIDE_NIGHT_CABINS_SAILOR', 'Abandoned Ship benedendek: de spookmatroos is na zijn praatje opgelost (verbergt hem)'),
]


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// abandoned_ship_night { (tools/grounded/maptools/abandoned_ship_night.py; FLAG_GROUNDED 1400-1439: ' \
          '1400-1402 nieuwe items (blok nieuwe_items), 1410 spookmatroos, 1403-1409 en 1411-1439 nog vrij)\n'
    for n, name, why in FLAGS:
        assert 1400 <= n <= 1439
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// abandoned_ship_night {' in s:
        i = s.index('// abandoned_ship_night {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// enamorus {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)
    ni.flags()


# ====================================================================== layouts
LAYOUTS = {l['name']: l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if 'name' in l}


def read_layout(name):
    L = LAYOUTS[name + '_Layout']
    w, h = L['width'], L['height']
    v = struct.unpack('<%dH' % (w * h), open(L['blockdata_filepath'], 'rb').read())
    return [list(v[y * w:(y + 1) * w]) for y in range(h)]


def setmt(g, x, y, mt, coll=None):
    v = g[y][x]
    if coll is not None:
        v = (v & ~0xC00) | (coll << 10)
    g[y][x] = (v & ~0x3FF) | mt


def register_layout(name, const, w, h):
    lj = open('data/layouts/layouts.json').read()
    entry = '''    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "gTileset_General",
      "secondary_tileset": "gTileset_InsideShip",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (const, name, w, h, name, name)
    if '"LAYOUT_%s"' % const in lj:
        i = lj.index('"id": "LAYOUT_%s"' % const); s = lj.rindex('    {', 0, i); e = lj.index('    }', i) + 5
        lj = lj[:s] + entry + lj[e:]
    else:
        i = lj.rindex('    }\n  ]')
        lj = lj[:i + 5] + ',\n' + entry + lj[i + 5:]
    json.loads(lj)
    open('data/layouts/layouts.json', 'w').write(lj)


def save_layout(name, const, g, border_from):
    os.makedirs('data/layouts/' + name, exist_ok=True)
    open('data/layouts/%s/map.bin' % name, 'wb').write(b''.join(struct.pack('<H', v) for r in g for v in r))
    open('data/layouts/%s/border.bin' % name, 'wb').write(open('data/layouts/%s/border.bin' % border_from, 'rb').read())
    register_layout(name, const, len(g[0]), len(g))


def deck_layout():
    g = read_layout('AbandonedShip_HiddenFloorCorridors')
    b1f = read_layout(B1F)
    # trap omhoog linksboven: exact de trap uit de B1F-gang (x 0-1, y 0-2)
    for y in range(3):
        for x in range(2):
            g[y][x] = b1f[y][x]
    setmt(g, 0, 3, 0x203, 0)                     # wanddecor onder de trap weg (zoals in B1F)
    # alle deuren open
    for y in range(len(g)):
        for x in range(len(g[0])):
            m = g[y][x] & 0x3FF
            if m == 0x233:
                setmt(g, x, y, 0x22B)
            elif m == 0x234:
                setmt(g, x, y, 0x21A)
    return g


def cabins_layout():
    return read_layout('AbandonedShip_HiddenFloorRooms')


# ====================================================================== bereikbaarheid
BEH = [re.match(r'\s*(MB_\w+)', l).group(1) for l in open('include/constants/metatile_behaviors.h')
       if re.match(r'\s*MB_\w+', l)]


def attrs(path):
    a = open(path, 'rb').read()
    return [struct.unpack_from('<H', a, i * 2)[0] for i in range(len(a) // 2)]


GEN = attrs('data/tilesets/primary/general/metatile_attributes.bin')
SHIP = attrs('data/tilesets/secondary/inside_ship/metatile_attributes.bin')


def beh(v):
    m = v & 0x3FF
    return BEH[(GEN[m] if m < 0x200 else SHIP[m - 0x200]) & 0xFF]


WATER = {'MB_OCEAN_WATER', 'MB_INTERIOR_DEEP_WATER', 'MB_DEEP_WATER', 'MB_POND_WATER'}


def walk(g, start, surf=False, solid=()):
    W, H = len(g[0]), len(g)
    seen = {start}; q = deque([start])
    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in seen or (nx, ny) in solid:
                continue
            v = g[ny][nx]
            if v & 0xC00:
                continue
            if beh(v) in WATER and not surf:
                continue
            seen.add((nx, ny)); q.append((nx, ny))
    return seen


def near(r, p):
    return any((p[0] + dx, p[1] + dy) in r for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))


# ====================================================================== map.json + scripts
def warp(x, y, dest, wid):
    return {'x': x, 'y': y, 'elevation': 3, 'dest_map': 'MAP_' + dest, 'dest_warp_id': str(wid)}


def obj(gfx, x, y, script, flag='0', move='MOVEMENT_TYPE_FACE_DOWN', item=None, qty=1):
    return {'graphics_id': gfx, 'x': x, 'y': y, 'elevation': 3, 'movement_type': move,
            'movement_range_x': qty if qty > 1 else 0, 'movement_range_y': 0, 'trainer_type': 'TRAINER_TYPE_NONE',
            'trainer_sight_or_berry_tree_id': item or '0', 'script': script, 'flag': flag}


def sign(x, y, script, facing='BG_EVENT_PLAYER_FACING_ANY'):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': 3, 'player_facing_dir': facing, 'script': script}


def write_map(name, const, objs, warps, bgs):
    mj = {'id': 'MAP_' + const, 'name': name, 'layout': 'LAYOUT_' + const, 'music': MUSIC,
          'region_map_section': 'MAPSEC_ABANDONED_SHIP', 'requires_flash': False, 'weather': 'WEATHER_SHADE',
          'map_type': 'MAP_TYPE_UNDERGROUND', 'allow_cycling': False, 'allow_escaping': True, 'allow_running': True,
          'show_map_name': name == DECK, 'battle_scene': 'MAP_BATTLE_SCENE_NORMAL', 'connections': None,
          'object_events': objs, 'warp_events': warps, 'coord_events': [], 'bg_events': bgs}
    os.makedirs('data/maps/' + name, exist_ok=True)
    open('data/maps/%s/map.json' % name, 'w').write(json.dumps(mj, indent=2, ensure_ascii=False) + '\n')


def text(label, s):
    out = '%s:\n' % label
    for part in dimp.to_strings(s):
        out += '\t.string "%s"\n' % part
    return out + '\n'


def write_scripts(name, code, texts):
    s = ('@ Project Grounded: %s (gegenereerd door tools/grounded/maptools/abandoned_ship_night.py; niet met de hand '
         'bewerken, teksten via de Dialoogstudio)\n' % name) + code.strip('\n') + '\n\n@ ' + '-' * 64 + \
        ' teksten (placeholders, Jordi herschrijft ze)\n' + ''.join(text(name + '_Text_' + k, v) for k, v in texts)
    open('data/maps/%s/scripts.inc' % name, 'w').write(s.rstrip('\n') + '\n')


TEXTS_B1F = {
    'HatchDay': "A hatch in the floor, boarded up with suspicious enthusiasm.\n\nSomeone chalked on the planks: “LOWER "
                "DECK. OPEN AFTER DARK.”\n\nUnderneath, in shakier handwriting: “please don't.”",
    'HatchNight': "The boards are gone. A staircase leads down into the dark.\n\nCold air drifts up, smelling of seaweed "
                  "and poor decisions.",
}
TEXTS_DECK = {
    'Sign': "LOWER DECK - CREW ONLY\n\nCrew status: deceased.\nCrew morale: weirdly high.",
    'Porthole': "You look through the porthole.\n\nSomething on the other side looks back. It waves. It has too many "
                "fingers for a wave.",
}
TEXTS_CABINS = {
    'Sailor': "Evening, mate. Night watch? Me too. Been on night watch since the ship went down. Since the ship went "
              "DOWN TO THE DOCKS, I mean. For supplies.\n\nShip's fine. Tight as a drum. The water in the corridor is "
              "decorative.\n\nWell, back to work. Don't tell the captain you saw me. Don't tell anyone you saw me. "
              "Technically, you can't have.",
    'SailorGone': "...The SAILOR is gone.\n\nHis chair is still spinning. Slowly. Against the clock.",
    'Lampent': "LAMPENT is keeping watch over the cabin.\n\nIt is also, very politely, sipping at your life force. "
               "It has a quota.\n\nIt's a small quota. Please hold still.",
    'Tuber': "Do you want to play hide-and-seek? I'm really good at it.\n\nNobody's found me in ages.\n\nMy mom said "
             "she'd come looking right after dinner.",
    'Log': "SHIP'S LOG, NIGHT 14,610\n\nWeather: underwater.\nMorale: low.\nPulse: none.\n\nThe passenger in cabin 3 "
           "keeps asking when we dock. I have run out of polite ways to say “never”.",
    'Trash': "There's a note in the bin.\n\n“If found, please return my body to cabin 2.”\n\nThis is cabin 2. You decide "
             "the note was not addressed to you.",
}

# objecten in de hutten (x, y), per hut gecontroleerd
CAB = dict(sailor=(9, 4), lampent=(40, 4), tuber=(32, 12), log=(10, 11), trash=(7, 10),
           ghost_memory=(25, 6), water_gem=(24, 12), water_memory=(31, 10))


def patch_b1f(hatch_idx_dest):
    """Trap + warp + bordje in de B1F-gang; ON_LOAD zet 's nachts de trap."""
    p = 'data/maps/%s/map.json' % B1F
    s = open(p).read()
    d = json.loads(s)
    ws = d['warp_events']
    mine = [i for i, w in enumerate(ws) if w['dest_map'] == 'MAP_' + DECK_C]
    if not mine:
        ws.append(warp(HATCH[0], HATCH[1], DECK_C, hatch_idx_dest))
    if not any(b.get('script') == B1F + '_EventScript_NightHatch' for b in d['bg_events']):
        d['bg_events'].append(sign(HATCH_WALL[0], HATCH_WALL[1], B1F + '_EventScript_NightHatch'))
    open(p, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
    idx = [i for i, w in enumerate(d['warp_events']) if w['dest_map'] == 'MAP_' + DECK_C][0]
    # scripts.inc: één gegenereerd blok + een call in ON_LOAD
    p = 'data/maps/%s/scripts.inc' % B1F
    s = open(p).read()
    call = '\tcall AbandonedShip_Corridors_B1F_EventScript_NightHatchTiles\n'
    if call not in s:
        s = s.replace('AbandonedShip_Corridors_B1F_OnLoad:\n', 'AbandonedShip_Corridors_B1F_OnLoad:\n' + call, 1)
    P = B1F + '_EventScript_'
    blk = ('@ --- benedendek (gegenereerd door abandoned_ship_night.py) ---\n'
           f'{P}NightHatchTiles::\n'
           '\tspecialvar VAR_RESULT, IsNightTime\n'
           '\tgoto_if_eq VAR_RESULT, FALSE, Common_EventScript_NopReturn\n'
           f'\tsetmetatile {HATCH[0]}, {HATCH[1]}, 0x20A, FALSE\n'
           f'\tsetmetatile {HATCH_WALL[0]}, {HATCH_WALL[1]}, 0x20B, TRUE\n'
           '\treturn\n\n'
           f'{P}NightHatch::\n'
           '\tspecialvar VAR_RESULT, IsNightTime\n'
           f'\tgoto_if_eq VAR_RESULT, TRUE, {P}NightHatchOpen\n'
           f'\tmsgbox {B1F}_Text_HatchDay, MSGBOX_SIGN\n'
           '\tend\n\n'
           f'{P}NightHatchOpen::\n'
           f'\tmsgbox {B1F}_Text_HatchNight, MSGBOX_SIGN\n'
           '\tend\n\n'
           + ''.join(text(B1F + '_Text_' + k, v) for k, v in TEXTS_B1F.items()).rstrip('\n') + '\n'
           '@ --- einde benedendek ---\n')
    if '@ --- benedendek' in s:
        i = s.index('@ --- benedendek'); j = s.index('@ --- einde benedendek ---\n', i) + len('@ --- einde benedendek ---\n')
        s = s[:i] + blk + s[j:]
    else:
        s = s.rstrip('\n') + '\n\n' + blk
    open(p, 'w').write(s)
    return idx


def ensure_nop_return():
    assert 'Common_EventScript_NopReturn::' in open('data/event_scripts.s').read(), 'Common_EventScript_NopReturn ontbreekt'


def register_maps():
    g = open('data/maps/map_groups.json').read()
    i = g.index('"%s": [' % GROUP); j = g.index(']', i)
    for name in (DECK, CABINS):
        if '"%s"' % name not in g[i:j]:
            k = g.rindex('"', i, j) + 1
            g = g[:k] + ',\n    "%s"' % name + g[k:]
            j = g.index(']', i)
    grp = re.findall(r'"([^"]+)"', g[g.index('[', i):j])
    assert len(grp) <= 128, len(grp)
    json.loads(g)
    open('data/maps/map_groups.json', 'w').write(g)
    es = open('data/event_scripts.s').read()
    a = '\t.include "data/maps/AbandonedShip_HiddenFloorRooms/scripts.inc"\n'
    for name in (CABINS, DECK):
        inc = '\t.include "data/maps/%s/scripts.inc"\n' % name
        if inc not in es:
            es = es.replace(a, a + inc, 1)
    open('data/event_scripts.s', 'w').write(es)


# ====================================================================== wilde Pokemon
# Plek in het verhaal: Route 108 / het schip (lv 40-53) -> lv 44-50. Ghost/Water, 12 unieke soorten, op deze
# levels allemaal in hun juiste evolutiefase (Houndstone 30, Golisopod 30, Doublade/Lampent: Dusk Stone,
# Drakloak -> Dragapult pas op 60).
LAND = [('HOUNDSTONE', 44, 46), ('LAMPENT', 44, 46), ('GOLISOPOD', 45, 47), ('CRAWDAUNT', 45, 47),
        ('DOUBLADE', 45, 47), ('COFAGRIGUS', 45, 47), ('PALOSSAND', 46, 48), ('BARBARACLE', 46, 48),
        ('DRAKLOAK', 47, 49), ('DHELMISE', 47, 49), ('SPIRITOMB', 49, 50), ('BASCULEGION_M', 50, 50)]
WATER_MONS = [('JELLICENT', 44, 48), ('HUNTAIL', 44, 48), ('LANTURN', 46, 50), ('CURSOLA', 48, 50), ('DONDOZO', 50, 50)]
WILD = {DECK_C: {'land': (10, LAND), 'water': (4, WATER_MONS)}, CABINS_C: {'land': (10, LAND)}}


def wild():
    p = 'src/data/wild_encounters.json'
    s = open(p).read()
    for mp, tabs in WILD.items():
        lbl = 'g' + {DECK_C: DECK, CABINS_C: CABINS}[mp]
        e = {'map': 'MAP_' + mp, 'base_label': lbl}
        for kind in ('land', 'water'):
            if kind not in tabs:
                continue
            rate, spec = tabs[kind]
            assert len(spec) == {'land': 12, 'water': 5}[kind]
            assert len({x[0] for x in spec}) == len(spec), ('dubbele soort', mp, kind)
            e[kind + '_mons'] = {'encounter_rate': rate,
                                 'mons': [{'min_level': a, 'max_level': b, 'species': 'SPECIES_' + sp} for sp, a, b in spec]}
        blob = '\n'.join('        ' + ln for ln in json.dumps(e, indent=2).split('\n'))
        key = '"map": "MAP_%s"' % mp
        if key in s:
            i = s.index(key); a = s.rindex('{', 0, i)
        else:
            i = s.rindex('"map": "MAP_', 0, s.index('"map": "MAP_ABANDONED_SHIP_HIDDEN_FLOOR_ROOMS"') + 1); a = s.rindex('{', 0, i)
        depth, j = 0, a
        while True:
            if s[j] == '{': depth += 1
            elif s[j] == '}':
                depth -= 1
                if depth == 0: break
            j += 1
        if key in s:
            s = s[:a] + blob.lstrip() + s[j + 1:]
        else:
            s = s[:j + 1] + ',\n' + blob + s[j + 1:]
    json.loads(s)
    open(p, 'w').write(s)


# ====================================================================== main
def main():
    ensure_nop_return()
    flags()
    wild()
    # ---------------- layouts
    dg = deck_layout(); cg = cabins_layout()
    save_layout(DECK, DECK_C, dg, 'AbandonedShip_HiddenFloorCorridors')
    save_layout(CABINS, CABINS_C, cg, 'AbandonedShip_HiddenFloorRooms')
    # ---------------- B1F (trap) en de warps van het benedendek
    hc = json.load(open('data/maps/AbandonedShip_HiddenFloorCorridors/map.json'))
    hr = json.load(open('data/maps/AbandonedShip_HiddenFloorRooms/map.json'))
    b1f_idx = patch_b1f(0)
    deck_warps = [warp(STAIRS[0], STAIRS[1], 'ABANDONED_SHIP_CORRIDORS_B1F', b1f_idx)]
    for w in hc['warp_events']:                        # deuren: index + 1 (trap is warp 0)
        deck_warps.append(warp(w['x'], w['y'], CABINS_C, w['dest_warp_id']))
    cab_warps = [warp(w['x'], w['y'], DECK_C, int(w['dest_warp_id']) + 1) for w in hr['warp_events']]
    # ---------------- objecten
    items = ni.items(CABINS)
    by_item = {it: (fl, q, h) for fl, it, q, h in items}
    assert set(by_item) == {'ITEM_GHOST_MEMORY', 'ITEM_WATER_GEM', 'ITEM_WATER_MEMORY'}, items
    P = CABINS + '_EventScript_'
    cobjs = [obj('OBJ_EVENT_GFX_SAILOR', *CAB['sailor'], P + 'Sailor', 'FLAG_HIDE_NIGHT_CABINS_SAILOR', 'MOVEMENT_TYPE_FACE_LEFT'),
             obj('OBJ_EVENT_GFX_SPECIES(LAMPENT)', *CAB['lampent'], P + 'Lampent', move='MOVEMENT_TYPE_LOOK_AROUND'),
             obj('OBJ_EVENT_GFX_TUBER_F', *CAB['tuber'], P + 'Tuber', move='MOVEMENT_TYPE_FACE_RIGHT')]
    for it in ('ITEM_GHOST_MEMORY', 'ITEM_WATER_GEM'):
        fl, q, h = by_item[it]
        cobjs.append(obj('OBJ_EVENT_GFX_ITEM_BALL', *CAB[it[5:].lower()], 'Common_EventScript_FindItem', fl,
                         'MOVEMENT_TYPE_LOOK_AROUND', item=it, qty=q))
    fl, q, h = by_item['ITEM_WATER_MEMORY']
    cbgs = [sign(*CAB['log'], P + 'Log'), sign(*CAB['trash'], P + 'Trash'),
            {'type': 'hidden_item', 'x': CAB['water_memory'][0], 'y': CAB['water_memory'][1], 'elevation': 3,
             'item': 'ITEM_WATER_MEMORY', 'flag': fl}]
    write_map(CABINS, CABINS_C, cobjs, cab_warps, cbgs)
    code = (f'{CABINS}_MapScripts::\n\t.byte 0\n\n'
            f'{P}Sailor::\n\tlock\n\tfaceplayer\n\tmsgbox {CABINS}_Text_Sailor, MSGBOX_DEFAULT\n\tclosemessage\n'
            '\tplayse SE_M_NIGHTMARE\n\tfadescreen FADE_TO_BLACK\n\tremoveobject VAR_LAST_TALKED\n'
            '\tsetflag FLAG_HIDE_NIGHT_CABINS_SAILOR\n\tfadescreen FADE_FROM_BLACK\n'
            f'\tmsgbox {CABINS}_Text_SailorGone, MSGBOX_DEFAULT\n\trelease\n\tend\n\n'
            f'{P}Lampent::\n\tlock\n\tfaceplayer\n\tplaymoncry SPECIES_LAMPENT, CRY_MODE_NORMAL\n'
            f'\tmsgbox {CABINS}_Text_Lampent, MSGBOX_DEFAULT\n\twaitmoncry\n\trelease\n\tend\n\n'
            f'{P}Tuber::\n\tmsgbox {CABINS}_Text_Tuber, MSGBOX_NPC\n\tend\n\n'
            f'{P}Log::\n\tmsgbox {CABINS}_Text_Log, MSGBOX_SIGN\n\tend\n\n'
            f'{P}Trash::\n\tmsgbox {CABINS}_Text_Trash, MSGBOX_SIGN\n\tend\n')
    write_scripts(CABINS, code, list(TEXTS_CABINS.items()))
    # benedendek-gang
    D = DECK + '_EventScript_'
    dbgs = [sign(4, 1, D + 'Sign', 'BG_EVENT_PLAYER_FACING_NORTH'), sign(9, 1, D + 'Porthole', 'BG_EVENT_PLAYER_FACING_NORTH')]
    write_map(DECK, DECK_C, [], deck_warps, dbgs)
    write_scripts(DECK, f'{DECK}_MapScripts::\n\t.byte 0\n\n'
                        f'{D}Sign::\n\tmsgbox {DECK}_Text_Sign, MSGBOX_SIGN\n\tend\n\n'
                        f'{D}Porthole::\n\tmsgbox {DECK}_Text_Porthole, MSGBOX_SIGN\n\tend\n',
                  list(TEXTS_DECK.items()))
    register_maps()
    check(dg, cg, deck_warps, cab_warps, cobjs, cbgs, dbgs)


def check(dg, cg, deck_warps, cab_warps, cobjs, cbgs, dbgs):
    # B1F: de trapplek is bereikbaar vanuit de rest van de gang (vanaf de trap naar 1F)
    b = read_layout(B1F)
    assert beh(b[HATCH[1]][HATCH[0]]) == 'MB_INDOOR_ENCOUNTER' and not b[HATCH[1]][HATCH[0]] & 0xC00
    rb = walk(b, (1, 3))
    assert HATCH in rb, 'trapplek in B1F onbereikbaar'
    # benedendek: vanaf de trap alle deuren (aangrenzend) en het water (surfen)
    r = walk(dg, STAIRS)
    for w in deck_warps[1:]:
        assert (w['x'], w['y']) in r or near(r, (w['x'], w['y'])), ('deur onbereikbaar', w)
    for x, y in [(s['x'], s['y']) for s in dbgs]:
        assert near(r, (x, y)), ('bord onbereikbaar', x, y)
    rs = walk(dg, STAIRS, surf=True)
    water = [(x, y) for y in range(len(dg)) for x in range(len(dg[0])) if beh(dg[y][x]) in WATER]
    assert water and all(p in rs for p in water), 'water niet (helemaal) bereikbaar'
    # hutten: per ingang lopen; alle objecten/borden aangrenzend bereikbaar, verborgen item zelf
    solid = {(o['x'], o['y']) for o in cobjs}
    reach = set()
    for w in cab_warps:
        s = (w['x'], w['y'] + (1 if w['y'] < 7 else -1))
        assert not cg[s[1]][s[0]] & 0xC00, ('ingang dicht', w)
        reach |= walk(cg, s, solid=solid)
    for o in cobjs:
        assert not cg[o['y']][o['x']] & 0xC00, ('object op een muur', o['script'], o['x'], o['y'])
        assert near(reach, (o['x'], o['y'])), ('object onbereikbaar', o['script'])
    for bg in cbgs:
        if bg['type'] == 'hidden_item':
            assert (bg['x'], bg['y']) in reach, ('verborgen item onbereikbaar', bg)
        else:
            assert near(reach, (bg['x'], bg['y'])), ('bord onbereikbaar', bg)
    # elke deur in de gang leidt naar een ingang in de hutten en terug
    for i, w in enumerate(deck_warps[1:], 1):
        cw = cab_warps[int(w['dest_warp_id'])]
        assert cw['dest_warp_id'] == str(i), ('warps niet wederkerig', i, cw)
    print('bereikbaarheid ok: %d tegels in de gang, %d in de hutten, %d water' % (len(r), len(reach), len(water)))


def render(out):
    from PIL import Image
    import subprocess
    tmp = []
    for name, h in ((DECK, 11), (CABINS, 15)):
        p = out + '.' + name + '.png'
        subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), name, p, '0', str(h)], check=True)
        tmp.append(Image.open(p))
    W = max(i.width for i in tmp); H = sum(i.height for i in tmp) + 16
    im = Image.new('RGB', (W, H), (16, 16, 24)); y = 0
    for i in tmp:
        im.paste(i, (0, y)); y += i.height + 16
    im.save(out)
    for name in (DECK, CABINS):
        os.remove(out + '.' + name + '.png')
    print('render:', out)


if __name__ == '__main__':
    main()
    if len(sys.argv) > 1:
        render(sys.argv[1])
