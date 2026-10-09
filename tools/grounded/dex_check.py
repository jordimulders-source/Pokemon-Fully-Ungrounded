#!/usr/bin/env python3
"""Project Grounded: welke soorten/vormen zijn zonder ruilen te krijgen?

Gebruik (na een geslaagde `make`, want de gegenereerde headers zijn nodig):
    python3 tools/grounded/dex_check.py            # schrijft tools/grounded/dex_beschikbaar.json + korte samenvatting
    python3 tools/grounded/dex_check.py --md       # print ook de Markdown-lijst voor DEX_ANALYSE.md
    python3 tools/grounded/dex_check.py --waarom SPECIES_X   # toon bronnen van één soort

Werkwijze: src/pokemon.c gaat door arm-none-eabi-cpp (zelfde flags als de Makefile), zodat precies de soorten/vormen
die in species_enabled.h aan staan meetellen. Daarna een vaste-puntberekening over bronnen:
  wild    alle tabellen in src/data/wild_encounters.json (gWildMonHeaders; Pyramid/Pike tellen niet)
  static  setwildbattle / seteventmon / setvar VAR_0x8004 (legendary-specials) in data/maps + data/scripts
  gift    givemon / giveegg / setvar VAR_TEMP_1 en VAR_TEMP_TRANSFERRED_SPECIES (keuzegifts), TryAddRoamer in src/roamer.c
  evo     evoluties uit species_info (items: moet ergens te krijgen zijn; EVO_TRADE telt niet = 'alleen ruilen')
  ei      fokken: de Daycare-baby van een verkrijgbare soort (niet Undiscovered; genderloos/alleen-mannelijk via Ditto;
          incense-baby's alleen als de incense te krijgen is)
  vorm    vormwissels buiten gevechten (ITEM_USE, ITEM_HOLD, DAYS_PASSED, ...) vanaf een verkrijgbare vorm
Battle-only vormen (Mega, Gmax, Primal, Ultra Burst, Tera, Totem en vormen die alleen in gevechten wisselen) tellen niet.
Items gelden als te krijgen als ze voorkomen in map.json (item balls/verborgen items), in scripts (behalve check/remove),
in winkels/C-bronnen met beloningen (zie ITEM_C_SOURCES) of als held item van een wild te vangen soort (Thief/Covet).
"""
import json, os, re, subprocess, sys, collections

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
OUT_JSON = os.path.join(REPO, 'tools/grounded/dex_beschikbaar.json')

# Bewust weggelaten (CLAUDE.md). De elemental monkeys mogen sinds 9 okt op routes (Jordi): leeg.
WEGGELATEN = set()
# Wordt nu door andere agents gebouwd (9 okt); apart rapporteren
IN_DE_MAAK = {
    'SPECIES_ARTICUNO', 'SPECIES_ZAPDOS', 'SPECIES_MOLTRES', 'SPECIES_ARTICUNO_GALAR', 'SPECIES_ZAPDOS_GALAR',
    'SPECIES_MOLTRES_GALAR', 'SPECIES_DIANCIE', 'SPECIES_MELOETTA_ARIA', 'SPECIES_ZYGARDE_50', 'SPECIES_ZYGARDE_10',
    'SPECIES_NIHILEGO', 'SPECIES_BUZZWOLE', 'SPECIES_PHEROMOSA', 'SPECIES_XURKITREE', 'SPECIES_CELESTEELA',
    'SPECIES_KARTANA', 'SPECIES_GUZZLORD', 'SPECIES_POIPOLE', 'SPECIES_NAGANADEL', 'SPECIES_STAKATAKA',
    'SPECIES_BLACEPHALON', 'SPECIES_NECROZMA', 'SPECIES_COSMOG', 'SPECIES_COSMOEM', 'SPECIES_SOLGALEO',
    'SPECIES_LUNALA', 'SPECIES_MARSHADOW',
}
ITEM_C_SOURCES = ['src/floating_market.c', 'src/fishing_tournament.c', 'src/apricorn_tree.c', 'src/new_game.c',
                  'src/data/battle_frontier/battle_frontier_exchange_corner.h', 'src/data/battle_frontier/trainer_hill.h',
                  'src/battle_casino.c', 'src/gen1_ghost.c']
INCENSE = {'SPECIES_MUNCHLAX': 'ITEM_FULL_INCENSE', 'SPECIES_HAPPINY': 'ITEM_LUCK_INCENSE', 'SPECIES_MIME_JR': 'ITEM_ODD_INCENSE',
           'SPECIES_BONSLY': 'ITEM_ROCK_INCENSE', 'SPECIES_MANTYKE': 'ITEM_WAVE_INCENSE', 'SPECIES_CHINGLING': 'ITEM_PURE_INCENSE',
           'SPECIES_BUDEW': 'ITEM_ROSE_INCENSE', 'SPECIES_AZURILL': 'ITEM_SEA_INCENSE', 'SPECIES_WYNAUT': 'ITEM_LAX_INCENSE'}
OUT_OF_BATTLE_FC = {'FORM_CHANGE_ITEM_USE', 'FORM_CHANGE_ITEM_USE_MULTICHOICE', 'FORM_CHANGE_ITEM_HOLD', 'FORM_CHANGE_DAYS_PASSED',
                    'FORM_CHANGE_DEPOSIT', 'FORM_CHANGE_WITHDRAW', 'FORM_CHANGE_TIME_OF_DAY', 'FORM_CHANGE_OVERWORLD_WEATHER',
                    'FORM_CHANGE_MOVE', 'FORM_CHANGE_END_BATTLE_ENVIRONMENT', 'FORM_CHANGE_STATUS'}
# vormen die alleen in een gevecht bestaan maar niet via een battle-vormwissel in de tabellen gevonden worden
BATTLE_ONLY_EXTRA = {'SPECIES_MIMIKYU_BUSTED', 'SPECIES_EISCUE_NOICE', 'SPECIES_ETERNATUS_ETERNAMAX', 'SPECIES_GRENINJA_ASH',
                     'SPECIES_ZYGARDE_COMPLETE', 'SPECIES_PALAFIN_HERO', 'SPECIES_CRAMORANT_GULPING', 'SPECIES_CRAMORANT_GORGING'}
BATTLE_FLAGS = ('isMegaEvolution', 'isPrimalReversion', 'isUltraBurst', 'isGigantamax', 'isTeraForm', 'isTotem')
REGIONAL = {'isAlolanForm': 'Alola', 'isGalarianForm': 'Galar', 'isHisuianForm': 'Hisui', 'isPaldeanForm': 'Paldea'}
TAGS = [('isLegendary', 'legendary'), ('isMythical', 'mythical'), ('isUltraBeast', 'UB'), ('isParadox', 'paradox')]


def read(p):
    with open(os.path.join(REPO, p), encoding='utf-8', errors='replace') as f:
        return f.read()


def defines(path, prefix):
    """{naam: waarde} voor '#define PREFIXx waarde' (aliassen en eenvoudige expressies opgelost)."""
    raw = {}
    for m in re.finditer(r'^#define\s+(%s\w+)\s+(.+?)\s*(?://.*)?$' % prefix, read(path), re.M):
        raw[m.group(1)] = m.group(2)
    val = {}

    def ev(n, depth=0):
        if n in val:
            return val[n]
        e = raw[n]
        e2 = re.sub(r'\b(%s\w+)\b' % prefix, lambda m: str(ev(m.group(1), depth + 1)) if m.group(1) in raw else m.group(1), e)
        try:
            v = int(eval(e2, {}))
        except Exception:
            v = None
        val[n] = v
        return v
    for n in raw:
        ev(n)
    return {k: v for k, v in val.items() if v is not None}


def preprocess():
    cmd = ['arm-none-eabi-cpp', '-iquote', 'include', '-Wno-trigraphs', '-DMODERN=1', '-DTESTING=0', '-DEMERALD',
           '-std=gnu17', 'src/pokemon.c']
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if r.returncode:
        sys.exit('cpp faalde (eerst make draaien?):\n' + r.stderr[:2000])
    return '\n'.join(l for l in r.stdout.split('\n') if not l.startswith('#'))


def split_entries(body):
    """'[n] = { ... },' op het hoogste niveau -> {n: tekst}."""
    out, i, depth, cur, start = {}, 0, 0, None, None
    for m in re.finditer(r'\[(\d+)\]\s*=\s*\{|\{|\}', body):
        t = m.group(0)
        if m.group(1) is not None and depth == 0:
            cur, start, depth = int(m.group(1)), m.end(), 1
        elif t == '{' or (m.group(1) is not None):
            depth += 1
        elif t == '}':
            depth -= 1
            if depth == 0 and cur is not None:
                out[cur] = body[start:m.start()]
                cur = None
    return out


def main():
    sp_val = defines('include/constants/species.h', 'SPECIES_')
    it_val = defines('include/constants/items.h', 'ITEM_')
    eg_val = defines('include/constants/pokemon.h', 'EGG_GROUP_')
    canon = {}
    for n, v in sp_val.items():  # voorkeur: de naam met een letterlijk getal (geen alias)
        if n in ('SPECIES_EGG', 'NUM_SPECIES', 'SPECIES_NONE'):
            continue
        lit = re.search(r'^#define\s+%s\s+\d+' % n, read('include/constants/species.h'), re.M) if v not in canon else None
        if v not in canon or lit:
            canon[v] = n
    item_name = {}
    for n, v in it_val.items():
        item_name.setdefault(v, n)
    egg_name = {v: n for n, v in eg_val.items()}

    pre = preprocess()
    i = pre.index('const struct SpeciesInfo gSpeciesInfo[] =')
    j = pre.index('{', i)
    # einde: eerste '};' op regelbegin na j
    k = re.compile(r'^\};', re.M).search(pre, j).start()
    entries = split_entries(pre[j + 1:k])

    # form-tabellen
    form_ids = {}
    for m in re.finditer(r'static const u16 (s\w+FormSpeciesIdTable)\[\] = \{(.*?)\};', pre, re.S):
        form_ids[m.group(1)] = [int(x) for x in re.findall(r'\b(\d+)\b', m.group(2)) if int(x) != 0xFFFF]
    form_changes = {}
    for m in re.finditer(r'static const struct FormChange (s\w+FormChangeTable)\[\]\s*=\s*\{(.*?)\};', pre, re.S):
        rows = []
        for r in re.finditer(r'\{\s*(FORM_CHANGE_\w+)\s*,\s*(\d+)\s*(?:,\s*([^,}]+))?', m.group(2)):
            rows.append((r.group(1), int(r.group(2)), (r.group(3) or '').strip()))
        form_changes[m.group(1)] = rows

    fusions = []   # (item, soort1, soort2, resultaat)
    for m in re.finditer(r'static const struct Fusion s\w+FusionTable\[\]\s*=\s*\{(.*?)\};', pre, re.S):
        for r in re.finditer(r'\{\s*\d+\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', m.group(1)):
            fusions.append(tuple(int(x) for x in r.groups()))
    mons = {}
    for num, txt in entries.items():
        if num == 0 or num not in canon:
            continue
        name = re.search(r'\.speciesName = _\("(.*?)"\)', txt)
        if not name:
            continue
        f = lambda key: re.search(r'\.%s = 1\b' % key, txt) is not None
        types = re.search(r'\.types = \{\s*TYPE_(\w+)\s*,\s*TYPE_(\w+)', txt)
        tl = [t.title() for t in types.groups()] if types else []
        if len(tl) == 2 and tl[0] == tl[1]:
            tl = tl[:1]
        gr = re.search(r'\.genderRatio = (.*?),\n', txt)
        gr = gr.group(1).strip() if gr else ''
        gender = {'0': 'male', '0x00': 'male', '254': 'female', '0xFE': 'female', '255': 'none', '0xFF': 'none'}.get(gr, 'both')
        eg = re.search(r'\.eggGroups = \{\s*(\d+)\s*,\s*(\d+)', txt)
        eggs = [int(x) for x in eg.groups()] if eg else [15, 15]
        evos = []
        em = re.search(r'\.evolutions = \(const struct Evolution\[\]\) \{(.*?)\{ 0xFFFF \}', txt, re.S)
        if em:
            for e in re.finditer(r'\{\s*(EVO_\w+)\s*,\s*([^,]+?)\s*,\s*(\d+)\s*(?:,\s*\(*const struct EvolutionParam\[\]\)\s*\{(.*?)\{CONDITIONS_END\}\s*\}\)*)?\s*\}', em.group(1), re.S):
                conds = re.findall(r'\{\s*(IF_\w+)\s*(?:,\s*([^,}]+))?(?:,\s*([^,}]+))?\s*\}', e.group(4) or '')
                evos.append((e.group(1), e.group(2), int(e.group(3)), conds))
        fst = re.search(r'\.formSpeciesIdTable = (s\w+)', txt)
        fct = re.search(r'\.formChangeTable = (s\w+)', txt)
        items = re.findall(r'\.item(?:Common|Rare) = (\d+)', txt)
        dex = re.search(r'\.natDexNum = NATIONAL_DEX_(\w+)', txt)
        mons[canon[num]] = dict(num=num, name=name.group(1), types=tl, gender=gender, eggs=eggs, evos=evos,
                                forms=form_ids.get(fst.group(1), []) if fst else [], fct=fct.group(1) if fct else None,
                                held=[int(x) for x in items], dex=dex.group(1) if dex else None,
                                battle=any(f(b) for b in BATTLE_FLAGS),
                                region=next((r for k2, r in REGIONAL.items() if f(k2)), None),
                                tags=[t for k2, t in TAGS if f(k2)])
    byname = mons
    bynum = {m['num']: n for n, m in mons.items()}

    # natDexNum -> generatie
    natdex = {}
    for m_ in re.finditer(r'^\s*NATIONAL_DEX_(\w+)\s*,', read('include/constants/pokedex.h'), re.M):
        natdex.setdefault(m_.group(1), len(natdex))

    def gen_of(d):
        for g, last in enumerate([151, 251, 386, 493, 649, 721, 809, 905, 9999], 1):
            if d <= last:
                return g

    # ---------- bronnen ----------
    src = collections.defaultdict(list)   # species -> [(soort, waar)]
    wj = json.loads(read('src/data/wild_encounters.json'))
    for grp in wj['wild_encounter_groups']:
        if grp.get('label') != 'gWildMonHeaders':
            continue
        for enc in grp['encounters']:
            mp = enc.get('base_label', enc['map'])[1:]
            for kind in ('land_mons', 'water_mons', 'fishing_mons', 'rock_smash_mons', 'hidden_mons'):
                for mon in enc.get(kind, {}).get('mons', []):
                    s = mon['species']
                    src[s].append(('wild', '%s:%s' % (mp, kind.replace('_mons', ''))))
    scr_files = []
    for root in ('data/maps', 'data/scripts'):
        for dp, _, fs in os.walk(os.path.join(REPO, root)):
            for fn in fs:
                if fn.endswith('.inc'):
                    scr_files.append(os.path.join(dp, fn))
    pat = re.compile(r'^\s*(setwildbattle|seteventmon|givemon|giveegg|setvar\s+(VAR_0x8004|VAR_TEMP_1|VAR_TEMP_TRANSFERRED_SPECIES)\s*,)\s*(SPECIES_\w+)')
    for p in scr_files:
        where = os.path.basename(os.path.dirname(p)) if '/maps/' in p else os.path.basename(p)
        for line in open(p, encoding='utf-8', errors='replace'):
            m = pat.match(line)
            if m:
                cmd = m.group(1).split()[0]
                kind = {'setwildbattle': 'static', 'seteventmon': 'static', 'givemon': 'gift', 'giveegg': 'ei-gift'}.get(cmd)
                if kind is None:
                    kind = 'script' if 'VAR_0x8004' in m.group(1) else 'gift'   # legendary-special of GiveGiftMon
                src[m.group(3)].append((kind, where))
    for m in re.finditer(r'TryAddRoamer\((SPECIES_\w+)', read('src/roamer.c')):
        src[m.group(1)].append(('static', 'roamer'))

    # ---------- items ----------
    items_ok = collections.defaultdict(list)
    for dp, _, fs in os.walk(os.path.join(REPO, 'data/maps')):
        for fn in fs:
            if fn == 'map.json':
                for it in re.findall(r'"(?:item|trainer_sight_or_berry_tree_id)": "(ITEM_\w+)"', open(os.path.join(dp, fn)).read()):
                    items_ok[it].append(os.path.basename(dp))
    bad = re.compile(r'checkitem|removeitem|checkpcitem|checkitemtype|checkitemspace|goto_if|call_if')
    for p in scr_files:
        for line in open(p, encoding='utf-8', errors='replace'):
            if bad.search(line):
                continue
            for it in re.findall(r'\b(ITEM_\w+)', line):
                items_ok[it].append(os.path.basename(os.path.dirname(p)) if '/maps/' in p else os.path.basename(p))
    for p in ITEM_C_SOURCES:
        if os.path.exists(os.path.join(REPO, p)):
            for it in set(re.findall(r'\b(ITEM_[A-Z0-9_]+)', read(p))):
                items_ok[it].append(os.path.basename(p))
    pk = read('src/battle_script_commands.c')
    pm = re.search(r'sPickupTable\w*\[\]\s*=\s*\{(.*?)\};', pk, re.S)
    if pm:
        for it in set(re.findall(r'\b(ITEM_[A-Z0-9_]+)', pm.group(1))):
            items_ok[it].append('Pickup')
    for x in ('ITEM_NONE', 'ITEM_LIST_END'):
        items_ok.pop(x, None)

    # ---------- vaste punt ----------
    src2 = collections.defaultdict(list)
    for s_, l in src.items():
        src2[canon.get(sp_val.get(s_), s_)].extend(l)
    src = src2
    have = {}   # species -> eerste bron (soort, waar)
    trade_only = {}
    for s, l in src.items():
        if s in byname:
            have[s] = l[0]

    def item_ok(n):
        return item_name.get(n, n) in items_ok if isinstance(n, int) else n in items_ok

    def cond_ok(c):
        kind, a, b = c
        if kind in ('IF_HOLD_ITEM',):
            return item_ok(int(a)) if a.isdigit() else a in items_ok
        if kind == 'IF_BAG_ITEM_COUNT':
            return item_ok(int(a)) if a.isdigit() else a in items_ok
        if kind == 'IF_REGION':
            return a.strip() == 'REGION_HOENN'
        if kind == 'IF_SPECIES_IN_PARTY':
            return bynum.get(int(a)) in have if a.isdigit() else True
        return True

    preevo = collections.defaultdict(list)
    for s, m in byname.items():
        for ev in m['evos']:
            if ev[2] in bynum:
                preevo[bynum[ev[2]]].append(s)

    def baby_of(s, seen=()):
        """Wat er uit een ei komt als s ouder is."""
        p = [x for x in preevo.get(s, []) if x not in seen]
        if not p:
            return s
        b = p[0]
        root = baby_of(b, seen + (s,))
        if root in INCENSE and not item_ok(INCENSE[root]):
            # zonder incense komt de volgende fase uit het ei
            nxt = [t for t in (bynum.get(e[2]) for e in byname[root]['evos']) if t]
            return nxt[0] if nxt else root
        return root

    changed = True
    while changed:
        changed = False
        for s, m in byname.items():
            if s not in have:
                continue
            # evoluties
            for kind, param, tgt, conds in m['evos']:
                t = bynum.get(tgt)
                if not t or t in have:
                    continue
                ok, why = True, s
                if kind == 'EVO_TRADE':
                    trade_only.setdefault(t, s)
                    continue
                if kind == 'EVO_NONE':
                    continue
                if kind == 'EVO_ITEM':
                    ok = item_ok(int(param)) if param.isdigit() else param in items_ok
                    why = '%s + %s' % (s, item_name.get(int(param), param) if param.isdigit() else param)
                if kind == 'EVO_SCRIPT_TRIGGER':
                    ok = s == 'SPECIES_KUBFU'
                if kind == 'EVO_SPLIT_FROM_EVO':
                    ok = bynum.get(int(param)) in have if param.isdigit() else True
                if ok and all(cond_ok(c) for c in conds):
                    have[t] = ('evo', why)
                    changed = True
            # vormwissels buiten gevechten
            if m['fct']:
                for kind, tgt, arg in form_changes.get(m['fct'], []):
                    t = bynum.get(tgt)
                    if not t or t in have or kind not in OUT_OF_BATTLE_FC or byname[t]['battle']:
                        continue
                    if kind in ('FORM_CHANGE_ITEM_USE', 'FORM_CHANGE_ITEM_USE_MULTICHOICE', 'FORM_CHANGE_ITEM_HOLD'):
                        if not (arg.isdigit() and (int(arg) == 0 or item_ok(int(arg)))):
                            continue
                        have[t] = ('vorm', '%s + %s' % (s, item_name.get(int(arg), arg)))
                    else:
                        have[t] = ('vorm', '%s (%s)' % (s, kind[12:].lower()))
                    changed = True
            # fusies (DNA Splicers, N-Solarizer/Lunarizer, Reins of Unity)
            for it, a, b, t in fusions:
                a, b, t = bynum.get(a), bynum.get(b), bynum.get(t)
                if a == s and t and t not in have and b in have and item_ok(it):
                    have[t] = ('fusie', '%s + %s + %s' % (a, b, item_name.get(it)))
                    changed = True
            # fokken
            if m['eggs'][0] != eg_val['EGG_GROUP_NO_EGGS_DISCOVERED'] and s != 'SPECIES_DITTO':
                if m['gender'] in ('none', 'male') and 'SPECIES_DITTO' not in have:
                    continue
                b = baby_of(s)
                if b not in have and not byname[b]['battle']:
                    have[b] = ('ei', s)
                    changed = True

    # items die een (verder bereikbare) vormwissel of evolutie blokkeren
    missing_item = collections.defaultdict(set)
    for s, m in byname.items():
        if s not in have:
            continue
        for kind, tgt, arg in (form_changes.get(m['fct'], []) if m['fct'] else []):
            t = bynum.get(tgt)
            if t and t not in have and kind in ('FORM_CHANGE_ITEM_USE', 'FORM_CHANGE_ITEM_USE_MULTICHOICE', 'FORM_CHANGE_ITEM_HOLD') \
                    and arg.isdigit() and int(arg) and not item_ok(int(arg)):
                missing_item[t].add(item_name.get(int(arg), arg))
        for kind, param, tgt, conds in m['evos']:
            t = bynum.get(tgt)
            if t and t not in have and kind == 'EVO_ITEM' and param.isdigit() and not item_ok(int(param)):
                missing_item[t].add(item_name.get(int(param), param))
    for it, a, b, t in fusions:
        t = bynum.get(t)
        if t and t not in have and not item_ok(it):
            missing_item[t].add(item_name.get(it))
    # Unown-letters: wilde Unown krijgt een letter uit de persoonlijkheid
    if 'SPECIES_UNOWN' in have:
        for s in byname:
            if s.startswith('SPECIES_UNOWN_') and s not in have:
                have[s] = ('wild', 'letter van wilde Unown')

    # ---------- entries: basissoorten + regionale vormen; overige vormen apart ----------
    def is_base(s):
        m = byname[s]
        return not m['forms'] or m['forms'][0] == m['num']

    res = []
    for s, m in sorted(byname.items(), key=lambda kv: (natdex.get(kv[1]['dex'] or '', 99999), kv[1]['num'])):
        if m['battle'] or s.endswith('_TOTEM') or s in BATTLE_ONLY_EXTRA:
            continue
        base = bynum.get(m['forms'][0]) if m['forms'] else s
        cat = 'soort' if is_base(s) else ('regionaal' if m['region'] else 'vorm')
        d = natdex.get(m['dex'], 0)
        status = 'ja' if s in have else ('weggelaten' if s in WEGGELATEN else ('in de maak' if (s in IN_DE_MAAK or base in IN_DE_MAAK) else
                 ('alleen ruilen' if s in trade_only else 'nee')))
        res.append(dict(key=s, name=m['name'] + (' (%s)' % m['region'] if m['region'] else ''), dex=d, gen=gen_of(d) if d else None,
                        cat=cat, types=m['types'], tags=m['tags'], status=status,
                        bron=list(have[s]) if s in have else None,
                        mist_item=sorted(missing_item.get(s, [])),
                        alle_bronnen=src.get(s, [])[:6]))
    # 'vorm' zonder route en zonder vormwissel binnen gevechten = cosmetisch/eventvorm; battle-only vormen weglaten
    battle_reach = set()
    for s, m in byname.items():
        for kind, tgt, arg in form_changes.get(m['fct'], []) if m['fct'] else []:
            if kind not in OUT_OF_BATTLE_FC and bynum.get(tgt) and bynum.get(tgt) != s:
                battle_reach.add(bynum[tgt])
    res = [r for r in res if not (r['cat'] != 'soort' and r['status'] != 'ja' and r['key'] in battle_reach)]
    return res, items_ok


def summary(res):
    main_ = [r for r in res if r['cat'] in ('soort', 'regionaal')]
    c = collections.Counter(r['status'] for r in main_)
    return c


def markdown(res):
    out = []
    main_ = [r for r in res if r['cat'] in ('soort', 'regionaal')]
    for st, title in (('nee', 'Niet te krijgen'), ('alleen ruilen', 'Alleen via ruilen'), ('in de maak', 'In de maak (andere agents)')):
        rows = [r for r in main_ if r['status'] == st]
        out.append('\n## %s (%d)\n' % (title, len(rows)))
        for g in range(1, 10):
            gr = [r for r in rows if r['gen'] == g]
            if gr:
                out.append('- **Gen %d:** ' % g + ', '.join('%s [%s]%s' % (r['name'], '/'.join(r['types']),
                           (' `%s`' % ','.join(r['tags'])) if r['tags'] else '') for r in gr))
    vorm = [r for r in res if r['cat'] == 'vorm' and r['status'] not in ('ja', 'in de maak')]
    mi = [r for r in vorm if r['mist_item']]
    out.append('\n## Vormen waarvan het item nergens ligt (%d)\n' % len(mi))
    for r in mi:
        out.append('- %s: %s' % (r['key'][8:].title(), ', '.join(i[5:].title() for i in r['mist_item'])))
    rest = [r for r in vorm if not r['mist_item']]
    fam = collections.OrderedDict()
    for r in rest:
        fam.setdefault(r['key'][8:].split('_')[0].title(), []).append(r['key'][8:].title())
    out.append('\n## Overige vormen zonder route (%d; cosmetisch/event/kleur, ter info)\n' % len(rest))
    out.append('; '.join('%s (%d)' % (k, len(v)) if len(v) > 3 else ', '.join(v) for k, v in fam.items()))
    return '\n'.join(out)


if __name__ == '__main__':
    res, items_ok = main()
    if '--waarom' in sys.argv:
        k = sys.argv[sys.argv.index('--waarom') + 1]
        for r in res:
            if r['key'] == k:
                print(json.dumps(r, indent=1, ensure_ascii=False))
        sys.exit()
    c = summary(res)
    meta = {'gegenereerd_door': 'tools/grounded/dex_check.py', 'telling_soorten_en_regionale_vormen': dict(c),
            'opm': 'status: ja / nee / alleen ruilen / in de maak / weggelaten; bron = eerste gevonden route'}
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        f.write('{"meta": %s,\n "species": [\n' % json.dumps(meta, ensure_ascii=False))
        f.write(',\n'.join('  ' + json.dumps(r, ensure_ascii=False) for r in res))
        f.write('\n ]\n}\n')
    print('soorten + regionale vormen:', dict(c))
    if '--md' in sys.argv:
        print(markdown(res))
