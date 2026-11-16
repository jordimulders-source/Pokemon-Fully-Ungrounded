# Volgorde r1 (vanuit deze map): model op natief raster -> kale reductie 1,5x -> palet -> kwantiseren -> opschonen -> ogen/ruis -> controle/vel
python3 natief.py ../gemini/r5.png natief_r5.png
python3 model_natief.py          # + 2 lagen (stapel_kleur.py op natief raster); vergelijking: cmp_model.png
python3 reductie.py 0 0          # 92x68 -> 62x46, oppervlak-middeling + lijnregels
python3 palet.py                 # 8 lijf + 3 rood + 3 bordeaux, allemaal echte modelkleuren
python3 kwant.py                 # kaal.png = kale reductie
python3 bouw.py                  # buitenlijn (zwart/selout), hoekpixels binnenlijnen, ruis
python3 ogen.py                  # ogen naar modeldekking, laatste ruis -> r1.png
python3 controle.py; python3 randzwart.py r1.png; python3 vel.py r1
