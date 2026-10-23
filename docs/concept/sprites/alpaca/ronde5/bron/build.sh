#!/bin/sh
# Bouwt ronde 5 opnieuw (vanuit bron/).
set -e
T=../../../../../../tools/concept/sprites
python3 compose.py alpaca5.txt
python3 $T/ascii_sprite.py load alpaca5.txt ../normal.pal ../anim_front.png
python3 compare5.py ../anim_front.png ../../ronde4/anim_front.png ../../../../../../graphics/pokemon ../compare.png
rm -rf __pycache__ sil.txt sil_sh.txt
