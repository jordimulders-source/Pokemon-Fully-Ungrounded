"""B1 (lijf 30, kantel 8) met aparte kopdraai naar de kijker; ortho 56 (groter in het vak). Draaien: python3.11 kopdraai.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import picapau
os.makedirs('kopdraai', exist_ok=True)
for kd in (15, 25, 35):
    picapau.render(os.path.abspath(f'kopdraai/k{kd}.png'), lijf=30, kantel=8, schaal=56, kop_draai=kd)
