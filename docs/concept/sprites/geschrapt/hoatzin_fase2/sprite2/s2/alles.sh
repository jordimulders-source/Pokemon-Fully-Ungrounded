#!/bin/sh
# s2: reductie met betere overname-instellingen (fase, wit-menging, penlijnen, snavel) + Jordi's oog (variant B)
# fase opnieuw zoeken: python3 fase.py (schrijft fase_keuze.txt)
cd "$(dirname "$0")"
set -- $(cat fase_keuze.txt)
DX=$1 DY=$2 python3 reduceer.py && python3 lijnen.py && PENMIN=6 python3 bouw.py && python3 oog.py
cp hoatzin_oogB.png hoatzin.png
python3 -c "from PIL import Image; Image.open('hoatzin.png').resize((512,512),Image.NEAREST).save('hoatzin_8x.png', transparency=0)"
python3 vel.py
python3 ../../sprite/r11/check.py hoatzin.png
python3 ../../sprite/r23/barcode.py hoatzin.png
python3 afwijking.py
