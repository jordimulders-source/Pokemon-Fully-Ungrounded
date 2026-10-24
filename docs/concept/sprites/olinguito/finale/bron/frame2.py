#!/usr/bin/env python3
"""Frame 2 (ademhaling): alles boven rij NAAD schuift 1 px omhoog, rij NAAD wordt verdubbeld; poten en voeten
blijven staan. De staart (x >= STAARTX) beweegt als geheel 1 px mee omhoog (vorm blijft gelijk).
Daarna de handcorrecties uit frame2.txt."""
import tools as T, subprocess, sys, os
NAAD = 42
STAARTX = 47
g = T.read_txt(T.H + '/werk_f1.txt')
out = [r[:] for r in g]
for y in range(63):
    for x in range(64):
        if y < NAAD or x >= STAARTX: out[y][x] = g[y + 1][x]
open(T.H + '/_f2.txt', 'w').write(T.to_txt(out))
subprocess.run([sys.executable, T.H + '/teken.py', T.H + '/_f2.txt', T.H + '/frame2.txt', T.H + '/werk_f2.txt'], check=True)
os.remove(T.H + '/_f2.txt')
