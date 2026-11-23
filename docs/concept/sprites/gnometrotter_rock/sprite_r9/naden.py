# naden.py: modelnaden (donkere lijnen) skeletoniseren en per spritepixel tellen -> naad.npy (aantal skeletpixels)
import numpy as np; from PIL import Image
from skimage.morphology import skeletonize
m=np.array(Image.open('../r8/gemini_r8.png').convert('RGB')).astype(float); L=m.mean(2)
P=8.1
G=[l.rstrip('\n') for l in open('grid.txt') if l.strip()]
fam=lambda c: 'P' if c in '678F' else 'B' if c in '9ABC' else 'W' if c in 'DE' else 'S' if c!='.' else None
T={'P':100,'B':80,'S':55,'W':95}
H,W=L.shape
# drempel per modelpixel volgens de familie van de spritepixel waar hij in valt
sx=np.floor((np.arange(W)-512)/P+32).astype(int); sy=np.floor((np.arange(H)-523)/P+60).astype(int)
thr=np.zeros((H,W)); inn=np.zeros((H,W),bool)
for y in range(H):
    j=sy[y]
    if not 0<=j<64: continue
    for x in range(W):
        i=sx[x]
        if not 0<=i<64: continue
        f=fam(G[j][i])
        if f: thr[y,x]=T[f]; inn[y,x]=True
lijn=(L<thr)&inn
sk=skeletonize(lijn)
N=np.zeros((64,64),int)
ys,xs=np.nonzero(sk)
for y,x in zip(ys,xs): N[sy[y],sx[x]]+=1
np.save('naad.npy',N); np.save('model_skelet.npy',sk)
print('ok',N.max())
