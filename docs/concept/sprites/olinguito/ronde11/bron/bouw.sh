#!/bin/sh
# Bouwt ronde 11: delen_abs.txt -> delen.txt -> anim_front.png/normal.pal (+ optioneel 8x-preview)
# Gebruik: sh bron/bouw.sh <ronde11-map> [preview.png]
D="$1"
python3 "$D/bron/abs2delen.py" "$D" && python3 "$D/bron/bouw9.py" "$D" $2
