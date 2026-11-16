# modeltoonkaart.py: gladde modelhelderheid binnen het roze (smooth/sample) en modeltoon per spritepixel.
import numpy as np; from PIL import Image
def gaussian_filter(a,s):
    import numpy as np
    k=int(3*s)+1; x=np.arange(-k,k+1); w=np.exp(-x**2/(2*s*s)); w/=w.sum()
    a=np.apply_along_axis(lambda v: np.convolve(v,w,'same'),0,a)
    return np.apply_along_axis(lambda v: np.convolve(v,w,'same'),1,a)
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pitahaya_draak_fase2/'
nat=np.array(Image.open(B+'sprite_r9/natief.png').convert('RGB')).astype(float)
r,g,b=nat[...,0],nat[...,1],nat[...,2]
L=0.299*r+0.587*g+0.114*b
pink=(r>g+40)&(r>b+10)   # roze vlakken (incl. d), niet groen/zwart/grijs
def smooth(sig):
    m=pink.astype(float); num=gaussian_filter(L*m,sig*3); den=gaussian_filter(m,sig*3)
    return num/np.maximum(den,1e-6)
def sample(S):
    out=np.zeros((64,64)); 
    for sy in range(13,64):
        for sx in range(64):
            ny,nx=3*(sy-13)+1,2+3*sx+1
            if 0<=ny<S.shape[0] and 0<=nx<S.shape[1]: out[sy,sx]=S[ny,nx]
    return out
def modeltoon(sp_im):
    a=np.array(sp_im); pal=np.array(sp_im.getpalette()[:42]).reshape(14,3)
    out=np.zeros((64,64),int)
    fg=nat.min(2)<225
    for y in range(13,64):
        for x in range(64):
            bl=nat[3*(y-13):3*(y-13)+3,2+3*x:5+3*x]; f=fg[3*(y-13):3*(y-13)+3,2+3*x:5+3*x]
            if bl.size==0 or f.sum()<5: continue
            c=bl[f].mean(0); out[y,x]=1+((pal[1:]-c)**2).sum(1).argmin()
    return out
