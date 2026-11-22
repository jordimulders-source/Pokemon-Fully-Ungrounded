# Afwijkingen t.o.v. de kale reductie (kaal.npy), per zone, gesplitst in: automatisch ontkorreld / handreparatie basis / bovenlaag
import numpy as np
from txt import CH
k=np.load('kaal.npy'); s0=np.load('schoon0.npy'); b=np.load('basis.npy'); o=np.load('na12.npy')
ZONES={'kegel':(0,10,0,13),'kop':(2,18,12,24),'handjes+top pijl':(10,15,0,12),'linkerarm':(13,22,0,4),'pijl+lijf midden':(15,32,4,16),'lus links':(22,34,0,4),'ring+stomp':(31,37,3,14),'onderkant':(37,50,0,14)}
def zone(r,c):
    for z,(r0,r1,c0,c1) in ZONES.items():
        if r0<=r<r1 and c0<=c<c1: return z
    return 'overig'
for v in 'AB':
    f=np.load(f'sprite_{v}.npy'); print('== variant',v,'totaal afwijkend van kaal:',int((f!=k).sum()))
    tab={}
    for r,c in zip(*np.where(f!=k)):
        z=zone(r,c)
        kind='ontkorrel' if s0[r,c]!=k[r,c] and b[r,c]==s0[r,c] and f[r,c]==b[r,c] else ('basis-hand' if f[r,c]==b[r,c] else 'bovenlaag')
        tab.setdefault(z,{}).setdefault(kind,0); tab[z][kind]+=1
    for z,d in tab.items(): print('  ',z,d)
    nieuw=[(int(r),int(c)) for r,c in zip(*np.where((f>0)&(k==0)))]
    print('  pixels buiten het kale silhouet (nieuw):',nieuw)
    print('  pixels weg uit het kale silhouet:',int(((f==0)&(k>0)).sum()))
