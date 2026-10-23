#!/bin/sh
# Ronde 19 bouwen (vanuit ronde19/bron): kop19.txt op het lijf van ronde 18, knip, frame 2, PNG.
set -e
python3 samen.py 13 21
python3 fix.py samen_f1.txt 38,31=31 38,32=332 38,33=345 38,34=34 37,35=334 37,36=334 36,37=3334 36,38=3334
python3 -c "
L=[l.rstrip('\n') for l in open('samen_f1.txt')]
open('samen_f1.txt','w').write('\n'.join(r[:40]+r[42:]+'..' for r in L)+'\n')"
python3 fix.py samen_f1.txt 40,43=2 39,44=32 40,45=2 40,49=1 40,50=1 40,51=1
python3 frame2.py
python3 fix.py samen_f2.txt 40,49=1 40,50=1 40,51=1 39,31=2
python3 maak.py
