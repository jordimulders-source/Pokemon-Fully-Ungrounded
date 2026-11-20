#!/bin/sh
# s5: s4 + licht/schaduw per vorm (pitahaya fase 3). Niets getekend.
cd "$(dirname "$0")"
set -- $(cat fase_keuze.txt)
DX=$1 DY=$2 python3 reduceer.py && python3 lijnen.py && python3 skelet.py && python3 kuifas.py >/dev/null && python3 bouw5.py
python3 vel.py ../s4/hoatzin.png
python3 ../../sprite/r11/check.py hoatzin.png
python3 ../../sprite/r23/barcode.py hoatzin.png
python3 los.py
python3 afwijking.py
