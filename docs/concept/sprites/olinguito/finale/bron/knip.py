#!/usr/bin/env python3
"""knip.py in.txt uit.txt y:x0-x1 ... : verwijdert rij y tussen x0 en x1 (inclusief); alles in die kolommen
erboven schuift 1 omlaag (strook wegknippen, §15). Geen nieuwe pixels; naden daarna met de hand nalopen."""
import sys, tools as T
g = T.read_txt(sys.argv[1])
for a in sys.argv[3:]:
    y, r = a.split(':'); y = int(y); x0, x1 = map(int, r.split('-'))
    for x in range(x0, x1 + 1):
        for yy in range(y, 0, -1): g[yy][x] = g[yy - 1][x]
        g[0][x] = 0
open(sys.argv[2], 'w').write(T.to_txt(g))
