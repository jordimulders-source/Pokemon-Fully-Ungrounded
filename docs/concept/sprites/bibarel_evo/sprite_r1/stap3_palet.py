# Stap 3: kale reductie B (modelkleuren) -> spritepalet per kleurgroep; rand van de figuur wordt omlijning. Niets hertekend.
import numpy as np, sys; sys.path.insert(0,'sprite_r1'); from gemeen import *
L=np.load('sprite_r1/kaal_C_lbl.npy')
idx=np.zeros(L.shape,int)
for k,p in KM2P.items(): idx[L==k]=p
fig=L>=0
P=np.pad(fig,1)
rand=fig&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
idx[rand]=1
opslaan(idx,'sprite_r1/basis.png',8)
print('kleuren',len(set(idx.ravel())))
