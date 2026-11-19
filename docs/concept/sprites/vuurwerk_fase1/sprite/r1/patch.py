# Pixelreparaties op schoon0 (= kale reductie + automatisch ontkorrelen), per zone, elk met reden. Uitvoer basis.npy (zonder bovenlaag).
import numpy as np, sys
from txt import CH, dump
I={c:i for i,c in enumerate(CH)}
def P(zone, spec, why):
    # spec: "r,c=X r,c=X ..."
    for t in spec.split():
        rc,v=t.split('='); r,c=map(int,rc.split(',')); PATCH.append((zone,r,c,v,why))
PATCH=[]
exec(open('patches_basis.txt').read())
a=np.load('schoon0.npy').copy()
for z,r,c,v,w in PATCH: a[r,c]=I[v]
np.save('basis.npy',a)
if __name__=='__main__': dump(a)
