#!/bin/sh
# s10: s9 opnieuw ingekleurd naar de studie van bestaande sprites. Vorm en oog bevroren.
cd "$(dirname "$0")"
python3 bouw10.py
python3 studievel.py
python3 naast.py ../s9/hoatzin.png hoatzin.png
python3 ../../sprite/r11/check.py hoatzin.png
python3 ../../sprite/r23/barcode.py hoatzin.png
python3 los.py
