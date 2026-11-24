#!/bin/sh
# r14: drie vormreparaties op r13 (Jordi "ja": verre arm, achterbeen gestrekt, rokpanden als één vorm). Draaien in deze map.
set -e
# vormgids achterbeen: modelbeen (natief, ../sprite_r1/natief.png) langs de beenas afgeschoven zodat de schoen
# 7 px naar links staat (x<=63) en 1 rij hoger dan in het model; verkleind met dezelfde reductie als de rest -> been_gids_k3.npy
python3 beenshear.py -17 -3.5 natief_been_k3.png
python3 -c "import numpy as np, red; np.save('been_gids_k3.npy', red.red_img('natief_been_k3.png',W=64,H=64))"
python3 r14.py       # -> mr_prime.png (palet en indexvolgorde van r13)
python3 diff.py      # telt per zone; buiten de zones moet 0 zijn
python3 check.py     # kleine clusters / open randen in de zones
python3 maak_vel.py  # -> vel.png, mr_prime_8x.png
