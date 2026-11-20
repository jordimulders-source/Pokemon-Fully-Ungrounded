# r22: vorm (bouw19.py + poten22.py) -> kleur22.py -> check -> vel
set -e
python3 bouw19.py
python3 poten22.py
python3 kleur22.py 4 5
python3 check.py
python3 vel.py
