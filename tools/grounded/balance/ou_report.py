#!/usr/bin/env python3
"""Vat de uitkomst van `ou_analysis.py rank` samen (stijgers, dalers, top, OU-referenties).

  python3 tools/grounded/balance/ou_report.py <rank.json> [<vanillamap>]"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ousim as S  # noqa: E402
from ou_refs import OU_REFS, UBERS  # noqa: E402


def best(o, player=False):
    if not o or 'error' in o:
        return None, None
    items = [(v['score'], ab, v) for ab, v in o.items() if not (player and v['hidden'])]
    if not items:
        return None, None
    sc, ab, v = max(items, key=lambda x: x[0])
    return sc, (ab, v)


def summarize(rank_path, vanilla=None):
    r = json.load(open(rank_path))
    cur = S.Data()
    van = S.Data(vanilla, os.path.join(S.ROOT, 'tools/learnset_helpers/build/all_learnables.json'), 'van') if vanilla else None
    refsp = set(cur.sp(l.split('@')[0].strip()) for l in OU_REFS.strip().split('\n\n') for l in [l.split('\n')[0]] if l)
    rows = []
    for sp, v in r.items():
        cv, cinfo = best(v.get('cur'))
        cp, pinfo = best(v.get('cur'), player=True)
        vv, vinfo = best(v.get('van'))
        if cv is None:
            continue
        d = cur.species.get(sp)
        chg = []
        if van and sp in van.species:
            dv = van.species[sp]
            bst = sum(d[s] for s in S.STATS) - sum(dv[s] for s in S.STATS)
            if bst:
                chg.append('BST %+d' % bst)
            if d['types'] != dv['types']:
                chg.append('/'.join(dv['types']) + '→' + '/'.join(d['types']))
            if d['abilities'] != dv['abilities']:
                chg.append('ab ' + '/'.join(a.title() for a in d['abilities']))
        rows.append(dict(sp=sp, name=d['dispname'], cur=cv, player=cp, van=vv, delta=(cp - vv) if (vv is not None and cp is not None) else None,
                         delta_all=(cv - vv) if vv is not None else None, cset=cinfo, pset=pinfo, vset=vinfo,
                         uber=sp in UBERS, ref=sp in refsp, chg=', '.join(chg)))
    return rows


def fmt(x):
    return '  -  ' if x is None else '%4.0f%%' % (100 * x)


def main():
    rows = summarize(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    nonuber = [x for x in rows if not x['uber']]
    print('== top 40 (speler-legaal, deze rom, zonder Ubers)')
    for x in sorted(nonuber, key=lambda x: -(x['player'] or 0))[:40]:
        ab, v = x['pset']
        print('%-22s %s (vanilla %s, Δ %s) %-16s %-9s %s | %s' % (x['name'], fmt(x['player']), fmt(x['van']), fmt(x['delta']), ab, v['kind'], v['item'],
                                                            ', '.join(v['moves']), ) + ('  [' + x['chg'] + ']' if x['chg'] else ''))
    print('\n== grootste stijgers (Δ speler-legaal vs vanilla)')
    for x in sorted([x for x in rows if x['delta'] is not None], key=lambda x: -x['delta'])[:40]:
        ab, v = x['pset']
        print('%-22s %s → %s (Δ %s)%s %-16s %s | %s  [%s]' % (x['name'], fmt(x['van']), fmt(x['player']), fmt(x['delta']), ' UBER' if x['uber'] else '',
                                                        ab, v['item'], ', '.join(v['moves']), x['chg']))
    print('\n== grootste dalers')
    for x in sorted([x for x in rows if x['delta'] is not None], key=lambda x: x['delta'])[:30]:
        ab, v = x['pset']
        vab, vv = x['vset']
        print('%-22s %s → %s (Δ %s) %s | %s  || vanilla %s %s | %s [%s]' % (x['name'], fmt(x['van']), fmt(x['player']), fmt(x['delta']), ab,
                                                                ', '.join(v['moves']), vab, vv['item'], ', '.join(vv['moves']), x['chg']))
    print('\n== OU-referenties')
    for x in sorted([x for x in rows if x['ref']], key=lambda x: (x['delta'] or 0)):
        print('%-22s vanilla %s → rom %s (Δ %s)' % (x['name'], fmt(x['van']), fmt(x['player']), fmt(x['delta'])))
    print('\n== gewijzigde soorten die laag blijven (speler-legaal < 40%)')
    for x in sorted([x for x in rows if x['chg'] and (x['player'] or 0) < 0.40 and x['delta'] is not None], key=lambda x: x['player'] or 0):
        print('%-22s %s (vanilla %s, Δ %s) [%s]' % (x['name'], fmt(x['player']), fmt(x['van']), fmt(x['delta']), x['chg']))
    print('\n== verborgen ability nodig (cur_all ≫ speler)')
    for x in sorted([x for x in rows if x['player'] is not None and x['cur'] - x['player'] > 0.04], key=lambda x: x['player'] - x['cur']):
        print('%-22s alle %s, speler %s, beste ability %s' % (x['name'], fmt(x['cur']), fmt(x['player']), x['cset'][0]))


if __name__ == '__main__':
    main()
