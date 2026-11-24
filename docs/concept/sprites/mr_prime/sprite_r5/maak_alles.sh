#!/bin/sh
# Mr. Prime sprite r5, hele keten vanaf gemini/r9.png (draaien in deze map)
set -e
python3 natief_r9.py                 # natief raster (pitch 5.12) -> natief.png
python3 been.py -17 -11 213          # achterbeen telescopisch inschuiven -> natief_been.png
python3 stok.py 3 2 58               # schacht 3 natieve px breder -> natief_stok.png
python3 kop_natief.py                # linkerring weg, voorhoofd (witte modelrij 5x), hand wit -> natief_kop.png (+ natief_kop_stok.png)
python3 -c "import numpy as np, gezicht_fase as g; np.save('kaal_idx.npy', g.red(0,2)); np.save('kaal_mode_idx.npy', g.red_mode(0,2))"
BRON=natief_kop_stok.png python3 -c "import numpy as np, gezicht_fase as g; np.save('kaal_stok_idx.npy', g.red(0,2))"
python3 stap1_basis.py               # in 64x64, r9-hoed/lokken weg -> basis.npy
python3 maak_vel.py                  # r5.py (voorhoofd +2, Rime-ogen, hoed A, kop rond, snorrand, opschoon, r3post) + stok5.py + palet.py -> mr_prime.png, vel.png
