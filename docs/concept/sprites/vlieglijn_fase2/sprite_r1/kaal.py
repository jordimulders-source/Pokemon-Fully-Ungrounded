# Kale reductie: natief model (109x123) -> 56x63, vlakgemiddelde per kleurgroep + dichtstbijzijnde paletkleur.
# Geen tekenwerk. Uitvoer: kaal.txt (indexraster 64x64), kaal.png, nclass.npy (natieve klassekaart).
import numpy as np; from PIL import Image
PAL=[(0,0,0),(16,16,24),(56,56,66),(118,118,132),(164,164,176),(214,214,222),
     (84,52,104),(126,76,140),(170,106,186),(52,48,76),(82,74,114),(126,122,166),
     (164,148,56),(228,216,96),(150,56,196),(240,170,255)]
GRP={1:'k',2:'k',3:'g',4:'g',5:'g',6:'p',7:'p',8:'p',9:'l',10:'l',11:'l',12:'y',13:'y',14:'e',15:'e'}
nat=np.asarray(Image.open('natief.png').convert('RGB')).astype(float)
fg=nat.min(-1)<235
P=np.array(PAL,float)
# model-kleuren: bevroren naar het palet (dichtstbijzijnde, hue-gewogen)
def nearest(c):
    d=((P[1:]-c)**2*np.array([1.0,1.2,1.0])).sum(1); return 1+int(d.argmin())
ncl=np.zeros(fg.shape,int)
for y,x in zip(*np.where(fg)): ncl[y,x]=nearest(nat[y,x])
np.save('nclass.npy',ncl)
yy,xx=np.where(fg); X0,Y0,W,H=xx.min(),yy.min(),xx.max()-xx.min()+1,yy.max()-yy.min()+1
SW,SH=56,63; fx,fy=W/SW,H/SH; OX,OY=4,1
def ov(a0,a1,n):  # gewichten per natieve cel voor interval [a0,a1)
    w=np.zeros(n); 
    for k in range(int(np.floor(a0)),int(np.ceil(a1))):
        if 0<=k<n: w[k]=min(a1,k+1)-max(a0,k)
    return w
out=np.zeros((64,64),int); cov=np.zeros((64,64)); kcov=np.zeros((64,64))
for j in range(SH):
    wy=ov(Y0+j*fy,Y0+(j+1)*fy,fg.shape[0])
    for i in range(SW):
        wx=ov(X0+i*fx,X0+(i+1)*fx,fg.shape[1])
        w=np.outer(wy,wx); tot=w.sum(); a=(w*fg).sum()/tot
        cov[OY+j,OX+i]=a
        if a<0.5: continue
        cl=ncl; wb=(w*((cl==1))).sum(); wf=(w*fg).sum()
        kcov[OY+j,OX+i]=wb/wf
        # groep met het meeste gewicht (zonder zwart)
        gw={}
        for idx in range(2,16):
            s=(w*(cl==idx)).sum()
            if s>0: gw[GRP[idx]]=gw.get(GRP[idx],0)+s
        if wb/wf>=0.5 or not gw: out[OY+j,OX+i]=1; continue
        g=max(gw,key=gw.get)
        m=np.isin(cl,[k for k in GRP if GRP[k]==g]) 
        if g=='k': m=(cl==2)
        mw=w*m; col=(nat*mw[...,None]).sum((0,1))/mw.sum()
        cands=[k for k in GRP if GRP[k]==g] if g!='k' else [2]
        out[OY+j,OX+i]=min(cands,key=lambda k:((P[k]-col)**2).sum())
np.savetxt('kaal.txt',out,fmt='%d'); np.save('cov.npy',cov); np.save('kcov.npy',kcov)
im=Image.new('P',(64,64)); im.putpalette(sum(PAL,())); im.putdata(out.flatten().tolist()); im.save('kaal.png',transparency=0)
print('figuur px',(out>0).sum())
