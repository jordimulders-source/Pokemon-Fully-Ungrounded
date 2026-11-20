# r19: vorm (bouw19.py: neklijnposities, pootvorm) -> kleur (kleur19.py, streep 4/9, penscheiding 5/9) -> check -> vel
set -e
python3 bouw19.py
python3 kleur19.py 4 5
python3 check.py
python3 vel.py
