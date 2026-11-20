# r17 helemaal opnieuw: reductie (fase 7/32, donkere lijn >=2 van 9, toonkaart sigma 1,5, donker L<62) -> pixelblad -> bouw -> beelden
set -e
python3 reduceer.py 7 32 blad.npy 2 1.5 62
python3 pixelblad.py
python3 bouw.py
python3 rastermodel.py
