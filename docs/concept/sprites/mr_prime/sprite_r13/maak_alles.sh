#!/bin/sh
# r13: DFC-eindkeuring (12 MOET-punten) op r12 O3, alleen omkleuren binnen het silhouet (alpha-diff 0 wordt in r13.py gecontroleerd).
# Keten: ../sprite_r11/maak_alles.sh -> ../sprite_r12/maak_alles.sh (maakt oog_O3.png) -> dit.
set -e
cp ../sprite_r12/oog_O3.png oog_O3.png
python3 r13.py   # -> mr_prime.png, mr_prime_8x.png, vel.png
