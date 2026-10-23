#!/bin/sh
# Bouwt ronde 17, variant_ogen: kop17.py (kop + staart) -> delen_abs.txt -> delen.txt -> anim_front.png/normal.pal (+ optioneel 8x-preview)
# Gebruik: sh bron/bouw.sh <ronde17/variant_ogen-map> [preview.png]   (kop17.py leest de snuit uit ../ronde15/bron/raster_f1.txt)
D="$1"
OLI_VARIANT=ogen python3 "$D/bron/kop17.py" "$D" && python3 "$D/bron/abs2delen.py" "$D" && python3 "$D/bron/bouw9.py" "$D" $2
