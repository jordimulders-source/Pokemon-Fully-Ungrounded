#!/bin/sh
# Palpaca r1 volledig opnieuw draaien (in deze map): model -> natief raster -> zones -> reductie (onderlaag) -> palet + opschonen -> reparaties -> meting -> vel
set -e
python3 natief.py ../../../model/model.png natief.png
python3 zones.py
python3 bouw.py > /dev/null
python3 maak.py > /dev/null
python3 reparatie.py
python3 meet.py
python3 vel.py
