#!/bin/sh
# Volledige ronde r1 opnieuw draaien (in deze map). Model -> natief -> zones -> onderlaag/stap A -> B/C/D -> hummlet.png + vel.png
set -e
python3 natief.py ../../../referenties/gemini_gekozen_r5.png natief.png
python3 zones.py >/dev/null
python3 bouw.py >/dev/null
python3 pfrac.py
python3 spikkels.py >/dev/null
python3 stappen.py
python3 maak.py
