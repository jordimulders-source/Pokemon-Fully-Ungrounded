# Kale reductie: natief model (109x123) -> 56x63 in het 64x64-kader. Geen tekenwerk.
# 1) elke modelpixel krijgt een kleurgroep op toon (zwart, grijs, paars, indigo-poot, geel, oog);
# 2) per spritepixel oppervlakgewogen: figuur als dekking >= 0.5; zwart als zwart >= 50% van de figuur;
#    anders de groep met het meeste gewicht, tint = dichtstbijzijnde paletkleur bij het vlakgemiddelde van die groep.
import numpy as np; from PIL import Image
PAL=[(0,0,0),(16,16,24),(56,56,66),(118,118,132),(164,164,176),(214,214,222),
     (96,56,112),(124,76,136),(168,108,182),(48,44,66),(70,66,100),(118,114,150),
     (168,156,56),(222,212,100),(150,56,196),(240,172,255)]
GI={'k':[2,3,4,5],'p':[6,7,8],'l':[9,10,11],'y':[12,13],'e':[14,15]}
nat=np.asarray(Image.open('natief.png').convert('RGB')).astype(float)
R,G,B=nat[...,0],nat[...,1],nat[...,2]
fg=nat.min(-1)<235
grp=np.full(fg.shape,'.',dtype='<U1')
grp[fg]='k'
grp[fg&(B-G>15)&(R-G<=20)]='l'
grp[fg&(R-G>20)]='p'
grp[fg&(R-G>20)&((B-G>75)|(nat.mean(-1)>180))]='e'
grp[fg&(R-B>40)]='y'
grp[fg&(nat.max(-1)<=30)]='#'
np.save('ngrp.npy',grp)
P=np.array(PAL,float)
yy,xx=np.where(fg); X0,Y0,W,H=xx.min(),yy.min(),xx.max()-xx.min()+1,yy.max()-yy.min()+1
SW,SH=56,63; fx,fy=W/SW,H/SH; OX,OY=4,1
def ov(a0,a1,n):
    w=np.zeros(n)
    for k in range(int(np.floor(a0)),int(np.ceil(a1))):
        if 0<=k<n: w[k]=min(a1,k+1)-max(a0,k)
    return w
out=np.zeros((64,64),int)
for j in range(SH):
    wy=ov(Y0+j*fy,Y0+(j+1)*fy,fg.shape[0])
    for i in range(SW):
        wx=ov(X0+i*fx,X0+(i+1)*fx,fg.shape[1])
        w=np.outer(wy,wx); a=(w*fg).sum()/w.sum()
        if a<0.5: continue
        wf=(w*fg).sum(); wb=(w*(grp=='#')).sum()
        gw={g:(w*(grp==g)).sum() for g in GI}
        g=max(gw,key=gw.get)
        if wb/wf>=0.5 or gw[g]==0: out[OY+j,OX+i]=1; continue
        mw=w*(grp==g); col=(nat*mw[...,None]).sum((0,1))/mw.sum()
        out[OY+j,OX+i]=min(GI[g],key=lambda k:((P[k]-col)**2).sum())
np.savetxt('kaal.txt',out,fmt='%d')
im=Image.new('P',(64,64)); im.putpalette(sum(PAL,())); im.putdata(out.flatten().tolist()); im.save('kaal_v1.png',transparency=0)
print('figuur px',(out>0).sum(),'geo',X0,Y0,fx,fy)
