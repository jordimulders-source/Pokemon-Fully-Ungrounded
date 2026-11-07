"""Ronde 1h (bevroren t.o.v. v7, behalve (29,29)/(30,30) toegestaan; diff per punt t.o.v. 1g): bevroren delen 0 px diff met v7, diff per zone, open randen, losse pixels, korrel.py."""
import os, subprocess
from collections import Counter
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(H)
g=[l.rstrip('\n') for l in open(os.path.join(R,'raster.txt'))]
v=[l.rstrip('\n') for l in open(os.path.join(R,'../ronde1f/v7/raster.txt'))]
P=lambda x,y: g[y][x] if 0<=x<64 and 0<=y<64 else '.'
BEV={
 'kop+gezicht+maan (x0-20, rij 29-47; rij 27-28 x0-13)': lambda x,y: (x<=20 and 29<=y<=47) or (x<=13 and 27<=y<=28),
 'hand/gloed/gezicht/maan-kleuren (FfPpBbGMmW in v7)': lambda x,y: v[y][x] in 'FfPpBbGMmW',
 'hand+gloed vak (x6-21, rij 44-63)': lambda x,y: 6<=x<=21 and 44<=y<=63,
 'staart (x>=44 rij 0-38; x>=49 rij 39-41)': lambda x,y: (x>=44 and y<=38) or (x>=49 and 39<=y<=41),
 'opgeheven been (x28-44, rij 0-30)': lambda x,y: 28<=x<=44 and y<=30,
 'buitenomtrek dij rechts (rij 31-35, x41-44)': lambda x,y: 31<=y<=35 and 41<=x<=44 and v[y][x] in 'KD',
}
for n,f in BEV.items():
    d=[(x,y) for y in range(64) for x in range(64) if f(x,y) and g[y][x]!=v[y][x] and (x,y) not in ((29,29),(30,30))]
    print('BEVROREN %-55s diff %d %s'%(n,len(d),d))
w=[l.rstrip('\n') for l in open(os.path.join(R,'../ronde1g/raster.txt'))]
print('toegestane beenpixels (29,29),(30,30): v7',v[29][29],v[30][30],'-> 1h',g[29][29],g[30][30])
v=w  # vanaf hier diff met 1g
ZONES=[('1 rug-dij-hoek',lambda x,y:y<=30),('4 heup bovenkant',lambda x,y:38<=y<=41 and x>=41),
       ('2 romp bol',lambda x,y:y<=45),('3 knie/bovenbeen',lambda x,y:True)]
dz=Counter(); om=Counter()
for y in range(64):
    for x in range(64):
        if g[y][x]!=v[y][x]:
            z=next(n for n,f in ZONES if f(x,y)); dz[z]+=1
            if (g[y][x]=='.')!=(v[y][x]=='.'): om[z]+=1
print('diff met 1g per punt',dict(dz),'totaal',sum(dz.values()))
print('omtrek (alpha) gewijzigd per zone',dict(om))
op=[(x,y,g[y][x]) for y in range(64) for x in range(64) if g[y][x] not in '.KDG' and any(P(x+a,y+b)=='.' for a,b in((1,0),(-1,0),(0,1),(0,-1)))]
print('open randen',len(op),op)
los=[(x,y,g[y][x]) for y in range(64) for x in range(64) if g[y][x]!='.' and all(P(x+a,y+b)!=g[y][x] for a,b in((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)))]
losv=[(x,y,c) for x,y,c in los if v[y][x]!=c or any(v[y+b][x+a]!=g[y+b][x+a] for a in(-1,0,1) for b in(-1,0,1) if 0<=x+a<64 and 0<=y+b<64)]
print('losse pixels totaal',len(los),'waarvan nieuw/in gewijzigde buurt',len(losv),losv)
print('pixels',sum(c!='.' for r in g for c in r),'(v7',sum(c!='.' for r in v for c in r),')')
