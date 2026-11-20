# Hoatzin r6: "blurry" oplossen op r5 (r5.png = kopie van ../r5/hoatzin.png); gebruikt ../r4/zone_t.npy, lijn_nat.npy, streep_nat.npy
python3 natief.py ../../MODEL.png natief.png 5.12 4.0
python3 zones.py > /dev/null
python3 r6.py > r6.log
python3 vel.py
python3 meet.py r5.png hoatzin.png
python3 vlek.py r5.png hoatzin.png
