#!/usr/bin/env python3
"""Bouwt finale/anim_front.png uit werk_f1.txt en werk_f2.txt (gemaakt door maak.py) en draait de controles (check.py).
Volgorde: python3 maak.py && python3 bouw.py"""
import os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tools as T
H = T.H; F = os.path.join(H, '..')
g1 = T.read_txt(os.path.join(H, 'werk_f1.txt'))
g2 = T.read_txt(os.path.join(H, 'werk_f2.txt'))
if __name__ == '__main__':
    T.save_png([g1, g2], os.path.join(F, 'anim_front.png'))
    shutil.copy(os.path.join(T.OL, 'ronde23', 'normal.pal'), os.path.join(F, 'normal.pal'))
    import check
    check.run(os.path.join(F, 'anim_front.png'))
