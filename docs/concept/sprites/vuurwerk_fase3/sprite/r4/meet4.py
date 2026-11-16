# r4 stap 1: meting op het model (1024 px, 12x12 modelpx per spritepixel; spritepixel (0,0) = modelpx (106,120)).
# Per spritepixel: dekking (achtergrond = bijna-wit verbonden met de rand), en binnen de dekking het aandeel
# lijn (lum<125, niet roze), roze (R-G>90), en van de creme-pixels mediaan/p15/max helderheid + mediane kleur.
# De mediaan per blok laat de glitter (losse witte stipjes, afwijking 1) grotendeels vallen.
import numpy as np; from PIL import Image
from scipy import ndimage
M=np.asarray(Image.open('../../referenties/model_v14.png').convert('RGB')).astype(float)
lab,_=ndimage.label(M.sum(2)>=735)
rand=set(np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]))-{0}
fg=~np.isin(lab,list(rand)); np.savez_compressed('model_fg.npz',fg=fg)
lum=M@[0.299,0.587,0.114]; pink=(M[...,0]-M[...,1])>90; line=(lum<125)&~pink
K={k:np.zeros((64,64)) for k in ('cov','lijn','roze','med','p15','max')}; MC=np.zeros((64,64,3)); MD=np.zeros((64,64,3))
for j in range(64):
    for i in range(64):
        sl=(slice(120+12*j,132+12*j),slice(106+12*i,118+12*i)); f=fg[sl]
        K['cov'][j,i]=f.mean(); K['lijn'][j,i]=(line[sl]&f).mean(); K['roze'][j,i]=(pink[sl]&f).mean()
        if f.sum()>5:                                   # randkleur: gemiddelde van de donkerste 30% van het blok (selout)
            l=lum[sl][f]; MD[j,i]=M[sl][f][l<=np.percentile(l,30)].mean(0)
        cr=f&~pink[sl]&~line[sl]
        if cr.sum()>5:
            l=lum[sl][cr]; K['med'][j,i]=np.median(l); K['p15'][j,i]=np.percentile(l,15); K['max'][j,i]=l.max(); MC[j,i]=np.median(M[sl][cr],axis=0)
np.savez_compressed('meting.npz',mc=MC,md=MD,**K); print('meting.npz')
