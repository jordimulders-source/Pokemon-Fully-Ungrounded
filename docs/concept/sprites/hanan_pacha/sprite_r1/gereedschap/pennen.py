# Vingerpennen in het r7-raster, per veer: elke donkere punt (component klasse 2) krijgt een as (PCA); vanaf het binnenste
# eind van de punt loopt de as naar binnen tot de witte band (of de pen ophoudt). Goudpixels binnen PERP van dat stuk as
# = vingerpen; s = afstand vanaf de punt / lengte -> karmijn (s < KS) of oranje. Kaart: 0 niets, 1 oranje, 2 karmijn.
import numpy as np
from scipy import ndimage
MID=(80,80)
def pennen(c,KS=0.58,PERP=2.6,MAXL=40):
    H,W=c.shape; yy,xx=np.mgrid[0:H,0:W]; uit=np.zeros((H,W),int); assen=[]
    lab,n=ndimage.label(c==2,structure=np.ones((3,3)))
    for i in range(1,n+1):
        ys,xs=np.where(lab==i)
        if len(ys)<4 or ys.mean()>100 or 45<xs.mean()<110: continue   # staartpunten en kraag-/kopdonker niet
        P=np.stack([xs,ys],1).astype(float); m=P.mean(0); u,s,vt=np.linalg.svd(P-m); d=vt[0]
        if np.dot(d,np.array(MID)-m)<0: d=-d             # d wijst naar het lijf
        proj=(P-m)@d; start=m+d*proj.max()               # binnenste eind van de punt
        Lf=None; buiten=0
        for st in np.arange(0.5,MAXL,0.5):
            x,y=start+d*st; xi,yi=int(round(x)),int(round(y))
            if not(0<=xi<W and 0<=yi<H): break
            k=c[yi,xi]
            if k==5: Lf=st; break
            if k==0: buiten+=1
            else: buiten=0
            if buiten>3: Lf=st-2; break
        if Lf is None: Lf=MAXL
        v=np.stack([xx-start[0],yy-start[1]],-1); sp=v@d; perp=np.abs(v@np.array([-d[1],d[0]]))
        sel=(c==4)&(sp>=-1)&(sp<=Lf+0.5)&(perp<=PERP)
        t=np.clip(sp/Lf,0,1)
        uit[sel]=np.where(t[sel]<KS,2,1); assen.append((tuple(start.round(1)),tuple(d.round(2)),Lf))
    return uit,assen
if __name__=='__main__':
    import sys; sys.path.insert(0,'gereedschap'); from klassen import klassen; from PIL import Image
    a,c,L=klassen('natief_r7.png'); u,assen=pennen(c)
    for x in assen: print(x)
    kl=np.array([[255,255,255],[0,0,0],[60,50,70],[200,40,60],[230,190,40],[240,240,235],[255,130,0]],'uint8')
    k=c.copy(); k[u==1]=6; k[u==2]=3
    Image.fromarray(kl[k]).resize((800,800),Image.NEAREST).save(sys.argv[1]); print((u==1).sum(),(u==2).sum())
