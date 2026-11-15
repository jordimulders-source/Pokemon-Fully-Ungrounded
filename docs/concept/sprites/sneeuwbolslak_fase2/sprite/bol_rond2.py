# Na r3: bovenkant van de bol was 8+ px recht (oude bovenrand van het model bleef staan). Jordi: "dat moet echt een bol blijven",
# "beide zijkanten hebben echt te lange rechte lijnen". Cirkel r 10.7 rond (31.5, 30.5): rechte stukken boven en opzij max 4 px.
# Alleen de ijspunten uit het model blijven buiten de cirkel (links x<=27,y<=23; midden x 28,y 20; rechts x>=39,y<=24). Uit: sprite/sil56_rond.npy (overschreven; oud: sil56_rond_v1.npy)
import numpy as np, shutil, os
if not os.path.exists('sprite/sil56_rond_v1.npy'): shutil.copy('sprite/sil56_rond.npy','sprite/sil56_rond_v1.npy')
M=np.load('sprite/sil56.npy'); O=np.load('sprite/sil56_rond_v1.npy'); yy,xx=np.mgrid[0:64,0:64]
C=((xx-31.5)**2+(yy-30.5)**2)<=10.7**2
sp=M&~C&(((xx<=27)&(yy<=23))|((xx==28)&(yy==20))|((xx>=39)&(yy<=24)))
Z=(xx>=19)&(xx<=44)&(yy>=18)&(yy<=35)&~((yy==35)&(xx>=40))
N=O.copy(); N[Z]=(C|sp)[Z]
np.save('sprite/sil56_rond.npy',N)
for y in range(18,37): print('%2d '%y+''.join('#' if N[y,x] else '.' for x in range(16,48)))
