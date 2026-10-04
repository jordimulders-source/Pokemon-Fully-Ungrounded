"""The Spire: rekenwerk voor de rentals, verboden moves, startmoves, beloningsmoves en item-getallen.

Gebruik:
    python3 spire_pool.py            # rapport naar SPIRE_BALANS.md, data naar src/data/spire_pool.h
    python3 spire_pool.py --show X   # details van één soort (bijv. --show PIKACHU)

Model (zie SPIRE_BALANS.md voor de uitleg):
- Een rental begint in zijn eerste (niet-baby) vorm en evolueert na de baas van act 1 en act 2.
- Rating van een vorm = wortel(aanval x bulk) x snelheidsfactor x ability-factor, op lv 50
  (IV 31, EV 84, zoals de rentals). 100 = mediaan van alle volledig geëvolueerde kandidaten.
- Runwaarde = gemiddelde rating over de drie acts (vorm per act).
- Startkit: STAB-aanval 40-50 per type (fysiek/speciaal naar de hoogste aanvalsstat over de run),
  een basis-statusmove (Growl, Tail Whip, ...; gekozen met een verwachtingswaardemodel van een gevecht)
  en een 'grounded' move die bij de soort past (Leech Seed, Sing, Thunder Wave, ...).
"""
import argparse, math, os, statistics, sys
import spiredata

ROOT = spiredata.ROOT
MOVES = spiredata.load_moves()
SPECIES = spiredata.load_species()

LEVEL, IV, EV = 50, 31, 84

# ---------------------------------------------------------------------------------------------
# 1. Verboden moves (gelden voor de speler, beloningen én tegenstanders)

BANNED = {
    'wisselen of vluchten (je kunt in de Spire niet wisselen)': [
        'TELEPORT', 'ROAR', 'WHIRLWIND', 'U_TURN', 'VOLT_SWITCH', 'FLIP_TURN', 'PARTING_SHOT', 'BATON_PASS',
        'SHED_TAIL', 'CHILLY_RECEPTION', 'DRAGON_TAIL', 'CIRCLE_THROW', 'HEALING_WISH', 'LUNAR_DANCE',
        'MEMENTO', 'REVIVAL_BLESSING'],
    'doet niets (of alleen buiten gevechten)': [
        'SPLASH', 'CELEBRATE', 'HOLD_HANDS', 'HAPPY_HOUR', 'SWEET_SCENT', 'CAMOUFLAGE', 'CONVERSION',
        'CONVERSION_2', 'SKETCH', 'RECYCLE', 'BESTOW', 'EMBARGO', 'TELEKINESIS', 'LUCKY_CHANT', 'MUD_SPORT',
        'WATER_SPORT', 'SNATCH', 'GRUDGE', 'IMPRISON', 'NIGHTMARE', 'ATTRACT', 'CAPTIVATE', 'DEFOG',
        'COURT_CHANGE', 'ION_DELUGE', 'FAIRY_LOCK', 'MEAN_LOOK', 'BLOCK', 'SPIDER_WEB', 'FORESIGHT',
        'ODOR_SLEUTH', 'MIRACLE_EYE', 'LOCK_ON', 'MIND_READER', 'SPOTLIGHT', 'MAGNET_RISE', 'MIMIC',
        'SPIKES', 'TOXIC_SPIKES', 'STEALTH_ROCK', 'STICKY_WEB', 'GRAVITY', 'MAGIC_ROOM', 'PLAY_NICE'],
    'vaste of procentuele schade (negeert de HP-vermenigvuldiger)': [
        'PSYWAVE', 'SONIC_BOOM', 'DRAGON_RAGE', 'SEISMIC_TOSS', 'NIGHT_SHADE', 'SUPER_FANG', 'NATURES_MADNESS',
        'RUINATION', 'ENDEAVOR', 'PAIN_SPLIT', 'FINAL_GAMBIT', 'GUILLOTINE', 'HORN_DRILL', 'FISSURE',
        'SHEER_COLD', 'GUARDIAN_OF_ALOLA', 'BIDE'],
    'KO ongeacht HP (breekt bazen met xHP)': ['PERISH_SONG', 'DESTINY_BOND'],
    'jezelf opofferen (zonder wissel blijft je partner alleen; Jordi: nutteloos)': [
        'EXPLOSION', 'SELF_DESTRUCT', 'MISTY_EXPLOSION'],
    'items stelen of ruilen (items zijn je relics)': [
        'TRICK', 'SWITCHEROO', 'COVET', 'THIEF', 'KNOCK_OFF', 'INCINERATE', 'CORROSIVE_GAS'],
    'objectief slechter dan een andere move (Jordi)': [
        'BUBBLE', 'POUND', 'SCRATCH', 'CONSTRICT', 'POWDER_SNOW'],
}
BANNED_SET = {m for lst in BANNED.values() for m in lst if m in MOVES}
for _lst in BANNED.values():
    for _m in _lst:
        if _m not in MOVES:
            print('waarschuwing: onbekende move', _m, file=sys.stderr)

# 'Kale' schadeffecten: alleen deze worden op dominantie vergeleken.
PLAIN_EFFECTS = {'HIT'}


def is_damaging(m):
    return m['cat'] != 'STATUS' and m['power'] > 1


def dominated_by(a, b):
    """Is move a objectief slechter dan move b? (zelfde type, categorie, doelwit en prioriteit; b minstens
    even sterk en accuraat; a heeft geen bijeffect dat b niet heeft)."""
    A, B = MOVES[a], MOVES[b]
    if a == b or not (is_damaging(A) and is_damaging(B)):
        return False
    if A['effect'] not in PLAIN_EFFECTS or B['effect'] not in PLAIN_EFFECTS:
        return False
    if (A['type'], A['cat'], A['target'], A['priority'], A['strikes']) != (B['type'], B['cat'], B['target'], B['priority'], B['strikes']):
        return False
    if A['charge'] != B['charge'] or B['charge'] or B['recharge'] or B['recoil'] > A['recoil']:
        return False
    if set(A['add']) - set(B['add']):
        return False
    if A['contact'] is False and B['contact'] is True:
        return False  # contact kan nadelig zijn (Rocky Helmet, Static)
    acc_a, acc_b = A['acc'] or 101, B['acc'] or 101
    if B['power'] > A['power'] + 20 or B['pp'] < A['pp']:
        return False  # een andere krachtklasse of minder PP is een afweging, geen 'objectief beter'
    return B['power'] >= A['power'] and acc_b >= acc_a and (B['power'] > A['power'] or acc_b > acc_a)


def compute_dominated():
    out = {}
    names = [n for n, m in MOVES.items() if is_damaging(m) and n not in BANNED_SET and not m['zmove']]
    common = [n for n in names if learner_count(n) >= 5]
    for a in names:
        for b in common:
            if dominated_by(a, b):
                out[a] = b
                break
    return out


_LEARNERS = {}


def learner_count(move):
    if not _LEARNERS:
        for s in SPECIES.values():
            ms = {m for _, m in s['levelup']} | set(s['teach']) | set(s['egg'])
            for m in ms:
                _LEARNERS[m] = _LEARNERS.get(m, 0) + 1
    return _LEARNERS.get(move, 0)


_LEVELUP_LEARNERS = {}


def levelup_learners(move):
    if not _LEVELUP_LEARNERS:
        for s in SPECIES.values():
            for m in {m for _, m in s['levelup']}:
                _LEVELUP_LEARNERS[m] = _LEVELUP_LEARNERS.get(m, 0) + 1
    return _LEVELUP_LEARNERS.get(move, 0)


# ---------------------------------------------------------------------------------------------
# 2. Stats en rating

def stat(base, hp=False):
    x = (2 * base + IV + EV // 4) * LEVEL // 100
    return x + LEVEL + 10 if hp else x + 5


ABILITY_FACTOR = {
    'HUGE_POWER': 1.6, 'PURE_POWER': 1.6, 'TRUANT': 0.5, 'SLOW_START': 0.55, 'DEFEATIST': 0.8,
    'WONDER_GUARD': 0.3, 'STALL': 0.9, 'KLUTZ': 0.95, 'SPEED_BOOST': 1.15, 'MOXIE': 1.08, 'INTIMIDATE': 1.08,
    'TECHNICIAN': 1.08, 'ADAPTABILITY': 1.15, 'TOUGH_CLAWS': 1.1, 'STRONG_JAW': 1.08, 'IRON_FIST': 1.05,
    'SHEER_FORCE': 1.1, 'GUTS': 1.05, 'REGENERATOR': 1.0, 'MULTISCALE': 1.08, 'SAND_STREAM': 1.05,
    'DROUGHT': 1.08, 'DRIZZLE': 1.08, 'LEVITATE': 1.05, 'FLUFFY': 1.05, 'FUR_COAT': 1.15, 'ICE_SCALES': 1.1,
    'GOOD_AS_GOLD': 1.05, 'PRANKSTER': 1.05, 'SKILL_LINK': 1.08, 'COMATOSE': 1.05, 'BEAST_BOOST': 1.05,
}


def ability_factor(sp):
    abil = [a for a in sp['abilities'][:2] if a and a != 'NONE'] or ['NONE']
    return sum(ABILITY_FACTOR.get(a, 1.0) for a in abil) / len(abil)


FOE_SPEED = stat(75)  # gemiddelde tegenstander


def rating_raw(name):
    s = SPECIES[name]
    atk, spa = stat(s['atk']), stat(s['spa'])
    hp, df, sd = stat(s['hp'], True), stat(s['def']), stat(s['spd'])
    off = max(atk, spa) * 1.5
    bulk = hp * 2 * df * sd / (df + sd)
    spe = stat(s['spe'])
    speed = 1 + 0.25 / (1 + math.exp(-(spe - FOE_SPEED) / 12.0))
    # aanval telt iets zwaarder dan bulk: vijanden hebben x HP (elites, bazen), passief spelen wordt afgestraft
    return off ** 0.55 * bulk ** 0.45 * speed * ability_factor(s)


# ---------------------------------------------------------------------------------------------
# 3. Lijnen: eerste vorm, evoluties per act

EXCLUDE_FLAGS = ('isLegendary', 'isMythical', 'isUltraBeast', 'isParadox', 'isMegaEvolution', 'isGigantamax',
                 'isTotem', 'isPrimalReversion', 'isTeraForm', 'isUltraBurst')
REGIONAL = ('isAlolanForm', 'isGalarianForm', 'isHisuianForm', 'isPaldeanForm')
# vormen die niet als losse rental bedoeld zijn
SKIP_SUFFIX = ('_GMAX', '_MEGA', '_TOTEM', '_COSPLAY', '_CAP', '_STARTER', '_PARTNER', '_BATTLE_BOND',
               '_ZEN', '_BUSTED', '_SCHOOL', '_COMPLETE', '_ETERNAMAX', '_PRIMAL', '_ORIGIN', '_THERIAN',
               '_CROWNED', '_HANGRY', '_NOICE', '_GULPING', '_GORGING', '_BLADE', '_PIROUETTE', '_DUSK_MANE',
               '_DAWN_WINGS', '_ULTRA', '_RESOLUTE', '_PALDEA_BLAZE', '_PALDEA_AQUA', '_ROAMING', '_HERO',
               '_STELLAR', '_TERASTAL', '_FAMILY_OF_THREE', '_THREE_SEGMENT', '_CORE', '_METEOR', '_SUNNY',
               '_RAINY', '_SNOWY', '_ATTACK', '_DEFENSE', '_SPEED', '_PRIMAL', '_SUNSHINE', '_OVERCAST', '_FAN',
               '_FROST', '_HEAT', '_MOW', '_WASH', '_SKY', '_ZERO', '_DROOPY', '_STRETCHY', '_ROCK_STAR',
               '_BELLE', '_POP_STAR', '_PHD', '_LIBRE', '_SMALL', '_LARGE', '_SUPER', '_LOW_KEY')


def is_candidate_form(name):
    s = SPECIES.get(name)
    if not s or name in ('NONE', 'EGG') or any(s[f] for f in EXCLUDE_FLAGS):
        return False
    if any(name.endswith(x) or (x + '_') in name for x in SKIP_SUFFIX):
        return False
    # andere vormen alleen als het een regionale vorm is
    if '_' in name and not any(s[f] for f in REGIONAL) and name not in ('MR_MIME', 'MIME_JR', 'MR_RIME',
                                                                        'TAPU_KOKO', 'PORYGON_Z', 'HO_OH',
                                                                        'JANGMO_O', 'HAKAMO_O', 'KOMMO_O',
                                                                        'TYPE_NULL', 'NIDORAN_F', 'NIDORAN_M',
                                                                        'FARFETCHD', 'SIRFETCHD', 'FLABEBE',
                                                                        'CHI_YU', 'TING_LU', 'CHIEN_PAO', 'WO_CHIEN'):
        return False
    return True


def is_baby(name):
    s = SPECIES[name]
    return 'NO_EGGS_DISCOVERED' in s['eggGroups'] and bool(s['evos']) and 'pre' not in s


def evo_targets(name):
    """Mogelijke evoluties voor de Spire: zelfde regio (geen regionale vorm uit een gewone basis en andersom),
    zonder dubbelen, max 3 (eerste drie, de rest willekeurig in de game)."""
    s = SPECIES[name]
    regional = any(s[f] for f in REGIONAL)
    out = []
    for e in s['evos']:
        t = e['target']
        if t not in SPECIES or t in out or not is_candidate_form(t):
            continue
        t_regional = any(SPECIES[t][f] for f in REGIONAL)
        if t_regional != regional and 'MAPSEC' in e.get('condtext', ''):
            continue
        out.append(t)
    return out


def line_forms(base):
    """Vorm per act (1-3) en het totaal aantal stadia. Bij vertakkingen: de sterkste tak (de speler mag in
    de game kiezen)."""
    forms = [base]
    cur = base
    while len(forms) < 3:
        ts = evo_targets(cur)
        if not ts:
            break
        cur = max(ts, key=rating_raw)
        forms.append(cur)
    stages = len(forms)
    while len(forms) < 3:
        forms.append(forms[-1])
    return forms, stages


def base_forms():
    out = []
    for name, s in SPECIES.items():
        if not is_candidate_form(name):
            continue
        pre = s.get('pre')
        if pre and is_candidate_form(pre) and not is_baby(pre):
            continue  # geen eerste vorm
        if is_baby(name):
            continue  # baby's doen niet mee; de lijn begint bij de volgende vorm
        out.append(name)
    return sorted(out)


# ---------------------------------------------------------------------------------------------
# 4. Startkit

def line_learnset(forms, include_teach=True):
    """move -> (bron, level). Bron 0 = level-up van de eerste vorm, 1 = level-up van de lijn, 2 = ei, 3 = TM/tutor."""
    out = {}
    for i, f in enumerate(dict.fromkeys(forms)):
        s = SPECIES[f]
        for lv, m in s['levelup']:
            src = 0 if i == 0 else 1
            if m not in out or (src, lv) < out[m]:
                out[m] = (src, lv)
        for m in s['egg']:
            out.setdefault(m, (2, 0))
        if include_teach:
            for m in s['teach']:
                out.setdefault(m, (3, 0))
    # eimoves staan alleen bij de eerste vorm van de lijn, dus ook bij de baby
    pre = SPECIES[forms[0]].get('pre')
    if pre:
        for m in SPECIES[pre]['egg']:
            out.setdefault(m, (2, 0))
        for lv, m in SPECIES[pre]['levelup']:
            out.setdefault(m, (1, lv))
    return out


def attack_category(forms):
    # gewogen over de drie acts
    atk = sum(stat(SPECIES[f]['atk']) for f in forms)
    spa = sum(stat(SPECIES[f]['spa']) for f in forms)
    return ('PHYSICAL' if atk >= spa else 'SPECIAL'), atk / spa


def stab_candidates(t, cat, lo=40, hi=50):
    out = []
    for n, m in MOVES.items():
        if m['type'] != t or m['cat'] != cat or not (lo <= m['power'] <= hi) or n in BANNED_SET:
            continue
        if m['zmove'] or m['charge'] or m['recharge'] or (m['acc'] and m['acc'] < 85) or m['strikes'] > 1:
            continue
        if m['effect'] not in ('HIT', 'ABSORB', 'FLINCH_HIT', 'RAPID_SPIN', 'FAKE_OUT', 'NONE') and not m['add'] \
                and m['effect'] not in ('HIT_ESCAPE',):
            # rare effecten (Round, Echoed Voice, Pursuit, ...) liever niet als vaste starter
            continue
        if m['effect'] in ('FAKE_OUT', 'FIRST_TURN_ONLY', 'SNORE', 'DREAM_EATER', 'LAST_RESORT', 'SUCKER_PUNCH', 'FOCUS_PUNCH',
                           'BELCH', 'SYNCHRONOISE', 'UPPER_HAND', 'FIRST_IMPRESSION', 'FLING', 'POWER_TRIP',
                           'STORED_POWER', 'RETURN', 'FRUSTRATION', 'ROUND', 'ECHOED_VOICE', 'FURY_CUTTER',
                           'ROLLOUT', 'PURSUIT', 'PAYBACK', 'REVENGE', 'ASSURANCE', 'RAGE'):
            continue
        out.append(n)
    return out


def pick_stab(t, cat, learn, dominated):
    best, best_score = None, None
    other = 'SPECIAL' if cat == 'PHYSICAL' else 'PHYSICAL'
    for c, lo, hi in ((cat, 40, 50), (cat, 35, 60), (cat, 30, 70), (other, 40, 50), (other, 35, 60)):
        for n in stab_candidates(t, c, lo, hi):
            m = MOVES[n]
            src = learn.get(n, (4, 0))[0]          # 4 = algemene typemove, past niet in de leerset
            score = (src, n in dominated, abs(m['power'] - 45) // 5, -(m['priority'] > 0),
                     -len(m['add']), learn.get(n, (4, 99))[1], n)
            if best_score is None or score < best_score:
                best, best_score = n, score
        if best:
            return best, best_score[0]
    return None, None


# Basis-statusmoves (slot 3): (soort effect, sterkte)
BASIC_STATUS = {
    'GROWL': ('atk_down_both', 1), 'TAIL_WHIP': ('def_down_both', 1), 'LEER': ('def_down_both', 1),
    'SAND_ATTACK': ('acc_down_one', 1), 'SMOKESCREEN': ('acc_down_one', 1), 'FLASH': ('acc_down_one', 1),
    'KINESIS': ('acc_down_one', 1), 'STRING_SHOT': ('spe_down_both', 2), 'SCARY_FACE': ('spe_down_one', 2),
    'COTTON_SPORE': ('spe_down_both', 2), 'CHARM': ('atk_down_one', 2), 'BABY_DOLL_EYES': ('atk_down_one_prio', 1),
    'FEATHER_DANCE': ('atk_down_one', 2), 'CONFIDE': ('spa_down_one', 1), 'NOBLE_ROAR': ('atkspa_down_one', 1),
    'TICKLE': ('atkdef_down_one', 1), 'FAKE_TEARS': ('spd_down_one', 2), 'METAL_SOUND': ('spd_down_one', 2),
    'SCREECH': ('def_down_one', 2), 'DEFENSE_CURL': ('def_up_self', 1), 'HARDEN': ('def_up_self', 1),
    'WITHDRAW': ('def_up_self', 1), 'HOWL': ('atk_up_both', 1), 'WORK_UP': ('atkspa_up_self', 1),
    'GROWTH': ('atkspa_up_self', 1), 'DOUBLE_TEAM': ('eva_up_self', 1), 'MINIMIZE': ('eva_up_self', 2),
    'SWEET_KISS': ('confuse_one', 1), 'SUPERSONIC': ('confuse_one', 1), 'MEDITATE': ('atk_up_self', 1),
    'SHARPEN': ('atk_up_self', 1), 'FOCUS_ENERGY': ('crit_up_self', 2), 'AGILITY': ('spe_up_self', 2),
    'CHARGE': ('spd_up_self', 1), 'AMNESIA': ('spd_up_self', 2), 'BARRIER': ('def_up_self', 2),
    'ACID_ARMOR': ('def_up_self', 2), 'IRON_DEFENSE': ('def_up_self', 2), 'COSMIC_POWER': ('defspd_up_self', 1),
    'DEFEND_ORDER': ('defspd_up_self', 1), 'AROMATIC_MIST': ('spd_up_ally', 1), 'LEER_': None,
}
BASIC_STATUS = {k: v for k, v in BASIC_STATUS.items() if v and k in MOVES}

# Gevechtsmodel (uit balance.py): beurten per gevecht, aandeel gevechten
FIGHTS = [  # (naam, beurten T, gewicht, aantal vijanden)
    ('normaal', 3, 0.60, 2),
    ('elite', 5, 0.25, 2),
    ('baas', 11, 0.15, 2),
]


def status_value(kind, strength, cat, speed_rel, phys_share_foes=0.5):
    """Verwachte winst van één statusmove in de eerste beurt, in 'beurten schade van de vijand' (H = 1).
    Kosten: één aanval minder = het gevecht duurt een halve beurt langer (twee aanvallers) = 0,5 H.
    cat = aanvalscategorie van de gebruiker; partner onbekend (50/50)."""
    own_phys = 1.0 if cat == 'PHYSICAL' else 0.0
    team_phys = (own_phys + 0.5) / 2           # aandeel fysieke schade van het team
    total = 0.0
    for _, T, w, _n in FIGHTS:
        rest = T - 1
        red = 0.0      # minder binnenkomende schade (fractie)
        gain = 0.0     # meer uitgaande schade (fractie)
        stage = {1: 1 / 3, 2: 1 / 2}               # -1 = x2/3, -2 = x1/2
        boost = {1: 0.5, 2: 1.0}
        if kind == 'atk_down_both':
            red = phys_share_foes * stage[strength]
        elif kind in ('atk_down_one', 'atk_down_one_prio'):
            red = 0.5 * phys_share_foes * stage[strength]
        elif kind == 'spa_down_one':
            red = 0.5 * (1 - phys_share_foes) * stage[strength]
        elif kind == 'atkspa_down_one':
            red = 0.5 * stage[strength]
        elif kind == 'atkdef_down_one':
            red = 0.5 * phys_share_foes * stage[strength]
            gain = 0.5 * team_phys * boost[strength]
        elif kind == 'def_down_both':
            gain = team_phys * boost[strength]
        elif kind == 'def_down_one':
            gain = 0.5 * team_phys * boost[strength]
        elif kind == 'spd_down_one':
            gain = 0.5 * (1 - team_phys) * boost[strength]
        elif kind == 'acc_down_one':
            red = 0.5 * 0.25 * (strength)
        elif kind == 'eva_up_self':
            red = 0.5 * 0.25 * strength
        elif kind == 'confuse_one':
            red = 0.5 * 0.33 * 0.75 * 0.75     # 33% raakt zichzelf, ~2-5 beurten, 75% accuraat
        elif kind == 'def_up_self':
            red = 0.5 * phys_share_foes * stage[strength]
        elif kind == 'defspd_up_self':
            red = 0.5 * stage[strength]
        elif kind == 'spd_up_self':
            red = 0.5 * (1 - phys_share_foes) * stage[strength]
        elif kind == 'spd_up_ally':
            red = 0.5 * (1 - phys_share_foes) * stage[strength]
        elif kind == 'atk_up_self':
            gain = 0.5 * own_phys * boost[strength]
        elif kind == 'atk_up_both':
            gain = team_phys * boost[strength]
        elif kind == 'atkspa_up_self':
            gain = 0.5 * boost[strength]
        elif kind == 'crit_up_self':
            gain = 0.5 * (1 / 8 - 1 / 24) * 0.5     # +2 stages: 1/24 -> 1/2 in gen 7+? (vereenvoudigd)
            gain = 0.5 * 0.45 * 0.5
        elif kind in ('spe_down_both', 'spe_down_one', 'spe_up_self'):
            # sneller zijn: in de laatste beurt sla je eerst; waarde ~ kans dat de volgorde omdraait
            flip = 1 / (1 + math.exp(speed_rel / 10.0))
            red = (0.5 if kind == 'spe_down_both' else 0.25) * flip * (1.0 / max(rest, 1))
        # winst: minder schade over de resterende beurten; meer schade = korter gevecht
        saved = red * rest + rest * (1 - 1 / (1 + gain))
        total += w * (saved - 0.5)
    return total


def pick_status(forms, learn, cat):
    s = SPECIES[forms[0]]
    speed_rel = stat(s['spe']) - FOE_SPEED
    # eerst de echte basismoves (sterkte 1, zoals Growl en Tail Whip); alleen als die er niet zijn sterkte 2.
    # Ontwijken (Double Team, Minimize) niet: dat is geluk, geen keuze.
    for max_strength in (1, 2):
        cands = []
        for n, (kind, strength) in BASIC_STATUS.items():
            if kind == 'eva_up_self' or strength > max_strength:
                continue
            if n in learn and learn[n][0] <= 2 and n not in BANNED_SET:
                v = status_value(kind, strength, cat, speed_rel)
                cands.append((round(v, 3), -learn[n][0], n))
        if cands:
            cands.sort(reverse=True)
            return cands
    return []


# 'Grounded' moves: wat de soort typeert. (sterkte 1-5; > 3 te sterk als startmove)
GROUNDED = {
    'LEECH_SEED': 3, 'SING': 3, 'THUNDER_WAVE': 3, 'SYNTHESIS': 3, 'MOONLIGHT': 3, 'MORNING_SUN': 3,
    'STUN_SPORE': 3, 'POISON_POWDER': 2, 'SLEEP_POWDER': 4, 'SPORE': 5, 'HYPNOSIS': 3, 'LOVELY_KISS': 4,
    'GRASS_WHISTLE': 3, 'YAWN': 3, 'CONFUSE_RAY': 3, 'SUPERSONIC': 2, 'SWEET_KISS': 2, 'WILL_O_WISP': 3,
    'TOXIC': 3, 'GLARE': 4, 'POISON_GAS': 2, 'RECOVER': 4, 'SOFT_BOILED': 4, 'MILK_DRINK': 4, 'SLACK_OFF': 4,
    'ROOST': 3, 'REST': 2, 'WISH': 3, 'AQUA_RING': 2, 'INGRAIN': 2, 'HELPING_HAND': 2, 'FOLLOW_ME': 3,
    'RAGE_POWDER': 3, 'ENCORE': 3, 'TAUNT': 3, 'DISABLE': 2, 'TORMENT': 1, 'RAIN_DANCE': 2, 'SUNNY_DAY': 2,
    'SANDSTORM': 2, 'HAIL': 2, 'SNOWSCAPE': 2, 'PROTECT': 2, 'DETECT': 2, 'ENDURE': 1, 'SUBSTITUTE': 3,
    'REFLECT': 3, 'LIGHT_SCREEN': 3, 'SAFEGUARD': 2, 'MIST': 1, 'HAZE': 2, 'WIDE_GUARD': 2, 'QUICK_GUARD': 2,
    'TAILWIND': 3, 'TRICK_ROOM': 4, 'STOCKPILE': 2, 'SWALLOW': 2, 'BELLY_DRUM': 5, 'SWORDS_DANCE': 4,
    'NASTY_PLOT': 4, 'CALM_MIND': 4, 'BULK_UP': 4, 'DRAGON_DANCE': 5, 'CURSE': 3, 'LEER': 1, 'SPIKY_SHIELD': 2,
    'KINGS_SHIELD': 3, 'BANEFUL_BUNKER': 3, 'MAGIC_COAT': 2, 'HEAL_BELL': 2, 'AROMATHERAPY': 2,
    'LIFE_DEW': 2, 'HEAL_PULSE': 2, 'FLORAL_HEALING': 2, 'POLLEN_PUFF': 2, 'AFTER_YOU': 1, 'ALLY_SWITCH': 2,
    'ACUPRESSURE': 2, 'COIL': 4, 'HONE_CLAWS': 3, 'STRENGTH_SAP': 4, 'SPIKY_SHIELD_': 0, 'PSYCH_UP': 2,
    'MIRROR_COAT': 2, 'COUNTER': 2, 'DESTINY_BOND': 3, 'PERISH_SONG': 2, 'METRONOME': 2, 'TRANSFORM': 3,
    'SWAGGER': 2, 'FLATTER': 2, 'ATTRACT_': 0, 'CHARGE': 1, 'MAGNET_RISE_': 0, 'TAR_SHOT': 2, 'SOAK': 2,
    'ENTRAINMENT': 2, 'WORRY_SEED': 2, 'SIMPLE_BEAM': 2, 'GASTRO_ACID': 2, 'SKILL_SWAP': 2, 'ROLE_PLAY': 2,
    'POWER_SPLIT': 2, 'GUARD_SPLIT': 2, 'SPEED_SWAP': 2, 'TEETER_DANCE': 3, 'HOWL': 1, 'FAKE_OUT': 3,
    'RAPID_SPIN': 1, 'NUZZLE': 3, 'MORTAL_SPIN': 2, 'INFESTATION': 2, 'WHIRLPOOL': 2, 'FIRE_SPIN': 2,
    'SAND_TOMB': 2, 'WRAP': 1, 'BIND': 1, 'CLAMP': 2, 'LEECH_LIFE': 2, 'ABSORB': 1, 'MEGA_DRAIN': 2,
    'DRAINING_KISS': 2, 'PARABOLIC_CHARGE': 2, 'ICY_WIND': 2, 'ELECTROWEB': 2, 'MUD_SHOT': 2, 'SNARL': 2,
    'STRUGGLE_BUG': 1, 'LUNGE': 2, 'TRAILBLAZE': 2, 'BULLDOZE': 2, 'ROCK_TOMB': 2, 'MUD_SLAP': 1,
    'BABY_DOLL_EYES_': 0, 'SHORE_UP': 4, 'PURIFY': 2, 'GEAR_UP': 2, 'MAGNETIC_FLUX': 2, 'DECORATE': 2,
    'COACHING': 2, 'JUNGLE_HEALING': 3, 'LUNAR_BLESSING': 3, 'CHILLY_RECEPTION_': 0, 'GRASSY_TERRAIN': 2,
    'MISTY_TERRAIN': 2, 'ELECTRIC_TERRAIN': 2, 'PSYCHIC_TERRAIN': 2, 'STUFF_CHEEKS': 2, 'TEATIME': 2,
    'OCTOLOCK': 2, 'NO_RETREAT': 4, 'JAW_LOCK': 2, 'FLOWER_SHIELD': 1, 'ROTOTILLER': 2, 'SPICY_EXTRACT': 2,
    'TIDY_UP': 4, 'TOPSY_TURVY': 2, 'VENOM_DRENCH': 2, 'TOXIC_THREAD': 2, 'MEMENTO_': 0, 'POWDER': 1,
    'STEALTH_ROCK_': 0, 'HEART_SWAP': 2, 'AUTOTOMIZE': 3, 'SHIFT_GEAR': 4, 'QUIVER_DANCE': 5, 'SHELL_SMASH': 5,
    'VICTORY_DANCE': 5, 'FILLET_AWAY': 4, 'CLANGOROUS_SOUL': 4, 'GEOMANCY': 5, 'DRAGON_CHEER': 2,
    'FUNGAL_CONTROL': 3, 'TRANSMUTATION': 3, 'MACHINE_LEARNING': 3, 'ACID_RAIN': 3, 'POLLEN_HAZE': 3,
    'COTTON_GUARD': 4, 'MAT_BLOCK': 2, 'CRAFTY_SHIELD': 1, 'IRON_DEFENSE': 3, 'ACID_ARMOR': 3,
    'BARRIER': 3, 'AMNESIA': 3, 'AGILITY': 3, 'ROCK_POLISH': 3,
    'LASER_FOCUS': 2, 'FOCUS_ENERGY': 2, 'COSMIC_POWER': 3, 'DEFEND_ORDER': 3, 'HEAL_ORDER': 4,
    'TICKLE': 1, 'CHARM': 2, 'FEATHER_DANCE': 2, 'SCARY_FACE': 2, 'STRING_SHOT': 2, 'COTTON_SPORE': 2,
    'SPITE_': 0, 'SPIDER_WEB_': 0, 'BEAT_UP': 2,
}
GROUNDED = {k: v for k, v in GROUNDED.items() if v and k in MOVES and k not in BANNED_SET}

# Jordi's voorbeelden en handmatige keuzes
GROUNDED_OVERRIDE = {
    'BULBASAUR': 'LEECH_SEED', 'PIKACHU': 'THUNDER_WAVE', 'JIGGLYPUFF': 'SING', 'ODDISH': 'MOONLIGHT',
}


def pick_grounded(base, forms, learn, avoid, cands_out=None):
    if base in GROUNDED_OVERRIDE and GROUNDED_OVERRIDE[base] in learn:
        return GROUNDED_OVERRIDE[base]
    types = set()
    for f in forms:
        types |= set(SPECIES[f]['types'])
    best, best_score = None, None
    for n, strength in GROUNDED.items():
        if n not in learn or n in avoid or strength > 3:
            continue
        src, lv = learn[n]
        if src > 2:
            continue  # alleen level-up en ei: wat de soort uit zichzelf doet
        m = MOVES[n]
        uniq = 1.0 / math.sqrt(max(1, levelup_learners(n)))
        # level-up telt zwaar (dat doet de soort uit zichzelf), eimoves alleen als er niets anders is
        score = (2.0 * uniq + (1.0 if m['type'] in types else 0) + (0.3 if m['cat'] == 'STATUS' else 0)
                 - (1.5 if src == 2 else 0.15 * src) + (0.3 if lv and lv <= 25 else 0) + 0.1 * strength)
        if cands_out is not None:
            cands_out.append((round(score, 3), n))
        if best_score is None or score > best_score:
            best, best_score = n, score
    return best


# ---------------------------------------------------------------------------------------------
# 5. Analyse

def analyse():
    dominated = compute_dominated()
    bases = base_forms()
    rows = []
    for b in bases:
        forms, stages = line_forms(b)
        r = [rating_raw(f) for f in forms]
        rows.append(dict(base=b, forms=forms, stages=stages, r=r))
    # normaliseren: 100 = mediaan van de eindvormen
    finals = [x['r'][2] for x in rows]
    med = statistics.median(finals)
    for x in rows:
        x['R'] = [v * 100 / med for v in x['r']]
    # drempels per act: een vorm moet in elke act kunnen meedoen (75% van de mediaan van die act)
    act_med = [statistics.median(x['R'][a] for x in rows if x['stages'] >= 2) for a in range(3)]
    T = [0.75 * m for m in act_med]
    # runwaarde: sterkte t.o.v. de act (act 3 telt zwaarder: de bazen zijn daar het zwaarst)
    for x in rows:
        x['V'] = 100 * sum(w * x['R'][a] / act_med[a] for a, w in enumerate(ACT_WEIGHT))
    # zonder evolutie: minstens zo sterk als een gemiddelde act-2-vorm (nu sterk, nooit beter = een afweging)
    single_min = act_med[1]
    # en hooguit 5% boven de mediaan van act 3: in act 1 zijn ze al bijna 2x zo sterk als een eerste vorm,
    # dus sterkere eenstaps-soorten (Heracross, Gholdengo, ...) breken act 1. Die komen alleen via events.
    single_max = act_med[2] * 1.05
    v_all = sorted(x['V'] for x in rows)
    # Een te zwakke eerste vorm sluit de lijn niet uit (Jordi): de lijn begint dan een stap later
    # (Magikarp -> Gyarados, Caterpie -> Butterfree). Zelfde drempels, dus het blijft eerlijk.
    queue = list(rows)
    seen = {x['base'] for x in rows}
    while queue:
        x = queue.pop(0)
        evaluate(x, T, act_med, med, single_min, single_max, dominated)
        early = [r for r in x['reasons'] if r.startswith('act 1') or r.startswith('act 2')]
        if early and x['stages'] >= 2:
            for t in evo_targets(x['base']):
                if t in seen:
                    continue
                seen.add(t)
                forms, stages = line_forms(t)
                y = dict(base=t, forms=forms, stages=stages, r=[rating_raw(f) for f in forms], later=x['base'])
                y['R'] = [v * 100 / med for v in y['r']]
                y['V'] = 100 * sum(w * y['R'][a] / act_med[a] for a, w in enumerate(ACT_WEIGHT))
                rows.append(y)
                queue.append(y)
    ok = [x for x in rows if x['ok'] and not x.get('eventOnly')]
    events = [x for x in rows if x['ok'] and x.get('eventOnly')]
    vs = sorted(x['V'] for x in ok)
    q = lambda p: vs[int(len(vs) * p)]
    cut = (q(0.30), q(0.60), q(0.85))
    for x in ok:
        x['tier'] = 0 if x['V'] < cut[0] else 1 if x['V'] < cut[1] else 2 if x['V'] < cut[2] else 3
    return dict(rows=rows, ok=ok, events=events, single_max=single_max, T=T, single_min=single_min, act_med=act_med, cut=cut, dominated=dominated, med=med)


def evaluate(x, T, act_med, med, single_min, single_max, dominated):
    if True:
        reasons = []
        for a in range(3):
            if x['R'][a] < T[a]:
                reasons.append('act %d te zwak (%s %.0f < %.0f)' % (a + 1, x['forms'][a], x['R'][a], T[a]))
        if x['stages'] == 1:
            if x['R'][0] > single_max:
                x['eventOnly'] = True   # te sterk voor de draft: alleen via events (met een prijs)
            if x['R'][0] < single_min and x.get('later') and x['R'][2] >= T[2]:
                # later begonnen eindvorm (Butterfree): rekenkundig gelijk aan Luvdisc, dus niet in de draft,
                # maar wel beschikbaar via events
                x['eventOnly'] = True
            elif x['R'][0] < single_min:
                reasons.append('geen evolutie en zwakker dan een gemiddelde act-2-vorm (%.0f < %.0f)' % (x['R'][0], single_min))
        learn = line_learnset(x['forms'])
        cat, ratio = attack_category(x['forms'])
        x['cat'] = cat
        stabs = []
        for t in dict.fromkeys(SPECIES[x['base']]['types']):
            mv, src = pick_stab(t, cat, learn, dominated)
            if mv is None:
                reasons.append('geen STAB-move %s %s' % (t, cat))
            stabs.append((mv, src))
        x['stabs'] = stabs
        sc = pick_status(x['forms'], learn, cat)
        x['statusCands'] = sc
        x['status'] = sc[0][2] if sc else None
        if not x['status']:
            reasons.append('geen basis-statusmove')
        x['groundedCands'] = []
        x['grounded'] = pick_grounded(x['base'], x['forms'], learn, {x['status']} | {m for m, _ in stabs}, x['groundedCands'])
        if not x['grounded']:
            reasons.append('geen grounded move')
        x['reasons'] = reasons
        x['ok'] = not reasons


# ---------------------------------------------------------------------------------------------
# 6. Items: Life Orb, Leftovers, Focus Sash (met het gevechtsmodel)

TAKEN = {'normaal': 0.15, 'elite': 0.25, 'baas': 0.65}   # HP-verlies per gevecht (fractie van max HP)


def item_math():
    out = []
    boost = 1.3
    rows = []
    for name, T, w, _ in FIGHTS:
        taken = TAKEN[name]
        saved = 2 * taken * (1 - 1 / (1 + (boost - 1) / 2))    # team, in HP van één Pokémon
        attacks = T                                               # aanvallen van de drager
        rows.append((name, T, taken, saved, saved / attacks))
    be = sum(w * r[4] for r, (_, _, w, _) in zip(rows, FIGHTS))
    out.append(('Life Orb', rows, be))
    return out


# ---------------------------------------------------------------------------------------------
# 7. Beloningsmoves per zeldzaamheid

STATUS_RARITY = {
    0: ['PROTECT', 'DETECT', 'HELPING_HAND', 'LEER', 'GROWL', 'HARDEN', 'WORK_UP', 'SCARY_FACE', 'CHARM',
        'FAKE_TEARS', 'METAL_SOUND', 'SANDSTORM', 'RAIN_DANCE', 'SUNNY_DAY', 'SNOWSCAPE', 'SAFEGUARD',
        'HOWL', 'CONFUSE_RAY', 'SUPERSONIC', 'POISON_POWDER', 'AQUA_RING', 'INGRAIN', 'MIST', 'ENDURE',
        'FOCUS_ENERGY', 'AFTER_YOU', 'QUICK_GUARD', 'STOCKPILE', 'AGILITY', 'ROCK_POLISH', 'IRON_DEFENSE',
        'AMNESIA', 'ACID_ARMOR', 'BARRIER', 'HONE_CLAWS', 'LASER_FOCUS'],
    1: ['THUNDER_WAVE', 'WILL_O_WISP', 'TOXIC', 'STUN_SPORE', 'YAWN', 'ENCORE', 'TAUNT', 'REFLECT',
        'LIGHT_SCREEN', 'TAILWIND', 'WIDE_GUARD', 'FOLLOW_ME', 'RAGE_POWDER', 'LEECH_SEED', 'SUBSTITUTE',
        'WISH', 'ROOST', 'SYNTHESIS', 'MOONLIGHT', 'MORNING_SUN', 'CALM_MIND', 'BULK_UP', 'HYPNOSIS',
        'SING', 'GRASS_WHISTLE', 'DISABLE', 'HAZE', 'COSMIC_POWER', 'CURSE', 'TICKLE', 'NOBLE_ROAR',
        'HEAL_PULSE', 'LIFE_DEW', 'COACHING', 'DECORATE', 'GRASSY_TERRAIN', 'MISTY_TERRAIN',
        'ELECTRIC_TERRAIN', 'PSYCHIC_TERRAIN', 'TAR_SHOT', 'SOAK', 'DEFOG_', 'SPIKY_SHIELD', 'KINGS_SHIELD',
        'BANEFUL_BUNKER', 'COIL', 'HEAL_BELL', 'AROMATHERAPY', 'DESTINY_BOND', 'SWAGGER', 'FLATTER',
        'POWER_SPLIT', 'GUARD_SPLIT', 'TOPSY_TURVY', 'ACUPRESSURE', 'STRENGTH_SAP_'],
    2: ['SWORDS_DANCE', 'NASTY_PLOT', 'DRAGON_DANCE', 'QUIVER_DANCE', 'SHELL_SMASH', 'SPORE', 'SLEEP_POWDER',
        'RECOVER', 'SOFT_BOILED', 'SLACK_OFF', 'MILK_DRINK', 'SHORE_UP', 'STRENGTH_SAP', 'TRICK_ROOM',
        'BELLY_DRUM', 'SHIFT_GEAR', 'VICTORY_DANCE', 'TIDY_UP', 'NO_RETREAT', 'CLANGOROUS_SOUL',
        'COTTON_GUARD', 'GLARE', 'LOVELY_KISS', 'AURORA_VEIL', 'JUNGLE_HEALING', 'LUNAR_BLESSING',
        'FILLET_AWAY', 'GEOMANCY_', 'HEAL_ORDER', 'DRAGON_CHEER', 'FUNGAL_CONTROL', 'TRANSMUTATION',
        'MACHINE_LEARNING', 'ACID_RAIN', 'POLLEN_HAZE'],
}

SKIP_DAMAGING_EFFECTS = {'FUTURE_SIGHT', 'FOCUS_PUNCH', 'SKY_DROP', 'SNORE', 'DREAM_EATER', 'LAST_RESORT',
                         'SPIT_UP', 'BELCH', 'FLING', 'NATURAL_GIFT', 'SYNCHRONOISE', 'STEEL_ROLLER',
                         'UPPER_HAND', 'POLTERGEIST', 'SUCKER_PUNCH_', 'HIT_SET_REMOVE_TERRAIN', 'BURN_UP',
                         'DOUBLE_SHOCK', 'AURA_WHEEL', 'HYPERSPACE_FURY', 'PLASMA_FISTS', 'SPECTRAL_THIEF',
                         'SPARKLY_SWIRL', 'RECHARGE', 'SEMI_INVULNERABLE', 'TWO_TURNS_ATTACK', 'SOLAR_BEAM',
                         'RAGE', 'ROLLOUT', 'FURY_CUTTER', 'ECHOED_VOICE', 'ROUND', 'ICE_BALL', 'UPROAR',
                         'MIND_BLOWN', 'STEEL_BEAM', 'SHELL_TRAP', 'BEAK_BLAST', 'DOUBLE_IRON_BASH'}


def damaging_score(n):
    m = MOVES[n]
    acc = (m['acc'] or 100) / 100
    p = m['power'] * m['strikes'] * acc
    if m['strikes'] > 1 and m['effect'] == 'MULTI_HIT':
        p = m['power'] * 3.1 * acc
    if m['target'] in ('BOTH', 'FOES_AND_ALLY'):
        p *= 1.25 if m['target'] == 'BOTH' else 1.1
    if m['priority'] > 0:
        p *= 1.3
    if m['drain']:
        p *= 1.15
    if m['recoil']:
        p *= 0.9
    for e in m['add']:
        if 'MINUS' in e and m['selfEffect']:
            p *= 0.92
    return p


def reward_pools(dominated):
    pools = {0: [], 1: [], 2: []}
    for n, m in MOVES.items():
        if n in BANNED_SET or m['zmove'] or n in dominated or m['signature']:
            continue
        if learner_count(n) < 8:
            continue
        if is_damaging(m):
            if m['effect'] in SKIP_DAMAGING_EFFECTS or m['charge'] or m['recharge'] or m['power'] < 50:
                continue
            s = damaging_score(n)
            r = 0 if s < 78 else 1 if s < 98 else 2
            pools[r].append(n)
    for r, lst in STATUS_RARITY.items():
        for n in lst:
            if n in MOVES and n not in BANNED_SET:
                pools[r].append(n)
    return {r: sorted(set(v)) for r, v in pools.items()}


# ---------------------------------------------------------------------------------------------
# uitvoer

TIER_NAMES = ['C', 'B', 'A', 'S']
ACT_WEIGHT = (0.3, 0.3, 0.4)


def write_header(res, pools):
    path = os.path.join(ROOT, 'src/data/spire_pool.h')
    L = ['// Gegenereerd door tools/grounded/spire/spire_pool.py - niet met de hand bewerken.', '',
         '// Rentals: eerste vorm, tier (0 C - 3 S), startmoves (STAB, [STAB], status, grounded).',
         'static const struct SpireRental sSpireRentals[] =', '{']
    for x in sorted(res['ok'], key=lambda x: (-x['tier'], x['base'])):
        mv = [m for m, _ in x['stabs']] + [x['status'], x['grounded']]
        mv += ['NONE'] * (4 - len(mv))
        L.append('    {SPECIES_%s, %d, {%s}},' % (x['base'], x['tier'], ', '.join('MOVE_' + m for m in mv)))
    L.append('};')
    L.append('')
    L.append('// Te sterk voor de draft (eenstaps, rating boven act 3): alleen via events, met een prijs.')
    L.append('static const struct SpireRental sSpireEventRentals[] =')
    L.append('{')
    for x in sorted(res['events'], key=lambda x: x['base']):
        mv = [m for m, _ in x['stabs']] + [x['status'], x['grounded']]
        mv += ['NONE'] * (4 - len(mv))
        L.append('    {SPECIES_%s, 3, {%s}},' % (x['base'], ', '.join('MOVE_' + m for m in mv)))
    L.append('};')
    L.append('')
    # evoluties (alle vormen in de pool)
    seen, evo = set(), []
    for x in res['ok'] + res['events']:
        cur = [x['base']]
        while cur:
            nxt = []
            for f in cur:
                if f in seen:
                    continue
                seen.add(f)
                ts = evo_targets(f)
                if ts:
                    evo.append((f, ts))
                    nxt += ts
            cur = nxt
    L.append('// Evoluties in de Spire (max 3 keuzes; bij meer dan één kiest de speler).')
    L.append('static const struct SpireEvolution sSpireEvolutions[] =')
    L.append('{')
    for f, ts in sorted(evo):
        ts = (ts + ['NONE'] * 3)[:3]
        L.append('    {SPECIES_%s, {%s}},' % (f, ', '.join('SPECIES_' + t for t in ts)))
    L.append('};')
    L.append('')
    banned = sorted(BANNED_SET, key=lambda n: list(MOVES).index(n))
    L.append('// Verboden moves (zie SPIRE_BALANS.md); tegenstanders krijgen ze niet, beloningen ook niet.')
    L.append('static const u16 sSpireBannedMoves[] =')
    L.append('{')
    for i in range(0, len(banned), 4):
        L.append('    ' + ' '.join('MOVE_%s,' % b for b in banned[i:i + 4]))
    L.append('};')
    L.append('')
    for r, name in ((0, 'Common'), (1, 'Uncommon'), (2, 'Rare')):
        lst = pools[r]
        L.append('static const u16 sSpire%sMoves[] =' % name)
        L.append('{')
        for i in range(0, len(lst), 4):
            L.append('    ' + ' '.join('MOVE_%s,' % b for b in lst[i:i + 4]))
        L.append('};')
        L.append('')
    with open(path, 'w') as f:
        f.write('\n'.join(L))
    return path


def fmt_moves(x):
    return ', '.join(MOVES[m]['name'] for m in [m for m, _ in x['stabs']] + [x['status'], x['grounded']] if m)


def write_report(res, pools):
    path = os.path.join(ROOT, 'SPIRE_BALANS.md')
    ok, rows = res['ok'], res['rows']
    L = ['# The Spire – rekenwerk (gegenereerd)', '',
         'Gemaakt met `tools/grounded/spire/spire_pool.py`; opnieuw draaien na wijzigingen in soorten of moves.', '',
         '## Model', '',
         '- **Rating** van een vorm op lv 50 (IV 31, EV 84):',
         '  `aanval^0,55 × bulk^0,45` (aanval iets zwaarder: vijanden hebben ×HP en passief spelen wordt afgestraft). Aanval = hoogste van Atk/SpA × 1,5 (STAB); bulk = HP × harmonisch gemiddelde van Def en SpD;',
         '  snelheid = 1 tot 1,25 (logistisch t.o.v. een base-75-tegenstander); ability-factor voor o.a. Huge Power ×1,6, Truant ×0,5.',
         '  **100 = mediaan van alle volledig geëvolueerde kandidaten** (%.0f ruw).' % res['med'],
         '- **Vorm per act**: act 1 = eerste vorm (baby\'s tellen niet), na elke baas één evolutie. Vertakkingen: de speler kiest; in de rating telt de sterkste tak.',
         '- **Runwaarde V** = gewogen gemiddelde van (rating / mediaan van die act) over de drie acts, 30/30/40% (act 3 zwaarder: daar zitten de zwaarste bazen). 100 = precies gemiddeld in elke act.',
         '- **Toelating**: in elke act minstens 75%% van de mediaan van die act (act 1: %.0f, act 2: %.0f, act 3: %.0f).' % tuple(res['T']),
         '  Soorten zonder evolutie alleen als ze minstens zo sterk zijn als een gemiddelde act-2-vorm (rating ≥ %.0f): dan is het een echte afweging (nu sterk, nooit beter).' % res['single_min'],
         '  En de startkit moet compleet zijn (STAB-aanval, statusmove, grounded move).',
         '- **Tiers** op V: C < %.0f ≤ B < %.0f ≤ A < %.0f ≤ S (30/30/25/15%%). Draft: C/B gewoon, A uncommon, S rare.' % res['cut'],
         '', '## Startkit', '',
         '- **STAB-aanval 40–50** per type van de eerste vorm; fysiek of speciaal naar de hoogste aanvalsstat over de drie acts.',
         '  Voorkeur: level-up van de eerste vorm > level-up van de lijn > eimove > TM > algemene typemove (bijv. Flame Charge voor een fysieke vuursoort).',
         '- **Statusmove**: de basismove uit de eigen leerset met de hoogste verwachtingswaarde in het gevechtsmodel',
         '  (60% gewone gevechten van 3 beurten, 25% elites van 5, 15% bazen van 11; een statusmove kost een halve beurt aan schade',
         '  en levert over de resterende beurten minder binnenkomende of meer uitgaande schade op).',
         '  Uitkomst in het kort: **Growl** (−1 Atk op beide) wint van Sand Attack/Double Team (één doel −25%%) zolang de helft van de vijanden fysiek is;',
         '  **Tail Whip/Leer** wint bij een fysieke aanvaller; alle statusmoves zijn netto negatief in gewone gevechten van 3 beurten en verdienen zich terug bij elites en bazen. Precies zoals Defend in Slay.',
         '- **Grounded move**: uit de eigen level-up/eimoves, iets wat de soort typeert (zeldzaam onder alle soorten, eigen type, vroeg geleerd), maximaal sterkte 3 (dus geen Spore, Sleep Powder, Swords Dance).',
         '  Vast: Bulbasaur Leech Seed, Pikachu Thunder Wave, Jigglypuff Sing, Oddish Moonlight.',
         '', '### Pikachu: Thunder Wave, Double Team of Growl?', '']
    pk = next((x for x in rows if x['base'] == 'PIKACHU'), None)
    if pk:
        L.append('Verwachtingswaarde (in beurten vijandelijke schade, + = winst) voor Pikachu als statusmove:')
        L.append('')
        for v, _, n in pk['statusCands'][:6]:
            L.append('- %s: %+.2f' % (MOVES[n]['name'], v))
        tw = status_value('acc_down_one', 1, 'SPECIAL', 0) + 0.0
        L.append('- Thunder Wave (verlamd: 25%% beurt kwijt + trager): ≈ %+.2f (plus snelheid); daarom de grounded move.' % tw)
        L.append('')
        L.append('Conclusie: **Growl** als statusmove, **Thunder Wave** als grounded move. Double Team wint niets van Growl en ontwijken is anti-fun (en tegen 2 vijanden raakt maar de helft van de aanvallen jou).')
    L += ['', '## Verboden moves', '']
    for reason, lst in BANNED.items():
        L.append('- **%s:** %s' % (reason, ', '.join(MOVES[m]['name'] for m in lst if m in MOVES)))
    L += ['', '## Later beginnen', '',
          'Is de eerste vorm in act 1 of 2 te zwak, dan begint de lijn een stap later (zelfde drempels):']
    for x in sorted([x for x in rows if x.get('later') and x['ok']], key=lambda x: x['base']):
        L.append('- %s in plaats van %s%s' % (SPECIES[x['base']]['dispname'], SPECIES[x['later']]['dispname'],
                 ' (alleen via events)' if x.get('eventOnly') else ''))
    L += ['', '## Objectief slechtere moves (automatisch)', '',
          'Zelfde type, categorie, doelwit en prioriteit; de andere is minstens even sterk en accuraat en heeft alle bijeffecten ook. Niet als startmove of beloning (tegenstanders mogen ze wel).', '']
    dom = res['dominated']
    L.append(', '.join('%s (→ %s)' % (MOVES[a]['name'], MOVES[b]['name']) for a, b in sorted(dom.items())))
    L += ['', '## Items (relics): getallen', '']
    for name, rws, be in item_math():
        L.append('**%s** (×1,3 schade voor de drager): het team neemt minder schade omdat gevechten korter duren.' % name)
        L.append('')
        L.append('| gevecht | beurten | HP-verlies | bespaard (team) | break-even terugslag per aanval |')
        L.append('|---|---|---|---|---|')
        for n, T, taken, saved, per in rws:
            L.append('| %s | %d | %d%% | %.1f%% | %.1f%% |' % (n, T, taken * 100, saved * 100, per * 100))
        L.append('')
        L.append('Gewogen break-even: **%.1f%%** van de max HP per aanval. Gekozen: **2%%** (de normale 10%% is met ×4 HP veel te zwaar). Netto kost Life Orb dus iets HP, maar wint tempo: sneller KO\'s, minder buffs en woede-opbouw van de vijand. Bij 1%% is hij altijd winst (geen afweging).' % (be * 100))
    L += ['',
          '**Leftovers**: normaal 1/16 per beurt; met ×4 HP is dat 6,25% van de balk per beurt, ofwel ±19% per gewoon gevecht: meer dan je in een gevecht verliest (±15%). In de Spire **1/32** (±9% per gewoon gevecht, ±34% per baas): nog steeds extreem sterk, dus rare.',
          '',
          '**Focus Sash**: overleeft één keer een KO-klap, op elke HP (niet alleen vol); daarna weg. Waarde ≈ één klap (±10% HP) plus het redden van een run.',
          '', '## Overige getallen (en waarom)', '',
          '- **Levels:** alles in de Spire is lv 100 (Jordi). Level is dus nooit een knop; sterkte komt uit soort, moves, items, totem-boosts en HP-vermenigvuldiger.',
          '- **Heal na een gevecht 10%, rustplek (Chansey) 40%.** Een gewoon gevecht kost ±11% (zie Ontmoetingen), een elite ±24%, een baas ±55%. Per act: ±2 zwakke (2×7%) + ±2 gewone (2×11%) + 1-2 elites (24-48%) ≈ 60-85% verlies, tegenover 6×10% + 1-2 rustplekken (40-80%) ≈ 100-140% herstel. Goed spel komt met ±70-90% bij de baas aan; slordig spel (gimmicks negeren = 1,5-2× zoveel verlies) strandt. Met de oude 20% na elk gevecht was een gewoon gevecht altijd gratis.',
          '- **Upgrade (Porygon2, "+"):** aanval +30% kracht; statusmove één stage extra en mist nooit; altijd max PP. Rekensom: de hoofdaanval wordt ±60% van de beurten gebruikt, dus ±18% meer schade, gevechten ±15% korter, ±15% minder schade incasseren: ±1,6% HP per gewoon gevecht, 3,6% per elite, 8% per baas. Over de ±15 gevechten die na de eerste rustplek nog komen is dat ±40% HP: precies even veel als rusten (40%). Vroeg in de run is upgraden dus beter, laat in de run rusten: een echte keuze.',
          '- **Geld:** gevecht 15-25¥, elite 35-45¥, baas 80¥ (Amulet Coin +50%): ±280¥ per act. Winkel: move 45/70/120¥ (common/uncommon/rare), vasthouditem 50/85/140¥, relic 120¥, Move Relearner 50¥ + 25¥ per eerder gebruik (zoals card removal in Slay: 75 + 25n). Eén winkelbezoek koopt dus 2-4 dingen.',
          '- **Vasthouditems:** één per Pokémon, zoals in de echte games; gebruikt (Focus Sash, bes) = weg voor de rest van de run. Spire-afwijkingen: Life Orb 2% terugslag, Focus Sash op elke HP, Leftovers 1/32 (zie boven). Nutteloos en dus niet in de pool: Red Card, Eject Button/Pack, Shed Shell, Smoke Ball, Exp. Share, Lucky Egg, Everstone, evolutie-items (Up-Grade, ...), Destiny Knot, Float Stone, Iron Ball, Lagging Tail, Sticky Barb, Ring Target, Full Incense, Macho Brace, Power-items, Cleanse Tag.',
          '- **Draft-zeldzaamheid:** C 35%, B 35%, A 22%, S 8% (zoals kaartzeldzaamheid in Slay: de sterkste opties zijn zeldzaam).',
          '- **Beloningskaarten:** kaart 1 past bij het type van je eerste Pokémon, kaart 2 bij je tweede, kaart 3 is vrij (zoals klassekaarten in Slay). Zeldzaamheid 60/30/10%.',
          '', '## Rentals', '']
    for t in (3, 2, 1, 0):
        lst = sorted([x for x in ok if x['tier'] == t], key=lambda x: -x['V'])
        L.append('### Tier %s (%d)' % (TIER_NAMES[t], len(lst)))
        L.append('')
        L.append('| soort | acts | V | startmoves |')
        L.append('|---|---|---|---|')
        for x in lst:
            acts = ' → '.join(dict.fromkeys(SPECIES[f]['dispname'] for f in x['forms']))
            L.append('| %s | %s | %.0f (%.0f/%.0f/%.0f) | %s |' % (SPECIES[x['base']]['dispname'], acts, x['V'], *x['R'], fmt_moves(x)))
        L.append('')
    L += ['### Alleen via events (te sterk voor de draft)', '',
          'Eenstaps-soorten met een rating boven %.0f (5%% boven de mediaan van act 3). In act 1 zouden ze bijna 2× zo sterk zijn als een eerste vorm en daarmee act 1 breken; via een event kosten ze iets (HP, geld of een move).' % res['single_max'], '']
    for x in sorted(res['events'], key=lambda x: -x['R'][0]):
        L.append('- %s (%.0f): %s' % (SPECIES[x['base']]['dispname'], x['R'][0], fmt_moves(x)))
    L += ['', '## Afgevallen', '']
    for x in sorted([x for x in rows if not x['ok']], key=lambda x: x['base']):
        L.append('- %s: %s' % (SPECIES[x['base']]['dispname'], '; '.join(x['reasons'])))
    L += ['', '## Beloningsmoves', '']
    for r, name in ((0, 'Common'), (1, 'Uncommon'), (2, 'Rare')):
        L.append('**%s (%d):** %s' % (name, len(pools[r]), ', '.join(MOVES[m]['name'] for m in pools[r])))
        L.append('')
    with open(path, 'w') as f:
        f.write('\n'.join(L) + '\n')
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--show')
    ap.add_argument('--no-write', action='store_true')
    a = ap.parse_args()
    res = analyse()
    pools = reward_pools(res['dominated'])
    if a.show:
        for x in res['rows']:
            if x['base'] == a.show:
                print(x['forms'], x['stages'], ['%.0f' % v for v in x['R']], 'V %.0f' % x['V'], x['cat'])
                print('ok' if x['ok'] else x['reasons'])
                print('stab', x['stabs'])
                print('status', x['statusCands'][:6])
                print('grounded', sorted(x['groundedCands'], reverse=True)[:6])
        return
    print('kandidaten %d, toegelaten %d; tiers %s' % (len(res['rows']), len(res['ok']),
          [sum(1 for x in res['ok'] if x['tier'] == t) for t in range(4)]))
    print('pools', {k: len(v) for k, v in pools.items()})
    if not a.no_write:
        print(write_header(res, pools))
        print(write_report(res, pools))


if __name__ == '__main__':
    main()
