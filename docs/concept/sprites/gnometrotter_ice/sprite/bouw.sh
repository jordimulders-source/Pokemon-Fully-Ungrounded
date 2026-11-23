#!/bin/sh
# volledige pijplijn Ice (volgorde): fam -> zones -> reductie -> maak -> meet -> ijs -> dc -> tel/controle -> vel
set -e
python3 fam.py >/dev/null; python3 zones.py >/dev/null; python3 reductie.py; python3 maak.py; python3 meet.py >/dev/null
python3 ijs.py; python3 dc.py; python3 tel.py; python3 controle.py gnometrotter_ice.png
