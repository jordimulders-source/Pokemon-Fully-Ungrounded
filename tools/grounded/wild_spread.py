#!/usr/bin/env python3
"""Project Grounded: hoe vaak komt elke soort voor in de wilde tabellen?

Gebruik:
    python3 tools/grounded/wild_spread.py              # rapport met uitschieters
    python3 tools/grounded/wild_spread.py --alles      # ook de volledige lijst per soort
    python3 tools/grounded/wild_spread.py --soort SPECIES_MIMIKYU   # waar komt één soort voor

Telt per soort (vorm = eigen soort, bijv. WOOPER_PALDEA):
  tabellen   aantal unieke tabellen (identieke tabellen van verdiepingen tellen één keer: Mt. Pyre 1F-4F e.d.)
  gewicht    som van de kans per ontmoeting over die tabellen (land 20/20/10/../1/1; water 60/30/5/4/1;
             vissen per hengel genormaliseerd; 1.0 = één tabel waar hij álles is)
  fasen      vroeg (mediaan lv <= 30), midden (31-55), laat (56-80), post-game (> 80)
  zeldzaam   komt alleen in slots van <= 1% voor
Alleen gWildMonHeaders (Pyramid/Pike tellen niet). Alledaagse soorten (ALLEDAAGS) mogen overal zitten.
"""
import json, os, sys, collections, statistics

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

# Soorten die logisch veel voorkomen: algemene dieren/vissen/vogels/stenen (ook hun evoluties).
ALLEDAAGS = set('SPECIES_' + s for s in '''
MAGIKARP GYARADOS ZUBAT GOLBAT CROBAT WOOBAT WINGULL PELIPPER TENTACOOL TENTACRUEL GEODUDE GRAVELER GOLEM
ROGGENROLA BOLDORE GOLDEEN SEAKING POLIWAG POLIWHIRL BARBOACH WHISCASH RATTATA RATICATE ZIGZAGOON LINOONE
PIDGEY PIDGEOTTO STARLY STARAVIA TAILLOW SWELLOW SPEAROW FEAROW PIDOVE TRANQUILL HOOTHOOT NOCTOWL FINNEON
LUMINEON PSYDUCK GOLDUCK SHELLDER STARYU CHINCHOU LANTURN CORSOLA LUVDISC REMORAID OCTILLERY HORSEA SEADRA
KRABBY KINGLER CORPHISH WOOPER QUAGSIRE MARILL AZUMARILL LOTAD LOMBRE BIDOOF BIBAREL SENTRET FURRET PATRAT
WATCHOG POOCHYENA MIGHTYENA CATERPIE METAPOD WEEDLE KAKUNA WURMPLE SILCOON CASCOON ODDISH GLOOM BELLSPROUT
WEEPINBELL SEEDOT NUZLEAF SHROOMISH DIGLETT DUGTRIO SANDSHREW NOSEPASS ARON LAIRON MACHOP WHISMUR
MAKUHITA MEDITITE NUMEL SLUGMA SPINARAK ARIADOS VENONAT PARAS GRIMER TRUBBISH KOFFING MAGNEMITE VOLTORB
SKWOVET GREEDENT ROOKIDEE CORVISQUIRE ARROKUDA BARRASKEWDA WISHIWASHI ALOMOMOLA MAREANIE WIGLETT
SWINUB PILOSWINE SNOVER SNORUNT SPHEAL SEEL VANILLITE BUNNELBY LILLIPUP HERDIER MEOWTH YUNGOOS GUMSHOOS
PIKIPEK TRUMBEAK FLETCHLING SURSKIT MASQUERAIN BASCULIN BASCULIN_RED_STRIPED BASCULIN_BLUE_STRIPED BASCULIN_WHITE_STRIPED
FRILLISH JELLICENT CLAMPERL WAILMER WAILORD SHARPEDO CARVANHA MANTYKE MANTINE SKRELP CROBAT
'''.split())

PHASES = ('vroeg', 'midden', 'laat', 'post')


def phase(lv):
    return 'vroeg' if lv <= 30 else 'midden' if lv <= 55 else 'laat' if lv <= 80 else 'post'


def load():
    d = json.load(open(os.path.join(REPO, 'src/data/wild_encounters.json')))
    g = next(x for x in d['wild_encounter_groups'] if x['label'] == 'gWildMonHeaders')
    fields = {f['type']: f for f in g['fields']}
    tabs = []
    seen = set()
    for e in g['encounters']:
        for k in ('land_mons', 'water_mons', 'rock_smash_mons', 'fishing_mons'):
            if k not in e:
                continue
            mons = e[k]['mons']
            key = (k, tuple((m['species'], m['min_level'], m['max_level']) for m in mons))
            if key in seen:
                continue
            seen.add(key)
            rates = fields[k]['encounter_rates']
            probs = [0.0] * len(mons)
            if k == 'fishing_mons':
                for rod, idx in fields[k]['groups'].items():
                    tot = sum(rates[i] for i in idx)
                    for i in idx:
                        if i < len(mons):
                            probs[i] = rates[i] / tot
            else:
                tot = sum(rates)
                for i in range(min(len(mons), len(rates))):
                    probs[i] = rates[i] / tot
            lv = statistics.median(m['max_level'] for m in mons)
            tabs.append(dict(label=e['base_label'], kind=k[:-5], mons=mons, probs=probs, phase=phase(lv)))
    return tabs


def stats(tabs):
    S = collections.defaultdict(lambda: dict(tabs=[], w=0.0, maxp=0.0, phases=collections.Counter()))
    for t in tabs:
        per = collections.defaultdict(float)
        for m, p in zip(t['mons'], t['probs']):
            per[m['species']] += p
        for sp, p in per.items():
            s = S[sp]
            s['tabs'].append('%s:%s' % (t['label'][1:], t['kind']))
            s['w'] += p
            s['maxp'] = max(s['maxp'], p)
            s['phases'][t['phase']] += 1
    return S


def families():
    """soort -> basis van de evolutielijn (uit species_info: .evolutions = EVOLUTION(... SPECIES_X ...))."""
    import glob, re
    parent = {}
    for f in glob.glob(os.path.join(REPO, 'src/data/pokemon/species_info/*.h')):
        t = open(f, encoding='utf-8').read()
        heads = list(re.finditer(r'^\s*\[(SPECIES_\w+)\]\s*=', t, re.M))
        for i, h in enumerate(heads):
            body = t[h.end():heads[i + 1].start() if i + 1 < len(heads) else len(t)]
            m = re.search(r'\.evolutions\s*=\s*EVOLUTION\((.*?)\),\s*\n', body, re.S)
            if m:
                # alleen het doel van elke evolutie, niet voorwaarden als IF_SPECIES_IN_PARTY (Mantyke/Remoraid)
                for tgt in re.findall(r'\{\s*EVO_\w+\s*,[^,{}]*,\s*(SPECIES_\w+)', m.group(1)):
                    parent.setdefault(tgt, h.group(1))

    def root(sp, depth=0):
        return root(parent[sp], depth + 1) if sp in parent and depth < 4 else sp
    return root


def fmt(sp, s):
    ph = ' '.join('%s%d' % (p[0], s['phases'][p]) for p in PHASES if s['phases'][p])
    return '%-28s %3d tab  gewicht %5.2f  max %4.0f%%  [%s]' % (sp[8:], len(s['tabs']), s['w'], 100 * s['maxp'], ph)


def main():
    tabs = load()
    S = stats(tabs)
    if '--soort' in sys.argv:
        sp = sys.argv[sys.argv.index('--soort') + 1]
        if not sp.startswith('SPECIES_'):
            sp = 'SPECIES_' + sp.upper()
        s = S.get(sp)
        print(fmt(sp, s) if s else '%s komt in geen enkele tabel voor' % sp)
        for t in (s['tabs'] if s else []):
            print('   ', t)
        return
    print('Unieke tabellen: %d, soorten/vormen: %d\n' % (len(tabs), len(S)))
    print('== Te vaak (niet-alledaags, >= 7 unieke tabellen of gewicht >= 1.5) ==')
    for sp, s in sorted(S.items(), key=lambda x: (-len(x[1]['tabs']), -x[1]['w'])):
        if sp not in ALLEDAAGS and (len(s['tabs']) >= 7 or s['w'] >= 1.5):
            print('  ' + fmt(sp, s))
    print('\n== Te weinig: alledaagse soort in <= 1 tabel of alleen als <= 1%-slot ==')
    for sp in sorted(ALLEDAAGS):
        s = S.get(sp)
        if not s:
            continue  # niet in de tabellen (bijv. vorm die niet bestaat of bewust elders)
        if len(s['tabs']) <= 1 or s['maxp'] <= 0.0101:
            print('  ' + fmt(sp, s))
    root = families()
    fam = collections.defaultdict(lambda: dict(tabs=set(), w=0.0, leden=set()))
    for sp, s in S.items():
        f = fam[root(sp)]
        f['tabs'].update(s['tabs'])
        f['w'] += s['w']
        f['leden'].add(sp[8:])
    print('\n== Alledaagse evolutielijnen (hele lijn samen) in <= 4 tabellen ==')
    for r in sorted(set(root(sp) for sp in ALLEDAAGS)):
        f = fam.get(r)
        if f and len(f['tabs']) <= 4:
            print('  %-14s %2d tab  gewicht %5.2f  (%s)' % (r[8:], len(f['tabs']), f['w'], ', '.join(sorted(f['leden']))))
    print('\n== Evolutielijnen in de meeste tabellen (top 15) ==')
    for r, f in sorted(fam.items(), key=lambda x: -len(x[1]['tabs']))[:15]:
        print('  %-14s %2d tab  gewicht %5.2f  (%s)' % (r[8:], len(f['tabs']), f['w'], ', '.join(sorted(f['leden']))))
    print('\n== Alledaagse soorten die helemaal niet wild voorkomen ==')
    print('  ' + ', '.join(sorted(sp[8:] for sp in ALLEDAAGS if sp not in S)))
    print('\n== Alleen op één plek als <= 1%-slot (info) ==')
    one = [sp for sp, s in S.items() if len(s['tabs']) == 1 and s['maxp'] <= 0.0101]
    print('  ' + ', '.join(sorted(sp[8:] for sp in one)))
    if '--alles' in sys.argv:
        print('\n== Alle soorten ==')
        for sp, s in sorted(S.items(), key=lambda x: (-len(x[1]['tabs']), -x[1]['w'])):
            print('  ' + fmt(sp, s))


if __name__ == '__main__':
    main()
