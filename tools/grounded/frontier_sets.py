#!/usr/bin/env python3
"""Controle (en reparatie) van de vaste Frontier-sets tegen de data van dit project (TODO 14).

Controleert de sets in
  - src/data/battle_frontier/battle_frontier_mons.h   (gBattleFrontierMons: Tower/Dome/Palace/Arena/Factory/Pike)
  - src/data/battle_frontier/battle_tent.h            (Slateport/Verdanturf/Fallarbor Battle Tent)
  - src/data/battle_frontier/battle_pyramid_*_wild_mons.h (wilde Pokémon in de Pyramid)
  - src/data/battle_frontier/trainer_hill.h           (Trainer Hill, zonder het ongebruikte JP-blok)

en meldt per set:
  move      : move die de soort (incl. voorgangers) in dit project niet kan leren
              (level-up gen_9.h + teachable_learnsets.h + egg_moves.h + sUniversalMoves)
  ability   : abilityNum die bij de soort niet bestaat (leeg slot)
  item      : item dat niet bestaat
  soort     : soort die weg is (elemental monkeys) of niet bestaat
  revisie   : move die t.o.v. upstream (ee1e02b2ef) van type of categorie veranderde
  categorie : hoofdaanval (>=60 power, geen prioriteit) van een categorie (fysiek/speciaal) waarvan de
              stat door een revisie >=40 onder de andere aanvalsstat kwam (in upstream niet, of de stat
              zakte >=15), bijv. Volbeat werd speciaal, Sableye fysiek
  dubbel    : dezelfde move twee keer in één set

Wat 'legaal' is, staat in learnable(): ook Smeargle (Sketch) kan alles. Handmatige keuzes na --fix
(Brave Bird op Swellow door Gale Wings, Brick Break op Spinda door Pure Power) blijven legaal en
worden dus niet teruggedraaid. Zie FRONTIER_SETS.md.

Gebruik: python3 tools/grounded/frontier_sets.py          (controle; exitcode 1 bij meldingen)
         python3 tools/grounded/frontier_sets.py --fix    (vervangt foute moves door de legale move met de
                                                          meest gelijke rol; past EV's/nature aan als alle
                                                          schade-moves daarna van de andere categorie zijn)
"""
import io, os, re, subprocess, sys, tarfile, tempfile
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'spire'))
import spiredata  # noqa: E402

ROOT = spiredata.ROOT
UPSTREAM = 'ee1e02b2ef'   # laatste expansion-commit vóór Project Grounded

FILES = [
    'src/data/battle_frontier/battle_frontier_mons.h',
    'src/data/battle_frontier/battle_tent.h',
    'src/data/battle_frontier/battle_pyramid_level_50_wild_mons.h',
    'src/data/battle_frontier/battle_pyramid_open_level_wild_mons.h',
    'src/data/battle_frontier/trainer_hill.h',
]

REMOVED = {'PANSAGE', 'SIMISAGE', 'PANSEAR', 'SIMISEAR', 'PANPOUR', 'SIMIPOUR'}

# Moves die in dit project van type/categorie veranderden maar in sets geen onzin opleveren (handmatig beoordeeld).
REVISION_OK = set()

UNIVERSAL = {'BIDE', 'FRUSTRATION', 'HIDDEN_POWER', 'MIMIC', 'NATURAL_GIFT', 'RAGE', 'RETURN', 'SECRET_POWER',
             'SUBSTITUTE', 'TERA_BLAST'}   # sUniversalMoves in src/pokemon.c


def read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return f.read()


# ---------------------------------------------------------------------------------------------
# sets lezen

def parse_sets(path):
    txt = read(path)
    skip_until = txt.index('sChallenge_Normal') if path.endswith('trainer_hill.h') else 0
    out = []
    starts = [m for m in re.finditer(r'\.species\s*=\s*SPECIES_(\w+)', txt) if m.start() >= skip_until]
    for i, m in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(txt)
        base = m.start()
        body = txt[base:end]
        mv = re.search(r'\.moves\s*=\s*\{([^}]*)\}', body)
        if not mv:
            continue
        it = re.search(r'\.heldItem\s*=\s*(ITEM_\w+)', body)
        ab = re.search(r'\.abilityNum\s*=\s*(\w+)', body)
        name = re.search(r'\[(FRONTIER_MON_\w+|\w+_TENT_MON_\w+)\]\s*=\s*\{\s*$', txt[max(0, base - 120):base])
        out.append(dict(
            file=path, line=txt.count('\n', 0, base) + 1, species=m.group(1),
            moves=[x.strip().replace('MOVE_', '') for x in mv.group(1).split(',') if x.strip()],
            item=it.group(1).replace('ITEM_', '') if it else None,
            ability=ab.group(1) if ab else None,
            label=name.group(1) if name else None,
            mvtokens=[(base + mv.start(1) + t.start(1), base + mv.start(1) + t.end(1), t.group(1).replace('MOVE_', ''))
                      for t in re.finditer(r'(MOVE_\w+)', mv.group(1))],
            body=(base, body),
        ))
    return out


# ---------------------------------------------------------------------------------------------
# data

def load_items():
    txt = read('include/constants/items.h')
    return set(re.findall(r'#define\s+ITEM_(\w+)\s', txt)) | set(re.findall(r'^\s*ITEM_(\w+)\s*[,=]', txt, re.M))


def old_moves():
    try:
        txt = subprocess.run(['git', '-C', ROOT, 'show', '%s:src/data/moves_info.h' % UPSTREAM],
                             capture_output=True, text=True, check=True).stdout
    except Exception:
        return {}
    orig = spiredata._read
    spiredata._read = lambda p: txt
    try:
        return spiredata.load_moves()
    finally:
        spiredata._read = orig


def old_species():
    """Soortdata van upstream (stats vóór de revisies), via git archive."""
    try:
        data = subprocess.run(['git', '-C', ROOT, 'archive', UPSTREAM, 'src/data/pokemon'],
                              capture_output=True, check=True).stdout
    except Exception:
        return {}
    tmp = tempfile.mkdtemp()
    tf = tarfile.open(fileobj=io.BytesIO(data))
    if hasattr(tarfile, 'data_filter'):
        tf.extractall(tmp, filter='data')
    else:
        tf.extractall(tmp)
    orig = spiredata.ROOT
    spiredata.ROOT = tmp
    try:
        return spiredata.load_species()
    finally:
        spiredata.ROOT = orig


_BODIES = None


def species_body(name):
    global _BODIES
    if _BODIES is None:
        import glob
        _BODIES = {}
        for p in glob.glob(os.path.join(ROOT, 'src/data/pokemon/species_info/gen_*_families.h')):
            _BODIES.update(spiredata._blocks(open(p, encoding='utf-8').read(), 'SPECIES'))
    return _BODIES.get(name, '')


def learnable(species, sp):
    out, seen = set(), set()
    s = species
    while s and s in sp and s not in seen:
        seen.add(s)
        d = sp[s]
        out |= {m for _, m in d['levelup']} | set(d['teach']) | set(d['egg'])
        s = d.get('pre')
    if not re.search(r'tmIlliterate\s*=\s*TRUE', species_body(species)):
        out |= UNIVERSAL
    return out


def learnable_fallback(name):
    """Soorten die via een macro gedefinieerd zijn (Unown): leertabellen op naam."""
    camel = name.title().replace('_', '')
    lv = spiredata.load_levelup().get('s%sLevelUpLearnset' % camel, [])
    te = spiredata.load_movelists('src/data/pokemon/teachable_learnsets.h').get('s%sTeachableLearnset' % camel, [])
    return {m for _, m in lv} | set(te) | UNIVERSAL


_SPECIES_H = None


def species_exists(name):
    global _SPECIES_H
    if _SPECIES_H is None:
        _SPECIES_H = set(re.findall(r'#define\s+SPECIES_(\w+)\s', read('include/constants/species.h')))
    return name in _SPECIES_H


UTILITY_EFFECTS = {'OHKO', 'SHEER_COLD', 'FIXED_HP_DAMAGE', 'LEVEL_DAMAGE', 'PSYWAVE', 'COUNTER', 'MIRROR_COAT',
                   'METAL_BURST', 'ENDEAVOR', 'SUPER_FANG', 'EXPLOSION', 'MISTY_EXPLOSION', 'RAPID_SPIN',
                   'FIRST_TURN_ONLY', 'HIT_ESCAPE', 'KNOCK_OFF', 'FOUL_PLAY', 'BODY_PRESS', 'FALSE_SWIPE',
                   'STEAL_ITEM', 'PURSUIT', 'BIDE', 'PRESENT', 'FINAL_GAMBIT'}


def is_damaging(m):
    return m['cat'] in ('PHYSICAL', 'SPECIAL')


def counts_for_cat(m):
    """Aanvallende move waarvan de schade van Atk/SpA afhangt (geen vaste schade of nutsmove)."""
    return is_damaging(m) and m['effect'] not in UTILITY_EFFECTS


def main_attack(m):
    """Hoofdaanval (>=60 power, geen prioriteit): alleen die tellen voor de categorie-melding."""
    return counts_for_cat(m) and m['power'] >= 60 and m['priority'] <= 0


def stat_of(cat):
    return 'atk' if cat == 'PHYSICAL' else 'spa'


def cat_gap(name, cat, sp, osp):
    """True als de categorie door een revisie >=40 onder de andere aanvalsstat zakte."""
    other = 'SPECIAL' if cat == 'PHYSICAL' else 'PHYSICAL'
    d, o = sp.get(name), osp.get(name)
    if not d or not o:
        return False
    gap_new = d[stat_of(other)] - d[stat_of(cat)]
    gap_old = o[stat_of(other)] - o[stat_of(cat)]
    return gap_new >= 40 and (gap_old < 40 or o[stat_of(cat)] - d[stat_of(cat)] >= 15)


class Data:
    def __init__(self):
        self.sp = spiredata.load_species()
        self.moves = spiredata.load_moves()
        self.items = load_items()
        self.old = old_moves()
        self.osp = old_species()
        self._legal = {}

    def legal(self, name):
        if name not in self._legal:
            legal = learnable(name, self.sp) if name in self.sp else learnable_fallback(name)
            if 'SKETCH' in legal:    # Smeargle: Sketch kopieert (bijna) alles
                legal = set(self.moves) - {'STRUGGLE', 'CHATTER', 'SKETCH', 'NONE'}
            self._legal[name] = legal
        return self._legal[name]


def set_problems(D, s):
    """Lijst (soort, bericht, move-of-None) voor één set."""
    out = []
    name = s['species']
    if name in REMOVED or not species_exists(name):
        return [('soort', name, None)]
    legal = D.legal(name)
    real = [m for m in s['moves'] if m != 'NONE']
    for mv in sorted({m for m in real if real.count(m) > 1}):
        out.append(('move', '%s staat dubbel in de set' % mv, None))
    for mv in s['moves']:
        if mv == 'NONE':
            continue
        if mv not in D.moves:
            out.append(('move', '%s bestaat niet' % mv, mv))
            continue
        if mv not in legal:
            out.append(('move', '%s kan %s niet leren' % (name, mv), mv))
            continue
        m = D.moves[mv]
        if mv in D.old and mv not in REVISION_OK:
            a = D.old[mv]
            if a['type'] != m['type'] or a['cat'] != m['cat']:
                out.append(('revisie', '%s: %s/%s -> %s/%s' % (mv, a['type'], a['cat'], m['type'], m['cat']), mv))
                continue
        if main_attack(m) and cat_gap(name, m['cat'], D.sp, D.osp):
            out.append(('categorie', '%s is %s, %s zakte door een revisie' % (mv, m['cat'].lower(), stat_of(m['cat'])), mv))
    if s['item'] and s['item'] not in D.items:
        out.append(('item', s['item'], None))
    if s['ability'] and s['ability'] not in ('ABILITY_RANDOM', 'ABILITY_HIDDEN') and name in D.sp:
        try:
            n = int(s['ability'])
        except ValueError:
            n = None
        abl = D.sp[name]['abilities']
        if n is None or n >= len(abl) or abl[n] == 'NONE':
            out.append(('ability', '%s abilityNum %s (%s)' % (name, s['ability'], abl), None))
    return out


def check():
    D = Data()
    problems, nsets = [], 0
    for path in FILES:
        for s in parse_sets(path):
            nsets += 1
            where = '%s:%d %s' % (os.path.basename(path), s['line'], s['label'] or s['species'])
            for kind, msg, _ in set_problems(D, s):
                problems.append((kind, where, msg))
    return nsets, problems


# ---------------------------------------------------------------------------------------------
# reparatie

def status_key(m):
    a = re.search(r'\.argument\s*=\s*\{([^}]*)\}', m['body'])
    return (m['effect'], a.group(1).strip() if a else '')


STATUS_GROUPS = (
    ('SLEEP|YAWN', 'sleep'), ('CONFUSE|SWAGGER|FLATTER|TEETER', 'confuse'), ('ROAR', 'phaze'),
    ('PROTECT|ENDURE|DETECT', 'protect'),
    ('RESTORE_HP|^REST$|SOFTBOILED|MORNING_SUN|SYNTHESIS|MOONLIGHT|ROOST|WISH|SHORE_UP', 'heal'),
    ('SPIKES|STEALTH_ROCK|STICKY_WEB|TOXIC_SPIKES', 'hazard'), ('REFLECT|LIGHT_SCREEN|SAFEGUARD|AURORA_VEIL|MIST', 'screen'),
    ('SUNNY|RAIN|SANDSTORM|HAIL|SNOW|WEATHER', 'weather'), ('_UP', 'boost'), ('_DOWN', 'drop'),
    ('ATTRACT|TORMENT|TAUNT|DISABLE|ENCORE|SPITE|GRUDGE|IMPRISON', 'disrupt'),
    ('FORESIGHT|ODOR_SLEUTH|MIRACLE_EYE|LOCK_ON|MIND_READER', 'identify'),
)


def status_group(m):
    k = status_key(m)[1]
    if 'nonVolatileStatus' in k:
        return 'status:' + k.split('MOVE_EFFECT_')[-1]
    for pat, g in STATUS_GROUPS:
        if re.search(pat, m['effect']):
            return g
    return m['effect']


# Vangnet als er geen status-move met dezelfde rol is: algemeen bruikbare moves eerst.
STATUS_FALLBACK = {'TOXIC': 20, 'PROTECT': 18, 'TAUNT': 18, 'THUNDER_WAVE': 16, 'WILL_O_WISP': 16, 'ENCORE': 14,
                   'YAWN': 14, 'SUBSTITUTE': 12, 'REST': 12, 'CONFUSE_RAY': 12, 'LIGHT_SCREEN': 10, 'REFLECT': 10,
                   'HAZE': 10, 'SWAGGER': 8, 'DOUBLE_TEAM': 6, 'SAFEGUARD': 6}
# Moves die nooit als vervanging gekozen worden (zwak, gokwerk of te raar voor een vaste set).
NO_PICK = {'BIDE', 'RAGE', 'MIMIC', 'NATURAL_GIFT', 'TERA_BLAST', 'SKETCH', 'METRONOME', 'SPLASH', 'CELEBRATE',
           'HOLD_HANDS', 'HAPPY_HOUR', 'TRANSFORM', 'STRUGGLE', 'NONE', 'FLING', 'LAST_RESORT', 'SNORE',
           'SLEEP_TALK', 'ASSIST', 'COPYCAT', 'MIRROR_MOVE', 'ME_FIRST', 'NATURE_POWER', 'CHATTER',
           'BELCH', 'SPIT_UP', 'SWALLOW', 'STOCKPILE', 'FOCUS_PUNCH', 'SKY_DROP', 'BEAT_UP', 'ATTRACT',
           'CAPTIVATE', 'PSYCH_UP', 'ROLE_PLAY', 'POWER_SPLIT', 'GUARD_SPLIT', 'POWER_TRICK', 'SPOTLIGHT'}
# Schade-moves met een bijzondere rol die onderling uitwisselbaar zijn.
UTILITY_GROUPS = ({'LEVEL_DAMAGE', 'PSYWAVE', 'FIXED_HP_DAMAGE', 'SUPER_FANG', 'ENDEAVOR'},
                  {'COUNTER', 'MIRROR_COAT', 'METAL_BURST'}, {'EXPLOSION', 'MISTY_EXPLOSION'})


def same_utility(a, b):
    return a == b or any(a in g and b in g for g in UTILITY_GROUPS)


def slow(m):
    """Laad- of rustbeurt (Solar Beam, Fly, Dig, Hyper Beam)."""
    return m['charge'] or m['recharge'] or m['effect'] == 'SEMI_INVULNERABLE'


def eff_power(m):
    p = m['power']
    if p <= 1:
        p = 70
    if m['strikes'] > 1:
        p *= m['strikes']
    elif m['effect'] == 'MULTI_HIT':
        p *= 3
    if slow(m):
        p *= 0.6
    return p


def score(D, orig, cand, others, name, wantcat):
    o, c = D.moves[orig], D.moves[cand]
    types = D.sp[name]['types'] if name in D.sp else []
    if not is_damaging(o):
        if is_damaging(c):
            # Roar/Whirlwind -> Dragon Tail/Circle Throw: zelfde rol (wegblazen)
            if status_group(o) == 'phaze' and c['effect'] == 'HIT_SWITCH_TARGET':
                return 60
            return -500
        sc = 0
        if status_key(c) == status_key(o):
            sc += 100
        elif c['effect'] == o['effect']:
            sc += 70
        elif status_group(c) == status_group(o):
            sc += 50
        else:
            sc += STATUS_FALLBACK.get(cand, 0)
        if c['target'] == o['target']:
            sc += 10
        if c['type'] == o['type']:
            sc += 5
        sc += (c['acc'] or 100) / 50
        return sc
    if not is_damaging(c):
        return -500
    sc = 0
    if o['effect'] in UTILITY_EFFECTS:
        if same_utility(c['effect'], o['effect']):
            sc += 120
    elif c['effect'] in UTILITY_EFFECTS:
        sc -= 80
    if c['cat'] == wantcat:
        sc += 60
    if c['type'] == o['type']:
        sc += 50
    if c['type'] in types:
        sc += 10
    if any(x in D.moves and is_damaging(D.moves[x]) and D.moves[x]['type'] == c['type'] for x in others):
        sc -= 40
    sc -= abs(eff_power(c) - eff_power(o)) * (0.3 if o['effect'] in UTILITY_EFFECTS else 1.0)
    sc -= (100 - (c['acc'] or 100)) * 0.4
    if slow(c) and not slow(o):
        sc -= 60
    if o['priority'] > 0 and c['priority'] > 0:
        sc += 30
    if o['priority'] <= 0 and c['priority'] > 0:
        sc -= 10
    if c['effect'] == o['effect'] and c['effect'] != 'HIT':
        sc += 25
    if set(c['add']) & set(o['add']):
        sc += 10
    if c['recoil'] and not o['recoil']:
        sc -= 10
    return sc


def best_replacement(D, orig, setmoves, name, wantcat):
    others = [x for x in setmoves if x != orig]
    cands = []
    for c in sorted(D.legal(name)):
        if c in setmoves or c not in D.moves or c in NO_PICK:
            continue
        m = D.moves[c]
        if m['zmove'] or m['effect'] in ('NONE', 'PLACEHOLDER'):
            continue
        if main_attack(m) and cat_gap(name, m['cat'], D.sp, D.osp):
            continue
        cands.append((score(D, orig, c, others, name, wantcat), c))
    cands.sort(key=lambda t: (-t[0], t[1]))
    return cands[0][1] if cands else 'NONE'


NATURES = ['HARDY', 'LONELY', 'BRAVE', 'ADAMANT', 'NAUGHTY', 'BOLD', 'DOCILE', 'RELAXED', 'IMPISH', 'LAX',
           'TIMID', 'HASTY', 'SERIOUS', 'JOLLY', 'NAIVE', 'MODEST', 'MILD', 'QUIET', 'BASHFUL', 'RASH',
           'CALM', 'GENTLE', 'SASSY', 'CAREFUL', 'QUIRKY']
NSTATS = ['atk', 'def', 'spe', 'spa', 'spd']


def nature_stats(n):
    i = NATURES.index(n)
    return NSTATS[i // 5], NSTATS[i % 5]


def swap_nature(n):
    up, down = nature_stats(n)
    sw = {'atk': 'spa', 'spa': 'atk'}
    up, down = sw.get(up, up), sw.get(down, down)
    return NATURES[NSTATS.index(up) * 5 + NSTATS.index(down)]


def fix_file(D, path, log):
    txt = read(path)
    edits = []
    for s in parse_sets(path):
        probs = set_problems(D, s)
        if not probs:
            continue
        name = s['species']
        if any(k == 'soort' for k, _, _ in probs):
            log.append(('soort', path, s, name, '(met de hand)'))
            continue
        bad = {mv for k, _, mv in probs if mv and k in ('move', 'revisie', 'categorie')}
        newmoves = list(s['moves'])
        for i, mv in enumerate(s['moves']):
            if mv not in bad:
                continue
            o = D.moves.get(mv)
            if o is None:
                newmoves[i] = 'NONE'
                continue
            want = o['cat']
            if is_damaging(o) and cat_gap(name, want, D.sp, D.osp):
                want = 'SPECIAL' if want == 'PHYSICAL' else 'PHYSICAL'
            newmoves[i] = best_replacement(D, mv, newmoves, name, want)
            log.append(('move', path, s, mv, newmoves[i]))
        for (a, b, tok), new in zip(s['mvtokens'], newmoves):
            if tok != new:
                edits.append((a, b, 'MOVE_' + new))
        # EV's/nature: alle schade-moves nu één categorie en de investering zit in de andere?
        cats = {D.moves[m]['cat'] for m in newmoves if m in D.moves and main_attack(D.moves[m])}
        if len(cats) != 1:
            continue
        cat = cats.pop()
        base, body = s['body']
        ev = re.search(r'TRAINER_PARTY_EVS\(([^)]*)\)', body)
        if ev:
            vals = [int(x) for x in ev.group(1).split(',')]
            ia, isp = 1, 4      # TRAINER_PARTY_EVS(hp, atk, def, speed, spatk, spdef)
            want, other = (ia, isp) if cat == 'PHYSICAL' else (isp, ia)
            if vals[want] == 0 and vals[other] > 0:
                vals[ia], vals[isp] = vals[isp], vals[ia]
                new = ', '.join(str(v) for v in vals)
                edits.append((base + ev.start(1), base + ev.end(1), new))
                log.append(('ev', path, s, ev.group(1), new))
        else:
            a = re.search(r'\.attackEV\s*=\s*\d+', body)
            sa = re.search(r'\.spAttackEV\s*=\s*\d+', body)
            wantf, otherf = (a, sa) if cat == 'PHYSICAL' else (sa, a)
            if wantf is None and otherf is not None:
                old = otherf.group(0)
                new = old.replace('.attackEV', '.spAttackEV') if old.startswith('.attackEV') else old.replace('.spAttackEV', '.attackEV')
                edits.append((base + otherf.start(), base + otherf.end(), new))
                log.append(('ev', path, s, old, new))
        na = re.search(r'\.nature\s*=\s*NATURE_(\w+)', body)
        if na:
            up, down = nature_stats(na.group(1))
            good = stat_of(cat)
            other = 'spa' if good == 'atk' else 'atk'
            if up == other or down == good:
                nn = swap_nature(na.group(1))
                edits.append((base + na.start(1), base + na.end(1), nn))
                log.append(('nature', path, s, na.group(1), nn))
    for a, b, new in sorted(edits, reverse=True):
        txt = txt[:a] + new + txt[b:]
    with open(os.path.join(ROOT, path), 'w', encoding='utf-8') as f:
        f.write(txt)


def fix():
    D = Data()
    log = []
    for path in FILES:
        fix_file(D, path, log)
    for kind, path, s, a, b in log:
        print('%-7s %-32s %-12s %s -> %s' % (kind, '%s:%d' % (os.path.basename(path), s['line']), s['species'], a, b))
    print('\n', dict(Counter(k for k, *_ in log)))
    return log


def main():
    if '--fix' in sys.argv:
        fix()
        return
    nsets, problems = check()
    for kind, where, msg in problems:
        print('%-9s %-55s %s' % (kind, where, msg))
    c = Counter(k for k, _, _ in problems)
    print('\n%d sets gecontroleerd, %d meldingen %s' % (nsets, len(problems), dict(c)))
    sys.exit(1 if problems else 0)


if __name__ == '__main__':
    main()
