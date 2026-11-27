set -e; cd "$(dirname "$0")/.."
python3 r2/reduceer.py 0 1 r2/basis.png natief_g1.png
cd r2; python3 romp.py; python3 gezicht_toon.py >/dev/null 2>&1; python3 gezicht.py lijnen.txt ogen.txt
python3 kap.py gez.npy kap.npy; python3 lijnen_onder.py kap.npy onder.npy
cp onder.npy pachamama_r2.npy; cp onder.png pachamama_r2.png; python3 ../zoom.py pachamama_r2.png pachamama_r2_8x.png; python3 vel.py
