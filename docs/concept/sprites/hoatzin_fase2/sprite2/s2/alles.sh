#!/bin/sh
# s1: kale reductie van MODEL.png -> sprite (alleen technisch opgeschoond, niets getekend)
cd "$(dirname "$0")"
python3 reduceer.py && python3 lijnen.py && python3 bouw.py && python3 vel.py
python3 ../../sprite/r11/check.py hoatzin.png
python3 ../../sprite/r23/barcode.py hoatzin.png
python3 afwijking.py
