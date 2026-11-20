#!/bin/sh
# s7: s6 + coordinatorpunten (omlijning snavel/poten, schaduw per pen, nek-sikkel). Niets getekend.
cd "$(dirname "$0")"
python3 bouw7.py
python3 vel.py ../s6/hoatzin.png
python3 naast.py ../s6/hoatzin.png hoatzin.png
python3 ../../sprite/r11/check.py hoatzin.png
python3 ../../sprite/r23/barcode.py hoatzin.png
python3 los.py
python3 telzones.py
