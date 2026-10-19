#!/usr/bin/env python3
"""OU-achtige gevechtssimulator voor Project Grounded (alleen analyse; verandert geen game-data).

Leest soorten, moves, abilities-namen en learnsets uit de repo (zoals `tools/grounded/spire/spiredata.py`) en,
ter vergelijking, uit een vanilla-checkout van pokeemerald-expansion (alleen de databestanden; zie
`fetch_vanilla()`), met de officiële movepools uit `tools/learnset_helpers/build/all_learnables.json`.

Wat wordt gesimuleerd (singles, lv 100, 31 IV's, EV's/nature per set, geen Tera/Mega/Z/Dynamax):
- schadeformule van Gen 5+ (rol 85-100%, crits met stages, STAB, typetabel uit types_info.h),
  de belangrijkste abilities, items, weer (ook Acid Rain en Pollen Haze van deze rom), terrein via surges,
  Tailwind, Trick Room, schermen, hazards (Stealth Rock/Spikes/Toxic Spikes/Moai Watch), status, verwarring,
  setup-moves, herstel, pivots (U-turn e.d.), Regenerator, Moxie/Beast Boost/Eelevate/Supreme Overlord,
  en de nieuwe effecten van deze rom die er competitief toe doen (zie `CUSTOM` hieronder).
- AI: per beurt kiest elke kant de actie (aanval, setup, herstel, status, hazard, wissel) met de beste
  uitkomst van een snelle 'race'-schatting (wie haalt de ander eerst neer, met welke marge).

Beperkingen: geen voorspellen/mind games, geen Protect-/Substitute-spel, geen Taunt/Encore/Trick,
geen Tera. Uitkomsten zijn bedoeld om te vergelijken (vanilla vs. deze rom), niet als exacte waarheid.

Gebruik (voorbeelden):
  python3 tools/grounded/balance/ousim.py duel "Great Tusk" Kingambit            # 1v1 met referentiesets
  python3 tools/grounded/balance/ousim.py rank --vanilla <map> [--out res.json]   # ranglijst cur vs vanilla
  python3 tools/grounded/balance/ousim.py teams [--n 40]                          # teams tegen elkaar
"""
import copy, glob, json, math, os, random, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
STATS = ('hp', 'atk', 'def', 'spa', 'spd', 'spe')

# =============================================================================================
# data


_COND = re.compile(r'\(?\s*[BP]_UPDATED_\w+\s*>=\s*GEN_\d+(?:\s*\|\|\s*[BP]_UPDATED_\w+\s*==\s*GEN_\d+)?\s*\?\s*([^:,]+?)\s*:\s*[^,)}\n]+\)?')


def _resolve(txt):
    txt = _COND.sub(lambda m: m.group(1), txt)
    # '[X] = // commentaar\n {' -> '[X] = {'
    return re.sub(r'=\s*//[^\n]*\n\s*\{', '= {', txt)


def _read(root, p):
    with open(os.path.join(root, p), encoding='utf-8') as f:
        return _resolve(f.read())


def _blocks(txt, key):
    out = {}
    for m in re.finditer(r'\n    \[%s_(\w+)\]\s*=\s*\{' % key, txt):
        start = m.end()
        end = txt.find('\n    },', start)
        out[m.group(1)] = txt[start:end]
    return out


def _flag(body, f):
    return re.search(r'\.%s\s*=\s*TRUE' % f, body) is not None


def load_moves(root):
    txt = _read(root, 'src/data/moves_info.h')
    out = {}
    for name, body in _blocks(txt, 'MOVE').items():
        def f(field, default=None, conv=str):
            m = re.search(r'\.%s\s*=\s*([^,\n]+)' % field, body)
            if not m:
                return default
            try:
                return conv(m.group(1).strip())
            except ValueError:
                return default
        adds = []
        ai = body.find('ADDITIONAL_EFFECTS(')
        if ai >= 0:
            i, depth = ai + len('ADDITIONAL_EFFECTS('), 1
            while i < len(body) and depth:
                depth += {'(': 1, ')': -1}.get(body[i], 0)
                i += 1
            for g in re.finditer(r'\{([^{}]*)\}', body[ai:i]):
                gm = re.search(r'\.moveEffect\s*=\s*MOVE_EFFECT_(\w+)', g.group(1))
                if not gm:
                    continue
                ch = re.search(r'\.chance\s*=\s*(\d+)', g.group(1))
                adds.append(dict(eff=gm.group(1), self='.self = TRUE' in g.group(1),
                                 chance=int(ch.group(1)) if ch else 0))
        arg = re.search(r'\.argument\s*=\s*\{([^}]*)\}', body)
        argtxt = arg.group(1) if arg else ''
        dname = re.search(r'\.name\s*=\s*COMPOUND_STRING\("([^"]*)"\)', body)
        num = lambda k: int(re.search(r'\.%s\s*=\s*(\d+)' % k, argtxt).group(1)) if re.search(r'\.%s\s*=\s*(\d+)' % k, argtxt) else 0
        argtype = re.search(r'\.type\s*=\s*TYPE_(\w+)', argtxt)
        nvs = re.search(r'nonVolatileStatus\s*=\s*MOVE_EFFECT_(\w+)', argtxt)
        out[name] = dict(
            key=name, name=dname.group(1) if dname else name.title(),
            effect=(f('effect', 'EFFECT_HIT') or 'EFFECT_HIT').replace('EFFECT_', ''),
            power=f('power', 0, int), type=(f('type', 'TYPE_NORMAL') or '').replace('TYPE_', ''),
            acc=f('accuracy', 0, int), pp=f('pp', 0, int), pri=f('priority', 0, int),
            target=(f('target', 'MOVE_TARGET_SELECTED') or '').replace('MOVE_TARGET_', ''),
            cat=(f('category', 'DAMAGE_CATEGORY_STATUS') or '').replace('DAMAGE_CATEGORY_', ''),
            strikes=f('strikeCount', 1, int) or 1, crit=f('criticalHitStage', 0, int) or 0,
            alwaysCrit=_flag(body, 'alwaysCriticalHit'), contact=_flag(body, 'makesContact'),
            sound=_flag(body, 'soundMove'), punch=_flag(body, 'punchingMove'), bite=_flag(body, 'bitingMove'),
            slice=_flag(body, 'slicingMove'), pulse=_flag(body, 'pulseMove'), wind=_flag(body, 'windMove'),
            ball=_flag(body, 'ballisticMove'), powder=_flag(body, 'powderMove'),
            ignoresProtect=_flag(body, 'ignoresProtect'), ignoreDefStages=_flag(body, 'ignoresTargetDefenseEvasionStages'),
            drain=num('absorbPercentage'), recoil=num('recoilPercentage'), pct=num('damagePercentage'),
            argtype=argtype.group(1) if argtype else None, status=nvs.group(1) if nvs else None,
            adds=adds, signature=_flag(body, 'isSignatureMove'),
        )
    return out


def load_typechart(root):
    txt = _read(root, 'src/data/types_info.h')
    types = ['NONE', 'NORMAL', 'FIGHTING', 'FLYING', 'POISON', 'GROUND', 'ROCK', 'BUG', 'GHOST', 'STEEL',
             'MYSTERY', 'FIRE', 'WATER', 'GRASS', 'ELECTRIC', 'PSYCHIC', 'ICE', 'DRAGON', 'DARK', 'FAIRY', 'STELLAR']
    macros = {'______': 1.0, 'STL_RS': 1.0, 'PSN_RS': 0.5, 'BUG_RS': 1.0, 'PSY_RS': 2.0, 'FIR_RS': 0.5}
    chart = {}
    for m in re.finditer(r'\[TYPE_(\w+)\]\s*=\s*\{([^}]*)\}', txt.split('gTypeEffectivenessTable')[1].split('};')[0]):
        vals = []
        for tok in [x.strip() for x in m.group(2).split(',') if x.strip()]:
            x = re.match(r'X\(([\d.]+)\)', tok)
            vals.append(float(x.group(1)) if x else macros[tok])
        chart[m.group(1)] = dict(zip(types, vals))
    return chart


def _movelists(root, path):
    out = {}
    for m in re.finditer(r'static const u16 (\w+)\[\] = \{(.*?)\};', _read(root, path), re.S):
        out[m.group(1)] = [x for x in re.findall(r'MOVE_(\w+)', m.group(2)) if x != 'UNAVAILABLE']
    return out


def _levelup(root):
    out = {}
    for m in re.finditer(r'static const struct LevelUpMove (\w+)\[\] = \{(.*?)\};',
                         _read(root, 'src/data/pokemon/level_up_learnsets/gen_9.h'), re.S):
        out[m.group(1)] = [mv for l, mv in re.findall(r'LEVEL_UP_MOVE\(\s*(\d+),\s*MOVE_(\w+)\)', m.group(2))]
    return out


OGERPON = {'TEAL': ('GRASS', 'DEFIANT'), 'WELLSPRING': ('WATER', 'WATER_ABSORB'),
           'HEARTHFLAME': ('FIRE', 'MOLD_BREAKER'), 'CORNERSTONE': ('ROCK', 'STURDY')}


def load_species(root):
    lvl = _levelup(root)
    teach = _movelists(root, 'src/data/pokemon/teachable_learnsets.h')
    eggs = _movelists(root, 'src/data/pokemon/egg_moves.h')
    files = sorted(glob.glob(os.path.join(root, 'src/data/pokemon/species_info/gen_*_families.h')))
    allsrc = _resolve(''.join(open(p, encoding='utf-8').read() for p in files))
    macros = {}
    for m in re.finditer(r'#define\s+(\w+)[ \t]+(.+)', allsrc):
        if m.group(1) not in macros:
            macros[m.group(1)] = re.sub(r'^\((\d+)\)$', r'\1', m.group(2).strip())
    out = {}
    for path in files:
        txt = _resolve(open(path, encoding='utf-8').read())
        for name, body in _blocks(txt, 'SPECIES').items():
            body = re.sub(r'\b[A-Z][A-Z0-9_]+\b', lambda m: macros.get(m.group(0), m.group(0)), body)
            d = {}
            ok = True
            for key, field in (('hp', 'baseHP'), ('atk', 'baseAttack'), ('def', 'baseDefense'),
                               ('spe', 'baseSpeed'), ('spa', 'baseSpAttack'), ('spd', 'baseSpDefense')):
                fm = re.search(r'\.%s\s*=\s*(\d+)' % field, body)
                if not fm:
                    ok = False
                    break
                d[key] = int(fm.group(1))
            t = re.search(r'(?:MON_TYPES\(|\.types\s*=\s*\{\s*)TYPE_(\w+)(?:,\s*TYPE_(\w+))?\s*[)}]', body)
            if not ok or not t:
                continue
            d['types'] = [t.group(1)] + ([t.group(2)] if t.group(2) and t.group(2) != t.group(1) else [])
            ab = re.search(r'\.abilities\s*=\s*\{([^}]*)\}', body)
            d['abilities'] = [a.replace('ABILITY_', '') for a in re.findall(r'ABILITY_\w+', ab.group(1))] if ab else []
            w = re.search(r'\.weight\s*=\s*(\d+)', body)
            d['weight'] = int(w.group(1)) if w else 500
            dn = re.search(r'\.speciesName\s*=\s*_\("([^"]*)"\)', body)
            d['dispname'] = dn.group(1) if dn else name.title()
            d['evos'] = re.findall(r'SPECIES_(\w+)', body[body.find('.evolutions'):body.find('.evolutions') + 600]) \
                if '.evolutions' in body else []
            for fl in ('isLegendary', 'isMythical', 'isParadox', 'isMegaEvolution', 'isGigantamax', 'isTotem',
                       'isPrimalReversion', 'isTeraForm', 'isUltraBurst'):
                d[fl] = _flag(body, fl)
            lu = re.search(r'\.levelUpLearnset\s*=\s*(\w+)', body)
            te = re.search(r'\.teachableLearnset\s*=\s*(\w+)', body)
            em = re.search(r'\.eggMoveLearnset\s*=\s*(\w+)', body)
            d['lv'] = set(lvl.get(lu.group(1), [])) if lu else set()
            d['tm'] = set(teach.get(te.group(1), [])) if te else set()
            d['egg'] = set(eggs.get(em.group(1), [])) if em else set()
            out[name] = d
    # Ogerpon staat als macro in gen_9_families.h
    for form, (ty, ab) in OGERPON.items():
        out['OGERPON_' + form] = dict(hp=80, atk=120, **{'def': 84}, spa=60, spd=96, spe=110,
                                      types=['GRASS'] + ([ty] if ty != 'GRASS' else []), abilities=[ab, 'NONE', 'NONE'],
                                      weight=398, dispname='Ogerpon-' + form.title(), evos=[], isLegendary=False,
                                      isMythical=False, isParadox=False, isMegaEvolution=False, isGigantamax=False,
                                      isTotem=False, isPrimalReversion=False, isTeraForm=False, isUltraBurst=False,
                                      lv=set(lvl.get('sOgerponLevelUpLearnset', [])),
                                      tm=set(teach.get('sOgerponTeachableLearnset', [])), egg=set())
    # voorgangers (egg moves en level-up van de voorganger zijn ook te leren)
    pre = {}
    for n, d in out.items():
        for e in d['evos']:
            if e in out and e != n:
                pre.setdefault(e, n)
    for n, d in out.items():
        pool = set(d['lv']) | d['tm'] | d['egg']
        c, seen = n, set()
        while c in pre and c not in seen:
            seen.add(c)
            c = pre[c]
            pool |= out[c]['lv'] | out[c]['egg'] | out[c]['tm']
        d['pool'] = pool
        d['nfe'] = any(e in out and e != n and not out[e]['isMegaEvolution'] and not out[e]['isGigantamax']
                       for e in d['evos'])
    return out


class Data:
    """Eén dataset: 'cur' = deze repo, 'van' = vanilla expansion met officiële movepools."""

    def __init__(self, root=ROOT, official_learnsets=None, label='cur'):
        self.label = label
        self.root = root
        self.moves = load_moves(root)
        self.chart = load_typechart(root)
        self.species = load_species(root)
        alias = {}
        for f in (os.path.join(root, 'include/constants/moves.h'), os.path.join(ROOT, 'include/constants/moves.h')):
            if os.path.exists(f):
                for a, b in re.findall(r'#define MOVE_(\w+)\s+MOVE_(\w+)', open(f, encoding='utf-8').read()):
                    alias.setdefault(a, b)
        self.alias = alias
        for d in self.species.values():
            d['pool'] = set(alias.get(m, m) for m in d['pool'])
            d['pool'] = set(m for m in d['pool'] if m in self.moves)
        if not official_learnsets:
            # universele moves van expansion (CanLearnTeachableMove): Return als TM27, Substitute
            for d in self.species.values():
                d['pool'] |= {'RETURN', 'SUBSTITUTE'}
        if official_learnsets:
            al = json.load(open(official_learnsets))
            for n, d in self.species.items():
                key = n
                while key and key not in al:
                    key = key.rsplit('_', 1)[0] if '_' in key else None
                if key:
                    off = set(alias.get(x.replace('MOVE_', ''), x.replace('MOVE_', '')) for x in al[key])
                    d['pool'] = d['pool'] | set(m for m in off if m in self.moves)
                d['pool'] -= {'RETURN', 'FRUSTRATION', 'HIDDEN_POWER'}   # niet in Gen 9
        for f, m in (('ROTOM_WASH', 'HYDRO_PUMP'), ('ROTOM_HEAT', 'OVERHEAT'), ('ROTOM_FROST', 'BLIZZARD'),
                     ('ROTOM_FAN', 'AIR_SLASH'), ('ROTOM_MOW', 'LEAF_STORM')):
            if f in self.species:     # vormwissel leert de signature move
                self.species[f]['pool'].add(m)
        self._sp_idx = {}
        for k, d in self.species.items():
            self._sp_idx.setdefault(norm(k), k)
            self._sp_idx.setdefault(norm(d['dispname']), k)
        self._mv_idx = {}
        for k, m in self.moves.items():
            self._mv_idx.setdefault(norm(m['name']), k)
            self._mv_idx.setdefault(norm(k), k)

    def sp(self, name):
        n = norm(name)
        alias = {'LANDORUST': 'LANDORUS_THERIAN', 'LANDORUSTHERIAN': 'LANDORUS_THERIAN', 'ZAMAZENTA': 'ZAMAZENTA_HERO',
                 'SAMUROTTH': 'SAMUROTT_HISUI', 'SAMUROTTHISUI': 'SAMUROTT_HISUI', 'SLOWKINGG': 'SLOWKING_GALAR',
                 'SLOWKINGGALAR': 'SLOWKING_GALAR', 'ROTOMW': 'ROTOM_WASH', 'ROTOMWASH': 'ROTOM_WASH',
                 'URSALUNABLOODMOON': 'URSALUNA_BLOODMOON', 'OGERPONWELLSPRING': 'OGERPON_WELLSPRING',
                 'OGERPONHEARTHFLAME': 'OGERPON_HEARTHFLAME', 'OGERPONCORNERSTONE': 'OGERPON_CORNERSTONE',
                 'OGERPON': 'OGERPON_TEAL', 'TORNADUST': 'TORNADUS_THERIAN', 'ENAMORUS': 'ENAMORUS_INCARNATE',
                 'MIMIKYU': 'MIMIKYU_DISGUISED', 'SINISTCHA': 'SINISTCHA_UNREMARKABLE', 'NINETALESALOLA': 'NINETALES_ALOLA',
                 'MUKALOLA': 'MUK_ALOLA', 'MOLTRESGALAR': 'MOLTRES_GALAR', 'WEEZINGGALAR': 'WEEZING_GALAR',
                 'ZAPDOSGALAR': 'ZAPDOS_GALAR', 'GOODRAHISUI': 'GOODRA_HISUI', 'ARCANINEHISUI': 'ARCANINE_HISUI',
                 'TYPHLOSIONHISUI': 'TYPHLOSION_HISUI', 'DECIDUEYEHISUI': 'DECIDUEYE_HISUI', 'THUNDURUST': 'THUNDURUS_THERIAN',
                 'INDEEDEE': 'INDEEDEE_M', 'BASCULEGION': 'BASCULEGION_M', 'MAUSHOLD': 'MAUSHOLD_FOUR',
                 'TAUROSPALDEAAQUA': 'TAUROS_PALDEA_AQUA', 'TAUROSPALDEABLAZE': 'TAUROS_PALDEA_BLAZE',
                 'TAUROSPALDEACOMBAT': 'TAUROS_PALDEA_COMBAT', 'LYCANROC': 'LYCANROC_MIDDAY', 'TOXTRICITY': 'TOXTRICITY_AMPED',
                 'URSHIFU': 'URSHIFU_SINGLE_STRIKE', 'URSHIFURAPIDSTRIKE': 'URSHIFU_RAPID_STRIKE', 'PALAFIN': 'PALAFIN_HERO',
                 'GRIMERHOENN': 'GRIMER_HOENN', 'MUKHOENN': 'MUK_HOENN', 'CASTFORM': 'CASTFORM_NORMAL',
                 'EISCUE': 'EISCUE_ICE', 'DUDUNSPARCE': 'DUDUNSPARCE_TWO_SEGMENT', 'SQUAWKABILLY': 'SQUAWKABILLY_GREEN',
                 'GIRATINA': 'GIRATINA_ALTERED', 'DEOXYS': 'DEOXYS_NORMAL', 'WORMADAM': 'WORMADAM_PLANT',
                 'MEOWSTIC': 'MEOWSTIC_M', 'GOURGEIST': 'GOURGEIST_AVERAGE', 'ORICORIO': 'ORICORIO_BAILE',
                 'WISHIWASHI': 'WISHIWASHI_SOLO', 'MORPEKO': 'MORPEKO_FULL_BELLY', 'OINKOLOGNE': 'OINKOLOGNE_M',
                 'KELDEO': 'KELDEO_ORDINARY', 'MELOETTA': 'MELOETTA_ARIA', 'ZYGARDE': 'ZYGARDE_50', 'SHAYMIN': 'SHAYMIN_LAND',
                 'HOOH': 'HO_OH', 'MRRIME': 'MR_RIME', 'TAPUKOKO': 'TAPU_KOKO', 'TAPULELE': 'TAPU_LELE', 'TAPUFINI': 'TAPU_FINI',
                 'TAPUBULU': 'TAPU_BULU', 'FARFETCHD': 'FARFETCHD', 'STUNFISKGALAR': 'STUNFISK_GALAR'}
        if n in alias and alias[n] in self.species:
            return alias[n]
        for cand in (n, n + 'NORMAL', n + 'MALE', n + 'M', n + 'INCARNATE', n + 'ALTERED', n + 'AVERAGE'):
            if cand in self._sp_idx:
                return self._sp_idx[cand]
        return None

    def mv(self, name):
        return self._mv_idx.get(norm(name))

    def eff(self, mtype, types):
        m = 1.0
        for t in types:
            m *= self.chart.get(mtype, {}).get(t, 1.0)
        return m


def norm(s):
    return re.sub(r'[^A-Z0-9]', '', s.upper().replace('É', 'E'))


# =============================================================================================
# sets

NATURES = {  # naam: (+, -)
    'ADAMANT': ('atk', 'spa'), 'JOLLY': ('spe', 'spa'), 'MODEST': ('spa', 'atk'), 'TIMID': ('spe', 'atk'),
    'BOLD': ('def', 'atk'), 'IMPISH': ('def', 'spa'), 'CALM': ('spd', 'atk'), 'CAREFUL': ('spd', 'spa'),
    'RELAXED': ('def', 'spe'), 'SASSY': ('spd', 'spe'), 'BRAVE': ('atk', 'spe'), 'QUIET': ('spa', 'spe'),
    'NAIVE': ('spe', 'spd'), 'HASTY': ('spe', 'def'), 'LONELY': ('atk', 'def'), 'MILD': ('spa', 'def'),
    'RASH': ('spa', 'spd'), 'NAUGHTY': ('atk', 'spd'), 'LAX': ('def', 'spd'), 'GENTLE': ('spd', 'def'),
    'HARDY': (None, None), 'SERIOUS': (None, None),
}


class MonSet:
    def __init__(self, species, ability, item, moves, evs=None, nature='HARDY', name=None, note=''):
        self.species, self.ability, self.item = species, ability, (item or '').upper().replace(' ', '_').replace('-', '_')
        self.moves = list(moves)
        self.evs = evs or {}
        self.nature = nature.upper()
        self.name = name or species
        self.note = note

    def stats(self, data):
        d = data.species[self.species]
        plus, minus = NATURES.get(self.nature, (None, None))
        out = {}
        for s in STATS:
            ev = self.evs.get(s, 0)
            if s == 'hp':
                out[s] = 1 if self.species == 'SHEDINJA' else (2 * d['hp'] + 31 + ev // 4) + 100 + 10
            else:
                v = (2 * d[s] + 31 + ev // 4) + 5
                if plus == s:
                    v = int(v * 1.1)
                elif minus == s:
                    v = int(v * 0.9)
                out[s] = v
        return out

    def showdown(self, data, comment=''):
        d = data.species[self.species]
        mvn = [data.moves[m]['name'] if m in data.moves else m for m in self.moves]
        it = self.item.replace('_', ' ').title() if self.item else ''
        evs = ' / '.join('%d %s' % (v, {'hp': 'HP', 'atk': 'Atk', 'def': 'Def', 'spa': 'SpA', 'spd': 'SpD', 'spe': 'Spe'}[k])
                         for k, v in self.evs.items() if v)
        s = '%s%s\nAbility: %s\nEVs: %s\n%s Nature\n' % (d['dispname'], (' @ ' + it) if it else '',
                                                          self.ability.replace('_', ' ').title(), evs, self.nature.title())
        s += ''.join('- %s\n' % m for m in mvn)
        return s


def parse_showdown(text, data):
    """Showdown-export -> lijst MonSet. Onbekende moves worden None (later aangevuld)."""
    sets = []
    for chunk in [c.strip() for c in re.split(r'\n\s*\n', text.strip()) if c.strip()]:
        lines = [l.strip() for l in chunk.split('\n') if l.strip()]
        head = lines[0]
        item = ''
        if '@' in head:
            head, item = [x.strip() for x in head.split('@', 1)]
        head = re.sub(r'\s*\((M|F)\)\s*$', '', head)
        sp = data.sp(head)
        if not sp:
            raise ValueError('onbekende soort: ' + head)
        ab, evs, nat, moves = None, {}, 'HARDY', []
        for l in lines[1:]:
            if l.startswith('Ability:'):
                ab = norm(l.split(':', 1)[1]).replace('', '')
                ab = l.split(':', 1)[1].strip().upper().replace(' ', '_').replace('-', '_').replace("'", '')
            elif l.startswith('EVs:'):
                for part in l[4:].split('/'):
                    v, k = part.split()
                    evs[{'HP': 'hp', 'ATK': 'atk', 'DEF': 'def', 'SPA': 'spa', 'SPD': 'spd', 'SPE': 'spe'}[k.upper()]] = int(v)
            elif l.endswith('Nature'):
                nat = l.split()[0]
            elif l.startswith('-'):
                moves.append(data.mv(l[1:].strip()) or ('?' + l[1:].strip()))
        sets.append(MonSet(sp, ab or data.species[sp]['abilities'][0], item, moves, evs, nat, name=head))
    return sets


def legalize(ms, data, allow_hidden=True):
    """Controleert leerbaarheid en ability; geeft (set, opmerkingen). Niet-leerbare moves gaan eruit."""
    d = data.species[ms.species]
    notes = []
    abil = [a for a in d['abilities'] if a != 'NONE']
    if ms.ability not in d['abilities']:
        notes.append('ability %s bestaat niet (%s)' % (ms.ability, '/'.join(abil)))
        ms.ability = abil[0]
    elif not allow_hidden and len(d['abilities']) > 2 and d['abilities'][2] == ms.ability and ms.ability not in d['abilities'][:2]:
        notes.append('verborgen ability %s' % ms.ability)
    keep = []
    for m in ms.moves:
        if m is None or m.startswith('?') or m not in data.moves:
            notes.append('move %s bestaat niet' % m)
        elif m not in d['pool']:
            notes.append('%s niet leerbaar' % data.moves[m]['name'])
        else:
            keep.append(m)
    ms.moves = keep
    return ms, notes


# =============================================================================================
# engine

STAGE = {i: (max(2, 2 + i) / max(2, 2 - i)) for i in range(-6, 7)}
ACC_STAGE = {i: (max(3, 3 + i) / max(3, 3 - i)) for i in range(-6, 7)}
CRIT_CHANCE = [1 / 24, 1 / 8, 1 / 2, 1, 1]
ATE = {'PIXILATE': 'FAIRY', 'REFRIGERATE': 'ICE', 'AERILATE': 'FLYING', 'GALVANIZE': 'ELECTRIC'}
TYPE_ITEMS = {'CHARCOAL': 'FIRE', 'MYSTIC_WATER': 'WATER', 'MAGNET': 'ELECTRIC', 'MIRACLE_SEED': 'GRASS',
              'NEVER_MELT_ICE': 'ICE', 'BLACK_BELT': 'FIGHTING', 'POISON_BARB': 'POISON', 'SOFT_SAND': 'GROUND',
              'SHARP_BEAK': 'FLYING', 'TWISTED_SPOON': 'PSYCHIC', 'SILVER_POWDER': 'BUG', 'HARD_STONE': 'ROCK',
              'SPELL_TAG': 'GHOST', 'DRAGON_FANG': 'DRAGON', 'BLACK_GLASSES': 'DARK', 'METAL_COAT': 'STEEL',
              'SILK_SCARF': 'NORMAL', 'FAIRY_FEATHER': 'FAIRY'}
MOLD_BREAKERS = {'MOLD_BREAKER', 'TERAVOLT', 'TURBOBLAZE'}
BREAKABLE = {'LEVITATE', 'EELEVATE', 'VOLT_ABSORB', 'WATER_ABSORB', 'STORM_DRAIN', 'LIGHTNING_ROD', 'MOTOR_DRIVE',
             'SAP_SIPPER', 'FLASH_FIRE', 'EARTH_EATER', 'WELL_BAKED_BODY', 'DRY_SKIN', 'MULTISCALE', 'FILTER',
             'SOLID_ROCK', 'THICK_FAT', 'FLUFFY', 'ICE_SCALES', 'FUR_COAT', 'HEATPROOF', 'WATER_BUBBLE',
             'PURIFYING_SALT', 'STURDY', 'DISGUISE', 'MARVEL_SCALE', 'UNAWARE', 'WONDER_GUARD', 'BULLETPROOF',
             'SOUNDPROOF', 'AURA_GUARD', 'PUNK_ROCK', 'WIND_RIDER', 'GOOD_AS_GOLD', 'OVERCOAT', 'FAKE_FOLIAGE',
             'MAGIC_BOUNCE', 'ARMOR_TAIL', 'QUEENLY_MAJESTY', 'DAZZLING', 'TELEPATHY', 'OBLIVIOUS', 'OWN_TEMPO',
             'INSOMNIA', 'VITAL_SPIRIT', 'IMMUNITY', 'LIMBER', 'WATER_VEIL', 'CLEAR_BODY', 'SHIELD_DUST', 'BATTLE_ARMOR',
             'SHELL_ARMOR', 'LEAF_GUARD', 'FRIEND_GUARD', 'PRISM_ARMOR'}
SETUP = {  # move: boosts (zelf)
    'SWORDS_DANCE': {'atk': 2}, 'DRAGON_DANCE': {'atk': 1, 'spe': 1}, 'BUNNY_HOP': {'atk': 1, 'spe': 1},
    'SHELL_SMASH': {'atk': 2, 'spa': 2, 'spe': 2, 'def': -1, 'spd': -1}, 'QUIVER_DANCE': {'spa': 1, 'spd': 1, 'spe': 1},
    'NASTY_PLOT': {'spa': 2}, 'CALM_MIND': {'spa': 1, 'spd': 1}, 'BULK_UP': {'atk': 1, 'def': 1},
    'AGILITY': {'spe': 2}, 'ROCK_POLISH': {'spe': 2}, 'SHIFT_GEAR': {'atk': 1, 'spe': 2}, 'COIL': {'atk': 1, 'def': 1, 'acc': 1},
    'HONE_CLAWS': {'atk': 1, 'acc': 1}, 'GROWTH': {'atk': 1, 'spa': 1}, 'TAIL_GLOW': {'spa': 3},
    'VICTORY_DANCE': {'atk': 1, 'def': 1, 'spe': 1}, 'TIDY_UP': {'atk': 1, 'spe': 1}, 'BELLY_DRUM': {'atk': 6},
    'CURSE': {'atk': 1, 'def': 1, 'spe': -1}, 'WORK_UP': {'atk': 1, 'spa': 1}, 'FILLET_AWAY': {'atk': 2, 'spa': 2, 'spe': 2},
    'CLANGOROUS_SOUL': {'atk': 1, 'def': 1, 'spa': 1, 'spd': 1, 'spe': 1}, 'NO_RETREAT': {'atk': 1, 'def': 1, 'spa': 1, 'spd': 1, 'spe': 1},
    'AUTOTOMIZE': {'spe': 2}, 'IRON_DEFENSE': {'def': 2}, 'ACID_ARMOR': {'def': 2}, 'AMNESIA': {'spd': 2},
    'COSMIC_POWER': {'def': 1, 'spd': 1}, 'DEFEND_ORDER': {'def': 1, 'spd': 1}, 'STOCKPILE': {'def': 1, 'spd': 1},
    'BEAVER_DAM': {'def': 1, 'spd': 1}, 'PRIMEVAL_WARD': {'def': 1, 'spd': 1}, 'PACK_HOWL': {'atk': 1, 'spe': 1},
    'MACHINE_LEARNING': {}, 'THE_OLD_DAYS': {'spa': 1}, 'SHELTER': {'def': 2},
}
HEAL = {'RECOVER': .5, 'SLACK_OFF': .5, 'SOFT_BOILED': .5, 'MILK_DRINK': .5, 'ROOST': .5, 'HEAL_ORDER': .5,
        'MOONLIGHT': .5, 'MORNING_SUN': .5, 'SYNTHESIS': .5, 'SHORE_UP': .5, 'OLIVE_OIL': .5, 'LUNAR_BLESSING': .25,
        'LIFE_DEW': .25, 'JUNGLE_HEALING': .25, 'WISH': .5, 'REST': 1.0, 'STRENGTH_SAP': 0}
STATUS_MOVES = {'WILL_O_WISP': 'BURN', 'TOXIC': 'TOXIC', 'THUNDER_WAVE': 'PARALYSIS', 'GLARE': 'PARALYSIS',
                'STUN_SPORE': 'PARALYSIS', 'SPORE': 'SLEEP', 'SLEEP_POWDER': 'SLEEP', 'HYPNOSIS': 'SLEEP',
                'LOVELY_KISS': 'SLEEP', 'SING': 'SLEEP', 'GRASS_WHISTLE': 'SLEEP', 'DARK_VOID': 'SLEEP',
                'POISON_POWDER': 'POISON', 'YAWN': 'YAWN', 'THE_OLD_DAYS': 'YAWN', 'VENOM_DUST': 'POISON',
                'TOXIC_THREAD': 'POISON', 'POISON_GAS': 'POISON'}
WEATHER_MOVES = {'RAIN_DANCE': 'RAIN', 'SUNNY_DAY': 'SUN', 'SANDSTORM': 'SAND', 'SNOWSCAPE': 'SNOW', 'HAIL': 'SNOW',
                 'ACID_RAIN': 'ACID', 'POLLEN_HAZE': 'POLLEN', 'CHILLY_RECEPTION': 'SNOW'}
WEATHER_ABIL = {'DRIZZLE': 'RAIN', 'DROUGHT': 'SUN', 'SAND_STREAM': 'SAND', 'SNOW_WARNING': 'SNOW',
                'AIR_POLLUTION': 'ACID', 'POLLEN_SEASON': 'POLLEN', 'ORICHALCUM_PULSE': 'SUN', 'DESOLATE_LAND': 'SUN',
                'PRIMORDIAL_SEA': 'RAIN'}
WEATHER_ROCK = {'RAIN': 'DAMP_ROCK', 'SUN': 'HEAT_ROCK', 'SAND': 'SMOOTH_ROCK', 'SNOW': 'ICY_ROCK',
                'POLLEN': 'SILVER_POWDER', 'ACID': 'BLACK_SLUDGE'}
TERRAIN_ABIL = {'ELECTRIC_SURGE': 'ELECTRIC', 'PSYCHIC_SURGE': 'PSYCHIC', 'GRASSY_SURGE': 'GRASSY', 'MISTY_SURGE': 'MISTY',
                'HADRON_ENGINE': 'ELECTRIC', 'SEED_SOWER': 'GRASSY'}
HAZARD_MOVES = {'STEALTH_ROCK': 'sr', 'SPIKES': 'spikes', 'TOXIC_SPIKES': 'tspikes', 'MOAI_WATCH': 'moai', 'STICKY_WEB': 'web'}
PIVOT = {'U_TURN', 'VOLT_SWITCH', 'FLIP_TURN', 'PARTING_SHOT', 'TELEPORT', 'SHED_TAIL', 'CHILLY_RECEPTION'}
PHAZE = {'ROAR', 'WHIRLWIND', 'DRAGON_TAIL', 'CIRCLE_THROW', 'IPPON', 'ABDUCTION'}
UNUSABLE = {'EXPLOSION', 'MISTY_EXPLOSION', 'OHKO', 'RECHARGE', 'TWO_TURNS_ATTACK', 'FUTURE_SIGHT', 'FOCUS_PUNCH',
            'BIDE', 'COUNTER', 'MIRROR_COAT', 'METAL_BURST', 'SKY_DROP', 'SHELL_TRAP', 'BEAT_UP', 'FINAL_GAMBIT',
            'SNORE', 'LAST_RESORT', 'SYNCHRONOISE', 'ROLLOUT', 'FURY_CUTTER', 'UPPER_HAND', 'POLTERGEIST',
            'BELCH', 'SPIT_UP', 'MIND_BLOWN', 'MEMENTO', 'DREAM_EATER', 'FIRST_TURN_ONLY', 'FAKE_OUT', 'NATURAL_GIFT',
            'FLING', 'HIDDEN_POWER', 'METEOR_BEAM', 'SOLAR_BEAM', 'GEOMANCY', 'ELECTRO_SHOT', 'PRESENT', 'MAGNITUDE',
            'SPIT_UP', 'STEEL_BEAM', 'ENDEAVOR', 'PSYWAVE', 'COUNTERFEIT_BALL', 'SUPER_SPLASH', 'TRANSMUTATION',
            'FUNGAL_CONTROL', 'PRAISE_HELIX', 'IMPLOSION', 'MARIONETTE', 'INNARD_PUNCH', 'MIMIC_SHADE', 'TUSK_TUMBLE',
            'WEATHER_REPORT', 'BURROW_MAZE', 'NINE_LIVES', 'TOTEM_GAZE_X', 'SEMI_INVULNERABLE',
            'UPROAR', 'SKY_DROP'}


class Side:
    def __init__(self, team, name):
        self.team = team          # lijst BMon
        self.name = name
        self.active = 0
        self.haz = dict(sr=0, spikes=0, tspikes=0, moai=0, web=0)
        self.tailwind = 0
        self.reflect = 0
        self.lscreen = 0
        self.veil = 0
        self.switches = 0
        self.fainted = 0
        self.wish = None

    @property
    def mon(self):
        return self.team[self.active]

    def alive(self):
        return [i for i, m in enumerate(self.team) if m.hp > 0]


class BMon:
    def __init__(self, ms, data):
        self.set = ms
        self.data = data
        self.d = data.species[ms.species]
        self.st = ms.stats(data)
        self.maxhp = self.st['hp']
        self.hp = self.maxhp
        self.item = ms.item
        self.ability = ms.ability
        self.status = None
        self.tox = 0
        self.slp = 0
        self.reset_volatile()
        self.moves = [m for m in ms.moves if m in data.moves]
        self.nine_lives = 'NINE_LIVES' in self.moves
        self.disguise = self.ability == 'DISGUISE'
        self.lost_item = False
        self.hits_taken = 0
        self.ate_ice_face = self.ability == 'ICE_FACE'

    def reset_volatile(self):
        self.boosts = dict(atk=0, defn=0, spa=0, spd=0, spe=0, acc=0, eva=0)
        self.conf = 0
        self.lock = None          # Choice-lock
        self.protean = False
        self.yawn = 0
        self.seeded = False
        self.salt = False
        self.trap = 0
        self.trapdmg = 0
        self.flashfire = False
        self.charge = False
        self.proto = None
        self.turns = 0
        self.last = None
        self.streak = 0
        self.ml = 0
        self.gaze = False
        self.burrow = 0
        self.ward = False
        self.types = list(self.d['types'])
        self.mummy = False
        self.unburden = False
        self.kelp = 0
        self.pitcher = False
        self.sub = 0
        self.thrash = 0

    @property
    def name(self):
        return self.d['dispname']

    def abil(self, ign=False):
        if self.mummy:
            return 'MUMMY'
        if ign and self.ability in BREAKABLE:
            return 'NONE'
        return self.ability

    def frac(self):
        return self.hp / self.maxhp


class Field:
    def __init__(self):
        self.weather = None
        self.wturns = 0
        self.terrain = None
        self.tturns = 0
        self.tr = 0
        self.harsh = None


class Battle:
    def __init__(self, team1, team2, data, rng=None, log=False, mode='team'):
        self.data = data
        self.rng = rng or random.Random()
        self.sides = [Side([BMon(s, data) for s in team1], 'A'), Side([BMon(s, data) for s in team2], 'B')]
        self.f = Field()
        self.turn = 0
        self.log = [] if log else None
        self.mode = mode
        self.choice_cache = {}

    # ---------------------------------------------------------------- helpers
    def L(self, *a):
        if self.log is not None:
            self.log.append(' '.join(str(x) for x in a))

    def foe(self, side):
        return self.sides[1 - self.sides.index(side)]

    def weather(self):
        """Actief weer, rekening houdend met Cloud Nine/Air Lock."""
        for s in self.sides:
            if s.mon.hp > 0 and s.mon.abil() in ('CLOUD_NINE', 'AIR_LOCK'):
                return None
        return self.f.weather

    def grounded(self, m):
        if 'FLYING' in m.types or m.abil() in ('LEVITATE', 'EELEVATE') or m.item == 'AIR_BALLOON':
            return False
        return True

    def speed(self, m, side):
        s = m.st['spe'] * STAGE[max(-6, min(6, m.boosts['spe']))]
        w = self.weather()
        a = m.abil()
        if m.item == 'CHOICE_SCARF':
            s *= 1.5
        if m.item == 'IRON_BALL':
            s *= 0.5
        if (a == 'SWIFT_SWIM' and w == 'RAIN') or (a == 'CHLOROPHYLL' and w == 'SUN') or \
           (a == 'SAND_RUSH' and w == 'SAND') or (a == 'SLUSH_RUSH' and w == 'SNOW'):
            s *= 2
        elif w == 'POLLEN' and 'BUG' in m.types:
            s *= 2
        if a == 'SURGE_SURFER' and self.f.terrain == 'ELECTRIC':
            s *= 2
        if a == 'QUICK_FEET' and m.status:
            s *= 1.5
        elif m.status == 'PARALYSIS':
            s *= 0.5
        if a == 'UNBURDEN' and m.unburden:
            s *= 2
        if a == 'SLOW_START' and m.turns < 5:
            s *= 0.5
        if m.proto == 'spe':
            s *= 1.5
        if side.tailwind:
            s *= 2
        return s

    def stat(self, m, key, crit=False, ign_boost=False, att=True, side=None, other=None):
        """Effectieve stat voor schade. key in atk/def/spa/spd (def heet intern 'defn' voor boosts)."""
        base = m.st['def' if key == 'def' else key]
        bk = 'defn' if key == 'def' else key
        stg = 0 if ign_boost else m.boosts[bk]
        if crit:
            stg = max(stg, 0) if att else min(stg, 0)
        v = base * STAGE[max(-6, min(6, stg))]
        a = m.abil()
        it = m.item
        w = self.weather()
        if key == 'atk':
            if a == 'SLOW_START' and m.turns < 5:
                v *= 0.5
            if a in ('HUGE_POWER', 'PURE_POWER'):
                v *= 2
            if a == 'GUTS' and m.status:
                v *= 1.5
            if a == 'HUSTLE':
                v *= 1.5
            if it == 'CHOICE_BAND':
                v *= 1.5
            if a == 'GORILLA_TACTICS':
                v *= 1.5
        if key == 'spa':
            if it == 'CHOICE_SPECS':
                v *= 1.5
            if a == 'SOLAR_POWER' and w == 'SUN':
                v *= 1.5
        if key == 'def':
            if a == 'FUR_COAT':
                v *= 2
            if a == 'MARVEL_SCALE' and m.status:
                v *= 1.5
            if w == 'SNOW' and 'ICE' in m.types:
                v *= 1.5
            if w == 'ACID' and 'POISON' in m.types:
                v *= 1.5
            if it == 'EVIOLITE' and m.d['nfe']:
                v *= 1.5
        if key == 'spd':
            if it == 'ASSAULT_VEST':
                v *= 1.5
            if w == 'SAND' and 'ROCK' in m.types:
                v *= 1.5
            if it == 'EVIOLITE' and m.d['nfe']:
                v *= 1.5
        if m.proto == key:
            v *= 1.3
        if a == 'FLOWER_GIFT' and w == 'SUN' and key in ('atk', 'spd'):
            v *= 1.5
        # Ruin-abilities van de ander
        if other is not None and other.hp > 0:
            oa = other.abil()
            if (oa == 'SWORD_OF_RUIN' and key == 'def') or (oa == 'BEADS_OF_RUIN' and key == 'spd') or \
               (oa == 'TABLETS_OF_RUIN' and key == 'atk') or (oa == 'VESSEL_OF_RUIN' and key == 'spa'):
                v *= 0.75
        return v

    # ---------------------------------------------------------------- type & kracht
    def move_type(self, att, mk):
        mv = self.data.moves[mk]
        t = mv['type']
        a = att.abil()
        w = self.weather()
        e = mv['effect']
        if e == 'WEATHER_BALL' and w:
            t = {'RAIN': 'WATER', 'SUN': 'FIRE', 'SAND': 'ROCK', 'SNOW': 'ICE', 'ACID': 'POISON', 'POLLEN': 'BUG'}.get(w, t)
        if e == 'IVY_CUDGEL':
            t = att.types[-1]
        if e in ('REVELATION_DANCE',):
            t = att.types[0]
        if mk == 'ECLIPSE':
            t = 'ROCK' if att.st['atk'] > att.st['spa'] else 'PSYCHIC'
        if mk == 'AFRO_CHARGE' and self.f.terrain:
            t = {'ELECTRIC': 'ELECTRIC', 'GRASSY': 'GRASS', 'MISTY': 'FAIRY', 'PSYCHIC': 'PSYCHIC'}[self.f.terrain]
        if mk == 'RAGING_BULL':
            t = att.types[-1]
        if t == 'NORMAL' and a in ATE:
            t = ATE[a]
        if a == 'NORMALIZE':
            t = 'NORMAL'
        if a == 'LIQUID_VOICE' and mv['sound']:
            t = 'WATER'
        return t

    def move_cat(self, att, mk):
        mv = self.data.moves[mk]
        if mk == 'ECLIPSE':
            return 'PHYSICAL' if att.st['atk'] > att.st['spa'] else 'SPECIAL'
        if mv['effect'] in ('PHOTON_GEYSER', 'SHELL_SIDE_ARM', 'TERA_BLAST') and att.st['atk'] > att.st['spa']:
            return 'PHYSICAL'
        return mv['cat']

    def usable(self, mk):
        mv = self.data.moves[mk]
        return mv['effect'] not in UNUSABLE and mk not in UNUSABLE and \
            not any(x['eff'] == 'RECHARGE' for x in mv['adds'])

    # ---------------------------------------------------------------- schade
    def damage(self, att, dfn, mk, aside, dside, crit=False, roll=1.0, hitno=0, expected=False, foe_action=None,
               moving_first=None):
        """Schade van één treffer (multi-hit: per treffer; hitno telt). Geeft (schade, effectiviteit)."""
        data = self.data
        mv = data.moves[mk]
        e = mv['effect']
        cat = self.move_cat(att, mk)
        if cat == 'STATUS':
            return 0, 1
        t = self.move_type(att, mk)
        aa = att.abil()
        mold = aa in MOLD_BREAKERS or mk in ('SUNSTEEL_STRIKE', 'MOONGEIST_BEAM', 'PHOTON_GEYSER')
        da = dfn.abil(ign=mold)
        w = self.weather()
        # vaste schade
        if e == 'LEVEL_DAMAGE':
            if data.eff(t, dfn.types) == 0:
                return 0, 0
            return 100, 1
        if e in ('FIXED_PERCENT_DAMAGE', 'SUPER_FANG'):
            if data.eff(t, dfn.types) == 0:
                return 0, 0
            return max(1, dfn.hp * (mv['pct'] or 50) // 100), 1
        # immuniteiten via ability
        imm = {'LEVITATE': 'GROUND', 'EELEVATE': 'GROUND', 'VOLT_ABSORB': 'ELECTRIC', 'LIGHTNING_ROD': 'ELECTRIC',
               'MOTOR_DRIVE': 'ELECTRIC', 'WATER_ABSORB': 'WATER', 'STORM_DRAIN': 'WATER', 'DRY_SKIN': 'WATER',
               'FLASH_FIRE': 'FIRE', 'WELL_BAKED_BODY': 'FIRE', 'SAP_SIPPER': 'GRASS', 'EARTH_EATER': 'GROUND'}
        if imm.get(da) == t:
            return 0, 0
        if self.f.harsh is not None and w and ((w == 'SUN' and t == 'WATER') or (w == 'RAIN' and t == 'FIRE')):
            return 0, 0
        if t == 'GROUND' and dfn.item == 'AIR_BALLOON' and mk != 'THOUSAND_ARROWS':
            return 0, 0
        if da == 'BULLETPROOF' and mv['ball'] or da == 'SOUNDPROOF' and mv['sound'] or \
           da == 'WIND_RIDER' and mv['wind']:
            return 0, 0
        # effectiviteit
        if e == 'TWO_TYPED_MOVE' or mk in ('FLYING_PRESS', 'TYRANT_HORN'):
            t2 = mv['argtype'] or ('FLYING' if mk == 'FLYING_PRESS' else 'GROUND')
            ef = data.eff(t, dfn.types) * data.eff(t2, dfn.types)
        else:
            ef = data.eff(t, dfn.types)
            t2 = None
        if e == 'SUPER_EFFECTIVE_ON_ARG' and mv['argtype'] in dfn.types:
            ef = ef / data.eff(t, [mv['argtype']]) * 2
        if t == 'GROUND' and not self.grounded(dfn) and ef == 0 and mk == 'THOUSAND_ARROWS':
            ef = 1
        if aa == 'SCRAPPY' and t in ('NORMAL', 'FIGHTING') and 'GHOST' in dfn.types:
            ef = data.eff(t, [x for x in dfn.types if x != 'GHOST'])
        if ef == 0:
            return 0, 0
        if da == 'WONDER_GUARD' and ef <= 1:
            return 0, 0
        if da == 'FAKE_FOLIAGE' and t == 'GRASS':
            ef *= 0.5
        # kracht
        p = mv['power']
        if e in ('LOW_KICK', 'GRASS_KNOT'):
            wt = dfn.d['weight']
            p = 20 if wt < 100 else 40 if wt < 250 else 60 if wt < 500 else 80 if wt < 1000 else 100 if wt < 2000 else 120
        elif e == 'HEAT_CRASH':
            r = att.d['weight'] / max(1, dfn.d['weight'])
            p = 40 if r < 2 else 60 if r < 3 else 80 if r < 4 else 100 if r < 5 else 120
        elif e == 'GYRO_BALL':
            p = min(150, int(25 * self.speed(dfn, dside) / max(1, self.speed(att, aside))) + 1)
        elif e == 'ELECTRO_BALL':
            r = self.speed(att, aside) / max(1, self.speed(dfn, dside))
            p = 150 if r >= 4 else 120 if r >= 3 else 80 if r >= 2 else 60 if r >= 1 else 40
        elif e == 'STORED_POWER':
            p = 20 + 20 * sum(max(0, v) for v in att.boosts.values())
        elif e == 'RAGE_FIST':
            p = min(350, 50 + 50 * att.hits_taken)
        elif e == 'LAST_RESPECTS':
            p = 50 + 50 * aside.fainted
        elif mk == 'KEYSTONE_CURSE':
            p = 60 + 20 * aside.fainted
        elif e == 'TRIPLE_KICK' or mk == 'COMBINATION':
            p = mv['power'] * (hitno + 1)
        elif e == 'WEATHER_BALL' and w:
            p = 100
        elif e == 'RETURN':
            p = 102
        elif e == 'POWER_BASED_ON_USER_HP':
            p = max(1, int(150 * att.hp / att.maxhp))
        elif e == 'STEEL_ROLLER' and not self.f.terrain:
            return 0, ef
        if e == 'FACADE' and att.status:
            p *= 2
        if e == 'DOUBLE_POWER_ON_ARG_STATUS' and dfn.status:
            p *= 2
        if e == 'KNOCK_OFF' and dfn.item and not dfn.lost_item:
            p *= 1.5
        if e == 'ACROBATICS' and not att.item:
            p *= 2
        if e in ('BOLT_BEAK', 'FISHIOUS_REND') and moving_first:
            p *= 2
        if e in ('PAYBACK',) and moving_first is False:
            p *= 2
        if e == 'VENOSHOCK' and dfn.status in ('POISON', 'TOXIC'):
            p *= 2
        if e == 'BRINE' and dfn.hp * 2 <= dfn.maxhp:
            p *= 2
        if e == 'COLLISION_COURSE' and ef > 1:
            p *= 4 / 3
        if e == 'FICKLE_BEAM':
            p *= 1.3 if expected else (2 if self.rng.random() < 0.3 else 1)
        if mk == 'FLYTRAP' and ('BUG' in dfn.types or 'FLYING' in dfn.types):
            p *= 2
        if mk == 'JOUST' and self.speed(dfn, dside) > self.speed(att, aside):
            p = 100
        if mk == 'STRAIGHT_LINE' and att.last == 'STRAIGHT_LINE':
            p = 100
        if mk == 'SOLSTICE_GATE' and w in ('SUN', 'SNOW'):
            p *= 1.5
        if mk in ('OMEN_STRIKE', 'KUSARIGAMA') and foe_action is not None and foe_action[0] == 'switch':
            p *= 2
        if mk == 'OMEN_STRIKE' and foe_action is not None and foe_action[0] == 'move' and \
           data.moves[foe_action[1]]['cat'] == 'STATUS':
            p *= 2
        if e == 'HYDRO_STEAM' and w == 'SUN':
            p *= 1  # zon versterkt i.p.v. verzwakt (zie weermodifier)
        if e == 'PSYBLADE' and self.f.terrain == 'ELECTRIC':
            p *= 1.5
        if e == 'SOLAR_BEAM' and w not in ('SUN', None):
            p *= 0.5
        if p <= 1:
            return 0, ef
        # ability-krachtbonussen
        if aa == 'TECHNICIAN' and p <= 60:
            p *= 1.5
        if aa == 'SHARPNESS' and mv['slice']:
            p *= 1.5
        if aa == 'STRONG_JAW' and mv['bite']:
            p *= 1.5
        if aa == 'IRON_FIST' and mv['punch']:
            p *= 1.2
        if aa == 'MEGA_LAUNCHER' and mv['pulse']:
            p *= 1.5
        if aa == 'PUNK_ROCK' and mv['sound']:
            p *= 1.3
        if aa == 'TOUGH_CLAWS' and mv['contact']:
            p *= 1.3
        if aa == 'RECKLESS' and (mv['recoil'] or e == 'RECOIL_IF_MISS'):
            p *= 1.2
        if aa == 'SHEER_FORCE' and any(not x['self'] or x['eff'].endswith('PLUS_1') for x in mv['adds']):
            p *= 1.3
        if aa == 'SAND_FORCE' and w == 'SAND' and t in ('ROCK', 'GROUND', 'STEEL'):
            p *= 1.3
        if aa in ATE and mv['type'] == 'NORMAL':
            p *= 1.2
        if aa == 'NORMALIZE':
            p *= 1.2
        if aa == 'TRANSISTOR' and t == 'ELECTRIC':
            p *= 1.3
        if aa == 'DRAGONS_MAW' and t == 'DRAGON':
            p *= 1.5
        if aa == 'STEELWORKER' and t == 'STEEL':
            p *= 1.5
        if aa == 'ROCKY_PAYLOAD' and t == 'ROCK':
            p *= 1.5
        if aa == 'WATER_BUBBLE' and t == 'WATER':
            p *= 2
        if aa == 'ANALYTIC' and moving_first is False:
            p *= 1.3
        if aa == 'TOXIC_BOOST' and att.status in ('POISON', 'TOXIC') and cat == 'PHYSICAL':
            p *= 1.5
        if aa in ('BLAZE', 'TORRENT', 'OVERGROW', 'SWARM') and att.hp * 3 <= att.maxhp and \
           t == {'BLAZE': 'FIRE', 'TORRENT': 'WATER', 'OVERGROW': 'GRASS', 'SWARM': 'BUG'}[aa]:
            p *= 1.5
        if aa == 'FLASH_FIRE' and att.flashfire and t == 'FIRE':
            p *= 1.5
        if att.charge and t == 'ELECTRIC':
            p *= 2
        if aa == 'SUPREME_OVERLORD':
            p *= 1 + 0.1 * min(5, aside.fainted)
        it = att.item
        if TYPE_ITEMS.get(it) == t or (it.endswith('_MASK') and att.d['dispname'].startswith('Ogerpon') and it != 'TEAL_MASK') \
           or (it == 'TEAL_MASK' and att.d['dispname'].startswith('Ogerpon')):
            p *= 1.2
        if it == 'MUSCLE_BAND' and cat == 'PHYSICAL' or it == 'WISE_GLASSES' and cat == 'SPECIAL':
            p *= 1.1
        if it == 'PUNCHING_GLOVE' and mv['punch']:
            p *= 1.1
        # terrein
        if self.f.terrain and self.grounded(att):
            if (self.f.terrain, t) in (('ELECTRIC', 'ELECTRIC'), ('GRASSY', 'GRASS'), ('PSYCHIC', 'PSYCHIC')):
                p *= 1.3
        if self.f.terrain == 'MISTY' and t == 'DRAGON' and self.grounded(dfn):
            p *= 0.5
        if self.f.terrain == 'GRASSY' and mk in ('EARTHQUAKE', 'BULLDOZE') and self.grounded(dfn):
            p *= 0.5
        if da == 'DRY_SKIN' and t == 'FIRE':
            p *= 1.25
        # stats
        ign_def = mv['ignoreDefStages'] or aa == 'UNAWARE' or mk in ('SPINNING_BACKFIST', 'DIM_MAK') or \
            (w == 'POLLEN' and 'BUG' in att.types)
        ign_atk = da == 'UNAWARE'
        if e == 'BODY_PRESS' or mk == 'QUEENS_WEIGHT':
            A = self.stat(att, 'def', crit, ign_atk, True, other=dfn)
        elif e == 'FOUL_PLAY':
            A = self.stat(dfn, 'atk', crit, ign_atk, True, other=dfn)
        else:
            A = self.stat(att, 'atk' if cat == 'PHYSICAL' else 'spa', crit, ign_atk, True, other=dfn)
        defkey = 'def' if (cat == 'PHYSICAL' or e == 'PSYSHOCK') else 'spd'
        D = self.stat(dfn, defkey, crit, ign_def, False, other=att)
        base = math.floor(math.floor(math.floor(2 * 100 / 5 + 2) * p * A / max(1, D)) / 50) + 2
        mod = 1.0
        # weer
        if w == 'RAIN':
            mod *= 1.5 if t == 'WATER' else 0.5 if t == 'FIRE' else 1
        elif w == 'SUN':
            mod *= 1.5 if (t == 'FIRE' or e == 'HYDRO_STEAM') else 0.5 if t == 'WATER' else 1
        elif w == 'POLLEN':
            mod *= 1.5 if t in ('BUG', 'GRASS') else 0.5 if t == 'FIRE' and aa != 'FORECAST' else 1
        elif w == 'ACID' and (aa != 'FORECAST' or e == 'WEATHER_BALL'):
            mod *= 0.5 if t in ('FIRE', 'WATER') else 1.5 if t == 'POISON' else 1
        if crit:
            mod *= 2.25 if aa == 'SNIPER' else 1.5
        mod *= roll
        stab = t in att.types or (t2 and t2 in att.types) or (aa in ('PROTEAN', 'LIBERO'))
        if stab:
            mod *= 2.0 if aa == 'ADAPTABILITY' else 1.5
        mod *= ef
        if att.status == 'BURN' and cat == 'PHYSICAL' and aa != 'GUTS' and e != 'FACADE':
            mod *= 0.5
        # schermen
        if not crit and aa != 'INFILTRATOR' and mk != 'LASER_BEAM' and e not in ('BRICK_BREAK',):
            if (cat == 'PHYSICAL' and (dside.reflect or dside.veil)) or (cat == 'SPECIAL' and (dside.lscreen or dside.veil)):
                mod *= 2 / 3 if self.mode == 'doubles' else 0.5
        # verdediger
        if da in ('MULTISCALE', 'SHADOW_SHIELD') and dfn.hp == dfn.maxhp and hitno == 0:
            mod *= 0.5
        if da in ('FILTER', 'SOLID_ROCK', 'PRISM_ARMOR') and ef > 1:
            mod *= 0.75
        if da == 'THICK_FAT' and t in ('FIRE', 'ICE'):
            mod *= 0.5
        if da in ('HEATPROOF', 'WATER_BUBBLE') and t == 'FIRE':
            mod *= 0.5
        if da == 'PURIFYING_SALT' and t == 'GHOST':
            mod *= 0.5
        if da == 'FLUFFY':
            if mv['contact'] and att.item != 'PUNCHING_GLOVE':
                mod *= 0.5
            if t == 'FIRE':
                mod *= 2
        if da == 'AURA_GUARD' and mv['contact'] and att.item != 'PUNCHING_GLOVE' and aa != 'LONG_REACH':
            mod *= 0.5
        if da == 'ICE_SCALES' and cat == 'SPECIAL':
            mod *= 0.5
        if da == 'PUNK_ROCK' and mv['sound']:
            mod *= 0.5
        if aa == 'TINTED_LENS' and ef < 1:
            mod *= 2
        if aa == 'NEUROFORCE' and ef > 1:
            mod *= 1.25
        if it == 'LIFE_ORB':
            mod *= 1.3
        if it == 'EXPERT_BELT' and ef > 1:
            mod *= 1.2
        dmg = base * mod
        return max(1, int(dmg)), ef

    def hits(self, att, mk, expected=False):
        mv = self.data.moves[mk]
        e = mv['effect']
        if e == 'MULTI_HIT' or mk in ('OTHISMOS',):
            if att.abil() == 'SKILL_LINK':
                return 5
            if att.item == 'LOADED_DICE':
                return 4.5 if expected else self.rng.choice([4, 5])
            if mk == 'OTHISMOS':
                return 2 + round(3 * att.frac())
            return 3.1 if expected else self.rng.choices([2, 3, 4, 5], [35, 35, 15, 15])[0]
        if e == 'POPULATION_BOMB':
            if att.abil() == 'SKILL_LINK' or att.item == 'WIDE_LENS':
                return 10 if att.abil() == 'SKILL_LINK' else 7
            return 6 if expected else min(10, 1 + sum(1 for _ in range(9) if self.rng.random() < 0.9))
        if e == 'TRIPLE_KICK':
            return 3
        if e == 'DRAGON_DARTS':
            return 2
        if att.abil() == 'PARENTAL_BOND' and mv['strikes'] == 1 and att.hp * 2 > att.maxhp:
            return 1.25 if expected else 2   # deze rom: de baby slaat alleen mee boven de helft van de HP
        return mv['strikes']

    def crit_chance(self, att, dfn, mk):
        mv = self.data.moves[mk]
        da = dfn.abil(ign=att.abil() in MOLD_BREAKERS)
        if da in ('BATTLE_ARMOR', 'SHELL_ARMOR'):
            return 0
        if mv['alwaysCrit'] or mk == 'IPPON' or (att.abil() == 'MERCILESS' and dfn.status in ('POISON', 'TOXIC')) or \
           (mk == 'BRAIN_FREEZE' and self.weather() == 'SNOW'):
            return 1
        st = mv['crit'] + (1 if att.abil() == 'SUPER_LUCK' else 0) + (1 if att.item in ('SCOPE_LENS', 'RAZOR_CLAW') else 0)
        if mk in ('SKY_SPEAR', 'ANCIENT_SCYTHE', 'MAWASHI_GERI', 'OMEN_STRIKE'):
            st = max(st, 1)
        return CRIT_CHANCE[min(4, st)]

    def accuracy(self, att, dfn, mk):
        mv = self.data.moves[mk]
        acc = mv['acc']
        w = self.weather()
        if acc == 0 or att.abil() == 'NO_GUARD' or dfn.abil() == 'NO_GUARD':
            return 1.0
        if mk in ('THUNDER', 'HURRICANE', 'BLEAKWIND_STORM', 'WILDBOLT_STORM', 'SANDSEAR_STORM'):
            if w in ('RAIN', 'ACID'):
                return 1.0
            if w == 'SUN':
                acc = 50
        if mk in ('BLIZZARD',) and w == 'SNOW':
            return 1.0
        if mk == 'TOXIC' and 'POISON' in att.types:
            return 1.0
        if mv['powder'] and w == 'POLLEN':
            acc = min(100, acc + 20)
        if att.abil() == 'COMPOUND_EYES':
            acc *= 1.3
        if att.abil() == 'HUSTLE' and mv['cat'] == 'PHYSICAL':
            acc *= 0.8
        if att.item == 'WIDE_LENS':
            acc *= 1.1
        stg = att.boosts['acc'] - (0 if (att.abil() in ('UNAWARE', 'KEEN_EYE', 'MINDS_EYE') or mv['ignoreDefStages']) else dfn.boosts['eva'])
        acc *= ACC_STAGE[max(-6, min(6, stg))]
        return min(1.0, acc / 100)

    def priority(self, m, mk, side, foe):
        if mk is None:
            return 0
        mv = self.data.moves[mk]
        p = mv['pri']
        a = m.abil()
        if a == 'GALE_WINGS' and mv['type'] == 'FLYING' and m.hp == m.maxhp:
            p += 1
        if a == 'PRANKSTER' and mv['cat'] == 'STATUS':
            p += 1
        if a == 'TRIAGE' and (mv['drain'] or mk in HEAL):
            p += 3
        if mk == 'GRASSY_GLIDE' and self.f.terrain == 'GRASSY':
            p += 1
        if mk == 'STRAIGHT_LINE' and m.last == 'STRAIGHT_LINE':
            p = 0
        if mk == 'JOUST' and self.speed(foe.mon, foe) > self.speed(m, side):
            p += 1
        if mk == 'LIFE_BUOY' and self.weather() == 'RAIN':
            p += 1
        if mk == 'ABDUCTION' and self.f.tr:
            p = 7
        return p

    # ---------------------------------------------------------------- verwachte waarden voor de AI
    def exp_dmg(self, att, dfn, mk, aside, dside, foe_action=None, moving_first=None):
        """Verwachte schade van één gebruik (gemiddelde rol, crits, accuracy, aantal treffers)."""
        if not self.usable(mk):
            return 0
        mv = self.data.moves[mk]
        if self.move_cat(att, mk) == 'STATUS':
            return 0
        if mv['effect'] == 'SUCKER_PUNCH' and (foe_action is None or foe_action[0] != 'move'
                                               or self.data.moves[foe_action[1]]['cat'] == 'STATUS'):
            pass
        if mk == 'IPPON' or mk == 'ABDUCTION':
            pass
        if dfn.abil() in ('ARMOR_TAIL', 'QUEENLY_MAJESTY', 'DAZZLING') and self.priority(att, mk, aside, dside) > 0:
            return 0
        if self.f.terrain == 'PSYCHIC' and self.priority(att, mk, aside, dside) > 0 and self.grounded(dfn):
            return 0
        if dfn.abil() == 'GOOD_AS_GOLD' and mv['cat'] == 'STATUS':
            return 0
        cc = self.crit_chance(att, dfn, mk)
        n = self.hits(att, mk, expected=True)
        tot = 0
        if mv['effect'] == 'TRIPLE_KICK' or mk == 'COMBINATION':
            acc = self.accuracy(att, dfn, mk)
            pr = 1
            for i in range(3):
                pr *= acc if mv['effect'] == 'TRIPLE_KICK' else 1
                d, _ = self.damage(att, dfn, mk, aside, dside, False, 0.925, i, True, foe_action, moving_first)
                tot += pr * d
            return tot * (1 + 0.5 * cc)
        d0, _ = self.damage(att, dfn, mk, aside, dside, False, 0.925, 0, True, foe_action, moving_first)
        dc, _ = self.damage(att, dfn, mk, aside, dside, True, 0.925, 0, True, foe_action, moving_first) if cc else (d0, 0)
        d = d0 * (1 - cc) + dc * cc
        if dfn.disguise and dfn.abil(ign=att.abil() in MOLD_BREAKERS) == 'DISGUISE':
            d = d * max(0, n - 1) / max(1, n) + dfn.maxhp / 8
            return d * self.accuracy(att, dfn, mk)
        if n != 1:
            d1, _ = self.damage(att, dfn, mk, aside, dside, False, 0.925, 1, True, foe_action, moving_first)
            d = d + (n - 1) * (d1 * (1 - cc) + d1 * 1.5 * cc)
        return d * self.accuracy(att, dfn, mk)

    def best_attack(self, att, dfn, aside, dside, moves=None):
        best, bd = None, 0.0
        for mk in (moves or att.moves):
            if att.lock and mk != att.lock:
                continue
            dd = self.exp_dmg(att, dfn, mk, aside, dside)
            mv = self.data.moves[mk]
            if mv['effect'] == 'SUCKER_PUNCH':
                dd *= 0.8
            if mv['drain']:
                dd *= 1.0 + 0.2 * mv['drain'] / 100
            if dd > bd:
                best, bd = mk, dd
        return best, bd

    def residual(self, m, side, other=None):
        """Netto HP-verlies per beurt (positief = verlies) door weer, status, items, seeds."""
        r = 0.0
        a = m.abil()
        mh = m.maxhp
        w = self.weather()
        mg = a == 'MAGIC_GUARD'
        if not mg:
            if w == 'SAND' and not set(m.types) & {'ROCK', 'GROUND', 'STEEL'} and a not in ('SAND_VEIL', 'SAND_RUSH', 'SAND_FORCE', 'OVERCOAT') \
               and m.item != 'SAFETY_GOGGLES':
                r += mh / 16
            if w == 'ACID' and 'POISON' not in m.types and 'STEEL' not in m.types and a not in ('OVERCOAT', 'FORECAST') \
               and m.item not in ('SAFETY_GOGGLES', 'UTILITY_UMBRELLA'):
                r += mh / 16
            if m.status == 'BURN':
                r += mh / 16
            if m.status == 'POISON' and a != 'POISON_HEAL':
                r += mh / 8
            if m.status == 'TOXIC' and a != 'POISON_HEAL':
                r += mh * min(15, m.tox + 1) / 16
            if m.seeded:
                r += mh / 8
            if m.salt:
                r += mh / (4 if set(m.types) & {'WATER', 'STEEL'} else 8)
            if m.trap:
                r += m.trapdmg
            if m.item == 'LIFE_ORB' and a != 'SHEER_FORCE':
                r += mh / 10   # benadering: bij elke aanval
        if w == 'ACID' and 'POISON' in m.types:
            r -= mh / 16
        if w == 'POLLEN' and ('GRASS' in m.types or a == 'FAKE_FOLIAGE'):
            r -= mh / 16
        if w == 'RAIN' and a in ('RAIN_DISH', 'DRY_SKIN'):
            r -= mh / (16 if a == 'RAIN_DISH' else 8)
        if w == 'SNOW' and a == 'ICE_BODY':
            r -= mh / 16
        if self.f.terrain == 'GRASSY' and self.grounded(m):
            r -= mh / 16
        if m.item == 'LEFTOVERS' or (m.item == 'BLACK_SLUDGE' and 'POISON' in m.types):
            r -= mh / 16
        if a == 'POISON_HEAL' and m.status in ('POISON', 'TOXIC'):
            r -= mh / 8
        if other is not None and other.seeded:
            r -= other.maxhp / 8
        if m.kelp and other is not None:
            pass
        return r

    def heal_frac(self, m):
        """Beste herstel-move (fractie max-HP) die deze Pokémon heeft, of 0."""
        best = 0.0
        w = self.weather()
        for mk in m.moves:
            if mk not in HEAL or mk in ('REST', 'WISH', 'STRENGTH_SAP'):
                if mk == 'WISH':
                    best = max(best, 0.4)
                if mk == 'STRENGTH_SAP':
                    best = max(best, 0.35)
                continue
            f = HEAL[mk]
            if mk in ('MOONLIGHT', 'MORNING_SUN', 'SYNTHESIS'):
                f = 2 / 3 if w == 'SUN' else 0.25 if w in ('RAIN', 'SAND', 'SNOW', 'ACID') else 0.5
            if mk == 'SHORE_UP' and w == 'SAND' or mk == 'OLIVE_OIL' and w == 'POLLEN':
                f = 2 / 3
            best = max(best, f)
        return best

    def race(self, me, foe, mside, fside, my_dmg=None, foe_dmg=None, my_first=None, extra_me=0.0, extra_foe=0.0,
             foe_skip=0, me_skip=0, t1_dmg=None, t1_first=None, heals=True):
        """Schat de uitkomst van 'allebei elke beurt de beste aanval' (met herstel-moves als die helpen).
        >0 = ik win (0..1 marge). t1_dmg/t1_first: andere aanval in de eerste beurt."""
        if my_dmg is None:
            _, my_dmg = self.best_attack(me, foe, mside, fside)
        if foe_dmg is None:
            _, foe_dmg = self.best_attack(foe, me, fside, mside)
        mult_m = (0.75 if me.status == 'PARALYSIS' else 1) * (0.67 if me.conf else 1) * (0.5 if me.abil() == 'TRUANT' else 1)
        mult_f = (0.75 if foe.status == 'PARALYSIS' else 1) * (0.67 if foe.conf else 1) * (0.5 if foe.abil() == 'TRUANT' else 1)
        my_dmg *= mult_m
        foe_dmg *= mult_f
        if t1_dmg is not None:
            t1_dmg *= mult_m
        if my_first is None:
            mb, _ = self.best_attack(me, foe, mside, fside)
            fb, _ = self.best_attack(foe, me, fside, mside)
            my_first = self.goes_first(me, mb, mside, foe, fb, fside)
        rm = self.residual(me, mside, foe) + extra_me
        rf = self.residual(foe, fside, me) + extra_foe
        hm, hf = float(me.hp), float(foe.hp)
        me_slp = max(me_skip, (me.slp if me.status == 'SLEEP' else 0))
        foe_slp = max(foe_skip, (foe.slp if foe.status == 'SLEEP' else 0))
        if foe.status == 'FREEZE':
            foe_slp = max(foe_slp, 2)
        if me.status == 'FREEZE':
            me_slp = max(me_slp, 2)
        hm_f = self.heal_frac(me) * me.maxhp if heals else 0
        hf_f = self.heal_frac(foe) * foe.maxhp if heals else 0
        hm_left, hf_left = 8, 8
        sturdy_f = foe.hp == foe.maxhp and (foe.abil() == 'STURDY' or foe.item == 'FOCUS_SASH')
        sturdy_m = me.hp == me.maxhp and (me.abil() == 'STURDY' or me.item == 'FOCUS_SASH')
        for t in range(40):
            first = my_first if (t > 0 or t1_first is None) else t1_first
            md = my_dmg if (t > 0 or t1_dmg is None) else t1_dmg
            order = ('m', 'f') if first else ('f', 'm')
            # herstellen als je anders binnen twee klappen valt en het herstel de klap overtreft
            m_heal = hm_f > foe_dmg * 1.05 and hm_left > 0 and hm <= foe_dmg * (2 if not first else 1) + rm and hm < me.maxhp * 0.6 \
                and md < hf + max(0, -rf)
            f_heal = hf_f > md * 1.05 and hf_left > 0 and hf <= md * (2 if first else 1) + rf and hf < foe.maxhp * 0.6 \
                and foe_dmg < hm + max(0, -rm)
            for who in order:
                if who == 'm':
                    if hm <= 0:
                        break
                    if me_slp > 0:
                        continue
                    if m_heal:
                        hm = min(me.maxhp, hm + hm_f)
                        hm_left -= 1
                        continue
                    nh = hf - md
                    if sturdy_f and nh <= 0 and hf == foe.maxhp:
                        nh = 1
                    sturdy_f = False
                    hf = nh
                else:
                    if hf <= 0:
                        break
                    if foe_slp > 0:
                        continue
                    if f_heal:
                        hf = min(foe.maxhp, hf + hf_f)
                        hf_left -= 1
                        continue
                    nh = hm - foe_dmg
                    if sturdy_m and nh <= 0 and hm == me.maxhp:
                        nh = 1
                    sturdy_m = False
                    hm = nh
            me_slp -= 1
            foe_slp -= 1
            if hm <= 0 or hf <= 0:
                break
            hm = min(me.maxhp, hm - rm)
            hf = min(foe.maxhp, hf - rf)
            if hm <= 0 or hf <= 0:
                break
            if my_dmg <= 0 and foe_dmg <= 0 and rm <= 0 and rf <= 0:
                return 0.0
        if hf <= 0 and hm > 0:
            return 0.5 + 0.5 * hm / me.maxhp
        if hm <= 0 and hf > 0:
            return -0.5 - 0.5 * hf / foe.maxhp
        if hm <= 0 and hf <= 0:
            return 0.0
        return 0.4 * (hm / me.maxhp - hf / foe.maxhp)

    def goes_first(self, m1, mk1, s1, m2, mk2, s2):
        p1, p2 = self.priority(m1, mk1, s1, s2), self.priority(m2, mk2, s2, s1)
        if p1 != p2:
            return p1 > p2
        a, b = self.speed(m1, s1), self.speed(m2, s2)
        if self.f.tr:
            a, b = -a, -b
        if a == b:
            return True
        return a > b

    # ---------------------------------------------------------------- AI
    def choose(self, side):
        """Kies ('move', mk) of ('switch', idx)."""
        me, foe = side.mon, self.foe(side).mon
        fside = self.foe(side)
        if me.lock and me.lock in me.moves and me.item.startswith('CHOICE'):
            opts = [me.lock]
        else:
            opts = [m for m in me.moves if self.usable(m) or self.data.moves[m]['cat'] == 'STATUS']
        if me.status == 'SLEEP' and 'SLEEP_TALK' in me.moves and me.slp > 1:
            return ('move', 'SLEEP_TALK')
        if getattr(me, 'thrash', 0) > 0 and me.thrash_move in me.moves:
            me.thrash -= 1
            if me.thrash == 0 and not me.conf and me.abil() != 'OWN_TEMPO':
                me.conf = self.rng.randint(2, 5)
            return ('move', me.thrash_move)
        base = self.race(me, foe, side, fside)
        fb, fd = self.best_attack(foe, me, fside, side)
        best, bscore = None, -9
        for mk in opts:
            sc = self.score_move(side, me, foe, fside, mk, base, fb, fd)
            if sc > bscore:
                best, bscore = mk, sc
        # vrijwillig wisselen (alleen in teamgevechten)
        if self.mode == 'team' and len(side.alive()) > 1 and side.switches < 12 and bscore < -0.25 and not me.trap \
           and not (foe.abil() in ('SHADOW_TAG',) or (foe.abil() == 'ARENA_TRAP' and self.grounded(me))
                    or (foe.abil() == 'MAGNET_PULL' and 'STEEL' in me.types)):
            idx, val = self.best_switch(side, entry_hit=fd if fb else 0, foe_move=fb)
            if idx is not None and val > bscore + 0.35 and val > 0:
                return ('switch', idx)
        if best is None:
            best = opts[0] if opts else 'STRUGGLE'
        return ('move', best)

    def score_move(self, side, me, foe, fside, mk, base, fb, fd):
        mv = self.data.moves[mk]
        e = mv['effect']
        my_first = self.goes_first(me, mk, side, foe, fb, fside)
        if mv['cat'] != 'STATUS' or mk in ('MACHINE_LEARNING',) and False:
            if not self.usable(mk):
                return -5
            d = self.exp_dmg(me, foe, mk, side, fside, moving_first=my_first)
            if e == 'SUCKER_PUNCH':
                if fb is None:
                    d = 0
                elif any(self.data.moves[x]['cat'] == 'STATUS' for x in foe.moves):
                    d *= 0.6
            if d <= 0:
                return -3
            # directe KO?
            if d >= foe.hp and (my_first or fd < me.hp):
                sc = 2.0 + self.accuracy(me, foe, mk) + (0.2 if my_first else 0)
                if mv['recoil'] or e == 'RECOIL_IF_MISS':
                    sc -= 0.05
                if mk in PIVOT and self.mode == 'team':
                    sc += 0.05
                return sc
            # anders: deze beurt deze move, daarna de beste aanval
            sc = self.race(me, foe, side, fside, t1_dmg=d, t1_first=my_first)
            # kleine voorkeuren
            if mv['drain']:
                sc += 0.02
            if e in ('RAPID_SPIN',) and any(side.haz.values()):
                sc += 0.1
            if mk in PIVOT and self.mode == 'team' and base < 0 and len(side.alive()) > 1:
                idx, val = self.best_switch(side, entry_hit=0, foe_move=fb)
                if idx is not None and val > base:
                    sc = max(sc, (val + sc) / 2 + 0.05)
            if e == 'SUCKER_PUNCH':
                sc -= 0.03
            if e in ('KNOCK_OFF',) and foe.item and not foe.lost_item:
                sc += 0.03
            if e == 'SALT_CURE' or any(x['eff'] == 'SALT_CURE' for x in mv['adds']):
                sc += 0.05 if not foe.salt else 0
            return sc
        # ------------------------- status-moves
        if foe.abil() in ('MAGIC_BOUNCE', 'GOOD_AS_GOLD') and mv['target'] not in ('USER', 'ALL_BATTLERS', 'OPPONENTS_FIELD', 'USERS_SIDE'):
            return -4
        dmg_taken = fd if fb else 0
        if mk in SETUP:
            boosts = SETUP[mk]
            if mk == 'MACHINE_LEARNING':
                boosts = self.ml_boosts(me)
            if mk == 'GROWTH' and self.weather() == 'SUN':
                boosts = {'atk': 2, 'spa': 2}
            if mk == 'PACK_HOWL':
                boosts = {'atk': 1, 'spe': 1}
            if mk == 'CURSE' and 'GHOST' in me.types:
                return -4
            if mk == 'BELLY_DRUM' and me.hp * 2 <= me.maxhp:
                return -4
            if mk == 'STOCKPILE' and me.streak >= 3:
                return -4
            if all(me.boosts['defn' if k == 'def' else k] >= 6 for k, v in boosts.items() if v > 0):
                return -4
            if sum(max(0, me.boosts[k]) for k in ('atk', 'spa', 'spe', 'defn', 'spd')) >= 6:
                return -1
            if dmg_taken >= me.hp and not (me.hp == me.maxhp and (me.abil() in ('STURDY',) or me.item == 'FOCUS_SASH')):
                if not (self.goes_first(me, mk, side, foe, fb, fside) and False):
                    return -2
            clone = copy.copy(me)
            clone.boosts = dict(me.boosts)
            mult = 2 if me.abil() == 'SIMPLE' else 1
            for k, v in boosts.items():
                kk = 'defn' if k == 'def' else k
                v = -v if me.abil() == 'CONTRARY' else v
                clone.boosts[kk] = max(-6, min(6, clone.boosts[kk] + v * mult))
            if mk == 'BELLY_DRUM':
                clone.hp -= me.maxhp // 2
            # na de setup-beurt: ik heb fd geïncasseerd (tenzij ik sneller ben en ...)
            fb2, fd2 = self.best_attack(foe, clone, fside, side)
            clone.hp = clone.hp - fd
            if clone.hp <= 0:
                return -2
            sc = self.race(clone, foe, side, fside, foe_dmg=fd2)
            return sc - 0.04
        if mk in HEAL:
            if me.hp >= me.maxhp * 0.75 and mk != 'REST':
                return -2
            frac = HEAL[mk]
            w = self.weather()
            if mk in ('MOONLIGHT', 'MORNING_SUN', 'SYNTHESIS'):
                frac = 2 / 3 if w == 'SUN' else 0.25 if w in ('RAIN', 'SAND', 'SNOW', 'ACID') else 0.5
            if mk == 'SHORE_UP' and w == 'SAND':
                frac = 2 / 3
            if mk == 'OLIVE_OIL' and w == 'POLLEN':
                frac = 2 / 3
            if mk == 'STRENGTH_SAP':
                frac = self.stat(foe, 'atk') / me.maxhp
            if mk == 'REST':
                if me.hp > me.maxhp * 0.5 or me.abil() in ('INSOMNIA', 'VITAL_SPIRIT'):
                    return -2
            if mk == 'WISH' and side.wish:
                return -2
            if self.f.terrain == 'MISTY' and mk == 'REST':
                return -2
            heal = min(me.maxhp - me.hp, me.maxhp * frac)
            clone = copy.copy(me)
            clone.hp = me.hp + heal - (fd if mk != 'WISH' else 0)
            if mk == 'WISH':
                clone.hp = me.hp - fd + heal
            if clone.hp <= 0:
                return -2
            sk = 2 if mk == 'REST' and 'SLEEP_TALK' not in me.moves else 0
            if mk == 'REST':
                clone.status = None
            first = self.goes_first(me, mk, side, foe, fb, fside)
            if not first:
                clone.hp = min(me.hp - fd, 0) if me.hp - fd <= 0 else min(me.maxhp, me.hp - fd + heal)
                if clone.hp <= 0:
                    return -2
            sc = self.race(clone, foe, side, fside, me_skip=sk)
            if mk == 'STRENGTH_SAP':
                sc += 0.05
            return sc - 0.03
        if mk in STATUS_MOVES:
            st = STATUS_MOVES[mk]
            if me.abil() == 'PRANKSTER' and 'DARK' in foe.types:
                return -3
            if not self.can_status(foe, st, me, fside) or foe.status:
                return -3
            if st == 'YAWN' and foe.yawn:
                return -3
            if st == 'SLEEP' and any(m.status == 'SLEEP' and m is not foe for m in fside.team):
                return -3   # Sleep Clause
            acc = self.accuracy(me, foe, mk)
            clone = copy.copy(foe)
            clone.status = st if st != 'YAWN' else None
            fdm = fd
            skip = 0
            extra = 0.0
            if st == 'BURN':
                if self.move_cat(foe, fb or 'TACKLE') == 'PHYSICAL' and foe.abil() not in ('GUTS',):
                    fdm = fd * 0.5
                if foe.abil() == 'GUTS':
                    fdm = fd * 1.5
            if st == 'PARALYSIS':
                fdm = fd * 0.75
            if st == 'SLEEP':
                skip = 2
            if st == 'YAWN':
                skip = 1
            clone.tox = 0
            dmg_now = fd
            meclone = copy.copy(me)
            meclone.hp = me.hp - dmg_now
            if meclone.hp <= 0:
                return -2
            first = None
            if st == 'PARALYSIS':
                first = self.speed(me, side) > self.speed(foe, fside) * 0.5 if not self.f.tr else None
            sc_hit = self.race(meclone, clone, side, fside, foe_dmg=fdm, foe_skip=skip, my_first=first)
            sc_miss = self.race(meclone, foe, side, fside)
            sc = acc * sc_hit + (1 - acc) * sc_miss
            if foe.abil() == 'SYNCHRONIZE' and st in ('BURN', 'PARALYSIS', 'TOXIC', 'POISON'):
                sc -= 0.1
            return sc - 0.02
        if mk in HAZARD_MOVES and self.mode == 'team':
            k = HAZARD_MOVES[mk]
            cap = {'sr': 1, 'spikes': 3, 'tspikes': 2, 'moai': 1, 'web': 1}[k]
            if fside.haz[k] >= cap or len(fside.alive()) <= 1:
                return -3
            if fd >= me.hp:
                return -2
            n = len(fside.alive()) - 1
            return base + 0.08 * n + (0.1 if self.turn < 3 else 0)
        if mk in ('DEFOG', 'RAPID_SPIN', 'MORTAL_SPIN', 'TIDY_UP') and self.mode == 'team':
            if not any(side.haz.values()):
                return -3
            return base + 0.25
        if mk in WEATHER_MOVES:
            w = WEATHER_MOVES[mk]
            if self.f.weather == w:
                return -3
            old = (self.f.weather, self.f.wturns)
            self.f.weather, self.f.wturns = w, 5
            meclone = copy.copy(me)
            fb2, fd2 = self.best_attack(foe, me, fside, side)
            meclone.hp = me.hp - fd2
            sc = self.race(meclone, foe, side, fside) if meclone.hp > 0 else -2
            self.f.weather, self.f.wturns = old
            return sc - 0.05
        if mk == 'TAILWIND' and not side.tailwind:
            side.tailwind = 4
            meclone = copy.copy(me)
            meclone.hp = me.hp - fd
            sc = self.race(meclone, foe, side, fside) if meclone.hp > 0 else -2
            side.tailwind = 0
            return sc - 0.1
        if mk == 'TRICK_ROOM' and not self.f.tr:
            self.f.tr = 5
            meclone = copy.copy(me)
            meclone.hp = me.hp - fd
            sc = self.race(meclone, foe, side, fside) if meclone.hp > 0 else -2
            self.f.tr = 0
            return sc - 0.1
        if mk in ('REFLECT', 'LIGHT_SCREEN', 'BUBBLE_DOME', 'AURORA_VEIL'):
            if mk == 'AURORA_VEIL' and self.weather() != 'SNOW':
                return -3
            cat = self.move_cat(foe, fb) if fb else 'PHYSICAL'
            if (mk == 'REFLECT' and (side.reflect or cat != 'PHYSICAL')) or (mk == 'LIGHT_SCREEN' and (side.lscreen or cat != 'SPECIAL')):
                return -3
            if mk in ('BUBBLE_DOME', 'AURORA_VEIL') and (side.veil or (side.reflect and side.lscreen)):
                return -3
            meclone = copy.copy(me)
            meclone.hp = me.hp - fd
            sc = self.race(meclone, foe, side, fside, foe_dmg=fd * 0.5) if meclone.hp > 0 else -2
            return sc - 0.12
        if mk == 'LEECH_SEED':
            if foe.seeded or 'GRASS' in foe.types:
                return -3
            meclone = copy.copy(me)
            meclone.hp = me.hp - fd
            clone = copy.copy(foe)
            clone.seeded = True
            sc = self.race(meclone, clone, side, fside) if meclone.hp > 0 else -2
            return sc * self.accuracy(me, foe, mk) - 0.03
        if mk == 'PAIN_SPLIT':
            if me.hp >= foe.hp:
                return -3
            avg = (me.hp + foe.hp) / 2
            meclone = copy.copy(me)
            meclone.hp = min(me.maxhp, avg) - fd
            clone = copy.copy(foe)
            clone.hp = min(foe.maxhp, avg)
            return (self.race(meclone, clone, side, fside) if meclone.hp > 0 else -2) - 0.03
        if mk in ('HAZE', 'CLEAR_SMOG') and sum(max(0, v) for v in foe.boosts.values()) >= 2:
            return base + 0.4
        if mk in PHAZE and self.mode == 'team' and (sum(max(0, v) for v in foe.boosts.values()) >= 2 or
                                                    (any(fside.haz.values()) and len(fside.alive()) > 1)):
            return base + 0.15 + 0.1 * sum(max(0, v) for v in foe.boosts.values())
        if mk in ('PROTECT', 'SPIKY_SHIELD', 'BANEFUL_BUNKER', 'KINGS_SHIELD', 'SILK_TRAP', 'BURNING_BULWARK', 'DETECT',
                  'PITCHER_TRAP', 'OBSTRUCT') and me.last not in ('PROTECT', 'SPIKY_SHIELD', 'BANEFUL_BUNKER', 'KINGS_SHIELD',
                                                                 'SILK_TRAP', 'BURNING_BULWARK', 'DETECT', 'PITCHER_TRAP', 'OBSTRUCT'):
            if me.abil() == 'SPEED_BOOST' and me.turns == 0:
                return base + 0.3
            if mk == 'PITCHER_TRAP' and fb and self.data.moves[fb]['contact'] and not foe.trap:
                return base + 0.25
            if foe.status in ('TOXIC', 'BURN', 'POISON') or foe.seeded or foe.salt or (side.wish and me.hp < me.maxhp * 0.6):
                return base + 0.05
            if me.abil() == 'POISON_HEAL' and me.status:
                return base + 0.02
            return -1
        if mk == 'TOTEM_GAZE':
            pass
        if mk == 'SUBSTITUTE':
            return -1
        return -3

    def ml_boosts(self, m):
        """Machine Learning: 1, 2, 3, daarna 5 stats +1 (hoogste basisstats eerst)."""
        order = sorted(('atk', 'def', 'spa', 'spd', 'spe'), key=lambda s: -m.d[s])
        n = [1, 2, 3, 5][min(3, m.ml)]
        return {s: 1 for s in order[:n]}

    def can_status(self, m, st, src, mside=None):
        a = m.abil(ign=src.abil() in MOLD_BREAKERS) if src else m.abil()
        if m.status or a in ('PURIFYING_SALT', 'COMATOSE', 'GOOD_AS_GOLD') and st != 'CONFUSION':
            return False
        if self.f.terrain == 'MISTY' and self.grounded(m):
            return False
        if st == 'BURN' and ('FIRE' in m.types or a in ('WATER_VEIL', 'WATER_BUBBLE', 'THERMAL_EXCHANGE')):
            return False
        if st == 'PARALYSIS' and ('ELECTRIC' in m.types or a == 'LIMBER'):
            return False
        if st in ('POISON', 'TOXIC') and (a in ('IMMUNITY', 'PASTEL_VEIL') or
                                          (set(m.types) & {'POISON', 'STEEL'} and not (src and src.abil() == 'CORROSION'))):
            return False
        if st in ('SLEEP', 'YAWN') and (a in ('INSOMNIA', 'VITAL_SPIRIT', 'SWEET_VEIL') or
                                        (self.f.terrain == 'ELECTRIC' and self.grounded(m))):
            return False
        if st == 'FREEZE' and ('ICE' in m.types or a == 'MAGMA_ARMOR' or self.weather() == 'SUN'):
            return False
        if a == 'LEAF_GUARD' and self.weather() == 'SUN':
            return False
        if st == 'SLEEP' and False:
            return False
        return True

    def best_switch(self, side, entry_hit=0, foe_move=None, forced=False):
        foe = self.foe(side).mon
        fside = self.foe(side)
        best, bv = None, -9
        for i in side.alive():
            if i == side.active and not forced:
                continue
            m = side.team[i]
            hz = self.hazard_damage(m, side)
            hit = 0
            if foe_move and not forced and foe.hp > 0:
                hit = self.exp_dmg(foe, m, foe_move, fside, side)
            clone = copy.copy(m)
            clone.hp = m.hp - hz - hit
            if clone.hp <= 0:
                v = -2
            else:
                clone.boosts = dict(m.boosts)
                v = self.race(clone, foe, side, fside) if foe.hp > 0 else clone.hp / clone.maxhp
            if v > bv:
                best, bv = i, v
        return best, bv

    def hazard_damage(self, m, side):
        if m.item == 'HEAVY_DUTY_BOOTS' or m.abil() in ('MAGIC_GUARD', 'HIVE_QUEEN'):
            return 0
        d = 0
        if side.haz['sr']:
            d += m.maxhp * self.data.eff('ROCK', m.types) / 8
        if side.haz['moai']:
            d += m.maxhp * self.data.eff('ROCK', m.types) / 8
        if side.haz['spikes'] and self.grounded(m):
            d += m.maxhp * {1: 1 / 8, 2: 1 / 6, 3: 1 / 4}[side.haz['spikes']]
        return d

    # ---------------------------------------------------------------- uitvoering
    def switch_in(self, side, idx, initial=False, entry=True):
        if not initial:
            out = side.mon
            if out.hp > 0:
                if out.abil() == 'REGENERATOR':
                    out.hp = min(out.maxhp, out.hp + out.maxhp // 3)
                if out.abil() == 'NATURAL_CURE':
                    out.status = None
                if out.abil() == 'ZERO_TO_HERO':
                    pass
                if 'LIFE_BUOY' in out.moves and out.last == 'LIFE_BUOY':
                    out.hp = min(out.maxhp, out.hp + out.maxhp // 4)
            out.reset_volatile()
            if self.f.harsh is out:
                self.f.harsh, self.f.weather, self.f.wturns = None, None, 0
        side.active = idx
        m = side.mon
        m.reset_volatile()
        self.L(side.name, 'stuurt', m.name, '(%d%%)' % (100 * m.frac()))
        # hazards
        if not (m.item == 'HEAVY_DUTY_BOOTS' or m.abil() == 'HIVE_QUEEN'):
            if m.abil() != 'MAGIC_GUARD':
                m.hp -= int(self.hazard_damage(m, side))
            if side.haz['tspikes'] and self.grounded(m):
                if 'POISON' in m.types:
                    side.haz['tspikes'] = 0
                elif self.can_status(m, 'POISON', None):
                    m.status = 'TOXIC' if side.haz['tspikes'] >= 2 else 'POISON'
            if side.haz['web'] and self.grounded(m):
                self.boost(m, {'spe': -1}, src=None)
        if m.abil() == 'HIVE_QUEEN':
            for k in side.haz:
                side.haz[k] = 0
        if m.hp <= 0:
            m.hp = 0
            return
        if entry:
            self.entry_ability(side, m)

    def entry_ability(self, side, m):
        a = m.abil()
        if a in WEATHER_ABIL or a == 'TRADE_WIND' or a == 'HELIOTROPISM':
            self.L('  ', m.name, a)
        foe = self.foe(side).mon
        if a == 'INTIMIDATE' and foe.hp > 0:
            fa = foe.abil()
            if fa in ('CLEAR_BODY', 'WHITE_SMOKE', 'FULL_METAL_BODY', 'HYPER_CUTTER', 'INNER_FOCUS', 'OWN_TEMPO',
                      'OBLIVIOUS', 'SCRAPPY') or foe.item == 'CLEAR_AMULET' or foe.ward:
                pass
            elif fa == 'GUARD_DOG':
                self.boost(foe, {'atk': 1}, None)
            else:
                self.boost(foe, {'atk': -1}, m)
                if fa == 'RATTLED':
                    self.boost(foe, {'spe': 1}, None)
        if a in WEATHER_ABIL:
            w = WEATHER_ABIL[a]
            if a in ('DESOLATE_LAND', 'PRIMORDIAL_SEA'):
                self.f.weather, self.f.wturns, self.f.harsh = w, 999, m
            elif self.f.weather != w and not self.f.harsh:
                self.f.weather = w
                self.f.wturns = 8 if m.item == WEATHER_ROCK.get(w) else 5
        if a == 'DELTA_STREAM':
            self.f.weather, self.f.wturns = None, 0
        if a in TERRAIN_ABIL:
            self.f.terrain = TERRAIN_ABIL[a]
            self.f.tturns = 8 if m.item == 'TERRAIN_EXTENDER' else 5
        if a == 'TRADE_WIND':
            side.tailwind = 3
        if a == 'HELIOTROPISM' and self.weather() == 'SUN':
            self.boost(m, {'atk': 2, 'def': 2, 'spa': 2, 'spd': 2, 'spe': 2}, None)
        if a == 'DAUNTLESS_SHIELD':
            self.boost(m, {'def': 1}, None)
        if a == 'INTREPID_SWORD':
            self.boost(m, {'atk': 1}, None)
        if a == 'DOWNLOAD' and foe.hp > 0:
            self.boost(m, {'atk': 1} if foe.st['def'] < foe.st['spd'] else {'spa': 1}, None)
        if a in ('PROTOSYNTHESIS', 'QUARK_DRIVE'):
            act = (a == 'PROTOSYNTHESIS' and self.weather() == 'SUN') or (a == 'QUARK_DRIVE' and self.f.terrain == 'ELECTRIC')
            if act or m.item == 'BOOSTER_ENERGY':
                best = max(('atk', 'def', 'spa', 'spd', 'spe'), key=lambda s: m.st[s])
                m.proto = best
                if not act:
                    m.item = ''
                    m.lost_item = True
        if a == 'ICE_FACE' and self.weather() == 'SNOW':
            m.ate_ice_face = True

    def boost(self, m, d, src):
        for k, v in d.items():
            kk = 'defn' if k == 'def' else k
            if v < 0 and src is not None and src is not m:
                if m.abil() in ('CLEAR_BODY', 'WHITE_SMOKE', 'FULL_METAL_BODY') or m.ward or m.item == 'CLEAR_AMULET':
                    continue
                if m.abil() == 'MIRROR_ARMOR':
                    self.boost(src, {k: v}, None)
                    continue
                if m.abil() == 'HYPER_CUTTER' and k == 'atk':
                    continue
            if m.abil() == 'CONTRARY':
                v = -v
            if m.abil() == 'SIMPLE':
                v *= 2
            m.boosts[kk] = max(-6, min(6, m.boosts[kk] + v))
            if v < 0 and src is not None and src is not m:
                if m.abil() == 'DEFIANT':
                    m.boosts['atk'] = min(6, m.boosts['atk'] + 2)
                if m.abil() == 'COMPETITIVE':
                    m.boosts['spa'] = min(6, m.boosts['spa'] + 2)

    def set_status(self, m, st, src):
        if not self.can_status(m, st, src):
            return False
        if st == 'POISON' and self.weather() == 'ACID':
            st = 'TOXIC'
        m.status = st
        m.tox = 0
        if st == 'SLEEP':
            m.slp = self.rng.randint(1, 3)
            if m.abil() == 'EARLY_BIRD':
                m.slp = max(1, m.slp // 2)
        if m.abil() == 'SYNCHRONIZE' and src is not None and st in ('BURN', 'PARALYSIS', 'POISON', 'TOXIC'):
            self.set_status(src, st, None)
        if m.item == 'LUM_BERRY':
            m.status = None
            m.item = ''
            m.lost_item = True
            m.unburden = True
        return True

    def do_move(self, side, mk, foe_action):
        me = side.mon
        fside = self.foe(side)
        foe = fside.mon
        if me.hp <= 0:
            return
        data = self.data
        mv = data.moves[mk]
        # slaap / bevriezing / verlamming / verwarring
        if me.status == 'SLEEP':
            me.slp -= 1
            if me.slp > 0:
                if mk == 'SLEEP_TALK':
                    others = [m for m in me.moves if m != 'SLEEP_TALK' and self.usable(m) and data.moves[m]['cat'] != 'STATUS']
                    if not others:
                        return
                    mk = self.rng.choice(others)
                    mv = data.moves[mk]
                else:
                    self.L(me.name, 'slaapt')
                    return
            else:
                me.status = None
        if me.status == 'FREEZE':
            if self.rng.random() < 0.2 or mv['type'] == 'FIRE' and mk in ('FLARE_BLITZ', 'SCALD', 'PYRO_BALL', 'SACRED_FIRE', 'FLAME_WHEEL'):
                me.status = None
            else:
                return
        if me.status == 'PARALYSIS' and self.rng.random() < 0.25:
            self.L(me.name, 'is verlamd')
            return
        if me.conf:
            me.conf -= 1
            if me.conf > 0 and self.rng.random() < 1 / 3:
                d = int((math.floor(math.floor(42 * 40 * self.stat(me, 'atk') / self.stat(me, 'def')) / 50) + 2) * self.rng.uniform(0.85, 1))
                me.hp -= d
                self.L(me.name, 'raakt zichzelf', d)
                if me.hp <= 0:
                    me.hp = 0
                return
        if mk == 'MACHINE_LEARNING' and self.rng.random() < 0.2:
            others = [m for m in data.moves if data.moves[m]['power'] > 1 and self.usable(m) and not data.moves[m]['signature']]
            mk = self.rng.choice(others)
            mv = data.moves[mk]
            self.L(me.name, 'hallucineert:', mk)
            me.streak_keep = True
        if me.abil() == 'TRUANT':
            me.loaf = not getattr(me, 'loaf', True)
            if me.loaf:
                me.turns += 1
                self.L(me.name, 'luiert')
                return
        if me.item.startswith('CHOICE') and mk != 'STRUGGLE':
            me.lock = mk
        if me.abil() in ('PROTEAN', 'LIBERO') and not me.protean:
            me.types = [self.move_type(me, mk)]
            me.protean = True
        prev_last = me.last
        if mk == 'MACHINE_LEARNING' or getattr(me, 'streak_keep', False):
            pass
        me.last = mk
        me.turns += 1
        self.L(me.name, 'gebruikt', mv['name'])
        cat = self.move_cat(me, mk)
        e = mv['effect']
        # ---------------------- status-moves
        if cat == 'STATUS':
            self.status_move(side, me, foe, fside, mk, prev_last)
            return
        if not self.usable(mk):
            return
        if foe.hp <= 0:
            return
        if e == 'SUCKER_PUNCH' and (foe_action is None or foe_action[0] != 'move' or data.moves[foe_action[1]]['cat'] == 'STATUS'
                                    or getattr(foe, 'moved', False)):
            self.L('mislukt')
            return
        if getattr(foe, 'protecting', False) and not (mv['ignoresProtect'] or mk in ('ROLLING_THUNDER', 'AFRO_CHARGE', 'MAWASHI_GERI', 'LASER_BEAM')):
            self.L(foe.name, 'beschermt zich')
            if getattr(foe, 'protecting') == 'PITCHER_TRAP' and mv['contact'] and not me.trap:
                me.trap = 99
                me.trapdmg = me.maxhp / (4 if 'BUG' in me.types else 8)
                foe.pitcher = True
            if getattr(foe, 'protecting') == 'SPIKY_SHIELD' and mv['contact']:
                me.hp -= me.maxhp // 8
            if e == 'RECOIL_IF_MISS':
                me.hp -= me.maxhp // 2
            return
        if foe.gaze:
            foe.gaze = False
            self.L(foe.name, 'zag het aankomen')
            return
        acc = self.accuracy(me, foe, mk)
        n = self.hits(me, mk)
        moving_first = not getattr(foe, 'moved', False)
        total = 0
        ef_last = 1
        da_breaks = me.abil() in MOLD_BREAKERS
        for i in range(int(n) if n == int(n) else 1):
            if (i == 0 or e in ('TRIPLE_KICK', 'POPULATION_BOMB') and mk != 'COMBINATION') and self.rng.random() > acc:
                if i == 0:
                    self.L('mist')
                    if e == 'RECOIL_IF_MISS':
                        me.hp -= me.maxhp // 2
                break
            if foe.hp <= 0:
                break
            crit = self.rng.random() < self.crit_chance(me, foe, mk)
            if mk == 'COMBINATION' and i == 2:
                crit = True
            dmg, ef = self.damage(me, foe, mk, side, fside, crit, self.rng.uniform(0.85, 1.0), i, False, foe_action, moving_first)
            ef_last = ef
            if ef == 0:
                self.absorb_effect(foe, me, mk)
                self.L('geen effect')
                break
            # Disguise / Ice Face
            if foe.disguise and foe.abil(ign=da_breaks) == 'DISGUISE':
                foe.disguise = False
                foe.hp -= foe.maxhp // 8
                continue
            if foe.ate_ice_face and foe.abil(ign=da_breaks) == 'ICE_FACE' and cat == 'PHYSICAL':
                foe.ate_ice_face = False
                continue
            if foe.burrow > 0:
                foe.burrow -= 1
                self.L(foe.name, 'glipt in een hol')
                break
            # Sturdy / Focus Sash
            if dmg >= foe.hp and foe.hp == foe.maxhp and (foe.abil(ign=da_breaks) == 'STURDY' or foe.item == 'FOCUS_SASH'):
                dmg = foe.hp - 1
                if foe.item == 'FOCUS_SASH':
                    foe.item = ''
                    foe.lost_item = True
            if dmg >= foe.hp and foe.nine_lives:
                foe.nine_lives = False
                dmg = foe.hp - 1
                foe.status = None
            dmg = min(dmg, foe.hp)
            foe.hp -= dmg
            total += dmg
            foe.hits_taken += 1
            self.L('  ', dmg, 'schade (%s, %d%% over)%s' % (foe.name, 100 * foe.frac(), ' crit' if crit else ''))
            # contact-effecten
            self.on_hit(me, foe, mk, side, fside, dmg, ef)
            if me.hp <= 0:
                break
        if total <= 0:
            return
        self.after_hit(side, me, foe, fside, mk, total, ef_last)

    def absorb_effect(self, dfn, att, mk):
        t = self.move_type(att, mk)
        a = dfn.abil()
        if a in ('VOLT_ABSORB', 'WATER_ABSORB', 'EARTH_EATER', 'DRY_SKIN') :
            dfn.hp = min(dfn.maxhp, dfn.hp + dfn.maxhp // 4)
        elif a == 'LIGHTNING_ROD' or a == 'STORM_DRAIN':
            self.boost(dfn, {'spa': 1}, None)
        elif a == 'MOTOR_DRIVE':
            self.boost(dfn, {'spe': 1}, None)
        elif a == 'SAP_SIPPER':
            self.boost(dfn, {'atk': 1}, None)
        elif a == 'FLASH_FIRE':
            dfn.flashfire = True
        elif a == 'WELL_BAKED_BODY':
            self.boost(dfn, {'def': 2}, None)
        elif a == 'WIND_RIDER':
            self.boost(dfn, {'atk': 1}, None)

    def on_hit(self, me, foe, mk, side, fside, dmg, ef):
        mv = self.data.moves[mk]
        contact = mv['contact'] and me.item != 'PUNCHING_GLOVE' and not (me.item == 'PROTECTIVE_PADS') and me.abil() != 'LONG_REACH'
        fa = foe.abil(ign=me.abil() in MOLD_BREAKERS)
        mg = me.abil() == 'MAGIC_GUARD'
        if contact:
            if fa in ('ROUGH_SKIN', 'IRON_BARBS') and not mg:
                me.hp -= me.maxhp // 8
            if foe.item == 'ROCKY_HELMET' and not mg:
                me.hp -= me.maxhp // 6
            if fa == 'FLAME_BODY' and self.rng.random() < 0.3:
                self.set_status(me, 'BURN', foe)
            if fa == 'STATIC' and self.rng.random() < 0.3:
                self.set_status(me, 'PARALYSIS', foe)
            if fa == 'POISON_POINT' and self.rng.random() < 0.3:
                self.set_status(me, 'POISON', foe)
            if fa == 'EFFECT_SPORE' and 'GRASS' not in me.types and self.rng.random() < 0.3:
                self.set_status(me, self.rng.choice(['SLEEP', 'PARALYSIS', 'POISON']), foe)
            if fa == 'MUMMY' or fa == 'WANDERING_SPIRIT':
                me.mummy = True
            if fa == 'GOOEY' or fa == 'TANGLING_HAIR':
                self.boost(me, {'spe': -1}, foe)
            if fa == 'CURSED_BODY':
                pass
        if fa == 'SPICY_SPRAY' and dmg > 0:
            self.set_status(me, 'BURN', foe)
        if fa == 'STAMINA':
            self.boost(foe, {'def': 1}, None)
        if fa == 'WEAK_ARMOR' and self.move_cat(me, mk) == 'PHYSICAL':
            self.boost(foe, {'def': -1, 'spe': 2}, None)
        if fa == 'ELECTROMORPHOSIS':
            foe.charge = True
        if fa in ('JUSTIFIED',) and self.move_type(me, mk) == 'DARK':
            self.boost(foe, {'atk': 1}, None)
        if fa == 'STEAM_ENGINE' and self.move_type(me, mk) in ('FIRE', 'WATER'):
            self.boost(foe, {'spe': 6}, None)
        if fa == 'THERMAL_EXCHANGE' and self.move_type(me, mk) == 'FIRE':
            self.boost(foe, {'atk': 1}, None)
        if fa == 'WATER_COMPACTION' and self.move_type(me, mk) == 'WATER':
            self.boost(foe, {'def': 2}, None)
        if fa == 'ANGER_POINT' and False:
            pass
        if foe.item == 'WEAKNESS_POLICY' and ef > 1 and foe.hp > 0:
            self.boost(foe, {'atk': 2, 'spa': 2}, None)
            foe.item = ''
            foe.lost_item = True
        if foe.item == 'AIR_BALLOON':
            foe.item = ''
            foe.lost_item = True
        if foe.item == 'SITRUS_BERRY' and 0 < foe.hp <= foe.maxhp // 2:
            foe.hp += foe.maxhp // 4
            foe.item = ''
            foe.lost_item = True
            foe.unburden = True
        if me.hp < 0:
            me.hp = 0

    def after_hit(self, side, me, foe, fside, mk, total, ef):
        mv = self.data.moves[mk]
        e = mv['effect']
        sheer = me.abil() == 'SHEER_FORCE' and any(not x['self'] for x in mv['adds'])
        mg = me.abil() == 'MAGIC_GUARD'
        # drain / recoil / life orb
        if mv['drain']:
            amt = total * mv['drain'] // 100
            if me.item == 'BIG_ROOT':
                amt = int(amt * 1.3)
            if foe.abil() == 'LIQUID_OOZE':
                me.hp -= amt
            else:
                me.hp = min(me.maxhp, me.hp + amt)
        if mk == 'FLYTRAP':
            me.hp = min(me.maxhp, me.hp + total // 2)
        if mv['recoil'] and me.abil() not in ('ROCK_HEAD', 'MAGIC_GUARD'):
            me.hp -= max(1, total * mv['recoil'] // 100)
        if e == 'RECOIL' and not mv['recoil'] and me.abil() not in ('ROCK_HEAD', 'MAGIC_GUARD'):
            me.hp -= max(1, total // 3)
        if me.item == 'LIFE_ORB' and not sheer and not mg:
            me.hp -= me.maxhp // 10
        if me.item == 'SHELL_BELL':
            me.hp = min(me.maxhp, me.hp + total // 8)
        if e in ('KNOCK_OFF',) and foe.item and foe.hp >= 0 and not (foe.abil() == 'STICKY_HOLD'):
            foe.item = ''
            foe.lost_item = True
        if mk == 'GULP_DOWN' and foe.item:
            foe.item = ''
            foe.lost_item = True
            me.hp = min(me.maxhp, me.hp + me.maxhp // 4)
        # bijeffecten
        sf = me.abil() == 'SERENE_GRACE'
        for x in mv['adds']:
            if sheer and not x['self']:
                continue
            ch = x['chance'] or 100
            if sf:
                ch = min(100, ch * 2)
            if x['eff'] in ('POISON', 'TOXIC') and self.weather() == 'ACID':
                ch = 100 if ch >= 50 else ch * 2
            if not x['self'] and foe.abil() == 'SHIELD_DUST' or not x['self'] and foe.item == 'COVERT_CLOAK':
                if x['chance']:
                    continue
            if self.rng.random() * 100 >= ch:
                continue
            self.apply_effect(me, foe, side, fside, x, mk)
        if mk == 'TWIN_LANCE' and foe.status == 'POISON':
            foe.status = 'TOXIC'
        if e == 'RAPID_SPIN':
            for k in side.haz:
                side.haz[k] = 0
            me.seeded = False
            me.trap = 0
        if e == 'CEASELESS_EDGE' and fside.haz['spikes'] < 3:
            fside.haz['spikes'] += 1
        if e == 'STONE_AXE':
            fside.haz['sr'] = 1
        if mk == 'BRAMBLE_LASH' and fside.haz['spikes'] < 3:
            fside.haz['spikes'] += 1
        if mk == 'TOTEM_GAZE':
            me.gaze = True
        if mk in ('KELP_SHROUD',) and 'GRASS' not in foe.types:
            foe.seeded = True
        if mk == 'ICE_SPINNER':
            self.f.terrain = None
        if mk in ('BEAR_HUG', 'HYPHAL_SNARE', 'MAGMA_STORM', 'STEEL_TRAP', 'MUMMYS_CURSE') and not foe.trap and \
           not (mk == 'HYPHAL_SNARE' and 'GRASS' in foe.types):
            foe.trap = self.rng.randint(4, 5)
            foe.trapdmg = foe.maxhp / 8
        if mk == 'MUMMYS_CURSE':
            foe.mummy = True
        # KO-abilities
        if foe.hp <= 0:
            foe.hp = 0
            a = me.abil()
            if a in ('MOXIE', 'CHILLING_NEIGH', 'AS_ONE_ICE'):
                self.boost(me, {'atk': 1}, None)
            if a in ('GRIM_NEIGH', 'AS_ONE_SHADOW'):
                self.boost(me, {'spa': 1}, None)
            if a in ('BEAST_BOOST', 'EELEVATE'):
                best = max(('atk', 'def', 'spa', 'spd', 'spe'), key=lambda s: me.st[s])
                self.boost(me, {best: 1}, None)
            if foe.abil() == 'AFTERMATH' and mv['contact']:
                me.hp -= me.maxhp // 4
            if foe.abil() == 'INNARDS_OUT':
                me.hp -= total
        if me.hp < 0:
            me.hp = 0
        # pivots
        if self.mode == 'team' and me.hp > 0 and len(side.alive()) > 1 and \
           (mk in PIVOT or (me.abil() == 'HOLE_UP' and foe.hp <= 0 and len(fside.alive()) > 0)):
            if foe.hp > 0:
                idx, val = self.best_switch(side, entry_hit=0, foe_move=None)
                cur = self.race(me, foe, side, fside)
                if idx is not None and val > cur + 0.05:
                    side.switches += 1
                    self.switch_in(side, idx)
            else:
                side.pending_pivot = True

    def apply_effect(self, me, foe, side, fside, x, mk):
        eff = x['eff']
        tgt = me if x['self'] else foe
        if tgt.hp <= 0 and not x['self']:
            return
        src = None if x['self'] else me
        m = re.match(r'(ATK|DEF|SP_ATK|SP_DEF|SPD|ACC|EVS)_(PLUS|MINUS)_(\d)', eff)
        if m:
            k = {'ATK': 'atk', 'DEF': 'def', 'SP_ATK': 'spa', 'SP_DEF': 'spd', 'SPD': 'spe', 'ACC': 'acc', 'EVS': 'eva'}[m.group(1)]
            v = int(m.group(3)) * (1 if m.group(2) == 'PLUS' else -1)
            if mk == 'FROSTY_TAP_DANCE' and k == 'spa' and self.weather() != 'SNOW':
                return
            self.boost(tgt, {k: v}, src)
            return
        if eff == 'DEF_SPDEF_DOWN':
            self.boost(tgt, {'def': -1, 'spd': -1}, src)
        elif eff == 'ATK_DEF_DOWN':
            self.boost(tgt, {'atk': -1, 'def': -1}, src)
        elif eff == 'V_CREATE':
            self.boost(tgt, {'def': -1, 'spd': -1, 'spe': -1}, src)
        elif eff in ('BURN', 'PARALYSIS', 'POISON', 'TOXIC', 'SLEEP', 'FREEZE', 'FREEZE_OR_FROSTBITE'):
            st = 'FREEZE' if eff.startswith('FREEZE') else eff
            if st == 'SLEEP' and any(mm.status == 'SLEEP' for mm in fside.team):
                return
            self.set_status(tgt, st, me)
        elif eff == 'TRI_ATTACK':
            self.set_status(tgt, self.rng.choice(['BURN', 'PARALYSIS', 'FREEZE']), me)
        elif eff == 'CONFUSION':
            if not tgt.conf and tgt.abil() != 'OWN_TEMPO':
                tgt.conf = self.rng.randint(2, 5)
        elif eff == 'FLINCH':
            if not getattr(tgt, 'moved', False):
                tgt.flinched = True
        elif eff == 'SALT_CURE':
            tgt.salt = True
        elif eff in ('WRAP',):
            if not tgt.trap:
                tgt.trap = self.rng.randint(4, 5)
                tgt.trapdmg = tgt.maxhp / 8
        elif eff == 'CLEAR_SMOG':
            for k in tgt.boosts:
                tgt.boosts[k] = 0
        elif eff == 'SCALE_SHOT':
            self.boost(me, {'spe': 1, 'def': -1}, None)
        elif eff == 'THRASH':
            if not getattr(me, 'thrash', 0):
                me.thrash = self.rng.randint(1, 2)
                me.thrash_move = mk
        elif eff == 'LEECH_SEED':
            if 'GRASS' not in tgt.types:
                tgt.seeded = True
        elif eff == 'TWIN_TAILS':
            ups = [k for k, v in tgt.boosts.items() if v > 0]
            if ups:
                k = self.rng.choice(ups)
                tgt.boosts[k] -= 1
                me.boosts[k] = min(6, me.boosts[k] + 1)

    def status_move(self, side, me, foe, fside, mk, prev_last):
        data = self.data
        mv = data.moves[mk]
        if me.abil() == 'PRANKSTER' and 'DARK' in foe.types and mv['target'] in ('SELECTED', 'BOTH', 'FOES_AND_ALLY'):
            return
        reflect = foe.abil() == 'MAGIC_BOUNCE' and mv['target'] in ('SELECTED', 'BOTH', 'FOES_AND_ALLY', 'OPPONENTS_FIELD')
        if foe.abil() == 'GOOD_AS_GOLD' and mv['target'] in ('SELECTED', 'BOTH'):
            return
        if reflect:
            me, foe, side, fside = foe, me, fside, side
        if mk in SETUP:
            if mk == 'MACHINE_LEARNING':
                if prev_last != 'MACHINE_LEARNING':
                    me.ml = 0
                b = self.ml_boosts(me)
                me.ml += 1
                self.boost(me, b, None)
            elif mk == 'BELLY_DRUM':
                if me.hp * 2 > me.maxhp:
                    me.hp -= me.maxhp // 2
                    me.boosts['atk'] = 6
            elif mk == 'GROWTH' and self.weather() == 'SUN':
                self.boost(me, {'atk': 2, 'spa': 2}, None)
            elif mk == 'THE_OLD_DAYS':
                self.boost(me, {'spa': 1}, None)
                if not foe.yawn and self.can_status(foe, 'SLEEP', me):
                    foe.yawn = 2
            elif mk == 'PRIMEVAL_WARD':
                self.boost(me, {'def': 1, 'spd': 1}, None)
                me.ward = True
            else:
                self.boost(me, SETUP[mk], None)
            if mk in ('STOCKPILE', 'BEAVER_DAM'):
                me.streak += 1
            return
        if mk in HEAL:
            frac = HEAL[mk]
            w = self.weather()
            if mk in ('MOONLIGHT', 'MORNING_SUN', 'SYNTHESIS'):
                frac = 2 / 3 if w == 'SUN' else 0.25 if w in ('RAIN', 'SAND', 'SNOW', 'ACID') else 0.5
            if mk == 'SHORE_UP' and w == 'SAND':
                frac = 2 / 3
            if mk == 'OLIVE_OIL':
                frac = 2 / 3 if w == 'POLLEN' else 0.5
                self.f.terrain, self.f.tturns = 'GRASSY', 5
            if mk == 'STRENGTH_SAP':
                amt = self.stat(foe, 'atk')
                self.boost(foe, {'atk': -1}, me)
                me.hp = min(me.maxhp, me.hp + int(amt))
                return
            if mk == 'WISH':
                side.wish = (self.turn + 1, me.maxhp // 2)
                return
            if mk == 'REST':
                me.hp = me.maxhp
                me.status = 'SLEEP'
                me.slp = 3
                return
            me.hp = min(me.maxhp, me.hp + int(me.maxhp * frac))
            return
        if mk in STATUS_MOVES:
            st = STATUS_MOVES[mk]
            if self.rng.random() > self.accuracy(me, foe, mk):
                return
            if mv['powder'] and ('GRASS' in foe.types or foe.abil() == 'OVERCOAT' or foe.item == 'SAFETY_GOGGLES'):
                return
            if st == 'YAWN':
                if not foe.status and not foe.yawn and self.can_status(foe, 'SLEEP', me):
                    foe.yawn = 2
                return
            if st == 'SLEEP' and any(mm.status == 'SLEEP' for mm in fside.team):
                return
            if mk == 'THUNDER_WAVE' and data.eff('ELECTRIC', foe.types) == 0:
                return
            self.set_status(foe, st, me)
            if mk in ('VENOM_DUST', 'TOXIC_THREAD'):
                self.boost(foe, {'spe': -1}, me)
            return
        if mk in HAZARD_MOVES:
            k = HAZARD_MOVES[mk]
            cap = {'sr': 1, 'spikes': 3, 'tspikes': 2, 'moai': 1, 'web': 1}[k]
            fside.haz[k] = min(cap, fside.haz[k] + 1)
            return
        if mk in ('DEFOG', 'TIDY_UP'):
            for s in (side, fside):
                for k in s.haz:
                    s.haz[k] = 0
            if self.f.weather == 'ACID' and mk == 'DEFOG':
                self.f.weather = None
            if mk == 'DEFOG':
                fside.reflect = fside.lscreen = fside.veil = 0
            return
        if mk in WEATHER_MOVES:
            w = WEATHER_MOVES[mk]
            if self.f.weather != w and not self.f.harsh:
                self.f.weather = w
                self.f.wturns = 8 if me.item == WEATHER_ROCK.get(w) else 5
            if mk == 'CHILLY_RECEPTION' and self.mode == 'team':
                side.pending_pivot = True
            return
        if mk == 'TAILWIND':
            side.tailwind = 4
            return
        if mk == 'TRICK_ROOM':
            self.f.tr = 0 if self.f.tr else 5
            return
        if mk == 'REFLECT':
            side.reflect = 8 if me.item == 'LIGHT_CLAY' else 5
            return
        if mk == 'LIGHT_SCREEN':
            side.lscreen = 8 if me.item == 'LIGHT_CLAY' else 5
            return
        if mk in ('AURORA_VEIL', 'BUBBLE_DOME'):
            side.veil = 8 if me.item == 'LIGHT_CLAY' else 5
            return
        if mk == 'LEECH_SEED':
            if 'GRASS' not in foe.types and self.rng.random() < 0.9:
                foe.seeded = True
            return
        if mk == 'PAIN_SPLIT':
            avg = (me.hp + foe.hp) // 2
            me.hp, foe.hp = min(me.maxhp, avg), min(foe.maxhp, avg)
            return
        if mk == 'HAZE':
            for m in (me, foe):
                for k in m.boosts:
                    m.boosts[k] = 0
            return
        if mk in ('PROTECT', 'SPIKY_SHIELD', 'BANEFUL_BUNKER', 'KINGS_SHIELD', 'SILK_TRAP', 'BURNING_BULWARK', 'DETECT',
                  'PITCHER_TRAP', 'OBSTRUCT'):
            if prev_last == mk:
                return
            me.protecting = mk
            return
        if mk in ('ROAR', 'WHIRLWIND') and self.mode == 'team':
            opts = [i for i in fside.alive() if i != fside.active]
            if opts:
                self.switch_in(fside, self.rng.choice(opts))
            return
        if mk == 'PARTING_SHOT':
            self.boost(foe, {'atk': -1, 'spa': -1}, me)
            if self.mode == 'team':
                side.pending_pivot = True
            return
        if mk == 'EYE_SPOTS':
            self.boost(foe, {'atk': -1, 'spe': -1}, me)
            if self.weather() == 'POLLEN' and not foe.conf:
                foe.conf = self.rng.randint(2, 5)
            return
        if mk == 'BURROW_MAZE':
            if not me.trap:
                me.burrow = min(3, me.burrow + 1)
            return
        if mk == 'NINE_LIVES':
            return
        if mk in ('LURE_LIGHT',):
            return

    def end_turn(self):
        w = self.weather()
        for side in self.sides:
            m = side.mon
            if m.hp <= 0:
                continue
            a = m.abil()
            mg = a == 'MAGIC_GUARD'
            mh = m.maxhp
            # wish
            if side.wish and side.wish[0] == self.turn:
                m.hp = min(mh, m.hp + side.wish[1])
                side.wish = None
            # weer
            if w == 'SAND' and not set(m.types) & {'ROCK', 'GROUND', 'STEEL'} and a not in ('SAND_VEIL', 'SAND_RUSH', 'SAND_FORCE', 'OVERCOAT', 'MAGIC_GUARD') \
               and m.item != 'SAFETY_GOGGLES':
                m.hp -= mh // 16
            if w == 'ACID':
                if 'POISON' in m.types:
                    m.hp = min(mh, m.hp + mh // 16)
                elif 'STEEL' not in m.types and a not in ('OVERCOAT', 'FORECAST', 'MAGIC_GUARD') and \
                        m.item not in ('SAFETY_GOGGLES', 'UTILITY_UMBRELLA'):
                    m.hp -= mh // 16
                if a == 'LANDFILL':
                    self.boost(m, {'def': 1, 'spd': 1}, None)
            if w == 'POLLEN' and ('GRASS' in m.types or a == 'FAKE_FOLIAGE'):
                m.hp = min(mh, m.hp + mh // 16)
            if w == 'RAIN' and a in ('RAIN_DISH', 'DRY_SKIN'):
                m.hp = min(mh, m.hp + mh // (16 if a == 'RAIN_DISH' else 8))
            if w == 'SUN' and a in ('DRY_SKIN', 'SOLAR_POWER') and not mg:
                m.hp -= mh // 8
            if w == 'SNOW' and a == 'ICE_BODY':
                m.hp = min(mh, m.hp + mh // 16)
            if self.f.terrain == 'GRASSY' and self.grounded(m):
                m.hp = min(mh, m.hp + mh // 16)
            # items
            if m.item == 'LEFTOVERS' or (m.item == 'BLACK_SLUDGE' and 'POISON' in m.types):
                m.hp = min(mh, m.hp + mh // 16)
            elif m.item == 'BLACK_SLUDGE' and not mg:
                m.hp -= mh // 8
            # status
            if m.status == 'BURN' and not mg:
                m.hp -= mh // (32 if a == 'HEATPROOF' else 16)
            if m.status in ('POISON', 'TOXIC'):
                if a == 'POISON_HEAL':
                    m.hp = min(mh, m.hp + mh // 8)
                elif not mg:
                    if m.status == 'TOXIC':
                        m.tox += 1
                        m.hp -= mh * min(15, m.tox) // 16
                    else:
                        m.hp -= mh // 8
            foe = self.foe(side).mon
            if m.seeded and not mg and foe.hp > 0:
                d = mh // 8
                m.hp -= d
                if foe.abil() != 'MAGIC_GUARD' or True:
                    foe.hp = min(foe.maxhp, foe.hp + d)
            if m.salt and not mg:
                m.hp -= mh // (4 if set(m.types) & {'WATER', 'STEEL'} else 8)
            if m.trap:
                if not mg:
                    d = int(m.trapdmg)
                    m.hp -= d
                    if m.trap == 99 and foe.pitcher and foe.hp > 0:
                        foe.hp = min(foe.maxhp, foe.hp + d)
                if m.trap != 99:
                    m.trap -= 1
            if m.yawn:
                m.yawn -= 1
                if m.yawn == 0 and not m.status:
                    self.set_status(m, 'SLEEP', None)
            if a == 'SPEED_BOOST' and m.turns > 0:
                self.boost(m, {'spe': 1}, None)
            if m.item == 'TOXIC_ORB' and not m.status:
                self.set_status(m, 'TOXIC', None)
            if m.item == 'FLAME_ORB' and not m.status:
                self.set_status(m, 'BURN', None)
            if m.item == 'SITRUS_BERRY' and 0 < m.hp <= mh // 2:
                m.hp += mh // 4
                m.item = ''
                m.lost_item = True
            if m.hp < 0:
                m.hp = 0
            m.protecting = False
            m.flinched = False
            m.moved = False
        # tellers
        if self.f.weather:
            self.f.wturns -= 1
            if self.f.wturns <= 0:
                self.f.weather = None
        if self.f.terrain:
            self.f.tturns -= 1
            if self.f.tturns <= 0:
                self.f.terrain = None
        if self.f.tr:
            self.f.tr -= 1
        for s in self.sides:
            for k in ('tailwind', 'reflect', 'lscreen', 'veil'):
                if getattr(s, k):
                    setattr(s, k, getattr(s, k) - 1)

    # ---------------------------------------------------------------- hoofdlus
    def run(self, max_turns=150):
        A, B = self.sides
        for s in self.sides:
            s.pending_pivot = False
        self.switch_in(A, 0, initial=True, entry=False)
        self.switch_in(B, 0, initial=True, entry=False)
        # entry-abilities: de snelste eerst, dus bij twee weer-abilities wint de langzaamste
        first = [A, B] if self.speed(A.mon, A) >= self.speed(B.mon, B) else [B, A]
        for s in first:
            self.entry_ability(s, s.mon)
        while self.turn < max_turns:
            self.turn += 1
            for s in self.sides:
                if s.mon.hp <= 0:
                    if not self.replace(s):
                        return self.result()
            acts = [self.choose(A), self.choose(B)]
            # wissels eerst
            for i, s in enumerate(self.sides):
                if acts[i][0] == 'switch':
                    s.switches += 1
                    foe_act = acts[1 - i]
                    self.switch_in(s, acts[i][1])
            # volgorde
            order = [0, 1]
            mk0 = acts[0][1] if acts[0][0] == 'move' else None
            mk1 = acts[1][1] if acts[1][0] == 'move' else None
            if mk0 and mk1:
                p0 = self.priority(A.mon, mk0, A, B)
                p1 = self.priority(B.mon, mk1, B, A)
                if p0 != p1:
                    order = [0, 1] if p0 > p1 else [1, 0]
                else:
                    s0, s1 = self.speed(A.mon, A), self.speed(B.mon, B)
                    if self.f.tr:
                        s0, s1 = -s0, -s1
                    if s0 == s1:
                        order = self.rng.sample([0, 1], 2)
                    else:
                        order = [0, 1] if s0 > s1 else [1, 0]
            for i in order:
                if acts[i][0] != 'move':
                    continue
                s = self.sides[i]
                m = s.mon
                if m.hp <= 0 or getattr(m, 'flinched', False):
                    m.flinched = False
                    continue
                self.do_move(s, acts[i][1], acts[1 - i])
                m.moved = True
                for ss in self.sides:
                    if getattr(ss, 'pending_pivot', False):
                        ss.pending_pivot = False
                        if ss.mon.hp > 0 and len(ss.alive()) > 1:
                            idx, val = self.best_switch(ss, forced=False)
                            if idx is not None:
                                self.switch_in(ss, idx)
                if self.over():
                    return self.result()
            self.end_turn()
            if self.over():
                return self.result()
        return self.result()

    def replace(self, s):
        if s.mon.hp > 0:
            return True
        s.fainted = len(s.team) - len(s.alive())
        alive = s.alive()
        if not alive:
            return False
        if self.mode != 'team':
            return False
        idx, _ = self.best_switch(s, forced=True)
        self.switch_in(s, idx if idx is not None else alive[0])
        if s.mon.hp <= 0:
            return self.replace(s)
        return True

    def over(self):
        for s in self.sides:
            s.fainted = len(s.team) - len(s.alive())
        return any(not s.alive() for s in self.sides)

    def result(self):
        a, b = len(self.sides[0].alive()), len(self.sides[1].alive())
        if a and not b:
            return 1.0
        if b and not a:
            return 0.0
        # gelijk of tijdslimiet: op resterende HP
        ha = sum(m.frac() for m in self.sides[0].team)
        hb = sum(m.frac() for m in self.sides[1].team)
        return 0.5 if abs(ha - hb) < 1e-6 else (0.75 if ha > hb else 0.25) if (a and b) else 0.5


def duel(set1, set2, data, n=20, seed=1):
    """1-tegen-1 (zonder wissels). Geeft winstkans van set1."""
    rng = random.Random(seed)
    tot = 0.0
    for _ in range(n):
        b = Battle([set1], [set2], data, rng=rng, mode='duel')
        tot += b.run(60)
    return tot / n


def team_battle(t1, t2, data, n=20, seed=1, log=False):
    rng = random.Random(seed)
    tot = 0.0
    last = None
    for _ in range(n):
        b = Battle(t1, t2, data, rng=rng, mode='team', log=log)
        tot += b.run(200)
        last = b
    return tot / n, last


