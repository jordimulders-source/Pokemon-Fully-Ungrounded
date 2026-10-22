#!/bin/sh
# Bouwt anim_front.png + normal.pal van de alpaca ronde 2 opnieuw (vanuit deze map).
set -e
T=/home/user/projectgrounded/tools/concept/sprites
python3 alpaca2.py .                      # procedurele basis -> anim_front.png + normal.pal
mv anim_front.png procbase.png
python3 $T/segraster.py alpaca2.seg normal.pal ../anim_front.png   # handwerk erover
mv normal.pal ../normal.pal
python3 thumbs.py ..
python3 compare2.py ../compare.png
