#!/usr/bin/env python3
"""Project Grounded: welke items zijn in deze rom te krijgen, en welke nuttige items nog niet?

Gebruik:
    python3 tools/grounded/item_check.py            # samenvatting: nuttige items die nergens te krijgen zijn, per categorie
    python3 tools/grounded/item_check.py --alles    # ook de rommel (mail, kostuum, ongebruikte key items, ...)
    python3 tools/grounded/item_check.py --waar ITEM_X [ITEM_Y ...]   # bronnen van een item
    python3 tools/grounded/item_check.py --strikt   # exit 1 als er nuttige items ontbreken

Bronnen (een item geldt als te krijgen als het ergens voorkomt als):
  kaart     item ball / verborgen item in data/maps/*/map.json, of een bessenboom (BERRY_TREE_..._<BES>)
  script    regels in data/maps/**/*.inc en data/scripts/*.inc (giveitem, finditem, additem, addpcitem, winkels
            (.2byte in een pokemart-lijst), setvar VAR_0x8009 (BP-balies), gift-held items ...); check/remove/buffer
            en debug.inc tellen niet
  C         beloningslijsten in C (C_SOURCES: drijvende markt, visserstoernooi, Frontier-prijzen, Trainer Hill,
            BP-winkels, Battle Casino, loterij, minigames, Pickup-tabel, ...)
  wild      held item (itemCommon/itemRare) van een soort die wild voorkomt (Thief/Covet/Frisk)
Nuttig = alles behalve: TM's/HM's (eigen systeem), Mega Stones, Z-kristallen, Tera Shards, Dynamax-items en hun
key items (CLAUDE.md "Besloten": geen Mega/Z/Dynamax/Tera voor de speler), Ability Patch (verborgen abilities zijn
niet verkrijgbaar), mail, ongebruikte key items, verkoopwaar zonder functie, kostuum-/contestitems, apricorns,
fossielen van soorten die niet in de game zitten e.d. (zie RUIS).
"""
import collections, json, os, re, sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

C_SOURCES = [
    'src/floating_market.c', 'src/fishing_tournament.c', 'src/apricorn_tree.c', 'src/new_game.c', 'src/gen1_ghost.c',
    'src/battle_casino.c', 'src/bp_shop.c', 'src/lottery_corner.c', 'src/pokemon_jump.c', 'src/dodrio_berry_picking.c',
    'src/data/battle_frontier/battle_frontier_exchange_corner.h', 'src/data/battle_frontier/trainer_hill.h',
]
# alleen bepaalde arrays uit een bestand (de rest is logica)
C_ARRAYS = {
    'src/battle_arena.c': ['sShortStreakPrizeItems', 'sLongStreakPrizeItems'],
    'src/battle_palace.c': ['sBattlePalaceEarlyPrizes', 'sBattlePalaceLatePrizes'],
    'src/battle_pyramid.c': ['sShortStreakRewardItems', 'sLongStreakRewardItems'],
    'src/battle_tent.c': ['sVerdanturfTentRewards', 'sFallarborTentRewards', 'sSlateportTentRewards'],
    'src/trainer_hill.c': [r'sPrizeList\w+'],
    'src/player_pc.c': ['sNewGamePCItems'],
    'src/battle_script_commands.c': ['sPickupTable'],
    'src/data/lilycove_lady.h': [r'sFavorLadyPrizes\w*', r'sQuizLadyPrizes\w*'],
}
SCRIPT_SKIP = re.compile(r'\b(checkitem|removeitem|checkpcitem|checkitemspace|checkitemtype|bufferitemname\w*|'
                         r'goto_if\w*|call_if\w*|compare\w*|bufferitemnameplural|checkbagitem|specialvar)\b')

# Bewust niet voor de speler / geen functie in deze rom
RUIS_SORT = {'ITEM_TYPE_MEGA_STONE', 'ITEM_TYPE_Z_CRYSTAL', 'ITEM_TYPE_TERA_SHARD', 'ITEM_TYPE_MAIL',
             'ITEM_TYPE_CONTEST_HELD_ITEM', 'ITEM_TYPE_SELLABLE', 'ITEM_TYPE_RELIC', 'ITEM_TYPE_SHARD', 'ITEM_TYPE_GROWTH'}
RUIS = {
    'ITEM_ABILITY_PATCH',                         # verborgen abilities niet verkrijgbaar
    'ITEM_DYNAMAX_CANDY', 'ITEM_MAX_MUSHROOMS', 'ITEM_MAX_HONEY', 'ITEM_WISHING_PIECE', 'ITEM_DYNAMAX_BAND',
    'ITEM_MEGA_RING', 'ITEM_Z_POWER_RING', 'ITEM_TERA_ORB', 'ITEM_ZYGARDE_CUBE', 'ITEM_GALAR_CURRY',
    'ITEM_STRANGE_SOUVENIR', 'ITEM_CHERISH_BALL', 'ITEM_PARK_BALL', 'ITEM_STRANGE_BALL', 'ITEM_SAFARI_BALL',
    'ITEM_TEA', 'ITEM_SOOT_SACK', 'ITEM_POKE_FLUTE', 'ITEM_PRISON_BOTTLE',
    'ITEM_RED_ORB', 'ITEM_BLUE_ORB',              # Primal Reversion: net als Mega alleen voor Spire-bazen/trainers
}
# fossielen die een wetenschapper tot leven wekt (Devon Corp, vanilla); de rest heeft geen functie
FOSSIL_REVIVAL = {'ITEM_ROOT_FOSSIL', 'ITEM_CLAW_FOSSIL'}
RUIS_PREFIX = ('ITEM_TM', 'ITEM_HM', 'ITEM_TR', 'ITEM_APRICORN', 'ITEM_RED_APRICORN', 'ITEM_BLUE_APRICORN',
               'ITEM_YELLOW_APRICORN', 'ITEM_GREEN_APRICORN', 'ITEM_PINK_APRICORN', 'ITEM_WHITE_APRICORN',
               'ITEM_BLACK_APRICORN')
# categorieën voor het rapport (op sortType)
CAT = {
    'ITEM_TYPE_HELD_ITEM': 'held item (gevecht)', 'ITEM_TYPE_TYPE_BOOST_HELD_ITEM': 'held item (typeversterker)',
    'ITEM_TYPE_EV_BOOST_HELD_ITEM': 'Power-items', 'ITEM_TYPE_GEM': 'gems', 'ITEM_TYPE_PLATE': 'plates',
    'ITEM_TYPE_MEMORY': 'memories', 'ITEM_TYPE_DRIVE': 'drives', 'ITEM_TYPE_INCENSE': 'incense', 'ITEM_TYPE_NECTAR': 'nectars',
    'ITEM_TYPE_EVOLUTION_STONE': 'evolutie', 'ITEM_TYPE_EVOLUTION_ITEM': 'evolutie',
    'ITEM_TYPE_SPECIAL_HELD_ITEM': 'held item (soortgebonden)', 'ITEM_TYPE_NATURE_MINT': 'mints',
    'ITEM_TYPE_STAT_BOOST_DRINK': 'vitamines', 'ITEM_TYPE_STAT_BOOST_FEATHER': 'vitamines (feathers)',
    'ITEM_TYPE_STAT_BOOST_MOCHI': 'vitamines (mochi)', 'ITEM_TYPE_LEVEL_UP_ITEM': 'levelen/training',
    'ITEM_TYPE_HEALTH_RECOVERY': 'medicijn', 'ITEM_TYPE_STATUS_RECOVERY': 'medicijn', 'ITEM_TYPE_PP_RECOVERY': 'medicijn',
    'ITEM_TYPE_BATTLE_ITEM': 'gevechtsitem (X)', 'ITEM_TYPE_X_ITEM': 'gevechtsitem (X)', 'ITEM_TYPE_FLUTE': 'fluiten',
    'ITEM_TYPE_AUX_ITEM': 'gevechtsitem (aux)', 'ITEM_TYPE_FIELD_USE': 'veld', 'ITEM_TYPE_FOSSIL': 'fossielen',
    'ITEM_TYPE_UNCATEGORIZED': 'overig',
}


def read(p):
    with open(os.path.join(REPO, p), encoding='utf-8', errors='replace') as f:
        return f.read()


def item_defines():
    """naam -> nummer (aliassen opgelost), nummer -> canonieke naam."""
    txt = read('include/constants/items.h')
    raw = dict(re.findall(r'^#define\s+(ITEMS?_\w+)\s+(\w+)', txt, re.M))
    literal = set(re.findall(r'^#define\s+(ITEM_\w+)\s+\d+', txt, re.M))
    val = {}
    for n in raw:
        v, seen = raw[n], set()
        while not v.isdigit() and v in raw and v not in seen:
            seen.add(v)
            v = raw[v]
        if v.isdigit():
            val[n] = int(v)
    count = val['ITEMS_COUNT']
    canon = {}
    for n, v in val.items():
        if n.startswith('ITEM_') and 0 < v < count and v not in canon and n in literal:
            canon[v] = n
    return val, canon


def items_info():
    """canonieke naam -> dict(sort, hold, pocket, name, use, importance) uit src/data/items.h."""
    s = read('src/data/items.h')
    info = {}
    for m in re.finditer(r'^\s{4}\[(ITEM_\w+)\]\s*=\s*\n\s{4}\{(.*?)\n\s{4}\},', s, re.S | re.M):
        b = m.group(2)
        g = lambda k: (re.search(r'\.%s\s*=\s*([^,\n]+)' % k, b) or [None, ''])[1].strip()
        nm = re.search(r'\.name\s*=\s*ITEM_NAME\("(.*?)"\)', b)
        info[m.group(1)] = dict(sort=g('sortType'), hold=g('holdEffect'), pocket=g('pocket'), use=g('fieldUseFunc'),
                                battle=g('battleUsage'),
                                importance=g('importance'), name=nm.group(1) if nm else m.group(1))
    return info


def sources(val, canon):
    src = collections.defaultdict(set)

    def add(name, where):
        v = val.get(name)
        if v is not None and v in canon:
            src[canon[v]].add(where)

    # kaarten
    for dp, _, fs in os.walk(os.path.join(REPO, 'data/maps')):
        if 'map.json' not in fs:
            continue
        mp = os.path.basename(dp)
        d = json.load(open(os.path.join(dp, 'map.json')))
        for o in d.get('object_events') or []:
            t = str(o.get('trainer_sight_or_berry_tree_id', ''))
            if t.startswith('ITEM_'):
                add(t, 'kaart: ' + mp)
            elif t.startswith('BERRY_TREE_'):
                add('ITEM_%s_BERRY' % t.split('_')[-1], 'bessenboom: ' + mp)
        for b in d.get('bg_events') or []:
            if b.get('type') == 'hidden_item':
                add(str(b.get('item')), 'verborgen: ' + mp)
    # scripts
    files = []
    for root in ('data/maps', 'data/scripts'):
        for dp, _, fs in os.walk(os.path.join(REPO, root)):
            files += [os.path.join(dp, f) for f in fs if f.endswith('.inc') and f != 'debug.inc']
    for p in files:
        where = os.path.basename(os.path.dirname(p)) if '/maps/' in p else os.path.basename(p)
        for line in open(p, encoding='utf-8', errors='replace'):
            line = line.split('@')[0]
            if 'ITEM_' not in line or SCRIPT_SKIP.search(line):
                continue
            for it in re.findall(r'\b(ITEM_\w+)', line):
                add(it, 'script: ' + where)
    # C
    for p in C_SOURCES:
        if os.path.exists(os.path.join(REPO, p)):
            code = re.sub(r'/\*.*?\*/|//[^\n]*', '', read(p), flags=re.S)
            for it in set(re.findall(r'\b(ITEM_[A-Z0-9_]+)', code)):
                add(it, 'C: ' + os.path.basename(p))
    for p, arrays in C_ARRAYS.items():
        if not os.path.exists(os.path.join(REPO, p)):
            continue
        code = re.sub(r'/\*.*?\*/|//[^\n]*', '', read(p), flags=re.S)
        for a in arrays:
            for m in re.finditer(r'\b%s\b(?:\[[^\]]*\])+\s*=\s*\{(.*?)\};' % a, code, re.S):
                for it in set(re.findall(r'\b(ITEM_[A-Z0-9_]+)', m.group(1))):
                    add(it, 'C: %s' % os.path.basename(p))
    # wilde held items
    wild = set()
    wj = json.loads(read('src/data/wild_encounters.json'))
    for grp in wj['wild_encounter_groups']:
        if grp.get('label') != 'gWildMonHeaders':
            continue
        for enc in grp['encounters']:
            for k, v in enc.items():
                if isinstance(v, dict) and 'mons' in v:
                    wild.update(m['species'] for m in v['mons'])
    for f in sorted(os.listdir(os.path.join(REPO, 'src/data/pokemon/species_info'))):
        s = read('src/data/pokemon/species_info/' + f)
        for m in re.finditer(r'\[(SPECIES_\w+)\]\s*=\s*\{(.*?)\n    \},', s, re.S):
            if m.group(1) in wild:
                for it in re.findall(r'\.item(?:Common|Rare)\s*=\s*(ITEM_\w+)', m.group(2)):
                    add(it, 'wild: ' + m.group(1))
    return src


def evo_and_form_items():
    evo, form = set(), set()
    for f in os.listdir(os.path.join(REPO, 'src/data/pokemon/species_info')):
        s = read('src/data/pokemon/species_info/' + f)
        for m in re.finditer(r'\.evolutions = EVOLUTION\((.*?)\),\n', s, re.S):
            evo.update(re.findall(r'\b(ITEM_\w+)', m.group(1)))
    for m in re.finditer(r'\{(FORM_CHANGE_\w+)[^}]*?\b(ITEM_\w+)', read('src/data/pokemon/form_change_tables.h')):
        if m.group(1) not in ('FORM_CHANGE_BATTLE_MEGA_EVOLUTION_ITEM', 'FORM_CHANGE_BATTLE_ULTRA_BURST',
                              'FORM_CHANGE_BATTLE_GIGANTAMAX', 'FORM_CHANGE_BATTLE_TERASTALLIZATION',
                              'FORM_CHANGE_BATTLE_PRIMAL_REVERSION'):
            form.add(m.group(2))
    return evo, form


def classify(name, inf, evo, form):
    """(nuttig?, categorie)"""
    if name in RUIS or name.startswith(RUIS_PREFIX):
        return False, 'ruis'
    sort = inf.get('sort', '')
    if sort in RUIS_SORT:
        return False, 'ruis'
    if name in form:
        return True, 'vormwissel'
    if name in evo:
        return True, 'evolutie'
    if inf.get('pocket') == 'POCKET_KEY_ITEMS':
        return False, 'key item'
    if sort == 'ITEM_TYPE_FOSSIL' and name not in FOSSIL_REVIVAL:
        return False, 'fossiel zonder revival (de soort is wild te vangen)'
    if sort in ('ITEM_TYPE_EVOLUTION_ITEM', 'ITEM_TYPE_EVOLUTION_STONE'):
        return False, 'evolutie-item zonder evolutie in deze rom'
    if inf.get('pocket') == 'POCKET_POKE_BALLS':
        return True, 'ballen'
    if inf.get('pocket') == 'POCKET_BERRIES':
        return True, 'bessen'
    if sort == 'ITEM_TYPE_FIELD_USE' and 'Mulch' in inf.get('name', ''):
        return False, 'ruis'
    if inf.get('use') in ('ItemUseOutOfBattle_CannotUse', '', 'NULL') and inf.get('hold') in ('', 'HOLD_EFFECT_NONE') \
            and inf.get('battle') in ('', '0'):
        return False, 'geen functie (Legends-items zonder effect e.d.)'
    return True, CAT.get(sort, 'overig')


def main():
    val, canon = item_defines()
    info = items_info()
    src = sources(val, canon)
    evo, form = evo_and_form_items()
    if '--waar' in sys.argv:
        for n in sys.argv[sys.argv.index('--waar') + 1:]:
            c = canon.get(val.get(n), n)
            print(c, '->', '; '.join(sorted(src.get(c, ()))) or 'NERGENS')
        return 0
    alles = '--alles' in sys.argv
    missing = collections.defaultdict(list)
    nok = ntot = 0
    for v in sorted(canon):
        n = canon[v]
        inf = info.get(n)
        if inf is None or inf['name'] in ('??????', '?????'):
            continue
        useful, cat = classify(n, inf, evo, form)
        if not useful and not alles:
            continue
        ntot += 1
        if src.get(n):
            nok += 1
            continue
        missing[cat if useful else 'ruis: ' + cat].append('%s (%s)' % (n, inf['name']))
    nmis = sum(len(l) for k, l in missing.items() if not k.startswith('ruis'))
    print('Nuttige items: %d, te krijgen: %d, ontbreekt: %d' % (ntot, nok, nmis))
    for cat in sorted(missing):
        print('\n[%s] %d' % (cat, len(missing[cat])))
        for x in missing[cat]:
            print('  ' + x)
    return 1 if ('--strikt' in sys.argv and nmis) else 0


if __name__ == '__main__':
    sys.exit(main())
