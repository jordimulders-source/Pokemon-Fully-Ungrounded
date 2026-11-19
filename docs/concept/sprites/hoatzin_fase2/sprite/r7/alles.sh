# Hoatzin r7 op r6 (r6.png = kopie van ../r6/hoatzin.png); gebruikt ../r4/zone_t.npy, lijn_nat.npy, streep_nat.npy
python3 natief.py ../../MODEL.png natief.png 5.12 4.0
python3 zones.py > /dev/null
python3 kuifkaart.py                 # kuif_t.npy (bruinaandeel per cel, vol model)
python3 r7.py > r7.log               # kop_A/B/C.png (alleen kuifzone verschilt)
cp kop_B.png hoatzin.png             # hoofdversie = B
python3 vel.py; python3 kopvel.py
python3 meet.py r6.png kop_A.png kop_B.png kop_C.png
