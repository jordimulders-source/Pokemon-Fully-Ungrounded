#!/bin/sh
# Bouwt ronde 4 opnieuw (vanuit bron/).
set -e
T=/home/user/projectgrounded/tools/concept/sprites
python3 alpaca4.py .
python3 $T/segraster.py alpaca4.seg normal.pal ../anim_front.png
mv normal.pal ../normal.pal
python3 thumbs4.py ..
python3 compare4.py ../compare.png
rm -rf __pycache__
