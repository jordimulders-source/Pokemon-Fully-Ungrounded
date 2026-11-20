#!/bin/sh
# s6: s5 + afwerking (omlijning kuif/snavel/poten, 3 tinten per kleurgroep, keurderpunten R1-R6). Niets getekend.
cd "$(dirname "$0")"
python3 bouw6.py
python3 vel.py ../s5/hoatzin.png
python3 naast.py ../s5/hoatzin.png hoatzin.png
python3 ../../sprite/r11/check.py hoatzin.png
python3 ../../sprite/r23/barcode.py hoatzin.png
python3 los.py
python3 telzones.py
