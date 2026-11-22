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
        rc,v=t.split('='); r,c=map(int,rc.split(','))
        if ':' in v:   # r4: alleen toepassen als de basis daar nog het oude (ster/lijn) heeft; r4 tekent die zones al zonder
            v,old=v.split(':')
            if CH[a[r,c]]!=old: continue
        out.append((r,c,CH[a[r,c]],v)); a[r,c]=I[v]
    return out
log={}; a=base.copy()
log['1 sterretjes los']=apply(a,"2,15=. 4,1=. 4,2=. 24,22=. 25,22=. 28,2=. 29,2=. 49,14=. 50,14=.")
log['1 ster op het lijf']=apply(a,"27,14=m:c 27,15=l:c")
log['2 rechterarm']=apply(a,"21,14=l:d 21,15=l:d")
np.save('na12.npy',a)
A=a.copy(); log['3A vlam als bocht']=apply(A,"54,8=m 55,9=l 55,10=l")
# r3: variant B vervalt (Jordi over r2: "A gaat wel de betere kant op, dus b is niet meer nodig")
for k,v in log.items(): print(k,len(v),v)
json.dump(log,open('log_overlay.json','w'))
np.save('sprite_A.npy',A)
