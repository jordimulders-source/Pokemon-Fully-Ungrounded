"""Project Grounded: het Tao-eiland (was Dragonspine Isle) rechts van Route 129 (verbinding; Town Map x 26-27, y 10).
Reshiram en Zekrom bovenin een ruïnetoren (Dragonspiral-hommage), Kyurem (neutraal) in een ijskelder onder de
Dragon's Den, en Ghetsis als post-league superboss die je de DNA Splicers geeft. Deterministisch en idempotent.

  TaoIsland              De rotspiek van de Sky Pillar (kopie van SkyPillar_Outside, General + Pacifidlog) in zee,
                         met de toren omhoog doorgetrokken en een zandstrand eronder (General-zand-autotiler).
                         De linker kolommen zijn alleen water (andere secondary dan Route 129; het script controleert
                         het). Deur in de toren -> TaoIsland_Tower1F; grot in de heuvel -> TaoIsland_Den.
  TaoIsland_Tower1F/2F/3F/Top
                         Hergebruiken de schone Sky Pillar-layouts (1F, 2F, 5F, Top). Bovenin slapen RESHIRAM en
                         ZEKROM (lv 70, pas na de Hall of Fame wakker); allebei te vangen.
  TaoIsland_Den          De oude Dragon's Den (Meteor Falls-stijl, Map-klasse van meteor_falls_ext.py). Een DRAGONITE
                         slaapt op een gat in de bovenhal; als je beide broers hebt, is hij weg.
  TaoIsland_FrostHollow  Hergebruikt de ijskamer van Shoal Cave: GHETSIS (superboss, DNA Splicers) en KYUREM (lv 70).

Ook: trainers (opponents.h-blok 'tao_island', id 1060-1067, en trainers.party), wilde Pokemon, flags
(FLAG_GROUNDED 430-469). Teksten zijn placeholders in de huisstijl (Jordi herschrijft ze).

Gebruik: python3 tools/grounded/maptools/tao_island.py [rendermap]"""
import importlib.util, json, os, random, re, struct, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chimney_ext as cx            # zet ook de werkmap op de repo-root
import ogerpon_quest as oq
import sea_market_steam as sms
import tapu_cresselia as tc
import meteor_falls_ext as mf

t, mt, WATER, reach = sms.t, sms.mt, sms.WATER, cx.reach

_spec = importlib.util.spec_from_file_location('dialogen_import', 'tools/dialogen/import.py')
dimp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dimp)


# ====================================================================== hulpjes
def text(label, s):
    out = '%s:\n' % label
    for part in dimp.to_strings(s):
        out += '\t.string "%s"\n' % part
    return out + '\n'


class Scr:
    """Verzamelt scripts en teksten van één kaart."""

    def __init__(self, name, header):
        self.name, self.P, self.T = name, name + '_EventScript_', name + '_Text_'
        self.head, self.code, self.texts = header, [], []

    def npc(self, key, s, kind='MSGBOX_NPC'):
        self.code.append('%s%s::\n\tmsgbox %s%s, %s\n\tend\n' % (self.P, key, self.T, key, kind))
        self.texts.append(text(self.T + key, s))
        return self.P + key

    def trainer(self, key, const, intro, defeat, post):
        P, T = self.P + key, self.T + key
        self.code.append(f'{P}::\n\ttrainerbattle_single TRAINER_{const}, {T}Intro, {T}Defeat\n'
                         f'\tmsgbox {T}Post, MSGBOX_AUTOCLOSE\n\tend\n')
        for k, s in (('Intro', intro), ('Defeat', defeat), ('Post', post)):
            self.texts.append(text(T + k, s))
        return P

    def raw(self, code, texts=()):
        self.code.append(code)
        for label, s in texts:
            self.texts.append(text(self.T + label, s))

    def write(self):
        s = self.head.rstrip('\n') + '\n\n' + '\n'.join(self.code) + \
            '\n@ ---------------------------------------------------------------- teksten (placeholders, Jordi herschrijft ze)\n' + \
            ''.join(self.texts)
        open('data/maps/%s/scripts.inc' % self.name, 'w').write(s.rstrip('\n') + '\n')


def register_layout(name, const, W, H, primary, secondary):
    lj = open('data/layouts/layouts.json').read()
    entry = '''    {
      "id": "LAYOUT_%s",
      "name": "%s_Layout",
      "width": %d,
      "height": %d,
      "primary_tileset": "%s",
      "secondary_tileset": "%s",
      "border_filepath": "data/layouts/%s/border.bin",
      "blockdata_filepath": "data/layouts/%s/map.bin"
    }''' % (const, name, W, H, primary, secondary, name, name)
    if '"LAYOUT_%s"' % const in lj:
        i = lj.index('"id": "LAYOUT_%s"' % const); s = lj.rindex('    {', 0, i); e = lj.index('    }', i) + 5
        lj = lj[:s] + entry + lj[e:]
    else:
        i = lj.rindex('    }\n  ]')
        lj = lj[:i + 5] + ',\n' + entry + lj[i + 5:]
    json.loads(lj)
    open('data/layouts/layouts.json', 'w').write(lj)


def layout(lid):
    return [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id') == lid][0]


def read_layout(lid):
    L = layout(lid)
    return oq.read_layout(L['blockdata_filepath'], L['width'], L['height']), L['width'], L['height']


def warp(x, y, dest, wid, elev=0):
    return {'x': x, 'y': y, 'elevation': elev, 'dest_map': 'MAP_' + dest, 'dest_warp_id': str(wid)}


def obj(gfx, x, y, script, flag='0', move='MOVEMENT_TYPE_FACE_DOWN', local_id=None, elev=3, sight='0'):
    o = sms.obj(gfx, x, y, script, flag, move=move, local_id=local_id, elev=elev)
    o['trainer_sight_or_berry_tree_id'] = sight
    return o


def tr(gfx, x, y, script, face, sight, elev=3, flag='0', local_id=None):
    o = obj(gfx, x, y, script, flag, move='MOVEMENT_TYPE_FACE_' + face, elev=elev, sight=str(sight), local_id=local_id)
    o['trainer_type'] = 'TRAINER_TYPE_NORMAL'
    return o


def ball(x, y, it, flag, elev=3):
    return obj('OBJ_EVENT_GFX_ITEM_BALL', x, y, 'Common_EventScript_FindItem', flag, 'MOVEMENT_TYPE_LOOK_AROUND',
               elev=elev, sight=it)


def sign(x, y, script):
    return {'type': 'sign', 'x': x, 'y': y, 'elevation': 0, 'player_facing_dir': 'BG_EVENT_PLAYER_FACING_NORTH',
            'script': script}


def write_map(name, const, layout_id, objs, warps, coords, bgs, **kw):
    sms.write_map(name, const, objs, warps, coords, bgs, **kw)
    p = 'data/maps/%s/map.json' % name
    m = json.load(open(p))
    m['layout'] = layout_id
    open(p, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    oq.register_map(name)


# ====================================================================== flags (FLAG_GROUNDED 430-469 = dit script)
FLAGS = [
    (430, 'FLAG_HIDDEN_ITEM_TAO_ISLAND_DRAGON_SCALE', 'Tao-eiland: verborgen Dragon Scale'),
    (431, 'FLAG_HIDDEN_ITEM_TAO_ISLAND_STAR_PIECE', 'Tao-eiland: verborgen Star Piece'),
    (432, 'FLAG_ITEM_TAO_ISLAND_MAX_REVIVE', 'Tao-eiland: Max Revive'),
    (433, 'FLAG_ITEM_TAO_DEN_PP_UP', "Dragon's Den: PP Up"),
    (434, 'FLAG_ITEM_TAO_DEN_MAX_ELIXIR', "Dragon's Den: Max Elixir"),
    (435, 'FLAG_HIDDEN_ITEM_TAO_DEN_BIG_NUGGET', "Dragon's Den: verborgen Big Nugget"),
    (436, 'FLAG_HIDE_TAO_RESHIRAM', 'Tao-toren: Reshiram gevangen/verslagen'),
    (437, 'FLAG_HIDE_TAO_ZEKROM', 'Tao-toren: Zekrom gevangen/verslagen'),
    (438, 'FLAG_HIDE_TAO_DEN_DRAGONITE', "Dragon's Den: Dragonite van het gat (na beide broers)"),
    (439, 'FLAG_HIDE_TAO_KYUREM', 'Frost Hollow: Kyurem gevangen/verslagen'),
    (440, 'FLAG_HIDE_TAO_GHETSIS', 'Frost Hollow: Ghetsis vertrokken (DNA Splicers gekregen)'),
    (441, 'FLAG_ITEM_TAO_TOWER_2F_DRAGON_FANG', 'Tao-toren 2F: Dragon Fang'),
    (442, 'FLAG_ITEM_TAO_TOWER_3F_FULL_RESTORE', 'Tao-toren 3F: Full Restore'),
    (443, 'FLAG_ITEM_TAO_FROST_NEVER_MELT_ICE', 'Frost Hollow: Never-Melt Ice'),
    (444, 'FLAG_ITEM_TAO_FROST_ICE_STONE', 'Frost Hollow: Ice Stone'),
]


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// tao_island { (tools/grounded/maptools/tao_island.py; FLAG_GROUNDED 430-469)\n'
    for n, name, why in FLAGS:
        assert 430 <= n <= 469
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// tao_island {' in s:
        i = s.index('// tao_island {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('\n', s.index('// Verdeling (houd bij!)')) + 1
        anchor = s.index('\n', anchor) + 1
        s = s[:anchor] + blk + '\n' + s[anchor:]
    open(p, 'w').write(s)


# ====================================================================== het eiland
IW, IH = 44, 38
OX, OY = 12, 7                      # plek van de Sky Pillar-rotspiek (28x23) in de kaart
SAFE_LEFT = 9                       # linker kolommen alleen primary (grens met Route 129)
DOOR = (OX + 14, OY + 5)            # torendeur
MOUND = (OX + 17, OY + 13)          # grot in de heuvel (plateau) -> Dragon's Den, tweede uitgang
ARCH = (OX + 15, OY + 20)           # grotmond aan het strand -> Dragon's Den (de Den is de doorgang naar het plateau)
BEACH_ROWS = {30: (22, 31), 31: (20, 33), 32: (18, 35), 33: (18, 35), 34: (19, 34), 35: (21, 32)}


def tao_island():
    name, const = 'TaoIsland', 'TAO_ISLAND'
    crag, CW, CH = read_layout('LAYOUT_SKY_PILLAR_OUTSIDE')
    g = [[t(WATER, False, 1)] * IW for _ in range(IH)]
    for y in range(CH):
        for x in range(CW):
            g[OY + y][OX + x] = crag[y][x]
    # rotsblok onderaan rechts (alleen de bovenkant stond in de kaart) wordt water
    for x in range(22, 27):
        g[OY + 22][OX + x] = t(WATER, False, 1)
    # de toren omhoog doortrekken (rijen wisselen: ramen / muur)
    cols = [x for x in range(CW) if mt(crag[0][x]) in range(0x2a0, 0x2a5)]
    assert len(cols) == 5, cols
    for y in range(OY):
        src = crag[(OY - y) % 2]
        for x in cols:
            g[y][OX + x] = src[x]
    # zandstrand onder de spiek (de zandgang van de Sky Pillar loopt erin door)
    land = [[mt(g[y][x]) != WATER for x in range(IW)] for y in range(IH)]
    for y, (a, b) in BEACH_ROWS.items():
        for x in range(a, b + 1):
            land[y][x] = True
    for y in range(OY + 23, IH):
        for x in range(IW):
            if land[y][x]:
                g[y][x] = tc.sand_tile(land, x, y)
    tc.place_rocks(g, 9, 643, lambda x, y: (x >= SAFE_LEFT + 1 and (x < OX - 2 or x > OX + CW + 1 or y > OY + CH + 1))
                   and not any(land[yy][xx] for yy in range(max(0, y - 2), min(IH, y + 4))
                               for xx in range(max(0, x - 2), min(IW, x + 4))))

    S = Scr(name, '''@ Project Grounded: het Tao-eiland (was Dragonspine Isle), rechts van Route 129.
@ Kaart en scripts: tools/grounded/maptools/tao_island.py. Toren -> RESHIRAM en ZEKROM, Dragon's Den -> KYUREM en
@ GHETSIS. Teksten zijn placeholders.
TaoIsland_MapScripts::
	.byte 0
''')
    P = S.P
    S.trainer('Vernon', 'TAO_VERNON',
              "Welcome to TAO ISLAND! Formerly DRAGONSPINE ISLE. We rebranded.\n\nThe dragons didn't notice. "
              "They still bite in the old font.",
              "Bitten. Again.",
              "I've been bitten 412 times. I keep count. It keeps me humble.\n\n"
              "That tower is three thousand years old. The “No Swimming” sign is older.")
    S.trainer('Saela', 'TAO_SAELA',
              "I came here to train with dragons. Mostly I've been training my running.",
              "Running away it is.",
              "Two dragons sleep at the top of that tower. One white, one black. Brothers.\n\n"
              "They haven't spoken in three hundred years. Honestly? Relatable.")
    S.npc('Adjuster',
          "I'm the island's insurance adjuster.\n\n"
          "Claims this week: fourteen scorched tents, three eaten canoes and one man who “just wanted to pet it.”\n\n"
          "All denied. Dragons count as an act of God. The tower counts as two acts of God. Double denied.")
    S.npc('Sign', "TAO TOWER\nBuilt: yes. Visitors: at own risk.\nLegendary dragons: do not poke.", 'MSGBOX_SIGN')
    objs = [tr('OBJ_EVENT_GFX_MAN_5', 21, 32, P + 'Vernon', 'RIGHT', 4),
            tr('OBJ_EVENT_GFX_WOMAN_5', OX + 10, OY + 8, P + 'Saela', 'DOWN', 3),
            obj('OBJ_EVENT_GFX_MAN_1', 32, 33, P + 'Adjuster', move='MOVEMENT_TYPE_LOOK_AROUND'),
            ball(OX + 8, OY + 9, 'ITEM_MAX_REVIVE', 'FLAG_ITEM_TAO_ISLAND_MAX_REVIVE')]
    bgs = [cx.hidden(34, 33, 'ITEM_DRAGON_SCALE', 'FLAG_HIDDEN_ITEM_TAO_ISLAND_DRAGON_SCALE'),
           cx.hidden(OX + 11, OY + 12, 'ITEM_STAR_PIECE', 'FLAG_HIDDEN_ITEM_TAO_ISLAND_STAR_PIECE'),
           sign(DOOR[0] - 2, DOOR[1] + 1, P + 'Sign')]
    warps = [warp(DOOR[0], DOOR[1], 'TAO_ISLAND_TOWER_1F', 0), warp(ARCH[0], ARCH[1], 'TAO_ISLAND_DEN', 0),
             warp(MOUND[0], MOUND[1], 'TAO_ISLAND_DEN', 2)]
    # ---- controles
    blocked = {(o['x'], o['y']) for o in objs}
    beach = (27, 33)
    beach_walk = reach(g, [beach], blocked=blocked)
    plateau = reach(g, [(MOUND[0], MOUND[1] + 1)], blocked=blocked)
    walk = beach_walk | plateau
    surf = reach(g, [(0, y) for y in range(IH)])
    assert any(cx.next_to(c, surf) for c in beach_walk), 'strand niet bereikbaar vanaf zee'
    assert (ARCH[0], ARCH[1] + 1) in beach_walk, 'grotmond niet bereikbaar vanaf het strand'
    assert (DOOR[0], DOOR[1] + 1) in plateau, 'torendeur niet bereikbaar vanaf het plateau'
    assert not (plateau & beach_walk), 'plateau hoort alleen via de Den bereikbaar te zijn'
    for o in objs:
        assert cx.next_to((o['x'], o['y']), walk), ('object onbereikbaar', o['script'])
        for c in cx.sight(o):
            assert c in walk or not cx.walkable(g[c[1]][c[0]]), ('zichtlijn over water', o['script'])
    for b in bgs:
        assert (b['x'], b['y']) in walk or b['type'] == 'sign', ('verborgen item onbereikbaar', b)
    assert all(mt(g[y][x]) < 0x200 for y in range(IH) for x in range(SAFE_LEFT)), 'linker kolommen niet primary'
    sms.save(g, name)
    sms.border(name, t(WATER, False, 1))
    register_layout(name, const, IW, IH, 'gTileset_General', 'gTileset_Pacifidlog')
    write_map(name, const, 'LAYOUT_' + const, objs, warps, [], bgs, music='MUS_ROUTE120', weather='WEATHER_SHADE',
              region_map_section='MAPSEC_TAO_ISLAND',
              connections=[{'map': 'MAP_ROUTE129', 'offset': 0, 'direction': 'left'}])
    S.write()
    return name


# ====================================================================== de toren (schone Sky Pillar-layouts)
TOWER = dict(music='MUS_MT_CHIMNEY', weather='WEATHER_NONE', map_type='MAP_TYPE_UNDERGROUND', allow_cycling=False,
             allow_escaping=True, show_map_name=False, region_map_section='MAPSEC_TAO_ISLAND')


def check_room(lid, objs, start, bgs=()):
    g, W, H = read_layout(lid)
    blocked = {(o['x'], o['y']) for o in objs}
    walk = reach(g, [start], blocked=blocked)
    for o in objs:
        assert cx.next_to((o['x'], o['y']), walk), (lid, 'object onbereikbaar', o['script'], o['x'], o['y'])
        assert not cx.walkable(g[o['y']][o['x']]) or True
        for c in cx.sight(o):
            assert c in walk, (lid, 'zichtlijn', o['script'], c)
    for b in bgs:
        assert (b['x'], b['y']) in walk, (lid, b)
    return walk


def tower():
    names = []
    # 1F
    S = Scr('TaoIsland_Tower1F', '''@ Project Grounded: Tao-toren 1F (layout van de schone Sky Pillar 1F). tools/grounded/maptools/tao_island.py
TaoIsland_Tower1F_MapScripts::
	.byte 0
''')
    S.npc('Guide', "Welcome to TAO TOWER. I'm the tour guide.\n\n"
                   "On your left: a wall. On your right: also a wall. Upstairs: two gods who hate each other.\n\n"
                   "The tour ends here. I don't go upstairs. Nobody pays me enough to go upstairs.")
    objs = [obj('OBJ_EVENT_GFX_WOMAN_2', 3, 11, S.P + 'Guide', move='MOVEMENT_TYPE_FACE_RIGHT')]
    check_room('LAYOUT_SKY_PILLAR_1F_CLEAN', objs, (6, 12))
    write_map('TaoIsland_Tower1F', 'TAO_ISLAND_TOWER_1F', 'LAYOUT_SKY_PILLAR_1F_CLEAN', objs,
              [warp(6, 13, 'TAO_ISLAND', 0), warp(7, 13, 'TAO_ISLAND', 0), warp(10, 1, 'TAO_ISLAND_TOWER_2F', 0)],
              [], [], **TOWER)
    S.write(); names.append(S.name)
    # 2F: team ZEKROM
    S = Scr('TaoIsland_Tower2F', '''@ Project Grounded: Tao-toren 2F (layout van de schone Sky Pillar 2F). tools/grounded/maptools/tao_island.py
TaoIsland_Tower2F_MapScripts::
	.byte 0
''')
    S.trainer('Jun', 'TAO_JUN',
              "I'm Team ZEKROM! Ideals! Lightning! Being right without any evidence at all!",
              "My ideals have been... grounded.",
              "Upstairs is a girl who's Team RESHIRAM. We've been arguing since Tuesday.\n\nTuesday of last year.")
    objs = [tr('OBJ_EVENT_GFX_MAN_3', 8, 11, S.P + 'Jun', 'LEFT', 4),
            ball(12, 6, 'ITEM_DRAGON_FANG', 'FLAG_ITEM_TAO_TOWER_2F_DRAGON_FANG')]
    check_room('LAYOUT_SKY_PILLAR_2F_CLEAN', objs, (10, 2))
    write_map('TaoIsland_Tower2F', 'TAO_ISLAND_TOWER_2F', 'LAYOUT_SKY_PILLAR_2F_CLEAN', objs,
              [warp(10, 1, 'TAO_ISLAND_TOWER_1F', 2), warp(3, 1, 'TAO_ISLAND_TOWER_3F', 0)], [], [], **TOWER)
    S.write(); names.append(S.name)
    # 3F: team RESHIRAM
    S = Scr('TaoIsland_Tower3F', '''@ Project Grounded: Tao-toren 3F (layout van de schone Sky Pillar 5F). tools/grounded/maptools/tao_island.py
TaoIsland_Tower3F_MapScripts::
	.byte 0
''')
    S.trainer('Ying', 'TAO_YING',
              "Team RESHIRAM! Truth! Fire! Being right, with footnotes!",
              "That's... true. Sadly.",
              "The brothers sleep on the roof. Wake one, and the other pretends it didn't notice.\n\n"
              "Wake both and it's basically Christmas dinner.")
    objs = [tr('OBJ_EVENT_GFX_WOMAN_5', 6, 12, S.P + 'Ying', 'RIGHT', 4),
            ball(1, 6, 'ITEM_FULL_RESTORE', 'FLAG_ITEM_TAO_TOWER_3F_FULL_RESTORE')]
    check_room('LAYOUT_SKY_PILLAR_5F_CLEAN', objs, (3, 2))
    write_map('TaoIsland_Tower3F', 'TAO_ISLAND_TOWER_3F', 'LAYOUT_SKY_PILLAR_5F_CLEAN', objs,
              [warp(3, 1, 'TAO_ISLAND_TOWER_2F', 1), warp(10, 1, 'TAO_ISLAND_TOWER_TOP', 0)], [], [], **TOWER)
    S.write(); names.append(S.name)
    # Top: de broers
    S = Scr('TaoIsland_TowerTop', '''@ Project Grounded: dak van de Tao-toren (layout van de schone Sky Pillar Top). RESHIRAM en ZEKROM slapen hier,
@ elk aan een eigen kant ("de broers kunnen niet samen in een kamer"); pas na de Hall of Fame wakker. Na de tweede
@ broer verdwijnt de DRAGONITE van het gat in de Dragon's Den (-> KYUREM). tools/grounded/maptools/tao_island.py
TaoIsland_TowerTop_MapScripts::
	.byte 0
''')
    for mon, other, trans in (('Reshiram', 'Zekrom', 'RESHIRAM'), ('Zekrom', 'Reshiram', 'ZEKROM')):
        P, T = S.P + mon, S.T + mon
        S.raw(f'''{P}::
	lock
	goto_if_unset FLAG_SYS_GAME_CLEAR, {P}Asleep
	msgbox {T}Wake, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_{trans}, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_{trans}, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}Stays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}Stays
	removeobject LOCALID_TAO_{trans}
	setflag FLAG_HIDE_TAO_{trans}
	call {S.P}CheckBrothers
{P}Stays::
	release
	end

{P}Asleep::
	msgbox {T}Asleep, MSGBOX_DEFAULT
	release
	end
''')
    S.raw(f'''{S.P}CheckBrothers::
	goto_if_unset FLAG_HIDE_TAO_RESHIRAM, {S.P}CheckBrothersEnd
	goto_if_unset FLAG_HIDE_TAO_ZEKROM, {S.P}CheckBrothersEnd
	setflag FLAG_HIDE_TAO_DEN_DRAGONITE
	msgbox {S.T}ColdWind, MSGBOX_DEFAULT
{S.P}CheckBrothersEnd::
	return

{S.P}Elder::
	lock
	faceplayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, {S.P}ElderEarly
	goto_if_set FLAG_HIDE_TAO_DEN_DRAGONITE, {S.P}ElderBoth
	msgbox {S.T}Elder, MSGBOX_DEFAULT
	release
	end

{S.P}ElderEarly::
	msgbox {S.T}ElderEarly, MSGBOX_DEFAULT
	release
	end

{S.P}ElderBoth::
	msgbox {S.T}ElderBoth, MSGBOX_DEFAULT
	release
	end
''', [('ReshiramAsleep', "RESHIRAM is asleep. It's giving off heat like a radiator someone forgot to turn off."),
      ('ZekromAsleep', "ZEKROM is asleep. Your hair stands up. All of it. Even the hair you didn't know you had."),
      ('ReshiramWake', "RESHIRAM wakes up!\n\nIt glances across the roof, decides its brother is still asleep, "
                       "and gives you its full attention."),
      ('ZekromWake', "ZEKROM wakes up!\n\nIt was never asleep. It was pretending, so it wouldn't have to talk to "
                     "its brother."),
      ('ColdWind', "Far below the island, something lets out a long, freezing sigh.\n\n"
                   "It sounds like it was waiting for both of them to leave first."),
      ('ElderEarly', "Two brothers sleep up here, RESHIRAM and ZEKROM. They fell out three hundred years ago over "
                     "who got the bigger side of the roof.\n\nNow neither will leave, in case the other one takes it.\n\n"
                     "They only wake up for a CHAMPION. Snobs, the both of them."),
      ('Elder', "Go on, CHAMPION, wake one. The other will pretend to be asleep.\n\n"
                "It is not asleep. It is listening. It has always been listening."),
      ('ElderBoth', "Both of them gone? Then who's been snoring under the DRAGON'S DEN all these years?\n\n"
                    "Something cold, I'd wager. Something that misses its brothers.")])
    objs = [obj('OBJ_EVENT_GFX_SPECIES(RESHIRAM)', 12, 4, S.P + 'Reshiram', 'FLAG_HIDE_TAO_RESHIRAM',
                local_id='LOCALID_TAO_RESHIRAM'),
            obj('OBJ_EVENT_GFX_SPECIES(ZEKROM)', 16, 4, S.P + 'Zekrom', 'FLAG_HIDE_TAO_ZEKROM',
                local_id='LOCALID_TAO_ZEKROM'),
            obj('OBJ_EVENT_GFX_OLD_MAN', 10, 11, S.P + 'Elder', move='MOVEMENT_TYPE_FACE_DOWN')]
    check_room('LAYOUT_SKY_PILLAR_TOP_CLEAN', objs, (16, 15))
    top = dict(TOWER, map_type='MAP_TYPE_ROUTE', weather='WEATHER_NONE')
    write_map('TaoIsland_TowerTop', 'TAO_ISLAND_TOWER_TOP', 'LAYOUT_SKY_PILLAR_TOP_CLEAN', objs,
              [warp(16, 14, 'TAO_ISLAND_TOWER_3F', 1)], [], [], **top)
    S.write(); names.append(S.name)
    return names


# ====================================================================== Dragon's Den (zijgrot)
NW, NH = 36, 40
DEN_EXIT = (17, 34)
DEN_EXIT2 = (27, 34)                 # tweede uitgang -> heuvel op het plateau
HOLE = (22, 4)                       # grotgat in de stalactietenwand van de bovenhal -> Frost Hollow


def dragon_den():
    name, const = 'TaoIsland_Den', 'TAO_ISLAND_DEN'
    m = mf.Map(NW, NH)
    m.room(4, 5, 31, 16)                 # bovenhal
    m.room(4, 22, 31, 34)                # onderhal
    m.water(12, 10, 23, 16)              # bovenmeer
    m.water(9, 22, 26, 27)               # ondermeer (onder de waterval)
    m.build()
    m.cliff(4, 31, 17, pillars=(6, 27))
    m.waterfall(14, 17)
    m.stal_wall(4, 31, 5, pillars=(7, 26))
    m.cave_hole(*HOLE)
    m.exit_south(*DEN_EXIT)
    m.exit_south(*DEN_EXIT2)
    m.crater(27, 6)
    m.crater(5, 31)
    rnd = random.Random(1491)
    keep = {DEN_EXIT, (17, 33), (17, 32), DEN_EXIT2, (27, 33), (27, 32), (26, 9), (26, 10), (8, 8), (9, 8), (8, 30), (9, 30), (10, 30), (11, 30),
            (28, 29), (27, 29), (26, 29), (29, 29), (5, 23), (30, 33), (5, 15), (6, 15), (29, 9), (30, 9), (24, 8),
            (10, 6), (10, 7), (11, 8), (12, 8), (HOLE[0], HOLE[1] + 1), (HOLE[0], HOLE[1] + 2),
            (HOLE[0] - 1, HOLE[1] + 1), (HOLE[0] + 1, HOLE[1] + 1)}
    for x in range(4, 32):
        keep |= {(x, 21), (x, 16)}
    m.rubble(rnd, 6, (4, 23, 31, 33), keep)
    m.rubble(rnd, 4, (4, 6, 31, 15), keep)
    g = m.build()

    S = Scr(name, '''@ Project Grounded: de Dragon's Den op het Tao-eiland. Kaart en scripts: tools/grounded/maptools/tao_island.py.
@ Onderhal met meer; de waterval (Waterfall, badge 8) leidt naar de bovenhal. Daar slaapt een DRAGONITE op het gat naar
@ Frost Hollow (KYUREM, GHETSIS); hij is weg zodra je RESHIRAM en ZEKROM allebei hebt. Teksten zijn placeholders.
TaoIsland_Den_MapScripts::
	.byte 0
''')
    P = S.P
    S.trainer('Osric', 'TAO_OSRIC',
              "Halt! This den is for DRAGON TAMERS only!\n\nDo you have a permit? ...Nobody has a permit.",
              "Fine. You may stay. Unofficially.",
              "Up the waterfall there's a DRAGONITE asleep on a hole in the floor.\n\nWe don't ask. It doesn't tell.")
    S.trainer('Mira', 'TAO_MIRA',
              "Shh. The dragons are sleeping. Let's fight very, very quietly.",
              "...That was not quiet.",
              "Something big is snoring up there. I hope it's a DRAGONITE.\n\n"
              "Something even bigger is snoring under the DRAGONITE.")
    S.trainer('Talon', 'TAO_TALON',
              "You climbed the waterfall? Impressive. I took the stairs.\n\n...There are no stairs. That's how good I am.",
              "There really are no stairs.",
              "Nobody has been down the hole under that DRAGONITE. It's cold down there.\n\nLike, emotionally cold.")
    S.npc('Dragonite', "DRAGONITE is asleep on top of a hole in the floor. Ice-cold air leaks out around it.\n\n"
                       "It isn't moving. It's a very large draught excluder.", 'MSGBOX_DEFAULT')
    objs = [tr('OBJ_EVENT_GFX_MAN_5', 8, 30, P + 'Osric', 'RIGHT', 4),
            tr('OBJ_EVENT_GFX_WOMAN_5', 29, 29, P + 'Mira', 'LEFT', 3),
            tr('OBJ_EVENT_GFX_MAN_3', 9, 7, P + 'Talon', 'DOWN', 3),
            obj('OBJ_EVENT_GFX_SPECIES(DRAGONITE)', HOLE[0], HOLE[1] + 1, P + 'Dragonite',
                'FLAG_HIDE_TAO_DEN_DRAGONITE', move='MOVEMENT_TYPE_FACE_DOWN'),
            ball(5, 23, 'ITEM_PP_UP', 'FLAG_ITEM_TAO_DEN_PP_UP'),
            ball(5, 15, 'ITEM_MAX_ELIXIR', 'FLAG_ITEM_TAO_DEN_MAX_ELIXIR')]
    bgs = [cx.hidden(30, 33, 'ITEM_BIG_NUGGET', 'FLAG_HIDDEN_ITEM_TAO_DEN_BIG_NUGGET')]
    warps = [warp(DEN_EXIT[0], DEN_EXIT[1], 'TAO_ISLAND', 1), warp(HOLE[0], HOLE[1], 'TAO_ISLAND_FROST_HOLLOW', 0),
             warp(DEN_EXIT2[0], DEN_EXIT2[1], 'TAO_ISLAND', 2)]
    # ---- controles: onderhal te voet, bovenhal alleen via het meer + de waterval
    blocked = {(o['x'], o['y']) for o in objs}
    start = (DEN_EXIT[0], DEN_EXIT[1] - 1)
    walk = mf.reachable(g, start, blocked=blocked)
    surf = mf.reachable(g, start, blocked=blocked, allow_water=True)
    upper = {(x, y) for x in range(4, 32) for y in range(5, 17) if (x, y) in surf and g[y][x] >> 12 != 1}
    assert upper and not (upper & walk), 'bovenhal hoort alleen via de waterval bereikbaar te zijn'
    for o in objs:
        c = (o['x'], o['y'])
        if c[1] >= 22:
            assert mf.next_to(walk, *c), ('onderhal: object onbereikbaar', o['script'])
        else:
            assert mf.next_to(upper, *c), ('bovenhal: object onbereikbaar', o['script'])
        for s in cx.sight(o):
            assert s in walk | upper or (g[s[1]][s[0]] >> 10) & 3, ('zichtlijn over water', o['script'])
    assert (30, 33) in walk and (DEN_EXIT2[0], DEN_EXIT2[1] - 1) in walk, 'tweede uitgang onbereikbaar'
    assert (HOLE[0], HOLE[1] + 1) in mf.reachable(g, start, allow_water=True), 'gat naar Frost Hollow onbereikbaar'
    mf.save_layout(name, g)
    register_layout(name, const, NW, NH, 'gTileset_General', 'gTileset_MeteorFalls')
    sms.write_map(name, const, objs, warps, [], bgs, music='MUS_SEALED_CHAMBER', weather='WEATHER_NONE',
                  map_type='MAP_TYPE_UNDERGROUND', region_map_section='MAPSEC_TAO_ISLAND', show_map_name=False,
                  allow_cycling=False, allow_escaping=True, battle_scene='MAP_BATTLE_SCENE_NORMAL')
    oq.register_map(name)
    S.write()
    return name


# ====================================================================== Frost Hollow (Kyurem, Ghetsis)
GHETSIS = (8, 25)
KYUREM = (4, 25)


def frost_hollow():
    name, const = 'TaoIsland_FrostHollow', 'TAO_ISLAND_FROST_HOLLOW'
    S = Scr(name, '''@ Project Grounded: Frost Hollow onder de Dragon's Den (layout van de ijskamer van Shoal Cave). GHETSIS is de
@ post-league superboss en geeft de DNA SPLICERS; KYUREM (neutraal, lv 70) pas na hem. tools/grounded/maptools/tao_island.py
TaoIsland_FrostHollow_MapScripts::
	.byte 0
''')
    P, T = S.P, S.T
    S.raw(f'''{P}Ghetsis::
	trainerbattle_single TRAINER_TAO_GHETSIS, {T}GhetsisIntro, {T}GhetsisDefeat, {P}GhetsisDefeated
	release
	end

{P}GhetsisDefeated::
	msgbox {T}GhetsisGift, MSGBOX_DEFAULT
	giveitem ITEM_DNA_SPLICERS
	msgbox {T}GhetsisLeave, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_TAO_GHETSIS
	setflag FLAG_HIDE_TAO_GHETSIS
	fadescreen FADE_FROM_BLACK
	release
	end

{P}Kyurem::
	lock
	goto_if_not_defeated TRAINER_TAO_GHETSIS, {P}KyuremGuarded
	msgbox {T}KyuremWake, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_KYUREM, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_KYUREM, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}KyuremStays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}KyuremStays
	removeobject LOCALID_TAO_KYUREM
	setflag FLAG_HIDE_TAO_KYUREM
{P}KyuremStays::
	release
	end

{P}KyuremGuarded::
	msgbox {T}KyuremGuarded, MSGBOX_DEFAULT
	release
	end
''', [('GhetsisIntro', "Ah. The CHAMPION. How convenient.\n\n"
                       "I am GHETSIS. I came for KYUREM: the empty shell left over when those two brothers split up.\n\n"
                       "With these DNA SPLICERS I would fill it with their power. Alas, both brothers are in your bag.\n\n"
                       "Hand them over, or I take them. That is not a negotiation. That is a weather forecast."),
      ('GhetsisDefeat', "Impossible! I had a cape and everything!"),
      ('GhetsisGift', "...Very well. Keep your dragons. Take the SPLICERS as well.\n\n"
                      "They are useless without both brothers and a willingness to do something deeply unethical "
                      "to them.\n\nI'm told you have the brothers."),
      ('GhetsisLeave', "TEAM PLASMA will return! Probably. Our funding is under review."),
      ('KyuremGuarded', "KYUREM is frozen in place, glaring at the man in the robe.\n\n"
                        "Nobody is going anywhere until he's dealt with."),
      ('KyuremWake', "KYUREM looks at you. Then at your bag, where its brothers are.\n\nIt would like a word.")])
    objs = [tr('OBJ_EVENT_GFX_GHETSIS', GHETSIS[0], GHETSIS[1], P + 'Ghetsis', 'RIGHT', 5,
               flag='FLAG_HIDE_TAO_GHETSIS', local_id='LOCALID_TAO_GHETSIS'),
            obj('OBJ_EVENT_GFX_SPECIES(KYUREM)', KYUREM[0], KYUREM[1], P + 'Kyurem', 'FLAG_HIDE_TAO_KYUREM',
                move='MOVEMENT_TYPE_FACE_RIGHT', local_id='LOCALID_TAO_KYUREM'),
            ball(12, 8, 'ITEM_NEVER_MELT_ICE', 'FLAG_ITEM_TAO_FROST_NEVER_MELT_ICE'),
            ball(12, 21, 'ITEM_ICE_STONE', 'FLAG_ITEM_TAO_FROST_ICE_STONE')]
    g, W, H = read_layout('LAYOUT_SHOAL_CAVE_LOW_TIDE_ICE_ROOM')
    walk = reach(g, [(17, 11)], blocked={(o['x'], o['y']) for o in objs})
    for o in objs[:2]:
        assert cx.next_to((o['x'], o['y']), walk), ('Frost Hollow: onbereikbaar', o['script'])
    for c in cx.sight(objs[0]):
        assert c in walk, ('zichtlijn Ghetsis', c)
    write_map(name, const, 'LAYOUT_SHOAL_CAVE_LOW_TIDE_ICE_ROOM', objs, [warp(17, 10, 'TAO_ISLAND_DEN', 1)], [], [],
              music='MUS_MT_PYRE', weather='WEATHER_NONE', map_type='MAP_TYPE_UNDERGROUND',
              region_map_section='MAPSEC_TAO_ISLAND', show_map_name=False, allow_cycling=False, allow_escaping=True)
    S.write()
    return name


# ====================================================================== wilde Pokemon
WILD = {
    'TAO_ISLAND': dict(
        land=(20, [('ALTARIA', 44, 47), ('CYCLIZAR', 44, 47), ('FLYGON', 44, 47), ('HAXORUS', 44, 47),
                   ('TYRANTRUM', 45, 48), ('DRUDDIGON', 44, 47), ('KOMMO_O', 45, 48), ('DRAMPA', 45, 48),
                   ('NOIVERN', 45, 48), ('SLIGGOO', 44, 47), ('DURALUDON', 47, 48), ('GARCHOMP', 48, 48)]),
        water=(4, [('SEADRA', 44, 47), ('DRAGALGE', 48, 48), ('DRAGONAIR', 45, 48), ('TATSUGIRI', 45, 48),
                   ('KINGDRA', 48, 48)]),
        fishing=(30, [('HORSEA', 28, 31), ('SKRELP', 28, 31), ('SEADRA', 33, 37), ('DRAGONAIR', 33, 37),
                      ('TATSUGIRI', 33, 37), ('KINGDRA', 42, 46), ('DRACOVISH', 42, 46), ('ARCTOVISH', 42, 46),
                      ('DRAGALGE', 48, 50), ('DRAGONITE', 51, 52)])),
    'TAO_ISLAND_DEN': dict(
        land=(10, [('GABITE', 46, 47), ('ZWEILOUS', 46, 50), ('SHELGON', 46, 49), ('ARCTIBAX', 46, 50),
                   ('DRACOZOLT', 46, 50), ('ARCTOZOLT', 46, 50), ('DRAKLOAK', 46, 49), ('TURTONATOR', 46, 50),
                   ('DURALUDON', 47, 50), ('SLIGGOO', 46, 49), ('SALAMENCE', 50, 50), ('DRAGAPULT', 50, 50)]),
        water=(4, [('DRAGONAIR', 46, 50), ('SEADRA', 46, 50), ('DRACOVISH', 48, 50), ('ARCTOVISH', 48, 50),
                   ('KINGDRA', 50, 50)])),
    'TAO_ISLAND_FROST_HOLLOW': dict(
        land=(10, [('BEARTIC', 47, 50), ('CRYOGONAL', 47, 50), ('AVALUGG', 47, 50), ('VANILLISH', 44, 46),
                   ('GLALIE', 47, 50), ('FROSLASS', 47, 50), ('ARCTIBAX', 47, 50), ('WEAVILE', 47, 50),
                   ('MAMOSWINE', 48, 50), ('DEWGONG', 47, 50), ('VANILLUXE', 50, 50), ('BAXCALIBUR', 54, 54)])),
}
TOWER_LAND = (8, [('GOLURK', 45, 48), ('DRUDDIGON', 45, 48), ('MIENSHAO', 45, 48), ('SIGILYPH', 45, 48),
                  ('BRONZONG', 45, 48), ('CLAYDOL', 45, 48), ('LAMPENT', 44, 46), ('ZWEILOUS', 45, 48),
                  ('FRAXURE', 44, 47), ('ALTARIA', 45, 48), ('HAXORUS', 48, 48), ('KOMMO_O', 48, 48)])
for _f in ('TOWER_1F', 'TOWER_2F', 'TOWER_3F'):
    WILD['TAO_ISLAND_' + _f] = dict(land=TOWER_LAND)


def wild():
    p = 'src/data/wild_encounters.json'
    s = open(p).read()

    def block_end(a):
        depth, j = 0, a
        while True:
            if s[j] == '{': depth += 1
            elif s[j] == '}':
                depth -= 1
                if depth == 0: return j
            j += 1
    for mp, tabs in WILD.items():
        lbl = 'g' + ''.join(w.title() for w in mp.split('_'))
        e = {'map': 'MAP_' + mp, 'base_label': lbl}
        for kind in ('land', 'water', 'fishing'):
            if kind in tabs:
                rate, spec = tabs[kind]
                assert len(spec) == {'land': 12, 'water': 5, 'fishing': 10}[kind]
                assert len({x[0] for x in spec}) == len(spec), ('dubbele soort', mp, kind)
                e[kind + '_mons'] = {'encounter_rate': rate, 'mons': [
                    {'min_level': a, 'max_level': b, 'species': 'SPECIES_' + sp} for sp, a, b in spec]}
        blob = json.dumps(e, indent=2)
        blob = '\n'.join('        ' + ln for ln in blob.split('\n'))
        key = '"map": "MAP_%s"' % mp
        if key in s:
            a = s.rindex('{', 0, s.index(key))
            s = s[:a] + blob.lstrip() + s[block_end(a) + 1:]
        else:
            a = s.rindex('{', 0, s.index('"base_label": "gTaoIsland"'))
            j = block_end(a)
            s = s[:j + 1] + ',\n' + blob + s[j + 1:]
    json.loads(s)
    open(p, 'w').write(s)


# ====================================================================== trainers
IV = 'IVs: 25 HP / 25 Atk / 25 Def / 25 SpA / 25 SpD / 25 Spe'
IV31 = 'IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe'
AI = 'AI: Check Bad Move / Try To Faint / Check Viability'
AI_BOSS = 'AI: Check Bad Move / Try To Faint / Check Viability / Smart Switching / Smart Mon Choices'


def mon(head, lvl, moves, ability=None, iv=IV, extra=()):
    out = [head, 'Level: %d' % lvl] + (['Ability: ' + ability] if ability else []) + [iv] + list(extra) + \
          ['- ' + m for m in moves]
    return '\n'.join(out)


FIRST_ID = 1060
TRAINERS = [
    # (const, waarom, naam, klasse, foto, geslacht, muziek, AI, items, extra kopregels, team)
    ('TAO_VERNON', 'Tao-eiland, strand: 412 keer gebeten', 'VERNON', 'Dragon Tamer', 'Dragon Tamer', 'Male', 'Intense', AI, None, [], [
        mon('Altaria', 46, ['Dragon Pulse', 'Air Slash', 'Cotton Guard', 'Roost']),
        mon('Flygon', 46, ['Earthquake', 'Dragon Claw', 'U-turn', 'Fire Punch']),
        mon('Drampa', 46, ['Dragon Pulse', 'Hyper Voice', 'Flamethrower', 'Glare'])]),
    ('TAO_SAELA', 'Tao-eiland, plateau: traint vooral rennen', 'SAELA', 'Cooltrainer', 'Cooltrainer F', 'Female', 'Cool', AI, None, [], [
        mon('Noivern', 46, ['Air Slash', 'Dragon Pulse', 'Super Fang', 'Roost']),
        mon('Cyclizar', 46, ['Double-Edge', 'Dragon Claw', 'U-turn', 'Shed Tail']),
        mon('Tyrantrum', 46, ['Rock Slide', 'Dragon Claw', 'Crunch', 'Dragon Dance'])]),
    ('TAO_OSRIC', "Tao-eiland, Dragon's Den onderhal: vergunningencontrole", 'OSRIC', 'Dragon Tamer', 'Dragon Tamer', 'Male', 'Intense', AI, None, [], [
        mon('Kommo-o', 49, ['Clanging Scales', 'Drain Punch', 'Iron Defense', 'Dragon Claw']),
        mon('Druddigon', 49, ['Dragon Claw', 'Rock Slide', 'Superpower', 'Glare']),
        mon('Dracozolt', 49, ['Bolt Beak', 'Dragon Claw', 'Stomping Tantrum', 'Rock Slide'])]),
    ('TAO_MIRA', "Tao-eiland, Dragon's Den onderhal: heel zacht vechten", 'MIRA', 'Cooltrainer', 'Cooltrainer F', 'Female', 'Cool', AI, None, [], [
        mon('Goodra', 49, ['Dragon Pulse', 'Sludge Bomb', 'Thunderbolt', 'Fire Blast']),
        mon('Duraludon', 49, ['Flash Cannon', 'Dragon Pulse', 'Thunderbolt', 'Stealth Rock']),
        mon('Tatsugiri', 49, ['Dragon Pulse', 'Muddy Water', 'Rapid Spin', 'Icy Wind']),
        mon('Appletun', 49, ['Apple Acid', 'Dragon Pulse', 'Recover', 'Leech Seed'])]),
    ('TAO_TALON', "Tao-eiland, Dragon's Den bovenhal: nam de trap", 'TALON', 'Cooltrainer', 'Cooltrainer M', 'Male', 'Cool', AI_BOSS, None, [], [
        mon('Garchomp', 52, ['Earthquake', 'Dragon Claw', 'Swords Dance', 'Stone Edge']),
        mon('Dragapult', 52, ['Dragon Darts', 'Phantom Force', 'U-turn', 'Will-O-Wisp']),
        mon('Haxorus', 52, ['Dragon Dance', 'Dragon Claw', 'Earthquake', 'Poison Jab']),
        mon('Hydreigon', 53, ['Dark Pulse', 'Dragon Pulse', 'Flamethrower', 'Nasty Plot'])]),
    ('TAO_GHETSIS', 'Tao-eiland, Frost Hollow: post-league superboss, geeft de DNA Splicers', 'GHETSIS', 'Plasma Boss', 'Ghetsis', 'Male', 'Suspicious',
     AI_BOSS, 'Full Restore / Full Restore', ['Mugshot: Purple'], [
        mon('Cofagrigus @ Leftovers', 82, ['Will-O-Wisp', 'Hex', 'Toxic Spikes', 'Pain Split'], 'Mummy', IV31,
            ['EVs: 252 HP / 252 Def / 4 SpD', 'Nature: Bold']),
        mon('Bouffalant @ Choice Band', 82, ['Head Charge', 'Close Combat', 'Earthquake', 'Megahorn'], 'Sap Sipper', IV31,
            ['EVs: 252 HP / 252 Atk / 4 SpD', 'Nature: Adamant']),
        mon('Seismitoad @ Life Orb', 82, ['Scald', 'Earth Power', 'Sludge Wave', 'Stealth Rock'], 'Water Absorb', IV31,
            ['EVs: 4 HP / 252 SpA / 252 Spe', 'Nature: Modest']),
        mon('Eelektross @ Assault Vest', 82, ['Thunderbolt', 'Flamethrower', 'Giga Drain', 'Knock Off'], 'Levitate', IV31,
            ['EVs: 252 HP / 252 SpA / 4 SpD', 'Nature: Modest']),
        mon('Kingambit @ Black Glasses', 83, ['Swords Dance', 'Sucker Punch', 'Iron Head', 'Kowtow Cleave'], 'Supreme Overlord', IV31,
            ['EVs: 252 HP / 252 Atk / 4 SpD', 'Nature: Adamant']),
        mon('Hydreigon @ Choice Specs', 84, ['Dark Pulse', 'Draco Meteor', 'Flamethrower', 'Earth Power'], 'Levitate', IV31,
            ['EVs: 4 HP / 252 SpA / 252 Spe', 'Nature: Timid'])]),
    ('TAO_JUN', 'Tao-toren 2F: Team Zekrom', 'JUN', 'Dragon Tamer', 'Dragon Tamer', 'Male', 'Intense', AI, None, [], [
        mon('Eelektross', 50, ['Wild Charge', 'Crunch', 'Drain Punch', 'Coil'], 'Levitate'),
        mon('Zweilous', 50, ['Crunch', 'Dragon Rush', 'Body Slam', 'Work Up']),
        mon('Ampharos', 50, ['Thunderbolt', 'Dragon Pulse', 'Signal Beam', 'Thunder Wave']),
        mon('Dracozolt', 51, ['Bolt Beak', 'Dragon Claw', 'Earthquake', 'Rock Slide'])]),
    ('TAO_YING', 'Tao-toren 3F: Team Reshiram', 'YING', 'Cooltrainer', 'Cooltrainer F', 'Female', 'Cool', AI, None, [], [
        mon('Volcarona', 51, ['Fiery Dance', 'Bug Buzz', 'Quiver Dance', 'Giga Drain']),
        mon('Turtonator', 51, ['Flamethrower', 'Dragon Pulse', 'Shell Trap', 'Shell Smash']),
        mon('Togekiss', 51, ['Air Slash', 'Dazzling Gleam', 'Flamethrower', 'Roost']),
        mon('Charizard', 52, ['Flamethrower', 'Air Slash', 'Dragon Pulse', 'Solar Beam'])]),
]


def replace_block(text_, start, end, new):
    if start in text_:
        i = text_.index(start)
        j = text_.index(end, i) + len(end)
        return text_[:i] + new + text_[j:]
    return text_.rstrip('\n') + '\n\n' + new + '\n'


def trainers():
    assert len(TRAINERS) <= 10
    p = 'include/constants/opponents.h'
    s = open(p).read()
    blk = '// tao_island { (tools/grounded/maptools/tao_island.py; id 1060-1069)\n'
    for i, tr_ in enumerate(TRAINERS):
        blk += '#define TRAINER_%-28s%d // Project Grounded: %s\n' % (tr_[0], FIRST_ID + i, tr_[1])
    blk += '// }'
    if '// tao_island {' in s:
        i = s.index('// tao_island {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        s = s.replace('\n#define TRAINERS_COUNT', '\n' + blk + '\n\n#define TRAINERS_COUNT', 1)
    for n in range(FIRST_ID, FIRST_ID + len(TRAINERS)):
        hits = re.findall(r'^#define TRAINER_\w+\s+%d\b' % n, s, re.M)
        assert len(hits) == 1, ('trainer-id dubbel', n, hits)
    open(p, 'w').write(s)

    p = 'src/data/trainers.party'
    s = open(p).read()
    blk = '/* --- tao_island (tools/grounded/maptools/tao_island.py) --- */\n\n'
    for const, why, nm, cls, pic, gender, music, ai, items, extra, team in TRAINERS:
        hdr = ['Name: ' + nm, 'Class: ' + cls, 'Pic: ' + pic, 'Gender: ' + gender, 'Music: ' + music]
        if items:
            hdr.append('Items: ' + items)
        hdr += ['Double Battle: No', ai] + extra
        blk += '=== TRAINER_%s ===\n%s\n\n%s\n\n' % (const, '\n'.join(hdr), '\n\n'.join(team))
    blk = blk.rstrip('\n') + '\n\n/* --- einde tao_island --- */'
    s = replace_block(s, '/* --- tao_island', '/* --- einde tao_island --- */', blk)
    open(p, 'w').write(s)


# ====================================================================== main
if __name__ == '__main__':
    flags()
    names = [tao_island()] + tower() + [dragon_den(), frost_hollow()]
    wild()
    trainers()
    if len(sys.argv) > 1:
        for n in names:
            m = json.load(open('data/maps/%s/map.json' % n))
            L = layout(m['layout'])
            subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), n,
                            os.path.join(sys.argv[1], n + '.png'), '0', str(L['height'])], check=True)
    print('klaar:', ', '.join(names))
