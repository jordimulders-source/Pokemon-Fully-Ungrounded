#!/bin/sh
# s8: s7 (sh ../s7/alles.sh) + keurderpunten op s7 (fix8.py). Alleen afwerking binnen het silhouet, bestaande paletindexen.
cd "$(dirname "$0")"
python3 fix8.py
cp ../s7/normal.pal .
python3 vel.py ../s7/hoatzin.png
python3 naast.py ../s7/hoatzin.png hoatzin.png
python3 ../../sprite/r11/check.py hoatzin.png
python3 ../../sprite/r23/barcode.py hoatzin.png
python3 los.py
