# Volledige pijplijn r1 (model -> sprite), reproduceerbaar
set -e
python3 natief.py; python3 klassen.py; python3 reduce.py 1 4 2; python3 lijnen.py; python3 schoon.py
python3 repareer.py; python3 bouw.py r1.npy; python3 vel.py ../../af/picapau_evo.png
