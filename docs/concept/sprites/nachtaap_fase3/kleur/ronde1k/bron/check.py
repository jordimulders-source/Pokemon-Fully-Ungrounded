"""Ronde 1k: alleen de vuistarm. 0 px diff met 1j buiten het armvak; kop (x <= kopomtrek) binnen het vak ook 0; lucht tussen arm en kruin; open randen; losse pixels."""
import os
from collections import Counter
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(H)
g=[l.rstrip('\n') for l in open(os.path.join(R,'raster.txt'))]
v=[l.rstrip('\n') for l in open(os.path.join(H,'basis_1j.txt'))]
P=lambda x,y: g[y][x] if 0<=x<64 and 0<=y<64 else '.'
arm=lambda x,y: 21<=y<=31 and 9<=x<=22
kop=lambda x,y: (y==27 and x<=13) or (28<=y<=31 and x<=y-14)   # kruin + kopomtrek (13,27)..(17,31)
d=[(x,y,v[y][x],g[y][x]) for y in range(64) for x in range(64) if g[y][x]!=v[y][x]]
print('diff met 1j totaal',len(d))
print('buiten armvak',[t for t in d if not arm(t[0],t[1])])
print('kop/maan binnen het vak',[t for t in d if kop(t[0],t[1])])
print('omtrek gewijzigd',sum((a=='.')!=(b=='.') for x,y,a,b in d))
for y in range(26,32):
    print('rij',y,'lucht tussen kop en arm:',[x for x in range(8,23) if g[y][x]=='.' and P(x-1,y)!='.' and P(x+1,y)!='.'])
op=[(x,y,g[y][x]) for y in range(64) for x in range(64) if g[y][x] not in '.KDG' and any(P(x+a,y+b)=='.' for a,b in((1,0),(-1,0),(0,1),(0,-1)))]
print('open randen',len(op),op)
los=[(x,y,g[y][x]) for y in range(64) for x in range(64) if arm(x,y) and g[y][x]!='.' and all(P(x+a,y+b)!=g[y][x] for a,b in((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)))]
print('losse pixels in armvak',los)
print('pixels',sum(c!='.' for r in g for c in r),'(1j',sum(c!='.' for r in v for c in r),')')
