#!/bin/sh
# Keten r3 (vanuit deze map): start op r2_basis.npy (bevroren lijf/lijnen/pijl), alleen kop + gezicht + spikkels.
set -e
python3 lijnkaart.py > /dev/null
python3 kop3.py 2
python3 spikkels3.py
cp sprite_V_B.png sprite.png
python3 telling3.py; python3 vel3.py
