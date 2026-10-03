"""Volledige data voor de Spire-rekenscripts: soorten (met evoluties, abilities, vlaggen en learnsets)
en moves (met effect, bijeffecten, prioriteit). Leest alles uit de broncode; geen eigen kopieën."""
import glob, os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))


def _read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f:
        return f.read()


_COND = re.compile(r'\(?\s*[BP]_UPDATED_\w+\s*>=\s*GEN_\d+(?:\s*\|\|\s*[BP]_UPDATED_\w+\s*==\s*GEN_\d+)?\s*\?\s*([^:,]+?)\s*:\s*[^,)}\n]+\)?')


def _resolve_updated(txt):
    """'B_UPDATED_MOVE_DATA >= GEN_6 ? 40 : 20' -> '40' (expansion neemt de nieuwste generatie)."""
    return _COND.sub(lambda m: m.group(1), txt)


def _blocks(txt, key):
    """Splits '[KEY_X] = { ... }' blokken (top-level, 4 spaties ingesprongen)."""
    out = {}
    for m in re.finditer(r'\n    \[%s_(\w+)\]\s*=\s*\{' % key, txt):
        start = m.end()
        end = txt.find('\n    },', start)
        out[m.group(1)] = txt[start:end]
    return out


# ---------------------------------------------------------------------------------------------
# moves

def load_moves():
    txt = _resolve_updated(_read('src/data/moves_info.h'))
    moves = {}
    for name, body in _blocks(txt, 'MOVE').items():
        def f(field, default=None, conv=str):
            m = re.search(r'\.%s\s*=\s*([^,\n]+)' % field, body)
            if not m:
                return default
            v = m.group(1).strip()
            try:
                return conv(v)
            except ValueError:
                return default
        dname = re.search(r'\.name\s*=\s*COMPOUND_STRING\("([^"]*)"\)', body)
        effects = re.findall(r'\.moveEffect\s*=\s*MOVE_EFFECT_(\w+)(?:,\s*\.self\s*=\s*TRUE)?', body)
        selfs = re.findall(r'\.moveEffect\s*=\s*MOVE_EFFECT_\w+,\s*(?:\.\w+\s*=\s*\w+,\s*)*\.self\s*=\s*TRUE', body)
        chances = [int(c) for c in re.findall(r'\.chance\s*=\s*(\d+)', body)]
        moves[name] = dict(
            name=dname.group(1) if dname else name.title(),
            effect=(f('effect', 'EFFECT_HIT') or 'EFFECT_HIT').replace('EFFECT_', ''),
            power=f('power', 0, int), type=(f('type', 'TYPE_NORMAL') or '').replace('TYPE_', ''),
            acc=f('accuracy', 0, int), pp=f('pp', 0, int), priority=f('priority', 0, int),
            target=(f('target', 'MOVE_TARGET_SELECTED') or '').replace('MOVE_TARGET_', ''),
            cat=(f('category', 'DAMAGE_CATEGORY_STATUS') or '').replace('DAMAGE_CATEGORY_', ''),
            strikes=f('strikeCount', 1, int),
            add=effects, addChance=chances, selfEffect=bool(selfs),
            recoil=f('recoilPercentage', 0, int) or (25 if 'recoil' in body.lower() and 'RECOIL' in body else 0),
            drain='EFFECT_ABSORB' in body or 'drainPercentage' in body,
            charge='TWO_TURN' in body or 'SOLAR_BEAM' in body or 'SKY_ATTACK' in body,
            recharge='RECHARGE' in body,
            sound='soundMove = TRUE' in body,
            contact='makesContact = TRUE' in body,
            signature='isSignatureMove' in body,
            zmove='EFFECT_MAX_MOVE' in body or 'Z_MOVE' in name or name.startswith('MAX_') or name.startswith('G_MAX'),
            body=body,
        )
    return moves


# ---------------------------------------------------------------------------------------------
# learnsets

def load_levelup():
    txt = _read('src/data/pokemon/level_up_learnsets/gen_9.h')
    out = {}
    for m in re.finditer(r'static const struct LevelUpMove (\w+)\[\] = \{(.*?)\};', txt, re.S):
        out[m.group(1)] = [(int(l), mv) for l, mv in re.findall(r'LEVEL_UP_MOVE\(\s*(\d+),\s*MOVE_(\w+)\)', m.group(2))]
    return out


def load_movelists(path):
    txt = _read(path)
    out = {}
    for m in re.finditer(r'static const u16 (\w+)\[\] = \{(.*?)\};', txt, re.S):
        out[m.group(1)] = [x for x in re.findall(r'MOVE_(\w+)', m.group(2)) if x != 'UNAVAILABLE']
    return out


# ---------------------------------------------------------------------------------------------
# soorten

FLAGS = ('isLegendary', 'isMythical', 'isUltraBeast', 'isParadox', 'isMegaEvolution', 'isGigantamax',
         'isTotem', 'isPrimalReversion', 'isTeraForm', 'isUltraBurst', 'isFrontierBanned',
         'isAlolanForm', 'isGalarianForm', 'isHisuianForm', 'isPaldeanForm', 'cannotBeTraded')


def load_species():
    levelup = load_levelup()
    teach = load_movelists('src/data/pokemon/teachable_learnsets.h')
    eggs = load_movelists('src/data/pokemon/egg_moves.h')
    allsrc = ''.join(open(p, encoding='utf-8').read() for p in glob.glob(os.path.join(ROOT, 'src/data/pokemon/species_info/*.h')))
    macros = {}
    for m in re.finditer(r'#define\s+(\w+)[ \t]+(.+)', _resolve_updated(allsrc)):
        if m.group(1) not in macros:     # eerste definitie = nieuwste generatie
            v = m.group(2).strip()
            v = re.sub(r'^\((\d+)\)$', r'\1', v)
            macros[m.group(1)] = v
    out = {}
    for path in sorted(glob.glob(os.path.join(ROOT, 'src/data/pokemon/species_info/gen_*_families.h'))):
        txt = _resolve_updated(open(path, encoding='utf-8').read())
        for name, body in _blocks(txt, 'SPECIES').items():
            body = re.sub(r'\b[A-Z][A-Z0-9_]+\b', lambda m: macros.get(m.group(0), m.group(0)), body)
            d = {}
            ok = True
            for key, field in (('hp', 'baseHP'), ('atk', 'baseAttack'), ('def', 'baseDefense'),
                               ('spe', 'baseSpeed'), ('spa', 'baseSpAttack'), ('spd', 'baseSpDefense')):
                f = re.search(r'\.%s\s*=\s*(\d+)' % field, body)
                if not f:
                    ok = False
                    break
                d[key] = int(f.group(1))
            t = re.search(r'(?:MON_TYPES\(|\.types\s*=\s*\{\s*)TYPE_(\w+)(?:,\s*TYPE_(\w+))?\s*[)}]', body)
            if not ok or not t:
                continue
            d['types'] = [t.group(1)] + ([t.group(2)] if t.group(2) and t.group(2) != t.group(1) else [])
            ab = re.search(r'\.abilities\s*=\s*\{([^}]*)\}', body)
            d['abilities'] = [a.replace('ABILITY_', '') for a in re.findall(r'ABILITY_\w+', ab.group(1))] if ab else []
            eg = re.search(r'MON_EGG_GROUPS\(([^)]*)\)', body)
            d['eggGroups'] = re.findall(r'EGG_GROUP_(\w+)', eg.group(1)) if eg else []
            dn = re.search(r'\.speciesName\s*=\s*_\("([^"]*)"\)', body)
            d['dispname'] = dn.group(1) if dn else name.title()
            for fl in FLAGS:
                d[fl] = bool(re.search(r'\.%s\s*=\s*TRUE' % fl, body))
            d['evos'] = []
            ei = body.find('.evolutions = EVOLUTION(')
            if ei >= 0:
                i = body.index('(', ei) + 1
                depth, start = 0, None
                while i < len(body):
                    c = body[i]
                    if c == '{':
                        if depth == 0:
                            start = i
                        depth += 1
                    elif c == '}':
                        depth -= 1
                        if depth == 0:
                            e = re.match(r'\{EVO_(\w+),\s*([^,]+),\s*SPECIES_(\w+)(.*)\}', body[start:i + 1], re.S)
                            if e:
                                d['evos'].append(dict(method=e.group(1), param=e.group(2).strip(), target=e.group(3),
                                                      cond='CONDITIONS' in e.group(4), condtext=e.group(4)))
                    elif c == ')' and depth == 0:
                        break
                    i += 1
            lu = re.search(r'\.levelUpLearnset\s*=\s*(\w+)', body)
            te = re.search(r'\.teachableLearnset\s*=\s*(\w+)', body)
            em = re.search(r'\.eggMoveLearnset\s*=\s*(\w+)', body)
            d['levelup'] = levelup.get(lu.group(1), []) if lu else []
            d['teach'] = teach.get(te.group(1), []) if te else []
            d['egg'] = eggs.get(em.group(1), []) if em else []
            d['file'] = os.path.basename(path)
            out[name] = d
    # voorgangers
    for name, d in out.items():
        for e in d['evos']:
            if e['target'] in out:
                out[e['target']].setdefault('pre', name)
    return out


def load_typechart():
    txt = _read('src/data/types_info.h')
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
