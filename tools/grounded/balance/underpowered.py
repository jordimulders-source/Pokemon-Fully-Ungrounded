#!/usr/bin/env python3
"""Zwakke eindvormen die je in de hoofdgame vaak tegenkomt: BST, 1-tegen-1-score tegen alle gyms/E4
(calc.rank), aantal encountertabellen van de lijn en of Jordi de soort heeft gereviseerd.

Gebruik: python3 tools/grounded/balance/underpowered.py [--top 50]"""
import os, re, sys

sys.path.insert(0, os.path.dirname(__file__))
import calc  # noqa: E402
import balancedata as bd  # noqa: E402

SP = calc.SPECIES


def revised():
    txt = open(os.path.join(bd.ROOT, 'CHANGELOG.md'), encoding='utf-8').read()
    names = set()
    for m in re.finditer(r'Revisie:\s*([^\n(]+)', txt):
        for part in re.split(r'[,&/]| en ', m.group(1)):
            names.add(calc.norm(part.replace('-lijn', '').strip()))
    for m in re.finditer(r'^#### (\w[\w\' .-]*)$', txt, re.M):
        names.add(calc.norm(m.group(1)))
    return names


def main():
    top = int(sys.argv[sys.argv.index('--top') + 1]) if '--top' in sys.argv else 50
    res = calc.rank(quiet=True)
    by_root = {r[2]: r for r in res}
    enc = {}
    for sp, st, lo, hi, m, meth, rate in bd.load_encounters():
        if sp in SP and st <= 8:
            enc.setdefault(calc.line_root(sp), set()).add(m)
    rev = revised()
    rows = []
    for root, r in by_root.items():
        tot, w1, _, fin, first, src, det, leg, ab = r
        if leg or first > 8:
            continue
        d = SP[fin]
        bst = sum(d[k] for k in ('hp', 'atk', 'def', 'spa', 'spd', 'spe'))
        n = len([x for x in det if x != '-'])
        rows.append((w1 / max(n, 1), fin, bst, w1, n, len(enc.get(root, ())), calc.norm(d['dispname']) in rev, ab, first))
    rows.sort()
    print('%-5s %-18s %-4s %-6s %-5s %-6s %-20s %s' % ('1v1/g', 'eindvorm', 'BST', '1v1', 'tabel', 'revisie', 'ability', 'fase'))
    for r in rows[:top]:
        print('%-5.2f %-18s %-4d %-6d %-5d %-6s %-20s %d' % (r[0], r[1][:18], r[2], r[3], r[5], 'ja' if r[6] else '', r[7][:20], r[8]))


if __name__ == '__main__':
    main()
