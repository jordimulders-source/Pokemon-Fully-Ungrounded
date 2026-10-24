#!/usr/bin/env python3
"""Bouwstraat (alles met de hand in tekstbestanden):
1. ronde 23 + kop.txt (achterkant schedel naar binnen; rest van de kop pixel-identiek), in ronde-23-coördinaten
2. alles 2 rijen omhoog (poten worden 2 rijen langer); de onderhelft (rij >= 40) en de staart worden opnieuw gelegd
3. staart.txt = de J-staart van ronde 23 (wortel en bovenste strook, rijen 34-41) 2 px naar rechts, exact dezelfde pixels
4. onder.txt: rug/staartwortel, poten, klauwen, hangende staartstrook + haak, met de hand
5. frame 2: frame2.py"""
import subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
sys.path.insert(0, H)
import tools as T
def run(*a): subprocess.run([sys.executable] + list(a), check=True)
run('teken.py', 'r23_f1.txt', 'kop.txt', '_s1.txt')
g = T.read_txt('_s1.txt'); r = T.read_txt('r23_f1.txt')
n = [[0] * 64 for _ in range(64)]
for y in range(2, 64): n[y - 2] = g[y][:]
for y in range(38, 64):
    for x in range(64): n[y][x] = 0 if y >= 40 else n[y][x]
for y in range(30, 40):
    for x in range(48, 64): n[y][x] = 0
t = [[0] * 64 for _ in range(64)]
for y in range(34, 42):
    for x in range(48, 58):
        if r[y][x]: t[y - 2][x + 2] = r[y][x]
open('staart.txt', 'w').write(T.to_txt(t))
open('_s2.txt', 'w').write(T.to_txt(n))
run('teken.py', '_s2.txt', 'onder.txt', 'werk_f1.txt')
run('frame2.py')
for f in ('_s1.txt', '_s2.txt'): os.remove(f)
