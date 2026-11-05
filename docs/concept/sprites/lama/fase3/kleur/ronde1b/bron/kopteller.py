"""Telt in de kopzone van de onderlaag (labels.txt: b=kop, v=lid, f=oog, w=lip, o=pony) hoeveel pixels als kop gekleurd zijn
(crème H/C/S, plus d als omlijningsbasis van de kop en k alleen voor oog/neus/lidlijn), per ronde.
Draaien: python3 kopteller.py"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
lab = [l[4:] for l in open(os.path.join(HERE, 'labels.txt')).read().split('\n\n')[0].splitlines()]
zone = [(x, y) for y, r in enumerate(lab) for x, c in enumerate(r) if c in 'bvfwo']
for naam, p in (('ronde 1', '../../ronde1/ronde1.txt'), ('ronde 1b', '../ronde1b.txt')):
    G = [l.rstrip('\n') for l in open(os.path.join(HERE, p))]
    crem = sum(G[y][x] in 'HCS' for x, y in zone); rand = sum(G[y][x] == 'd' for x, y in zone)
    donker = [(x, y, G[y][x]) for x, y in zone if G[y][x] not in 'HCSd']
    print(f'{naam}: kopzone {len(zone)} px | crème {crem} | omlijningsbasis d {rand} | anders {len(donker)}: ' + ' '.join(f'{c}@{x},{y}' for x, y, c in donker))
