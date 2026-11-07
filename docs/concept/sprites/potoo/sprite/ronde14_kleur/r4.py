"""Ronde 4: ronde 3 + keelspleet (donkerste punt achter in de muil, met de hand: 3 px)."""
import runpy, os
R = runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'r3.py'))['R']
O = {18:[(20,"1")],19:[(20,"1")],20:[(20,"1")]}
for y, segs in O.items(): R[y] = R.get(y, []) + segs
