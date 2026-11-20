#!/bin/sh
# s12: s10 opnieuw ingekleurd op hoofd, poten en verre vleugel. Vorm en oog bevroren (assert in bouw12.py).
cd "$(dirname "$0")"
python3 bouw12.py
python3 vel12.py
python3 ../../sprite/r11/check.py hoatzin.png
python3 ../../sprite/r23/barcode.py hoatzin.png
python3 ../s10/los.py hoatzin.png
