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

# --- ronde 1c: diff met 1b per zone en afwijking van het silhouet per zone
b1=[l.rstrip('\n') for l in open(os.path.join(H,'../../ronde1b/raster.txt'))]
ZONES={'1 hand+gloed':(5,45,25,64),'2 kop+maan':(1,26,21,35),'3 spiraal':(48,28,62,37),
       '4 ogen':(4,36,13,39),'4 plooi':(28,39,33,46),'4 dijrand':(42,47,48,52),'4 vuist':(0,13,13,23)}
def zone(x,y):
    for n,(x0,y0,x1,y1) in ZONES.items():
        if x0<=x<x1 and y0<=y<y1: return n
    return 'BUITEN ZONE'
dz=Counter(); oz=Counter(); uit=[]
for y in range(64):
    for x in range(64):
        if g[y][x]!=b1[y][x]: dz[zone(x,y)]+=1
        if (g[y][x]!='.')!=(sil[y][x]=='#'):
            oz[zone(x,y)]+=1; uit.append((x,y,'erbij' if g[y][x]!='.' else 'eraf'))
print('diff met 1b per zone',dict(dz),'totaal',sum(dz.values()))
print('afwijking silhouet per zone',dict(oz),'totaal',sum(oz.values()))
print(uit)
open('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/730fa6d2-b179-5919-a5dc-5a7ead9d8899/scratchpad/sil1c.txt','w').write('\n'.join(''.join('#' if c!='.' else '.' for c in r) for r in g)+'\n')
