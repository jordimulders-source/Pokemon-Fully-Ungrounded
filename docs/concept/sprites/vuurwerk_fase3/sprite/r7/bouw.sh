#!/bin/sh
# Keten r7 (vanuit deze map): alleen het oog 1,5x groter (zelfde reductie als r5, extra vergroting rond het oogmidden) + pupil.
set -e
python3 oog7.py 13,22 1.5,2.0,3.2 stil
python3 telling7.py
python3 vel7.py
