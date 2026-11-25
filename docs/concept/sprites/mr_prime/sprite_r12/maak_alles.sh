#!/bin/sh
# r12: draai eerst ../sprite_r11/maak_alles.sh (r11 -> r11.png is daar mr_prime.png), dan dit
set -e
cp ../sprite_r11/mr_prime.png r11.png
python3 r12.py   # oogvarianten O1-O4 + ronde kop -> oog_O*.png, mr_prime.png (O4), ogen_vel.png, mr_prime_8x.png
