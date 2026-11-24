#!/bin/sh
# Mr. Prime sprite r1, hele keten vanaf gemini/r9.png (draaien in deze map)
set -e
python3 natief_r9.py                 # natief raster (pitch 5.12) -> natief.png
python3 been.py -17 -11 213          # achterbeen telescopisch inschuiven -> natief_been.png
python3 stok.py 3 2 58               # schacht 3 natieve px breder (middenkolommen gedupliceerd) -> natief_stok.png
python3 -c "import numpy as np, gezicht_fase as g; np.save('kaal_idx.npy', g.red(0,2)); np.save('kaal_mode_idx.npy', g.red_mode(0,2))"
python3 stap1_basis.py               # in 64x64, r9-hoed/lokken weg -> basis.npy
python3 maak_vel.py                  # ogen, hoed/haar, opschoning -> mr_prime.png, varianten, vel.png
