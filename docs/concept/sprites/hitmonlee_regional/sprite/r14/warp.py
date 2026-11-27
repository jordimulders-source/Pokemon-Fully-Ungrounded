# Gladde warp ek2 -> natief: de geschrapte rijen/kolommen (onderlaag.py) als gladde, monotone afbeelding
# i.p.v. sprongen; daarmee het natieve masker oppervlakgewogen bemonsteren op de ek2-plekken.
from PIL import Image; import numpy as np
from scipy import ndimage
D='docs/concept/sprites/hitmonlee_regional/'
a=np.asarray(Image.open(D+'sprite/natief.png').convert('RGB')).astype(float)
lab,n=ndimage.label(a.min(2)>=226)
rand=set(lab[0])|set(lab[-1])|set(lab[:,0])|set(lab[:,-1]); rand.discard(0)
fig=~np.isin(lab,list(rand))
rows=[4,8,13,17,22,28,45,55,64,70]; cols=[1,5,16,37,42,50,56,60,65]
kr=np.array([i for i in range(74) if i not in rows]); kc=np.array([i for i in range(68) if i not in cols])
def glad(k,sig):
    # randen = pixelgrenzen: positie van grens i (0..n) in 2x-coord
    g=np.concatenate([[k[0]],(k[:-1]+k[1:]+1)/2.0,[k[-1]+1]]).astype(float)
    pad=np.pad(g,8,mode='reflect',reflect_type='odd')
    return ndimage.gaussian_filter1d(pad,sig)[8:-8]
def maak(sig):
    gy=glad(kr,sig); gx=glad(kc,sig)
    k=6
    C=np.zeros((64,64))
    for y in range(64):
        ys=np.interp(y+(np.arange(k)+.5)/k,np.arange(65),gy)*2
        for x in range(59):
            xs=np.interp(x+(np.arange(k)+.5)/k,np.arange(60),gx)*2
            yy=np.clip(ys.astype(int),0,fig.shape[0]-1); xx=np.clip(xs.astype(int),0,fig.shape[1]-1)
            C[y,x+2]=fig[np.ix_(yy,xx)].mean()
    return C,gy,gx
if __name__=='__main__':
    import sys
    sig=float(sys.argv[1]) if len(sys.argv)>1 else 3
    C,gy,gx=maak(sig); np.save(D+'sprite/r14/covw.npy',C)
    e=np.array(Image.open(D+'eindkeuring/ek2.png')); M=C>=0.5; E=e>0
    for y in range(64):
        print('%2d '%y+''.join('#' if M[y,x] and E[y,x] else ('+' if M[y,x] else ('-' if E[y,x] else '.')) for x in range(64)))
    print((M&~E).sum(),(E&~M).sum())
