# px.py x,y x,y ... : modelhelderheid per spritepixel (gem / 15e pct / max) + spritewaarde (naar poedelmot/kleur_r19/stappen/px.py)
import sys,os,numpy as np
H=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,H+'/../silhouet')
from geo import *
L=model().mean(2)
R=[l.rstrip('\n') for l in open(H+'/raster.txt')]
for a in sys.argv[1:]:
    x,y=map(int,a.split(',')); ya,yb,xa,xb=blok(x,y); b=L[ya:yb,xa:xb]
    print(f'({x},{y}) sprite {R[y][x]}  model gem {b.mean():.0f} p15 {np.percentile(b,15):.0f} max {b.max():.0f}')
