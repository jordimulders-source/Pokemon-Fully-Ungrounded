# Hoatzin r5: pixelreparaties op r4 (r4.png = kopie van ../r4/hoatzin.png)
python3 natief.py ../../MODEL.png natief.png 5.12 4.0
python3 zones.py > /dev/null
python3 r5.py > r5.log
python3 vel.py
(cd buik && python3 buik.py)
