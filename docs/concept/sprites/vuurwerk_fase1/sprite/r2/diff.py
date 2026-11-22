# Afwijkingen t.o.v. de kale reductie (kaal.npy) per zone: ontkorrel/kleurregels (clean.py + ontkorrel2), buitenlijnpass, handreparatie, bovenlaag
import numpy as np, json
from txt import CH
k=np.load('kaal.npy'); s0=np.load('schoon0.npy'); b=np.load('basis.npy')
plog=json.load(open('log_patch.json')); hand={(r,c) for z,r,c,o,n in plog if z not in ('ontkorrel2','buitenlijn')}
auto={(r,c) for z,r,c,o,n in plog if z=='ontkorrel2'}; lijn={(r,c) for z,r,c,o,n in plog if z=='buitenlijn'}
ZONES=[('kegel',0,13,0,15),('kop',3,22,13,30),('handjes+top pijl',12,19,0,13),('linkerarm',17,32,0,5),('pijl+lijf midden',19,40,5,20),('lus links',30,40,0,5),('ring+stomp',39,46,4,17),('onderkant',46,62,0,17)]
def zone(r,c):
    for z,r0,r1,c0,c1 in ZONES:
        if r0<=r<r1 and c0<=c<c1: return z
    return 'overig'
for v in 'AB':
    f=np.load(f'sprite_{v}.npy'); tab={}
    for r,c in zip(*np.where(f!=k)):
        r,c=int(r),int(c)
        if f[r,c]!=b[r,c]: kind='bovenlaag'
        elif (r,c) in hand: kind='hand'
        elif (r,c) in lijn: kind='buitenlijn'
        else: kind='kleurregel/ontkorrel'
        tab.setdefault(zone(r,c),{}).setdefault(kind,0); tab[zone(r,c)][kind]+=1
    print('== variant',v,'totaal afwijkend van kaal:',int((f!=k).sum()))
    for z,d in tab.items(): print('  ',z,d)
    print('  nieuw buiten kaal silhouet:',[(int(r),int(c)) for r,c in zip(*np.where((f>0)&(k==0)))])
    print('  weg uit kaal silhouet:',int(((f==0)&(k>0)).sum()))
