"""Silhouet van lijf/hals/staart/achterpoten als onderdelenkaart -> sil.txt"""
import sys
g = [['.'] * 64 for _ in range(64)]


def put(ch, rows):
    for y, spans in rows.items():
        for a, b in (spans if isinstance(spans, list) else [spans]):
            for x in range(a, b + 1):
                g[y][x] = ch


put('p', {39: (43, 46), 40: (43, 46), 41: (43, 46), 42: (44, 47), 43: (44, 47), 44: (44, 47)})
put('k', {45: (43, 48), 46: (43, 48)})
put('T', {22: (45, 47), 23: (44, 48), 24: (44, 49), 25: (44, 49), 26: (45, 48), 27: (46, 47)})
import numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from cloud import cloud
cm, _ = cloud()
for y, x in zip(*np.nonzero(cm)):
    g[y][x] = 'W'
put('P', {40: (36, 39), 41: (36, 39), 42: (36, 39), 43: (37, 40), 44: (37, 40), 45: (37, 40), 46: (37, 40)})
put('K', {47: (36, 41), 48: (36, 41)})
N = {24: (20, 28), 25: (18, 28), 26: (16, 28), 27: (13, 29), 28: (11, 30), 29: (11, 30), 30: (12, 30),
     31: (12, 29), 32: (12, 29), 33: (12, 29), 34: (13, 29), 35: (14, 28), 36: (15, 28), 37: (16, 27),
     38: (17, 27), 39: (18, 26), 40: [(19, 22), (24, 26)]}
put('N', N)
with open(sys.argv[1], 'w') as f:
    for r in g:
        f.write(''.join(r) + '\n')
