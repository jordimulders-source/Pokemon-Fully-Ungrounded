#!/usr/bin/env python3
"""Bouwstraat (alles met de hand in tekstbestanden):
1. ronde 23 rijen <= 39 (kop, rug, staartwortel) en de hangende staartstrook (ronde 23, x >= 51, rijen 40-46) 3 rijen omhoog:
   kop, oren, masker, staartwortel en strook pixel-identiek aan ronde 23 (zelfde x)
2. lijf.txt: borst, buik, dij, vier korte dikke poten (Poochyena als onderlaag), klauwen, staarthaak, met de hand
3. frame 2: frame2.py"""
import subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
sys.path.insert(0, H)
import tools as T
def run(*a): subprocess.run([sys.executable] + list(a), check=True)
r = T.read_txt('r23_f1.txt')
n = [[0] * 64 for _ in range(64)]
SH = 3
for y in range(SH, 40):
    n[y - SH] = r[y][:]
for y in range(40, 47):
    for x in range(51, 64): n[y - SH][x] = r[y][x]
open('_s1.txt', 'w').write(T.to_txt(n))
run('teken.py', '_s1.txt', 'lijf.txt', '_s2.txt')
# één romprij (40) weg: compactere romp; alles eronder 1 rij omhoog
g = T.read_txt('_s2.txt')
g = g[:40] + g[41:] + [[0] * 64]
open('werk_f1.txt', 'w').write(T.to_txt(g))
os.remove('_s2.txt')
run('frame2.py')
os.remove('_s1.txt')
