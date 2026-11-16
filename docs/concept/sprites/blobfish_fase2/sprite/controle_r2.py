# Controle r1: afwijkingen van de kale reductie per zone, kleuren, kleine tintvlakjes, randzwart
import json; import numpy as np
o=np.load('r2.npy'); k=np.load('kaal.npy'); P=json.load(open('kaal_palet.json')); LB=np.load('label.npy')
lab=np.full((64,64),-1); lab[17:17+LB.shape[0],1:1+LB.shape[1]]=LB
op=o>0; p=np.pad(op,1); rand=op&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
gez=np.zeros((64,64),bool); gez[27:44,8:36]=True
zones={'buitenlijn':rand,'gezicht (ogen/neus/mond, binnen)':gez&~rand,'lijf overig (binnen)':(lab==0)&op&~gez&~rand,'rode laag (binnen)':(lab==1)&~rand,'bordeaux laag (binnen)':(lab==2)&~rand}
d=o!=k
for n,z in zones.items(): print(f'{n}: {(d&z).sum()} van {z.sum()} px afwijkend')
print('totaal afwijkend',d.sum(),'kleuren gebruikt',len(np.unique(o)),'(incl. transparant)')
print('silhouet gelijk aan kale reductie:',((o>0)==(k>0)).all())
# tintvlakjes < 3 px (niet glans=2, niet zwart=1)
small=[]
for c in np.unique(o):
    if c in (0,1,2): continue
    m=o==c; seen=np.zeros_like(m)
    for y,x in zip(*np.where(m)):
        if seen[y,x]: continue
        st=[(y,x)]; n=0; seen[y,x]=1
        while st:
            a,b=st.pop(); n+=1
            for aa,bb in ((a-1,b),(a+1,b),(a,b-1),(a,b+1)):
                if 0<=aa<64 and 0<=bb<64 and m[aa,bb] and not seen[aa,bb]: seen[aa,bb]=1; st.append((aa,bb))
        if n<3 and not rand[y,x]: small.append((int(c),int(x),int(y),n))
print('tintvlakjes <3 px binnen (excl. glans/zwart):',len(small),small[:20])
ys,xs=np.where(op); print('maat',xs.max()-xs.min()+1,'x',ys.max()-ys.min()+1,'bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max())
