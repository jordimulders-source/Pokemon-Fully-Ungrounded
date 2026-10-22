#!/bin/sh
# Bouwt anim_front.png, normal.pal, thumbnails.png en compare.png van ronde 3 opnieuw (vanuit bron/).
set -e
T=/home/user/projectgrounded/tools/concept/sprites
python3 alpaca3.py .
python3 $T/segraster.py alpaca3.seg normal.pal ../anim_front.png
mv normal.pal ../normal.pal
python3 thumbs3.py ..
python3 compare3.py ../compare.png
