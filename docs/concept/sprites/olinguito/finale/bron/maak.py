#!/usr/bin/env python3
"""Bouwstraat (alles met de hand in tekstbestanden; ronde-23-coördinaten):
1. ronde 23 als basis (kop, voorpoten, romp, dij, nabije achterpoot, J-staart blijven staan)
2. kop.txt: achterkant van de schedel naar binnen (rest van de kop pixel-identiek)
3. klauwen.txt: twee Sandslash-haken per voorpoot (vervangen de klodders van ronde 23)
4. voorpoot.txt: onderarm van de nabije voorpoot in een boog
5. achterlijf.txt: rug zonder rechte stukken, knie-knik nabije achterpoot, verre achterpoot (nieuw)
6. frame 2 (zie frame2.txt)"""
import subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
def run(*a): subprocess.run([sys.executable] + list(a), check=True)
run('teken.py', 'r23_f1.txt', 'kop.txt', '_s1.txt')
run('teken.py', '_s1.txt', 'klauwen.txt', '_s2.txt')
run('teken.py', '_s2.txt', 'voorpoot.txt', '_s3.txt')
run('teken.py', '_s3.txt', 'achterlijf.txt', 'werk_f1.txt')
run('frame2.py')
for f in ('_s1.txt', '_s2.txt', '_s3.txt'):
    os.remove(f)
