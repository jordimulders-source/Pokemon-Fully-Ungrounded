# Native pixels -> klassen (dichtstbijzijnde referentiekleur), om tinten te meten.
from PIL import Image; import numpy as np
a=np.asarray(Image.open('natief.png')).astype(int); d=765-a.sum(axis=2)
ref={'lijn':(14,18,46),'ijs_hi':(236,246,248),'ijs_l':(212,232,240),'ijs_m':(165,195,218),'ijs_d':(110,140,172),'ijs_dd':(70,95,130),
'sp_d':(42,40,90),'sp_m':(66,62,118),'nev':(110,92,165),'nev_l':(160,130,214),'waas':(200,200,236),'gas':(228,244,247),
'oog':(110,240,245),'oog_k':(210,255,255),'oog_r':(70,180,200)}
names=list(ref); R=np.array([ref[n] for n in names])
dist=((a[:,:,None,:]-R[None,None])**2).sum(-1); lab=dist.argmin(-1); lab[d<=20]=-1
np.save('lab.npy',lab)
for i,n in enumerate(names):
    m=lab==i
    print(n,m.sum(), a[m].mean(0).astype(int) if m.sum() else '')
