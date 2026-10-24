#!/usr/bin/env python3
"""Volledige bouwstraat van frame 1 (alles met de hand getekend in de tekstbestanden):
1. basis.py: ronde 23 zonder staart/achterlijf, achterhoofd 2 px korter; J-staart (bevroren) op (+2,-3)
2. achterlijf.txt: rug, romp, dij, nabije achterpoot met hak, verre achterpoot (+ staart ertussen)
3. klauwen.txt: twee Sandslash-haken per voorpoot
4. knippen (strook weg, §15): KNIP hieronder (frame 1 en frame 2 apart)
5. naden_f1.txt / naden_f2.txt: met de hand nagelopen naden na het knippen (coördinaten van het eindraster)"""
import subprocess, sys, os
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
# Frame 1 knipt drie stroken; frame 2 laat de laatste (een rij onder de kaak/dij) staan: kop, romp en staartwortel
# staan dan 1 px hoger, de poten 1 rij langer en de hangende staart 1 rij langer (ademhaling); voeten blijven op de grond.
KNIP = {'f1': ['42:0-63', '26:0-37', '40:0-63'], 'f2': ['42:0-63', '26:0-37']}
def run(*a): subprocess.run([sys.executable] + list(a), check=True)
run('basis.py', '2', '-3', '_s1.txt')
run('teken.py', '_s1.txt', 'achterlijf.txt', '_s2.txt')
run('teken.py', '_s2.txt', 'klauwen.txt', '_s3.txt')
for f in ('f1', 'f2'):
    run('knip.py', '_s3.txt', '_s4.txt', *KNIP[f])
    run('teken.py', '_s4.txt', 'naden_%s.txt' % f, 'werk_%s.txt' % f)

for f in ('_s1.txt', '_s2.txt', '_s3.txt', '_s4.txt'):
    os.remove(f)
