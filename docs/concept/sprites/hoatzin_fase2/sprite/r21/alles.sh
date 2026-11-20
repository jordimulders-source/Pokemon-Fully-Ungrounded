# r21: vorm (bouw19.py, = r19-vorm) -> kleur21.py (r20 + veerlijnen armpennen + kuifplukken uit lijnen.py) -> check -> vel
set -e
python3 bouw19.py
python3 kleur21.py 4 5
python3 check.py
python3 vel.py
