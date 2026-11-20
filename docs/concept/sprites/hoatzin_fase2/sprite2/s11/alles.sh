#!/bin/sh
# s11: s10 opnieuw ingekleurd op hoofd, poten en verre vleugel. Vorm en oog bevroren (assert in bouw11.py).
cd "$(dirname "$0")"
python3 bouw11.py
python3 vel11.py
python3 ../../sprite/r11/check.py hoatzin.png
python3 ../../sprite/r23/barcode.py hoatzin.png
python3 ../s10/los.py hoatzin.png
