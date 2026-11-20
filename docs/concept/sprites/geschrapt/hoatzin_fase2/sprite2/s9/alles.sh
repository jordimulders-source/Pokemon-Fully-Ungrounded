#!/bin/sh
# s9: s8 + kleur/lijn (eigen snavelgrijs, zwarte buitenlijn, krop zachte selout, sikkels). Vorm bevroren.
cd "$(dirname "$0")"
python3 bouw9.py
python3 vel.py ../s8/hoatzin.png
python3 naast.py ../s8/hoatzin.png hoatzin.png
python3 ../../sprite/r11/check.py hoatzin.png
python3 ../../sprite/r23/barcode.py hoatzin.png
python3 los.py
