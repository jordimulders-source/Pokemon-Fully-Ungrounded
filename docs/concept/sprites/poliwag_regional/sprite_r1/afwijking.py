# Afwijking r1 t.o.v. de kale reductie (kaal.npy), per zone: (a) pixels met andere index, (b) pixels met ander MATERIAAL dan de modelcel
# (lucht/geel/rood/ijs/donker; omlijning 1 en ijs-selout b/f tellen als de klasse van de buur die ze omlijnen niet mee: zie notities)
import numpy as np
z=np.load('reductie.npz'); cls=z['cls']; kaal=np.load('kaal.npy'); r=np.load('r1.npy')
def mat(v): return {0:0,1:4,2:4,3:4,4:4,5:1,6:1,7:1,8:3,9:3,10:3,11:3,15:3,12:2,13:2,14:2}[int(v)]
M=np.vectorize(mat)(r)
Z={'ver oog':(2,8,7,14),'nabij oog':(13,20,7,14),'mond':(6,13,12,17),'kristal 1':(19,25,0,7),'kristal 2':(24,28,6,10),
   'kristal 3':(29,32,14,19),'schijf+spiraal':(0,19,17,34),'staart':(26,49,13,31),'poten':(2,27,35,40)}
used=np.zeros(r.shape,bool)
rows=[]
for n,(x0,x1,y0,y1) in Z.items():
    m=np.zeros(r.shape,bool); m[y0:y1+1,x0:x1+1]=True; m&=~used; used|=m
    rows.append((n,m))
rows.append(('rest (kop geel, lijf)',~used))
for n,m in rows:
    a=((r!=kaal)&m).sum(); b=((M!=cls)&m).sum(); t=(m&((r>0)|(kaal>0))).sum()
    print('%-22s %4d px, andere index %3d, ander materiaal %3d'%(n,t,a,b))
print('totaal andere index',(r!=kaal).sum(),'ander materiaal',(M!=cls).sum())
