# MAG manen (keuring v2): losse 1-px korrels in de vier manen samenvoegen tot kraters, silhouet + omlijning bevroren.
# Regels (alleen binnenpixels van een maan: alle 8 buren grijs/K, geen transparant en geen lijf):
#  1. losse lichte korrel (geen 8-buur met dezelfde tint, lichter dan de meerderheid) -> meerderheidstint;
#  2. losse donkere korrel (g/G) die een donkere buur (g/G/K) heeft -> g, één krater met die buur; K blijft;
#  3. losse donkere korrel zonder donkere buur -> meerderheidstint.
# Daarna wordt per maan het aantal kraters (samenhangende g-vlekjes binnenin) geteld.
import sys
from collections import Counter
R=[list(l.rstrip('\n')) for l in open(sys.argv[1])][:64]
GR='gGhH'; DONKER='gGK'; L={'g':1,'G':2,'h':3,'H':4,'K':0}
MANEN={'boven':(0,10,24,38),'links':(39,53,0,12),'rechts':(18,33,50,63),'rechtsonder':(48,63,38,57)}
def binnen(y,x,box):
    a,b,c,d=box
    if not(a<=y<=b and c<=x<=d) or R[y][x] not in GR+'K': return False
    nb=[R[y+dy][x+dx] if 0<=y+dy<64 and 0<=x+dx<64 else '.' for dy in(-1,0,1) for dx in(-1,0,1) if dy or dx]
    return all(n in GR+'K' for n in nb)
log=[]
for naam,box in MANEN.items():
    for _ in range(3):
        for y in range(box[0],box[1]+1):
            for x in range(box[2],box[3]+1):
                if not binnen(y,x,box) or R[y][x]=='K': continue   # K binnenin (kraterkern, teenlijn) = model
                c=R[y][x]
                nb=[(y+dy,x+dx) for dy in(-1,0,1) for dx in(-1,0,1) if dy or dx]
                kl=[R[p][q] for p,q in nb]
                if c in kl: continue
                maj=Counter(k for k in kl if k in GR).most_common(1)[0][0]
                if c in DONKER and L[c]<L[maj]:
                    dn=[(p,q) for p,q in nb if R[p][q] in DONKER and binnen(p,q,box)]
                    if dn:
                        if c!='g': log.append(f'{naam}: ({y},{x}) {c}->g krater (sluit aan op donkere buur)'); R[y][x]='g'
                        continue
                log.append(f'{naam}: ({y},{x}) {c}->{maj} korrel'); R[y][x]=maj
open(sys.argv[2],'w').write('\n'.join(''.join(r) for r in R)+'\n')
print('\n'.join(log))
# kraters tellen
for naam,box in MANEN.items():
    seen=set(); n=[]
    for y in range(box[0],box[1]+1):
        for x in range(box[2],box[3]+1):
            if (y,x) in seen or R[y][x]!='g' or not binnen(y,x,box): continue
            st=[(y,x)]; seen.add((y,x)); k=0
            while st:
                p,q=st.pop(); k+=1
                for dy in(-1,0,1):
                    for dx in(-1,0,1):
                        t=(p+dy,q+dx)
                        if t not in seen and 0<=t[0]<64 and 0<=t[1]<64 and R[t[0]][t[1]]=='g' and binnen(*t,box): seen.add(t); st.append(t)
            n.append(k)
    print(naam,'kraters (g-vlekjes binnenin, grootte):',n)
