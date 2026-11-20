# r18 = r17 + linkerpoot (bouw18.py, tabel meetpoot.txt) + nek los van de vleugel (nek.py); vel.py -> poot_vel.png
set -e
python3 bouw18.py
python3 check.py
python3 vel.py
