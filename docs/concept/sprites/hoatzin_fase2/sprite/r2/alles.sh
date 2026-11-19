# Hoatzin r2 opnieuw bouwen
python3 natief.py ../../MODEL.png natief.png 5.12 4.0
python3 zones.py > /dev/null
python3 bouw.py > bouw.log            # kale reductie -> onderlaag.png, zone_t.npy
python3 stappen.py > /dev/null        # r1-regels: levert stapA.npy (onderlaag in paletkleuren) als vergelijkingsbasis
python3 lijnkaart.py                  # lijnkaart.png: scheidingslijnen (rood) en lichte strepen (cyaan) op het model
python3 pennen.py                     # pennen.png: pennen gesegmenteerd op het model
python3 r2.py > r2.log                # hoatzin.png
python3 zonediff.py
python3 vel.py
