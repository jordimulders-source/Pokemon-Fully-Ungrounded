# Onderlaag v2 (omlijningsbewust), nog steeds alleen uit het model berekend:
#  vulling  = spritecellen met model-vulling (figuur zonder zwart) >= FT; kleur = groep met meeste gewicht, tint bij vlakgemiddelde
#             binnenlijn zwart als zwart >= 50% van de cel
#  omlijning= cellen buiten de vulling, 4-buur van de vulling, met modelfiguur >= RT  (de modellijn als 1-px-ring)
import numpy as np,sys; from PIL import Image
from kaal_pal import PAL
FT=float(sys.argv[1]) if len(sys.argv)>1 else 0.35; RT=float(sys.argv[2]) if len(sys.argv)>2 else 0.15
GI={'k':[2,3,4,5],'p':[6,7,8],'l':[9,10,11],'y':[12,13],'e':[14,15]}
nat=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); grp=np.load('ngrp.npy')
fg=grp!='.'; blk=grp=='#'
P=np.array(PAL,float); X0,Y0,fx,fy,OX,OY=21,12,109/56,123/63,4,1
def ov(a0,a1,n):
    w=np.zeros(n)
    for k in range(int(np.floor(a0)),int(np.ceil(a1))):
        if 0<=k<n: w[k]=min(a1,k+1)-max(a0,k)
    return w
cf=np.zeros((64,64)); cb=np.zeros((64,64)); col=np.zeros((64,64),int)
for j in range(64):
    wy=ov(Y0+(j-OY)*fy,Y0+(j-OY+1)*fy,fg.shape[0])
    for i in range(64):
        wx=ov(X0+(i-OX)*fx,X0+(i-OX+1)*fx,fg.shape[1]); w=np.outer(wy,wx); t=w.sum()
        if t==0: continue
        cf[j,i]=(w*fg).sum()/t; cb[j,i]=(w*blk).sum()/t
        gw={g:(w*(grp==g)).sum() for g in GI}; g=max(gw,key=gw.get)
        if gw[g]==0: continue
        mw=w*(grp==g); c=(nat*mw[...,None]).sum((0,1))/mw.sum()
        col[j,i]=min(GI[g],key=lambda k:((P[k]-c)**2).sum())
F=(cf-cb)>=FT
out=np.zeros((64,64),int)
out[F]=col[F]
out[F&(cb>=0.5*np.maximum(cf,1e-9))]=1
for j in range(64):
    for i in range(64):
        if F[j,i] or cf[j,i]<RT: continue
        if any(0<=v<64 and 0<=u<64 and F[v,u] for v,u in ((j-1,i),(j+1,i),(j,i-1),(j,i+1))): out[j,i]=1
out[(~F)&(cf>=0.5)]=1
np.save('cf.npy',cf); np.save('cb.npy',cb); np.save('col.npy',col)
np.savetxt('kaal2.txt',out,fmt='%d')
ys,xs=np.where(out>0); print('bbox',xs.min(),xs.max(),ys.min(),ys.max(),'px',(out>0).sum())
