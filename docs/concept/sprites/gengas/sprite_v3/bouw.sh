#!/bin/sh
# v3 = v2 + keuringsreparaties. Keten: v3.py (zones) -> manen.py -> raster.txt -> gengas_v3.png, controles, diff, vel
cd "$(dirname "$0")"; mkdir -p tussen
python3 v3.py tussen/r1_zones.txt
python3 manen.py tussen/r1_zones.txt raster.txt > tussen/manen.log; cat tussen/manen.log | tail -4
python3 maak.py
python3 controle.py raster.txt
python3 diff.py
python3 vel.py
