set -e
cd "$(dirname "$0")"
python3 reduceer.py 0 0 fase/f00.png 2>/dev/null; cp fase/f00.npy basis.npy; cp fase/f00_deel.npy basis_deel.npy; cp fase/f00.png basis.png
python3 stap2.py; python3 stap3.py; python3 gezicht.py >/dev/null; python3 stap4.py; python3 stap5.py; python3 vel.py pachamama_r1.png vel.png
