"""Telt rechte stukken (binnenkant; buitenrand = silhouet telt niet mee) >=4 px buiten de toren: (a) lijnruns (index 1 of 4, horizontaal/verticaal),
(b) rechte tintgrenzen: >=4 opeenvolgende grenzen tussen twee verschillende niet-transparante tinten op dezelfde rij/kolomlijn.
Gebruik: python3 recht.py sprite.png [lijst]"""
import sys, numpy as np
from PIL import Image
a=np.array(Image.open(sys.argv[1])).astype(int)
def toren(x,y): return x>=44 and y<=32 and not (x<=46 and y>=29)
def ok(x,y): return not toren(x,y)
def rand(x,y): return any(a[y+b,x+c]==0 for c,b in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=x+c<64 and 0<=y+b<64)
runs=[]
for y in range(64):
    x=0
    while x<64:
        v=a[y,x]
        if v in (1,4) and ok(x,y) and not rand(x,y):
            e=x
            while e+1<64 and a[y,e+1]==v and ok(e+1,y) and not rand(e+1,y): e+=1
            if e-x+1>=4: runs.append(('lijn-h',v,x,y,e-x+1))
            x=e+1
        else: x+=1
for x in range(64):
    y=0
    while y<64:
        v=a[y,x]
        if v in (1,4) and ok(x,y) and not rand(x,y):
            e=y
            while e+1<64 and a[e+1,x]==v and ok(x,e+1) and not rand(x,e+1): e+=1
            if e-y+1>=4: runs.append(('lijn-v',v,x,y,e-y+1))
            y=e+1
        else: y+=1
# tintgrenzen: horizontale grens tussen rij y en y+1 (beide ondoorzichtig, verschillend, geen lijnindex), run in x
def fill(v): return v not in (0,1)
for y in range(63):
    x=0
    while x<64:
        def g(x): return ok(x,y) and ok(x,y+1) and fill(a[y,x]) and fill(a[y+1,x]) and a[y,x]!=a[y+1,x]
        if g(x):
            e=x
            while e+1<64 and g(e+1) and a[y,e+1]==a[y,x] and a[y+1,e+1]==a[y+1,x]: e+=1
            if e-x+1>=4: runs.append(('grens-h',(a[y,x],a[y+1,x]),x,y,e-x+1))
            x=e+1
        else: x+=1
for x in range(63):
    y=0
    while y<64:
        def g(y): return ok(x,y) and ok(x+1,y) and fill(a[y,x]) and fill(a[y,x+1]) and a[y,x]!=a[y,x+1]
        if g(y):
            e=y
            while e+1<64 and g(e+1) and a[e+1,x]==a[y,x] and a[e+1,x+1]==a[y,x+1]: e+=1
            if e-y+1>=4: runs.append(('grens-v',(a[y,x],a[y,x+1]),x,y,e-y+1))
            y=e+1
        else: y+=1
from collections import Counter
c=Counter(r[0] for r in runs); print(sys.argv[1], dict(c), 'totaal',len(runs), 'px',sum(r[4] for r in runs))
if len(sys.argv)>2:
    for r in sorted(runs,key=lambda r:-r[4]): print('  ',r)
