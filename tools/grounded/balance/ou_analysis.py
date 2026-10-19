#!/usr/bin/env python3
"""OU-balansanalyse voor Project Grounded: setbouwer, ranglijst (rom vs. vanilla), dreigingen en teams.

  python3 tools/grounded/balance/ou_analysis.py fetch <map>               # vanilla-databestanden (expansion 1.14.4)
  python3 tools/grounded/balance/ou_analysis.py rank <vanillamap> <uit.json> [--jobs 4] [--only A,B]
  python3 tools/grounded/balance/ou_analysis.py refs <vanillamap>         # OU-referenties: legaliteit + onderling
  python3 tools/grounded/balance/ou_analysis.py teams <teams.txt> [--n 40] [--vs-refs]
  python3 tools/grounded/balance/ou_analysis.py duel "<set1>" "<set2>"     # sets als Showdown-tekst of soortnaam

De vanilla-dataset gebruikt de officiële movepools uit tools/learnset_helpers/build/all_learnables.json
(zet die over uit de hoofdcheckout als hij in een worktree ontbreekt)."""
import json, math, os, random, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ousim as S  # noqa: E402
from ou_refs import OU_REFS, UBERS  # noqa: E402

LEARNABLES = os.path.join(S.ROOT, 'tools/learnset_helpers/build/all_learnables.json')
VANILLA_FILES = ['src/data/moves_info.h', 'src/data/types_info.h', 'src/data/pokemon/level_up_learnsets/gen_9.h',
                 'src/data/pokemon/teachable_learnsets.h', 'src/data/pokemon/egg_moves.h'] + \
                ['src/data/pokemon/species_info/gen_%d_families.h' % i for i in range(1, 10)]
SKIP_FORMS = re.compile(r'_(MEGA|GMAX|TOTEM|TERA|PRIMAL|ULTRA|BUSTED|NOICE|ZEN|BLADE|SCHOOL|PIROUETTE|HANGRY|GULPING|'
                        r'GORGING|ETERNAMAX|COMPLETE|COSPLAY|ROCK_STAR|BELLE|POP_STAR|PHD|LIBRE|PARTNER|STARTER|'
                        r'CAP|SUNNY|RAINY|SNOWY|SUNSHINE|STELLAR|DROOPY|STRETCHY|NOICE_FACE|BATTLE_BOND|ASH|'
                        r'RIDER|CROWNED|TERASTAL|ORIGINAL|MEGA_X|MEGA_Y|PALDEA_COMBAT_TERA|_10|_COMPLETE)\b')


def fetch(dest):
    base = 'https://raw.githubusercontent.com/rh-hideout/pokeemerald-expansion/expansion/1.14.4/'
    for f in VANILLA_FILES:
        p = os.path.join(dest, f)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        subprocess.run(['curl', '-sS', '-f', '-o', p, base + f], check=True)
    print('vanilla-bestanden in', dest)


# =============================================================================================
# datasets

_DATA = {}


def get_data(label, vanilla=None):
    if label not in _DATA:
        if label == 'cur':
            _DATA[label] = S.Data(S.ROOT, None, 'cur')
        else:
            _DATA[label] = S.Data(vanilla, LEARNABLES, 'van')
    return _DATA[label]


def ref_sets(data, allow_hidden=True):
    """OU-referentiesets voor deze dataset; ontbrekende moves aangevuld met de setbouwer."""
    out, notes = [], {}
    for ms in S.parse_showdown(OU_REFS, data):
        ms, n = S.legalize(ms, data, allow_hidden)
        if len(ms.moves) < 4:
            fill = best_fill(ms, data, 4 - len(ms.moves))
            if fill:
                n.append('aangevuld: ' + ', '.join(data.moves[m]['name'] for m in fill))
            ms.moves += fill
        out.append(ms)
        notes[ms.species] = n
    return out, notes


def best_fill(ms, data, k):
    cands = attack_candidates(ms.species, data, ms.ability)
    d = data.species[ms.species]
    if ms.evs.get('atk', 0) != ms.evs.get('spa', 0):
        cat = 'PHYSICAL' if ms.evs.get('atk', 0) > ms.evs.get('spa', 0) else 'SPECIAL'
    else:
        cat = 'PHYSICAL' if d['atk'] >= d['spa'] else 'SPECIAL'
    cands = [m for m in cands if m not in ms.moves and (data.moves[m]['cat'] == cat or
                                                        data.moves[m]['effect'] in ('BODY_PRESS', 'LEVEL_DAMAGE'))]
    if not cands:
        return []
    dummy = [S.MonSet('BLISSEY', 'NATURAL_CURE', '', ['TACKLE'])]
    refs = REF_CACHE.get(data.label) or dummy
    chosen = list(ms.moves)
    out = []
    for _ in range(k):
        best, bv = None, -1
        for m in cands:
            if m in chosen:
                continue
            v = coverage(ms, chosen + [m], refs, data)
            if v > bv:
                best, bv = m, v
        if not best:
            break
        chosen.append(best)
        out.append(best)
    return out


REF_CACHE = {}
MODELED = set(re.findall(r"'([A-Z][A-Z0-9_]+)'", open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ousim.py')).read()))

# =============================================================================================
# setbouwer

GOOD_STATUS = ['WILL_O_WISP', 'TOXIC', 'THUNDER_WAVE', 'SPORE', 'GLARE', 'YAWN', 'STRENGTH_SAP']
HAZARDS = ['STEALTH_ROCK', 'SPIKES', 'MOAI_WATCH', 'TOXIC_SPIKES']
PHYS_SETUP = ['SHELL_SMASH', 'DRAGON_DANCE', 'BUNNY_HOP', 'VICTORY_DANCE', 'SHIFT_GEAR', 'SWORDS_DANCE', 'PACK_HOWL',
              'TIDY_UP', 'BULK_UP', 'COIL', 'CURSE', 'BELLY_DRUM', 'HONE_CLAWS', 'MACHINE_LEARNING']
SPEC_SETUP = ['SHELL_SMASH', 'QUIVER_DANCE', 'TAIL_GLOW', 'NASTY_PLOT', 'CALM_MIND', 'MACHINE_LEARNING', 'THE_OLD_DAYS',
              'GROWTH', 'WORK_UP']
DEF_SETUP = ['IRON_DEFENSE', 'COSMIC_POWER', 'CALM_MIND', 'BULK_UP', 'CURSE', 'PRIMEVAL_WARD', 'BEAVER_DAM',
             'STOCKPILE', 'AMNESIA', 'ACID_ARMOR', 'SHELTER', 'DEFEND_ORDER', 'MACHINE_LEARNING']
RECOVERY = ['RECOVER', 'SLACK_OFF', 'SOFT_BOILED', 'MILK_DRINK', 'ROOST', 'MOONLIGHT', 'MORNING_SUN', 'SYNTHESIS',
            'SHORE_UP', 'HEAL_ORDER', 'STRENGTH_SAP', 'OLIVE_OIL', 'WISH', 'LUNAR_BLESSING', 'REST']


def attack_candidates(sp, data, ability):
    d = data.species[sp]
    out = []
    for m in d['pool']:
        mv = data.moves.get(m)
        if not mv or mv['cat'] == 'STATUS':
            continue
        if mv['effect'] in S.UNUSABLE or m in S.UNUSABLE:
            continue
        if mv['power'] <= 1 and mv['effect'] not in ('LEVEL_DAMAGE', 'FIXED_PERCENT_DAMAGE', 'LOW_KICK', 'GRASS_KNOT', 'RETURN',
                                                       'HEAT_CRASH', 'GYRO_BALL', 'ELECTRO_BALL'):
            continue
        if mv['effect'] in ('SUCKER_PUNCH',) and mv['type'] != 'DARK' and m != 'THUNDERCLAP':
            pass
        if m in ('STRUGGLE', 'CHATTER') or mv['zmove'] if 'zmove' in mv else False:
            continue
        if m.startswith('MAX_') or m.startswith('G_MAX') or any(x['eff'] == 'RECHARGE' for x in mv['adds']):
            continue
        out.append(m)
    # snoeien: per type de 4 sterkste (ruwe waarde)
    def raw(m):
        mv = data.moves[m]
        p = mv['power'] if mv['power'] > 1 else 80
        p *= (mv['acc'] or 100) / 100 * (mv['strikes'] or 1)
        if mv['effect'] == 'MULTI_HIT':
            p *= 3
        if mv['effect'] == 'TRIPLE_KICK':
            p *= 4
        if mv['type'] in d['types']:
            p *= 1.5
        if mv['recoil']:
            p *= 0.9
        if mv['pri'] > 0:
            p *= 1.2
        if any(x['self'] and 'MINUS_2' in x['eff'] for x in mv['adds']):
            p *= 0.85
        return p
    by = {}
    for m in out:
        by.setdefault((data.moves[m]['type'], data.moves[m]['cat']), []).append(m)
    keep = []
    for k, ms in by.items():
        ms.sort(key=raw, reverse=True)
        keep += ms[:3]
        keep += [m for m in ms[3:] if data.moves[m]['pri'] > 0][:1]
    return keep


def coverage(ms, moves, refs, data):
    b = S.Battle([ms], [refs[0]], data, mode='duel')
    att = b.sides[0].mon
    att.moves = moves
    val = 0.0
    for r in refs:
        dfn = S.BMon(r, data)
        best = 0
        for m in moves:
            d = b.exp_dmg(att, dfn, m, b.sides[0], b.sides[1])
            mv = data.moves[m]
            if mv['pri'] > 0:
                d *= 1.1
            best = max(best, d)
        val += min(1.0, best / dfn.maxhp) + 0.15 * min(2.0, best / dfn.maxhp)
    return val / len(refs)


def pick_attacks(ms, cands, k, refs, data):
    chosen = []
    for _ in range(k):
        best, bv = None, -1
        for m in cands:
            if m in chosen:
                continue
            v = coverage(ms, chosen + [m], refs, data)
            if v > bv:
                best, bv = m, v
        if best is None:
            break
        chosen.append(best)
    return chosen


def evs_for(d, role, bulky=False):
    if bulky:
        k = 'def' if d['def'] <= d['spd'] else 'spd'
        if role == 'spec':
            nat = 'BOLD' if k == 'def' else 'CALM'
        else:
            nat = 'IMPISH' if k == 'def' else 'CAREFUL'
        return {'hp': 252, k: 252, 'spa' if role == 'spec' else 'atk': 4}, nat
    a = 'atk' if role == 'phys' else 'spa'
    if d['spe'] < 55:
        return {'hp': 252, a: 252, 'spd': 4}, 'BRAVE' if role == 'phys' else 'QUIET'
    if d['spe'] >= 75:
        return {a: 252, 'spe': 252, 'hp': 4}, 'JOLLY' if role == 'phys' else 'TIMID'
    return {a: 252, 'spe': 252, 'hp': 4}, 'ADAMANT' if role == 'phys' else 'MODEST'


def build_variants(sp, data, ability, refs):
    d = data.species[sp]
    pool = d['pool']
    roles = []
    if d['atk'] >= d['spa'] * 0.87 or ability in ('HUGE_POWER', 'PURE_POWER'):
        roles.append('phys')
    if d['spa'] >= d['atk'] * 0.87 and ability not in ('HUGE_POWER', 'PURE_POWER'):
        roles.append('spec')
    cands_all = attack_candidates(sp, data, ability)
    variants = []
    paradox = ability in ('PROTOSYNTHESIS', 'QUARK_DRIVE')
    for role in roles:
        cat = 'PHYSICAL' if role == 'phys' else 'SPECIAL'
        cands = [m for m in cands_all if data.moves[m]['cat'] == cat or m in ('ECLIPSE',) or
                 data.moves[m]['effect'] in ('LEVEL_DAMAGE', 'FIXED_PERCENT_DAMAGE', 'BODY_PRESS', 'FOUL_PLAY')]
        if not cands:
            continue
        evs, nat = evs_for(d, role)
        base = S.MonSet(sp, ability, '', [], evs, nat)
        atk4 = pick_attacks(base, cands, 4, refs, data)
        # A: Choice/Life Orb-aanvaller
        item = ('CHOICE_BAND' if role == 'phys' else 'CHOICE_SPECS')
        if ability == 'SHEER_FORCE' or ability == 'MAGIC_GUARD':
            item = 'LIFE_ORB'
        if paradox:
            item = 'BOOSTER_ENERGY'
        if ability == 'GUTS':
            item = 'TOXIC_ORB' if 'POISON' in d['types'] or 'STEEL' in d['types'] else 'FLAME_ORB'
        if ability == 'POISON_HEAL':
            item = 'TOXIC_ORB'
        variants.append(('aanvaller', S.MonSet(sp, ability, item, atk4, evs, nat)))
        if 70 <= d['spe'] <= 105 and not paradox:
            evs2, nat2 = evs_for(dict(d, spe=100), role)
            variants.append(('scarf', S.MonSet(sp, ability, 'CHOICE_SCARF', atk4, evs2, nat2)))
        # B: setup
        setups = [m for m in (PHYS_SETUP if role == 'phys' else SPEC_SETUP) if m in pool]
        if setups:
            su = setups[0]
            atk3 = pick_attacks(base, cands, 3, refs, data)
            it = 'LIFE_ORB' if d['spe'] >= 70 or su in ('DRAGON_DANCE', 'SHELL_SMASH', 'BUNNY_HOP') else 'LEFTOVERS'
            if paradox:
                it = 'BOOSTER_ENERGY'
            if su == 'BELLY_DRUM':
                it = 'SITRUS_BERRY'
            if ability in ('GUTS', 'POISON_HEAL'):
                it = variants[-1][1].item
            if su == 'SHELL_SMASH':
                it = 'WHITE_HERB' if False else 'FOCUS_SASH'
            variants.append(('setup', S.MonSet(sp, ability, it, [su] + atk3, evs, nat)))
        # C: bulky
        rec = [m for m in RECOVERY if m in pool]
        dsu = [m for m in DEF_SETUP if m in pool and (m not in ('CALM_MIND',) or role == 'spec')
               and (m not in ('BULK_UP', 'CURSE') or role == 'phys')]
        stat = [m for m in GOOD_STATUS if m in pool]
        if rec and (d['hp'] + d['def'] + d['spd'] >= 250 or ability in ('MULTISCALE', 'REGENERATOR', 'MAGIC_GUARD', 'UNAWARE')):
            evs3, nat3 = evs_for(d, role, bulky=True)
            bp = 'BODY_PRESS' in pool and 'IRON_DEFENSE' in pool
            if bp:
                mvset = ['IRON_DEFENSE', 'BODY_PRESS', rec[0]]
                more = pick_attacks(S.MonSet(sp, ability, '', [], evs3, nat3), [m for m in cands if m != 'BODY_PRESS'], 1, refs, data)
                variants.append(('bulky-bp', S.MonSet(sp, ability, 'LEFTOVERS', mvset + more, evs3, 'BOLD' if role == 'spec' else 'IMPISH')))
            extra = dsu[:1] if dsu else stat[:1]
            if stat and extra != stat[:1]:
                extra2 = stat[:1]
            else:
                extra2 = []
            atk = pick_attacks(S.MonSet(sp, ability, '', [], evs3, nat3), cands, 4 - 1 - len(extra) - len(extra2), refs, data)
            variants.append(('bulky', S.MonSet(sp, ability, 'LEFTOVERS', [rec[0]] + extra + extra2 + atk, evs3, nat3)))
    return variants


def _mask(sp, ms):
    if sp.startswith('OGERPON_'):
        ms.item = sp.split('_', 1)[1] + '_MASK'
    return ms


def score_set(ms, refs, data, n=4, seed=7):
    tot = 0.0
    for i, r in enumerate(refs):
        if r.species == ms.species:
            continue
        tot += S.duel(ms, r, data, n=n, seed=seed + i)
    return tot / max(1, len([r for r in refs if r.species != ms.species]))


def best_set_for(sp, data, refs, abilities, n_quick=2, n_final=10):
    res = {}
    for ab in abilities:
        best, bs, bname = None, -1, None
        for name, ms in build_variants(sp, data, ab, refs):
            if not ms.moves:
                continue
            ms = _mask(sp, ms)
            s = score_set(ms, refs, data, n=n_quick)
            if s > bs:
                best, bs, bname = ms, s, name
        if best is not None:
            res[ab] = (score_set(best, refs, data, n=n_final, seed=101), best, bname)
    return res


def changed_species(cur, van):
    """Soorten met andere stats/types/abilities dan vanilla, of met een eigen (signature) move van deze rom."""
    custom = set(m for m in cur.moves if m not in van.moves)
    out = set()
    for sp, d in cur.species.items():
        v = van.species.get(sp)
        if v is None or any(d[s] != v[s] for s in S.STATS) or d['types'] != v['types'] or d['abilities'] != v['abilities']:
            out.add(sp)
        elif any(m in custom and len([x for x in cur.species.values() if m in x['pool']]) <= 4 for m in d['pool']):
            out.add(sp)
    return out


def candidates(data, extra=(), min_bst=470):
    out = []
    for sp, d in data.species.items():
        if d['nfe'] or d['isMegaEvolution'] or d['isGigantamax'] or d['isTotem'] or d['isPrimalReversion'] or \
           d['isTeraForm'] or d['isUltraBurst'] or SKIP_FORMS.search(sp):
            continue
        bst = sum(d[s] for s in S.STATS)
        if bst < min_bst and sp not in extra:
            continue
        if sp.startswith(('ARCEUS_', 'SILVALLY_', 'UNOWN', 'ALCREMIE', 'MINIOR', 'PIKACHU_', 'VIVILLON_', 'FURFROU_',
                          'FLABEBE', 'FLOETTE_', 'FLORGES_', 'MOTHIM', 'SQUAWKABILLY_', 'TATSUGIRI_', 'GENESECT_',
                          'MAUSHOLD_THREE', 'DUDUNSPARCE_THREE', 'PICHU_', 'XERNEAS_', 'POLTCHAGEIST_', 'SINISTCHA_MASTER',
                          'ZARUDE_', 'MAGEARNA_', 'TOXTRICITY_LOW', 'GIMMIGHOUL', 'BASCULIN', 'SHELLOS', 'GASTRODON_EAST',
                          'BURMY', 'WORMADAM_SANDY', 'WORMADAM_TRASH', 'CHERRIM', 'DEERLING', 'SAWSBUCK_', 'GRENINJA_',
                          'ROCKRUFF', 'ORICORIO_', 'LYCANROC_DUSK', 'WISHIWASHI', 'MIMIKYU_BUSTED', 'CRAMORANT_',
                          'EISCUE_NOICE', 'INDEEDEE_F', 'MORPEKO_HANGRY', 'ZACIAN_CROWNED', 'ETERNATUS_', 'URSHIFU_RAPID',
                          'CALYREX_', 'BASCULEGION_F', 'OINKOLOGNE_F', 'MEOWSTIC_F', 'PYROAR_F', 'NIDORAN', 'UNFEZANT_F',
                          'FRILLISH_F', 'JELLICENT_F', 'HIPPOWDON_F', 'MAGIKARP_', 'GYARADOS_')) and \
           sp not in ('SAWSBUCK_SPRING',):
            if not sp.startswith('MAUSHOLD_FOUR'):
                continue
        out.append(sp)
    return sorted(out)


def _rank_worker(args):
    sp, label, vanilla = args
    data = get_data(label, vanilla)
    if label not in REF_CACHE:
        REF_CACHE[label] = ref_sets(data)[0]
    refs = REF_CACHE[label]
    if sp not in data.species:
        return sp, label, None
    d = data.species[sp]
    abil = [a for a in dict.fromkeys(d['abilities']) if a != 'NONE']
    hidden0 = d['abilities'][2] if len(d['abilities']) > 2 and d['abilities'][2] not in d['abilities'][:2] else None
    mod = [a for a in abil if a in MODELED]
    if not [a for a in mod if a != hidden0]:          # altijd minstens één speler-legale ability
        mod = [a for a in abil if a != hidden0][:1] + mod
    abil = mod or abil[:1]
    hidden = d['abilities'][2] if len(d['abilities']) > 2 and d['abilities'][2] not in d['abilities'][:2] else None
    try:
        res = best_set_for(sp, data, refs, abil)
    except Exception as ex:  # noqa: BLE001
        return sp, label, {'error': repr(ex)}
    out = {}
    for ab, (sc, ms, name) in res.items():
        out[ab] = dict(score=sc, kind=name, hidden=(ab == hidden), set=ms.showdown(data),
                       moves=ms.moves, item=ms.item, evs=ms.evs, nature=ms.nature)
    return sp, label, out


def rank(vanilla, outpath, jobs=4, only=None):
    from multiprocessing import Pool
    cur = get_data('cur')
    van = get_data('van', vanilla)
    chg = changed_species(cur, van)
    sps = only or sorted(set(candidates(cur, chg)) | set(candidates(van, chg)))
    sps = [s for s in sps if s in cur.species or s in van.species]
    tasks = [(s, l, vanilla) for s in sps for l in ('cur', 'van')]
    results = {}
    if os.path.exists(outpath):
        results = json.load(open(outpath))
    tasks = [t for t in tasks if not (t[0] in results and t[1] in results[t[0]])]
    print('taken', len(tasks), file=sys.stderr)
    with Pool(jobs) as p:
        for i, (sp, label, out) in enumerate(p.imap_unordered(_rank_worker, tasks, chunksize=2)):
            results.setdefault(sp, {})[label] = out
            if i % 40 == 0:
                json.dump(results, open(outpath, 'w'))
                print(i, '/', len(tasks), file=sys.stderr)
    json.dump(results, open(outpath, 'w'))
    return results


# =============================================================================================
# teams

def load_teams(path, data):
    txt = open(path).read()
    teams = []
    for block in re.split(r'^=== ', txt, flags=re.M)[1:]:
        title, body = block.split('\n', 1)
        sets = S.parse_showdown(body, data)
        notes = []
        for ms in sets:
            _, n = S.legalize(ms, data, allow_hidden=True)
            notes += ['%s: %s' % (ms.species, x) for x in n]
        teams.append((title.strip(' ='), sets, notes))
    return teams


def round_robin(teams, data, n=40):
    res = {}
    for i, (ti, si, _) in enumerate(teams):
        for j, (tj, sj, _) in enumerate(teams):
            if j <= i:
                continue
            a, _ = S.team_battle(si, sj, data, n=n // 2, seed=11 + i * 31 + j)
            b, _ = S.team_battle(sj, si, data, n=n // 2, seed=17 + i * 31 + j)
            w = (a + (1 - b)) / 2
            res[(ti, tj)] = w
            res[(tj, ti)] = 1 - w
    return res


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return
    cmd = a[0]
    if cmd == 'fetch':
        fetch(a[1])
    elif cmd == 'rank':
        jobs = int(a[a.index('--jobs') + 1]) if '--jobs' in a else 4
        only = a[a.index('--only') + 1].split(',') if '--only' in a else None
        rank(a[1], a[2], jobs, only)
    elif cmd == 'refs':
        for label in ('van', 'cur'):
            data = get_data(label, a[1])
            sets, notes = ref_sets(data)
            REF_CACHE[label] = sets
            print('==', label)
            for ms in sets:
                print('%-22s %s' % (ms.species, '; '.join(notes[ms.species]) or 'ok'))
    elif cmd == 'teams':
        data = get_data('cur')
        REF_CACHE['cur'] = ref_sets(data)[0]
        n = int(a[a.index('--n') + 1]) if '--n' in a else 40
        teams = load_teams(a[1], data)
        for t, s, notes in teams:
            if notes:
                print(t, notes)
        res = round_robin(teams, data, n)
        names = [t for t, _, _ in teams]
        for t in names:
            tot = sum(res[(t, u)] for u in names if u != t) / (len(names) - 1)
            print('%-34s %5.1f%%  ' % (t, 100 * tot) + ' '.join('%3d' % round(100 * res[(t, u)]) if u != t else '  -' for u in names))
    elif cmd == 'duel':
        data = get_data('cur')
        s1 = S.parse_showdown(a[1].replace('\\n', '\n'), data)[0]
        s2 = S.parse_showdown(a[2].replace('\\n', '\n'), data)[0]
        print(S.duel(s1, s2, data, n=100))


if __name__ == '__main__':
    main()
