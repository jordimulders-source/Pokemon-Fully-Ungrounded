# Stap 1: masker van het bevroren model v3.
# (a) ruwe achtergrond via flood fill vanaf de rand; (b) lokale achtergrondschatting daaruit
# (genormaliseerde vervaging); (c) figuur = duidelijk afwijkend van die lokale achtergrond.
import sys, numpy as np
from collections import deque
from PIL import Image, ImageFilter
from scipy import ndimage as nd
SRC='../referenties/model_gemini_pose_v3.png'
T=float(sys.argv[1]) if len(sys.argv)>1 else 6
im=Image.open(SRC).convert('RGB')
a=np.asarray(im.filter(ImageFilter.MedianFilter(3))).astype(float)
H,W,_=a.shape; lum=a.mean(2); sat=a.max(2)-a.min(2)
ok=(lum>=226)&(sat<=8)
bg=np.zeros((H,W),bool); q=deque([(y,x) for x in range(W) for y in (0,H-1)]+[(y,x) for y in range(H) for x in (0,W-1)])
while q:
    y,x=q.popleft()
    if bg[y,x] or not ok[y,x]: continue
    bg[y,x]=True
    for ny,nx in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
        if 0<=ny<H and 0<=nx<W and not bg[ny,nx] and ok[ny,nx] and abs(lum[ny,nx]-lum[y,x])<4: q.append((ny,nx))
zeker=nd.binary_erosion(bg,iterations=6)
s=12
bgest=nd.gaussian_filter(lum*zeker,s)/np.maximum(nd.gaussian_filter(zeker.astype(float),s),1e-6)
d=lum-bgest
fig=(np.abs(d)>T)|(sat>14)|~bg
fig=nd.binary_opening(fig,iterations=1)
lab,n=nd.label(fig); sz=nd.sum(fig,lab,range(1,n+1)); fig=np.isin(lab,1+np.nonzero(sz>1500)[0])
fig[997:]=False   # grondschaduw onder de hand
fig=nd.binary_fill_holes(fig)
Image.fromarray((fig*255).astype('uint8')).save('masker_groot.png')
ys,xs=np.nonzero(fig); print('bbox',xs.min(),ys.min(),xs.max(),ys.max())
