"""Project Grounded: zeevulling 1 (Route 107, 126, 127 en Underwater 105/125/128/129).

Op het water: kleine eilandjes (ondiepe rand + zand, General-autotile zoals Juans eiland in tides_juan.py)
met NPC's, trainers, items en verborgen items. Onderwater: zeewiervelden (wilde encounters, zie
wild_encounters.json) en verborgen items.

- Route 107: sushi-eilandje (kok + Sailor Duncan, boot), rots-eilandje met een "ruïne" (Ruin Maniac Simon).
- Route 126: picknickbank (Old Couple Hal & Mae), "Great Pacifidlog Garbage Patch" (vrijwilliger, raadselkist,
  rubber eend), vogeleilandje (Bird Keeper Oswald), zeemeermin-fan Sirena (grap-trainer) zwemt bij Sootopolis.
- Route 127: gestrande Wailmer op de ondiepte (Ranger Marisol), verdwaalde toerist, tweeling Pip & Pep.
- Onderwater: zeewier + verborgen items; 105 zeemansgraf (rots met opschrift + schat), 125 duiker.

Idempotent: zet eerst de vakken van de eilandjes terug op zee (asserts dat er alleen zee of eigen tiles lag),
haalt eigen objecten/bg-events/scriptblokken weg en voegt ze opnieuw toe. Controleert de bereikbaarheid.
Gebruik (vanuit de repo-root): python3 tools/grounded/maptools/zee_vulling_1.py
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

random.seed(1071)
BLOCK, E1, E3 = 1 << 10, 1 << 12, 3 << 12
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


GEN = attrs('data/tilesets/primary/general/metatile_attributes.bin')
SEC = {s: attrs('data/tilesets/secondary/%s/metatile_attributes.bin' % s) for s in ('mossdeep', 'dewford', 'underwater')}
SURF = {'MB_OCEAN_WATER', 'MB_DEEP_WATER', 'MB_POND_WATER', 'MB_SEAWEED', 'MB_NO_SURFACING', 'MB_SEAWEED_NO_SURFACING',
        'MB_WESTWARD_CURRENT', 'MB_EASTWARD_CURRENT', 'MB_NORTHWARD_CURRENT', 'MB_SOUTHWARD_CURRENT'}


def beh(c, sec):
    mt = c & 0x3FF
    a = GEN[mt] if mt < 0x200 else SEC[sec][mt - 0x200]
    return MB.get(a & 0xFF, a & 0xFF)


def cell(mt, sec, blocked=False):
    return mt | (E1 if beh(mt, sec) in SURF else E3) | (BLOCK if blocked else 0)


# --- General-autotile: ondiepe rand (RING) rond zand (SAND); zelfde tiles als tides_juan.py ---
RING = {'TL': 0x1AD, 'T': 0x1AE, 'TR': 0x1AF, 'L': 0x1B5, 'R': 0x1B7, 'BL': 0x1BD, 'B': 0x1BE, 'BR': 0x1BF,
        'NW': 0x19B, 'NE': 0x19C, 'SW': 0x1A3, 'SE': 0x1A4, 'C': 0x19E}
SAND = {'C': 0x124, 'TL': 0x195, 'T': 0x196, 'TR': 0x197, 'L': 0x19D, 'R': 0x19F, 'BL': 0x1A5, 'B': 0x1A6,
        'BR': 0x1A7, 'NW': 0x185, 'NE': 0x186, 'SW': 0x18D, 'SE': 0x18E}
ROCK_SAND = [0x0A3, 0x0A4, 0x0AB, 0x0AC]
PALM = [0x308, 0x309, 0x310, 0x311]  # Mossdeep
TALL_GRASS = 0x00D
OWN = set(RING.values()) | set(SAND.values()) | set(ROCK_SAND) | set(PALM) | {OCEAN}


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


def load(layout, w, h):
    b = open('data/layouts/%s/map.bin' % layout, 'rb').read()
    assert len(b) == w * h * 2, layout
    return [[struct.unpack_from('<H', b, (y * w + x) * 2)[0] for x in range(w)] for y in range(h)]


def save(layout, v):
    open('data/layouts/%s/map.bin' % layout, 'wb').write(b''.join(struct.pack('<H', c) for r in v for c in r))
    if ORIG: json.dump(ORIG, open(ORIG_PATH, 'w'), indent=0, sort_keys=True)


ORIG_PATH = 'tools/grounded/maptools/zee_vulling_1_orig.json'
ORIG = json.load(open(ORIG_PATH)) if os.path.exists(ORIG_PATH) else {}  # layout -> {"x,y": oorspronkelijke tile}


def restore(layout, v):
    """Zet alle tiles die dit script ooit overschreef terug (idempotent)."""
    for k, c in ORIG.get(layout, {}).items():
        x, y = map(int, k.split(','))
        v[y][x] = c


def islet(layout, v, sec, area, sand, rocks=(), palms=(), grass=()):
    """area = hele eiland (rand + zand), sand = zandvlak; rocks/palms = linkerbovenhoek van een 2x2-blok op het zand."""
    orig = ORIG.setdefault(layout, {})
    xs, ys = [p[0] for p in area], [p[1] for p in area]
    for cx, cy, dx, dy in ((min(xs), min(ys), 1, 1), (max(xs), min(ys), -1, 1), (min(xs), max(ys), 1, -1),
                           (max(xs), max(ys), -1, -1)):  # hoeken afronden waar het zand er niet tegenaan ligt
        if (cx + dx, cy + dy) not in sand:
            area = area - {(cx, cy)}
    for (x, y) in area:
        c = v[y][x]
        assert beh(c, sec) == 'MB_OCEAN_WATER' and not c & BLOCK, 'eiland op (%d,%d) overlapt %x' % (x, y, c & 0x3FF)
        orig.setdefault('%d,%d' % (x, y), c)
    for (x, y) in area:
        v[y][x] = cell(SAND[shape(sand, x, y)], sec) if (x, y) in sand else cell(RING[shape(area, x, y)], sec)
    for blk, tiles in ((rocks, ROCK_SAND), (palms, PALM)):
        for (px, py) in blk:
            for i in range(4):
                cx, cy = px + i % 2, py + i // 2
                assert (v[cy][cx] & 0x3FF) == SAND['C'], '2x2-blok (%d,%d) niet op vol zand' % (px, py)
                v[cy][cx] = cell(tiles[i], sec, tiles is ROCK_SAND or i >= 2)
    for (x, y) in grass:  # hoog gras (wilde Pokémon) alleen op vol zand
        assert (v[y][x] & 0x3FF) == SAND['C'], 'gras (%d,%d) niet op vol zand' % (x, y)
        v[y][x] = cell(TALL_GRASS, sec)


FAIL = []


def reach(name, v, sec, start, targets):
    """Surfen + lopen: alles wat niet geblokkeerd is. Doelen = tegels waar de speler moet kunnen staan."""
    seen, q = {start}, deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            p = (x + dx, y + dy)
            if p in seen or not (0 <= p[0] < len(v[0]) and 0 <= p[1] < len(v)): continue
            if v[p[1]][p[0]] & BLOCK or p in SOLID: continue
            seen.add(p); q.append(p)
    miss = [t for t in targets if t not in seen]
    if miss:
        print('%s: niet bereikbaar: %s' % (name, miss)); FAIL.append(name)


# =====================================================================================================
# map.json-hulpjes
MARK = '@ --- zee_vulling_1 (gegenereerd door tools/grounded/maptools/zee_vulling_1.py) ---'
MARK_END = '@ --- einde zee_vulling_1 ---'


def obj(gfx, x, y, script, elev=3, move='MOVEMENT_TYPE_FACE_DOWN', trainer=False, sight=0, flag='0', item=None):
    return {'graphics_id': gfx, 'x': x, 'y': y, 'elevation': elev, 'movement_type': move,
            'movement_range_x': 0, 'movement_range_y': 0,
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


def apply_events(mapname, objs, bgs, script_text):
    path = 'data/maps/%s/map.json' % mapname
    m = json.load(open(path))
    mine_scripts = {o['script'] for o in objs if o['script'] != 'Common_EventScript_FindItem'}
    mine_flags = {o['flag'] for o in objs if o['flag'] != '0'} | {b.get('flag') for b in bgs if 'flag' in b}
    mine_bg_scripts = {b.get('script') for b in bgs if 'script' in b}
    m['object_events'] = [o for o in m['object_events'] if o['script'] not in mine_scripts and o['flag'] not in mine_flags]
    m['bg_events'] = [b for b in m['bg_events'] if b.get('flag') not in mine_flags and b.get('script') not in mine_bg_scripts]
    m['object_events'] += objs  # achteraan (nummers van bestaande NPC's blijven gelijk)
    m['bg_events'] += bgs
    os_ = m['object_events']
    assert len(os_) <= 60, mapname
    for o in os_:  # max. 15 objecten tegelijk in beeld (beeld + spawnmarge ~ 24x18 tiles)
        near = [p for p in os_ if abs(p['x'] - o['x']) <= 12 and abs(p['y'] - o['y']) <= 9]
        assert len(near) <= 15, '%s: te veel objecten rond (%d,%d)' % (mapname, o['x'], o['y'])
    open(path, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    inc_path = 'data/maps/%s/scripts.inc' % mapname
    inc = open(inc_path).read()
    if MARK in inc:
        inc = inc[:inc.index(MARK)].rstrip('\n') + '\n' + inc[inc.index(MARK_END) + len(MARK_END):].lstrip('\n')
    inc = inc.rstrip('\n') + '\n\n' + MARK + '\n' + script_text.strip('\n') + '\n' + MARK_END + '\n'
    open(inc_path, 'w').write(inc)


def trainer_single(label, trainer, intro, defeat, post):
    return ('%s::\n\ttrainerbattle_single %s, %s_Intro, %s_Defeat\n\tmsgbox %s_Post, MSGBOX_AUTOCLOSE\n\tend\n\n'
            % (label, trainer, label.replace('EventScript', 'Text'), label.replace('EventScript', 'Text'),
               label.replace('EventScript', 'Text'))
            + text(label.replace('EventScript', 'Text') + '_Intro', intro)
            + text(label.replace('EventScript', 'Text') + '_Defeat', defeat)
            + text(label.replace('EventScript', 'Text') + '_Post', post))


def trainer_double(label, trainer, intro, defeat, notenough, post):
    t = label.replace('EventScript', 'Text')
    return ('%s::\n\ttrainerbattle_double %s, %s_Intro, %s_Defeat, %s_NotEnough\n\tmsgbox %s_Post, MSGBOX_AUTOCLOSE\n\tend\n\n'
            % (label, trainer, t, t, t, t)
            + text(t + '_Intro', intro) + text(t + '_Defeat', defeat) + text(t + '_NotEnough', notenough)
            + text(t + '_Post', post))


def text(label, s):
    return '%s:\n\t.string "%s$"\n\n' % (label, s)


def talk(label, body):
    return '%s::\n%s\n\n' % (label, body.strip('\n'))


# =====================================================================================================
# Route 107 (Dewford, 60x20): sushi-eilandje en een rots-eilandje met "ruïne"
W, H = 60, 20
v = load('Route107', W, H)
SUSHI = rect(25, 7, 31, 10)
SUSHI_SAND = rect(26, 8, 30, 9)
RUIN = rect(42, 6, 49, 11)
RUIN_SAND = rect(43, 7, 48, 10)
restore('Route107', v)
islet('Route107', v, 'dewford', SUSHI, SUSHI_SAND)
islet('Route107', v, 'dewford', RUIN, RUIN_SAND, rocks=[(45, 8)])
save('Route107', v)
P = 'Route107_EventScript_ZV'
objs = [
    obj('OBJ_EVENT_GFX_COOK', 28, 8, P + 'SushiChef'),
    obj('OBJ_EVENT_GFX_SAILOR', 30, 8, P + 'Duncan', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=3),
    obj('OBJ_EVENT_GFX_MR_BRINEYS_BOAT', 24, 9, P + 'Boat', elev=1, move='MOVEMENT_TYPE_FACE_RIGHT'),
    obj('OBJ_EVENT_GFX_MANIAC', 44, 9, P + 'Simon', move='MOVEMENT_TYPE_FACE_RIGHT', trainer=True, sight=3),
    ball(48, 10, 'ITEM_DIVE_BALL', 'FLAG_ITEM_ROUTE_107_DIVE_BALL'),
]
bgs = [hidden(26, 9, 'ITEM_BIG_PEARL', 'FLAG_HIDDEN_ITEM_ROUTE_107_BIG_PEARL'),
       hidden(47, 7, 'ITEM_HARD_STONE', 'FLAG_HIDDEN_ITEM_ROUTE_107_HARD_STONE'),
       sign(45, 9, P + 'Ruin'), sign(46, 9, P + 'Ruin')]
SOLID = {(o['x'], o['y']) for o in objs if o['graphics_id'] != 'OBJ_EVENT_GFX_ITEM_BALL'}
reach('Route 107', v, 'dewford', (0, 8), [(27, 8), (29, 8), (31, 8), (26, 9), (44, 10), (47, 7), (48, 9), (45, 10), (46, 10),
                                         (50, 8), (59, 8)])
scr = talk(P + 'SushiChef', '''
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_ROUTE_107_LEFTOVERS, %sSushiChef_After
	msgbox Route107_Text_ZVSushiChef, MSGBOX_DEFAULT
	giveitem ITEM_LEFTOVERS
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_ROUTE_107_LEFTOVERS
	release
	end
%sSushiChef_After:
	msgbox Route107_Text_ZVSushiChefAfter, MSGBOX_DEFAULT
	release
	end''' % (P, P))
scr += text('Route107_Text_ZVSushiChef',
            "Welcome to SUSHI 107. Omakase only.\\n"
            "Seating: one sandbank.\\p"
            "I used to serve raw fish. Then a\\n"
            "WAILMER watched me through the\\l"
            "window. For three days. Blinking.\\p"
            "Now I serve rice. Just rice.\\n"
            "Here, take the leftovers.\\l"
            "Literally. They're called that.")
scr += text('Route107_Text_ZVSushiChefAfter',
            "Today's special is rice.\\n"
            "Yesterday's special was also rice.\\p"
            "Tomorrow? Don't spoil it.")
scr += talk(P + 'Boat', '\tmsgbox Route107_Text_ZVBoat, MSGBOX_SIGN\n\tend')
scr += text('Route107_Text_ZVBoat', "A boat named the S.S. NIGIRI.\\n"
            "The hull says: 'NOT A DELIVERY BOAT.'\\l"
            "Someone has added: 'UBER?'")
scr += talk(P + 'Ruin', '\tmsgbox Route107_Text_ZVRuin, MSGBOX_SIGN\n\tend')
scr += text('Route107_Text_ZVRuin', "It's a rock.\\p"
            "Someone has scratched into it:\\n"
            "'ANCIENT RUIN. DO NOT TOUCH.\\l"
            "-SIMON'")
scr += trainer_single(P + 'Duncan', 'TRAINER_SAILOR_DUNCAN',
                      "Oi! I've been waiting forty minutes\\n"
                      "for one bowl of rice!\\p"
                      "I'm taking it out on you. That's\\n"
                      "how customer service works!",
                      "Fine. FINE. I'll leave a\\n"
                      "two-star review.",
                      "The rice is actually very good.\\n"
                      "Don't tell him. He'll get ideas.")
scr += trainer_single(P + 'Simon', 'TRAINER_RUIN_MANIAC_SIMON',
                      "Careful! This rock is an ancient\\n"
                      "ruin of the Hoenn sea people!\\p"
                      "Probably! I have no evidence,\\n"
                      "but I DO have a grant!",
                      "My research funding...\\n"
                      "It's slipping away like sand...",
                      "Carbon dating says this rock is\\n"
                      "'a rock'. The lab is clearly biased.")
apply_events('Route107', objs, bgs, scr)

# =====================================================================================================
# Route 126 (Mossdeep, 80x80): picknickbank, Garbage Patch, vogeleilandje, Sirena
W, H = 80, 80
v = load('Route126', W, H)
PICNIC = rect(36, 3, 45, 8)
PICNIC_SAND = rect(37, 4, 44, 7)
TRASH = rect(70, 35, 78, 43)
TRASH_SAND = rect(71, 36, 77, 42)
BIRD = rect(71, 60, 75, 63)
BIRD_SAND = rect(72, 61, 74, 62)
restore('Route126', v)
islet('Route126', v, 'mossdeep', PICNIC, PICNIC_SAND, palms=[(42, 5)])
islet('Route126', v, 'mossdeep', TRASH, TRASH_SAND, grass=rect(74, 39, 76, 41))
islet('Route126', v, 'mossdeep', BIRD, BIRD_SAND)
save('Route126', v)
P = 'Route126_EventScript_ZV'
objs = [
    obj('OBJ_EVENT_GFX_OLD_MAN', 39, 5, P + 'OldCouple', move='MOVEMENT_TYPE_FACE_RIGHT', trainer=True, sight=3),
    obj('OBJ_EVENT_GFX_OLD_WOMAN', 40, 5, P + 'OldCouple', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=3),
    obj('OBJ_EVENT_GFX_WOMAN_3', 72, 40, P + 'Volunteer', move='MOVEMENT_TYPE_WANDER_AROUND'),
    obj('OBJ_EVENT_GFX_MOVING_BOX', 71, 37, P + 'Crate'),
    obj('OBJ_EVENT_GFX_DITTO_DOLL', 77, 37, P + 'Duck'),
    ball(71, 42, 'ITEM_METAL_COAT', 'FLAG_ITEM_ROUTE_126_METAL_COAT'),
    obj('OBJ_EVENT_GFX_MAN_5', 73, 61, P + 'Oswald',
        move='MOVEMENT_TYPE_LOOK_AROUND', trainer=True, sight=4),
    obj('OBJ_EVENT_GFX_SWIMMER_F', 38, 63, P + 'Sirena', elev=1, move='MOVEMENT_TYPE_LOOK_AROUND', trainer=True, sight=4),
]
bgs = [hidden(38, 7, 'ITEM_BERRY_JUICE', 'FLAG_HIDDEN_ITEM_ROUTE_126_BERRY_JUICE'),
       hidden(74, 37, 'ITEM_BLACK_SLUDGE', 'FLAG_HIDDEN_ITEM_ROUTE_126_BLACK_SLUDGE'),
       hidden(74, 62, 'ITEM_PRETTY_FEATHER', 'FLAG_HIDDEN_ITEM_ROUTE_126_PRETTY_FEATHER')]
SOLID = {(o['x'], o['y']) for o in objs if o['graphics_id'] != 'OBJ_EVENT_GFX_ITEM_BALL'}
reach('Route 126', v, 'mossdeep', (70, 50), [(38, 5), (41, 5), (38, 7), (72, 37), (71, 38), (76, 37), (74, 37),
                                           (71, 41), (75, 40), (72, 61), (74, 62), (38, 64), (56, 22), (51, 65)])
scr = trainer_double(P + 'OldCouple', 'TRAINER_OLD_COUPLE_HAL_AND_MAE',
                     "HAL: Fifty years married, and every\\n"
                     "anniversary we picnic on a sandbank.\\p"
                     "MAE: The tide takes the sandbank\\n"
                     "at four. We have until then.\\l"
                     "Make it quick, dear.",
                     "HAL: Mae, the young one won.\\n"
                     "MAE: I heard, Hal. I'm right here.",
                     "HAL: Bring a friend, youngster.\\n"
                     "We only fight as a couple.\\l"
                     "It's in the vows.",
                     "MAE: Hal proposed on this very\\n"
                     "sandbank. It was a different\\l"
                     "sandbank. Sandbanks move.")
scr += talk(P + 'Volunteer', '\tmsgbox Route126_Text_ZVVolunteer, MSGBOX_NPC\n\tend')
scr += text('Route126_Text_ZVVolunteer',
            "Welcome to the GREAT PACIFIDLOG\\n"
            "GARBAGE PATCH. Day 412 of the\\l"
            "clean-up.\\p"
            "So far I've removed one sock.\\n"
            "It came back. With a friend.\\p"
            "The currents bring everything\\n"
            "here. Last week: a whole TV.\\l"
            "Still showing the weather.")
scr += talk(P + 'Crate', '''
	lock
	goto_if_set FLAG_ROUTE_126_CRATE_SOLVED, %sCrate_Done
	msgbox Route126_Text_ZVCrate, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, %sCrate_No
	msgbox Route126_Text_ZVCrateYes, MSGBOX_DEFAULT
	giveitem ITEM_PP_MAX
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_ROUTE_126_CRATE_SOLVED
	release
	end
%sCrate_No:
	msgbox Route126_Text_ZVCrateNo, MSGBOX_DEFAULT
	release
	end
%sCrate_Done:
	msgbox Route126_Text_ZVCrateDone, MSGBOX_DEFAULT
	release
	end''' % (P, P, P, P))
scr += text('Route126_Text_ZVCrate',
            "A crate is floating here. Stamped on\\n"
            "the lid: 'ANSWER ME AND I OPEN.'\\p"
            "It speaks. Somehow.\\p"
            "'What has a bed but never sleeps,\\n"
            "and a mouth but never eats?'\\p"
            "...\\p"
            "'A RIVER. Obviously.\\n"
            "Was that correct?'")
scr += text('Route126_Text_ZVCrateYes',
            "'Thank you. Nobody ever lets me\\n"
            "win.' The lid creaks open.")
scr += text('Route126_Text_ZVCrateNo',
            "'...Then YOU tell me what it is.'\\p"
            "The crate sulks. Loudly.")
scr += text('Route126_Text_ZVCrateDone',
            "The crate is empty. It is thinking\\n"
            "of a new riddle. It's been a while.")
scr += talk(P + 'Duck', '\tmsgbox Route126_Text_ZVDuck, MSGBOX_SIGN\n\tend')
scr += text('Route126_Text_ZVDuck',
            "A pink rubber duck.\\p"
            "On closer inspection: a DITTO.\\n"
            "It has been a duck for so long\\l"
            "it has forgotten how to stop.\\p"
            "It seems happy. Let it be.")
scr += trainer_single(P + 'Oswald', 'TRAINER_BIRD_KEEPER_OSWALD',
                      "I came out here to watch seabirds.\\n"
                      "My birds don't swim. Or float.\\p"
                      "We've been on this rock since\\n"
                      "Tuesday. Battle me, it's something\\l"
                      "to do.",
                      "Squawk.\\n"
                      "...Sorry, that was me.",
                      "If you see a boat, wave it over.\\n"
                      "Not too much. My birds are proud.")
scr += trainer_single(P + 'Sirena', 'TRAINER_SIRENA',
                      "Shh! I'm a MERMAID.\\p"
                      "My lawyer says I have to add:\\n"
                      "'legally a swimmer in a costume.'\\p"
                      "My POKeMON are very rare and\\n"
                      "very tiny. Don't hurt them. Or do.\\l"
                      "It's a battle.",
                      "The tail is rented. I can't afford\\n"
                      "to lose. I just did. Oh no.",
                      "Under the sea it's better, down\\n"
                      "where it's wetter. I sing that\\l"
                      "to the WAILMER. They leave.")
apply_events('Route126', objs, bgs, scr)

# =====================================================================================================
# Route 127 (Mossdeep, 80x80): gestrande Wailmer, toerist, tweeling
v = load('Route127', W, H)
WAIL_SAND = rect(10, 7, 13, 9)
restore('Route127', v)
for (x, y) in rect(9, 6, 14, 10):  # zandvlak midden in de ondiepte: alles eromheen moet ondiep water zijn
    assert beh(v[y][x], 'mossdeep') == 'MB_SHALLOW_WATER', (x, y, hex(v[y][x]))
    ORIG.setdefault('Route127', {}).setdefault('%d,%d' % (x, y), v[y][x])
for (x, y) in WAIL_SAND:
    v[y][x] = cell(SAND[shape(WAIL_SAND, x, y)], 'mossdeep')
save('Route127', v)
P = 'Route127_EventScript_ZV'
objs = [
    obj('OBJ_EVENT_GFX_SPECIES(WAILMER)', 11, 8, P + 'Wailmer', flag='FLAG_ROUTE_127_WAILMER_RESCUED'),
    obj('OBJ_EVENT_GFX_PICNICKER', 13, 9, P + 'Marisol', move='MOVEMENT_TYPE_FACE_LEFT', trainer=True, sight=3),
    obj('OBJ_EVENT_GFX_MAN_1', 54, 61, P + 'Tourist', move='MOVEMENT_TYPE_LOOK_AROUND'),
    obj('OBJ_EVENT_GFX_TWIN', 56, 59, P + 'Twins', move='MOVEMENT_TYPE_FACE_DOWN', trainer=True, sight=3),
    obj('OBJ_EVENT_GFX_TWIN', 57, 59, P + 'Twins', move='MOVEMENT_TYPE_FACE_DOWN', trainer=True, sight=3),
]
bgs = [hidden(11, 16, 'ITEM_BIG_PEARL', 'FLAG_HIDDEN_ITEM_ROUTE_127_BIG_PEARL'),
       hidden(49, 25, 'ITEM_MYSTIC_WATER', 'FLAG_HIDDEN_ITEM_ROUTE_127_MYSTIC_WATER'),
       hidden(59, 73, 'ITEM_DAMP_ROCK', 'FLAG_HIDDEN_ITEM_ROUTE_127_DAMP_ROCK')]
SOLID = {(o['x'], o['y']) for o in objs if o['graphics_id'] != 'OBJ_EVENT_GFX_ITEM_BALL'}
reach('Route 127', v, 'mossdeep', (30, 30), [(10, 8), (12, 8), (11, 7), (12, 9), (53, 61), (56, 60), (57, 60),
                                           (11, 16), (49, 25), (59, 73), (14, 6)])
scr = talk(P + 'Wailmer', '''
	lock
	faceplayer
	msgbox Route127_Text_ZVWailmer, MSGBOX_DEFAULT
	playmoncry SPECIES_WAILMER, CRY_MODE_NORMAL
	waitmoncry
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	setflag FLAG_ROUTE_127_WAILMER_RESCUED
	fadescreen FADE_FROM_BLACK
	msgbox Route127_Text_ZVWailmerGone, MSGBOX_DEFAULT
	giveitem ITEM_SHELL_BELL
	release
	end''')
scr += text('Route127_Text_ZVWailmer',
            "A WAILMER is stranded on the\\n"
            "sand. It looks at you like you\\l"
            "owe it money.\\p"
            "You push. And push. It rolls into\\n"
            "the sea with the grace of a\\l"
            "dropped piano.")
scr += text('Route127_Text_ZVWailmerGone',
            "Far away, a spout of water.\\n"
            "Something shiny lands at your feet.\\p"
            "A tip. From a whale.")
scr += trainer_single(P + 'Marisol', 'TRAINER_RANGER_MARISOL',
                      "Stand back! This WAILMER has been\\n"
                      "stranded for six hours.\\p"
                      "I've been observing it. Taking\\n"
                      "notes. Very important notes.\\l"
                      "Mostly drawings.",
                      "You're right. Pushing it back\\n"
                      "would also have been an option.",
                      "Ranger protocol says observe, don't\\n"
                      "interfere. Ranger protocol has\\l"
                      "never met a sad whale.")
scr += talk(P + 'Tourist', '\tmsgbox Route127_Text_ZVTourist, MSGBOX_NPC\n\tend')
scr += text('Route127_Text_ZVTourist',
            "Excuse me, is this Kalos?\\p"
            "My map says the hotel is right\\n"
            "here. The map is of Kalos.\\p"
            "...Is it upside down? Oh. Oh no.\\n"
            "Then I swam the wrong way for\\l"
            "two weeks.\\p"
            "Still. Five stars. Great water.")
scr += trainer_double(P + 'Twins', 'TRAINER_TWINS_PIP_AND_PEP',
                      "PIP: We swam here on a floatie!\\n"
                      "PEP: The floatie popped!\\p"
                      "PIP: Now we live here!\\n"
                      "PEP: Mom doesn't know yet!",
                      "PIP: We lost!\\n"
                      "PEP: Like the floatie!",
                      "PIP: Two against one is unfair.\\n"
                      "PEP: Come back with a friend!",
                      "PIP: If you see Mom, say we're\\n"
                      "at a sleepover.\\p"
                      "PEP: With a sandbank!")
apply_events('Route127', objs, bgs, scr)

# =====================================================================================================
# Onderwater: zeewier (wilde encounters) + verborgen items
# bodem zonder/met opduiken -> zeewier zonder/met opduiken; 0x25B/0x256 = vlakke bodem van de trog (128)
SEAWEED = {0x2A9: 0x281, 0x216: 0x201, 0x25B: 0x281, 0x256: 0x281}


def seaweed(layout, w, h, patches, mapname, objs, bgs, scr):
    v = load(layout, w, h)
    restore(layout, v)
    orig = ORIG.setdefault(layout, {})
    n = 0
    for (cx, cy, r) in patches:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r - 1, cx + r + 2):
                if not (0 <= x < w and 0 <= y < h): continue
                d = ((x - cx) / (r + 1.0)) ** 2 + ((y - cy) / (r + 0.5)) ** 2
                if d <= 1.0 and random.random() < 0.85 and (v[y][x] & 0x3FF) in SEAWEED:
                    orig.setdefault('%d,%d' % (x, y), v[y][x])
                    v[y][x] = (v[y][x] & ~0x3FF) | SEAWEED[v[y][x] & 0x3FF]; n += 1
    for b in bgs + [o for o in objs]:
        c = v[b['y']][b['x']]
        want_block = b.get('type') == 'sign'
        assert bool(c & BLOCK) == want_block, '%s (%d,%d) %s' % (layout, b['x'], b['y'], 'muur' if c & BLOCK else 'vrij')
    save(layout, v)
    print('%s: %d zeewiertegels' % (layout, n))
    apply_events(mapname, objs, bgs, scr)


# vanilla had op deze vier kaarten geen zeewier: alles wat 0x201/0x281 is, is van ons

P = 'Underwater_Route105_EventScript_ZV'
scr = talk(P + 'Grave', '\tmsgbox Underwater_Route105_Text_ZVGrave, MSGBOX_SIGN\n\tend')
scr += text('Underwater_Route105_Text_ZVGrave',
            "Words are carved into the rock:\\p"
            "'HERE LIES CAPTAIN BARNABY.\\n"
            "HE SAID HE COULD HOLD HIS BREATH\\l"
            "FOR AN HOUR.'\\p"
            "'HE COULD NOT.'")
seaweed('Underwater_Route105', 40, 80, [(8, 13, 2), (15, 32, 1), (19, 68, 1), (9, 23, 1)], 'Underwater_Route105',
        [ball(14, 27, 'ITEM_BIG_NUGGET', 'FLAG_ITEM_UNDERWATER_105_BIG_NUGGET')],
        [sign(11, 25, P + 'Grave'),
         hidden(5, 15, 'ITEM_DEEP_SEA_TOOTH', 'FLAG_HIDDEN_ITEM_UNDERWATER_105_DEEP_SEA_TOOTH'),
         hidden(18, 33, 'ITEM_HEART_SCALE', 'FLAG_HIDDEN_ITEM_UNDERWATER_105_HEART_SCALE'),
         hidden(20, 67, 'ITEM_BIG_PEARL', 'FLAG_HIDDEN_ITEM_UNDERWATER_105_BIG_PEARL')], scr)

P = 'Underwater_Route125_EventScript_ZV'
scr = talk(P + 'Diver', '\tmsgbox Underwater_Route125_Text_ZVDiver, MSGBOX_NPC\n\tend')
scr += text('Underwater_Route125_Text_ZVDiver',
            "...!\\p"
            "(He is holding his breath for\\n"
            "charity. He points at a sign:)\\p"
            "'DAY 3. DON'T MAKE ME LAUGH.'\\p"
            "(His face is very blue. It could\\n"
            "be the water. It is not the water.)")
seaweed('Underwater_Route125', 80, 40, [(12, 13, 2), (19, 14, 1), (47, 31, 1), (54, 23, 1)], 'Underwater_Route125',
        [obj('OBJ_EVENT_GFX_SWIMMER_M', 16, 13, P + 'Diver', move='MOVEMENT_TYPE_LOOK_AROUND')],
        [hidden(9, 14, 'ITEM_NEVER_MELT_ICE', 'FLAG_HIDDEN_ITEM_UNDERWATER_125_NEVER_MELT_ICE'),
         hidden(44, 32, 'ITEM_HEART_SCALE', 'FLAG_HIDDEN_ITEM_UNDERWATER_125_HEART_SCALE')], scr)

seaweed('Underwater_Route128', 120, 40, [(38, 10, 3), (56, 12, 2), (42, 30, 3), (72, 21, 1), (27, 22, 1)],
        'Underwater_Route128', [],
        [hidden(60, 12, 'ITEM_DEEP_SEA_SCALE', 'FLAG_HIDDEN_ITEM_UNDERWATER_128_DEEP_SEA_SCALE'),
         hidden(40, 34, 'ITEM_STAR_PIECE', 'FLAG_HIDDEN_ITEM_UNDERWATER_128_STAR_PIECE')], '')

seaweed('Underwater_Route129', 80, 40, [(16, 14, 2), (21, 16, 1), (35, 22, 1), (26, 6, 1)], 'Underwater_Route129', [],
        [hidden(13, 17, 'ITEM_DRAGON_SCALE', 'FLAG_HIDDEN_ITEM_UNDERWATER_129_DRAGON_SCALE'),
         hidden(24, 15, 'ITEM_PEARL', 'FLAG_HIDDEN_ITEM_UNDERWATER_129_PEARL'),
         hidden(31, 23, 'ITEM_HEART_SCALE', 'FLAG_HIDDEN_ITEM_UNDERWATER_129_HEART_SCALE')], '')

assert not FAIL, FAIL
json.dump(ORIG, open(ORIG_PATH, 'w'), indent=0, sort_keys=True)
print('ok')
