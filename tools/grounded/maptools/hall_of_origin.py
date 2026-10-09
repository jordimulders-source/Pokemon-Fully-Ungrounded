"""Project Grounded: Arceus, de Azure Flute en de Hall of Origin (SPACETIME_PLAN §3 stap 5-6; Jordi 9 okt).

  Stap 5  Na Spear Pillar (FLAG_SPACETIME_CORONET_DONE) word je naar het Coronet-portaal in de Spacetime Cave
          geteleporteerd. Daar spreekt ARCEUS (stem uit het niets, wit flitsend scherm, geen sprite): vang alle
          legendaries die nog over zijn, en hier is de AZURE FLUTE (Key Item, ITEM_AZURE_FLUTE). De fluit geeft vanuit
          de tas een hint over de volgende niet-gevangen legendary (lijst: tools/grounded/azure_flute.py,
          src/azure_flute.c, src/data/azure_flute_hints.h).
  Stap 6  Alles gevangen (of voorgoed op) -> de fluit: "meet me at SKY PILLAR" (FLAG_ARCEUS_SKY_PILLAR). Op de top
          van Sky Pillar (SkyPillar_Top) daalt dan een trap van licht neer naar de HALL OF ORIGIN:
            HallOfOrigin_Stairway  drie treden (nested terrassen), emissaries van lucht, zee en land (4 legendaries)
            HallOfOrigin_Atrium    plein met zuilen, emissaries van geest, dromen, rechtvaardigheid en vuur (5)
            HallOfOrigin_Summit    de top in Spear Pillar-stijl: emissaries van orde (6 Regi's) en tijd/ruimte (6),
                                   dan ARCEUS lv 100 (pas als alle negen emissaries verslagen zijn; Arceus healt je
                                   team eerst, hij wil een eerlijk gevecht). Verslagen = hij komt terug, gevangen = weg.
          Lichtfonteinen (bg-events) op de trap en in het atrium genezen je team.

Trainers: hergebruikte ongebruikte vanilla-constanten (117, 173, 462, 485, 486, 568, 581, 633, 634), hernoemd naar
TRAINER_HOO_*. Flags FLAG_GROUNDED 1220-1279 (blok 'hall_of_origin'; nieuwe items in nieuwe_items.py 1240-1259).
Tileset: coronet_snow (Spear Pillar). Teksten zijn placeholders in de huisstijl (Jordi herschrijft ze).
Patcht ook: SpacetimeCave (scène-haak, in het .inc en in spacetime_cave.py), SkyPillar_Top (scène, trap van licht),
src/battle_setup.c (eigen case voor Arceus) en schrijft data/scripts/azure_flute.inc.
Gebruik: python3 tools/grounded/maptools/hall_of_origin.py [render-uitmap]"""
import os as _os, sys as _sys  # noqa: E401
_sys.path.append(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
import check_levels  # noqa: E402
check_levels.protect()
import json, os, random, re, subprocess, sys  # noqa: E402,E401

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import coronet as co          # noqa: E402  (zet de werkmap op de repo-root en de tileset op coronet_snow)
import beacon_dragon as bd    # noqa: E402
import meteor_falls_ext as mf  # noqa: E402
import snowlib as sl          # noqa: E402

N = sl.N
ST, AT, SU = 'HallOfOrigin_Stairway', 'HallOfOrigin_Atrium', 'HallOfOrigin_Summit'
ORDER = [ST, AT, SU]
CONST = {ST: 'HALL_OF_ORIGIN_STAIRWAY', AT: 'HALL_OF_ORIGIN_ATRIUM', SU: 'HALL_OF_ORIGIN_SUMMIT'}
co.CONST.update(CONST)
MUSIC = 'MUS_SEALED_CHAMBER'          # placeholder tot de muziekfase
MAPSEC = ('MAPSEC_HALL_OF_ORIGIN', 'HALL OF ORIGIN', 'MAPPOPUP_THEME_MARBLE', 'Hall of Origin (Arceus)')
SKY_TOP_LANDING = (14, 10)             # aankomst op SkyPillar_Top bij terugkeer (nieuwe warp 1)
SKY_TOP_STAIR = (14, 8)                # bg-event: de trap van licht (vanaf (14, 9) noordwaarts aanspreken)

# ====================================================================== flags (FLAG_GROUNDED 1220-1279)
FLAGS = [
    (1220, 'FLAG_ARCEUS_MET', 'Arceus-scene in de Spacetime Cave gezien, Azure Flute ontvangen'),
    (1221, 'FLAG_ARCEUS_SKY_PILLAR', 'alle legendaries afgehandeld: Arceus wacht op Sky Pillar'),
    (1222, 'FLAG_HALL_OF_ORIGIN_OPEN', 'Sky Pillar: de trap van licht naar de Hall of Origin is neergedaald'),
    (1223, 'FLAG_HALL_ARCEUS_DONE', 'Hall of Origin: Arceus gevangen of verslagen (afsluitende tekst gezien)'),
    (1224, 'FLAG_HIDE_HALL_ARCEUS', 'Hall of Origin: Arceus-object verborgen (gezet in ON_TRANSITION als hij gevangen is)'),
]
# 1240-1259: nieuwe items (nieuwe_items.py); 1225-1239 en 1260-1279 nog vrij


def flags():
    p = 'include/constants/flags.h'
    s = open(p).read()
    blk = ('// hall_of_origin { (tools/grounded/maptools/hall_of_origin.py; FLAG_GROUNDED 1220-1279: 1240-1259 nieuwe '
           'items (blok nieuwe_items), 1225-1239 en 1260-1279 nog vrij)\n')
    for n, name, why in FLAGS:
        assert 1220 <= n <= 1279
        blk += '#define %-48s FLAG_GROUNDED(%d) // Project Grounded: %s\n' % (name, n, why)
    blk += '// }'
    if '// hall_of_origin {' in s:
        i = s.index('// hall_of_origin {'); j = s.index('// }', i) + 4
        s = s[:i] + blk + s[j:]
    else:
        anchor = s.index('// yoshis_island {')
        s = s[:anchor] + blk + '\n' + s[anchor:]
    for n, *_ in FLAGS:
        assert len(re.findall(r'FLAG_GROUNDED\(%d\)' % n, s)) == 1, ('flag dubbel', n)
    open(p, 'w').write(s)


# ====================================================================== nieuwe items (nergens anders te krijgen)
NEW_ITEMS = [  # (n, kaart, item, aantal, verborgen, omschrijving)
    (1240, ST, 'ITEM_COVERT_CLOAK', 1, False, 'Hall of Origin, trap: Covert Cloak'),
    (1241, AT, 'ITEM_CLEAR_AMULET', 1, False, 'Hall of Origin, atrium: Clear Amulet'),
    (1242, AT, 'ITEM_PUNCHING_GLOVE', 1, True, 'Hall of Origin, atrium: verborgen Punching Glove'),
    (1243, SU, 'ITEM_GRISEOUS_ORB', 1, False, 'Hall of Origin, top: Griseous Orb (Giratina Origin)'),
]


def new_items():
    p = os.path.join(HERE, 'nieuwe_items.py')
    s = open(p).read()
    rows = ''.join("    (%d, '%s', '%s', %d, %s, '%s'),\n" % r for r in NEW_ITEMS)
    blk = '    # Hall of Origin (hall_of_origin.py; flags uit het eigen blok FLAG_GROUNDED 1220-1279)\n' + rows
    if '# Hall of Origin (hall_of_origin.py' in s:
        i = s.index('    # Hall of Origin (hall_of_origin.py'); j = s.index('\n]\n', i) + 1
        s = s[:i] + blk + s[j:]
    else:
        i = s.index('\n]\nFIRST, LAST')
        s = s[:i + 1] + blk + s[i + 1:]
    if '(1240, 1259)' not in s:
        s = re.sub(r'EXTRA_RANGES = \[(.*?)\]', lambda m: 'EXTRA_RANGES = [%s, (1240, 1259)]' % m.group(1), s, count=1)
    assert '(1240, 1259)' in s
    open(p, 'w').write(s)
    import importlib
    import nieuwe_items as ni
    importlib.reload(ni)
    ni.flags()
    return ni


# ====================================================================== trainers (lv 100, legendaries)
IV = 'IVs: 31 HP / 31 Atk / 31 Def / 31 SpA / 31 SpD / 31 Spe'
AI = 'AI: Check Bad Move / Try To Faint / Check Viability / Smart Switching / Smart Mon Choices'


def mon(head, moves, lvl=100):
    return '\n'.join([head, 'Level: %d' % lvl, IV] + ['- ' + m for m in moves])


TRAINERS = [  # (sleutel, id, oude constante, naam, klasse, pic, gender, gfx, team, waarom)
    # de emissaries zijn constructen van ARCEUS: eigen klasse en sprite, paletwissel per thema (tools/grounded/construct_sprites.py)
    ('STRATOS', 117, 'CINDY_2', 'STRATOS', 'Construct', 'Construct Sky', 'Male', 'OBJ_EVENT_GFX_CONSTRUCT_SKY', [
        mon('Ho-Oh @ Leftovers', ['Sacred Fire', 'Brave Bird', 'Earthquake', 'Recover']),
        mon('Tornadus', ['Hurricane', 'Heat Wave', 'Focus Blast', 'Tailwind']),
        mon('Thundurus', ['Thunderbolt', 'Focus Blast', 'Grass Knot', 'Nasty Plot']),
        mon('Rayquaza @ Life Orb', ['Dragon Ascent', 'Extreme Speed', 'Earthquake', 'Dragon Dance'])],
     'Hall of Origin, trap: emissary van de lucht'),
    ('THALASSA', 173, 'DUDLEY', 'THALASSA', 'Construct', 'Construct Sea', 'Male', 'OBJ_EVENT_GFX_CONSTRUCT_SEA', [
        mon('Tapu Fini', ['Moonblast', 'Surf', "Nature's Madness", 'Calm Mind']),
        mon('Suicune', ['Scald', 'Ice Beam', 'Extrasensory', 'Calm Mind']),
        mon('Lugia @ Leftovers', ['Aeroblast', 'Psychic', 'Roost', 'Calm Mind']),
        mon('Kyogre @ Mystic Water', ['Origin Pulse', 'Ice Beam', 'Thunder', 'Calm Mind'])],
     'Hall of Origin, trap: emissary van de zee'),
    ('BEDROCK', 462, 'KAYLEE', 'BEDROCK', 'Construct', 'Construct Land', 'Male', 'OBJ_EVENT_GFX_CONSTRUCT_LAND', [
        mon('Terrakion', ['Close Combat', 'Stone Edge', 'Earthquake', 'Swords Dance']),
        mon('Ting-Lu @ Leftovers', ['Ruination', 'Earthquake', 'Heavy Slam', 'Stealth Rock']),
        mon('Landorus', ['Earth Power', 'Sludge Bomb', 'Stone Edge', 'Rock Polish']),
        mon('Groudon @ Soft Sand', ['Precipice Blades', 'Stone Edge', 'Fire Punch', 'Swords Dance'])],
     'Hall of Origin, trap: emissary van het land'),
    ('NOUS', 485, 'AMY_AND_LIV_3', 'NOUS', 'Construct', 'Construct Mind', 'Male', 'OBJ_EVENT_GFX_CONSTRUCT_MIND', [
        mon('Uxie', ['Psychic', 'U-turn', 'Yawn', 'Stealth Rock']),
        mon('Mesprit', ['Psychic', 'Ice Beam', 'Thunderbolt', 'Calm Mind']),
        mon('Azelf', ['Psychic', 'Flamethrower', 'Dazzling Gleam', 'Nasty Plot']),
        mon('Deoxys @ Focus Sash', ['Psycho Boost', 'Superpower', 'Extreme Speed', 'Ice Beam']),
        mon('Mewtwo @ Life Orb', ['Psystrike', 'Aura Sphere', 'Ice Beam', 'Recover'])],
     'Hall of Origin, atrium: emissary van de geest'),
    ('SOMNIA', 486, 'GINA_AND_MIA_2', 'SOMNIA', 'Construct', 'Construct Dream', 'Male', 'OBJ_EVENT_GFX_CONSTRUCT_DREAM', [
        mon('Cresselia @ Leftovers', ['Psychic', 'Moonblast', 'Moonlight', 'Calm Mind']),
        mon('Jirachi', ['Doom Desire', 'Psychic', 'Thunderbolt', 'Calm Mind']),
        mon('Tapu Lele', ['Psychic', 'Moonblast', 'Focus Blast', 'Calm Mind']),
        mon('Mew', ['Psychic', 'Aura Sphere', 'Will-O-Wisp', 'Nasty Plot']),
        mon('Darkrai @ Life Orb', ['Dark Pulse', 'Sludge Bomb', 'Focus Blast', 'Nasty Plot'])],
     'Hall of Origin, atrium: emissary van de dromen'),
    ('GLADIUS', 568, 'GRUNT_UNUSED', 'GLADIUS', 'Construct', 'Construct Justice', 'Male', 'OBJ_EVENT_GFX_CONSTRUCT_JUSTICE', [
        mon('Virizion', ['Leaf Blade', 'Close Combat', 'Stone Edge', 'Swords Dance']),
        mon('Cobalion', ['Close Combat', 'Iron Head', 'Stone Edge', 'Swords Dance']),
        mon('Keldeo', ['Secret Sword', 'Hydro Pump', 'Air Slash', 'Calm Mind']),
        mon('Urshifu_Rapid_Strike @ Choice Band', ['Surging Strikes', 'Close Combat', 'Aqua Jet', 'U-turn']),
        mon('Zacian @ Rusted Sword', ['Behemoth Blade', 'Play Rough', 'Close Combat', 'Swords Dance'])],
     'Hall of Origin, atrium: emissary van de rechtvaardigheid'),
    ('HEPHAEST', 581, 'TERRY', 'HEPHAEST', 'Construct', 'Construct Forge', 'Male', 'OBJ_EVENT_GFX_CONSTRUCT_FORGE', [
        mon('Victini', ['V-create', 'Zen Headbutt', 'U-turn', 'Bolt Strike']),
        mon('Volcanion', ['Steam Eruption', 'Flamethrower', 'Earth Power', 'Sludge Bomb']),
        mon('Chi-Yu', ['Heat Wave', 'Dark Pulse', 'Psychic', 'Nasty Plot']),
        mon('Heatran @ Leftovers', ['Magma Storm', 'Earth Power', 'Flash Cannon', 'Stealth Rock']),
        mon('Reshiram @ Charcoal', ['Blue Flare', 'Draco Meteor', 'Earth Power', 'Roost'])],
     'Hall of Origin, atrium: emissary van het vuur (de smidse)'),
    ('ORDO', 633, 'LUCAS_2', 'ORDO', 'Construct', 'Construct Order', 'Male', 'OBJ_EVENT_GFX_CONSTRUCT_ORDER', [
        mon('Regirock', ['Stone Edge', 'Hammer Arm', 'Curse', 'Stealth Rock']),
        mon('Regice', ['Ice Beam', 'Thunderbolt', 'Focus Blast', 'Amnesia']),
        mon('Registeel', ['Iron Head', 'Body Press', 'Iron Defense', 'Curse']),
        mon('Regieleki', ['Thunder Cage', 'Volt Switch', 'Extreme Speed', 'Thunder Wave']),
        mon('Regidrago', ['Dragon Energy', 'Draco Meteor', 'Fire Fang', 'Earthquake']),
        mon('Regigigas @ Leftovers', ['Body Slam', 'Knock Off', 'Earthquake', 'Drain Punch'])],
     'Hall of Origin, top: emissary van de orde (de bouwers)'),
    ('KAIROS', 634, 'MIKE_1', 'KAIROS', 'Construct', 'Construct Spacetime', 'Male', 'OBJ_EVENT_GFX_CONSTRUCT_SPACETIME', [
        mon('Celebi', ['Leaf Storm', 'Psychic', 'Earth Power', 'Recover']),
        mon('Hoopa-Unbound', ['Hyperspace Fury', 'Psychic', 'Gunk Shot', 'Drain Punch']),
        mon('Eternatus', ['Dynamax Cannon', 'Sludge Bomb', 'Flamethrower', 'Recover']),
        mon('Giratina-Origin @ Griseous Core', ['Shadow Force', 'Draco Meteor', 'Earthquake', 'Will-O-Wisp']),
        mon('Palkia @ Lustrous Orb', ['Spacial Rend', 'Hydro Pump', 'Thunderbolt', 'Fire Blast']),
        mon('Dialga @ Adamant Orb', ['Roar of Time', 'Flash Cannon', 'Earth Power', 'Fire Blast'])],
     'Hall of Origin, top: emissary van tijd en ruimte (de laatste)'),
]
TR = {t[0]: t for t in TRAINERS}


def const(s):
    return re.sub(r'[^A-Z0-9]+', '_', s.upper().replace("'", '')).strip('_')


def check_names():
    moves = set(re.findall(r'#define (MOVE_\w+)', open('include/constants/moves.h').read()))
    species = set(re.findall(r'#define (SPECIES_\w+)', open('include/constants/species.h').read()))
    items = set(re.findall(r'#define (ITEM_\w+)', open('include/constants/items.h').read()))
    for key, n, old, nm, cls, pic, gender, gfx, team, why in TRAINERS:
        for block in team:
            head = block.split('\n')[0]
            sp, _, it = head.partition(' @ ')
            assert 'SPECIES_' + const(sp) in species, (key, sp)
            assert not it or 'ITEM_' + const(it) in items, (key, it)
            for line in block.split('\n'):
                if line.startswith('- '):
                    assert 'MOVE_' + const(line[2:]) in moves, (key, line)


def trainers():
    check_names()
    p = 'include/constants/opponents.h'
    s = open(p).read()
    for key, n, old, nm, cls, pic, gender, gfx, team, why in TRAINERS:
        new = 'TRAINER_HOO_' + key
        line = '#define %-35s %d // Project Grounded: %s (was TRAINER_%s, ongebruikt)' % (new, n, why, old)
        pat = re.compile(r'^#define TRAINER_\w+\s+%d\b.*$' % n, re.M)
        hits = pat.findall(s)
        assert len(hits) == 1, ('trainer-id', n, hits)
        assert ('TRAINER_' + old) in hits[0] or new in hits[0], ('onverwachte constante', n, hits[0])
        s = pat.sub(line, s, 1)
    open(p, 'w').write(s)
    p = 'src/data/trainers.party'
    s = open(p).read()
    for key, n, old, nm, cls, pic, gender, gfx, team, why in TRAINERS:
        new = 'TRAINER_HOO_' + key
        hdr = ['Name: ' + nm, 'Class: ' + cls, 'Pic: ' + pic, 'Gender: ' + gender, 'Music: Intense',
               'Items: Full Restore / Full Restore', 'Double Battle: No', AI]
        blk = '/* Project Grounded: %s (hall_of_origin.py) */\n=== %s ===\n%s\n\n%s\n\n' % (
            why, new, '\n'.join(hdr), '\n\n'.join(team))
        for name in (new, 'TRAINER_' + old):
            tag = '=== %s ===\n' % name
            if tag in s:
                t0 = i = s.index(tag)
                k = s.rfind('\n', 0, i - 1) + 1
                if s[k:i].startswith('/* Project Grounded: '):
                    i = k
                j = s.find('\n=== ', t0 + len(tag))       # vanaf de eigen kop zoeken, niet vanaf het commentaar
                if j < 0:
                    j = len(s)
                else:
                    j += 1
                    k = s.rfind('\n', 0, j - 1) + 1         # commentaar van het volgende blok laten staan
                    if s[k:j].startswith('/* '):
                        j = k
                s = s[:i] + blk + s[j:]
                break
        else:
            raise SystemExit('trainerblok niet gevonden: %s / %s' % (new, old))
    open(p, 'w').write(s.rstrip('\n') + '\n')


# ====================================================================== kaarten
def rect(x0, y0, x1, y1):
    return co.rect(x0, y0, x1, y1)


def sky(W, H, seed):
    """Leegte van licht en wolken (tileset spear_pillar, palet LITE): onbegaanbaar."""
    sl.use_tileset('spear_pillar')
    m = sl.M(W, H)
    for y in range(H):
        for x in range(W):
            m.put(x, y, 'cloud_%d%d' % (x % 2, y % 2), 1, 3)
    return m, random.Random(seed)


def lfloor(rnd):
    def f(x, y):
        r = rnd.random()
        return 'lfloor0' if r < 0.82 else 'lfloor1' if r < 0.93 else 'lfloor2'
    return f


def platform(m, rnd, x0, y0, x1, y1, gap):
    """Zwevend platform van licht (wit glas, gouden rand, gloeiende onderkant) met een trapgat in het zuiden."""
    co.ruin_platform(m, rnd, x0, y0, x1, y1, gap, pre='lrim_', floor=lfloor(rnd), landing=False)


def light_stair(m, gap, ya, yb, top=False, bot=False):
    """Trap van licht van rij ya t/m yb (ya = boven); top/bot = pijl-warp (noord/zuid) op de uiterste rij."""
    for y in range(ya, yb + 1):
        part = 'top' if (top and y == ya) else 'bot' if (bot and y == yb) else 'mid'
        for i, x in enumerate(gap):
            m.put(x, y, 'lstair_%s_%s' % (part, 'lr'[i]), 0, 3)


def runner(m, gap, ya, yb):
    """Loper van licht over het middenpad (rij ya t/m yb)."""
    for y in range(ya, yb + 1):
        m.put(gap[0], y, 'lrun_l', 0)
        m.put(gap[1], y, 'lrun_r', 0)


def put_art(m, key, x, y):
    return co.put_obj(m, key, x, y)


def decor_pillars(m, rows, keep):
    taken = set()
    for key, x, y in rows:
        cells = put_art(m, key, x, y)
        assert not cells & keep, ('pilaar op een pad/event', key, x, y)
        taken |= cells
    return taken


def mirror(items, x0, x1, swap=None):
    out = []
    for key, x, y in items:
        w = co.ctt.spear_blocked()[1][key][0]
        out.append((key, x, y))
        out.append(((swap or {}).get(key, key), x0 + x1 - x - w + 1, y))
    return out


MAPS, EV = {}, {}


# --------------------------------------------------------------------- de trap (lucht, zee, land): drie zwevende platforms
ST_W, ST_H = 26, 52
ST_GAP = (12, 13)
ST_TRAINERS = {'STRATOS': ((8, 40), 'RIGHT', 5), 'THALASSA': ((17, 27), 'LEFT', 5), 'BEDROCK': ((9, 13), 'RIGHT', 4)}
ST_FOUNTAIN = (8, 44)


def build_stairway(ni):
    m, rnd = sky(ST_W, ST_H, 6101)
    g = ST_GAP
    platform(m, rnd, 4, 36, 21, 45, g)
    platform(m, rnd, 6, 22, 19, 31, g)
    platform(m, rnd, 8, 8, 17, 17, g)
    for ya, yb in ((37, 44), (23, 30), (9, 16)):
        runner(m, g, ya, yb)
    light_stair(m, g, 47, 49, bot=True)
    light_stair(m, g, 33, 36)
    light_stair(m, g, 19, 22)
    light_stair(m, g, 4, 8, top=True)
    EV[ST] = {'entry': [(g[0], 49), (g[1], 49)], 'top': [(g[0], 4), (g[1], 4)]}
    it = co.item_list(ni, ST)
    EV[ST]['items'] = [((16, 30), it[0][1], it[0][0], it[0][2], it[0][3])]
    keep = {p for p, *_ in ST_TRAINERS.values()} | {ST_FOUNTAIN, (16, 30)} | set(co.rect(11, 9, 14, 44))
    for _, (xy, face, n) in ST_TRAINERS.items():
        dx, dy = co.FACE[face]
        keep |= {(xy[0] + dx * k, xy[1] + dy * k) for k in range(0, n + 1)}
    pil = mirror([('mpillar', 5, 37), ('mbroken', 5, 42), ('mpillar', 7, 23), ('mbroken', 9, 9)], 4, 21) + \
        mirror([('mbroken', 7, 28)], 6, 19)
    decor_pillars(m, pil, keep)
    m.put(*ST_FOUNTAIN, 'fountain', 1)
    return m


# --------------------------------------------------------------------- het atrium (geest, dromen, recht, vuur)
AT_W, AT_H = 34, 40
AT_GAP = (16, 17)
AT_TRAINERS = {'NOUS': ((12, 29), 'RIGHT', 4), 'SOMNIA': ((21, 26), 'LEFT', 4),
               'GLADIUS': ((12, 18), 'RIGHT', 4), 'HEPHAEST': ((21, 15), 'LEFT', 4)}
AT_FOUNTAIN = (8, 31)


def build_atrium(ni):
    m, rnd = sky(AT_W, AT_H, 6102)
    g = AT_GAP
    platform(m, rnd, 3, 9, 30, 33, g)
    runner(m, g, 10, 32)
    light_stair(m, g, 35, 37, bot=True)
    light_stair(m, g, 4, 9, top=True)
    EV[AT] = {'entry': [(g[0], 37), (g[1], 37)], 'top': [(g[0], 4), (g[1], 4)]}
    it = co.item_list(ni, AT)
    EV[AT]['items'] = [((27, 30), it[0][1], it[0][0], it[0][2], it[0][3]),
                       ((9, 22), it[1][1], it[1][0], it[1][2], it[1][3])]
    keep = {p for p, *_ in AT_TRAINERS.values()} | {AT_FOUNTAIN, (27, 30), (9, 22)} | set(co.rect(15, 10, 18, 32))
    for _, (xy, face, n) in AT_TRAINERS.items():
        dx, dy = co.FACE[face]
        keep |= {(xy[0] + dx * k, xy[1] + dy * k) for k in range(0, n + 1)}
    pil = mirror([('mpillar', 4, 10), ('mpillar', 4, 16), ('mbroken', 4, 22), ('mpillar', 4, 27),
                  ('mpillar', 10, 10), ('mbroken', 10, 24), ('mpillar', 9, 17)], 3, 30, {'mbroken': 'mpillar', 'mpillar': 'mpillar'})
    decor_pillars(m, pil, keep)
    m.put(*AT_FOUNTAIN, 'fountain', 1)
    return m


# --------------------------------------------------------------------- de top (orde, tijd/ruimte, Arceus)
SU_W, SU_H = 30, 36
SU_GAP = (14, 15)
SU_TRAINERS = {'ORDO': ((11, 18), 'RIGHT', 4), 'KAIROS': ((15, 14), 'DOWN', 3)}
SU_DAIS = (13, 7)
SU_ARCEUS = (14, 9)
SU_ALTARS = [(8, 8), (20, 8)]


def build_summit(ni):
    m, rnd = sky(SU_W, SU_H, 6103)
    g = SU_GAP
    platform(m, rnd, 3, 5, 26, 29, g)
    runner(m, g, 11, 28)
    light_stair(m, g, 31, 33, bot=True)
    EV[SU] = {'entry': [(g[0], 33), (g[1], 33)]}
    put_art(m, 'dais', *SU_DAIS)
    for i, (x, y) in enumerate(SU_ALTARS):
        put_art(m, 'altar_l_' + ('dialga', 'palkia')[i], x, y)
    it = co.item_list(ni, SU)
    EV[SU]['items'] = [((23, 9), it[0][1], it[0][0], it[0][2], it[0][3])]
    keep = {p for p, *_ in SU_TRAINERS.values()} | {(23, 9), (14, 10), (15, 10)} | set(co.rect(13, 7, 16, 28))
    keep |= {(x + dx, 10) for x, _ in SU_ALTARS for dx in (0, 1)}
    for _, (xy, face, n) in SU_TRAINERS.items():
        dx, dy = co.FACE[face]
        keep |= {(xy[0] + dx * k, xy[1] + dy * k) for k in range(0, n + 1)}
    pil = mirror([('mpillar', 4, 6), ('mpillar', 4, 12), ('mbroken', 4, 18), ('mpillar', 4, 23),
                  ('mbroken', 8, 14), ('mpillar', 9, 22), ('mpillar', 11, 7)], 3, 26, {'mbroken': 'mpillar', 'mpillar': 'mbroken'})
    decor_pillars(m, pil, keep)
    return m


BUILD = {ST: build_stairway, AT: build_atrium, SU: build_summit}


def build_maps(ni):
    for name in ORDER:
        m = BUILD[name](ni)
        g = co.snow_g(m)
        MAPS[name] = g
        co.save(name, g, co.SEC_SPEAR, [N['cloud_00'], N['cloud_10'], N['cloud_01'], N['cloud_11']])
    sl.use_tileset('coronet_snow')


def mapsecs():
    saved = co.MAPSECS
    co.MAPSECS = [MAPSEC]
    try:
        co.mapsecs()
    finally:
        co.MAPSECS = saved


def battle_setup():
    p = 'src/battle_setup.c'
    s = open(p).read()
    if 'case SPECIES_ARCEUS_NORMAL' not in s:
        a = '    case SPECIES_ZERAORA:'
        assert a in s
        s = s.replace(a, '    case SPECIES_ARCEUS_NORMAL: // Project Grounded: Hall of Origin (placeholder: Kanto-legendary-'
                         'thema, het licht valt in banen)\n'
                         '        CreateBattleStartTask(B_TRANSITION_WHITE_BARS_FADE, MUS_RG_VS_LEGEND);\n        break;\n'
                         + a, 1)
        open(p, 'w').write(s)


# ====================================================================== scripts
def head(name, scripts=()):
    os.makedirs('data/maps/' + name, exist_ok=True)
    h = '@ Project Grounded: %s (tools/grounded/maptools/hall_of_origin.py)\n%s_MapScripts::\n' % (name, name)
    for kind, lbl in scripts:
        h += '\tmap_script %s, %s\n' % (kind, lbl)
    return h + '\t.byte 0\n'


TEXTS = {  # sleutel -> (intro, verloren, daarna); constructen van ARCEUS (placeholders in de huisstijl)
    'STRATOS': ("CONSTRUCT ONLINE. DESIGNATION: SKY.\n\nARCEUS carved me out of a cloud. "
                "It took six tries. The other five drifted off.",
                "Altitude... lost. Filing a complaint with gravity.",
                "My maker watches through my eyes. Wave. No, the other eye."),
    'THALASSA': ("CONSTRUCT ONLINE. DESIGNATION: SEA.\n\nI am made of stone and I guard the ocean. "
                 "Nobody at the planning meeting saw the problem.",
                 "Sinking. As predicted. By everyone.",
                 "Every ocean in every dimension says hi. They're mostly salty about it."),
    'BEDROCK': ("CONSTRUCT ONLINE. DESIGNATION: LAND.\n\nI was the first thing ARCEUS made after the floor. "
                "Technically, I am also the floor.",
                "Eroded. It happens to the best of us. Slowly, usually.",
                "Mind the steps. They're my cousins. They bite."),
    'NOUS': ("CONSTRUCT ONLINE. DESIGNATION: MIND.\n\nI already calculated how this ends. "
             "I'm only here because ARCEUS likes to watch the numbers happen.",
             "Recalculating. Recalculating. ...Oh no.",
             "I have no thoughts of my own. ARCEUS lends me his. They're very loud."),
    'SOMNIA': ("CONSTRUCT ONLINE. DESIGNATION: DREAMS.\n\nStatues don't sleep. I've been awake for "
               "four thousand years. Ask me how I'm doing.",
               "Finally. Darkness. Five more minutes.",
               "If you see yourself falling, don't worry. That's just the next floor."),
    'GLADIUS': ("CONSTRUCT ONLINE. DESIGNATION: JUSTICE.\n\nARCEUS gave me a sword arm and no sword. "
                "I've been very fair about it.",
                "Justice served. Cold. With a side of gravel.",
                "The forge is next door. Don't touch anything glowing. Everything is glowing."),
    'HEPHAEST': ("CONSTRUCT ONLINE. DESIGNATION: FORGE.\n\nI built the other eight. Then they asked "
                 "who built me. Awkward silence. Fourteen centuries of it.",
                 "Cracked. Hairline. Don't tell the others.",
                 "Upstairs are the last two. One of them alphabetises time."),
    'ORDO': ("CONSTRUCT ONLINE. DESIGNATION: ORDER.\n\nSix golems, one ancient blueprint, "
             "and me: the prototype. ARCEUS kept the receipt.",
             "Order... disrupted. Filing it under 'you'.",
             "REGIGIGAS is slow to start. So was creation. Look how that turned out."),
    'KAIROS': ("CONSTRUCT ONLINE. DESIGNATION: TIME AND SPACE.\n\nI am the last door. ARCEUS is behind me. "
               "Literally. Don't look, it makes him self-conscious.",
               "That... was the right moment. Just not for me.",
               "ARCEUS is waiting on the wheel. It has been waiting since before waiting was invented."),
}


def tr_objs(S, table):
    objs = []
    for key, (xy, face, n) in table.items():
        script = S.trainer(key.title(), 'HOO_' + key, *TEXTS[key])
        objs.append(bd.tr(TR[key][7], xy[0], xy[1], script, face, n))
    return objs


def items_ev(name):
    objs, bgs = [], []
    for p, it, fl, q, hid in EV[name].get('items', []):
        if hid:
            bgs.append(co.hidden(p, it, fl, q))
        else:
            o = bd.ball(p[0], p[1], it, fl)
            if q > 1:
                o['movement_range_x'] = q
            objs.append(o)
    return objs, bgs


def write_map(name, objs, warps, bgs, coords=(), scripts_head=None):
    co.MUSIC[name] = MUSIC
    co.write_map(name, objs, warps, bgs, coords, region_map_section=MAPSEC[0], show_map_name=(name == ST),
                 map_type='MAP_TYPE_ROUTE', weather='WEATHER_NONE')


FOUNTAIN_TEXT = ("A pool of light, humming to itself. Your POKéMON drink from it and look healthier.\n\n"
                 "You feel judged, but in a supportive way.")


def fountain(S, key):
    S.raw(f"""{S.P}{key}::
	lockall
	fadescreen FADE_TO_WHITE
	special HealPlayerParty
	fadescreen FADE_FROM_WHITE
	msgbox {S.T}Fountain, MSGBOX_DEFAULT
	releaseall
	end
""", [('Fountain', FOUNTAIN_TEXT)])
    return S.P + key


def events():
    # ---------------------------------------------------------------- trap
    S = bd.Scr(ST, head(ST))
    objs = tr_objs(S, ST_TRAINERS)
    fs = fountain(S, 'Fountain')
    S.write()
    io, ib = items_ev(ST)
    e, d = EV[ST]['entry'], EV[ST]['top']
    # terug naar waar je vandaan kwam (Spear Pillar of Sky Pillar): MAP_DYNAMIC; een warp-tegel naar deze kaart zet de
    # dynamische warp vanzelf (field_control_avatar.c), de scripts op Sky Pillar met setdynamicwarp
    dyn = lambda x, y: {'x': x, 'y': y, 'elevation': 3, 'dest_map': 'MAP_DYNAMIC', 'dest_warp_id': 'WARP_ID_DYNAMIC'}  # noqa: E731
    warps = [dyn(*e[0]), dyn(*e[1]), bd.warp(d[0][0], d[0][1], CONST[AT], 0, elev=3),
             bd.warp(d[1][0], d[1][1], CONST[AT], 0, elev=3)]
    bgs = [bd.sign(ST_FOUNTAIN[0], ST_FOUNTAIN[1], fs)] + ib
    write_map(ST, objs + io, warps, bgs)
    # ---------------------------------------------------------------- atrium
    S = bd.Scr(AT, head(AT))
    objs = tr_objs(S, AT_TRAINERS)
    fs = fountain(S, 'Fountain')
    S.write()
    io, ib = items_ev(AT)
    e, d = EV[AT]['entry'], EV[AT]['top']
    warps = [bd.warp(e[0][0], e[0][1], CONST[ST], 2, elev=3), bd.warp(e[1][0], e[1][1], CONST[ST], 3, elev=3),
             bd.warp(d[0][0], d[0][1], CONST[SU], 0, elev=3), bd.warp(d[1][0], d[1][1], CONST[SU], 1, elev=3)]
    bgs = [bd.sign(AT_FOUNTAIN[0], AT_FOUNTAIN[1], fs)] + ib
    write_map(AT, objs + io, warps, bgs)
    # ---------------------------------------------------------------- top
    S = bd.Scr(SU, head(SU, [('MAP_SCRIPT_ON_TRANSITION', SU + '_OnTransition')]))
    objs = tr_objs(S, SU_TRAINERS)
    P, T = S.P, S.T
    keys = [k for k, *_ in TRAINERS]
    count = ''.join('\tcall_if_defeated TRAINER_HOO_%s, %sCountOne\n' % (k, P) for k in keys)
    S.raw(f"""{SU}_OnTransition:
	getcaughtmon SPECIES_ARCEUS
	call_if_ne VAR_RESULT, 0, {P}HideArceus
	call_if_eq VAR_RESULT, 0, {P}ShowArceus
	end

{P}HideArceus:
	setflag FLAG_HIDE_HALL_ARCEUS
	return

{P}ShowArceus:
	clearflag FLAG_HIDE_HALL_ARCEUS
	return

{P}CountOne:
	addvar VAR_0x8005, 1
	return

{P}Arceus::
	lock
	setvar VAR_0x8005, 0
{count}	goto_if_ne VAR_0x8005, {len(keys)}, {P}ArceusNotYet
	goto_if_set FLAG_HALL_ARCEUS_DONE, {P}ArceusAgain
	msgbox {T}ArceusGreeting, MSGBOX_DEFAULT
	goto {P}ArceusBattle

{P}ArceusAgain:
	msgbox {T}ArceusAgain, MSGBOX_DEFAULT
{P}ArceusBattle:
	closemessage
	fadescreen FADE_TO_WHITE
	special HealPlayerParty
	fadescreen FADE_FROM_WHITE
	msgbox {T}ArceusHeals, MSGBOX_DEFAULT
	closemessage
	setvar VAR_0x8004, 3
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 3
	special ShakeCamera
	waitstate
	playmoncry SPECIES_ARCEUS, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_ARCEUS, 100
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}ArceusWaits
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}ArceusWaits
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {P}ArceusCaught
	fadescreen FADE_TO_WHITE
	removeobject LOCALID_HALL_ARCEUS
	fadescreen FADE_FROM_WHITE
	call_if_unset FLAG_HALL_ARCEUS_DONE, {P}Epilogue
	msgbox {T}ArceusDefeated, MSGBOX_DEFAULT
	release
	end

{P}ArceusCaught:
	removeobject LOCALID_HALL_ARCEUS
	setflag FLAG_HIDE_HALL_ARCEUS
	call_if_unset FLAG_HALL_ARCEUS_DONE, {P}Epilogue
	msgbox {T}ArceusCaught, MSGBOX_DEFAULT
	release
	end

{P}Epilogue:
	setflag FLAG_HALL_ARCEUS_DONE
	msgbox {T}Epilogue, MSGBOX_DEFAULT
	return

{P}ArceusWaits:
	msgbox {T}ArceusWaits, MSGBOX_DEFAULT
	release
	end

{P}ArceusNotYet:
	buffernumberstring STR_VAR_1, VAR_0x8005
	msgbox {T}ArceusNotYet, MSGBOX_DEFAULT
	release
	end

{P}Altar::
	msgbox {T}Altar, MSGBOX_DEFAULT
	end
""", [
        ('ArceusGreeting', "ARCEUS: So. You came.\n\nEvery legend in every dimension, accounted for. You even "
                           "brought the flute back. Most people lose it in a sofa.\n\nI made the world. Let us see "
                           "what the world made."),
        ('ArceusAgain', "ARCEUS: Again? Good. I was getting bored, and I invented boredom."),
        ('ArceusHeals', "A warm light washes over your team.\n\nARCEUS: There. Now nobody can say it wasn't fair."),
        ('ArceusDefeated', "ARCEUS dissolves into a thousand plates of light.\n\nARCEUS: A draw, on my scale. "
                           "I'll be here. I'm always here. Come back with a ball you believe in."),
        ('ArceusCaught', "The ball doesn't even wobble. It just... accepts it.\n\nSomewhere, the universe files a "
                         "change of address."),
        ('Epilogue', "For a moment, everything is very quiet. Time stops ticking. Space stops being big.\n\n"
                     "Then a voice, from everywhere at once:\n\nARCEUS: Thank you for playing.\n\n...It means "
                     "the game. The world. Both. Go home. Have a sandwich. You've earned it."),
        ('ArceusWaits', "ARCEUS: You ran. That's fine. I have all the time there is. Literally."),
        ('ArceusNotYet', "ARCEUS watches you from the golden wheel.\n\nARCEUS: My constructs have opinions about you. "
                         "{STR_VAR_1} of nine have shared theirs.\n\nHear the rest. Then we talk."),
        ('Altar', "An altar of white stone. It hums at a frequency only very old things can hear."),
    ])
    S.write()
    io, ib = items_ev(SU)
    objs = objs + io
    objs.append(bd.obj('OBJ_EVENT_GFX_SPECIES(ARCEUS)', SU_ARCEUS[0], SU_ARCEUS[1], P + 'Arceus',
                       'FLAG_HIDE_HALL_ARCEUS', move='MOVEMENT_TYPE_FACE_DOWN', local_id='LOCALID_HALL_ARCEUS'))
    bgs = ib
    for (x, y) in SU_ALTARS:
        for dx in (0, 1):
            bgs.append(bd.sign(x + dx, y + 1, P + 'Altar', 'BG_EVENT_PLAYER_FACING_NORTH'))
    e = EV[SU]['entry']
    write_map(SU, objs, [bd.warp(e[0][0], e[0][1], CONST[AT], 2, elev=3),
                         bd.warp(e[1][0], e[1][1], CONST[AT], 3, elev=3)], bgs)


# ---------------------------------------------------------------- de fluit, de hub-scène en Sky Pillar
GLOBAL_INC = 'data/scripts/azure_flute.inc'


def text_block(label, s):
    return bd.text(label, s)


def global_scripts():
    code = f"""@ Project Grounded: Azure Flute, Arceus in de Spacetime Cave en de trap van licht op Sky Pillar.
@ Gegenereerd door tools/grounded/maptools/hall_of_origin.py; de hintlijst door tools/grounded/azure_flute.py.

@ ---------------------------------------------------------------- de fluit (vanuit de tas, src/item_use.c)
EventScript_AzureFlute::
	lockall
	playfanfare MUS_RG_POKE_FLUTE
	goto_if_set FLAG_HALL_ARCEUS_DONE, AzureFlute_EventScript_AfterArceus
	goto_if_set FLAG_HALL_OF_ORIGIN_OPEN, AzureFlute_EventScript_StairOpen
	goto_if_set FLAG_ARCEUS_SKY_PILLAR, AzureFlute_EventScript_SkyPillar
	special AzureFlute_GetHint
	goto_if_eq VAR_RESULT, 0, AzureFlute_EventScript_AllDone
	msgbox gStringVar4, MSGBOX_DEFAULT
	releaseall
	end

AzureFlute_EventScript_AllDone:
	call AzureFlute_EventScript_Flash
	msgbox AzureFlute_Text_AllDone, MSGBOX_DEFAULT
	setflag FLAG_ARCEUS_SKY_PILLAR
	releaseall
	end

AzureFlute_EventScript_SkyPillar:
	msgbox AzureFlute_Text_SkyPillar, MSGBOX_DEFAULT
	releaseall
	end

AzureFlute_EventScript_StairOpen:
	msgbox AzureFlute_Text_StairOpen, MSGBOX_DEFAULT
	releaseall
	end

AzureFlute_EventScript_AfterArceus:
	msgbox AzureFlute_Text_AfterArceus, MSGBOX_DEFAULT
	releaseall
	end

AzureFlute_EventScript_Flash:
	fadescreenspeed FADE_TO_WHITE, 0
	fadescreenspeed FADE_FROM_WHITE, 2
	fadescreenspeed FADE_TO_WHITE, 0
	fadescreenspeed FADE_FROM_WHITE, 2
	return

@ ---------------------------------------------------------------- Spacetime Cave: Arceus spreekt (na Spear Pillar)
@ Haak in SpacetimeCave_OnTransition / _OnFrame (spacetime_cave.py): VAR_TEMP_3 = 1 -> scene.
Spacetime_EventScript_ArmArceus::
	goto_if_unset FLAG_SPACETIME_CORONET_DONE, Common_EventScript_NopReturn
	goto_if_set FLAG_ARCEUS_MET, Common_EventScript_NopReturn
	setvar VAR_TEMP_3, 1
	return

Spacetime_EventScript_ArceusScene::
	lockall
	setvar VAR_TEMP_3, 0
	delay 30
	call AzureFlute_EventScript_Flash
	playmoncry SPECIES_ARCEUS, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox Spacetime_Text_ArceusVoice1, MSGBOX_DEFAULT
	call AzureFlute_EventScript_Flash
	msgbox Spacetime_Text_ArceusVoice2, MSGBOX_DEFAULT
	giveitem ITEM_AZURE_FLUTE
	setflag FLAG_ARCEUS_MET
	msgbox Spacetime_Text_ArceusVoice3, MSGBOX_DEFAULT
	releaseall
	end

@ ---------------------------------------------------------------- Sky Pillar: de trap van licht
@ Haak in SkyPillar_Top_OnTransition / _OnFrame: VAR_TEMP_4 = 1 -> scene bij de eerste keer na de fluit.
SkyPillar_Top_EventScript_ArmHallOfOrigin::
	goto_if_unset FLAG_ARCEUS_SKY_PILLAR, Common_EventScript_NopReturn
	goto_if_set FLAG_HALL_OF_ORIGIN_OPEN, Common_EventScript_NopReturn
	setvar VAR_TEMP_4, 1
	return

SkyPillar_Top_EventScript_HallOfOriginScene::
	lockall
	setvar VAR_TEMP_4, 0
	delay 20
	msgbox SkyPillar_Top_Text_ArceusCalls, MSGBOX_DEFAULT
	closemessage
	call AzureFlute_EventScript_Flash
	playmoncry SPECIES_ARCEUS, CRY_MODE_ENCOUNTER
	waitmoncry
	setflag FLAG_HALL_OF_ORIGIN_OPEN
	msgbox SkyPillar_Top_Text_StairDescends, MSGBOX_DEFAULT
	closemessage
	playse SE_M_TELEPORT
	fadescreen FADE_TO_WHITE
	setdynamicwarp MAP_SKY_PILLAR_TOP, 1
	warpsilent MAP_HALL_OF_ORIGIN_STAIRWAY, 0
	waitstate
	releaseall
	end

SkyPillar_Top_EventScript_StairOfLight::
	goto_if_unset FLAG_HALL_OF_ORIGIN_OPEN, SkyPillar_Top_EventScript_NoStair
	lockall
	msgbox SkyPillar_Top_Text_StairOfLight, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SkyPillar_Top_EventScript_StairRelease
	closemessage
	playse SE_M_TELEPORT
	fadescreen FADE_TO_WHITE
	setdynamicwarp MAP_SKY_PILLAR_TOP, 1
	warpsilent MAP_HALL_OF_ORIGIN_STAIRWAY, 0
	waitstate
SkyPillar_Top_EventScript_StairRelease:
	releaseall
	end

SkyPillar_Top_EventScript_NoStair:
	end

"""
    texts = [
        ('AzureFlute_Text_AllDone', "The AZURE FLUTE plays a note that goes on far longer than your breath.\n\n"
                                    "ARCEUS: Every legend answers to you now. Even the ones who hate answering.\n\n"
                                    "Meet me at the top. SKY PILLAR or SPEAR PILLAR, I built both and I'm not "
                                    "precious about it. Don't bring snacks; I'll know."),
        ('AzureFlute_Text_SkyPillar', "The AZURE FLUTE hums: SKY PILLAR or SPEAR PILLAR. The top of either.\n\n"
                                      "It says it in the tone of a parent who has already said it twice."),
        ('AzureFlute_Text_StairOpen', "The AZURE FLUTE points up. Way up. Above SKY PILLAR and SPEAR PILLAR a stair "
                                      "of light is still waiting for you."),
        ('AzureFlute_Text_AfterArceus', "The AZURE FLUTE plays a little tune. Somewhere, ARCEUS hums along. "
                                        "Off-key. On purpose."),
        ('Spacetime_Text_ArceusVoice1', "A voice. Not from the cave. Not from anywhere. From the gaps between.\n\n"
                                        "???: You walked through time. You walked through space. Both of them "
                                        "complained about you to me.\n\nI am ARCEUS. I'm the one they complain to."),
        ('Spacetime_Text_ArceusVoice2', "ARCEUS: The legends of every world are scattered, sulking in caves and "
                                        "volcanoes and very specific islands.\n\nGather them. All of them. Take this, "
                                        "so you don't get lost. I've seen your sense of direction."),
        ('Spacetime_Text_ArceusVoice3', "ARCEUS: Play it, and it will tell you who is still missing. It does not do "
                                        "requests.\n\nWhen it falls silent, find me. I'll be the one at the top."),
        ('SkyPillar_Top_Text_ArceusCalls', "The AZURE FLUTE starts playing on its own, from inside your bag.\n\n"
                                           "ARCEUS: Up here. No, further. Further. There."),
        ('SkyPillar_Top_Text_StairDescends', "A stair of light unfolds out of the sky and stops right in front of "
                                             "your feet.\n\nIt doesn't have a railing. Of course it doesn't."),
        ('SkyPillar_Top_Text_StairOfLight', "A stair of light hangs above the old altar, humming.\n\nClimb to the "
                                            "HALL OF ORIGIN?"),
    ]
    out = code + '@ ---------------------------------------------------------------- teksten (placeholders, Jordi ' \
                 'herschrijft ze)\n' + ''.join(text_block(lbl, s) for lbl, s in texts)
    open(GLOBAL_INC, 'w').write(out.rstrip('\n') + '\n')


def patch(path_, old, new, marker):
    s = open(path_).read()
    if marker in s:
        return False
    assert old in s, (path_, old[:60])
    s = s.replace(old, new, 1)
    open(path_, 'w').write(s)
    return True


def hub_hook():
    """Arceus-scene in de Spacetime Cave: in de gegenereerde scripts.inc en in de generator (spacetime_cave.py)."""
    inc = 'data/maps/SpacetimeCave/scripts.inc'
    patch(inc, '\tcall_if_set FLAG_SPACETIME_LAKES_SCENE, SpacetimeCave_EventScript_DisarmLakes\n\tend\n',
          '\tcall_if_set FLAG_SPACETIME_LAKES_SCENE, SpacetimeCave_EventScript_DisarmLakes\n'
          '\tcall Spacetime_EventScript_ArmArceus\n\tend\n', 'Spacetime_EventScript_ArmArceus')
    patch(inc, '\tmap_script_2 VAR_TEMP_1, 1, SpacetimeCave_EventScript_FirstVisit\n\t.2byte 0\n',
          '\tmap_script_2 VAR_TEMP_1, 1, SpacetimeCave_EventScript_FirstVisit\n'
          '\tmap_script_2 VAR_TEMP_3, 1, Spacetime_EventScript_ArceusScene\n\t.2byte 0\n',
          'Spacetime_EventScript_ArceusScene')
    py = os.path.join(HERE, 'spacetime_cave.py')
    patch(py, "'\\tcall_if_set FLAG_SPACETIME_LAKES_SCENE, SpacetimeCave_EventScript_DisarmLakes\\n\\tend\\n\\n'",
          "'\\tcall_if_set FLAG_SPACETIME_LAKES_SCENE, SpacetimeCave_EventScript_DisarmLakes\\n'\n"
          "          '\\tcall Spacetime_EventScript_ArmArceus\\n\\tend\\n\\n'  # Arceus (hall_of_origin.py)",
          'Spacetime_EventScript_ArmArceus')
    patch(py, "'SpacetimeCave_OnFrame:\\n\\tmap_script_2 VAR_TEMP_1, 1, SpacetimeCave_EventScript_FirstVisit\\n"
              "\\t.2byte 0\\n\\n'",
          "'SpacetimeCave_OnFrame:\\n\\tmap_script_2 VAR_TEMP_1, 1, SpacetimeCave_EventScript_FirstVisit\\n'\n"
          "          '\\tmap_script_2 VAR_TEMP_3, 1, Spacetime_EventScript_ArceusScene\\n\\t.2byte 0\\n\\n'",
          'Spacetime_EventScript_ArceusScene')
    s = open(inc).read()
    assert 'VAR_TEMP_3' not in s.replace('VAR_TEMP_3, 1, Spacetime_EventScript_ArceusScene', ''), 'VAR_TEMP_3 al in gebruik'


def sky_pillar_hook():
    inc = 'data/maps/SkyPillar_Top/scripts.inc'
    s = open(inc).read()
    assert 'VAR_TEMP_4' not in s.replace('VAR_TEMP_4, 1, SkyPillar_Top_EventScript_HallOfOriginScene', '')
    patch(inc, '\tmap_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, SkyPillar_Top_OnWarp\n',
          '\tmap_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, SkyPillar_Top_OnWarp\n'
          '\tmap_script MAP_SCRIPT_ON_FRAME_TABLE, SkyPillar_Top_OnFrame\n', 'SkyPillar_Top_OnFrame')
    patch(inc, '\tcall SkyPillar_Top_EventScript_TryShowShinyRayquaza\n\tend\n',
          '\tcall SkyPillar_Top_EventScript_TryShowShinyRayquaza\n'
          '\tcall SkyPillar_Top_EventScript_ArmHallOfOrigin @ Project Grounded: Arceus (data/scripts/azure_flute.inc)\n'
          '\tend\n\n'
          'SkyPillar_Top_OnFrame:\n'
          '\tmap_script_2 VAR_TEMP_4, 1, SkyPillar_Top_EventScript_HallOfOriginScene\n'
          '\t.2byte 0\n', 'SkyPillar_Top_EventScript_ArmHallOfOrigin')
    p = 'data/maps/SkyPillar_Top/map.json'
    d = json.load(open(p))
    changed = False
    if not any(w['dest_map'] == 'MAP_HALL_OF_ORIGIN_STAIRWAY' for w in d['warp_events']):
        d['warp_events'].append(bd.warp(SKY_TOP_LANDING[0], SKY_TOP_LANDING[1], CONST[ST], 0, elev=3))
        changed = True
    assert d['warp_events'][1]['dest_map'] == 'MAP_HALL_OF_ORIGIN_STAIRWAY'
    if not any(b.get('script') == 'SkyPillar_Top_EventScript_StairOfLight' for b in d['bg_events']):
        d['bg_events'].append(bd.sign(SKY_TOP_STAIR[0], SKY_TOP_STAIR[1], 'SkyPillar_Top_EventScript_StairOfLight',
                                      'BG_EVENT_PLAYER_FACING_NORTH'))
        changed = True
    if changed:
        open(p, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')


# ====================================================================== controles
FACE = co.FACE


def checks():
    for name in ORDER:
        g = MAPS[name]
        d = json.load(open('data/maps/%s/map.json' % name))
        objs = [o for o in d['object_events'] if 'SPECIES(' not in o['graphics_id']]
        start = (d['warp_events'][0]['x'], d['warp_events'][0]['y'])
        solid = {(o['x'], o['y']) for o in d['object_events']} - {start}
        r_all = mf.reachable(g, start, solid)
        for o in d['object_events']:
            p = (o['x'], o['y'])
            assert not g[p[1]][p[0]] & 0xC00, (name, 'object op een muur', o['script'], p)
            assert mf.next_to(r_all, *p), (name, 'object onbereikbaar', o['script'], p)
            if o['trainer_type'] == 'TRAINER_TYPE_NORMAL':
                dx, dy = FACE[o['movement_type'].split('_')[-1]]
                for k in range(1, int(o['trainer_sight_or_berry_tree_id']) + 1):
                    assert (o['x'] + dx * k, o['y'] + dy * k) in r_all, (name, 'zichtlijn', o['script'], k)
        for w in d['warp_events']:
            assert (w['x'], w['y']) in r_all or (w['x'], w['y']) == start, (name, 'warp onbereikbaar', w)
        for b in d['bg_events']:
            p = (b['x'], b['y'])
            assert p in r_all if b['type'] == 'hidden_item' else mf.next_to(r_all, *p), (name, 'bg onbereikbaar', p)
        print('%-24s bereikbaar: %d tegels' % (name, len(r_all)))
    # Sky Pillar: landing en trap van licht
    import struct
    lj = json.load(open('data/layouts/layouts.json'))['layouts']
    for lid in ('LAYOUT_SKY_PILLAR_TOP', 'LAYOUT_SKY_PILLAR_TOP_CLEAN'):
        L = [x for x in lj if x.get('id') == lid][0]
        raw = open(L['blockdata_filepath'], 'rb').read()
        W = L['width']
        v = lambda x, y: struct.unpack_from('<H', raw, 2 * (y * W + x))[0]  # noqa: E731
        for (x, y) in (SKY_TOP_LANDING, (SKY_TOP_STAIR[0], SKY_TOP_STAIR[1] + 1)):
            assert not v(x, y) & 0xC00, ('Sky Pillar-tegel geblokkeerd', lid, (x, y))


def render(name, out):
    H = len(MAPS[name])
    subprocess.run([sys.executable, os.path.join(HERE, 'render_map.py'), name, out, '0', str(H)], check=True,
                   capture_output=True)
    from PIL import Image
    im = Image.open(out).convert('RGB')
    W = len(MAPS[name][0])
    im.crop((0, 0, W * 16, H * 16)).save(out)


def main():
    flags()
    ni = new_items()
    build_maps(ni)
    mapsecs()
    events()
    trainers()
    battle_setup()
    global_scripts()
    hub_hook()
    sky_pillar_hook()
    checks()
    if len(sys.argv) > 1:
        for name in ORDER:
            render(name, os.path.join(sys.argv[1], name + '.png'))


if __name__ == '__main__':
    main()
