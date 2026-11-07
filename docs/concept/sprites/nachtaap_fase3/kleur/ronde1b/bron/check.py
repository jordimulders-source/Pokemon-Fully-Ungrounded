"""Controle: open randen, losse pixels, alpha-diff, rechte randstukken, telling."""
import os
H=os.path.dirname(os.path.abspath(__file__))
g=[l.rstrip('\n') for l in open(os.path.join(H,'../raster.txt'))]
sil=[l.rstrip('\n') for l in open(os.path.join(H,'../../../silhouet/ronde1.txt'))]
P=lambda x,y: g[y][x] if 0<=x<64 and 0<=y<64 else '.'
ad=sum((g[y][x]!='.')!=(sil[y][x]=='#') for y in range(64) for x in range(64))
print('pixels',sum(c!='.' for r in g for c in r),'alpha-diff',ad)
open_=[(x,y,g[y][x]) for y in range(64) for x in range(64) if g[y][x]!='.' and g[y][x] not in 'KDG'
       and any(P(x+dx,y+dy)=='.' for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
print('open randen',len(open_),open_)
los=[(x,y,g[y][x]) for y in range(64) for x in range(64) if g[y][x]!='.' and
     all(P(x+dx,y+dy)!=g[y][x] for dx,dy in((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)))]
print('losse pixels (geen gelijke buur, 8-buren)',len(los),los)
from collections import Counter
c=Counter(ch for r in g for ch in r if ch!='.'); print(dict(c))
# zwart-aandeel van de rand
rand=[g[y][x] for y in range(64) for x in range(64) if g[y][x]!='.' and any(P(x+dx,y+dy)=='.' for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))]
print('rand zwart-aandeel %.2f'%(rand.count('K')/len(rand)))
