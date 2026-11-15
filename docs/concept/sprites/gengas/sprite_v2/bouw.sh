#!/bin/sh
# Volledige keten: model -> raster.txt -> gengas_v2.png -> controles -> vel.png (tussenrasters in tussen/)
cd "$(dirname "$0")"; mkdir -p tussen
python3 kwantiseer.py tussen/r0_kwantiseer.txt
python3 gezicht_schuif.py tussen/r0_kwantiseer.txt tussen/r1_gezicht.txt
python3 ontruis.py tussen/r1_gezicht.txt tussen/r2_ontruis.txt
python3 handwerk.py tussen/r2_ontruis.txt raster.txt
python3 maak.py
python3 controle.py raster.txt
python3 vel.py
