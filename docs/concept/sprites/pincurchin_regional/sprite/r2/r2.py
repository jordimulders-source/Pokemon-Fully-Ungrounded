# r2: alleen de keurreparaties (BIJNA) op r1. Coördinaten (x,y). Waarden: K0 D(br5)1 s(br8)2 m(br1)3 l(br4)4 r(r7)5 R6 L7
import numpy as np
from toon import save
K,D,S,M,Lb,r=0,1,2,3,4,5
A=np.load('../r1/A.npy').copy(); B=np.load('../r1/B.npy').copy()
REP={}
# 1. staafje linksboven: NO-rand r7, ZW-rand zwart (model)
for p in [(11,18),(12,19),(13,20),(14,21),(15,22),(16,23),(17,24),(18,25)]: REP[p]=r
for p in [(10,18),(9,19),(9,20),(10,21),(10,22),(11,23),(12,24),(13,25),(14,26),(14,27)]: REP[p]=K
# 2. zwart aan de lichte linkerkant van staafjes -> r7
for p in [(19,19),(20,24),(21,27),(21,28),(26,18),(27,23)]: REP[p]=r
# 4. lichte vlekjes schaduwkant -> modeltint
REP.update({(45,43):S,(46,43):D,(43,44):M,(36,46):M,(37,46):D,(32,47):S,(33,47):S,(34,47):S})
# 5. onderrand 1 px
for x in range(28,34): REP[(x,54)]=S
ZONE=set(REP)
for (x,y),v in REP.items(): A[y,x]=v; B[y,x]=v
# 3. alleen A: naad dicht bij x=17
for p in [(17,45),(17,46)]: A[p[1],p[0]]=D; ZONE.add(p)
np.save('A.npy',A); np.save('B.npy',B); save(A,'A.png'); save(B,'B.png')
# bewijs
A1=np.load('../r1/A.npy'); B1=np.load('../r1/B.npy')
z=np.zeros((64,64),bool)
for x,y in ZONE: z[y,x]=True
print('A: gewijzigd',(A!=A1).sum(),'buiten zones',((A!=A1)&~z).sum())
print('B: gewijzigd',(B!=B1).sum(),'buiten zones',((B!=B1)&~z).sum())
mond=np.zeros((64,64),bool); mond[41:50,17:28]=True
print('A vs B buiten mondvak',((A!=B)&~mond).sum(),'| B-mond ongewijzigd',(B[mond]==B1[mond]).all())
print('silhouet gelijk aan r1',((A>=0)==(A1>=0)).all() and ((B>=0)==(B1>=0)).all())
