#!/bin/sh
# Keten r4 (vanuit deze map): alleen de KOP, op ../r3/sprite.png (gezicht V, spikkels B); de rest is bevroren.
set -e
python3 meet4.py            # meting per spritepixel op het model (dekking, lijn, roze, helderheid) -> meting.npz, model_fg.npz
python3 goudkaart.py > /dev/null   # goud/tan-strengen uit het natieve model -> kaart_goud.npy
python3 kop4.py kaal stil   # kale kop-reductie (zonder reparaties) -> sprite_kaal.png
python3 kop4.py stil        # + gezicht4.json en opschoning -> sprite.png
python3 telling4.py         # bewijs: diff per zone, buiten de kop 0
python3 schoon.py           # tintvlakjes < 3 px in de kop (twinkels staan er ook in)
python3 vel4.py
