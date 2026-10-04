#!/usr/bin/env python3
"""Kleine schade- en snelheidscalculator + 'sweep-simulatie' tegen de gymleiders, E4 en Champion.

Gebruik:
  python3 tools/grounded/balance/calc.py rank [--top 40] [--setup]   # ranglijst van de hele dex
  python3 tools/grounded/balance/calc.py mon KRICKETUNE [--setup]     # detail per gym
  python3 tools/grounded/balance/calc.py dmg ATTACKER LV MOVE DEFENDER LV  # één berekening

Aannames (bewust simpel, voor vergelijken, niet voor exacte rolls):
- Speler: IV 20, geen EV's, neutrale nature, geen item; level = ace-level van de gym (LEVEL_AT_STAGE).
- Gymteams: IV's uit trainers.party (meestal 31), geen EV's, abilities en items uit het bestand
  (Choice Band/Specs/Scarf, Life Orb, Expert Belt, Eviolite, Assault Vest en Focus Sash tellen mee).
- Moves van de speler: level-up (huidige vorm + voorgangers t/m hun evolutielevel) + TM's/HM's die in die
  fase al te krijgen zijn (TM_STAGE). Geen egg/tutor moves. De beste aanval = hoogste verwachte schade
  (accuracy meegewogen). Schade met gemiddelde roll (0,925), zonder crits; weer en terrein genegeerd.
- Sweep = 1-tegen-1 achter elkaar met overgedragen HP; wie sneller is slaat eerst (prioriteit telt mee).
  'Setup' = de speler gebruikt eerst één keer zijn beste boost-move (en incasseert die beurt).
"""
import math, os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
import balancedata as bd  # noqa: E402
import spiredata  # noqa: E402

SPECIES = spiredata.load_species()
MOVES = spiredata.load_moves()
CHART = spiredata.load_typechart()


def norm(s):
    return re.sub(r'[^A-Z0-9]', '', s.upper())


_MOVE_IDX = {}
for k, m in MOVES.items():
    _MOVE_IDX[norm(m['name'])] = k
    _MOVE_IDX.setdefault(norm(k), k)
_SP_IDX = {}
for k, d in SPECIES.items():
    _SP_IDX.setdefault(norm(k), k)
    _SP_IDX.setdefault(norm(d['dispname']), k)


def species_key(name):
    n = norm(name.replace('-', '_'))
    if n in _SP_IDX:
        return _SP_IDX[n]
    for suf in ('ALOLA', 'GALAR', 'HISUI', 'PALDEA'):
        if n.endswith(suf) and n[:-len(suf)] + suf in _SP_IDX:
            return _SP_IDX[n]
    return _SP_IDX.get(n + 'NORMAL') or _SP_IDX.get(n + 'MALE') or _SP_IDX.get(n + 'PLANT')


def move_key(name):
    return _MOVE_IDX.get(norm(name))


def ability_key(name):
    return norm(name)


# ---------------------------------------------------------------------------------------------
# stats en schade

def calc_stats(sp, lv, iv=20):
    d = SPECIES[sp]
    ivs = iv if isinstance(iv, list) else [iv] * 6
    if len(ivs) < 6:
        ivs = (ivs + [31] * 6)[:6]
    hp = (2 * d['hp'] + ivs[0]) * lv // 100 + lv + 10
    o = lambda b, i: (2 * b + i) * lv // 100 + 5
    return dict(hp=hp, atk=o(d['atk'], ivs[1]), def_=o(d['def'], ivs[2]), spa=o(d['spa'], ivs[3]),
                spd=o(d['spd'], ivs[4]), spe=o(d['spe'], ivs[5]))


def eff(mtype, types):
    m = 1.0
    for t in types:
        m *= CHART.get(mtype, {}).get(t, 1.0)
    return m


STAGE_MULT = {-2: 0.5, -1: 2 / 3, 0: 1.0, 1: 1.5, 2: 2.0, 3: 2.5, 4: 3.0, 5: 3.5, 6: 4.0}
ATE = {'PIXILATE': 'FAIRY', 'REFRIGERATE': 'ICE', 'AERILATE': 'FLYING', 'GALVANIZE': 'ELECTRIC'}
IMMUNE = {'LEVITATE': 'GROUND', 'VOLT_ABSORB': 'ELECTRIC', 'LIGHTNING_ROD': 'ELECTRIC', 'MOTOR_DRIVE': 'ELECTRIC',
          'WATER_ABSORB': 'WATER', 'STORM_DRAIN': 'WATER', 'DRY_SKIN': 'WATER', 'FLASH_FIRE': 'FIRE',
          'SAP_SIPPER': 'GRASS', 'EARTH_EATER': 'GROUND', 'WELL_BAKED_BODY': 'FIRE'}
TYPE_ITEMS = {'CHARCOAL': 'FIRE', 'MYSTIC WATER': 'WATER', 'MAGNET': 'ELECTRIC', 'MIRACLE SEED': 'GRASS',
              'NEVER-MELT ICE': 'ICE', 'BLACK BELT': 'FIGHTING', 'POISON BARB': 'POISON', 'SOFT SAND': 'GROUND',
              'SHARP BEAK': 'FLYING', 'TWISTEDSPOON': 'PSYCHIC', 'TWISTED SPOON': 'PSYCHIC', 'SILVER POWDER': 'BUG',
              'HARD STONE': 'ROCK', 'SPELL TAG': 'GHOST', 'DRAGON FANG': 'DRAGON', 'BLACK GLASSES': 'DARK',
              'METAL COAT': 'STEEL', 'SILK SCARF': 'NORMAL', 'FAIRY FEATHER': 'FAIRY'}
BAD_EFFECTS = {'EXPLOSION', 'MISTY_EXPLOSION', 'OHKO', 'RECHARGE', 'SOLAR_BEAM', 'TWO_TURNS_ATTACK', 'FUTURE_SIGHT',
               'FOCUS_PUNCH', 'BIDE', 'COUNTER', 'MIRROR_COAT', 'METAL_BURST', 'SKY_DROP', 'SHELL_TRAP',
               'BEAT_UP', 'FINAL_GAMBIT', 'DREAM_EATER', 'SNORE', 'SLEEP_TALK', 'LAST_RESORT', 'SUCKER_PUNCH',
               'FAKE_OUT', 'FIRST_IMPRESSION', 'SYNCHRONOISE', 'HYPER_BEAM', 'ROLLOUT', 'FURY_CUTTER',
               'UPPER_HAND', 'POLTERGEIST', 'BELCH', 'SPIT_UP', 'STEEL_BEAM', 'MIND_BLOWN', 'MEMENTO'}


class Mon:
    def __init__(self, sp, lv, iv=20, ability=None, item='', moves=None, boosts=None):
        self.sp, self.lv = sp, lv
        self.d = SPECIES[sp]
        self.st = calc_stats(sp, lv, iv)
        self.ability = ability or (self.d['abilities'][0] if self.d['abilities'] else 'NONE')
        self.item = (item or '').upper()
        self.moves = moves or []
        self.boosts = boosts or {}
        self.types = self.d['types']

    def stat(self, key):
        v = self.st[key] * STAGE_MULT[max(-2, min(6, self.boosts.get(key, 0)))]
        if key == 'spe' and 'SCARF' in self.item:
            v *= 1.5
        if key in ('atk',) and self.ability in ('HUGE_POWER', 'PURE_POWER'):
            v *= 2
        if key in ('def_', 'spd') and self.item == 'EVIOLITE' and self.d['evos']:
            v *= 1.5
        if key == 'spd' and self.item == 'ASSAULT VEST':
            v *= 1.5
        return v


def move_power(att, mk, dfn):
    """(type, power, category, hits) na abilities van de aanvaller; None als hij niet bruikbaar is."""
    m = MOVES[mk]
    if m['cat'] == 'STATUS' or m['power'] <= 1 or m['effect'] in BAD_EFFECTS or m['charge'] or m['recharge'] or m['zmove']:
        return None
    t, p = m['type'], m['power']
    if m['type'] == 'NORMAL' and att.ability in ATE:
        t, p = ATE[att.ability], p * 1.2
    if att.ability == 'NORMALIZE':
        t, p = 'NORMAL', p * 1.2
    if att.ability == 'TECHNICIAN' and p <= 60:
        p *= 1.5
    body = m['body']
    if att.ability == 'SHARPNESS' and 'slicingMove = TRUE' in body:
        p *= 1.5
    if att.ability == 'STRONG_JAW' and 'bitingMove = TRUE' in body:
        p *= 1.5
    if att.ability == 'IRON_FIST' and 'punchingMove = TRUE' in body:
        p *= 1.2
    if att.ability == 'MEGA_LAUNCHER' and 'pulseMove = TRUE' in body:
        p *= 1.5
    if att.ability == 'PUNK_ROCK' and m['sound']:
        p *= 1.3
    if att.ability == 'TOUGH_CLAWS' and m['contact']:
        p *= 1.3
    if att.ability == 'RECKLESS' and m['recoil']:
        p *= 1.2
    if att.ability == 'SHEER_FORCE' and m['add'] and not m['selfEffect']:
        p *= 1.3
    hits = m['strikes'] or 1
    if m['effect'] in ('MULTI_HIT',):
        hits = 5 if att.ability == 'SKILL_LINK' else (4.5 if 'LOADED' in att.item else 3.1)
    if m['effect'] == 'TRIPLE_KICK':
        hits = 3
    return t, p, m['cat'], hits


def damage(att, mk, dfn, roll=0.925):
    """Verwachte schade (HP) van één gebruik, accuracy meegewogen."""
    r = move_power(att, mk, dfn)
    if not r:
        return 0.0
    t, p, cat, hits = r
    if dfn.ability in IMMUNE and IMMUNE[dfn.ability] == t:
        return 0.0
    e = eff(t, dfn.types)
    if e == 0:
        return 0.0
    if cat == 'PHYSICAL':
        a, d = att.stat('atk'), dfn.stat('def_')
        if att.ability != 'GUTS' and False:
            pass
    else:
        a, d = att.stat('spa'), dfn.stat('spd')
    if MOVES[mk]['effect'] == 'BODY_PRESS':
        a = att.stat('def_')
    base = math.floor(math.floor(math.floor(2 * att.lv / 5 + 2) * p * a / d) / 50) + 2
    mod = roll * e
    if t in att.types or (att.ability in ('PROTEAN', 'LIBERO') and not getattr(att, 'protean_used', False)):
        mod *= 2.0 if att.ability == 'ADAPTABILITY' else 1.5
    if att.item in ('LIFE ORB',):
        mod *= 1.3
    if att.item == 'CHOICE BAND' and cat == 'PHYSICAL' or att.item == 'CHOICE SPECS' and cat == 'SPECIAL':
        mod *= 1.5
    if att.item == 'EXPERT BELT' and e > 1:
        mod *= 1.2
    if TYPE_ITEMS.get(att.item) == t:
        mod *= 1.2
    if att.ability == 'TINTED_LENS' and e < 1:
        mod *= 2
    if dfn.ability in ('SOLID_ROCK', 'FILTER', 'PRISM_ARMOR') and e > 1:
        mod *= 0.75
    if dfn.ability == 'THICK_FAT' and t in ('FIRE', 'ICE'):
        mod *= 0.5
    if dfn.ability in ('MULTISCALE', 'SHADOW_SHIELD'):
        mod *= 0.75          # half bij volle HP: gemiddeld over twee treffers
    if dfn.ability == 'FLUFFY':
        mod *= 0.5 if MOVES[mk]['contact'] else 1
        mod *= 2 if t == 'FIRE' else 1
    if dfn.ability == 'ICE_SCALES' and cat == 'SPECIAL':
        mod *= 0.5
    if dfn.ability == 'HEATPROOF' and t == 'FIRE':
        mod *= 0.5
    if dfn.ability == 'PURIFYING_SALT' and t == 'GHOST':
        mod *= 0.5
    if dfn.ability == 'WONDER_GUARD' and e <= 1:
        return 0.0
    acc = MOVES[mk]['acc'] or 100
    if att.ability in ('NO_GUARD',) or dfn.ability == 'NO_GUARD':
        acc = 100
    if att.ability == 'COMPOUND_EYES':
        acc = min(100, acc * 1.3)
    return base * mod * hits * acc / 100


def best_move(att, dfn, movelist):
    best, bd_ = None, 0.0
    for mk in movelist:
        if mk not in MOVES:
            continue
        dmg = damage(att, mk, dfn)
        if dmg > bd_:
            best, bd_ = mk, dmg
    return best, bd_


SETUP = {  # move: boosts
    'SWORDS_DANCE': {'atk': 2}, 'DRAGON_DANCE': {'atk': 1, 'spe': 1}, 'SHELL_SMASH': {'atk': 2, 'spa': 2, 'spe': 2, 'def_': -1, 'spd': -1},
    'QUIVER_DANCE': {'spa': 1, 'spd': 1, 'spe': 1}, 'NASTY_PLOT': {'spa': 2}, 'CALM_MIND': {'spa': 1, 'spd': 1},
    'BULK_UP': {'atk': 1, 'def_': 1}, 'AGILITY': {'spe': 2}, 'ROCK_POLISH': {'spe': 2}, 'SHIFT_GEAR': {'atk': 1, 'spe': 2},
    'COIL': {'atk': 1, 'def_': 1}, 'HONE_CLAWS': {'atk': 1}, 'GROWTH': {'atk': 1, 'spa': 1}, 'TAIL_GLOW': {'spa': 3},
    'GEOMANCY': {'spa': 2, 'spd': 2, 'spe': 2}, 'VICTORY_DANCE': {'atk': 1, 'def_': 1, 'spe': 1},
    'TIDY_UP': {'atk': 1, 'spe': 1}, 'BELLY_DRUM': {'atk': 6}, 'CURSE': {'atk': 1, 'def_': 1, 'spe': -1},
    'WORK_UP': {'atk': 1, 'spa': 1}, 'FILLET_AWAY': {'atk': 2, 'spa': 2, 'spe': 2}, 'CLANGOROUS_SOUL': {'atk': 1, 'def_': 1, 'spa': 1, 'spd': 1, 'spe': 1},
    'NO_RETREAT': {'atk': 1, 'def_': 1, 'spa': 1, 'spd': 1, 'spe': 1}, 'AUTOTOMIZE': {'spe': 2}, 'IRON_DEFENSE': {'def_': 2},
    'MACHINE_LEARNING': {'atk': 1, 'spa': 1, 'spe': 1},  # benadering: 2 beurten = top-3 +1 (eerste beurt top-1)
}


def known_moves(sp, lv, stage):
    """Level-up (deze vorm + voorgangers t/m evolutielevel) + TM's die in deze fase te krijgen zijn."""
    out = set(m for l, m in SPECIES[sp]['levelup'] if l <= lv)
    cur = sp
    while SPECIES[cur].get('pre'):
        pre = SPECIES[cur]['pre']
        evo_lv = lv
        for e in SPECIES[pre]['evos']:
            if e['target'] == cur:
                try:
                    evo_lv = int(e['param'])
                except ValueError:
                    pass
        out |= set(m for l, m in SPECIES[pre]['levelup'] if l <= min(lv, evo_lv))
        cur = pre
    for m in SPECIES[sp]['teach']:
        if bd.TM_STAGE.get(m, 99) <= stage:
            out.add(m)
    return out


def best_setup(moves):
    best, score = None, 0
    for m in moves:
        if m in SETUP:
            s = sum(max(v, 0) for k, v in SETUP[m].items() if k in ('atk', 'spa', 'spe')) + (2 if m == 'BELLY_DRUM' else 0)
            if s > score:
                best, score = m, s
    return best


def make_enemy(m):
    sp = species_key(m['species'])
    if not sp:
        return None
    ab = ability_key(m['ability']) if m['ability'] else None
    mv = [move_key(x) for x in m['moves']]
    mv = [x for x in mv if x] or [x for l, x in SPECIES[sp]['levelup'] if l <= m['level']][-4:]
    return Mon(sp, m['level'], m['ivs'], ab, m['item'], mv)


def speed_order(a, am, b, bm):
    pa = MOVES[am]['priority'] if am else 0
    pb = MOVES[bm]['priority'] if bm else 0
    if a.ability == 'GALE_WINGS' and am and MOVES[am]['type'] == 'FLYING':
        pa += 1
    if b.ability == 'GALE_WINGS' and bm and MOVES[bm]['type'] == 'FLYING':
        pb += 1
    if pa != pb:
        return pa > pb
    return a.stat('spe') >= b.stat('spe')


def duel(me, foe, my_moves, hp_me, setup=None):
    """Simuleert 1-tegen-1. Geeft (gewonnen, resterende HP, beurten, details)."""
    foe_hp = foe.st['hp']
    sash = 'FOCUS SASH' in foe.item
    turns = 0
    acts = {'me': 0, 'foe': 0}
    if setup:
        fm, fd = best_move(foe, me, foe.moves)
        hp_me -= fd
        if hp_me <= 0:
            return False, 0, 1, 'sneuvelt tijdens %s' % setup
        for k, v in SETUP[setup].items():
            me.boosts[k] = me.boosts.get(k, 0) + v * (2 if me.ability == 'SIMPLE' else 1)
        if setup == 'BELLY_DRUM':
            hp_me -= me.st['hp'] / 2
        turns += 1
    while turns < 12:
        mm, md = best_move(me, foe, my_moves)
        fm, fd = best_move(foe, me, foe.moves)
        if md <= 0 and fd <= 0:
            return False, hp_me, turns, 'patstelling'
        first = speed_order(me, mm, foe, fm)
        order = [('me', mm, md), ('foe', fm, fd)] if first else [('foe', fm, fd), ('me', mm, md)]
        turns += 1
        for who, mv, dmg in order:
            mon = me if who == 'me' else foe
            acts[who] += 1
            if mon.ability == 'TRUANT' and acts[who] % 2 == 0:
                continue        # Truant: elke tweede beurt niets
            if who == 'me':
                if me.ability in ('PROTEAN', 'LIBERO') and not getattr(me, 'protean_used', False) and mv:
                    me.types, me.protean_used = [MOVES[mv]['type']], True   # Gen 9: één keer per inzet
                if sash and foe_hp == foe.st['hp'] and dmg >= foe_hp and (MOVES[mv]['strikes'] or 1) == 1 \
                        and MOVES[mv]['effect'] != 'MULTI_HIT':
                    foe_hp = 1
                else:
                    foe_hp -= dmg
                if foe_hp <= 0:
                    return True, hp_me, turns, '%s' % MOVES[mm]['name'] if mm else ''
            else:
                hp_me -= dmg
                if hp_me <= 0:
                    return False, 0, turns, 'verliest van %s (%s)' % (foe.sp, MOVES[fm]['name'] if fm else '-')
        if me.ability == 'SPEED_BOOST':
            me.boosts['spe'] = me.boosts.get('spe', 0) + 1
    return False, hp_me, turns, 'te lang'


def ability_for(sp, slot):
    ab = SPECIES[sp]['abilities'] or ['NONE']
    a = ab[slot] if slot < len(ab) else 'NONE'
    return ab[0] if a == 'NONE' else a


def sweep(sp, stage, tid, setup=False, lv=None, slot=0):
    """Aantal tegenstanders dat de soort achter elkaar verslaat (ability-slot 0/1/2)."""
    tr = bd.load_trainer(tid)
    lv = lv or bd.LEVEL_AT_STAGE[stage]
    moves = known_moves(sp, lv, stage)
    sm = best_setup(moves) if setup else None
    me = Mon(sp, lv, ability=ability_for(sp, slot))
    hp = me.st['hp']
    kos, log, alive = 0, [], True
    wins1v1 = 0
    for i, m in enumerate(tr['mons']):
        foe = make_enemy(m)
        if not foe:
            continue
        fresh = Mon(sp, lv, ability=me.ability)
        w1, _, _, _ = duel(fresh, foe, moves, fresh.st['hp'], sm if setup else None)
        wins1v1 += w1
        if not alive:
            continue
        foe = make_enemy(m)
        won, hp, t, info = duel(me, foe, moves, hp, sm if (setup and i == 0) else None)
        log.append((foe.sp, won, round(100 * max(hp, 0) / me.st['hp']), info))
        if not won:
            alive = False
            continue
        kos += 1
    sweep.last_1v1 = wins1v1
    return kos, len(tr['mons']), log


def matchup_table(sp, stage, tid, lv=None, slot=0):
    """Per tegenstander: % schade heen en terug, snelheid."""
    tr = bd.load_trainer(tid)
    lv = lv or bd.LEVEL_AT_STAGE[stage]
    moves = known_moves(sp, lv, stage)
    me = Mon(sp, lv, ability=ability_for(sp, slot))
    rows = []
    for m in tr['mons']:
        foe = make_enemy(m)
        if not foe:
            continue
        mm, md = best_move(me, foe, moves)
        fm, fd = best_move(foe, me, foe.moves)
        rows.append((foe.sp, foe.lv, MOVES[mm]['name'] if mm else '-', round(100 * md / foe.st['hp']),
                     MOVES[fm]['name'] if fm else '-', round(100 * fd / me.st['hp']),
                     'sneller' if speed_order(me, mm, foe, fm) else 'trager'))
    return rows


# ---------------------------------------------------------------------------------------------

def line_root(sp):
    while SPECIES[sp].get('pre'):
        sp = SPECIES[sp]['pre']
    return sp


def forms_at(av):
    """Per lijn en fase de sterkste beschikbare vorm (hoogste BST)."""
    lines = {}
    for sp, a in av.items():
        d = SPECIES[sp]
        if d['isMegaEvolution'] or d['isGigantamax'] or d['isTeraForm'] or d['isPrimalReversion'] or d['isUltraBurst']:
            continue
        lines.setdefault(line_root(sp), []).append(sp)
    out = {}
    for root, sps in lines.items():
        for st in range(9):
            cand = [s for s in sps if av[s]['stage'] <= st]
            if cand:
                best = max(cand, key=lambda s: sum(SPECIES[s][k] for k in ('hp', 'atk', 'def', 'spa', 'spd', 'spe')))
                out.setdefault(root, {})[st] = best
    return out


def rank(top=40, setup=False, quiet=False, by1v1=False):
    av = bd.availability(SPECIES)
    fa = forms_at(av)
    results = []
    gyms = bd.GYMS
    for root, per in fa.items():
        first = min(per)
        best = None
        for slot in (0, 1):  # verborgen abilities zijn voor de speler niet te krijgen (geen Ability Patch, geen DexNav)
            if slot and all(ability_for(s, slot) == ability_for(s, 0) for s in per.values()):
                continue
            tot, n, detail, w1 = 0, 0, [], 0
            for tid, st in gyms:
                if st not in per:
                    detail.append('-')
                    continue
                try:
                    k, of, _ = sweep(per[st], st, tid, setup, slot=slot)
                except Exception:  # noqa
                    detail.append('?')
                    continue
                tot += k
                w1 += sweep.last_1v1
                n += 1
                detail.append(k)
            if n and (best is None or (tot, w1) > (best[0], best[4])):
                best = (tot, n, detail, ability_for(per[max(per)], slot) + (' (HA)' if slot == 2 else ''), w1)
        if best:
            tot, n, detail, ab, w1 = best
            legend = any(SPECIES[s]['isLegendary'] or SPECIES[s]['isMythical'] for s in per.values())
            results.append((tot, w1, root, per[max(per)], first, av[per[first]]['src'], detail, legend, ab))
    key = (lambda r: (r[1], r[0])) if by1v1 else (lambda r: (r[0], r[1]))
    results.sort(key=key, reverse=True)
    if not quiet:
        print('%-4s %-4s %-14s %-16s %-18s %-4s %-34s %s' % ('som', '1v1', 'lijn', 'eindvorm', 'ability', 'fase', 'eerste bron',
              'KO\'s op rij per gevecht (R B W F N W T&L Wal | Sid Pho Gla Dra Ste)'))
        for tot, w1, root, fin, first, src, det, leg, ab in results[:top]:
            print('%-4d %-4d %-14s %-16s %-18s %-4d %-34s %s%s' % (tot, w1, root, fin[:16], ab[:18], first, src[:34],
                  ' '.join(str(x) for x in det), ' (legendary)' if leg else ''))
    return results


def main():
    a = sys.argv[1:]
    setup = '--setup' in a
    if not a or a[0] == 'rank':
        top = int(a[a.index('--top') + 1]) if '--top' in a else 40
        rank(top, setup, by1v1='--1v1' in a)
    elif a[0] == 'mon':
        sp = species_key(a[1])
        av = bd.availability(SPECIES)
        fa = forms_at(av)
        per = fa.get(line_root(sp), {})
        print(sp, av.get(sp))
        for tid, st in bd.GYMS:
            if st not in per:
                continue
            form = sp if sp in av and av[sp]['stage'] <= st else per[st]
            if form != sp and sp in per.values() and st < av[sp]['stage']:
                pass
            slot = int(a[a.index('--slot') + 1]) if '--slot' in a else 0
            k, of, log = sweep(form, st, tid, setup, slot=slot)
            print('\n%s (fase %d, %s lv %d, %s): %d/%d op rij, %d/%d 1-tegen-1' % (
                tid.replace('TRAINER_', ''), st, form, bd.LEVEL_AT_STAGE[st], ability_for(form, slot), k, of, sweep.last_1v1, of))
            for r in matchup_table(form, st, tid, slot=slot):
                print('   vs %-16s lv%-3d  ik: %-14s %4d%%   zij: %-14s %4d%%  %s' % r)
    elif a[0] == 'dmg':
        att = Mon(species_key(a[1]), int(a[2]))
        dfn = Mon(species_key(a[4]), int(a[5]), 31)
        mk = move_key(a[3])
        d = damage(att, mk, dfn)
        print('%s lv%s %s -> %s lv%s: %.0f HP = %.0f%% (HP %d), snelheid %d vs %d' % (
            att.sp, att.lv, MOVES[mk]['name'], dfn.sp, dfn.lv, d, 100 * d / dfn.st['hp'], dfn.st['hp'],
            att.stat('spe'), dfn.stat('spe')))


if __name__ == '__main__':
    main()
