"""The Spire: elk startteam tegen elke elite en baas (Jordi, 5 okt: 'een 0% winkans mag in geen enkele run ontstaan').

Waar encounters.py met een gemiddeld team rekent (geen types, geen abilities), speelt dit script echte gevechten na:
twee rentals uit de draft (src/data/spire_pool.h, met hun startmoves en de vorm van die act) tegen de echte
ontmoeting (encounters.py: soorten, moves, patronen, abilities, items, totem-boosts, HP-vermenigvuldigers na de
kalibratie). Schadeformule Gen 5+ met types, STAB, crits, rolls, spread, stat-stages, weer, schermen; de abilities
en moves die in de ontmoetingen voorkomen zijn uitgewerkt (Water Bubble, Schooling, Levitate, Sturdy, Mirror Coat,
Wide Guard, Soak, Rage, Echoed Voice, ...). Openingsbescherming en DEFEND zoals in src/spire.c.

De speler is een bot die de intenties leest (zoals een mens): hij verdedigt als een intentie een Pokémon zou
uitschakelen en het blok dat voorkomt, slaat niet in een Protect/Wide Guard/Mirror Coat/Counter, en richt zich op
de gevaarlijkste vijand die het snelst valt. Moves: de startkit + per type van de Pokémon één beloningsmove
(STAB, kracht per act, zie REWARD) - geen dekking, geen relics, geen upgrades: dus een pessimistische speler.

Controle (Jordi): voor elke elite en baas moet de slechtste startcombinatie een winkans van minstens MIN_WIN halen.
Gebruik:
    python3 matchups.py                 # alle elites en bazen (kalibratie uit spire_calib.json)
    python3 matchups.py --only Wishiwashi --pair BELDUM ZORUA -n 400
    python3 matchups.py --quick --only Nexus       # een derde van de rentals
    python3 matchups.py --hits                     # klappen boven 45% van een volle Pokémon
    python3 -c "import matchups as M; M.trace('Totem Wishiwashi', ('BELDUM', 'ZORUA'))"
encounters.py kalibreert hiermee de HP-factoren (spire_calib.json), schrijft het rapport en faalt als de controle faalt.
"""
import argparse, math, os, random, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import encounters as E  # noqa: E402
import spiredata  # noqa: E402

ROOT = E.ROOT
SPECIES, MOVES = E.SPECIES, E.MOVES
CHART = spiredata.load_typechart()

LEVEL = 100
HP_PLAYER = 4.0
DEFEND_BIAS = 1.6        # bot: verdedigen alleen als het blok duidelijk meer oplevert dan aanvallen
MIN_WIN = 0.10          # slechtste gedrafte startcombinatie per elite/baas (Jordi: nooit 0%; taak: 10-20%)
SECTION = '### Slechtste startcombinatie per elite en baas (matchups.py)'


def _read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return f.read()


def c_define(name, default=None):
    m = re.search(r'#define\s+%s\s+(\d+)' % name, _read('include/spire.h'))
    return int(m.group(1)) if m else default


OPENING_TURNS = c_define('SPIRE_OPENING_TURNS')
OPENING_CAP = c_define('SPIRE_OPENING_CAP') / 100
HIT_CAP = c_define('SPIRE_HIT_CAP', 100) / 100      # één klap van een vijand: hooguit dit deel van de max HP
BLOCK_PCT = c_define('SPIRE_BLOCK_PERCENT') / 100
BLOCK_SPLIT = c_define('SPIRE_BLOCK_SPLIT') / 100
ACT_BLOCK = {1: 1.0, 2: 1.25, 3: 1.5}

# Wat een speler bij die kamer ongeveer heeft (Slay: de deck groeit per gevecht). Beloningskaarten: 60/30/10%
# common/uncommon/rare, commons tot ±75 kracht, uncommons 80-95, rares 100+; ±1 kaart per gevecht, upgrades op
# rustplekken (±2 per act, +30%), ±3 relics per act (+10-35% schade, zie relics.py).
# REWARD: kracht van de STAB-beloningsmoves (één per type van de Pokémon); None = alleen de startkit (eerste verdiepingen).
# COVERAGE: dekkingsmove (kaart 3 is vrij van type), REWARD min dit getal. Bij een baas kiest de speler hem tegen
#   deze baas (die staat vanaf het begin op de kaart); bij een elite is hij minder gericht (-20); gewone gevechten geen.
# PROGRESS: upgrades (Porygon2, +30% op een move) en de gewone schade-relics (Muscle Band, ...), als schadefactor;
#   bewust laag (de bot neemt geen boss-relics, vasthouditems of statusmoves).
# ARRIVE: HP bij aankomst (runsim.py: ±90% bij de baas; elites kies je als je gezond bent).
REWARD = {(1, 'weak'): None, (1, 'normal'): 65, (1, 'elite'): 70, (1, 'boss'): 80,
          (2, 'weak'): 80, (2, 'normal'): 85, (2, 'elite'): 85, (2, 'boss'): 90,
          (3, 'weak'): 90, (3, 'normal'): 95, (3, 'elite'): 95, (3, 'boss'): 100}
COVERAGE = {'elite': 20, 'boss': 10}
PROGRESS = {(1, 'weak'): 1.0, (1, 'normal'): 1.0, (1, 'elite'): 1.05, (1, 'boss'): 1.15,
            (2, 'weak'): 1.2, (2, 'normal'): 1.2, (2, 'elite'): 1.25, (2, 'boss'): 1.3,
            (3, 'weak'): 1.35, (3, 'normal'): 1.35, (3, 'elite'): 1.4, (3, 'boss'): 1.45}
ARRIVE = {'weak': 0.9, 'normal': 0.85, 'elite': 0.85, 'boss': 0.9}


# ---------------------------------------------------------------------------------------------
# rentals uit de echte header

def load_rentals():
    txt = _read('src/data/spire_pool.h')
    body = txt.split('sSpireRentals[] =')[1].split('};')[0]
    rentals = []
    for sp, tier, mv in re.findall(r'\{SPECIES_(\w+), (\d), \{([^}]*)\}\}', body):
        moves = [m.replace('MOVE_', '') for m in re.findall(r'MOVE_\w+', mv) if m != 'MOVE_NONE']
        rentals.append(dict(s=sp, tier=int(tier), m=moves))
    evo = {}
    for sp, ts in re.findall(r'\{SPECIES_(\w+), \{([^}]*)\}\}', txt.split('sSpireEvolutions[] =')[1].split('};')[0]):
        evo[sp] = [t.replace('SPECIES_', '') for t in re.findall(r'SPECIES_\w+', ts) if t != 'SPECIES_NONE']
    return rentals, evo


def form_in_act(species, act, evo):
    """Vorm in deze act: na elke baas één evolutie; bij een vertakking de sterkste (de speler kiest)."""
    s = species
    for _ in range(act - 1):
        ts = evo.get(s)
        if not ts:
            break
        s = max(ts, key=lambda t: sum(SPECIES[t][k] for k in ('hp', 'atk', 'def', 'spa', 'spd', 'spe')) if t in SPECIES else 0)
    return s


# ---------------------------------------------------------------------------------------------
# Pokémon in het gevecht

def stat(base, hp=False, iv=31, ev=84):
    x = (2 * base + iv + ev // 4) * LEVEL // 100
    return x + LEVEL + 10 if hp else x + 5


STAGE = {k: 0 for k in ('atk', 'def', 'spa', 'spd', 'spe', 'acc', 'eva')}


class Mon:
    def __init__(self, species, moves, side, hp_mult, iv, ev, ability=None, item=None, boosts=None, pattern=None,
                 gimmick=None, name=None):
        self.side, self.species = side, species
        self.name = name or species
        self.base = SPECIES[species]
        self.types = list(self.base['types'])
        self.iv, self.ev = iv, ev
        self.hp_mult = hp_mult
        self.maxhp = int(stat(self.base['hp'], True, iv, ev) * hp_mult)
        self.hp = self.maxhp
        self.set_stats(species)
        self.ability = ability or (self.base['abilities'][0] if self.base['abilities'] else 'NONE')
        self.item = item
        self.moves = [m for m in moves if m in MOVES]
        self.pattern = pattern or []
        self.pstep = 0
        self.stages = dict(STAGE)
        for k, v in (boosts or {}).items():
            self.stages[k] = v
        self.status, self.sleep, self.tox = '', 0, 0
        if gimmick == 'SLEEP3':
            self.status, self.sleep = 'slp', 3
        self.confused = 0
        self.sub = 0
        self.recharge = False
        self.charging = None
        self.seeded = False
        self.trapped = 0
        self.ring = False
        self.rage = False
        self.echo = 0
        self.charged = False
        self.focus = False
        self.yawn = 0
        self.taunt = 0
        self.flinch = False
        self.sash = (item == 'ITEM_FOCUS_SASH')
        self.berry = item in ('ITEM_SITRUS_BERRY', 'ITEM_ORAN_BERRY', 'ITEM_PETAYA_BERRY', 'ITEM_BERRY_JUICE')
        self.innards = 0

    def set_stats(self, species):
        b = SPECIES[species]
        self.atk, self.df = stat(b['atk'], False, self.iv, self.ev), stat(b['def'], False, self.iv, self.ev)
        self.spa, self.spd = stat(b['spa'], False, self.iv, self.ev), stat(b['spd'], False, self.iv, self.ev)
        self.spe = stat(b['spe'], False, self.iv, self.ev)

    @property
    def alive(self):
        return self.hp > 0


def stage_mult(s):
    return (2 + s) / 2 if s >= 0 else 2 / (2 - s)


def eff(mtype, types, defender=None):
    m = 1.0
    for t in types:
        m *= CHART.get(mtype, {}).get(t, 1.0)
    if defender is not None and defender.ability == 'DELTA_STREAM' and 'FLYING' in types and CHART[mtype].get('FLYING', 1) > 1:
        m /= 2
    return m


NO_GROUND = ('LEVITATE',)
IMMUNE = {'LEVITATE': 'GROUND', 'FLASH_FIRE': 'FIRE', 'WATER_ABSORB': 'WATER', 'STORM_DRAIN': 'WATER', 'DRY_SKIN': 'WATER',
          'VOLT_ABSORB': 'ELECTRIC', 'LIGHTNING_ROD': 'ELECTRIC', 'MOTOR_DRIVE': 'ELECTRIC', 'SAP_SIPPER': 'GRASS',
          'EARTH_EATER': 'GROUND', 'WELL_BAKED_BODY': 'FIRE'}


class Field:
    def __init__(self, start=None):
        self.weather, self.wturns = None, 0
        self.trick = 5 if start == 'TRICK_ROOM' else 0
        self.tail = {0: 0, 1: 4 if start == 'TAILWIND_OPPONENT' else 0}
        self.screens = {0: {}, 1: {}}   # side -> {'REFLECT': turns, 'LIGHT_SCREEN': turns}
        self.terrain = start if start and start.endswith('TERRAIN') else None
        self.turn = 0


def power_of(att, mv, name, target, field, foes_alive):
    p = mv['power']
    e = mv['effect']
    if name in E.MODEL_POWER:
        p = E.MODEL_POWER[name]
    if e == 'BEAT_UP':
        return 'BEAT_UP'
    if e == 'GYRO_BALL':
        p = min(150, int(25 * max(target.spe, 1) / max(att.spe, 1)) + 1)
    if e == 'ELECTRO_BALL':
        r = att.spe / max(target.spe, 1)
        p = 150 if r >= 4 else 120 if r >= 3 else 80 if r >= 2 else 60 if r >= 1 else 40
    if e in ('HEAT_CRASH', 'LOW_KICK'):
        p = 80
    if e == 'ECHOED_VOICE':
        p = min(200, 40 * (2 ** att.echo))
    if e == 'DOUBLE_POWER_ON_ARG_STATUS' and target.status:
        p *= 2
    if e == 'REVENGE':
        p = 90
    if e == 'DYNAMAX_DOUBLE_DMG':
        p = 100
    return p


def damage(att, target, name, field, rng, spread=False, crit=None, roll=None, helping=False, players=None):
    """Schade van één klap (zonder blok/openingsbescherming). rng=None: verwachte waarde (mediaan-roll, geen crit)."""
    mv = MOVES[name]
    if mv['cat'] == 'STATUS':
        return 0
    mtype = mv['type']
    if att.ability == 'NORMALIZE':
        mtype = 'NORMAL'
    ab_def = target.ability
    if IMMUNE.get(ab_def) == mtype and not att.ability == 'MOLD_BREAKER' and att.ability != 'NEUROFORCE':
        return 0
    if mtype == 'GROUND' and ('FLYING' in target.types) and name != 'THOUSAND_ARROWS':
        return 0
    te = eff(mtype, target.types, target)
    if te == 0 and att.ability == 'SCRAPPY' and mtype in ('NORMAL', 'FIGHTING'):
        te = eff(mtype, [t for t in target.types if t != 'GHOST'] or ['NORMAL'])
    if te == 0:
        return 0
    if ab_def == 'WONDER_GUARD' and te <= 1:
        return 0
    p = power_of(att, mv, name, target, field, None)
    if p == 'BEAT_UP':
        hits = [m for m in players if m.alive and not m.status] if players else [att]
        return sum(_damage_core(att, target, 5 + SPECIES[m.species]['atk'] // 10, 'DARK', 'PHYSICAL', name, field, rng, spread, crit, roll, helping, te)
                   for m in hits)
    if p <= 1:
        return 0
    if att.ability == 'TECHNICIAN' and p <= 60:
        p *= 1.5
    if att.ability == 'TOUGH_CLAWS' and mv['contact']:
        p *= 1.3
    if att.ability == 'STRONG_JAW' and name in ('BITE', 'CRUNCH', 'ICE_FANG', 'FIRE_FANG', 'THUNDER_FANG', 'POISON_FANG', 'PSYCHIC_FANGS', 'JAW_LOCK', 'HYPER_FANG'):
        p *= 1.5
    if att.ability == 'IRON_FIST' and 'PUNCH' in name:
        p *= 1.2
    if att.ability == 'SHEER_FORCE' and mv['add'] and not mv['selfEffect']:
        p *= 1.3
    if att.ability == 'WATER_BUBBLE' and mtype == 'WATER':
        p *= 2
    if att.charged and mtype == 'ELECTRIC':
        p *= 2
    hits = 1
    if mv['effect'] == 'MULTI_HIT':
        hits = 5 if att.ability == 'SKILL_LINK' else (rng.choice((2, 2, 2, 3, 3, 3, 4, 5)) if rng else 3.1)
    hits *= mv['strikes'] if mv['effect'] != 'MULTI_HIT' else 1
    one = _damage_core(att, target, p, mtype, mv['cat'], name, field, rng, spread, crit, roll, helping, te)
    if rng and hits > 1:
        return sum(_damage_core(att, target, p, mtype, mv['cat'], name, field, rng, spread, crit, None, helping, te) for _ in range(int(hits)))
    return one * hits


def _damage_core(att, target, p, mtype, cat, name, field, rng, spread, crit, roll, helping, te):
    if name == 'BODY_PRESS':
        a = att.df * stage_mult(att.stages['def'])
    elif name == 'PHOTON_GEYSER':
        a = max(att.atk * stage_mult(att.stages['atk']), att.spa * stage_mult(att.stages['spa']))
        cat = 'PHYSICAL' if att.atk * stage_mult(att.stages['atk']) > att.spa * stage_mult(att.stages['spa']) else 'SPECIAL'
    elif cat == 'PHYSICAL':
        a = att.atk * stage_mult(att.stages['atk'])
    else:
        a = att.spa * stage_mult(att.stages['spa'])
    if att.ability in ('HUGE_POWER', 'PURE_POWER') and cat == 'PHYSICAL':
        a *= 2
    if cat == 'PHYSICAL' or name == 'PSYSTRIKE':
        d = target.df * stage_mult(target.stages['def'])
    else:
        d = target.spd * stage_mult(target.stages['spd'])
    if target.item == 'ITEM_EVIOLITE':
        d *= 1.5
    if target.item == 'ITEM_ASSAULT_VEST' and cat == 'SPECIAL':
        d *= 1.5
    if crit is None:
        crit = False if rng is None else rng.random() < (0.5 if att.focus else 1 / 24)
    if crit:
        a = max(a, att.atk if cat == 'PHYSICAL' else att.spa)
        d = min(d, target.df if cat == 'PHYSICAL' else target.spd)
    base = math.floor(math.floor(math.floor(2 * LEVEL / 5 + 2) * p * a / max(d, 1)) / 50) + 2
    m = 1.0
    if spread:
        m *= 0.75
    w = field.weather
    if w == 'RAIN' and mtype == 'WATER' or w == 'SUN' and mtype == 'FIRE':
        m *= 1.5
    if w == 'RAIN' and mtype == 'FIRE' or w == 'SUN' and mtype == 'WATER':
        m *= 0.5
    if crit:
        m *= 1.5
    m *= (roll if roll is not None else (rng.randint(85, 100) / 100 if rng else 0.925))
    if mtype in att.types:
        m *= 2.0 if att.ability == 'ADAPTABILITY' else 1.5
    m *= te
    if att.status == 'brn' and cat == 'PHYSICAL' and att.ability != 'GUTS':
        m *= 0.5
    scr = field.screens[target.side]
    if not crit and ((cat == 'PHYSICAL' and scr.get('REFLECT')) or (cat == 'SPECIAL' and scr.get('LIGHT_SCREEN'))):
        m *= 2732 / 4096
    ab = target.ability
    if ab == 'WATER_BUBBLE' and mtype == 'FIRE' or ab in ('THICK_FAT',) and mtype in ('FIRE', 'ICE') or ab == 'HEATPROOF' and mtype == 'FIRE':
        m *= 0.5
    if ab == 'DRY_SKIN' and mtype == 'FIRE':
        m *= 1.25
    if ab in ('FILTER', 'SOLID_ROCK', 'PRISM_ARMOR') and te > 1:
        m *= 0.75
    if ab == 'MULTISCALE' and target.hp == target.maxhp:
        m *= 0.5
    if ab == 'FUR_COAT' and cat == 'PHYSICAL' or ab == 'ICE_SCALES' and cat == 'SPECIAL':
        m *= 0.5
    if ab == 'TERA_SHELL' and target.hp == target.maxhp:
        m *= 0.5 / max(te, 0.5)
    if att.ability == 'NEUROFORCE' and te > 1:
        m *= 1.25
    if att.ability == 'TINTED_LENS' and te < 1:
        m *= 2
    if att.item == 'ITEM_LIFE_ORB':
        m *= 1.3
    if att.item in ('ITEM_LIGHT_BALL',) and att.species.startswith('PIKACHU'):
        m *= 2
    if att.item == 'ITEM_THICK_CLUB' and cat == 'PHYSICAL':
        m *= 2
    if helping:
        m *= 1.5
    m *= getattr(att, 'progress', 1.0)
    if field.terrain == 'GRASSY_TERRAIN' and mtype == 'GRASS' or field.terrain == 'ELECTRIC_TERRAIN' and mtype == 'ELECTRIC':
        m *= 1.3
    return max(1, int(base * m))


# ---------------------------------------------------------------------------------------------
# Gevecht

STATUS_MOVES = {'TOXIC': 'tox', 'WILL_O_WISP': 'brn', 'THUNDER_WAVE': 'par', 'STUN_SPORE': 'par', 'GLARE': 'par',
                'HYPNOSIS': 'slp', 'SLEEP_POWDER': 'slp', 'SPORE': 'slp', 'SING': 'slp', 'GRASS_WHISTLE': 'slp',
                'DARK_VOID': 'slp', 'POISON_POWDER': 'psn', 'POISON_GAS': 'psn', 'LOVELY_KISS': 'slp'}
SECONDARY = {'BURN': 'brn', 'PARALYSIS': 'par', 'POISON': 'psn', 'TOXIC': 'tox', 'SLEEP': 'slp', 'FREEZE': 'par'}
DROPS = {'ATK_MINUS_1': ('atk', -1), 'DEF_MINUS_1': ('def', -1), 'SP_ATK_MINUS_1': ('spa', -1), 'SP_DEF_MINUS_1': ('spd', -1),
         'SPD_MINUS_1': ('spe', -1), 'DEF_MINUS_2': ('def', -2), 'SP_DEF_MINUS_2': ('spd', -2), 'ACC_MINUS_1': ('acc', -1)}
SELF = {'ATK_PLUS_1': {'atk': 1}, 'SP_ATK_PLUS_1': {'spa': 1}, 'DEF_PLUS_1': {'def': 1}, 'SPD_PLUS_1': {'spe': 1},
        'DEF_SPDEF_DOWN': {'def': -1, 'spd': -1}, 'ATK_DEF_DOWN': {'atk': -1, 'def': -1}, 'SP_ATK_MINUS_2': {'spa': -2},
        'ALL_STATS_UP': {'atk': 1, 'def': 1, 'spa': 1, 'spd': 1, 'spe': 1}}
SETUP = {'SWORDS_DANCE': {'atk': 2}, 'NASTY_PLOT': {'spa': 2}, 'TAIL_GLOW': {'spa': 3}, 'CALM_MIND': {'spa': 1, 'spd': 1},
         'DRAGON_DANCE': {'atk': 1, 'spe': 1}, 'QUIVER_DANCE': {'spa': 1, 'spd': 1, 'spe': 1}, 'BULK_UP': {'atk': 1, 'def': 1},
         'CURSE': {'atk': 1, 'def': 1, 'spe': -1}, 'COIL': {'atk': 1, 'def': 1}, 'HONE_CLAWS': {'atk': 1}, 'GROWTH': {'atk': 1, 'spa': 1},
         'WORK_UP': {'atk': 1, 'spa': 1}, 'HOWL': {'atk': 1}, 'IRON_DEFENSE': {'def': 2}, 'COSMIC_POWER': {'def': 1, 'spd': 1},
         'COTTON_GUARD': {'def': 3}, 'DEFENSE_CURL': {'def': 1}, 'HARDEN': {'def': 1}, 'WITHDRAW': {'def': 1}, 'AGILITY': {'spe': 2},
         'ROCK_POLISH': {'spe': 2}, 'AMNESIA': {'spd': 2}, 'ACID_ARMOR': {'def': 2}, 'BARRIER': {'def': 2}, 'SHELL_SMASH': {'atk': 2, 'spa': 2, 'spe': 2, 'def': -1, 'spd': -1},
         'MACHINE_LEARNING': {'spa': 1, 'atk': 1}, 'ACUPRESSURE': {'def': 2}, 'DEFEND_ORDER': {'def': 1, 'spd': 1},
         'STOCKPILE': {'def': 1, 'spd': 1}, 'TIDY_UP': {'atk': 1, 'spe': 1}, 'VICTORY_DANCE': {'atk': 1, 'def': 1, 'spe': 1}}
FOE_DROPS = {'SCREECH': ('def', -2), 'FAKE_TEARS': ('spd', -2), 'GROWL': ('atk', -1), 'LEER': ('def', -1), 'TAIL_WHIP': ('def', -1),
             'CHARM': ('atk', -2), 'BABY_DOLL_EYES': ('atk', -1), 'METAL_SOUND': ('spd', -2), 'SCARY_FACE': ('spe', -2),
             'STRING_SHOT': ('spe', -2), 'COTTON_SPORE': ('spe', -2), 'TICKLE': ('atk', -1), 'FEATHER_DANCE': ('atk', -2),
             'SAND_ATTACK': ('acc', -1), 'SMOKESCREEN': ('acc', -1), 'MUD_SLAP': ('acc', -1), 'FLASH': ('acc', -1)}
HEAL_HALF = ('RECOVER', 'ROOST', 'SOFT_BOILED', 'SLACK_OFF', 'MILK_DRINK', 'HEAL_ORDER', 'MOONLIGHT', 'MORNING_SUN',
             'SYNTHESIS', 'SHORE_UP')
PROTECTS = ('PROTECT', 'DETECT', 'KINGS_SHIELD', 'SPIKY_SHIELD', 'BANEFUL_BUNKER', 'SILK_TRAP', 'OBSTRUCT', 'BURNING_BULWARK')


def accuracy(att, target, mv):
    acc = mv['acc'] or 0
    if acc == 0:
        return 1.0
    s = att.stages['acc'] - target.stages['eva']
    return min(1.0, acc / 100 * stage_mult(max(-6, min(6, s))) if s >= 0 else acc / 100 * 3 / (3 - s))


def speed(m, field):
    s = m.spe * stage_mult(m.stages['spe'])
    if m.status == 'par':
        s *= 0.5
    if field.tail.get(m.side):
        s *= 2
    return s


class Battle:
    def __init__(self, players, foes, act, field_start, rng):
        self.p, self.f = players, foes
        self.act, self.rng = act, rng
        self.field = Field(field_start)
        self.block = {}
        self.taken = {}
        self.log = []
        for x in players + foes:
            x.side = 0 if x in players else 1
        # Intimidate van de speler
        for x in players:
            if x.ability == 'INTIMIDATE':
                for y in foes:
                    if y.ability not in ('CLEAR_BODY', 'HYPER_CUTTER', 'INNER_FOCUS', 'OBLIVIOUS', 'OWN_TEMPO', 'SCRAPPY'):
                        y.stages['atk'] = max(-6, y.stages['atk'] - 1)
                        if y.ability == 'DEFIANT':
                            y.stages['atk'] = min(6, y.stages['atk'] + 2)
        for y in foes:
            if y.ability == 'DRIZZLE':
                self.field.weather, self.field.wturns = 'RAIN', 5
            if y.ability == 'DROUGHT':
                self.field.weather, self.field.wturns = 'SUN', 5
            if y.ability == 'SNOW_WARNING':
                self.field.weather, self.field.wturns = 'SNOW', 5
            if y.species == 'WISHIWASHI_SCHOOL' and y.ability == 'SCHOOLING':
                y.schooling = True

    # --- vijand kiest (patroon of vrije AI) -------------------------------------------------
    def foe_choice(self, f):
        alive_p = [x for x in self.p if x.alive]
        if not alive_p or f.recharge:
            return None
        move = None
        if f.pattern:
            slot = f.pattern[f.pstep % len(f.pattern)] - 1
            if 0 <= slot < len(f.moves):
                move = f.moves[slot]
        if move is None:
            dmg = [(max(damage(f, t, m, self.field, None) for t in alive_p), m) for m in f.moves]
            best = max(dmg)
            move = best[1] if best[0] > 0 and self.rng.random() < 0.8 else self.rng.choice(f.moves)
        mv = MOVES[move]
        if f.taunt and mv['cat'] == 'STATUS':
            move = max(f.moves, key=lambda m: max(damage(f, t, m, self.field, None) for t in alive_p))
            mv = MOVES[move]
        tgt = None
        if mv['cat'] != 'STATUS' and mv['target'] not in ('BOTH', 'FOES_AND_ALLY'):
            # AI: het doel waar deze move het meeste doet (procent van de HP, KO eerst)
            tgt = max(alive_p, key=lambda t: (min(1.0, damage(f, t, move, self.field, None) / max(t.hp, 1)), self.rng.random()))
        elif mv['target'] == 'SELECTED':
            tgt = self.rng.choice(alive_p)
        return (move, tgt)

    def capped(self, f, t, dmg):
        if self.field.turn < OPENING_TURNS and t.side == 0 and f.side == 1:
            left = max(0, int(t.maxhp * OPENING_CAP) - self.taken.get(id(t), 0))
            return min(dmg, max(1, left))
        return dmg

    def expected_incoming(self, intents):
        """Verwachte schade per spelers-Pokémon deze beurt (intentie = mediaan-roll, zoals het scherm)."""
        inc = {id(x): 0 for x in self.p}
        for f, ch in intents.items():
            if not ch:
                continue
            move, tgt = ch
            mv = MOVES[move]
            if mv['cat'] == 'STATUS' or mv['effect'] in ('MIRROR_COAT', 'COUNTER'):
                continue
            targets = [x for x in self.p if x.alive] if mv['target'] in ('BOTH', 'FOES_AND_ALLY') else ([tgt] if tgt else [])
            spread = len(targets) > 1
            for t in targets:
                d = damage(f, t, move, self.field, None, spread=spread, players=self.f) * 1.08   # iets marge (hoge roll)
                inc[id(t)] += min(d, t.maxhp * HIT_CAP)
        for t in self.p:
            if self.field.turn < OPENING_TURNS:
                inc[id(t)] = min(inc[id(t)], t.maxhp * OPENING_CAP)
        return inc

    def block_amount(self, m):
        ref = (2 * 80 + 31 + 21) * LEVEL // 100 + 5
        return int(m.maxhp * BLOCK_PCT * ((m.df + m.spd) / 2) / ref * ACT_BLOCK[self.act])

    # --- speler kiest -----------------------------------------------------------------------
    def player_choices(self, intents):
        alive = [x for x in self.p if x.alive]
        foes = [x for x in self.f if x.alive]
        inc = self.expected_incoming(intents)
        choice = {}
        self._pending = {}
        # DEFEND: als een intentie een Pokémon zou uitschakelen en het blok dat voorkomt
        threatened = [x for x in alive if inc[id(x)] >= x.hp and x.status != 'slp' and not getattr(x, 'saved', False)]
        for x in alive:
            x.saved = False
        for t in sorted(threatened, key=lambda x: -x.maxhp):
            need = inc[id(t)] - t.hp + 1
            opts = []
            for d in alive:
                if id(d) in choice or d.status == 'slp' or d.recharge or d.charging:
                    continue
                amt = self.block_amount(d)
                if amt >= need:
                    opts.append((self.offense(d, foes), d))
            if opts:
                d = min(opts, key=lambda o: o[0])[1]
                choice[id(d)] = ('DEFEND', t)
                t.saved = True
                self._pending[id(t)] = self._pending.get(id(t), 0) + self.block_amount(d)
        # Daarna per Pokémon: aanvallen of verdedigen, wat de race het meest verschuift (in beurten):
        # afgevangen schade / vijandelijke schade per beurt tegen eigen schade / schade van het team per beurt.
        # (Een Pokémon die alleen over is, verdedigt dus alleen nog om een KO te voorkomen.)
        atts, dmgs = {}, {}
        for x in alive:
            if id(x) in choice:
                continue
            att = self.best_attack(x, foes, intents)
            d, kills = 0, False
            if att[0] in MOVES and att[1] is not None:
                t = att[1]
                d = min(t.hp, damage(x, t, att[0], self.field, None) * accuracy(x, t, MOVES[att[0]]))
                kills = d >= t.hp and id(t) not in [id(f) for f, c in intents.items() if c and c[0] in PROTECTS]
                if kills:
                    d *= 1.5
            atts[id(x)], dmgs[id(x)] = att, d
            if kills:
                choice[id(x)] = att        # een KO gaat altijd voor
        team_dmg = sum(dmgs.values()) or 1
        foe_dmg = max(sum(inc.values()), 1)
        for x in alive:
            if id(x) in choice:
                continue
            att = atts[id(x)]
            v_att = dmgs[id(x)] / team_dmg
            best_def, v_def = None, 0
            if x.status != 'slp' and not x.recharge and not x.charging:
                b = self.block_amount(x)
                partner = [y for y in alive if y is not x]
                opts = [(x, min(b, inc[id(x)] - self.pending_block(x)))]
                if partner:
                    y = partner[0]
                    opts.append((y, min(b, inc[id(y)] - self.pending_block(y))))
                for t, absorbed in opts:
                    if absorbed < 0.08 * t.maxhp:
                        continue        # een kras blokkeren loont niet
                    v = max(0, absorbed) / foe_dmg
                    if v > v_def:
                        best_def, v_def = t, v
            # opbouwen (Growth, Swords Dance, Work Up, ...): +1 stage = +50% schade in elke volgende beurt;
            # loont als het gevecht nog lang duurt (zoals een Power in Slay)
            setup, v_set = None, 0
            if att[0] in MOVES and x.status != 'slp' and not x.taunt:
                stat = 'atk' if MOVES[att[0]]['cat'] == 'PHYSICAL' else 'spa'
                turns_left = sum(f.hp for f in foes) / max(sum(dmgs.values()) / 1.0, 1)
                for m in x.moves:
                    up = SETUP.get(m, {}).get(stat, 0)
                    if up > 0 and x.stages[stat] < 2:
                        gain = (stage_mult(min(6, x.stages[stat] + up)) / stage_mult(x.stages[stat]) - 1)
                        v = gain * max(0, turns_left - 1) * v_att
                        if v > v_set:
                            setup, v_set = m, v
            if best_def is not None and v_def > DEFEND_BIAS * max(v_att, v_set):
                choice[id(x)] = ('DEFEND', best_def)
                self._pending[id(best_def)] = self._pending.get(id(best_def), 0) + self.block_amount(x)
            elif setup and v_set > v_att and inc[id(x)] < x.hp:
                choice[id(x)] = (setup, None)
            else:
                choice[id(x)] = att
        self._pending = {}
        return choice

    def pending_block(self, t):
        return self._pending.get(id(t), 0)

    def offense(self, x, foes):
        return max((damage(x, t, m, self.field, None) / max(t.hp, 1) for m in x.moves for t in foes), default=0)

    def best_attack(self, x, foes, intents):
        best, bestv = None, -1
        for m in x.moves:
            mv = MOVES[m]
            if mv['cat'] == 'STATUS':
                continue
            spread = mv['target'] in ('BOTH', 'FOES_AND_ALLY')
            targets = foes if spread else foes
            for t in targets:
                ch = intents.get(t)
                tm = ch[0] if ch else None
                v = 0
                hit = foes if spread else [t]
                for h in hit:
                    hc = intents.get(h)
                    hm = hc[0] if hc else None
                    if hm in PROTECTS or (hm == 'WIDE_GUARD' and spread) or any(intents.get(o) and intents[o][0] == 'WIDE_GUARD' for o in foes if spread):
                        continue
                    if (hm == 'MIRROR_COAT' and mv['cat'] == 'SPECIAL') or (hm == 'COUNTER' and mv['cat'] == 'PHYSICAL'):
                        v -= 0.5
                        continue
                    d = damage(x, h, m, self.field, None, spread=spread and len(foes) > 1) * accuracy(x, h, mv)
                    threat = 1.0 + 0.5 * max(0, max(h.stages['atk'], h.stages['spa']))
                    v += min(1.0, d / max(h.hp, 1)) * threat + (0.6 if d >= h.hp else 0)
                if mv['priority'] > 0:
                    v *= 1.02
                if v > bestv:
                    best, bestv = (m, t), v
                if spread:
                    break
        if best is None:
            return ('NONE', None)
        return best

    # --- één beurt --------------------------------------------------------------------------
    def turn(self, intents=None, pc=None):
        fl = self.field
        if intents is None:
            intents = {f: self.foe_choice(f) for f in self.f if f.alive}
            pc = self.player_choices(intents)
        self.block = {}
        self.taken = {}
        protected, wide, helping = set(), set(), set()
        hit_this_turn = {}
        actions = []
        for x in self.p:
            if x.alive:
                c = pc.get(id(x))
                pr = 4 if c and c[0] == 'DEFEND' else (MOVES[c[0]]['priority'] if c and c[0] in MOVES else 0)
                actions.append((pr, x, c))
        for f, ch in intents.items():
            if ch:
                pr = MOVES[ch[0]]['priority']
                actions.append((pr, f, ch))
            elif f.recharge:
                f.recharge = False
        tr = fl.trick > 0
        self.rng.shuffle(actions)
        actions.sort(key=lambda a: (-a[0], (speed(a[1], fl) if tr else -speed(a[1], fl))))
        for pr, x, c in actions:
            if not x.alive or not c:
                continue
            if x.recharge:
                x.recharge = False
                continue
            if x.flinch:
                continue
            if x.status == 'slp':
                if x.sleep > 0:
                    x.sleep -= 1
                    if x.sleep > 0:
                        continue
                x.status = ''
            if x.status == 'par' and self.rng.random() < 0.25:
                continue
            if x.confused:
                x.confused -= 1
                if self.rng.random() < 0.33:
                    x.hp -= _damage_core(x, x, 40, 'NONE', 'PHYSICAL', 'STRUGGLE', fl, self.rng, False, False, None, False, 1.0)
                    x.hp = max(0, x.hp)
                    continue
            if c[0] == 'DEFEND':
                amt = self.block_amount(x)
                t = c[1]
                self.block[id(t)] = self.block.get(id(t), 0) + amt
                continue
            move, tgt = c
            if move == 'NONE':
                continue
            self.use_move(x, move, tgt, protected, wide, helping, hit_this_turn, pc)
            if not any(f.alive for f in self.f) or not any(p.alive for p in self.p):
                break
        for x in self.p + self.f:
            x.flinch = False
        self.end_turn()

    def use_move(self, x, move, tgt, protected, wide, helping, hit_this_turn, pc):
        fl, rng = self.field, self.rng
        mv = MOVES[move]
        e = mv['effect']
        allies = self.p if x.side == 0 else self.f
        enemies = self.f if x.side == 0 else self.p
        if move in PROTECTS:
            protected.add(id(x))
            return
        if move == 'WIDE_GUARD':
            wide.add(x.side)
            return
        if move == 'HELPING_HAND':
            for a in allies:
                if a is not x and a.alive:
                    helping.add(id(a))
            return
        if e == 'TWO_TURNS_ATTACK' and x.charging is None:
            x.charging = move
            x.stages['spa'] = min(6, x.stages['spa'] + 1)
            return
        x.charging = None
        if mv['cat'] == 'STATUS':
            self.status_move(x, move, tgt, allies, enemies)
            return
        if e in ('MIRROR_COAT', 'COUNTER'):
            cat = 'SPECIAL' if e == 'MIRROR_COAT' else 'PHYSICAL'
            got = hit_this_turn.get((id(x), cat))
            if got:
                src, amt = got
                if src.alive:
                    self.hit(x, src, None, 2 * amt, direct=True)
            return
        if e == 'SUCKER_PUNCH':
            tc = pc.get(id(tgt)) if tgt else None
            if not tc or tc[0] == 'DEFEND' or tc[0] not in MOVES or MOVES[tc[0]]['cat'] == 'STATUS':
                return
        if e == 'FIRST_TURN_ONLY' and fl.turn > 0:
            return
        spread = mv['target'] in ('BOTH', 'FOES_AND_ALLY')
        if spread:
            targets = [t for t in enemies if t.alive]
            if mv['target'] == 'FOES_AND_ALLY':
                targets += [a for a in allies if a.alive and a is not x]
        else:
            if tgt is None or not tgt.alive:
                cands = [t for t in enemies if t.alive]
                if not cands:
                    return
                tgt = cands[0]
            targets = [tgt]
        many = len(targets) > 1
        for t in targets:
            if id(t) in protected or (spread and t.side in wide):
                continue
            if rng.random() > accuracy(x, t, mv):
                continue
            d = damage(x, t, move, fl, rng, spread=many, helping=id(x) in helping, players=allies)
            if d <= 0:
                continue
            dealt = self.hit(x, t, move, d)
            if dealt and t.side != x.side:
                hit_this_turn[(id(t), mv['cat'])] = (x, dealt)
                if t.rage:
                    t.stages['atk'] = min(6, t.stages['atk'] + 1)
            # bijeffecten
            for i, a in enumerate(mv['add']):
                ch = mv['addChance'][i] if i < len(mv['addChance']) else 100
                if mv['selfEffect'] and a in SELF:
                    if t is targets[-1]:
                        for k, v in SELF[a].items():
                            x.stages[k] = max(-6, min(6, x.stages[k] + v))
                    continue
                if not t.alive or rng.random() * 100 >= ch:
                    continue
                if a in DROPS:
                    k, v = DROPS[a]
                    t.stages[k] = max(-6, t.stages[k] + v)
                elif a in SECONDARY and not t.status:
                    self.inflict(t, SECONDARY[a])
                elif a == 'FLINCH':
                    t.flinch = True
                elif a == 'WRAP' and not t.trapped:
                    t.trapped = 5
                elif a == 'CONFUSION' and not t.confused:
                    t.confused = rng.randint(2, 5)
            if mv['drain'] and dealt:
                x.hp = min(x.maxhp, x.hp + dealt // 2)
            if mv['recoil'] and dealt:
                x.hp = max(0, x.hp - dealt * mv['recoil'] // 100)
        if e == 'ECHOED_VOICE':
            x.echo = min(4, x.echo + 1)
        if mv['recharge']:
            x.recharge = True
        if move == 'RAGE':
            x.rage = True
        if mv['type'] == 'ELECTRIC':
            x.charged = False

    def hit(self, x, t, move, d, direct=False):
        """Schade toebrengen: blok, openingsbescherming, substitute, Sturdy/Focus Sash, Schooling, bessen."""
        if t.side == 0 and x.side == 1:
            d = min(d, max(1, int(t.maxhp * HIT_CAP)))
            b = self.block.get(id(t), 0)
            ab = min(b, d)
            self.block[id(t)] = b - ab
            d -= ab
            if d <= 0:
                return 0
            if self.field.turn < OPENING_TURNS:
                d = self.capped(x, t, d)
                self.taken[id(t)] = self.taken.get(id(t), 0) + d
        if t.sub > 0 and move and not MOVES[move]['sound']:
            ab = min(t.sub, d)
            t.sub -= ab
            return 0
        full = t.hp == t.maxhp
        d = min(d, t.hp)
        if d >= t.hp and ((full and t.ability == 'STURDY') or t.sash):
            if t.sash and not (full and t.ability == 'STURDY'):
                t.sash = False
            d = t.hp - 1
        t.hp -= d
        if t.hp <= 0 and t.ability == 'INNARDS_OUT' and x.alive:
            x.hp = max(0, x.hp - d)
        if t.hp > 0 and getattr(t, 'schooling', False) and t.hp * 4 < t.maxhp:
            t.schooling = False
            t.set_stats('WISHIWASHI')
        if t.berry and t.hp > 0 and t.hp * 2 <= t.maxhp:
            t.berry = False
            if t.item == 'ITEM_PETAYA_BERRY':
                t.stages['spa'] = min(6, t.stages['spa'] + 1)
            else:
                t.hp = min(t.maxhp, t.hp + t.maxhp // 4)
        return d

    def inflict(self, t, st):
        if t.status or t.sub:
            return
        if st in ('psn', 'tox') and ('POISON' in t.types or 'STEEL' in t.types):
            return
        if st == 'brn' and ('FIRE' in t.types or t.ability == 'WATER_BUBBLE'):
            return
        if st == 'par' and 'ELECTRIC' in t.types:
            return
        if st == 'slp' and t.ability in ('INSOMNIA', 'VITAL_SPIRIT', 'SWEET_VEIL'):
            return
        t.status = st
        if st == 'slp':
            t.sleep = self.rng.randint(1, 3) + 1
        if st == 'tox':
            t.tox = 0

    def status_move(self, x, move, tgt, allies, enemies):
        fl, rng = self.field, self.rng
        mv = MOVES[move]
        live_en = [t for t in enemies if t.alive]
        if move in SETUP:
            for k, v in SETUP[move].items():
                x.stages[k] = max(-6, min(6, x.stages[k] + v))
            if move == 'CURSE' and 'GHOST' in x.types:
                pass
            return
        if move in FOE_DROPS:
            ts = live_en if mv['target'] in ('BOTH', 'FOES_AND_ALLY') else ([tgt] if tgt and tgt.alive else live_en[:1])
            k, v = FOE_DROPS[move]
            for t in ts:
                if rng.random() <= accuracy(x, t, mv):
                    t.stages[k] = max(-6, t.stages[k] + v)
            return
        if move in STATUS_MOVES:
            ts = live_en if mv['target'] in ('BOTH',) else ([tgt] if tgt and tgt.alive else (rng.sample(live_en, 1) if live_en else []))
            for t in ts:
                if rng.random() <= accuracy(x, t, mv):
                    self.inflict(t, STATUS_MOVES[move])
            return
        if move in HEAL_HALF:
            x.hp = min(x.maxhp, x.hp + x.maxhp // 2)
            return
        if move == 'STRENGTH_SAP' and live_en:
            t = tgt if tgt and tgt.alive else live_en[0]
            x.hp = min(x.maxhp, x.hp + int(t.atk * stage_mult(t.stages['atk'])))
            t.stages['atk'] = max(-6, t.stages['atk'] - 1)
            return
        if move in ('AQUA_RING', 'INGRAIN'):
            x.ring = True
            return
        if move == 'LEECH_SEED' and live_en:
            t = tgt if tgt and tgt.alive else rng.choice(live_en)
            if 'GRASS' not in t.types and rng.random() < 0.9:
                t.seeded = True
            return
        if move in ('SUPERSONIC', 'CONFUSE_RAY', 'SWEET_KISS', 'TEETER_DANCE') and live_en:
            t = tgt if tgt and tgt.alive else rng.choice(live_en)
            if rng.random() <= accuracy(x, t, mv) and not t.confused:
                t.confused = rng.randint(2, 5)
            return
        if move == 'YAWN' and live_en:
            t = tgt if tgt and tgt.alive else rng.choice(live_en)
            if not t.status and not t.yawn:
                t.yawn = 2
            return
        if move == 'SOAK' and live_en:
            t = tgt if tgt and tgt.alive else rng.choice(live_en)
            if rng.random() <= accuracy(x, t, mv):
                t.types = ['WATER']
            return
        if move == 'TAUNT' and live_en:
            t = tgt if tgt and tgt.alive else rng.choice(live_en)
            t.taunt = 3
            return
        if move in ('RAIN_DANCE', 'SUNNY_DAY', 'SANDSTORM', 'SNOWSCAPE', 'HAIL'):
            fl.weather = {'RAIN_DANCE': 'RAIN', 'SUNNY_DAY': 'SUN', 'SANDSTORM': 'SAND'}.get(move, 'SNOW')
            fl.wturns = 5
            return
        if move == 'TRICK_ROOM':
            fl.trick = 0 if fl.trick else 5
            return
        if move == 'TAILWIND':
            fl.tail[x.side] = 4
            return
        if move in ('REFLECT', 'LIGHT_SCREEN'):
            fl.screens[x.side][move] = 5
            return
        if move == 'SUBSTITUTE' and x.hp > x.maxhp // 4 and not x.sub:
            x.hp -= x.maxhp // 4
            x.sub = x.maxhp // 4
            return
        if move == 'HAZE':
            for m in self.p + self.f:
                m.stages = dict(STAGE)
            return
        if move == 'CHARGE':
            x.charged = True
            x.stages['spd'] = min(6, x.stages['spd'] + 1)
            return
        if move == 'FOCUS_ENERGY':
            x.focus = True
            return
        if move == 'METRONOME':
            if live_en:
                t = rng.choice(live_en)
                d = _damage_core(x, t, 80, 'NORMAL', 'SPECIAL' if x.spa > x.atk else 'PHYSICAL', 'METRONOME', fl, rng, False, None, None, False, eff('NORMAL', t.types))
                self.hit(x, t, 'TACKLE', d)
            return
        if move == 'TRANSFORM' and live_en:
            t = max(live_en, key=lambda m: max(m.atk, m.spa))
            x.types = list(t.types)
            x.atk, x.df, x.spa, x.spd, x.spe = t.atk, t.df, t.spa, t.spd, t.spe
            x.moves = list(t.moves)
            x.pattern = []
            return
        # overige statusmoves (Mist, After You, Purify, Encore, Torment, ...): geen effect in het model

    def end_turn(self):
        fl = self.field
        for x in self.p + self.f:
            if not x.alive:
                continue
            frac = 0
            if x.status == 'brn':
                frac += 1 / 16
            if x.status == 'psn':
                frac += 1 / 8
            if x.status == 'tox':
                x.tox += 1
                frac += x.tox / 16
            if x.trapped:
                x.trapped -= 1
                frac += 1 / 8
            if x.seeded:
                frac += 1 / 8
                for o in (self.f if x.side == 0 else self.p):
                    if o.alive:
                        o.hp = min(o.maxhp, o.hp + int(x.maxhp / 8))
                        break
            if fl.weather == 'SAND' and not set(x.types) & {'ROCK', 'GROUND', 'STEEL'}:
                frac += 1 / 16
            if x.status == 'slp' and any(o.ability == 'BAD_DREAMS' and o.alive for o in (self.f if x.side == 0 else self.p)):
                frac += 1 / 8
            if frac and x.ability != 'MAGIC_GUARD':
                x.hp = max(0, x.hp - int(x.maxhp * frac))
            heal = 0
            if x.ring:
                heal += 1 / 16
            if x.item == 'ITEM_LEFTOVERS':
                heal += 1 / 32     # in de Spire 1/32 voor iedereen (battle_hold_effects.c)
            if fl.terrain == 'GRASSY_TERRAIN':
                heal += 1 / 16
            if fl.weather == 'RAIN' and x.ability == 'RAIN_DISH':
                heal += 1 / 16
            if heal and x.alive:
                x.hp = min(x.maxhp, x.hp + int(x.maxhp * heal))
            if x.yawn:
                x.yawn -= 1
                if x.yawn == 0:
                    self.inflict(x, 'slp')
            if x.taunt:
                x.taunt -= 1
            if x.ability == 'SPEED_BOOST':
                x.stages['spe'] = min(6, x.stages['spe'] + 1)
        if fl.wturns:
            fl.wturns -= 1
            if not fl.wturns:
                fl.weather = None
        if fl.trick:
            fl.trick -= 1
        for s in (0, 1):
            if fl.tail[s]:
                fl.tail[s] -= 1
            for k in list(fl.screens[s]):
                fl.screens[s][k] -= 1
                if fl.screens[s][k] <= 0:
                    del fl.screens[s][k]
        for f in self.f:
            f.pstep += 1   # Spire_EndTurn: elk patroon schuift elke beurt door
        fl.turn += 1

    def run(self, max_turns=40):
        while self.field.turn < max_turns:
            self.turn()
            if not any(f.alive for f in self.f):
                return True
            if not any(p.alive for p in self.p):
                return False
        return False


# ---------------------------------------------------------------------------------------------
# Opbouw

def coverage_type(sp, foes):
    """Het type dat het meest doet tegen deze vijanden (gemiddelde effectiviteit, gewogen naar HP)."""
    best, bv = None, -1
    for t in CHART:
        if t in ('NONE', 'MYSTERY', 'STELLAR') or t in SPECIES[sp]['types']:
            continue
        v = 0
        for f in foes:
            fs = SPECIES[f['s']] if f['s'] in SPECIES else None
            if not fs:
                continue
            ab = f.get('a')
            e = 0 if IMMUNE.get(ab) == t else eff(t, fs['types'])
            v += e * f.get('hp', 1.0)
        if v > bv:
            best, bv = t, v
    return best


def player_mon(rental, act, kind, evo, enc=None):
    sp = form_in_act(rental['s'], act, evo)
    b = SPECIES[sp]
    moves = list(rental['m'])
    phys = b['atk'] >= b['spa']
    power = REWARD[(act, kind)]
    if power:
        for t in b['types'][:2]:
            moves.append(('REWARD', t, 'PHYSICAL' if phys else 'SPECIAL', power))
        if enc is not None and kind in COVERAGE:
            ct = coverage_type(sp, enc['foes'])
            if ct:
                moves.append(('REWARD', ct, 'PHYSICAL' if phys else 'SPECIAL', power - COVERAGE[kind]))
    m = Mon(sp, [], 0, HP_PLAYER, 31, 84, name=sp)
    m.moves = []
    for mv in moves:
        if isinstance(mv, tuple):
            key = 'REWARD_%s_%s_%d' % (mv[1], mv[2], mv[3])
            if key not in MOVES:
                MOVES[key] = dict(name=key, effect='HIT', power=mv[3], type=mv[1], cat=mv[2], acc=100, pp=10, priority=0,
                                  target='SELECTED', strikes=1, add=[], addChance=[], selfEffect=False, recoil=0, drain=False,
                                  charge=False, recharge=False, sound=False, contact=mv[2] == 'PHYSICAL', signature=False, zmove=False, body='')
            m.moves.append(key)
        elif mv in MOVES:
            m.moves.append(mv)
    m.hp = int(m.maxhp * ARRIVE[kind])
    m.progress = PROGRESS[(act, kind)]
    return m


def foe_mons(enc, hfac):
    out = []
    for f in enc['foes']:
        sp = E.MODEL_AS.get(f['s'], f['s']) if f.get('a') == 'SCHOOLING' else f['s']
        if sp not in SPECIES:
            sp = f['s']
        hpm = round(f.get('hp', 1.0) * E.foe_hfac(enc, f, hfac) * 10) / 10
        m = Mon(sp, f['m'], 1, hpm, 20, 0, ability=f.get('a') or None, item=f.get('i'), boosts=f.get('b'),
                pattern=f.get('p'), gimmick=f.get('g'), name=f['s'])
        if f.get('a') is None:
            m.ability = SPECIES[sp]['abilities'][0] if SPECIES[sp]['abilities'] else 'NONE'
        out.append(m)
    return out


def simulate(enc, act, kind, hfac, pair, rentals_by, evo, n, seed=1):
    rng = random.Random(seed)
    wins, lost = 0, []
    for i in range(n):
        players = [player_mon(rentals_by[s], act, kind, evo, enc) for s in pair]
        foes = foe_mons(enc, hfac)
        start = sum(p.hp for p in players)
        b = Battle(players, foes, act, enc.get('field'), rng)
        ok = b.run()
        wins += ok
        lost.append((start - sum(p.hp for p in players)) / sum(p.maxhp for p in players))
    return wins / n, statistics.mean(lost)


def one_battle(enc, act, kind, hfac, pair, rentals_by, evo, seed):
    """(gewonnen, HP-verlies als deel van de team-HP, beurten)."""
    rng = random.Random(seed)
    players = [player_mon(rentals_by[s], act, kind, evo, enc) for s in pair]
    foes = foe_mons(enc, hfac)
    start = sum(p.hp for p in players)
    b = Battle(players, foes, act, enc.get('field'), rng)
    ok = b.run()
    return ok, (start - sum(p.hp for p in players)) / sum(p.maxhp for p in players), b.field.turn


# ---------------------------------------------------------------------------------------------
# Kalibratie (Slay: gewone gevechten kosten weinig, elites en bazen veel, elke act meer)

DRAFT_ODDS = (35, 35, 22, 8)    # C/B/A/S, zoals Spire_RandomRental


def random_pairs(rentals, n, seed=12345):
    rng = random.Random(seed)
    by_tier = {t: [r['s'] for r in rentals if r['tier'] == t] for t in range(4)}
    out = []
    while len(out) < n:
        pair = []
        for _ in range(2):
            x = rng.randrange(100)
            t = 0 if x < 35 else 1 if x < 70 else 2 if x < 92 else 3
            pair.append(rng.choice(by_tier[t]))
        if pair[0] != pair[1]:
            out.append(tuple(pair))
    return out


def enc_stats(enc, act, kind, hfac, pairs, rentals_by, evo, salt=0):
    res = [one_battle(enc, act, kind, hfac, p, rentals_by, evo, seed=1000 * i + salt) for i, p in enumerate(pairs)]
    return dict(win=sum(r[0] for r in res) / len(res), loss=100 * statistics.mean(r[1] for r in res),
                turns=statistics.median(r[2] for r in res))


def group_key(act, kind, e):
    """Kalibratiegroep: zwakke, gewone en elite-gevechten per act samen (de puzzels binnen een groep verschillen
    bewust: de verhouding blijft staan), bazen elk apart."""
    return (act, kind) if kind != 'boss' else (act, 'boss:' + e['name'])


TURN_RANGE = {'weak': (1.5, 4), 'normal': (2, 5), 'elite': (3, 7), 'boss': (6, 10)}   # bazen hooguit ±10 beurten: langer = HP-spons, dan wint alleen nog schade


def calibrate_sim(rows, n_pairs=None, verbose=False):
    """Per act en soort gevecht (bazen elk apart) één HP-factor, zodat de mediaan van het gemiddelde HP-verlies
    (willekeurige draftparen, echte gevechten) op het doel valt (encounters.TARGET_ACT). Returns
    (calib, stats): calib[key] = (0, factor, mediaan beurten, mediaan verlies), stats[naam] = dict(win, loss, turns)."""
    rentals, evo = load_rentals()
    by = {r['s']: r for r in rentals}
    pairs = random_pairs(rentals, n_pairs or CALIB_PAIRS)
    groups = {}
    for act, kind, biome, e in rows:
        groups.setdefault(group_key(act, kind, e), []).append((act, kind, e))
    calib, stats = {}, {}
    for key, items in sorted(groups.items(), key=lambda kv: str(kv[0])):
        act, kind = key[0], items[0][1]
        tturns, target = E.TARGET_ACT[(kind, act)]
        lo_t, hi_t = TURN_RANGE[kind]

        def err(h):
            st = [enc_stats(e, a, k, h, pairs, by, evo, salt=j) for j, (a, k, e) in enumerate(items)]
            ml = statistics.median(x['loss'] for x in st)
            mt = statistics.median(x['turns'] for x in st)
            # op HP-verlies, met de beurten erbij (een baas van 30 beurten is geen baas maar geduld)
            v = math.log(max(ml, 0.5) / target) ** 2 + (1.0 if kind == 'boss' else 0.3) * math.log(mt / tturns) ** 2
            if not lo_t <= mt <= hi_t:
                v += 5 + abs(mt - (lo_t if mt < lo_t else hi_t))
            return v
        grid = [0.25 * 1.25 ** i for i in range(19)]           # 0.25 .. 13
        errs = {h: err(h) for h in grid}
        h0 = min(errs, key=errs.get)
        for h in (h0 / 1.12, h0 / 1.06, h0 * 1.06, h0 * 1.12):
            errs[h] = err(h)
        h = round(min(errs, key=errs.get), 2)
        st = [enc_stats(e, a, k, h, pairs, by, evo, salt=j) for j, (a, k, e) in enumerate(items)]
        for (a, k, e), x in zip(items, st):
            stats[e['name']] = x
        calib[key] = (0, h, statistics.median(x['turns'] for x in st), statistics.median(x['loss'] for x in st))
        if verbose:
            print('kalibratie %-28s ×%.2f  verlies %4.1f%% (doel %d%%)  beurten %.1f' % (str(key), h, calib[key][3], target, calib[key][2]))
    return calib, stats


def all_targets():
    """Alle elites (per biome) en bazen, met hun kalibratie."""
    E.totem_elites()
    warns = []
    rows = []
    for b in E.BIOMES:
        for e in E.ENCOUNTERS[b['key']]:
            E.check(e, b['key'], warns)
            rows.append((b['act'], e['kind'], b['name'], e))
    for act, lst in E.BOSSES.items():
        for e in lst:
            E.check(e, 'BOSS', warns)
            e['kind'] = 'boss'
            rows.append((act, 'boss', 'Boss', e))
    return rows


CALIB_PAIRS = 40
CALIB_FILE = os.path.join(HERE, 'spire_calib.json')


def save_calib(calib, stats):
    import json
    data = dict(calib={'%d|%s' % k: v for k, v in calib.items()}, stats=stats)
    with open(CALIB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1, sort_keys=True)


def load_calib():
    import json
    data = json.load(open(CALIB_FILE, encoding='utf-8'))
    calib = {}
    for k, v in data['calib'].items():
        act, kind = k.split('|', 1)
        calib[(int(act), kind)] = tuple(v)
    return calib, data['stats']


# --- slechtste startcombinatie (parallel) ------------------------------------------------------
_W = {}


def draft_pairs(rentals, n, seed=777):
    """Startcombinaties zoals een speler ze kiest: tien aanbiedingen (C/B/A/S 35/35/22/8%, Spire_RandomRental),
    de twee sterkste (tier), bij gelijke tier liefst verschillende types. De baas ken je bij de draft nog niet."""
    rng = random.Random(seed)
    by_tier = {t: [r for r in rentals if r['tier'] == t] for t in range(4)}
    out = []
    while len(out) < n:
        offers = []
        while len(offers) < 10:
            x = rng.randrange(100)
            t = 0 if x < 35 else 1 if x < 70 else 2 if x < 92 else 3
            r = rng.choice(by_tier[t])
            if r not in offers:
                offers.append(r)
        rng.shuffle(offers)
        offers.sort(key=lambda r: -r['tier'])
        first = offers[0]
        t1 = SPECIES[first['s']]['types']
        rest = offers[1:]
        top = rest[0]['tier']
        cands = [r for r in rest if r['tier'] == top and not set(SPECIES[r['s']]['types']) & set(t1)] or rest
        out.append((first['s'], cands[0]['s']))
    return out


def _worst_one(job):
    act, kind, biome, e, hfac, n_screen, n_pairs, worst_k, quick = job
    rentals, evo, by, drafts = _W['rentals'], _W['evo'], _W['by'], _W['drafts']
    # 1. realistische startcombinaties (draft): de eis
    scr = []
    for i, p in enumerate(drafts):
        w = sum(one_battle(e, act, kind, hfac, p, by, evo, seed=31 * k + i)[0] for k in range(n_screen)) / n_screen
        scr.append((w, p))
    scr.sort()
    fin = []
    for i, (w0, p) in enumerate(scr[:worst_k]):
        rs = [one_battle(e, act, kind, hfac, p, by, evo, seed=5000 + 1000 * k + i) for k in range(n_pairs)]
        fin.append((p, (sum(x[0] for x in rs) / n_pairs, statistics.mean(x[1] for x in rs))))
    fin.sort(key=lambda x: x[1][0])
    # 2. theoretisch slechtste (alle rentals met zichzelf, dan de zwaksten onderling): ter informatie
    pool = rentals[::3] if quick else rentals
    single = []
    for r in pool:
        w = sum(one_battle(e, act, kind, hfac, (r['s'], r['s']), by, evo, seed=(zlib_hash(r['s']) + 7 * i))[0] for i in range(max(4, n_screen // 2))) / max(4, n_screen // 2)
        single.append((w, r['s']))
    single.sort()
    worst = [x for _, x in single[:6]]
    res_pairs = []
    for i in range(len(worst)):
        for j in range(i + 1, len(worst)):
            p = (worst[i], worst[j])
            rs = [one_battle(e, act, kind, hfac, p, by, evo, seed=1000 * k + i * 31 + j) for k in range(20)]
            res_pairs.append((p, (sum(x[0] for x in rs) / 20, statistics.mean(x[1] for x in rs))))
    res_pairs.sort(key=lambda x: x[1][0])
    return dict(act=act, kind=kind, biome=biome, name=e['name'],
                foes=' + '.join(SPECIES[f['s']]['dispname'] if f['s'] in SPECIES else f['s'] for f in e['foes']),
                draft_mean=statistics.mean(w for w, _ in scr), draft_low=sum(w < MIN_WIN for w, _ in scr) / len(scr),
                worst_draft=fin[0] if fin else None,
                worst_pair=res_pairs[0] if res_pairs else None,
                median_single=statistics.median(w for w, _ in single), worst_single=single[:3])


def zlib_hash(s):
    import zlib
    return zlib.crc32(s.encode()) & 0xFFFF


N_DRAFTS = 150


def worst_case(rows, calib, kinds=('elite', 'boss'), only=None, n_screen=6, n_pairs=40, worst_k=8, quick=False, procs=3):
    """Per elite/baas: N_DRAFTS gedrafte startparen (zoals een speler kiest), de acht slechtste opnieuw met n_pairs
    gevechten: het slechtste draftpaar telt (de eis). Ter informatie ook het theoretisch slechtste paar uit alle rentals."""
    import multiprocessing as mp
    rentals, evo = load_rentals()
    _W.update(rentals=rentals, evo=evo, by={r['s']: r for r in rentals}, drafts=draft_pairs(rentals, N_DRAFTS))
    jobs = []
    for act, kind, biome, e in rows:
        if kind not in kinds or (only and only.lower() not in e['name'].lower()):
            continue
        hfac = calib.get(group_key(act, kind, e), (0, 1.0))[1]
        jobs.append((act, kind, biome, e, hfac, n_screen, n_pairs, worst_k, quick))
    if procs > 1 and len(jobs) > 1:
        with mp.get_context('fork').Pool(procs) as pool:
            return pool.map(_worst_one, jobs)
    return [_worst_one(j) for j in jobs]


def pair_report(rows, calib, pairs, only=None, n=200):
    rentals, evo = load_rentals()
    by = {r['s']: r for r in rentals}
    out = []
    for act, kind, biome, e in rows:
        if kind not in ('elite', 'boss') or (only and only.lower() not in e['name'].lower()):
            continue
        hfac = calib.get(group_key(act, kind, e), (0, 1.0))[1]
        for p in pairs:
            rs = [one_battle(e, act, kind, hfac, p, by, evo, seed=k) for k in range(n)]
            out.append((act, kind, e['name'], p, sum(x[0] for x in rs) / n, statistics.mean(x[1] for x in rs),
                        statistics.median(x[2] for x in rs)))
    return out


def _dist_one(job):
    act, kind, e, hfac, pairs, n = job
    by, evo = _W['by'], _W['evo']
    out = []
    for i, p in enumerate(pairs):
        out.append(sum(one_battle(e, act, kind, hfac, p, by, evo, seed=97 * k + i)[0] for k in range(n)) / n)
    return e['name'], out


def pair_distribution(rows, calib, n_pairs=200, n=10, kinds=('elite', 'boss'), only=None, procs=3):
    """Winkans per willekeurig draftpaar: hoeveel paren zitten onder 5/15%? (de staart van de verdeling)"""
    import multiprocessing as mp
    rentals, evo = load_rentals()
    _W.update(rentals=rentals, evo=evo, by={r['s']: r for r in rentals})
    pairs = random_pairs(rentals, n_pairs, seed=4242)
    jobs = [(act, kind, e, calib.get(group_key(act, kind, e), (0, 1.0))[1], pairs, n) for act, kind, b, e in rows
            if kind in kinds and (not only or only.lower() in e['name'].lower())]
    with mp.get_context('fork').Pool(procs) as pool:
        res = pool.map(_dist_one, jobs)
    return [(name, sum(w < 0.05 for w in ws) / len(ws), sum(w < 0.15 for w in ws) / len(ws), statistics.mean(ws),
             sorted(zip(ws, pairs))[:3]) for name, ws in res]


def report(results):
    R = ['', SECTION, '',
         'Jordi (5 okt): een 0%% winkans mag in geen enkele run ontstaan. Per elite en baas %d startparen zoals een speler ze draft '
         '(tien aanbiedingen C/B/A/S 35/35/22/8%%, de twee sterkste, liefst verschillende types; de baas ken je dan nog niet), elk %d gevechten; '
         'de acht slechtste opnieuw met 40 gevechten. **Eis: het slechtste draftpaar wint minstens %d%%** (`matchups.MIN_WIN`, encounters.py faalt anders). '
         'Ter informatie het theoretisch slechtste paar uit álle rentals (de zwakste zes met zichzelf als partner, dan onderling): dat zijn teams die een speler '
         'niet kiest (twee C-rentals met hetzelfde zwakke type) en die krijgen in het echt ook relics, items en betere beloningen dan de bot.' % (N_DRAFTS, 6, MIN_WIN * 100), '',
         'Speler = bot die de intenties leest: DEFEND om een KO te voorkomen of als het blok meer oplevert dan aanvallen, opbouwen (Growth, Swords Dance, ...) als het gevecht lang duurt, '
         'een KO gaat altijd voor; startkit + STAB-beloningen + één dekkingsmove, schade x%.2f-%.2f voor upgrades en schade-relics (zie `matchups.py`). '
         'Aankomst met %d%% (elite) / %d%% (baas) HP. Openingsbescherming: in beurt 1-%d per beurt hooguit %d%% van de max HP; klap-limiet: één klap hooguit %d%%.'
         % (min(PROGRESS.values()), max(PROGRESS.values()), ARRIVE['elite'] * 100, ARRIVE['boss'] * 100, OPENING_TURNS, OPENING_CAP * 100, HIT_CAP * 100), '',
         '| act | soort | ontmoeting | gem. draftpaar | onder de eis | slechtste draftpaar | winkans | theoretisch slechtste |',
         '|---|---|---|---|---|---|---|---|']
    for r in results:
        if not r.get('worst_draft'):
            continue
        (a, b), (w, l) = r['worst_draft']
        (c, d), (w2, _) = r['worst_pair']
        R.append('| %d | %s | %s (%s) | %.0f%% | %.1f%% | %s + %s | **%.0f%%** | %s + %s %.0f%% |' % (
            r['act'], r['kind'], r['name'], r['foes'], 100 * r['draft_mean'], 100 * r['draft_low'],
            SPECIES[a]['dispname'], SPECIES[b]['dispname'], 100 * w, SPECIES[c]['dispname'], SPECIES[d]['dispname'], 100 * w2))
    return R


def check(results):
    bad = []
    for r in results:
        if r.get('worst_draft') and r['worst_draft'][1][0] < MIN_WIN:
            (a, b), (w, l) = r['worst_draft']
            bad.append('act %d %s %s: draftpaar %s + %s wint %.0f%%' % (r['act'], r['kind'], r['name'], a, b, 100 * w))
    return bad


def print_worst(res):
    for r in res:
        (x, y), (w, l) = r['worst_draft']
        (c, d), (w2, _) = r['worst_pair']
        print('act %d %-6s %-26s draft gem %3.0f%% (%4.1f%% < eis)  slechtste draft %s + %s: %3.0f%%  | theoretisch %s + %s %3.0f%%' % (
            r['act'], r['kind'], r['name'], 100 * r['draft_mean'], 100 * r['draft_low'], x, y, 100 * w, c, d, 100 * w2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only')
    ap.add_argument('--pair', nargs=2, action='append')
    ap.add_argument('-n', type=int, default=200)
    ap.add_argument('--quick', action='store_true')
    ap.add_argument('--recalibrate', action='store_true', help='niet spire_calib.json lezen maar opnieuw kalibreren')
    ap.add_argument('--hits', action='store_true', help='klappen boven 45%% van een volle Pokémon')
    ap.add_argument('--dist', action='store_true', help='winkans van 150 willekeurige draftparen per elite/baas')
    a = ap.parse_args()
    rows = all_targets()
    if a.recalibrate or not os.path.exists(CALIB_FILE):
        calib, _ = calibrate_sim(rows, verbose=True)
    else:
        calib, _ = load_calib()
    if a.only and not a.recalibrate:
        # alleen de groep(en) van deze ontmoeting opnieuw kalibreren (snel itereren)
        keys = {group_key(act, kind, e) for act, kind, b, e in rows if a.only.lower() in e['name'].lower()}
        sub = [r for r in rows if group_key(r[0], r[1], r[3]) in keys]
        c2, st2 = calibrate_sim(sub, verbose=True)
        calib.update(c2)
        for act, kind, b, e in sub:
            x = st2[e['name']]
            print('  %-28s winkans %3.0f%%  verlies %4.1f%%  beurten %.1f' % (e['name'], 100 * x['win'], x['loss'], x['turns']))
    E.CALIB.update(calib)
    if a.dist:
        for name, p5, p15, mean, worst in pair_distribution(rows, calib, n_pairs=150, n=8, only=a.only):
            print('%-28s <5%%: %4.1f%%  <15%%: %4.1f%%  gem %3.0f%%  slechtst %s' % (
                name, 100 * p5, 100 * p15, 100 * mean, ', '.join('%s+%s %.0f%%' % (p[0], p[1], 100 * w) for w, p in worst)))
        return
    if a.hits:
        for r in hit_table(rows):
            print('act %d %-5s %-22s %-18s %-14s med %3.0f%% max %3.0f%% (%s)' % (r[0], r[1], r[2][:22], r[3][:18], r[4], 100 * r[5], 100 * r[6], r[7]))
        return
    if a.pair:
        for act, kind, name, p, w, l, t in pair_report(rows, calib, [tuple(x) for x in a.pair], a.only, a.n):
            print('act %d %-6s %-28s %s + %s: winkans %3.0f%%, HP-verlies %3.0f%%, beurten %.1f' % (act, kind, name, p[0], p[1], 100 * w, 100 * l, t))
        return
    res = worst_case(rows, calib, only=a.only, quick=a.quick)
    print_worst(res)
    bad = check(res)
    if bad:
        print('\nONDER DE EIS (%d%%):' % (MIN_WIN * 100))
        for b in bad:
            print('  ' + b)
        sys.exit(1)


def calibrated_rows():
    rows = all_targets()
    E.CALIB.update(load_calib()[0])
    return rows


def hit_table(rows=None, limit=0.45, kinds=('elite', 'boss')):
    """Per vijandelijke aanval: schade van één klap (hoogste roll, geen crit) op een volle Pokémon van de speler
    (vorm van die act, ×4 HP), als mediaan over alle rentals en de hoogste. Returns [(act, kind, naam, soort, move, med, max, wie)]."""
    rows = rows or calibrated_rows()
    rentals, evo = load_rentals()
    fl = Field()
    out = []
    for act, kind, biome, e in rows:
        if kind not in kinds:
            continue
        key = (act, kind) if kind != 'boss' else (act, 'boss:' + e['name'])
        fs = foe_mons(e, E.CALIB.get(key, (0, 1.0))[1])
        ps = [player_mon(r, act, kind, evo, e) for r in rentals]
        for f in fs:
            for m in f.moves:
                mv = MOVES[m]
                if mv['cat'] == 'STATUS' or mv['effect'] in ('MIRROR_COAT', 'COUNTER'):
                    continue
                spread = mv['target'] in ('BOTH', 'FOES_AND_ALLY')
                vals = sorted((damage(f, p, m, fl, None, spread=spread, roll=1.0, players=fs) / p.maxhp, p.species) for p in ps)
                med, mx = vals[len(vals) // 2][0], vals[-1]
                if mx[0] > limit:
                    out.append((act, kind, e['name'], f.species, m, med, mx[0], mx[1]))
    return out


def trace(name, pair, seed=1, turns=30):
    """Eén gevecht beurt voor beurt (debug): python3 -c "import matchups as M; M.trace('Totem Wishiwashi', ('BELDUM', 'ZORUA'))"."""
    rows = calibrated_rows()
    rentals, evo = load_rentals()
    by = {r['s']: r for r in rentals}
    act, kind, _, e = [r for r in rows if r[3]['name'] == name][0]
    key = (act, kind) if kind != 'boss' else (act, 'boss:' + e['name'])
    ps = [player_mon(by[s], act, kind, evo, e) for s in pair]
    fs = foe_mons(e, E.CALIB[key][1])
    for m in ps + fs:
        print('%-14s hp %4d/%4d atk %3d def %3d spa %3d spd %3d spe %3d %-14s %s %s' % (
            m.species, m.hp, m.maxhp, m.atk, m.df, m.spa, m.spd, m.spe, m.ability, m.types, m.moves))
    b = Battle(ps, fs, act, e.get('field'), random.Random(seed))
    for t in range(turns):
        intents = {f: b.foe_choice(f) for f in b.f if f.alive}
        pc = b.player_choices(intents)
        print('T%d vijand %s | speler %s' % (t + 1, ', '.join('%s:%s>%s' % (f.species, c[0], c[1].species if c[1] else '-') for f, c in intents.items() if c),
                                             ', '.join('%s:%s>%s' % (p.species, pc[id(p)][0], pc[id(p)][1].species if pc[id(p)][1] else '-') for p in b.p if p.alive)))
        b.turn(intents, pc)
        print('    ' + ', '.join('%s %d%%%s' % (m.species, 100 * m.hp // m.maxhp, ('/' + m.status) if m.status else '') for m in ps + fs))
        if not any(f.alive for f in fs) or not any(p.alive for p in ps):
            break


if __name__ == '__main__':
    main()
