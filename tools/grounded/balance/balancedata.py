"""Gedeelde data voor de balansanalyse van de hoofdgame (Hoenn).

- Fase (stage) = aantal badges dat je nodig hebt om ergens te komen (0..7), 8 = Victory Road/E4,
  9 = post-game. Grove indeling volgens de Emerald-route; zie STAGE_OF_MAP en de HM-regels.
- Beschikbaarheid per soort: wilde encounters (+ hengel/Surf/Rock Smash/Dive-poorten), cadeaus
  en statics (hand-lijst), en evoluties volgens de evolutielevels van dít project.
- Gymteams uit src/data/trainers.party.
"""
import functools, json, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'spire'))
import spiredata  # noqa: E402

ROOT = spiredata.ROOT

# Level van de speler per fase = level van de ace van de volgende gymleider (de gymgidsen noemen dat).
LEVEL_AT_STAGE = [17, 21, 30, 43, 44, 51, 62, 71, 77, 90]  # gym-ace − 2 (levelcurve 12 okt; was 16..70 van vóór de herijking)
STAGE_NAMES = ['Roxanne', 'Brawly', 'Wattson', 'Flannery', 'Norman', 'Winona', 'Tate & Liza', 'Wallace',
               'E4 + Champion', 'post-game']

# Minimale fase per methode (Emerald: Old Rod in Dewford, Rock Smash = Dynamo Badge, Good Rod Route 118,
# Surf = Balance Badge, Dive na Tate & Liza, Super Rod Mossdeep, Waterfall = Rain Badge).
METHOD_STAGE = {'land_mons': 0, 'old_rod': 1, 'good_rod': 3, 'rock_smash_mons': 3, 'water_mons': 5, 'super_rod': 7}

STAGE_OF_MAP = {
    0: ['ROUTE101', 'ROUTE102', 'ROUTE103', 'ROUTE104', 'PETALBURG_WOODS', 'ROUTE116', 'RUSTURF_TUNNEL',
        'ROUTE102_MINI_FOREST', 'PETALBURG_CITY'],
    1: ['GRANITE_CAVE_1F', 'GRANITE_CAVE_B1F', 'GRANITE_CAVE_B2F', 'GRANITE_CAVE_STEVENS_ROOM', 'ROUTE115',
        'DEWFORD_TOWN', 'ROUTE106', 'ROUTE107', 'ROUTE108', 'ROUTE109', 'SLATEPORT_CITY'],
    2: ['ROUTE110', 'ROUTE117', 'ROUTE118'],
    3: ['ROUTE111', 'ROUTE112', 'ROUTE113', 'ROUTE114', 'FIERY_PATH', 'METEOR_FALLS_1F_1R', 'JAGGED_PASS',
        'METEOR_FALLS_CRATER_ROOM'],
    4: ['MIRAGE_TOWER_1F', 'MIRAGE_TOWER_2F', 'MIRAGE_TOWER_3F', 'MIRAGE_TOWER_4F'],
    5: ['ROUTE119', 'ROUTE105', 'NEW_MAUVILLE_ENTRANCE', 'NEW_MAUVILLE_INSIDE', 'ABANDONED_SHIP_ROOMS_B1F',
        'ABANDONED_SHIP_HIDDEN_FLOOR_CORRIDORS', 'METEOR_FALLS_1F_2R', 'COLDSTEP_CAVE_ENTRANCE',
        'COLDSTEP_CAVE_ICE_ROOM_1', 'COLDSTEP_CAVE_ICE_ROOM_2', 'ROUTE135', 'ROUTE136', 'ASHFROST_TOWN',
        'ROUTE120', 'ROUTE121', 'ROUTE122', 'ROUTE123', 'LILYCOVE_CITY', 'MT_PYRE_1F', 'MT_PYRE_2F',
        'MT_PYRE_3F', 'MT_PYRE_4F', 'MT_PYRE_5F', 'MT_PYRE_6F', 'MT_PYRE_EXTERIOR', 'MT_PYRE_SUMMIT',
        'SAFARI_ZONE_SOUTH', 'SAFARI_ZONE_SOUTHWEST', 'SAFARI_ZONE_NORTH', 'SAFARI_ZONE_NORTHWEST',
        'MAUVILLE_CITY', 'PETALBURG_CITY_WATER'],
    6: ['ROUTE124', 'ROUTE125', 'ROUTE126', 'MOSSDEEP_CITY', 'SHOAL_CAVE_LOW_TIDE_STAIRS_ROOM',
        'SHOAL_CAVE_LOW_TIDE_LOWER_ROOM', 'SHOAL_CAVE_LOW_TIDE_INNER_ROOM', 'SHOAL_CAVE_LOW_TIDE_ENTRANCE_ROOM',
        'SHOAL_CAVE_LOW_TIDE_ICE_ROOM', 'MAGMA_HIDEOUT_1F', 'MAGMA_HIDEOUT_2F_1R', 'MAGMA_HIDEOUT_2F_2R',
        'MAGMA_HIDEOUT_3F_1R', 'MAGMA_HIDEOUT_3F_2R', 'MAGMA_HIDEOUT_4F', 'MAGMA_HIDEOUT_3F_3R',
        'MAGMA_HIDEOUT_2F_3R'],
    7: ['UNDERWATER_ROUTE124', 'UNDERWATER_ROUTE126', 'ROUTE127', 'ROUTE128', 'ROUTE129', 'ROUTE130', 'ROUTE131',
        'ROUTE132', 'ROUTE133', 'ROUTE134', 'SEAFLOOR_CAVERN_ENTRANCE', 'SEAFLOOR_CAVERN_ROOM1',
        'SEAFLOOR_CAVERN_ROOM2', 'SEAFLOOR_CAVERN_ROOM3', 'SEAFLOOR_CAVERN_ROOM4', 'SEAFLOOR_CAVERN_ROOM5',
        'SEAFLOOR_CAVERN_ROOM6', 'SEAFLOOR_CAVERN_ROOM7', 'SEAFLOOR_CAVERN_ROOM8', 'CAVE_OF_ORIGIN_ENTRANCE',
        'CAVE_OF_ORIGIN_1F', 'SOOTOPOLIS_CITY', 'PACIFIDLOG_TOWN', 'SKY_PILLAR_1F', 'SKY_PILLAR_3F',
        'SKY_PILLAR_5F'],
    8: ['VICTORY_ROAD_1F', 'VICTORY_ROAD_B1F', 'VICTORY_ROAD_B2F', 'EVER_GRANDE_CITY', 'METEOR_FALLS_B1F_1R',
        'METEOR_FALLS_B1F_2R'],
    9: ['SAFARI_ZONE_SOUTHEAST', 'SAFARI_ZONE_NORTHEAST', 'DESERT_UNDERPASS', 'ARTISAN_CAVE_B1F',
        'ARTISAN_CAVE_1F', 'ALTERING_CAVE', 'METEOR_FALLS_STEVENS_CAVE', 'CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP1',
        'CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP2', 'CAVE_OF_ORIGIN_UNUSED_RUBY_SAPPHIRE_MAP3'],
}
MAP_STAGE = {m: s for s, ms in STAGE_OF_MAP.items() for m in ms}
# Land-encounters waar het gras alleen met Surf bereikbaar is (gecontroleerd met reach.py):
# Route 115 (alle 20 grastiles achter water) en Route 118 (gras alleen oostelijk van de rivier).
# Route 111 deelt één tabel voor woestijn en gras; het gras in het noorden is al in fase 3 bereikbaar.
LAND_STAGE = {'ROUTE115': 5, 'ROUTE118': 5}

# Cadeaus en statics (bron: givemon/setwildbattle in data/maps). (soort, level, fase, bron)
GIFTS = [
    ('TREECKO', 5, 0, 'starter'), ('TORCHIC', 5, 0, 'starter'), ('MUDKIP', 5, 0, 'starter'),
    ('ZIGZAGOON_GALAR', 5, 0, 'cadeau Littleroot'), ('RELLOR', 7, 0, 'cadeau Route 102'),
    ('SILICOBRA', 10, 1, 'cadeau Slateport (keuze)'), ('CRAMORANT', 10, 1, 'cadeau Slateport (keuze)'),
    ('BULBASAUR', 15, 1, 'Oak, Slateport (keuze)'), ('CHARMANDER', 15, 1, 'Oak, Slateport (keuze)'),
    ('SQUIRTLE', 15, 1, 'Oak, Slateport (keuze)'),
    ('GRIMER_HOENN', 22, 3, 'Birch, Verdanturf'),
    ('BAGON', 20, 3, 'static kraterkamer (25%, willekeurig)'), ('DEINO', 20, 3, 'static kraterkamer'),
    ('LAPRAS', 22, 3, 'static kraterkamer'), ('MIENFOO', 20, 3, 'static kraterkamer'),
    ('MINIOR_METEOR', 20, 3, 'static kraterkamer'), ('CARBINK', 20, 3, 'static kraterkamer'),
    ('LILEEP', 20, 4, 'fossiel'), ('ANORITH', 20, 4, 'fossiel'),
    ('CASTFORM_NORMAL', 25, 5, 'Weather Institute'), ('KECLEON', 30, 5, 'static Route 120'),
    ('SPIRITOMB', 45, 5, 'static Abandoned Ship'), ('ROTOM', 28, 5, 'static Mauville-kelder'),
    ('VOLTORB', 25, 5, 'static New Mauville'), ('ELECTRODE', 30, 5, 'static New Mauville'),
    ('LAPRAS', 36, 5, 'static Route 135'), ('BERGMITE', 33, 5, 'static Route 135'), ('EISCUE', 33, 5, 'static Route 135'),
    ('BELDUM', 5, 9, 'Steven (post-game)'),
    ('CYNDAQUIL', 5, 9, 'Johto-starter (post-game)'), ('TOTODILE', 5, 9, 'Johto-starter (post-game)'),
    ('CHIKORITA', 5, 9, 'Johto-starter (post-game)'),
]

# Evolutie-items: fase waarin je het item kunt hebben.
ITEM_STAGE = {'ITEM_MOON_STONE': 2,  # Capt. Stern, Slateport (was Petalburg Woods) 'ITEM_FIRE_STONE': 3, 'ITEM_THUNDER_STONE': 5, 'ITEM_WATER_STONE': 5,
              'ITEM_LEAF_STONE': 5, 'ITEM_ICE_STONE': 5, 'ITEM_SHINY_STONE': 5, 'ITEM_DUSK_STONE': 5,
              'ITEM_DAWN_STONE': 5, 'ITEM_SUN_STONE': 6}


def stage_for_level(lv):
    for s, L in enumerate(LEVEL_AT_STAGE):
        if L >= lv:
            return s
    return 9


def load_encounters():
    d = json.load(open(os.path.join(ROOT, 'src/data/wild_encounters.json'), encoding='utf-8'))
    grp = d['wild_encounter_groups'][0]
    fish_groups = grp['fields'][3]['groups']
    out = []   # (species, stage, minlv, maxlv, map, method, rate%)
    for enc in grp['encounters']:
        m = (enc.get('map') or '').replace('MAP_', '')
        if m not in MAP_STAGE:
            continue
        mstage = MAP_STAGE[m]
        for field in grp['fields']:
            t = field['type']
            if t not in enc:
                continue
            mons = enc[t]['mons']
            rates = field['encounter_rates']
            if t == 'fishing_mons':
                for rod, idxs in fish_groups.items():
                    tot = sum(rates[i] for i in idxs)
                    for i in idxs:
                        if i < len(mons):
                            mo = mons[i]
                            out.append((mo['species'].replace('SPECIES_', ''), max(mstage, METHOD_STAGE[rod]),
                                        mo['min_level'], mo.get('max_level', mo['min_level']), m, rod,
                                        round(100 * rates[i] / tot)))
            else:
                st = max(mstage, METHOD_STAGE[t], LAND_STAGE.get(m, 0) if t == 'land_mons' else 0)
                for i, mo in enumerate(mons):
                    out.append((mo['species'].replace('SPECIES_', ''), st,
                                mo['min_level'], mo.get('max_level', mo['min_level']), m, t.replace('_mons', ''),
                                rates[i] if i < len(rates) else 0))
    return out


def availability(species):
    """{soort: dict(stage, level, src)}: vroegste fase en het level waarop je hem dan hebt."""
    best = {}

    def offer(sp, stage, lv, src):
        if sp not in species:
            return
        cur = best.get(sp)
        if cur is None or (stage, -lv) < (cur['stage'], -cur['level']):
            best[sp] = dict(stage=stage, level=lv, src=src)

    for sp, st, lo, hi, m, meth, rate in load_encounters():
        offer(sp, st, hi, '%s %s %d%% lv%d-%d' % (m.title().replace('_', ' '), meth, rate, lo, hi))
    for sp, lv, st, src in GIFTS:
        offer(sp, st, lv, src)
    # evoluties doorrekenen (een paar rondes, ketens zijn kort)
    for _ in range(4):
        for sp, a in list(best.items()):
            for e in species[sp]['evos']:
                t = e['target']
                if e['method'] in ('LEVEL', 'LEVEL_MALE', 'LEVEL_FEMALE', 'LEVEL_DAY', 'LEVEL_NIGHT',
                                   'LEVEL_ATK_GT_DEF', 'LEVEL_ATK_LT_DEF', 'LEVEL_ATK_EQ_DEF', 'LEVEL_SILCOON',
                                   'LEVEL_CASCOON', 'LEVEL_NINJASK', 'LEVEL_SHEDINJA', 'LEVEL_RANDOM'):
                    try:
                        L = int(e['param'])
                    except ValueError:
                        continue
                    lv = max(L, a['level'])
                    offer(t, max(a['stage'], stage_for_level(L)), lv, 'evo van %s (lv %d)' % (sp, L))
                elif e['method'] == 'ITEM':
                    st = max(a['stage'], ITEM_STAGE.get(e['param'], 6))
                    offer(t, st, max(a['level'], LEVEL_AT_STAGE[st] - 6 if st < 9 else a['level']),
                          'evo van %s (%s)' % (sp, e['param'].replace('ITEM_', '').title()))
                elif e['method'] in ('FRIENDSHIP', 'FRIENDSHIP_DAY', 'FRIENDSHIP_NIGHT'):
                    offer(t, a['stage'] + 1, a['level'] + 6, 'evo van %s (vriendschap)' % sp)
                elif e['method'] == 'SPLIT_FROM_EVO':
                    offer(t, max(a['stage'], stage_for_level(20)), max(a['level'], 20), 'evo van %s (lege huls)' % sp)
                elif e['method'] == 'TRADE':
                    continue
                else:
                    if e['method'].startswith('LEVEL') or e['method'] in ('MOVE', 'MOVE_TYPE', 'MAPSEC', 'SPECIFIC_MAP'):
                        offer(t, a['stage'] + 1, a['level'] + 6, 'evo van %s (%s)' % (sp, e['method'].lower()))
    return best


# ---------------------------------------------------------------------------------------------
# trainers.party

@functools.lru_cache(maxsize=None)
def load_trainer(tid):
    txt = open(os.path.join(ROOT, 'src/data/trainers.party'), encoding='utf-8').read()
    m = re.search(r'^=== %s ===\n(.*?)(?=^=== )' % re.escape(tid), txt, re.S | re.M)
    if not m:
        return None
    body = m.group(1)
    head, _, rest = body.partition('\n\n')
    mons = []
    for blk in rest.strip().split('\n\n'):
        lines = [l.strip() for l in blk.strip().split('\n') if l.strip() and not l.strip().startswith('#')]
        if not lines:
            continue
        first = lines[0]
        sp, _, item = first.partition('@')
        sp = sp.strip()
        sp = re.sub(r'\s*\((M|F)\)$', '', sp)
        mon = dict(species=sp, item=item.strip(), level=50, ability='', moves=[], ivs=31)
        for l in lines[1:]:
            if l.startswith('Level:'):
                mon['level'] = int(l.split(':')[1])
            elif l.startswith('Ability:'):
                mon['ability'] = l.split(':', 1)[1].strip()
            elif l.startswith('- '):
                mon['moves'].append(l[2:].strip())
            elif l.startswith('IVs:'):
                mon['ivs'] = [int(x) for x in re.findall(r'(\d+)', l)]
        mons.append(mon)
    ai = re.search(r'^AI:\s*(.*)$', head, re.M)
    return dict(id=tid, mons=mons, ai=ai.group(1) if ai else '')


GYMS = [('TRAINER_ROXANNE_1', 0), ('TRAINER_BRAWLY_1', 1), ('TRAINER_WATTSON_1', 2), ('TRAINER_FLANNERY_1', 3),
        ('TRAINER_NORMAN_1', 4), ('TRAINER_WINONA_1', 5), ('TRAINER_TATE_AND_LIZA_1', 6), ('TRAINER_WALLACE_1', 7),
        ('TRAINER_SIDNEY', 8), ('TRAINER_PHOEBE', 8), ('TRAINER_GLACIA', 8), ('TRAINER_DRAKE', 8),
        ('TRAINER_STEVEN', 8)]


# Fase waarin een TM te krijgen is (vindplaatsen uit data/maps; gymbeloningen tellen pas ná die gym).
TM_STAGE = {
    'BULLET_SEED': 0, 'STEALTH_ROCK': 1, 'FOCUS_PUNCH': 1, 'SLUDGE_BOMB': 1, 'FLASH_CANNON': 1,
    'HIDDEN_POWER': 1, 'SECRET_POWER': 1, 'NASTY_PLOT': 1, 'TRICK_ROOM': 1, 'DRAIN_PUNCH': 2,
    'THUNDERBOLT': 2, 'FLAMETHROWER': 2, 'ICE_BEAM': 2, 'PSYCHIC': 2, 'DOUBLE_TEAM': 2, 'ATTRACT': 2,
    'MACHINE_LEARNING': 3, 'TOXIC': 3, 'IRON_HEAD': 3, 'STORED_POWER': 3, 'DIG': 3, 'RETURN': 3,
    'OVERHEAT': 4, 'SANDSTORM': 4, 'FACADE': 5, 'VOLT_SWITCH': 5, 'POLLEN_HAZE': 5, 'SCALD': 5,
    'CALM_MIND': 5, 'GIGA_DRAIN': 5, 'SHADOW_SIPHON': 5, 'SHADOW_BALL': 5, 'DARK_PULSE': 5, 'SOLAR_BEAM': 5,
    'RAIN_DANCE': 5, 'SUNNY_DAY': 5, 'LAGER_LAGOON': 5, 'REST': 5, 'BLIZZARD': 5, 'FIRE_BLAST': 5,
    'HYPER_BEAM': 5, 'LIGHT_SCREEN': 5, 'PROTECT': 5, 'REFLECT': 5, 'THUNDER': 5, 'U_TURN': 5,
    'BRAVE_BIRD': 6, 'SELTZER_SURGE': 6, 'ACID_RAIN': 6, 'HAIL': 6, 'LASER_BEAM': 7, 'EARTHQUAKE': 7,
    'DAZZLING_GLEAM': 7, 'BRICK_BREAK': 7, 'VINTAGE_SPILL': 8, 'DRAGON_CLAW': 8, 'TAUNT': 9, 'PLAY_ROUGH': 9,
    # HM's: badge + HM in de tas
    'CUT': 1, 'FLASH': 1, 'ROCK_SMASH': 3, 'STRENGTH': 4, 'SURF': 5, 'FLY': 6, 'DIVE': 7, 'WATERFALL': 8,
}
