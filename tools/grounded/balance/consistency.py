#!/usr/bin/env python3
"""Vergelijkt de "Pokémon Revisie"-secties in CHANGELOG.md met de code (types, abilities, base stats,
level-up learnset in gen_9.h). Alleen rapporteren; niets aanpassen.

Gebruik: python3 tools/grounded/balance/consistency.py [--learnsets]
Latere changelog-secties (bijv. v0.4.x-fixes) kunnen een revisie overschrijven: controleer elke
melding met de hand voordat je iets aanpast."""
import os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'spire'))
import spiredata  # noqa: E402

ROOT = spiredata.ROOT
CHANGELOG_END = 8388          # vanaf hier (v0.3.0) geen revisieblokken meer

STATKEYS = {'hp': 'hp', 'atk': 'atk', 'attack': 'atk', 'def': 'def', 'defense': 'def',
            'spatk': 'spa', 'spa': 'spa', 'sp.atk': 'spa', 'spatk.': 'spa', 'sp. atk': 'spa', 'spatt': 'spa',
            'spdef': 'spd', 'spd': 'spd', 'sp.def': 'spd', 'sp. def': 'spd', 'speed': 'spe', 'spe': 'spe', 'spd.': 'spd'}


def norm(s):
    return re.sub(r'[^A-Z0-9]', '', s.upper())


def species_index(species):
    idx = {}
    for k, d in species.items():
        idx.setdefault(norm(d['dispname']), k)
        idx.setdefault(norm(k), k)
    return idx


SUBHEAD = [
    re.compile(r'^#{3,4}\s+([A-Z][\w\' .-]*?)\s*$'),                       # ### Staryu / #### Rhydon
    re.compile(r'^\*\s*\*\*(.+?)\s+Stats\b'),                               # * **Vibrava Stats (..):**
    re.compile(r'^\*\*Level-up Learnset \((.+?)\):\*\*'),                   # **Level-up Learnset (Paras):**
    re.compile(r'^static const struct LevelUpMove s(\w+?)LevelUpLearnset'),  # C-code in de changelog
    re.compile(r'^// --- (\w+) DATA ---'),                                 # // --- PARASECT DATA ---
]


def split_blocks(lines, resolve=lambda n: None):
    """Geeft (naam, startregel, regels) per revisieblok. Lijn-secties worden gesplitst op
    subkoppen die naar een (andere) soort verwijzen."""
    blocks, cur = [], None
    for i, raw in enumerate(lines[:CHANGELOG_END], 1):
        line = raw.strip()
        m3 = re.match(r'###\s*\[[^\]]*\]\s*-\s*(?:Pokémon Revisie:\s*)?(.*)', line)
        if line.startswith('### ') and m3:
            cur = [m3.group(1), i, []]
            blocks.append(cur)
            continue
        if cur is not None:
            for rx in SUBHEAD:
                m = rx.match(line)
                if m:
                    nm = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', m.group(1)) if rx is SUBHEAD[3] else m.group(1)
                    k = resolve(nm)
                    if k and k != resolve(cur[0]):
                        cur = [nm, i, []]
                        blocks.append(cur)
                    break
            cur[2].append(raw)
    return blocks


def parse_block(text):
    out = {}
    t = re.search(r'^\s*\*?\s*\**Types?:?\**:?\s*(.+)$', text, re.M)
    if t and 'wijziging' not in t.group(1).lower():
        val = re.sub(r'\(.*', '', t.group(1)).replace('*', '').strip()
        types = [x.strip().upper() for x in re.split(r'/|&|\band\b', val) if x.strip()]
        if all(re.fullmatch(r'[A-Z]+', x) for x in types) and types:
            out['types'] = types
    ab = {}
    for m in re.finditer(r'Ability\s*(?:\((Slot 1|Slot 2|Hidden)\)|(1|2|H)\b)\s*\**:?\**\s*:?\s*\**([A-Za-z\'\- ]+)', text):
        slot = m.group(1) or m.group(2)
        slot = {'Slot 1': 0, '1': 0, 'Slot 2': 1, '2': 1, 'Hidden': 2, 'H': 2}[slot]
        ab[slot] = m.group(3).strip()
    if ab:
        out['abilities'] = ab
    stats = {}
    one = re.search(r'Base Stats[^:\n]*:\**\s*(\d+\s*HP.*)', text)
    if one:
        for v, k in re.findall(r'(\d+)\s*([A-Za-z.]+)', one.group(1)):
            k = STATKEYS.get(k.lower())
            if k:
                stats[k] = int(v)
    for k, v in re.findall(r'(?:^\s*\*?|\|)\s*\**(HP|Atk|Attack|Def|Defense|SpAtk|Sp\.? ?Atk|SpDef|Sp\.? ?Def|Speed)\**:\**\s*(\d+)', text, re.M):
        k = STATKEYS.get(k.lower().replace(' ', ''))
        if k:
            stats[k] = int(v)
    cmap = {'HP': 'hp', 'Attack': 'atk', 'Defense': 'def', 'Speed': 'spe', 'SpAttack': 'spa', 'SpDefense': 'spd'}
    for k, v in re.findall(r'\.base(HP|Attack|Defense|Speed|SpAttack|SpDefense)\s*=\s*(\d+)', text):
        stats[cmap[k]] = int(v)
    if len(stats) == 6:
        out['stats'] = stats
    lu = re.findall(r'LEVEL_UP_MOVE\(\s*(\d+)\s*,\s*MOVE_(\w+)\s*\)', text)
    if lu:
        out['levelup'] = [(int(a), b) for a, b in lu]
    return out


# Moves die later (v0.8.45+) bewust aan learnsets zijn toegevoegd; geen verschil met de revisie.
LATER_MOVES = {'POLLEN_HAZE', 'TRANSMUTATION', 'CHILLY_RECEPTION', 'SHADOW_SIPHON', 'ACID_RAIN',
               'IMPLOSION', 'FUNGAL_CONTROL'}
# Bekende tikfouten in de changelog (v0.5.0/v0.5.1 en v0.6.67).
KNOWN_TYPOS = {'NATURE_MADNESS': 'NATURES_MADNESS', 'LEAR': 'LEER', 'PURE_PULSE': 'DRAGON_PULSE'}
# Later bewust gewijzigd: Galar Zigzagoon zonder Leer (v0.6.67), Parasect Spore op 1 en 22 (v0.8.45).
LATER_CHANGES = {('ZIGZAGOON_GALAR', 1, 'LEER'), ('PARASECT', 0, 'SPORE'), ('PARASECT', 1, 'SPORE'), ('PARASECT', 22, 'SPORE')}

# [0.2.0-TYPES]: type-overzicht (volgorde telt niet).
TYPES_SECTION = {
    'PSYDUCK': 'WATER PSYCHIC', 'GOLDUCK': 'WATER PSYCHIC', 'CELEBI': 'FAIRY GRASS', 'NOCTOWL': 'FLYING DARK',
    'LUGIA': 'WATER PSYCHIC', 'CASTFORM_NORMAL': 'PSYCHIC', 'CASTFORM_RAINY': 'WATER PSYCHIC',
    'CASTFORM_SUNNY': 'FIRE PSYCHIC', 'CASTFORM_SNOWY': 'ICE PSYCHIC', 'CHINGLING': 'PSYCHIC STEEL',
    'CHIMECHO': 'PSYCHIC STEEL', 'PINSIR': 'BUG GROUND', 'DUNSPARCE': 'NORMAL GROUND',
    'MASQUERAIN': 'BUG WATER', 'DODUO': 'FLYING GROUND', 'DODRIO': 'FLYING GROUND', 'PARASECT': 'GRASS GHOST',
    'KECLEON': 'GRASS', 'DEWGONG': 'ICE FAIRY', 'PORYGON': 'ELECTRIC', 'PORYGON2': 'ELECTRIC PSYCHIC',
    'PORYGON_Z': 'ELECTRIC GHOST', 'HAUNTER': 'GHOST', 'GENGAR': 'GHOST', 'SHUPPET': 'GHOST',
    'BANETTE': 'GHOST DARK', 'ABSOL': 'DARK FAIRY', 'SABLEYE': 'GHOST ROCK', 'RHYHORN': 'ROCK', 'RHYDON': 'ROCK',
    'ARON': 'STEEL', 'LAIRON': 'STEEL', 'AGGRON': 'STEEL', 'NOSEPASS': 'ROCK ELECTRIC',
    'PROBOPASS': 'ROCK ELECTRIC', 'VOLBEAT': 'ELECTRIC FIRE', 'ILLUMISE': 'BUG ELECTRIC', 'TAILLOW': 'FLYING',
    'SWELLOW': 'FLYING', 'BLASTOISE': 'WATER STEEL', 'LOUDRED': 'ELECTRIC STEEL', 'EXPLOUD': 'ELECTRIC STEEL',
    'JIRACHI': 'FAIRY STEEL', 'ARBOK': 'POISON DARK', 'HYPNO': 'PSYCHIC DARK', 'VENOMOTH': 'POISON PSYCHIC',
    'FARFETCHD': 'FLYING FIGHTING', 'LEDIAN': 'BUG NORMAL', 'POLITOED': 'WATER NORMAL',
    'SPOINK': 'PSYCHIC NORMAL', 'GRUMPIG': 'PSYCHIC NORMAL', 'SPINDA': 'FIGHTING NORMAL',
    'HUNTAIL': 'WATER DARK', 'GOREBYSS': 'WATER PSYCHIC', 'STARMIE': 'WATER ELECTRIC',
    'NUZLEAF': 'GRASS FAIRY', 'SHIFTRY': 'GRASS ICE', 'TRAPINCH': 'BUG GROUND', 'VIBRAVA': 'BUG DRAGON',
    'FLYGON': 'BUG DRAGON', 'WYNAUT': 'NORMAL', 'WOBBUFFET': 'PSYCHIC NORMAL', 'TORCHIC': 'FIRE FLYING',
}


def main():
    check_ls = '--learnsets' in sys.argv
    species = spiredata.load_species()
    idx = species_index(species)
    lines = open(os.path.join(ROOT, 'CHANGELOG.md'), encoding='utf-8').read().split('\n')
    # ability-weergavenamen -> constante
    abtxt = open(os.path.join(ROOT, 'src/data/abilities.h'), encoding='utf-8').read()
    abname = {}
    for m in re.finditer(r'\[ABILITY_(\w+)\]\s*=\s*\{\s*\.name\s*=\s*_\("([^"]*)"\)', abtxt):
        abname[norm(m.group(2))] = m.group(1)
        abname[norm(m.group(1))] = m.group(1)
    findings, order = [], []

    def resolve(name):
        nm = re.sub(r'\(.*?\)', '', name).replace('-lijn', '').strip()
        nm = re.sub(r'^(Alolan|Galar|Galarian|Hisuian)\s+(.*)', r'\2 \1', nm)
        nm = nm.replace('Alolan', 'Alola').replace('Galarian', 'Galar').replace('Hisuian', 'Hisui')
        return idx.get(norm(nm))

    for name, start, body in split_blocks(lines, resolve):
        text = '\n'.join(body)
        if 'geen wijziging' in text.lower()[:600] and 'LEVEL_UP_MOVE' not in text:
            continue
        key = resolve(name)
        if not key:
            continue
        d = species[key]
        p = parse_block(text)
        if 'types' in p:
            want = [x for i, x in enumerate(p['types']) if x not in p['types'][:i]]
            if set(want) != set(d['types']):
                findings.append((key, start, 'type', '/'.join(want), '/'.join(d['types'])))
            elif want != d['types']:
                order.append((key, start, 'type (alleen volgorde)', '/'.join(want), '/'.join(d['types'])))
        if 'stats' in p:
            for k in ('hp', 'atk', 'def', 'spa', 'spd', 'spe'):
                if p['stats'][k] != d[k]:
                    findings.append((key, start, 'stat ' + k, p['stats'][k], d[k]))
        if 'abilities' in p:
            code = d['abilities'] + ['NONE'] * (3 - len(d['abilities']))
            for slot, a in p['abilities'].items():
                c = abname.get(norm(a))
                if norm(a) in ('NONE', 'GEEN'):
                    c = 'NONE'
                if c is None:
                    findings.append((key, start, 'ability %d (onbekend)' % (slot + 1), a, code[slot]))
                    continue
                if c == 'NONE' and slot == 1 and code[1] in ('NONE', code[0]):
                    continue
                if c != code[slot]:
                    if slot < 2 and c == code[1 - slot] and p['abilities'].get(1 - slot) and \
                            abname.get(norm(p['abilities'][1 - slot])) == code[slot]:
                        order.append((key, start, 'ability 1/2 (alleen volgorde)', c, code[slot]))
                        continue
                    findings.append((key, start, 'ability %d' % (slot + 1), c, code[slot]))
        if check_ls and 'levelup' in p:
            want = set((l, KNOWN_TYPOS.get(m, m)) for l, m in p['levelup'] if (key, l, m) not in LATER_CHANGES)
            have = set((l, m) for l, m in d['levelup'] if (key, l, m) not in LATER_CHANGES)
            missing = sorted(want - have)
            extra = sorted(x for x in have - want if x[1] not in LATER_MOVES)
            if missing or extra:
                findings.append((key, start, 'learnset', 'mist in code: %s' % missing, 'extra in code: %s' % extra))
    for key, want in TYPES_SECTION.items():
        if key in species and set(want.split()) != set(species[key]['types']):
            findings.append((key, 0, 'type (0.2.0-TYPES)', want.replace(' ', '/'), '/'.join(species[key]['types'])))
    # [v.0.4.0] evolutielevels: "Naam -> lvl N"
    s0 = next(i for i, l in enumerate(lines) if l.startswith('### [v.0.4.0]'))
    s1 = next(i for i in range(s0 + 1, len(lines)) if lines[i].startswith('### ['))
    for i in range(s0, s1):
        m = re.match(r'^([A-Z][A-Za-z ]+?)\s*-?>\s*[Ll]vl\s*(\d+)\s*$', lines[i].strip())
        if not m:
            continue
        nm = m.group(1).strip()
        nm = re.sub(r'^(Alola|Galar)\s+(.*)', r'\2 \1', nm)
        key = idx.get(norm(nm)) or idx.get(norm(nm.replace('Tyanamo', 'Tynamo')))
        if not key:
            findings.append((nm, i + 1, 'evolutie (soort onbekend)', m.group(2), '?'))
            continue
        lv = [e['param'] for e in species[key]['evos'] if e['method'].startswith('LEVEL')]
        if m.group(2) not in lv:
            findings.append((key, i + 1, 'evolutielevel', m.group(2), ','.join(lv) or
                             ','.join('%s %s' % (e['method'], e['param']) for e in species[key]['evos'])))
    for f in findings:
        print('%-22s r.%-5d %-28s changelog=%s  code=%s' % f)
    print(len(findings), 'verschillen')
    if '--order' in sys.argv:
        for f in order:
            print('%-22s r.%-5d %-28s changelog=%s  code=%s' % f)
    print(len(order), 'alleen-volgorde-verschillen (--order om te tonen)')


if __name__ == '__main__':
    main()
