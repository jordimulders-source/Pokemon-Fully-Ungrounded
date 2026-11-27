set -e; cd "$(dirname "$0")/.."
python3 natief.py; python3 hoofdgroot.py 1.2 1.28 62 16 natief_g1.png
python3 reduceer.py 0 0 fase/f00.png natief.png 2>/dev/null; python3 reduceer.py 0 1 fase/f01.png natief.png
python3 reduceer.py 0 1 r1/basis.png natief_g1.png
cd r1; python3 romp.py; python3 gezicht_toon.py >/dev/null; python3 gezicht.py lijnen.txt ogen.txt
cp gez.png pachamama_r1.png; cp gez.npy pachamama_r1.npy; python3 ../zoom.py pachamama_r1.png pachamama_r1_8x.png; python3 vel.py
