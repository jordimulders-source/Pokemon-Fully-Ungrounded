#!/bin/sh
# Keten r2 (vanuit deze map). Gebruikt natief.png en ref_burst.json; schrijft sprite_A/B/C.png, sprite.png (= A) en vel.png.
set -e
python3 reductie.py > /dev/null; python3 reductie.py deglitter > /dev/null
python3 ref_burst.py > /dev/null
python3 kop.py 0.35 > /dev/null
python3 r2.py; python3 lijnen.py; python3 gezicht2.py; python3 pijl.py; python3 afwerken.py
cp sprite_A.png sprite.png
python3 telling2.py; python3 vel2.py
