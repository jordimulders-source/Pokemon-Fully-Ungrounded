# modelhelderheid per spritepixel (poedelmot px.py-aanpak): gemiddelde, p15 en max van de luminantie van de modelpixels in elke spritecel
import numpy as np; from PIL import Image
R='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/capykart/'
def meet(H=62,W=62):
    a=np.asarray(Image.open(R+'referenties/model_r5.png').convert('RGB')).astype(float)
    lum=a@[0.299,0.587,0.114]; fg=a.min(2)<225
    x0,p=133,12.064516129032258; y0=860-H*p
    gem=np.full((H,W),np.nan); p15=gem.copy(); mx=gem.copy()
    for y in range(H):
        for x in range(W):
            b=lum[int(round(y0+y*p)):int(round(y0+(y+1)*p)),int(round(x0+x*p)):int(round(x0+(x+1)*p))]
            f=fg[int(round(y0+y*p)):int(round(y0+(y+1)*p)),int(round(x0+x*p)):int(round(x0+(x+1)*p))]
            if f.sum()==0: continue
            v=b[f]; gem[y,x]=v.mean(); p15[y,x]=np.percentile(v,15); mx[y,x]=v.max()
    return gem,p15,mx
if __name__=='__main__':
    g,_,_=meet(); np.save(R+'sprite/model_lum.npy',g)
    print(np.nanpercentile(g,[5,25,50,75,95]))
