# Hoatzin r1 opnieuw bouwen
python3 pitch.py
python3 natief.py ../../MODEL.png natief.png 5.12 4.0
python3 zones.py
python3 bouw.py > bouw.log
OOG=B python3 stappen.py > /dev/null && cp hoatzin.png hoatzin_oogB.png
python3 stappen.py > stappen.log
python3 vel.py
