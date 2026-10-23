#!/bin/sh
# Bouwt ronde 16: kop16.py (kop + staart) -> delen_abs.txt -> delen.txt -> anim_front.png/normal.pal (+ optioneel 8x-preview)
# Gebruik: sh bron/bouw.sh <ronde16-map> [preview.png]   (kop16.py leest de snuit uit ../ronde15/bron/raster_f1.txt)
D="$1"
python3 "$D/bron/kop16.py" "$D" && python3 "$D/bron/abs2delen.py" "$D" && python3 "$D/bron/bouw9.py" "$D" $2
