# Facetkaart uit het model: elke natieve modelpixel -> bruinklasse (S/M/L, donkerste modelbruin telt als S),
# per spritepixel de MEERDERHEID (geen gemiddelde) -> harde, hoekige facetgrenzen zoals de gehakte steen van het model.
import sys, numpy as np
from PIL import Image
sys.path.insert(0,'../r2')
from reduceer import fig, X0,X1,Y0,Y1, wts, W, H
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float)
BRC=np.array([(99,62,57),(148,99,86),(186,141,126)],float)
lum=n@[0.299,0.587,0.114]; r,g,b=n[...,0],n[...,1],n[...,2]
brown=fig&(lum>48)&~((b>r-30)&(b>g+8))&~((r>200)&(g>185))&~(n.min(axis=2)>200)
cls=np.argmin(((n[:,:,None]-BRC[None,None])**2).sum(3),2)
tw,th=50,45
Wx=wts(X0,X1,tw)[:, :W]; Wy=wts(Y0,Y1,th)[:, :H]
Wx=np.pad(Wx,((0,0),(0,W-Wx.shape[1]))); Wy=np.pad(Wy,((0,0),(0,H-Wy.shape[1])))
votes=np.stack([Wy@((cls==k)&brown).astype(float)@Wx.T for k in range(3)],2)
tot=votes.sum(2); fac=np.where(tot>0.15, votes.argmax(2)+3, 0)   # 3=S 4=M 5=L, 0 = geen bruin in het model
np.save('facet.npy',fac)
print('facet px',(fac>0).sum())
