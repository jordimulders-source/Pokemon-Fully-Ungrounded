# r20: vorm (bouw19.py, = r19-vorm) -> kleur20.py (streep 4/9, penscheiding 5/9) -> check -> vel
set -e
python3 bouw19.py
python3 kleur20.py 4 5
python3 check.py
python3 vel.py
