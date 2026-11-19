# Bovenlaag (laatste stap) met Jordi's toegestane afwijkingen op basis.npy:
# 1) sterretjes weg (losse + de ster midden op het lijf); 2) rechterarm: Jordi's lijn uitgummen; 3) lijf verbinden A/B.
import numpy as np, json
from txt import CH
from reduce2 import save
I={c:i for i,c in enumerate(CH)}
base=np.load('basis.npy')
def apply(a,spec):
    out=[]
    for t in spec.split():
        rc,v=t.split('='); r,c=map(int,rc.split(',')); out.append((r,c,CH[a[r,c]],v)); a[r,c]=I[v]
    return out
log={}; a=base.copy()
log['1 sterretjes los']=apply(a,"2,15=. 4,1=. 4,2=. 24,22=. 25,22=. 28,2=. 29,2=. 49,14=. 50,14=.")
log['1 ster op het lijf']=apply(a,"27,14=m 27,15=l")
log['2 rechterarm']=apply(a,"21,14=l 21,15=l")
np.save('na12.npy',a)
A=a.copy(); log['3A vlam als bocht']=apply(A,"54,8=m 55,9=l 55,10=l")
B=a.copy(); log['3B compacte bocht']=apply(B,"54,8=m 55,9=l 55,10=l 56,6=. 56,7=. 56,8=# 56,9=# 56,10=# 56,11=# 56,12=. "
  "57,6=. 57,7=. 57,8=. 57,9=. 57,10=. 57,11=. 57,12=. 58,8=. 58,9=. 58,10=. 58,11=. 58,12=. 59,8=. 59,9=. 59,10=. 59,11=. 60,8=. 60,9=. 60,10=. 61,9=. 61,10=.")
for k,v in log.items(): print(k,len(v),v)
json.dump(log,open('log_overlay.json','w'))
np.save('sprite_A.npy',A); np.save('sprite_B.npy',B)
