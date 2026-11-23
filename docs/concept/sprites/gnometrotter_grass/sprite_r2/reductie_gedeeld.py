# reductie_gedeeld.py <model.png> <uit.png> [palet.png]
# GEDEELDE REDUCTIE voor alle Gnometrotter-vormen (Rock, Ice, Grass, Ice-hybride, Grass-hybride): zie GEDEELD.md.
# Elk 1024x559-model met de vaste omtrek (figuur x 274-749, y 41-522) gaat met exact dezelfde geometrie naar 64x64:
#   pitch P = 8,1 modelpx per spritepx (geen natief raster: Gemini-raster te zwak/ongelijk, zie GEDEELD.md)
#   modelrand y = 523 -> spriterand 60 (voeten op rij 59);  model x = 512 -> spriterand x 32
#   spritepixel (X,Y) beslaat model x [512+(X-32)P, 512+(X-31)P), y [523-(60-Y)P, 523-(59-Y)P)
#   in de figuur als >= 50 % van dat vlak geen achtergrond is (achtergrond = min(R,G,B) >= 235)
# Uit: <uit.png> = 64x64 RGBA vlakgemiddelde (kale kleur), en <uit>_kaal.png = geindexeerd: elk vlakgemiddelde -> dichtstbijzijnde
# kleur uit [palet.png] (een 64x64 P-sprite, bv. gnometrotter_rock.png) of anders uit een k-means-palet (15) van het model zelf.
import sys, numpy as np; from PIL import Image
P=8.1; X0M,X0S=512.0,32.0; Y0M,Y0S=523.0,60.0; DREMPEL=0.5
def vlak(X,Y):
    return X0M+(X-X0S)*P, X0M+(X+1-X0S)*P, Y0M-(Y0S-Y)*P, Y0M-(Y0S-Y-1)*P
def bron(X,Y,W=1024,H=559):
    """(u,v,w): modelpixels en hun bedekkingsgewicht voor spritepixel (X,Y)."""
    ua,ub,va,vb=vlak(X,Y)
    for v in range(int(np.floor(va)),int(np.ceil(vb))):
        wy=max(0,min(vb,v+1)-max(va,v))
        if wy<=1e-9 or not 0<=v<H: continue
        for u in range(int(np.floor(ua)),int(np.ceil(ub))):
            wx=max(0,min(ub,u+1)-max(ua,u))
            if wx>1e-9 and 0<=u<W: yield u,v,wx*wy
def reduceer(a):
    """a: HxWx3 model -> (gem 64x64x3, dekking 64x64)."""
    fg=a.min(2)<235; gem=np.zeros((64,64,3)); dek=np.zeros((64,64))
    for Y in range(64):
        for X in range(64):
            acc=np.zeros(3); tw=0; fw=0
            for u,v,w in bron(X,Y,a.shape[1],a.shape[0]):
                tw+=w
                if fg[v,u]: acc+=w*a[v,u]; fw+=w
            if tw: dek[Y,X]=fw/tw
            if fw: gem[Y,X]=acc/fw
    return gem,dek
def kmeans_palet(a,K=15):
    X=a[a.min(2)<235][::5].astype(float); rng=np.random.default_rng(1); C=X[rng.choice(len(X),K,replace=False)]
    for _ in range(40):
        l=((X[:,None]-C[None])**2).sum(2).argmin(1); C=np.array([X[l==k].mean(0) if (l==k).any() else C[k] for k in range(K)])
    return [tuple(int(v) for v in c) for c in C[np.argsort(C.mean(1))]]
if __name__=='__main__':
    a=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
    gem,dek=reduceer(a); m=dek>=DREMPEL
    rgba=np.zeros((64,64,4),'uint8'); rgba[...,:3]=np.round(gem).astype('uint8'); rgba[...,3]=255*m
    Image.fromarray(rgba).save(sys.argv[2])
    if len(sys.argv)>3:
        im=Image.open(sys.argv[3]); pal=[tuple(im.getpalette()[i*3:i*3+3]) for i in range(16)]
    else: pal=[(152,208,160)]+kmeans_palet(a)
    Pp=np.array(pal[1:],float); o=np.zeros((64,64),int)
    for Y,X in zip(*np.where(m)): o[Y,X]=1+np.argmin(((Pp-gem[Y,X])**2).sum(1))
    p=Image.fromarray(o.astype('uint8'),'P'); f=[v for c in pal for v in c]; p.putpalette(f+[0]*(768-len(f)))
    uit=sys.argv[2][:-4]+'_kaal.png'; p.save(uit,transparency=0)
    yy,xx=np.where(m); print('figuur x%d-%d y%d-%d, %d px ->'%(xx.min(),xx.max(),yy.min(),yy.max(),m.sum()),sys.argv[2],uit)
