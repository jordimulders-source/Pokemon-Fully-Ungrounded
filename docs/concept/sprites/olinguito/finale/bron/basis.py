#!/usr/bin/env python3
"""basis.py dx dy uit.txt : ronde 23 zonder staart en zonder achterlijf (x>=37 op y31-55, vanaf y33 x>=38),
achterhoofd ingekort; de bevroren J-staart van ronde 23 apart in staart.txt op (dx,dy)."""
import sys, tools as T, staart
dx, dy, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
g = T.read_txt(T.H + '/r23_f1.txt')
P = staart.tail_pixels()
for (x, y) in P: g[y][x] = 0
for y in range(31, 56):
    for x in range(64):
        if (y <= 32 and x >= 37) or (33 <= y <= 44 and x >= 38) or (y >= 45 and x >= 36): g[y][x] = 0
for l in open(T.H + '/kop.txt'):
    l = l.split('#')[0].split()
    if not l: continue
    y, (x0, s) = int(l[0]), l[1].split(':')
    for i, c in enumerate(s): g[y][int(x0) + i] = 0 if c == '.' else int(c, 16)
open(out, 'w').write(T.to_txt(g))
t = [[0] * 64 for _ in range(64)]
for (x, y), v in P.items(): t[y + dy][x + dx] = v
open(T.H + '/staart.txt', 'w').write(T.to_txt(t))
