#!/bin/sh
# Keten r5 (vanuit deze map): kop groter (115% en 125%), oogvarianten, losse vlam, spikkels opnieuw. Basis ../r4/sprite.png.
set -e
python3 klassen.py
for s in 1.15 1.25; do for k in 13 14 7 11; do python3 kop5.py $s 2 $k stil; done; done   # oog 13 geel, 14 goud, 7 magenta, 11 rood
python3 maak5.py            # + vlam5.py + spikkels B -> sprite_<maat>_<oog>.png
python3 telling5.py
python3 vel5.py
