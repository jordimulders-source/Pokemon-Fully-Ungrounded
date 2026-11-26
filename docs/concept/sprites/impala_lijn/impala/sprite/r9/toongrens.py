# modeltoongrenzen als punten (sprite-64-coordinaten): grenzen tussen de toonklassen van het model (helderheid <100|135|170|197|226, 5x5 gemiddeld,
# zwarte lijnen <60 eruit), plus het skelet van de zwarte modellijn (curve.npy uit r7/zones/curve.py)
import numpy as np, json
from PIL import Image
km=json.load(open('kaal_meta.json')); x0,y0,p=km['x0'],km['y0'],km['p']
a=np.asarray(Image.open('../referenties/model_r5.png').convert('RGB')).astype(float); L=(a*[.299,.587,.114]).sum(2)
wl=np.load('witlab.npz')['a']; fg=~((wl==-2)|(wl==1))
k=np.ones(5)/5; Ls=np.apply_along_axis(lambda r: np.convolve(r,k,'same'),1,L); Ls=np.apply_along_axis(lambda r: np.convolve(r,k,'same'),0,Ls)
C=np.digitize(Ls,[100,135,170,197,226]); ok=fg&(L>=60)
E=np.zeros_like(ok)
E[:,1:]|=(C[:,1:]!=C[:,:-1])&ok[:,1:]&ok[:,:-1]; E[1:,:]|=(C[1:,:]!=C[:-1,:])&ok[1:,:]&ok[:-1,:]
ys,xs=np.nonzero(E[::2,::2]); OX,OY=10,1
np.save('/tmp/claude-0/s/toon.npy',np.c_[(xs*2+.5-x0)/p+OX,(ys*2+.5-y0)/p+OY])
print(len(xs))
