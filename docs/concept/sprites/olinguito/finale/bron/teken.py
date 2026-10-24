#!/usr/bin/env python3
"""teken.py basis.txt tekening.txt uit.txt
Met de hand getekende rijen met absolute x: 'y  x:pixels  x:pixels ...' ('.' = transparant).
Secties '[naam]' worden in volgorde gelegd; '[staart]' legt staart.txt (bevroren J-staart) op dat moment."""
import sys, tools as T
g = T.read_txt(sys.argv[1])
for l in open(sys.argv[2]):
    l = l.split('#')[0].strip()
    if not l: continue
    if l == '[staart]':
        t = T.read_txt(T.H + '/staart.txt')
        for y in range(64):
            for x in range(64):
                if t[y][x]: g[y][x] = t[y][x]
        continue
    if l.startswith('['): continue
    parts = l.split(); y = int(parts[0])
    for p in parts[1:]:
        x0, s = p.split(':'); x0 = int(x0)
        for i, c in enumerate(s):
            assert 0 <= x0 + i < 64
            g[y][x0 + i] = 0 if c == '.' else int(c, 16)
open(sys.argv[3], 'w').write(T.to_txt(g))
