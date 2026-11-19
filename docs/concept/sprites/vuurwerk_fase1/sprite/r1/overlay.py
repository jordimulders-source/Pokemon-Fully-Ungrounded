# Bovenlaag met Jordi's toegestane afwijkingen, als laatste stap op basis.npy:
# 1) losse sterretjes weg; 2) rechterarm: lijn tussen arm en lijf uitgummen (Jordi's witte lijn); 3) lijf verbinden (A/B).
import numpy as np
from txt import CH, dump
from reduce2 import save
I={c:i for i,c in enumerate(CH)}
base=np.load('basis.npy')
def apply(a,spec):
    out=[]
    for t in spec.split():
        rc,v=t.split('='); r,c=map(int,rc.split(',')); out.append((r,c,CH[a[r,c]],v)); a[r,c]=I[v]
    return out
log={}
a=base.copy()
log['1 sterretjes']=apply(a,"2,12=. 2,13=. 3,1=. 19,18=. 20,18=. 23,2=. 40,11=.")
log['2 rechterarm']=apply(a,"16,11=l 17,12=l 18,13=l")
np.save('na12.npy',a)
A=a.copy(); log['3A vlam als bocht']=apply(A,"43,7=m 44,7=m 44,8=l")
B=a.copy(); log['3B compacte bocht']=apply(B,"43,7=m 44,7=m 44,8=l 44,9=l 45,5=. 45,6=# 45,7=# 45,8=# 45,9=# 45,10=. 44,10=# 46,6=. 46,7=. 46,8=. 46,9=. 46,10=. 47,6=. 47,7=. 47,8=. 47,9=. 48,7=. 48,8=. 49,8=.")
for k,v in log.items(): print(k,len(v),v)
np.save('sprite_A.npy',A); np.save('sprite_B.npy',B)
save(A,'sprite_A.png'); save(B,'sprite_B.png')
