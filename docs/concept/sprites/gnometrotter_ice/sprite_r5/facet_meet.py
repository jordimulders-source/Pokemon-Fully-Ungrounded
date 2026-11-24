# facet_meet.py: facetten van romp en benen uit het Ice-model r3 (zoals sprite_r3/meet.py bij Rock: meten, niet tekenen).
# Lijn = lichte barst (lum >= 215, weinig kleur) of donkere lijn (lum < 110), 1 modelpx verdikt; facet = samenhangend
# stuk ertussen, >= 350 modelpx (~5 spritepx). Per spritepixel: facet met de grootste bedekking (>= 15 %), anders -1.
# -> facet_romp.npy, facet_been.npy (64x64, id per spritepixel), facet_lum (gemiddelde modelhelderheid per facet)
import numpy as np, os; from PIL import Image; from scipy import ndimage as nd
H=os.path.dirname(os.path.abspath(__file__))
a=np.asarray(Image.open(os.path.join(H,'../r3/gemini_r3_lijf.png')).convert('RGB')).astype(float); L=a.mean(2); d=a[:,:,0]-a[:,:,2]
P=8.1
def mx(X): return int(round(512+(X-32)*P))
def my(Y): return int(round(523-(60-Y)*P))
def facetten(mat,crackthr,darkthr,box,naam):
    X0,X1,Y0,Y1=box
    crack=(L>=crackthr)&(np.abs(d)<60) if mat=='roze' else (L>=crackthr)
    dark=L<darkthr
    if mat=='roze': kleur=(d>30)
    else: kleur=(a[:,:,2]-a[:,:,0]>30)
    lijn=nd.binary_dilation(crack|dark,iterations=1)
    lab,k=nd.label(kleur&~lijn)
    s=nd.sum(np.ones_like(lab),lab,np.arange(1,k+1))
    F=-np.ones((64,64),int); lums={}
    for Y in range(Y0,Y1):
        for X in range(X0,X1):
            c=lab[my(Y):my(Y+1),mx(X):mx(X+1)].ravel(); c=c[c>0]; c=c[s[c-1]>=350]
            if len(c)==0: continue
            ids,cnt=np.unique(c,return_counts=True); i=ids[cnt.argmax()]
            if cnt.max()>=0.15*P*P: F[Y,X]=i
    for i in np.unique(F[F>=0]): lums[int(i)]=float(L[lab==i].mean())
    np.save(os.path.join(H,naam),F); return F,lums
FR,LR=facetten('roze',215,110,(29,50,19,38),'facet_romp.npy')
# benen: barstdrempel 170 scheidt de facetten; het lichte bovenvlak valt daar weg als 'barst' en komt uit drempel 200
FB,LB=facetten('blauw',170,90,(17,51,40,56),'facet_been.npy')
FB2,LB2=facetten('blauw',200,90,(17,51,40,56),'facet_been200.npy')
licht=(FB<0)&(FB2>=0); FB[licht]=FB2[licht]+100000
for i in np.unique(FB2[licht]): LB[int(i)+100000]=LB2[int(i)]+40   # lichte vlakken: helderheid incl. de lichte delen
np.save(os.path.join(H,'facet_been.npy'),FB); os.remove(os.path.join(H,'facet_been200.npy'))
np.save(os.path.join(H,'facet_lum.npy'),{'romp':LR,'been':LB},allow_pickle=True)
if __name__=='__main__':
    for F,Lm,(x0,x1,y0,y1) in ((FR,LR,(26,52,18,39)),(FB,LB,(15,52,39,57))):
        ids=sorted(Lm); sym={i:'abcdefghijklmnopqrstuvwxyz'[k] for k,i in enumerate(ids)}
        print({sym[i]:(int(Lm[i]),int((F==i).sum())) for i in ids})
        for Y in range(y0,y1): print('%2d '%Y+''.join(sym[F[Y,X]] if F[Y,X]>=0 else '.' for X in range(x0,x1)))
