#!/bin/sh
# Mr. Prime sprite r7, hele keten vanaf gemini/r9.png (draaien in deze map): r6-keten, dan r7.py via vel7.py
set -e
python3 natief_r9.py                 # natief raster (pitch 5.12) -> natief.png
python3 been.py -17 -11 213          # achterbeen telescopisch inschuiven -> natief_been.png
python3 stok.py 3 2 58               # schacht 3 natieve px breder -> natief_stok.png
python3 kop_natief.py                # linkerring weg, voorhoofd (witte modelrij 5x), hand wit -> natief_kop.png (+ natief_kop_stok.png)
python3 -c "import numpy as np, gezicht_fase as g; np.save('kaal_idx.npy', g.red(0,2)); np.save('kaal_mode_idx.npy', g.red_mode(0,2))"
BRON=natief_kop_stok.png python3 -c "import numpy as np, gezicht_fase as g; np.save('kaal_stok_idx.npy', g.red(0,2))"
python3 stap1_basis.py               # in 64x64, r9-hoed/lokken weg -> basis.npy
python3 maak_vel.py                  # r6.py (voorhoofd +2, Rime-ogen, kopomtrek model, hoed A, snorrand, neus model, opschoon, r3post) + stok5.py + palet.py -> mr_prime.png, vel.png
cp mr_prime.png r6_uit.png          # r6-uitvoer (identiek aan ../sprite_r6/mr_prime.png)
python3 vel7.py                      # r7.py (stok, linkeroog, linkerhaar Rime 1-op-1, ronde kop, DC-omlijning + schaduw met licht.py) -> mr_prime.png, vel.png
python3 controle.py                  # kleuren, losse tintvlakjes
