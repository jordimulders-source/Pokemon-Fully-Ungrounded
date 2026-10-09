"""Project Grounded: legendaries ronde 'legends2' (Jordi, 9 okt: alle legendaries te krijgen). Idempotent.

  Kanto-vogels (post-game, lv 85; verslagen = bij het volgende bezoek terug, gevangen = weg):
    Articuno   Shoal Cave, Frozen Depths (ijsgrot, de rotsnis rechtsboven)
    Zapdos     Route 119, de afgelegen richel in het onweer boven het Weather Institute
    Moltres    Mt. Chimney, de kraterrand van de top (MtChimney_Summit)
  Galar-vogels (pas als alle drie de Kanto-vogels gevangen zijn, lv 88):
    Articuno-Galar (Psychic)  Mossdeep, uitkijkpunten bij het Space Center; teleporteert bij binnenkomst naar een
                              willekeurige plek en flitst één keer weg als je hem aanspreekt (daarna gevecht)
    Zapdos-Galar (Fighting)   Route 111, de open woestijn in het noorden; rent rond (snelle wander, zie
                              IsRunningWanderer in src/event_object_movement.c)
    Moltres-Galar (Dark)      Route 120, de mistige nis naast de Ancient Tomb
  Diancie    gift in de Granite Cave-kristalgrot (post-game, tussen twee Carbink)
  Meloetta   Route 123: Snorlax ligt de hele game in de enige opening van de bessenvelden van de Berry Master (het hek
             is daarvoor dichtgezet tot één vakje); post-game ligt er een Poke Flute naast; oppakken = spelen, Snorlax
             loopt weg, Meloetta (lv 62) volgt en vecht
  Zygarde    Desert Underpass, een nis in het midden; verschijnt als Xerneas en Yveltal gevangen zijn (Pokedex), lv 90

Flags: FLAG_GROUNDED 1520-1579 (blok 'legends2' in flags.h). Geen nieuwe GFX (overworld-mons).
Draai na dungeon_extra.py / chimney_ext.py (die herschrijven de kaarten): python3 tools/grounded/maptools/legends2.py
Teksten: placeholders in de huisstijl (Jordi herschrijft ze in de Dialoogstudio)."""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
import check_levels  # noqa: E402
check_levels.protect()
import json, os, struct, sys  # noqa: E401,E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import beacon_dragon as bd  # noqa: E402  (zet de werkmap op de repo-root)

# ====================================================================== flags
FLAGS = [
    (1520, 'FLAG_CAUGHT_KANTO_ARTICUNO', 'Articuno (Shoal Cave) gevangen'),
    (1521, 'FLAG_CAUGHT_KANTO_ZAPDOS', 'Zapdos (Route 119) gevangen'),
    (1522, 'FLAG_CAUGHT_KANTO_MOLTRES', 'Moltres (Mt. Chimney) gevangen'),
    (1523, 'FLAG_CAUGHT_GALAR_ARTICUNO', 'Galar-Articuno (Mossdeep) gevangen'),
    (1524, 'FLAG_CAUGHT_GALAR_ZAPDOS', 'Galar-Zapdos (Route 111) gevangen'),
    (1525, 'FLAG_CAUGHT_GALAR_MOLTRES', 'Galar-Moltres (Route 120) gevangen'),
    (1526, 'FLAG_RECEIVED_DIANCIE', 'Diancie (Granite Cave-kristalgrot) gekregen'),
    (1527, 'FLAG_ROUTE123_SNORLAX_GONE', 'Route 123: Snorlax is weggelopen (verbergt hem; bessenvelden vrij)'),
    (1528, 'FLAG_CAUGHT_MELOETTA', 'Meloetta (Route 123) gevangen'),
    (1529, 'FLAG_CAUGHT_ZYGARDE', 'Zygarde (Desert Underpass) gevangen'),
    (1530, 'FLAG_HIDE_LEGENDS_ARTICUNO', 'verbergt Articuno (gezet/gewist in ON_TRANSITION)'),
    (1531, 'FLAG_HIDE_LEGENDS_ZAPDOS', 'verbergt Zapdos (ON_TRANSITION)'),
    (1532, 'FLAG_HIDE_LEGENDS_MOLTRES', 'verbergt Moltres (ON_TRANSITION)'),
    (1533, 'FLAG_HIDE_LEGENDS_GALAR_ARTICUNO', 'verbergt Galar-Articuno (ON_TRANSITION)'),
    (1534, 'FLAG_HIDE_LEGENDS_GALAR_ZAPDOS', 'verbergt Galar-Zapdos (ON_TRANSITION)'),
    (1535, 'FLAG_HIDE_LEGENDS_GALAR_MOLTRES', 'verbergt Galar-Moltres (ON_TRANSITION)'),
    (1536, 'FLAG_HIDE_LEGENDS_MELOETTA', 'verbergt Meloetta (ON_TRANSITION)'),
    (1537, 'FLAG_HIDE_LEGENDS_ZYGARDE', 'verbergt Zygarde (ON_TRANSITION)'),
    (1538, 'FLAG_HIDE_LEGENDS_DIANCIE', 'verbergt Diancie (ON_TRANSITION)'),
    (1539, 'FLAG_HIDE_LEGENDS_CARBINK', 'verbergt de twee Carbink naast Diancie (ON_TRANSITION, alleen post-game zichtbaar)'),
    (1540, 'FLAG_HIDE_LEGENDS_POKE_FLUTE', 'verbergt de Poke Flute naast Snorlax (ON_TRANSITION, alleen post-game)'),
]


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = '// legends2 { (tools/grounded/maptools/legends2.py; FLAG_GROUNDED 1520-1579: 1520-1540 in gebruik, 1541-1579 nog vrij)\n'
    for n, name, why in FLAGS:
        assert 1520 <= n <= 1579
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// legends2 {' in s:
        i = s.index('// legends2 {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('\n// Special Flags (Stored in EWRAM')
        s = s[:anchor] + '\n' + blk + '\n' + s[anchor:]
    for n, *_ in FLAGS:
        assert s.count('FLAG_GROUNDED(%d)' % n) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


# ====================================================================== hulpjes
def layout(mapname):
    m = json.load(open('data/maps/%s/map.json' % mapname))
    L = [l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id') == m['layout']][0]
    return L


def tile(mapname, x, y):
    L = layout(mapname)
    w = L['width']
    data = open(L['blockdata_filepath'], 'rb').read()
    return struct.unpack_from('<H', data, 2 * (y * w + x))[0]


def set_tile(mapname, x, y, value):
    L = layout(mapname)
    p = L['blockdata_filepath']
    data = bytearray(open(p, 'rb').read())
    struct.pack_into('<H', data, 2 * (y * L['width'] + x), value)
    open(p, 'wb').write(bytes(data))


def obj(mapname, local_id, gfx, x, y, script, flag, move='MOVEMENT_TYPE_FACE_DOWN', rx=0, ry=0, arg='0'):
    t = tile(mapname, x, y)
    assert not (t >> 10) & 3, ('object op een blokkade', mapname, x, y)
    return {'local_id': local_id, 'graphics_id': gfx, 'x': x, 'y': y, 'elevation': t >> 12, 'movement_type': move,
            'movement_range_x': rx, 'movement_range_y': ry, 'trainer_type': 'TRAINER_TYPE_NONE',
            'trainer_sight_or_berry_tree_id': arg, 'script': script, 'flag': flag}


def put_objects(mapname, objs):
    """Vervangt eerdere legends2-objecten (herkend aan local_id LOCALID_LEGENDS_*) en zet de nieuwe achteraan."""
    p = 'data/maps/%s/map.json' % mapname
    m = json.load(open(p))
    m['object_events'] = [o for o in m['object_events'] if not str(o.get('local_id', '')).startswith('LOCALID_LEGENDS_')]
    m['object_events'] += objs
    open(p, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')


def scripts_block(mapname, block, transition_label=None):
    p = 'data/maps/%s/scripts.inc' % mapname
    s = open(p).read()
    start, end = '@ --- legends2 (', '@ --- einde legends2 ---'
    new = '@ --- legends2 (gegenereerd door tools/grounded/maptools/legends2.py) ---\n' + block.rstrip('\n') + '\n' + end
    s = bd.replace_block(s, start, end, new)
    if transition_label:
        hook = '\tcall %s\n' % transition_label
        hdr = '%s_MapScripts::\n' % mapname
        i = s.index(hdr)
        j = s.index('.byte 0', i)
        head = s[i:j]
        import re
        mm = re.search(r'map_script MAP_SCRIPT_ON_TRANSITION, (\w+)', head)
        if mm:
            lab = mm.group(1)
            k = re.search(r'^%s::?\n' % lab, s, re.M)
            assert k, ('label niet gevonden', lab)
            if not s[k.end():].startswith(hook):
                s = s[:k.end()] + hook + s[k.end():]
        else:
            own = '%s_Legends2_OnTransition' % mapname
            s = s[:i + len(hdr)] + '\tmap_script MAP_SCRIPT_ON_TRANSITION, %s\n' % own + s[i + len(hdr):]
            if '%s:\n' % own not in s:
                s = s.rstrip('\n') + '\n\n%s:\n%s\tend\n' % (own, hook)
    open(p, 'w').write(s.rstrip('\n') + '\n')


T = bd.text


# ====================================================================== stationaire legendary (gemeenschappelijk)
def battle_script(P, key, species, level, local_id, hide_flag, caught_flag, intro, fled, after_caught=''):
    """Gevecht; gevangen = weg (caught_flag), verslagen = weg tot het volgende bezoek, gevlucht = blijft staan."""
    return f'''{P}{key}::
	lock
	faceplayer
	playmoncry {species}, CRY_MODE_ENCOUNTER
	msgbox {P.replace('_EventScript_', '_Text_')}{key}, MSGBOX_DEFAULT
	waitmoncry
	closemessage
{P}{key}_Battle::
	setwildbattle {species}, {level}
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}{key}_Caught
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}{key}_Stays
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}{key}_Stays
	removeobject {local_id}
	setflag {hide_flag}
	msgbox {P.replace('_EventScript_', '_Text_')}{key}Fled, MSGBOX_DEFAULT
{P}{key}_Stays::
	release
	end

{P}{key}_Caught::
	removeobject {local_id}
	setflag {hide_flag}
	setflag {caught_flag}
{after_caught}	release
	end

''' + T(P.replace('_EventScript_', '_Text_') + '' + key, intro) + T(P.replace('_EventScript_', '_Text_') + '' + key + 'Fled', fled)


KANTO_LV, GALAR_LV = 85, 88
GALAR_CHECK = '''	call Legends2_EventScript_CheckGalarArrive
'''


def kanto_transition(P, hide, caught):
    return f'''{P}Legends2_Transition:
	setflag {hide}
	goto_if_unset FLAG_SYS_GAME_CLEAR, {P}Legends2_TransitionEnd
	goto_if_set {caught}, {P}Legends2_TransitionEnd
	clearflag {hide}
{P}Legends2_TransitionEnd:
	return

'''


def galar_transition(P, hide, caught, extra=''):
    return f'''{P}Legends2_GalarTransition:
	setflag {hide}
	goto_if_set {caught}, {P}Legends2_GalarTransitionEnd
	call Legends2_EventScript_GalarReady
	goto_if_eq VAR_RESULT, FALSE, {P}Legends2_GalarTransitionEnd
	clearflag {hide}
{extra}{P}Legends2_GalarTransitionEnd:
	return

'''


# ====================================================================== 1. Kanto-vogels
def articuno():
    name = 'ShoalCave_LowTideFrozenDepths'
    P = name + '_EventScript_'
    blk = kanto_transition(P, 'FLAG_HIDE_LEGENDS_ARTICUNO', 'FLAG_CAUGHT_KANTO_ARTICUNO')
    blk += battle_script(P, 'Articuno', 'SPECIES_ARTICUNO', KANTO_LV, 'LOCALID_LEGENDS_ARTICUNO',
                         'FLAG_HIDE_LEGENDS_ARTICUNO', 'FLAG_CAUGHT_KANTO_ARTICUNO',
                         "Kyaaah!\n\n(It has been sitting here so long the ice thinks it's furniture.)",
                         "ARTICUNO shattered into a cloud of snow and was gone.\n\n"
                         "It'll reassemble. It always does. Mostly out of spite.", GALAR_CHECK)
    scripts_block(name, blk, P + 'Legends2_Transition')
    put_objects(name, [obj(name, 'LOCALID_LEGENDS_ARTICUNO', 'OBJ_EVENT_GFX_SPECIES(ARTICUNO)', 14, 2, P + 'Articuno',
                           'FLAG_HIDE_LEGENDS_ARTICUNO', 'MOVEMENT_TYPE_FACE_DOWN')])


def zapdos():
    name = 'Route119'
    P = name + '_EventScript_'
    blk = kanto_transition(P, 'FLAG_HIDE_LEGENDS_ZAPDOS', 'FLAG_CAUGHT_KANTO_ZAPDOS')
    blk += battle_script(P, 'Zapdos', 'SPECIES_ZAPDOS', KANTO_LV, 'LOCALID_LEGENDS_ZAPDOS',
                         'FLAG_HIDE_LEGENDS_ZAPDOS', 'FLAG_CAUGHT_KANTO_ZAPDOS',
                         "Gyaoo!\n\n(So that's why the WEATHER INSTITUTE's forecast always says 'thunder'. "
                         "It's not a forecast. It's a tenant.)",
                         "ZAPDOS flew off into the clouds. The clouds did not look happy about it.\n\n"
                         "The storm will bring it back. The storm brings everything back.", GALAR_CHECK)
    scripts_block(name, blk, P + 'Legends2_Transition')
    put_objects(name, [obj(name, 'LOCALID_LEGENDS_ZAPDOS', 'OBJ_EVENT_GFX_SPECIES(ZAPDOS)', 3, 16, P + 'Zapdos',
                           'FLAG_HIDE_LEGENDS_ZAPDOS', 'MOVEMENT_TYPE_FACE_RIGHT')])


def moltres():
    name = 'MtChimney_Summit'
    P = name + '_EventScript_'
    blk = kanto_transition(P, 'FLAG_HIDE_LEGENDS_MOLTRES', 'FLAG_CAUGHT_KANTO_MOLTRES')
    blk += battle_script(P, 'Moltres', 'SPECIES_MOLTRES', KANTO_LV, 'LOCALID_LEGENDS_MOLTRES',
                         'FLAG_HIDE_LEGENDS_MOLTRES', 'FLAG_CAUGHT_KANTO_MOLTRES',
                         "Kyaaoo!\n\n(It's warming its feet in the crater. The lava is warming its feet on MOLTRES.)",
                         "MOLTRES dove straight into the lava.\n\nIt does that. It's fine. It's always fine. "
                         "It'll be back on the rim tomorrow, smug and slightly crispy.", GALAR_CHECK)
    scripts_block(name, blk, P + 'Legends2_Transition')
    put_objects(name, [obj(name, 'LOCALID_LEGENDS_MOLTRES', 'OBJ_EVENT_GFX_SPECIES(MOLTRES)', 12, 6, P + 'Moltres',
                           'FLAG_HIDE_LEGENDS_MOLTRES', 'MOVEMENT_TYPE_FACE_DOWN')])


# ====================================================================== 2. Galar-vogels
GA_SPOTS = [(70, 10), (59, 15), (69, 20)]     # Mossdeep: hoge terrassen rond het Space Center (allemaal elevation 9;
#                                              niet achter de raket: daar valt hij weg achter de toren)


def galar_articuno():
    name = 'MossdeepCity'
    P = name + '_EventScript_'
    lid = 'LOCALID_LEGENDS_GALAR_ARTICUNO'
    place = ''.join(f'''	goto_if_eq VAR_TEMP_9, {i}, {P}Legends2_GASpot{i}
''' for i in range(len(GA_SPOTS)))
    spots = ''.join(f'''{P}Legends2_GASpot{i}:
	setobjectxyperm {lid}, {x}, {y}
	return

''' for i, (x, y) in enumerate(GA_SPOTS))
    extra = f'''	random {len(GA_SPOTS)}
	copyvar VAR_TEMP_9, VAR_RESULT
	call {P}Legends2_GAPlace
'''
    blk = galar_transition(P, 'FLAG_HIDE_LEGENDS_GALAR_ARTICUNO', 'FLAG_CAUGHT_GALAR_ARTICUNO', extra)
    blk += f'''{P}Legends2_GAPlace:
{place}	return

{spots}@ Eerste keer aanspreken: flitst weg naar een andere uitkijkplek (VAR_TEMP_A = 1). Daarna: gevecht.
{P}GalarArticuno::
	lock
	goto_if_eq VAR_TEMP_A, 1, {P}GalarArticunoFight
	playmoncry SPECIES_ARTICUNO_GALAR, CRY_MODE_ENCOUNTER
	msgbox {P.replace('_EventScript_', '_Text_')}GalarArticunoBlink, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	playse SE_M_TELEPORT
	fadescreen FADE_TO_WHITE
	removeobject {lid}
	addvar VAR_TEMP_9, 1
	goto_if_lt VAR_TEMP_9, {len(GA_SPOTS)}, {P}GalarArticunoMove
	setvar VAR_TEMP_9, 0
{P}GalarArticunoMove:
	call {P}Legends2_GAPlace
	addobject {lid}
	fadescreen FADE_FROM_WHITE
	setvar VAR_TEMP_A, 1
	msgbox {P.replace('_EventScript_', '_Text_')}GalarArticunoGone, MSGBOX_DEFAULT
	release
	end

{P}GalarArticunoFight::
	faceplayer
	playmoncry SPECIES_ARTICUNO_GALAR, CRY_MODE_ENCOUNTER
	msgbox {P.replace('_EventScript_', '_Text_')}GalarArticunoAgain, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	goto {P}GalarArticuno2_Battle

''' + T(P.replace('_EventScript_', '_Text_') + 'GalarArticunoBlink', "A purple ARTICUNO is staring at the stars. Then at you.\n\n"
                                         "Its eyes glow. It has decided you are a spoiler.") \
        + T(P.replace('_EventScript_', '_Text_') + 'GalarArticunoGone', "It blinked somewhere else on the island.\n\n"
                                          "Rude. Also, honestly, a good trick.") \
        + T(P.replace('_EventScript_', '_Text_') + 'GalarArticunoAgain', "It sighs telepathically. It sounds like a dial-up modem.\n\n"
                                           "Fine. It'll fight. But it's judging your star chart.")
    # gevecht zonder eigen intro (de 'Again'-tekst is de intro)
    b = battle_script(P, 'GalarArticuno2', 'SPECIES_ARTICUNO_GALAR', GALAR_LV, lid, 'FLAG_HIDE_LEGENDS_GALAR_ARTICUNO',
                      'FLAG_CAUGHT_GALAR_ARTICUNO', 'unused',
                      "ARTICUNO folded space around itself and left.\n\n"
                      "Somewhere, an astronomer just found a new star. It's ARTICUNO. It's mocking him.")
    # het label GalarArticuno2:: met de intro is niet nodig: alleen _Battle en verder
    b = b[b.index(P + 'GalarArticuno2_Battle::'):]
    b = b.replace(T(P.replace('_EventScript_', '_Text_') + 'GalarArticuno2', 'unused'), '')
    blk += b
    scripts_block(name, blk, P + 'Legends2_GalarTransition')
    x, y = GA_SPOTS[0]
    put_objects(name, [obj(name, lid, 'OBJ_EVENT_GFX_SPECIES(ARTICUNO_GALAR)', x, y, P + 'GalarArticuno',
                           'FLAG_HIDE_LEGENDS_GALAR_ARTICUNO', 'MOVEMENT_TYPE_LOOK_AROUND')])
    for (sx, sy) in GA_SPOTS:          # setobjectxyperm verandert de elevation niet: alle plekken gelijk
        t = tile(name, sx, sy)
        assert not (t >> 10) & 3 and (t >> 12) == (tile(name, *GA_SPOTS[0]) >> 12), ('plek', sx, sy)


def galar_zapdos():
    name = 'Route111'
    P = name + '_EventScript_'
    blk = galar_transition(P, 'FLAG_HIDE_LEGENDS_GALAR_ZAPDOS', 'FLAG_CAUGHT_GALAR_ZAPDOS')
    blk += battle_script(P, 'GalarZapdos', 'SPECIES_ZAPDOS_GALAR', GALAR_LV, 'LOCALID_LEGENDS_GALAR_ZAPDOS',
                         'FLAG_HIDE_LEGENDS_GALAR_ZAPDOS', 'FLAG_CAUGHT_GALAR_ZAPDOS',
                         "Gya-gya!\n\n(An orange ZAPDOS that cannot fly, will not fly, and is doing laps. "
                         "It's been doing laps since the LEAGUE. It is on lap four thousand.)",
                         "ZAPDOS sprinted off into the sandstorm.\n\nYou can hear it doing laps out there. "
                         "It'll be back. It never actually leaves the track.")
    scripts_block(name, blk, P + 'Legends2_GalarTransition')
    put_objects(name, [obj(name, 'LOCALID_LEGENDS_GALAR_ZAPDOS', 'OBJ_EVENT_GFX_SPECIES(ZAPDOS_GALAR)', 23, 41,
                           P + 'GalarZapdos', 'FLAG_HIDE_LEGENDS_GALAR_ZAPDOS', 'MOVEMENT_TYPE_WANDER_AROUND',
                           rx=4, ry=2)])


def galar_moltres():
    name = 'Route120'
    P = name + '_EventScript_'
    blk = galar_transition(P, 'FLAG_HIDE_LEGENDS_GALAR_MOLTRES', 'FLAG_CAUGHT_GALAR_MOLTRES')
    blk += battle_script(P, 'GalarMoltres', 'SPECIES_MOLTRES_GALAR', GALAR_LV, 'LOCALID_LEGENDS_GALAR_MOLTRES',
                         'FLAG_HIDE_LEGENDS_GALAR_MOLTRES', 'FLAG_CAUGHT_GALAR_MOLTRES',
                         "Kyaaah...\n\n(A MOLTRES made of bad vibes. Its flames are the colour of a bruise. "
                         "It came for the tomb. It stayed for the fog.)",
                         "MOLTRES dissolved into the mist.\n\nThe fog got a little thicker. The fog got a little "
                         "meaner. It'll be back when the mood is right. The mood is always right here.")
    scripts_block(name, blk, P + 'Legends2_GalarTransition')
    put_objects(name, [obj(name, 'LOCALID_LEGENDS_GALAR_MOLTRES', 'OBJ_EVENT_GFX_SPECIES(MOLTRES_GALAR)', 2, 51,
                           P + 'GalarMoltres', 'FLAG_HIDE_LEGENDS_GALAR_MOLTRES', 'MOVEMENT_TYPE_FACE_DOWN')])


# ====================================================================== 3. Diancie
def diancie():
    name = 'GraniteCave_CrystalGrotto'
    P = name + '_EventScript_'
    blk = f'''{P}Legends2_Transition:
	setflag FLAG_HIDE_LEGENDS_DIANCIE
	setflag FLAG_HIDE_LEGENDS_CARBINK
	goto_if_unset FLAG_SYS_GAME_CLEAR, {P}Legends2_TransitionEnd
	clearflag FLAG_HIDE_LEGENDS_CARBINK
	goto_if_set FLAG_RECEIVED_DIANCIE, {P}Legends2_TransitionEnd
	clearflag FLAG_HIDE_LEGENDS_DIANCIE
{P}Legends2_TransitionEnd:
	return

{P}Diancie::
	lock
	faceplayer
	playmoncry SPECIES_DIANCIE, CRY_MODE_ENCOUNTER
	msgbox {P.replace('_EventScript_', '_Text_')}Diancie, MSGBOX_DEFAULT
	waitmoncry
	setvar VAR_0x8004, SPECIES_DIANCIE
	setvar VAR_0x8005, 80
	setvar VAR_0x8006, ITEM_NONE
	call Grounded_EventScript_GiveGiftMon
	goto_if_eq VAR_RESULT, FALSE, {P}DiancieNoRoom
	setflag FLAG_RECEIVED_DIANCIE
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_LEGENDS_DIANCIE
	setflag FLAG_HIDE_LEGENDS_DIANCIE
	fadescreen FADE_FROM_BLACK
	msgbox {P.replace('_EventScript_', '_Text_')}DiancieAfter, MSGBOX_DEFAULT
	release
	end

{P}DiancieNoRoom::
	msgbox {P.replace('_EventScript_', '_Text_')}DiancieNoRoom, MSGBOX_DEFAULT
	release
	end

{P}Carbink::
	lock
	faceplayer
	playmoncry SPECIES_CARBINK, CRY_MODE_NORMAL
	msgbox {P.replace('_EventScript_', '_Text_')}Carbink, MSGBOX_DEFAULT
	waitmoncry
	release
	end

''' + T(P.replace('_EventScript_', '_Text_') + 'Diancie',
        "Between the CARBINK, a pink crystal opens its eyes.\n\n"
        "DIANCIE looks you over like a jeweller looks at a fake. Then it notices the CHAMPION ribbon, "
        "or the dirt on your shoes. Hard to say which.\n\n"
        "It floats closer. It has decided you're its new royal guard. Nobody asked the CARBINK.") \
        + T(P.replace('_EventScript_', '_Text_') + 'DiancieAfter',
            "The CARBINK watch their princess leave with you.\n\n"
            "Next door, in his own little cave, STEVEN is going to be so jealous. Don't tell him. Do tell him.") \
        + T(P.replace('_EventScript_', '_Text_') + 'DiancieNoRoom',
            "DIANCIE looks at your full party and your full PC.\n\nIt refuses to be the eighth wheel. Make room.") \
        + T(P.replace('_EventScript_', '_Text_') + 'Carbink', "Carbink!\n\n(It's guarding the princess. It's a rock. It's doing its best.)")
    scripts_block(name, blk, P + 'Legends2_Transition')
    put_objects(name, [
        obj(name, 'LOCALID_LEGENDS_DIANCIE', 'OBJ_EVENT_GFX_SPECIES(DIANCIE)', 13, 9, P + 'Diancie',
            'FLAG_HIDE_LEGENDS_DIANCIE', 'MOVEMENT_TYPE_FACE_LEFT'),
        obj(name, 'LOCALID_LEGENDS_CARBINK_1', 'OBJ_EVENT_GFX_SPECIES(CARBINK)', 13, 8, P + 'Carbink',
            'FLAG_HIDE_LEGENDS_CARBINK', 'MOVEMENT_TYPE_FACE_LEFT'),
        obj(name, 'LOCALID_LEGENDS_CARBINK_2', 'OBJ_EVENT_GFX_SPECIES(CARBINK)', 11, 9, P + 'Carbink',
            'FLAG_HIDE_LEGENDS_CARBINK', 'MOVEMENT_TYPE_FACE_RIGHT')])


# ====================================================================== 4. Meloetta (Route 123)
FENCE = 0x549
GAP = (14, 7)                      # enige opening naar de bessenvelden; Snorlax ligt erin
FENCED = [(13, 7), (15, 7), (16, 7)]
FLUTE = (16, 8)
MELOETTA = (15, 9)
MELOETTA_LV = 62


def meloetta():
    name = 'Route123'
    P = name + '_EventScript_'
    for (x, y) in FENCED:
        assert tile(name, x, y) & 0x3ff in (0x001, FENCE & 0x3ff), (x, y, hex(tile(name, x, y)))
        set_tile(name, x, y, FENCE)
    blk = f'''{P}Legends2_Transition:
	setflag FLAG_HIDE_LEGENDS_POKE_FLUTE
	setflag FLAG_HIDE_LEGENDS_MELOETTA
	goto_if_set FLAG_ROUTE123_SNORLAX_GONE, {P}Legends2_TransitionMeloetta
	setflag FLAG_TEMP_14
	goto_if_unset FLAG_SYS_GAME_CLEAR, {P}Legends2_TransitionEnd
	clearflag FLAG_HIDE_LEGENDS_POKE_FLUTE
	return
{P}Legends2_TransitionMeloetta:
	goto_if_set FLAG_CAUGHT_MELOETTA, {P}Legends2_TransitionEnd
	clearflag FLAG_HIDE_LEGENDS_MELOETTA
{P}Legends2_TransitionEnd:
	return

{P}Snorlax::
	lock
	msgbox {P.replace('_EventScript_', '_Text_')}Snorlax, MSGBOX_DEFAULT
	release
	end

@ Post-game: de Poke Flute naast Snorlax. Oppakken = meteen spelen (geen ja/nee), Snorlax loopt weg, Meloetta komt.
{P}PokeFlute::
	lock
	removeobject LOCALID_LEGENDS_POKE_FLUTE
	setflag FLAG_HIDE_LEGENDS_POKE_FLUTE
	giveitem ITEM_POKE_FLUTE
	msgbox {P.replace('_EventScript_', '_Text_')}FluteBlow, MSGBOX_DEFAULT
	closemessage
	playfanfare MUS_RG_POKE_FLUTE
	waitfanfare
	playmoncry SPECIES_SNORLAX, CRY_MODE_ENCOUNTER
	applymovement LOCALID_LEGENDS_SNORLAX, Common_Movement_ExclamationMark
	waitmovement 0
	waitmoncry
	msgbox {P.replace('_EventScript_', '_Text_')}SnorlaxWakes, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_LEGENDS_SNORLAX, {P}Movement_SnorlaxLeaves
	waitmovement 0
	removeobject LOCALID_LEGENDS_SNORLAX
	setflag FLAG_ROUTE123_SNORLAX_GONE
	delay 30
	msgbox {P.replace('_EventScript_', '_Text_')}SomeoneHums, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_HIDE_LEGENDS_MELOETTA
	addobject LOCALID_LEGENDS_MELOETTA
	playse SE_M_HEAL_BELL
	waitse
	playmoncry SPECIES_MELOETTA_ARIA, CRY_MODE_ENCOUNTER
	msgbox {P.replace('_EventScript_', '_Text_')}MeloettaAppears, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	goto {P}Meloetta_Battle

{P}Movement_SnorlaxLeaves:
	walk_down
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_down
	step_end

''' + T(P.replace('_EventScript_', '_Text_') + 'Snorlax',
        "A SNORLAX is asleep in the only gap in the fence.\n\n"
        "Behind it: the BERRY MASTER's prize fields, eaten down to the dirt. In front of it: you. "
        "It has chosen a side.\n\n"
        "Snoring intensifies.") \
        + T(P.replace('_EventScript_', '_Text_') + 'FluteBlow',
            "A POKé FLUTE was lying next to SNORLAX, like a snooze button someone left out.\n\n"
            "You play it. Obviously.") \
        + T(P.replace('_EventScript_', '_Text_') + 'SnorlaxWakes',
            "SNORLAX woke up!\n\nIt looks at the berries. It looks at you. It decides neither is worth getting up "
            "for, gets up anyway, and wanders off to sleep somewhere quieter.") \
        + T(P.replace('_EventScript_', '_Text_') + 'SomeoneHums',
            "...Someone is humming your song back at you. Slightly better.") \
        + T(P.replace('_EventScript_', '_Text_') + 'MeloettaAppears',
            "MELOETTA drifted down out of nowhere!\n\n"
            "It was sleeping on SNORLAX's belly the whole time. Your solo has been reviewed. "
            "The review is a fight.")
    blk += battle_script(P, 'Meloetta', 'SPECIES_MELOETTA_ARIA', MELOETTA_LV, 'LOCALID_LEGENDS_MELOETTA',
                         'FLAG_HIDE_LEGENDS_MELOETTA', 'FLAG_CAUGHT_MELOETTA',
                         "La la laaa!\n\n(MELOETTA is still humming your POKé FLUTE tune. It has added a key change. "
                         "It wants a rematch.)",
                         "MELOETTA spun away mid-note.\n\nIt'll be back for the encore. It always comes back for "
                         "the encore.")
    scripts_block(name, blk, P + 'Legends2_Transition')
    put_objects(name, [
        obj(name, 'LOCALID_LEGENDS_SNORLAX', 'OBJ_EVENT_GFX_SPECIES(SNORLAX)', GAP[0], GAP[1], P + 'Snorlax',
            'FLAG_ROUTE123_SNORLAX_GONE', 'MOVEMENT_TYPE_FACE_DOWN'),
        obj(name, 'LOCALID_LEGENDS_POKE_FLUTE', 'OBJ_EVENT_GFX_ITEM_BALL', FLUTE[0], FLUTE[1], P + 'PokeFlute',
            'FLAG_HIDE_LEGENDS_POKE_FLUTE', 'MOVEMENT_TYPE_LOOK_AROUND'),
        obj(name, 'LOCALID_LEGENDS_MELOETTA', 'OBJ_EVENT_GFX_SPECIES(MELOETTA_ARIA)', MELOETTA[0], MELOETTA[1],
            P + 'Meloetta', 'FLAG_HIDE_LEGENDS_MELOETTA', 'MOVEMENT_TYPE_FACE_DOWN')])
    # Zolang Snorlax er ligt, heeft hij de bessenvelden kaalgegeten: de 12 bessenbomen achter het hek zijn dan
    # verborgen (FLAG_TEMP_14, gezet in ON_TRANSITION). Anders zitten er met de trainers erbij al 16 objecten in beeld
    # en verschijnen Snorlax/de fluit niet (max. 16 objecten).
    p = 'data/maps/%s/map.json' % name
    m = json.load(open(p))
    n = 0
    for o in m['object_events']:
        if o['graphics_id'] == 'OBJ_EVENT_GFX_BERRY_TREE' and 11 <= o['x'] <= 18 and 3 <= o['y'] <= 5:
            o['flag'] = 'FLAG_TEMP_14'; n += 1
    assert n == 12, n
    open(p, 'w').write(json.dumps(m, indent=2, ensure_ascii=False) + '\n')
    check_route123()


def check_route123():
    """Bereikbaarheid: met Snorlax in de opening zijn de bessenvelden dicht; het huis van de Berry Master,
    alle andere objecten en de uitgangen (oost/west) blijven bereikbaar."""
    name = 'Route123'
    L = layout(name)
    w, h = L['width'], L['height']
    data = struct.unpack('<%dH' % (w * h), open(L['blockdata_filepath'], 'rb').read())
    m = json.load(open('data/maps/%s/map.json' % name))
    blocked = {(o['x'], o['y']) for o in m['object_events']
               if o['graphics_id'] not in ('OBJ_EVENT_GFX_ITEM_BALL', 'OBJ_EVENT_GFX_CUTTABLE_TREE')
               and o.get('flag') not in ('FLAG_HIDE_LEGENDS_MELOETTA',)}
    door = (22, 6)

    def walk(start, blocked):
        seen, todo = {start}, [start]
        while todo:
            x, y = todo.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if not (0 <= n[0] < w and 0 <= n[1] < h) or n in seen or n in blocked:
                    continue
                if (data[n[1] * w + n[0]] >> 10) & 3 and n != door:
                    continue
                seen.add(n); todo.append(n)
        return seen
    start = (0, 13)
    with_snorlax = walk(start, blocked)
    assert door in with_snorlax, 'Berry Master-huis onbereikbaar'
    # het hoofdpad (y 12-16, met richels) ligt ver onder de opening; Snorlax en Meloetta staan er niet op
    assert all((x, y) in with_snorlax for x in range(1, 36) for y in (13,) if not (data[y * w + x] >> 10) & 3
               and (x, y) not in blocked), 'hoofdpad onderbroken'
    for f in ((11, 4), (14, 4), (17, 4), (12, 6)):
        assert f not in with_snorlax, ('bessenveld bereikbaar langs Snorlax', f)
    assert any(abs(FLUTE[0] - x) + abs(FLUTE[1] - y) == 1 for x, y in with_snorlax), 'fluit onbereikbaar'
    without = walk(start, blocked - {GAP})
    assert (14, 4) in without, 'bessenveld blijft dicht zonder Snorlax'


# ====================================================================== 5. Zygarde
def zygarde():
    name = 'DesertUnderpass'
    P = name + '_EventScript_'
    blk = f'''{P}Legends2_Transition:
	setflag FLAG_HIDE_LEGENDS_ZYGARDE
	goto_if_set FLAG_CAUGHT_ZYGARDE, {P}Legends2_TransitionEnd
	specialvar VAR_RESULT, Grounded_CaughtXerneasAndYveltal
	goto_if_eq VAR_RESULT, FALSE, {P}Legends2_TransitionEnd
	clearflag FLAG_HIDE_LEGENDS_ZYGARDE
{P}Legends2_TransitionEnd:
	return

'''
    blk += battle_script(P, 'Zygarde', 'SPECIES_ZYGARDE_50', 90, 'LOCALID_LEGENDS_ZYGARDE',
                         'FLAG_HIDE_LEGENDS_ZYGARDE', 'FLAG_CAUGHT_ZYGARDE',
                         "Grrrooo...\n\n(Life and death are both in your PC now. Somebody had to come and check "
                         "the paperwork. ZYGARDE is that somebody. It is unimpressed with your filing.)",
                         "ZYGARDE fell apart into a hundred little cells and crawled into the cracks.\n\n"
                         "That's not a retreat. That's a reorganisation. It'll be back.")
    scripts_block(name, blk, P + 'Legends2_Transition')
    put_objects(name, [obj(name, 'LOCALID_LEGENDS_ZYGARDE', 'OBJ_EVENT_GFX_SPECIES(ZYGARDE_50)', 79, 14,
                           P + 'Zygarde', 'FLAG_HIDE_LEGENDS_ZYGARDE', 'MOVEMENT_TYPE_FACE_RIGHT')])


if __name__ == '__main__':
    flags()
    articuno(); zapdos(); moltres()
    galar_articuno(); galar_zapdos(); galar_moltres()
    diancie(); meloetta(); zygarde()
    print('klaar')
