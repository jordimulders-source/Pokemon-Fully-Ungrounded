# Telt per zone de pixels die afwijken van de kale reductie (kaal2.txt), uitgesplitst naar oorzaak.
import numpy as np
from txt import CH
k=np.loadtxt('kaal2.txt',dtype=int); r=np.loadtxt('mug_r1.idx',dtype=int)
def zone(x,y):
    # naald: band rond de lijn (17,27)-(4,43)
    t=np.clip(((x-17)*(4-17)+(y-27)*(43-27))/((4-17)**2+(43-27)**2),0,1); px,py=17+t*(4-17),27+t*(43-27)
    if y>=27 and ((x-px)**2+(y-py)**2)**.5<=1.8: return 'naald'
    if 12<=x<=31 and 14<=y<=26 and not (x>=21 and y<=16) and not (x>=29 and y<=21): return 'kop/vizier'
    if y<=24 and (x>=30 or (x>=21 and y<=21)): return 'vleugels'
    if x<=26 and 27<=y<=42: return 'voorpoten'
    if 24<=x<=37 and 17<=y<=33: return 'borststuk'
    if x>=36 and 25<=y<=47: return 'achterlijf'
    return 'achterpoten'
from collections import Counter
c=Counter(); tot=Counter()
for y in range(64):
    for x in range(64):
        if k[y,x] or r[y,x]: tot[zone(x,y)]+=1
        if k[y,x]!=r[y,x]: c[zone(x,y)]+=1
for z in ['kop/vizier','naald','voorpoten','borststuk','achterlijf','vleugels','achterpoten']: print(f'{z:12s} {c[z]:3d} van {tot[z]:4d} px ({100*c[z]/max(1,tot[z]):.0f}%)')
print('totaal',sum(c.values()),'van',(r>0).sum(),'figuurpx; silhouet-diff',((k>0)!=(r>0)).sum())
# oorzaak per zone
rep={(int(l.split('(')[1].split(',')[0]),int(l.split(',')[1].split(')')[0])) for l in open('reparaties.txt')}
m=r>0
def rand(y,x): return any(not(0<=y+dy<64 and 0<=x+dx<64) or not m[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
oz=Counter()
for y in range(64):
    for x in range(64):
        if k[y,x]==r[y,x]: continue
        o='reparatie' if (x,y) in rep else ('rand' if rand(y,x) else 'vlekje')
        oz[(zone(x,y),o)]+=1
for z in ['kop/vizier','naald','voorpoten','borststuk','achterlijf','vleugels','achterpoten']:
    print(f'{z:12s}',', '.join(f'{o} {oz[(z,o)]}' for o in ('rand','vlekje','reparatie') if oz[(z,o)]))
