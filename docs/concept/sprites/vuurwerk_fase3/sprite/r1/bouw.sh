#!/bin/sh
# Volledige keten r1 (draaien vanuit deze map). Kale reductie -> opschonen -> gezicht -> twinkels -> bovenlaag (Jordi's afwijkingen).
set -e
python3 natief.py                       # natief raster 199x199 (pitch 5,12)
python3 reductie.py                     # kaal.png      = kale reductie (met glitter), referentie voor de telling
python3 reductie.py deglitter           # kaal_dg.png   = idem zonder glitterstippen (afwijking 1, deel 'weg')
python3 opschoon.py kaal_dg.png opgeschoond.png
python3 gezicht.py opgeschoond.png stap_gezicht.png
python3 glitter.py                      # glinsterplekken in het lijf (op stap_gezicht.png)
python3 twinkel.py stap_gezicht.png stap_twinkel.png
python3 ref_burst.py > /dev/null        # Jordi's vuurwerkvel -> ref_burst.json
python3 bovenlaag.py stap_twinkel.png sprite.png b1
python3 telling.py
python3 vel.py sprite.png vel.png
